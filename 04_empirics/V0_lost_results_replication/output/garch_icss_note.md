# C2 — ICSS-then-within-regime GARCH (note)

**Method.** ICSS on daily log returns locates unconditional-variance change-points;
GARCH(1,1) is then fit WITHIN each regime instead of a single naive pre/post split. This
is the mandatory Hillebrand (2005) fix: neglected variance breaks bias GARCH persistence
(alpha+beta) toward 1 (IGARCH artifact).

**Primary detector = `k2` (Sanso, Arago & Carrion (2004) kappa-2, HAC-corrected).** Raw Inclan-Tiao assumes iid returns and badly
OVER-detects on GARCH-type series — it reads every volatility cluster (and every fat-tailed
mandi jump) as a variance break. Sanso-Arago-Carrion replace the iid 2*sigma^4 scaling with a
Bartlett-HAC long-run variance of squared returns, correcting for the 4th moment and serial
dependence; it is the standard ICSS variant for financial returns. Both are run below.

ICSS sup-stat critical value = 1.358 (~5%); a break counts as 'near' the suspension
within +/-30 trading days; GARCH fit requires >= 250 obs per regime.

## Detector contrast — break counts (the over-detection problem)

| commodity | series | n_breaks (raw IT) | n_breaks (k2 HAC) |
|---|---|---|---|
| castor | distmed | 36 | 0 |
| castor | national | 35 | 0 |
| chana | distmed | 38 | 1 |
| chana | national | 38 | 0 |
| guarseed413 | distmed | 4 | 0 |
| guarseed413 | national | 18 | 0 |
| wheat | distmed | 31 | 0 |
| wheat | national | 35 | 0 |

Raw IT finds dozens of 'breaks' (volatility-cluster / heavy-tail artifacts); the HAC-
corrected k2 finds at most one. Reporting raw-IT regimes would be Hillebrand's error in
reverse — chopping the sample into un-fittable slivers.

## Detected variance breaks (primary detector `k2`)

| commodity | series | n_breaks | break dates | near suspension? (gap td) |
|---|---|---|---|---|
| chana | distmed | 1 | 2018-09-14 | False (761) |
| wheat | distmed | 0 | (none) | False (n/a) |
| castor | distmed | 0 | (none) | False (n/a) |
| guarseed413 | distmed | 0 | (none) | False (n/a) |
| chana | national | 0 | (none) | False (n/a) |
| wheat | national | 0 | (none) | False (n/a) |
| castor | national | 0 | (none) | False (n/a) |
| guarseed413 | national | 0 | (none) | False (n/a) |

## Does ICSS+regime-split cure the degenerate persistence?

Naive pre/post persistence (from `garch_summary*.csv`) vs the within-regime persistence
on the regimes that actually fit (>= MIN_REGIME obs):

| commodity | series | naive pre | naive post | within-regime persist (per fitted regime) |
|---|---|---|---|---|
| chana | distmed | 1.000 | 1.000 | R1=0.908, R2=1.000* |
| wheat | distmed | 1.000 | 0.972 | R1=0.997 |
| castor | distmed | 0.948 | 0.986 | R1=0.756 |
| guarseed413 | distmed | 0.900 | 0.847 | R1=0.942 |
| chana | national | 0.554 | 0.693 | R1=0.629 |
| wheat | national | 0.681 | 0.414 | R1=0.540 |
| castor | national | 0.869 | 1.000 | R1=0.973 |
| guarseed413 | national | 0.998 | 0.718 | R1=0.927 |

\* = persistence still >= 0.999 (degenerate / IGARCH even within regime).

## Substantive C2 finding (was there a variance break near the suspension?)

- Under the correct (HAC-corrected `k2`) detector, NO commodity has a variance
  change-point within +/-30 trading days of its suspension date — on either the
  district-median or the national series. The only k2 break anywhere is distmed-chana
  at 2018-09-14, ~761 trading days BEFORE the Aug-2021 chana suspension (unrelated).
- The apparent 'breaks near the ban' under raw IT (e.g. wheat-national flags one 26 td
  out) are heavy-tail / cluster artifacts that the HAC correction removes. So this
  GARCH-ICSS baseline gives NO independent evidence of a ban-induced unconditional-
  variance shift; the volatility case rests on the SCM/DiD (C1) results, not on C2.

## Honest verdict (district-median chana — the degenerate case)

- Naive pre/post persistence was ~1.0 (IGARCH artifact / degenerate), the symptom
  Hillebrand attributes to a neglected variance break.
- The HAC-corrected ICSS finds 1 break (2018-09-14), splitting the series into
  an early regime (443 obs) and a long 2018-2025 regime (1852 obs).
- **PARTIAL help, not a cure.** The early regime drops to persist=0.908 (off the
  IGARCH boundary), but the LONG 2018-2025 regime is STILL persist=1.000. So the
  degeneracy is only partly a neglected-break artifact: removing the one break
  fixes the short early window, yet the bulk of the series remains degenerate.
- Crucially the break is ~761 td from the suspension, so this does NOT manufacture
  a ban effect. Verdict: report distmed-chana GARCH persistence as UNRELIABLE;
  do not headline a persistence number for it — lean on SCM/DiD (C1) for vol.

## Caveats
- Raw IT over-detects badly under heavy tails / volatility clustering (30-40 'breaks'/series);
  the HAC-corrected k2 is the reportable detector. The IT rows are kept only for contrast.
- k2 is conservative in moderate samples — finding ~0 breaks is partly low power, not proof
  of perfect variance stability. Read it as: no break large enough to dominate GARCH bias.
- paddy/wheat spot are MSP-censored (msp_flag) — their variance dynamics are partly mechanical.
- Short regimes (< MIN_REGIME obs) get realized-vol only, no GARCH, by design.