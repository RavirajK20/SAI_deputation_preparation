# 6B-6 — Analytical Validity Audit (2026-09-17)

A critical review of 6B-1 through 6B-5's execution, not new computation. The specification (6A) was
executed literally throughout — no population, variable, or exclusion rule was changed in response
to an intermediate result. This audit surfaces what the results themselves imply about the
evidence base's limits.

## 1. Coverage: how much of the 638-athlete register do any of these findings touch?

Every relationship in 6B-2 through 6B-5 ultimately traces back through Pop-B-primary (71) or Pop-C
(16), both drawn from the 75-athlete research cohort — the only population with Stage 3-5
identity/outcome work. **71/638 = 11.1%** of the full government support register has any
identity-verified outcome linkage at all; **16/638 = 2.5%** is lag-eligible. Any finding from 6B-4
or 6B-5, positive or null, describes at most 2.5% of the register and must not be generalized
beyond it. Pop-D (6B-2/6B-3) is larger (341/638 = 53.4%) but is a geography-only population — it
carries no outcome or identity information and cannot be combined with the 6B-4/6B-5 findings
without conflating two different populations, which this project has not done.

## 2. 6B-4's null finding: mechanism, not just magnitude

0/16 athletes showed a confirmed within-window co-occurrence at any of +1/+3/+5 years. This
traces to a specific, checkable mechanism, not an arbitrary small-sample fluke:

- Only 2 of Pop-C's 16 athletes have an `ACTUAL_DATE` anchor at all (both `EXPLICIT_ADDITION` —
  consistent with the Stage 6.2 finding that exactly 2/75 cohort athletes have a documented
  addition event). For both, the anchor date (2023) is **later** than every one of their major-games
  outcomes (2010–2022) — the computed lag is negative in all 14 pairs. This means the
  `EXPLICIT_ADDITION` event these two athletes have on record is not their first support date; it
  is a later re-addition/continuation event, occurring after the results it might naively be
  compared against.
- The remaining 14 athletes have only `ALREADY_RECEIVING_BY_DATE` (upper-bound) anchors, which —
  per the corrected Rule 2 (§below) — structurally cannot confirm a within-window result.

**Validity implication**: passing the Item-5 "genuine date" eligibility test guarantees the date is
real, not that it represents what a lag analysis needs it to represent (a support *start*). This is
a general risk for any future use of `EXPLICIT_ADDITION` dates as a proxy for "support began here" —
worth flagging for any future stage, not just this one.

## 3. A correction made during 6B-4, disclosed here

While implementing 6B-4, a directional error was found in the frozen `TEMPORAL_MODEL.md` (Item 5,
approved 2026-09-17): Rule 2 stated "true lag ≤ computed lag" for `ALREADY_RECEIVING_BY_DATE`
anchors. Verified numerically (an athlete confirmed receiving support by 2018 with a true start
anywhere at or before 2018 necessarily has a true lag to a 2020 outcome that is **greater than or
equal to** the lag computed from 2018, never less) — the correct direction is **true lag ≥ computed
lag**. `TEMPORAL_MODEL.md` has been corrected in place with the verification shown; the practical
consequence is more conservative than the original (wrong) rule, not less: an upper-bound anchor
can only be used to confirm a pair is *outside* a window, never *inside* one. 6B-4 was implemented
using the corrected rule throughout — this was caught before any lag was computed against real
data, not after.

## 4. 6B-5's structural null: financial timing is currently unobservable for this population

0 of Pop-C's 16 genuinely-dated support rows carry a `SANCTIONED`/`RELEASED_PAID` accounting stage
— all 16 are `NOT_FINANCIAL` (PIB batch-release/induction events). The athletes for whom this
project has a genuine date are systematically not the athletes for whom this project has a
determined financial stage. This is a coverage gap in the underlying government sources, not a
methodology artifact: financial disbursement records in this dataset are overwhelmingly
`snapshot_date`-only (666/1,108 rows project-wide), while genuine dates cluster in the smaller,
separately-sourced PIB induction-event records. **A support/outcome relationship restricted to
genuinely-timed financial support cannot currently be estimated from the available public
evidence** — the correct conclusion per the standing methodological rule, not a result to route
around.

## 5. 6B-3's known matching-quality issue (surfaced during execution, not previously reported)

3 of the 120 HIGH-confidence A7↔MDSD matches (2.5%) target an MDSD project that a second A7 row
also matched HIGH — the frozen Item-3 algorithm scores each A7 row independently and does not
enforce a 1-to-1 constraint. In all 3 cases the higher-scoring match is very likely correct and the
lower-scoring one very likely a false match reusing the same target (see `6B3_QA_LOG.txt` for the
specific rows). This affects at most 3 of 143 A7 projects (2.1%) and does not materially change the
state-level counts in `6B3_infrastructure_access.csv`, but it is a concrete, real illustration of
the safeguard the user asked to preserve: **a HIGH match score is a strong heuristic, not a
verified identical project**, and should be read that way in any future use of this table.

## 6. Confounding, restated for the record (not a new finding — required by spec §7 item 4)

Even where 6B-5 had produced a non-null result, any support/outcome co-occurrence in this dataset
would be confounded by reverse causation and selection: athletes already on a medal-contending
track are more likely to receive TOPS-family and similar support in the first place. Nothing in
this project's evidence base can separate "support contributed to the outcome" from "the athlete
was already on a trajectory that attracted both the support and the outcome." This applies
regardless of what 6B-5 found, and is not diminished by the fact that 6B-5 in fact found nothing to
interpret.

## 6B. Post-freeze correction log (added 2026-09-17, during Stage 7 build)

**Paralympics/Asian Para Games mislabeling, found and corrected.** While building the Stage 7
presentation layer, 16 of the 368 major-games outcome rows (5 para-sport athletes) were found
labeled "Olympics"/"Asian Games" instead of "Paralympics"/"Asian Para Games" — a Stage 6.1
classification gap (host-city+year matching without cross-referencing the athlete's own already-
correct para-sport identity evidence). Corrected via
`tools/stage6_correction_paralympic_reclassification.py`, exhaustively verified (all 16
Olympics/Asian-Games rows belonging to para-flagged athletes checked, not sampled). Full disclosure
in `STAGE6_2_DESCRIPTIVE_REPORT.md` §6.2.2. One affected athlete (Tarun Dhillon, ATH-0336) is in
Pop-C; 6B-4 was re-run after the correction and produced an **identical result** (0/16 confirmed
within-window co-occurrence at all three lag windows) — the correction changes a display label
only, not any frozen analytical finding. No other 6B output was affected (6B-1, 6B-2, 6B-3, 6B-5 do
not use `competition_type_normalized`).

## 7. What 6B did NOT do

No population, variable, or exclusion rule was adjusted based on an intermediate result. No
alternative lag window, accounting-stage inclusion, or state classification was substituted after
seeing a small N. No chart, ranking, or composite score was produced. No causal or near-causal
language was used to describe any 6B-2 through 6B-5 output.

## 8. Summary table

| Step | Population | Result | Status |
|---|---|---|---|
| 6B-1 | Pop-A/B/C/D constructed | 8/8 QA checks pass | Complete |
| 6B-2 | Pop-D (582 rows / 341 athletes) | Descriptive counts by state, alphabetical, no ranking | Complete |
| 6B-3 | A7 (143) + MDSD-only (232) by state, vs. Pop-D density | Descriptive juxtaposition; 1 matching-quality caveat surfaced | Complete |
| 6B-4 | Pop-C (16 athletes, 99 pairs) | **0/16 confirmed within-window co-occurrence at +1/+3/+5y** — explained by mechanism in §2 | Complete, null |
| 6B-5 | Pop-C ∩ {SANCTIONED, RELEASED_PAID} | **0 eligible rows — cannot be estimated** (§4) | Stopped, per instruction |
| 6B-6 | This audit | 1 frozen-document correction, 1 new matching-quality finding, coverage/confounding restated | Complete |

No presentation layer (charts, dashboards, or visual summaries) has been produced at this stage, per
explicit instruction — this is the raw analytical record, including the null and stopped branches,
for review before any decision about what (if anything) deserves visualization.
