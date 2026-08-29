# H1 — Effect of the 2021 Derivatives Suspension on Spot-Price Volatility

## 1. Research question

This analysis examines whether India's 2021 suspension of agricultural commodity derivatives
changed spot-price volatility in the affected commodities relative to comparable commodities
that were not suspended.

The initial hypothesis was that the suspension may have increased spot-market volatility by
removing or weakening the stabilizing role of futures markets. The empirical analysis does
not support an aggregate increase in volatility after the suspension.

---

## 2. Data and sample

The analysis uses district-level mandi spot-price data. Daily price series are used to
construct rolling 30-observation realized volatility, which is then aggregated to a monthly panel.

The main outcome is:

`ln(rv30)` = log of 30-day realized volatility.

The final treated commodities used in the primary volatility analysis are:

- chana
- mustard
- wheat
- soybean
- moong

Paddy is excluded from the primary analysis because a large proportion of its observed price
changes are zero, making the volatility series strongly affected by MSP-related price
censoring.

CPO is not included in the spot-volatility analysis because a comparable mandi spot-price
series is not available.

The final comparison group consists of nine commodities:

- castor
- guarseed413
- cotton
- jeera
- turmeric
- barley
- maize
- jowar
- bajra (partial coverage)

This nine-commodity comparison set is frozen for the final reported H1 results; adding new
commodities to the underlying data does not automatically change the estimation donor pool.

The estimation panel contains district-level observations, but treatment is assigned at the
commodity level. Inference therefore accounts for the relatively small number of commodity
clusters rather than treating districts as independent treatment units.

---

## 3. Empirical strategy

The analysis combines several estimators and validation checks.

### 3.1 Difference-in-Differences

The primary aggregate estimate is obtained using a two-way fixed-effects
Difference-in-Differences model on the district-level panel.

The aggregate specification uses a **common-exposure design**. All observations through
July 2021 are treated as pre-suspension, August--December 2021 is excluded as the staggered
transition period, and the common post-period begins in January 2022. This ensures that the
pooled treated group is genuinely untreated in the pre-period and fully treated in the
post-period.

Inference is clustered at the commodity level.

### 3.2 Synthetic Control

Synthetic Control is estimated separately for each treated commodity.

The commodity-level specifications use the relevant suspension dates: **16 August 2021 for
chana, 8 October 2021 for mustard, and 20 December 2021 for wheat, soybean and moong**.

The method constructs a weighted combination of comparison commodities whose pre-suspension
volatility path resembles that of the treated commodity. Post-suspension differences between
the treated commodity and its synthetic counterpart provide an additional estimate of the
policy-associated change.

In-space placebo tests are used to evaluate how unusual the treated-unit gap is relative to
gaps obtained when donor commodities are artificially treated.

### 3.3 Validation and robustness

The main estimates are evaluated using:

- alternative data-quality and liquidity filters;
- leave-one-commodity-out specifications;
- placebo treatment dates;
- pre-treatment trend tests;
- alternative counterfactual estimators.

These checks are important because the number of independent treatment clusters is small and
the choice of comparison commodities materially affects the estimated treatment effect.

---

## 4. Main Difference-in-Differences result

The final common-exposure Difference-in-Differences estimate is:

**−10.0%**

The underlying coefficient is approximately **−0.1059**.

The final estimation sample contains:

- **139,816 observations**
- **2,243 commodity-district units**
- **14 commodity clusters**

Inference is clustered at the commodity level.

- clustered p-value: **0.1235**
- t(G−1)-reference p-value: **0.1475**

The point estimate therefore goes in the opposite direction from the hypothesis that
suspension increased spot-price volatility, but it is not conventionally statistically
significant.

More importantly, the corrected pre-treatment diagnostics reject the parallel-trends
restriction. The DiD coefficient is therefore treated as a **benchmark rather than a clean
causal estimate**.

The appropriate aggregate conclusion is that the analysis finds **no evidence of an increase
in spot-price volatility following the suspension**.

---

## 5. Sensitivity to the comparison group

The choice of comparison commodities has an important effect on the estimated magnitude.
This donor-pool progression is retained as a substantive robustness result because it shows
how strongly the estimated treatment effect depends on the quality of the counterfactual.

An earlier specification using a narrower comparison group consisting mainly of
industrial and spice commodities produced an estimated effect of approximately:

**−20.7%**

That estimate was statistically stronger.

After economically closer food-cereal commodities were added to the comparison group, the
estimated aggregate effect declined in magnitude to approximately:

**−10.0%**

and was no longer statistically significant.

This difference shows that the result is sensitive to the construction of the
counterfactual. The broader nine-commodity comparison group is therefore used for the final
interpretation.

The five-donor −20.7% estimate is retained as a donor-sensitivity result, but
it is not treated as the preferred estimate.

---

## 6. Synthetic Control results

Commodity-level Synthetic Control produces the following estimated post-suspension effects:

| Commodity | Estimated effect | In-space placebo p-value |
|---|---:|---:|
| Chana | **−37.3%** | **0.10** |
| Mustard | −28.2% | 0.60 |
| Wheat | −37.8% | 0.60 |
| Soybean | −27.6% | 0.30 |
| Moong | −8.7% | 0.40 |

Chana again produces the strongest result.

With nine donor commodities, the smallest possible in-space placebo p-value is 0.10.
Synthetic Control therefore provides useful evidence on the direction and magnitude of the
effect, but its placebo inference cannot establish conventional 5% statistical significance
for an individual treated commodity.

---

## 7. Robustness of the aggregate estimate

The aggregate sign remains negative across the main sample-quality restrictions.

| Specification | Effect | t(G−1) p-value |
|---|---:|---:|
| Baseline | **−10.0%** | 0.1475 |
| Winsorize rv30 at p99 | −10.0% | 0.1463 |
| Drop rv30 > 5 | −10.2% | 0.1334 |
| Minimum 24 months | −9.8% | 0.1591 |
| Minimum 36 months | −9.0% | 0.2051 |
| Robust combined filter | −10.0% | 0.1458 |

Leave-one-treated-commodity-out estimates are:

| Specification | Effect | t(G−1) p-value |
|---|---:|---:|
| Excluding chana | −7.3% | 0.3100 |
| Excluding mustard | −9.6% | 0.2294 |
| Excluding wheat | **−15.6%** | **0.0037** |
| Excluding soybean | −9.7% | 0.1947 |
| Excluding moong | −8.5% | 0.2437 |

The sign is stable, but inference varies materially across specifications.

Wheat is not used as the headline commodity-level result because its post-suspension period
overlaps with substantial MSP, procurement, export and other policy interventions.

---

## 8. Placebo and pre-treatment validation

The final falsification exercises are important limitations on causal interpretation.

### Pre-treatment trends

The corrected pre-trend exercise uses only genuinely pre-treatment observations before the
earliest suspension.

The three lead-bin estimates are:

- months −18 to −13: beta = −0.2263, p = 0.0616
- months −12 to −7: beta = −0.1446, p = 0.1655
- months −6 to −2: beta = +0.0412, p = 0.6053

The joint small-cluster reference test gives:

**F(3,13) = 7.95, p = 0.0029**

Parallel pre-trends are therefore **rejected**.

### Pre-treatment placebo

The placebo specification excludes a fake August--December 2019 transition period, begins
the fake post-period in January 2020, and excludes observations exposed to the actual policy.

The placebo estimate is approximately:

**−9.6%**

with:

- conventional p-value: **0.1569**
- t(G−1)-reference p-value: **0.1804**

Although statistically insignificant, the placebo magnitude is economically close to the
actual −10.0% benchmark. It is therefore not reassuring.

Taken together, the failed pre-trend restriction and economically large placebo mean that the
aggregate DiD coefficient should **not** be interpreted causally.

---

## 9. Trading-day correction

During validation, an earlier version of the volatility panel produced a substantial effect
around a false treatment date and problematic pre-treatment behaviour.

Investigation showed that the mandi data behaved like a seven-day calendar grid, with some
markets reporting on weekends, while realized volatility was annualized using a 252-trading-day
convention. This created an inconsistent time-frequency construction.

The panel was therefore rebuilt using **Monday-to-Friday observations** before the final
estimates were calculated. A separate exchange-holiday calendar is not imposed, so this
correction should be understood as a weekday filter rather than a complete market-calendar
adjustment.

The correction materially changed the estimates and removed an inconsistent time-frequency
construction. However, the final corrected specification still fails the joint pre-trend
diagnostic. The calendar correction therefore improves measurement but does not rescue a
causal DiD interpretation.

---

## 10. Commodity-level interpretation

### 10.1 Chana

Chana provides the clearest evidence of lower spot-price volatility after the suspension.

- Synthetic Control: **−37.3%**

This is the strongest commodity-level result in the volatility analysis. With nine
donors, however, the in-space placebo p-value is bounded below by 0.10.

The limited number of donor commodities nevertheless restricts the precision of
Synthetic-Control placebo inference.

### 10.2 Mustard

Mustard's Synthetic Control estimate is negative:

- Synthetic Control: **−28.2%**

The direction is consistent with lower volatility, but statistical evidence is weak.

### 10.3 Soybean

Soybean also produces negative estimates:

- Synthetic Control: **−27.6%**

The estimate is negative, although placebo inference remains weak.

### 10.4 Wheat

Wheat is the most difficult treated commodity to interpret.

- Synthetic Control: **−37.8%**

Its in-space placebo p-value is **0.60**, so the estimate is not unusually large relative to
placebo gaps. More importantly, contemporaneous MSP, procurement, export and other policy
interventions make wheat a less reliable commodity for isolating the effect of the derivatives
suspension.

### 10.5 Moong

Moong produces relatively small negative effects:

- Synthetic Control: **−8.7%**

The statistical evidence is weak.

---

## 11. District-level Synthetic Control

Synthetic Control was also estimated at the district level to examine heterogeneity within
treated commodities.

Average district-level effects are negative for all five treated commodities.

These results are useful for describing heterogeneity across local spot markets, but they do
not solve the small-cluster inference problem.

The policy treatment occurs at the commodity level. A larger number of district observations
therefore does not create additional independent treatment assignments.

District-level Synthetic Control is consequently treated as supporting analysis rather than
as the primary basis for statistical inference.

---

## 12. Limitations

Several limitations are important when interpreting the results.

### Concurrent policy interventions

The suspension occurred alongside other interventions affecting agricultural commodity
markets, including export restrictions, stock limits, MSP and procurement policies, and
edible-oil policy changes.

These interventions make clean commodity-specific attribution difficult, particularly for
wheat.

### Counterfactual availability

The final comparison group contains nine commodities. Some potentially useful food and
oilseed comparison commodities are not available in the final district panel.

The counterfactual is therefore broader and more economically relevant than the initial
comparison group but is not exhaustive.

### Small number of treatment clusters

Treatment is assigned at the commodity level. The large number of district observations
does not remove the limited-cluster inference problem.

### Synthetic-Control inference

With nine donors, in-space placebo inference is coarse and cannot generate a p-value below
0.10.

### Aggregate statistical significance

The preferred aggregate Difference-in-Differences estimate is not statistically significant.
The evidence should therefore not be presented as a general statistically established decline
in volatility.

---

## 13. Conclusion

The empirical analysis does not support the hypothesis that India's 2021 suspension of
agricultural commodity derivatives increased spot-price volatility.

The final common-exposure Difference-in-Differences benchmark is approximately **−10.0%**,
but it is statistically insignificant and the corrected parallel-pre-trend restriction is
strongly rejected.

Commodity-level Synthetic Control estimates are also negative:

- Chana: **−37.3%**
- Mustard: **−28.2%**
- Wheat: **−37.8%**
- Soybean: **−27.6%**
- Moong: **−8.7%**

These estimates differ substantially in pre-treatment fit, placebo evidence and sensitivity.
Wheat is policy-confounded, while moong is particularly donor- and horizon-sensitive.

The estimated magnitude also depends materially on the donor pool. Expanding the comparison
set from the earlier five-donor specification to the final nine-donor specification changes
the aggregate benchmark from approximately **−20.7% to −10.0%**.

The defensible conclusion is therefore:

**there is no support for an increase in spot-price volatility following the suspension, but
the evidence does not justify a broad causal claim that the suspension reduced volatility.**

## 14. Final reproducibility and inference audit — 28 August 2026

The raw district-level Agmarknet collection contains **7,242,927 market-day records** across
16 commodity slugs and 569 JSON files.

The cleaned monthly volatility panel contains **172,381 observations**.

Restricting the panel to the final five treated and nine donor commodities gives **147,616
candidate observations**. Because the regression outcome is `ln(rv30)`, zero-volatility
observations cannot enter the log specification.

The final common-exposure DiD additionally excludes the August--December 2021 staggered
transition period. Its final estimation sample is therefore:

- **139,816 observations**
- **2,243 commodity-district units**
- **14 commodity clusters**
- **5 treated commodities and 9 controls**

The final baseline estimate is **−10.0%**, with clustered p = **0.1235** and t(G−1)-reference
p = **0.1475**.

The corrected joint pre-trend test rejects parallel trends at **p = 0.0029**, so the aggregate
DiD estimate is retained as a benchmark rather than a causal treatment effect.
