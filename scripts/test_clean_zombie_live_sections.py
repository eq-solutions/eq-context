#!/usr/bin/env python3
"""
Unit tests for clean_zombie_live_sections.clean_text.

Cross-platform, no network, no fixtures on disk. Builds synthetic live +
archive text and asserts what's removed, what's kept, and that nothing
genuinely open is ever touched.
Run: python scripts/test_clean_zombie_live_sections.py
"""
import sys

import clean_zombie_live_sections as czl

passed = failed = 0

LIVE_FM = "---\ntitle: EQ Shell — Pending\nlast_updated: 2026-07-01\nstatus: live\n---\n"
ARCH_FM = "---\ntitle: EQ Tier — Archive\nlast_updated: 2026-07-01\nstatus: archived\n---\n"


def run(live_body, archive_body):
    return czl.clean_text(LIVE_FM + live_body, ARCH_FM + archive_body)


def check(name, cond, detail=""):
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        print(f"FAIL: {name} {detail}")


# 1 — whole zombie: section fully done, exact match already in archive ->
# entire section dropped from live.
live = "\n## finished thing (2026-08-01)\n*intro*\n\n- [x] did A\n- [x] did B\n\n---\n\n" \
       "## still open (2026-08-01)\n\n- [ ] todo C\n"
arch = "\n## finished thing (2026-08-01) (rotated 2026-08-05)\n*intro*\n\n- [x] did A\n- [x] did B\n\n---\n\n"
text, r = run(live, arch)
check("whole-zombie: dropped", r["whole_zombies_dropped"] == 1, r)
check("whole-zombie: gone from live", "finished thing" not in text)
check("whole-zombie: unrelated section untouched", "- [ ] todo C" in text and "still open" in text)

# 2 — mixed zombie: section has real open work AND some already-archived
# done items -> only the confirmed-zombie done blocks are removed, open
# items and header/intro survive byte-identical.
live = "\n## mixed session (2026-07-10)\n*context intro*\n\n" \
       "- [x] shipped the fix\n" \
       "- [ ] a genuinely unbuilt follow-up\n"
arch = "\n## mixed session (2026-07-10) (rotated 2026-07-15 — open items remain in eq/pending/eq-shell.md)\n\n" \
       "- [x] shipped the fix\n\n---\n\n"
text, r = run(live, arch)
check("mixed: one block removed", r["zombie_blocks_removed"] == 1, r)
check("mixed: section kept (open work remains)", "mixed session" in text)
check("mixed: zombie done line gone", "- [x] shipped the fix" not in text)
check("mixed: open item survives verbatim", "- [ ] a genuinely unbuilt follow-up" in text)
check("mixed: intro survives", "*context intro*" in text)

# 3 — a done item with NO matching archive entry is left completely alone
# (hasn't been through a successful rotation attempt yet).
live = "\n## never rotated (2026-08-20)\n\n- [x] did something real\n- [ ] still open\n"
arch = "\n## unrelated thing (2026-08-01)\n\n- [x] something else\n\n---\n\n"
text, r = run(live, arch)
check("no-match: nothing touched", r["sections_touched"] == 0, r)
check("no-match: signals no-write (None) rather than rewriting unchanged text", text is None, text)

# 4 — continuation lines are part of the block: a done item with an indented
# sub-bullet only counts as a zombie if the WHOLE block (all lines) matches
# the archive exactly, not just the first line.
live = "\n## multi-line done (2026-08-01)\n\n" \
       "- [x] did A\n  extra detail line\n" \
       "- [ ] open thing\n"
arch_full_match = "\n## multi-line done (2026-08-01) (rotated 2026-08-05 — open items remain in x)\n\n" \
                   "- [x] did A\n  extra detail line\n\n---\n\n"
text, r = run(live, arch_full_match)
check("continuation: full block matched and removed", r["zombie_blocks_removed"] == 1, r)
check("continuation: extra detail line gone with it", "extra detail line" not in text)

arch_partial_match = "\n## multi-line done (2026-08-01) (rotated 2026-08-05 — open items remain in x)\n\n" \
                      "- [x] did A\n\n---\n\n"  # missing the continuation line -- not an exact match
text2, r2 = run(live, arch_partial_match)
check("continuation: partial-text match does NOT remove (exact block required)", r2["sections_touched"] == 0, r2)

# 5 — a section with a matching key where every done item matches but one
# open item does NOT exist in the archive at all: section is kept (mixed),
# not dropped, since real open work remains.
live = "\n## partly done (2026-08-01)\n\n- [x] finished part\n- [~] still applying\n"
arch = "\n## partly done (2026-08-01) (rotated 2026-08-10 — open items remain in x)\n\n" \
       "- [x] finished part\n\n---\n\n"
text, r = run(live, arch)
check("partial-marker: section kept ([~] counts as unfinished)", "partly done" in text, r)
check("partial-marker: [~] line untouched", "- [~] still applying" in text)
check("partial-marker: done line removed", "- [x] finished part" not in text)

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
