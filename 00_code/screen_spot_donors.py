"""Screen candidate SPOT control commodities as SCM donors for C1 spot-volatility.

Trading-day-corrected clean data (rebuilt 2026-06-21). For each candidate control:
  (a) correlation of spot PRICE level and monthly rv30 with chana and with wheat
  (b) coverage: rows, span, #districts, missingness
  (c) contamination signals: flat-return share, jumps, unit-break scan, level outliers

Reads ONLY 02_data/clean/. Does not write — prints a report.

Series used:
  spot_daily_<c>.csv           CEDA NATIONAL daily spot (date, price)  -> price-level corr
  spot_daily_<c>_distmed.csv   cross-district-median robust national   -> robustness check
  vol_panel_monthly.csv        district rv30 panel (commodity,state,district,date,rv30,post)
                               -> rv30 corr (collapsed to national month median) + coverage
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "02_data" / "clean"

CANDIDATES = ["castor", "jeera", "turmeric", "guarseed413", "guar", "cotton"]
BANNED_REF = ["chana", "wheat"]
ALL_BANNED = ["chana", "wheat", "mustard", "soybean", "moong", "paddy"]


def load_spot(slug, suffix=""):
    fp = CLEAN / f"spot_daily_{slug}{suffix}.csv"
    if not fp.exists():
        return None
    df = pd.read_csv(fp, parse_dates=["date"]).sort_values("date")
    return df.set_index("date")["price"]


def log_ret(s):
    return np.log(s).diff()


# ---- monthly rv30, national (district-median across the panel) ----
panel = pd.read_csv(CLEAN / "vol_panel_monthly.csv", parse_dates=["date"])
panel = panel[panel.commodity != "commodity"]  # stray header row guard
panel["rv30"] = pd.to_numeric(panel["rv30"], errors="coerce")

# national monthly rv30 = median across districts (robust collapse)
rv_nat = (panel.groupby(["commodity", "date"])["rv30"].median()
          .unstack("commodity").sort_index())

print("=" * 100)
print("MONTHLY rv30 — national (cross-district median) — overlap & corr vs chana/wheat")
print("=" * 100)


def corr_pair(a, b, frame):
    """Pearson corr on common non-NaN index; returns (corr, n)."""
    if a not in frame.columns or b not in frame.columns:
        return np.nan, 0
    sa = frame[a]
    sb = frame[b]
    if isinstance(sa, pd.DataFrame):
        sa = sa.iloc[:, 0]
    if isinstance(sb, pd.DataFrame):
        sb = sb.iloc[:, 0]
    sub = pd.concat([sa.rename("a"), sb.rename("b")], axis=1).dropna()
    if len(sub) < 8:
        return np.nan, len(sub)
    return sub["a"].corr(sub["b"]), len(sub)


rv_rows = []
for c in CANDIDATES + ALL_BANNED:
    if c not in rv_nat.columns:
        rv_rows.append((c, np.nan, 0, np.nan, 0))
        continue
    rc, nc = corr_pair(c, "chana", rv_nat)
    rw, nw = corr_pair(c, "wheat", rv_nat)
    rv_rows.append((c, rc, nc, rw, nw))
print(f"{'commodity':14s} {'rv30~chana':>11s} {'n':>4s}   {'rv30~wheat':>11s} {'n':>4s}")
for c, rc, nc, rw, nw in rv_rows:
    print(f"{c:14s} {rc:11.3f} {nc:4d}   {rw:11.3f} {nw:4d}")

# ---- also rv30 corr on log-DIFFERENCED rv (shock comovement, less trend-driven) ----
print("\n--- rv30 corr in first-differences (de-trended shock comovement) ---")
rv_d = rv_nat.diff()
print(f"{'commodity':14s} {'d_rv~chana':>11s} {'n':>4s}   {'d_rv~wheat':>11s} {'n':>4s}")
for c in CANDIDATES:
    if c not in rv_d.columns:
        print(f"{c:14s}  (absent)")
        continue
    rc, nc = corr_pair(c, "chana", rv_d)
    rw, nw = corr_pair(c, "wheat", rv_d)
    print(f"{c:14s} {rc:11.3f} {nc:4d}   {rw:11.3f} {nw:4d}")

# ---- PRICE-LEVEL correlation (national spot) ----
print("\n" + "=" * 100)
print("DAILY SPOT PRICE — national series — corr vs chana/wheat (levels and log-returns)")
print("=" * 100)
spot = {}
for c in CANDIDATES + BANNED_REF:
    s = load_spot(c)
    if s is not None:
        spot[c] = s
spot_df = pd.DataFrame(spot).sort_index()
ret_df = spot_df.apply(log_ret)

print(f"{'commodity':14s} {'PXlvl~chana':>11s} {'PXlvl~wheat':>11s}   "
      f"{'ret~chana':>10s} {'ret~wheat':>10s} {'ovlp_days':>9s}")
for c in CANDIDATES:
    if c not in spot_df.columns:
        print(f"{c:14s}  (absent)")
        continue
    lc, nlc = corr_pair(c, "chana", spot_df)
    lw, nlw = corr_pair(c, "wheat", spot_df)
    rc, _ = corr_pair(c, "chana", ret_df)
    rw, _ = corr_pair(c, "wheat", ret_df)
    print(f"{c:14s} {lc:11.3f} {lw:11.3f}   {rc:10.3f} {rw:10.3f} {nlc:9d}")

# ---- COVERAGE & CONTAMINATION per candidate ----
print("\n" + "=" * 100)
print("COVERAGE & CONTAMINATION (national spot + district panel)")
print("=" * 100)
for c in CANDIDATES:
    s_nat = load_spot(c)
    s_dm = load_spot(c, "_distmed")
    pc = panel[panel.commodity == c]
    print(f"\n### {c}")
    if s_nat is None:
        print("  national spot MISSING")
    else:
        span = f"{s_nat.index.min().date()}..{s_nat.index.max().date()}"
        # calendar-day grid expected weekdays in span
        cal_wd = pd.bdate_range(s_nat.index.min(), s_nat.index.max())
        miss = 1 - len(s_nat) / len(cal_wd)
        r = log_ret(s_nat)
        flat = (r.abs() < 1e-9).mean()
        jumps20 = int((r.abs() > 0.20).sum())
        jumps10 = int((r.abs() > 0.10).sum())
        # unit-break scan: largest single-day level jump and where
        big = r.abs().sort_values(ascending=False).head(3)
        print(f"  national: {len(s_nat)} rows  {span}  weekday-miss {miss:5.1%}  "
              f"flat-ret {flat:5.1%}  |ret|>10%: {jumps10}  >20%: {jumps20}")
        print(f"    px p1/p50/p99: {s_nat.quantile(.01):,.0f}/{s_nat.median():,.0f}/"
              f"{s_nat.quantile(.99):,.0f} Rs/qtl   max|ret| days: "
              + ", ".join(f"{d.date()}={v:.0%}" for d, v in big.items()))
    if s_dm is not None and s_nat is not None:
        common = pd.concat([s_nat.rename("nat"), s_dm.rename("dm")], axis=1).dropna()
        if len(common) > 8:
            print(f"  nat-vs-distmed level corr {common.nat.corr(common.dm):.3f}  "
                  f"(level agreement; low => national-series composition contamination)")
    if len(pc):
        ndist = pc.district.nunique()
        mspan = f"{pc.date.min().date()}..{pc.date.max().date()}"
        rv = pc.rv30.dropna()
        print(f"  panel: {ndist} districts, {len(pc):,} cell-months, {mspan}  "
              f"rv30 p1/p50/p99: {rv.quantile(.01):.2f}/{rv.median():.2f}/{rv.quantile(.99):.2f}")
    else:
        print("  panel: ABSENT")

# ---- ban-reference internal corr (sanity: do banned comove with each other?) ----
print("\n" + "=" * 100)
print("SANITY — rv30 corr AMONG banned (chana vs others) for benchmark scale")
print("=" * 100)
for c in [x for x in ALL_BANNED if x != "chana"]:
    if c in rv_nat.columns:
        rc, nc = corr_pair(c, "chana", rv_nat)
        print(f"  chana ~ {c:10s}: rv30 corr {rc:6.3f} (n={nc})")
