# H7 — Did harvest-season price troughs deepen after the ban?

**Hypothesis.** With agri-derivatives suspended (2021-12-20) there is no forward/futures
signal to smooth seasonal gluts, so harvest-time price *troughs* should deepen post-ban
(distress sales, no storage/hedging signal). chana is the designated headline commodity;
wheat is procurement-dominated (MSP) and is flagged, not interpreted.

**Verdict: NOT SUPPORTED (and if anything the sign is opposite).** On price-only data,
banned-commodity seasonal troughs got *slightly shallower* after the ban relative to
controls. The difference is small and statistically insignificant. There is no evidence
that the ban deepened harvest troughs.

---

## What was tested (price-only)

Monthly national modal spot prices, 2017-01..2025-10 (106 months/commodity, weekday-clean),
from `02_data/clean/spot_daily_<c>.csv`. Two complementary trough metrics, each estimated
**separately pre vs post ban**, then compared banned vs control in a difference-in-differences:

1. **Primary — trend-detrended annual trough depth.**
   `depth = 1 − (annual-minimum monthly price / centered-12-month-MA trend at that month)`.
   Higher = the year's low dipped further below the smooth trend. Averaged over pre years
   (2017–2021) and post years (2022–2025).

2. **Robustness — seasonal-index amplitude.** Classical multiplicative seasonal index
   (ratio-to-2×12-MA, median over years, normalised to mean 1). `amplitude = 1 − min(seasonal factor)`.
   Harvest-aligned by construction (the seasonal low *is* the glut month).

Banned headline set = chana, mustard, soybean, moong. Controls = still-traded futures
commodities (castor, guarseed413, jeera, turmeric, cotton) + non-banned food/oilseed donors
(barley, maize, jowar, bajra, ragi, groundnut, sesamum, sunflower). wheat excluded from the
DiD (MSP-flagged); paddy dropped entirely (MSP price-censored).

## Results

| Metric | banned change (post−pre) | control change | **DiD (banned − control)** | p |
|---|---|---|---|---|
| Primary (detrended trough depth) | −0.0218 | −0.0008 | **−0.0211** | 0.20 |
| Robustness (seasonal amplitude)  | −0.0153 | +0.0168 | **−0.0321** | n/a |

Both metrics give a **negative** DiD — the opposite sign to the H7 prediction — and the
primary OLS DiD (commodity FE, cluster-robust SE by commodity, n=119 commodity-years) is
not significant (p=0.20).

Headline commodity **chana**: trough essentially unchanged (seasonal amplitude pre 0.058 →
post 0.057, Δ ≈ −0.002; detrended depth 0.060 → 0.051). **soybean** troughs got notably
*shallower* (amplitude 0.081 → 0.035). Among controls, jeera and turmeric troughs deepened
sharply post-2021 — driven by their own supply cycles / price booms, not the ban — which is
exactly the kind of idiosyncratic control move that makes the small banned-side change
uninformative.

**wheat (flagged, not in DiD):** apparent trough *deepening* (amplitude 0.017 → 0.066), but
this is an MSP/procurement artifact — pre-period wheat spot was pinned near the support price
(tiny seasonal amplitude), so the change reflects procurement dynamics, not a market signal.

## Blocked / cannot be shown with this data (honest)

- **Arrivals / quantity concentration is NOT available.** The spec.md method's core leg —
  "share of crop sold within X weeks of harvest, pre vs post" — needs mandi *arrival quantities*,
  which are not in our dataset (we have prices only). The actual distress-sale mechanism
  (farmers dumping more tonnage at harvest) can therefore **not** be observed directly. We see
  only the *price shadow* of a glut, and prices reflect demand, imports, MSP, stocks and global
  moves too — so a null on prices does **not** prove arrivals were unaffected.
- **MSP procurement quantities** (the spec's wheat control) are likewise unavailable, so wheat
  and paddy can only be flagged, not used.
- **Power.** Only ~4 pre and ~3 post crop-years per commodity; 2021 straddles the Dec ban. With
  4 banned commodities the DiD is underpowered to detect a small trough change, and control
  commodities have their own large idiosyncratic seasonal shifts (jeera, turmeric, sunflower).
  Treat the magnitude as indicative, not precise.

## Bottom line

On the evidence we can compute, **H7 fails**: harvest-season price troughs did not deepen for
banned commodities after the suspension — the point estimates lean the other way and are not
significant. The economically meaningful version of the hypothesis (more tonnage dumped at
harvest) is **blocked** for want of arrivals data and cannot be settled here.

## Outputs (`04_empirics/H7_harvest_troughs/output/`)
- `h7_seasonal_index.csv` — month × commodity × {pre,post,full} multiplicative seasonal factors
- `h7_trough_depth.csv` — per commodity-year trough depth + detected trough month
- `h7_summary.csv` — per-commodity pre/post trough depth and change, by group
- `h7_seasonal_amplitude.csv` — robustness amplitude metric per commodity
- `h7_did.csv` — both DiD estimates
- `h7_seasonal_<c>.png` — seasonal index pre vs post for 8 key commodities (harvest band shaded)
