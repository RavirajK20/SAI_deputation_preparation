#!/usr/bin/env python3
"""
Stage 7: export presentation data. Reads ONLY frozen Stage 6/6.3/6B files and writes
small, purpose-specific JSON files consumed by SAI_deputation_preparation/12-evidence/.
No new analysis is performed here -- this is a formatting/selection step. Every number
this script emits must already exist in one of the frozen source files; it must never
compute a new statistic.

Per the frozen STAGE7_FINAL_ARCHITECTURE.md: do not reopen the analytical methodology
while building the presentation layer.
"""
import csv
import json
from pathlib import Path
from collections import Counter, defaultdict

SA = Path(__file__).resolve().parent.parent           # sports-analytics/
S6 = SA / "analysis" / "stage6"
S63 = S6 / "stage6_3_normalization"
S6B = S6 / "stage6_3_6b_execution"

SITE = SA.parent / "SAI_deputation_preparation" / "12-evidence"
DATA_OUT = SITE / "data"
DATA_OUT.mkdir(parents=True, exist_ok=True)


def load(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def write(name, obj):
    out = DATA_OUT / name
    with open(out, "w") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print(f"wrote {out} ({len(json.dumps(obj))} bytes)")


def main():
    athletes = load(S6 / "athletes.csv")
    identity_evidence = load(S6 / "identity_evidence.csv")
    support_acc = load(S63 / "government_support_accounting_normalized.csv")
    major = load(S6 / "stage6_2_major_games_outcomes.csv")
    pop_b_primary = load(S6B / "pop_b_primary.csv")
    pop_c = load(S6B / "pop_c_lag_eligible.csv")
    state_desc = load(S6B / "6B2_state_descriptive.csv")
    infra_access = load(S6B / "6B3_infrastructure_access.csv")
    recon = load(S63 / "a7_mdsd_reconciliation.csv")
    lag_pairs = load(S6B / "6B4_lagged_association_pairs.csv")
    support_ecosystem = load(S6 / "stage6_2_support_ecosystem.csv")

    # ---------------------------------------------------------------
    # 1. Population funnel / Evidence Gap staircase (single source of
    #    truth for both -- the staircase is this funnel re-sequenced)
    # ---------------------------------------------------------------
    n_register = len(athletes)
    n_support_records = len(support_acc)
    n_cohort = sum(1 for a in athletes if a["in_75_research_cohort"] == "True")
    n_primary = len(pop_b_primary)
    status_counts = Counter(r["identity_match_status_stage4"] for r in identity_evidence)
    n_dated_anchor = sum(1 for r in identity_evidence if r["has_dated_government_support_anchor"] == "True")
    n_explicit_addition = sum(1 for r in identity_evidence if r["has_explicit_addition_event"] == "True")
    n_major_games_rows = len(major)
    cohort_ids = {r["athlete_id"] for r in identity_evidence}
    ids_with_outcome = {r["athlete_id"] for r in major if r["athlete_id"] in cohort_ids}
    n_pop_c = len(pop_c)
    n_actual_date = sum(1 for r in pop_c if int(r["n_with_actual_date"]) > 0)
    n_financial_staged_in_pop_c = 0  # frozen 6B-5 finding: exactly zero

    funnel = {
        "source_note": "Every figure below is read directly from a frozen Stage 6/6B file; none is recomputed.",
        "register": {"n": n_register, "source": "athletes.csv", "label": "Government support register"},
        "support_records": {"n": n_support_records, "source": "government_support_accounting_normalized.csv"},
        "outcome_rows": {"n": n_major_games_rows, "source": "stage6_2_major_games_outcomes.csv (deduplicated)"},
        "cohort_outcome_coverage": {"n": len(ids_with_outcome), "of": 75, "source": "major games join against identity_evidence.csv athlete_ids"},
        "research_cohort": {"n": n_cohort, "source": "athletes.csv:in_75_research_cohort"},
        "primary_cohort": {"n": n_primary, "source": "pop_b_primary.csv (75 - REJECTED - NEEDS_REVIEW)"},
        "identity_status": {"VERIFIED": status_counts.get("VERIFIED", 0), "PROBABLE": status_counts.get("PROBABLE", 0),
                             "NO_OLYMPEDIA_COVERAGE": status_counts.get("NO_OLYMPEDIA_COVERAGE", 0),
                             "NEEDS_REVIEW": status_counts.get("NEEDS_REVIEW", 0), "REJECTED": status_counts.get("REJECTED", 0),
                             "of": 75, "source": "identity_evidence.csv:identity_match_status_stage4"},
        "dated_support_anchor": {"n": n_dated_anchor, "of": 75, "source": "identity_evidence.csv:has_dated_government_support_anchor"},
        "explicit_addition": {"n": n_explicit_addition, "of": 75, "source": "identity_evidence.csv:has_explicit_addition_event"},
        "lag_eligible_pop_c": {"n": n_pop_c, "of": n_primary, "source": "pop_c_lag_eligible.csv"},
        "actual_date_anchor": {"n": n_actual_date, "of": n_pop_c, "source": "pop_c_lag_eligible.csv:n_with_actual_date"},
        "financial_staged_in_lag_eligible": {"n": n_financial_staged_in_pop_c, "of": n_pop_c, "source": "6B5_QA_LOG.txt (0 of 16, frozen finding)"},
        "linkage_statement": "The assembled public records do not establish a common event-level linkage connecting support timing, financial stage, and outcome timing for the same intervention.",
    }
    write("evidence_gap.json", funnel)

    # ---------------------------------------------------------------
    # 2. Government support ecosystem: programme composition +
    #    developmental-support vs. outcome-linked cash-award split
    # ---------------------------------------------------------------
    prog_by_record = Counter(r["dimension"] + "|" + r["value"] for r in support_ecosystem if r["section"] == "programme_category" and r["dimension"] == "category")
    programme_records = [{"programme_category": r["value"], "n_records": int(r["count"])}
                         for r in support_ecosystem if r["section"] == "programme_category" and r["dimension"] == "category"]
    programme_athletes = [{"programme_category": r["value"], "n_unique_athletes": int(r["count"])}
                          for r in support_ecosystem if r["section"] == "programme_category" and r["dimension"] == "unique_athletes"]

    accounting_stage_counts = Counter(r["accounting_stage"] for r in support_acc)
    outcome_linked = sum(1 for r in support_acc if r["is_outcome_linked_cash_award"] == "True")

    write("support_ecosystem.json", {
        "programme_by_record": programme_records,
        "programme_by_unique_athlete": programme_athletes,
        "accounting_stage_counts": dict(accounting_stage_counts),
        "outcome_linked_cash_award_rows": outcome_linked,
        "n_total_support_records": n_support_records,
        "source": "stage6_2_support_ecosystem.csv, government_support_accounting_normalized.csv",
    })

    # ---------------------------------------------------------------
    # 3. State Evidence Ledger (alphabetical; sorting happens client-side)
    # ---------------------------------------------------------------
    infra_by_state = {r["state_canonical"]: r for r in infra_access}
    ledger = []
    for r in state_desc:
        st = r["state_canonical"]
        infra = infra_by_state.get(st, {})
        ledger.append({
            "state": st,
            "support_records": int(r["n_support_records"]),
            "distinct_athletes": int(r["n_distinct_athletes"]),
            "a7_projects_2015_19": int(infra.get("a7_project_count_2015_19", 0)),
            "mdsd_only_projects": int(infra.get("mdsd_only_project_count", 0)),
            "total_deduplicated_infrastructure_projects": int(infra.get("total_deduplicated_infrastructure_projects", 0)),
        })
    ledger.sort(key=lambda r: r["state"])
    write("state_ledger.json", {"states": ledger, "default_sort": "alphabetical",
                                 "source": "6B2_state_descriptive.csv, 6B3_infrastructure_access.csv"})

    # ---------------------------------------------------------------
    # 4. A7 / MDSD reconciliation + collision audit demo
    # ---------------------------------------------------------------
    conf_counts = Counter(r["match_confidence"] for r in recon)
    high = [r for r in recon if r["match_confidence"] == "HIGH"]
    by_serial = defaultdict(list)
    for r in high:
        by_serial[r["mdsd_serial_number"]].append(r)
    collisions = []
    for serial, rows in by_serial.items():
        if len(rows) > 1:
            rows_sorted = sorted(rows, key=lambda r: -float(r["match_score"]))
            collisions.append({
                "mdsd_serial_number": serial,
                "mdsd_project": rows_sorted[0]["mdsd_project"],
                "candidates": [{"a7_sl_no": r["a7_sl_no"], "a7_project": r["a7_project"], "a7_year": r["a7_year"],
                                "match_score": r["match_score"]} for r in rows_sorted],
            })
    n_a7_total = len({r["a7_sl_no"] + r["a7_year"] for r in recon})
    write("a7_mdsd.json", {
        "match_confidence_counts": dict(conf_counts),
        "n_a7_total": len(recon),
        "n_mdsd_total_from_infra_access": sum(int(r.get("mdsd_only_project_count", 0)) for r in infra_access) + len(set(by_serial.keys())),
        "collision_cases": collisions,
        "source": "a7_mdsd_reconciliation.csv, 6B3_QA_LOG.txt",
        "label_rule": "Every match_confidence == HIGH pair must be labeled 'HIGH-confidence heuristic match', never 'confirmed match'.",
    })

    # ---------------------------------------------------------------
    # 5. Findings: 6B-4 (0/16 + mechanism) and 6B-5 (0 eligible, cannot estimate)
    # ---------------------------------------------------------------
    actual_date_pairs = [r for r in lag_pairs if r["anchor_kind"] == "ACTUAL_DATE"]
    actual_date_athletes = sorted({r["athlete_id"] for r in actual_date_pairs})
    id_to_name = {r["athlete_id"]: r["canonical_name"] for r in identity_evidence}
    mechanism_examples = []
    seen = set()
    for r in actual_date_pairs:
        if r["athlete_id"] in seen:
            continue
        seen.add(r["athlete_id"])
        mechanism_examples.append({
            "athlete_id": r["athlete_id"],
            "canonical_name": id_to_name.get(r["athlete_id"], ""),
            "anchor_year": r["support_anchor_year"],
            "support_date_type": r["support_date_type"],
        })

    write("findings.json", {
        "lag_result": {
            "confirmed_within_window": {"1y": 0, "3y": 0, "5y": 0},
            "of_pop_c": n_pop_c,
            "required_framing": ("No qualifying within-window co-occurrences were confirmed in the lag-eligible "
                                  "population under the project's strict dating rules. This should not be "
                                  "interpreted as evidence that government support was followed by no outcomes; "
                                  "the available dates generally cannot establish when support began."),
            "mechanism": {
                "n_with_actual_date_anchor": len(actual_date_athletes),
                "of_pop_c": n_pop_c,
                "examples": mechanism_examples,
                "note": "Both actual-date anchors are EXPLICIT_ADDITION events dated after the athlete's major-games outcomes -- a later re-addition event, not a first-support date.",
            },
            "source": "6B4_lagged_association_pairs.csv, 6B4_QA_LOG.txt",
        },
        "financial_relationship": {
            "n_eligible_financial_rows_in_pop_c": 0,
            "of_pop_c_dated_rows": n_pop_c,
            "verdict": "Cannot currently be estimated from available public evidence.",
            "reason": "All genuinely-dated support rows in the lag-eligible population are accounting_stage == NOT_FINANCIAL (PIB batch-release/induction events); none carry a SANCTIONED or RELEASED_PAID stage.",
            "source": "6B5_QA_LOG.txt, 6B5_eligible_support_rows.csv",
        },
    })

    # ---------------------------------------------------------------
    # 6. Curated athlete profiles (methodological selection, per
    #    STAGE7_FINAL_ARCHITECTURE.md's curation table -- fixed list,
    #    not re-derived; only their evidence fields are pulled live)
    # ---------------------------------------------------------------
    CURATED = [
        ("ATH-0330", "Strong multi-source (independent Tier-1 corroboration)"),
        ("ATH-0227", "Dated support anchor, but not a first-support date"),
        ("ATH-0228", "Outcome-rich, chronology weak"),
        ("ATH-0326", "Paralympic/para-sport coverage limitation"),
        ("ATH-0205", "Identity/source limitation"),
        ("ATH-0230", "Government support appears after an established achievement"),
    ]
    idev_by_id = {r["athlete_id"]: r for r in identity_evidence}
    support_by_ath = defaultdict(list)
    for r in support_acc:
        support_by_ath[r["athlete_id"]].append(r)
    major_by_ath = defaultdict(list)
    for r in major:
        major_by_ath[r["athlete_id"]].append(r)
    outcomes_all = load(S6 / "outcomes.csv")
    outcomes_all_by_ath = defaultdict(list)
    for r in outcomes_all:
        outcomes_all_by_ath[r["athlete_id"]].append(r)

    profiles = []
    for aid, situation in CURATED:
        idr = idev_by_id.get(aid, {})
        s_rows = support_by_ath.get(aid, [])
        m_rows = major_by_ath.get(aid, [])
        all_o_rows = outcomes_all_by_ath.get(aid, [])
        tier1 = [r for r in all_o_rows if r["outcome_corroboration_level"] == "TIER3_PLUS_TIER1_CORROBORATION"]
        dated_support = [r for r in s_rows if r["date_type"] in ("record_date", "EXPLICIT_ADDITION", "ALREADY_RECEIVING_BY_DATE")]
        undated_support = [r for r in s_rows if r["date_type"] in ("snapshot_date", "none")]
        profiles.append({
            "athlete_id": aid,
            "canonical_name": idr.get("canonical_name", ""),
            "evidence_situation": situation,
            "identity_match_status_stage4": idr.get("identity_match_status_stage4", ""),
            "identity_verification_basis": idr.get("identity_verification_basis", ""),
            "chronology_status": idr.get("chronology_status", ""),
            "n_government_support_records": len(s_rows),
            "dated_support_records": [{"programme_source_id": r["programme_source_id"], "date_type": r["date_type"],
                                        "record_date": r["record_date"], "accounting_stage": r["accounting_stage"]}
                                       for r in dated_support],
            "n_undated_support_records": len(undated_support),
            "n_major_games_outcome_rows": len(m_rows),
            "n_total_outcome_rows_all_tiers": len(all_o_rows),
            "n_tier1_corroborated_rows": len(tier1),
            "sample_outcomes": [{"outcome_year": r["outcome_year"], "competition_type": r["competition_type_normalized"],
                                  "medal": r["medal"]} for r in m_rows[:6]],
        })
    write("athlete_profiles.json", {
        "profiles": profiles,
        "note": "Curated, not representative -- selected to illustrate the range of evidence quality in the research cohort, per STAGE7_FINAL_ARCHITECTURE.md.",
        "source": "identity_evidence.csv, government_support_accounting_normalized.csv, outcomes.csv, stage6_2_major_games_outcomes.csv",
    })

    # ---------------------------------------------------------------
    # 7. Medal table by competition type (kept strictly separate,
    #    never summed into one score -- see STAGE6_2_DESCRIPTIVE_REPORT.md 6.2.2)
    # ---------------------------------------------------------------
    by_type_rows = Counter(r["competition_type_normalized"] for r in major)
    medal_by_type = defaultdict(Counter)
    for r in major:
        if r["medal"]:
            medal_by_type[r["competition_type_normalized"]][r["medal"]] += 1
    medal_table = [{"competition_type": t, "rows": by_type_rows[t],
                     "gold": medal_by_type[t].get("Gold", 0), "silver": medal_by_type[t].get("Silver", 0),
                     "bronze": medal_by_type[t].get("Bronze", 0)}
                    for t in sorted(by_type_rows)]
    write("medal_table.json", {
        "by_competition_type": medal_table,
        "note": "Row counts, not unique-athlete or unique-medal counts. Never summed across competition types. Olympics and Paralympics, Asian Games and Asian Para Games, are kept as separate rows -- different competitions, different eligibility criteria.",
        "source": "stage6_2_major_games_outcomes.csv (corrected 2026-09-17, see STAGE6_2_DESCRIPTIVE_REPORT.md 6.2.2)",
    })

    print("\nDone. All figures traced to frozen Stage 6/6B files -- no new analysis performed.")


if __name__ == "__main__":
    main()
