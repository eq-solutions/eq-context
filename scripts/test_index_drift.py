#!/usr/bin/env python3
"""Unit tests for the pure classifier in index_drift.py.

No filesystem, no network — find_orphans() takes plain strings/lists.

Run:  python scripts/test_index_drift.py
"""
import sys

from index_drift import find_orphans


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

    # Real regression case: system/README.md's Files table listed 6 of 17 files.
    real_readme = "Files: architecture.md, infrastructure.md, lessons.md, md-style.md."
    real_files = ["architecture.md", "infrastructure.md", "lessons.md", "md-style.md", "TODAY.md", "worktree-registry.md"]
    f += check(
        "system/README.md 2026-07-19 regression",
        find_orphans(real_files, real_readme, "README.md"),
        ["TODAY.md", "worktree-registry.md"],
    )

    print()
    if f:
        print(f"{f} test(s) FAILED")
    else:
        print("all tests passed")
    sys.exit(1 if f else 0)


if __name__ == "__main__":
    main()
