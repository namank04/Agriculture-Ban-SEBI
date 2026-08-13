# C1 Pre-Registration — spot-volatility effect of the suspension (frozen 2026-06-21)

Frozen BEFORE estimating the synthetic-control results. Locks the primary spec and the
robustness curve so later choices can't be reverse-engineered from the answer. Companion:
`../V0_lost_results_replication/spec.md` (the original §A/§B pre-registration, now superseded
for C1 by this), `01_literature/methodology_menu_c1_c2.md §437`, `00_admin/decision_log.md`.

## Question
Did India's Dec-2021 agri-derivatives suspension change **spot price volatility** of the
banned commodities, relative to a credible counterfactual? (Inherited claim: +8–10%. V0 naive
DiD refuted it: effect is negative, and after the trading-day fix the DiD is no longer
pre-trend-dead but its placebo still recovers −11.7% (56% of the headline) → SCM/robust inference needed for a trustworthy number.)

## Locked design

**Outcome.** `ln(rv30)` — log of the 30-day realized volatility (annualized √252) of daily
log spot returns, monthly. Built on **trading-day-only** series (weekday filter, the 2026-06-21
calendar-grid fix). Robustness twins: 60-day rv; Parkinson H–L if OHLC spot available.

**Data / level.** **District panel** `02_data/clean/vol_panel_monthly.csv` (commodity × district
× month), trading-day-corrected. National-mean series are headline-only (and must be rebuilt as a
median first — guar national-mean carries a ₹14.3M outlier). Treatment is assigned at the
**commodity** level → **cluster all inference by commodity**, never over-crediting district count.

**Treated units (banned).** chana, wheat, soybean, moong, mustard. **paddy DROPPED** from the
primary (MSP price-censored — 40.3% flat returns; decision_log 2026-06-21). **wheat KEPT** but
MSP-flagged (19.7% flat; core-trio commodity, read as robustness). CPO is **routed out** of the
spot-vol track (no mandi spot) to the basis/international track (H4).

**Donor pool (Option B).** Core, screened, in hand: **castor, guarseed413, cotton, jeera,
turmeric** (guar id 75 dropped; cotton's Aug-2022 unit-break confined to the futures track). To
be ADDED once acquired + re-screened: non-banned food staples **coriander, barley** (then
maize/jowar/bajra with an own-policy screen). Donors must (a) be the same/adjacent group where
possible, (b) stay traded & liquid through the ban, (c) carry no own treatment in-window.

**Treatment timing (per-commodity / staggered).** chana **2021-08-16**, mustard **2021-10-08**,
{wheat, paddy, soybean, moong, CPO} **2021-12-20** (policy ledger). No already-suspended
commodity may serve as a donor for a later episode.

**Estimator — convergent panel (not a single number).**
- **Primary (v1, now):** Abadie synthetic control per treated commodity on the district-median
  `ln(rv30)` path, weights fit to the pre-treatment path (simplex: w≥0, Σw=1).
- **Co-primary (v2, after food donors):** Synthetic DiD (Arkhangelsky) + Augmented SCM
  (Ben-Michael–Feller–Rothstein) + **district-level penalized SCM** (Abadie–L'Hour) on the full
  panel — the real few-cluster escape.
- **Sensitivity layer:** Honest-DiD; predictor-matched SCM (intl prices, production, net imports).

**Inference.** In-space placebos (treat each donor as fake-treated) + pre/post RMSE-ratio test
(Abadie). With only 5 donors the placebo p-value floor is ~1/6 — **inference is weak until the
food donors widen the pool** (the explicit reason to acquire them). v2 adds conformal/scpi and a
wild-cluster bootstrap clustered by commodity.

## Pass/fail (decided now)
- C1 "ban raised vol" is **supported** only if the SCM gap is **positive**, in a defensible band,
  and the treated RMSE-ratio sits in the **top tail** of the placebo distribution.
- A **negative** gap that beats placebos = the ban is associated with **lower** spot vol
  (descriptive, given remaining endogeneity) — report as such, do not over-causalise.
- Headline = **convergence across estimators**, never one point estimate (Ferman–Pinto: SC
  reduces but doesn't eliminate selection bias).

## Frozen rosters / exclusions
- Donors excluded: guar id 75 (gum), kapas (illiquid), any commodity with an own in-window shock.
- Exclusion windows from the policy ledger applied before estimation (e.g. cotton Aug-2022).
- Specification curve to report: ±{30,60}-day rv × {drop paddy / keep flagged} × {core / core+food}
  × {per-commodity dates / single Dec-2021}.
