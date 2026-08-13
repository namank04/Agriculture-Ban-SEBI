"""Clean Investing.com historical futures exports -> pipeline format.
Handles: BOM, DD-MM-YYYY dates, comma-thousands, Vol strings (1.2K/3.4M/empty), Change %.
Banned commodities are HARD-TRUNCATED at the suspension date (post-ban quotes are stale).
Usage: python clean_investing_futures.py <raw_csv> <commodity_name>
Output: 02_data/clean/futures_daily_<commodity>.csv  (date, open, high, low, close, volume)
        + diagnostics printed to stdout (paste into data_log notes)."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

BAN_DATE = pd.Timestamp("2021-12-20")
BANNED = {"wheat", "chana", "cpo", "mustard", "soybean", "paddy", "moong"}

def parse_vol(v):
    if pd.isna(v) or str(v).strip() in ("", "-"):
        return np.nan
    s = str(v).strip().upper().replace(",", "")
    mult = 1.0
    if s.endswith("K"): mult, s = 1e3, s[:-1]
    elif s.endswith("M"): mult, s = 1e6, s[:-1]
    elif s.endswith("B"): mult, s = 1e9, s[:-1]
    try:
        return float(s) * mult
    except ValueError:
        return np.nan

def clean(raw_path: str, commodity: str) -> pd.DataFrame:
    df = pd.read_csv(raw_path, encoding="utf-8-sig")
    df.columns = [c.strip().lower().replace(" %", "_pct").replace(".", "") for c in df.columns]
    df = df.rename(columns={"price": "close", "vol": "volume"})
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", ""), errors="coerce")
    df["volume"] = df["volume"].map(parse_vol) if "volume" in df else np.nan
    df = (df.dropna(subset=["date", "close"])
            .sort_values("date")
            .drop_duplicates(subset="date", keep="last")
            .reset_index(drop=True))
    # base commodity decides ban status: leg-suffixed names (cpo_c1, wheat_c2, ...)
    # must truncate exactly like their parent commodity
    if commodity.lower().split("_")[0] in BANNED:
        n_before = len(df)
        df = df[df.date <= BAN_DATE]
        print(f"[truncate] {commodity}: banned -> kept {len(df)}/{n_before} rows (<= {BAN_DATE.date()})")
    return df[["date", "open", "high", "low", "close", "volume"]]

def diagnostics(df: pd.DataFrame, commodity: str):
    print(f"\n=== DIAGNOSTICS: {commodity} ===")
    print(f"span: {df.date.min().date()} -> {df.date.max().date()}, rows: {len(df)}")
    per_year = df.groupby(df.date.dt.year).size()
    print("rows/year:", dict(per_year))
    flat = (df[["open", "high", "low", "close"]].nunique(axis=1) == 1).mean()
    print(f"O=H=L=C rows: {flat:.1%}  (high share => single daily quote; Parkinson vol NOT usable)")
    vol_ok = df.volume.notna() & (df.volume > 0)
    print(f"usable volume rows: {vol_ok.mean():.1%}")
    r = np.log(df.close).diff()
    print(f"daily log-ret: mean {r.mean():.5f}, sd {r.std():.4f}, |max| {r.abs().max():.4f}")
    big = df.loc[r.abs() > 0.05, ["date", "close"]]
    print(f"jumps >5% (possible roll artifacts/events): {len(big)}")
    if len(big): print(big.tail(8).to_string(index=False))
    # weekday gaps
    bd = pd.bdate_range(df.date.min(), df.date.max())
    print(f"missing business days vs naive calendar: {len(bd.difference(pd.DatetimeIndex(df.date)))} "
          f"(includes Indian holidays — rough gauge only)")

if __name__ == "__main__":
    raw, name = sys.argv[1], sys.argv[2].lower()
    out_dir = Path(__file__).resolve().parents[1] / "02_data" / "clean"
    out_dir.mkdir(parents=True, exist_ok=True)
    d = clean(raw, name)
    diagnostics(d, name)
    out = out_dir / f"futures_daily_{name}.csv"
    d.to_csv(out, index=False)
    print(f"\nsaved -> {out}")
