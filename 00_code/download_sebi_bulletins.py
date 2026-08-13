"""Download SEBI monthly bulletins (2019-01 .. 2021-12) -> raw/sebi_bulletins/.

These bulletins carry participant-wise open-interest tables needed for H8.
DOWNLOAD ONLY: this script never parses/extracts/transforms document content.

Discovery note (2026-06-10)
---------------------------
SEBI's listing pages and detail pages are JS shells for normal user-agents, and
the getnewslistinfo.jsp AJAX endpoint returns "No record(s)" for every category
ID we tried. What works: detail pages ARE server-rendered for a crawler
user-agent (Googlebot), exposing the document links under /sebi_data/.
Detail-page URLs were therefore harvested once via web search + Wayback CDX and
frozen in 02_data/sources/sebi_bulletin_detail_urls.csv (months marked MISSING
could not be located and must be fetched manually).

Format note: from 2019 SEBI publishes the bulletin as MSWord (narrative) +
MSExcel (tables) rather than a single PDF. Both are downloaded per month; a PDF
is downloaded too whenever the detail page links one. For H8 extraction the
Excel tables file is the one that matters.

Usage:  python download_sebi_bulletins.py
Output: 02_data/raw/sebi_bulletins/sebi_bulletin_YYYY-MM_text.docx
        02_data/raw/sebi_bulletins/sebi_bulletin_YYYY-MM_tables.<xls|xlsx|xlsm>
        (+ sebi_bulletin_YYYY-MM.pdf when available)
        + a per-run summary printed to stdout.
Idempotent: months whose files are already present and valid are skipped.
Stdlib + requests only.
"""
from __future__ import annotations

import csv
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, quote

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "02_data" / "raw" / "sebi_bulletins"
MANIFEST = ROOT / "02_data" / "sources" / "sebi_bulletin_detail_urls.csv"

# SEBI serves full server-rendered pages only to crawler UAs.
UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
HEADERS = {"User-Agent": UA, "Accept": "text/html,application/pdf,*/*"}
TIMEOUT = 90
SLEEP = 1.0
MIN_BYTES = 20 * 1024

DOC_LINK_RE = re.compile(
    r"href=\s*['\"]\s*([^'\"]*sebi_data/(?:commondocs|attachdocs)/[^'\"]+?"
    r"\.(?:pdf|docx|doc|xlsx|xlsm|xls))\s*['\"]",
    re.I,
)

MAGIC = {  # extension -> required file signature
    "pdf": (b"%PDF",),
    "docx": (b"PK",), "xlsx": (b"PK",), "xlsm": (b"PK",),
    "doc": (b"\xd0\xcf",), "xls": (b"\xd0\xcf",),
}


def classify(url: str) -> str:
    """word | excel | pdf based on extension."""
    ext = url.rsplit(".", 1)[-1].lower()
    if ext == "pdf":
        return "pdf"
    if ext in ("xls", "xlsx", "xlsm"):
        return "excel"
    return "word"


def dest_for(month: str, url: str) -> Path:
    ext = url.rsplit(".", 1)[-1].lower()
    kind = classify(url)
    if kind == "pdf":
        return RAW_DIR / f"sebi_bulletin_{month}.pdf"
    suffix = "text" if kind == "word" else "tables"
    return RAW_DIR / f"sebi_bulletin_{month}_{suffix}.{ext}"


def valid(path: Path) -> bool:
    ext = path.suffix.lstrip(".").lower()
    sigs = MAGIC.get(ext, ())
    try:
        if path.stat().st_size < MIN_BYTES:
            return False
        head = path.open("rb").read(8)
        return any(head.startswith(s) for s in sigs)
    except OSError:
        return False


def month_done(month: str) -> bool:
    """A month counts as done when a valid text + tables pair (or a PDF) exists."""
    files = list(RAW_DIR.glob(f"sebi_bulletin_{month}*"))
    kinds = {("pdf" if f.suffix == ".pdf" else ("text" if "_text" in f.stem else "tables"))
             for f in files if valid(f)}
    return "pdf" in kinds or {"text", "tables"} <= kinds


def fetch_doc_links(session: requests.Session, detail_url: str) -> list[str]:
    r = session.get(detail_url, headers=HEADERS, timeout=TIMEOUT)
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code} on detail page")
    links = []
    for href in DOC_LINK_RE.findall(r.text):
        absolute = urljoin(detail_url, href.strip())
        if absolute not in links:
            links.append(absolute)
    return links


def download(session: requests.Session, url: str, dest: Path) -> tuple[bool, str]:
    # paths contain literal spaces — encode, keeping the scheme/host intact
    safe = quote(url, safe=":/%")
    try:
        r = session.get(safe, headers=HEADERS, timeout=TIMEOUT)
    except requests.RequestException as exc:
        return False, f"request error: {exc}"
    if r.status_code != 200:
        return False, f"HTTP {r.status_code}"
    ext = dest.suffix.lstrip(".").lower()
    if not any(r.content.startswith(s) for s in MAGIC.get(ext, (b"",))):
        return False, "wrong file signature (HTML error page?)"
    if len(r.content) < MIN_BYTES:
        return False, f"too small ({len(r.content)} bytes)"
    dest.write_bytes(r.content)
    return True, f"{len(r.content)/1024:.0f} KB"


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open() as fh:
        rows = list(csv.DictReader(fh))

    session = requests.Session()
    ok: dict[str, list[str]] = {}
    failed: dict[str, str] = {}

    for row in rows:
        month, detail = row["month"], row["detail_url"].strip()
        if detail == "MISSING":
            failed[month] = "no detail URL found (fetch manually)"
            continue
        if month_done(month):
            print(f"[skip] {month}: already complete")
            continue
        try:
            links = fetch_doc_links(session, detail)
        except Exception as exc:
            failed[month] = f"detail page: {exc}"
            print(f"[FAIL] {month}: {failed[month]}")
            time.sleep(SLEEP)
            continue
        if not links:
            failed[month] = "no document links on detail page"
            print(f"[FAIL] {month}: {failed[month]}")
            time.sleep(SLEEP)
            continue
        got = []
        for url in links:
            dest = dest_for(month, url)
            if dest.exists() and valid(dest):
                got.append(f"{dest.name} (cached)")
                continue
            good, msg = download(session, url, dest)
            status = "ok" if good else "FAIL"
            print(f"[{status}] {month} {dest.name}: {msg}")
            if good:
                got.append(f"{dest.name} ({msg})")
            time.sleep(SLEEP)
        if got:
            ok[month] = got
        else:
            failed[month] = "all document downloads failed"
        time.sleep(SLEEP)

    print("\n===== SUMMARY =====")
    print(f"months with files: {len(ok)}")
    for m in sorted(ok):
        print(f"  {m}: {'; '.join(ok[m])}")
    print(f"months failed/missing: {len(failed)}")
    for m in sorted(failed):
        print(f"  {m}: {failed[m]}")

    complete = sum(month_done(f"{y}-{m:02d}") for y in (2019, 2020, 2021) for m in range(1, 13))
    print(f"\ncomplete months (text+tables or pdf): {complete}/36")


if __name__ == "__main__":
    main()
