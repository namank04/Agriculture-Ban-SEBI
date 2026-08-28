# Literature Review

## 1. Indian policy context

Agricultural futures trading in India has repeatedly been questioned during periods of
food-price inflation. The policy concern is that speculative activity in derivatives may
raise or destabilize spot prices, while the counterargument is that futures markets provide
hedging, liquidity, and information about expected prices.

A central policy reference is the **2008 Expert Committee on Futures Trading**, chaired by
Abhijit Sen. Reviewing the earlier wave of agricultural-futures suspensions, the committee
did not find conclusive evidence that futures trading was responsible for the observed rise
in agricultural commodity prices. This unresolved policy debate is important for the 2021
suspension: the intervention again removed futures trading from selected agricultural
commodities with the objective of controlling price pressures, but the effect on the
underlying spot markets remained an empirical question.

The December 2021 suspension therefore provides a useful setting for evaluating whether
removing futures trading was followed by improved spot-price stability and whether the
functioning of the remaining spot markets changed.

---

## 2. Evidence on the 2021 agricultural-derivatives suspensions

### 2.1 Aggarwal, Chatterjee and Sehgal

Aggarwal, Chatterjee and Sehgal study Indian commodity-derivatives suspension episodes
using **Synthetic Control Methods**. Their analysis includes the 2021 chana and mustard
suspensions and constructs counterfactual price paths from commodities that were not
suspended.

Their results provide little evidence that suspending derivatives reduced the relevant
commodity prices or food-price inflation. The importance of this study for the present
project is methodological as much as substantive: evaluating a suspension requires a
credible counterfactual rather than a simple comparison of prices before and after the
policy.

This directly motivates the use of comparison commodities and synthetic-control methods in
our analysis.

### 2.2 Gaurav and Pandey (2024)

Gaurav and Pandey examine the impact of the recent suspension using futures, spot and retail
price data for major affected agricultural commodities. Their study considers several
outcomes, including price behaviour, volatility and broader effects on the agricultural
market ecosystem.

An important distinction in their results is between simple pre/post comparisons and
controlled comparisons. Descriptive volatility measures may rise after the suspension, but
their volatility Difference-in-Differences results against comparison commodities are much
weaker and are largely null.

This distinction is central to our project. The post-2021 period contained many other
commodity-market shocks, so an observed change after the suspension cannot by itself be
interpreted as the effect of the suspension. Their work therefore provides both a direct
comparison for our volatility analysis and further motivation for using explicit
counterfactual designs.

### 2.3 Dey and Gairola (2024)

Dey and Gairola examine agricultural-futures suspensions using commodities including chana,
soybean and refined soy oil. They report higher post-suspension spot-price volatility for
some commodities, particularly chickpeas and refined soy oil.

These results are useful as a contrasting empirical benchmark because their volatility
comparison is primarily based on pre- and post-suspension behaviour. Our analysis asks
whether such apparent changes remain once banned commodities are compared against
commodities exposed to the same macroeconomic period but not to the suspension.

The difference in research design is therefore important when comparing conclusions across
the two studies.

### 2.4 Rajib, Barai and Arora (2024)

Rajib, Barai and Arora study the suspension from a broader commodity-market ecosystem
perspective. Among their results is evidence on price dispersion across mandis and changes
in market linkages after the suspension.

Their use of the word *volatility* must be distinguished from the outcome used in our main
analysis. Much of their relevant measure reflects **cross-mandi spatial price dispersion**,
whereas our H1 outcome is **time-series realized volatility of spot-price changes**. These
are related aspects of market functioning but are not the same estimand.

The spatial dimension of their work is particularly relevant to our supporting H3 analysis,
which asks whether spot markets became less informationally efficient or less integrated
after futures trading was removed.

---

## 3. What the existing literature implies for research design

The direct Indian evidence does not produce a single unambiguous answer. Some descriptive
studies report higher volatility after futures suspensions, while studies using explicit
comparison markets or synthetic counterfactuals generally provide weaker evidence that the
suspensions improved prices or stability.

Three design issues follow from this literature.

### 3.1 A pre/post comparison is not enough

The suspension was not followed by an economically quiet period. Global food and energy
markets experienced major shocks, while individual Indian commodities were also affected
by interventions such as export restrictions, stock limits, procurement and support-price
policies.

A change in a banned commodity after the suspension can therefore reflect the suspension,
common macroeconomic shocks, commodity-specific policies, or ordinary mean reversion.

For this reason, the main analysis uses untreated commodities as a counterfactual rather
than interpreting the banned commodities' own pre/post change as the treatment effect.

### 3.2 The counterfactual itself must be tested

The project initially showed why merely adding a control group is not sufficient. An
earlier specification using a narrow industrial/spice-heavy donor set produced an estimated
volatility decline of approximately **20.7%**. After expanding the comparison set with
food-cereal commodities that provide a more economically relevant counterfactual, the
aggregate estimate fell to approximately **9.8% lower volatility** and lost conventional
statistical significance.

The movement in the estimate is itself an important result: conclusions depend materially
on the quality of the comparison group.

The final H1 analysis therefore uses several complementary approaches:

- Difference-in-Differences on the district-level spot-price panel;
- commodity-level Synthetic Control;
- Synthetic Difference-in-Differences;
- leave-one-out and data-quality robustness checks;
- placebo-date falsification and pre-trend testing; and
- few-cluster inference, including a wild-cluster bootstrap.

These methods are used as alternative views of the same underlying comparison rather than
as independent confirmations of the result.

### 3.3 Identification checks are part of the result

The project's falsification tests materially affected the analysis. An earlier version of
the panel generated a significant effect at a false 2019 treatment date and showed
problematic pre-treatment behaviour. Investigation of those failures revealed a
calendar-grid measurement problem: non-trading-day price observations were being mixed with
a volatility construction based on trading days.

After rebuilding the panel on trading-day-consistent data and revising the donor set, the
placebo and pre-trend results became substantially cleaner.

This experience reinforces the methodological concerns emphasized in the DiD literature:
serial dependence, few treatment clusters, pre-treatment behaviour and counterfactual choice
can materially change the apparent precision and interpretation of a policy estimate.

### 3.4 Methodological references

The main methods used in this project are supported by a small set of standard methodological
papers. Abadie, Diamond and Hainmueller (2010) provide the foundation for **Synthetic Control**,
while Arkhangelsky et al. (2021) develop **Synthetic Difference-in-Differences**. Bertrand,
Duflo and Mullainathan (2004) motivate careful inference in Difference-in-Differences with
correlated panel data, and MacKinnon and Webb (2018) motivate the **wild-cluster bootstrap**
when the number of treatment clusters is small. Roth (2022) provides guidance on interpreting
pre-trend tests cautiously, while Ferman and Pinto (2017) discuss important limitations of
Synthetic Control inference. These references are retained because they directly support
methods or validation checks used in the final analysis.

---

## 4. Position of this project in the literature

### 4.1 Spot-price volatility

The main empirical contribution is a district-level evaluation of spot-price volatility
using roughly 5.7 million raw mandi price observations.

The final food-donor specification does **not** support the inherited hypothesis that spot
volatility rose by roughly 8–10% after the suspension. The aggregate Difference-in-
Differences estimate instead implies approximately **9.8% lower volatility**, but this
aggregate effect is **not statistically significant under the preferred few-cluster
inference**.

The negative evidence is heterogeneous across commodities and is strongest for **chana**.
Wheat is treated cautiously because its post-suspension period coincides with substantial
additional policy intervention.

Accordingly, the project does not interpret the results as evidence that the suspension
generally and significantly reduced agricultural spot volatility. The defensible conclusion
is narrower: the hypothesized aggregate volatility increase is not supported, the estimated
aggregate decline is modest and statistically uncertain, and the strongest commodity-level
negative signal is concentrated in chana.

### 4.2 Spot-market efficiency and spatial integration

The supporting H3 analysis studies a different question: whether the functioning of the
remaining **spot markets** changed after futures trading was suspended.

Two measures are used:

- variance-ratio behaviour of spot returns as an indicator of informational efficiency; and
- cross-mandi cointegration and price-deviation correction as indicators of spatial market
  integration.

Both move in the direction of weaker post-suspension market functioning for the banned
commodities relative to controls. The cross-mandi integration result is the stronger of the
two, but the number of clean commodity-level observations is small and the evidence is
statistically underpowered.

The appropriate interpretation is therefore **suggestive evidence of weaker spot-market
efficiency and spatial integration**, not a definitive causal result.

This distinction is also important conceptually: H3 does **not** directly estimate
futures-versus-spot price discovery.

### 4.3 Conditional-volatility evidence

ICSS and GARCH analysis is retained as a supplementary time-series diagnostic rather than a
separate headline result. Among the tested series, the analysis does not find evidence of a
volatility-regime break near the suspension date.

This fails to reproduce the earlier claim of elevated conditional volatility associated
with the suspension and supports keeping the main volatility conclusion anchored in H1.

### 4.4 Market-participant composition

SEBI participant data provide descriptive context on the market that was suspended. In the
available pre-suspension bulletin sample, the explicitly registered hedger category forms a
small share of reported NCDEX agricultural turnover.

This result is interpreted cautiously. The SEBI category is a narrow classification and
client activity may also contain hedging activity, while the currently parsed bulletins
cover only part of the desired pre-ban period. The composition analysis is therefore
supporting institutional context rather than evidence that hedging activity was absent.

---

## 5. Price discovery as a future extension

The present project should not equate weaker cross-mandi spot integration with direct
evidence of a loss of futures-market price discovery.

True price discovery asks how information is incorporated between **futures and spot
markets** and which market contributes more to the common efficient price. The Indian
literature of Aggarwal, Jain and Thomas and Garg et al. provides relevant applications,
while Hasbrouck's Information Share and the Gonzalo-Granger permanent-component approach
provide standard frameworks for measuring the contribution of competing markets to price
discovery.

A future extension would require sufficiently reliable historical futures and matched spot
series and would study the pre-suspension futures-spot relationship using cointegration,
VECM-based dynamics, Information Share and Component Share measures. Comparable
still-trading commodities could then provide additional evidence on how the information
environment evolved through the suspension period.

Until that analysis is executed, the current project makes no direct empirical claim about
the magnitude of futures-versus-spot price-discovery loss.

---

## 6. Summary

The Indian literature provides mixed evidence on whether agricultural-futures suspensions
stabilize underlying spot markets. The most important lesson for this project is that
uncontrolled pre/post comparisons are insufficient: treatment timing, common commodity
shocks, commodity-specific interventions and the choice of comparison markets can strongly
affect the apparent result.

The completed analysis therefore focuses on explicit counterfactual construction,
falsification and robustness. Its main finding is that the 2021 suspension is not associated
with the previously hypothesized increase in spot-price volatility; the final aggregate
estimate is a modest and statistically insignificant decline, with stronger negative
evidence concentrated in chana. Supporting analysis provides suggestive, but underpowered,
evidence of weaker post-suspension spot-market integration and efficiency.

These conclusions leave the futures-versus-spot price-discovery question open as the main
future extension rather than treating it as something already established by the completed
analysis.
