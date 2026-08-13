# Reading List (priority order)
**Every document cited/used gets an entry in `references.md` (link + accessed date + local PDF in `papers/`).**
## Tier 1 — must read fully
- [ ] Abhijit Sen Committee Report (2008) — Govt of India, the historical anchor
- [ ] ICRIER Working Paper 383 — Linking farmers to futures markets (Gulati et al.)
- [ ] DES/MoA report: Futures Market for Agricultural Commodities in India (2021-22)
## Tier 2 — for methodology templates
- [ ] Working, H. (1960) — Speculation on hedging markets (for Working's T index, H8)
- [ ] Hasbrouck (1995) — information shares (H2)
- [ ] Gonzalo & Granger (1995) — common factor decomposition (H2)
- [ ] Abadie et al. — synthetic control method papers (H1)
- [ ] Nerlove acreage-response literature + Indian applications (H6)
## Tier 3 — Indian ban literature
- [ ] Nair (2011); Lingareddy (2008, 2015); Sahadevan; Bose — post-2008 ban studies
- [x] 2021-ban-specific sweep — done 2026-06-10 (web sweep; SSRN/EconPapers pass still worthwhile):

### 3a. Papers on THE 2021 suspension (direct competitors/complements — read before V0 verdict)
- [ ] **Gaurav, Sarthak & Pandey, Piyush (2024)** — *Impact of Suspension of Agri Commodities on
      Food Prices and Agri Ecosystem* — SJMSOM IIT Bombay + BIMTECH empirical report (Nov 2024).
      Findings: no evidence futures trading drove spot prices for the suspended commodities;
      edible-oil retail prices ROSE post-suspension; price analysis + farmer/trader surveys in
      MH, MP, GJ. [Get the full report PDF from IIT-B/BIMTECH; only press coverage in hand.]
- [ ] **Aggarwal, Nidhi (IIM Udaipur); Chatterjee, Tirtha (JSGPP); Sehgal, Karan** — study of
      mustard & chana around the suspension. Key results reported: pre-ban futures held ~64%
      share of price discovery for mustard; mandi price volatility INCREASED post-suspension
      (mustard, soybean). [Locate the working paper itself — likely IIM-U/XKDR WP; we have
      press coverage only. Directly overlaps our H1/H2 — must know their specs before locking ours.]
- [ ] **Dey, Kushankur (IIM Lucknow) & Gairola, Gaurav (2024)** — *Is Suspending Agricultural
      Futures Justified?* EPW Vol 59(9), Mar 2024. Chana/soybean/refined soy oil; finds spot
      volatility considerably higher post-ban for chana and refined soy oil; notes the review
      committee never published pre/post analysis.
- [ ] Secondary press synthesis (context only): Business Standard (Nov 2024) "Futures trading
      ban fails to cool retail prices"; Down To Earth study summary; BS editorial "Rethinking
      suspension". Useful for the policy-debate framing in the intro, not as evidence.
- [ ] **Aggarwal, N., Jain, S. & Thomas, S. (2014, IGIDR WP)** — price discovery/hedging
      effectiveness around EARLIER Indian commodity bans — methodology template that the
      IIM-U team likely reuses; pairs with the post-2008 studies above.

### 3b. Spot price provision mechanics (data infrastructure — feeds streams 4 + H2/H3 measurement notes)
- [ ] **Agmarknet**: APMC mandi staff enter daily min/max/modal prices + arrivals via the
      AGMARK application; ~4,000+ mandis, 300+ commodities. Portal: agmarknet.gov.in.
      **CEDA (Ashoka Univ.) cleaned mirror: agmarknet.ceda.ashoka.edu.in — candidate bulk
      source to unblock V0; provenance/cleaning steps must be documented before use.**
- [ ] **eNAM**: e-auction trade-level platform (enam.gov.in dashboards); actual transaction
      prices, narrower mandi coverage — alternative/validation source for mandi modal prices.
- [ ] **Exchange polled spot (NCDEX)**: exchange polls value-chain participants/accredited
      agencies at delivery centres; polled spot is the basis for final settlement of futures.
      See NCDEX AGRIDEX methodology PDF (ncdex.com, 2020) + ncdex.com/markets/spotprices
      (historical polled spot — test download depth). **Agriwatch** = private agri-intelligence
      agency (agriwatch.com), historically one of the spot-polling agencies — its archives are
      a fallback spot source for CPO/edible oils.
- [ ] Open measurement question for spec: mandi modal (Agmarknet) vs polled spot (exchange) —
      which is "the" spot for basis/H2/H3, and does the choice change results? (robustness twin)

### 3c. MSP as confounder (feeds policy timeline + H3/H7 controls)
- [ ] MSP procurement is heavily concentrated (wheat/paddy; Punjab-Haryana-west UP); ICAR-NIAP:
      only ~9.6% of wheat farmers sell under MSP procurement — so MSP binds regionally, not
      nationally. Wheat spot near procurement windows is the contaminated case (consistent with
      our "wheat = most confounded" ranking).
- [ ] Jha, Natasha et al. — *Minimum Support Prices in Indian Agriculture* (WP) — empirical MSP
      price-effects paper; + Emerald J. Econ & Dev (2023): farmer knowledge of MSP does not
      improve farm-gate prices absent procurement.
- [ ] TODO for policy timeline: add MSP announcement + procurement-window dates for wheat/chana
      (CACP/FCI) as interventions — they move spot independently of the ban.
## Notes convention
One file per paper: 01_literature/notes_AUTHOR_YEAR.md (citation, 3-bullet summary, what we borrow, page refs)
