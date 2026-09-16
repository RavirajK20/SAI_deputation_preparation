# Stage 6.2 — Descriptive Evidence Audit (2026-09-17)

**What does the assembled evidence actually show?** Not "what story can we tell" — every number
below is a direct read of the five CSVs built alongside this report, restricted to fields the
Stage 6.1 QA pass marked strong enough to use. No charts. No correlations, causal claims, or
efficiency measures.

## Pre-step: `outcomes_join_audit.csv`

Of 1,098 outcome rows: **236 NATIVE_ID** (athlete_id carried directly in the source, Olympedia),
**102 MANUAL_VERIFIED_NAME** (the 6 Stage 5B-Part A athletes whose identity was discipline-
cross-checked, plus 5 Part-B athletes whose wrong-page bugs were caught and individually fixed),
**760 EXACT_CANONICAL_NAME** (joined by text match, not individually re-verified beyond the
aggregate spot-checks already done). This is the current provenance/confidence limitation
affecting roughly 70% of the outcome layer — not a defect introduced now, but made explicit rather
than left implicit in an `athlete_id` column that looked uniformly reliable.

## 6.2.1 — Support ecosystem (`stage6_2_support_ecosystem.csv`, 67 rows)

- **638 athletes total** in the government register; **75 (11.8%)** are in the research cohort
  with any Stage 3-5 identity/outcome work; **20 (3.1%)** are held in `IDENTITY_HOLD`, excluded
  from all cohort work pending manual resolution.
- **Identity readiness across all 638**: the A/B/C/D distribution is unchanged from Stage 1.5 —
  restated here for one-stop reference, not recomputed.
- **Programme categories**, by unique athlete count (not record count): Cash Award/Medal and
  TOPS-family sources have the broadest athlete reach; State Welfare and SAI Employment are
  narrower. Exact counts in the CSV — deliberately not summarized into one ranked list here, since
  "broadest reach" is a count, not an indication of importance.
- **Programme combinations**: most athletes appear under exactly one programme category; a smaller
  number appear under 2+ combinations (e.g. TOPS + Cash Award/Medal, TOPS + NSDF/Welfare). The
  15 most common combinations are listed in the CSV.
- **Discipline distribution**: reported as raw free text, explicitly NOT deduplicated across
  spelling variants (e.g. "boxing" and "Boxing" may both appear as distinct rows) — this table
  should not be read as a clean discipline count until that normalization is done.
- **Source-count distribution**: most athletes have 1-2 government sources; a small number have
  5+. Restated explicitly: **this is corroboration breadth, not an effectiveness or success
  signal** — a data-dictionary rule, not a new interpretation.

## 6.2.2 — Major-games outcomes (`stage6_2_major_games_outcomes.csv`, 368 rows, deduplicated)

Restricted to the 6 reliably-classified competition types (see correction note below; 36.9% of all
outcome data — the remaining 63.1% stays out of this table by design, per the QA finding). 405 raw
rows in these categories were deduplicated to 368 (37 duplicate copies removed, Olympedia kept as
the primary record where both sources described the same result).

**Correction (2026-09-17, disclosed, found during Stage 7 presentation-layer build)**: 16 of these
368 rows, belonging to 5 independently-identified para-sport athletes (Amit Kumar Saroha, Ajeet
Singh, Rubina Francis, Tarun Dhillon, Rakesh Kumar — each explicitly documented as a Para
Sports/Para Athletics/Para Shooting/Para Badminton/Para Archery athlete in
`identity_evidence.csv`'s Stage 5B verification-basis text), were originally labeled "Olympics" or
"Asian Games" instead of "Paralympics" or "Asian Para Games." The cause: Stage 6.1's competition-type
classifier matched host-city + year text alone (Paris hosted both the 2024 Olympics and 2024
Paralympics; Incheon/Jakarta/Hangzhou each hosted both the Asian Games and the Asian Para Games in
2014/2018/2022 respectively) without cross-referencing the athlete's own already-correct para-sport
identity evidence. Found and corrected via
`tools/stage6_correction_paralympic_reclassification.py` — exhaustive, not sampled: every
Olympics/Asian-Games-labeled row belonging to a para-flagged athlete was checked, all 16 corrected,
none left ambiguous. The table below reflects the corrected labels; the previous version of this
report (218/76 Olympics/Asian Games rows) is superseded.

**Medals, kept separate by competition type, never summed into one score:**

| Competition | Rows | Gold | Silver | Bronze |
|---|---|---|---|---|
| Olympics | 215 | 1 | 2 | 28 |
| Paralympics | 3 | 0 | 1 | 2 |
| Youth Olympics | 20 | 3 | 5 | 0 |
| Asian Games | 63 | 26 | 12 | 25 |
| Asian Para Games | 13 | 5 | 4 | 4 |
| Commonwealth Games | 54 | 23 | 27 | 4 |

These are row counts (an athlete can appear more than once per competition type across different
editions/events), not unique-athlete or unique-medal counts — read accordingly. No combined total
is presented, per explicit instruction; a Gold at the Commonwealth Games and a Gold at the Olympics
are not being treated as equivalent achievements anywhere in this table. Olympics and Paralympics
are kept as separate rows for the same reason — they are different competitions with different
eligibility criteria, and a Paralympic medal must never be counted toward an "Olympics" total.

## 6.2.3 — Chronology map (`stage6_2_chronology.csv`, 75 rows, every athlete named)

| Category | Count | Meaning |
|---|---|---|
| `EXPLICIT_ADDITION` | 2/75 | Atanu Das, Mehuli Ghosh — documented addition/re-inclusion event, not proven first-ever |
| `DATED_ANCHOR_NOT_START` | 17/75 | A real date exists confirming support was active on that date; start date unknown |
| `SNAPSHOT_ONLY_NO_GENUINE_DATE` | 56/75 | Only a dataset-publication date exists; no evidence of when support began or was confirmed active |
| **First-ever support date established** | **0/75** | Not achieved for any athlete, including the 2 explicit-addition cases |

This table is the clearest single communication of what the earlier framing called "the
observability of the government-to-athlete pathway" — 74.7% of the cohort has no dated anchor of
any kind beyond a dataset's own publication date.

## 6.2.4 — Evidence-quality layer (`stage6_2_evidence_quality.csv`, 13 rows)

- **Outcome corroboration**: the primary source for all 1,098 outcome rows is Tier 3; **2 rows
  (0.18%)** additionally have independent Tier-1 government corroboration (Rakesh Kumar's and
  Rubina Francis's 2022 Asian Para Games medals).
- **Outcome source tier**: 100% of outcome data is currently Tier 3 (Olympedia or Wikipedia) —
  no Tier-1 government source has been used as the primary outcome source for any row.
- **Duplicate flag**: 72 of 1,098 rows (6.6%) are flagged as describing the same real-world result
  as another row.
- **Identity match status** (75 cohort athletes): the PROBABLE/NEEDS_REVIEW/REJECTED/
  NO_OLYMPEDIA_COVERAGE distribution from Stage 4/5B, restated here. **0 are VERIFIED** — no
  government DOB exists for this cohort to cross-check against.
- **Outcome coverage**: **60 of 75 cohort athletes (80%) have at least one recovered outcome row;
  15 (20%) have zero** — these 15 are not "unsuccessful athletes," they are athletes for whom no
  outcome source in this project's current acquisition returned a match (see Stage 4/5B notes for
  the specific reasons per athlete: NEEDS_REVIEW ambiguity, REJECTED wrong-candidate, or genuine
  source-coverage gaps).
- **Chronology coverage**: restated from 6.2.3 for one-stop reference — 19/75 dated anchor, 2/75
  explicit addition, 0/75 first-ever support date.

## What this audit does NOT do

No ranking of states, programmes, or athletes. No financial totals (explicitly deferred pending
the unit/provenance fix). No combined medal score. No claim about which programme "produces"
outcomes. No statement stronger than what a specific table cell directly shows. Interpretation —
deciding what these numbers mean for policy — is explicitly out of scope for this report, per the
instruction to describe before interpreting.
