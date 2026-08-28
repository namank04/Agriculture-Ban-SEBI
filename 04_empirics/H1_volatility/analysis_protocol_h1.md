# H1 Analysis Protocol and Final Implementation

## 1. Purpose

This document records the empirical design used to study the effect of India's 2021
agricultural-derivatives suspension on spot-price volatility.

It serves two purposes:

1. to preserve the analysis decisions that were specified before the main Synthetic Control
   stage; and
2. to document how the final H1 analysis was actually implemented.

The design evolved during the project as data-quality problems, counterfactual limitations
and falsification results were identified. The final implementation therefore differs in
several places from the earlier analysis plan. Those differences are recorded explicitly
below.

The corresponding empirical results are reported in:

`c1_findings.md`

---

## 2. Research question

The main question is:

**Did the suspension of agricultural commodity derivatives change spot-price volatility in
the affected commodities relative to a credible comparison group?**

The outcome of interest is spot-market volatility rather than futures-market volatility.

The original working hypothesis was that removal of derivatives trading could increase spot
volatility by weakening information aggregation or risk-transfer mechanisms.

The analysis therefore tests whether treated commodities experienced a different change in
spot volatility after suspension compared with commodities whose derivatives were not
suspended.

---

## 3. Stage at which the protocol was specified

The H1 design was formalized after the initial Difference-in-Differences and data-validation
work had already begun.

In particular, the earlier analysis had already revealed:

- sensitivity of the result to data construction;
- problems with the original calendar grid;
- weak falsification performance in an early specification;
- the need for a more credible comparison group; and
- the need to supplement Difference-in-Differences with synthetic counterfactual methods.

The protocol was therefore not specified before any data analysis.

It was used to discipline the later H1 stage, particularly the Synthetic Control, donor-pool and robustness analyses.

---

## 4. Outcome construction

The primary outcome is:

`ln(rv30)`

where `rv30` is the rolling 30-day realized volatility of daily log spot-price returns.

For a spot-price series \(P_t\), the daily log return is:

\[
r_t = \ln(P_t) - \ln(P_{t-1})
\]

The rolling volatility measure is based on the standard deviation of these returns over a
30-observation window and is annualized using a 252-trading-day convention.

The logarithm of realized volatility is used in the panel regressions.

The main data are district-level mandi spot-price observations.

---

## 5. Calendar correction

An important modification to the original data construction occurred during validation.

The mandi data behaved partly like a seven-day calendar grid because some markets reported
observations on weekends, while the volatility calculation used a 252-trading-day
annualization convention.

This created an inconsistent time-frequency construction.

The final panel therefore retains **Monday-to-Friday observations** before constructing
returns and rolling realized volatility.

This is a weekday filter rather than a complete exchange-holiday adjustment.

The correction was adopted before producing the final H1 estimates because the earlier
calendar construction generated problematic placebo and pre-treatment behaviour.

---

## 6. Treated commodities

The final primary H1 analysis uses five treated commodities:

- chana
- mustard
- wheat
- soybean
- moong

Two other suspended commodities are not included in the primary volatility analysis.

### Paddy

Paddy is excluded because its observed mandi-price series contains a very high proportion
of exactly flat price changes.

The resulting realized-volatility measure is strongly affected by MSP and procurement-related
price censoring and is therefore not treated as a clean market-volatility outcome.

### CPO

CPO is excluded because a comparable mandi spot-price series is not available for the
spot-volatility analysis.

CPO-related futures work is therefore separate from H1.

---

## 7. Comparison commodities

The initial comparison set relied mainly on commodities already available in the data:

- castor
- guarseed413
- cotton
- jeera
- turmeric

This comparison group was useful for the first stage of analysis but was economically
imperfect for several treated food commodities.

The donor pool was subsequently expanded with food-cereal commodities.

The final comparison group used in the main H1 analysis is:

- castor
- guarseed413
- cotton
- jeera
- turmeric
- barley
- maize
- jowar
- bajra

Bajra has partial coverage in the final district panel.

The final nine-commodity comparison set is frozen for all reported H1 DiD and SCM results.
The code does not auto-expand the donor pool if additional commodities later appear in the
underlying panel.

The expansion of the comparison group materially changes the estimated aggregate effect and
is therefore treated as an important counterfactual-sensitivity result rather than as a
minor data update.

---

## 8. Guar-series correction

The original guar series with commodity ID 75 was excluded after validation showed that it
was contaminated by guar-gum observations and did not behave like the intended guar-seed
underlying.

The clean comparison series is:

`guarseed413`

The contaminated guar series is not used in the final H1 comparison group.

---

## 9. Treatment timing

Treatment timing differs across the empirical estimators.

### Aggregate Difference-in-Differences

The primary aggregate Difference-in-Differences specification uses a common post-treatment
date:

**20 December 2021**

This provides one common treatment indicator for the pooled treated group.

### Commodity-level Synthetic Control

Commodity-level Synthetic Control uses the relevant suspension dates:

| Commodity | Treatment date |
|---|---|
| Chana | 16 August 2021 |
| Mustard | 8 October 2021 |
| Wheat | 20 December 2021 |
| Soybean | 20 December 2021 |
| Moong | 20 December 2021 |

This distinction is important when comparing the aggregate DiD estimate with
commodity-specific synthetic estimates.

---

## 10. Initial planned empirical strategy

After the first-stage diagnostics, the analysis plan proposed using several complementary
estimators rather than relying on a single Difference-in-Differences coefficient.

The main planned components were:

- district-panel Difference-in-Differences;
- commodity-level Synthetic Control;
- placebo tests;
- pre-treatment diagnostics;
- commodity-clustered inference;
- robustness to alternative donor pools and data filters.

Several additional methods were considered during this stage, including:

- Augmented Synthetic Control;
- penalized Synthetic Control;
- Honest-DiD sensitivity analysis;
- conformal or SCPI-style Synthetic Control inference;
- additional staggered-DiD estimators.

These additional estimators were **considered but were not part of the final implemented
analysis**.

They are therefore not used to support the final H1 conclusions.

---

## 11. Final implemented Difference-in-Differences analysis

The final aggregate specification uses a two-way fixed-effects panel model.

The empirical structure can be written schematically as:

\[
\ln(RV_{i,t})
=
\alpha_i
+
\gamma_t
+
\beta(Treated_i \times Post_t)
+
\varepsilon_{i,t}
\]

where:

- \(i\) denotes a district-commodity unit;
- \(t\) denotes month;
- \(\alpha_i\) are unit fixed effects;
- \(\gamma_t\) are time fixed effects;
- `Treated` identifies suspended commodities; and
- `Post` begins on 20 December 2021 in the aggregate specification.

The coefficient \(\beta\) measures the relative post-suspension change in log realized
volatility for treated commodities.

Treatment is assigned at the **commodity level**.

Although the panel contains many district observations, these districts are not independent
treatment assignments.

Inference therefore clusters at the commodity level.

Because the final specification has 14 commodity clusters, the clustered t statistic is also
evaluated against a **t(G−1)** reference distribution as a small-cluster sensitivity check.

---

## 12. Final implemented Synthetic Control analysis

Synthetic Control is estimated separately for each treated commodity.

For each treated commodity, donor weights are selected to reproduce its pre-treatment
volatility path as closely as possible using the comparison commodities.

The synthetic counterfactual is:

\[
Y^{SC}_{t}
=
\sum_j w_jY_{j,t},
\]

subject to:

\[
w_j \geq 0,
\qquad
\sum_j w_j = 1.
\]

The post-treatment difference between the treated series and its synthetic counterpart is
used to estimate the treatment-associated change.

Synthetic Control is estimated at the commodity level as the main synthetic analysis.

---

## 13. Synthetic Control inference

In-space placebo tests are used for Synthetic Control inference.

Each donor commodity is treated in turn as though it had received the intervention. The
treated commodity's post-treatment gap is then compared with the distribution of placebo
gaps.

With nine donor commodities, the smallest attainable placebo p-value is:

\[
\frac{1}{9+1}=0.10.
\]

This limits the statistical resolution of commodity-level Synthetic Control.

The Synthetic Control results are therefore interpreted jointly with the other estimators
rather than as standalone conventional significance tests.

---

## 14. District-level Synthetic Control

Synthetic Control was also estimated at the district level.

The purpose of this analysis is to examine heterogeneity in the estimated post-suspension
effect across local markets.

District-level SCM does **not** solve the small-number-of-treatment-clusters problem.

The policy is assigned at the commodity level, not independently at the district level.
Therefore, a larger number of district observations does not create additional independent
treatments.

These results are treated as supporting and heterogeneity evidence rather than as the main
basis for statistical inference.

---

## 15. Robustness analysis

The final H1 analysis evaluates the aggregate DiD estimate under several alternative data
restrictions.

These include:

- winsorizing realized volatility at the commodity-level 99th percentile;
- dropping observations with very high realized volatility;
- requiring districts to have at least 24 months of observations;
- requiring districts to have at least 36 months of observations;
- combining minimum-history and outlier restrictions;
- excluding each treated commodity one at a time.

The purpose is to determine whether the estimated effect depends on a small number of noisy
districts, extreme volatility observations or a single treated commodity.

---

## 16. Placebo and pre-treatment validation

The final specification is evaluated using placebo and pre-treatment exercises.

### Placebo treatment date

A false treatment date is used to test whether the model generates a treatment-like effect
when no actual suspension occurred.

A substantial placebo effect would weaken confidence in the interpretation of the main
estimate.

### Pre-treatment trends

Pre-treatment behaviour is examined to determine whether treated and comparison commodities
were already moving differently before the intervention.

The final specification does not produce statistically significant evidence of differential
pre-treatment behaviour under the reported joint test.

## 17. Changes from the earlier analysis plan

The final implementation differs from the earlier analysis plan in several important ways.

### 17.1 Comparison group expanded

The initial five-commodity industrial/spice-heavy comparison set was expanded with four
economically closer food-cereal commodities. This progression is retained as a donor-pool
sensitivity exercise: the estimated aggregate effect moved from approximately −20.7% to
−9.8%, demonstrating that counterfactual composition materially affects the estimated
magnitude. The fixed nine-commodity pool is used for the preferred specification.

This change materially reduced the magnitude of the aggregate estimate.

### 17.2 Paddy excluded

Paddy was removed from the primary volatility analysis because of substantial price
censoring and flat returns.

### 17.3 Guar ID 75 excluded

The contaminated guar series was replaced by the validated guarseed413 series.

### 17.4 Calendar construction corrected

The volatility panel was rebuilt using Monday-to-Friday observations after the earlier
calendar construction produced problematic falsification results.

### 17.5 Several proposed estimators were not implemented

Augmented SCM, penalized SCM, Honest-DiD, conformal/SCPI inference and other proposed
staggered-DiD extensions were not part of the final empirical execution.

They are therefore not presented as completed methods.

### 17.6 District SCM retained only as supporting analysis

District-level Synthetic Control was implemented, but it is interpreted as a heterogeneity
analysis rather than as a solution to the small-cluster inference problem.

---

## 18. Interpretation rule

No H1 conclusion is based on a single estimator.

The final interpretation considers together:

- aggregate Difference-in-Differences;
- commodity-level Synthetic Control;
- placebo and pre-treatment diagnostics;
- donor-pool sensitivity;
- leave-one-commodity-out robustness;
- data-construction validation.

Consistency across these components strengthens an interpretation, while disagreement or
sensitivity is reported explicitly.

The preferred aggregate estimate and the complete empirical interpretation are given in
`c1_findings.md`.

---

## 19. Main implementation files

The principal scripts supporting H1 are:

- `00_code/build_volatility_panel.py`
- `00_code/run_v0_did.py`
- `00_code/run_v0_placebo.py`
- `00_code/run_c1_robustness.py`
- `00_code/run_c1_scm.py`
- `00_code/run_c1_scm_district.py`

The main H1 output files are stored in:

`04_empirics/H1_volatility/output/`

The final interpretation of these outputs is documented in:

`04_empirics/H1_volatility/c1_findings.md`

## Reproducibility audit update — 28 August 2026

This section records the final independent audit of the H1 panel, sample construction
and baseline inference used for the final report.

### Panel provenance

The current raw Agmarknet district directory contains **569 JSON files**
covering 16 commodity slugs. The files contain **7,242,927 raw market-day
records** in total; 301 state-commodity files are valid but contain no data.

The constructed monthly volatility panel contains **172,381 observations**
from February 2017 through October 2025, with no duplicate
commodity-state-district-month keys.

The final H1 treatment/control set contains:

- treated: chana, mustard, wheat, soybean and moong;
- controls: castor, guarseed413, cotton, jeera, turmeric, barley, maize,
  jowar and bajra.

This produces **147,616 candidate observations** across 14 commodities.

### Zero-volatility observations

There are **1,109 zero-`rv30` observations** in the final 14-commodity
candidate sample, approximately **0.75%** of candidate observations. Because
the regression outcome is `ln(rv30)`, zero values are undefined on the log
scale and are excluded. The final baseline estimation sample is therefore:

- **146,507 observations**;
- **2,244 commodity-district units**;
- **14 commodity clusters**;
- **5 treated clusters and 9 control clusters**.

### Treatment-month audit

The common treatment date is 20 December 2021, while the estimation outcome is
monthly. Three treatments of the mixed December-2021 cell were checked:

- December counted as post: **−9.7947%**;
- December retained as pre, January 2022 onward post: **−9.8291%**;
- December removed, January 2022 onward post: **−9.9206%**.

The treatment-month convention therefore has negligible effect on the
aggregate estimate.

### Estimation-window sensitivity

Using January 2022 as the post-period start and dropping December 2021:

- ±12 months: **−20.4525%**, t(G−1)-reference p = **0.0074**;
- ±24 months: **−10.4751%**, p = **0.1589**;
- ±36 months: **−4.8437%**, p = **0.5304**.

The full-panel estimate remains approximately **−9.8%**. These results show
meaningful horizon sensitivity. The ±12-month result is an exploratory
sensitivity result, not a replacement headline specification.
