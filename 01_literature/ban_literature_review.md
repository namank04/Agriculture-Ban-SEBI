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

The 2021 suspension episode, implemented in stages from August to December, therefore
provides a useful setting for evaluating whether removing futures trading was followed by
changes in spot-price stability and in the functioning of the remaining spot markets. Because
SEBI did not publish a commodity-specific causal rationale for the intervention, the policy is
treated as an intervention to be evaluated rather than as evidence that futures trading itself
was responsible for the preceding price pressures.

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

Dey and Gairola examine chana, soybean and refined soy oil using futures and spot-price data
from the period around the suspension. Their evidence illustrates why the sign of a simple
pre/post volatility comparison is not uniform across commodities. In their five-month
annualized-volatility comparison, volatility falls after suspension for chana and soybean but
rises for refined soy oil. Other variability measures in the paper also differ across
commodities.

The study is useful for the present project because it combines evidence on speculation,
liquidity, price discovery, hedging and volatility, but does not construct the same
treated-versus-control volatility counterfactual used in H1. We therefore treat it as an
important empirical benchmark rather than as directly comparable causal evidence.

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

Merely adding a comparison group is not sufficient; the composition of that comparison group
matters.

An earlier five-donor specification based mainly on industrial and spice commodities produced
an estimated aggregate volatility decline of approximately **20.7%**. Expanding the donor pool
to the final nine commodities, including food cereals that provide a more economically relevant
comparison for the treated staples, reduced the aggregate Difference-in-Differences estimate to
approximately **10.0% lower volatility**.

The movement from roughly **−20.7% to −10.0%** is retained as an important robustness result.
It shows that the estimated magnitude is materially sensitive to the economic composition of
the counterfactual.

The final H1 evidence therefore combines:

- commodity-level Synthetic Control using the frozen nine-donor pool;
- a common-exposure Difference-in-Differences benchmark;
- in-space Synthetic-Control placebos;
- leave-one-donor-out and leave-one-treated-out sensitivity;
- treatment-month and post-horizon sensitivity;
- district-level heterogeneity; and
- placebo-date and pre-treatment diagnostics.

These are complementary diagnostics of the same research question, not independent
confirmations of one causal coefficient.

### 3.3 Identification checks are part of the result

The final diagnostic results place an important limit on causal interpretation of the pooled
Difference-in-Differences estimate.

Using genuine pre-treatment months before the earliest suspension, the joint lead test rejects
the parallel-pre-trends restriction:

\[
F(3,13), \qquad p = 0.0029.
\]

The fake-2019 placebo also produces an economically substantial estimated decline of about
**9.6%**, although it is statistically insignificant. Its magnitude is close enough to the actual
approximately **10.0%** DiD estimate to make a causal interpretation especially unsafe.

The final role of DiD is therefore as a transparent treated-versus-control benchmark, not the
primary causal estimator. Synthetic Control is given greater weight because it constructs a
commodity-specific counterfactual from the pre-treatment path, while its own limitations are
assessed through pre-fit quality, donor weights, placebo ranks and sensitivity checks.

This is also why a statistically insignificant coefficient alone is not the conclusion of H1:
the identification diagnostics, counterfactual sensitivity and commodity heterogeneity are part
of the substantive result.

### 3.4 Methodological references

The methodological literature is kept deliberately small and tied to methods actually used in
the final project.

Abadie, Diamond and Hainmueller (2010) provide the foundation for Synthetic Control. Ferman
and Pinto (2017) examine placebo-based inference for Synthetic Control and motivate caution
when interpreting finite donor-placebo distributions. Bertrand, Duflo and Mullainathan (2004)
motivate careful treatment of dependence in Difference-in-Differences, while Roth (2022)
explains why conventional pre-trend testing should not be treated as automatic validation of
parallel trends.

For H3, Lo and MacKinlay (1988) provide the variance-ratio framework used to assess departures
from a random-walk benchmark. Engle and Granger (1987) provide the cointegration and
error-correction framework underlying the pairwise mandi analysis. Ravallion (1986) is a
foundational agricultural-market application showing why spatial market integration should be
studied dynamically rather than through simple static price correlations.

## 4. Position of this project in the literature

### 4.1 Spot-price volatility

The main empirical contribution is a district-level evaluation of spot-price volatility built
from more than **7.2 million raw mandi market-day observations**.

The final common-exposure Difference-in-Differences benchmark implies approximately **10.0%
lower volatility** for the treated basket relative to controls:

\[
e^{-0.10586}-1 pprox -10.04\%.
\]

The estimate is statistically insignificant under commodity-clustered inference
(\(p=0.1235\); \(t(G-1)\) reference \(p=0.1475\)). More importantly, the corrected joint
pre-trend test strongly rejects parallel pre-trends (\(p=0.0029\)). The pooled DiD estimate is
therefore **not interpreted causally**.

Commodity-level Synthetic Control generally produces negative post-suspension gaps, but the
strength of that evidence varies materially with pre-treatment fit and placebo inference.
Chana provides the strongest suggestive negative result. Soybean has a relatively stable
negative gap but weak placebo inference. Mustard is weaker, wheat is heavily confounded by
other policy interventions and poor pre-fit, and moong is comparatively fragile.

The defensible H1 conclusion is therefore narrower than either “the suspension raised
volatility” or “the suspension reduced volatility.” The data provide **no support for the
hypothesis that the suspension increased spot volatility**. Negative estimates are common, but
the evidence is heterogeneous and does not establish a general causal volatility reduction.

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

### 4.3 Futures-market mechanisms and price discovery — H2 future extension

H2 is deliberately separated from the completed H1 and H3 analyses.

The relevant question is whether futures markets contributed to information incorporation,
reference pricing and risk management before they were suspended. Indian evidence already
suggests an informational role for commodity futures. Aggarwal, Jain and Thomas find that
Indian commodity futures contribute meaningfully to price discovery, although hedging
effectiveness is more uneven. Garg et al. provide a more recent Indian application studying
information transmission between agricultural spot and derivatives markets.

A direct extension of this project would require reliable matched historical futures and spot
series. Cointegration and a Vector Error-Correction Model would first establish the common
long-run price relationship. Price-discovery contributions could then be summarized using
standard approaches such as Hasbrouck's Information Share and the Gonzalo-Granger
permanent-component framework.

Participant-category information from SEBI bulletins may also provide institutional context on
who used the pre-suspension derivatives market. However, participant composition is **not
treated as a completed empirical result in the present project**. The available category labels
do not cleanly identify all economic hedging activity, and incomplete bulletin coverage prevents
a strong composition claim.

Accordingly, the project makes no completed H2 claim about the magnitude of price-discovery
loss, hedging loss, or participant composition. These remain data-dependent extensions rather
than results used to support H1 or H3.

## 6. Summary

The literature does not provide a simple theoretical or empirical presumption that suspending
agricultural futures should stabilize spot markets. The Indian evidence is mixed, and the most
relevant recent studies show why uncontrolled pre/post comparisons can be misleading.

The final H1 analysis therefore places counterfactual construction and identification
diagnostics at the centre of the design. The pooled DiD benchmark is approximately **−10.0%**,
but the parallel-pre-trends restriction is strongly rejected and a fake-2019 placebo is
economically large. DiD is consequently retained only as a benchmark. Commodity-level
Synthetic Control provides generally negative but heterogeneous evidence, with the strongest
suggestive result in chana. Overall, the hypothesized increase in spot volatility is **not
supported**, while a broad causal reduction in volatility is also not established.

H3 asks a separate spot-market-functioning question. Its variance-ratio and cross-mandi
integration results point in the direction of weaker post-suspension efficiency and spatial
integration, but the small commodity sample and descriptive pairwise structure require a
suggestive rather than definitive interpretation.

H2 combines the future price-discovery, hedging and participant-structure questions. It is not
a completed empirical hypothesis in the current project. Direct futures-versus-spot analysis
remains the principal extension if sufficiently reliable historical futures data become
available.
