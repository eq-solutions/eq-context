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

LADDER = {0: "unknown", 1: "prose lesson", 2: "session checklist",
          3: "CI check (catches after)", 4: "HOOK (prevents)"}

src = open("system/failures.md", encoding="utf-8").read()
due = []
for blk in re.split(r"\n\s*-\s+id:\s*", src)[1:]:
    fid = blk.split("\n", 1)[0].strip()
    g = lambda k, d=None: (re.search(rf"{k}:\s*(.+)", blk) or [None, d])[1]
    rec = int((re.search(r"recurrences:\s*(\d+)", blk) or [0, 0])[1])
    rung = int((re.search(r"\brung:\s*(\d+)", blk) or [0, 0])[1])
    target = int((re.search(r"target_rung:\s*(\d+)", blk) or [0, 4])[1])
    if rec >= 2 and rung < target:
        due.append(dict(id=fid, title=(g("title") or "").strip(), rec=rec,
                        rung=rung, target=target, guard=(g("guard") or "").strip()))

if not due:
    print("guard-ratchet: no promotions due.")
    with open(os.environ.get("GITHUB_OUTPUT", "/dev/null"), "a") as fh:
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
