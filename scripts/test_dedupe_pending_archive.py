#!/usr/bin/env python3
"""
Unit tests for dedupe_pending_archive.dedupe_text.

Cross-platform, no network, no fixtures on disk. Builds synthetic
pending-archive.md text and asserts what collapses, what's left alone, and
that no unique done-item line is ever lost.
Run: python scripts/test_dedupe_pending_archive.py
"""
import sys

import dedupe_pending_archive as dpa

passed = failed = 0

FM = "---\ntitle: EQ Tier — Pending Actions Archive\nlast_updated: 2026-07-01\nstatus: archived\n---\n"


def run(body):
    return dpa.dedupe_text(FM + body)


def check(name, cond, detail=""):
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        print(f"FAIL: {name} {detail}")


# 1 — true duplicate (identical modulo rotation date) collapses to one, newest kept
body = (
    "\n## finished thing (2026-08-01) (rotated 2026-08-05)\n*intro*\n\n- [x] did A\n\n---\n\n"
    "## finished thing (2026-08-01) (rotated 2026-08-06)\n*intro*\n\n- [x] did A\n\n---\n\n"
    "## finished thing (2026-08-01) (rotated 2026-08-07)\n*intro*\n\n- [x] did A\n\n---\n\n"
)
text, r = run(body)
check("true-dup: 1 group deduped", r["groups_deduped"] == 1, r)
check("true-dup: 2 copies removed", r["copies_removed"] == 2, r)
check("true-dup: newest date kept", "(rotated 2026-08-07)" in text)
check("true-dup: older dates gone", "(rotated 2026-08-05)" not in text and "(rotated 2026-08-06)" not in text)
check("true-dup: exactly one copy of the header text remains", text.count("## finished thing (2026-08-01)") == 1)

# 2 — non-identical duplicates where later is a strict superset (mixed
# section that kept accumulating more done items each failed-removal night)
# collapse to the superset copy, nothing lost.
body = (
    "\n## mixed thing (2026-08-01) (rotated 2026-08-05)\n*intro*\n\n- [x] did A\n\n---\n\n"
    "## mixed thing (2026-08-01) (rotated 2026-08-06)\n*intro*\n\n- [x] did A\n- [x] did B\n\n---\n\n"
)
text, r = run(body)
check("superset: 1 group deduped", r["groups_deduped"] == 1, r)
check("superset: newest/fullest kept", "- [x] did B" in text and "(rotated 2026-08-06)" in text)
check("superset: no conflict flagged", r["groups_conflicted"] == [])

# 3 — genuine conflict (neither copy's done-lines are a superset of the
# other's) is left untouched and reported, never guessed at.
body = (
    "\n## conflict thing (2026-08-01) (rotated 2026-08-05)\n*intro*\n\n- [x] did A\n\n---\n\n"
    "## conflict thing (2026-08-01) (rotated 2026-08-06)\n*intro*\n\n- [x] did C\n\n---\n\n"
)
text, r = run(body)
check("conflict: nothing deduped", r["groups_deduped"] == 0, r)
check("conflict: flagged", any("conflict thing (2026-08-01)" in k for k in r["groups_conflicted"]), r["groups_conflicted"])
check("conflict: both copies still present", text.count("## conflict thing") == 2)
check("conflict: both done lines survive", "- [x] did A" in text and "- [x] did C" in text)

# 4 — a section with no duplicates anywhere is left completely alone
body = "\n## unique thing (2026-08-01)\n*intro*\n\n- [x] did A\n\n---\n\n"
text, r = run(body)
check("unique: no groups deduped", r["groups_deduped"] == 0, r)
check("unique: content unchanged", "- [x] did A" in text and text.count("## unique thing") == 1)

# 5 — mix of a real duplicate pair and an unrelated singleton section: only
# the duplicate collapses, the singleton and its content are untouched.
body = (
    "\n## dup one (2026-08-01) (rotated 2026-08-05)\n\n- [x] X\n\n---\n\n"
    "## singleton (2026-08-02)\n\n- [x] Y\n\n---\n\n"
    "## dup one (2026-08-01) (rotated 2026-08-06)\n\n- [x] X\n\n---\n\n"
)
text, r = run(body)
check("order-preserved: 1 dedup, singleton untouched", r["groups_deduped"] == 1 and "- [x] Y" in text, r)
check("order-preserved: only one dup one remains", text.count("## dup one") == 1)

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
