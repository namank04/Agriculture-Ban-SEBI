"""V0 step 2: DiD + event study on the volatility panel. Verifies claim C1 (+8-10% vol).
INPUT : 02_data/clean/vol_panel_monthly.csv  (+ banned flag added here)
OUTPUT: 04_empirics/V0_lost_results_replication/output/{did_results.txt, event_study.png}
Optional args: [panel_csv_name] [output_suffix] [drop_commodity ...] — e.g.
  run_v0_did.py vol_panel_monthly_national.csv national guar
runs the national first pass excluding guar (data-quality flag 2026-06-12)."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from linearmodels.panel import PanelOLS
from utils import BANNED, BAN_DATE

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "04_empirics" / "V0_lost_results_replication" / "output"

def main():
    panel_name = sys.argv[1] if len(sys.argv) > 1 else "vol_panel_monthly.csv"
    suffix = f"_{sys.argv[2]}" if len(sys.argv) > 2 else ""
    drop = set(sys.argv[3:])
    df = pd.read_csv(ROOT/"02_data"/"clean"/panel_name, parse_dates=["date"])
    if drop:
        df = df[~df.commodity.isin(drop)]
        print(f"dropped: {sorted(drop)}")
    df["banned"] = df.commodity.isin(BANNED).astype(int)
    df["unit"] = df.commodity + "_" + df.district.astype(str)
    df["lnrv"] = np.log(df.rv30.replace(0, np.nan))
    df = df.dropna(subset=["lnrv"]).set_index(["unit", "date"])
    df["treat_post"] = df.banned * df.post

    # ---- DiD: log vol -> beta is ~% effect. Cluster by commodity (few clusters -> see NOTE)
    m = PanelOLS.from_formula("lnrv ~ treat_post + EntityEffects + TimeEffects", data=df)
    res = m.fit(cov_type="clustered", clusters=df.reset_index().set_index(["unit","date"]).commodity)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR/f"did_results{suffix}.txt").write_text(str(res))
    beta = res.params["treat_post"]
    print(f"DiD beta = {beta:.4f}  ->  vol effect ≈ {100*(np.exp(beta)-1):.1f}% "
          f"(claim C1 band to confirm: +4% to +16%, p<0.05)")
    # NOTE: few treated clusters -> run wild-cluster bootstrap (wildboottest pkg) before trusting p.

    # ---- Event study: monthly leads/lags +-18m
    df2 = df.reset_index()
    df2["rel_m"] = ((df2.date.dt.year - BAN_DATE.year)*12 + (df2.date.dt.month - BAN_DATE.month)).clip(-18, 18)
    dummies = pd.get_dummies(df2.rel_m, prefix="m").drop(columns=["m_-1"])  # omit t=-1
    inter = dummies.mul(df2.banned, axis=0)
    X = inter.set_index(df2.set_index(["unit","date"]).index)
    es = PanelOLS(df2.set_index(["unit","date"]).lnrv, X, entity_effects=True, time_effects=True
                  ).fit(cov_type="clustered", clusters=df2.set_index(["unit","date"]).commodity)
    coefs = es.params.filter(like="m_")
    order = sorted(coefs.index, key=lambda c: int(c.split("_")[1]))
    xs = [int(c.split("_")[1]) for c in order]
    plt.figure(figsize=(9,4)); plt.axvline(0, ls="--", c="gray"); plt.axhline(0, c="k", lw=.5)
    plt.errorbar(xs, coefs[order], yerr=1.96*es.std_errors[order], fmt="o", ms=3)
    plt.title("Event study: log spot volatility, banned vs control"); plt.xlabel("months from ban")
    plt.tight_layout(); plt.savefig(OUTDIR/f"event_study{suffix}.png", dpi=150)
    print("Pre-trend check: leads (m_-18..m_-2) should be ~0 and jointly insignificant.")

if __name__ == "__main__":
    main()
