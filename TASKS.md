# TASKS — execution queue for Claude Code
(Design/judgment questions go to the researcher, not solved here.)

## Sprint 1 — data acquisition (current)
- [x] git init + first commit of entire project (insurance against another total loss) — done 2026-06-10, commit dc0f2a1
- [x] Kapas (Investing.com) downloaded, cleaned, logged — done in chat 2026-06-10
- [ ] Investing.com pulls → clean via 00_code/clean_investing_futures.py → log:
  - [ ] chana (NCDEX page), range 2017–2021  ← DECISIVE: confirms vendor route for banned commodities
  - [ ] wheat (NCDEX), 2017–2021
  - [x] crude palm oil — SOLVED VIA MCX DIRECT instead (better: volume+OI): 64 contracts
        raw/mcx/ (MCX-001) + constructed c1/c2/c3 in 02_data/constructed/ (MCXC-001..003),
        2026-06-10. Investing.com CPO pull no longer needed.
  - [x] guar seed, castor seed, jeera (NCDEX) 2017–2026 — c1/c2/c3 legs each, plus kapas
        c2/c3 — downloaded, cleaned, logged INV-002..014 (2026-06-10). Convention:
        all legs kept; files named commodity_cN_daily_YYYY_YYYY.csv
  - [x] turmeric (NCDEX) — c1/c2 done; c3 DOES NOT EXIST (only 2 expiries list; see decision_log) — set complete
  - [ ] cotton (MCX), 2017–2026 (c1/c2/c3)
- [~] Agmarknet district-level daily PRICES — RECON DONE 2026-06-11; route is DECISION NEEDED
      (see 02_data/sources/spot_source_comparison.md). Commodity strings SOLVED via
      Agmarknet 2.0 API → agmarknet_commodity_ids.json (wheat=1, chana=6, castor=106,
      jeera=38, turmeric=35, guar=62/342). Recommended: CEDA API (needs free key — researcher
      registers) primary + Agmarknet-official validation. Then I write the puller. UNBLOCKS V0.
- [~] DCA price portal (fcainfoweb.nic.in): CPO/edible-oil wholesale daily → raw/dca/
      — probed 2026-06-11: reachable, ASP.NET report form (report-type + language + date
      selectors); historical retrieval likely per-date (daily report), so 2017–2025 ≈ ~3000
      requests → needs a headed-Chrome puller when prioritized (after spot data)
- [x] SEBI monthly bulletins 2019-01–2021-12 → raw/sebi_bulletins/ (download only;
      extraction script comes after researcher + chat review 2–3 samples)
      — done 2026-06-10, logged SEBI-001. NOTE: format is Word text + Excel tables (SEBI
      dropped PDFs ~2019; Excel is better for OI extraction anyway). 3 manual gaps:
      2019-08 + 2019-09 (whole months), 2020-03 tables file (404 on SEBI server)
- [ ] International: FCPO (Bursa CPO), ZW=F (CBOT wheat) daily 2017–2025 → raw/international/
  - [x] ZW=F done 2026-06-10 via yfinance (00_code/download_international.py), logged INTL-001
  - [ ] FCPO — not on Yahoo; vendor route (Investing.com "FCPO" page) with the other pulls
- [ ] RBI USD/INR reference rate 2017–2025; USD/MYR (FRED DEXMAUS) → raw/international/
  - [x] USD/MYR done 2026-06-10 via yfinance (FRED unreachable from this network), logged INTL-002
  - [~] RBI USD/INR reference rate — probed 2026-06-11: RBI archive is an ASP.NET VIEWSTATE
        form that didn't yield rows via POST or headed-Chrome submit; DECISION NEEDED:
        invest more in the RBI form vs use yfinance INR=X as public substitute (like USD/MYR)
- [x] MCX public bhavcopy archive: probe earliest available date — ANSWERED 2026-06-10:
      CPO expiry dropdown lists contracts back to 2004 (archive deep); access requires a
      real browser (Akamai 403s scripts) — headed-Chrome route scripted in
      00_code/download_mcx_cpo_bhavcopy.py

## Sprint 2 — V0 pipeline (after Sprint 1 prices land)
- [ ] Adapt build_volatility_panel.py COL_MAP to actual Agmarknet headers
- [ ] Build vol_panel_monthly.csv; run run_v0_did.py + run_v0_garch.py
- [ ] Save outputs to 04_empirics/V0_lost_results_replication/output/
- [ ] STOP — verdict on claims C1–C3 is made by researcher in chat, not here

## Blocked/waiting
- NCDEX academic email reply (full bhavcopy w/ volume+OI) — upgrades streams 1&3
  (final draft ready to send: 00_admin/emails/ncdex_academic_data_request_2026-06-11.md —
  fill name/affiliation placeholders, find current contact on ncdex.com, send)
- Control screening memo (chat task) — finalizes donor list
