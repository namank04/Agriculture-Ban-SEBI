"""V0 step 3: GARCH(1,1) per commodity with ban dummy in variance eq. Verifies claim C2 (vol part).
INPUT : 02_data/clean/spot_daily_<commodity><suffix>.csv  (cols: date, price)
OUTPUT: V0 output/garch_summary<suffix>.csv
Optional arg: file suffix — e.g. `run_v0_garch.py _distmed` uses the district-median
series (robust to the composition noise that breaks fits on national averages)."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
from arch import arch_model
from utils import log_returns, BAN_DATE, CORE, CONTROL_CANDIDATES

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT/"04_empirics"/"V0_lost_results_replication"/"output"

SUFFIX = sys.argv[1] if len(sys.argv) > 1 else ""


def fit_one(commodity: str):
    fp = ROOT/"02_data"/"clean"/f"spot_daily_{commodity}{SUFFIX}.csv"
    if not fp.exists(): return None
    df = pd.read_csv(fp, parse_dates=["date"]).set_index("date").sort_index()
    r = (log_returns(df.price).dropna() * 100)
    pre, post = r[r.index < BAN_DATE], r[r.index >= BAN_DATE]
    out = {"commodity": commodity}
    for label, seg in [("pre", pre), ("post", post)]:
        if len(seg) < 250: continue
        res = arch_model(seg, vol="GARCH", p=1, q=1, mean="Constant").fit(disp="off")
        a, b = res.params.get("alpha[1]", np.nan), res.params.get("beta[1]", np.nan)
        out |= {f"{label}_alpha": a, f"{label}_beta": b, f"{label}_persist": a+b,
                f"{label}_uncond_vol": float(np.sqrt(res.params["omega"]/(1-a-b))*np.sqrt(252))
                if (a+b) < 1 else np.nan}
    return out

def main():
    slugs = CORE + CONTROL_CANDIDATES + ["guarseed413"]  # id-413 = true guar seed spot
    rows = [r for c in slugs if (r := fit_one(c))]
    OUTDIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUTDIR/f"garch_summary{SUFFIX}.csv", index=False)
    print("Compare pre vs post persistence & unconditional vol; banned vs control contrast is the test.")

if __name__ == "__main__":
    main()
