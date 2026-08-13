"""Download MCX cotton contract-wise bhavcopy — BOTH generations of the contract:
  COTTON      (bales of 170 kg; halted Aug-2022, last expiry Dec-2022)
  COTTONCNDY  (candy of 356 kg; relaunched 31-Jan-2023, runs today)

Same headed-Chrome route as download_mcx_cpo_bhavcopy.py (MCX bot protection rejects
every non-browser client). Unlike the CPO script, expiry lists are ENUMERATED FROM THE
DATA: GetCommoditywiseBhavCopy accepts Expiry="" and returns every contract trading in
the window, so we sweep half-year windows, collect distinct ExpiryDate values, and
snapshot them to raw/mcx/_<slug>_expiries_enumerated_<date>.json for provenance.
(The page's symbol picker is a Telerik widget, not a <select> — dropdown scraping fails.)

⚠️ The two generations quote in DIFFERENT units (Rs/bale vs Rs/candy) — the unit
break at Jan-2023 plus the Sep-2022..Jan-2023 trading gap are handled in CLEANING,
not here. Raw JSON saved verbatim, one file per contract; idempotent (skip existing).

Usage:  .venv/bin/python 00_code/download_mcx_cotton_bhavcopy.py
Output: 02_data/raw/mcx/cotton_futcom_expiry_<DDMONYYYY>.json
        02_data/raw/mcx/cottoncndy_futcom_expiry_<DDMONYYYY>.json
"""
import json
import re
import time
from datetime import datetime, timedelta
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "02_data" / "raw" / "mcx"
PAGE = "https://www.mcxindia.com/market-data/bhavcopy"
API = "https://www.mcxindia.com/backpage.aspx/GetCommoditywiseBhavCopy"
SLEEP = 1.5
PULL_DATE = "2026-06-12"
SYMBOLS = {"COTTON": "cotton", "COTTONCNDY": "cottoncndy"}  # symbol -> file slug
EXPIRY_RE = re.compile(r"^\d{2}[A-Z]{3}\d{4}$")

FETCH_JS = """async ({api, payload}) => {
    const r = await fetch(api, {
        method: 'POST',
        headers: {'Content-Type': 'application/json; charset=UTF-8'},
        body: JSON.stringify(payload)});
    const text = await r.text();
    return {status: r.status, text: text};
}"""

ENUM_WINDOWS = [(datetime(y, m, 1), datetime(y, m + 5, 30 if m == 1 else 31))
                for y in range(2017, 2027) for m in (1, 7)]  # half-years 2017..2026


def discover_date_format(page) -> str | None:
    """Same probe as the CPO script, on the known-liquid CPO 29JAN2021 contract."""
    exp = datetime.strptime("29JAN2021", "%d%b%Y")
    lo, hi = exp - timedelta(days=305), exp + timedelta(days=30)
    fmts = {"%Y%m%d": "yyyymmdd", "%d%b%Y": "ddMONyyyy",
            "%d/%m/%Y": "dd/mm/yyyy", "%m/%d/%Y": "mm/dd/yyyy", "%Y-%m-%d": "iso"}
    for fmt in fmts:
        payload = {"Symbol": "CPO", "Expiry": "29JAN2021",
                   "FromDate": lo.strftime(fmt), "ToDate": hi.strftime(fmt),
                   "InstrumentName": "FUTCOM"}
        res = page.evaluate(FETCH_JS, {"api": API, "payload": payload})
        ok = res["status"] == 200 and '"d":' in res["text"] and len(res["text"]) > 200
        n = res["text"].count("\"Date\"")
        print(f"  format {fmts[fmt]:<11} -> HTTP {res['status']}, ~{n} rows", flush=True)
        if ok and n > 10:
            return fmt
        time.sleep(1)
    return None


def discover_expiries(page, symbol: str, fmt: str) -> list[str]:
    """Sweep half-year windows with Expiry='' and collect distinct ExpiryDate values."""
    found = set()
    for lo, hi in ENUM_WINDOWS:
        payload = {"Symbol": symbol, "Expiry": "",
                   "FromDate": lo.strftime(fmt), "ToDate": hi.strftime(fmt),
                   "InstrumentName": "FUTCOM"}
        try:
            res = page.evaluate(FETCH_JS, {"api": API, "payload": payload})
        except Exception as e:
            print(f"  [enum {lo:%Y-%m}] error {str(e)[:60]}", flush=True)
            time.sleep(SLEEP)
            continue
        n = 0
        if res["status"] == 200 and '"d":' in res["text"]:
            d = json.loads(res["text"])["d"]
            rows = d["Data"] if isinstance(d, dict) and "Data" in d else (d or [])
            exps = {r["ExpiryDate"] for r in rows
                    if r.get("ExpiryDate") and EXPIRY_RE.match(r["ExpiryDate"])}
            found |= exps
            n = len(rows)
        print(f"  [enum {lo:%Y-%m}..{hi:%Y-%m}] {n} rows, "
              f"{len(found)} expiries so far", flush=True)
        time.sleep(SLEEP)
    exps = sorted(found, key=lambda e: datetime.strptime(e, "%d%b%Y"))
    snap = RAW / f"_{SYMBOLS[symbol]}_expiries_enumerated_{PULL_DATE}.json"
    snap.write_text(json.dumps({"symbol": symbol, "method": "Expiry='' half-year sweep",
                                "snapshot_date": PULL_DATE, "expiries": exps}, indent=1))
    return exps


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        page = ctx.new_page()
        page.goto(PAGE, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)

        print("discovering date format...", flush=True)
        fmt = discover_date_format(page)
        if not fmt:
            print("FATAL: no date format accepted — inspect manually", flush=True)
            browser.close()
            return
        print(f"using format: {fmt}\n", flush=True)

        ok, failed = [], {}
        for symbol, slug in SYMBOLS.items():
            print(f"=== {symbol}: discovering expiries ===", flush=True)
            expiries = discover_expiries(page, symbol, fmt)
            keep = [e for e in expiries
                    if datetime.strptime(e, "%d%b%Y").year >= 2017]
            print(f"  dropdown lists {len(expiries)} expiries; keeping {len(keep)} (>=2017)",
                  flush=True)
            for exp_s in keep:
                dest = RAW / f"{slug}_futcom_expiry_{exp_s}.json"
                if dest.exists() and dest.stat().st_size > 50:
                    print(f"[skip] {symbol} {exp_s} (exists)", flush=True)
                    continue
                exp = datetime.strptime(exp_s, "%d%b%Y")
                payload = {"Symbol": symbol, "Expiry": exp_s,
                           "FromDate": (exp - timedelta(days=305)).strftime(fmt),
                           "ToDate": (exp + timedelta(days=30)).strftime(fmt),
                           "InstrumentName": "FUTCOM"}
                try:
                    res = page.evaluate(FETCH_JS, {"api": API, "payload": payload})
                except Exception as e:
                    failed[f"{symbol} {exp_s}"] = str(e)[:80]
                    print(f"[FAIL] {symbol} {exp_s}: {failed[f'{symbol} {exp_s}']}", flush=True)
                    time.sleep(SLEEP)
                    continue
                n = res["text"].count("\"Date\"")
                if res["status"] == 200 and n > 0:
                    dest.write_text(res["text"])
                    ok.append((f"{symbol} {exp_s}", n))
                    print(f"[ok]   {symbol} {exp_s}: {n} rows, {len(res['text'])/1024:.0f} KB",
                          flush=True)
                else:
                    failed[f"{symbol} {exp_s}"] = f"HTTP {res['status']}, rows={n}"
                    print(f"[FAIL] {symbol} {exp_s}: {failed[f'{symbol} {exp_s}']}", flush=True)
                time.sleep(SLEEP)
        browser.close()

    print("\n===== SUMMARY =====", flush=True)
    print(f"downloaded: {len(ok)} contracts", flush=True)
    if ok:
        rows = [n for _, n in ok]
        print(f"rows per contract: min {min(rows)}, median {sorted(rows)[len(rows)//2]}, "
              f"max {max(rows)}", flush=True)
    print(f"failed: {len(failed)}", flush=True)
    for k, v in failed.items():
        print(f"  {k}: {v}", flush=True)


if __name__ == "__main__":
    main()
