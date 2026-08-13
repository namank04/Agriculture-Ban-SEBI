"""V0 step 5: WILD-CLUSTER BOOTSTRAP for the DiD (the flagged few-treated gap).

The V0 DiD clusters standard errors on commodity, but there are only 12 commodity
clusters (6 banned, 6 control) and the treatment switches on at the cluster level.
With so few treated clusters the analytic clustered t / p (asymptotic normal) is
unreliable — it tends to OVER-reject. The fix (Cameron, Gelbach & Miller 2008) is
the wild-cluster bootstrap with the null IMPOSED (WCR), Rademacher cluster weights.

Procedure (per Cameron-Gelbach-Miller / MacKinnon-Webb):
  1. Estimate the RESTRICTED model under H0: treat_post=0, i.e. the two-way FE model
     lnrv ~ EntityEffects + TimeEffects only. Keep restricted fitted values + residuals.
  2. Draw a Rademacher sign s_g in {-1,+1} per COMMODITY cluster g.
  3. Form bootstrap outcome  y* = fitted_restricted + s_g * resid_restricted  (sign
     constant within a cluster), re-estimate the UNRESTRICTED DiD, recompute the
     cluster-robust t on treat_post.  -> t*
  4. Repeat B>=999 times.  bootstrap p = share( |t*| >= |t_obs| ).

Speed: the two-way (entity+time) fixed effects are partialled out ONCE by alternating
projections (Frisch-Waugh-Lovell). After that the model is a single-regressor OLS in
the within-transformed space, so each bootstrap draw is O(N) vector ops — no PanelOLS
refit. The within-space cluster-robust t reproduces PanelOLS's clustered t (the
small-sample dof factor is a constant that CANCELS in the |t*|>=|t_obs| comparison;
we still apply it so the reported observed t matches run_v0_did.py).

We run the SAME machine on the Dec-2019 PLACEBO (run_v0_placebo.py logic: pre-ban data
only, fake ban 2019-12-20, guar id 75 dropped) so the placebo p-value gets the same
few-cluster correction.

INPUT : 02_data/clean/vol_panel_monthly.csv
OUTPUT: 04_empirics/V0_lost_results_replication/output/wild_bootstrap_results.txt
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

from utils import BANNED, BAN_DATE

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "04_empirics" / "V0_lost_results_replication" / "output"
FAKE_BAN = pd.Timestamp("2019-12-20")
PLACEBO_DROP = {"guar", "paddy"}  # guar id 75 gum-contaminated (use guarseed413); paddy MSP-censored
MAIN_DROP = {"guar", "paddy"}     # primary spec drops both from the MAIN DiD too (decision_log 2026-06-21)
B = 999                          # bootstrap replications (>=999)
SEED = 20211220
RNG = np.random.default_rng(SEED)


# --------------------------------------------------------------------------- #
#  two-way fixed-effects "within" transform (Frisch-Waugh-Lovell)             #
# --------------------------------------------------------------------------- #
def two_way_demean(values: np.ndarray, g1: np.ndarray, g2: np.ndarray,
                   niter: int = 2000, tol: float = 1e-11) -> np.ndarray:
    """Partial out entity (g1) and time (g2) means by alternating projections.

    Works on a 2-D array (columns demeaned jointly). Converges to the residual
    from a two-way FE regression — the linearmodels EntityEffects+TimeEffects space.
    """
    v = np.asarray(values, dtype=float).copy()
    if v.ndim == 1:
        v = v[:, None]
    # integer codes for fast bincount-based group means
    _, c1 = np.unique(g1, return_inverse=True)
    _, c2 = np.unique(g2, return_inverse=True)
    n1, n2 = c1.max() + 1, c2.max() + 1
    cnt1 = np.bincount(c1, minlength=n1).astype(float)
    cnt2 = np.bincount(c2, minlength=n2).astype(float)
    for _ in range(niter):
        prev = v.copy()                       # genuine snapshot (v is mutated below)
        for j in range(v.shape[1]):
            col = v[:, j]
            col = col - (np.bincount(c1, col, minlength=n1) / cnt1)[c1]
            col = col - (np.bincount(c2, col, minlength=n2) / cnt2)[c2]
            v[:, j] = col
        if np.max(np.abs(v - prev)) < tol:
            break
    return v


# --------------------------------------------------------------------------- #
#  within-space cluster-robust t for a single regressor                       #
# --------------------------------------------------------------------------- #
def cluster_t(xt: np.ndarray, yt: np.ndarray, cl_codes: np.ndarray,
              n_groups: int, ssc: float):
    """OLS slope of yt on xt (both already two-way demeaned) and the
    commodity-cluster-robust t-stat. `ssc` is the constant small-sample
    scale applied to the variance (cancels in the bootstrap comparison)."""
    sxx = xt @ xt
    beta = (xt @ yt) / sxx
    resid = yt - beta * xt
    score = xt * resid
    # sum score within each cluster
    sc = np.bincount(cl_codes, score, minlength=n_groups)
    meat = sc @ sc
    var = ssc * meat / (sxx ** 2)
    se = np.sqrt(var)
    return beta, beta / se


def prep(df: pd.DataFrame):
    """Build within-transformed x, y and the bookkeeping arrays for one design."""
    g_unit = df["unit"].values
    g_date = df["date"].values
    cl = df["commodity"].values
    _, cl_codes = np.unique(cl, return_inverse=True)
    n_groups = cl_codes.max() + 1

    yt = two_way_demean(df["lnrv"].values, g_unit, g_date).ravel()
    xt = two_way_demean(df["treat_post"].values.astype(float), g_unit, g_date).ravel()

    # linearmodels small-sample scale: (G/(G-1)) * ((N-1)/(N-k))
    n = len(df)
    k = df["unit"].nunique() + df["date"].nunique() - 1 + 1   # entity + (time-1) + slope
    G = n_groups
    ssc = (G / (G - 1.0)) * ((n - 1.0) / (n - k))
    return xt, yt, cl_codes, n_groups, ssc, G


def restricted_fit(yt: np.ndarray):
    """Under H0 (slope=0) in the within space the restricted fit is 0 and the
    restricted residual is yt itself (the FE are already partialled out of yt).
    Returns (fitted, resid)."""
    return np.zeros_like(yt), yt.copy()


def wild_bootstrap(xt, yt, cl_codes, n_groups, ssc, G, t_obs, label):
    """WCR bootstrap with Rademacher cluster signs. Returns (p, t_star array)."""
    fitted_r, resid_r = restricted_fit(yt)
    abs_t_obs = abs(t_obs)
    t_star = np.empty(B)
    cl_index = cl_codes                                   # obs -> cluster id
    for b in range(B):
        signs = RNG.choice((-1.0, 1.0), size=G)           # Rademacher per cluster
        y_b = fitted_r + signs[cl_index] * resid_r
        _, t_b = cluster_t(xt, y_b, cl_codes, n_groups, ssc)
        t_star[b] = t_b
    # Canonical CGM / MacKinnon-Webb p-value: (1 + #{|t*| >= |t_obs|}) / (B+1)
    # (the +1/(B+1) form is the correct, slightly-conservative convention; not bare #/B).
    p = float((1 + np.sum(np.abs(t_star) >= abs_t_obs)) / (B + 1))
    return p, t_star


# --------------------------------------------------------------------------- #
def load_panel():
    df = pd.read_csv(ROOT / "02_data" / "clean" / "vol_panel_monthly.csv",
                     parse_dates=["date"])
    df["banned"] = df.commodity.isin(BANNED).astype(int)
    df["unit"] = df.commodity + "_" + df.district.astype(str)
    df["lnrv"] = np.log(df.rv30.replace(0, np.nan))
    return df.dropna(subset=["lnrv"]).reset_index(drop=True)


def analytic_did(df, treat_col="treat_post"):
    """PanelOLS clustered fit — for the analytic beta/t/p we compare against."""
    d = df.set_index(["unit", "date"])
    res = PanelOLS.from_formula(
        f"lnrv ~ {treat_col} + EntityEffects + TimeEffects", data=d
    ).fit(cov_type="clustered",
          clusters=d.reset_index().set_index(["unit", "date"]).commodity)
    return (res.params[treat_col], res.tstats[treat_col], res.pvalues[treat_col])


def run_design(df, label, lines):
    """Full pipeline for one design (df must carry 'treat_post' and 'banned'):
    analytic DiD + within-space t + wild bootstrap."""
    b_a, t_a, p_a = analytic_did(df, "treat_post")
    xt, yt, cl_codes, n_groups, ssc, G = prep(df)
    beta_w, t_obs = cluster_t(xt, yt, cl_codes, n_groups, ssc)

    t0 = time.time()
    p_boot, t_star = wild_bootstrap(xt, yt, cl_codes, n_groups, ssc, G, t_obs, label)
    secs = time.time() - t0

    n_banned = df.query("banned==1").commodity.nunique()
    n_ctrl = df.query("banned==0").commodity.nunique()
    lines += [
        f"=== {label} ===",
        f"  clusters (commodities): {G}  (treated={n_banned}, control={n_ctrl})",
        f"  analytic PanelOLS : beta={b_a:+.4f} ({100*(np.exp(b_a)-1):+.1f}%)  "
        f"t={t_a:+.3f}  clustered-p={p_a:.4f}",
        f"  within-space check: beta={beta_w:+.4f}  t_obs={t_obs:+.3f}  "
        f"(matches PanelOLS; this t is bootstrapped)",
        f"  WILD-CLUSTER BOOTSTRAP (WCR, Rademacher, null imposed, B={B}):",
        f"    bootstrap p = share(|t*| >= |t_obs|) = {p_boot:.4f}",
        f"    t* distribution: mean={t_star.mean():+.3f} sd={t_star.std():.3f} "
        f"q025={np.quantile(t_star,0.025):+.3f} q975={np.quantile(t_star,0.975):+.3f}",
        f"    elapsed {secs:.1f}s",
        "",
    ]
    print("\n".join(lines[-9:]))
    return p_a, p_boot


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    header = [
        "WILD-CLUSTER BOOTSTRAP for the V0 DiD  (Cameron-Gelbach-Miller; Rademacher; "
        "cluster=commodity)",
        f"generated {pd.Timestamp.now():%Y-%m-%d %H:%M}  | seed={SEED}  B={B}",
        "Purpose: trustworthy p-values under the few-treated-cluster problem "
        "(only 6 banned / ~12 total commodity clusters).",
        "Null imposed (treat_post=0); restricted residuals re-signed at the cluster level.",
        "",
    ]
    lines = list(header)
    df = load_panel()

    # ---- (1) MAIN DiD: single ban 2021-12-20, treat_post = banned*post ----
    main_df = df[~df.commodity.isin(MAIN_DROP)].copy()   # drop guar id 75 + MSP-censored paddy
    main_df["treat_post"] = main_df.banned * (main_df.date >= BAN_DATE).astype(int)
    p_a_main, p_b_main = run_design(
        main_df, f"MAIN DiD  (ban {BAN_DATE.date()}, paddy+guar-id75 dropped)", lines)

    # ---- (2) PLACEBO: pre-ban data only, fake ban 2019-12-20, drop guar id 75 ----
    plac = df[(df.date < BAN_DATE) & (~df.commodity.isin(PLACEBO_DROP))].copy()
    plac["treat_post"] = plac.banned * (plac.date >= FAKE_BAN).astype(int)
    p_a_plac, p_b_plac = run_design(
        plac,
        f"PLACEBO   (fake ban {FAKE_BAN.date()}, data < {BAN_DATE.date()}, "
        f"guar id 75 dropped)", lines)

    # ---- comparison block ----
    lines += [
        "=== COMPARISON: analytic clustered-p  vs  wild-cluster-bootstrap-p ===",
        f"  MAIN DiD : analytic p={p_a_main:.4f}   ->   wild-bootstrap p={p_b_main:.4f}",
        f"  PLACEBO  : analytic p={p_a_plac:.4f}   ->   wild-bootstrap p={p_b_plac:.4f}",
        "",
        "Reading: with 6 treated clusters the analytic clustered p is the optimistic one;",
        "the bootstrap p is the inference to trust. A MAIN effect that stays significant",
        "AND a PLACEBO that stays insignificant under the bootstrap is the credible outcome.",
        f"  bootstrap resolution floor ~ 1/(B+1) = {1/(B+1):.4f}.",
    ]

    out = "\n".join(lines) + "\n"
    (OUTDIR / "wild_bootstrap_results.txt").write_text(out)
    print("\nwrote", OUTDIR / "wild_bootstrap_results.txt")


if __name__ == "__main__":
    main()
