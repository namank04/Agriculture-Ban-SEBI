# Policy Intervention Timeline ("Confounder Ledger")

## Purpose

This folder records a **selected set of major government and regulatory interventions**
that are material to interpreting the agricultural-derivatives suspension and the
post-suspension spot-price evidence.

It is not intended to be an exhaustive catalogue of every agricultural policy change.
The ledger focuses on interventions that directly affected a treatment commodity,
its close substitutes, or the information environment created by the derivatives suspension.

## How the ledger is used

The timeline supports:

1. transparent disclosure of important concurrent policies in the identification discussion;
2. interpretation of commodity-level heterogeneity;
3. selection and discussion of cleaner or more heavily confounded windows; and
4. candidate robustness/sensitivity analyses where a specific intervention is relevant.

The existence of an entry does **not** imply that a corresponding policy dummy was included
in every regression. The ledger does not eliminate all possible confounding.

## Fields

- `date`: intervention/order date used for the timeline.
- `commodity`: affected commodity or commodity group.
- `intervention`: concise description of the policy action.
- `direction_on_spot`: **ex ante qualitative channel or pressure**, not an estimated effect.
- `affects`: which treatment or comparison context the intervention is most relevant to.
- `status`: verification status.
- `source_url`: primary official source wherever available.
- `notes`: implementation details, effective dates, later amendments, or interpretation caveats.

All entries in the current version are marked `CONFIRMED_PRIMARY` and are supported by
SEBI, PIB, DGFT/APEDA, or another Government of India primary source.

## Interpretation rules

`direction_on_spot` should never be read as a measured causal coefficient. For example,
an export prohibition is coded as downward domestic-price pressure because it is expected
to increase domestic availability, while removal of such a prohibition is coded as upward
domestic-price pressure. Actual price effects may differ because of market conditions and
other simultaneous policies.

SEBI derivatives restrictions are coded `info_loss` to identify the treatment/information
channel. This label does not by itself establish that price discovery deteriorated.

## Main confounding patterns

### Wheat

Wheat has the densest policy environment in the post-suspension period, including the
May-2022 export prohibition, restrictions on wheat-flour exports, OMSS releases, repeated
stock-limit regimes, and later withdrawal/re-imposition changes. Wheat estimates therefore
require especially cautious interpretation.

### Mustard and the oilseed complex

Mustard is not affected only by its 8 October 2021 derivatives suspension. A central
edible-oil/oilseed stock-limit regime also became effective on 8 October 2021, creating a
same-date confounder. Import-duty changes in October 2021 and subsequent edible-oil measures
also affect the broader oilseed complex.

### Crude Palm Oil

CPO is exposed to repeated import-duty changes and substitution from soybean and sunflower
oil. These policies are material confounders for any CPO-specific interpretation.

### Paddy / rice

Rice markets were affected by the September-2022 broken-rice restriction and export duty,
the July-2023 non-basmati white-rice prohibition, and the March-2025 liberalisation of
broken-rice exports. This reinforces the decision to treat paddy/rice evidence cautiously.

### Chana and pulses

Chana is relatively cleaner earlier in the sample but is affected by the June-2024
tur/chana stock-limit order. Kabuli chana was subsequently excluded from that order by
S.O. 2718(E) dated 11 July 2024. Tur/urad interventions are also relevant as pulse-market
context for moong.

## Derivatives-suspension chronology

- 16 Aug 2021: Chana restrictions, SEBI PR 25/2021.
- 08 Oct 2021: Mustard Seed restrictions, SEBI PR 29/2021.
- 19 Dec 2021: directions issued for the seven-commodity suspension; SEBI PR 36/2021
  was released on 20 Dec 2021.
- 20 Dec 2022: extended through 20 Dec 2023, PR 38/2022.
- 27 Oct 2023: extended through 20 Dec 2024, PR 25/2023.
- 18 Dec 2024: extended through 31 Jan 2025, PR 37/2024.
- 31 Jan 2025: extended through 31 Mar 2025, PR 07/2025.
- 24 Mar 2025: extended through 31 Mar 2026, PR 16/2025.
- 27 Mar 2026: extended through 31 Mar 2027, PR 21/2026.

There is **no January-to-March 2026 gap** in the suspension chain: PR 16/2025 had already
extended the restriction through 31 March 2026.

## Verification status

Primary-source verification completed through **27 March 2026**, including the extension
of the seven-commodity derivatives suspension through **31 March 2027**.

Last ledger review: 28 August 2026.
