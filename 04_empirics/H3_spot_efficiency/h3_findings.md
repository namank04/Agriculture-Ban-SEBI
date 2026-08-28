# H3 — Spot-Market Efficiency and Spatial Integration After the Derivatives Suspension

## 1. Research question

This analysis studies whether the suspension of agricultural commodity derivatives was
followed by changes in the functioning of the corresponding spot markets.

Two aspects of spot-market functioning are examined:

1. **informational efficiency** — whether spot-price returns became more predictable; and
2. **spatial integration** — whether prices across mandis became less closely linked.

This analysis concerns the functioning of **spot markets**. It should not be interpreted as
a direct futures-versus-spot price-discovery test.

---

## 2. Commodity sample

The primary treated commodities are:

- chana
- mustard
- soybean
- moong

Wheat is retained only as a secondary, policy-confounded series because its post-suspension
period overlaps with substantial MSP, procurement and trade-policy interventions.

Paddy is excluded because its mandi-price series is strongly affected by price censoring and
a large proportion of exactly flat returns.

The comparison commodities are:

- castor
- guarseed413
- jeera
- turmeric
- cotton

These commodities retained derivatives trading and are used to describe the corresponding
changes in untreated spot markets.

---

## 3. Treatment timing

The primary H3 specification uses the actual suspension date of each treated commodity:

| Commodity | Suspension date |
|---|---|
| Chana | 16 August 2021 |
| Mustard | 8 October 2021 |
| Soybean | 20 December 2021 |
| Moong | 20 December 2021 |

For each treated commodity, the control commodities are split into pre- and post-periods
using **the same date as that treated commodity**.

For example, chana is compared with changes in the control commodities around
16 August 2021, while mustard is compared with the same controls around 8 October 2021.

This avoids classifying already-treated observations for chana and mustard as part of their
pre-treatment periods.

An earlier specification used 20 December 2021 as a common cutoff for all commodities.
Those results are retained as a timing-robustness check.

---

# Part A — Informational Efficiency

## 4. Variance-ratio methodology

Informational efficiency is examined using Lo-MacKinlay variance-ratio statistics on daily
national spot-price returns.

Under a random-walk benchmark:

\[
VR(q)=1.
\]

A larger absolute departure from one,

\[
|VR(q)-1|,
\]

indicates stronger serial dependence in returns and therefore greater predictability.

The analysis uses horizons:

\[
q \in \{2,5,10\}.
\]

For each commodity, the change in the inefficiency measure is:

\[
\Delta |VR-1|
=
|VR_{post}-1|-|VR_{pre}-1|.
\]

A positive value means that the spot-return process moved further away from the random-walk
benchmark after the relevant suspension date.

Daily returns are winsorized separately within the pre- and post-periods at the 1% tails to
reduce the influence of isolated extreme price-reporting or composition changes in the
national mandi series.

---

## 5. Aggregate variance-ratio results

Using commodity-specific suspension dates:

| Horizon | Treated mean change | Control mean change | Treated − control |
|---|---:|---:|---:|
| q = 2 | +0.032 | +0.021 | +0.012 |
| q = 5 | +0.086 | +0.015 | +0.071 |
| q = 10 | **+0.128** | **+0.014** | **+0.115** |

The difference becomes larger at longer horizons.

At \(q=10\), the treated commodities move approximately **0.115 further away from the
random-walk benchmark relative to the controls**.

This is consistent with weaker spot-return efficiency after the suspension, although the
number of treated commodities is too small for this contrast to provide strong standalone
statistical evidence.

---

## 6. Commodity-level variance-ratio results

At \(q=10\):

| Commodity | Treated change | Matched control change | Difference |
|---|---:|---:|---:|
| Chana | +0.103 | +0.004 | **+0.099** |
| Mustard | +0.115 | +0.008 | **+0.106** |
| Soybean | +0.325 | +0.021 | **+0.304** |
| Moong | −0.029 | +0.021 | **−0.050** |

Three of the four primary treated commodities move further away from the random-walk
benchmark relative to their matched control changes.

Soybean shows the largest deterioration in this measure.

Moong is the exception: its variance ratio moves slightly closer to the random-walk
benchmark.

The result should therefore be interpreted as an aggregate directional pattern rather than a
uniform commodity-level response.

---

## 7. Variance-ratio test validation

The implementation reports both the homoskedastic and heteroskedasticity-robust
Lo-MacKinlay test statistics.

During code validation, an earlier implementation of the heteroskedasticity-robust variance
contained an incorrect sample-size factor. This affected the reported test statistic but not
the underlying variance-ratio point estimates.

The formula was corrected before the final results were interpreted.

With the corrected implementation, the random-walk null is rejected for most
commodity-window combinations.

This means that the important H3 quantity is not whether spot prices form a perfect random
walk in either period. Rather, it is whether their **distance from the random-walk benchmark
changes differently for suspended and comparison commodities**.

---

# Part B — Spatial Integration

## 8. Mandi selection

Spatial integration is studied using mandi-level spot prices.

For each commodity, the analysis selects the **eight mandis with the strongest reporting
coverage**, subject to the requirement that a selected mandi reports on at least 40% of
business days in both the pre- and post-periods.

The mandis are therefore selected by **data coverage**, not by trading volume.

Volume or arrivals data are not available consistently enough to rank mandis by economic
turnover.

---

## 9. Price-series construction

For each selected mandi:

- modal prices are restricted to positive observations;
- multiple observations for the same market and day are collapsed using the median;
- the series is placed on a business-day grid;
- short missing stretches of up to five business days are forward-filled;
- prices are transformed to logarithms.

The pre- and post-periods are defined using the relevant treated commodity's suspension
date.

---

## 10. Cointegration measure

For eight selected mandis there are:

\[
\binom{8}{2}=28
\]

possible mandi pairs.

Each pair is tested separately using an Engle-Granger cointegration test on log price
levels.

For each commodity and period, the analysis reports:

1. the **share of mandi pairs classified as cointegrated at the 5% level**; and
2. the **median half-life of deviations from the estimated long-run price relationship**
   among cointegrated pairs.

A decrease in the share of cointegrated mandi pairs indicates weaker spatial integration.

A longer adjustment half-life means that deviations between linked mandi prices take longer
to correct.

The cointegration share is used as a descriptive integration index. Because 28 pairwise
tests are performed for each commodity-window and no multiple-testing adjustment is imposed,
the individual 5% classifications should not be interpreted as 28 independent formal
hypothesis tests.

---

## 11. Aggregate spatial-integration results

Using commodity-specific treatment dates:

### Cointegration share

Mean post-minus-pre change:

- treated commodities: **−0.143**
- matched controls: **+0.045**
- treated-minus-control difference: **−0.188**

Thus, the share of integrated mandi pairs falls for the treated group while it increases
slightly for the comparison commodities.

### Adjustment half-life

Mean post-minus-pre change:

- treated commodities: **+1.67 days**
- matched controls: **−0.15 days**
- treated-minus-control difference: **+1.82 days**

The average adjustment of spatial price deviations therefore becomes slower for the treated
commodities relative to the controls.

Both measures point toward weaker post-suspension spatial integration at the aggregate level.

---

## 12. Commodity-level spatial-integration results

| Commodity | Δ cointegration share | Matched-control Δ | Difference | Δ half-life | Matched-control Δ | Difference |
|---|---:|---:|---:|---:|---:|---:|
| Chana | −0.107 | +0.014 | **−0.121** | −0.00 | −0.08 | +0.07 |
| Mustard | +0.036 | +0.050 | **−0.014** | +6.41 | −0.32 | **+6.72** |
| Soybean | −0.143 | +0.057 | **−0.200** | −0.31 | −0.11 | −0.20 |
| Moong | −0.357 | +0.057 | **−0.414** | +0.57 | −0.11 | **+0.68** |

The commodity-level evidence is heterogeneous.

### Chana

Chana experiences a moderate decline in the share of cointegrated mandi pairs relative to
controls, while its adjustment half-life is approximately unchanged.

### Mustard

Mustard's cointegration share changes little relative to controls, but the estimated
adjustment half-life increases sharply.

This indicates slower correction of spatial price deviations even though the number of
cointegrated pairs does not materially decline.

### Soybean

Soybean experiences a clear decline in the share of cointegrated mandi pairs relative to
controls.

Its estimated half-life, however, improves slightly. The two integration measures therefore
do not move in the same direction for soybean.

### Moong

Moong produces the largest decline in the share of cointegrated mandi pairs and also shows
slower adjustment relative to controls.

It provides the strongest commodity-level evidence of weaker spatial integration.

---

## 13. Treatment-timing robustness

The original H3 implementation used 20 December 2021 as a common pre/post cutoff for all
commodities.

Correcting the timing for the earlier chana and mustard suspensions does not materially
change the overall result.

| Measure | Common 20-Dec specification | Commodity-specific specification |
|---|---:|---:|
| q=10 variance-ratio contrast | +0.108 | **+0.115** |
| Cointegration-share contrast | −0.218 | **−0.188** |
| Half-life contrast | +1.51 days | **+1.82 days** |

All three measures retain the same direction.

The common-date specification is therefore retained as a robustness comparison, while the
commodity-specific timing is preferred for the main interpretation.

In the earlier common-date cross-commodity comparison, the variance-ratio contrast had a
Mann-Whitney p-value of approximately 0.21 and the cointegration-share contrast had a
one-sided p-value of approximately 0.069.

These values illustrate the limited statistical power of the small commodity sample and are
not treated as primary inference for the staggered specification.

---

## 14. Interpretation

The two parts of H3 provide directionally consistent aggregate evidence.

First, suspended commodities move further away from the random-walk benchmark than the
controls, particularly at longer variance-ratio horizons.

Second, their mandi networks show a lower share of cointegrated price pairs and slower
average correction of spatial price deviations relative to matched control changes.

However, the response is not uniform across commodities or indicators.

The results therefore support a **suggestive deterioration in spot-market efficiency and
spatial integration**, rather than establishing a precise common treatment effect for every
commodity.

---

## 15. Limitations

### Small number of treated commodities

The primary comparison contains only four relatively clean treated commodities and five
controls.

The large number of daily observations does not create a large number of independent policy
treatments.

### Concurrent shocks and policies

The post-suspension period includes other important agricultural and macroeconomic
developments.

These include MSP and procurement changes, trade interventions and the global commodity
shock associated with the Russia-Ukraine war.

The control commodities help provide a benchmark but cannot remove all commodity-specific
confounding.

### National-series aggregation

The variance-ratio analysis uses national daily mandi price series.

Changes in the composition of reporting markets can add noise to these aggregate series.

The mandi-level integration analysis therefore provides a useful complementary measure.

### Mandi selection

The eight mandis are selected by reporting coverage rather than trading volume because
consistent arrivals or turnover data are unavailable.

### Pairwise cointegration testing

The integration measure is based on the share of 28 mandi pairs passing an Engle-Granger
test at the 5% level.

No multiple-testing correction is applied, so the share is interpreted as a descriptive
measure of spatial integration rather than as a collection of independent significance
claims.

### Missing market-activity data

Consistent mandi arrivals and transaction-volume data are unavailable, preventing direct
measurement of whether economically larger mandis experienced different effects.

---

## 16. Conclusion

H3 provides **suggestive evidence that spot-market functioning weakened after the
agricultural derivatives suspensions**.

Using commodity-specific treatment dates, the \(q=10\) variance-ratio inefficiency measure
increases by approximately **0.115 more for treated commodities than for matched controls**.

The share of cointegrated mandi pairs falls by approximately **0.188 more for treated
commodities**, while the adjustment half-life of spatial price deviations increases by
approximately **1.82 days relative to controls**.

The earlier common-date specification produces similar results, indicating that the
direction of the findings is not driven by treatment-date misclassification for chana and
mustard.

At the same time, the sample contains only four primary treated commodities and the
commodity-level results are heterogeneous.

The evidence should therefore be presented as **supporting evidence of weaker spot-market
efficiency and spatial integration**, not as definitive causal proof and not as a direct
measure of futures-versus-spot price discovery.

---

## 17. Output files

Primary staggered-timing results are stored in:

`04_empirics/H3_spot_efficiency/output_staggered/`

including:

- `A_staggered_summary.csv`
- `A_staggered_by_treated.csv`
- `A_staggered_controls.csv`
- `B_staggered_summary.csv`
- `B_staggered_by_treated.csv`
- `B_staggered_controls.csv`

The original common-date robustness results are retained in:

`04_empirics/H3_spot_efficiency/output/`

The principal analysis scripts are:

- `00_code/run_h3_efficiency.py`
- `00_code/run_h3_efficiency_staggered.py`
