# Methodology Menu — C1 (spot-vol effect) & C2 (vol dynamics / basis)

> **STATUS NOTE (2026-07-04).** This decision menu records why the estimator family was chosen; it is
> not the current results memo. The motivating V0 numbers below are superseded by the food-donor rerun:
> aggregate DiD **−9.8%**, not significant (CR1 p≈0.145; wild bootstrap p≈0.153), with the lower-vol
> signal concentrated in chana and wheat confounded. Read the estimator rankings as design guidance,
> not as current findings. Canonical results: `04_empirics/H1_volatility/c1_findings.md`.

Decision menu for the researcher. Reading order: this file assumes the V0 facts are known —
two-way-FE DiD on log realized vol = **−16.4% (p=.029, 11 commodity clusters)**, BUT the Dec-2019
**placebo ban = −13.6% (p=.046)** and the **binned joint lead test rejects (p=.033)**: naive DiD is
DEAD by pre-registered rules. Cause = **policy endogeneity** (ban timing selected on the 2021
food-vol/inflation run-up; banned commodities ran hot ~12 months pre-ban then mean-reverted).

Every estimator choice, donor-pool choice, and pre-registration item below is flagged
**DECISION NEEDED (researcher)** per CLAUDE.md rule 6 — Claude does not make these.

Annotated citations for every method are in `ban_literature_review.md` §4 (causal) / §5 (vol-basis);
PDFs in `01_literature/papers/`. This file gives the verdict grid + the three novel designs.

---

## Part (i) — C1 estimator menu (spot realized-volatility effect)

The question: did the suspension raise spot realized volatility (claimed +8–10% by the lost
analysis)? The binding constraint is policy endogeneity + few treated (7) / few clean controls (~4).

Survives-endogeneity verdict legend: **YES** = design absorbs selection-on-the-2021-run-up;
**PARTIAL** = reduces but does not eliminate it (needs sensitivity layer); **NO** = killed by it.

| # | Method | Key assumption | Survives policy endogeneity? | Difficulty | Software | Our-data adequacy |
|---|---|---|---|---|---|---|
| 1 | **Naive two-way-FE DiD** | parallel trends in log-vol | **NO** — placebo −13.6%, leads reject | trivial | Python/`linearmodels` | DEAD; keep only as the foil |
| 2 | **Honest DiD (Rambachan-Roth)** | bound post-trend by observed pre-trend (M̄) | PARTIAL — quantifies fragility, doesn't fix selection | low | `HonestDiD` (R) | adequate; mandatory sensitivity layer |
| 3 | **Vanilla SCM (Abadie-Diamond-Hainmueller)** | good pre-fit over long pre-period; treated in donor hull; no pre-treatment spike | PARTIAL→YES *if* full 2017–21 pre-window matched (absorbs run-up by matching the path) | low-med | `pysyncon`/`scpi` (Py) | OK national; **noisy vol target → overfit risk** (Abadie-Vives 2022) |
| 4 | **Augmented SCM (Ben-Michael-Feller-Rothstein)** | ridge bias-correction for imperfect pre-fit; multiple treated | YES (best for imperfect fit, our likely case) | med | `augsynth` (R) | fits all 7 treated; SCM-vs-ASCM gap = extrapolation diagnostic |
| 5 | **Synthetic DiD (Arkhangelsky et al.)** | latent factor structure; time + unit weights | YES — time-weights discount anomalous 2021 periods | med | `synthdid` (R) | co-equal; **default jackknife SE unreliable at 7 treated** |
| 6 | **gsynth / IFE (Xu; Bai)** | low-rank factor structure absorbs selection | YES *if* 2021 heat loads on common factors; **NO** on idiosyncratic spike | med | `gsynth` (R) | T~96–108 adequate; bootstrap shaky at ~4 controls |
| 7 | **Matrix completion (Athey et al.)** | low-rank + MAR-given-structure; nests SCM/IFE | YES (same idiosyncratic-spike Achilles heel) | med | `gsynth(mc)`/`MCPanel` | pools all 7 treated + donors; degrades gracefully |
| 8 | **Penalized SCM (Abadie-L'Hour)** | many treated/donors; pairwise-similarity penalty | YES + escapes few-cluster trap | med-high | `pensynth` | **ADOPT IF district-level** — 131k panel → hundreds of treated commodity-districts |
| 9 | **Demeaned SCM (Ferman-Pinto 2021)** | imperfect pre-fit; subtract pre-means | PARTIAL — formally states SC still biased under confounding | low | hand-roll | the on-point robustness layer; pairs with spec test |
| 10 | **Changes-in-Changes (Athey-Imbens)** | monotone rank invariance; stable distributions | PARTIAL — scale-invariant, but no selection-on-transitory cure | med | `qte` (R) | distributional check: did the ban shift the whole vol distribution? |
| 11 | **CausalImpact / BSTS (Brodersen et al.)** | controls unaffected; pre-relationship persists; native seasonality | PARTIAL — same contemporaneous-confounder risk | low | `CausalImpact` (R/Py) | **strong for our seasonal monthly vol** (SCM ignores seasonality); per-commodity cross-check |
| 12 | **Announcement event-study (Casini-McCloskey)** | policy-surprise variance dominates a tight window | **NO** — ban pre-figured by months of inflation, no surprise | low | — | AVOID; cite to explain why event-study is wrong here |

### Inference layer (orthogonal to the estimator — the V0 SE are untrustworthy on cluster grounds alone)
- **scpi prediction intervals** (Cattaneo et al.) — PRIMARY SCM inference engine (Python; multiple
  treated + staggered). Over raw placebo plots, which Ferman-Pinto show mislead.
- **Conformal (Chernozhukov-Wüthrich-Zhu)** — LEAD method per banned commodity as its own series;
  survives a single treated unit + single date. Block-permute on the crop year; prefer the short
  (h∈[1,6]) horizon (the novel-design audits flag anti-conservativeness under strong serial dependence
  + large post/total ratio).
- **Conley-Taber** + **Ibragimov-Müller t-test** + **wild-cluster (Webb 6-pt) bootstrap** — few-cluster
  backstops; IM is the defensible primary at 7-treated/~4-control. RMSPE-ratio statistic (Ferman-Pinto
  2017), Firpo-Possebom sensitivity curve for placebo p-values.
- **Roadmap:** Alvarez-Ferman-Wüthrich (2025) — written for our exact regime (few treated, one date,
  endogenous timing). State which homogeneity/exchangeability assumption underwrites each reported CI.

### RANKED RECOMMENDATION (C1) — DECISION NEEDED (researcher)
**Headline = the synthetic-control family, run as a convergent panel, never a single estimator.**
Justification from our own facts: the naive DiD died because the placebo at Dec-2019 reproduced the
"effect" (mean reversion of the selecting run-up) and the leads reject — i.e. the bias is
selection-on-a-transitory-mean-reverting-shock (Chabé-Ferret 2015 is the formal statement;
Ashenfelter 1978 the original). SCM-family methods attack this directly: by matching the treated
commodity's *actual* pre-ban volatility path (including the 2021 run-up), they absorb the very
pre-trend that biases DiD, and SDID's time-weighting plus gsynth/MC's factor structure absorb the
common 2021 food-inflation shock that DiD mis-attributed. Ferman-Pinto (2021) is the honest caveat —
SC reduces but does NOT eliminate selection bias — so the credibility argument is **convergence of
four estimators** (ASCM ≈ SDID ≈ gsynth ≈ MC) plus Honest-DiD sensitivity, not any one number.

1. **Augmented SCM (#4)** — primary point estimate (built for imperfect pre-fit, our likely case;
   handles 7 treated).
2. **Synthetic DiD (#5)** — co-primary; its time-weighting is the cleanest answer to the 2021 run-up.
3. **gsynth + matrix completion (#6, #7)** — model-based triangulation under the factor story.
4. **Penalized SCM at the district level (#8)** — the route out of the few-cluster trap; multiplies
   effective clusters via the 131k commodity-district panel. **This is the single highest-value
   pivot — DECISION NEEDED on whether to run C1 disaggregated.**
5. **CausalImpact (#11)** — per-commodity seasonal cross-check (SCM ignores seasonality; our vol is
   strongly seasonal).
6. **Honest DiD (#2) + Changes-in-Changes (#10)** — mandatory sensitivity / distributional layers.
- **Inference:** scpi + conformal as primary; Conley-Taber / Ibragimov-Müller / WCB as backstops.
- **DECISION NEEDED:** per-commodity treatment date (chana 2021-08-16, mustard 2021-10-08, rest
  2021-12-20) vs a single Dec-2021 date; donor-pool membership and contamination screening (cotton
  excluded post-Aug-2022); identification hierarchy (chana = cleanest; CPO has **no mandi spot** so it
  cannot anchor a spot-vol headline — route CPO to the basis/international track).

---

## Part (ii) — C2 menu (volatility dynamics & futures-spot basis)

Two arms. **Vol-dynamics arm:** GARCH-family persistence pre vs post (the V0 plan). **Basis arm:**
futures-spot basis — intrinsically **pre-ban-only**, because banned commodities have NO futures after
Dec-2021 (any "post-ban basis" claim is incoherent; this is C2's built-in internal-consistency catch).

### THE central caveat against the current pre/post GARCH-persistence plan
**Hillebrand (2005) + Lamoureux-Lastrapes (1990): an unmodelled variance-level break at the ban date
biases estimated GARCH persistence (α+β) UPWARD toward 1.** Our core C2 test — comparing pre vs post
GARCH(1,1)+ban-dummy persistence — will therefore see a *spurious* persistence change from a single
level shift it failed to model. **Mandatory fix: ICSS-date the variance break first (Inclán-Tiao
1994), estimate persistence WITHIN regimes, and test whether the break actually sits at Dec-2021 vs
elsewhere** (the variance-process analogue of the C1 placebo). Without this, the persistence
comparison is not interpretable. Internal preliminary fits already show the symptom: distmed chana
α+β pins at the IGARCH boundary in split-sample fits.

| # | Method | Key assumption | Survives endogeneity / Hillebrand? | Difficulty | Software | Adequacy |
|---|---|---|---|---|---|---|
| 1 | **Plain GARCH(1,1) + ban dummy, pre/post persistence** | constant params except the dummy | **NO** — Hillebrand-spurious persistence + ban date selected on outcome | trivial | `arch` (Py) | DEAD as headline; foil only |
| 2 | **ICSS-then-GARCH (Inclán-Tiao → within-regime GARCH)** | breaks datable in unconditional variance; pre-whiten first | YES on Hillebrand; PARTIAL on endogeneity (break-date *is* the diagnostic) | low-med | `ICSS`(R)+`arch` | **mandatory baseline**; ~1,250 daily obs/commodity → power |
| 3 | **EGARCH / GJR (Nelson; Glosten et al.)** | log-variance / asymmetric leverage term | inherits #2's break caveat; asymmetry is a *result* (ag sign may invert) | low | `arch` | fine on daily mandi returns; Sobti (2020) precedent |
| 4 | **Markov-switching GARCH (Haas et al.)** | data-chosen high/low-vol regimes | YES-ish — directly models hot-then-revert; do regime probs shift at Dec-2021? | med-high | `MSGARCH` (R) | needs long daily series (have it); composition noise can spuriously switch — robustness only |
| 5 | **Monthly HAR-RV + ban dummy (Corsi, modified)** | RV from within-month daily returns; AR cascade | cleaner than latent GARCH (no distributional assumption) | low | hand-roll/pandas | **131k-cell monthly RV panel fits**; control n-mandis-reporting |
| 6 | **DCBD-GARCH (novel — see Part iii)** | multiplicative long-run component + estimated break date | YES by construction (break-date forensic + staggered coincidence) | high | custom QMLE | core ~90% in hand |

**Basis arm (pre-ban-only by construction):**
| # | Method | Use |
|---|---|---|
| 7 | **Hasbrouck info share + Gonzalo-Granger PT (Baillie et al. pairing)** | pre-ban futures-spot price-discovery share — the magnitude whose loss C2 is about. Indian template: Inani (2018) covers our treated + donors. Report bounds (daily sampling). |
| 8 | **Working/Fama-French storage-theory basis regression** | regress pre-ban basis on interest-rate proxy + harvest/seasonal dummies → carry vs convenience yield. A falling/inverting basis = tightening stocks = the scarcity that plausibly triggered the ban (endogeneity evidence). |
| 9 | **Bessembinder-Seguin expected/unexpected volume + OI in the variance equation** | the MECHANISM: if deep OI dampened spot vol pre-ban, removing futures should RAISE it — a falsifiable C1/C2 prediction. CPO contract-level volume+OI in hand; chana/wheat incoming. Sharma-Malhotra (2015) Indian precedent. |
| 10 | **Diebold-Yilmaz connectedness** | did banned spot become more isolated / more intl-exposed once the NCDEX anchor vanished? Small VAR (~7+4 nodes) — rolling/TVP, interpret cautiously. |
| 11 | **Ederington hedging effectiveness** | COST-ARM (two-armed guardrail): pre-ban risk-reduction the ban forfeited for hedgers. |
| 12 | **Gregory-Hansen / Zivot-Andrews break-robust cointegration** | pre-ban basis cointegration with an endogenous break (COVID-2020 / position-limit curbs) so a constant-parameter test isn't corrupted. |

### RANKED RECOMMENDATION (C2) — DECISION NEEDED (researcher)
- **Vol-dynamics headline:** ICSS-then-within-regime GARCH (#2) as the disciplined baseline, EGARCH/GJR
  (#3) for asymmetry, **DCBD-GARCH (#6) as the publishable estimator** that turns the Hillebrand
  caveat and the break-date into the identification strategy. **Never report a plain ban-dummy GARCH
  persistence change as a result** — it is exactly the doubly-invalid design (Hillebrand bias +
  endogenous date) the prior ban literature ran.
- **Basis headline:** pre-ban Hasbrouck+Gonzalo-Granger discovery share (#7) + storage-theory basis
  characterization (#8) + Bessembinder-Seguin volume/OI mechanism (#9). State up front that basis is
  pre-ban-only; deseasonalize (Yeasin et al. 2024) before any vol contrast.
- **Deseasonalization is mandatory** for every vol comparison (harvest-cycle seasonality, Yeasin 2024).
- **DECISION NEEDED:** which spot is "the spot" (eNAM vs mandi-modal vs NCDEX-polled, Garg 2023);
  whether to demote paddy/wheat from the GARCH set for MSP bottom-censoring; donor set for the
  long-run-component factor.

---

## Part (iii) — NOVEL DESIGNS (surviving + post-mortems)

All three novel designs were audited under a 3-lens hostile review and **kept (verdict: fixable)** —
none survives unmodified; each carries required fixes that are themselves **DECISION NEEDED**.

---

### NOVEL DESIGN 1 — RF-SC: Reaction-Function-Tilted Synthetic Control (target C1)
**Status: KEEP (fixable). Two audits, both "fixable", high confidence.**

**Specification.** Three moves on the 7 banned + ~30–36 listed-not-banned donors:
1. **Pre-run-up-fit SCM.** Per banned commodity, build a demeaned/ridge-augmented synthetic control
   fitting ONLY on 2017m1–2020m12 and **holding out the 2021 run-up window (2021m1→ban date) as an
   out-of-sample overidentification test** of donor spanning — if the synthetic tracks the run-up it
   spans the ban-triggering factor; if not, that commodity is gated out. Turns policy endogeneity from
   an untestable confound into a *testable restriction*.
2. **Estimated regulator reaction function** P(ban | CPI weight, Essential-Commodities-Act status,
   food dummy, import share, trailing 2021 inflation/vol run-up) over all ~43 commodities, used as the
   assignment model for **design-based (tilted) randomization inference** — placebo "banned 7-sets"
   drawn ∝ modeled assignment likelihood, so p-values respect endogenous selection instead of false
   uniform permutation (operationalizes Lei 2024 / Borusyak-Hull 2023 recentering).
3. **Rebound benchmark** (assumption-distinct): predict each banned commodity's counterfactual 2022+
   vol decline from the empirical run-up→reversion mapping among the non-banned commodities
   (Illenberger-Small RTM correction). SC consistent under factor-spanning; rebound consistent under
   selection-purely-on-run-up — agreement = triangulation, disagreement diagnoses which assumption broke.
- **Onset-alignment falsification** from the within-2021 stagger: a causal effect onsets at each
  commodity's own ban date; mean-reversion onsets at the common run-up peak.
- **Inference:** per-commodity conformal (CWZ) + exact tilted randomization across commodities +
  Rosenbaum-Λ sensitivity band for the estimated propensity. No asymptotics in N.
- **Feasibility:** Grade B, 2–4 weeks; binding constraint = the ~30-donor CEDA pull (40 req/hr cap).

**Audit verdicts — issues + required fixes (verbatim-summarised):**
- **FATAL-CANDIDATE: bundled-policy confounding (both audits' deepest flaw).** Every banned commodity
  was simultaneously hit by a co-treatment basket controls were NOT — wheat 6 export-ban/stock-limit/
  OMSS actions, paddy 3 rice export bans, CPO 3+ import-duty swings, chana 2024-06 stock limits. So
  "treatment" = futures-suspension + a commodity-specific trade/stock-policy bundle; τ conflates them
  and A2 is silent on this. **FIX:** redefine the estimand as the bundled policy package, OR exploit
  the staggered timing of the *non-suspension* interventions (export bans land months AFTER Dec-2021)
  to carve a clean **2022-01..2022-04 window where only the suspension is active** and restrict
  tau_early to it, OR use CPO/edible-oils where the duty CUTS push the opposite (price-down) direction
  (sign-conservativeness). A per-commodity "clean window" table from the policy ledger must drive this.
- **CPO has NO spot series in the panel** (verified: no palm/cpo in `vol_panel_monthly.csv`). **FIX:**
  drop CPO from the SC spot-vol headline → route it to the basis/international track; re-anchor on
  chana + one other commodity with both data and a positive run-up.
- **Premise contradicted by data:** at the spot-vol level 4 of 6 available banned commodities have
  NEGATIVE 2021 run-ups (chana −0.18, wheat −0.19, mustard −0.08, moong −0.09) while all 5 controls
  are POSITIVE; chana (the "cleanest" headline) shows a vol DECLINE through 2021. The
  selection-on-RV premise may be false at the spot-vol level. **FIX:** re-derive V_j^run from the
  actual panel; **re-motivate selection on price-level / item-CPI inflation** (what the regulator
  actually reacted to) rather than spot RV — this may run the right way even when RV does not.
- **Overlap / perfect separation is the MODAL outcome, not a tail risk:** if banned = the 7 most
  CPI-salient food commodities, the reaction function separates them perfectly from castor/jeera/guar/
  turmeric (non-food industrials), collapsing the tilted randomization distribution → the headline
  joint p-value is uninformative by construction. **FIX:** seed the donor pool with non-banned FOOD
  commodities carrying CPI weight (barley, sugar, maize, jowar, bajra, ragi, coriander) so overlap is
  even possible; **pre-register that if separation exceeds a threshold the tilted-RI headline is
  abandoned ex ante** and the paper leads with per-commodity conformal + clean-window DiD.
- **Firth logit can't identify 5+ covariates on 7 events / 11 units.** **FIX:** collapse to a 1-D
  pre-registered reaction index (V_j^run + at most one salience covariate) and report the **full
  Rosenbaum-Λ sensitivity curve ("survives Λ ≤ L*") as the headline object**, not a point p-value.
- **Tilted-RI resolution self-defeating at the data in hand:** with only 11 commodities C(11,7)=330,
  and tilting concentrates mass on a few sets → minimum attainable p can exceed 0.05. **FIX:** acquire
  & screen the donor pool FIRST; report realized overlap + effective support size before claiming any
  cross-sectional p-value.
- **Stagger test weaker than claimed:** mean-reversion can onset at commodity-specific *seasonal* dates,
  not a common peak; 5 of 7 share the Dec date → ~2 informative early onsets. **FIX:** simulate
  onset timing under each commodity's estimated seasonal cycle and show observed onsets are
  inconsistent with THAT.
- **Rebound benchmark inference under-specified + extrapolating** (banned R_j at the LOW end of donor
  support). **FIX:** propagate κ̂/β̂ error (jackknife/parametric bootstrap), report whether R_j is in
  support; downgrade to robustness if out-of-support.
- **Measurement comparability:** thin-donor RV is upward-biased/noisier; eNAM rollout can fake vol
  changes. **FIX:** arrivals/coverage + thin-market RV-bias gate per donor before admission.
- **Fit/validation GATE is a pre-test** that distorts the joint null. **FIX:** re-run the gate inside
  each placebo draw, or report per-commodity inference only.
- **MISSING prior art the audit flags:** compound-treatment / bundled-intervention identification
  (Hernán-Robins target-trial; de Chaisemartin-D'Haultfœuille contaminated treatments) — must be
  engaged given the export-ban/stock-limit ledger.

**Honest novelty assessment:** the genuine contributions are (a) an *estimated regulator reaction
function as the assignment model* for design-based placebo inference in SCM (Lei 2024 / Borusyak-Hull
in the small-J single-date regime where applied work uses provably invalid uniform permutations); (b)
the *fit/validation split holding out the run-up window* as an overidentification test of donor
spanning (current SC practice fits straight through the run-up — the RTM trap Illenberger-Small
document); (c) triangulation of two estimators consistent under complementary halves of the selection
problem; (d) the onset-alignment falsification on the unnoticed within-2021 stagger. Not a new
estimator — a novel *assembly*. **What would make it publishable:** the substantive prize (the largest
agri-derivatives shutdown ever, with no correct existing answer) + the methods template
(policy-timing-selected-on-the-outcome with few treated and a modeled selection rule) generalizes to
capital controls / trading halts / export bans → a methods audience (JAE / J. Econometrics applied)
beyond the field audience (JDE / AJAE / J. Commodity Markets). **It is publishable only after the
bundled-policy estimand is honestly redefined (clean-window or sign-conservative) and overlap is
empirically demonstrated** — both DECISION NEEDED.

---

### NOVEL DESIGN 2 — DCBD-GARCH: Donor-Conditioned Break-Dated GARCH (target C2)
**Status: KEEP (fixable). Three audits, all "fixable" (two high, one medium confidence).**

**Specification.** Each commodity's daily spot-return variance is multiplicatively
sigma2 = h·g: a unit-mean short-run GARCH(1,1) g, and a long-run component
ln h = c + s(t) + δ'X_{t-1} + θ·1[t>τ] where X = (matched international futures vol, a donor
log-vol factor = PC1 of the controls, control-futures volume, harvest harmonics) and **the break date
τ is profiled/estimated, not imposed.** Causal object = the step θ_i at each commodity's OWN
suspension date, net of the donor factor; headline = the treated-minus-control contrast in θ. Three
innovations vs the dead naive ban-dummy GARCH:
1. **Break-date confidence set (Eo-Morley 2015) used as an identification DIAGNOSTIC** — if the data
   date the regime change to the mid-2021 surge (that caused the ban) rather than the suspension, the
   method SAYS SO instead of mislabeling mean reversion as policy.
2. **Staggered-suspension coincidence test** (chana Aug, mustard Oct, five Dec) — common-shock mean
   reversion cannot generate commodity-specific breaks at commodity-specific legal dates.
3. **Inference never invokes N-asymptotics at N=11** — per-series null-imposed residual-bootstrap
   sup-LR (answers Hillebrand/Davies break-selection), cross-commodity contrast via exact Fisher
   randomization (330 assignments) + dependence-preserving joint moving-block bootstrap.
- **Mechanism overid (pre-ban only):** loading of ln h on own futures volume/|basis| (CPO has full
  volume+OI) → predicted shutdown effect θ̃_i to compare with θ̂_i; also re-expresses C2's impossible
  "post-ban basis" as the only measurable content (a pre-ban channel extrapolated to market-off).
- **Feasibility:** medium-high, 2–4 weeks; ~90% of data in hand (distmed spot files); main build =
  custom QMLE (~600–900 lines); bootstrap embarrassingly parallel.

**Audit verdicts — issues + required fixes (verbatim-summarised):**
- **Estimand is PARTIALLY identified, presented as point-identified (deepest flaw).** θ is the
  coefficient on a STEP mechanically confounded with any smooth treated-specific long-run vol movement
  the finite Fourier+X basis can't absorb — and mean reversion of the 2021 surge is exactly such a
  smooth movement. The donor factor is COMMON (PC1 of controls); **treated-SPECIFIC mean reversion is
  orthogonal to it by construction and loads directly onto θ.** A sup-LR break test can't distinguish a
  true jump from a sharp continuous bend at monthly resolution, so the break-date diagnostic has LOW
  power against the exact rival it must rule out (and under omitted-persistent-covariate misspecification
  the GARCH-X collapses to IGARCH and the break LOCATION is biased — Han-Park). **FIX:** reframe θ as
  partially identified (a bound/sign test); show θ robust to absorbing arbitrary smooth treated-specific
  drift (a treated-specific pre-ban spline); **build a per-commodity SYNTHETIC combination of controls
  matched on pre-ban variance dynamics** (SCM-in-variance) so the *differential* treated-vs-control
  selection channel — the actual endogeneity mechanism — is differenced out, not just the common factor.
- **A2 not strictly weaker than parallel trends in the way claimed.** A common donor factor cannot
  partial out a treated-vs-control DIFFERENTIAL, which is the very source of endogeneity. **FIX:** promote
  the f-volatility-conditioned (Rosenbaum-adjusted) θ to a PRIMARY result; test state-dependence of α+β
  on the inflation regime.
- **Calendar-day data artifact (verified, unstated).** The distmed spot series are 7-day CALENDAR
  series (~457–460 rows for every weekday incl. Sat/Sun); mandi prices are carried across non-trading
  days → spurious zero-return blocks that break iid-z and GARCH dynamics, and misalign the int'l-vol X
  (CBOT/FCPO trade a different calendar). Near-unity persistence may itself be a zero-inflation
  artifact. **FIX:** re-run on TRADING-DAY returns only (drop carried weekend/holiday rows), re-align X,
  report whether IGARCH-like persistence survives.
- **MSP bottom-censoring is differential and hits the treated set hardest (verified):** flat-return
  share paddy 40.3%, wheat 19.7% vs chana 2.5%, jeera 1.7%, castor 1.1% — concentrated in 2 of 7
  treated, post-period-concentrated → mechanically suppresses post-ban variance, biasing their θ toward
  zero and the contrast. **FIX:** pre-register paddy OUT and wheat as censored-flagged BEFORE
  estimation; add a Tobit/censored-GARCH or mass-at-floor diagnostic; redefine Λ_B over the uncensored
  subset.
- **Sharp-null vs ATT mismatch.** Exact RI (min p=1/330≈0.003) rejects if SOME commodity has a break —
  it does not identify the AVERAGE effect; with verified persistence heterogeneity (treated chana/wheat/
  guar/cotton α+β≈1.00 vs controls castor 0.35, turmeric 0.44, jeera 0.54) the studentized RI can
  reject from a single hot series, and "ATT" is barely distinguishable from "the chana effect." **FIX:**
  report per-commodity θ CIs as PRIMARY; treat the contrast as descriptive at N=7; Conley-Taber interval
  for Λ_B that doesn't assume exchangeability; block-permute within variance-type strata.
- **Exchangeability (A8) FALSIFIED by the project's own data:** treated near-unit-root variance vs
  mean-reverting controls = different process TYPES pre-ban, so the Fisher randomization null is not
  credible and the generated-regressor donor factor (estimated from the permuted units) breaks RI
  exactness. **FIX:** make the studentized RI the SOLE test (drop the "exact" label), wrap factor
  extraction inside each permutation or use a leave-treated-out factor; make the joint block bootstrap
  PRIMARY; pre-commit to reporting the weaker conclusion on RI/bootstrap disagreement.
- **Coincidence test collapses to 2 commodities** (only chana, mustard staggered; both PARTIAL
  new-positions-only bans with attenuated/lagged signatures; surge peaked Oct-Nov 2021 between their
  dates). **CPO confounded by simultaneous import-duty cuts** (2021-10-14, 2022-02-12). **FIX:** demote
  to a 2-commodity targeted test with explicit power analysis + a partial-ban-lag model; drop CPO from
  the stagger test.
- **Pre-test / forking-paths cascade** (LM screen → break test → CS → fix τ → θ → RI, plus
  data-dependent branches) not priced into the headline p. **FIX:** pre-register ONE frozen primary
  spec; route every branch to the appendix; report a specification curve / max-over-specs adjusted p.
- **Two-break misspecification:** Ukraine (Feb-2022, ~2 months post) + COVID-2020 inside the sample →
  one-break long-run component misspecified, Hillebrand within-regime bias re-enters. **FIX:** add the
  two-break / known-event-dummy spec as a reported robustness; exclude COVID window in the primary;
  demote any commodity whose break CS can't be separated from the Feb-2022 date.
- **Internal empirical overstatement (fix before circulation):** the cited chana "α+β 0.99→0.78 across
  regimes" is NOT in `garch_summary_distmed.csv` (which shows pre≈post≈1.0000); the 0.78 must come from
  a break-allowed/covariate-augmented fit. **FIX:** show that fit or drop the specific numbers.

**Honest novelty assessment:** every component is established (Engle-Rangel spline-GARCH; Engle-Ghysels-
Sohn GARCH-MIDAS; Amado-Teräsvirta TV-GARCH; Eo-Morley break CS; Cavaliere et al. bootstrap GARCH;
Conley-Taber / MacKinnon-Webb RI) — and regime-switching GARCH-MIDAS already puts a break in the
long-run component. The novelty is the **assembly**: an SCM-style donor log-vol factor as a long-run
covariate + the break-date CS repurposed as a falsification diagnostic against policy-endogenous timing
+ the staggered-legal-date coincidence test. Referees will read it as "GARCH-MIDAS-with-a-break + a
careful placebo battery" — **incremental-as-method, novel-as-application.** **What would make it
publishable:** lead with the substantive prize (largest/longest suspension) and the demonstrated
DOUBLE failure (naive DiD AND naive GARCH-dummy both invalid here), reframe novelty honestly against
regime-switching GARCH-MIDAS, and execute the SCM-in-variance per-commodity donor fix so the
treated-specific selection channel is actually differenced out (otherwise the headline diagnostic
self-undercuts). Theory home: Kawai (1983) vs Turnovsky-Campbell (1985) on whether futures stabilize
storable-commodity spot prices. Outlets: JAE / J. Financial Econometrics / J. Commodity Markets / AJAE.

---

### NOVEL DESIGN 3 — FDCD: Factor-Differenced Convergence Design ("reverse telegraph") (target both)
**Status: KEEP (fixable). Two audits, both "fixable" (one high, one medium confidence).**

**Specification.** Treats the futures market as information infrastructure (the inverse of
Steinwender's 1866 telegraph) and asks whether its removal slowed price-convergence speed — across
districts (Layer B, primary) and world→domestic (Layer A, mechanism case studies). District log
prices p_idt = δ_id + f_it + w_idt; the policy was selected on the history/level of the common factor
f, but **pairwise district differencing g_ij,t = p_idt − p_jdt annihilates f exactly**, so the
convergence-speed parameter ρ of the LOP wedge is identified from relative prices invariant to the
selection variable by construction. Estimand = a DiD in convergence speed (log half-life of
district-pair gaps), treated (6 banned in the mandi panel) vs controls (castor, jeera, turmeric,
cotton-ex-halt; guar pending id-413). **Refutation architecture:** exact permutation inference over
C(10,6)=210 assignments; a **dose-response test using pre-ban futures liquidity** (moong/paddy futures
near-dead → built-in zero-dose placebo-treated units); an **A-B-A reversal test from MCX cotton's own
Aug-2022–Jan-2023 halt.** This is the mechanism behind C1 (does lost discovery raise vol via slower
aggregation?) and the post-ban continuation of C2 (price discovery from what remains observable, since
basis dies with futures).
- **Feasibility:** medium, 4–6 sessions; Layer B runnable from data already on disk (needs only a
  district-day cleaning script); does NOT need post-ban futures for banned commodities (which don't exist).

**Audit verdicts — issues + required fixes (verbatim-summarised):**
- **"f cancels EXACTLY" is FALSE under heterogeneous factor loadings (the load-bearing flaw).** The
  model imposes a UNIT loading on f; if districts load heterogeneously (λ_id·f_it), differencing leaves
  (λ_id−λ_jd)·f_it in the gap → g is NOT f-invariant and selection-on-f CAN bias the estimand (the whole
  CCE/IFE literature exists because simple differencing fails here). A1 (pairwise stationarity) only
  holds under common loadings. **FIX:** make loading-homogeneity an explicit TESTED assumption — estimate
  the commodity factor (PC1), regress each district on it, restrict pairs to indistinguishable loadings,
  and where loadings differ switch to CCE-residualised / interactive-FE (Bai 2009) wedges before the AR.
- **Exactness overstated — RI is not size-exact at these N.** Simulated: with the coefficient statistic
  and heteroskedastic Δ_i (controls 3× noisier — the expected case: dense MSP staples vs thin spice
  markets, jeera 33 vs paddy 335 districts) RI rejects at 8.2% vs nominal 5%; **studentized RI still
  7.5%** because per-group variances are themselves noisy at 4 controls. **FIX:** make the studentized
  (MacKinnon-Webb 2020) t-RI the SOLE primary test, stop calling it "exact," and **Monte-Carlo-calibrate
  its finite-sample size**; report a size-adjusted critical value if nominal exceeds ~6%.
- **A1 pre-test biases the estimand toward the hypothesis (regression-to-the-mean).** Keeping pairs
  that reject a unit root in the PRE period only drags ρ_pre artificially down while leaving ρ_post
  alone → simulated SPURIOUS Δρ of +0.02 to +0.07 (a fake "slowdown," the hypothesized sign), worst for
  thin controls, so it does NOT cancel in the DiD. **FIX:** screen SYMMETRICALLY (reject unit root in
  pre AND post, or in a disjoint pre-pre window), run a placebo-screen Monte Carlo confirming
  E[Δρ]≈0 per commodity, and report/subtract the per-commodity screen-induced bias.
- **Selection on the LEVEL of f need not be orthogonal to the SPEED ρ** (state-dependent menu-cost
  adjustment: bands narrow when f runs hot). **FIX:** promote the pre-period-f-volatility-conditioned Δ_i
  (currently buried as diagnostic D8) to a NECESSARY identification requirement, not optional.
- **Transformation-aggregation bias (internal inconsistency):** Δ_i = h(mean ρ) but mean-group / Imbs et
  al. require mean(h(ρ)); Fisher-z/half-life are nonlinear. **FIX:** redefine Δ_i = trimmed-mean of
  pair-level h(ρ_post)−h(ρ_pre); bias-correct on the statistic, not on ρ.
- **Differential small-T (Nickell) bias does NOT cancel:** Δ_i differences two AR(1) estimates from
  periods of different length (T_pre≈1200, T_post≈1000) → a spurious component with the same sign as a
  "slowdown." **FIX:** median-unbiased (Andrews 1993) ρ before differencing and/or equalize T_pre/T_post;
  validate with a pre-period-only placebo at a fake date with the same length ratio.
- **Layer A break-search multiplicity handled inconsistently** (many candidate break dates near the ban
  in the ledger: CPO duty 2021-10-14/2022-02-12/2024-09-14, wheat export 2022-05-13, rice 2022-09-08).
  **FIX:** pre-commit IN WRITING to the single ban date as the only split examined and list all
  confounder dummies before estimation, else use sup-Wald (Andrews) / Bai-Perron critical values.
- **Effective-N / combinatorics fragile to the roster** the project itself flags (CPO→Layer A, guar
  pending, cotton double-duty as control AND reversal unit): each change moves the p-floor (C(8,4)=70 →
  min p=0.014 fails 1%; C(11,7)=330). **FIX:** finalize the roster BEFORE estimation, state the
  resulting C(n,k) and p-floor, lock cotton's halt-exclusion window from the ledger, run both plausible
  rosters as a robustness band.
- **Dose-response p miscounted + underpowered** ("6! orderings" is a Spearman permutation on 6 ranks,
  min p=0.0014; moong/paddy as zero-dose leave ~4 informative points). **FIX:** reclassify as
  descriptive/illustrative, not inferential support.
- **Power triage:** with 6 treated / 4 controls and large Δ_i dispersion, "directionally consistent,
  not significant" is the MODAL outcome. The wheat/paddy logistics-confound exclusions remove 2 of the
  3 zero-dose commodities. **FIX:** lean inference on (a) the exclusion-robust treated set (chana,
  mustard, soybean, moong), (b) the cotton A-B-A reversal as the strongest single causal contrast
  (immune to the H5 SUTVA bias and the 210 floor), (c) the dispersion-IQR corollary on the 131k-cell
  monthly panel which has far more cross-sectional units; pre-commit to reporting a bounded null as
  informative.

**Honest novelty assessment:** survives a hostile novelty search — no existing 2021-ban work (Dey-
Gairola; BIMTECH; Aggarwal-Chatterjee-Sehgal) or 2008-ban work estimates a causal effect on SPATIAL
price-convergence speed, and none exploits factor-differencing to neutralize selection-on-the-outcome-
level. But every COMPONENT is off-the-shelf (Steinwender 2018 telegraph/LOP; Goyal 2010 ICT-mandi-
soybean in literally adjacent markets; Obstfeld-Taylor band-TAR; Duranton-Gobillon-Overman spatial
differencing; Pesaran-Smith mean-group; MacKinnon-Webb/Conley-Taber RI; Imbs et al. half-life
aggregation). It is a **recombination — incremental-but-real, not category-defining.** The strongest
genuinely-novel kernel: **"the policy was selected on the LEVEL of a common factor; we estimate a
SPEED that is invariant to that level by construction"** — generalizes to any evaluation where
treatment timing is triggered by an aggregate outcome but the question concerns cross-sectional
frictions. **What would make it publishable:** foreground that transferable methods kernel (explicitly
distinguished from Steinwender's positive shock and Goyal's adjacent markets); repair the heterogeneous-
loadings identity (CCE/IFE residualisation) so "f cancels" is actually true; fix the RI size via
calibration and the pre-test/aggregation/small-T biases; and pre-register the roster + cotton window.
The cross-commodity bridge (microstructure price discovery × trade/information frictions via a NEGATIVE
information-infrastructure shock) plus the three falsification axes give a methods-and-application
contribution. Outlets: same as the others (JDE / AJAE / J. Commodity Markets, with a methods angle).

---

### KILLED DESIGNS — post-mortem
No designs were killed in this round — all three audited novel designs returned **"fixable"** (none
"kill"). For completeness and to avoid silently losing the eliminated *baseline* approaches that the
audits ruled out as headlines:

- **Naive two-way-FE DiD on log realized vol (C1)** — KILLED by the project's own pre-registered rules:
  the Dec-2019 placebo reproduces the "effect" (−13.6%, p=.046) and the binned joint lead test rejects
  (p=.033). Cause = selection-on-a-transitory-mean-reverting-shock (Chabé-Ferret 2015). Retained only
  as the foil the SCM-family must beat.
- **Plain GARCH(1,1) + ban-dummy pre/post persistence comparison (C2)** — KILLED as a headline: doubly
  invalid here (Hillebrand-spurious persistence from one unmodelled level break + a ban date selected on
  the outcome). This is exactly the design the prior ban literature (NCDEX/BIMTECH, IIM-Udaipur, Sobti
  2020-style E-GARCH) ran; demonstrating its failure with our own placebo machinery is itself part of
  the publishable contribution. Retained only as the foil DCBD-GARCH improves on.
- **Announcement event-study around Dec-2021 (C1)** — RULED OUT (Casini-McCloskey conditions fail): the
  ban was endogenous and pre-figured by months of inflation, so there is no policy-surprise to exploit
  and no high-frequency window (we have monthly vol). Cited to explain why it is inappropriate, not run.

---

## Decision-needed summary (for the design discussion)
1. **C1 disaggregation** — run C1 at the district level (penalized SCM) to escape the few-cluster trap?
2. **C1 treatment date** — per-commodity (chana Aug / mustard Oct / rest Dec) vs single Dec-2021?
3. **C1 donor pool** — membership, contamination screening (cotton post-Aug-2022), and whether to seed
   with non-banned FOOD commodities (barley/sugar/maize/jowar/bajra/ragi/coriander) for overlap.
4. **Bundled-policy estimand (RF-SC)** — clean 2022-01..2022-04 window, sign-conservative CPO route, or
   explicitly estimate the joint policy package? Engage compound-treatment identification literature.
5. **Selection variable** — re-motivate on price-level / item-CPI inflation rather than spot RV (the
   spot-vol run-up premise is contradicted for the headline commodities).
6. **CPO routing** — out of the spot-vol headline (no mandi spot) into the basis/international track.
7. **C2 GARCH discipline** — ICSS-then-within-regime as the mandatory baseline; never report a plain
   ban-dummy persistence change.
8. **MSP censoring** — demote paddy (OUT) and flag wheat (censored) before estimation; Tobit-GARCH?
9. **Calendar vs trading days** — re-run all daily-return work on trading-day-only series.
10. **Which spot is "the spot"** — eNAM vs mandi-modal vs NCDEX-polled.
11. **Pre-registration** — one frozen primary spec per design; specification curve for the rest;
    Monte-Carlo-calibrate every randomization test's finite-sample size; lock rosters and exclusion
    windows from the policy ledger BEFORE estimation.
