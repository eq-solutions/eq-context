#!/usr/bin/env python3
"""Unit tests for the session-start budget gate.

The gate's whole value is that it FAILS. A budget check that can only pass is
decoration -- and decoration is what let eq/pending.md reach 491 KB on the
mandated-read list while every nightly job stayed green.

So the cases below pin both directions, and the headline one reconstructs the
real pre-2026-08-15 chain (with the tier pending.md mandated) and asserts the
gate would have caught it.

Run:  python scripts/test_session_start_budget.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import session_start_budget as budget  # noqa: E402


def check(name, got, want):
    if got != want:
        print(f"FAIL {name}: got {got!r}, want {want!r}")
        return 1
    print(f"ok   {name}")
    return 0


def with_tree(files, always, tiers, total=None, per_file=None):
    """Run the gate against a synthetic tree. Returns its exit code."""
    saved = (budget.ROOT, budget.ALWAYS, budget.TIERS, budget.TOTAL_BUDGET, budget.PER_FILE_BUDGET)
    with tempfile.TemporaryDirectory() as tmp:
        for rel, size_bytes in files.items():
            path = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as fh:
                fh.write(b"x" * size_bytes)
        budget.ROOT = tmp
        budget.ALWAYS = always
        budget.TIERS = tiers
        if total is not None:
            budget.TOTAL_BUDGET = total
        if per_file is not None:
            budget.PER_FILE_BUDGET = per_file
        try:
            return budget.main()
        finally:
            (budget.ROOT, budget.ALWAYS, budget.TIERS,
             budget.TOTAL_BUDGET, budget.PER_FILE_BUDGET) = saved


def main():
    f = 0
    KB = 1024

    # A lean chain passes.
    f += check(
        "chain within budget -> pass",
        with_tree(
            {"CLAUDE.md": 20 * KB, "eq/README.md": 12 * KB},
            ["CLAUDE.md"], {"EQ": ["eq/README.md"]},
            total=140 * KB, per_file=40 * KB,
        ),
        0,
    )

    # THE case: the real chain as CLAUDE.md mandated it until 2026-08-15, with
    # eq/pending.md at its actual measured size. This must fail, or the gate
    # would not have prevented the thing it was written for.
    f += check(
        "pre-fix chain with pending.md mandated -> FAIL",
        with_tree(
            {
                "CLAUDE.md": 20 * KB, "suite-state.md": 26 * KB, "digest.md": 21 * KB,
                "system/TODAY.md": 7 * KB, "system/punch-list.md": 8 * KB,
                "eq/README.md": 12 * KB, "eq/pending.md": 491 * KB,
            },
            ["CLAUDE.md", "suite-state.md", "digest.md", "system/TODAY.md", "system/punch-list.md"],
            {"EQ": ["eq/README.md", "eq/pending.md"]},
            total=140 * KB, per_file=40 * KB,
        ),
        1,
    )

    # One file bloating past the per-file cap fails even when the total is fine
    # -- that is the early warning, before the whole chain is over.
    f += check(
        "single file over per-file cap -> FAIL",
        with_tree(
            {"CLAUDE.md": 60 * KB},
            ["CLAUDE.md"], {"EQ": []},
            total=500 * KB, per_file=40 * KB,
        ),
        1,
    )

    # A mandated read that does not exist is a bug, not a zero-byte saving.
    # CLAUDE.md pointed at eq/templates.md for months and it never existed.
    f += check(
        "mandated file missing -> FAIL",
        with_tree(
            {"CLAUDE.md": 10 * KB},
            ["CLAUDE.md", "system/gone.md"], {"EQ": []},
            total=140 * KB, per_file=40 * KB,
        ),
        1,
    )

    # The budget is measured against the heaviest tier, not an average no real
    # session pays.
    f += check(
        "worst-case tier is the one counted",
        with_tree(
            {"CLAUDE.md": 10 * KB, "eq/README.md": 5 * KB,
             "sks/README.md": 60 * KB, "sks/active.md": 60 * KB},
            ["CLAUDE.md"],
            {"EQ": ["eq/README.md"], "SKS": ["sks/README.md", "sks/active.md"]},
            total=100 * KB, per_file=200 * KB,
        ),
        1,
    )

    print()
    if f:
        print(f"{f} test(s) FAILED")
    else:
        print("all tests passed")
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
