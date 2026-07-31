#!/usr/bin/env python3
"""
Unit tests for rotate_pending.rotate_text — the per-item done-rotation engine.

Cross-platform, no network, no fixtures on disk. Builds synthetic pending.md
text and asserts what moves, what stays, and that nothing is ever lost.
Run: python scripts/test_rotate_pending.py
"""
import datetime
import sys

import rotate_pending as rp

TODAY = datetime.date(2026, 7, 27)
passed = failed = 0

FM = "---\ntitle: EQ Tier — Pending Actions\nlast_updated: 2026-07-01\nstatus: live\n---\n"


def run(body, grace_days=3):
    return rp.rotate_text(FM + body, "EQ", "pending.md", grace_days, TODAY)


def check(name, cond, detail=""):
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        print(f"FAIL: {name} {detail}")


# 1 — fully-done old section moves whole, header stamped
body = (
    "\n## finished thing (2026-07-01)\n*intro line*\n\n"
    "- [x] did A\n- [x] did B\n\n---\n\n"
    "## still open (2026-07-01)\n\n- [ ] todo C\n"
)
live, append, s = run(body)
check("full-move: both done items moved", s["moved"] == 2 and s["full"] == 1, s)
check("full-move: section gone from live", "finished thing" not in live)
check("full-move: narrative intact in archive", "*intro line*" in append)
check("full-move: header stamped", "## finished thing (2026-07-01) (rotated 2026-07-27)" in append)
check("full-move: open section untouched", "- [ ] todo C" in live)

# 2 — a section with real open work left (not just a verify line): open
# items stay byte-identical, done blocks move, and a verify line riding
# alongside genuine open work stays put too (mixed sections aren't split).
body = (
    "\n## mixed session (2026-07-10)\n*context intro*\n\n"
    "- [x] shipped the fix\n"
    "- [ ] **Royce to confirm live** it works _(added 2026-07-10)_\n"
    "- [ ] a genuinely unbuilt follow-up, not a verify item\n"
)
live, append, s = run(body)
check("mixed: one done moved", s["moved"] == 1 and s["partial"] == 1, s)
check("mixed: no verify moved (real open work still there)", s["moved_verify"] == 0, s)
check("mixed: verify item stays put", "- [ ] **Royce to confirm live** it works _(added 2026-07-10)_" in live)
check("mixed: real open item stays", "- [ ] a genuinely unbuilt follow-up, not a verify item" in live)
check("mixed: intro stays live", "*context intro*" in live)
check("mixed: archive header notes the split",
      "## mixed session (2026-07-10) (rotated 2026-07-27 — open items remain in pending.md)" in append)
check("mixed: done item in archive", "- [x] shipped the fix" in append)

# 2b — the actual fix's target case: a section whose only remaining open
# item is a verify line (nothing left to build) rotates whole — done items
# to the archive as always, the verify line to the queue instead of
# pinning the write-up live forever.
body = (
    "\n## fully shipped but unconfirmed (2026-06-01)\n*shipped it*\n\n"
    "- [x] shipped the fix\n"
    "- [ ] **Royce to click through live** and confirm it works\n"
)
live, append, s = run(body)
check("2b: section leaves live file", "fully shipped but unconfirmed" not in live, live)
check("2b: done item archived", "- [x] shipped the fix" in append)
check("2b: narrative archived too", "*shipped it*" in append)
check("2b: one verify item moved", s["moved_verify"] == 1, s)
check("2b: queue append has the verify line",
      "- [ ] **Royce to click through live** and confirm it works" in s["queue_append"], s)
check("2b: queue append traces its source section",
      "**From:** fully shipped but unconfirmed (2026-06-01)" in s["queue_append"], s)

# 2c — still real open work alongside a verify line: the section must NOT
# rotate, and the verify line must NOT move — this is what stops the split
# from over-firing on sections that aren't actually done yet.
body = (
    "\n## still real work left (2026-06-01)\n\n"
    "- [x] done part\n"
    "- [ ] Royce to click through live and confirm\n"
    "- [ ] build the second half of this feature\n"
)
live, append, s = run(body)
check("2c: section stays live (real work remains)", "still real work left" in live)
check("2c: verify line stays put, not queued", "Royce to click through live and confirm" in live)
check("2c: nothing queued", s.get("queue_append", "") == "", s)
check("2c: moved_verify is 0", s["moved_verify"] == 0, s)

# 2d — a section with ONLY a verify item, no done items at all (e.g. a
# doc-only note with nothing to "credit" as shipped) still rotates and
# queues cleanly rather than getting stuck on the moved_done==0 early exit.
body = "\n## nothing built, just a note (2026-06-01)\n\n- [ ] Royce to spot-check this live\n"
live, append, s = run(body)
check("2d: section leaves live file", "nothing built, just a note" not in live, live)
check("2d: verify item queued", s["moved_verify"] == 1, s)
check("2d: nothing archived (no done items)", s["moved"] == 0, s)

# 3 — section inside the grace window is untouched even if fully done
body = "\n## fresh work (2026-07-26)\n\n- [x] just did this\n"
live, append, s = run(body)
check("grace: nothing moved", s["moved"] == 0 and live is None, s)

# 4 — undated section with done items counts as old and rotates
body = "\n## undated leftovers\n\n- [x] ancient done thing\n"
live, append, s = run(body)
check("undated: rotates", s["moved"] == 1 and "ancient done thing" in append, s)

# 5 — continuation lines travel with their bullet
body = (
    "\n## wrapped bullets (2026-06-01)\n\n"
    "- [x] done with a wrapped\n  continuation line here\n"
    "- [ ] open with its own\n  wrapped continuation\n"
)
live, append, s = run(body)
check("continuation: moved with done bullet", "  continuation line here" in append)
check("continuation: stayed with open bullet", "  wrapped continuation" in live)
check("continuation: not duplicated", "wrapped continuation" not in append)

# 6 — '(added 2026-07-26)' style dates on the header also trigger grace
body = "\n## thing (added 2026-07-26)\n\n- [x] recent done\n"
live, append, s = run(body)
check("grace via added-date: nothing moved", s["moved"] == 0, s)

# 7 — no done items anywhere -> no-op
live, append, s = run("\n## only open (2026-06-01)\n\n- [ ] todo\n")
check("no-op: live is None", live is None and s["moved"] == 0)

# 8 — plain (non-checkbox) notes in a mixed section stay live
body = (
    "\n## with notes (2026-06-01)\n\n"
    "- [x] done thing\n- [ ] open thing\n\n"
    "### Notes\n- plain note bullet, no checkbox\n"
)
live, append, s = run(body)
check("notes: stay live", "- plain note bullet, no checkbox" in live)
check("notes: not archived", "plain note" not in append)

# 9 — regression (found 2026-07-27): a '[~]' (partial/in-progress) item must
# never be whole-section-archived alongside real done items, and must never
# itself be moved to the archive.
body = (
    "\n## partial only (2026-06-01)\n"
    "*intro*\n\n"
    "- [~] still partially applied\n"
    "- [x] this part is done\n"
)
live, append, s = run(body)
check("partial: section NOT whole-moved", live is not None and "- [~] still partially applied" in live, live)
check("partial: intro stays live", live is not None and "*intro*" in live)
check("partial: done bullet moved", "- [x] this part is done" in append)
check("partial: partial bullet never archived", "still partially applied" not in append)

# 9 — conservation across a realistic multi-section file
body = (
    "\npreamble text\n\n"
    "## a (2026-06-01)\n- [x] a1\n- [x] a2\n\n---\n\n"
    "## b (2026-06-05)\n- [x] b1\n- [ ] b2\n- [ ] b3\n\n---\n\n"
    "## c (2026-07-26)\n- [x] c1\n- [ ] c2\n\n---\n\n"
    "## d (2026-06-10)\n- [ ] d1\n"
)
live, append, s = run(body)
open_live = [l for l in live.split("\n") if l.startswith("- [ ]")]
done_arch = [l for l in append.split("\n") if l.strip().startswith("- [x]")]
check("conservation: 4 open kept", len(open_live) == 4, open_live)
check("conservation: 3 done archived (c1 in grace)", len(done_arch) == 3, done_arch)
check("conservation: c1 still live", "- [x] c1" in live)
check("conservation: preamble kept", "preamble text" in live)
check("conservation: frontmatter last_updated bumped", "last_updated: 2026-07-27" in live)

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
