#!/usr/bin/env python3
"""
DISCLOSED CORRECTION (2026-09-17), found during Stage 7 presentation-layer build.

Stage 6.1's competition-type classifier matched outcome rows to "Olympics" / "Asian
Games" by host-city + year text alone, without checking whether the accompanying
event text carries a Paralympic classification code (e.g. F46, SH1). Paris (2024)
hosted both the Olympics and the Paralympics; Incheon (2014) / Jakarta (2018) /
Hangzhou (2022) each hosted both the Asian Games and the Asian Para Games. As a
result, 16 rows belonging to 5 independently-identified para-sport athletes
(identity_evidence.csv's Stage 5B verification-basis text already correctly says
"Para Sports"/"Para Athletics"/"PARALYMPIC GAMES" etc. for all 5 -- this text was
never cross-referenced against the separate competition-type column) were labeled
"Olympics" or "Asian Games" instead of "Paralympics" or "Asian Para Games".

Scope, found by cross-referencing identity_evidence.csv's para-sport athletes
against outcomes.csv's Olympics/Asian Games rows -- verified exhaustively, not
sampled: exactly 16 rows, 5 athletes, all from OUTCOME_ROWS_WIKIPEDIA.csv (Part A,
targeted), none flagged as a duplicate copy. Every row's (host city, year) pair
matches a real, verifiable Paralympic or Asian Para Games edition exactly.

This script performs the narrow, disclosed correction authorized by the user:
reclassify these 16 rows in outcomes.csv, then regenerate
stage6_2_major_games_outcomes.csv with Paralympics/Asian Para Games as two
additional genuine major-games categories (evidence-based, not host-city-only
inference -- distinct from the Item-4 finding that the 693 UNCLASSIFIED rows
cannot be defensibly classified from host-city text alone, because those rows
lack the corroborating para-sport identity evidence these 16 have).
"""
import csv
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
S6 = ROOT / "analysis" / "stage6"

# (athlete_id, competition_raw_text, outcome_year) -> corrected competition_type_normalized
# Built from the exhaustive cross-reference documented above -- every row explicit, none inferred.
CORRECTIONS = {
    ("ATH-0316", "Incheon Club throw F51", "2014"): "Asian Para Games",
    ("ATH-0316", "Jakarta Club throw F51", "2018"): "Asian Para Games",
    ("ATH-0316", "Incheon Discus throw F51", "2014"): "Asian Para Games",
    ("ATH-0316", "Hangzhou Club throw F51", "2022"): "Asian Para Games",
    ("ATH-0326", "Paris Javelin throw F46", "2024"): "Paralympics",
    ("ATH-0326", "Hangzhou Javelin throw F46", "2022"): "Asian Para Games",
    ("ATH-0330", "Paris P2 10 m air pistol SH1", "2024"): "Paralympics",
    ("ATH-0330", "Hangzhou 10 m air pistol", "2022"): "Asian Para Games",
    ("ATH-0336", "Jakarta Men's singles", "2018"): "Asian Para Games",
    ("ATH-0336", "Hangzhou Men's doubles", "2022"): "Asian Para Games",
    ("ATH-0336", "Incheon Men's singles", "2014"): "Asian Para Games",
    ("ATH-0336", "Jakarta Men's team", "2018"): "Asian Para Games",
    ("ATH-0342", "Paris Mixed team", "2024"): "Paralympics",
    ("ATH-0342", "Hangzhou Mixed team", "2022"): "Asian Para Games",
    ("ATH-0342", "Hangzhou Individual", "2022"): "Asian Para Games",
    ("ATH-0342", "Hangzhou Team", "2022"): "Asian Para Games",
}


def load(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def main():
    outcomes = load(S6 / "outcomes.csv")
    applied = 0
    before_counts = Counter(r["competition_type_normalized"] for r in outcomes)
    for r in outcomes:
        key = (r["athlete_id"], r["competition_raw_text"], r["outcome_year"])
        if key in CORRECTIONS:
            old = r["competition_type_normalized"]
            r["competition_type_normalized"] = CORRECTIONS[key]
            applied += 1
            print(f"  corrected: {r['athlete_id']} {r['canonical_name']!r} {r['competition_raw_text']!r} : {old!r} -> {CORRECTIONS[key]!r}")

    assert applied == len(CORRECTIONS), f"expected {len(CORRECTIONS)} corrections, applied {applied} -- STOP, do not write, investigate mismatch"

    with open(S6 / "outcomes.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(outcomes[0].keys()))
        w.writeheader()
        w.writerows(outcomes)

    after_counts = Counter(r["competition_type_normalized"] for r in outcomes)
    print(f"\nApplied {applied} corrections to outcomes.csv.")
    print("Before:", dict(before_counts))
    print("After: ", dict(after_counts))
    print(f"\nSaved: {S6 / 'outcomes.csv'}")


if __name__ == "__main__":
    main()
