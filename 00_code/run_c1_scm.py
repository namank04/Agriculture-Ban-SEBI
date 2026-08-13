"""C1 step (H1): synthetic control for the spot-volatility effect of the suspension.
Pre-registered in 04_empirics/H1_volatility/preregistration_c1.md.

v1 = Abadie synthetic control per treated commodity on the DISTRICT-MEDIAN ln(rv30)
path (trading-day-corrected panel), with per-commodity (staggered) treatment dates and
in-space placebo inference. v2 (district-level penalized SCM + Synthetic-DiD) follows
once the food donors land.

INPUT : 02_data/clean/vol_panel_monthly.csv  (commodity x district x month, rv30, trading-day-clean)
OUTPUT: 04_empirics/H1_volatility/output/{c1_scm_results.csv, c1_scm_<commodity>.png}

The SCM weight problem per treated unit: choose w over the J donors (w>=0, sum w=1) to
minimise the pre-treatment MSE between the treated ln(rv30) path and the donor-weighted path.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
PANEL_NAME = sys.argv[1] if len(sys.argv) > 1 else "vol_panel_monthly.csv"
PANEL = ROOT / "02_data" / "clean" / PANEL_NAME
SUFFIX = "_national" if "national" in PANEL_NAME else ""
OUTDIR = ROOT / "04_empirics" / "H1_volatility" / "output"

# Donor pool = Option B (decision_log 2026-06-21). guar id 75 EXCLUDED.
DONORS = ["castor", "guarseed413", "cotton", "jeera", "turmeric"]   # clean core
# Food donors (added once acquired+screened); auto-included when present in the panel.
FOOD_DONORS = ["barley", "maize", "jowar", "bajra", "ragi", "groundnut", "sesamum", "sunflower"]
# Treated banned commodities with per-commodity suspension dates (staggered).
TREAT_DATE = {
    "chana":   pd.Timestamp("2021-08-16"),
    "mustard": pd.Timestamp("2021-10-08"),
    "wheat":   pd.Timestamp("2021-12-20"),
    # paddy DROPPED — MSP price-censored (40.3% flat returns; FCI procurement pins spot); decision_log 2026-06-21
    "soybean": pd.Timestamp("2021-12-20"),
    "moong":   pd.Timestamp("2021-12-20"),
}
MSP_FLAG = {"wheat"}  # paddy dropped; wheat kept (core trio) but MSP-flagged as a robustness caveat


def commodity_series(panel: pd.DataFrame) -> pd.DataFrame:
    """commodity x month wide table of ln(median rv30 across districts)."""
    s = (panel.groupby(["commodity", "date"])["rv30"].median()
              .replace(0, np.nan).pipe(np.log)
              .unstack("commodity").sort_index())
    return s


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
    Returns dict with att (mean post gap, ln), pre_rmse, post_rmse, weights, paths."""
    df = pd.concat([y.rename("y"), donors], axis=1).dropna()
    if df.empty:
        return None
    pre, post = df[df.index < t0], df[df.index >= t0]
    if len(pre) < 12 or len(post) < 6:
        return None
    w = scm_weights(pre["y"].values, pre[donors.columns].values)
    synth = df[donors.columns].values @ w
    gap = df["y"].values - synth
    pre_mask = df.index < t0
    return {
        "att": float(gap[~pre_mask].mean()),
        "att_pct": float(np.exp(gap[~pre_mask].mean()) - 1),
        "pre_rmse": float(np.sqrt((gap[pre_mask] ** 2).mean())),
        "post_rmse": float(np.sqrt((gap[~pre_mask] ** 2).mean())),
        "n_pre": int(pre_mask.sum()), "n_post": int((~pre_mask).sum()),
        "weights": dict(zip(donors.columns, np.round(w, 3))),
        "index": df.index, "y": df["y"].values, "synth": synth, "pre_mask": pre_mask,
    }


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    panel = pd.read_csv(PANEL, parse_dates=["date"])
    wide = commodity_series(panel)
    donor_list = [d for d in DONORS + FOOD_DONORS if d in wide.columns]
    missing = [d for d in DONORS if d not in wide.columns]
    if missing:
        raise SystemExit(f"core donors missing from panel: {missing}")
    print(f"panel={PANEL_NAME}  donor pool ({len(donor_list)}): {donor_list}")

    rows = []
    for comm, t0 in TREAT_DATE.items():
        if comm not in wide.columns:
            print(f"[{comm}] not in panel — skipped"); continue
        donors = wide[donor_list]
        fit = fit_unit(wide[comm], donors, t0)
        if fit is None:
            print(f"[{comm}] insufficient pre/post — skipped"); continue

        # in-space placebos: treat each donor as fake-treated, pool = other donors
        placebo_ratios = []
        for d in donor_list:
            others = [x for x in donor_list if x != d]
            pf = fit_unit(wide[d], wide[others], t0)
            if pf and pf["pre_rmse"] > 0:
                placebo_ratios.append(pf["post_rmse"] / pf["pre_rmse"])
        treat_ratio = fit["post_rmse"] / fit["pre_rmse"] if fit["pre_rmse"] > 0 else np.nan
        # rank-based p: share of (treated + placebos) with ratio >= treated's
        all_ratios = placebo_ratios + [treat_ratio]
        p_rank = float(np.mean([r >= treat_ratio for r in all_ratios]))

        rows.append({
            "commodity": comm, "treat_date": t0.date(),
            "att_lnrv": round(fit["att"], 4), "att_pct": round(100 * fit["att_pct"], 1),
            "pre_rmse": round(fit["pre_rmse"], 4), "rmse_ratio": round(treat_ratio, 2),
            "placebo_p": round(p_rank, 3), "n_pre": fit["n_pre"], "n_post": fit["n_post"],
            "msp_flag": comm in MSP_FLAG,
            "weights": "; ".join(f"{k}:{v}" for k, v in fit["weights"].items() if v >= 0.01),
        })
        print(f"[{comm:8s}] ATT={100*fit['att_pct']:+5.1f}%  pre-RMSE={fit['pre_rmse']:.3f}  "
              f"ratio={treat_ratio:.2f}  placebo-p={p_rank:.3f}  "
              f"{'[MSP-flag]' if comm in MSP_FLAG else ''}")

        # plot treated vs synthetic
        plt.figure(figsize=(8, 3.5))
        plt.plot(fit["index"], fit["y"], label=comm, lw=1.6)
        plt.plot(fit["index"], fit["synth"], label="synthetic", ls="--", lw=1.4)
        plt.axvline(t0, c="gray", ls=":"); plt.axhline(0, c="k", lw=.3)
        plt.title(f"C1 SCM: ln(rv30) {comm} vs synthetic (ATT={100*fit['att_pct']:+.1f}%)")
        plt.xlabel("month"); plt.ylabel("ln rv30"); plt.legend(fontsize=8)
        plt.tight_layout(); plt.savefig(OUTDIR / f"c1_scm_{comm}{SUFFIX}.png", dpi=140); plt.close()

    out = pd.DataFrame(rows)
    out.to_csv(OUTDIR / f"c1_scm_results{SUFFIX}.csv", index=False)
    print(f"\nwrote {OUTDIR/('c1_scm_results'+SUFFIX+'.csv')}  ({len(out)} treated commodities)")
    print(f"placebo-p floor ~ 1/{len(donor_list)+1:.0f} (in-space placebos over the donor pool).")


if __name__ == "__main__":
    main()
