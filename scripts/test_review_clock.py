#!/usr/bin/env python3
"""Unit tests for the pure classifier and clock in review_clock.py.

No filesystem, no network — classify()/cadence_days()/review_due() take plain
strings and dates.

Run:  python scripts/test_review_clock.py
"""
import datetime
import sys

from review_clock import (
    cadence_days,
    classify,
    days_overdue,
    parse_date,
    parse_frontmatter,
    review_due,
)

D = datetime.date


def check(name, got, want):
    if got != want:
        print(f"FAIL {name}: got {got!r}, want {want!r}")
        return 1
    print(f"ok   {name}")
    return 0


def main():
    f = 0

    # --- classify: the record signals -------------------------------------
    for path in (
        "sessions/2026-08-15.md",
        "archive/changelog-ahd.md",
        "eq/changelog/eq-shell.md",
        "eq/sprints/2026-08-12-field-mobile-centering.md",
        "eq/progress/2026-07.md",
    ):
        f += check(f"record dir: {path}", classify(path), "record")

    # A date in the FILENAME means the file is about that date, wherever it sits.
    f += check(
        "dated filename anywhere is a record",
        classify("eq-platform-verified-state-2026-06-03.md"),
        "record",
    )

    # --- classify: the safety asymmetry -----------------------------------
    # THE load-bearing property. An unrecognised path must default to state, so a
    # wrong guess costs an unnecessary review rather than a claim that is never
    # checked again. If this ever flips to 'record', the guard goes quiet instead
    # of noisy and nobody finds out.
    f += check("unknown path defaults to state", classify("eq/some-new-thing.md"), "state")
    f += check("root file defaults to state", classify("CLAUDE.md"), "state")
    f += check("deep unknown path defaults to state", classify("a/b/c/d.md"), "state")

    # A record DIRECTORY makes a record; a file merely NAMED like one does not.
    # parts[:-1] is what draws that line — a root-level sessions.md is a doc about
    # sessions, not a session log.
    f += check("file named like a record dir is still state", classify("sessions.md"), "state")
    f += check("archive.md at root is still state", classify("archive.md"), "state")

    # A dated DIRECTORY does not make its contents records. Only the filename and
    # the known record dirs count — anything looser would sweep live plans that
    # happen to live under a dated folder into the never-reviewed bucket.
    f += check(
        "dated directory does not make contents records",
        classify("eq/2026-08-14-migration/plan.md"),
        "state",
    )

    # --- classify: generated + explicit override --------------------------
    f += check("named generated file", classify("digest.md"), "generated")
    f += check("nested generated file", classify("sessions/INDEX.md"), "generated")
    f += check(
        "explicit kind overrides the path",
        classify("sessions/2026-08-15.md", {"kind": "state"}),
        "state",
    )
    f += check(
        "explicit kind is normalised",
        classify("eq/x.md", {"kind": "  RECORD  "}),
        "record",
    )
    # An unknown explicit value is returned as-is so main() can fail loudly on it
    # rather than silently falling back to a default.
    f += check(
        "typo'd kind is surfaced, not defaulted",
        classify("eq/x.md", {"kind": "recrod"}),
        "recrod",
    )

    # --- cadence ----------------------------------------------------------
    f += check("critical is 30d", cadence_days("state", "critical"), 30)
    f += check("high is 60d", cadence_days("state", "high"), 60)
    f += check("reference falls back to 90d", cadence_days("state", "reference"), 90)
    f += check("missing read_priority falls back to 90d", cadence_days("state", None), 90)
    f += check("read_priority is case-insensitive", cadence_days("state", "Critical"), 30)
    f += check("records have no clock", cadence_days("record", "critical"), None)
    f += check("generated gets the tight cron clock", cadence_days("generated", "critical"), 3)

    # --- review_due -------------------------------------------------------
    f += check(
        "due = last_updated + cadence",
        review_due(D(2026, 7, 1), 30),
        D(2026, 7, 31),
    )
    f += check("no clock -> no due date", review_due(D(2026, 7, 1), None), None)
    f += check("no last_updated -> no due date", review_due(None, 30), None)
    f += check(
        "explicit review_by wins over the derived date",
        review_due(D(2026, 7, 1), 30, D(2026, 12, 25)),
        D(2026, 12, 25),
    )

    # --- days_overdue -----------------------------------------------------
    f += check("overdue counts days past due", days_overdue(D(2026, 8, 1), D(2026, 8, 15)), 14)
    # Never negative: a file due next week is 0 overdue, not -7. A signed value
    # would make len(overdue) meaningless the moment anyone summed it.
    f += check("not yet due is zero, not negative", days_overdue(D(2026, 9, 1), D(2026, 8, 15)), 0)
    f += check("due today is not overdue", days_overdue(D(2026, 8, 15), D(2026, 8, 15)), 0)
    f += check("no due date is never overdue", days_overdue(None, D(2026, 8, 15)), 0)

    # --- frontmatter parsing ---------------------------------------------
    good = "---\ntitle: X\nread_priority: critical\nstatus: live\n---\n\n# Body\n"
    f += check(
        "parses a well-formed block",
        parse_frontmatter(good).get("read_priority"),
        "critical",
    )
    # An unterminated block must yield {} rather than swallowing the document
    # body as frontmatter — otherwise a stray '---' turns prose into metadata and
    # a file silently acquires whatever 'kind:' happens to appear in its text.
    f += check(
        "unterminated block yields nothing",
        parse_frontmatter("---\ntitle: X\n\n# Body\nkind: record\n"),
        {},
    )
    f += check("no frontmatter yields nothing", parse_frontmatter("# Just a heading\n"), {})
    f += check(
        "BOM does not defeat the delimiter",
        parse_frontmatter("﻿---\nkind: record\n---\n").get("kind"),
        "record",
    )
    f += check("quotes are stripped", parse_frontmatter('---\nkind: "state"\n---\n')["kind"], "state")

    # --- parse_date -------------------------------------------------------
    f += check("ISO date parses", parse_date("2026-08-15"), D(2026, 8, 15))
    f += check("trailing text is tolerated", parse_date("2026-08-15 (nightly)"), D(2026, 8, 15))
    f += check("non-date yields None", parse_date("soon"), None)
    f += check("empty yields None", parse_date(""), None)
    # An impossible date must not raise — a typo in one file cannot be allowed to
    # take the whole gate down, or the gate gets removed instead of the typo.
    f += check("impossible date yields None, not a crash", parse_date("2026-13-45"), None)

    # --- the real 2026-08-15 regression -----------------------------------
    # rules/brand-eq.md is read_priority: critical and was last touched
    # 2026-05-30 — 77 days before this was written. Under the 90d default it
    # would not surface at all; on the 30d clock its own read_priority earns, it
    # is 47 days overdue. That gap is the reason cadence is tiered rather than
    # flat: brand hex values had already drifted once undetected (#1F335C vs
    # #203060, found by hand 2026-07-30), which is exactly what an unreviewed
    # critical file costs.
    lu, today = D(2026, 5, 30), D(2026, 8, 15)
    due = review_due(lu, cadence_days("state", "critical"))
    f += check("brand-eq.md is 47d overdue on its own clock", days_overdue(due, today), 47)
    f += check(
        "...and invisible under a flat 90d clock",
        days_overdue(review_due(lu, 90), today),
        0,
    )

    print()
    if f:
        print(f"{f} test(s) FAILED")
    else:
        print("all tests passed")
    sys.exit(1 if f else 0)


if __name__ == "__main__":
    main()
