# Data Specification v1.0 — 2026-06-10
**Decision rule:** hypothesis → estimator → variables → frequency → window → source.
Collect nothing no estimator consumes; promise no estimator data we cannot source.

## Scope decisions (locked)
- **Instruments: FUTURES ONLY.** Options excluded — pre-ban liquidity negligible vs futures;
  all hypotheses concern price discovery & hedging located in futures. (Parking lot: pre-ban
  options IV as robustness garnish if ever needed.)
- **Frequency: daily EOD.** No intraday/tick — no estimator requires it; access cost huge.
- **Commodities: 12 total.**
  - Banned 7: wheat, chana, mustard seed complex, soybean complex, paddy (non-basmati),
    moong [NCDEX] + crude palm oil [**MCX — NOT NCDEX; separate request/source needed**]
  - Control candidates 5: guar seed, castor seed, turmeric, jeera [NCDEX] + cotton [MCX] /
    kapas [NCDEX] (screening will keep 3–4)
  - Core analysis: wheat, chana, CPO + surviving controls. Rest = appendix.
- **Exchange caveat:** cotton = MCX, kapas = NCDEX — confirm which during control screening.

## Window asymmetry (do not get this wrong)
- Banned commodities' futures: 2017-01-01 → 2021-12-20 (trading ceased)
- Control commodities' futures: 2017-01-01 → 2025-12-31 (needed post-ban for H1 donors, H5)
- All spot/structural series: 2017 → 2025 (sowing data from 2015 for H6 lags)

## The nine streams
| # | Stream | Variables | Freq | Window | Source | Feeds | Status |
|---|---|---|---|---|---|---|---|
| 1 | NCDEX futures bhavcopy (banned 6) | OHLC, vol, value, OI, expiry by contract | daily | 2017–2021 | exchange request / vendor / Wayback | H2 H5 | 🔴 blocked (archive floor Jul 2024) |
| 2 | MCX futures bhavcopy (CPO) | same | daily | 2017–2021 | MCX contract-wise endpoint (browser route) | H2 H4 | 🟢 acquired 2026-06-10 (64 contracts incl vol+OI; c1–c3 constructed) |
| 3 | Controls' futures | same | daily | 2017–2025 | NCDEX bhavcopy (post-Jul-2024 public; earlier same problem as #1) | H1 H5 | 🟡 partial |
| 4 | Spot prices | mandi modal + exchange polled spot | daily | 2017–2025 | Agmarknet; exchange polled spot archives | H1 H2 H3 H4 H7 | 🟢 public |
| 5 | Mandi arrivals | qty arrived by mandi | daily/wk | 2017–2025 | Agmarknet | H7 | 🟢 public |
| 6 | Participant-wise OI | OI by category | monthly | 2019–2021 | SEBI monthly bulletins | H2 (future) | 🟢 public, tedious |
| 7 | Delivery per expiry | qty delivered | per expiry | 2017–2021 | NCCL circulars / exchange | H2 (future) | 🟡 scattered |
| 8 | International + FX | CBOT wheat & soy, Bursa FCPO; USD/INR, MYR/INR | daily | 2017–2025 | public vendors; RBI | H4 | 🟢 public |
| 9 | Structural | state sowing area; CPI/WPI food; MSP + procurement qty; policy-intervention dates | ann/mo | 2015–2025 | DES; MoSPI; OEA; CACP/FCI; confounder ledger | H6 H7 + robustness | 🟢 public |

## What bhavcopy does NOT contain (common confusion — do not expect it there)
spot prices (stream 4) · participant categories (stream 6) · delivery quantities (stream 7)
· arrivals (5) · anything structural (9). Bhavcopy = futures contract-level trading summary only.

## Action edits triggered by this spec
- [ ] Send PARALLEL data request to MCX for CPO (and cotton) 2017–2021 — adapt NCDEX email
- [ ] Test MCX public bhavcopy archive depth (mcxindia.com/market-data/bhavcopy) before emailing
- [ ] Control screening must record each candidate's exchange (NCDEX vs MCX)
- [x] data_log.csv: add column `exchange` — done 2026-06-10
