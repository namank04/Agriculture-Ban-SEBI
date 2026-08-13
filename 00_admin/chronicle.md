# Project Chronicle — the story of how every dataset got here
Running narrative of acquisition/construction work: what was done, why, how, what broke,
what was learned. **Append as the project moves; never rewrite history.** Companion files:
`data_log.csv` (per-series facts) · `decision_log.md` (choices) · `session_log.md` (3-liners)
· `01_literature/references.md` (citations). Git commits are the fine-grained trail.

---

## Chapter 1 — Foundations (2026-06-10, sessions 1–3, chat + Claude Code)
Project scaffolded after total loss of prior work; V0 replication module created as Priority
One because the lost results' flagship claims (+8–10% vol DiD; post-ban basis widening) were
partly *internally impossible* — banned commodities have no post-ban futures, so any post-ban
basis result is a red flag we must never reproduce. NCDEX public archive found to floor at
Jul-2024 → vendor route (Investing.com) tested with kapas and CONFIRMED for pre-2022 data.
`clean_investing_futures.py` built: BOM/date/volume parsing + hard truncation of banned
commodities at 2021-12-20 (rule 4).

## Chapter 2 — Git insurance + internationals (2026-06-10, session 4)
- `git init` + full first commit (`dc0f2a1`) — the "never again" insurance.
- **CBOT wheat (ZW=F)** and **USD/MYR** pulled via yfinance (`download_international.py`),
  2017–2025, logged INTL-001/002. FRED and stooq are unreachable from this network; Yahoo
  substituted as public vendor (same series concept) — noted in log.
- `exchange` column added to data_log (spec action item).

## Chapter 3 — SEBI bulletins for H8 (2026-06-10, session 4)
The H8 input is participant-wise OI in SEBI monthly bulletins, 2019-01–2021-12.
**Access story:** SEBI's listing pages are JS shells; the `getnewslistinfo.jsp` AJAX returns
"No records" for every category tried; the sitemap carries no bulletin URLs. What worked:
detail pages ARE server-rendered for crawler user-agents (Googlebot UA), and detail-page
URLs are discoverable via web search + Wayback CDX. URLs frozen into
`02_data/sources/sebi_bulletin_detail_urls.csv`; `download_sebi_bulletins.py` rewritten
manifest-driven. **Result: 33/36 months** (66 files). Discovery: SEBI stopped publishing
bulletin PDFs ~2019 — format is Word (text) + Excel (tables); Excel is better for OI
extraction anyway. Gaps for manual pickup: 2019-08, 2019-09 (detail pages unfindable),
2020-03 tables (404 on SEBI's own server). Logged SEBI-001.

## Chapter 4 — Literature & references (2026-06-10, session 4)
2021-ban literature swept (reading_list Tier 3a–c): **Aggarwal–Chatterjee–Sehgal** (SSRN
4261360 — synthetic control on this exact ban; overlaps our H1, read before locking specs);
**Gaurav–Pandey** (IIT-B SJMSOM) and **Rajib–Arora–Barai** (BIMTECH) — two SEPARATE 2024
reports though press bundles them; **Dey–Gairola** (EPW 2024). Spot-provision mechanics
documented (Agmarknet = APMC keyed entries; eNAM = e-auction transactions; NCDEX polled spot
settles futures; Agriwatch = private poller). MSP = regionally-binding confounder (wheat).
Reference ledger created: `01_literature/references.md` + `papers/` (3 PDFs in hand:
ICRIER WP383, NCDEX AGRIDEX methodology, Jha MSP). CEDA (Ashoka) cleaned Agmarknet mirror
found — candidate V0 unblock, **decision pending**. Press reports ban extended to 2027 —
verify against actual SEBI circular for the policy timeline.

## Chapter 5 — Control futures, three legs each (2026-06-10, session 5)
Researcher downloaded Investing.com continuous series as **c1/c2/c3 legs** (front/next/far)
for castor, guar, jeera, kapas (+turmeric c1/c2 — **c3 does not exist**: only two turmeric
expiries list at a time). 13 files renamed to `commodity_cN_daily_YYYY_YYYY.csv`, cleaned,
logged INV-002..014. A re-downloaded kapas c1 was md5-identical to the original → deduped;
original later restored from git history under the leg convention after an accidental
deletion (insurance worked).
**Findings:** c1/c2 are analysis-grade (≤5% flat quotes, 98–99% usable volume — vendor
volume IS usable; kapas was the outlier, not the rule); c2 is uniformly the cleanest leg;
c3 thin everywhere (34–44% flat); kapas weak in all legs (control-screening evidence).

## Chapter 6 — Reverse-engineering the vendor's roll convention (2026-06-10, session 5)
Question: what does Investing.com do at expiry, so our own constructions can match?
`explore_roll_convention.py` detects roll days as "c1 today adopts c2's yesterday price".
**Verdict:** rolls cluster on day 21 of the month = the day after the NCDEX ~20th expiry →
the vendor holds the front contract through its last trading day, switches the next session,
and leaves the splice UNADJUSTED (median artifact ~2% per roll). Mild pre-roll thinning.
Implication recorded: roll-day returns in all vendor series must be flagged at cleaning.

## Chapter 7 — MCX CPO: the real thing (2026-06-10, session 5)
Goal: contract-level CPO futures (banned commodity, MCX), 2017 → suspension.
**Access story:** mcxindia.com 403s every non-browser client (curl with cookies, WebFetch,
even headless Chrome). What worked: **headed real Chrome** via Playwright (project `.venv`),
visiting mcxindia.com only. The bhavcopy page's own JS exposed the endpoint + payload:
`POST /backpage.aspx/GetCommoditywiseBhavCopy {Symbol, Expiry, FromDate, ToDate,
InstrumentName}`. The expiry dropdown enumerated CPO contracts back to 2004 (answers the
old "archive depth" probe); last listed contract = 29APR2022 (the suspension froze the
product). `download_mcx_cpo_bhavcopy.py` pulled **all 64 contracts 31JAN2017–29APR2022,
zero failures**, ~104–110 rows each, saved as verbatim JSON (raw). Fields include
**Volume, Value, OpenInterest** — the columns the vendor route lacked. Logged MCX-001.
**Critical data discovery:** rows continue months past the 2021-12-20 suspension as
settlement-only marks (O=H=L=0). These stale quotes are exactly why rule 4 (hard truncation)
exists — and likely what fooled the lost work into "post-ban" results.

## Chapter 8 — Constructing CPO c1/c2/c3 (2026-06-10, session 5)
`build_mcx_continuous.py` chains the 64 contracts into continuous legs replicating the
verified vendor convention (expiry-hold, switch next trading day, unadjusted), **raw-phase
discipline: nothing filtered** — zero-OHLC and stale post-ban rows kept for cleaning to
handle. Output mimics the Investing.com export structure (so the standard cleaner ingests
it) + extra columns: Open Interest, Contract Expiry, Days To Expiry, Roll Day. One
construction bug caught: pre-2017 dates would mislabel JAN2017 as front (nearer 2016
contracts not in our set) → validity trim at 2016-12-31, landing the series exactly on the
spec window start. Verified against the 31JAN2017 expiry: c1 holds to 31-Jan then adopts
FEB (roll-flagged); c2 simultaneously FEB→MAR — the whole chain rolls on the front's expiry.
Output: `02_data/constructed/` (new folder for derived, pre-cleaning series), logged
MCXC-001..003. c1: 1,368 rows, 63 rolls; c2: 1,348/62; c3: 1,325/61.

## Chapter 9 — Confounder ledger verified + spot-source recon (2026-06-11, session 7)
Policy timeline taken from seeded-from-memory to primary-sourced: 24 rows, 22 CONFIRMED with
`source_url` and exact dates (3 narrow VERIFYs left). Full SEBI suspension chain reconstructed
— original 2021-12-19 order + six extensions (PR 25/2023, PR 16/2025, PR 21/2026 identified;
current end 2027-03-31). Edible-oil duty cuts (2021-10-14, 2022-02-12), TRQ (2022-05-24),
wheat/rice export controls, and the 2023–2025 stock-limit cycle all date-pinned; chana stock
limit corrected to 2024-06-21.
**Data-source recon:** RBI USD-INR reference-rate archive is an ASP.NET VIEWSTATE form whose
results render via a JS path that resisted both the POST round-trip and a headed-Chrome submit
(no rows returned) — **needs more work or the yfinance INR=X substitution (researcher call)**.
FBIL is a thin JS shell. DCA (fcainfoweb.nic.in) reachable, also an ASP.NET form — full pull
deferred (probe only). **Spot sources:** big find — Agmarknet 2.0 exposes a public JSON API
(`api.agmarknet.gov.in/v1/`, no key); the 571-commodity id↔name list was pulled and saved
(`agmarknet_commodity_ids.json`), CLOSING the missing-acquisition-manual blocker (wheat=1,
chana=6 "Bengal Gram(Gram)(Whole)", castor=106, jeera=38, turmeric=35, guar=62/342). CEDA
(Ashoka) offers the same data cleaned via an API needing a free key. eNAM = transaction-price
validation source only. Comparison + recommendation in `spot_source_comparison.md`
(DECISION NEEDED: CEDA-primary vs Agmarknet-primary).

## Chapter 10 — CEDA spot data: national landed, district paced (2026-06-11, session 8)
Spot route executed. CEDA API reverse-engineered from its OpenAPI spec (base `/v1`,
`Authorization: Bearer`, endpoints commodities/geographies/prices); key in git-ignored `.env`
(expires 2026-06-18). **Hard lesson: the API caps at 40 requests/hour** — the first puller's
blind 429-backoff silently burned the quota (wheat ran 17 min, 0 rows). Rebuilt the puller to
be rate-limit-aware (reads RateLimit-Remaining/Reset + Retry-After, sleeps to the window) and
resumable (one file per unit). **Commodity-id trap avoided:** CEDA ids differ from
agmarknet.gov.in (turmeric 39≠35, jeera 42≠38, guar 75≠62, castor 123≠106) — verified all 11
against /commodities before pulling.
**Phase 1 (national) COMPLETE & committed:** 11 commodities (6 banned treatment + 5 control),
daily min/max/modal, 2017-01-01..2025-10-30, ~3052–3212 rows each, 35,020 total
(`raw/agmarknet/national/`, CEDA-NAT-001). **V0 is unblocked.**
**Phase 2 (district panel) running paced in background:** big states (UP/Rajasthan) 504'd on
full-9yr×all-districts responses → puller now adaptively halves the date range on persistent
504 until the server returns it. ~396+ requests at 40/hr ≈ many hours, resumable
(`raw/agmarknet/district/<slug>__state<sid>.json`). CEDA browser tool (bulk CSV) was
unreachable, so the paced API is the only route.

## Chapter 11 — District panel finished, guar repaired, MCX cotton (2026-06-12, session 9b)
The paced district pull **completed: 396/396 state-files, 5.74M market-day rows, 0 dropped**
(CEDA-DIST-001), after a terminal crash mid-run was recovered (resumable one-file-per-unit
design + an hourly health-check cron). **guar forensics paid off:** CEDA id 75 "Guar" is
gum-contaminated (corr 0.038 vs guar futures; gum is a ~10× refined product); id 413
"Guar Seed" is the true futures underlying (corr 0.987, stable +10% basis) → guar control
switched to id 413, its own district pull launched (CEDA-DIST-002). **MCX cotton acquired**
via the same headed-Chrome route — **both generations**: COTTON (77 contracts, 170kg bale)
and COTTONCNDY (15 contracts, 356kg candy), expiries enumerated from the data, 0 failures;
c1–c3 constructed per the CPO convention (MCX-002/003, MCXC-004/005). Cotton's usability is
compromised twice over: it had its **own** anti-speculation halt (Aug-2022) and a bale→candy
**unit break** at 2023 — flagged as control-contamination. kapas confirmed unusable
(vol>0 only 20–45% of days). District vol panel built: 131,425 commodity×district×month cells.

## Chapter 12 — Literature corpus + methodology menu (2026-06-13, session 10)
An ultracode deep-research workflow (38 agents, 1.73M tokens; survived a session-limit kill +
resume) produced **118 verified references, 67 PDFs** to `01_literature/papers/` (gitignored —
on disk + ledgered, not force-added), and three committed deliverables: `ban_literature_review.md`
(847 ln), `methodology_menu_c1_c2.md` (455 ln), and `references.md` (+55). **Headline methodology
finding:** C1's estimator should be the **synthetic-control family as a convergent panel**
(Augmented SCM + Synthetic DiD co-primary; district-level penalized SCM to escape the
7-treated/~4-control few-cluster trap; scpi/conformal inference; Honest-DiD sensitivity) —
credibility from estimator *convergence*, not any single number. For C2, Hillebrand
neglected-break bias **invalidates** a plain pre/post GARCH-persistence test → ICSS-then-within-
regime is mandatory. Three novel designs (RF-SC, DCBD-GARCH, FDCD) survived a 3-lens hostile
audit as "fixable." The run also **surfaced four pipeline bugs** (now part of the standing
caveat set): (a) distmed files are 7-day **calendar** grids with carried weekend prices →
re-run daily-return work on trading-day-only series; (b) **MSP censoring** (paddy flat-return
40.3%, wheat 19.7%) → pre-register paddy OUT, flag wheat; (c) the spot-vol run-up endogeneity
premise is **contradicted** for chana/wheat/mustard/moong → re-motivate selection on
price-level/CPI inflation; (d) CPO has no mandi spot → route out of the spot-vol headline into
the basis/international track.

## Chapter 13 — The analytical milestone the acquisition was for (2026-06-12 → verdict 2026-06-21)
> **SUPERSEDED — the numbers in this chapter are the pre-fix "before" values, not current results.**
> Canonical current state: `04_empirics/H1_volatility/c1_findings.md` (post trading-day fix, paddy
> drop, GARCH retraction, and adversarial referee review). What this chapter calls the result was
> later revised: the headline DiD is now **−20.7%** (not −16.4%/−18.8%), with **honest few-cluster
> p≈0.026 CR1 / 0.046 wild-boot** (the analytic p=0.008 is over-optimistic); the **−13.6% placebo /
> Wald 8.71 / p=0.033 pre-trend** below are pre-fix artifacts (the current placebo is a MARGINAL
> −11.7%, and the current pre-trend joint p=0.19 masks a +10% lead bin); and the **chana GARCH
> 0.99→0.78 / 71→46%** was a CALENDAR-GRID ARTIFACT (on clean data ≈ flat 0.55→0.69 → C2-vol
> inconclusive). The "naive DiD is dead → SCM primary" framing here is also superseded: after the
> data fix the DiD is the calibrated headline, with the SCM family as mechanical (not independent)
> corroboration. The sign-flip conclusion (refutes "+8–10% rose") stands; the magnitudes/inference below do not.

With the district panel in hand, V0's DiD ran at district level — **the single most important
result so far, and a negative one.** National DiD: null (β=−0.0115, p=0.93). District DiD:
**−16.4% (p=0.029) — opposite in sign** to the lost work's claimed +8–10%. And even that does
not survive: a fake-ban **Dec-2019 placebo recovers −13.6% (p=0.046, ~83% of the "effect")**
and the joint pre-trend lead test rejects (Wald 8.71, **p=0.033**). By the pre-registered rule,
**the naive DiD is dead → the synthetic-control family becomes primary for C1.** GARCH adds a
hedged sub-result: national chana persistence 0.99→0.78 and unconditional vol 71%→46% (vol
*down*) — but its district-median counterpart is **degenerate** (persistence pinned at 1.0,
NaN vol; likely the calendar-grid artifact), so the deferred "district-median verdict" never
closed. The full claim-by-claim memo is `04_empirics/V0_lost_results_replication/output/v0_verdict.md`.
**[SUPERSEDED 2026-06-21 — these are the session-13 figures (paddy-included, pre-referee-review). CURRENT
state in `04_empirics/H1_volatility/c1_findings.md`: DiD −20.7% with honest few-cluster p≈0.026 (CR1) /
0.046 (wild-boot) — the −16.4% is a pre-fix "before" value; the placebo is MARGINAL not a clean kill
(−11.7%, recovers 56% of the headline); and the chana GARCH "0.99→0.78 / 71→46%" was itself a
calendar-grid artifact → on clean data ~0.55→0.69 ≈ flat (C2-vol inconclusive).]**
Sessions 11–12 then paused research to build the interview pack (`05_paper/interview_pack/`)
for a 19-Jun interview; session 13 (2026-06-21) audited project state, wrote the V0 verdict
memo, and refreshed this chronicle.

## Standing conventions established so far
- Raw = verbatim originals, immutable; **constructed/** = deterministic derivations
  (script + inputs documented); **clean/** = pipeline-format outputs only.
- Contract legs: keep c1/c2/c3 wherever they exist; files `commodity_cN_daily_YYYY_YYYY.*`;
  leg choice for analysis = open decision.
- Returns across a roll are never computed within analysis (roll days flagged in data).
- Every download → data_log row; every cited document → references.md entry (+ PDF in
  papers/ when downloadable); every method choice → decision_log; story → this file.

## Open items (as of 2026-06-10)
Banned-trio vendor pulls: chana + wheat (NCDEX) still missing — CPO now solved via MCX.
FCPO (Bursa) pending. Cotton deferred until control screening. Agmarknet route DECISION
NEEDED (CEDA mirror vs direct) — blocks V0. Leg-choice DECISION NEEDED. RBI/FBIL USD-INR
pending. 3 SEBI manual gaps. MCX bhavcopy browser probe now MOOT (depth answered).

## Open items (as of 2026-06-21)
*Acquisition is largely done; the project is between the V0 verdict and the SCM rebuild,
paused behind a now-passed interview.*
- **Blocked stream:** the 6 **banned NCDEX futures** (wheat/chana/mustard/soybean/paddy/moong,
  2017–2021) exist nowhere — only CPO (MCX) banned futures were obtainable. NCDEX academic
  request submitted 2026-06-11, reply pending (resend ~2026-06-25). Resolved: spot route
  (CEDA primary), guar (id 413), cotton (acquired, contaminated), MCX bhavcopy depth.
- **Researcher-owned vendor files still pending (block C2 basis):** chana/wheat Investing.com
  daily futures (c1–c3) and FCPO (Bursa CPO).
- **Confirmed data bugs to fix before any further estimation:** calendar-grid returns
  (re-run on trading-day-only series) and MSP censoring (drop paddy, flag wheat).
- **Stale-state cleared this session:** chronicle now covers the district sign-flip (was missing);
  CEDA API key expired ~2026-06-18; all spot series end 2025-10-30; the handoff_2026-06-13
  "deep-research partially failed" item was already resolved by session 10.
- **DECISION NEEDED (rule 6):** ratify "naive DiD dead → SCM primary"; the 11 methodology-menu
  §437 choices; then build the SCM pipeline + guarseed413 panel regen + wild-cluster bootstrap.
