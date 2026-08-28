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

For this aggregate specification, a common post-treatment date of **20 December 2021** is
used for the treated commodities. The model compares the change in realized volatility for
suspended commodities after this date with the corresponding change for the comparison
commodities.

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

The preferred Difference-in-Differences estimate is approximately:

**−9.8%**

This indicates that realized spot-price volatility was, on average, lower for the suspended
commodities after the policy relative to the comparison group.

However, the estimate is not statistically significant under commodity-clustered inference.

- estimated effect: **−9.8%**
- number of commodity clusters: **14**
- clustered small-sample p-value: approximately **0.145**

Therefore, the main aggregate result should not be interpreted as evidence that the
suspension significantly reduced volatility.

The more appropriate conclusion is that the analysis finds **no evidence of an aggregate
increase in spot-price volatility following the suspension**.

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

**−9.8%**

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

The estimated aggregate effect remains negative under the main data-quality and liquidity
restrictions.

Across these specifications, the estimated effect is approximately between:

**−8.7% and −10.0%**

Selected leave-one-commodity-out estimates are:

| Specification | Estimated effect |
|---|---:|
| Baseline | **−9.8%** |
| Excluding chana | −7.4% |
| Excluding wheat | **−15.2%** |
| Excluding mustard | −9.3% |
| Excluding soybean | −9.0% |
| Excluding moong | −8.5% |

The estimate obtained after excluding wheat is approximately −15.2% and is statistically
significant under the reported clustered inference.

This indicates that the negative aggregate estimate is not mechanically driven by wheat.

At the same time, wheat should not be treated as a clean commodity-specific estimate because
its post-suspension period overlaps with substantial MSP, procurement, export and other policy
interventions.

---

## 8. Placebo and pre-treatment validation

The final specification performs substantially better in the main falsification exercises
than earlier versions of the panel.

The placebo-date estimate is approximately:

**−6.5%**

with:

- conventional placebo p-value ≈ **0.34**

The joint pre-treatment trend test gives:

**p ≈ 0.45**

These tests do not prove that the identifying assumptions are satisfied, but they do not
provide evidence of a statistically significant treatment-like effect before the actual
policy intervention.

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

After this correction, the placebo and pre-treatment diagnostics improved substantially.

This correction is important because it shows that the initial falsification failure was
related to data construction rather than being ignored or absorbed into the final
specification.

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

## 12. Conditional-volatility evidence







The conditional-volatility analysis consequently provides no additional evidence of a
post-suspension increase in volatility. The main conclusion is based on the realized-volatility
counterfactual analysis.

---

## 13. Limitations

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

## 14. Conclusion

The empirical analysis does not support the hypothesis that India's 2021 suspension of
agricultural commodity derivatives increased spot-price volatility.

The preferred aggregate Difference-in-Differences estimate is approximately **−9.8%**, but
the estimate is not statistically significant under commodity-level clustered inference.

The most appropriate aggregate conclusion is therefore:

**there is no evidence of an increase in spot-price volatility following the suspension.**

The strongest commodity-level evidence of lower volatility is concentrated in **chana**.
Synthetic Control estimates an effect of approximately **−37.3%**, with an in-space placebo
p-value of **0.10**.

Results for mustard, soybean and moong are negative but have weaker placebo evidence. Wheat is
particularly difficult to interpret because of concurrent policy interventions.

The analysis also shows that the estimated magnitude depends materially on the choice of
counterfactual. Expanding the comparison set from the earlier narrow donor group changes the
aggregate estimate from approximately −20.7% to −9.8%.

Taken together, the results reject a simple interpretation in which the suspension generated
a broad increase in spot-market volatility. They instead indicate a modest negative aggregate
estimate with substantial commodity heterogeneity and considerable uncertainty around causal
attribution.

## 15. Reproducibility and inference audit — 28 August 2026

The final H1 district-panel result was independently reconstructed from the
current repository before preparation of the final report.

The final 14-commodity candidate sample contains **147,616** monthly
commodity-district observations. **1,109 observations (0.75%)** have zero
measured `rv30`; because the main outcome is `ln(rv30)`, these observations
cannot be logged and are excluded. The resulting estimation sample contains
**146,507 observations, 2,244 commodity-district units, and 14 commodity
clusters (5 treated and 9 controls)**.

### Treatment-month sensitivity

The December 2021 monthly cell combines observations from before and after the
20 December common treatment date. This coding choice is not driving the main
estimate:

| Treatment-month rule | Estimated change |
|---|---:|
| December 2021 counted as post | **−9.79%** |
| December 2021 retained as pre; post begins January 2022 | **−9.83%** |
| December 2021 dropped; post begins January 2022 | **−9.92%** |

### Estimation-window sensitivity

The magnitude is more sensitive to the overall estimation horizon:

| Window around December 2021 | Estimated change | t(G−1)-reference p |
|---|---:|---:|
| ±12 months | **−20.45%** | **0.0074** |
| ±24 months | **−10.48%** | **0.1589** |
| ±36 months | **−4.84%** | **0.5304** |
| Full available panel | **−9.79%** | **0.1447** |

The shorter-window result is therefore reported as a sensitivity result rather
than selected as the headline specification. The preferred interpretation is
that the negative association is strongest relatively close to the suspension
and attenuates as increasingly distant periods and additional policy changes
enter the comparison.
