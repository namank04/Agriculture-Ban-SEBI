"""Reverse-engineer Investing.com's continuous-contract (c1/c2/c3) roll convention.

Logic: on a roll day, the c1 series stops tracking the expiring contract and adopts
the next one — so c1_t should sit close to c2_{t-1} while showing a sizeable jump
vs c1_{t-1}. We flag such days, then ask: where in the month do rolls cluster
(expiry-day roll vs early roll)? And does c1 go thin/flat in the days just before
a roll (i.e., did the vendor hold the front contract into its illiquid tail)?

Usage: python explore_roll_convention.py
Reads: 02_data/clean/futures_daily_<commodity>_c{1,2}.csv
Prints summary per commodity; no files written.
"""
from pathlib import Path
import numpy as np
import pandas as pd

CLEAN = Path(__file__).resolve().parents[1] / "02_data" / "clean"
COMMODITIES = ["castor", "guar", "jeera", "turmeric", "kapas"]

NEAR_C2 = 0.005   # c1_t within 0.5% of c2_{t-1}  -> "adopted next contract"
JUMP = 0.015      # and c1 day-on-day move > 1.5% -> visible splice


def load(name: str) -> pd.DataFrame | None:
    p = CLEAN / f"futures_daily_{name}.csv"
    if not p.exists():
        return None
    df = pd.read_csv(p, parse_dates=["date"])
    return df.set_index("date")


def analyze(com: str) -> None:
    c1, c2 = load(f"{com}_c1"), load(f"{com}_c2")
    if c1 is None or c2 is None:
        print(f"\n--- {com}: missing leg files, skipped")
        return
    m = pd.DataFrame({
        "c1": c1.close, "c2": c2.close,
        "c1_open": c1.open, "c1_high": c1.high, "c1_low": c1.low,
        "c1_vol": c1.volume,
    }).dropna(subset=["c1", "c2"])
    m["c1_prev"], m["c2_prev"] = m.c1.shift(1), m.c2.shift(1)
    m["ret"] = np.log(m.c1 / m.c1_prev)
    m["flat"] = (m[["c1_open", "c1_high", "c1_low", "c1"]].nunique(axis=1) == 1)

    roll = (
        ((m.c1 / m.c2_prev - 1).abs() < NEAR_C2)
        & (m.ret.abs() > JUMP)
        & ((m.c1 - m.c1_prev).abs() > (m.c1 - m.c2_prev).abs())
    )
    rolls = m[roll]
    print(f"\n=== {com.upper()} ===  ({len(m)} matched days, {len(rolls)} detected rolls)")
    if not len(rolls):
        print("  no rolls detected — thresholds may be too tight or splice is seamless")
        return

    months = (m.index.max().to_period('M') - m.index.min().to_period('M')).n + 1
    print(f"  rolls/month: {len(rolls)/months:.2f}  (1.0 => every monthly expiry detected)")
    dom = rolls.index.day
    print(f"  day-of-month of rolls: median {np.median(dom):.0f}, "
          f"IQR [{np.percentile(dom,25):.0f}-{np.percentile(dom,75):.0f}], "
          f"range [{dom.min()}-{dom.max()}]")
    hist = pd.Series(dom).value_counts().sort_index()
    print("  day-of-month histogram:", dict(hist))
    print(f"  median |roll-day jump|: {rolls.ret.abs().median():.2%} "
          f"(these are splice artifacts, NOT market moves)")

    # behaviour of c1 in the 5 days BEFORE a roll vs unconditional
    pre_flags, pre_vols = [], []
    pos = m.index.get_indexer(rolls.index)
    for p in pos:
        w = m.iloc[max(0, p - 5):p]
        pre_flags.append(w.flat.mean())
        pre_vols.append(w.c1_vol.mean())
    uncond_flat = m.flat.mean()
    uncond_vol = m.c1_vol.mean()
    print(f"  flat-quote share, 5d pre-roll: {np.nanmean(pre_flags):.1%} "
          f"vs unconditional {uncond_flat:.1%}")
    if np.isfinite(uncond_vol) and uncond_vol > 0:
        print(f"  volume, 5d pre-roll: {np.nanmean(pre_vols)/uncond_vol:.0%} of unconditional avg")


if __name__ == "__main__":
    for com in COMMODITIES:
        analyze(com)
