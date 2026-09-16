# Stage 6.3 — Analytical Relationships, Pre-Analysis Phase (2026-09-17)

Per authorized scope: items 1–5 only. **Item 6 (analytical design) is explicitly NOT started** and
awaits separate authorization. No charts, correlations, rankings, financial aggregation, or policy
recommendations appear anywhere below. All outputs live in
`analysis/stage6/stage6_3_normalization/`.

## Item 1 — State crosswalk (`tools/stage6_3_state_crosswalk.py`)

Classified all 45 distinct raw `state_raw` values from `government_support.csv` into
CANONICAL / MULTI_STATE / CITY_DISTRICT / AGGREGATE / UNRESOLVED. Raw values preserved throughout.

- By distinct value: 32 CANONICAL, 10 CITY_DISTRICT, 3 AGGREGATE, 0 UNRESOLVED.
- By row (1,108 total): 582 CANONICAL, 496 BLANK (no state field in that source record — expected,
  not an error), 17 AGGREGATE, 13 CITY_DISTRICT.
- Outputs: `state_classification_lookup.csv`, `government_support_state_normalized.csv`.

## Item 2 — Accounting-stage normalization (`tools/stage6_3_accounting_stage.py`)

Classified every (programme_source_id, amount_field_source) pair into SANCTIONED /
RELEASED_PAID / CASH_AWARD_OUTCOME_LINKED / AMBIGUOUS / NOT_FINANCIAL / NO_AMOUNT, based on field
name and, where the field name alone is silent, the original dataset title. Reasoning recorded per
pair, not guessed silently.

- By row: 386 AMBIGUOUS (35% — field names/titles genuinely do not disclose the stage; left
  explicit rather than assumed), 318 RELEASED_PAID, 192 CASH_AWARD_OUTCOME_LINKED, 60 SANCTIONED,
  76 NO_AMOUNT, 76 NOT_FINANCIAL.
- The 192 outcome-linked cash-award rows are now structurally isolated and flagged
  (`is_outcome_linked_cash_award`) — these must never be summed into a "developmental support"
  total in any future stage, per the standing rule.
- Outputs: `government_support_accounting_normalized.csv`, `accounting_stage_lookup.csv`.

## Item 3 — A7 vs MDSD infrastructure reconciliation (`tools/stage6_3_infra_reconciliation.py`)

No shared project ID exists between the two sources, so this is a heuristic match — normalized
state + sanction-year proximity + project-description token overlap + amount proximity — explicitly
confidence-graded, **not a forced merge**. Both source files are untouched; only a mapping table
is produced (`a7_mdsd_reconciliation.csv`, 143 rows).

**Row-accounting audit (corrected)** — traced directly from the raw source file
(`RS_Session_248_AU_920.1.B.csv`), because the first version of this report gave an internally
inconsistent derivation ("146 raw rows... 3 header-adjacent noise") that did not reconcile with the
143-row reconciliation population. The correct derivation:

```
148 raw physical CSV records (csv.reader, embedded-newline-safe)
−  1 header row
= 147 data rows
−  4 subtotal/"Total" rows (one per fiscal year: 2015-16, 2016-17, 2017-18, 2018-19)
−  0 other non-project rows (verified: 0 blank Sl. No., 0 non-numeric Sl. No.,
     0 duplicate (Year, Sl. No.) pairs among the remaining rows)
= 143 genuine A7 project rows
```

There is no "header-adjacent noise" category — that line in the original report did not correspond
to anything actually present in the data and has been removed. The two-step subtraction (147 − 4 =
143) fully and exactly accounts for the population.

**Correction log** — during row-level review, one state-alias gap was found: A7's `"Jammu &
Kashmir"` was not mapped to MDSD's `"Jammu and Kashmir"` string, causing one genuine match to be
missed. Adding that alias moved the match distribution from **119 HIGH / 6 MEDIUM / 1 LOW / 17
NO_MATCH** (first run) to **120 HIGH / 6 MEDIUM / 1 LOW / 16 NO_MATCH** (current, reported below).
This is a one-row reconciliation correction, not a re-run of the matching algorithm — no other
matching logic was changed.

- **120 HIGH** confidence matches (near-identical project text, same state/year, amount matches or
  very close) — spot-checked manually, hold up.
- **6 MEDIUM**, **1 LOW** confidence — text overlap exists but is not strong enough to treat as
  confirmed; one MEDIUM case ("Upgradation of Hockey Astroturf" vs "Upgradation of Shooting range"
  at the same stadium/year) is flagged specifically as a likely **false-positive risk** — same
  venue and year, different project type. MEDIUM/LOW rows should be treated as candidates needing
  human review, not as established matches.
- **16 NO_MATCH**, of which **13 are structurally explained, not a matching failure**: they are all
  from A7's 2015-16 cohort, and MDSD's earliest sanction date in the entire 349-row register is
  2017-02-09 — **MDSD's project register does not cover 2015-16 at all**. This is a genuine
  coverage-boundary finding, not noise.
- **3 remaining NO_MATCH** rows fall inside MDSD's covered date range (2017-18, 2018-19) and are
  genuinely unresolved — either projects not present in MDSD's current register, or projects
  whose text diverges too far from any MDSD entry for this matching approach to find (e.g. a
  multi-site aggregate project, "Development of playfields (17) in different schools/locations in
  Rajasthan," which may map to several MDSD rows rather than one). Left as NO_MATCH rather than
  forced onto a weak candidate.
- **Conclusion, per instruction to preserve both datasets rather than force a unified history**:
  A7 and MDSD are best treated as two overlapping-but-not-identical views of the same underlying
  infrastructure programme — MDSD is the more current and more complete register from ~2017
  onward, A7 is the only source with 2015-16/2016-17 coverage. Any future infrastructure-access
  analysis must draw on BOTH, explicitly, rather than picking one as canonical.

## Item 4 — Outcome/competition-type normalization

The major-games dedup itself was already completed in Stage 6.2 (368 rows from 405, reused as-is,
not rebuilt). This item asked whether the remaining 693 UNCLASSIFIED rows (63.1% of all 1,098
outcome rows) could be defensibly assigned to a controlled taxonomy (e.g. World Championships,
World Cup, Asian Championships).

**Finding: no.** Checked all 693 UNCLASSIFIED rows' raw competition text
(`competition_raw_text`) for any actual competition-name keyword (championship, world cup, world
championships, asian championship, national games, world para, grand prix, trophy, open, etc.) —
**zero genuine hits** (one apparent hit, "Copenhagen," was a false positive from "open" appearing
inside the city name). The underlying source rows (675 of 693 from
`OUTCOME_ROWS_WIKIPEDIA_ENRICHMENT.csv`, 18 from the Part-A targeted table) carry only a host city,
year, and (for para-sport rows) an event classification code — e.g. `'Suhl Individual'`, `'Doha
Javelin throw F46'` — never the tournament name itself.

Assigning these to a taxonomy would require **new external research** (a host-city+year+sport
lookup against known championship calendars) to reconstruct what tournament each row belongs to —
this is source-acquisition work, not normalization of data already in hand, and is explicitly out
of scope for Stage 6.3. Per the standing methodological rule, this is reported as a genuine
evidence gap rather than bridged with an unverified guess: **the 693-row UNCLASSIFIED bucket stays
UNCLASSIFIED**, and any future outcome analysis is restricted to the 405-row (368 deduplicated)
major-games layer already validated in Stage 6.2, unless a future stage explicitly authorizes new
research to reconstruct competition identity for the rest.

## Item 5 — Temporal model (`stage6_3_normalization/TEMPORAL_MODEL.md`)

Rules only, decided before any lag is computed, per instruction. Full document at the path above;
summary:

- Only `record_date`, `ALREADY_RECEIVING_BY_DATE`, and `EXPLICIT_ADDITION` support-side dates may
  anchor intervention timing; `snapshot_date` (666 of 1,108 rows) and rows with no date at all (222
  rows) may not — this extends the same rule already established for the 75-athlete cohort in
  Stage 5A/6.2 to the full 1,108-row support table.
- `ALREADY_RECEIVING_BY_DATE` anchors are upper bounds on the true start, not the true start
  itself, and must be labeled as such wherever used.
- Candidate lag windows fixed in advance: **+1, +3, +5 years** from a genuine support anchor to an
  outcome year. No other window is pre-authorized.
- Coverage consequence stated explicitly: only 220 of 1,108 rows (19.9%) qualify as lag-eligible at
  all; 151 of those give an actual date rather than an upper bound. Any future lagged analysis runs
  on this small, non-random subset — a limitation to disclose, not to route around.

## What remains frozen

Item 6 (analytical design: descriptive state comparisons, lagged associations, infrastructure/
access relationships, support/outcome relationships) is **not started** and requires separate
authorization, per the user's explicit staging. Stage 6.2 remains frozen as previously agreed. No
new charts, correlations, rankings, financial aggregation, or policy recommendations were produced
in this stage.
