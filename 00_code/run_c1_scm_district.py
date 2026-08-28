"""C1 step (H1): district-unit Synthetic Control heterogeneity analysis.

The policy is assigned at the commodity level, so district-level SCM does not create
additional independent treatment assignments and is not used to solve few-cluster
inference. It is retained only to describe heterogeneity across treated districts.

Each treated commodity-district series is compared with the same frozen final donor
pool used by the commodity-level SCM. In-space placebos are constructed from donor
commodity districts using leave-one-donor-out donor medians.

INPUT : 02_data/clean/vol_panel_monthly.csv  (commodity x district x month, rv30, trading-day-clean)
OUTPUT: 04_empirics/H1_volatility/output/{c1_scm_district_results.csv, c1_scm_district_dist.png}

Per treated district d (banned commodity c, suspension date t0_c):
  y_d  = ln(rv30) monthly path of that district
  X    = donor-commodity columns, each = cross-district MEDIAN ln(rv30) of that donor commodity
  w    = simplex weights (w>=0, sum w=1) minimising pre-treatment MSE  ||y_pre - X_pre w||^2
  ATT  = mean post gap (y - Xw), in ln; ATT% = exp(ATT)-1; keep pre_rmse.

In-space placebo: each DONOR-commodity district is treated as fake-treated against the OTHER
donor commodities' medians (leave-one-donor-out so the unit can't synthesise itself), at the same
t0. This yields a placebo distribution of district-level effects; the per-commodity p-value is the
share of placebo |ATT| >= the treated mean |ATT| (a two-sided in-space placebo test).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import minimize

from utils import (
    FINAL_H1_DONORS,
    FINAL_H1_TREAT_DATES,
)

ROOT = Path(__file__).resolve().parents[1]
PANEL_NAME = sys.argv[1] if len(sys.argv) > 1 else "vol_panel_monthly.csv"
PANEL = ROOT / "02_data" / "clean" / PANEL_NAME
SUFFIX = "_national" if "national" in PANEL_NAME else ""
OUTDIR = ROOT / "04_empirics" / "H1_volatility" / "output"

# Frozen final donor pool used for all reported H1 SCM results.
DONORS = list(FINAL_H1_DONORS)
# Treated banned commodities with per-commodity suspension dates (staggered).
TREAT_DATE = dict(FINAL_H1_TREAT_DATES)
MSP_FLAG = {"wheat"}  # paddy dropped; wheat kept (core trio) but MSP-flagged as a robustness caveat

MIN_PRE, MIN_POST = 12, 6


def donor_medians(panel: pd.DataFrame) -> pd.DataFrame:
    """commodity x month wide table of ln(median rv30 across districts). Donor columns."""
    s = (panel.groupby(["commodity", "date"])["rv30"].median()
              .replace(0, np.nan).pipe(np.log)
              .unstack("commodity").sort_index())
    return s


def district_series(panel: pd.DataFrame, commodity: str) -> pd.DataFrame:
    """district x month wide table of ln(rv30) for one commodity (one column per district)."""
    sub = panel[panel["commodity"] == commodity]
    s = (sub.set_index(["district", "date"])["rv30"]
            .replace(0, np.nan).pipe(np.log)
            .unstack("district").sort_index())
    return s  # index=date, columns=district


def scm_weights(y_pre: np.ndarray, X_pre: np.ndarray) -> np.ndarray:
    """Simplex-constrained least squares: min ||y_pre - X_pre w||^2, w>=0, sum w=1."""
    J = X_pre.shape[1]
    res = minimize(lambda w: float(np.mean((y_pre - X_pre @ w) ** 2)),
                   x0=np.full(J, 1.0 / J), method="SLSQP",
                   bounds=[(0.0, 1.0)] * J,
                   constraints=({"type": "eq", "fun": lambda w: w.sum() - 1.0},),
                   options={"maxiter": 500, "ftol": 1e-10})
    return res.x


def fit_unit(y: pd.Series, donors: pd.DataFrame, t0: pd.Timestamp):
    """Fit SCM for one treated series y against donor columns, treatment date t0.
    Returns dict with att (mean post gap, ln), att_pct, pre/post rmse, or None if too short."""
    df = pd.concat([y.rename("y"), donors], axis=1).dropna()
    if df.empty:
        return None
    pre_mask = df.index < t0
    if int(pre_mask.sum()) < MIN_PRE or int((~pre_mask).sum()) < MIN_POST:
        return None
    Xcols = list(donors.columns)
    w = scm_weights(df.loc[pre_mask, "y"].values, df.loc[pre_mask, Xcols].values)
    synth = df[Xcols].values @ w
    gap = df["y"].values - synth
    return {
        "att": float(gap[~pre_mask].mean()),
        "att_pct": float(np.exp(gap[~pre_mask].mean()) - 1),
        "pre_rmse": float(np.sqrt((gap[pre_mask] ** 2).mean())),
        "post_rmse": float(np.sqrt((gap[~pre_mask] ** 2).mean())),
        "n_pre": int(pre_mask.sum()), "n_post": int((~pre_mask).sum()),
    }


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    panel = pd.read_csv(PANEL, parse_dates=["date"])
    med = donor_medians(panel)
    donor_list = list(DONORS)
    missing = [d for d in donor_list if d not in med.columns]
    if missing:
        raise SystemExit(f"final H1 donors missing from panel: {missing}")
    print(f"panel={PANEL_NAME}  frozen donor pool ({len(donor_list)}): {donor_list}")

    # ----- placebo distribution: donor-commodity districts as fake-treated -----
    # LIKE-FOR-LIKE null (adversarial-review fix 2026-06-21): the treated statistic is a
    # commodity MEAN over districts, so the placebo must also be commodity MEANS (mean over
    # each donor's districts) — comparing a mean to single placebo districts mechanically
    # inflates p toward 1. We cache per-donor-commodity district ATTs (for the plot) and
    # derive the commodity means for the p-value. p-floor = 1/(n_donors+1).
    placebo_cache: dict[pd.Timestamp, dict] = {}

    def placebo_by_commodity(t0: pd.Timestamp) -> dict:
        if t0 in placebo_cache:
            return placebo_cache[t0]
        out = {}
        for dc in donor_list:                       # donor commodity providing fake-treated districts
            other_med = med[[x for x in donor_list if x != dc]]   # leave-one-donor-out pool
            dser = district_series(panel, dc)
            atts = [pf["att"] for dist in dser.columns
                    if (pf := fit_unit(dser[dist], other_med, t0)) is not None]
            if atts:
                out[dc] = atts
        placebo_cache[t0] = out
        return out

    rows = []
    summary_atts = {}   # commodity -> list of treated district ATTs (ln) for the plot
    for comm, t0 in TREAT_DATE.items():
        if comm not in panel["commodity"].unique():
            print(f"[{comm}] not in panel — skipped"); continue
        donors = med[donor_list]
        dser = district_series(panel, comm)

        unit_atts, unit_attpct, pre_rmses = [], [], []
        for dist in dser.columns:
            fit = fit_unit(dser[dist], donors, t0)
            if fit is None:
                continue
            unit_atts.append(fit["att"])
            unit_attpct.append(fit["att_pct"])
            pre_rmses.append(fit["pre_rmse"])

        if not unit_atts:
            print(f"[{comm}] no district met >=12 pre / >=6 post — skipped"); continue

        unit_atts = np.asarray(unit_atts)
        unit_attpct = np.asarray(unit_attpct)
        summary_atts[comm] = unit_atts

        mean_att = float(unit_atts.mean())
        median_att = float(np.median(unit_atts))
        pct_neg = float(100.0 * np.mean(unit_atts < 0))

        # in-space placebo p (like-for-like): treated commodity MEAN ATT vs each donor
        # commodity's MEAN ATT. p = (#|placebo mean| >= |treated mean| + 1)/(n+1).
        plac_by = placebo_by_commodity(t0)
        plac_means = np.asarray([float(np.mean(v)) for v in plac_by.values()])
        if plac_means.size:
            p_val = float((np.sum(np.abs(plac_means) >= abs(mean_att)) + 1) / (plac_means.size + 1))
        else:
            p_val = np.nan

        rows.append({
            "commodity": comm, "treat_date": t0.date(),
            "n_districts": int(len(unit_atts)),
            "mean_att_lnrv": round(mean_att, 4),
            "mean_att_pct": round(100 * float(np.exp(mean_att) - 1), 1),
            "median_att_pct": round(100 * float(np.exp(median_att) - 1), 1),
            "mean_att_pct_avg": round(100 * float(unit_attpct.mean()), 1),  # mean of per-district %s
            "pct_districts_negative": round(pct_neg, 1),
            "mean_pre_rmse": round(float(np.mean(pre_rmses)), 4),
            "n_placebo_donors": int(plac_means.size),
            "placebo_p": round(p_val, 4) if plac_means.size else np.nan,
            "msp_flag": comm in MSP_FLAG,
        })
        print(f"[{comm:8s}] n={len(unit_atts):3d}  medATT={100*(np.exp(median_att)-1):+6.1f}%  "
              f"meanATT={100*(np.exp(mean_att)-1):+6.1f}%  %neg={pct_neg:4.0f}  "
              f"placebo-p={p_val:.3f} (vs {plac_means.size} donor-commodity means)  "
              f"{'[MSP-flag]' if comm in MSP_FLAG else ''}")

    out = pd.DataFrame(rows)
    out_path = OUTDIR / f"c1_scm_district_results{SUFFIX}.csv"
    out.to_csv(out_path, index=False)
    print(f"\nwrote {out_path}  ({len(out)} treated commodities)")

    # ----- distribution plot: per-commodity district-ATT distributions vs placebo -----
    if summary_atts:
        comms = list(summary_atts.keys())
        # one panel: violin/box of district ATTs per commodity, with placebo band overlaid.
        fig, ax = plt.subplots(figsize=(10, 4.5))
        data = [100 * (np.exp(summary_atts[c]) - 1) for c in comms]
        positions = np.arange(1, len(comms) + 1)
        bp = ax.boxplot(data, positions=positions, widths=0.55, showmeans=True,
                        patch_artist=True, manage_ticks=False)
        for patch in bp["boxes"]:
            patch.set_facecolor("#9ecae1"); patch.set_alpha(0.7)
        # overlay placebo distribution (pooled over t0s actually used) as a gray strip on the right
        all_plac = (np.concatenate([np.asarray(a) for d in placebo_cache.values() for a in d.values()])
                    if placebo_cache else np.array([]))
        if all_plac.size:
            plac_pct = 100 * (np.exp(all_plac) - 1)
            xpl = len(comms) + 1
            ax.scatter(np.full(plac_pct.size, xpl) + np.random.uniform(-0.12, 0.12, plac_pct.size),
                       plac_pct, s=6, c="gray", alpha=0.35, label="placebo districts")
            comms_lbl = comms + ["placebo"]
            positions_lbl = list(positions) + [xpl]
        else:
            comms_lbl = comms
            positions_lbl = list(positions)
        ax.axhline(0, c="k", lw=0.5)
        ax.set_xticks(positions_lbl); ax.set_xticklabels(comms_lbl, rotation=20)
        ax.set_ylabel("district ATT (% change in rv30)")
        ax.set_title("C1 district-unit SCM: distribution of per-district ATT by banned commodity")
        ax.legend(fontsize=8, loc="upper right")
        plt.tight_layout()
        plot_path = OUTDIR / f"c1_scm_district_dist{SUFFIX}.png"
        plt.savefig(plot_path, dpi=140); plt.close()
        print(f"wrote {plot_path}")

    n_plac_floor = sum(len(a) for d in placebo_cache.values() for a in d.values())
    print(f"placebo p compares treated commodity MEAN vs donor-commodity MEANS (like-for-like; "
          f"floor 1/(n_donors+1)); plotted placebo strip pools {n_plac_floor} donor-district fits.")


if __name__ == "__main__":
    main()
