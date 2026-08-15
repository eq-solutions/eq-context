#!/usr/bin/env python3
"""Unit tests for the prune ratchet's classifiers.

Run:  python scripts/test_prune_ratchet.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prune_ratchet as pr  # noqa: E402


def check(name, got, want):
    if got != want:
        print(f"FAIL {name}: got {got!r}, want {want!r}")
        return 1
    print(f"ok   {name}")
    return 0


def residue_of(body):
    saved = pr.ROOT
    with tempfile.TemporaryDirectory() as tmp:
        pr.ROOT = tmp
        with open(os.path.join(tmp, "p.md"), "w", encoding="utf-8") as fh:
            fh.write(body)
        try:
            return pr.count_residue("p.md")
        finally:
            pr.ROOT = saved


def main():
    f = 0

    # The shape that made pending.md unreadable: follow-up notes stapled to a
    # section whose own heading says the work is finished.
    f += check(
        "open item under a done heading counts",
        residue_of("## eq-shell: thing — shipped, live (2026-08-15)\n- [ ] follow-up\n"),
        1,
    )

    # An open item under a genuinely open heading is real work, not residue.
    # If this ever counted, the ratchet would be measuring the backlog itself
    # and would fire forever.
    f += check(
        "open item under an open heading is NOT residue",
        residue_of("## eq-shell: rework the importer\n- [ ] do the thing\n"),
        0,
    )

    # Ticked items are already handled by rotate_pending.py; counting them here
    # would double-count the thing that already has a guard.
    f += check(
        "done items are not residue",
        residue_of("## thing — merged\n- [x] done\n"),
        0,
    )

    # Heading state must not leak past the next heading.
    f += check(
        "heading scope resets",
        residue_of(
            "## a — shipped\n- [ ] one\n\n## b — still open work\n- [ ] two\n- [ ] three\n"
        ),
        1,
    )

    f += check(
        "multiple residue under one done heading",
        residue_of("## a — closed, live\n- [ ] one\n- [ ] two\n- [x] three\n"),
        2,
    )

    # A missing file must read as "unknown", not as zero -- a silent zero would
    # let the whole check pass while measuring nothing, which is the same
    # class of bug as a guard that is wired but never runs.
    f += check("missing file -> None, not 0", pr.count_residue("does-not-exist.md"), None)

    print()
    print("all tests passed" if not f else f"{f} test(s) FAILED")
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
