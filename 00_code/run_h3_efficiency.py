"""H3 — Did removing futures degrade SPOT-market efficiency / integration?

Two pieces, pre vs post the 2021-12-20 suspension, banned vs control commodities:

  (A) Lo-MacKinlay (1988) variance-ratio tests of the random-walk / informational-
      efficiency hypothesis on DAILY national spot log-returns. Under a random walk
      VR(q) = 1; |VR(q)-1| > 0 indicates predictability (return autocorrelation),
      i.e. LESS informationally efficient. We use the heteroskedasticity-ROBUST
      M2(q) statistic (Lo-MacKinlay eq. for the robust variance), N(0,1) under H0.
      We read off whether |VR-1| grows post-ban for banned vs controls.

  (B) Cross-mandi spatial INTEGRATION. Per commodity, pick the top-N mandis by
      trading-day coverage (selection rule fixed BEFORE looking at integration
      results — see SELECT_TOP_MANDIS / coverage filter below). For every mandi
      pair, run Engle-Granger cointegration on log price levels, separately in the
      PRE and POST windows. Report the share of pairs that are cointegrated
      (5% level) and the median error-correction half-life of price deviations.
      Less integration / longer half-lives post-ban = spatial efficiency loss.

Design notes / honesty:
  * paddy DROPPED (MSP price-censored — utils.EXCLUDE_PRIMARY). wheat is MSP-FLAGGED;
    kept only as a flagged secondary banned series, not in the headline banned mean.
  * Primary banned = chana, mustard, soybean, moong. Controls (futures still trade) =
    castor, guarseed413, jeera, turmeric, cotton.
  * e-NAM expansion post-2021 pushes spatial integration UP over time, working
    AGAINST a disintegration finding. So any post-ban integration DROP for banned
    relative to controls is a conservative / lower-bound result (spec.md risk note).
  * Power is limited: ~4 clean banned commodities, daily spot has microstructure
    noise, and post window is short. Treated as descriptive + a DiD-in-VR contrast,
    not a high-powered test. Stated explicitly in the memo.

INPUT : 02_data/clean/spot_daily_<slug>.csv              (national modal, A)
        02_data/raw/agmarknet/district/<slug>__state*.json (mandi-day, B)
OUTPUT: 04_empirics/H3_spot_efficiency/output/
"""
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.stattools import coint
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant

from utils import BAN_DATE, trading_days_only, log_returns

warnings.simplefilter("ignore")

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "02_data" / "clean"
RAW = ROOT / "02_data" / "raw" / "agmarknet" / "district"
OUT = ROOT / "04_empirics" / "H3_spot_efficiency" / "output"
OUT.mkdir(parents=True, exist_ok=True)

# ---- commodity sets ---------------------------------------------------------
BANNED_PRIMARY = ["chana", "mustard", "soybean", "moong"]
BANNED_FLAGGED = ["wheat"]                       # MSP-flagged; reported separately
CONTROLS = ["castor", "guarseed413", "jeera", "turmeric", "cotton"]
ALL_C = BANNED_PRIMARY + BANNED_FLAGGED + CONTROLS

GROUP = {**{c: "banned" for c in BANNED_PRIMARY},
         **{c: "banned_flagged" for c in BANNED_FLAGGED},
         **{c: "control" for c in CONTROLS}}

# ---- Part B selection rule (fixed BEFORE seeing integration results) --------
SELECT_TOP_MANDIS = 8          # spec: 6-10 major mandis per commodity
MIN_COVERAGE_FRAC = 0.40       # a mandi must report on >=40% of trading days in BOTH
                               # the pre and post window to qualify (else gaps make
                               # the cointegration regression meaningless)
COINT_ALPHA = 0.05


# ============================================================================
# PART A — Lo-MacKinlay variance-ratio test (heteroskedasticity-robust)
# ============================================================================
def lomac_vr(returns: np.ndarray, q: int):
    """Lo-MacKinlay (1988) variance ratio for holding period q on a return series.

    Returns (VR, M1 z, M2 z) where M1 = homoskedastic test stat, M2 = hetero-
    robust test stat (both ~ N(0,1) under the random-walk null). |VR-1| measures
    departure from the random walk (positive => positive serial correlation =>
    predictable => less informationally efficient).
    """
    x = np.asarray(returns, dtype=float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < q * 10:                      # need enough data for a stable estimate
        return np.nan, np.nan, np.nan
    mu = x.mean()
    # variance of 1-period returns (unbiased)
    var1 = np.sum((x - mu) ** 2) / (n - 1)
    if var1 == 0:
        return np.nan, np.nan, np.nan
    # variance of q-period (overlapping) returns, bias-corrected (Lo-MacKinlay m)
    m = q * (n - q + 1) * (1 - q / n)
    summ = 0.0
    for t in range(q - 1, n):
        summ += (np.sum(x[t - q + 1:t + 1]) - q * mu) ** 2
    varq = summ / m
    vr = varq / var1

    # homoskedastic stat M1
    phi1 = 2.0 * (2 * q - 1) * (q - 1) / (3.0 * q * n)
    z1 = (vr - 1) / np.sqrt(phi1) if phi1 > 0 else np.nan

    # hetero-robust stat M2 (asymptotic variance = sum of delta(j) weights).
    # Lo-MacKinlay (1988) / Campbell-Lo-MacKinlay (1997) eq 2.4.43:
    #   delta(j) = [ sum_t (x_t-mu)^2 (x_{t-j}-mu)^2 ] / [ sum_t (x_t-mu)^2 ]^2
    # (NO extra n factor — including one deflates z2 by sqrt(n) and kills power).
    phi2 = 0.0
    for j in range(1, q):
        num = np.sum((x[j:] - mu) ** 2 * (x[:n - j] - mu) ** 2)
        den = (np.sum((x - mu) ** 2)) ** 2
        delta = num / den
        phi2 += (2.0 * (q - j) / q) ** 2 * delta
    z2 = (vr - 1) / np.sqrt(phi2) if phi2 > 0 else np.nan
    return vr, z1, z2


def load_national(slug: str) -> pd.Series:
    fp = CLEAN / f"spot_daily_{slug}.csv"
    if not fp.exists():
        return pd.Series(dtype=float)
    df = pd.read_csv(fp, parse_dates=["date"]).sort_values("date")
    df = df[df.price > 0]
    s = df.set_index("date")["price"]
    return s


# National daily MANDI modal returns carry extreme single-day spikes (excess
# kurtosis ~20) from one-day reporting/composition glitches in the modal series
# (a mandi modal jumping 40%+ for a day then reverting). We winsorize returns at
# 1% (project utils convention) so the VR point estimate reflects genuine serial
# dependence, not a handful of glitch jumps. (The hetero-robust M2 statistic is
# by construction insensitive to such fat tails once computed correctly — see the
# delta(j) note in lomac_vr; an earlier spurious n-factor had deflated M2 by
# sqrt(n) and falsely looked like "fat tails kill the robust test".)
# Winsorization is applied PER WINDOW so pre and post are treated symmetrically.
WINSOR_P = 0.01


def _winsor(r: pd.Series, p: float = WINSOR_P) -> pd.Series:
    r = r.dropna()
    if r.empty:
        return r
    lo, hi = r.quantile(p), r.quantile(1 - p)
    return r.clip(lo, hi)


def part_a():
    rows = []
    qs = [2, 5, 10]
    for slug in ALL_C:
        s = load_national(slug)
        if s.empty:
            print(f"[A:{slug}] no national series")
            continue
        ret = log_returns(s)
        pre = _winsor(ret[ret.index < BAN_DATE])
        post = _winsor(ret[ret.index >= BAN_DATE])
        for q in qs:
            vr_pre, z1_pre, z_pre = lomac_vr(pre.values, q)
            vr_post, z1_post, z_post = lomac_vr(post.values, q)
            rows.append(dict(
                commodity=slug, group=GROUP[slug], q=q,
                n_pre=int(pre.notna().sum()), n_post=int(post.notna().sum()),
                vr_pre=vr_pre, z_pre=z_pre, z1_pre=z1_pre,
                vr_post=vr_post, z_post=z_post, z1_post=z1_post,
                # inefficiency measure: distance of VR from the RW null of 1
                ineff_pre=abs(vr_pre - 1) if pd.notna(vr_pre) else np.nan,
                ineff_post=abs(vr_post - 1) if pd.notna(vr_post) else np.nan,
                d_ineff=(abs(vr_post - 1) - abs(vr_pre - 1))
                if pd.notna(vr_pre) and pd.notna(vr_post) else np.nan,
            ))
    vr = pd.DataFrame(rows)
    vr.to_csv(OUT / "A_variance_ratios.csv", index=False)

    # group-level DiD-in-inefficiency: mean change in |VR-1|, banned vs control
    did = (vr[vr.group.isin(["banned", "control"])]
           .groupby(["group", "q"])["d_ineff"].mean().unstack("group"))
    did["did_banned_minus_control"] = did["banned"] - did["control"]
    did.to_csv(OUT / "A_vr_did_summary.csv")
    print("\n[A] mean change in |VR-1| (post - pre), by group and q:")
    print(did.round(3).to_string())
    return vr, did


# ============================================================================
# PART B — cross-mandi spatial integration (Engle-Granger, pre vs post)
# ============================================================================
def load_mandi_panel(slug: str) -> pd.DataFrame:
    """All mandi(market)-day modal prices for a commodity, trading-days only."""
    frames = []
    for fp in sorted(RAW.glob(f"{slug}__state*.json")):
        try:
            blob = json.loads(fp.read_text())
        except Exception:
            continue
        if not blob.get("data"):
            continue
        df = pd.DataFrame(blob["data"])
        df["date"] = pd.to_datetime(df["date"].str[:10])
        df = df[(df.modal_price > 0) & trading_days_only(df.date)]
        if df.empty:
            continue
        # one modal per market-day (median collapses intra-market dupes)
        g = (df.groupby(["market_id", "date"], as_index=False)["modal_price"]
               .median())
        frames.append(g)
    if not frames:
        return pd.DataFrame()
    out = pd.concat(frames, ignore_index=True)
    out["market_id"] = out["market_id"].astype(int)
    return out.rename(columns={"modal_price": "price"})


def select_mandis(panel: pd.DataFrame):
    """Pick top-N mandis by total trading-day coverage that also clear the
    MIN_COVERAGE_FRAC threshold in BOTH windows. Rule fixed pre-results."""
    pre_days = pd.bdate_range("2017-01-01", BAN_DATE - pd.Timedelta(days=1))
    post_days = pd.bdate_range(BAN_DATE, panel.date.max())
    npre, npost = len(pre_days), len(post_days)

    cov = (panel.assign(post=(panel.date >= BAN_DATE))
                .groupby(["market_id", "post"])["date"].nunique()
                .unstack("post").fillna(0))
    cov.columns = ["n_pre", "n_post"] if list(cov.columns) == [False, True] \
        else cov.columns
    cov = cov.rename(columns={False: "n_pre", True: "n_post"})
    cov["frac_pre"] = cov["n_pre"] / npre
    cov["frac_post"] = cov["n_post"] / npost
    cov["frac_min"] = cov[["frac_pre", "frac_post"]].min(axis=1)
    elig = cov[(cov.frac_pre >= MIN_COVERAGE_FRAC) &
               (cov.frac_post >= MIN_COVERAGE_FRAC)]
    chosen = elig.sort_values("frac_min", ascending=False).head(SELECT_TOP_MANDIS)
    return list(chosen.index), cov


def wide_log_prices(panel: pd.DataFrame, markets: list, lo, hi) -> pd.DataFrame:
    sub = panel[(panel.market_id.isin(markets)) &
                (panel.date >= lo) & (panel.date < hi)]
    w = sub.pivot_table(index="date", columns="market_id", values="price",
                        aggfunc="median")
    # business-day grid, forward-fill short gaps (<=5 days) so the cointegration
    # regression sees aligned series without inventing long stretches
    w = w.reindex(pd.bdate_range(w.index.min(), w.index.max()))
    w = w.ffill(limit=5)
    w = np.log(w)
    return w


def halflife(spread: np.ndarray) -> float:
    """Error-correction half-life from an AR(1) on the cointegrating spread:
    d_spread_t = a + b*spread_{t-1}; half-life = -ln2/ln(1+b)."""
    s = pd.Series(spread).dropna()
    if len(s) < 30:
        return np.nan
    lag = s.shift(1)
    d = (s - lag).dropna()
    lag = lag.dropna()
    idx = d.index.intersection(lag.index)
    X = add_constant(lag.loc[idx].values)
    res = OLS(d.loc[idx].values, X).fit()
    b = res.params[1]
    rho = 1 + b
    if rho <= 0 or rho >= 1:
        return np.nan
    return -np.log(2) / np.log(rho)


def coint_window(w: pd.DataFrame):
    """All pairwise Engle-Granger tests on a wide log-price frame. Returns share
    cointegrated at COINT_ALPHA and median half-life over cointegrated pairs."""
    cols = list(w.columns)
    pvals, hls = [], []
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            pair = w[[cols[i], cols[j]]].dropna()
            if len(pair) < 60:
                continue
            y, x = pair.iloc[:, 0].values, pair.iloc[:, 1].values
            try:
                _, pval, _ = coint(y, x)
            except Exception:
                continue
            pvals.append(pval)
            if pval < COINT_ALPHA:
                # cointegrating residual = y - (a + b x)
                beta = OLS(y, add_constant(x)).fit().params
                resid = y - (beta[0] + beta[1] * x)
                hls.append(halflife(resid))
    if not pvals:
        return np.nan, np.nan, 0
    share = float(np.mean(np.array(pvals) < COINT_ALPHA))
    med_hl = float(np.nanmedian(hls)) if hls else np.nan
    return share, med_hl, len(pvals)


def part_b():
    rows = []
    for slug in ALL_C:
        panel = load_mandi_panel(slug)
        if panel.empty:
            print(f"[B:{slug}] empty mandi panel")
            continue
        markets, cov = select_mandis(panel)
        if len(markets) < 3:
            print(f"[B:{slug}] only {len(markets)} eligible mandis — skipped "
                  f"(insufficient for pairwise integration)")
            rows.append(dict(commodity=slug, group=GROUP[slug],
                             n_mandi=len(markets), share_pre=np.nan,
                             share_post=np.nan, hl_pre=np.nan, hl_post=np.nan,
                             npairs_pre=0, npairs_post=0))
            continue
        hi = panel.date.max() + pd.Timedelta(days=1)
        w_pre = wide_log_prices(panel, markets, pd.Timestamp("2017-01-01"), BAN_DATE)
        w_post = wide_log_prices(panel, markets, BAN_DATE, hi)
        sh_pre, hl_pre, np_pre = coint_window(w_pre)
        sh_post, hl_post, np_post = coint_window(w_post)
        rows.append(dict(
            commodity=slug, group=GROUP[slug], n_mandi=len(markets),
            share_pre=sh_pre, share_post=sh_post,
            d_share=(sh_post - sh_pre) if pd.notna(sh_pre) and pd.notna(sh_post)
            else np.nan,
            hl_pre=hl_pre, hl_post=hl_post,
            npairs_pre=np_pre, npairs_post=np_post,
        ))
        print(f"[B:{slug:11s}] mandis={len(markets)} "
              f"coint share pre={sh_pre:.2f} post={sh_post:.2f} "
              f"hl pre={hl_pre:.1f} post={hl_post:.1f}")
    integ = pd.DataFrame(rows)
    integ.to_csv(OUT / "B_integration_by_commodity.csv", index=False)

    grp = (integ[integ.group.isin(["banned", "control"])]
           .groupby("group")[["share_pre", "share_post", "d_share",
                              "hl_pre", "hl_post"]].mean())
    if {"banned", "control"}.issubset(grp.index):
        grp.loc["did_banned_minus_control"] = grp.loc["banned"] - grp.loc["control"]
    grp.to_csv(OUT / "B_integration_did_summary.csv")
    print("\n[B] integration by group (mean over commodities):")
    print(grp.round(3).to_string())
    return integ, grp


def main():
    print("=" * 70)
    print("H3 — spot-market efficiency & integration, pre/post ban")
    print(f"banned(primary)={BANNED_PRIMARY}  flagged={BANNED_FLAGGED}")
    print(f"controls={CONTROLS}  ban_date={BAN_DATE.date()}")
    print("=" * 70)
    vr, did_a = part_a()
    integ, did_b = part_b()
    print("\nOutputs written to", OUT)


if __name__ == "__main__":
    main()
