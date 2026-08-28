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
construct rolling 30-day realized volatility, which is then aggregated to a monthly panel.

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

### 3.3 Synthetic Difference-in-Differences

Synthetic Difference-in-Differences is used as an additional counterfactual estimator,
combining features of Difference-in-Differences and Synthetic Control.

Results are reported both for the pooled treated group and separately by commodity.

### 3.4 Validation and robustness

The main estimates are evaluated using:

- alternative data-quality and liquidity filters;
- leave-one-commodity-out specifications;
- placebo treatment dates;
- pre-treatment trend tests;
- wild-cluster bootstrap inference;
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
- wild-cluster bootstrap p-value: approximately **0.153**

Therefore, the main aggregate result should not be interpreted as evidence that the
suspension significantly reduced volatility.

The more appropriate conclusion is that the analysis finds **no evidence of an aggregate
increase in spot-price volatility following the suspension**.

---

## 5. Sensitivity to the comparison group

The choice of comparison commodities has an important effect on the estimated magnitude.

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

The earlier −20.7% estimate remains useful as a robustness and model-development result, but
it is not treated as the preferred estimate.

---

## 6. Synthetic Difference-in-Differences results

The pooled Synthetic Difference-in-Differences estimate is:

**−19.1%**

with a placebo-based z-statistic of approximately:

**−1.88**

This is directionally consistent with the Difference-in-Differences estimate but is not
strong enough to provide decisive aggregate statistical evidence.

Commodity-level Synthetic Difference-in-Differences estimates are:

| Commodity | Estimated effect | Approx. z-statistic |
|---|---:|---:|
| Chana | **−38.7%** | **−2.05** |
| Mustard | −15.2% | −0.68 |
| Wheat | +0.4% | +0.02 |
| Soybean | −26.1% | −1.32 |
| Moong | −11.5% | −0.53 |

The strongest individual result is obtained for chana.

Wheat produces an estimate close to zero under Synthetic Difference-in-Differences, which
also indicates that its result is sensitive to estimator choice and should be interpreted
carefully.

---

## 7. Synthetic Control results

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

## 8. Robustness of the aggregate estimate

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

## 9. Placebo and pre-treatment validation

The final specification performs substantially better in the main falsification exercises
than earlier versions of the panel.

The placebo-date estimate is approximately:

**−6.5%**

with:

- conventional placebo p-value ≈ **0.34**
- wild-cluster bootstrap p-value ≈ **0.43**

The joint pre-treatment trend test gives:

**p ≈ 0.45**

These tests do not prove that the identifying assumptions are satisfied, but they do not
provide evidence of a statistically significant treatment-like effect before the actual
policy intervention.

---

## 10. Trading-day correction

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

## 11. Commodity-level interpretation

### 11.1 Chana

Chana provides the clearest evidence of lower spot-price volatility after the suspension.

- Synthetic DiD: **−38.7%**
- Synthetic Control: **−37.3%**

The similar magnitude across the two synthetic estimators makes chana the strongest
commodity-level result in the volatility analysis.

The limited number of donor commodities nevertheless restricts the precision of
Synthetic-Control placebo inference.

### 11.2 Mustard

Mustard produces negative estimates under both synthetic approaches:

- Synthetic DiD: **−15.2%**
- Synthetic Control: **−28.2%**

The direction is consistent with lower volatility, but statistical evidence is weak.

### 11.3 Soybean

Soybean also produces negative estimates:

- Synthetic DiD: **−26.1%**
- Synthetic Control: **−27.6%**

The magnitudes are similar across the two methods, although inference remains weak.

### 11.4 Wheat

Wheat is the most difficult treated commodity to interpret.

Synthetic DiD gives an effect close to zero, while Synthetic Control produces a much larger
negative estimate.

The disagreement between estimators, together with contemporaneous agricultural and trade
policy interventions, makes wheat a less reliable commodity for isolating the effect of the
derivatives suspension.

### 11.5 Moong

Moong produces relatively small negative effects:

- Synthetic DiD: **−11.5%**
- Synthetic Control: **−8.7%**

The statistical evidence is weak.

---

## 12. District-level Synthetic Control

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

## 13. Conditional-volatility evidence

A supplementary ICSS/GARCH analysis was used to examine whether the suspension coincided with
a distinct conditional-volatility regime change.

Among the commodity series tested, ICSS does not identify a volatility break close to the
suspension date.

The district-median chana GARCH specification is unstable or degenerate and is therefore not
used as primary evidence.

The conditional-volatility analysis consequently provides no additional evidence of a
post-suspension increase in volatility. The main conclusion is based on the realized-volatility
counterfactual analysis.

---

## 14. Limitations

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

## 15. Conclusion

The empirical analysis does not support the hypothesis that India's 2021 suspension of
agricultural commodity derivatives increased spot-price volatility.

The preferred aggregate Difference-in-Differences estimate is approximately **−9.8%**, but
the estimate is not statistically significant under commodity-level clustered inference.

The most appropriate aggregate conclusion is therefore:

**there is no evidence of an increase in spot-price volatility following the suspension.**

The strongest evidence of lower volatility is concentrated in **chana**, for which both
Synthetic Difference-in-Differences and Synthetic Control produce effects of approximately
−37% to −39%.

Results for mustard, soybean and moong are negative but statistically weaker. Wheat is
particularly sensitive to estimator choice and concurrent policy interventions.

The analysis also shows that the estimated magnitude depends materially on the choice of
counterfactual. Expanding the comparison set from the earlier narrow donor group changes the
aggregate estimate from approximately −20.7% to −9.8%.

Taken together, the results reject a simple interpretation in which the suspension generated
a broad increase in spot-market volatility. They instead indicate a modest negative aggregate
estimate with substantial commodity heterogeneity and considerable uncertainty around causal
attribution.
