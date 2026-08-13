# Ban-Period Literature Review (annotated)

> **STATUS NOTE (2026-07-04).** This is a planning/reference artifact, not the canonical results memo.
> Its method-selection reasoning remains useful, but any C1 numbers or "naive DiD is dead" framing in
> the body belong to earlier states of the analysis. The current food-donor rerun refutes the inherited
> "+8–10% vol rose" claim, but the aggregate estimate is only **−9.8%** and **not significant** (CR1
> p≈0.145; wild bootstrap p≈0.153). The honest result is donor sensitivity: lower volatility is
> concentrated in chana, wheat is confounded, and the full oilseed/ragi donor pull is still pending.
> Canonical truth: `04_empirics/H1_volatility/c1_findings.md` and
> `00_admin/RESUME_HERE_2026-06-21.md`.

Annotated bibliography of derivatives-suspension / futures-ban analysis, organised by episode.
Companion to `references.md` (the provenance ledger: URLs, access dates, local paths) — this file
carries the **method + finding + for-us verdict** per entry and does NOT repeat full link/path
metadata. Where a `[saved: file]` tag appears, the PDF is in `01_literature/papers/`; `[url only]`
means no archived copy (paywall/login wall — see `references.md` for the URL and **[MANUAL]** flag).

Verdict tags: **ADOPT** (use the method/data/framing), **AVOID** (design we must not replicate),
**BEWARE** (cite-and-rebut, or conflict-of-interest / scope caveat).

Sections: (1) India 2021 suspension · (2) India 2007–08 bans & 2012 guar · (3) Global / theory
precedents · (4) Methods — causal identification · (5) Methods — volatility & basis.

---

## 1. India 2021 suspension (direct competitors / complements)

**Aggarwal, Chatterjee & Sehgal (2023, rev. Aug 2025). *Trading Suspensions and Food Price Inflation.* SSRN WP 4407637.** [url only]
SCM on three episodes (chana Jun-2016, chana Aug-2021, mustard Oct-2021); donor pool of
non-suspended pulses/oilseeds; predictors = international prices, global/domestic production
shocks, net imports, mandi establishment. Finds the synthetic counterfactual tracks actual prices
in every episode — suspension neither raised nor lowered prices/inflation.
**For us: ADOPT** — the single most important methodological precedent. Their donor pool and
predictor set map directly onto our control-commodity problem and their per-episode (staggered)
treatment respects the precursor bans we currently pool into Dec-2021. **GAP WE FILL:** they study
price LEVELS/inflation; our realized-VOL (C1) and basis (C2) are the novel margins, plus the
disaggregated district panel and modern few-treated inference. Their null is the result we confirm
or overturn. (Earlier version SSRN 4261360 separately posted/cited — see below.)

**Aggarwal, Chatterjee & Sehgal (2022). *Assessing the Impact of Commodity Derivatives Suspensions.* SSRN WP 4261360.** [url only — SSRN 403s scripted fetch]
Earlier SCM agenda on chana (Aug-2021) and mustard seed (Oct-2021); counterfactual price paths from
unaffected comparison commodities. No evidence derivatives trading caused food-price inflation.
Press coverage adds: futures had ~64% price-discovery share for mustard pre-ban, which ceased with
the ban; commodities without futures face no position/margin/price limits and are likely MORE
volatile.
**For us: ADOPT** the 64% mustard discovery share as a motivating statistic for C2's basis/discovery
framing. Superseded by 4407637 but separately cited.

**Sehgal, Chatterjee & Aggarwal (2025). *Do commodity derivatives suspensions rein in food price inflation?* Ideas for India, Feb 27 2025.** [url only]
Non-technical exposition of the SCM in 4407637, with actual-vs-synthetic figures.
**For us: ADOPT** as the freely accessible figure source to sanity-check our SCM replication targets
before obtaining the full WP manually (SSRN blocks scripted access).

**Gaurav, S. & Pandey, P. (2024). *Impact of Suspension of Commodity Derivatives on the Agri Ecosystem.* NCDEX-commissioned report, SJMSOM, IIT Bombay (114 pp.).** [saved: Gaurav2024_suspension_agri_ecosystem.pdf]
Daily futures/spot/retail 2003/04–2024 for 5 of 7 banned commodities: Granger causality, speculation
ratio (OI/volume), pre/post vol at 3/6/12-month windows, **and a DiD of volatility (suspended vs
domestic+international peer commodities, Table 2.12).** Plus Maharashtra/Rajasthan/MP survey (probit /
ordered probit). Retail prices did NOT fall; naive pre/post shows vol up for all; **but their
vol DiD vs peers is NULL except soy oil (higher 12m post).**
**For us: ADOPT** their peer/donor mapping (Table 2.12), 3/6/12-month windows, Granger/speculation
evidence for C2 mechanisms. **KEY FACT:** the NULL vol DiD is consistent with our placebo-driven kill
of naive DiD; their "volatility increased" headline is uncontrolled pre/post. **AVOID** naive pre/post
vol tests. **BEWARE** NCDEX funding (flag conflict).

**Rajib, Barai & Arora (2024). *Impact on Suspension of Commodity Derivatives on Commodity Market Ecosystem.* NCDEX-funded report, BIMTECH / VGSOM IIT Kharagpur (34 pp.).** [saved: Rajib2024_suspension_market_ecosystem.pdf]
Jan-2016–Apr-2024, mustard/soybean/soy oil/mustard oil (+palm): retail-wholesale gap t-tests;
domestic vs international basis-risk F-tests; "daily volatility" = cross-mandi dispersion regressed
on a post-dummy; polled-price dispersion; FPO survey. International basis variance far exceeds
domestic (F=47.5 soybean, 56.3 soy oil). Cross-mandi dispersion of mustard seed up post-ban
(b=47.91, p<.01). **Notes volatility was already rising from Apr-2021, BEFORE the Dec-2021 ban.**
**For us: BEWARE** — their "volatility" is spatial cross-mandi dispersion, a different estimand from
our time-series RV; do not conflate. Their Fig 4.1 (vol climbing pre-ban) is documentary support for
our policy-endogeneity story. **ADOPT** cross-mandi dispersion as an auxiliary integration outcome
(directly feeds the FDCD dispersion corollary) and the domestic-vs-international basis-risk framing
for C2. **AVOID** the single-post-dummy regression with no counterfactual. NCDEX-funded.

**Dey, K. & Gairola, G. (2024). *Is Suspending Agricultural Futures Justified?* EPW 59(9), Special Articles.** [url only — EPW paywall]
Daily futures/spot for chana, soybean, refined soy oil; pre-ban futures speculation/liquidity
metrics; pre/post spot-vol comparison. Pre-ban high speculative activity; **spot vol considerably
INCREASED post-ban for chickpeas and refined soy oil.**
**For us:** the closest *published* peer-reviewed claim to our C1 (+vol post-ban) — benchmark our
commodity-level signs against theirs. **ADOPT** their speculation/liquidity metrics as a C2
treatment-intensity moderator. **AVOID** their pre/post-no-control design — the exact design our
placebo kills. This is a strong candidate for "the claim we are stress-testing."

**Dubey, P. & Dey, S. (2023). *Inflationary Effect of Agricultural Commodity Futures Market in India.* Vision (SAGE).** [url only]
AGRIDEX futures volume vs CPI (long/short run) + 12 individual commodities. AGRIDEX volume
significantly positively associated with CPI; but only 4 of 11 commodities show significant
futures-volume→spot-price effects.
**For us: BEWARE composition** — aggregate associations look inflationary while commodity-level
effects are sparse (a warning for our pooled estimates). Not a ban evaluation; volume ends pre/around
suspension. We hold the AGRIDEX methodology note.

**Sumalatha & Nirmal Roy (2023). *Agricultural Commodity Futures Market in India.* EPW 58(52), Commentary.** [url only — EPW paywall]
Review of trends since 2003 revival, recurring suspensions, low farmer participation; no original
econometrics on Dec-2021.
**For us:** lit-review value only — catalogs India's suspension history and the farmer-participation
critique for our introduction. No estimates to benchmark.

**PwC (2023). *Price Risk Management for Agricultural Commodities.* Report to NCDEX Investor Protection Fund Trust (151 pp.).** [saved: PwC2023_price-risk-management-agri.pdf]
Stakeholder interviews + secondary analysis (FIA volumes/OI 2019–21). Suspension damaged confidence;
hedgers left without domestic tools; **documents which commodities stayed tradable (castor, guar,
turmeric) vs suspended.**
**For us: ADOPT** as grey-lit confirming our control commodities stayed listed/liquid through the ban
window; stakeholder hedging-vacuum mechanism for C2. **AVOID** for magnitudes (no econometrics).
NCDEX-IPFT-funded.

**Kabi, Panda & Chari (2023). *Price Discovery in Agricultural Commodities Markets for India: A Case of Cotton.* Management and Labour Studies 48(4).** [url only]
VAR / ARDL / Granger / VECM on 13 commodities around the COVID-era trade suspension; lead-lag flip
pre/post. 5 of 13 flipped from futures-leads-spot to spot-leads-futures after the halt.
**For us:** methodology only (COVID halt, not Dec-2021). **ADOPT** the lead-lag-flip design for C2's
pre-ban discovery role; cotton results matter because MCX cotton (our contaminated control) had its
own Aug-2022–Jan-2023 halt.

**Jha, B. & Chakravarty, S. (2021). *Future Market for Agriculture Commodities in India (Final Report).* MoA&FW / Institute of Economic Growth, Jun 2021.** [saved: Jha2021_futures-market-agri-commodities.pdf]
Pre-ban government assessment: spot-futures graphical analysis, backwardation/contango, market
efficiency, causality, futures-inflation discussion, stakeholder feedback. (Authors note the
volatility objective was "compromised significantly" — lost a research assistant.)
**For us:** official pre-ban baseline showing the policy debate inside MoA&FW immediately before
suspension — supports policy-endogeneity (ban decided amid elevated 2021 inflation, not on this
study). Institutional context, not estimates. This is the **DES2022** item in `references.md`,
NOW LOCATED (desagri.gov.in; SSL fault — fetch with cert-check disabled).

**BIMTECH (Rajib et al.) (2024). *Impact on Suspension … Commodity Market Ecosystem* (7-commodity ecosystem study).** [saved: Rajib2024_suspension_market_ecosystem.pdf]
Spot/retail for all 7 banned + turnover; descriptive/event-window pre/post + FPO survey. Reports
suspension destabilized prices, worsened discovery, exacerbated inflation; **NCDEX turnover collapsed
(banned commodities were >70% of volume).**
**For us: ADOPT** the turnover-collapse fact and the qualitative "no clear reference price in the
mandis" claim (the mechanism behind the FDCD design and C2). **AVOID** its descriptive,
industry-commissioned pre/post as a template. (Same underlying report as Rajib et al. above; the
bibliography lists it twice under different lane tags.)

**Sneagen, S. (2022). *Essays on Indian Futures Markets.* PhD thesis, Univ. of Essex.** [url only]
NCDEX wheat futures around suspension episodes (Ch.2 market efficiency; Ch.4 contract size/liquidity).
**For us:** closest academic treatment of an Indian futures suspension at the contract level (wheat);
methods/data reference for the C2 futures side. Confirms the cross-commodity volatility angle is
under-explored (our niche). VERIFY which ban episode Ch.2 uses.

---

## 2. India 2007–08 bans & 2012 guar

**Sobti, N. (2020). *Does Ban on Futures trading (de)stabilise spot volatility?* South Asian J. of Business Studies 9(2).** [url only]
Wheat/sugar/soya oil/rubber/chana across pre-ban / ban / post-relaunch (2007–08 era): cointegration,
VECM, Granger, Welch ANOVA, Kruskal-Wallis, **augmented E-GARCH with ban + relaunch dummies on spot
vol.** Spot vol HIGHEST during the ban phase for most commodities (chana a partial exception);
destabilisation holds pre-ban, weakens post-relaunch.
**For us:** the direct methodological template for C2. **ADOPT** the augmented E-GARCH spec and the
three-phase design (our 2021 ban has no relaunch yet → only two phases); within-India precedent that
bans RAISE spot vol. **AVOID** its lack of a cross-commodity counterfactual (same endogeneity).

**Nath, G. C. & Lingareddy, T. (2008). *Commodity Derivative Market and its Impact on Spot Market* (SSRN 1087904) / *Impact of Futures Trading on Commodity Prices* (EPW 43(03)).** [saved: Nath2008_commodity-derivative-spot-market.pdf]
Three-regime volatility comparison (before futures / during futures / after ban) for urad, tur,
wheat (2007 delisting); WPI-based. Volatility in urad/pulses HIGHER during futures trading than
before or after; "apparently led to" higher urad prices.
**For us: BEWARE / cite-and-rebut** — the canonical pro-ban empirical citation. The exact naive
before/during/after design our placebo kills: treatment timing (both introduction and ban) selected
on the outcome. Use as the historical mirror of our 2021 endogeneity story (banned commodities ran
hot pre-2007 too, then mean-reverted; a regime comparison misreads this as a ban benefit).

**Lingareddy, T. (2008). *Expert Committee on Commodity Futures: Agreements and Disagreements.* EPW 43(34).** [url only]
Critical reading of the Sen Committee's internal disagreements/supplementary notes; futures work only
for commodities meeting selection criteria.
**For us:** best secondary source on the Sen Committee dissent; her selection-criteria argument maps
onto which 2021 commodities had viable contracts (CPO/soy vs paddy/moong) — heterogeneity hypothesis
for C1.

**Bose, S. (2008). *Commodity Futures Market in India: … Notional Multi-Commodity Indices.* Money & Finance (ICRA Bulletin); SSRN 1262742.** [saved: Bose2008_notional_multicommodity_indices.pdf]
Efficiency/information-flow tests on notional multi-commodity indices around the 2007 delistings.
Metals/energy indices efficient; agricultural indices much weaker.
**For us: ADOPT** as support that Indian agri futures were informationally weak even pre-ban — tempers
how much price-discovery loss C1 can attribute to the 2021 suspension.

**Bose, S. (2009). *The Role of Futures Market in Aggravating Commodity Price Inflation….* Money & Finance (ICRA Bulletin).** [saved: Bose2009_futures_aggravating_inflation.pdf]
Price/inflation trend analysis around futures introduction and the 2007–08 bans (full methods not
extracted). Direct response to the 2007–08 ban wave / Sen Committee.
**For us:** companion to Bose (2008); part of the contemporaneous verdict that the 2007–08 bans were
inflation politics, not evidence — feeds policy-endogeneity narrative.

**Lokare, S. M. (2007). *Commodity Derivatives and Price Risk Management: An Empirical Anecdote from India.* RBI Occasional Papers 28(2).** [saved: Lokare2007_commodity_derivatives_risk.pdf]
Cointegration of spot/futures, hedging effectiveness, basis-risk vs price-risk across commodities
(incl. later-banned), pre-2007. Cointegrated for almost all; liquidity below critical mass; basis
risk EXCEEDS price risk in cotton/gur/wheat/mustard/sugar; basis < price risk in castor/guar/pepper/tur.
**For us: ADOPT** the per-commodity basis-risk benchmarks for C2's pre-ban basis analysis (e.g.
chana/wheat vs castor/guar donors). RBI provenance gives citation weight.

**Sahi, G. S. & Raizada, G. (2006). *Commodity Futures Market Efficiency in India and Effect on Inflation.* SSRN 949161.** [url only]
Johansen cointegration on NCDEX wheat futures/spot; futures→inflation Granger tests pre Feb-2007 wheat
delisting (abstract-level).
**For us:** pre-ban wheat evidence contemporaneous with the delisting; historical-background section
and what the wheat basis looked like before a ban.

**IIM Bangalore (Naik group) (2008). *Performance of Futures Market … Wheat, Chana, Sugar, Guar seed, Urad, Tur.* FMC-commissioned.** [url only]
Basis-risk vs spot-price-risk + farmer impact for six politically sensitive commodities. Per IEG's
summary: basis risks small for guar seed and tur (below spot price risk) — hedging worked for some
banned commodities; minimal farmer participation.
**For us:** the regulator's OWN evaluation of banned commodities. Worth a manual hunt in FMC archives
(now under sebi.gov.in/sebi_data/fmcfiles/) — strong grey-lit that FMC evidence contradicted the bans.

**Mukherjee, K. N. (2011). *Impact of Futures Trading on Indian Agricultural Commodity Market.* MPRA 29290 (NIBM).** [saved: Mukherjee2011_impact_futures_indian_agri.pdf]
Daily spot/futures, 9 commodities, 2004–2010 (spans 2007/08 bans): regression, VAR, Granger, GARCH
spillover. Futures→spot vol effect negligible for most; spillover futures→spot for jeera and soy oil;
spot→futures for castor and soy oil.
**For us: ADOPT** — covers both banned (wheat, soy oil) and donor (jeera, castor, turmeric)
commodities with our C2 toolkit; use its spillover map to justify donor choices and benchmark our
GARCH(1,1) ban-dummy spec.

**Aggarwal, Jain & Thomas (2014). *Do futures markets help in price discovery and risk management for commodities in India?* IGIDR WP-2014-020.** [saved: Aggarwal2014_futures-price-discovery-india.pdf]
Information shares + hedging effectiveness post-2003, treating bans/margins as disruptions. Futures
discover information efficiently but manage risk poorly; policy interventions a cause of weak hedging.
**For us:** methodological anchor from the IGIDR school (Aggarwal later authored the leading 2021
study). Hedging-effectiveness framing supports C2's basis arm; "interventions damage risk management"
is the welfare counterpoint to C1's vol estimate.

**Sendhil, R. & Ramasundaram, P. (2014). *Performance and Relevance of Wheat Futures Market in India.* AAEA / AgEcon 174839.** [saved: Sendhil2014_wheat-futures-market-india.pdf]
Johansen cointegration (India-US, futures-spot) + GARCH on wheat across inception (2005), ban
(Feb-2007), revival (May-2009). Domestic integration strong, none with CBOT; spot vol HIGH at
inception/revival but LOW during the ban.
**For us: BEWARE** — "low vol during ban" is exactly the mean-reversion artifact our placebo exposes
(vol spiked pre-ban, triggering the ban, then calmed). **ADOPT** the India-CBOT non-integration fact
when using CBOT wheat as a control series.

**Fernandez, C. P. S. (2013). *Futures Trading in Agricultural Commodities: Effects of the Ban….* Artha J. of Social Sciences 12(4).** [saved: Fernandez2013_futures-ban-commodities-india.pdf]
Descriptive/correlation on MCX & NCDEX for seven sometime-banned commodities; pre/post correlation,
ban-inflation. Bans largely redundant; chana rose only ~2% after relisting; **wheat traded volume
collapsed after the ban was lifted (lasting liquidity damage).**
**For us:** low-grade econometrics but a tidy catalogue of pre-2013 episodes; the
wheat-liquidity-never-recovered finding previews what relisting our 7 commodities in 2027 may look
like (external-validity point).

**Chhajed, I. & Mehta, S. (2013). *Market Behavior and Price Discovery in Indian Agriculture Commodity Market.* IJSRP 3(3).** [saved: Chhajed2013_price-discovery-agri-commodity.pdf]
Granger causality on monthly spot/futures of 9 commodities, 2009–2010 (post-2008 relisting). Mostly
bidirectional causality after relisting.
**For us:** minor — evidence that price discovery re-established quickly after the 2008–09 bans ended;
relevant to interpreting basis behaviour after any 2021 commodity is relisted.

**Babshetti, V. & Basanna, P. (2019). *Impact of Commodity Futures on Inflation: Perception and Reality.* Indian J. of Research in Capital Markets 6(2).** [saved: Babshetti2019_commodity-futures-inflation.pdf]
WPI of the 2007/2008-banned commodities over 2007–2011; pre/post-ban inflation comparisons. Some
futures→spot influence, but banning did NOT curb inflation of the banned commodities.
**For us:** direct precedent with the cleanest statement of the null on the 2007–08 episodes; also a
literature-review hub (Sen Committee, Mukherjee, etc.).

**Datta, B. (2017). *Role of Commodity Futures Trading in Triggering Commodity Spot Prices … Potato.* Pacific Business Review International.** [url only]
Four-regime comparison of potato spot returns/vol (pre-futures / active / BAN May–Dec 2008 / resumed);
ANOVA + Kruskal-Wallis. NO significant change in mean or volatility across any regime.
**For us: ADOPT** the four-window per-commodity template (deflated prices + nonparametric tests) as a
C1 robustness exercise. **BEWARE** the supply confounder: potato fell post-ban due to a bumper crop.

**Gupta, A. & Varma, P. (2016). *Impact of Futures Trading on Spot Markets: … Rubber in India.* Eastern Economic Journal 42(3).** [saved: Gupta2016_futures-spot-rubber-india.pdf]
Rubber (banned May–Nov 2008): Granger between spot/futures prices and volatilities, GARCH
persistence, ECM. Stronger futures→spot flow; **spot vol is both cause AND consequence of trading
activity.**
**For us: ADOPT** — the "vol is both cause and consequence" finding is our policy-endogeneity
mechanism at market level; cite when arguing the 2021 ban responded to vol that futures partly
reflected rather than created.

**Sharma, D. K. & Malhotra, M. (2015). *Impact of futures trading on volatility of spot market — guar seed.* Agricultural Finance Review 75(3).** [url only]
Guar seed spot returns as GARCH(1,1); **futures volume/OI decomposed into expected vs unexpected,
entered in the variance equation.** Unexpected volume positively related to spot vol; authors conclude
the 2012 guar curb "was justified."
**For us:** the strongest pro-ban econometric paper in the lane and the closest cousin of C2's GARCH
design. **ADOPT** the expected/unexpected volume decomposition for our CPO (and incoming chana/wheat)
volume+OI. **BEWARE / rebut** its regime-blind inference with our placebo framework. **NB:** guar is
one of our donor commodities with its own 2012 treatment — donor-contamination check (id-413 already
flagged).

**Soni, T. K. & Singla, H. K. (2013). *A Study of the Efficiency and Unbiasedness in NCDEX: … Guar Gum.* Indian J. of Finance 7(11).** [saved: Soni2013_efficiency-unbiasedness-guar-gum.pdf]
Cointegration + ECM + GARCH-M-ECM on NCDEX guar gum around the 2012 manipulation. Guar gum futures
inefficient short and long run — over-speculation/manipulation.
**For us:** independent corroboration that the 2012 guar episode was a genuine market failure (unlike
the diffuse 2021 inflation rationale) — sharpens the manipulation-triggered vs inflation-triggered
suspension contrast; reinforces the guar-donor contamination check.

**Bandyopadhyay, Bhowmik & Rajib (2022). *Wavelet-based analysis of guar futures in India: did we kill the golden goose?* J. of Agribusiness in Developing and Emerging Economies 12(1).** [url only]
Bivariate Granger, BEKK-GARCH, wavelet MRA linking WTI, guar futures/spot, exports across the 2012
bubble/suspension. Excessive speculation spilled into spot vol and damaged guar exports (US shale
buyers switched suppliers).
**For us:** shows ban episodes have persistent real-side effects (export substitution) beyond price
moments — candidate mechanism for why our RV DiD may understate welfare effects; wavelet is an
alternative horizon-specific vol method if GARCH is fragile.

**Singh, K. / Madhyam (2012). *Excessive Speculation and Market Manipulation….* Madhyam Briefing Paper.** [saved: Singh2012_excessive-speculation-guar.pdf]
Grey-lit policy narrative of the 2012 guar spike, FMC's manipulation findings, the 27-Mar-2012
delisting. Documentary, not econometric.
**For us:** dates and institutional detail for the guar control-commodity timeline in our panel — the
one suspension with a genuine manipulation trigger.

**Gulati, Chatterjee & Hussain (2017). *Agricultural Commodity Futures: Searching for Potential Winners.* ICRIER WP 349.** [saved: Gulati2017_agri-futures-potential-winners.pdf]
Criteria-based screening for futures suitability (production, tradability, storability, MSP exposure);
documents 15 suspensions since 2003 with durations/margin chronology; suspension duration correlates
with food-basket sensitivity; flags wheat/paddy as poor futures candidates.
**For us: ADOPT** — (a) the suitability criteria as an exogenous pre-2021 justification for our
donor/control choices and for arguing wheat/paddy futures were thin pre-ban (treatment heterogeneity);
(b) the **suspension-chronology table** as the authoritative event list for the historical ban panel;
(c) the food-sensitivity scoring as a ready covariate for the regulator reaction function (RF-SC
design). Same Chatterjee as the SCM papers; distinct from ICRIER WP383 already held.

**Chatterjee, Raghunathan & Gulati (2019). *Linking Farmers to Futures Market in India.* ICRIER WP 383.** [saved: icrier_wp383_gulati_farmers_futures.pdf]
FPO participation channels into agri-futures; barriers (lot size, trust, middlemen). Small/marginal
farmers do not trade directly; FPO aggregation is the feasible link.
**For us:** the farmer/FPO exposure channel that both NCDEX-funded reports later surveyed post-ban.
(Already in hand; `references.md` ICRIER383 — verify exact title on read.)

**Sahoo, P. & Kumar, R. (2009). *Efficiency and Futures Trading-Price Nexus in Indian Commodity Futures Markets.* Global Business Review 10(2).** [url only]
Efficiency + futures-inflation tests for five commodities incl. chana and soy oil (both banned
May-2008). Markets efficient; no sufficient evidence futures raise inflation.
**For us:** peer-reviewed counter-evidence on chana and soy oil specifically (two treated commodities)
from the prior ban round — quotable that futures→inflation causality was never established for these.

**Kumar, Brajesh (2009). *Effect of Futures Trading on Spot Market Volatility.* SSRN 1364231 (IIMA).** [url only]
VAR lead-lag between spot vol, futures volume, OI across agri/metals/energy; Granger, variance
decomposition, IRFs (abstract-level).
**For us:** methodological sibling of Sharma-Malhotra for C2's volume/OI channel on our CPO
contract-level data (the one banned commodity with volume+OI in hand).

**Singh, M. & Goyal, A. (2011). *Impact of trading in the commodity futures market on inflation.* Elixir Management 31.** [url only]
Granger between spot/futures for sugar, urad, chana, wheat. Futures→spot only for sugar and urad;
spot→futures for urad/chana/wheat/sugar; no conclusive futures-inflation link.
**For us:** minor corroborating null; the spot→futures dominance is consistent with our endogeneity
story (spot conditions drive derivative activity and policy, not the reverse).

**UNCTAD Study Group (2009). *Development Impacts of Commodity Exchanges in Emerging Markets.* UNCTAD/DITC/COM/2008/9.** [saved: UNCTAD2009_commodity-exchanges-emerging-markets.pdf]
Comparative impact evaluation of agri exchanges (Brazil/China/India/Malaysia/South Africa); India
chapters on MCX/NCDEX post-2007-ban policy environment.
**For us:** international assessment bracketing the 2007–08 bans; framing for regulatory-uncertainty
costs in the introduction.

---

## 3. Global / theory precedents (the US onion experiment, financialization, storage theory)

**Working, H. (1960). *Price Effects of Futures Trading.* Food Research Institute Studies 1(1).** [saved: Working1960_price_effects_futures_trading.pdf]
Pre/post cash-price variability with vs without futures (US onions et al.); descriptive variance.
Futures trading associated with REDUCED cash-price variability.
**For us: ADOPT** as the framing precedent — the canonical "removing futures raises spot vol" natural
experiment. **AVOID** the naive pre/post variance design (they did not face our selection problem; we do).

**Gray, R. W. (1963). *Onions Revisited.* J. of Farm Economics 45(2).** [url only]
Re-examines onion cash-price variability before vs after the 1958 US onion futures ban. Variability
generally HIGHER in years without futures.
**For us: ADOPT** as the cleanest historical "futures removed by law" analogue to the 2021 SEBI ban;
note its limit (single commodity, no formal counterfactual) that our multi-commodity design improves on.

**Cox, C. C. (1976). *Futures Trading and Market Information.* J. of Political Economy 84(6).** [url only]
Model linking spot-price behaviour to information; tests futures' information effect across six
commodities. Futures trading increases the information content of spot prices; removal degrades
discovery.
**For us: ADOPT** the information/price-discovery angle for the C2 basis/discovery narrative and the
FDCD "reverse telegraph" mechanism (third leg of the onion trilogy).

**Irwin, S. & Sanders, D. (2011). *Index Funds, Financialization, and Commodity Futures Markets.* AEPP 33(1).** [url only]
Survey + critique of CFTC index-trader positions vs futures price levels. No systematic
financialization-drives-prices evidence.
**For us:** framing — the pro-ban premise (speculation inflates prices/vol) is contested in canonical
US work. **ADOPT** the skeptical prior; **AVOID** their price-LEVEL focus (our outcome is vol).

**Irwin, S. & Sanders, D. (2012). *Testing the Masters Hypothesis in Commodity Futures Markets.* Energy Economics 34(1).** [url only]
Fama-MacBeth + Granger + long-horizon regressions of returns AND volatility on index positions. Very
little evidence index positions influence returns or volatility.
**For us:** on the volatility margin (closer to C1 than the 2011 paper). **ADOPT** the explicit
returns-vs-volatility distinction; note it is a futures-internal test, not a futures-removal
experiment like ours.

**Tang, K. & Xiong, W. (2012). *Index Investment and the Financialization of Commodities.* FAJ 68(6) / NBER 16385.** [saved: TangXiong2012_index_investment_financialization.pdf]
Rolling correlation of non-energy futures with oil; index-membership as treatment. Post-2004 index
commodities more correlated with oil, larger vol increase around 2008.
**For us:** the "financialization DOES matter" counterweight. **ADOPT** the membership-as-treatment
framing for control-commodity selection logic; **BEWARE** over-reading correlation as causal.

**Cheng, I.-H. & Xiong, W. (2014). *Financialization of Commodity Markets.* Annu. Rev. Financial Economics 6.** [saved: ChengXiong2014_financialization_commodity_markets.pdf]
Survey through risk-sharing vs information-discovery channels. Mixed evidence; effects via risk
sharing and information, not simple speculation-inflates-prices.
**For us: ADOPT** as the conceptual frame for "what does removing futures do to information discovery /
basis"; articulates why naive correlation/DiD on these markets is hazardous — supports our
policy-endogeneity diagnosis.

**Danthine, J.-P. (1978). *Information, Futures Prices, and Stabilizing Speculation.* J. of Economic Theory 17(1).** [url only]
Rational-expectations theory: futures provide forecasts guiding production/storage, generally
INCREASING spot stability.
**For us: ADOPT** as the pro-stabilization null (ban should RAISE vol). Pair with Turnovsky/Newbery
for the destabilization side — theory is explicitly inconclusive, which is why the empirics matter.

**Turnovsky, S. (1979). *Futures Markets, Private Storage, and Price Stabilization* / Newbery, D. (1987). *When Do Futures Destabilize Spot Prices?*** [saved: Newbery1987_when_futures_destabilize_spot.pdf]
Equilibrium storage models where futures can either stabilize or destabilize spot depending on
parameters. No unconditional result — the sign is empirical.
**For us: ADOPT** as the destabilization-side counterweight and the honest framing for C1/C2: theory
cannot settle the +8–10% claim — only endogeneity-robust data can.

**Working, H. (1949). *The Theory of Price of Storage.* AER 39(6).** [url only]
Supply-of-storage curve relating basis (price of storage) to stocks; negative basis signals scarcity.
**For us: ADOPT** as the theory governing the PRE-BAN basis trend in C2 — a falling/inverting basis
means tightening stocks, the same fundamental tightness that plausibly triggered the ban (endogeneity
story). **BEWARE:** basis dies with futures, so it is intrinsically pre-ban-only (C2's internal-
inconsistency catch — any "post-ban basis" claim is incoherent).

**Fama, E. & French, K. (1987). *Commodity Futures Prices: … Theory of Storage.* J. of Business 60(1).** [url only]
Indirect test via basis: basis varies with interest rates and seasonal convenience yield; decomposes
basis into premium + forecast.
**For us: ADOPT** as the empirical template for the pre-ban basis figure — regress basis on an
interest-rate proxy + harvest/seasonal dummies to separate carry from convenience yield.

**Garbade, K. & Silber, W. (1983). *Price Movements and Price Discovery in Futures and Cash Markets.* REStat 65(2).** [url only]
Structural model of cash-futures dynamics; relative speed/dominance + arbitrage elasticity. Futures
typically lead cash; degree depends on arbitrage/carry costs.
**For us: ADOPT** as the foundational lead-lag/discovery model (pre-Hasbrouck) framing the basis as
the arbitrage-linked spread — bridges C2's discovery and basis arms and grounds the FDCD reference-
price mechanism.

**Ederington, L. (1979). *The Hedging Performance of the New Futures Markets.* J. of Finance 34(1).** [saved: Ederington1979_hedging_performance_futures.pdf]
Minimum-variance hedge ratio + hedging effectiveness = proportional variance reduction.
**For us: ADOPT** for the COST-ARM (always two-armed): pre-ban hedging effectiveness for banned
commodities = the risk-reduction the ban forfeited for hedgers. Pre-ban-only by construction.

---

## 4. Methods — causal identification

### 4a. Synthetic-control family (the C1 workhorse)
**Abadie, Diamond & Hainmueller (2010). *Synthetic Control Methods ….* JASA 105(490).** [saved: AbadieDiamondHainmueller2010_synthetic_control_tobacco.pdf]
Convex, sum-to-one donor weights matching the treated unit's pre-treatment path + predictors;
placebo (permutation) inference.
**For us: ADOPT** as the C1 workhorse replacing dead TWFE-DiD. SCM does NOT require parallel trends
and absorbs the 2021 run-up by matching the actual pre-ban path. **BEWARE** (Abadie 2021): a single
transitory pre-treatment spike can be mechanically matched — pair with a long pre-period and
no-anticipation checks; exclude cotton post-Aug-2022.

**Abadie (2021). *Using Synthetic Controls: Feasibility, Data Requirements, Methodological Aspects.* JEL 59(2).** [saved: Abadie2021_using_synthetic_controls.pdf]
The conditions/guidance paper. Reliable SCM needs: good pre-fit over substantial pre-periods, treated
inside donor convex hull, NO large idiosyncratic shock just before treatment, no anticipation, clean
donors.
**For us: ADOPT** as the C1 pre-registration checklist. RED FLAG on point: our banned commodities ran
hot ~12 months pre-ban then mean-reverted — use the full 2017–2021 window, report donor weights /
pre-RMSPE, run backdating validation, drop contaminated donors.

**Abadie & Vives-i-Bastida (2022). *Synthetic Controls in Action.* arXiv 2203.06279.** [saved: Abadie2022_synthetic_controls_in_action.pdf]
Seven practical principles; explicitly warns HIGH-volatility outcomes invite overfitting and demand
longer pre-periods + validation.
**For us: ADOPT** as the SCM operating manual — we model volatility itself (a noisy target), so use the
full pre-window, leave-one-out donor validation, backdated placebo-in-time tests.

**Ben-Michael, Feller & Rothstein (2021). *The Augmented Synthetic Control Method.* JASA 116(536).** [saved: BenMichael2021_augmented_synthetic_control.pdf]
ASCM: fit an outcome model (default ridge) to estimate/subtract bias from imperfect pre-fit; allows
penalized extrapolation; multiple treated units (augsynth).
**For us: ADOPT** as the primary C1 robustness estimator — our setting is "imperfect pre-fit likely."
Supports our 7 treated commodities; SCM-vs-ASCM divergence is itself an extrapolation diagnostic.

**Arkhangelsky et al. (2021). *Synthetic Difference-in-Differences.* AER 111(12).** [saved: Arkhangelsky2021_synthetic_diff_in_diff.pdf]
SDID: SCM unit weights + time weights + DiD double-differencing; down-weights donors/periods unlike
the treated.
**For us: ADOPT** as a co-equal C1 estimator — SDID's time-weighting discounts the anomalous 2021
pre-ban periods. **BEWARE:** jackknife SE unreliable with very few treated — pair with conformal /
Conley-Taber, not default SE.

**Xu (2017). *Generalized Synthetic Control Method.* Political Analysis 25(1).** [saved: Xu2017_generalized_synthetic_control.pdf]
gsynth: interactive-fixed-effects model on controls, impute treated counterfactuals from latent
factors; multiple treated, CV on #factors.
**For us: ADOPT** as a model-based C1 alternative letting the ban correlate with latent food-inflation
factors. **BEWARE:** bootstrap shaky with tiny control N — triangulation, not sole inference.

**Athey et al. (2021). *Matrix Completion Methods for Causal Panel Data.* JASA 116(536).** [saved: Athey2021_matrix_completion_causal_panel.pdf]
MC-NNM: untreated outcomes as low-rank matrix; impute treated cells via nuclear-norm regularization;
nests SCM and IFE.
**For us: ADOPT** as a robustness check that nests our other estimators and degrades gracefully with
few units; convergence of SCM/SDID/gsynth/MC is our main C1 credibility argument.

**Abadie & L'Hour (2021). *A Penalized Synthetic Control Estimator for Disaggregated Data.* JASA 116(536).** [saved: AbadieLHour2021_penalized_synthetic_control.pdf]
pensynth: penalty on pairwise discrepancies → each treated unit draws on individually-similar donors;
unique weights for many-treated settings.
**For us: ADOPT IF** we run C1 at the DISTRICT level — our 131k commodity-district-month panel turns 7
treated commodities into hundreds of treated commodity-districts, multiplying effective clusters. Our
path out of the "only 7 treated" trap.

**Bai (2009). *Panel Data Models With Interactive Fixed Effects.* Econometrica 77(4).** [saved: Bai2009_panel_interactive_fixed_effects.pdf]
IFE estimator y_it = x_it'b + lambda_i'f_t + e_it; large-N large-T.
**For us: ADOPT** as the formal justification under gsynth/MC ("ban unconfounded conditional on latent
food-price factors"); theoretical anchor, not standalone estimator. **Also central to the DCBD-GARCH
loading-homogeneity repair (interactive-FE residualisation when district factor loadings differ).**

**Doudchenko & Imbens (2016). *Balancing, Regression, DiD and Synthetic Control Methods: A Synthesis.* NBER 22791.** [saved: Doudchenko2016_balancing_regression_did_scm.pdf]
Writes SCM/DiD/regression as one class; relaxing sum-to-one/non-negativity (elastic-net SC) improves
fit but reintroduces extrapolation.
**For us: ADOPT** as the conceptual backbone for the C1 robustness grid (DiD ↔ demeaned-SC ↔
elastic-net SC ↔ SDID) — show the estimate's path across restriction choices.

### 4b. SCM inference & few-treated / few-cluster inference
**Cattaneo, Feng & Titiunik (2021). *Prediction Intervals for Synthetic Control Methods.* JASA 116(536) [scpi software].** [saved: Cattaneo2021_prediction_intervals_synthetic.pdf]
Model-based prediction intervals decomposing in-sample + out-of-sample error; multiple treated +
staggered; software scpi (R/Python/Stata).
**For us: ADOPT** as the PRIMARY SCM inference engine for C1 (over raw placebo plots). Quantifies
uncertainty for 7 treated commodities jointly, implemented in Python (our stack).

**Chernozhukov, Wüthrich & Zhu (2021). *An Exact and Robust Conformal Inference Method ….* JASA 116(536).** [saved: Chernozhukov2021_conformal_inference_synthetic.pdf]
Conformal/permutation on residuals; valid for SCM/DiD/factor/MC under approximate exchangeability/
stationarity; survives a SINGLE treated unit and date.
**For us: ADOPT** as the lead inference method treating each banned commodity as its own time series —
solves the "one date, 7 treated, 4 controls" crisis. **BEWARE:** block-permute respecting the crop
year; both novel designs' audits flag that strong serial dependence + a large post/total ratio make
this anti-conservative — keep blocks crop-year-aligned, prewhiten, prefer the short (h∈[1,6]) horizon.

**Conley & Taber (2011). *Inference with DiD with a Small Number of Policy Changes.* REStat 93(1).** [saved: ConleyTaber2011_did_small_policy_changes.pdf]
Estimate the estimator's null distribution from the empirical residual distribution among many
NON-treated groups; few treated, many controls.
**For us: ADOPT** for C1 inference at the disaggregated (commodity-district) level where controls are
plentiful. **BEWARE:** assumes treated-group errors are drawn from the control distribution — the
exact exchangeability our audits flag as weak (staples vs spices); use within-stratum versions.

**MacKinnon & Webb (2018). *The Wild Bootstrap for Few (Treated) Clusters.* Econometrics Journal 21(2).** [saved: MacKinnonWebb2018_wild_bootstrap_few_clusters.pdf]
WCB under-/over-rejects with few treated clusters; subcluster variant partial rescue. (The
studentized-RI lineage is MacKinnon-Webb 2020, J. Econometrics.)
**For us: ADOPT** as the honest-inference benchmark — tells us the existing p=.029 DiD SE are
untrustworthy on cluster grounds ALONE, independent of the placebo failure. Motivates conformal /
Conley-Taber / Ibragimov-Müller instead.

**Ibragimov & Müller (2010). *t-Statistic Based Correlation and Heterogeneity Robust Inference.* JBES 28(4).** [url only]
Partition into q≥2 groups, estimate per group, run a t-test on group estimates; valid with ~2–11
heterogeneous correlated clusters.
**For us: ADOPT** as a primary small-cluster inference method for C1 (7 treated / ~4 control
commodities); standard cluster-robust SE are unreliable below ~30 clusters. Report alongside WCB.

**Ferman & Pinto (2017). *Synthetic Control and Inference.* Econometrics 5(4):52.** [saved: FermanPinto2017_synthetic_control_inference.pdf]
Raw gap-plot placebos mislead (donors differ in pre-fit); recommends the post/pre RMSPE-ratio
statistic; few-donor power fragile.
**For us: AVOID** naive gap-plot placebo inference; **ADOPT** the RMSPE-ratio statistic — the guardrail
against resurrecting a spurious +8–10% claim from one picture.

**Ferman & Pinto (2021). *Synthetic Controls with Imperfect Pretreatment Fit.* Quantitative Economics 12(4).** [saved: FermanPinto2021_imperfect_pretreatment_fit.pdf]
Theory under imperfect pre-fit: standard SC is BIASED if treatment correlates with unobserved
confounders even as pre-periods grow; proposes a DEMEANED SC + specification test.
**For us: CRITICAL caution** — the single most on-point paper for our endogeneity worry. **ADOPT** the
demeaned-SC variant + spec test; **AVOID** claiming SCM is automatically immune. Frame: SC reduces but
does not eliminate selection bias → triangulate (SDID/gsynth/MC) + report sensitivity (Rambachan-Roth).

**Firpo & Possebom (2018). *Synthetic Control Method: Inference, Sensitivity Analysis and Confidence Sets.* J. Causal Inference 6(2).** [url only]
Generalized permutation with a parametric weight family → sensitivity of the placebo p-value to the
weighting scheme; confidence sets by inverting a modified RMSPE statistic.
**For us: ADOPT** to report confidence sets + a sensitivity curve rather than a single placebo
p-value, pre-empting "is significance an artifact of donor weighting?"

### 4c. DiD: parallel-trends credibility, staggering, the endogeneity diagnosis
**Rambachan & Roth (2023). *A More Credible Approach to Parallel Trends.* REStud 90(5).** [saved: RambachanRoth2023_credible_parallel_trends.pdf]
Honest DiD: bound post-treatment trend violations by observed pre-treatment magnitude (M / M̄
restrictions), robust confidence sets (HonestDiD).
**For us: ADOPT** as MANDATORY sensitivity reporting given our binned joint lead test REJECTED
(p=.033) — states how much trend-violation overturns an effect, turning the pre-trend failure into a
quantified caveat. Also applies to the C2 BASIS pre-ban trend.

**Roth (2022). *Pretest with Caution….* AER:Insights 4(3).** [saved: Roth2022_pretest_with_caution.pdf]
Pre-trend tests have LOW power; conditioning on "passing" induces pretest bias.
**For us: ADOPT** as the rationale for NOT resurrecting any estimator merely because it passes a
pre-trend/pre-fit check, and for NOT cherry-picking the donor pool until pre-trends look flat (that IS
pretest bias). Justifies the pre-registered "naive DiD is dead."

**Roth, Sant'Anna, Bilinski & Poe (2023). *What's Trending in Difference-in-Differences?* J. Econometrics 235(2).** [saved: Roth2023_whats_trending_did.pdf]
Synthesis of modern DiD; decision tree. For a SINGLE adoption date with no staggering, staggered-DiD
machinery is moot; binding issues = parallel-trends credibility (Honest DiD) + few-cluster inference.
**For us: ADOPT** as the framing reference explaining why staggered estimators don't apply and
redirecting to SCM + Honest-DiD + few-cluster inference — pre-empts "why not Callaway-Sant'Anna?"

**Callaway & Sant'Anna (2021). *Difference-in-Differences with Multiple Time Periods.* J. Econometrics 225(2).** [saved: CallawaySantAnna2021_did_multiple_periods.pdf]
Group-time ATT(g,t) with not-yet-/never-treated comparisons; conditional parallel trends.
**For us: ADOPT** for the within-episode staggered design (chana Aug, mustard Oct, five Dec) — later-
treated commodities as not-yet-treated controls, aggregated to a clean event study (a route the field
has NOT exploited). Pair with placebo tests since few clusters limit inference.

**Sun & Abraham (2021). *Estimating Dynamic Treatment Effects … Heterogeneous Treatment Effects.* J. Econometrics 225(2).** [saved: SunAbraham2021_event_study_heterogeneous.pdf]
Interaction-weighted event-study estimator; clean leads/lags under heterogeneity.
**For us: ADOPT** as the primary dynamic specification — makes our binned-lead pre-trend test
(rejecting p=.033) interpretation-proof against TWFE contamination.

**de Chaisemartin & D'Haultfœuille (2020). *Two-Way Fixed Effects Estimators with Heterogeneous Treatment Effects.* AER 110(9).** [saved: deChaisemartinDHaultfoeuille2020_twfe_heterogeneous.pdf]
TWFE = weighted sum of ATEs with possibly-negative weights; DID_M estimator; negative-weight
diagnostic.
**For us: ADOPT** the twowayfeweights diagnostic as a robustness exhibit (3 staggered cohorts → the
negative-weighting critique applies); DID_M alongside Callaway-Sant'Anna. **Also relevant prior art
for the bundled-policy / compound-treatment problem the RF-SC audit raised** (export bans + stock
limits as contaminating co-treatments).

**Goodman-Bacon (2021). *Difference-in-Differences with Variation in Treatment Timing.* J. Econometrics 225(2).** [saved: GoodmanBacon2021_did_variation_timing.pdf]
Decomposes TWFE into all 2×2 comparisons with variance weights; isolates "already-treated as control"
bad comparisons.
**For us: ADOPT** bacondecomp as a transparency exhibit on our Aug/Oct/Dec staggering — shows how much
of −16.4% comes from clean vs already-treated comparisons.

### 4d. The Ashenfelter / selection-on-transitory-shock lineage (why our DiD died)
**Ashenfelter (1978). *Estimating the Effect of Training Programs on Earnings.* REStat 60(1).** [url only]
The original "Ashenfelter's dip": selection into treatment correlated with a transitory pre-treatment
dip biases before-after / DiD.
**For us: ADOPT** the dip framing — banned commodities were selected BECAUSE 2021 vol/inflation ran hot
("reverse Ashenfelter bump"), then mean-reverted. Names the mechanism behind our placebo-2019 failure
(−13.6%, p=.046).

**Chabé-Ferret (2015). *Analysis of the Bias of Matching and DiD under Alternative Earnings and Selection Processes.* J. Econometrics 185(1).** [url only]
Analytical bias + Monte Carlo: selection on a transitory (mean-reverting) shock biases DiD;
symmetric-DiD reduces bias.
**For us:** the FORMAL result our placebo-2019 finding instantiates — the single most load-bearing
methodology cite for "naive DiD is dead by pre-registered rules." **ADOPT** symmetric-DiD / long-window
remedies as a candidate C1 fix.

**Heckman, Ichimura, Smith & Todd (1998). *Characterizing Selection Bias Using Experimental Data.* Econometrica 66(5).** [saved: HeckmanIchimuraSmithTodd1998_selection_bias.pdf]
Decomposes selection bias; semiparametric DiD removes time-invariant bias best (bias = stable level
difference + a dip).
**For us: ADOPT** the bias-decomposition language — shows which part of selection bias DiD CAN remove
(time-invariant) vs cannot (the transitory dip).

**Malani & Reif (2015). *Interpreting Pre-Trends as Anticipation….* J. Public Economics 124.** [saved: MalaniReif2015_pretrends_anticipation.pdf]
Distinguishes endogeneity from anticipation as sources of pre-trends; IV for expectations.
**For us: ADOPT** — pre-Dec-2021 position-limit curbs + press anticipation mean part of our pre-trend
could be anticipation, not pure selection. Must argue WHICH drives it (different corrections).
Complements Ashenfelter/Chabé-Ferret.

**Bertrand, Duflo & Mullainathan (2004). *How Much Should We Trust Differences-in-Differences Estimates?* QJE 119(1).** [saved: BertrandDufloMullainathan2004_trust_did.pdf]
Placebo-law Monte Carlo: serially-correlated outcomes inflate DiD significance (up to 45% spurious at
5%); remedies = block bootstrap, cluster, collapse-to-pre/post.
**For us: ESSENTIAL** given our serially-correlated monthly RV panel and 11 clusters — our p-values
(.029, .046, .033) must be hardened. **ADOPT** collapse-to-two-periods + cluster-robust; pairs with
Ibragimov-Müller. Even the significant −16.4% is fragile under proper inference.

### 4e. Other estimators considered
**Athey & Imbens (2006). *Identification and Inference in Nonlinear Difference-in-Differences Models* (Changes-in-Changes).* Econometrica 74(2).** [saved: AtheyImbens2006_changes_in_changes.pdf]
CIC: nonparametric DiD recovering the entire counterfactual DISTRIBUTION; scale-invariant (log vs
level).
**For us: ADOPT** as a distributional robustness check — whether the ban shifted the whole vol
distribution or just the mean, removing the log-transform scale-dependence. Secondary to SCM-family.

**Brodersen et al. (2015). *Inferring Causal Impact Using Bayesian Structural Time-Series Models* (CausalImpact).* Annals of Applied Statistics 9(1).** [saved: Brodersen2015_causal_impact_bsts.pdf]
BSTS counterfactual: local trend + seasonality + spike-and-slab-selected controls; pointwise +
cumulative impact with credible intervals.
**For us: ADOPT** as a per-commodity C1 cross-check with built-in seasonality (our monthly mandi vol is
strongly seasonal, which SCM does not model). Spike-and-slab picks donors data-drivenly. **BEWARE:**
exclude post-Aug-2022 cotton and any ban-responsive covariate.

**Casini & McCloskey (2024). *Identification and Estimation of Causal Effects in High-Frequency Event Studies.* arXiv 2406.15667.** [saved: Casini2024_high_frequency_event_studies.pdf]
Event-study estimates can be causal despite reverse causality IF the policy-surprise variance
dominates a tight window.
**For us: MOSTLY AVOID** for monthly-vol C1 — our ban was endogenous and pre-figured by months of
inflation (no sharp surprise, no high-frequency window). Cite to explain WHY a naive announcement
event-study is inappropriate and to motivate the counterfactual route.

**Alvarez, Ferman & Wüthrich (2025). *Inference with Few Treated Units.* arXiv 2504.19841.** [saved: Alvarez2025_inference_few_treated_units.pdf]
Survey of few-treated inference (Conley-Taber, Ferman-Pinto, wild/permutation bootstrap, SCM
permutation, conformal), organized by exogenous vs endogenous timing.
**For us: ADOPT** as the single best roadmap for the C1 inference section — written for exactly our
problem (few treated, one date, endogenous timing). No free lunch: every valid method buys validity
with a homogeneity/exchangeability assumption; standard cluster-robust + naive WCB FAIL. Use to
justify the conformal + Conley-Taber + scpi triangulation and state which assumption underwrites each CI.

---

## 5. Methods — volatility & basis (C2)

### 5a. The structural-break / persistence-bias warning (against naive pre/post GARCH)
**Hillebrand (2005). *Neglecting parameter changes in GARCH models.* J. Econometrics 129(1–2).** [url only]
Failing to model unconditional-variance breaks imparts a large UPWARD bias to estimated GARCH
persistence (α+β → 1); spurious near-integration.
**For us: ADOPT** as the CENTRAL caveat for C2 — our core test is a pre vs post persistence comparison
of GARCH(1,1)+ban-dummy; a single unmodelled ban-date level shift inflates persistence and masquerades
as a persistence change. Mandatory: estimate persistence on within-regime / ICSS-cleaned windows
first. **This is the named flaw the DCBD-GARCH novel design is built to defeat.**

**Lamoureux & Lastrapes (1990). *Persistence in Variance, Structural Change, and the GARCH Model.* JBES 8(2).** [url only]
Data + Monte Carlo: persistence overstated when deterministic variance shifts ignored; break dummies
sharply reduce it (sometimes to near zero).
**For us: ADOPT** as the operational predecessor to Hillebrand and direct justification for our
ICSS-then-GARCH workflow.

**Inclán & Tiao (1994). *Use of Cumulative Sums of Squares for Retrospective Detection of Changes of Variance.* JASA 89(427).** [url only]
ICSS algorithm to date MULTIPLE unconditional-variance breakpoints (CRAN ICSS).
**For us: ADOPT** as the break-dating engine for C2 (~1,250 daily obs/commodity 2017–21 → power). Use
to test whether a variance break sits AT Dec-2021 vs elsewhere (endogeneity diagnostic mirroring the
placebo) and to supply within-regime windows for Hillebrand-robust persistence. **CAVEAT:** pre-whiten
(AR/seasonal) first or it over-detects under ARCH.

**Hasanov, Frankel & Mostarac (2024). *Structural breaks and GARCH models of exchange rate volatility.* J. Applied Econometrics 39(7).** [url only]
Re-examines/extends ICSS-then-GARCH; break-augmented GARCH outperforms break-ignorant across loss
functions/horizons.
**For us: ADOPT** as the current-best-practice anchor showing ICSS→GARCH is live — single cite to
pre-empt "why not plain GARCH with a dummy."

**Lama, Jha, Paul & Gurung (2021). *Modeling Agricultural Commodity Price Volatility using GARCH Model with Structural Break.* (grey-lit; venue unconfirmed, 403-blocked).** [url only]
GARCH-family vol for ag commodities with explicit structural-break handling (per title; full text not
retrieved).
**For us: TO-FETCH** (institutional/browser) — the exact GARCH+break template on ag data to read
before locking C2. **AVOID as evidence** until full text confirmed.

### 5b. Asymmetric / regime / realized-vol models
**Nelson (1991). *Conditional Heteroskedasticity in Asset Returns* (EGARCH).* Econometrica 59(2).** [saved: Nelson1991_egarch_conditional_heteroskedasticity.pdf]
EGARCH models log conditional variance (positivity automatic), separates sign and size effects.
**For us: ADOPT** EGARCH (and/or GJR) as the asymmetry-robust C2 spec (Sobti 2020 precedent). For ag
SPOT, asymmetry may INVERT (shortages push price+vol up) — the asymmetry sign is itself a result.

**Glosten, Jagannathan & Runkle (1993). *On the Relation between the Expected Value and the Volatility … (GJR-GARCH).* J. of Finance 48(5).** [saved: Glosten1993_gjr_garch_expected_volatility.pdf]
GARCH + a negative-shock-indicator term for asymmetric variance response.
**For us: ADOPT** as the simplest asymmetry spec alongside EGARCH (cheaper, nests symmetric GARCH via
γ=0, easy LR test). Run both; report spec-robustness of the asymmetry conclusion.

**Haas, Mittnik & Paolella (2004). *A New Approach to Markov-Switching GARCH Models.* J. Financial Econometrics 2(4).** [url only]
K separate GARCH processes per Markov state, avoiding path dependence (MSGARCH).
**For us: CONSIDER** as a robustness alternative to a hard-coded ban dummy — let data choose high/low-
vol regimes and ask whether regime probabilities shift at Dec-2021 (addresses the hot-then-revert
endogeneity worry). Secondary/robustness; single date + few regimes limit identification; mandi-median
composition noise can spuriously trigger switches.

**Corsi (2009). *A Simple Approximate Long-Memory Model of Realized Volatility* (HAR-RV).* J. Financial Econometrics 7(2).** [saved: Corsi2009_har_rv_long_memory.pdf]
Additive daily/weekly/monthly RV cascade → simple AR; needs a realized-vol dependent variable.
**For us:** limited fit as conceived (HAR needs intraday RV; daily mandi gives only daily returns) BUT
our monthly RV panel is RV-from-daily-within-month → a MONTHLY HAR-style decomposition is feasible and
lets the ban dummy enter a realized-vol regression rather than a latent GARCH (cleaner). **ADOPT in
modified monthly form.** **CAVEAT:** control for n-mandis-reporting (composition noise inflates RV
non-classically).

**Barndorff-Nielsen & Shephard (2004). *Power and Bipower Variation with Stochastic Volatility and Jumps.* J. Financial Econometrics 2(1).** [saved: BarndorffNielsen2004_power_bipower_variation.pdf]
Realized bipower variation separates the continuous part of QV from jumps (model-free jump test) —
an intraday construct.
**For us: POOR FIT** at intended granularity (daily mandi cannot support bipower); **AVOID** claiming
jump-robust RV. The IDEA matters (ag spot has genuine jumps from shortages/policy/MSP) — address jumps
via robust/quantile vol measures + outlier flags (cf. guar id-75), NOT bipower. Theoretical motivation
only.

### 5c. Price discovery, basis & spillover (C2 satellites)
**Hasbrouck (1995). *One Security, Many Markets: … Contributions to Price Discovery* (Information Share).* J. of Finance 50(4).** [saved: Hasbrouck1995_information_share_price_discovery.pdf]
VECM on cointegrated prices; information share = each market's share of innovation variance; bounds
when innovations correlated.
**For us: ADOPT** for the PRE-BAN futures-spot discovery share (only computable pre-Dec-2021 since
banned futures die then — a clean asymmetry, not a flaw). The magnitude whose loss C2 is about.
**CAVEAT:** bounds widen with daily sampling + high contemporaneous correlation — report bounds, pair
with Gonzalo-Granger.

**Gonzalo & Granger (1995). *Estimation of Common Long-Memory Components in Cointegrated Systems.* JBES 13(1).** [saved: Gonzalo1995_common_long_memory_cointegrated.pdf]
Permanent-transitory decomposition; the market that adjusts LESS contributes MORE to the common factor.
**For us: ADOPT** alongside Hasbrouck as the standard twin (report both; divergence is informative).
Less sensitive to the daily-sampling correlation problem, so more robust on daily mandi data.

**Baillie, Booth, Tse & Zabotina (2002). *Price Discovery and Common Factor Models.* J. of Financial Markets 5(3).** [url only]
Compares Hasbrouck information-share vs Gonzalo-Granger permanent-transitory; relates via innovation
variance.
**For us: ADOPT** the paired reporting as the canonical price-discovery exhibit reviewers expect, on
pre-ban CPO (and forthcoming chana/wheat) futures-spot pairs.

**Inani, S. K. (2018). *Price Discovery and Efficiency of Indian Agricultural Commodity Futures Market.* J. of Quantitative Economics 16(1).** [url only]
Component share (Gonzalo-Granger) + information share (Hasbrouck) + modified info share (Lien-Shrestha)
on 10 NCDEX agri commodities incl. chana, mustard, castor, turmeric, guar, jeera. Futures lead spot in
6 of 10.
**For us: ADOPT** as the direct Indian-agri template for our pre-ban discovery-share calculation — it
covers our treated AND donor commodities; borrow its 3-method reporting format. Lien-Shrestha reconciles
the Hasbrouck/Gonzalo-Granger pair.

**Garg, Singhal, Sood, Rupeika-Apoga & Grima (2023). *Price Discovery … between National Agriculture Market and NCDEX.* JRFM 16(2):62.** [saved: Garg2023_price_discovery_enam_ncdex.pdf]
Johansen + VECM + Granger + bivariate-GARCH spillover between eNAM spot, NCDEX spot, NCDEX futures.
NCDEX spot dominant in discovery.
**For us: ADOPT** (open access) as a recent Indian template combining discovery + spillover — a compact
C2-satellite model; also informs the open which-spot question (eNAM vs mandi-modal vs NCDEX-polled).

**Diebold & Yilmaz (2012). *Better to Give than to Receive: … Volatility Spillovers.* Int. J. of Forecasting 28(1).** [saved: DieboldYilmaz2012_volatility_spillovers_directional.pdf]
VAR + generalized FEVD → total/directional/net connectedness; rolling / TVP-VAR variant.
**For us: ADOPT** for a C2 satellite — connectedness among {banned spot, control spot, CBOT wheat /
FCPO}; did banned spot become more isolated / more intl-exposed once the domestic futures anchor
vanished? **CAVEAT:** only ~7 treated + ~4 control nodes → small VAR; use rolling/TVP to date any shift
vs Dec-2021 (further endogeneity check).

**Garbade & Silber (1983)** — see §3 (foundational lead-lag/discovery; bridges discovery and basis).

### 5d. Basis, hedging & the Samuelson effect
**Bessembinder & Seguin (1992). *Futures-Trading Activity and Stock Price Volatility.* J. of Finance 47(5).** [url only]
Partition futures volume + OI into expected/unexpected; spot vol rises with unexpected volume, FALLS
with forecastable (deep-market) activity.
**For us: ADOPT** as the core MECHANISM theory and strongest pre-ban analysis: run on banned spot vol
vs futures volume/OI while futures existed (CPO contract-level in hand; chana/wheat incoming). If deep
OI dampened spot vol pre-ban, removing futures should RAISE spot vol — a falsifiable prediction for
C1/C2 robust to the DiD's death. Indian precedent: Sharma-Malhotra (2015).

**Gupta, S. & Rajib, P. (2012). *Samuelson Hypothesis & Indian Commodity Derivatives Market.* Asia-Pacific Financial Markets 19(4).** [url only]
Tests the maturity effect (futures vol rises into expiry) on Indian futures, controlling for
seasonality (full text not retrieved).
**For us: CONSIDER** for the CPO contract-level analysis — we hold 64 MCX CPO contracts with
volume+OI, so the Samuelson effect is testable and MUST be controlled when measuring CPO pre-ban
volatility (expiry-clustering biases vol). Relevant only where we have contract-level data = CPO. A
nuisance to control, not a headline.

**Yeasin, Sharma, Paul, Meena & Anwer (2024). *Understanding Price Volatility and Seasonality in Agricultural Commodities in India.* AERR 36(2).** [url only]
Decomposes Indian agri series into trend/seasonal/volatility; harvest-cycle seasonality in vol (peaks
pre/at harvest, troughs post-harvest).
**For us: ADOPT** as India-specific evidence that C2 vol comparisons MUST deseasonalize before pre/post
contrast (else seasonal composition differences confound the ban effect). Supports the H7 harvest-
troughs link.

---

## 6. Indian policy lineage (institutional history)

**Dantwala (1966). *Report of the Forward Markets Review Committee.*** [saved: Dantwala1966_forward_markets_review.pdf]
Cautioned that suppressing futures prices irrespective of spot behaviour destroys the utility of
futures markets; preceded the 1966 cotton ban.
**For us: ADOPT** the Dantwala dictum as a historical epigraph for the identification problem — a govt
committee anticipating our finding.

**Khusro (1980). *Report of the Committee on Forward Markets.*** [saved: Khusro1980_forward_markets_committee.pdf]
Majority recommended reintroducing futures in many commodities (oilseeds, castor, basmati, onion);
cautious on sensitive staples; basis for the 2003 reintroduction.
**For us: ADOPT** for the institutional-history section — ban-on-suspicion as a recurrent Indian reflex
driven by inflation politics. **NOTE:** verify the archive.org scan is the Khusro (not Kabra) volume.

**Kabra (1994). *Report of the Committee on Forward Markets.*** [url only — see Khusro1980 PDF mirror note]
Policy review with majority/minority recommendations on which commodities to (re)permit.
**For us:** anchors the lineage Dantwala 1966 → Khusro 1980 → Kabra 1994 → Sen 2008 → 2021.

**Expert Committee (Abhijit Sen) (2008). *Report … Impact of Futures Trading on Agricultural Commodity Prices.* MoCAF&PD.** [url only — login-walled mirrors]
Pre/post-futures inflation comparison; the 2007 delisting (wheat/rice/tur/urad); dissent notes. Could
not establish a causal futures-inflation link; inflation accelerated post-futures in 14 commodities,
decelerated in 7; Sen's note kept wheat concerns open.
**For us: ADOPT** the acceleration/deceleration tabulation style; the canonical Indian precedent — the
government's own committee found no causal link, yet bans recurred (politically, not evidentially,
driven). Period mismatch — methodology/framing only.

---

## Coverage notes

### Known paywalled / login-walled (no archived PDF; URLs + [MANUAL] in references.md)
- **EPW** (paywalled, institutional access): Dey & Gairola (2024) — the closest published C1 claim;
  Sumalatha & Nirmal Roy (2023); Lingareddy (2008); Nath & Lingareddy (2008) EPW commentary (the
  longer SSRN 1087904 version IS archived as `Nath2008_…pdf`).
- **SSRN** (403s scripted fetch; free browser login): Aggarwal-Chatterjee-Sehgal 2022 (4261360) AND
  2023 (4407637) — the two SCM precedents; Sahi & Raizada (2006, 949161); Brajesh Kumar (2009, 1364231).
  Use the Ideas-for-India (2025) summary for the 4407637 figures meanwhile.
- **Emerald / publisher walls:** Sobti (2020); Sharma & Malhotra (2015); Bandyopadhyay et al. (2022);
  Gupta & Rajib (2012) — abstract/landing only.
- **Other landing-only:** Dubey & Dey (2023, SAGE); Kabi et al. (2023, SAGE); Datta (2017, PBR);
  Sneagen (2022, Essex repository — Ch.2 ban episode UNVERIFIED, PDF fetch timed out); Yeasin et al.
  (2024, ICAR epubs — open, fetch full text for the seasonal-adjustment method); Inani (2018, Springer);
  Diebold-Yilmaz / Hillebrand / Lamoureux-Lastrapes / Inclán-Tiao / Hasanov et al. / Haas et al. /
  Bessembinder-Seguin / Working 1949 / Fama-French 1987 / Ibragimov-Müller / Firpo-Possebom (method
  PDFs to collect via institutional access as read).
- **FMC-commissioned (grey, archive hunt):** IIM Bangalore (Naik) 2008 — now under
  sebi.gov.in/sebi_data/fmcfiles/.

### Unverifiable / dropped claims (recorded so the work is not silently lost)
- **Lama, Jha, Paul & Gurung (2021)** GARCH-with-structural-break on ag prices: ResearchGate record
  403-blocked; venue NOT independently confirmed; authors/data unverified. Listed as TO-FETCH; **do not
  cite as evidence** until full text is read.
- **Sneagen (2022)** thesis: the specific ban episode used in Ch.2 could not be confirmed (repository
  metadata only) — cite for framing, verify the episode before citing a result.
- **Gulati/Naik/FMC basis-risk magnitudes** for guar/tur are taken from IEG's *secondary* summary, not
  the primary FMC report — flag as second-hand until the FMC scan is located.
- **NCDEX-funded reports** (Gaurav-Pandey 2024; Rajib et al. 2024; PwC 2023): conflict-of-interest must
  be flagged at every citation; their "volatility increased" headlines rest on uncontrolled pre/post
  comparisons our placebo undermines — cite for institutional context and the NULL vol-DiD, not for
  causal magnitudes.

### Cross-reference
This file does NOT duplicate `01_literature/references.md` (the provenance ledger with URLs, access
dates, local paths and **[MANUAL]** download flags). Entries here add method/finding/verdict. Two
items resolved during this synthesis: **DES2022** in references.md = Jha & Chakravarty (2021),
`Jha2021_futures-market-agri-commodities.pdf` (now located); the ConleyTaber2011 and FermanPinto2017
PDFs exist on disk despite empty `saved_file` tags in the source bibliography. The new method PDFs are
appended to `references.md` §4 (causal) / §5 (vol-basis).
