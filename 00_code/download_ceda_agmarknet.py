"""Download Agmarknet mandi prices via the CEDA Data Portal API -> raw/agmarknet/.

CEDA (Ashoka Univ.) re-serves Ministry of Agriculture Agmarknet data, cleaned, via a
documented JSON API (chosen spot route — see 02_data/sources/spot_source_comparison.md).
Provenance: cite BOTH CEDA and the underlying MoA Agmarknet; validate a sample vs the
official portal separately.

⚠️ RATE LIMIT: 40 requests / hour (RateLimit-Policy: 40;w=3600). This script is
rate-limit-AWARE (reads RateLimit-Remaining / Reset headers and sleeps to the window;
honours Retry-After on 429) and RESUMABLE (one file per unit of work; existing files
skipped). Safe to kill and relaunch.

Phases (national first so V0 is unblocked within one window; district accrues after):
  1. national  — state_id=0, no district_id -> 1 request/commodity (11 total)
  2. district  — per state, all its districts -> ~36 requests/commodity (~396 total, ~10h)

API: POST {base}/agmarknet/prices  Authorization: Bearer <CEDA_API_KEY (.env)>
  body {commodity_id, state_id, district_id?[], from_date, to_date, indicator:"price"}

Usage:  .venv/bin/python 00_code/download_ceda_agmarknet.py
Output: raw/agmarknet/national/<slug>_national_price_2017_2026.json
        raw/agmarknet/district/<slug>__state<sid>.json
        raw/agmarknet/_ceda_geographies.json
"""
import json
import time
import urllib.request
import urllib.error
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "02_data" / "raw" / "agmarknet"
BASE = "https://api.ceda.ashoka.edu.in/v1"
FROM_DATE, TO_DATE = "2017-01-01", "2026-04-30"
PACE = 2.0  # base politeness sleep between successful calls (seconds)

TARGETS = [  # (slug, CEDA commodity_id, group) — ids verified vs /commodities 2026-06-11
    ("wheat", 1, "treatment"), ("chana", 6, "treatment"), ("mustard", 12, "treatment"),
    ("soybean", 13, "treatment"), ("paddy", 2, "treatment"), ("moong", 9, "treatment"),
    ("guar", 75, "control"), ("castor", 123, "control"), ("jeera", 42, "control"),
    ("turmeric", 39, "control"), ("cotton", 15, "control"),
    # id 75 "Guar" is gum-contaminated (corr 0.04 vs guar futures); id 413 "Guar
    # Seed(Cluster Beans Seed)" matches the futures underlying (corr 0.99, 2026-06-12)
    ("guarseed413", 413, "control"),
    # --- C1 Option-B food donors (added 2026-06-21; ids verified vs /commodities) ---
    # non-banned cereals/coarse-grains + oilseeds to restore food-channel similarity.
    # NOTE coriander SEED (dhania) is NOT in CEDA's list (only "Coriander(Leaves)",
    # id 43, a perishable herb — unusable); cereals/oilseeds substituted.
    ("barley", 29, "donor"), ("maize", 4, "donor"), ("jowar", 5, "donor"),
    ("bajra", 28, "donor"), ("ragi", 30, "donor"), ("groundnut", 10, "donor"),
    ("sesamum", 11, "donor"), ("sunflower", 14, "donor"),
]


def api_key() -> str:
    for line in (ROOT / ".env").read_text().splitlines():
        if line.startswith("CEDA_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("CEDA_API_KEY not in .env")


HEADERS = {"Authorization": f"Bearer {api_key()}", "Content-Type": "application/json",
           "User-Agent": "Mozilla/5.0 (academic research; agri-ban-project)"}


class TooBig(Exception):
    """Server 504 — response too large to generate; caller should split the range."""


def call(body: dict, split_on_504: bool = False) -> tuple[list, dict]:
    """POST /prices, honouring rate limits. Returns (rows, headers). Blocks as needed.
    429 -> sleep to window. 504 -> retry a few times, then raise TooBig (if
    split_on_504) so the caller can chunk the date range; else keep retrying."""
    data = json.dumps(body).encode()
    timeouts = 0
    while True:
        req = urllib.request.Request(f"{BASE}/agmarknet/prices", data=data, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                payload = json.load(r)
                hdrs = {k: r.headers[k] for k in r.headers}
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = int(e.headers.get("Retry-After", "60")) + 3
                print(f"    [429] sleeping {wait}s ({wait//60}m{wait%60:02d}s)...", flush=True)
                time.sleep(wait)
                continue
            if e.code in (502, 503, 504):
                timeouts += 1
                if split_on_504 and timeouts >= 2:
                    raise TooBig(f"{e.code} x{timeouts}")
                print(f"    [{e.code}] gateway; retry {timeouts} in 8s", flush=True)
                time.sleep(8)
                continue
            raise
        except (urllib.error.URLError, OSError) as e:
            # OSError covers ConnectionResetError/socket errors (URLError is also an
            # OSError). Transient — back off and retry generously so a single blip
            # never crashes a multi-hour run; only give up (-> split/skip) after many.
            timeouts += 1
            if timeouts >= 8:
                if split_on_504:
                    raise TooBig(f"neterr x{timeouts}: {str(e)[:40]}")
                print(f"    [neterr] giving up after {timeouts}: {str(e)[:40]}", flush=True)
                return [], {}
            wait = min(8 * timeouts, 60)
            print(f"    [neterr] {str(e)[:40]}; retry {timeouts} in {wait}s", flush=True)
            time.sleep(wait)
            continue
        o = payload.get("output", payload)
        rows = o.get("data", o) if isinstance(o.get("data", o), list) else []
        rem = hdrs.get("RateLimit-Remaining")
        if rem is not None and int(rem) <= 0:
            reset = int(hdrs.get("RateLimit-Reset", "3600")) + 3
            print(f"    [pace] 0 left; sleeping to reset {reset}s ({reset//60}m)...", flush=True)
            time.sleep(reset)
        else:
            time.sleep(PACE)
        return rows, hdrs


DISTRICT_BATCH = 15  # big states 504 with wide district arrays; batch the districts


def fetch_districts(cid: int, sid: int, dids: list) -> list:
    """District/market-level pull for one state over the full range. Requests
    districts in batches (root cause of 504 is array breadth, not date range);
    on persistent 504 halve the district batch and recurse."""
    rows = []
    for i in range(0, len(dids), DISTRICT_BATCH):
        rows.extend(_fetch_batch(cid, sid, dids[i:i + DISTRICT_BATCH]))
    return rows


def _fetch_batch(cid: int, sid: int, batch: list) -> list:
    body = {"commodity_id": cid, "state_id": sid, "district_id": batch,
            "from_date": FROM_DATE, "to_date": TO_DATE, "indicator": "price"}
    try:
        rows, _ = call(body, split_on_504=True)
        return rows
    except TooBig:
        if len(batch) <= 1:
            # a single dense district (e.g. Raipur paddy) too big over full range
            # -> fall back to splitting the DATE range instead of dropping it
            print(f"      [district-too-big] {batch} alone; date-chunking", flush=True)
            return _fetch_district_by_date(cid, sid, batch[0], FROM_DATE, TO_DATE)
        h = len(batch) // 2
        print(f"      [split-districts] {len(batch)} -> {h}+{len(batch)-h}", flush=True)
        return _fetch_batch(cid, sid, batch[:h]) + _fetch_batch(cid, sid, batch[h:])


def _fetch_district_by_date(cid: int, sid: int, did: int, lo: str, hi: str, depth: int = 0) -> list:
    import datetime as dt
    body = {"commodity_id": cid, "state_id": sid, "district_id": [did],
            "from_date": lo, "to_date": hi, "indicator": "price"}
    try:
        rows, _ = call(body, split_on_504=True)
        return rows
    except TooBig:
        if depth >= 5:  # ~9yr -> ~3-4 month chunks; give up below that
            print(f"        [skip-district] did={did} {lo}..{hi} still 504", flush=True)
            return []
        a = dt.date.fromisoformat(lo); b = dt.date.fromisoformat(hi)
        mid = (a + (b - a) / 2)
        nxt = (mid + dt.timedelta(days=1)).isoformat()
        print(f"        [split-date] did={did} {lo}..{hi}", flush=True)
        return (_fetch_district_by_date(cid, sid, did, lo, mid.isoformat(), depth + 1)
                + _fetch_district_by_date(cid, sid, did, nxt, hi, depth + 1))


def load_geo() -> tuple[dict, dict]:
    p = RAW / "_ceda_geographies.json"
    if not p.exists():
        req = urllib.request.Request(f"{BASE}/agmarknet/geographies", headers=HEADERS)
        with urllib.request.urlopen(req, timeout=60) as r:
            p.write_text(json.dumps(json.load(r), indent=1))
    geo = json.loads(p.read_text())
    o = geo.get("output", geo)
    rows = o.get("data", o)
    by_state, sname = defaultdict(list), {}
    for r in rows:
        by_state[r["census_state_id"]].append(r["census_district_id"])
        sname[r["census_state_id"]] = r["census_state_name"]
    return by_state, sname


def meta(slug, cid, group, level, **extra):
    return {"source": "CEDA Data Portal API /v1/agmarknet/prices",
            "underlying": "MoA&FW Agmarknet", "commodity_slug": slug,
            "ceda_commodity_id": cid, "group": group, "level": level,
            "indicator": "price", "from_date": FROM_DATE, "to_date": TO_DATE,
            "pulled_date": "2026-06-11", **extra}


def main():
    import sys
    argv = sys.argv[1:]
    national_only = "--national-only" in argv
    only = {a for a in argv if not a.startswith("--")}  # optional slug filter
    targets = [t for t in TARGETS if not only or t[0] in only]

    (RAW / "national").mkdir(parents=True, exist_ok=True)
    (RAW / "district").mkdir(parents=True, exist_ok=True)
    by_state, sname = load_geo()
    print(f"geographies: {len(by_state)} states | targets: {[t[0] for t in targets]}"
          f"{' | NATIONAL-ONLY' if national_only else ''}", flush=True)

    # PHASE 1 — national
    print("\n=== PHASE 1: national ===", flush=True)
    for slug, cid, group in targets:
        dest = RAW / "national" / f"{slug}_national_price_2017_2026.json"
        if dest.exists():
            print(f"[skip] {slug} national", flush=True)
            continue
        rows, _ = call({"commodity_id": cid, "state_id": 0,
                        "from_date": FROM_DATE, "to_date": TO_DATE, "indicator": "price"})
        dest.write_text(json.dumps({"_meta": meta(slug, cid, group, "national",
                        n_rows=len(rows)), "data": rows}, indent=1))
        span = f"{min(r['date'][:10] for r in rows)}..{max(r['date'][:10] for r in rows)}" if rows else "EMPTY"
        print(f"[ok] {slug} national: {len(rows)} rows {span}", flush=True)

    # PHASE 2 — district (per commodity x state)
    if national_only:
        print("\n[national-only] skipping district phase.", flush=True)
        return
    print("\n=== PHASE 2: district ===", flush=True)
    for slug, cid, group in targets:
        for sid, dids in by_state.items():
            dest = RAW / "district" / f"{slug}__state{sid}.json"
            if dest.exists():
                continue
            rows = fetch_districts(cid, sid, dids)
            dest.write_text(json.dumps({"_meta": meta(slug, cid, group, "district",
                            state_id=sid, state_name=sname[sid], n_rows=len(rows)),
                            "data": rows}, indent=1))
            print(f"[ok] {slug} {sname[sid]}: {len(rows)} rows", flush=True)
    print("\nALL DONE.", flush=True)


if __name__ == "__main__":
    main()
