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

where `rv30` is realized volatility constructed from a rolling window of 30 observed
daily log spot-price returns.

For a spot-price series \(P_t\), the daily log return is:

\[
r_t = \ln(P_t) - \ln(P_{t-1})
\]

The rolling volatility measure is based on the standard deviation of the most recent
30 observed returns and is annualized using a 252-trading-day convention. The window is
therefore based on observations rather than a fixed 30-calendar-day interval.

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

The final aggregate Difference-in-Differences uses a **common-exposure design**:

- observations through **July 2021** form the genuine pre-treatment period;
- **August--December 2021** is excluded as the staggered transition period;
- the common post-treatment period begins in **January 2022**.

This avoids classifying months in which chana or mustard had already been suspended while
other treated commodities had not yet entered suspension as either a clean pooled pre-period
or a clean pooled post-period.

### Commodity-level Synthetic Control

Commodity-level Synthetic Control uses each commodity's actual suspension date:

| Commodity | Treatment date |
|---|---|
| Chana | 16 August 2021 |
| Mustard | 8 October 2021 |
| Wheat | 20 December 2021 |
| Soybean | 20 December 2021 |
| Moong | 20 December 2021 |

This distinction is important: the pooled DiD estimates a common-exposure benchmark, whereas
Synthetic Control preserves the actual commodity-specific policy timing.

---

## 10. Final empirical strategy

The final H1 analysis uses complementary counterfactual and validation exercises:

- district-panel Difference-in-Differences as an aggregate benchmark;
- commodity-level Synthetic Control as the main commodity-specific counterfactual method;
- in-space Synthetic-Control placebos;
- district-level Synthetic Control for heterogeneity;
- pre-treatment trend diagnostics;
- a pre-treatment placebo-date exercise;
- commodity-clustered inference with a t(G−1) reference check;
- donor-pool sensitivity;
- alternative sample-quality filters;
- leave-one-treated-commodity-out analysis; and
- treatment-horizon sensitivity.

No H1 conclusion is based on a single coefficient.

---

## 11. Final implemented Difference-in-Differences analysis

The final aggregate specification uses a two-way fixed-effects panel model on the
common-exposure sample.

The empirical structure is:

\[
\ln(RV_{i,t})
=
\alpha_i
+
\gamma_t
+
\beta(Treated_i \times Post_t)
+
\varepsilon_{i,t},
\]

where:

- \(i\) denotes a commodity-district unit;
- \(t\) denotes month;
- \(\alpha_i\) are unit fixed effects;
- \(\gamma_t\) are month fixed effects;
- `Treated` identifies the five suspended commodities; and
- `Post` equals one from January 2022 onward.

The August--December 2021 transition period is excluded.

The coefficient \(\beta\) measures the relative post-suspension change in log realized
volatility for treated commodities compared with the nine comparison commodities.

Treatment is assigned at the **commodity level**. Districts therefore do not represent
independent treatment assignments.

Inference is clustered by commodity. With 14 commodity clusters, the clustered t statistic
is also evaluated against a **t(G−1)** reference distribution.

The final common-exposure estimation sample contains:

- **139,816 observations**
- **2,243 commodity-district units**
- **14 commodity clusters**

The baseline coefficient is approximately **−0.1059**, corresponding to an effect of
approximately **−10.0%**.

The conventional clustered p-value is **0.1235** and the t(G−1)-reference p-value is
**0.1475**.

Because the corrected pre-treatment diagnostic rejects parallel trends, this coefficient is
retained as an **aggregate benchmark rather than a clean causal estimate**.

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

The final specification is evaluated using both a pre-treatment placebo and a genuine
pre-treatment trend test.

### Pre-treatment placebo

The placebo design uses a fake transition period from August--December 2019, starts the fake
post-period in January 2020, and excludes observations exposed to the actual suspension.

The placebo estimate is approximately:

**−9.6%**

with:

- conventional clustered p-value: **0.1569**
- t(G−1)-reference p-value: **0.1804**

Although statistically insignificant, the placebo magnitude is economically close to the
actual −10.0% benchmark. It therefore weakens rather than strengthens a causal interpretation.

### Pre-treatment trends

The pre-trend exercise uses only genuinely untreated months before the earliest suspension.

Three half-year lead bins are estimated:

- months −18 to −13: beta = **−0.2263**, p = 0.0616
- months −12 to −7: beta = **−0.1446**, p = 0.1655
- months −6 to −2: beta = **+0.0412**, p = 0.6053

The joint small-cluster reference test gives:

**F(3,13) = 7.95, p = 0.0029**

The parallel-pre-trend restriction is therefore **rejected**.

Accordingly, the final aggregate DiD coefficient is not interpreted as a clean causal
treatment effect.

---

## 17. Important design refinements

### 17.1 Comparison group expanded

The initial five-commodity comparison set consisted mainly of industrial and spice
commodities:

- castor
- guarseed413
- cotton
- jeera
- turmeric

Four food-cereal controls were subsequently added:

- barley
- maize
- jowar
- bajra

This donor-pool progression is retained as an important model-risk result. The aggregate
estimate moved from approximately **−20.7%** under the narrower five-donor specification to
approximately **−10.0%** under the final nine-donor specification.

Counterfactual composition therefore materially affects estimated magnitude.

### 17.2 Paddy excluded

Paddy was removed from the primary volatility analysis because its mandi-price series contains
substantial flat-price behavior consistent with MSP/procurement-related censoring.

### 17.3 Guar series validated

The contaminated guar series was replaced by the validated `guarseed413` series.

### 17.4 Calendar construction corrected

The volatility panel was rebuilt using Monday-to-Friday observations before constructing
returns. This removed an inconsistent calendar-frequency construction.

The correction did **not** make the final DiD design causally valid: the corrected joint
pre-trend test still rejects parallel trends.

### 17.5 District SCM retained as heterogeneity analysis

District-level Synthetic Control is used to describe local heterogeneity. It is not treated as
additional independent policy-level inference because treatment occurs at the commodity level.

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

Agreement across these components is treated as supporting evidence, while disagreement,
failed diagnostics and specification sensitivity are reported explicitly. In particular, the
failed pre-trend test prevents a broad causal interpretation of the aggregate DiD.

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

## Final reproducibility audit — 28 August 2026

The final raw Agmarknet district collection contains:

- **569 JSON files**
- **16 commodity slugs**
- **7,242,927 raw market-day records**

The cleaned monthly volatility panel contains **172,381 observations** from February 2017
through October 2025.

Restricting the panel to the final five treated and nine comparison commodities produces
**147,616 candidate observations**.

The aggregate common-exposure DiD then:

1. excludes observations with zero `rv30` because `ln(rv30)` is undefined; and
2. excludes the August--December 2021 staggered transition period.

The resulting final baseline estimation sample contains:

- **139,816 observations**
- **2,243 commodity-district units**
- **14 commodity clusters**

The final aggregate benchmark is approximately **−10.0%**:

- beta = **−0.1059**
- clustered p = **0.1235**
- t(G−1)-reference p = **0.1475**

The corrected joint pre-treatment test gives:

**F(3,13) = 7.95, p = 0.0029**

Parallel pre-trends are therefore rejected. The DiD estimate is retained as a benchmark and
not interpreted causally.
