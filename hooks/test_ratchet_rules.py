#!/usr/bin/env python3
"""Unit tests for the single promotion rule.

Run:  python hooks/test_ratchet_rules.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ratchet_rules import classify, parse_entry, scan  # noqa: E402


def check(name, got, want):
    if got != want:
        print(f"FAIL {name}: got {got!r}, want {want!r}")
        return 1
    print(f"ok   {name}")
    return 0


def main():
    f = 0

    # target_rung must not satisfy a search for rung. session_start.py used a
    # bare `rung:\s*(\d+)` and read the right value only because `rung:` happens
    # to be listed before `target_rung:` in every current entry -- reverse the
    # order and it compared a value against itself and never fired.
    reversed_order = "  title: x\n  recurrences: 2\n  target_rung: 4\n  rung: 1\n"
    f += check("target_rung does not masquerade as rung", parse_entry(reversed_order), (2, 1, 4))

    normal_order = "  title: x\n  recurrences: 2\n  rung: 1\n  target_rung: 4\n"
    f += check("normal field order", parse_entry(normal_order), (2, 1, 4))

    # Missing rung reads as 0: an entry that forgot to declare one is unguarded
    # until it says otherwise, which is the safe direction to be wrong in.
    f += check("missing fields default safe", parse_entry("  title: x\n"), (0, 0, 4))

    # At or above target is not due, however often it recurred.
    f += check("at target -> not due", classify(9, 4, 4), None)
    f += check("above target -> not due", classify(9, 4, 3), None)

    # Below target with repeat failures is the classic promotion.
    f += check("below target, recurred -> OVERDUE", classify(2, 1, 4), "OVERDUE")

    # Below target WITHOUT a second occurrence still owes a guard. The old rule
    # required recurrences >= 2, which is why F4 and F5 sat at rung 0 against a
    # declared target of 3 and could never be raised: the ledger said out loud
    # they needed a CI guard and the ratchet was structurally unable to say so.
    f += check("below target, not yet recurred -> DUE", classify(1, 0, 3), "DUE")
    f += check("rung 0 with target 3 -> DUE", classify(0, 0, 3), "DUE")

    # scan() end to end over two entries, one of each verdict.
    text = (
        "\n- id: F1\n  title: first\n  recurrences: 3\n  rung: 2\n  target_rung: 4\n"
        "\n- id: F2\n  title: second\n  recurrences: 1\n  rung: 0\n  target_rung: 3\n"
        "\n- id: F3\n  title: done\n  recurrences: 5\n  rung: 4\n  target_rung: 4\n"
    )
    f += check(
        "scan reports both verdicts and skips the satisfied one",
        [(r[0], r[5]) for r in scan(text)],
        [("F1", "OVERDUE"), ("F2", "DUE")],
    )

    print()
    print("all tests passed" if not f else f"{f} test(s) FAILED")
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
