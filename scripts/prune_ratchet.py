#!/usr/bin/env python3
"""Keep the substrate pruned by refusing to let it re-bloat.

Why this and not a bigger cleanup (2026-08-15). The repair campaign that added
this file kept hitting the same wall: every previous cleanup was correct on the
day and false a month later. The 2026-07-20 root pass had four of its nine
justifications expire inside four weeks. eq/pending.md was swept repeatedly and
grew 17 KB -> 491 KB anyway. A prune is an event; the thing that was missing is
a property.

So this does not prune. It ratchets: it measures the shapes that actually grew
and fails when they grow past where they are today. Cleanup is then somebody's
deliberate choice, but re-bloat is not available by default.

What it measures, and why each one:

  residue      Open `- [ ]` items sitting under a heading that says the work
               shipped/closed/merged/deployed. 385 of eq/pending.md's 635 open
               items were this -- follow-up notes stapled to finished sessions
               and never ticked. They are what made the queue unreadable, and
               nothing counted them.

  root_files   Loose .md at repo root. Went 21 -> 16 on 2026-08-15. Root is the
               first thing every tool sees; it silts up because a dated one-off
               is always easier to drop here than to file.

  archive_unindexed
               Files in archive/ with no row in archive/README.md. Archiving
               without recording WHY is how a file becomes unrevivable -- and
               how the next pass re-derives the same evidence from scratch.

Thresholds are the measured state on 2026-08-15, not aspirations. That is the
point: they can only be lowered. Raising one is a deliberate, reviewable edit
with a reason, which is exactly the conversation that never happened while
pending.md quietly quadrupled.

Run:   python scripts/prune_ratchet.py
Gate:  exit 1 when any metric exceeds its ceiling.
       PRUNE_RATCHET_REPORT=1 reports without gating.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PENDING_FILES = ["eq/pending.md", "sks/pending.md", "ops/pending.md"]

# A heading whose own words say the work is finished. Deliberately narrow --
# these are the exact words the substrate uses, and a looser pattern would
# sweep in genuinely open sections.
DONE_HEADING = re.compile(
    r"\b(shipped|closed|live|merged|deployed|fixed|done|resolved)\b", re.I
)
OPEN_ITEM = re.compile(r"^\s*-\s*\[ \]")
HEADING = re.compile(r"^##\s+")

# Measured 2026-08-15: residue 412 (eq 390 / sks 15 / ops 7), root 16,
# archive-unindexed 0. Lower these as the substrate improves; raising one needs
# a reason in the commit message.
#
# On headroom. Residue gets ~9% because a normal session legitimately adds a
# few follow-ups under a section it just closed, and a ceiling that trips on
# ordinary work is a ceiling somebody disables -- the same failure this
# campaign already hit once, building a sync check that shouted at every
# feature branch. 450 still catches the shape that actually went wrong
# (pending.md grew 17 KB -> 491 KB; residue does not drift to 450 by accident).
#
# root_files and archive_unindexed get NO headroom, deliberately. Adding a
# loose file to root, or archiving one without recording why, should both be
# arguments you have on purpose. They are rare events, so the friction is
# cheap and lands exactly where the judgement is needed.
CEILINGS = {
    "residue": 450,
    "root_files": 16,
    "archive_unindexed": 0,
}


def count_residue(rel):
    """Open items sitting under a heading that claims the work is done."""
    path = os.path.join(ROOT, rel)
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().split("\n")
    except OSError:
        return None

    heading, residue = "", 0
    for line in lines:
        if HEADING.match(line):
            heading = line
        elif OPEN_ITEM.match(line) and DONE_HEADING.search(heading):
            residue += 1
    return residue


def count_root_files():
    return len(
        [
            f
            for f in os.listdir(ROOT)
            if f.endswith(".md") and os.path.isfile(os.path.join(ROOT, f))
        ]
    )


def count_archive_unindexed():
    """archive/ files with no mention in archive/README.md.

    Boundary-matched, for the same reason index_drift.py is: a bare substring
    test lets a shorter filename hide inside a longer one.
    """
    adir = os.path.join(ROOT, "archive")
    readme = os.path.join(adir, "README.md")
    try:
        with open(readme, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return None

    missing = []
    for dirpath, _, filenames in os.walk(adir):
        for name in filenames:
            if not name.endswith(".md") or name == "README.md":
                continue
            if not re.search(r"(?<![A-Za-z0-9_.-])" + re.escape(name), text):
                missing.append(os.path.relpath(os.path.join(dirpath, name), ROOT))
    return missing


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("--- Prune ratchet (measured ceilings, lower-only) ---\n")
    failures = []

    total_residue = 0
    for rel in PENDING_FILES:
        n = count_residue(rel)
        if n is None:
            print(f"  {'--':>5}  {rel} (not found)")
            continue
        total_residue += n
        print(f"  {n:>5}  residue items in {rel}")
    print(
        f"  {total_residue:>5}  TOTAL residue"
        f"   ceiling {CEILINGS['residue']}"
    )
    if total_residue > CEILINGS["residue"]:
        failures.append(
            f"residue is {total_residue}, over the ceiling of {CEILINGS['residue']}. "
            f"These are open [ ] items under headings that say the work already "
            f"shipped -- close them, or move them somewhere they read as real work."
        )

    root_n = count_root_files()
    print(f"\n  {root_n:>5}  loose .md at repo root   ceiling {CEILINGS['root_files']}")
    if root_n > CEILINGS["root_files"]:
        failures.append(
            f"repo root has {root_n} loose .md files, over the ceiling of "
            f"{CEILINGS['root_files']}. A dated one-off belongs in a tier folder "
            f"or archive/, not at root."
        )

    missing = count_archive_unindexed()
    if missing is None:
        print("\n  archive/README.md unreadable — skipped")
    else:
        print(
            f"\n  {len(missing):>5}  archive files with no row in archive/README.md"
            f"   ceiling {CEILINGS['archive_unindexed']}"
        )
        for m in missing[:10]:
            print(f"         - {m}")
        if len(missing) > CEILINGS["archive_unindexed"]:
            failures.append(
                f"{len(missing)} archived file(s) carry no 'why archived' row. "
                f"Archiving without the reason is how a file becomes unrevivable "
                f"and how the next pass re-derives the same evidence from scratch."
            )

    print()
    if failures:
        print("FAIL")
        for f in failures:
            print(f"  - {f}")
        print(
            "\n  These ceilings are the measured state on 2026-08-15, not targets.\n"
            "  Raising one is allowed but must be deliberate and explained in the\n"
            "  commit -- the failure mode this guards is the one where nobody ever\n"
            "  had that conversation and the file quietly quadrupled."
        )
        if os.environ.get("PRUNE_RATCHET_REPORT") == "1":
            print("\n  (PRUNE_RATCHET_REPORT=1 — reporting only, not gating)")
            return 0
        return 1

    print("OK — nothing has re-bloated past its ceiling")
    return 0


if __name__ == "__main__":
    sys.exit(main())
