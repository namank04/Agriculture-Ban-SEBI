"""C1 co-primary estimator (H1): Synthetic Diff-in-Diff (Arkhangelsky, Athey,
Hirshberg, Imbens & Wager 2021, AER) on the commodity-level district-median ln(rv30)
series. Companion to run_c1_scm.py (Abadie SCM) and run_v0_did.py (two-way FE DiD).

SDID = a doubly-weighted 2x2 DiD. It learns BOTH unit weights (omega, a la SCM but
with an intercept + ridge regularization, matching donor pre-paths to the treated
pre-path) AND time weights (lambda, matching control pre-periods to control post-periods),
then forms the weighted double-difference. It relaxes SCM's exact-pre-fit requirement
(the intercept absorbs level gaps) and DiD's parallel-trends requirement (lambda
down-weights non-comparable pre-periods).

INPUT : 02_data/clean/vol_panel_monthly.csv  (commodity x district x month, rv30)
OUTPUT: 04_empirics/H1_volatility/output/c1_sdid_results.csv

DESIGN CHOICE / DOCUMENTED LIMITATION
-------------------------------------
The canonical SDID estimator (the omega/lambda solve below) is defined for a SINGLE
adoption date and a balanced block. The suspension is STAGGERED at the commodity level
(chana 2021-08-16, mustard 2021-10-08, the rest 2021-12-20). We follow the task spec and
the run_c1_scm.py convention by:
  (a) reporting a POOLED SDID with one common treatment date 2021-12-20 (all banned
      commodities treated together) on the balanced window, AND
  (b) reporting a PER-COMMODITY SDID using each commodity's own suspension date (one
      treated unit vs the donor pool), which respects the staggering.
The pooled (a) is the headline co-primary number; chana/mustard are mildly mis-timed in
it (their true ban predates 2021-12-20, so a few "pre" months in the pooled window are
already post-treatment for them -> a conservative attenuation). The per-commodity (b)
removes that mis-timing. We do NOT implement the full block-bootstrap staggered SDID of
Arkhangelsky et al. App. A (would require a researcher decision on cohort pooling).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
PANEL_NAME = sys.argv[1] if len(sys.argv) > 1 else "vol_panel_monthly.csv"
PANEL = ROOT / "02_data" / "clean" / PANEL_NAME
SUFFIX = "_national" if "national" in PANEL_NAME else ""
OUTDIR = ROOT / "04_empirics" / "H1_volatility" / "output"

# Mirror run_c1_scm.py exactly: same donor pool, same treated set, same staggered dates.
DONORS = ["castor", "guarseed413", "cotton", "jeera", "turmeric"]          # clean core
FOOD_DONORS = ["barley", "maize", "jowar", "bajra", "ragi", "groundnut",   # auto-include
               "sesamum", "sunflower"]
TREAT_DATE = {
    "chana":   pd.Timestamp("2021-08-16"),
    "mustard": pd.Timestamp("2021-10-08"),
    "wheat":   pd.Timestamp("2021-12-20"),
    # paddy DROPPED — MSP price-censored (40.3% flat returns; FCI procurement pins spot); decision_log 2026-06-21
    "soybean": pd.Timestamp("2021-12-20"),
    "moong":   pd.Timestamp("2021-12-20"),
}
POOLED_DATE = pd.Timestamp("2021-12-20")
MSP_FLAG = {"wheat"}  # paddy dropped; wheat kept (core) MSP-flagged


# ----------------------------------------------------------------------------- data
def commodity_series(panel: pd.DataFrame) -> pd.DataFrame:
    """commodity x month wide table of ln(median rv30 across districts)."""
    return (panel.groupby(["commodity", "date"])["rv30"].median()
                 .replace(0, np.nan).pipe(np.log)
                 .unstack("commodity").sort_index())


# ------------------------------------------------------------- SDID weight solvers
def _simplex_intercept_solve(target: np.ndarray, basis: np.ndarray, zeta: float,
                             n_reg: int) -> tuple[float, np.ndarray]:
    """min_{b0, w>=0, sum w=1} || target - (b0 + basis @ w) ||^2 + zeta^2 * n_reg * ||w||^2.

    Used for BOTH weight problems:
      - omega: target = donor-mean pre-path?? no -> target = treated pre-path over time,
        basis  = donor pre-paths (rows=pre periods, cols=donors). Solves for unit weights.
      - lambda: target = control post-period means (per control), basis = control
        pre-period block (rows=controls, cols=pre periods). Solves for time weights.
    The intercept b0 is the SDID innovation vs Abadie SCM (absorbs the level gap);
    the ridge term zeta^2*n_reg*||w||^2 is the Arkhangelsky et al. regularization that
    makes omega unique / well-behaved with many donors.
    """
    J = basis.shape[1]
    reg = (zeta ** 2) * n_reg

    def obj(theta):
        b0, w = theta[0], theta[1:]
        resid = target - (b0 + basis @ w)
        return float(resid @ resid + reg * (w @ w))

    x0 = np.concatenate([[0.0], np.full(J, 1.0 / J)])
    res = minimize(obj, x0, method="SLSQP",
                   bounds=[(None, None)] + [(0.0, 1.0)] * J,
                   constraints=({"type": "eq", "fun": lambda t: t[1:].sum() - 1.0},),
                   options={"maxiter": 1000, "ftol": 1e-12})
    return float(res.x[0]), res.x[1:]


def sdid_fit(Y_co: np.ndarray, Y_tr: np.ndarray, n_pre: int):
    """Core SDID on a balanced block.
      Y_co : (N_co  x T) control outcomes
      Y_tr : (N_tr  x T) treated outcomes (averaged over treated units inside)
      n_pre: number of pre-treatment columns (cols 0:n_pre are pre, n_pre: are post)
    Returns dict with att (ln), omega, lambda, intercepts, fit diagnostics.
    Follows Arkhangelsky et al. (2021) Eqs. (2.2)-(2.7) and the zeta in their Sec. 2.
    """
    N_co, T = Y_co.shape
    n_post = T - n_pre
    y_tr = Y_tr.mean(axis=0)                       # treated-average path, length T

    # zeta (regularization): (N_tr*n_post)^(1/4) * sigma_hat, where sigma_hat is the s.d.
    # of first-differenced control outcomes over the PRE period (Arkhangelsky et al. 2021,
    # Sec. 2). NOTE on these data: sigma_hat ~ 0.20 (monthly vol series are noisy) and the
    # donor pool is small (5), so the penalty zeta^2 * n_pre * ||omega||^2 is large relative
    # to the pre-fit SSR -> omega is shrunk toward EQUAL weights. That is the intended SDID
    # behaviour (ridge dominates when individual donors are uninformative), not a bug; the
    # near-uniform omega below is therefore expected, and the SDID intercept omega0 carries
    # the level match. A larger/more heterogeneous donor pool would sharpen omega.
    dY = np.diff(Y_co[:, :n_pre], axis=1)          # control pre first-differences
    sigma_hat = dY.std(ddof=1) if dY.size > 1 else 1.0
    zeta = ((Y_tr.shape[0] * n_post) ** 0.25) * sigma_hat

    # --- omega (unit weights): match donor pre-paths to treated-avg pre-path over time.
    # target = treated-avg pre path (length n_pre); basis = control pre block transposed
    # (rows = pre periods, cols = controls). Regularize with n_reg = n_pre (Arkhangelsky).
    omega0, omega = _simplex_intercept_solve(
        target=y_tr[:n_pre], basis=Y_co[:, :n_pre].T, zeta=zeta, n_reg=n_pre)

    # --- lambda (time weights): match control pre-periods to control post-period mean.
    # target = control post-period means (length N_co); basis = control pre block
    # (rows = controls, cols = pre periods). No ridge on lambda (zeta=0), per the paper.
    post_mean_co = Y_co[:, n_pre:].mean(axis=1)     # length N_co
    lam0, lam = _simplex_intercept_solve(
        target=post_mean_co, basis=Y_co[:, :n_pre], zeta=0.0, n_reg=0)

    # --- SDID ATT = weighted 2x2 double difference.
    # tau = [ (treated post - omega.control post) ]
    #     - [ lambda-weighted( treated pre - omega.control pre ) ]
    co_pre_t  = omega @ Y_co[:, :n_pre]             # length n_pre  (synthetic-control pre path)
    co_post   = omega @ Y_co[:, n_pre:]            # length n_post
    tr_pre_t  = y_tr[:n_pre]
    tr_post   = y_tr[n_pre:]

    treated_diff = tr_post.mean() - (lam @ tr_pre_t)
    control_diff = co_post.mean() - (lam @ co_pre_t)
    att = float(treated_diff - control_diff)

    # pre-fit diagnostics (how well omega+intercept tracks treated pre-path)
    synth_pre = omega0 + omega @ Y_co[:, :n_pre]
    pre_resid = tr_pre_t - synth_pre
    pre_rmse = float(np.sqrt((pre_resid ** 2).mean()))

    return {
        "att": att, "att_pct": float(np.exp(att) - 1),
        "omega": omega, "omega0": omega0, "lam": lam, "lam0": lam0,
        "zeta": float(zeta), "sigma_hat": float(sigma_hat),
        "pre_rmse": pre_rmse, "n_pre": n_pre, "n_post": n_post,
    }


# --------------------------------------------------------------------- inference
def placebo_se(Y_co: np.ndarray, n_pre: int, n_tr: int, att_hat: float, B: int = 400,
               seed: int = 11) -> float:
    """Placebo SE (Arkhangelsky et al. 2021, Algorithm 4 'placebo variance').
    Repeatedly draw n_tr pseudo-treated units FROM THE CONTROLS, run SDID treating
    them as treated (remaining controls as donors), collect the placebo ATTs; SE is
    their s.d. Valid when N_co > n_tr. Requires no treated information beyond n_tr."""
    rng = np.random.default_rng(seed)
    N_co = Y_co.shape[0]
    if N_co <= n_tr + 1:
        return np.nan
    taus = []
    for _ in range(B):
        idx = rng.choice(N_co, size=n_tr, replace=False)
        mask = np.zeros(N_co, dtype=bool); mask[idx] = True
        fit = sdid_fit(Y_co[~mask], Y_co[mask], n_pre)
        taus.append(fit["att"])
    taus = np.asarray(taus)
    return float(taus.std(ddof=1))


def jackknife_se(Y_co: np.ndarray, Y_tr: np.ndarray, n_pre: int) -> float:
    """Leave-one-out jackknife SE over the CONTROL units (Arkhangelsky et al. Alg. 3,
    adapted). Drops each donor in turn, re-estimates SDID, scales the spread. For a
    single treated unit the treated-side jackknife is undefined, so we jackknife donors
    only (a documented simplification — reported alongside the placebo SE)."""
    N_co = Y_co.shape[0]
    if N_co < 3:
        return np.nan
    taus = []
    for j in range(N_co):
        keep = np.ones(N_co, dtype=bool); keep[j] = False
        fit = sdid_fit(Y_co[keep], Y_tr, n_pre)
        taus.append(fit["att"])
    taus = np.asarray(taus)
    tau_bar = taus.mean()
    return float(np.sqrt((N_co - 1) / N_co * ((taus - tau_bar) ** 2).sum()))


# --------------------------------------------------------------------------- main
def balanced_block(wide: pd.DataFrame, cols: list[str], t0: pd.Timestamp):
    """Rows = months where ALL `cols` are present; split at t0. Returns (Y dict, n_pre, idx)."""
    sub = wide[cols].dropna()
    pre_mask = sub.index < t0
    n_pre = int(pre_mask.sum())
    return sub, n_pre, sub.index


def run_one(wide, treated_cols, donor_list, t0, label):
    cols = treated_cols + donor_list
    sub, n_pre, idx = balanced_block(wide, cols, t0)
    n_post = len(sub) - n_pre
    if n_pre < 12 or n_post < 6:
        print(f"[{label:18s}] insufficient pre/post (pre={n_pre}, post={n_post}) — skipped")
        return None
    Y_tr = sub[treated_cols].values.T        # (N_tr x T)
    Y_co = sub[donor_list].values.T          # (N_co x T)
    fit = sdid_fit(Y_co, Y_tr, n_pre)
    se_plac = placebo_se(Y_co, n_pre, n_tr=len(treated_cols), att_hat=fit["att"])
    se_jack = jackknife_se(Y_co, Y_tr, n_pre)
    # The placebo SE (Alg. 4) is the ONLY valid uncertainty here; it needs N_co > n_tr+1.
    # The donor-jackknife holds the treated side FIXED and only swaps donors, so it measures
    # donor-substitution STABILITY, not treated-unit/counterfactual variance — it is NOT a valid
    # standard error and must not be turned into a z (doing so produced a spurious z~-7.7).
    # So we report a z ONLY when the placebo SE is defined; the pooled spec (n_tr=5, N_co=5
    # donors -> placebo undefined) reports its point estimate with z = n/a.
    valid = np.isfinite(se_plac)
    se = se_plac if valid else np.nan
    se_src = "placebo" if valid else "none (placebo undefined; donor-jk is stability-only, not an SE)"
    z = fit["att"] / se if (valid and se > 0) else np.nan
    fit.update(donor_list=donor_list, se_placebo=se_plac, se_jack=se_jack,
               se=se, se_src=se_src, z=z, idx=idx)
    wt = "; ".join(f"{d}:{w:.3f}" for d, w in zip(donor_list, fit["omega"]) if w >= 0.01)
    zstr = f"{z:+.2f}" if np.isfinite(z) else "n/a"
    print(f"[{label:18s}] ATT={100*fit['att_pct']:+6.1f}%  pre-RMSE={fit['pre_rmse']:.3f}  "
          f"SE(plac)={se_plac:.3f}  donor-jk-spread={se_jack:.3f}  z={zstr}({se_src})  "
          f"w0={fit['omega0']:+.2f}")
    print(f"{'':20s} omega: {wt}")
    return fit


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    panel = pd.read_csv(PANEL, parse_dates=["date"])
    wide = commodity_series(panel)
    donor_list = [d for d in DONORS + FOOD_DONORS if d in wide.columns]
    missing = [d for d in DONORS if d not in wide.columns]
    if missing:
        raise SystemExit(f"core donors missing from panel: {missing}")
    treated_present = [c for c in TREAT_DATE if c in wide.columns]
    print(f"panel={PANEL_NAME}  donors({len(donor_list)})={donor_list}")
    print(f"treated({len(treated_present)})={treated_present}\n")

    rows = []

    # ----- (a) POOLED SDID: all banned treated together, single date 2021-12-20.
    print("=== POOLED SDID (single date 2021-12-20, all banned treated jointly) ===")
    pooled = run_one(wide, treated_present, donor_list, POOLED_DATE, "POOLED(all banned)")
    if pooled:
        rows.append({
            "spec": "pooled", "commodity": "ALL_BANNED",
            "treat_date": POOLED_DATE.date(), "n_treated_units": len(treated_present),
            "att_lnrv": round(pooled["att"], 4), "att_pct": round(100 * pooled["att_pct"], 1),
            "se_placebo": round(pooled["se_placebo"], 4) if np.isfinite(pooled["se_placebo"]) else np.nan,
            "se_jackknife": round(pooled["se_jack"], 4),
            "se_reported": round(pooled["se"], 4), "se_source": pooled["se_src"],
            "z": round(pooled["z"], 2) if np.isfinite(pooled["z"]) else np.nan,
            "pre_rmse": round(pooled["pre_rmse"], 4),
            "n_pre": pooled["n_pre"], "n_post": pooled["n_post"],
            "zeta": round(pooled["zeta"], 4), "omega0": round(pooled["omega0"], 4),
            "msp_flag": False,
            "omega": "; ".join(f"{d}:{w:.3f}" for d, w in
                               zip(donor_list, pooled["omega"]) if w >= 0.01),
        })

    # ----- (b) PER-COMMODITY SDID: each treated unit vs donor pool, own ban date.
    print("\n=== PER-COMMODITY SDID (own suspension date, single treated unit) ===")
    for comm in treated_present:
        t0 = TREAT_DATE[comm]
        fit = run_one(wide, [comm], donor_list, t0, comm)
        if not fit:
            continue
        rows.append({
            "spec": "per_commodity", "commodity": comm,
            "treat_date": t0.date(), "n_treated_units": 1,
            "att_lnrv": round(fit["att"], 4), "att_pct": round(100 * fit["att_pct"], 1),
            "se_placebo": round(fit["se_placebo"], 4) if np.isfinite(fit["se_placebo"]) else np.nan,
            "se_jackknife": round(fit["se_jack"], 4),
            "se_reported": round(fit["se"], 4), "se_source": fit["se_src"],
            "z": round(fit["z"], 2) if np.isfinite(fit["z"]) else np.nan,
            "pre_rmse": round(fit["pre_rmse"], 4),
            "n_pre": fit["n_pre"], "n_post": fit["n_post"],
            "zeta": round(fit["zeta"], 4), "omega0": round(fit["omega0"], 4),
            "msp_flag": comm in MSP_FLAG,
            "omega": "; ".join(f"{d}:{w:.3f}" for d, w in
                               zip(donor_list, fit["omega"]) if w >= 0.01),
        })

    out = pd.DataFrame(rows)
    out.to_csv(OUTDIR / f"c1_sdid_results{SUFFIX}.csv", index=False)
    print(f"\nwrote {OUTDIR/('c1_sdid_results'+SUFFIX+'.csv')}  ({len(out)} rows)")

    # ----- cross-estimator comparison (SDID vs SCM vs DiD), for the per-commodity rows.
    scm_fp = OUTDIR / f"c1_scm_results{SUFFIX}.csv"
    if scm_fp.exists():
        scm = pd.read_csv(scm_fp).set_index("commodity")["att_pct"]
        print("\n=== SDID vs SCM (per-commodity ATT %, district-median ln rv30) ===")
        print(f"{'commodity':10s} {'SDID%':>8s} {'SCM%':>8s} {'diff':>8s}")
        for r in rows:
            if r["spec"] != "per_commodity":
                continue
            c = r["commodity"]
            s = scm.get(c, np.nan)
            d = r["att_pct"] - s if np.isfinite(s) else np.nan
            print(f"{c:10s} {r['att_pct']:+8.1f} {s:+8.1f} {d:+8.1f}")
    print("\nDiD reference (run_v0_did.py, district panel, paddy+guar dropped, current food-donor "
          "panel): beta=-0.103 -> -9.8%, CR1 p≈0.145 / wild boot p≈0.153. SDID/SCM are companion "
          "diagnostics, not independent confirmation; the current reading is donor sensitivity with "
          "a chana-centered lower-volatility signal.")
    print("LIMITATIONS: pooled spec uses one date (2021-12-20); chana/mustard truly banned "
          "earlier -> attenuated (per-commodity rows fix timing). POOLED SE is undefined "
          "(n_tr=5; donor pool depends on acquired food donors). Report the placebo-based SE/z where "
          "available; wheat is MSP/export-ban confounded and no longer supports the headline.")


if __name__ == "__main__":
    main()
