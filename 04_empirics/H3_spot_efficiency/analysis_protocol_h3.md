# H3 Analysis Protocol and Final Implementation

## 1. Purpose

This document records the design used to examine whether the 2021 agricultural-derivatives
suspensions were followed by changes in the functioning of the corresponding spot markets.

The analysis has two components:

1. informational efficiency of spot-price returns; and
2. spatial integration across mandis.

The associated results are reported in:

`04_empirics/H3_spot_efficiency/h3_findings.md`

H3 is a supporting analysis to the main volatility results. It does not directly estimate
futures-versus-spot price discovery.

---

## 2. Research question

The main question is:

**After derivatives trading was suspended, did the affected commodities show weaker spot-market
efficiency or weaker integration across mandis relative to commodities whose derivatives
continued trading?**

Two empirical indicators are used.

### Part A — informational efficiency

Daily spot returns are examined using Lo-MacKinlay variance ratios.

The central question is whether treated commodities move further away from a random-walk
benchmark after suspension relative to the control commodities.

### Part B — spatial integration

Mandi-level spot prices are used to examine whether prices across geographically separate
markets remain linked through long-run price relationships.

The central question is whether treated commodities experience:

- a lower share of cointegrated mandi pairs; or
- slower correction of deviations between mandi prices.

---

## 3. Commodity sample

The primary treated commodities are:

- chana
- mustard
- soybean
- moong

Wheat is not included in the primary treated-group averages because its post-suspension
period is strongly affected by other agricultural and trade-policy interventions.

It is retained only as a secondary flagged series in the original common-date analysis.

Paddy is excluded because its mandi-price series contains substantial price censoring and a
large fraction of exactly flat price changes.

The comparison commodities are:

- castor
- guarseed413
- jeera
- turmeric
- cotton

These commodities continued to have derivatives trading and provide the comparison group for
changes in spot-market behaviour.

---

## 4. Treatment dates

The final preferred H3 design uses commodity-specific suspension dates:

| Commodity | Suspension date |
|---|---|
| Chana | 16 August 2021 |
| Mustard | 8 October 2021 |
| Soybean | 20 December 2021 |
| Moong | 20 December 2021 |

For each treated commodity, all comparison commodities are divided into pre- and post-periods
using that treated commodity's date.

For example, when chana is evaluated, both chana and all controls are split on
16 August 2021.

This preserves a common comparison window within each treated-control comparison without
assigning the controls an independent treatment event.

---

## 5. Earlier common-date specification

The first implemented H3 specification used:

**20 December 2021**

as a common cutoff for all commodities.

That approach was convenient for a pooled pre/post comparison but classified some
already-suspended observations for chana and mustard as pre-treatment observations.

The commodity-specific timing specification was therefore added as the preferred design.

The original common-date results are retained as a robustness check because they provide a
useful test of whether the findings depend materially on treatment timing.

---

# Part A — Informational Efficiency

## 6. Data

Part A uses cleaned national daily mandi spot-price series.

For each commodity:

- observations must have positive prices;
- prices are ordered by date;
- daily log returns are constructed;
- returns are divided into pre- and post-suspension windows.

The national series is an aggregate spot-price series and can be affected by changes in the
composition of reporting mandis.

Part A is therefore interpreted jointly with the mandi-level analysis in Part B.

---

## 7. Variance-ratio measure

For daily log returns \(r_t\), the Lo-MacKinlay variance ratio at horizon \(q\) compares the
variance of multi-period returns with the variance implied by a random walk.

Under a random walk:

\[
VR(q)=1.
\]

The horizons used are:

\[
q \in \{2,5,10\}.
\]

The main H3 efficiency measure is:

\[
I(q)=|VR(q)-1|.
\]

A larger value means a greater departure from the random-walk benchmark.

For each commodity:

\[
\Delta I(q)
=
I_{post}(q)-I_{pre}(q).
\]

The treated-control contrast compares this change with the corresponding change in the
control commodities over the same dates.

---

## 8. Return winsorization

National daily mandi series contain occasional extreme one-day movements that may reflect
reporting or composition changes rather than persistent market dynamics.

Returns are therefore winsorized separately within each pre- and post-period at the 1% tails.

The same rule is applied symmetrically to treated and comparison commodities.

---

## 9. Lo-MacKinlay inference

The implementation reports both:

- the homoskedastic Lo-MacKinlay statistic; and
- the heteroskedasticity-robust statistic.

During code validation, an incorrect sample-size factor was identified in an earlier version
of the heteroskedasticity-robust variance formula.

That error affected the test statistic but not the underlying variance-ratio point estimate.

The formula was corrected before the final H3 interpretation.

The main comparison therefore focuses on the pre-to-post change in the distance from the
random-walk benchmark rather than simply asking whether each individual series is a perfect
random walk.

---

# Part B — Spatial Integration

## 10. Mandi-level data

Part B uses mandi-level modal spot prices from the district/state Agmarknet files.

For each commodity:

- only positive modal prices are retained;
- observations are restricted to Monday-to-Friday dates;
- duplicate market-day observations are collapsed using the median.

The analysis is performed separately for the pre- and post-treatment windows.

---

## 11. Mandi selection

The original research plan proposed using approximately 6–10 major mandis per commodity.

Consistent mandi turnover or arrivals data were not available for a reliable volume-based
ranking.

The final implementation therefore uses the **eight mandis with the best reporting coverage**,
subject to the requirement that each selected mandi reports on at least 40% of business days
in both the pre- and post-periods.

This selection rule is based on data continuity rather than economic market size.

---

## 12. Price-series alignment

For each selected mandi:

1. market-day prices are placed on a business-day grid;
2. gaps of no more than five business days are forward-filled;
3. longer missing periods are left missing;
4. price levels are transformed to logarithms.

Short-gap filling is used to align the mandi series without creating long artificial price
histories.

---

## 13. Pairwise cointegration

With eight selected mandis there are:

\[
\binom{8}{2}=28
\]

possible mandi pairs.

Each pair is tested using an Engle-Granger cointegration test on log price levels.

The test is performed separately in the pre- and post-periods.

For each commodity, the main integration statistic is:

\[
S =
\frac{\text{number of pairs with }p<0.05}
{\text{number of valid mandi pairs}}.
\]

The change is:

\[
\Delta S=S_{post}-S_{pre}.
\]

A negative value is consistent with weaker spatial integration.

---

## 14. Multiple-testing interpretation

The 28 pairwise Engle-Granger tests are evaluated at the 5% level without a
multiple-testing correction.

Therefore, the share \(S\) is interpreted as a **descriptive integration index**.

It should not be interpreted as 28 independent confirmatory hypothesis tests.

The treated-control comparison in the change in this index is more important than any
individual mandi-pair classification.

---

## 15. Error-correction half-life

For mandi pairs classified as cointegrated, the cointegrating residual is estimated.

An AR(1)-type error-correction equation is used to estimate the persistence of the deviation
from the long-run price relationship.

The implied half-life measures approximately how long a price deviation takes to decay by
half.

A longer post-treatment half-life indicates slower spatial price adjustment.

The analysis compares:

\[
\Delta HL=HL_{post}-HL_{pre}
\]

for treated commodities with the corresponding changes in controls.

---

## 16. Preferred staggered comparison

For each treated commodity:

1. use its actual suspension date;
2. calculate the treated commodity's pre-to-post change;
3. calculate the same pre-to-post change for each of the five controls using the same date;
4. average the control changes;
5. calculate the treated-minus-control contrast.

The final H3 summary averages these contrasts across the four primary treated commodities.

This design avoids using already-treated chana or mustard observations as part of their
pre-treatment period.

---

## 17. Common-date robustness

The original analysis using 20 December 2021 for all commodities is retained separately.

The common-date and commodity-specific specifications produce the same qualitative direction
for all three principal aggregate indicators:

- variance-ratio inefficiency;
- cointegration share;
- error-correction half-life.

The commodity-specific specification is therefore used for the main interpretation.

---

## 18. Statistical power

The primary treated group contains only four commodities.

The large number of daily observations and mandi pairs does not create a large number of
independent policy treatments.

Cross-commodity inference therefore has limited power.

The H3 results are interpreted as supporting and suggestive evidence rather than as a
high-powered causal estimate.

---

## 19. Concurrent influences

The post-suspension period includes several other developments that may affect spot-price
behaviour, including:

- MSP and procurement changes;
- trade restrictions;
- commodity-specific policy interventions;
- the global commodity shock associated with the Russia-Ukraine war.

The comparison commodities provide a benchmark for common changes, but they cannot remove
all commodity-specific confounding.

No claim is made that developments such as e-NAM mechanically make the H3 estimate a
"lower bound."

---

## 20. Changes from the initial plan

The final implementation differs from the early H3 planning note in several ways.

### 20.1 Actual treatment dates

The initial implementation used a common 20 December 2021 cutoff.

Commodity-specific suspension dates are now the preferred specification.

### 20.2 Mandi ranking

The early plan referred to major or volume-ranked mandis.

Because consistent arrivals or turnover measures were unavailable, the final selection is
based on reporting coverage.

### 20.3 Interpretation of e-NAM

The early planning note suggested that post-2021 e-NAM expansion could make any observed
integration decline conservative.

That interpretation is not directly tested within H3 and is therefore not used as a formal
result.

### 20.4 Cointegration significance

The final interpretation explicitly treats the share of pairwise Engle-Granger rejections as
a descriptive integration index because no multiple-testing adjustment is imposed.

### 20.5 Treatment-effect interpretation

H3 is not presented as a direct measure of futures-versus-spot price discovery and is not
treated as a definitive causal estimate.

---

## 21. Interpretation rule

The final H3 interpretation considers together:

- the change in variance-ratio inefficiency;
- the share of cointegrated mandi pairs;
- the adjustment half-life;
- commodity-level heterogeneity;
- treatment-timing robustness;
- the small number of independent treated commodities;
- concurrent policy and market shocks.

Evidence is described as stronger when multiple indicators move consistently.

Disagreement across indicators or commodities is reported explicitly rather than averaged
away in the discussion.

---

## 22. Implementation files

The original common-date analysis is implemented in:

`00_code/run_h3_efficiency.py`

The preferred commodity-specific timing analysis is implemented in:

`00_code/run_h3_efficiency_staggered.py`

Primary staggered-timing outputs are stored in:

`04_empirics/H3_spot_efficiency/output_staggered/`

The original common-date outputs are retained in:

`04_empirics/H3_spot_efficiency/output/`

The final empirical interpretation is documented in:

`04_empirics/H3_spot_efficiency/h3_findings.md`
