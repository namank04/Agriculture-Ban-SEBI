"""H8: market COMPOSITION of the agri-derivatives segment before the suspension.
Source = SEBI monthly bulletin "Table 70: Participant-wise percentage share of turnover
at MCX, NCDEX, ICEX, BSE and NSE" (sheet varies by file). The table gives, per exchange,
the Agri-segment turnover share held by Proprietary / Client / Hedgers, monthly.

This is necessarily a PRE-BAN, segment-level descriptive (the banned futures were suspended
2021-12-20, so no post-ban OI exists; and SEBI reports at exchange x segment level, not per
commodity). It answers "who was in the agri-derivatives market that the suspension removed?"
The "Hedgers" column is SEBI's own label, so no hedger/speculator crosswalk decision is needed
for the descriptive composition (Working's T, which needs long/short OI, remains future work).

INPUT : 02_data/raw/sebi_bulletins/sebi_bulletin_YYYY-MM_tables.xls*
OUTPUT: 04_empirics/H8_market_composition/output/{h8_agri_participation.csv, h8_summary.csv,
        h8_agri_composition.png} + h8_findings.md is written separately.
"""
import re
import datetime as _dt
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "02_data" / "raw" / "sebi_bulletins"
OUT = ROOT / "04_empirics" / "H8_market_composition" / "output"


def find_table70(xl: pd.ExcelFile, fp) -> str | None:
    """Return the sheet name whose first rows are the participant-wise turnover table."""
    for sh in xl.sheet_names:
        try:
            head = pd.read_excel(fp, sheet_name=sh, header=None, nrows=2, dtype=str).fillna("")
            t = " ".join(head.values.ravel()).lower()
            if "participant" in t and "turnover" in t:
                return sh
        except Exception:
            continue
    return None


def parse_one(fp: Path):
    """Return long DataFrame: date, exchange, segment, participant, share (for that bulletin)."""
    xl = pd.ExcelFile(fp)
    sh = find_table70(xl, fp)
    if sh is None:
        return None
    raw = pd.read_excel(fp, sheet_name=sh, header=None, dtype=object)
    # locate the exchange header row robustly (it lists MCX & NCDEX); then +1 (segment), +2 (participant).
    # (The table number and the "Year/Month" wording both vary month-to-month, so key off the exchanges.)
    hdr = None
    for i in range(min(8, len(raw))):
        row = " ".join(str(v) for v in raw.iloc[i].values).lower()
        is_exch_row = "mcx" in row and "ncdex" in row and "participant" not in row and "table" not in row
        if ("year" in row and "month" in row) or is_exch_row:
            hdr = i
            break
    if hdr is None or hdr + 2 >= len(raw):
        return None
    exch = raw.iloc[hdr].ffill()        # MCX / NCDEX / ICEX ... (merged -> ffill)
    seg = raw.iloc[hdr + 1].ffill()     # Agri Segment / Non-Agri Segment
    part = raw.iloc[hdr + 2]            # Proprietary / Client / Hedgers
    data = raw.iloc[hdr + 3:].copy()
    out = []
    datecol = data.columns[0]
    for col in data.columns[1:]:
        e, s, p = str(exch[col]), str(seg[col]), str(part[col])
        # AGRI commodity segment only: keep "Agri Segment", drop "Non-Agri Segment" and "Agridex Index"
        if "agri segment" not in s.lower() or "non" in s.lower():
            continue
        if not re.search(r"propriet|client|hedger", p, re.I):
            continue
        for _, r in data.iterrows():
            dt = r[datecol]
            val = pd.to_numeric(r[col], errors="coerce")
            if pd.isna(val):
                continue
            # keep only true monthly date rows (datetime cells); skip annual "2019-20" / "$" strings
            if isinstance(dt, (pd.Timestamp, _dt.datetime, _dt.date)):
                out.append({"date": pd.Timestamp(dt).normalize(), "exchange": e.strip(),
                            "participant": p.strip().title(), "share": float(val)})
    if not out:
        return None
    df = pd.DataFrame(out)
    df["exchange"] = df.exchange.str.upper().str.extract(r"(MCX|NCDEX|ICEX|BSE|NSE)")[0]
    return df.dropna(subset=["exchange"])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = sorted(RAW.glob("sebi_bulletin_*_tables.xls*"))
    frames, parsed, failed = [], 0, []
    for fp in files:
        try:
            d = parse_one(fp)
        except Exception as e:
            d = None
        if d is None or d.empty:
            failed.append(fp.name)
        else:
            frames.append(d); parsed += 1
    if not frames:
        raise SystemExit("no Table-70 data parsed")
    panel = (pd.concat(frames, ignore_index=True)
               .drop_duplicates(["date", "exchange", "participant"])
               .sort_values(["exchange", "date", "participant"]))
    panel.to_csv(OUT / "h8_agri_participation.csv", index=False)
    print(f"parsed {parsed}/{len(files)} bulletins; {len(failed)} without a parseable Table 70")
    print(f"panel: {len(panel)} rows, {panel.date.min().date()}..{panel.date.max().date()}, "
          f"exchanges {sorted(panel.exchange.unique())}")

    # sanity: within exchange-month, Prop+Client(+Hedgers) should be ~100 (Prop+Client) — report
    piv = panel.pivot_table(index=["exchange", "date"], columns="participant", values="share")
    chk = (piv.get("Proprietary", 0) + piv.get("Client", 0))
    print(f"sanity: Proprietary+Client mean = {chk.mean():.1f} (expect ~100 within a segment)")

    # summary: mean participant share by exchange (the agri-derivatives composition)
    summ = panel.groupby(["exchange", "participant"]).share.mean().round(2).reset_index()
    summ.to_csv(OUT / "h8_summary.csv", index=False)
    print("\nmean Agri-segment turnover share by participant (2019-2021, pre-ban):")
    print(summ.to_string(index=False))

    # plot NCDEX/MCX agri hedger + client + prop shares over time
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    for ax, exch in zip(axes, ["NCDEX", "MCX"]):
        sub = panel[panel.exchange == exch]
        for p in ["Proprietary", "Client", "Hedgers"]:
            s = sub[sub.participant == p].set_index("date").share.sort_index()
            if len(s):
                ax.plot(s.index, s.values, marker=".", ms=3, label=p)
        ax.axvline(pd.Timestamp("2021-12-20"), c="gray", ls=":")
        ax.set_title(f"{exch} agri segment"); ax.set_ylabel("% of turnover"); ax.legend(fontsize=8)
    plt.tight_layout(); plt.savefig(OUT / "h8_agri_composition.png", dpi=140); plt.close()
    print(f"\nwrote {OUT}/h8_agri_participation.csv, h8_summary.csv, h8_agri_composition.png")
    if failed:
        print(f"NOTE unparsed bulletins ({len(failed)}): {failed[:5]}{' ...' if len(failed)>5 else ''}")


if __name__ == "__main__":
    main()
