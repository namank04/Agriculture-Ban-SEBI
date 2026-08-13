# WORK DIRECTION — Agri-Derivatives Ban Project
### v1.1 · 10 June 2026 — V0 replication module added as PRIORITY ONE
**Open this file at the start of every working session.**

---

## 1. The one-line mission
Produce a journal-grade empirical evaluation of India's 2021–2026 agri-derivatives suspension: did it deliver price stability, and what did it cost each stakeholder?

## 2. How this folder works (FORMATTING RULES)

```
agri_ban_project/
├── README.md            ← you are here (work direction, rules, status)
├── 00_admin/            ← roadmap, data log, decision log
├── 01_literature/       ← annotated bibliography, paper PDFs, reading notes
├── 02_data/
│   ├── raw/             ← downloads, NEVER edited. One subfolder per source
│   ├── clean/           ← processed datasets, created only by scripts
│   └── sources/         ← source guide + access notes per series
├── 03_policy_timeline/  ← the confounder ledger (interventions dataset)
├── 04_empirics/         ← one folder per hypothesis (H1–H8), each contains:
│   │                       spec.md (what/how/risks) + code + output/
├── 05_paper/            ← outline, drafts, figures, tables
└── 99_parking_lot/      ← ideas explicitly NOT in this paper
```

### Naming conventions (non-negotiable, future-you will thank present-you)
- Files: `lowercase_with_underscores`, dates as `YYYY-MM-DD`
- Raw data: `raw/SOURCE/commodity_frequency_startYYYY_endYYYY.ext`
  e.g. `raw/agmarknet/chana_daily_2017_2025.csv`
- Clean data: `clean/commodity_purpose_vN.csv` e.g. `clean/wheat_spot_h1_v2.csv`
- Scripts: numbered by run order: `01_import.py`, `02_clean.py`, `03_estimate.py`
- Every figure/table for the paper: `05_paper/figures/figN_shortname.ext`
- Drafts: `05_paper/draft_vN_YYYY-MM-DD.md` — never overwrite, always version up

### The three logs (live in 00_admin/, update as you go, not later)
1. `data_log.csv` — every series: what, where from, URL, download date, window, frequency, issues
2. `decision_log.md` — every scoping/methodological decision + one-line rationale + date
3. `session_log.md` — 3 lines at end of each work session: did / found / next

## 3. Locked decisions so far
| Decision | Value | Date |
|---|---|---|
| Target | Journal publication, heavily empirical | locked |
| Core commodities | Wheat, Chana, Crude Palm Oil (4 others → appendix) | locked |
| Event windows | Pre: Jan 2017–Dec 2021 · Post: Jan 2022–latest. Robustness: drop Mar–Dec 2020 | locked |
| Identification hierarchy | Chana = cleanest, CPO = best intl story, Wheat = salient but confounded | locked |
| Attack order | **V0 (verify lost results) → H8 → H4 → H2 → H1 → H3/H7 → H6 → H5** | locked |
| Software | Python (pandas/statsmodels/linearmodels/arch) — see 00_code/requirements.txt | locked |
| Control commodities | **PENDING — candidates: guar, castor, cotton, turmeric, jeera (screening needed)** | open |

## 4. Current sprint (Week 1)
- [x] NCDEX archive tested — floor is July 2024 → Plan B active (vendor test → Wayback → academic email drafted)
- [ ] **Pull Agmarknet district-level data for core trio + 2 controls → unblocks V0 immediately (all public)**
- [ ] Test MCX bhavcopy archive depth (CPO!); send NCDEX academic email; test Investing.com range floor
- [ ] Begin H8: locate SEBI monthly bulletins with participant-wise OI (2019–2021); save PDFs to `02_data/raw/sebi_bulletins/`
- [ ] Begin H4 data pull: CBOT wheat, Bursa Malaysia CPO daily closes 2017–2025 (public)
- [ ] Verify the policy timeline entries marked `VERIFY` in `03_policy_timeline/`
- [ ] Read: Abhijit Sen Committee Report (2008) — notes to `01_literature/`

## 5. Working rhythm with Claude
- Start each session by pasting/uploading the relevant log or file — context restores instantly
- Data lands → upload sample to Claude → get cleaning script → run → log it
- Each H module: read its `spec.md`, work the checklist top to bottom
- Anything that doesn't fit the paper → one line in `99_parking_lot/ideas.md`, move on

## 6. Standing guardrails (referee-proofing — never violate)
1. Never claim the ban *caused* post-harvest food loss (NABCONS context only)
2. Low delivery ratios are normal, not proof of gambling — preempt, don't commit, this fallacy
3. Ukraine contamination → answered by control commodities facing the same shock; say so explicitly
4. Always two-armed: benefit arm + cost arm. Evaluation, not advocacy
5. Every result gets a robustness twin (alt window / alt control / placebo date)

## 7. Status board (refreshed 2026-07-04 — canonical results: `00_admin/RESUME_HERE_2026-06-21.md` + current output CSVs)
> **Headline state:** inherited "+8–10% vol rose" claim is **REFUTED**. The latest food-donor rerun
> materially revises the earlier clean-core result: aggregate C1 DiD is **−9.8%** and **not robustly
> significant** (CR1 p≈0.145; wild bootstrap p≈0.153). The defensible headline is donor sensitivity:
> the suspension is associated with lower spot volatility **concentrated in chana**, while the aggregate
> effect is modest and not significant under a better food-staple counterfactual. Wheat now collapses to
> ~zero in SDID (+0.4%), consistent with MSP/export-ban confounding. C2/GARCH "elevated vol" remains
> **not supported / inconclusive**. Framing = descriptive/quasi-causal, explicitly hedged.

| Module | Status |
|---|---|
| **V0 lost-results replication** | ✅ **verdict delivered — "+8–10% rose" REFUTED; see V0 verdict + c1_findings.md** |
| H1 volatility (C1) | 🟡 **latest: aggregate ~−10% spot vol, NOT significant; chana-centered effect; full oilseed/ragi donor pull pending** |
| H8 market composition | 🟢 descriptive done — pre-ban agri segment ~98.5% speculative, ~1.4% hedger turnover (10/33 bulletins) |
| H3 spot efficiency | 🟡 done, underpowered — cross-mandi cointegration DiD −0.22 (MWU p≈0.07): efficiency/integration LOSS |
| H7 harvest troughs | 🟡 done — harvest-trough deepening NULL (p=0.20) |
| C2 GARCH/basis | 🟡 GARCH "elevated vol" not supported / inconclusive; basis internally impossible post-ban (no futures) |
| H4 insulation | ⬜ blocked on vendor futures (FCPO) |
| H2 price discovery | 🔒 blocked on NCDEX banned-futures access |
| H6 acreage response | ⬜ queued (high risk — droppable; needs sowing data) |
| H5 migration | ⬜ descriptive only |
| Policy timeline | ✅ verified — 22/24 rows primary-sourced |
| Literature | 🟡 118 refs / 67 PDFs swept; methodology menu C1/C2 written; many entries remain MANUAL/paywalled and need page-level verification before submission |
