"""Clean CEDA Agmarknet NATIONAL spot prices -> pipeline formats.
INPUT : 02_data/raw/agmarknet/national/<slug>_national_price_2017_2026.json
        (CEDA API rows: date, commodity_id, min_price, max_price, modal_price; Rs/quintal)
OUTPUT: 02_data/clean/spot_daily_<slug>.csv          cols: date, price   (feeds run_v0_garch.py)
        02_data/clean/vol_panel_monthly_national.csv  same schema as vol_panel_monthly.csv
        with state="ALL", district="NATIONAL"        (feeds run_v0_did.py national first pass)
Spot series are NOT truncated at the ban date (rule 4 applies to futures only — post-ban
spot volatility is the DiD outcome). Prints rule-7 diagnostics per series.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from utils import log_returns, realized_vol, trading_days_only, BAN_DATE

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "02_data" / "raw" / "agmarknet" / "national"
OUT = ROOT / "02_data" / "clean"


def load_one(fp: Path) -> tuple[str, pd.DataFrame]:
    blob = json.loads(fp.read_text())
    slug = blob["_meta"]["commodity_slug"]
    df = pd.DataFrame(blob["data"])
    df["date"] = pd.to_datetime(df["date"].str[:10])
    df = (df.rename(columns={"modal_price": "price"})[["date", "price"]]
            .dropna().sort_values("date")
            .drop_duplicates(subset="date", keep="last"))
    df = df[(df.price > 0) & trading_days_only(df.date)]  # trading-day fix
    return slug, df


def diagnostics(slug: str, df: pd.DataFrame) -> None:
    span = f"{df.date.min().date()}..{df.date.max().date()}"
    per_year = df.groupby(df.date.dt.year).size()
    gaps = df.date.diff().dt.days
    r = log_returns(df.set_index("date").price)
    jumps = int((r.abs() > 0.20).sum())
    print(f"[{slug:9s}] {len(df):5d} rows  {span}  "
          f"rows/yr {per_year.min()}-{per_year.max()}  "
          f"max gap {int(gaps.max())}d  |ret|>20%: {jumps:3d}  "
          f"price p1/p50/p99: {df.price.quantile(.01):,.0f}/{df.price.median():,.0f}/"
          f"{df.price.quantile(.99):,.0f} Rs/qtl")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    frames = []
    for fp in sorted(RAW.glob("*_national_price_*.json")):
        slug, df = load_one(fp)
        diagnostics(slug, df)
        df.to_csv(OUT / f"spot_daily_{slug}.csv", index=False)
        frames.append(df.assign(commodity=slug))

    # national monthly vol panel (same schema as district vol_panel_monthly.csv)
    panel = pd.concat(frames, ignore_index=True)
    panel["state"], panel["district"] = "ALL", "NATIONAL"
    panel = panel.sort_values(["commodity", "date"])
    g = panel.groupby("commodity")
    panel["ret"] = g["price"].transform(lambda s: log_returns(s))
    panel["rv30"] = g["ret"].transform(lambda s: realized_vol(s, 30))
    monthly = (panel.set_index("date")
                    .groupby(["commodity", "state", "district"])
                    .resample("ME")[["rv30"]].mean().reset_index())
    monthly["post"] = (monthly["date"] >= BAN_DATE).astype(int)
    monthly.to_csv(OUT / "vol_panel_monthly_national.csv", index=False)
    print(f"\nnational panel: {monthly.shape}, commodities: {sorted(monthly.commodity.unique())}")


if __name__ == "__main__":
    main()
