#!/usr/bin/env python3
"""Every changelog file for one product must explain its own duplication.

Why (2026-08-15). eq/changelog/ held 4 dead twins -- cards.md, eq-field.md,
shell.md, service.md -- each superseded weeks ago, each still sitting in the
live folder. That is how a 5th pair went unnoticed for longer than it should
have: eq-service.md and eq-solves-service.md were BOTH live, BOTH appended on
the same day by different sessions, and PR #727 got recorded as "open, holds
for Royce" a full day after it had actually merged, because whichever file a
session opened first was the one it trusted.

This does not force a resolution. Consolidating two live histories into one is
a judgement call about which record survives -- that stays Royce's, same
posture as the archive/README.md "why archived" requirement. What this closes
is the SILENT half: a duplicate with no marker looks, to a session that only
opens one of the two files, like a complete history. The fix is not merging
content, it's making the gap impossible to miss.

THE RULE. Group changelog files by product slug (eq-shell / eq-solves-service
both mean "service" -- the stripped prefixes are the ones actually in use in
this folder). A group of one is fine. A group of more than one is fine ONLY if
every member is self-marked as one of:

  superseded_by: <filename>   in frontmatter -- "I am the dead one, read X"
  UNRECONCILED PAIR            anywhere in the file -- "I know about my twin,
                                unresolved, flagged for Royce"

A file in a multi-member group with neither marker fails: either a genuinely
new duplicate appeared, or an old one lost its marker. A group where every
member points away (all superseded_by, nobody canonical) also fails -- that is
a set of pointers to nothing. Cross-checked: every superseded_by target must
exist on disk in the same folder, or the pointer itself is the defect.

Run:   python scripts/changelog_duplicates.py
Gate:  exit 1 on any unmarked or dangling duplicate.
       CHANGELOG_DUP_REPORT=1 reports without gating.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
CHANGELOG_DIR = os.path.join(ROOT, "eq", "changelog")

sys.path.insert(0, HERE)
from review_clock import parse_frontmatter  # noqa: E402  -- one parser, not a third copy

# Longest prefix first, so "eq-solves-" strips before the shorter "eq-" would.
PREFIXES = ("eq-solves-", "eq-")

UNRECONCILED_MARK = re.compile(r"UNRECONCILED PAIR", re.I)


def slug(filename):
    """'eq-solves-service.md' / 'eq-service.md' / 'service.md' -> 'service'."""
    stem = filename[:-3] if filename.lower().endswith(".md") else filename
    low = stem.lower()
    for p in PREFIXES:
        if low.startswith(p):
            return low[len(p):]
    return low


def classify(filename, text, group_files):
    """Return (marked, reason) for ONE file in isolation.

    'marked' means this specific file explains ITS OWN place in the
    duplicate group -- either it points at a live sibling via
    superseded_by, or it carries the UNRECONCILED marker. A file with
    neither is not automatically wrong (it might be the one canonical
    file the others point at) -- group_status() below is what decides
    that, using this per-file result as its raw material.
    """
    fm = parse_frontmatter(text)
    target = fm.get("superseded_by", "").strip()
    if target:
        if target not in group_files:
            return False, f"superseded_by: {target!r} does not match any file in its own duplicate group {sorted(group_files)}"
        return True, f"superseded_by: {target}"
    if UNRECONCILED_MARK.search(text):
        return True, "UNRECONCILED PAIR marker present"
    return False, "no superseded_by frontmatter key and no UNRECONCILED PAIR marker"


def group_status(members, texts):
    """members: [filenames] sharing a slug. texts: {filename: content}.

    Returns a list of problem strings (empty = this group is fully explained).

    The rule is deliberately minimal -- catch a SILENT duplicate, nothing
    more. A file is "explained" if it points validly at a sibling via
    superseded_by, or carries the UNRECONCILED PAIR marker. A "bare" file
    (neither) is allowed ONLY if at least one sibling's superseded_by names
    it -- i.e. something in the group actually vouches for it as canonical.
    A bare file nobody points at is the actual failure this exists to catch:
    a duplicate where nothing anywhere says so.

    Mutation-tested 2026-08-15: stripping the marker from ONE side of a
    2-file unreconciled pair, leaving it bare with an unreconciled sibling
    and no pointer relationship between them, must fail. An earlier version
    of this rule ("at most one bare file is fine, full stop") missed this --
    a lone bare file was presumed canonical by ELIMINATION, with nothing
    checking that anyone actually endorsed it. That is precisely the shape of
    the real regression this tool exists to prevent: a live file that quietly
    stops explaining itself.

    This does NOT require every group to resolve to one uniform shape. The
    real live case that forced this design (2026-08-15): eq/changelog/'s
    "service" slug has THREE files -- service.md (dead, superseded_by:
    eq-service.md), and eq-service.md / eq-solves-service.md (both live, both
    UNRECONCILED, neither superseding the other). That is one dead pointer
    plus a genuinely unresolved pair, in the same group. An earlier version of
    this function required either "exactly one bare file + everyone else
    points at it" XOR "every file is marked UNRECONCILED" -- two rigid shapes
    that cannot both be true at once, so the real 3-file group failed no
    matter which shape it was checked against. Counting bare files directly,
    instead of matching group-wide shapes, handles the mix without a special
    case.

    Deliberately does not call classify() in a loop: an earlier version tried
    to derive these states by grepping classify()'s human-readable reason
    string for the word "UNRECONCILED" -- which also appears in the sentence
    explaining that the marker is ABSENT, so "doesn't have it" and "has it"
    matched the same substring. classify() stays as its own tested, correct,
    single-file check; this function reads the raw markers directly.
    """
    member_set = set(members)
    has_target = {}
    target_valid = {}
    has_unreconciled = {}
    for fn in members:
        fm = parse_frontmatter(texts[fn])
        t = fm.get("superseded_by", "").strip()
        has_target[fn] = bool(t)
        target_valid[fn] = (t in member_set) if t else None
        has_unreconciled[fn] = bool(UNRECONCILED_MARK.search(texts[fn]))

    dangling = [fn for fn in members if has_target[fn] and not target_valid[fn]]
    problems = [
        f"{fn}: superseded_by: {parse_frontmatter(texts[fn]).get('superseded_by','').strip()!r} "
        f"does not match any file in its own duplicate group {sorted(member_set)}"
        for fn in dangling
    ]

    # Only VALID targets count as vouching -- a typo'd/dangling superseded_by
    # (already reported above) does not get to also silently excuse the file
    # it was clumsily trying to point at.
    valid_targets = {
        parse_frontmatter(texts[fn]).get("superseded_by", "").strip()
        for fn in members
        if has_target[fn] and target_valid[fn]
    }

    bare = [fn for fn in members if not has_target[fn] and not has_unreconciled[fn]]
    for fn in bare:
        if fn not in valid_targets:
            problems.append(
                f"{fn}: no superseded_by frontmatter key and no UNRECONCILED PAIR marker, "
                f"and nothing in the group points at it via superseded_by either "
                f"(one of {sorted(member_set)})"
            )

    return problems


def scan(changelog_dir=CHANGELOG_DIR):
    """Returns (groups, problems). groups: {slug: [filenames]}. problems: [str]."""
    if not os.path.isdir(changelog_dir):
        return {}, [f"{changelog_dir} not found"]

    files = sorted(f for f in os.listdir(changelog_dir) if f.endswith(".md"))
    groups = {}
    for f in files:
        groups.setdefault(slug(f), []).append(f)

    problems = []
    for s, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        texts = {}
        for fn in members:
            with open(os.path.join(changelog_dir, fn), encoding="utf-8", errors="replace") as fh:
                texts[fn] = fh.read()
        for p in group_status(members, texts):
            problems.append(f"{s}: {p}")
    return groups, problems


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    groups, problems = scan()
    dup_groups = {s: m for s, m in groups.items() if len(m) > 1}

    print("--- Changelog duplicate scan ---\n")
    print(f"  {len(groups)} product(s), {len(dup_groups)} with more than one file\n")
    for s, members in sorted(dup_groups.items()):
        flag = "FAIL" if any(s in p for p in problems) else "ok  "
        print(f"  {flag}  {s:<10} {members}")

    print()
    if problems:
        print("FAIL:")
        for p in problems:
            print(f"  - {p}")
        print(
            "\n  A duplicate is allowed to exist -- it is not allowed to be silent.\n"
            "  Add 'superseded_by: <live-file.md>' to the dead one's frontmatter, or\n"
            "  put the literal phrase UNRECONCILED PAIR in both files if neither is\n"
            "  dead yet (see eq/changelog/eq-service.md for the pattern)."
        )
        if os.environ.get("CHANGELOG_DUP_REPORT") == "1":
            print("\n  (CHANGELOG_DUP_REPORT=1 -- reporting only, not gating)")
            return 0
        return 1

    print("OK -- every changelog duplicate explains itself")
    return 0


if __name__ == "__main__":
    sys.exit(main())
