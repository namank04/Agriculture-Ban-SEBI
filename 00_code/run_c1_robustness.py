"""C1 robustness + honest few-cluster inference (referee-driven refinement).
Re-runs the PRIMARY DiD (paddy + guar id-75 dropped) under (a) district-liquidity / outlier
filters and (b) LEAVE-ONE-TREATED-COMMODITY-OUT, and reports BOTH the default clustered p
AND the few-cluster CR1 p (t-reference with G-1 = 9 dof) — because with only ~10 commodity
clusters (5 treated) the asymptotic/large-df p is over-optimistic.

INPUT : 02_data/clean/vol_panel_monthly.csv
OUTPUT: 04_empirics/H1_volatility/output/c1_robustness.csv (+ console)
"""
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
from linearmodels.panel import PanelOLS
from utils import BANNED, BAN_DATE, EXCLUDE_PRIMARY

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "04_empirics" / "H1_volatility" / "output"


def did(df):
    """Two-way-FE DiD on lnrv, clustered by commodity. Returns dict with default + few-cluster p."""
    d = df.copy()
    d["banned"] = d.commodity.isin(BANNED).astype(int)
    d["unit"] = d.commodity + "_" + d.district.astype(str)
    d["lnrv"] = np.log(d.rv30.replace(0, np.nan))
    d = d.dropna(subset=["lnrv"]).set_index(["unit", "date"])
    d["treat_post"] = d.banned * (d.index.get_level_values("date") >= BAN_DATE).astype(int)
    clusters = d.reset_index().set_index(["unit", "date"]).commodity
    res = PanelOLS.from_formula("lnrv ~ treat_post + EntityEffects + TimeEffects",
                                data=d).fit(cov_type="clustered", clusters=clusters)
    b, t = res.params["treat_post"], res.tstats["treat_post"]
    G = int(clusters.nunique())
    cr1_p = float(2 * stats.t.sf(abs(t), df=G - 1))      # honest few-cluster reference: t(G-1)
    return {"beta": round(b, 4), "effect_pct": round(100 * (np.exp(b) - 1), 1),
            "p_default": round(float(res.pvalues["treat_post"]), 4),
            "p_cr1_t(G-1)": round(cr1_p, 4), "G_clusters": G,
            "nobs": int(res.nobs), "n_units": int(d.index.get_level_values("unit").nunique())}


def main():
    df = pd.read_csv(ROOT / "02_data" / "clean" / "vol_panel_monthly.csv", parse_dates=["date"])
    df = df[~df.commodity.isin(EXCLUDE_PRIMARY)]            # primary spec: drop paddy + guar id75
    df["unit"] = df.commodity + "_" + df.district.astype(str)
    mo = df.groupby("unit").size()
    treated = [c for c in ["chana", "wheat", "mustard", "soybean", "moong"] if c in df.commodity.unique()]

    def winsor(d, p=0.99):
        d = d.copy()
        d.rv30 = np.minimum(d.rv30, d.groupby("commodity").rv30.transform(lambda s: s.quantile(p)))
        return d

    specs = {
        "baseline (primary)":             df,
        "winsorize rv30 @p99":            winsor(df),
        "drop rv30>5 (noisy tail)":       df[df.rv30 <= 5],
        "min 24 months/district":         df[df.unit.isin(mo[mo >= 24].index)],
        "min 36 months/district":         df[df.unit.isin(mo[mo >= 36].index)],
        "robust (min24 + winsor + tail)": winsor(df[(df.rv30 <= 5) & (df.unit.isin(mo[mo >= 24].index))]),
    }
    # leave-one-treated-commodity-out (does the effect survive dropping any single banned commodity?)
    for c in treated:
        specs[f"ex-{c}"] = df[df.commodity != c]

    rows = []
    print(f"{'spec':34s} {'effect':>8s} {'p_dflt':>7s} {'p_CR1':>7s} {'G':>3s} {'nobs':>8s}")
    for name, d in specs.items():
        r = did(d); r = {"spec": name, **r}
        rows.append(r)
        flag = "  <- few-cluster p not sig" if r["p_cr1_t(G-1)"] >= 0.05 else ""
        print(f"{name:34s} {r['effect_pct']:+7.1f}% {r['p_default']:6.4f} {r['p_cr1_t(G-1)']:6.4f} "
              f"{r['G_clusters']:3d} {r['nobs']:8d}{flag}")

    OUTDIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUTDIR / "c1_robustness.csv", index=False)
    print(f"\nwrote {OUTDIR/'c1_robustness.csv'}")
    print("READ: 'effect' should stay clearly negative across filters AND leave-one-out (esp. ex-wheat,")
    print("the MSP-flagged largest contributor). p_CR1 (t with G-1 dof) is the HONEST few-cluster p;")
    print("p_default is the over-optimistic large-df value and should not be the headline.")


if __name__ == "__main__":
    main()
