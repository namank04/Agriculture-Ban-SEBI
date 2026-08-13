# Data Source Guide & Access Notes
| Series | Source | Access | Status |
|---|---|---|---|
| Pre-ban futures (price/volume/OI) | NCDEX bhavcopy archives / annual reports | UNKNOWN — TEST FIRST | 🔴 critical path |
| Spot/mandi prices + arrivals | Agmarknet (agmarknet.gov.in) | Public, scrapable | 🟢 |
| Participant-category OI | SEBI monthly bulletins (sebi.gov.in) | Public PDFs ~2019+ | 🟢 tedious |
| Delivery data per expiry | NCDEX/NCCL circulars | Public, scattered | 🟡 |
| CBOT wheat, soy | Public market data / FRED / vendor | Public | 🟢 |
| Bursa Malaysia CPO (FCPO) | Bursa / vendor / investing archives | Mostly public | 🟢 |
| CPI/WPI food sub-indices | MoSPI / Office of Economic Adviser | Public | 🟢 |
| Sowing area (state-level) | DES Land Use Statistics, state ag depts | Public, lagged | 🟢 |
| FX rates USD/INR MYR/INR | RBI | Public | 🟢 |
| NABCONS 2022 / ICAR-CIPHET 2015 | MoFPI / PIB | Public reports | 🟢 context only |
Rule: every download → row in 00_admin/data_log.csv, file → 02_data/raw/SOURCE/
