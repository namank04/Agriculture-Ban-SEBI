# Data Specification — Final Research Scope
**Purpose:** document the data actually used in the final empirical analysis and the data retained for the future H2 extension.
Collect nothing no estimator consumes; promise no estimator data we cannot source.

## Final scope

The final research package contains two completed empirical branches and one future extension.

### H1 — Spot-price volatility
Completed.

- Outcome: district-level mandi spot-price realized volatility.
- Primary empirical methods: Difference-in-Differences and Synthetic Control.
- Treated commodities: chana, mustard, wheat, soybean and moong.
- Final comparison commodities: castor, guarseed413, cotton, jeera, turmeric, barley, maize, jowar and bajra.
- Paddy is excluded because of substantial flat-price/MSP-related censoring.
- CPO is not included in H1 because a comparable mandi spot-price series is unavailable.

### H3 — Spot-market functioning
Completed as supporting evidence.

- Informational-efficiency analysis uses national mandi spot-price returns.
- Spatial-integration analysis uses mandi-level spot-price series.
- Main measures are variance ratios, pairwise Engle-Granger cointegration shares and adjustment half-lives.
- H3 concerns spot-market functioning and is not a direct futures-versus-spot price-discovery test.

### H2 — Futures-market mechanisms / price discovery
Future extension only.

Historical futures data are incomplete for the main suspended NCDEX commodities, so no completed H2 empirical result is reported.

If sufficient historical futures data become available, H2 may examine:

- futures-versus-spot price discovery;
- VECM-based dynamics;
- Hasbrouck information shares;
- Gonzalo-Granger component shares;
- participant-category market structure; and
- delivery/open-interest information.

Participant-category and delivery data are therefore retained only as possible future H2 inputs, not as completed findings.

## Data windows

### Spot-price data

The completed H1 and H3 analyses use mandi spot-price data from approximately 2017 through 2025.

The final cleaned monthly H1 volatility panel runs from February 2017 through October 2025.

### Futures data

Historical futures series are used only where they are available for source validation, exploratory construction and possible future H2 work.

The 2021 suspension means that treated-commodity domestic futures do not provide a post-suspension series. A post-ban domestic futures-versus-spot basis therefore cannot be constructed for the suspended contracts.

Historical NCDEX futures availability remains the main constraint on a completed H2 price-discovery analysis.

## Final data streams

| Stream | Variables | Frequency | Role in final project | Status |
|---|---|---|---|---|
| Agmarknet/CEDA mandi spot prices | modal prices by market/district | daily | H1, H3 | acquired and used |
| Monthly volatility panel | `rv30`, commodity, state, district, month | monthly | H1 | constructed and used |
| Mandi-level spot series | modal prices by mandi | daily | H3 spatial integration | acquired and used |
| Policy-intervention timeline | major agricultural policy events | dated events | H1/H3 interpretation and confounding assessment | completed |
| Historical domestic futures | OHLC, volume, OI, expiry | daily | future H2 | incomplete for key NCDEX suspended contracts |
| Participant-category data | participant-wise OI / market composition | monthly | future H2 | possible extension |
| Delivery information | delivery quantities by contract/expiry | contract/expiry | future H2 | possible extension |

The raw district-level Agmarknet collection used in the project contains **7,242,927 market-day records across 16 commodity slugs and 569 JSON files**.

The cleaned monthly volatility panel contains **172,381 observations**.

The final H1 candidate set contains **147,616 observations across five treated and nine comparison commodities**.

## What a futures bhavcopy does not contain

A futures bhavcopy is a contract-level trading summary. It should not be confused with:

- mandi spot prices;
- participant-category tables;
- physical delivery quantities; or
- the agricultural policy-intervention timeline.

These come from separate data sources.

## Final interpretation rule

Only H1 and H3 are treated as completed empirical analyses in the current project.

H2 is retained as a future research extension and must not be presented as a completed result unless the required historical futures data are obtained and the corresponding analysis is actually executed.
