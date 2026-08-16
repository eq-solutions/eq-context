#!/usr/bin/env python3
"""Every internal markdown link must resolve to a real file.

Why (2026-08-15). 20 of 261 internal links were broken -- including one in
suite-state.md, the file every session reads first. A broken link is worse
than no link: it teaches an agent a document doesn't exist, or worse, sends
it looking in the wrong place. The 20 fell into three real shapes, not one:

  moved but not repointed    5 links -- 4 root docs archived (this campaign,
                              phase 1) but nothing pointing at them was
                              updated; 1 root-relative path (suite-state.md's
                              own `changelog/eq-intake.md`) was simply missing
                              its `eq/` segment.
  wrong relative depth       9 links, all in one 2026-05-20 session log --
                              every `../identity/...` and `../cards/...`
                              needed an `eq/` segment that was never there.
                              Same bug, repeated by habit throughout one file.
  never existed              6 links -- 3 in two archived plan files were
                              Claude-memory citations ("Memory says (per
                              `supabase-architecture-decision.md` Phase 1.E)")
                              that got formatted as file links by habit; a
                              `git log --diff-filter=A` sweep confirmed no
                              commit ever added them. 1 more (a scoping doc
                              promised in three separate places) was simply
                              never written.

Fixed by correcting the resolvable ones and turning the unresolvable ones
into honest prose ("never a file in this repo" / "never actually written"),
matching the pattern eq/README.md already used for `eq/templates.md`. This
script is the guard that keeps the zero: ratchet, not cliff, at 0 -- unlike
prune_ratchet's residue ceiling, a broken link has no honest reason to exist,
so there is no headroom to give it.

Run:   python scripts/link_check.py
Gate:  exit 1 if any internal .md link is broken.
       LINK_CHECK_REPORT=1 reports without gating.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def find_md_files(root):
    """Tracked-looking .md files under root, skipping .git and other sessions'
    checked-out worktrees (.claude/worktrees/<name>/ is a full nested clone of
    this repo -- walking into it double-counts every file and re-resolves
    links against a copy that may be mid-edit, producing false positives that
    don't reproduce in a clean CI checkout, which has no worktree)."""
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root).replace(os.sep, "/")
        if rel_dir == ".claude":
            dirnames[:] = [d for d in dirnames if d != "worktrees"]
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__", ".pytest_cache", "node_modules")]
        for name in filenames:
            if name.endswith(".md"):
                out.append(os.path.relpath(os.path.join(dirpath, name), root))
    return sorted(p.replace(os.sep, "/") for p in out)


def internal_targets(text):
    """Yield the raw link target for every markdown link in text that looks
    like an internal .md reference -- external URLs, mailto:, and anchors-only
    links are excluded. Anchor fragments are stripped (resolution is by file,
    not by heading)."""
    for m in LINK_RE.finditer(text):
        target = m.group(1).split("#", 1)[0].strip()
        if not target:
            continue
        if target.startswith(("http://", "https://", "mailto:", "//")):
            continue
        if not target.lower().endswith(".md"):
            continue
        yield target


def check_file(rel_path, text, root):
    """Returns [(target, resolved_path)] for every broken link in this file."""
    file_dir = os.path.dirname(os.path.join(root, rel_path))
    broken = []
    for target in internal_targets(text):
        resolved = os.path.normpath(os.path.join(file_dir, target))
        if not os.path.isfile(resolved):
            broken.append((target, resolved))
    return broken


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    total_links = 0
    total_broken = 0
    by_file = {}

    for rel in find_md_files(ROOT):
        path = os.path.join(ROOT, rel)
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        targets = list(internal_targets(text))
        total_links += len(targets)
        broken = check_file(rel, text, ROOT)
        if broken:
            by_file[rel] = broken
            total_broken += len(broken)

    print("--- Internal link check ---\n")
    print(f"  {total_links} internal .md link(s) checked, {total_broken} broken\n")
    for rel, broken in sorted(by_file.items()):
        for target, resolved in broken:
            print(f"  BROKEN {rel} -> {target}")

    print()
    if total_broken:
        msg = f"{total_broken} broken internal link(s) found"
        print(f"FAIL: {msg}")
        print(
            "\n  A broken link has no honest reason to exist -- fix the path, or if\n"
            "  the target never existed, replace the link with plain text saying so\n"
            "  (see eq/README.md's `eq/templates.md` row for the established pattern)."
        )
        if os.environ.get("LINK_CHECK_REPORT") == "1":
            print("\n  (LINK_CHECK_REPORT=1 — reporting only, not gating)")
            return 0
        return 1

    print("ok: every internal link resolves")
    return 0


if __name__ == "__main__":
    sys.exit(main())
