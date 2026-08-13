"""V0 step 4: pre-registered falsification checks for C1 (spec section B).
1. PLACEBO DATE — pre-ban data only (< 2021-12-20), fake ban at 2019-12-20:
   a real design should show ~nothing.
2. JOINT LEAD TEST — event-study leads m_-18..m_-2 jointly zero (Wald);
   rejection kills the DiD per the pre-registered rule.
Guar id 75 (gum-contaminated) is dropped; id 413 serves as the guar control.
Still pending separately: wild-cluster bootstrap (11 commodity clusters).

INPUT : 02_data/clean/vol_panel_monthly.csv
OUTPUT: V0 output/placebo_results.txt (+ console)
"""
from pathlib import Path

import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

from utils import BANNED, BAN_DATE

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "04_empirics" / "V0_lost_results_replication" / "output"
FAKE_BAN = pd.Timestamp("2019-12-20")
DROP = {"guar", "paddy"}  # guar id 75 gum-contaminated (use guarseed413); paddy MSP-censored (40.3% flat) — decision_log 2026-06-21


def load():
    df = pd.read_csv(ROOT / "02_data" / "clean" / "vol_panel_monthly.csv",
                     parse_dates=["date"])
    df = df[~df.commodity.isin(DROP)]
    df["banned"] = df.commodity.isin(BANNED).astype(int)
    df["unit"] = df.commodity + "_" + df.district.astype(str)
    df["lnrv"] = np.log(df.rv30.replace(0, np.nan))
    return df.dropna(subset=["lnrv"])


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    lines = []
    df = load()

    # ---- 1. placebo: pre-ban window only, fake ban Dec-2019
    pre = df[df.date < BAN_DATE].copy()
    pre["treat_post"] = pre.banned * (pre.date >= FAKE_BAN).astype(int)
    pre = pre.set_index(["unit", "date"])
    res = PanelOLS.from_formula("lnrv ~ treat_post + EntityEffects + TimeEffects",
                                data=pre).fit(
        cov_type="clustered", clusters=pre.reset_index().set_index(["unit", "date"]).commodity)
    b, p = res.params["treat_post"], res.pvalues["treat_post"]
    lines.append(f"PLACEBO (fake ban {FAKE_BAN.date()}, data < {BAN_DATE.date()}): "
                 f"beta={b:.4f} ({100*(np.exp(b)-1):+.1f}%), p={p:.4f}")
    lines.append("  pass rule: ~zero and insignificant; a 'significant effect' here "
                 "means the design finds effects where none can exist.")

    # ---- 2. joint lead test on the event-study leads
    df2 = df.copy()
    df2["rel_m"] = ((df2.date.dt.year - BAN_DATE.year) * 12
                    + (df2.date.dt.month - BAN_DATE.month)).clip(-18, 18)
    dummies = pd.get_dummies(df2.rel_m, prefix="m").drop(columns=["m_-1"])
    inter = dummies.mul(df2.banned, axis=0).astype(float)
    idx = df2.set_index(["unit", "date"]).index
    X = inter.set_index(idx)
    es = PanelOLS(df2.set_index(["unit", "date"]).lnrv, X,
                  entity_effects=True, time_effects=True).fit(
        cov_type="clustered", clusters=df2.set_index(["unit", "date"]).commodity)
    # 17 individual leads exceed the rank of an 11-cluster covariance (G-1=10
    # testable restrictions) -> Wald is degenerate. Test half-year LEAD BINS instead.
    df2["lead_bin"] = pd.cut(df2.rel_m, bins=[-19, -13, -7, -2],
                             labels=["lead_18_13", "lead_12_7", "lead_6_2"])
    bins = pd.get_dummies(df2.lead_bin).mul(df2.banned, axis=0).astype(float)
    Xb = pd.concat([bins, dummies.filter(regex=r"m_\d").mul(df2.banned, axis=0)
                    .astype(float)], axis=1).set_index(idx)
    esb = PanelOLS(df2.set_index(["unit", "date"]).lnrv, Xb,
                   entity_effects=True, time_effects=True).fit(
        cov_type="clustered", clusters=df2.set_index(["unit", "date"]).commodity)
    lead_cols = ["lead_18_13", "lead_12_7", "lead_6_2"]
    R = np.zeros((len(lead_cols), len(esb.params)))
    for i, c in enumerate(lead_cols):
        R[i, list(esb.params.index).index(c)] = 1.0
    w = esb.wald_test(restriction=R, value=np.zeros(len(lead_cols)))
    for c in lead_cols:
        lines.append(f"  {c}: beta={esb.params[c]:+.4f}, p={esb.pvalues[c]:.4f}")
    lines.append(f"JOINT LEAD TEST (3 half-year lead bins = 0): "
                 f"stat={w.stat:.2f}, p={w.pval:.4f}")
    lines.append("  pre-registered rule: rejection -> DiD dead, synthetic control primary.")

    out = "\n".join(lines)
    (OUTDIR / "placebo_results.txt").write_text(out + "\n")
    print(out)


if __name__ == "__main__":
    main()
