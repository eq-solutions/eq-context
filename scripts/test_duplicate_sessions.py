#!/usr/bin/env python3
"""Unit tests for the pure logic in duplicate_sessions.py.

Run:  python scripts/test_duplicate_sessions.py
"""
import sys

from duplicate_sessions import find_duplicates


def check(name, got, want):
    if got != want:
        print(f"FAIL {name}: got {got!r}, want {want!r}")
        return 1
    print(f"ok   {name}")
    return 0


def main():
    f = 0

    f += check(
        "no files -> no duplicates",
        find_duplicates([]),
        [],
    )
    f += check(
        "distinct content -> no duplicates",
        find_duplicates([("a.md", b"day one"), ("b.md", b"day two")]),
        [],
    )
    f += check(
        "identical content under two paths -> one duplicate pair",
        find_duplicates([("2026-08-14.md", b"same text"), ("2026-08-15.md", b"same text")]),
        [("2026-08-14.md", "2026-08-15.md")],
    )
    # The first-seen path is reported as "original", later ones as the dupe --
    # order in the input list decides this, which is why main() sorts by
    # filename before calling in, so results don't depend on os.listdir order.
    f += check(
        "input order decides which path is 'first'",
        find_duplicates([("2026-08-15.md", b"same text"), ("2026-08-14.md", b"same text")]),
        [("2026-08-15.md", "2026-08-14.md")],
    )
    # Three-way duplicate: the second and third both match the first, not
    # each other -- two pairs, both anchored on the earliest file.
    f += check(
        "three-way duplicate reports two pairs, both against the first",
        find_duplicates([("a.md", b"x"), ("b.md", b"x"), ("c.md", b"x")]),
        [("a.md", "b.md"), ("a.md", "c.md")],
    )
    # Empty files are still content -- two blank session stubs are still a
    # real accidental-duplicate signal, not a special case to exempt.
    f += check(
        "two empty files still count as duplicates",
        find_duplicates([("a.md", b""), ("b.md", b"")]),
        [("a.md", "b.md")],
    )
    # One-byte difference (a trailing newline, a typo) must NOT match --
    # this is a content check, not a fuzzy/near-duplicate check.
    f += check(
        "near-identical but not exact content is not flagged",
        find_duplicates([("a.md", b"hello\n"), ("b.md", b"hello")]),
        [],
    )
    # Filename pattern is irrelevant here by design -- rule 17.4 in
    # md-health.yml already owns filename shape; this file only ever looks
    # at bytes, so a plausible AND a garbage filename with the same content
    # both get caught.
    f += check(
        "filename shape is irrelevant -- content is the only signal",
        find_duplicates([("2026-08-14.md", b"same"), ("not-a-real-session-name.md", b"same")]),
        [("2026-08-14.md", "not-a-real-session-name.md")],
    )

    print()
    if f:
        print(f"{f} test(s) FAILED")
    else:
        print("all tests passed")
    sys.exit(1 if f else 0)


if __name__ == "__main__":
    main()
