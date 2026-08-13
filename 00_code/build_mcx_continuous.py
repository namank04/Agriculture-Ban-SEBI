"""Construct c1/c2/c3 continuous futures series for MCX contracts from contract-wise raw
JSON, replicating the Investing.com vendor convention EXACTLY (verified in
explore_roll_convention.py): the front contract is held through its expiry day
included, the chain shifts on the next trading day, prices are spliced UNADJUSTED.

Symbols: cpo (default), cotton (old bale contract, ends Dec-2022), cottoncndy
(candy contract, from Jan-2023). cotton and cottoncndy are built as SEPARATE series —
they quote in different units (Rs/bale vs Rs/candy); any cross-generation splice is a
flagged methodological decision, not done here.

RAW-PHASE RULES (per researcher, 2026-06-10):
- No filtering: zero-OHLC settlement rows and post-suspension stale quotes are
  KEPT — truncation/filtering belongs to the cleaning stage (rule 4 applies there).
- Output mimics the Investing.com export structure (Date DD-MM-YYYY, newest-first,
  columns Date/Price/Open/High/Low/Vol./Change %) so clean_investing_futures.py
  ingests it unchanged, PLUS extra columns: Open Interest, Contract Expiry,
  Days To Expiry, Roll Day.
- Raw contract files in 02_data/raw/mcx/ are read-only inputs; nothing is deleted.
- Output goes to 02_data/constructed/ (separate from raw/ because these files are
  derived, and separate from clean/ because they are pre-cleaning vendor-format).

Usage:  python 00_code/build_mcx_continuous.py [slug]   (slug: cpo | cotton | cottoncndy)
Output: 02_data/constructed/<slug>_c{1,2,3}_daily_<startY>_<endY>.csv
"""
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "02_data" / "raw" / "mcx"
OUT = ROOT / "02_data" / "constructed"
LEGS = 3
SLUG = sys.argv[1] if len(sys.argv) > 1 else "cpo"


def load_contracts() -> dict[datetime, dict[datetime, dict]]:
    """{expiry: {date: row}} from every <slug>_futcom_expiry_*.json (read-only)."""
    contracts = {}
    for f in sorted(RAW.glob(f"{SLUG}_futcom_expiry_*.json")):
        d = json.load(f.open())["d"]
        rows = d["Data"] if isinstance(d, dict) and "Data" in d else d
        expiry = datetime.strptime(f.stem.rsplit("_", 1)[1], "%d%b%Y")
        by_date = {}
        for r in rows:
            dt = datetime.strptime(r["Date"], "%m/%d/%Y")
            by_date[dt] = r  # one row per date per contract
        contracts[expiry] = by_date
    return contracts


# Leg assignment is only correct once every nearer contract is in our set.
# cpo/cotton: earliest downloaded expiry is 31JAN2017; the prior (Dec-2016) contract
# expired 30-Dec-2016, so JAN2017 is genuinely the front only from 31-Dec-2016 onward.
# Dates before that would mislabel JAN2017 as c1 — excluded by construction validity.
# cottoncndy: first contract EVER listed Jan-2023 — no prior contract exists, so the
# whole history is valid.
VALID_FROM = {"cpo": datetime(2016, 12, 31), "cotton": datetime(2016, 12, 31),
              "cottoncndy": datetime(2023, 1, 1)}[SLUG]


def build_leg(contracts: dict, leg: int) -> list[dict]:
    """Vendor convention: on day t the leg-N contract is the N-th smallest expiry
    with expiry >= t. Row exists only if that contract has data for t (as-is)."""
    all_dates = sorted({d for c in contracts.values() for d in c if d >= VALID_FROM})
    expiries = sorted(contracts)
    series, prev_close, prev_expiry = [], None, None
    for t in all_dates:
        live = [e for e in expiries if e >= t]
        if len(live) < leg:
            continue
        exp = live[leg - 1]
        row = contracts[exp].get(t)
        if row is None:
            continue  # contract had no record that day — taken as-is, no fill
        close = row["Close"]
        chg = "" if prev_close in (None, 0) else f"{(close / prev_close - 1) * 100:.2f}%"
        series.append({
            "Date": t.strftime("%d-%m-%Y"),
            "Price": close,
            "Open": row["Open"],
            "High": row["High"],
            "Low": row["Low"],
            "Vol.": row["Volume"],
            "Change %": chg,
            "Open Interest": row["OpenInterest"],
            "Contract Expiry": exp.strftime("%d%b%Y"),
            "Days To Expiry": (exp - t).days,
            "Roll Day": 1 if (prev_expiry is not None and exp != prev_expiry) else 0,
        })
        prev_close, prev_expiry = close, exp
    return series


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    contracts = load_contracts()
    print(f"loaded {len(contracts)} contracts "
          f"({min(contracts):%d%b%Y} .. {max(contracts):%d%b%Y})")
    for leg in range(1, LEGS + 1):
        s = build_leg(contracts, leg)
        dates = [datetime.strptime(r["Date"], "%d-%m-%Y") for r in s]
        rolls = sum(r["Roll Day"] for r in s)
        zero = sum(1 for r in s if r["Open"] == 0 and r["High"] == 0 and r["Low"] == 0)
        post_ban = sum(1 for d in dates if d > datetime(2021, 12, 20))
        y0, y1 = min(dates).year, max(dates).year
        out = OUT / f"{SLUG}_c{leg}_daily_{y0}_{y1}.csv"
        import csv
        with out.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(s[0].keys()))
            w.writeheader()
            for r in reversed(s):  # newest-first, like the vendor export
                w.writerow(r)
        print(f"c{leg}: {len(s)} rows {min(dates):%Y-%m-%d}..{max(dates):%Y-%m-%d} | "
              f"{rolls} rolls | zero-OHLC rows {zero} ({zero/len(s):.1%}) | "
              f"rows after ban date {post_ban} (stale — cleaning will truncate) | -> {out.name}")


if __name__ == "__main__":
    main()
