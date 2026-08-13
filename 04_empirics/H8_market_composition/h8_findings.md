# H8 — Who was in the agri-derivatives market the suspension removed?

**Run:** `00_code/run_h8_composition.py` → `04_empirics/H8_market_composition/output/`
**Question:** What was the participant composition of the agri-derivatives segment before the
Dec-2021 suspension — i.e. who actually used the market that was switched off?

## Data
SEBI monthly bulletin table *"Participant-wise percentage share of turnover at MCX, NCDEX,
ICEX, BSE and NSE"* — the **Agri segment** columns, split into **Proprietary / Client /
Hedgers**, monthly. This is necessarily **pre-ban** (no post-ban agri futures exist) and
**segment-level** (SEBI does not report participant shares per commodity in this table).
SEBI labels "Hedgers" directly, so the descriptive composition needs **no** hedger/speculator
crosswalk decision.

**Coverage caveat (honest).** The table's number and layout **vary month to month** (it appears
as Table 70/71/72 in different bulletins, with shifting header rows), so a single parser cleanly
extracted **10 of 33** bulletins — the window **2020-04 to 2021-03** (the year immediately before
the suspension, the most policy-relevant pre-ban snapshot). The 2019 and a few 2021 bulletins use
variant layouts the current parser does not handle; full 2019–2021 coverage needs a multi-layout
parser and is left as a refinement. Within-exchange participant shares **sum to 100%** (sanity
check passes), so the parsed numbers are internally valid.

## Finding: the suspended agri market was overwhelmingly speculative
Mean Agri-segment turnover share, 2020-04..2021-03:

| Exchange | Proprietary | Client | Hedgers |
|---|---|---|---|
| **NCDEX** (agri staples: chana, mustard, guar, jeera…) | 42.0% | 56.5% | **1.4%** |
| **MCX** (CPO, cotton) | 35.9% | 64.1% | — (no hedger column) |
| ICEX | 27.6% | 55.8% | — |

**Genuine hedger participation in NCDEX agri futures was ~1.4% of turnover** — the market was
~98.5% proprietary + client (speculative/financial) flow.

## Interpretation (two-sided, honest)
- The pro-ban premise was that futures *serve* the physical market (hedging, price discovery).
  On the hedging leg, **direct hedger use was already minimal** before the suspension — so the
  "we protected farmers' hedging tool" framing on *either* side overstates how much hedging the
  market actually carried.
- But "mostly speculative" does **not** mean "worthless." A speculator/client-dominated market
  still supplies **liquidity and price discovery**, and **H3 finds exactly that was lost** (spot
  markets became less efficient/integrated post-ban). So the cost of the suspension shows up in
  the **price-discovery / integration** channel (H3), not in a large direct-hedging loss.
- The "Hedgers" category is SEBI's narrow registration; some client flow is latent hedging, so
  1.4% is a lower bound on hedging — but the order of magnitude (low) is the point.

## Limitations
- **10/33 bulletins** (2020-04..2021-03); turnover **share** (not open interest); **segment**-level
  (not per commodity); pre-ban descriptive only.
- **Working's speculative T** (needs participant long/short OI, not just turnover share) is future
  work and would require the long/short OI tables plus a researcher decision on the
  hedger/speculator mapping (CLAUDE.md rule 6).

## Bottom line
The NCDEX agri-derivatives market the suspension removed was **speculator/client-dominated, with
~1.4% hedger turnover**. Combined with H3, the welfare cost of the ban is best read as a loss of
**price discovery and spatial market integration**, not a large loss of direct farmer hedging —
a more precise (and more defensible) cost story than "farmers lost their hedging tool."
