# Stage 6.3, Item 5 — Temporal Model (rules only, not yet applied to data)

Defines the permissible lag structures for any future lagged-association analysis, decided
**before** looking at results, per explicit instruction. This document sets rules; it does not
run any analysis, and no analytical output in this repository yet uses it.

## 1. What can and cannot anchor "intervention timing"

Every date associated with a government_support or identity_evidence row falls into one of the
evidence types already established in Stage 5A/6.2 (`date_type` field, `government_support.csv`,
1,108 rows):

| date_type | Count | Usable as intervention-timing anchor? |
|---|---|---|
| `record_date` | 144 | **Yes** — a genuine event date tied to that specific record |
| `ALREADY_RECEIVING_BY_DATE` | 69 | **Yes, as a lower bound only** — confirms support was active by this date; true start may be earlier |
| `EXPLICIT_ADDITION` | 7 | **Yes** — a documented addition/re-inclusion event |
| `snapshot_date` | 666 | **No** — this is the date the source *dataset* was published/extracted, not a date on which anything happened to the athlete. Using it as a funding-year anchor would silently convert "we don't know when this started" into a specific calendar year, manufacturing precision the evidence doesn't have. |
| `none` | 222 | **No** — no date evidence exists at all for these rows |

This mirrors the chronology categories already reported in Stage 6.2.3 for the 75-athlete cohort,
restated here as a row-level rule for the full 1,108-row support table.

**Rule 1**: A funding/support record may only serve as the "before" side of a lag if its
`date_type` is `record_date`, `ALREADY_RECEIVING_BY_DATE`, or `EXPLICIT_ADDITION`. A
`snapshot_date`-only record is not eligible, full stop — it can be reported as "support existed by
[snapshot date]" but never as "support began in [year]."

**Rule 2 (corrected 2026-09-17 — see 6B-4 execution note)**: `ALREADY_RECEIVING_BY_DATE` anchors
define a lag window's *latest possible* start, not its actual start: the true start is on or
before this date, but could be earlier by an unknown amount. Treating this date as if it were the
true start therefore produces a lag that is a **lower bound** on the true lag (true lag ≥ computed
lag) — the true lag can only be as long or longer, never shorter, because an earlier true start
only stretches the gap to the outcome. (An earlier version of this rule stated the inequality
backwards, "true lag ≤ computed lag"; that was an arithmetic error, caught and corrected before any
lag was computed against real data — see the 6B-4 execution report for the verification.)

**Practical consequence for 6B-4**: an `ALREADY_RECEIVING_BY_DATE` anchor can be used to confirm
that a pair falls **outside** a lag window (if computed lag already exceeds the window, true lag
exceeds it too), but can **never** be used to confirm a pair falls **inside** a window — the true
lag might still exceed the window even when the computed lag does not. Such pairs must be reported
as indeterminate, not counted as a confirmed within-window co-occurrence.

## 2. Outcome-side dates

Outcome rows (`outcomes.csv`) carry `outcome_year`, sourced from Olympedia/Wikipedia competition
records — these are genuine event dates (the year a competition was actually held), not snapshot
dates, and are usable on the "after" side of a lag without the same caveat. This is a different
evidentiary category from the support side, and the asymmetry itself should be stated wherever a
lag is reported: the "before" side is frequently uncertain, the "after" side is generally solid.

## 3. Candidate lag windows

Per the user's own suggested structure, the following windows are defined as the only ones this
project will test if/when Item 6 (analytical design) is authorized:

- **funding year → +1 year**: outcome observed within 1 year of a genuine support anchor
- **funding year → +3 years**: within 3 years
- **funding year → +5 years**: within 5 years

No other window (e.g., +2, +10, "ever after") is pre-authorized. If a future stage wants a
different window, that is a new methodological decision to make explicitly, not an ad hoc choice
made after seeing which window produces the cleanest-looking result — the entire point of freezing
this now, before Item 6, is to prevent that.

## 4. Coverage consequence (stated honestly)

Applying Rule 1 to the full support table: only **220 of 1,108** support rows (19.9%) carry a
date type eligible to anchor a lag at all. Of those, only 151 (144 `record_date` + 7
`EXPLICIT_ADDITION`) give an actual date rather than an upper-bound. This means any future lagged
analysis will necessarily run on a small, non-random subset of the data — a coverage limitation to
be stated in any Item 6 output, not something to route around by loosening the rule above.

## 5. Explicitly out of scope for this document

No lag is computed here. No association between any support record and any outcome is calculated
or implied. This is a rules document only, per the user's framing: "Define the permissible lag
structures before looking at results."
