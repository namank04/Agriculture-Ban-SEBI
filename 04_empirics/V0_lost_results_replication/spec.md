# V0 — Replication & Verification of Lost Results [PRIORITY ONE]
**Status:** This module runs FIRST. Its output becomes H1's first pass (no duplicated work).

## The claims under verification (from lost work's summary)
| # | Claim | Trust level | Why |
|---|---|---|---|
| C1 | DiD + event study on district panel → spot vol +8–10% post-ban | UNVERIFIED | No stated vol measure, base, spec, or SE treatment |
| C2 | "Persistent basis widening" post-ban + GARCH(1,1) elevated vol, sig at 10% | **INTERNALLY INCONSISTENT** | Banned commodities have NO futures post-Dec-2021 → no basis can exist. Was it (a) pre-ban basis trend, (b) control-commodity basis, (c) domestic–international spread mislabeled? Must determine before any rerun |
| C3 | CPI/WPI + acreage + district production → inflation transmission (in progress) | INCOMPLETE | Was never finished; treat as design idea, not result |

## Verification protocol (PRE-REGISTER before touching data — fill Section A first)
### A. Lock the specification (write down BEFORE estimation)
- Volatility measure (primary): 30-day rolling std of daily log returns, annualized.
  Robustness twins: 60-day; Parkinson high–low if OHLC spot available; EGARCH conditional vol.
- DiD spec: vol_it = α_i + λ_t + β·(banned_i × post_t) + X_it + ε_it
  - i = commodity×district (panel), t = month
  - FE: unit and time. Cluster SEs at COMMODITY level (few clusters → wild-cluster bootstrap)
  - X_it: rainfall deviation, policy-intervention dummies from confounder ledger
- Event study: monthly leads/lags ±18 months around Dec 2021; pre-trend test = joint sig of leads
- GARCH(1,1) per commodity spot series with ban step-dummy in the VARIANCE equation;
  compare persistence (α+β) pre vs post
- "Basis" resolution: compute pre-ban basis (futures − spot) trend up to Dec 2021 ONLY;
  separately compute domestic-spot vs international-futures spread for CPO/wheat post-ban
  and label it correctly (this is probably what the lost work actually did)
### B. Pass/fail rules (decide now, not after seeing results)
- C1 CONFIRMED only if: same sign + magnitude within [4%, 16%] band + p<0.05 under
  wild-cluster bootstrap + survives placebo-date test (fake ban at Dec 2019 shows nothing)
- C1 magnitude differs but sign holds → report OUR number, cite verification, move on
- Pre-trends fail → DiD result is dead regardless of significance; synthetic control becomes primary
- 10%-significance results: report but never headline
### C. Data needed (all PUBLIC — V0 is fully unblocked by the bhavcopy wall)
- District/mandi-level spot prices, banned + control commodities, 2017–2025 (Agmarknet)
- Rainfall by district (IMD), policy dummies (confounder ledger)
- CPI/WPI food sub-indices monthly (MoSPI/OEA) for C3 design
- Pre-ban futures ONLY needed for the basis-trend piece → that sub-task waits on data access

## Order of work
1. [ ] Fill Section A blanks final (with Claude)  2. [ ] Pull Agmarknet panel for core trio + 2 controls
3. [ ] Build vol panel (00_code/build_volatility_panel.py)  4. [ ] DiD + event study (run_v0_did.py)
5. [ ] GARCH per commodity (run_v0_garch.py)  6. [ ] Placebos + wild-cluster bootstrap
7. [ ] Verdict memo: output/v0_verdict.md — claim by claim: confirmed / revised / dead
## Resume note
This module = "replicated and stress-tested prior causal estimates; identified internal
inconsistency in basis analysis; pre-registered verification protocol" — strong research-integrity
signal for a quant/research profile.
