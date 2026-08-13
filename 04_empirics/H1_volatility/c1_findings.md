# C1 findings — spot-volatility effect of the suspension

Status: trading-day-corrected data, paddy dropped, guar id75 excluded, 9-donor food-cereal rebuild
(clean core + barley/maize/jowar/bajra). Updated 2026-07-04 to make the food-donor rerun the body
of the memo rather than a warning banner. This supersedes the clean-core −20.7% framing.

## Headline: the inherited "+8–10% rose" claim is refuted, but the latest aggregate decline is modest and not significant.

The current defensible claim is: the suspension did **not** raise spot volatility, and is associated
with lower volatility **concentrated in chana**. Once food-cereal donors are included, the aggregate
DiD is **−9.8%** and **not robustly significant** (CR1 p≈0.145; wild bootstrap p≈0.153). The older
clean-core result (−20.7%, p≈0.026/0.046) was inflated by using industrial/spice donors as the
counterfactual for food staples.

| Estimator | Point estimate | Honest inference |
|---|---|---|
| **Two-way-FE DiD** (district panel) | **−9.8%** | CR1 p≈**0.145**; wild bootstrap p≈**0.153**. Not significant. |
| **Synthetic DiD** (pooled) | **−19.1%** | placebo SE now available with 9 donors; z≈**−1.88** (borderline, not decisive). |
| **Synthetic DiD** (per commodity) | chana **−38.7**, mustard −15.2, wheat **+0.4**, soybean −26.1, moong −11.5 | chana z≈**−2.05**; wheat ≈zero, consistent with MSP/export-ban confounding. |
| **SCM** (Abadie, commodity) | chana **−37.3**, mustard −28.2, wheat −37.8, soybean −27.6, moong −8.7 | chana at placebo floor p=0.100 with 9 donors; other SCM p-values remain weak. |
| **District-unit SCM** | negative for all treated, strongest for chana/mustard/wheat | placebo floor p=0.100 with 9 donors; still not a conventional 5% test. |

## What is genuinely robust
- The sign remains negative across district-liquidity and outlier filters: about **−8.7% to −10.0%**.
- Dropping wheat still gives a significant negative estimate (**−15.2%, CR1 p≈0.003**), so the non-wheat
  result is not mechanically driven by the MSP/export-ban wheat series.
- Chana is the cleanest and strongest case: SDID **−38.7%** (z≈−2.05) and SCM **−37.3%** (placebo
  floor p=0.100).
- The falsifications are cleaner than the clean-core run: placebo **−6.5%** (p≈0.34; wild bootstrap
  p≈0.43), and pre-trend p≈0.45.

## What is weak / unresolved (the referee's real concerns — keep these caveats)
1. **Aggregate significance disappears.** The main DiD is not significant once food-cereal donors enter.
2. **Full food/oilseed donor set is still incomplete.** Barley/maize/jowar are complete and bajra is
   partial; ragi, groundnut, sesamum, and sunflower are not in the district panel. This matters most
   for mustard and soybean.
3. **Wheat is confounded.** SDID wheat is ~zero after food donors, so the earlier wheat decline should
   not be read as a futures-ban effect.
4. **SCM inference remains coarse.** With 9 donors, the placebo floor improves to p=0.100 but still
   cannot establish 5% significance.
5. **Treatment remains bundled with other policy shocks.** Export bans, stock limits, MSP/procurement,
   and edible-oil tariff changes contaminate commodity-specific attribution.
6. **No Honest-DiD / Callaway-Sant'Anna / Sun-Abraham upgrade yet.** The current result is descriptive
   and quasi-causal, not a publishable causal estimate.

## C2 (GARCH) — unchanged: "elevated vol" not supported; ICSS finds no break near the ban; district-median chana GARCH degenerate. Volatility case rests on C1, not C2.

## Honest bottom line
The inherited "+8–10% rose" is **refuted**. The current food-donor result is **not** a strong aggregate
"ban lowered volatility" result; it is a donor-sensitivity result. The defensible claim is: the
suspension did not raise spot volatility, the aggregate estimate is about **−10%** and not significant,
and the only strong positive evidence for lower volatility is concentrated in **chana**. Reaching a
publishable causal result requires finishing the full food/oilseed donor pull, rerunning all estimators,
and adding Honest-DiD / staggered-DiD robustness plus a wild-bootstrap confidence interval.

## Next
Finish food/oilseed district pull → rebuild panel + re-run; then propagate the final donor-sensitivity
story to the paper and companion documents.
