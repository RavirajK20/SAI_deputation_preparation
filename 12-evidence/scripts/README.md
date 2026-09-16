# Reproducibility scripts

These are copies of the two scripts that produced this module's data, reproduced here for
auditability. They run against the full `sports-analytics/` project (frozen Stage 6/6.3/6B CSVs),
which is not part of this repository — they are included so a reviewer can see exactly how every
number in `12-evidence/` was derived, not as standalone executables.

- `stage6_correction_paralympic_reclassification.py` — a narrow, disclosed correction to 16 of
  1,098 outcome rows (5 para-sport athletes) in the frozen Stage 6.1 `outcomes.csv`, found during
  this module's build. Stage 6.1's competition-type classifier matched host-city + year text alone
  and mislabeled 3 Paralympic and 13 Asian Para Games results as "Olympics"/"Asian Games". This is a
  targeted classification fix (16 specific rows, individually verified against each athlete's own
  already-correct para-sport identity evidence) — **it is not a new analytical methodology**, and it
  does not change any frozen 6B finding (6B-4 was re-run afterward and produced an identical 0/16
  result). Full disclosure: `12-evidence/methodology/STAGE6_2_DESCRIPTIVE_REPORT.md` §6.2.2 and
  `12-evidence/methodology/6B6_ANALYTICAL_VALIDITY_AUDIT.md` §6B.
- `stage7_export_presentation_data.py` — reads only the (corrected) frozen Stage 6/6.3/6B CSV
  files and writes the JSON files under `12-evidence/data/`. It performs no analysis of its own —
  every figure it emits already exists in a named source file, selected and formatted only.
