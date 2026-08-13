# Research Roadmap — The Cost of India's Agri-Derivatives Suspension (2021–2026)

**Target:** Journal publication, heavily empirical (econometrics)
**Researcher:** Solo (with Claude as research assistant throughout)
**Status anchor:** Ban in force Dec 2021 → extended to 31 March 2027 (per the verified policy ledger; SEBI suspension chain reconstructed in the chronicle); SEBI actively reviewing lifting it. Timing advantage: finish before/around the policy decision.

> **Note (2026-06-21):** this roadmap is the original *plan*; for current empirical findings the
> canonical source is `04_empirics/H1_volatility/c1_findings.md`. Headline so far: the inherited
> "+8–10% vol rose" hypothesis (H1) is **refuted** — spot vol is ~20% **lower** post-ban, but the
> result is **suggestive/quasi-causal, not conclusive** (borderline few-cluster significance,
> marginal placebo). Do not cite this file for results.

---

## Working title (draft)

*"Banning the Messenger: Did India's Suspension of Agricultural Derivatives Deliver Price Stability, and at What Cost? Evidence from the 2021–2026 Episode"*

## Core research question

Did the December 2021 suspension of derivatives trading in seven agricultural commodities reduce spot-price volatility and improve price stability in the underlying physical markets — and what were the costs in terms of price discovery, hedging effectiveness, market efficiency, and farmer decision-making?

## Commodity scope (DECISION MADE — confirm)

**Core trio:** Wheat, Chana, Crude Palm Oil. Remaining four (paddy non-basmati, moong, mustard complex, soybean complex) → robustness appendix.
*Rationale: wheat = political salience + large spot market; chana = deepest pre-ban NCDEX futures data; CPO = import-dependent, cleanest international benchmark (Bursa Malaysia), sharpest insulation test.*

---

## Hypotheses (locked from prior session)

| # | Hypothesis (null to test) | Empirical method | Paper section |
|---|---|---|---|
| H1 | Spot volatility of banned commodities did NOT decline post-ban relative to controls | DiD + synthetic control on volatility; GARCH/EGARCH pre-post | "Did the ban work?" |
| H2 | Pre-ban, futures led spot in price discovery (information share > 50%) | Johansen cointegration → VECM → Hasbrouck / Gonzalo-Granger information shares | "What was lost — discovery" |
| H3 | Post-ban, spot markets became less informationally efficient & less spatially integrated | Variance ratio tests pre/post; inter-mandi cointegration pre/post | "What was lost — efficiency" |
| H4 | Domestic prices did NOT decouple from international prices post-ban (insulation failed) | Cointegration/pass-through of domestic spot vs CBOT (wheat) & Bursa Malaysia (CPO), pre vs post | "Did the ban work? (insulation)" |
| H5 | Trading interest migrated to substitute venues post-ban | Descriptive: non-banned NCDEX contract volumes, international OI proxies; framed cautiously (dabba unobservable) | "Where did the market go?" |
| H6 | Sowing-area price-responsiveness weakened post-ban (farmers lost forward signal) | Nerlovian acreage-response model: futures price at sowing (pre-ban) vs lagged spot only (post-ban) | "Farmer decision channel" |
| H7 | Harvest-time price troughs / distress-sale pressure deepened post-ban | Seasonal price-spread + mandi arrivals analysis (Agmarknet), pre vs post | "Storage & distress-sale channel" |
| H8 | Pre-ban speculation was NOT excessive relative to hedging demand | Working's T speculation index; participant-category OI shares; delivery-ratio analysis (with correct interpretation) | "What kind of market was banned?" |

**Framing guardrails (referee-proofing):**
- NEVER claim the ban *caused* post-harvest food loss. NABCONS loss data (₹1.53 trillion/yr, cereals 3.89–5.92%) is *context only* — physical causes dominate. Frame as foregone improvement.
- Low delivery ratios are NORMAL in futures markets, not evidence of gambling — preempt this folk argument explicitly.
- Ukraine-war contamination of post-period → answered by design: controls faced the same global shock. State in identification section.
- Two-armed framing always: benefit arm (regulator's implicit goal) + cost arm (stakeholder losses). Evaluation, not advocacy.

---

## Phase plan

### PHASE 0 — Setup & scoping (Week 1)
- [ ] Confirm core trio of commodities
- [ ] Define event windows: Pre = Jan 2017–Dec 17 2021 (5 yrs); Post = Jan 2022–latest available. Sensitivity: exclude Covid-spike months Mar–Dec 2020 as robustness
- [ ] Pick control commodities (candidates: guar seed, castor, cotton/kapas, turmeric, jeera, coriander — must have continuous futures trading through 2021–25)
- [ ] Set up project folder structure + data log (every series: source, URL, download date, frequency, units)
- [ ] Choose software (R or Python — decide once, stay consistent)
- **Claude's role:** draft folder structure, data-log template, control-commodity suitability screening

### PHASE 1 — Literature & institutional record (Weeks 1–3, parallel with Phase 2)
- [ ] Abhijit Sen Committee Report (2008) — the historical anchor; read fully
- [ ] Post-2008 ban literature (Nair 2011, Lingareddy 2008/2015, Sahadevan, Bose)
- [ ] 2021 ban-specific studies (scan SSRN, EconPapers, Indian journals — under-studied = your gap, but must verify)
- [ ] International evidence: futures bans/restrictions & spot volatility (China's interventions, Working 1960, Jacks 2007 "Populists v. theorists")
- [ ] Regulatory record: every SEBI extension order Dec 2021 → present; CPAI representations; SEBI working-group papers from current review
- [ ] ICRIER WP 383 (farmers–futures linkage); DES report "Futures Market for Agricultural Commodities in India" (2021–22); Tamil Nadu farmer-perception dataset (PMC9278025)
- **Deliverable:** annotated bibliography + 2-page "gap statement"
- **Claude's role:** search & summarize papers, build the bibliography, draft the gap statement

### PHASE 2 — Data collection (Weeks 2–6) ← critical path
| Series | Source | Window | Used for |
|---|---|---|---|
| Daily futures prices, volume, OI (banned trio + controls) | NCDEX historical data / annual reports; Bhavcopy archives | 2017–Dec 2021 (banned); 2017–2025 (controls) | H1, H2, H5, H8 |
| Daily/weekly spot & mandi prices, arrivals | Agmarknet, DES, NCDEX polled spot | 2017–2025 | H1, H3, H6, H7 |
| Participant-category open interest | SEBI monthly bulletins (~2019 onward) | 2019–Dec 2021 | H8 |
| Delivery data per expiry | NCDEX/NCCL circulars & reports | 2017–2021 | H8 |
| International prices | CBOT wheat, Bursa Malaysia CPO, CBOT soy | 2017–2025 | H4 |
| CPI/WPI food sub-indices | MoSPI, Office of Economic Adviser | 2017–2025 | Context, H1 |
| Sowing area by crop/state | DES Land Use Statistics, state ag depts | 2015–2025 | H6 |
| Exchange rate USD/INR, MYR/INR | RBI | 2017–2025 | H4 pass-through |
| NABCONS 2022 + ICAR-CIPHET 2015 loss studies | MoFPI / PIB | — | Context framing only |
- [ ] Build master data log as you go; flag every gap immediately
- **Known risk:** pre-ban NCDEX bhavcopy access may need exchange request or paid vendor — test access in Week 2, not Week 6
- **Claude's role:** cleaning scripts, format harmonization, merging, gap diagnostics, descriptive stats

### PHASE 3 — Empirics (Weeks 6–14)
Order matters — each block feeds the next:
1. **Descriptives & stylized facts** (volume collapse, NCDEX agri share over time, price charts) — also your Figure 1
2. **H2 first** (pre-ban price discovery) — establishes something real was lost; foundation for everything
3. **H8** (market composition pre-ban) — establishes *whose* market it was
4. **H1 + H4** (the "did it work" arm) — DiD, synthetic control, GARCH, pass-through
5. **H3, H6, H7** (the cost channels)
6. **H5** (migration) — descriptive, framed last and cautiously
7. Robustness: alternative controls, alternative windows, placebo dates, remaining four commodities
- **Claude's role:** specification drafting, code (R/Python) for every test, diagnostics interpretation, robustness design

### PHASE 4 — Writing & submission (Weeks 12–20, overlaps Phase 3)
- [ ] Skeleton early (Week 12): Intro → Institutional background → Literature → Data → Methodology → Results (benefit arm, then cost arms) → Policy discussion → Conclusion
- [ ] Target journal shortlist (discuss): *Journal of Commodity Markets*, *Food Policy*, *Journal of Futures Markets*, *Economic & Political Weekly* (faster, policy reach), *Indian Economic Review*, *Agricultural Economics*
- [ ] Decide single-paper vs. split (benefit-arm paper + cost-arm paper) once results are in
- [ ] Working-paper version (SSRN) for timestamp + visibility while under review — valuable given live policy debate
- **Claude's role:** section drafting support, referee-objection stress-testing, journal formatting, cover letter

---

## Immediate next actions (this week)
1. Confirm the core trio + control candidates (reply here)
2. Test NCDEX historical data access TODAY — this is the single biggest project risk
3. Start Phase 1 reading with the Sen Committee report
4. Set up the project folder + data log (I can generate both)

## Standing risks
- **Data access (HIGH):** pre-ban futures tick/daily data behind exchange walls → mitigate via annual reports, vendor data, or direct exchange request citing academic use
- **Policy moves before submission (MEDIUM):** if ban is lifted mid-project, reframe as *ex-post evaluation* — arguably strengthens the paper (adds a re-listing event study)
- **Solo workload (HIGH):** mitigate by strict sequencing above; do not parallel-process Phase 3 blocks
- **Scope creep (MEDIUM):** every new idea goes to a "future research" parking lot at the bottom of this file, not into the paper

## Parking lot (future research, NOT this paper)
- Political-economy of recurring bans (election cycles)
- Comparative: US position-limits response vs Indian bans (2008)
- Dabba/informal market estimation
- Re-listing event study (if/when ban lifts)
