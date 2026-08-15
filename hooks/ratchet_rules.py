#!/usr/bin/env python3
"""The one definition of "is this guard overdue for promotion".

There were two, and they disagreed:

  hooks/session_start.py     rec >= 2 and rung < 4        (target hardcoded)
  .github/scripts/guard_ratchet.py
                             rec >= 2 and rung < target   (target read)

Latent today only because no entry with recurrences >= 2 carries a target_rung
below 4. F3 sits at target_rung: 3 — one more recurrence and the gate a session
sees and the issue CI opens would permanently disagree. Two implementations of
one rule, free to drift, is the exact shape of F13; a guard built by copy-paste
reproduces the failure it exists to prevent. So both now import this.

Two behaviour changes came with the merge, both fixing real holes:

1. **Field matching is boundary-anchored.** session_start.py searched
   `rung:\\s*(\\d+)`, which also matches the tail of `target_rung: 3`. It read
   the right value only because `rung:` happens to be listed before
   `target_rung:` in every current entry — flip the field order and the gate
   silently compares a value against itself. Same substring-collision class as
   the index_drift bug fixed in this campaign.

2. **Recurrence is urgency, not eligibility.** The old rule required
   `recurrences >= 2`, so a failure already KNOWN to be unguarded could never
   be raised. F4 and F5 both sit at rung 0 with a stated target of 3 and
   recurrences of 1: the ledger says out loud that they need a CI guard, and
   the ratchet was structurally incapable of ever saying so. Waiting for a
   second occurrence to act on a hazard you have already written down is the
   opposite of a ratchet. Now anything below its own declared target is DUE;
   two-or-more recurrences make it OVERDUE.
"""
import re

LADDER = {
    0: "unknown / no guard",
    1: "prose",
    2: "session checklist",
    3: "CI (catches after)",
    4: "hook (prevents)",
}

# Boundary-anchored so `target_rung:` cannot satisfy a search for `rung:`.
# `_` is a word character, so \b does not help here — an explicit negative
# lookbehind on the preceding character is what actually separates them.
RE_RECURRENCES = re.compile(r"(?<![A-Za-z0-9_])recurrences:\s*(\d+)")
RE_RUNG = re.compile(r"(?<![A-Za-z0-9_])rung:\s*(\d+)")
RE_TARGET = re.compile(r"(?<![A-Za-z0-9_])target_rung:\s*(\d+)")

DEFAULT_TARGET = 4


def parse_entry(block):
    """(recurrences, rung, target) from one failures.md entry body.

    Missing recurrences/rung read as 0 — an entry that forgot to declare a rung
    is unguarded until it says otherwise, which is the safe direction. Missing
    target falls back to the ladder top.
    """
    rec = RE_RECURRENCES.search(block)
    rung = RE_RUNG.search(block)
    target = RE_TARGET.search(block)
    return (
        int(rec.group(1)) if rec else 0,
        int(rung.group(1)) if rung else 0,
        int(target.group(1)) if target else DEFAULT_TARGET,
    )


def classify(recurrences, rung, target):
    """None | 'DUE' | 'OVERDUE'.

    DUE     — below its own declared target. The ledger already says this needs
              a stronger guard than it has.
    OVERDUE — that, and it has escaped the same guard more than once. A lesson
              that failed twice IS the thing that failed.
    """
    if rung >= target:
        return None
    return "OVERDUE" if recurrences >= 2 else "DUE"


def split_entries(failures_text):
    """Yield (id, block) per entry in system/failures.md."""
    for blk in re.split(r"\n\s*-\s+id:\s*", failures_text)[1:]:
        yield blk.split("\n", 1)[0].strip(), blk


def scan(failures_text):
    """[(id, title, recurrences, rung, target, verdict)] for everything not at target."""
    found = []
    for fid, blk in split_entries(failures_text):
        rec, rung, target = parse_entry(blk)
        verdict = classify(rec, rung, target)
        if verdict is None:
            continue
        title = re.search(r"title:\s*(.+)", blk)
        found.append(
            (fid, title.group(1).strip() if title else "", rec, rung, target, verdict)
        )
    return found
