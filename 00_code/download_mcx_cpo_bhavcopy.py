"""Download MCX CPO (crude palm oil) contract-wise bhavcopy via the exchange's own
commodity-wise endpoint, driven through a real Chrome window (MCX's bot protection
rejects every non-browser client; the headed browser is the supported access path).

Endpoint + payload shape come from the bhavcopy page's own JS:
  POST /backpage.aspx/GetCommoditywiseBhavCopy
  {'Symbol','Expiry','FromDate','ToDate','InstrumentName'}

One JSON file per contract expiry is saved VERBATIM (raw = exact server response;
CSV conversion happens later in cleaning). Idempotent: existing non-empty files
are skipped. Visits mcxindia.com ONLY.

Usage:  .venv/bin/python 00_code/download_mcx_cpo_bhavcopy.py
Output: 02_data/raw/mcx/cpo_futcom_expiry_<DDMONYYYY>.json
"""
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

from playwright.sync_api import sync_playwright

RAW = Path(__file__).resolve().parents[1] / "02_data" / "raw" / "mcx"
PAGE = "https://www.mcxindia.com/market-data/bhavcopy"
API = "https://www.mcxindia.com/backpage.aspx/GetCommoditywiseBhavCopy"
SLEEP = 1.5

# All CPO expiries from Jan-2017 through the post-suspension tail (Apr-2022),
# as enumerated from the page's own expiry dropdown on 2026-06-10.
EXPIRIES = [
    "31JAN2017","28FEB2017","31MAR2017","28APR2017","31MAY2017","30JUN2017",
    "31JUL2017","31AUG2017","29SEP2017","31OCT2017","30NOV2017","29DEC2017",
    "31JAN2018","28FEB2018","28MAR2018","30APR2018","31MAY2018","29JUN2018",
    "31JUL2018","31AUG2018","28SEP2018","31OCT2018","30NOV2018","31DEC2018",
    "31JAN2019","28FEB2019","29MAR2019","30APR2019","31MAY2019","28JUN2019",
    "31JUL2019","30AUG2019","30SEP2019","31OCT2019","29NOV2019","31DEC2019",
    "31JAN2020","28FEB2020","31MAR2020","30APR2020","29MAY2020","30JUN2020",
    "31JUL2020","31AUG2020","30SEP2020","30OCT2020","27NOV2020","31DEC2020",
    "29JAN2021","26FEB2021","31MAR2021","30APR2021","31MAY2021","30JUN2021",
    "30JUL2021","31AUG2021","30SEP2021","29OCT2021","30NOV2021","31DEC2021",
    "31JAN2022","28FEB2022","31MAR2022","29APR2022",
]

FETCH_JS = """async ({api, payload}) => {
    const r = await fetch(api, {
        method: 'POST',
        headers: {'Content-Type': 'application/json; charset=UTF-8'},
        body: JSON.stringify(payload)});
    const text = await r.text();
    return {status: r.status, text: text};
}"""


def window(expiry: str) -> tuple[str, str]:
    """Query window: 10 months before expiry -> 1 month after (dates as yyyymmdd)."""
    exp = datetime.strptime(expiry, "%d%b%Y")
    return ((exp - timedelta(days=305)).strftime("%Y%m%d"),
            (exp + timedelta(days=30)).strftime("%Y%m%d"))


def discover_date_format(page) -> str | None:
    """Try plausible FromDate/ToDate formats on one known-liquid contract."""
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
        print(f"  format {fmts[fmt]:<11} -> HTTP {res['status']}, ~{n} rows")
        if ok and n > 10:
            return fmt
        time.sleep(1)
    return None


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        page = ctx.new_page()
        page.goto(PAGE, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)

        print("discovering date format...")
        fmt = discover_date_format(page)
        if not fmt:
            print("FATAL: no date format accepted — inspect manually")
            browser.close()
            return
        print(f"using format: {fmt}\n")

        ok, failed = [], {}
        for exp_s in EXPIRIES:
            dest = RAW / f"cpo_futcom_expiry_{exp_s}.json"
            if dest.exists() and dest.stat().st_size > 50:
                print(f"[skip] {exp_s} (exists)")
                continue
            exp = datetime.strptime(exp_s, "%d%b%Y")
            payload = {"Symbol": "CPO", "Expiry": exp_s,
                       "FromDate": (exp - timedelta(days=305)).strftime(fmt),
                       "ToDate": (exp + timedelta(days=30)).strftime(fmt),
                       "InstrumentName": "FUTCOM"}
            try:
                res = page.evaluate(FETCH_JS, {"api": API, "payload": payload})
            except Exception as e:
                failed[exp_s] = str(e)[:80]
                print(f"[FAIL] {exp_s}: {failed[exp_s]}")
                time.sleep(SLEEP)
                continue
            n = res["text"].count("\"Date\"")
            if res["status"] == 200 and n > 0:
                dest.write_text(res["text"])
                ok.append((exp_s, n))
                print(f"[ok]   {exp_s}: {n} rows, {len(res['text'])/1024:.0f} KB")
            else:
                failed[exp_s] = f"HTTP {res['status']}, rows={n}"
                print(f"[FAIL] {exp_s}: {failed[exp_s]}")
            time.sleep(SLEEP)
        browser.close()

    print("\n===== SUMMARY =====")
    print(f"downloaded: {len(ok)} contracts")
    if ok:
        rows = [n for _, n in ok]
        print(f"rows per contract: min {min(rows)}, median {sorted(rows)[len(rows)//2]}, max {max(rows)}")
    print(f"failed: {len(failed)}")
    for k, v in failed.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
