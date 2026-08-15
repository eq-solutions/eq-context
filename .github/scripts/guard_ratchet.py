#!/usr/bin/env python3
"""
guard-ratchet — the self-improving loop.

Reads system/failures.md. Any failure with recurrences >= 2 whose guard still sits
below rung 4 gets PROPOSED for promotion. Propose-only: this never edits a guard.

The ladder:
  0 unknown · 1 prose lesson · 2 checklist · 3 CI (catches after) · 4 hook (prevents)

Why prose is rung 1: on 2026-07-11 the F2 truncation lesson existed in lessons.md,
was READ that session, and still did not prevent the failure. Knowledge that depends
on an agent recalling the right line of 455 at the right instant is not a safeguard.
"""
import os, re, sys

# The promotion rule is IMPORTED, not restated. This file and
# hooks/session_start.py each used to carry their own copy and they already
# disagreed -- this one read target_rung, that one hardcoded 4. Two definitions
# of one rule, free to drift, is the shape of F13, so there is now exactly one:
# hooks/ratchet_rules.py.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "hooks"))
from ratchet_rules import LADDER, parse_entry, classify  # noqa: E402

src = open("system/failures.md", encoding="utf-8").read()
due = []
for blk in re.split(r"\n\s*-\s+id:\s*", src)[1:]:
    fid = blk.split("\n", 1)[0].strip()
    g = lambda k, d=None: (re.search(rf"{k}:\s*(.+)", blk) or [None, d])[1]
    rec, rung, target = parse_entry(blk)
    # Only OVERDUE opens an issue. Anything merely below its declared target is
    # surfaced by the session gate instead -- an issue per un-recurred entry
    # would file three on day one and train everyone to close them unread.
    if classify(rec, rung, target) == "OVERDUE":
        due.append(dict(id=fid, title=(g("title") or "").strip(), rec=rec,
                        rung=rung, target=target, guard=(g("guard") or "").strip()))

if not due:
    print("guard-ratchet: no promotions due.")
    # os.devnull, not "/dev/null" -- the literal makes every local run on
    # Windows crash after printing its result, which discourages running the
    # ratchet by hand at exactly the moment you would want to.
    with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as fh:
        fh.write("due=\n")
    sys.exit(0)

lines = ["## A safeguard has failed twice. It must climb.", "",
         "`guard-ratchet` is **propose-only**. Nothing has been changed. This is an argument, not an action.", ""]
for d in due:
    lines += [
        f"### {d['id']} — {d['title']}",
        f"- **Recurrences:** {d['rec']} — it has escaped the same guard more than once.",
        f"- **Current rung:** {d['rung']} ({LADDER.get(d['rung'],'?')})",
        f"- **Required rung:** {d['target']} ({LADDER.get(d['target'],'?')})",
        f"- **Guard:** {d['guard']}", "",
        "**A guard that failed twice IS the thing that failed.** Writing another lesson about it is",
        "rung 1 — the rung that already failed. Promote it or accept the failure recurs.", "",
    ]
lines += ["---", "_Oracle: reality (a failure that actually escaped). Not the substrate's opinion of itself._",
          "_Raised by `.github/workflows/guard-ratchet.yml` from `system/failures.md`._"]
body = "\n".join(lines)

print(body)
with open(os.environ.get("GITHUB_OUTPUT", "/dev/null"), "a") as fh:
    fh.write(f"due={','.join(d['id'] for d in due)}\n")
    fh.write("body<<RATCHET_EOF\n" + body + "\nRATCHET_EOF\n")
