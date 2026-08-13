# H1 — Did the ban reduce spot volatility? [THE HEADLINE — do after warm-up]
**Hypothesis:** Spot volatility did NOT decline post-ban relative to controls.
**Difficulty:** method HIGH, identification HIGH (max referee scrutiny).
## Pre-fit diagnostic GATE (do first): build synthetic control from donors (guar, castor, cotton, turmeric, jeera) on PRE-2021 volatility — if pre-fit poor → fall back to DiD with parallel-trends plots. This decides the paper's main spec.
## Method: realized vol (rolling σ of log returns) + EGARCH conditional vol; DiD with commodity & time FE; synthetic control per commodity; placebo-in-time and placebo-in-commodity tests
## Controls must be screened: continuous trading 2017–2025, no major own-policy shocks (check confounder ledger), comparable seasonality
## Risks: Ukraine shock (answered: controls share it — say explicitly); India-specific wheat interventions (use chana as headline if wheat too messy); donor-pool justification is the whole battle
## Checklist: [ ] control screening  [ ] vol series  [ ] pre-fit diagnostic  [ ] DiD  [ ] synth control  [ ] placebos  [ ] memo

## RELATION TO V0 (added v1.1)
V0 replication IS H1's first pass: its DiD/event-study/GARCH outputs feed directly here.
H1 then adds: synthetic control, donor-pool justification, placebo battery, EGARCH. Do not redo V0 work.
