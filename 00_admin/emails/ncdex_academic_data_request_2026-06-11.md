# NCDEX academic data request — ready to send
**To:** [NCDEX market data / academic liaison — check current address on ncdex.com → Contact Us; commonly the market-data or "askus" desk]
**From:** [Your name] <[your institutional email if available — improves response odds]>
**Subject:** Academic research request — contract-wise daily bhavcopy (futures), 11 agri commodities, 2017–2025

---

Dear NCDEX Market Data Team,

I am [Name], [designation, institution]. I am conducting an academic study evaluating the
December 2021 suspension of derivatives trading in agricultural commodities — specifically,
its effects on price volatility, price discovery, and market participants. The work is
intended for peer-reviewed journal publication. Exchange-published data is essential because
public vendor sources lack volume and open interest, which the analysis requires.

**Data requested — contract-wise daily bhavcopy (end-of-day), i.e., one row per contract per
trading day, for ALL contract expiries of each commodity:**

| Field | Description |
|---|---|
| Date | Trading date |
| Symbol | Commodity symbol |
| Expiry date | Contract identifier |
| Open, High, Low, Close | Daily traded prices |
| Previous close / settlement price | As published |
| Volume (lots and/or quantity) | Daily traded volume |
| Value (Rs) | Daily turnover, if published |
| Open interest | End-of-day OI per contract |

**Commodities and periods:**

1. *Suspended commodities* — wheat, chana, mustard seed complex, soybean complex,
   paddy (non-basmati), moong: **2017-01-01 to the 2021-12-20 suspension** (including any
   post-suspension settlement records of then-live contracts, if published).
2. *Comparison commodities* — guar seed, castor seed, turmeric, jeera, kapas:
   **2017-01-01 to 2025-12-31** (or latest available).

In short: the maximum available daily contract-level history for these 11 commodities.

**Format:** CSV or Excel, any structure convenient to you (per commodity, per contract, or
pooled). If the exchange also maintains the corresponding **daily polled spot price series**
for these commodities, that would be valuable supplementary data, though the bhavcopy is
the core request.

The data will be used solely for academic research, will not be redistributed, and NCDEX
will be acknowledged as the source in any resulting publication. I am happy to sign a data
use agreement, provide an institutional letter, or pay any applicable academic fee.

Could you let me know the procedure and any costs involved?

Thank you for your time.

Regards,
[Name]
[Designation, Institution]
[Phone] · [Email]

---
*Internal notes (do not send):* schema mirrors what MCX publishes per contract (see
`02_data/raw/mcx/` — Date, Symbol, ExpiryDate, OHLC, PreviousClose, Volume, Value,
OpenInterest), so both exchanges' data land pipeline-identical. The "post-suspension
settlement records" line is deliberate — it documents the stale-quote regime rather than
letting it surprise us. If no reply in ~2 weeks: resend, then try the NCDEX Investor
Protection/academic outreach channel or a faculty co-signature.
