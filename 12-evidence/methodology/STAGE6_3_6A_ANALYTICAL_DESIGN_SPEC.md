# Stage 6.3.6A — Analytical Design Specification (2026-09-17)

**This document computes nothing.** It defines populations, variables, exclusions, denominators
rules, missing-data treatment, lag treatment, the whitelist of permissible statistical
relationships, and interpretation boundaries — before any of it is applied to data. No query
against `outcomes.csv`, `government_support.csv`, or any Stage 6.3 output has been run to produce
this document; every number cited below is a previously frozen fact already reported in Stage
6.1/6.2/6.3, not a new calculation. Item 6B (execution) is a separate, later authorization and must
not begin until this specification itself is reviewed and frozen.

## 1. Analytical populations

Four distinct populations are defined. No analysis may mix them without saying which one it used.

| ID | Definition | Size (frozen, already reported) |
|---|---|---|
| **Pop-A** | Full government support register | 638 athletes / 1,108 support rows |
| **Pop-B** | Research cohort — the only population with any Stage 3-5 identity/outcome work | 75 athletes |
| **Pop-C** | Lag-eligible cohort — Pop-B athletes who have ≥1 support row qualifying under the Item-5 lag rule (`record_date`, `ALREADY_RECEIVING_BY_DATE`, or `EXPLICIT_ADDITION`) **and** ≥1 outcome row in the deduplicated 368-row major-games table | Not yet counted — sizing this is 6B's first step, not 6A's |
| **Pop-D** | State-comparison population — support rows whose `state_classification == CANONICAL` only | 582 rows (Item 1) |

**Explicit exclusion from every cohort-level population**: the 20 athletes in `IDENTITY_HOLD`
(Pop-A only, never enters Pop-B/C). Their identity conflicts are unresolved; including them would
silently launder an unresolved identity question into a population count.

Pop-C's size is deliberately left unstated here. Computing it now — before the design is frozen —
would let the population definition get quietly reshaped around whatever number looks analyzable,
which is the exact risk the 6A/6B split exists to prevent. If Pop-C turns out too small to support
a given test, that is a 6B finding to report as "cannot be estimated," not a 6A parameter to tune.

## 2. Variables permitted

**Support-side ("developmental support")**
- Restricted to rows with `accounting_stage` in `{SANCTIONED, RELEASED_PAID}` only.
- `CASH_AWARD_OUTCOME_LINKED` rows are **never** used as a support/input variable — they are an
  outcome-adjacent reward, not developmental input, per the standing rule reaffirmed in Item 2.
- `AMBIGUOUS` rows (386, 35% of all support rows) are excluded from any financial-intensity or
  support-presence variable. They may be reported as a separate coverage caveat ("N ambiguous-stage
  records also exist for this athlete/state, stage undetermined") but never folded into a count of
  confirmed support.
- No financial amount is ever summed across `amount_unit_verified == False` rows without flagging
  the unit-verification gap (carried over from the Stage 6.1 QA finding).

**Outcome-side**
- Restricted to the 368-row deduplicated major-games table (Olympics, Youth Olympics, Asian Games,
  Commonwealth Games only). The 693-row UNCLASSIFIED bucket is not used in any relationship
  variable, per Item 4.
- `medal` is kept as a categorical variable **per competition type**, never combined into a single
  cross-competition score (an Olympic medal and a Commonwealth Games medal are not equivalent and
  must never be added, weighted, or ranked together).
- `outcome_year` used only as the "after" side of a lag, per Item 5.

**Geography**
- `state_canonical` used only where `state_classification == CANONICAL`. `CITY_DISTRICT`,
  `AGGREGATE`, and `MULTI_STATE` rows are excluded from any state-level comparison, not
  approximated to a nearest state.

**Identity confidence**
- `identity_match_status_stage4` must be carried as a reported covariate on every cohort-level
  table, not filtered out silently. `REJECTED` athletes are excluded entirely from cohort analysis.
  `NEEDS_REVIEW` athletes are excluded from primary analysis and may only appear in an explicitly
  labeled sensitivity check, never blended into the primary N.

## 3. Exclusions (consolidated)

| Exclusion | Reason |
|---|---|
| `IDENTITY_HOLD` athletes (20) | Unresolved identity conflict |
| `REJECTED` identity match status | Wrong-candidate risk established at Stage 4 |
| `likely_duplicate_of_another_source == True` outcome rows | Same result double-counted |
| Outcome rows outside the 4 major-games categories | No defensible competition identity (Item 4) |
| `CASH_AWARD_OUTCOME_LINKED` support rows | Outcome-linked reward, not developmental input |
| `AMBIGUOUS` accounting-stage rows | Undetermined financial stage |
| Support rows with `date_type == snapshot_date` or `none` | Not eligible as an intervention-timing anchor (Item 5) |
| Non-`CANONICAL` state rows | Not a genuine, unambiguous state value (Item 1) |
| A7↔MDSD `MEDIUM`/`LOW` confidence matches, used as confirmed | Heuristic match, not a verified identity — usable only as flagged candidates |

## 4. Denominator rule

**Every reported statistic must carry its own N and its own coverage rate against the relevant
population above it in the table in §1.** There is no single project-wide N. A state-comparison
table's N is the CANONICAL-state row count for that specific variable, not 638, not 1,108. A
lagged-association table's N is Pop-C, sized at 6B execution time, not assumed in advance. Any
output that reports a percentage or count without also stating which population and which
exclusions produced it is non-compliant with this specification.

## 5. Missing-data treatment

- **No imputation, anywhere in this project.** This has been the de facto rule since Stage 1 and is
  now made explicit.
- Missing state, missing accounting stage, missing outcome, or missing date = **excluded from that
  specific analysis** and reported as a coverage/missingness rate. Never treated as zero, never
  treated as "no effect," never back-filled from a related record.
- The 15 of 75 cohort athletes with zero recovered outcome rows (Stage 6.2.4) are **missing data,
  not "no medal."** They must be excluded from any outcome-based comparison, never coded as a
  negative outcome or absence-of-success.
- Where a proposed table's usable N falls below a size that could support any meaningful
  comparison (no fixed threshold is set here — that judgment is made in the open, in 6B, with the
  actual N stated), the correct output is a stated conclusion that the relationship cannot be
  estimated from available evidence, not a table built anyway.

## 6. Lag treatment

Governed entirely by `stage6_3_normalization/TEMPORAL_MODEL.md`, frozen under Item 5. Restated for
completeness, not redefined:
- Only `record_date`, `ALREADY_RECEIVING_BY_DATE`, `EXPLICIT_ADDITION` support dates anchor a lag.
- `ALREADY_RECEIVING_BY_DATE` is an upper bound on start, labeled as such wherever used.
- Fixed windows: funding anchor → +1 / +3 / +5 years. No other window is authorized.
- Outcome-year dates are treated as genuine event dates, not subject to the same caveat.

## 7. Permissible statistical relationships (whitelist — nothing outside this list without new authorization)

1. **Descriptive state comparison** — counts/rates of Pop-D athletes and CANONICAL-state support
   records by state. Purely descriptive; no ranking, scoring, or "best state" framing of any kind.
2. **Lagged association** — presence of a qualifying support anchor (§2, §6) vs. presence of a
   major-games outcome within the fixed lag windows, for Pop-C. Reported as an association only
   (e.g. co-occurrence rate, not a slope, coefficient framed as effect size, or "impact").
3. **Infrastructure/access relationship** — A7/MDSD reconciled projects (HIGH-confidence matches
   only; MEDIUM/LOW reported separately as candidates) by state, set alongside Pop-D athlete
   density by state. Descriptive juxtaposition only — no claim that infrastructure caused athlete
   density or vice versa.
4. **Support/outcome relationship** — restricted to `{SANCTIONED, RELEASED_PAID}` support rows
   against the 368-row major-games outcome table, within Pop-C and the fixed lag windows. This is
   the relationship most exposed to reverse causation and selection (athletes already on a
   medal-contending track are more likely to receive TOPS-family support in the first place), and
   that confound must be stated every time this relationship is reported, not once in a methods
   footnote.

No composite index, no weighted score, no ranking of states/programmes/athletes, and no
aggregation across competition tiers is authorized under any of the four items above.

## 8. Interpretation boundaries

- **No causal language, anywhere.** Banned: "improves," "drives," "boosts," "leads to," "causes,"
  "produces better outcomes." Permitted: "is associated with," "co-occurs with," "athletes who
  received X in this dataset were more/less likely to have outcome Y, within the stated population
  and lag window."
- **"Cannot be estimated from available public evidence" is a valid, and preferred, output** over a
  proxy relationship that looks informative but doesn't survive scrutiny — restated per the user's
  original standing instruction.
- A HIGH-confidence A7↔MDSD match is a strong heuristic match, **not a confirmed identical
  project**, and must never be reported as verified in Item 6 output.
- Every table must carry its N, its population ID (Pop-A/B/C/D), and its exclusion list inline —
  not in a separate methods section a reader could miss.
- No statement may imply government support was the only or primary input to any athlete's
  outcome; the evidence in this project cannot support or rule out any other contributing factor.

## 9. What this document explicitly does NOT do

No population is sized beyond what was already frozen in Items 1–5. No relationship listed in §7
has been computed, previewed, or trial-run. No chart, table, or number describing any
support-outcome relationship exists yet. This is a rules document only, submitted for review before
Item 6B (execution) may begin.
