"""V0 step 1: build commodity x district x month volatility panel from the CEDA
Agmarknet DISTRICT raw files (the realized spot route — see spot_source_comparison.md;
this replaced the originally-expected direct-Agmarknet CSV exports).

INPUT : 02_data/raw/agmarknet/district/<slug>__state<sid>.json
        (market-day rows: date, census_district_id, market_id, modal_price Rs/qtl)
OUTPUT: 02_data/clean/vol_panel_monthly.csv
            cols: commodity, state, district, date (month-end), rv30, post
        02_data/clean/spot_daily_<slug>_distmed.csv   cols: date, price
            cross-district median of district-day medians — robust national series
            (feeds run_v0_garch.py via the _distmed suffix)

Guar: id 75 ("guar") is gum-contaminated; id 413 ("guarseed413") is the futures
underlying (probe 2026-06-12, corr 0.99 vs futures). BOTH are built when present —
the panel keeps them as separate commodity slugs; analysis scripts choose.
Spot series are NOT ban-truncated (rule 4 is futures-only).
"""
import json
from collections import defaultdict
from pathlib import Path

import pandas as pd

from utils import log_returns, realized_vol, trading_days_only, BAN_DATE

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "02_data" / "raw" / "agmarknet" / "district"
OUT = ROOT / "02_data" / "clean"


def load_commodity(slug: str, files: list[Path]) -> pd.DataFrame:
    """Market rows -> district-day median (kills outlier mandis), tagged with state."""
    frames = []
    for fp in files:
        blob = json.loads(fp.read_text())
        if not blob["data"]:
            continue
        df = pd.DataFrame(blob["data"])
        df["date"] = pd.to_datetime(df["date"].str[:10])
        df = df[(df.modal_price > 0) & trading_days_only(df.date)]  # trading-day fix
        if df.empty:
            continue
        dd = (df.groupby(["census_district_id", "date"], as_index=False)
                ["modal_price"].median())
        dd["state"] = blob["_meta"]["state_name"]
        frames.append(dd)
    if not frames:
        return pd.DataFrame()
    out = pd.concat(frames, ignore_index=True)
    out["commodity"] = slug
    out["district"] = out.pop("census_district_id").astype(str)
    return out.rename(columns={"modal_price": "price"})


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    by_slug = defaultdict(list)
    for fp in sorted(RAW.glob("*__state*.json")):
        by_slug[fp.name.split("__state")[0]].append(fp)

    monthly_frames = []
    for slug, files in sorted(by_slug.items()):
        panel = load_commodity(slug, files)
        if panel.empty:
            print(f"[{slug}] EMPTY — skipped")
            continue
        panel = panel.sort_values(["district", "date"])

        # robust national daily series: cross-district median (for GARCH)
        distmed = panel.groupby("date")["price"].median().rename("price")
        distmed.to_csv(OUT / f"spot_daily_{slug}_distmed.csv")

        g = panel.groupby(["state", "district"])
        panel["ret"] = g["price"].transform(lambda s: log_returns(s))
        panel["rv30"] = g["ret"].transform(lambda s: realized_vol(s, 30))
        monthly = (panel.set_index("date")
                        .groupby(["commodity", "state", "district"])
                        .resample("ME")[["rv30"]].mean().reset_index()
                        .dropna(subset=["rv30"]))
        monthly_frames.append(monthly)
        print(f"[{slug}] {panel.district.nunique()} districts, "
              f"{len(panel):,} district-days -> {len(monthly):,} panel cells")

    full = pd.concat(monthly_frames, ignore_index=True)
    full["post"] = (full["date"] >= BAN_DATE).astype(int)
    full.to_csv(OUT / "vol_panel_monthly.csv", index=False)
    print(f"\npanel: {full.shape}, commodities: {sorted(full.commodity.unique())}")


if __name__ == "__main__":
    main()
