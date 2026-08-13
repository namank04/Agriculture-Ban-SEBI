# Folder Guide — Evaluating India's 2021 Agricultural Derivatives Suspension

Prepared by Naman Karwa - Student, Department of Mathematics, Indian Institute of Technology, Guwahati.

This guide explains how the project folder is organised, where every input, script, and
result lives, and how to reproduce the analysis. The full narrative of the work — data
collection, cleaning, methods, errors and corrections, and findings — is in the
accompanying **work report** (`05_paper/project_report.tex` / its compiled PDF).

## Suggested reading order
1. `05_paper/project_report.tex` (compiled) — the complete work report.
2. `04_empirics/H1_volatility/c1_findings.md` — the canonical, up-to-date results memo.
3. `05_paper/drafts/paper.tex` — the academic paper draft built on those results.
4. This guide, for navigating data and code.

## Folder map

| Folder | Contents |
|---|---|
| `00_admin/` | `data_log.csv` — the provenance log: one row per acquired data series, with source, dates, units, and known issues. |
| `00_code/` | All Python code, in four stages: `download_*.py` (acquisition), `clean_*.py` (cleaning), `build_*.py` (construction of panels/continuous futures), `run_*.py` (estimation), `make_paper_tables.py` (generates the paper's tables directly from result files), `utils.py` (shared constants: ban date, banned list, volatility functions). |
| `01_literature/` | `ban_literature_review.md` (annotated review, ~118 references), `methodology_menu_c1_c2.md` (estimator selection analysis), `references.md` (citation ledger), `papers/` (collected PDFs). |
| `02_data/` | Three tiers. `raw/` — verbatim downloads, never edited (mandi price JSONs, exchange contract files, regulator bulletins, international series). `constructed/` — deterministic derivations from raw (continuous futures series). `clean/` — analysis-ready CSVs produced only by scripts in `00_code/`. |
| `03_policy_timeline/` | `policy_interventions.csv` — 24 dated policy events (the suspension, its extensions, export bans, stock limits, duty changes), each with a primary-source URL. Used to identify confounders. |
| `04_empirics/` | One sub-folder per hypothesis. `V0_lost_results_replication/` (the verification protocol and its outputs), `H1_volatility/` (the central volatility analysis: pre-registration, findings memo, all estimator outputs), `H3_spot_efficiency/`, `H7_harvest_troughs/`, `H8_market_composition/` (each with a `spec.md`, outputs, and a findings memo). H2/H4/H5/H6 hold specifications only (blocked on data availability, explained in the report). |
| `05_paper/` | `project_report.tex` (the work report), `drafts/paper.tex` + `drafts/sections/` (academic paper draft), `drafts/tables/` and `drafts/figures/` (generated tables and figures), `outline.md`. |

## The key result files

| File | What it is |
|---|---|
| `04_empirics/H1_volatility/c1_findings.md` | Canonical results memo (current estimates, robustness, caveats). |
| `04_empirics/H1_volatility/output/c1_robustness.csv` | DiD under filters and leave-one-commodity-out, with honest few-cluster p-values. |
| `04_empirics/H1_volatility/output/c1_sdid_results.csv` | Synthetic difference-in-differences, pooled and per commodity. |
| `04_empirics/H1_volatility/output/c1_scm_results.csv`, `c1_scm_district_results.csv` | Synthetic-control estimates (commodity level and district level), with placebo p-values. |
| `04_empirics/V0_lost_results_replication/output/did_results_district.txt` | Full regression output for the headline DiD. |
| `04_empirics/V0_lost_results_replication/output/placebo_results.txt`, `wild_bootstrap_results.txt` | Falsification battery: fake-2019 placebo, pre-trend test, wild-cluster bootstrap. |
| `04_empirics/V0_lost_results_replication/output/garch_icss_results.csv`, `garch_icss_note.md` | Conditional-volatility (GARCH with structural-break detection) analysis. |
| `04_empirics/H3_.../output/`, `H7_.../output/`, `H8_.../output/` | Companion analyses: spot-market efficiency/integration, harvest-season troughs, market composition. |

## Reproducing the analysis

All scripts use paths relative to the repository root and read from `02_data/clean/`.
With Python 3 and `pip install -r 00_code/requirements.txt`:

```
# headline DiD (district panel; paddy and the mislabelled guar series excluded)
python 00_code/run_v0_did.py vol_panel_monthly.csv district paddy guar

# robustness: filters + leave-one-commodity-out + few-cluster p-values
python 00_code/run_c1_robustness.py

# falsification: fake-2019 placebo + pre-trend test; wild-cluster bootstrap
python 00_code/run_v0_placebo.py
python 00_code/run_v0_bootstrap.py

# synthetic control (commodity and district level) and synthetic DiD
python 00_code/run_c1_scm.py
python 00_code/run_c1_scm_district.py
python 00_code/run_c1_sdid.py

# conditional volatility (ICSS break detection + within-regime GARCH)
python 00_code/run_c2_garch_icss.py

# companion hypotheses
python 00_code/run_h3_efficiency.py
python 00_code/run_h7_troughs.py
python 00_code/run_h8_composition.py

# regenerate the paper's tables from the result files
python 00_code/make_paper_tables.py
```

Two cautions. (1) `download_*.py` scripts re-contact external sources (one requires an API
key, one requires a visible browser session) — they are not needed to reproduce results, as
all raw data is already in `02_data/raw/`. (2) `build_volatility_panel.py` rebuilds the
main panel from raw; running it mid-way through the ongoing donor-data extension will change
the panel composition. The shipped `02_data/clean/vol_panel_monthly.csv` is the panel on
which all reported results were estimated.

## Data status note
The district-level data extension for four additional comparison commodities (groundnut,
sesamum, sunflower, ragi) was still downloading at submission time (the source enforces a
40-requests/hour limit). Results for mustard and soybean are therefore marked provisional
in the report; all other results are estimated on complete data.
