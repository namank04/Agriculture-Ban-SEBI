# H4 — Did the ban insulate domestic prices? [SECOND — best effort/payoff]
**Hypothesis:** Domestic prices did NOT decouple from international prices post-ban.
**Difficulty:** access EASY, method MED, payoff HIGH. CPO is the star (60%+ import dependence).
## Data
- Bursa Malaysia FCPO daily settle 2017–2025; CBOT wheat; CBOT soybean (appendix)
- Domestic spot: CPO landed/Kandla price, wheat mandi benchmark; FX USD/INR MYR/INR (RBI)
- From policy timeline: import-duty change dates (CPO) and wheat export-ban date as controls/breaks
## Method
1. Convert intl prices to INR; log series
2. Pre vs post: Johansen cointegration domestic↔international; ECM speed-of-adjustment comparison
3. Pass-through elasticity pre vs post with duty-change dummies
4. Wheat twist: export ban (2022-05) mechanically severs the link — that is ITSELF a finding: insulation required a SECOND, costlier intervention; the derivatives ban alone did nothing
## Output: pass-through table pre/post per commodity + ECM adjustment speeds + result memo
## Risks: structural breaks from duty changes (handle with dummies/break tests, dates from confounder ledger)
## Checklist
- [ ] Pull intl series  - [ ] Pull domestic spot  - [ ] FX merge  - [ ] Cointegration pre/post
- [ ] Pass-through estimates  - [ ] Result memo
