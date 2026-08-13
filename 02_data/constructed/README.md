# 02_data/constructed/ — derived continuous series (pre-cleaning)

Files here are **deterministically constructed** from immutable raw inputs by scripts in
`00_code/` — they are not downloads (so not `raw/`) and not pipeline-cleaned (so not
`clean/`). Re-runnable at any time; never hand-edit.

| File | Built by | Inputs | Convention |
|---|---|---|---|
| `cpo_c{1,2,3}_daily_2017_2022.csv` | `build_mcx_continuous.py` | `raw/mcx/cpo_futcom_expiry_*.json` (64 contracts) | Investing.com-replica: front contract held through expiry day, chain shifts next trading day, unadjusted splice. No filtering — zero-OHLC settlement rows and post-suspension stale quotes retained (cleaning truncates banned commodities at 2021-12-20 per CLAUDE.md rule 4). |

Structure mimics the Investing.com export (Date DD-MM-YYYY newest-first, Price/Open/High/
Low/Vol./Change %) so `clean_investing_futures.py` ingests these unchanged, plus extra
columns: `Open Interest`, `Contract Expiry`, `Days To Expiry`, `Roll Day`.
