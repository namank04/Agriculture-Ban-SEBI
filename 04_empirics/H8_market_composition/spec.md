# H8 — What kind of market was banned? [FIRST UP — quick win]
**Hypothesis:** Pre-ban speculation was not excessive relative to hedging demand.
**Difficulty:** method LOW, labor HIGH (PDF extraction), identification NONE (descriptive)
## Data needed
- SEBI monthly bulletins, participant-category OI (farmers/FPOs, value-chain participants, others/prop), ~2019-01 to 2021-12 → raw/sebi_bulletins/
- NCDEX delivery data per expiry for wheat, chana, CPO-adjacent, 2017–2021 → raw/ncdex_delivery/
- Contract volumes & OI by commodity (NCDEX annual reports as fallback)
## Method
1. Tabulate participant-category OI shares per commodity per month
2. Compute Working's T = 1 + SS/(HL+HS) if hedging net short (SS=spec short, HL/HS=hedge long/short) — map SEBI categories to hedger/speculator carefully, DOCUMENT the mapping
3. Delivery ratio = qty delivered / qty traded per expiry; benchmark against intl norms (low single digits is NORMAL — state this)
## Output
- Table: participant composition by commodity (becomes paper Table 2)
- Figure: Working's T over time vs. literature thresholds (T < 1.15–1.25 ≈ not excessive)
- 1-page result memo: was mustard-2021 the exception? (concede if so — strengthens credibility)
## Risks
- SEBI category definitions may shift across bulletins → build a crosswalk
- Working's T needs long/short split by category; if bulletins give net only, use modified index and say so
## Checklist
- [ ] Locate & download bulletins  - [ ] Extraction script  - [ ] Category crosswalk
- [ ] Working's T series  - [ ] Delivery ratios  - [ ] Result memo
