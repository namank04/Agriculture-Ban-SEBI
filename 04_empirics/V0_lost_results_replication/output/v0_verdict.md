# V0 Verdict Memo — claim by claim: confirmed / revised / dead

**Module:** V0 — Replication & Verification of Lost Results [PRIORITY ONE]
**Date:** 2026-06-21 · **Status:** documents the *verified* state of the V0 runs.

> **⚠️ SUPERSEDED for current numbers by `../../H1_volatility/c1_findings.md` (canonical).** The
> figures in THIS memo (DiD −18.8%, placebo −12.8%/p=0.055, pre-trend stat 2.99/p=0.39) are the
> trading-day-fix INTERMEDIATE state with **paddy still included**. The final primary spec **drops
> paddy** (MSP-censored): DiD **−20.7%**, placebo **−11.7%** (analytic p=0.116, bootstrap p=0.189),
> pre-trend **p=0.186**. After internal referee review, the honest inference is **few-cluster
> p≈0.026–0.046** (the naive p=0.008 is over-optimistic) and the SDID pooled has **no valid SE**
> (the earlier z≈−7.7 was a jackknife artifact). See `c1_findings.md`. This memo is kept as the
> historical V0 trading-day-fix record.

> **⚠️ Re-run on trading-day-corrected data, 2026-06-21.** All spot series were rebuilt
> excluding weekend rows (the "calendar-grid" bug: mandi files behaved like 7-day grids but
> realized vol was annualized with √252 trading days). This **materially changed the results** —
> the falsification picture and the chana GARCH sub-result both moved a lot. Pre-fix numbers are
> shown in parentheses for comparison. The pre-fix outputs are preserved in git history.
> **Consequence (resolved):** `cv_story.tex` and `05_paper/interview_pack/` have since been
> **reconciled** to the canonical numbers (DiD −20.7%; honest few-cluster p≈0.026/0.046; placebo
> −11.7%); any −16.4% / chana 0.99→0.78 they still contain now appears *only* explicitly flagged as
> the pre-fix "before"/calendar-grid-artifact value, never as a current finding.

Pass/fail rules are those pre-registered in `../spec.md §B`. Methodological pivots recommended
below (SCM family primary; per-commodity dates; ICSS-within-regime GARCH) remain **DECISION
NEEDED** per rule 6, except the trading-day clean which the researcher authorized 2026-06-21.

---

## C1 — "DiD + event study → spot vol +8–10% post-ban"  →  **inherited +ve claim REFUTED; DiD effect is negative (~−20%), borderline-significant under honest few-cluster inference — SUGGESTIVE not conclusive**

**Lost claim:** spot realized volatility rises **+8 to +10%** post-ban (district panel).

**DiD** (30-day rolling-std annualized RV; `vol_it = α_i + λ_t + β·(banned×post) + ε`, commodity-clustered), trading-day-corrected. **Final primary spec (canonical) drops paddy** (MSP price-censored); the paddy-INCLUDED intermediate rows from the V0 run are retained in the rightmost column only as the historical progression — they are NOT the current numbers.

| Spec | β | effect e^β−1 | inference | (V0 paddy-included intermediate) |
|---|---|---|---|---|
| National | −0.1125 | −10.6% | p=0.214 (large-df, not headline) | — |
| **District (canonical, paddy DROPPED)** | — | **−20.7%** | few-cluster **p≈0.026** (CR1, t with G−1=9 df) / **0.046** (wild bootstrap); naive large-df p=0.008 is over-optimistic, NOT the headline | (paddy-in: −18.8%, naive p=0.0030) |
| District, ex-guar (id 75) | — | (within −18.3% to −25.5% leave-one-out band) | few-cluster p ≤ 0.044 across district-liquidity/outlier filters | (paddy-in: −18.8%, p=0.0137) |

The effect is **negative** — opposite in sign to the lost +8–10%. National and district agree in sign (both negative), where before national was null. The headline magnitude is **−20.7%** on the canonical paddy-dropped panel; it is **robust to leave-one-commodity-out (−18.3% to −25.5%)**, and **dropping the MSP-flagged wheat makes it stronger (−25.5%, p≈0.003)** → not wheat/MSP-driven.

**Synthetic DiD / SCM (canonical, for context):** Synthetic DiD pooled **−26.9% but with NO valid SE** (5 treated, 5 donors → placebo SE undefined; the earlier z≈−7.7 was a donor-jackknife artifact, **withdrawn**). Per-commodity SDID placebo z's run −1.5..−3.4 (wheat −1.5 insignificant). Abadie SCM: chana −40, mustard −40, wheat −49, soybean −25, **moong +3 (wrong sign)**; **4 of 5 fail the in-space placebo**, poor pre-fit. Estimator agreement is **mechanical** (same panel, 5 treated/5 donors, SDID weights ≈ uniform → collapses toward DiD), **not** four independent confirmations.

**Falsification battery** (`placebo_results.txt`), trading-day-corrected, **canonical paddy-dropped**:
- **Placebo fake-ban Dec-2019** (pre-ban data only): **−11.7% (analytic p=0.116, bootstrap p=0.189)** — MARGINAL, recovering **56% of the headline**. A design that finds half the effect where nothing happened is a warning sign, not a clean pass. *(V0 paddy-included intermediate was −12.8%, p=0.0547; pre-fix −13.6%, p=0.046.)*
- **Joint pre-trend lead test:** joint **p=0.186 — not rejected**, BUT this MASKS a significant most-recent pre-ban lead bin at **+10% (p=0.049)** — volatility was already diverging before the ban. *(V0 paddy-included intermediate joint stat 2.99, p=0.3928; pre-fix Wald 8.71, p=0.033, rejected — that rejection was largely the weekend artifact.)*

**Verdict logic vs spec §B:**
- The pre-registered death-trigger — *"pre-trends fail → DiD dead"* — **no longer fires on the joint test** (p=0.186), but the **significant +10% most-recent lead bin** is a live pre-trend warning the joint test masks.
- C1 is **not "confirmed"**: the placebo recovers 56% of the effect, inference is only borderline (honest few-cluster p≈0.026–0.046, not the over-optimistic 0.008), SCM fits poorly, and mean-reversion is unresolved.
- **Net:** the inherited +8–10% is **refuted** (effect is negative, ~−20%). The defensible claim is **descriptive/quasi-causal** — "the suspension did not raise, and is associated with lower, spot volatility" — explicitly hedged: **suggestive, not conclusive.**

**Recommended next inference [DECISION NEEDED]:** widen the donor pool with the pre-registered food
donors, then Honest-DiD (Rambachan–Roth) sensitivity, a Callaway–Sant'Anna estimate, and the
wild-bootstrap confidence interval. See `01_literature/methodology_menu_c1_c2.md §437` and the
canonical `../../H1_volatility/c1_findings.md`.

**Still-open data-integrity items behind the −20.7% headline:** food donors not yet in the panel
(industrial/spice donors are weak counterfactuals for food staples); no DiD-robust estimator
(Callaway–Sant'Anna / Sun–Abraham) for the staggered 47-month-post design; per-commodity treatment
dates confirmed (chana 2021-08-16, mustard 2021-10-08, rest 2021-12-20) but not yet wired into this DiD.

---

## C2 — "persistent basis widening + GARCH(1,1) elevated vol"  →  **basis UNTESTABLE as stated; GARCH 'elevated' NOT SUPPORTED (and the 'calmer' counter-result was mostly artifact)**

### Arm (i) — basis: **internally impossible as literally stated; reframe pending data** *(unchanged)*
Banned commodities have **no futures after Dec-2021**, so a post-ban basis cannot exist.
Re-classify (per spec §A) as a pre-ban basis trend, a control-commodity basis, or a
domestic-spot vs **international**-futures spread. **Blocked** on researcher vendor files
(chana/wheat Investing.com futures; FCPO). Routes to **H4 (insulation)**.

### Arm (ii) — GARCH vol-dynamics: trading-day-corrected

| series | chana persist (pre→post) | chana uncond vol (pre→post) | wheat persist (pre→post) |
|---|---|---|---|
| **National** (corrected) | **0.554 → 0.693** | **47.3% → 45.7%** | 0.681 → 0.414 (vol 20.5→15.7) |
| National (pre-fix) | (0.99 → 0.78) | (71.2% → 45.9%) | (0.467 → 0.462) |
| **District-median** (corrected) | 1.000 → 1.000 (degenerate) | NaN → NaN | 1.000 → 0.972 (vol absurd→14.6) |

**The dramatic pre-fix chana result (0.99→0.78, vol 71%→46%) was substantially a
calendar-grid artifact.** On clean data chana persistence is *flat-to-slightly-up* (0.55→0.69)
and unconditional vol is **essentially unchanged** (47%→46%). The "market became calmer after
the ban" sub-result **does not survive the data fix** and should be retired (or heavily
re-caveated). Wheat does show a decline (persist 0.68→0.41, vol 20.5→15.7), but wheat is
MSP-censored. The **district-median GARCH remains degenerate** for chana (persistence pinned at
1.0, NaN vol) even after the weekday filter — the "real test" series still won't fit a
stationary GARCH.

Plus the standing methodological invalidity: **Hillebrand neglected-break bias** biases a plain
pre/post persistence comparison toward 1 → **ICSS-then-within-regime is the mandatory C2
baseline [DECISION NEEDED].**

**Verdict:** the lost work's "GARCH **elevated** vol post-ban" is **not supported**. But neither
is the clean "calmer" story — on corrected data chana is roughly flat. Treat C2-GARCH as
**inconclusive pending ICSS-within-regime on a properly de-seasonalized, non-censored series.**

> **Interview-pack note (resolved):** `05_paper/interview_pack/` and `cv_story.tex` have been
> **rewritten** — they now present chana "0.99→0.78, vol 71%→46%" *only* as the early, calendar-dirty
> fit that **washes out** on trading-day-clean data (chana ≈ flat, persistence ≈0.55→0.69), with the
> explicit verdict that **C2-volatility is inconclusive and the volatility case rests on C1.** The
> numbers were real and correctly transcribed; they were just computed on the buggy calendar-grid series.

---

## C3 — "CPI/WPI + acreage → inflation transmission"  →  **DESIGN IDEA, not a result** *(unchanged)*
Never finished in the lost work; overview depth only. Operationalize later as the FDCD
spatial-convergence design + CPI/WPI pass-through. Nothing to confirm or kill.

---

## Bottom line (canonical, paddy-dropped, post-referee-review, 2026-06-21)
- **C1:** inherited +8–10% **refuted** (point estimate ≈ **−20.7%**, sign-flipped). It is **robust
  to leave-one-out (−18.3% to −25.5%), incl. dropping MSP wheat (−25.5%, stronger)**, but the
  evidence is **SUGGESTIVE not conclusive**: honest few-cluster inference is borderline (p≈0.026
  CR1 / 0.046 wild-boot; the naive 0.008 is over-optimistic), the placebo recovers 56% (−11.7%),
  the joint pre-trend masks a significant +10% most-recent lead bin, SCM fits poorly, estimator
  agreement is mechanical, and mean-reversion is unresolved. SDID pooled −26.9% has **no valid SE**.
  The defensible claim is **descriptive/quasi-causal**, explicitly hedged. (Canonical:
  `../../H1_volatility/c1_findings.md`.)
- **C2 (basis):** untestable as stated (no banned-commodity futures post-ban); reframe to a domestic–international spread (H4); blocked on vendor futures.
- **C2 (GARCH):** "elevated vol" not supported; ICSS finds no variance break near the ban; the
  pre-fix "calmer chana" (0.99→0.78, vol 71%→46%) was a calendar-grid artifact → on clean data
  ≈ flat (≈0.55→0.69) → **inconclusive**, pending ICSS-within-regime.
- **C3:** design idea only.

**The research-integrity story still holds — and is now sharper:** a pre-registered replication
that refuted the inherited claim, *and* caught a data-pipeline bug whose removal overturned both
its own "DiD is dead" verdict and its headline GARCH sub-result — followed by an adversarial
referee review that retracted the over-stated inference (z=−7.7, p=0.008) down to honest borderline
significance. Robustness to the measurement fix, and to honest inference, is itself the finding.

## Researcher decisions gating the next step (rule 6 — flagged, not taken)
1. Widen the donor pool with the pre-registered food donors (the current industrial/spice donors are weak counterfactuals for food staples) before any publishable C1 magnitude.
2. The remaining `methodology_menu §437` choices — MSP handling (paddy dropped per decision_log), donor pool, which-spot, pre-registration freeze.
3. Honest-DiD (Rambachan–Roth) sensitivity · Callaway–Sant'Anna estimate · wild-bootstrap CI · ICSS-within-regime GARCH.
4. Supply C2-basis vendor files (chana/wheat futures; FCPO); follow up NCDEX request (~2026-06-25).
