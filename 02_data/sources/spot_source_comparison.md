# Spot-price data source comparison — DECISION NEEDED
Probed 2026-06-11. Spot/mandi prices (streams 4 & 5) feed H1, H2, H3, H4, H7 and **unblock
V0**. Three sources evaluated. The researcher chooses the route (rule 6); this memo gives the
facts to decide. Nothing bulk-downloaded yet.

## TL;DR recommendation
**Primary: CEDA API** (needs a free API-key registration — a 2-minute user action) for fast,
clean, documented bulk pulls. **Provenance anchor: Agmarknet official API** (no key; spot-check
a sample of CEDA against it for the data appendix). **eNAM: validation only**, later. Rationale
below; the only blocker on the recommended path is the CEDA key, which only you can register for.

## 1. Agmarknet — official portal (agmarknet.gov.in) — PRIMARY SOURCE OF RECORD
- Site is now **Agmarknet 2.0**, a React SPA backed by a **public JSON API** at
  `api.agmarknet.gov.in/v1/` (no key; needs `Origin: https://agmarknet.gov.in` header).
- **Commodity strings SOLVED** — the missing acquisition-manual problem is closed. Full
  571-commodity id→name list saved to `agmarknet_commodity_ids.json`. Our targets:
  - Wheat = id **1** ("Wheat"); Chana = id **6** ("Bengal Gram(Gram)(Whole)");
    Guar = id **62** ("Guar") or **342** ("Guar Seed(Cluster Beans Seed)") — verify which
    carries the futures-relevant series; Castor = **106** ("Castor Seed");
    Turmeric = **35**; Jeera = **38** ("Cummin Seed(Jeera)").
  - Filter master also exposes 37 states, 729 districts, 4209 markets (district granularity
    available), grade (FAQ), variety.
- **Gap:** the actual price/arrival *data* endpoint (beyond the filter master
  `dashboard-filters`) was NOT captured passively — the SPA fetches it only after in-page
  commodity+date selection, and guessed endpoint names 404'd. Recovering it needs a short
  headed-Chrome session that performs a real selection and sniffs the resulting XHR (same
  technique used for MCX). One focused probe, then a scripted puller is straightforward.
- **Effort for full pull:** moderate once the endpoint is captured; coverage 2000→present.

## 2. CEDA (Ashoka University) — cleaned mirror + API — RECOMMENDED PRIMARY
- Cleaned re-serving of the same MoA Agmarknet data: **300+ commodities, 2700+ mandis,
  2000→present, updated monthly**, daily/monthly/yearly frequencies.
- **Two access modes:** browser tool (`agmarknet.ceda.ashoka.edu.in` — was intermittently
  unreachable during probe; main `ceda.ashoka.edu.in` is fine) and a **programmatic API**
  (`api.ceda.ashoka.edu.in`) that **requires a free API key (register on the API page)**.
- **Usage terms:** free download/display/reuse for **non-commercial** purposes — matches our
  academic use; cite CEDA. (Provenance note for the paper: CEDA is a third-party cleaner, so
  we cite both CEDA and the underlying MoA Agmarknet source, and validate a sample against #1.)
- **Why primary:** cleaning already done (saves us the Agmarknet quirks — holiday gaps,
  name drift, unit inconsistencies); documented; bulk-friendly. Fastest path to V0.

## 3. eNAM (enam.gov.in/web/dashboard/trade-data) — VALIDATION ONLY
- Live dashboard, server-rendered with commodity + APMC selectors; scriptable.
- **Different data:** actual e-auction *transaction* prices, narrower/younger mandi coverage
  (eNAM rollout from 2016, uneven). Not a substitute for Agmarknet's broad polled mandi
  series — use as a **robustness/validation** cross-check on Agmarknet modal prices and as a
  data point in the "how is spot measured" methodology discussion. Defer until core spot lands.

## Decision required from researcher
1. **Route:** CEDA-primary (recommended) vs Agmarknet-official-primary (heavier but
   first-party, no third-party-cleaning provenance question).
2. **If CEDA:** register for the free API key at api.ceda.ashoka.edu.in (only you can).
3. Either way: I can write the puller + validation cross-check once the route is chosen and
   (for CEDA) the key exists, or (for Agmarknet) after one headed-Chrome endpoint-capture probe.

## Done as part of this probe
- `agmarknet_commodity_ids.json` — 571 official commodity id↔name strings (kills the missing
  acquisition-manual blocker).
