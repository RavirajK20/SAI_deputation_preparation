# Stage 7 — Final Presentation Architecture (2026-09-17)

**Status: FROZEN (2026-09-17), after 3 mandatory pre-build corrections applied in place — see the
Evidence Gap staircase (§4) and Policy Question #1 (§3), both marked "Correction applied"/"Corrected
pre-build" inline. Implementation is authorized against this frozen version.** This document
resolves the five open questions from
`STAGE7_PRESENTATION_DESIGN_REVIEW.md`, incorporates the user's narrative-balance refinement, the
redesigned Evidence Gap staircase, the interactive Policy Question → Evidence → Answerability
model, the methodological athlete curation, and the A7/MDSD collision as an audit demonstration.
Per instruction, this is a second gate: implementation begins only after this document is reviewed
and frozen.

## Reconciling the two section lists in the authorization message

The user's message contains two overlapping structures: an 11-beat narrative sketch ("01 The
Question" … "11 Evidence Ledger") offered as reasoning, and an explicit approval of "Claude's
11-section architecture essentially as written" (the 0–10 list from the design review). The second
is the one explicitly approved, so it is the frozen backbone below. The finer narrative beats from
the first list (Geography, The Time Problem, The Analytical Test, The Answerability Matrix) are not
lost — they are sequenced as internal beats inside sections 4, 6, 7 and 8 respectively, noted
explicitly at each section below so the mapping is auditable rather than silently merged.

## The narrative spine (governs every section's copy, not just the opening)

Every section must resolve through this arc, per the user's explicit refinement — never "here's why
the data is bad":

> **What the evidence establishes → what it reveals → where it stops → what would make the next
> question answerable.**

Concretely, no section may end on a limitation alone. A limitation is always followed, in the same
visual unit, by either (a) what it reveals about the system's data architecture, or (b) a link
forward to §9 (Evidence Architecture Recommendations). This is the operational fix for "avoid making
limitations look like disclaimers" — it is a copy rule, not just a visual one.

---

## 1. Final narrative sequence

| § | Title | Core content | Narrative-beat mapping from the user's sketch |
|---|---|---|---|
| 0 | **The Question** | Tension statement (design review §2); "what does India's sports system need to know to manage itself" | = "01 The Question" |
| 1 | **The System** | Institutional map: MYAS → SAI → schemes → athletes → competitions; state governments → infrastructure → access, kept as a visually separate branch | = "02 The System" |
| 2 | **The Evidence Base** | Population funnel 638→75→71→16→2, tiered counters | = "03 The Evidence" |
| 3 | **Government Support Ecosystem** | Programme composition; developmental support vs. outcome-linked cash award split | contributes to "04 The Athlete" (system-level half) |
| 4 | **Infrastructure** | A7/MDSD three-way split, state ledger, restrained dot-map, collision audit demo | = "06 The Infrastructure Record"; the geography beat ("05 The Geography") is the state-ledger/dot-map sub-view inside this section, not a separate top-level section — infrastructure and athlete-density geography are the same underlying "where is evidence observable" question and splitting them would duplicate the state ledger |
| 5 | **Athlete Evidence** | 6 curated profiles (methodological selection, below) | = "04 The Athlete" (human half) |
| 6 | **The Evidence Gap** | The branching staircase (redesigned per user's diagram) | = "07 The Time Problem" is the staircase's second half (support timing → financial timing → longitudinal linkage) |
| 7 | **Findings** | 0/16 with mechanism; financial relationship not estimable, zero-overlap framing; confound restated | = "08 The Analytical Test" |
| 8 | **Policy Question → Evidence → Answerability** | Interactive click-through module, promoted to headline, 4-5 real questions | = "09 The Answerability Matrix" |
| 9 | **Evidence Architecture Recommendations** | "If we wanted to answer this properly" — general data-design principles | = "10 The Data Architecture Insight" |
| 10 | **Methodology / Evidence Ledger** | Full drill-down: 6A spec, exclusions, source tiers, provenance, temporal model, A7/MDSD detail, known limitations | = "11 Evidence Ledger" |

---

## 2. Exact visualizations, with exact data source per visualization

Every number on the page must be traceable to one of these. No visualization may be hand-authored
from memory of a frozen report — all data ships as small JSON/CSV exports regenerated from these
files by a thin export script (see §11).

| Visualization | Section | Exact source |
|---|---|---|
| Population funnel (638→75→71→16→2) | 2, referenced again in 7 | `analysis/stage6/athletes.csv` (638, 75 via `in_75_research_cohort`), `analysis/stage6/stage6_3_6b_execution/pop_b_primary.csv` (71), `pop_c_lag_eligible.csv` (16, plus `n_with_actual_date` column for the 2) |
| Institutional system map | 1 | Not a frozen dataset — hand-authored static diagram from the project's own documented institutional structure (MYAS/SAI/schemes as named throughout `analysis/stage6/*` programme_category values); **must be labeled as an orienting diagram, not a data visualization**, since it has no row-level source file |
| Programme-category composition (record counts, unique-athlete counts) | 3 | `analysis/stage6/stage6_2_support_ecosystem.csv` (sections `programme_category`, both `by-record` and `unique_athletes` rows) |
| Developmental support vs. outcome-linked cash award split | 3 | `analysis/stage6/stage6_3_normalization/accounting_stage_lookup.csv` + `government_support_accounting_normalized.csv` (`accounting_stage`, `is_outcome_linked_cash_award`) |
| State Evidence Ledger (alphabetical, sortable) | 4 | `analysis/stage6/stage6_3_6b_execution/6B2_state_descriptive.csv` (support records/athletes by state) + `6B3_infrastructure_access.csv` (A7/MDSD-only project counts by state) |
| Optional dot-map | 4 | Same as above, plotted by state centroid; **counts only, never a filled/graduated choropleth** |
| A7 ↔ MDSD three-way split + collision audit demo | 4 | `analysis/stage6/stage6_3_normalization/a7_mdsd_reconciliation.csv` (match_confidence groups) + `analysis/stage6/stage6_3_6b_execution/6B3_QA_LOG.txt` (the 3 named collision cases: MDSD #290/#320/#24) |
| Curated athlete profiles (6) | 5 | See §curation table below — each profile's exact source rows named per athlete |
| Evidence Gap branching staircase | 6 | Coverage figures at each transition sourced from: `stage6_2_evidence_quality.csv` (outcome coverage 60/75), `identity_evidence.csv` (`has_dated_government_support_anchor`/`has_explicit_addition_event`, 19/75), `pop_c_lag_eligible.csv` (16/71, 2/16 actual-date), `6B5_QA_LOG.txt` (0 eligible financial rows) |
| "Observability" coverage bars (data-availability framing, never performance) | 6 | Same sources as the staircase, re-expressed as proportions against their correct denominator (see §5 for the denominator-labeling rule) |
| 0/16 finding + mechanism | 7 | `analysis/stage6/stage6_3_6b_execution/6B4_lagged_association_pairs.csv` and `6B4_QA_LOG.txt` |
| Financial relationship zero-overlap diagram | 7 | `6B5_QA_LOG.txt` / `6B5_eligible_support_rows.csv` (0 rows) |
| Policy Question → Evidence → Answerability module (4-5 questions) | 8 | Hand-curated question text, each answerability verdict traceable to the specific frozen finding named in §4 below — **no new computation, this section only re-presents already-frozen 6A/6B results as an interaction, it does not run new queries** |
| Evidence Architecture Recommendations | 9 | Not data-sourced — general principles, explicitly framed as such (see §5) |
| Methodology / Evidence Ledger | 10 | Direct links/embeds of `STAGE6_3_6A_ANALYTICAL_DESIGN_SPEC.md`, `TEMPORAL_MODEL.md`, `STAGE6_3_NORMALIZATION_REPORT.md`, `6B6_ANALYTICAL_VALIDITY_AUDIT.md`, `6B_ACCEPTANCE_AND_PERMANENT_CAVEATS.md` |

### Athlete curation table (§ Athlete Evidence, methodological selection)

The user's six evidence-situation categories, each grounded in a real, checked candidate. Two
categories both trace to the project's only `EXPLICIT_ADDITION` cases (2/75, Atanu Das and Mehuli
Ghosh) — this overlap is real, not an oversight, and is handled by using a **different athlete for
each of the two framings** so the page doesn't repeat one profile twice under two headings:

| # | Evidence situation | Athlete | Source basis |
|---|---|---|---|
| 1 | Strong multi-source (independent Tier-1 corroboration) | Rubina Francis (ATH-0330) or Rakesh Kumar (ATH-0342) — pick one | `outcomes.csv`, `outcome_corroboration_level == TIER3_PLUS_TIER1_CORROBORATION` (only 2 rows in the entire project carry this) |
| 2 | Dated support anchor, but not a first-support date | Atanu Das (ATH-0227) | `identity_evidence.csv`, `has_explicit_addition_event == True`; anchor year 2023 postdates his 2010-2022 outcomes (`6B4_lagged_association_pairs.csv`) |
| 3 | Outcome-rich, chronology weak | Deepika Kumari (ATH-0228, 12 major-games rows) or Seema Punia (ATH-0238, 13 rows) | `stage6_2_major_games_outcomes.csv` row counts; `chronology_status == SNAPSHOT_ONLY_NO_GENUINE_DATE` in `identity_evidence.csv` |
| 4 | Paralympic/para-sport coverage limitation | Ajeet Singh (ATH-0326, javelin F46, includes a 2024 Paris Paralympic silver) or Amit Kumar Saroha (ATH-0316, club/discus F51) | `identity_evidence.csv` verification basis text; underlying outcome rows are in the 693-row UNCLASSIFIED bucket (host-city + classification-code text only, no competition name — Item 4 finding) — this profile is also the natural place to *show*, not just state, why that bucket can't be taxonomized |
| 5 | Identity/source limitation | PV Sindhu (ATH-0205, `NO_OLYMPEDIA_COVERAGE`) or one of the 3 `NEEDS_REVIEW` athletes (Sajan/ATH-0310, Gohela Boro/ATH-0435, Chandro Devi Tomar/ATH-0443) | `identity_evidence.csv`, `identity_match_status_stage4` |
| 6 | Government support appears after an established achievement | Mehuli Ghosh (ATH-0230) | Same mechanism as #2, different athlete — `EXPLICIT_ADDITION` anchor (2023) postdates 2018-2022 outcomes |

**Recommendation**: use PV Sindhu for #5 over a `NEEDS_REVIEW` athlete — precisely *because* she is
widely recognized, seeing a household name land in `NO_OLYMPEDIA_COVERAGE` (not REJECTED, not
VERIFIED — a genuine "the automated identity pipeline correctly declined to assert a match it
couldn't support") is a far more credible demonstration of the project's identity-matching
discipline than an unfamiliar name would be. Each profile view shows: **Identity → Government
evidence → Outcome evidence → Timeline (dated lane / undated shelf, per design review §10) → What
can be said → What cannot be said** — six fixed fields per profile, so the set reads as a
consistent instrument, not six different mini-essays.

---

## 3. Interaction model

**Policy Question → Evidence → Answerability (§8)**, the headline interactive module. Pattern, per
the user's specification, generalized to all questions:

```
[Policy question, as a real question a senior official would ask]
        ↓ (click: "What do we need to answer this?")
[Ingredient list — identity, timing, financial stage, comparable population, etc.]
        ↓ (click: "What do we have?")
[Same ingredient list, each now annotated: substantial / partial / inadequate — sourced per §2]
        ↓ (auto-reveals once both are open)
[Answerability verdict, one line, from the fixed vocabulary below]
```

Fixed answerability vocabulary (never invent new labels per-question): **Answerable descriptively**
/ **Severely constrained** / **Not currently estimable**. This vocabulary must match the verdicts
already used in frozen documents (e.g. 6B-5's "cannot currently be estimated") — the interaction
must not introduce new phrasing that could drift from the frozen record.

Proposed 4 questions for the module (each verdict pre-determined by an already-frozen finding, not
computed live):

1. *"What can the available evidence tell us about the relationship between government sports
   support and international competitive outcomes?"* → descriptive evidence exists; temporal/causal
   answerability severely constrained (ties together §2's population funnel). (Corrected pre-build:
   the original draft's "translate into" is causal-adjacent language and is replaced with this
   neutral framing, consistent with the prohibition on causal verbs in §8.)
2. *"Does earlier athlete support precede competitive outcomes?"* → not currently estimable in a
   generalizable way (0/16, §7, Finding B).
3. *"Does financially-timed support associate with outcome timing?"* → not currently estimable
   (§7, Finding C, the zero-overlap case).
4. *"Is infrastructure investment associated with where athletes originate?"* → answerable only as
   a purely descriptive juxtaposition (§4's state ledger), not as an association claim — this
   question exists specifically to demonstrate that "we have a chart for this" is not the same as
   "this is answerable," reinforcing the whole module's discipline.

**A7/MDSD collision, interactive audit demo (§4)**: a "Why isn't this a confirmed match?" affordance
on the reconciliation view opens a fixed case study (MDSD project #290, or #320, or #24 — one is
enough, pick #290 for its cleanest score gap) showing both competing A7 rows side by side, their
scores, and the plain-language explanation already written in `6B3_QA_LOG.txt`. This is a static
worked example, not a live query — it does not need to generalize to arbitrary matches.

**Evidence Gap staircase (§6)**: hover/tap on each transition reveals the "why" annotation (a short
sentence, sourced per §2) — the diagram is inert until interacted with, per the user's "genuinely
interactive, not animated charts" instruction.

**State Evidence Ledger (§4)**: sortable by column, **default sort is alphabetical by state name,
never by count** — a user may re-sort by count as an explicit action, but the page must never open
in count-sorted order, since that default would itself constitute the ranking the project prohibits.

---

## 4. Evidence Gap staircase — final visual structure

Adopting the user's branching (not linear-funnel) structure exactly, with each transition annotated:

```
                    OBSERVABLE
                        │
          ┌─────────────┴─────────────┐
          │                           │
  Government support            Competition outcomes
  1,108 records · 638 athletes    368 deduplicated major-
                                   games rows · 60/75 cohort
                                   athletes with ≥1 recovered
                                   outcome
          └─────────────┬─────────────┘
                        │
                        ▼
         Research / identity evidence
         75-person research cohort
         71-person primary cohort (Pop-B-primary)
         0/75 VERIFIED · 60/75 PROBABLE
                        │
                        ▼
                 Support timing
         19/75 have any dated support anchor
         0/75 have a first-ever-support date
                        │
                        ▼
             Lag-eligible population
                    16/71 (Pop-C)
                        │
                        ▼
              Actual-date anchors
                      2/16
                        │
                        ▼
                Financial timing
         0/16 lag-eligible athletes have a
         financially staged dated anchor
                        │
                        ▼
        Longitudinal / financial linkage
         The assembled public records do not
         establish a common event-level linkage
         connecting support timing, financial
         stage, and outcome timing for the same
         intervention.
                        │
                        ▼
              Causal estimation
         Not attempted — no design in this
         project claims to estimate this.
```

**Correction applied (2026-09-17, pre-build review)**: the previous draft placed the `71/638`
population-construction figure inside an "athlete identity" transition alongside `0/75 VERIFIED`
— two different populations and two different concepts collapsed into one annotation. The corrected
structure above makes the chain explicit — register → research cohort → primary cohort →
lag-eligible → actual-date-anchored → financial-timing-eligible — so every number's population is
named at the step it belongs to, per the architecture's own denominator-labeling rule (§5). The
"no shared identifier" wording was also corrected: the project has athlete-level identifiers and
has performed real joins, so the accurate limitation is the absence of a common **event-level**
linkage across support timing, financial stage, and outcome timing — not an absence of
identifiers as such. The wording above ("The assembled public records do not establish a common
event-level linkage...") is the frozen wording for this transition; it must be reproduced verbatim
in the built page, not paraphrased.

Each arrow's annotation is the "why it narrows" sentence — this is the single visual asked to do
the most work in the whole module, so its copy must be reviewed word-by-word against the frozen
permanent caveats before implementation, not written fresh at build time.

---

## 5. Evidence/caveat treatment

- **Denominator labeling is mandatory and visually consistent**: every count or percentage on the
  page carries a small fixed-format tag naming its population (e.g. "71/638 · Pop-B-primary" or
  "16/71 · Pop-C"), reusing the population IDs already defined in `STAGE6_3_6A_ANALYTICAL_DESIGN_SPEC.md`
  — not a new, page-specific labeling scheme.
- **Coverage bars (§6) are explicitly titled "Data availability / coverage," never "performance"
  or "success," and the section header states this in words, not only via a legend.**
- **The A/B/C distinction** (descriptive evidence exists / a test returned null / a relationship is
  not estimable) must appear, verbatim in substance, in §7's copy — this is a hard requirement from
  `6B_ACCEPTANCE_AND_PERMANENT_CAVEATS.md`, not a style preference.
- **Every limitation-bearing visual resolves through the narrative spine** (§ above) — ends on
  "what this reveals" or a link to §9, never on the limitation alone.
- **The Evidence Architecture Recommendations section (§9)** must use the frame *"a record that
  captured X would make Y possible"* — never *"SAI/MYAS lacks X."* No sentence in that section may
  assert a specific institution's internal-systems capability, since no authoritative source in this
  project's evidence base establishes what those internal systems contain.

---

## 6. Mobile and desktop behaviour

- **Desktop**: wider canvas than the existing site's 640px single-column (`--maxw`) — propose
  960–1100px for this module specifically, since it is data-dense (state ledger, branching diagram,
  multi-field athlete profiles need more horizontal room than the existing narrative pages). Grid
  layouts for the state ledger and the programme-composition view; the branching Evidence Gap
  diagram renders as drawn in §4 (two-wide at the top, single column below).
- **Mobile (≤700px breakpoint)**: state ledger becomes a stacked card list (one state per card,
  same fields, no horizontal scroll); the Evidence Gap diagram's branching top collapses to a
  vertical stack in the same top-to-bottom reading order (Government support, then Competition
  outcomes, then the merge point) rather than side-by-side; the Policy Question module's click
  reveals stack vertically instead of appearing as adjacent panels; athlete profile's six fixed
  fields become an accordion instead of a fixed-width table.
- **Both**: section navigation (0–10) is a sticky, collapsible index — expanded rail on desktop,
  a compact dropdown/hamburger on mobile — consistent with the existing site's mobile-first
  original design intent even though this module runs wider on desktop.
- No visualization may rely on hover-only interaction for content that matters (tap must reveal
  everything hover does, given mobile has no hover) — this applies directly to the Evidence Gap
  staircase's transition annotations and the collision-demo affordance.

---

## 7. Visual design system

- **Reuse the existing site's tokens as the base palette**, for continuity: `--bg:#12151A`,
  `--surface:#1B2027`, `--line:#2E353F`, `--text:#EDEAE2`, `--text-dim:#9AA3AD`,
  `--gold:#C79A3D`/`--gold-dim:#8E6E2B` as the single accent. Do **not** introduce the existing
  site's `--green`/`--red` (quiz right/wrong colors) anywhere in this module — those specific two
  colors are reserved in the visual language for correct/incorrect quiz answers, and reusing them
  here would accidentally imply a value judgment (good/bad) on coverage or match-confidence data.
- **New tokens needed for this module only**: a neutral, non-alarming tone for "coverage/gap"
  bars (a muted blue-grey or a second, desaturated gold tint — not red) and a distinct but equally
  restrained tone for "heuristic/candidate" states (MEDIUM/LOW matches) — proposal: a dotted/hatched
  fill pattern rather than a third color, so confidence gradations read as a texture change, not a
  traffic-light color change.
- **Typography**: keep Barlow Condensed for headers, Source Sans 3 for body (site-wide consistency)
  but increase the type scale's top end for this module's pull-quotes (the 0/16 finding, the
  zero-overlap financial finding) — these should read as editorial pull-quotes, not chart labels.
- **No gauges, no KPI tiles, no trend arrows, no traffic-light coding, no category-rainbow palettes.**
- **Citation format**: a small, consistent inline citation (e.g. a superscript or bracketed tag)
  linking every number to its source file, in the manner of a footnoted report — reuse across all
  sections, not invented per-section.

---

## 8. What is explicitly prohibited

Consolidated from the design review and this round's discussion — an implementation checklist, not
new content:

- A filled/graduated choropleth India map as the primary infrastructure or athlete-density visual.
- A full searchable roster of all 71 (or 75, or 638) athletes.
- A proportional-flow Sankey diagram for the investment→outcome pathway.
- A medal "funnel" or any support→outcome conversion-rate visual.
- Any state, programme, or athlete ranking or "best/worst" framing, including an unlabeled
  default-sorted-by-count table.
- Traffic-light color coding, trend arrows, gauges, or KPI-tile treatments.
- A snapshot-dated support record placed on any timeline's x-axis, dashed or otherwise.
- Describing an A7/MDSD HIGH match as "confirmed" or "matched project" anywhere on the page.
- Treating the 0/16 result (§7, Finding B) as evidence support produced no outcomes.
- Treating the "cannot be estimated" financial relationship (§7, Finding C) as a null-effect finding.
- Any composite/aggregated financial figure drawn from `AMBIGUOUS`-stage or unit-unverified rows.
- Treating a cohort athlete's zero recovered outcome rows as "no medal" / a negative outcome.
- Any causal-language verb ("improves," "drives," "boosts," "leads to," "causes") anywhere in copy.
- A claim, anywhere in §9, about what SAI's or MYAS's actual internal (non-public) systems contain.
- **Visual design decisions that alter analytical semantics** (added at freeze, per explicit
  instruction): rounded numbers where an exact figure matters; visual area/size encoding a
  magnitude relationship the analysis doesn't support; a larger element implying
  "more important" or "better"; opacity implying data quality unless the mapping is explicitly
  defined and labeled; any ordering that implies ranking; a timeline position for anything other
  than a genuine date; a proximity or connecting line implying causal linkage.

---

## 9. Proposed executive 3-minute path (scroll-only, no clicks required)

§0 (tension statement) → §1 (system map, static) → §2 (population funnel, the four numbers that
matter) → §3 (one clear visual: developmental support vs. cash award split) → §6 (the Evidence Gap
staircase, fully visible on scroll even without hovering each transition — the shape alone tells
the story) → §7 (the two headline findings with their required framing sentences) → §8's headline
verdict row only (the 4 answerability verdicts, without necessarily opening every click-through).
A viewer who never clicks anything and only scrolls must still leave with the correct A/B/C
distinction intact — this is the executive path's hard requirement, not an aspiration.

## 10. Proposed deep-dive path (15-20 minutes)

Everything in the 3-minute path, plus: §4 in full (state ledger sorting, the A7/MDSD collision
demo), §5 (all 6 curated profiles, each fully expanded), §8's full interactive click-through on
every question, §9 in full, and §10 (methodology/evidence ledger — direct access to every frozen
document named in §2's source table). The deep-dive path should be reachable by scrolling further,
not by a separate "advanced mode" toggle — consistent with the two-depth-in-one-page pattern
already used in the existing site (`<details>` elements in `index.html`'s Module 8 section).

---

## 11. Technical architecture for GitHub Pages

- **New module location**: `SAI_deputation_preparation/12-evidence/index.html` (following the
  existing `NN-name/index.html` convention used by `10-handbook`, `11-story`), linked as a new card
  from the root `index.html`'s "Learn" section — no existing section is modified or replaced.
- **Data pipeline**: a new export script, `sports-analytics/tools/stage7_export_presentation_data.py`,
  reads only the frozen files named in §2's source table and writes small, purpose-specific
  JSON/CSV files into `SAI_deputation_preparation/12-evidence/data/`. This keeps the page
  provably regenerable from the frozen analytical record and avoids hand-transcribing any number.
  The export script performs no new analysis — it is a formatting/selection step only, matching the
  frozen figures exactly.
- **No backend, no build step** — static HTML/CSS/vanilla JS, matching every other module in the
  repository. Prefer hand-built SVG for the system map, population funnel, and Evidence Gap
  staircase; D3 (loaded from a pinned CDN version) only where its scale/binding utilities are
  genuinely useful (state ledger sorting, any dot-map projection) — not a general chart library,
  to avoid the "generic dashboard" visual signature.
- **Accessibility**: sufficient color contrast against the dark background (existing site's palette
  already targets this); every visualization has a text-equivalent summary for screen readers,
  particularly the Evidence Gap staircase and the population funnel, since these carry the module's
  core argument and must not be image-only or canvas-only without an accessible fallback.
- **Performance**: lazy-load §10's full methodology documents (render on expand, not on page load)
  given their size; keep the executive-path sections (§0-3, 6-7) as the fast-loading first paint.

---

## 12. Acceptance criteria for the finished product

- [ ] Every number on the page traces to a named file in §2's source table; spot-checkable by
      re-running `stage7_export_presentation_data.py` against the frozen CSVs and diffing output.
- [ ] None of the items in §8 (prohibited list) appear anywhere on the page.
- [ ] Every visualization carries an adjacent "what this does/does not establish" statement,
      styled as a design element per the visual design system, not a buried footnote.
- [ ] The A/B/C distinction (descriptive evidence / null test / not-estimable relationship) is
      intact and correctly labeled everywhere Finding B or Finding C is referenced.
- [ ] All 6 permanent caveats in `6B_ACCEPTANCE_AND_PERMANENT_CAVEATS.md` are represented, in
      substance, somewhere on the page (not necessarily verbatim, but never contradicted).
- [ ] The executive 3-minute scroll-only path (§9) delivers the correct headline conclusion without
      requiring any click.
- [ ] Mobile layout (tested at 375px width) has no horizontal page scroll and no hover-only content.
- [ ] The existing site's `index.html` and all other existing modules are unmodified except for the
      one new linking card.
- [ ] State Evidence Ledger's default sort is alphabetical, not by count, on first load.
- [ ] No `--green`/`--red` quiz-reserved tokens are used anywhere in this module.
- [ ] The interactive Policy Question module's answerability verdicts use only the fixed vocabulary
      in §3 and match the frozen findings' own wording, not a paraphrase invented at build time.
- [ ] No visual design decision alters analytical semantics: no rounded numbers where exact figures
      matter, no area/size encoding an unsupported magnitude, no size implying "better," no
      undefined opacity-as-quality mapping, no ordering implying ranking, no timeline position for
      a non-genuine date, no proximity/connecting line implying causal linkage.
- [ ] The Evidence Gap staircase reproduces the corrected population chain and the corrected
      "common event-level linkage" wording verbatim (pre-build corrections, this document).
- [ ] Policy Question #1 uses the corrected non-causal phrasing (pre-build correction, this
      document), not "translate into."

---

This document is the second and final architectural gate. Implementation begins only once this is
reviewed and explicitly frozen, per the user's instruction.
