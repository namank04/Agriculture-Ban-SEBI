"""Download international daily series (stream 8) via Yahoo Finance -> raw/international/.
Series: CBOT wheat front-month continuous (ZW=F), USD/MYR (MYR=X).
NOT here: Bursa FCPO (not on Yahoo -> vendor route), RBI USD/INR reference rate (RBI source).
Raw files are saved as downloaded (no transformation beyond column flattening).
Usage: python download_international.py
Output: 02_data/raw/international/<name>_daily_2017_2025.csv
        + diagnostics printed to stdout (paste into data_log notes)."""
from pathlib import Path
import numpy as np
import pandas as pd
import yfinance as yf

START, END = "2017-01-01", "2026-01-01"  # spec window: 2017-2025 inclusive

SERIES = {
    # out_name: (yahoo ticker, description, units)
    "cbot_wheat": ("ZW=F", "CBOT wheat front-month continuous, daily OHLCV", "US cents per bushel"),
    "usdmyr": ("MYR=X", "USD/MYR spot reference, daily OHLC", "MYR per USD"),
}

def fetch(ticker: str) -> pd.DataFrame:
    df = yf.Ticker(ticker).history(start=START, end=END, auto_adjust=False)
    if df.empty:
        raise RuntimeError(f"no data returned for {ticker}")
    df = df.reset_index()
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None).dt.normalize()
    keep = [c for c in ("date", "open", "high", "low", "close", "volume") if c in df.columns]
    df = (df[keep].dropna(subset=["close"])
            .sort_values("date").drop_duplicates(subset="date", keep="last")
            .reset_index(drop=True))
    return df

def diagnostics(df: pd.DataFrame, name: str, units: str):
    print(f"\n=== DIAGNOSTICS: {name} ===")
    print(f"span: {df.date.min().date()} -> {df.date.max().date()}, rows: {len(df)}")
    print("rows/year:", dict(df.groupby(df.date.dt.year).size()))
    flat = (df[["open", "high", "low", "close"]].nunique(axis=1) == 1).mean()
    print(f"O=H=L=C rows: {flat:.1%}")
    r = np.log(df.close).diff()
    print(f"daily log-ret: mean {r.mean():.5f}, sd {r.std():.4f}, |max| {r.abs().max():.4f}")
    big = df.loc[r.abs() > 0.05, ["date", "close"]]
    print(f"jumps >5% (roll artifacts/events): {len(big)}")
    if len(big): print(big.tail(8).to_string(index=False))
    bd = pd.bdate_range(df.date.min(), df.date.max())
    print(f"missing business days vs naive calendar: {len(bd.difference(pd.DatetimeIndex(df.date)))}")
    print(f"unit sanity ({units}): close min {df.close.min():.2f}, median {df.close.median():.2f}, "
          f"max {df.close.max():.2f}")

if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parents[1] / "02_data" / "raw" / "international"
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, (ticker, desc, units) in SERIES.items():
        df = fetch(ticker)
        diagnostics(df, f"{name} ({ticker})", units)
        out = out_dir / f"{name}_daily_2017_2025.csv"
        if out.exists():
            print(f"[skip-write] {out} already exists — raw is immutable; delete manually to refresh")
            continue
        df.to_csv(out, index=False)
        print(f"saved -> {out}")
