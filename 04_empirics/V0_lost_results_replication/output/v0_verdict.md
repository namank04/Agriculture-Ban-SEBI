## C1 — "DiD + event study → spot vol +8–10% post-ban"  →  **inherited +ve claim REFUTED; DiD effect is negative (~−20%), borderline-significant under honest few-cluster inference — SUGGESTIVE not conclusive**

**Lost claim:** spot realized volatility rises **+8 to +10%** post-ban (district panel).

**DiD** (30-day rolling-std annualized RV; `vol_it = α_i + λ_t + β·(banned×post) + ε`, commodity-clustered), trading-day-corrected. **Final primary spec (canonical) drops paddy** (MSP price-censored); the paddy-INCLUDED intermediate rows from the V0 run are retained in the rightmost column only as the historical progression — they are NOT the current numbers.

| Spec | β | effect e^β−1 | inference | (V0 paddy-included intermediate) |
|---|---|---|---|---|
| National | −0.1125 | −10.6% | p=0.214 (large-df, not headline) | — |
| **District (canonical, paddy DROPPED)** | — | **−20.7%** | few-cluster **p≈0.026** (t with G−1=9 df); naive large-df p=0.008 is over-optimistic, NOT the headline | (paddy-in: −18.8%, naive p=0.0030) |
| District, ex-guar (id 75) | — | (within −18.3% to −25.5% leave-one-out band) | few-cluster p ≤ 0.044 across district-liquidity/outlier filters | (paddy-in: −18.8%, p=0.0137) |

The effect is **negative** — opposite in sign to the lost +8–10%. National and district agree in sign (both negative), where before national was null. The headline magnitude is **−20.7%** on the canonical paddy-dropped panel; it is **robust to leave-one-commodity-out (−18.3% to −25.5%)**, and **dropping the MSP-flagged wheat makes it stronger (−25.5%, p≈0.003)** → not wheat/MSP-driven.

**Falsification battery** (`placebo_results.txt`), trading-day-corrected, **canonical paddy-dropped**:
- **Placebo fake-ban Dec-2019** (pre-ban data only): **−11.7% (p=0.116)** — MARGINAL, recovering **56% of the headline**. A design that finds half the effect where nothing happened is a warning sign, not a clean pass. *(V0 paddy-included intermediate was −12.8%, p=0.0547; pre-fix −13.6%, p=0.046.)*
- **Joint pre-trend lead test:** joint **p=0.186 — not rejected**, BUT this MASKS a significant most-recent pre-ban lead bin at **+10% (p=0.049)** — volatility was already diverging before the ban. *(V0 paddy-included intermediate joint stat 2.99, p=0.3928; pre-fix Wald 8.71, p=0.033, rejected — that rejection was largely the weekend artifact.)*

**Verdict logic vs spec §B:**
- The documented failure trigger — *"pre-trends fail → DiD dead"* — **no longer fires on the joint test** (p=0.186), but the **significant +10% most-recent lead bin** is a live pre-trend warning the joint test masks.
- C1 is **not "confirmed"**: the placebo recovers 56% of the effect, inference is only borderline (t(G−1)-reference p≈0.026, not the over-optimistic 0.008), SCM fits poorly, and mean-reversion is unresolved.
- **Net:** the inherited +8–10% is **refuted** (effect is negative, ~−20%). The defensible claim is **descriptive/quasi-causal** — "the suspension did not raise, and is associated with lower, spot volatility" — explicitly hedged: **suggestive, not conclusive.**

**Recommended next inference [DECISION NEEDED]:** widen the donor pool with the documented food
donors, then Honest-DiD (Rambachan–Roth) sensitivity, a Callaway–Sant'Anna estimate, and the
additional small-cluster sensitivity analysis. See `01_literature/methodology_menu_c1_c2.md §437` and the
canonical `../../H1_volatility/c1_findings.md`.

**Still-open data-integrity items behind the −20.7% headline:** food donors not yet in the panel
(industrial/spice donors are weak counterfactuals for food staples); no DiD-robust estimator
(Callaway–Sant'Anna / Sun–Abraham) for the staggered 47-month-post design; per-commodity treatment
dates confirmed (chana 2021-08-16, mustard 2021-10-08, rest 2021-12-20) but not yet wired into this DiD.

---

### Arm (i) — basis: **internally impossible as literally stated; reframe pending data** *(unchanged)*
Banned commodities have **no futures after Dec-2021**, so a post-ban basis cannot exist.
Re-classify (per spec §A) as a pre-ban basis trend, a control-commodity basis, or a
domestic-spot vs **international**-futures spread. **Blocked** on researcher vendor files
(chana/wheat Investing.com futures; FCPO). Routes to **H4 (insulation)**.
