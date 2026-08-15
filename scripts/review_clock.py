#!/usr/bin/env python3
"""Classify every doc as generated / record / state, and clock only the state.

THE PROBLEM (measured 2026-08-15). 174 files declared `status: live` and 82 of
them -- 47% -- had not been touched in over 30 days. Nothing noticed. The
substrate automates pruning of things that are DONE (rotate_pending.py), of
REGROWTH (prune_ratchet.py), and of GENERATED content (refresh_digest.py,
refresh_suite_state.py), but nothing at all detects a hand-written claim about
how things are *now* that quietly stopped being true. That is the shape behind
F1 and F13, and behind the `urjh` incident where the substrate pointed the whole
fleet at a deleted Supabase project for weeks.

WHY 47% IS THE WRONG NUMBER, AND WHY THAT MATTERS. Most of those 82 are not
stale, they are MISLABELLED. A session log from May is not out of date; it is a
record of May. Splitting them:

    generated    2 files    rebuilt from source, cannot rot
    record      94 files    dated, past-tense, true forever
    state       78 files    claims about now -- the ONLY kind that can lie

The real overdue list is 23, not 82. That distinction is the whole fix. A
blanket review clock over all 174 would have gone overdue on 82 files on day
one, which means it gets grandfathered at birth, which is F10 -- rung 4 on
paper, rung 0 in practice. Two per fortnight is a clock a solo operator
actually keeps. Eighty-two is a clock he mutes.

The substrate already half-knew this split and never named it:
frontmatter-check.yml exempts sessions/, archive/ and */changelog/ from its
required-key schema as "navigational or append-only, not governed docs". That
exemption list IS an unnamed record classification. This file names it and makes
it do work.

DERIVED, NOT STAMPED. `kind` is computed from the path, not written into 329
files. Two reasons. A hand-stamped field is manual curation, and the finding
that runs through this entire campaign is that manual curation decays in about
four weeks while generated or ratcheted state holds. And a derived rule means a
new session log filed tomorrow classifies correctly forever without anyone
remembering a convention. An explicit `kind:` in frontmatter overrides the
derivation, for the cases where the path guesses wrong.

The derivation DEFAULTS TO STATE. Only strong signals (a dated filename, or a
path under sessions/archive/changelog/sprints/progress) make something a record.
A wrong guess therefore costs an unnecessary review, never a missed one. That
asymmetry is deliberate: this guard's job is to over-report, not under-report.

DERIVED CLOCK, NOT A TYPED DEADLINE -- and this is the F3 distinction, which
matters more than it looks. F3 was a phantom deadline nobody owned that steered
two weeks of sessions. A date typed into frontmatter by hand is that failure
waiting to happen again. So the clock here is a property of what a file IS
(last_updated + a cadence set by read_priority), and it governs TRUST IN A FILE,
not priority of work. It says "this may be out of date," never "you must ship by
this date." Nothing here is allowed to create an obligation with a deadline.

GENERATED IS NOT AN EXEMPTION. Files rebuilt by cron get the TIGHTEST clock (3
days). If the nightly action dies, digest.md and suite-state.md silently freeze
while still reading as current -- suite-state.md's own body says "if this file
is >48h old, the cron is broken", which was a comment addressed to a human who
would have to notice. Now it trips. That turns the generated class from an
exemption into a cron-liveness check.

Run:   python scripts/review_clock.py
       REVIEW_CLOCK_LIST=1  also list every overdue state file
Gate:  exit 1 on a hard violation, or when overdue state files exceed the
       ceiling. REVIEW_CLOCK_REPORT=1 reports without gating.
"""
import datetime
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KINDS = ("generated", "record", "state")

# Rebuilt from source by a workflow. Named explicitly rather than pattern-matched
# because being wrong here means silently exempting a hand-written file.
GENERATED = {
    "digest.md",
    "suite-state.md",
    "sessions/INDEX.md",
}

# Path segments that make a file a record. These mirror frontmatter-check.yml's
# existing exemption list -- same judgement, now named and load-bearing.
RECORD_DIRS = {
    "sessions",
    "archive",
    "changelog",
    "sprints",
    "progress",
    "md-health-reports",
    "drafts",
}

# A date in the filename means the file is about that date. eq-platform-verified
# -state-2026-06-03.md cannot go stale; it was verified on 2026-06-03 and always
# will have been. substrate_honesty.py already uses this same signal.
DATED_NAME = re.compile(r"\d{4}-\d{2}-\d{2}")

# How long a state claim is trusted before it wants a look. Keyed on
# read_priority because that is the substrate's own existing measure of how much
# damage a wrong claim does -- a critical file is read at session start by every
# tool, so a false claim in one propagates immediately.
CADENCE = {
    "critical": 30,
    "high": 60,
}
DEFAULT_CADENCE = 90
GENERATED_CADENCE = 3

FM_DELIM = re.compile(r"^---\s*$")


def parse_frontmatter(text):
    """Return the frontmatter block as a dict. Empty dict when there is none."""
    lines = text.lstrip("﻿").split("\n")
    if not lines or not FM_DELIM.match(lines[0]):
        return {}
    fm = {}
    for line in lines[1:]:
        if FM_DELIM.match(line):
            return fm
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*?)\s*$", line)
        if m:
            fm[m.group(1).lower()] = m.group(2).strip().strip('"').strip("'")
    return {}  # unterminated block -- treat as absent rather than guessing


def classify(rel_path, frontmatter=None):
    """generated | record | state, from the path (explicit `kind:` wins).

    Pure. Defaults to 'state' so an unrecognised file is over-reviewed rather
    than silently trusted forever.
    """
    fm = frontmatter or {}
    explicit = fm.get("kind", "").strip().lower()
    if explicit:
        return explicit  # validated by the caller so a typo is a loud failure

    rel = rel_path.replace(os.sep, "/").lstrip("./")
    if rel in GENERATED:
        return "generated"

    parts = rel.split("/")
    if any(p in RECORD_DIRS for p in parts[:-1]):
        return "record"
    if DATED_NAME.search(parts[-1]):
        return "record"
    return "state"


def cadence_days(kind, read_priority):
    """Days a file of this kind is trusted. None means no clock (records)."""
    if kind == "generated":
        return GENERATED_CADENCE
    if kind == "record":
        return None
    return CADENCE.get((read_priority or "").strip().lower(), DEFAULT_CADENCE)


def parse_date(value):
    m = re.match(r"^(\d{4}-\d{2}-\d{2})", (value or "").strip())
    if not m:
        return None
    try:
        return datetime.date.fromisoformat(m.group(1))
    except ValueError:
        return None


def review_due(last_updated, cadence, explicit_review_by=None):
    """The date this file stops being trusted. None when it has no clock."""
    if explicit_review_by is not None:
        return explicit_review_by
    if cadence is None or last_updated is None:
        return None
    return last_updated + datetime.timedelta(days=cadence)


def days_overdue(due, today):
    if due is None:
        return 0
    return max(0, (today - due).days)


# Ratchet, not cliff -- the ceiling is where the substrate is today and can only
# be lowered. A gate that failed on day one would be grandfathered on day one,
# which is the failure it exists to prevent. Lowering this is the actual review
# work; raising it needs a reason in the commit message.
#
# 2026-08-15 first measurement:  3 generated / 234 record /  91 state, 15 overdue
# 2026-08-15 after the review:   3 generated / 237 record /  88 state,  5 overdue
#
# The 10 cleared in between were not cleared by bumping dates. Three were
# finished work still flying status: live (the executed canonical-readiness and
# Cards migration plans, and the go-live runbook) and became kind: record. Seven
# were re-verified against the live systems and corrected where they disagreed --
# spine.md's headline was 55 tables against a live 128, brand-sks.md still
# specified the retired #1F335C, and the Field visibility model claimed all 40
# people were hidden when all 83 are visible.
#
# The 5 that remain are SKS operational files (sks/active.md, sks-team/*) whose
# truth lives with Royce, not in any system this can query. They are left overdue
# on purpose: a number that stays honest is worth more than a number driven to
# zero by stamping files nobody read.
#
# No headroom, unlike prune_ratchet's residue ceiling. Residue gets slack because
# ordinary sessions legitimately add follow-ups and a gate that trips on normal
# work is a gate somebody disables. Staleness is the opposite shape: every commit
# that touches a state file bumps its last_updated and REMOVES it from this
# count, so normal work drives the number down, never up. It rises only when
# something ages out untouched, which is precisely the event worth stopping for.
STATE_OVERDUE_CEILING = 5


def iter_tracked_md():
    """Tracked .md paths, repo-relative, POSIX separators.

    git ls-files rather than os.walk so __pycache__, .pytest_cache and any
    untracked scratch file cannot influence a gate.
    """
    try:
        out = subprocess.run(
            ["git", "-C", ROOT, "ls-files", "*.md"],
            capture_output=True, text=True, timeout=30,
        )
        if out.returncode == 0:
            return [p for p in out.stdout.split("\n") if p.strip()]
    except Exception:
        pass
    found = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__", ".pytest_cache")]
        for name in filenames:
            if name.endswith(".md"):
                rel = os.path.relpath(os.path.join(dirpath, name), ROOT)
                found.append(rel.replace(os.sep, "/"))
    return sorted(found)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    today = datetime.date.today()
    ceiling = int(os.environ.get("REVIEW_CLOCK_CEILING", str(STATE_OVERDUE_CEILING)))

    counts = {k: 0 for k in KINDS}
    overdue = {k: [] for k in KINDS}
    hard = []
    unclocked_state = []

    for rel in iter_tracked_md():
        path = os.path.join(ROOT, rel)
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read(4000)
        except OSError:
            continue

        fm = parse_frontmatter(text)
        kind = classify(rel, fm)

        if kind not in KINDS:
            hard.append(f"{rel}: kind '{kind}' is not one of {'/'.join(KINDS)}")
            continue
        counts[kind] += 1

        explicit_by = parse_date(fm.get("review_by", ""))
        if kind == "record" and explicit_by is not None:
            hard.append(
                f"{rel}: a record carries review_by. A record is an account of "
                f"what happened; it is superseded, never reviewed. Either drop "
                f"review_by or set 'kind: state' if it is really a live claim."
            )
            continue

        last_updated = parse_date(fm.get("last_updated", ""))
        cadence = cadence_days(kind, fm.get("read_priority"))
        due = review_due(last_updated, cadence, explicit_by)

        if kind == "state" and due is None:
            # A live claim with no date can never be caught aging. Reported
            # separately from overdue -- it is a different repair (add the key).
            if fm:
                unclocked_state.append(rel)
            continue

        n = days_overdue(due, today)
        if n:
            overdue[kind].append((n, rel))

    for k in KINDS:
        overdue[k].sort(reverse=True)

    print("--- Review clock (only 'state' can go stale) ---\n")
    for k in KINDS:
        clock = {
            "generated": f"{GENERATED_CADENCE}d (cron liveness)",
            "record": "no clock",
            "state": f"{CADENCE['critical']}/{CADENCE['high']}/{DEFAULT_CADENCE}d by read_priority",
        }[k]
        print(f"  {counts[k]:>4}  {k:<10} {clock:<40} overdue: {len(overdue[k])}")

    # A dead cron is not a backlog item -- there are zero today, so this gates
    # immediately with nothing to grandfather.
    for n, rel in overdue["generated"]:
        hard.append(
            f"{rel}: {n}d past its {GENERATED_CADENCE}d refresh window. This file is "
            f"rebuilt by a workflow, so it being old means the workflow is not "
            f"running -- it will keep reading as current while it freezes."
        )

    if unclocked_state:
        print(f"\n  {len(unclocked_state)} state file(s) with no last_updated — cannot be clocked:")
        for rel in unclocked_state[:10]:
            print(f"         - {rel}")

    if overdue["state"]:
        print(f"\n  {len(overdue['state'])} state file(s) overdue (ceiling {ceiling}):")
        show = overdue["state"] if os.environ.get("REVIEW_CLOCK_LIST") == "1" else overdue["state"][:10]
        for n, rel in show:
            print(f"         {n:>4}d  {rel}")
        if len(show) < len(overdue["state"]):
            print(f"         ... and {len(overdue['state']) - len(show)} more (REVIEW_CLOCK_LIST=1)")

    print()
    if hard:
        print("FAIL — hard violations:")
        for h in hard:
            print(f"  - {h}")

    over = len(overdue["state"]) > ceiling
    if over:
        print(
            f"FAIL — {len(overdue['state'])} overdue state files, over the ceiling of {ceiling}.\n"
            f"  This ceiling is the measured state on 2026-08-15, not a target. It can\n"
            f"  only be lowered. Either review the oldest files and bump last_updated,\n"
            f"  or reclassify: if a file is an account of something that happened, it\n"
            f"  is a record — move it or set 'kind: record' and it stops asking."
        )

    if hard or over:
        if os.environ.get("REVIEW_CLOCK_REPORT") == "1":
            print("\n  (REVIEW_CLOCK_REPORT=1 — reporting only, not gating)")
            return 0
        return 1

    print("OK — no dead crons, no misclassified records, staleness within ceiling")
    return 0


if __name__ == "__main__":
    sys.exit(main())
