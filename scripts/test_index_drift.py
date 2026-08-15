#!/usr/bin/env python3
"""Unit tests for the pure classifier in index_drift.py.

No filesystem, no network — find_orphans() takes plain strings/lists.

Run:  python scripts/test_index_drift.py
"""
import os
import sys
import tempfile

from index_drift import discover_md_files, find_orphans


def check(name, got, want):
    if got != want:
        print(f"FAIL {name}: got {got!r}, want {want!r}")
        return 1
    print(f"ok   {name}")
    return 0


def main():
    f = 0

    # A file mentioned anywhere in the README text is not an orphan.
    readme = "See [products.md](products.md) and the pending list in pending.md."
    f += check(
        "mentioned file -> not orphaned",
        find_orphans(["products.md", "pending.md"], readme, "README.md"),
        [],
    )

    # A file never mentioned is an orphan.
    f += check(
        "unmentioned file -> orphaned",
        find_orphans(["products.md", "changelog/shell.md"], readme, "README.md"),
        ["changelog/shell.md"],
    )

    # Matching is on basename, so a nested path still counts as indexed if its
    # filename appears anywhere in the text (loose by design).
    readme2 = "The shell changelog lives at eq-shell.md."
    f += check(
        "nested path matched by basename",
        find_orphans(["changelog/eq-shell.md"], readme2, "README.md"),
        [],
    )

    # The README's own file is never flagged, even if somehow passed in.
    f += check(
        "readme itself excluded",
        find_orphans(["README.md", "products.md"], readme, "README.md"),
        [],
    )

    # Explicit exempt set (used for root's pointer files) is excluded too.
    f += check(
        "exempt set excluded",
        find_orphans(["CLAUDE.md", "products.md"], readme, "README.md", exempt={"CLAUDE.md"}),
        [],
    )

    # Substring collision (found 2026-08-15). The check used to be a bare
    # `base not in readme_text`, so a shorter filename matched INSIDE a longer
    # one and was reported as indexed. In eq/ this masked four files at once —
    # service.md, cards.md, field.md, shell.md — each the half of a real
    # duplicate pair that this check exists to surface. It is the worst possible
    # blind spot for this particular repo: an unreconciled changelog twin is the
    # exact thing that let PR #727 be recorded as "open" a day after it merged.
    collision = "The service changelog is eq-service.md; the shell one is eq-shell.md."
    f += check(
        "shorter name must not match inside a longer one",
        find_orphans(["changelog/service.md", "changelog/shell.md"], collision, "README.md"),
        ["changelog/service.md", "changelog/shell.md"],
    )

    # ...while the longer names in that same text are still correctly indexed,
    # so the fix cannot be satisfied by a check that just flags everything.
    f += check(
        "longer names in the same text stay indexed",
        find_orphans(["changelog/eq-service.md", "changelog/eq-shell.md"], collision, "README.md"),
        [],
    )

    # A path separator is not a filename character, so a markdown link to a
    # nested path still indexes the basename. This is the looseness the check
    # is meant to keep — the boundary rule must not break it.
    linked = "Full detail in [the log](eq/changelog/field.md)."
    f += check(
        "link path still indexes the basename",
        find_orphans(["changelog/field.md"], linked, "README.md"),
        [],
    )

    # Real regression case: system/README.md's Files table listed 6 of 17 files.
    real_readme = "Files: architecture.md, infrastructure.md, lessons.md, md-style.md."
    real_files = ["architecture.md", "infrastructure.md", "lessons.md", "md-style.md", "TODAY.md", "worktree-registry.md"]
    f += check(
        "system/README.md 2026-07-19 regression",
        find_orphans(real_files, real_readme, "README.md"),
        ["TODAY.md", "worktree-registry.md"],
    )

    # discover_md_files gained an `extensions` arg so the machinery tiers
    # (hooks/, scripts/, .github/*) can be indexed too. Default must stay .md,
    # or every prose tier silently starts scanning the wrong thing.
    with tempfile.TemporaryDirectory() as tmp:
        for name in ("a.md", "b.py", "c.yml", "d.json"):
            open(os.path.join(tmp, name), "w").close()

        f += check("default extensions is .md only", discover_md_files(tmp, False), ["a.md"])
        f += check(
            "explicit extensions are honoured",
            discover_md_files(tmp, False, (".py", ".yml")),
            ["b.py", "c.yml"],
        )
        # Overlapping globs must not double-count a file.
        f += check(
            "no duplicates when extensions overlap",
            discover_md_files(tmp, False, (".md", ".md")),
            ["a.md"],
        )

    print()
    if f:
        print(f"{f} test(s) FAILED")
    else:
        print("all tests passed")
    sys.exit(1 if f else 0)


if __name__ == "__main__":
    main()
