# Decision Log
Format: **Date | Decision | Rationale (1 line)**

> **Canonical results note (2026-06-21):** the dated entries below record decisions *and the numbers
> believed at the time of each decision*. Several of those numbers were later revised by the internal
> adversarial referee review. For the CURRENT state always use
> `04_empirics/H1_volatility/c1_findings.md`. In particular, treat as **superseded** wherever the log
> below states them as live: the SDID **z=−7.7** (a donor-jackknife artifact, withdrawn — pooled SDID
> has NO valid SE), the analytic **p=0.008** as a headline (over-optimistic; honest few-cluster
> p≈0.026 CR1 / 0.046 wild-boot), and **"all falsification tests now PASS" / placebo "insignificant"**
> (the placebo is MARGINAL — it recovers −11.7% ≈ 56% of the headline, p≈0.116 analytic / 0.19 boot;
> and the pre-trend joint p=0.19 masks a significant +10% most-recent lead bin, p=0.049). The
> pre-fix "−16.4% / p.029", "−18.8% / p.003", and the old placebo "−13.6% / −12.8%" figures are
> historical "before" values, not current results.

- 2026-06-10 | Core trio = wheat, chana, CPO; rest to appendix | Depth over breadth for journal referees
- 2026-06-10 | Identification hierarchy: chana cleanest, CPO best intl, wheat most confounded | Wheat hit by export ban + stock limits + OMSS post-2021
- 2026-06-10 | Attack order H8→H4→H2→H1→H3/H7→H6→H5 | Momentum + de-risking: quick wins while NCDEX access resolves
- 2026-06-10 | H5 kept descriptive only | Dabba trading unobservable; causal claims indefensible
- 2026-06-10 | Software = Python | User choice; stack: pandas/statsmodels/linearmodels/arch
- 2026-06-10 | NCDEX public bhavcopy floor = July 2024 | Plan B: vendors → Wayback → academic request (email drafted); MCX twin needed for CPO
- 2026-06-10 | Lost-results summary recovered; V0 replication module created as PRIORITY ONE | Claims: +8-10% vol (DiD), basis widening + GARCH sig@10%, inflation transmission. C2 internally inconsistent (no post-ban basis possible) → full pre-registered verification before reuse
- 2026-06-10 | Options data EXCLUDED; futures only; 12 commodities across NCDEX+MCX | See 02_data/sources/data_specification.md
- 2026-06-10 | Folder made Claude-Code-turnkey: CLAUDE.md (agent rules) + TASKS.md (execution queue) added | Division of labor locked: Claude Code executes, researcher verifies, chat decides
- 2026-06-10 | Keep ALL contract legs (c1/c2/c3) for every commodity where they exist | May use one or a combination; choice needs theoretical backing — pending design discussion
- 2026-06-10 | Turmeric leg set = c1/c2 only and is COMPLETE | Exchange lists only two expiries at a time; c3 does not exist (researcher-verified)
- 2026-06-10 | CPO futures sourced from MCX contract-level bhavcopy (64 contracts), NOT vendor continuous | Exchange data carries volume+OI and lets us control/document the splice; vendor lacked both
- 2026-06-10 | CPO c1/c2/c3 constructed replicating the verified Investing.com convention (expiry-hold, unadjusted) | Comparability with vendor-sourced control series; crossover-roll variant reserved as robustness twin
- 2026-06-10 | New data tier 02_data/constructed/ for derived series (raw -> constructed -> clean) | Constructions are not originals (≠ raw/) and not pipeline-cleaned (≠ clean/); reproducible by script
- 2026-06-11 | Spot route = CEDA Data Portal API (Bearer key in .env); cite CEDA + MoA Agmarknet | Cleaned, documented, programmatic; validate sample vs official portal
- 2026-06-11 | CEDA API rate limit = 40 req/hour (hard) → national pull now (11 req, unblocks V0), district panel as paced ~10h resumable job | National series sufficient for first-pass DiD; district adds FE/within-commodity power later
- 2026-06-21 | TRADING-DAY FIX: spot series restricted to weekdays (Mon–Fri) before returns/RV; panels + V0 rebuilt | Researcher: "clean it properly". Weekend-carried mandi prices + √252 annualization were a units mismatch (calendar-grid bug). Effect (figures as believed at the time; superseded — see c1_findings.md): district DiD −16.4%→−18.8% (p .029→.003); pre-trend test flips from REJECT (p.033) to PASS (p.39); chana GARCH "0.99→0.78/71→46%" collapses to ~flat (0.55→0.69). [SUPERSEDED: the headline is now DiD −20.7% with honest few-cluster p≈0.026/0.046, not p.003; the pre-trend "PASS" masks a +10% lead bin; both −16.4% and −18.8% are pre-fix "before" values.] Pre-fix outputs preserved in git history
- 2026-06-21 | C1 primary estimator = synthetic-control FAMILY (Aug-SCM + Synthetic-DiD co-primary; district penalized SCM) | Naive DiD no longer pre-trend-dead after the data fix, but placebo still recovers −12.8% → magnitude untrustworthy; per methodology_menu §437 [SUPERSEDED on the numbers/role: the −12.8% is an old placebo value (current placebo −11.7%); and post-referee-review the calibrated DiD −20.7% is the headline with the SCM family as MECHANICAL, not independent, corroboration — SDID weights ≈ uniform → collapses toward DiD. See c1_findings.md.]
- 2026-06-21 | Treatment timing = per-commodity ("own") suspension dates | chana 2021-08-16, mustard 2021-10-08, wheat/paddy/soybean/CPO/moong 2021-12-20 (policy ledger); to be wired into the SCM spec
- 2026-06-21 | Pre-registration freeze BEFORE SCM estimation | One frozen primary spec per design + specification curve; lock donor roster + exclusion windows from the policy ledger first
- 2026-06-21 | MSP-censoring handling = HELD for researcher decision (paddy 40.3% / wheat 19.7% flat-return share) | Options being weighed (drop vs censored-model vs flag); not yet enacted
- 2026-06-21 | MSP DECISION RESOLVED: DROP paddy from primary C1; KEEP wheat (MSP-flagged); drop guar id75 | Researcher call. Paddy 40.3% flat daily returns — FCI/MSP procurement pins the spot price, so realized vol is a mechanical censoring artifact not market volatility; paddy is not a core commodity. Wheat 19.7% flat but is core-trio -> kept, flagged, read as robustness. guar id75 gum-contaminated -> guarseed413 is the control. Enacted in utils.EXCLUDE_PRIMARY + all estimators. Effect (figures as believed at the time; partially superseded — see c1_findings.md): DiD -18.8%->-20.7% (honest few-cluster p≈0.026 CR1 / 0.046 wild-boot; the analytic p.008 is over-optimistic); placebo MARGINAL not insignificant (-11.7%, analytic p.116 / boot p.19 — recovers 56% of the headline); pre-trend joint p.19 BUT masks a significant +10% most-recent lead bin (p.049); SDID pooled -26.9% with NO valid SE [the "z-7.7" was a donor-jackknife ARTIFACT, WITHDRAWN]. [SUPERSEDED: the post-referee-review verdict is "falsification MARGINAL, suggestive not conclusive" — NOT "all falsification tests now PASS".]
- 2026-06-21 | guar id-413 vol-panel robustness re-pass DEPRIORITIZED | Researcher: not important; national rebuild already includes guarseed413 and the district panel keeps both slugs for analysis to choose
- 2026-06-21 | C1 DONOR POOL = Option B: clean core {castor, guarseed413, cotton, jeera, turmeric} + ACQUIRE non-banned food staples (coriander, barley first; then maize/jowar/bajra w/ own-policy screen) | Past-researcher rules: same-group, stays-traded-through-ban, no own-shock (drop guar id75, cotton break->futures only). Clean 5 are non-food industrials/spices; food donors restore the food-inflation/MSP channel chana/wheat load on. Build starts on clean core; food donors blocked on CEDA key re-registration (expired ~2026-06-18)
- 2026-06-21 | C1 SPOT LEVEL = district panel (vol_panel_monthly.csv) primary; national = headline charts only | District escapes the few-cluster trap (1,994 units, 130k obs, real cross-sectional variation, supports penalized SCM); national-mean is non-robust (guar 14.3M-Rs outlier) and ~6v6 only. Cluster SEs by commodity regardless (treatment assigned at commodity level)
- 2026-06-21 | C1 SCM build staged: v1 = commodity-level SCM (Abadie) + in-space placebos on district-median series, runnable now on clean core; v2 = district-level penalized SCM + Synthetic-DiD/Augmented-SCM once food donors land | Few-donor inference (5 placebos) is weak by construction -> motivates the food-donor pull; v1 gives point estimates today
