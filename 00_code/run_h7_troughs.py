"""H7 — Did harvest-season price TROUGHS deepen after the ban?

Hypothesis (spec.md): with futures suspended there is no forward/storage signal to
smooth seasonal gluts, so harvest-time price troughs deepen post-ban (distress sales).
chana is the headline commodity (wheat is procurement-dominated -> MSP-flagged).

WHAT THIS SCRIPT CAN DO (price-only):
  - monthly seasonal price indices per commodity, estimated SEPARATELY pre vs post ban,
  - a deseasonalised TROUGH-DEPTH metric (how far below the local trend price falls in
    the seasonal low), pre vs post,
  - banned-vs-control difference-in-differences on trough depth.

WHAT IS BLOCKED (note honestly, do NOT fabricate):
  - arrivals / quantity data are NOT in our dataset, so the "share of crop sold within
    X weeks of harvest" (arrivals-concentration) leg of the spec.md method CANNOT be
    computed. We can only observe the PRICE shadow of a glut, not the quantity.
  - MSP procurement quantities are likewise unavailable as a control; wheat/paddy spot
    is MSP-administered so its trough is a policy artifact, flagged not interpreted.

INPUT : 02_data/clean/spot_daily_<c>.csv  (date, price)  national modal, weekday-clean
OUTPUT: 04_empirics/H7_harvest_troughs/output/
          h7_seasonal_index.csv     month x commodity x (pre/post) multiplicative index
          h7_trough_depth.csv       per commodity-year trough depth (deseasonalised)
          h7_summary.csv            per-commodity pre/post trough depth + change
          h7_did.csv                banned-vs-control DiD on trough depth
          h7_seasonal_<c>.png       seasonal index pre vs post (key commodities)
        plus 04_empirics/H7_harvest_troughs/h7_findings.md (memo)
"""
from pathlib import Path
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from utils import BAN_DATE

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "02_data" / "clean"
OUTDIR = ROOT / "04_empirics" / "H7_harvest_troughs" / "output"
MEMO = ROOT / "04_empirics" / "H7_harvest_troughs" / "h7_findings.md"

# ---- commodity sets (per DATA REALITY brief) -------------------------------------
# banned: paddy dropped (MSP-censored), wheat kept but FLAGGED (procurement-dominated).
BANNED_HEADLINE = ["chana", "mustard", "soybean", "moong"]   # clean banned set
BANNED_FLAGGED = ["wheat"]                                    # MSP/procurement-flagged
# controls: still-traded futures commodities + non-banned food/oilseed donors.
CONTROL = ["castor", "guarseed413", "jeera", "turmeric", "cotton"]
DONOR = ["barley", "maize", "jowar", "bajra", "ragi", "groundnut", "sesamum", "sunflower"]

BANNED_ALL = BANNED_HEADLINE + BANNED_FLAGGED
ALL = BANNED_ALL + CONTROL + DONOR

# Indian harvest months (rough, mandi-arrival peak) — used to LABEL the expected trough,
# not to define it; the trough is found empirically as the seasonal-index minimum.
HARVEST_MONTHS = {
    "chana": [3, 4],        # rabi, Mar-Apr
    "mustard": [3, 4],      # rabi, Mar-Apr
    "wheat": [4, 5],        # rabi, Apr-May
    "barley": [4, 5],
    "soybean": [10, 11],    # kharif, Oct-Nov
    "moong": [10, 11],      # kharif (+summer Jun)
    "maize": [10, 11],
    "jowar": [11, 12],
    "bajra": [10, 11],
    "ragi": [11, 12],
    "groundnut": [11, 12],
    "sesamum": [10, 11],
    "sunflower": [3, 4],
    "castor": [2, 3],
    "guarseed413": [10, 11],
    "jeera": [3, 4],
    "turmeric": [2, 3],
    "cotton": [11, 12],
}

BAN_MONTH = BAN_DATE.to_period("M")   # 2021-12


def load_monthly(c):
    f = CLEAN / f"spot_daily_{c}.csv"
    if not f.exists():
        return None
    df = pd.read_csv(f, parse_dates=["date"])
    df = df.dropna(subset=["price"])
    df = df[df.price > 0]
    df["ym"] = df.date.dt.to_period("M")
    mo = df.groupby("ym").price.mean().rename("price").to_frame()
    mo["month"] = mo.index.month
    mo["year"] = mo.index.year
    mo["post"] = (mo.index >= BAN_MONTH).astype(int)
    return mo


def ratio_to_ma_index(mo):
    """Classical multiplicative seasonal index via ratio-to-12mo-centered-moving-average.

    Returns a 12-vector (month 1..12) of seasonal factors, normalised to mean 1.0.
    Robust to the price LEVEL trend (the centered MA removes trend+cycle); the residual
    ratio is the seasonal+irregular, averaged by calendar month -> seasonal factor.
    Uses median across years for the calendar-month average (outlier-robust).
    """
    s = mo["price"].astype(float)
    if s.shape[0] < 18:               # need >~1.5yr for a 12mo centered MA
        return None
    # centered 12-month MA: 2x12 = average of two consecutive 12-term means
    ma = s.rolling(12, center=True).mean()
    ma2 = ma.rolling(2).mean().shift(-0)   # already centered-ish; refine with 2x12
    # proper 2x12: weights 1/24 at ends, 1/12 interior
    w = np.array([1] + [2] * 11 + [1]) / 24.0
    vals = s.values
    cma = np.full(len(vals), np.nan)
    for i in range(6, len(vals) - 6):
        cma[i] = np.dot(w, vals[i - 6:i + 7])
    cma = pd.Series(cma, index=s.index)
    ratio = s / cma
    tmp = pd.DataFrame({"month": s.index.month, "ratio": ratio.values}).dropna()
    if tmp.empty:
        return None
    si = tmp.groupby("month").ratio.median()
    si = si.reindex(range(1, 13))
    # interpolate any missing month, then normalise to mean 1
    si = si.interpolate().bfill().ffill()
    si = si / si.mean()
    return si


def trough_depth_per_year(mo):
    """Deseasonalised trough depth per CALENDAR year.

    For each year: trough_depth = 1 - (min monthly price / local-trend price at that month),
    where local trend = centered 12-mo MA (so we measure how far the annual LOW dips below
    the smooth trend, net of the price level/trend). Higher = deeper trough.
    Requires a full-ish year of months and a defined trend.
    """
    s = mo["price"].astype(float)
    vals = s.values
    w = np.array([1] + [2] * 11 + [1]) / 24.0
    cma = np.full(len(vals), np.nan)
    for i in range(6, len(vals) - 6):
        cma[i] = np.dot(w, vals[i - 6:i + 7])
    cma = pd.Series(cma, index=s.index)
    dev = s / cma - 1.0          # fractional deviation from trend; trough = most negative
    out = []
    for yr, g in pd.DataFrame({"dev": dev, "month": s.index.month,
                               "year": s.index.year}).dropna().groupby("year"):
        if g.shape[0] < 8:        # need most of the year with a defined trend
            continue
        trough_month = int(g.loc[g.dev.idxmin(), "month"])
        depth = float(-g.dev.min())       # depth>0 means price dipped below trend
        out.append({"year": int(yr), "trough_month": trough_month, "depth": depth})
    return pd.DataFrame(out)


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)

    seas_rows = []        # long: commodity, month, regime, index
    summary_rows = []     # commodity, pre/post mean trough depth + change
    depth_long = []       # commodity, year, depth, post (for DiD)
    spans = {}

    for c in ALL:
        mo = load_monthly(c)
        if mo is None:
            print(f"[skip] {c}: no file")
            continue
        spans[c] = (str(mo.index.min()), str(mo.index.max()), len(mo))

        # --- seasonal index, estimated separately pre and post ban ---
        for regime, sub in [("pre", mo[mo.post == 0]), ("post", mo[mo.post == 1]),
                            ("full", mo)]:
            si = ratio_to_ma_index(sub)
            if si is None:
                continue
            for m in range(1, 13):
                seas_rows.append({"commodity": c, "regime": regime, "month": m,
                                  "seas_index": round(float(si.loc[m]), 4)})

        # --- trough depth per year, then average pre vs post ---
        td = trough_depth_per_year(mo)
        if td.empty:
            continue
        td["commodity"] = c
        td["post"] = (td.year >= 2022).astype(int)   # 2022 = first full post-ban crop yr
        # 2021 straddles the ban (Dec) -> assign to PRE for trough purposes (its harvest
        # troughs for chana/mustard Mar-Apr 2021 are pre-ban). Keep simple: post = year>=2022.
        for _, r in td.iterrows():
            depth_long.append({"commodity": c, "year": int(r.year),
                               "trough_month": int(r.trough_month),
                               "depth": float(r.depth), "post": int(r.post)})

        pre_d = td.loc[td.post == 0, "depth"]
        post_d = td.loc[td.post == 1, "depth"]
        if len(pre_d) and len(post_d):
            summary_rows.append({
                "commodity": c,
                "group": ("banned" if c in BANNED_HEADLINE else
                          "banned_flagged" if c in BANNED_FLAGGED else
                          "control" if c in CONTROL else "donor"),
                "n_pre_yrs": len(pre_d), "n_post_yrs": len(post_d),
                "pre_depth": round(pre_d.mean(), 4),
                "post_depth": round(post_d.mean(), 4),
                "delta_depth": round(post_d.mean() - pre_d.mean(), 4),
                "pre_trough_mode_mo": int(td.loc[td.post == 0, "trough_month"].mode().iloc[0]),
                "post_trough_mode_mo": int(td.loc[td.post == 1, "trough_month"].mode().iloc[0]),
            })

    seas = pd.DataFrame(seas_rows)
    summ = pd.DataFrame(summary_rows)
    depths = pd.DataFrame(depth_long)
    seas.to_csv(OUTDIR / "h7_seasonal_index.csv", index=False)
    depths.to_csv(OUTDIR / "h7_trough_depth.csv", index=False)
    summ.to_csv(OUTDIR / "h7_summary.csv", index=False)

    # ---- DiD on trough depth: banned (headline) vs control+donor ----------------
    # depth_ct = a + b*post + c*banned + d*(post*banned) + commodity FE (absorbed via demean)
    # Simple, transparent: group-mean change diff. Also OLS with commodity FE + cluster.
    d = depths.copy()
    d = d[d.commodity.isin(BANNED_HEADLINE + CONTROL + DONOR)]   # exclude wheat (flagged)
    d["banned"] = d.commodity.isin(BANNED_HEADLINE).astype(int)
    did_rows = []
    # 2x2 means
    for grp, lab in [(1, "banned_headline"), (0, "control+donor")]:
        g = d[d.banned == grp]
        pre = g.loc[g.post == 0, "depth"].mean()
        post = g.loc[g.post == 1, "depth"].mean()
        did_rows.append({"group": lab, "pre_depth": round(pre, 4),
                         "post_depth": round(post, 4), "change": round(post - pre, 4)})
    did_tab = pd.DataFrame(did_rows)
    did_est = (did_tab.loc[did_tab.group == "banned_headline", "change"].iloc[0]
               - did_tab.loc[did_tab.group == "control+donor", "change"].iloc[0])

    # OLS DiD with commodity FE, cluster SE by commodity
    try:
        import statsmodels.formula.api as smf
        d2 = d.copy()
        m = smf.ols("depth ~ post*banned + C(commodity)", data=d2).fit(
            cov_type="cluster", cov_kwds={"groups": d2["commodity"]})
        beta = m.params.get("post:banned", np.nan)
        pval = m.pvalues.get("post:banned", np.nan)
        nobs = int(m.nobs)
    except Exception as e:
        beta = pval = np.nan
        nobs = len(d)
        print("[warn] OLS DiD failed:", e)

    # ---- ROBUSTNESS DiD: trough depth from the SEASONAL INDEX itself ------------
    # amplitude = 1 - min(seasonal factor); harvest-aligned by construction (the seasonal
    # low IS the glut). Computed on pre/post-estimated seasonal indices. Independent of the
    # per-year detrending metric above, so a useful cross-check.
    amp_rows = []
    for c, g in seas[seas.regime.isin(["pre", "post"])].groupby("commodity"):
        pre_i, post_i = g[g.regime == "pre"], g[g.regime == "post"]
        if pre_i.empty or post_i.empty:
            continue
        amp_rows.append({"commodity": c,
                         "pre_amp": round(1 - pre_i.seas_index.min(), 4),
                         "post_amp": round(1 - post_i.seas_index.min(), 4),
                         "pre_low_mo": int(pre_i.loc[pre_i.seas_index.idxmin(), "month"]),
                         "post_low_mo": int(post_i.loc[post_i.seas_index.idxmin(), "month"])})
    amp = pd.DataFrame(amp_rows)
    amp["delta"] = (amp.post_amp - amp.pre_amp).round(4)
    amp["banned"] = amp.commodity.isin(BANNED_HEADLINE).astype(int)
    amp_b = amp[amp.commodity.isin(BANNED_HEADLINE)]
    amp_c = amp[amp.commodity.isin(CONTROL + DONOR)]
    amp_did = amp_b.delta.mean() - amp_c.delta.mean()
    amp.to_csv(OUTDIR / "h7_seasonal_amplitude.csv", index=False)

    pd.DataFrame([{
        "metric": "trend-detrended annual trough depth (primary)",
        "did_2x2_estimate": round(did_est, 4),
        "did_ols_beta_post_x_banned": (round(float(beta), 4) if np.isfinite(beta) else None),
        "did_ols_pvalue": (round(float(pval), 4) if np.isfinite(pval) else None),
        "n_obs": nobs,
        "n_banned_commodities": d.loc[d.banned == 1, "commodity"].nunique(),
        "n_control_commodities": d.loc[d.banned == 0, "commodity"].nunique(),
        "note": "depth = 1 - (annual-min price / centered-12mo-MA trend). +ve DiD = troughs deepened more for banned.",
    }, {
        "metric": "seasonal-index amplitude (robustness)",
        "did_2x2_estimate": round(float(amp_did), 4),
        "did_ols_beta_post_x_banned": None,
        "did_ols_pvalue": None,
        "n_obs": len(amp),
        "n_banned_commodities": int(amp_b.commodity.nunique()),
        "n_control_commodities": int(amp_c.commodity.nunique()),
        "note": "amp = 1 - min(seasonal factor), pre vs post. harvest-aligned. +ve DiD = troughs deepened more for banned.",
    }]).to_csv(OUTDIR / "h7_did.csv", index=False)

    # ---- plots: seasonal index pre vs post for key commodities ------------------
    key = ["chana", "mustard", "soybean", "moong", "wheat", "castor", "jeera", "maize"]
    for c in key:
        sub = seas[seas.commodity == c]
        if sub.empty:
            continue
        fig, ax = plt.subplots(figsize=(7, 4))
        for regime, style in [("pre", "-o"), ("post", "-s")]:
            r = sub[sub.regime == regime].sort_values("month")
            if not r.empty:
                ax.plot(r.month, r.seas_index, style, label=f"{regime}-ban")
        ax.axhline(1.0, color="grey", lw=0.8, ls="--")
        hm = HARVEST_MONTHS.get(c, [])
        for m in hm:
            ax.axvspan(m - 0.4, m + 0.4, color="orange", alpha=0.12)
        flag = "  [MSP/procurement-flagged]" if c in BANNED_FLAGGED else ""
        ax.set_title(f"{c} multiplicative seasonal index (orange = harvest){flag}")
        ax.set_xlabel("month"); ax.set_ylabel("seasonal factor (mean=1)")
        ax.set_xticks(range(1, 13)); ax.legend()
        fig.tight_layout()
        fig.savefig(OUTDIR / f"h7_seasonal_{c}.png", dpi=110)
        plt.close(fig)

    # ---- console report ---------------------------------------------------------
    print("\n=== H7 trough-depth summary (depth = fractional dip of annual low below trend) ===")
    if not summ.empty:
        order = ["banned", "banned_flagged", "control", "donor"]
        summ_sorted = summ.sort_values(["group", "commodity"],
                                       key=lambda s: s.map({g: i for i, g in enumerate(order)})
                                       if s.name == "group" else s)
        print(summ_sorted.to_string(index=False))
        print("\nGroup-mean depth change (post-pre):")
        print(summ.groupby("group")[["pre_depth", "post_depth", "delta_depth"]].mean().round(4))
    print("\n=== DiD (banned headline vs control+donor) on trough depth ===")
    print(did_tab.to_string(index=False))
    print(f"\nDiD 2x2 estimate (banned change - control change) = {did_est:+.4f}")
    print(f"DiD OLS beta(post x banned) = {beta:+.4f}   p = {pval:.4f}   nobs = {nobs}")
    print("  (+) => harvest troughs deepened MORE for banned commodities after the ban.")
    print(f"\nROBUSTNESS (seasonal-index amplitude) DiD = {amp_did:+.4f}")
    print(f"  banned amp change  = {amp_b.delta.mean():+.4f}   control amp change = {amp_c.delta.mean():+.4f}")

    print("\nSpans (months) used:")
    for c, (a, b, n) in spans.items():
        print(f"  {c:14s} {a}..{b}  ({n} mo)")

    print(f"\nWrote outputs to {OUTDIR}")


if __name__ == "__main__":
    main()
