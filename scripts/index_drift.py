#!/usr/bin/env python3
"""Index drift check — verify every tier README actually lists its own folder.

The 2026-07-19 full substrate audit found this as the single most common defect
class — sampling a handful of tiers by hand turned up a few missing files, but
running this check for real found 62 orphaned files across root/system/eq
alone. An index that's wrong is worse than no index — it actively misdirects
an agent into thinking a file doesn't exist. This check makes that class of
drift visible on every PR instead of waiting for the next manual audit.

Heuristic: for each tier README, every other .md file physically present in that
tier's folder must have its filename mentioned *somewhere* in the README's text
(table row, prose link, anywhere — deliberately loose so it doesn't force one
indexing format). A file whose name never appears is "orphaned" — present but
undiscoverable via the normal load path.

Report-only by default (matches substrate_honesty.py's pattern) — set
INDEX_DRIFT_STRICT=1 to exit non-zero on any orphan. CI sets it, since the
backlog this found was cleared in the same change that added the check —
there's nothing pre-existing to grandfather in.

Run:  python scripts/index_drift.py
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

# tier name -> (folder relative to repo root, readme relative to repo root, recursive?)
TIERS = {
    "root": (".", "README.md", False),
    "system": ("system", "system/README.md", True),
    "eq": ("eq", "eq/README.md", True),
    "sks": ("sks", "sks/README.md", True),
    "sks-team": ("sks-team", "sks-team/README.md", True),
    "ops": ("ops", "ops/README.md", True),
    "archive": ("archive", "archive/README.md", True),
}

# Root-level files that are their own special-cased pointers, not tier content —
# excluded from root's index requirement so this check doesn't flag them forever.
ROOT_EXEMPT = {
    "README.md", "CLAUDE.md", "AGENTS.md", "CHAT-PROMPT.md", "COWORK-PROMPT.md",
    "AUTONOMOUS-SPRINT-RULES.md",
}


def discover_md_files(folder_abs, recursive):
    """List .md basenames in folder_abs (pure: no README exclusion here)."""
    if recursive:
        pattern = os.path.join(folder_abs, "**", "*.md")
        files = glob.glob(pattern, recursive=True)
    else:
        pattern = os.path.join(folder_abs, "*.md")
        files = glob.glob(pattern)
    return sorted(os.path.relpath(f, folder_abs).replace(os.sep, "/") for f in files)


def find_orphans(relative_paths, readme_text, readme_basename, exempt=frozenset()):
    """Pure: which relative_paths (e.g. 'changelog/shell.md') are unmentioned in
    readme_text. A file is considered indexed if its basename appears anywhere
    in the README text — loose on purpose (table, prose link, either is fine).
    """
    orphans = []
    for rel in relative_paths:
        base = os.path.basename(rel)
        if base == readme_basename or base in exempt:
            continue
        if base not in readme_text:
            orphans.append(rel)
    return orphans


def main():
    # Windows consoles default to cp1252, which can't encode em/en-dashes this
    # script prints — force UTF-8 stdout (same fix session_start.py needed).
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    strict = os.environ.get("INDEX_DRIFT_STRICT") == "1"
    total_orphans = 0

    print("--- Index drift scan (files present but not mentioned in their tier README) ---")
    for tier, (folder, readme_rel, recursive) in TIERS.items():
        folder_abs = os.path.join(ROOT, folder)
        readme_abs = os.path.join(ROOT, readme_rel)
        if not os.path.isfile(readme_abs):
            print(f"  ?     {tier:<10} no README at {readme_rel}, skipped")
            continue

        with open(readme_abs, "r", encoding="utf-8") as fh:
            readme_text = fh.read()

        files = discover_md_files(folder_abs, recursive)
        exempt = ROOT_EXEMPT if tier == "root" else frozenset()
        orphans = find_orphans(files, readme_text, os.path.basename(readme_rel), exempt)

        if orphans:
            total_orphans += len(orphans)
            print(f"  DRIFT {tier:<10} {len(orphans)} of {len(files)} files unindexed in {readme_rel}:")
            for o in orphans:
                print(f"          - {folder}/{o}" if folder != "." else f"          - {o}")
        else:
            print(f"  ok    {tier:<10} {len(files)} files, all indexed in {readme_rel}")

    print()
    if total_orphans:
        msg = f"{total_orphans} orphaned file(s) found across all tiers"
        if strict:
            print(f"FAIL: {msg}")
            sys.exit(1)
        print(f"{msg} (report-only — set INDEX_DRIFT_STRICT=1 to gate on this)")
    else:
        print("ok: no index drift found")


if __name__ == "__main__":
    main()
