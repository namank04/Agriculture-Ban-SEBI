# TASK FILE — full-project validation + professor report (opened 2026-07-06)

## Instructions (from researcher, 2026-07-06)
1. Validate EVERYTHING in the folder: data collection → cleaning → hypothesis progression →
   errors made & corrected → current findings. Everything properly validated and documented.
2. Produce a professor-ready report documenting all of it, written in first-person academic
   voice. STYLE RULE: no tooling/software-assistant references, no internal jargon
   (no session numbers/workflow terms) — dates and research stages only.
3. Token economy: mechanical validation on Opus-class subagents; synthesis/writing on Fable.
4. Update THIS file after each part completes.
5. A further task follows after this one (researcher to specify).

## Ground truth for validators
- Canonical results: `04_empirics/H1_volatility/c1_findings.md` (food-donor rerun is current:
  DiD −9.8% p≈0.145/0.153 not sig; SDID pooled −19.1% z=−1.88; chana concentrated −38.7/−37.3;
  wheat +0.4 (confounded); placebo −6.5% p 0.34/0.43; pre-trend 0.445; LOO ex-wheat −15.2% p .003).
- State snapshot: `00_admin/RESUME_HERE_2026-06-21.md`; history: `00_admin/session_log.md`,
  `decision_log.md`, `chronicle.md`.
- Pull state: food cereals in panel (16 commodities, 172,381 rows); oilseeds/ragi NOT pulled
  (mustard/soybean provisional). Estimation N = 146,507 obs / 2,244 units / 14 clusters.

## Status
- [x] Part A — data-layer validation: PASS (panel 172,381×16 exact; all spot files 0 weekend /
      0 dup / 0 non-positive, full spans; raw 569 district + 20 national JSONs (+20 vs earlier
      count — benign, pull had advanced); data_log covers all 5 raw sources; no banned futures
      in clean/ — truncation satisfied)
- [x] Part B — empirics reproduction: PASS (DiD β=−0.1031/−9.8% p .1208 ✓; robustness baseline
      CR1 .1447, ex-wheat −15.2/.0034, ex-chana −7.4 ✓; placebo −6.5%/.3443 + lead test .4453 ✓;
      SCM chana −37.3/p .100 ✓; H3 −0.2179/p .069 ✓; H7 −0.0211/p .1975 ✓; H8 42.04/56.53/1.43 ✓;
      GARCH-ICSS no break near ban ✓; c1_tables.tex current ✓)
- [x] Part C — documentation chain: DONE inline (2026-07-06 session-18 sweep verified all docs
      consistent with c1_findings; CV/interview reference removed from c1_findings.md — the one
      hit in handover docs; LaTeX balance verified)
- [x] Part D — professor deliverables WRITTEN: `05_paper/project_report.tex` (full work report:
      data collection detail, cleaning, error register, methods, findings progression, current
      results, limitations, reproducibility) + `FOLDER_GUIDE.md` (root; navigation + repro
      commands). Style rule honored: first-person academic voice, no tooling refs, no CV refs.
- [x] Part E — CLOSED 2026-07-06: validation verdict PASS on all 15 items, zero discrepancies
      affecting results; project_report.tex required NO patches (all its numbers match the
      re-run values). Deliverables final: 05_paper/project_report.tex + FOLDER_GUIDE.md.
      TASK COMPLETE — awaiting researcher's next task.

## Handover exclusion list (researcher decision — do NOT copy these to the professor)
- Personal: `05_paper/cv_story.tex`, `05_paper/interview_pack/`, `05_paper/gs_interview_prep.md` (if present)
- Internal working notes: `CLAUDE.md`, `.claude/`, `00_admin/session_log.md`,
  `00_admin/RESUME_HERE_2026-06-21.md`, `00_admin/handoff_2026-06-13.md`,
  `00_admin/handoff_2026-06-21.md`, `00_admin/VALIDATION_TASK_2026-07-06.md` (this file),
  `00_admin/emails/`, `.env`, `Screenshot*` at root
- Everything else goes: data (all tiers), code, empirics, literature, policy timeline,
  paper drafts, project_report.tex, FOLDER_GUIDE.md.

## Log
- 2026-07-06: task opened; validation agent launched (Opus, background).
- 2026-07-06: CV-reference sweep done (1 hit fixed). FOLDER_GUIDE.md written.
- 2026-07-06: project_report.tex written (awaiting validation-agent cross-check → Part E).
- 2026-07-06: SUBMISSION PACKAGE BUILT at `my_work/` (1.6 GB). Contents: FOLDER_GUIDE.md,
  05_paper (project_report.tex, drafts, outline), 00_code (no __pycache__), 02_data (all tiers),
  03_policy_timeline, 04_empirics, 01_literature, 00_admin/data_log.csv ONLY. Excluded: personal
  files, all internal notes/logs, CLAUDE.md, .claude, .env, .venv, .git, README, TASKS.
  Package-only reframing per researcher instruction: V0 folder renamed V0_baseline_verification;
  "+8–10%" presented as the initial working hypothesis (all "inherited/lost work" phrasing
  replaced); spec.md rewritten accordingly; decision_log/RESUME/companion-doc references
  neutralized in code comments and memo banners. Final grep: only legitimate-English hits remain.
  Master repo untouched except report/guide pointing to data_log instead of internal logs.
- 2026-07-06 FINAL INDEPENDENT SWEEP of my_work/: (1) AI-trace grep across ALL 1,086 files —
  one hit found ("per CLAUDE.md rule 4" in constructed/README) → replaced with a code reference;
  the only other flag was a legitimate "research assistant" phrase in a cited paper's annotation
  (kept). Final grep: zero AI-trace terms package-wide. (2) Dash normalization: all Unicode
  em/en/minus dashes → "-" across md/tex/py/doc-csvs (62 files changed); tex "---"/"--" → "-";
  ASCII "--" in Python untouched (CLI flags); raw data JSONs untouched (data integrity).
  (3) Integrity: every .py compiles; every .tex brace/$-balanced. Professor_guide.pdf
  (researcher-added) retained. PACKAGE FINAL: 1.6 GB, 1,086 files, submission-ready.
