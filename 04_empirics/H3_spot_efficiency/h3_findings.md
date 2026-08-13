# H3 — Did removing futures degrade spot-market efficiency / integration?

**Run:** `00_code/run_h3_efficiency.py` → `04_empirics/H3_spot_efficiency/output/`
**Question:** After the 2021-12-20 derivatives suspension, did the *spot* markets of
banned commodities become **less informationally efficient** (Part A) and **less
spatially integrated** (Part B), relative to controls whose futures kept trading?

**Commodity sets**
- Banned (primary): chana, mustard, soybean, moong. paddy dropped (MSP price-censored,
  `utils.EXCLUDE_PRIMARY`); wheat reported separately as **MSP-flagged**, not in the
  headline banned mean.
- Controls (futures still trade): castor, guarseed413, jeera, turmeric, cotton.
- Windows: PRE = pre-2021-12-20, POST ≥ 2021-12-20. ~1,290 trading days pre, ~1,000 post.

---

## Headline

| | direction expected if H3 true | banned | control | banned − control |
|---|---|---|---|---|
| **A. Δ\|VR−1\| (q=10)** efficiency loss | ↑ | **+0.13** | +0.02 | **+0.11** |
| **B. Δ coint-share** integration loss | ↓ | **−0.16** | +0.06 | **−0.22** |
| **B. Δ dev. half-life (days)** | ↑ | **+1.4** | −0.1 | +1.5 |

Both pieces point the **same way**: banned commodities' spot markets look *less*
efficient and *less* integrated after losing the futures price signal, while controls
do not — and in part B controls actually *improved* (consistent with the e-NAM tailwind,
which works *against* the disintegration finding, so the banned drop is a lower bound).

**But the effects are NOT statistically significant at conventional levels** — see Power.

---

## Part A — Lo-MacKinlay variance-ratio tests (national daily spot returns)

Under a random walk VR(q)=1; |VR−1|>0 ⇒ predictable returns ⇒ less informationally
efficient. We use holding periods q∈{2,5,10} and treat **Δ|VR−1| = |VR_post−1| − |VR_pre−1|**
as the efficiency-loss measure, contrasted banned vs control (a DiD-in-VR).

- Δ|VR−1| (post−pre), group means: q=2 → banned +0.04 / control +0.03; q=5 → +0.10 / +0.02;
  **q=10 → +0.13 / +0.02 (DiD +0.11)**. The contrast grows with horizon, as expected if
  the futures signal mainly disciplined longer-horizon mean reversion.
- 3 of 4 banned commodities moved further from the RW null (soybean largest, +0.33;
  moong the exception). 3 of 5 controls moved away too but by less.

**Note on the VR significance (corrected 2026-06-21).** An earlier version of this script
had a coding error in the Lo-MacKinlay heteroskedasticity-robust statistic — a spurious
sample-size factor in the M2 variance (Campbell–Lo–MacKinlay 1997, eq. 2.4.43) that deflated
its z by √n and made M2 spuriously fail to reject while the homoskedastic M1 rejected. That
bug was found in adversarial review and fixed. The corrected M2 now **rejects the random walk
for nearly all commodity-windows** (|z| ≈ 1–9) and **agrees with M1**: spot mandi returns are
predictable (not a random walk) in both windows. The efficiency-LOSS signal is the pre→post
**change in |VR−1|** (the point estimates, which the bug never touched); returns are winsorized
at 1% per window (`WINSOR_P`) so the VR reflects genuine serial dependence, not glitch jumps.
The binding limitation is the small number of **commodities** for the cross-commodity contrast
(4 banned vs 5 controls), not the VR test itself.

Files: `output/A_variance_ratios.csv` (per-commodity VR, both z-stats, all q),
`output/A_vr_did_summary.csv`.

## Part B — cross-mandi spatial integration (Engle-Granger, pre vs post)

**Selection rule (fixed BEFORE looking at integration results, per spec):** per commodity,
the top **8** mandis (`SELECT_TOP_MANDIS`) by trading-day coverage that report on **≥40%**
(`MIN_COVERAGE_FRAC`) of trading days in **both** windows. Log price levels, business-day
grid, short gaps (≤5d) forward-filled. All 8C2=28 mandi pairs get an Engle-Granger
cointegration test at 5%; we report the **share of cointegrated pairs** and the **median
error-correction half-life** (AR(1) on the cointegrating residual) in each window.

- **Coint share Δ (post−pre):** banned −0.16 vs control **+0.06**.
  3 of 4 banned **lost** integrated pairs (moong −0.36, chana −0.14, soybean −0.14;
  mustard flat). Only **1 of 5** controls fell (cotton); the other four held or **rose**
  (turmeric +0.29, jeera +0.18). MWU banned<control **p=0.069** (one-sided, n=4 vs 5).
- **Deviation half-life Δ:** banned +1.4 days (mustard 1.0→6.4 the driver) vs control −0.1.
  Slower price-error correction post-ban for banned = exactly the predicted efficiency loss.
- Controls *improving* over 2022–25 is the **e-NAM expansion tailwind** working *against*
  H3 — so the banned-vs-control gap (−0.22 in share) is a **conservative lower bound** on
  disintegration. (spec.md risk note.)

Files: `output/B_integration_by_commodity.csv`, `output/B_integration_did_summary.csv`.

---

## Power / honest limitations

- **Underpowered.** Only 4 clean banned commodities vs 5 controls. The cross-commodity
  contrasts are descriptive: Part A DiD-in-VR Mann-Whitney **p=0.21**; Part B coint-share
  MWU **p=0.069**. Directionally consistent, not significant at 5%.
- **VR test is valid** (the M2 formula was corrected 2026-06-21; it now rejects the random
  walk for ~all commodity-windows and agrees with M1). The binding limit is the small number
  of *commodities* for the cross-commodity DiD-in-VR contrast (p=0.21), not the VR test.
- **Aggregation.** Part A uses the national modal series; the modal-of-modals construction
  injects composition noise. Part B (true mandi-level) is the cleaner test and is the
  stronger result.
- **Confounds.** 2022–23 also saw a Russia-Ukraine commodity shock, MSP hikes, and e-NAM
  growth; the control group is the defense, but the small n limits how much it absorbs.
- **No volume/arrivals data** — mandi importance proxied by reporting coverage, not turnover.

## Bottom line
H3 is **directionally supported but statistically underpowered**. The cleaner mandi-level
integration test (Part B) shows banned commodities losing cross-mandi cointegration and
correcting price deviations more slowly after the ban, while controls did not (and even
improved against the e-NAM tailwind) — MWU p≈0.07. The VR efficiency test (Part A) moves
the same way (DiD +0.11 at q=10); the corrected VR tests reject the random walk, and the
cross-commodity contrast is underpowered at p≈0.21 (only 4 banned commodities). **Suggestive evidence of spot-market
efficiency/integration loss; not a clean rejection of the null. Recommend treating as
corroborating, not standalone.**
