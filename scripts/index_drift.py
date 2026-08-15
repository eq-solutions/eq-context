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
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

# tier name -> (folder relative to repo root, readme relative to repo root, recursive?)
TIERS = {
    "root": (".", "README.md", False),
    "system": ("system", "system/README.md", True),
    # rules/ was absent from this map until 2026-08-15 despite every file in it
    # being read_priority: critical. The consequence was live:
    # rules/gap-protocol.md is missing from CLAUDE.md section 8, so /gap is
    # undiscoverable from the contract while /decide and /reflect are both
    # documented. rules/ has no README, so it indexes against CLAUDE.md, which
    # is where its files are actually meant to be listed.
    "rules": ("rules", "CLAUDE.md", True),
    "eq": ("eq", "eq/README.md", True),
    "sks": ("sks", "sks/README.md", True),
    "sks-team": ("sks-team", "sks-team/README.md", True),
    "ops": ("ops", "ops/README.md", True),
    "archive": ("archive", "archive/README.md", True),
    # The machinery tiers, added 2026-08-15. Until then the prose half of the
    # substrate had a CI-enforced per-file index and the executable half had
    # none: 17 of 18 scripts, all 22 workflows and all 6 CI scripts were
    # unlisted anywhere, and hooks/README.md had fallen four files behind.
    # All four point at one home so there is a single place to look and a
    # single place to keep current.
    "hooks": ("hooks", "system/machinery.md", False, (".py", ".json")),
    "scripts": ("scripts", "system/machinery.md", False, (".py",)),
    "ci-scripts": (".github/scripts", "system/machinery.md", False, (".py",)),
    "workflows": (".github/workflows", "system/machinery.md", False, (".yml",)),
}

# Root-level files that are their own special-cased pointers, not tier content —
# excluded from root's index requirement so this check doesn't flag them forever.
ROOT_EXEMPT = {
    "README.md", "CLAUDE.md", "AGENTS.md", "CHAT-PROMPT.md", "COWORK-PROMPT.md",
    "CHATGPT-PROMPT.md", "GROK-PROMPT.md", "AUTONOMOUS-SPRINT-RULES.md",
}


def discover_md_files(folder_abs, recursive, extensions=(".md",)):
    """List matching basenames in folder_abs (pure: no README exclusion here).

    `extensions` exists so the machinery tiers can be checked too. The prose
    tiers had a per-file index enforced here for months while hooks/, scripts/
    and .github/ had none — which is the half where a filename tells you least
    (substrate_honesty.py vs prune_ratchet.py vs claim_expiry.py).
    """
    files = []
    for ext in extensions:
        if recursive:
            files += glob.glob(os.path.join(folder_abs, "**", "*" + ext), recursive=True)
        else:
            files += glob.glob(os.path.join(folder_abs, "*" + ext))
    return sorted(
        set(os.path.relpath(f, folder_abs).replace(os.sep, "/") for f in files)
    )


def find_orphans(relative_paths, readme_text, readme_basename, exempt=frozenset()):
    """Pure: which relative_paths (e.g. 'changelog/shell.md') are unmentioned in
    readme_text. A file is considered indexed if its basename appears anywhere
    in the README text — loose on purpose (table, prose link, either is fine).

    Matched on a filename BOUNDARY, not as a bare substring. The old test was
    `if base not in readme_text`, which meant a shorter name matched inside a
    longer one: "service.md" was reported as indexed because the README mentions
    "eq-service.md". In eq/ alone that collision hid four changelogs —
    service.md, cards.md, field.md and shell.md — every one of which is half of
    a real duplicate pair, which is exactly what this check exists to surface.

    The boundary is "not preceded by a filename character". A leading `/` still
    counts as a mention, so `eq/changelog/shell.md` in a link indexes
    `shell.md` — that is the intended looseness. `eq-shell.md` does not.
    """
    orphans = []
    for rel in relative_paths:
        base = os.path.basename(rel)
        if base == readme_basename or base in exempt:
            continue
        if not re.search(r"(?<![A-Za-z0-9_.-])" + re.escape(base), readme_text):
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
    for tier, spec in TIERS.items():
        folder, readme_rel, recursive = spec[0], spec[1], spec[2]
        extensions = spec[3] if len(spec) > 3 else (".md",)
        folder_abs = os.path.join(ROOT, folder)
        readme_abs = os.path.join(ROOT, readme_rel)
        if not os.path.isfile(readme_abs):
            print(f"  ?     {tier:<10} no README at {readme_rel}, skipped")
            continue

        with open(readme_abs, "r", encoding="utf-8") as fh:
            readme_text = fh.read()

        files = discover_md_files(folder_abs, recursive, extensions)
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
