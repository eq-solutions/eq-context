#!/usr/bin/env python3
"""Unit tests for the pure logic in link_check.py.

No filesystem beyond a throwaway tempdir per test.

Run:  python scripts/test_link_check.py
"""
import os
import sys
import tempfile

from link_check import check_file, find_md_files, internal_targets


def check(name, got, want):
    if got != want:
        print(f"FAIL {name}: got {got!r}, want {want!r}")
        return 1
    print(f"ok   {name}")
    return 0


def main():
    f = 0

    # --- internal_targets: what counts as an internal .md link -----------
    f += check(
        "a real internal link is captured",
        list(internal_targets("See [x](foo/bar.md) for detail.")),
        ["foo/bar.md"],
    )
    f += check(
        "external http(s) links are excluded",
        list(internal_targets("[ext](https://example.com/readme.md)")),
        [],
    )
    f += check("mailto links are excluded", list(internal_targets("[a](mailto:x@y.com)")), [])
    f += check(
        "non-.md targets are excluded (images, anchors-only, etc.)",
        list(internal_targets("![img](pic.png) [a](other.py) [b](#just-an-anchor)")),
        [],
    )
    f += check(
        "an anchor fragment is stripped before resolution",
        list(internal_targets("[x](foo/bar.md#section-two)")),
        ["foo/bar.md"],
    )
    f += check(
        "an empty target is skipped, not treated as './'",
        list(internal_targets("[x]()")),
        [],
    )
    f += check(
        "multiple links on one line are all captured",
        list(internal_targets("[a](x.md) and [b](y.md)")),
        ["x.md", "y.md"],
    )

    # --- check_file: resolution against a real directory layout -----------
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "eq", "changelog"))
        os.makedirs(os.path.join(tmp, "archive"))
        open(os.path.join(tmp, "eq", "changelog", "eq-intake.md"), "w").close()
        open(os.path.join(tmp, "archive", "old-plan.md"), "w").close()

        f += check(
            "a link that resolves is not broken",
            check_file("suite-state.md", "[x](eq/changelog/eq-intake.md)", tmp),
            [],
        )
        # THE real 2026-08-15 regression: suite-state.md's own link was
        # missing the 'eq/' path segment -- 'changelog/eq-intake.md' from
        # root does not resolve, even though the file exists one level down.
        f += check(
            "a link missing a path segment is broken",
            [t for t, _ in check_file("suite-state.md", "[x](changelog/eq-intake.md)", tmp)],
            ["changelog/eq-intake.md"],
        )
        # Relative resolution is FROM THE LINKING FILE'S OWN DIRECTORY, not
        # from repo root -- a file inside eq/ using '../archive/x.md' must
        # resolve against eq/'s parent, not against tmp/ directly.
        f += check(
            "relative paths resolve from the linking file's directory",
            check_file("eq/pending.md", "[x](../archive/old-plan.md)", tmp),
            [],
        )
        f += check(
            "the same relative path from repo root does NOT resolve (proves the fix isn't a coincidence)",
            [t for t, _ in check_file("pending.md", "[x](../archive/old-plan.md)", tmp)],
            ["../archive/old-plan.md"],
        )
        # A file with several links: only the genuinely broken ones surface.
        multi = check_file(
            "sessions/2026-05-20-part-c.md",
            "[a](../eq/changelog/eq-intake.md) [b](../ghost.md) [c](../archive/old-plan.md)",
            tmp,
        )
        f += check("mixed good/bad links -> only the bad ones reported", len(multi), 1)
        f += check("...names the actually-broken one", multi[0][0], "../ghost.md")

    # --- find_md_files: walks and normalises separators, skips .git ------
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, ".git", "hooks"))
        os.makedirs(os.path.join(tmp, "eq"))
        open(os.path.join(tmp, "a.md"), "w").close()
        open(os.path.join(tmp, "eq", "b.md"), "w").close()
        open(os.path.join(tmp, ".git", "hooks", "c.md"), "w").close()
        open(os.path.join(tmp, "not-markdown.txt"), "w").close()

        found = find_md_files(tmp)
        f += check("finds files at root and nested", found, ["a.md", "eq/b.md"])
        f += check(".git contents are never walked", any(".git" in p for p in found), False)

    print()
    if f:
        print(f"{f} test(s) FAILED")
    else:
        print("all tests passed")
    sys.exit(1 if f else 0)


if __name__ == "__main__":
    main()
