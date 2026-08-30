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

# 3 — non-superset copies (neither's done-lines contain the other's -- the
# rotation bug's mixed-section shape: each failed-removal night appended a
# different, non-overlapping extract of the same live section) union-merge
# into ONE section holding every distinct done-block. Nothing dropped, no
# copy silently preferred over another.
body = (
    "\n## union thing (2026-08-01) (rotated 2026-08-05)\n*first intro*\n\n- [x] did A\n\n---\n\n"
    "## union thing (2026-08-01) (rotated 2026-08-06)\n*second intro*\n\n- [x] did C\n\n---\n\n"
)
text, r = run(body)
check("union: 1 group deduped (via union-merge)", r["groups_deduped"] == 1, r)
check("union: flagged as union-merged, not left as conflict", any("union thing (2026-08-01)" in k for k in r["groups_union_merged"]) and r["groups_conflicted"] == [], r)
check("union: exactly one copy of the header remains", text.count("## union thing") == 1)
check("union: both done lines survive in the merged section", "- [x] did A" in text and "- [x] did C" in text)
check("union: newest copy's own intro kept (not the older one)", "*second intro*" in text and "*first intro*" not in text)

# 3b — the true backstop case: a "duplicate" group where NEITHER copy has
# any done item at all (shouldn't happen in a real archive, which is
# done-items-only by convention, but must never crash or guess). Left
# completely untouched and reported -- there's nothing safe to union.
body = (
    "\n## no-done thing (2026-08-01) (rotated 2026-08-05)\n*intro A*\n\n---\n\n"
    "## no-done thing (2026-08-01) (rotated 2026-08-06)\n*intro B*\n\n---\n\n"
)
text, r = run(body)
check("backstop: nothing deduped", r["groups_deduped"] == 0, r)
check("backstop: flagged as a genuine conflict, not union-merged", any("no-done thing" in k for k in r["groups_conflicted"]) and r["groups_union_merged"] == [], r)
check("backstop: both copies still present untouched", text.count("## no-done thing") == 2)

# 3c — same-day tie on rotation date: the richer intro wins, not file
# order. Caught live on eq/pending-archive.md's own "SKS tenant LIVE...
# Big correction" pair (both stamped the same date; file-order tiebreak
# would have kept the near-empty intro over the one explaining the
# correction). The union of done-items must hold regardless of which
# intro wins.
body = (
    "\n## same-day tie (2026-08-01) (rotated 2026-08-05)\n\n- [x] short version item\n\n---\n\n"
    "## same-day tie (2026-08-01) (rotated 2026-08-05)\n*Big correction vs the earlier draft: here is what was actually wrong.*\n\n- [x] fuller version item\n\n---\n\n"
)
text, r = run(body)
check("tiebreak: richer intro wins on a same-date tie", "*Big correction vs the earlier draft" in text, r)
check("tiebreak: both done items still survive the union", "- [x] short version item" in text and "- [x] fuller version item" in text)
check("tiebreak: only one header remains", text.count("## same-day tie") == 1)

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
