# RESUME HERE — full state snapshot, 2026-06-21 (read this first to restart)

This file lets you (or a fresh session) pick the project back up from exactly where it stopped.
Everything below is **saved to disk**; nothing depends on a live session. Canonical results memo:
`04_empirics/H1_volatility/c1_findings.md`.

## THE CURRENT HEADLINE FINDING (latest — supersedes the clean-core −20.7%)
The C1 analysis went through three states; the **latest and most honest is the FOOD-DONOR re-run**:

| | clean-core (5 industrial/spice donors) | **food-donor (9 donors: +barley/maize/jowar/bajra)** |
|---|---|---|
| DiD | −20.7%, p≈0.026–0.046 (sig) | **−9.8%, p=0.145 / boot 0.153 (NOT significant)** |
| DiD ex-wheat | −25.5% | −15.2%, **p=0.003 (sig)** |
| SDID pooled | −26.9% (no valid SE) | **−19.1%, z=−1.88** (valid SE now; borderline ~p.06) |
| SDID chana | −36% | −38.7%, **z=−2.05 (sig)** |
| SDID wheat | −19% | **+0.4% (≈ZERO — wheat decline was MSP/export-ban confound, NOT the futures ban)** |
| SCM chana | −40% (floor .167) | −37%, placebo **p=0.100** (at floor) |
| Placebo | −11.7%, p.19 | **−6.5%, p=0.34 / boot 0.43 (cleaner)** |
| Pre-trend | p.19 | **p=0.45 (cleaner)** |

**Honest verdict (current):** the suspension did NOT raise spot volatility and is *associated with* lower
volatility **concentrated in chana** (the cleanest commodity, significant across all methods). The
**aggregate effect is modest (~−10%) and NOT robustly significant** once a proper food-staple
counterfactual is used — the strong −20% was inflated by industrial/spice donors that aren't a valid
counterfactual for food staples. Wheat is confounded out (MSP/export bans). Falsification is now clean.
**This is INTERIM: only 4 of 8 food donors (the cereals) are in. The 3 OILSEED donors
(groundnut/sesamum/sunflower) + ragi are NOT pulled yet — they are the right counterfactual for the
banned OILSEEDS (mustard, soybean), so those two numbers will likely shift when the pull completes.**

## DATA STATE
- `02_data/clean/vol_panel_monthly.csv` is CURRENTLY the **9-donor (food-cereal) rebuild** (16 commodities).
  The result files in `04_empirics/H1_volatility/output/` and `.../V0.../output/` now hold the FOOD-DONOR
  numbers (did_results_district.txt = −9.8%, etc.). The clean-core numbers are in git history + the docs.
- Food-donor district pull is **PAUSED** (I killed it for the clean rebuild). Complete: barley, maize,
  jowar (36/36), bajra (29/36). NOT pulled: ragi, groundnut, sesamum, sunflower (0/36).
- CEDA API key in `.env` valid to **2026-06-28**. Rate limit 40 req/hr.

## TO RESUME (exact commands)
1. **Finish the food-donor pull** (resumable, skips done files; ~6–10 h at 40/hr):
   `.venv/bin/python 00_code/download_ceda_agmarknet.py bajra ragi groundnut sesamum sunflower`
2. **Rebuild the panel + re-run all estimators** (after the pull, for the full 8-donor result):
   `.venv/bin/python 00_code/build_volatility_panel.py`
   `.venv/bin/python 00_code/run_v0_did.py vol_panel_monthly.csv district paddy guar`
   `.venv/bin/python 00_code/run_c1_robustness.py` (leave-one-out + honest few-cluster p)
   `.venv/bin/python 00_code/run_c1_scm.py` ; `run_c1_scm_district.py` ; `run_c1_sdid.py`
   `.venv/bin/python 00_code/run_v0_placebo.py` ; `run_v0_bootstrap.py` ; `run_c2_garch_icss.py`
   `.venv/bin/python 00_code/make_paper_tables.py` (regenerates the paper tables from the outputs)
3. **To get back the clean-core (5-donor) result instead:** the panel is rebuilt from raw; to exclude the
   food donors, temporarily remove them from `FOOD_DONORS` in run_c1_scm/_district/_sdid.py and pass them
   to the drop-list of run_v0_did/placebo/bootstrap, then rebuild+re-run.

## WHAT IS DONE (all on disk)
- **Data:** CEDA/Agmarknet spot (5.74M district rows, 12 commodities) + 4 food-cereal donors (1.24M+ rows).
  Trading-day (weekday) fix applied; paddy dropped (MSP); guar=id413. Control/CPO/cotton futures.
- **Estimators (00_code/):** run_v0_did, run_v0_placebo, run_v0_bootstrap (wild-cluster, corrected),
  run_c1_scm, run_c1_scm_district, run_c1_sdid, run_c1_robustness (leave-one-out + CR1 few-cluster p),
  run_c2_garch_icss, run_h3_efficiency, run_h7_troughs, run_h8_composition, make_paper_tables.
- **Companion results:** H3 (spot integration loss, p≈0.07), H7 (harvest-trough null), H8 (NCDEX agri
  ~1.4% hedgers) — see each `04_empirics/H*/h*_findings.md`.
- **Adversarial REFEREE REVIEW done** (3 flows): all numbers reproduce exactly; flagged over-stated
  inference; CORRECTED (removed spurious SDID z=−7.7, honest few-cluster p, leave-one-out, marginal
  placebo, mechanical convergence). See session_log session 16.
- **Project-wide consistency sweep done** — paper/cv_story/interview/admin all reconciled to c1_findings
  (clean-core −20.7% framing). **NOTE: these docs now need re-propagation to the FOOD-DONOR numbers above.**
- **Deliverables:** paper draft `05_paper/drafts/paper.tex` (+7 sections + tables + 3 figures);
  `05_paper/cv_story.tex`; `05_paper/interview_pack/*.tex`. All currently carry the clean-core −20.7%.

## WHAT IS PENDING (priority order)
1. **Finish the pull (4 oilseed/ragi donors) → re-run → the FULL 8-donor result.** mustard/soybean will
   refine with oilseed counterfactuals.
2. **Re-propagate the FOOD-DONOR finding to the paper/cv_story/interview** (they still say −20.7%; the
   honest current headline is the donor-sensitivity story: ~−10% aggregate, concentrated in chana,
   wheat confounded). The donor-pool sensitivity IS the key result.
3. **Inference upgrades the referee demanded:** Honest-DiD (Rambachan–Roth) sensitivity; Callaway–Sant'Anna
   / Sun–Abraham; wild-bootstrap confidence interval.
4. Paper: `pdflatex+bibtex` compile (no toolchain in this env); tidy the stub bibliography.
5. Blocked on data: C2 basis (chana/wheat futures + FCPO); H2/H5/H6.

## GIT / COMMIT
Working tree is **uncommitted** (all changes saved to disk). The harness blocked stripping the AI
co-author trailer, so commits were not made by the assistant. To version this yourself:
`git add -A && git commit -m "..."` (on your machine, your call on attribution). Nothing is lost without
a commit. The 5.74M-row raw pull and all outputs are on disk.

## ONE-LINE STATUS
Reproducible, referee-reviewed evaluation; honest current finding = **suspension associated with lower
spot volatility, concentrated in chana, ~−10% aggregate and not robustly significant under a proper
food-staple counterfactual; wheat confounded.** Interim (4/8 food donors). Everything saved.
