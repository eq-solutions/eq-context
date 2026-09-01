#!/usr/bin/env python3
"""
Unit tests for pulse_promotion_guard.extract_pulse_rows / hand_edited_rows —
the F5 promotion-guard's pure logic: a PR may never assert its own value for
a Product Pulse row (system/failures.md F4), only the nightly bot may.

Run: python scripts/test_pulse_promotion_guard.py
"""
from pulse_promotion_guard import extract_pulse_rows, hand_edited_rows

passed = failed = 0


def check(name, got, expect):
    global passed, failed
    ok = got == expect
    print(("PASS" if ok else "FAIL") + f" {name}")
    if ok:
        passed += 1
    else:
        failed += 1
        print(f"     got {got!r}\n     expected {expect!r}")


PULSE_A = """## Product Pulse (as of 2026-09-01)
_7-day window._

| Signal | Value (7d) | Flip? |
|--------|-----------:|-------|
| Prestarts created | 12 | |
| Toolbox talks created | 0 | |

_No flips this run._
"""

PULSE_A_TAMPERED = """## Product Pulse (as of 2026-09-01)
_7-day window._

| Signal | Value (7d) | Flip? |
|--------|-----------:|-------|
| Prestarts created | 9999 | |
| Toolbox talks created | 0 | |

_No flips this run._
"""

PULSE_A_NEW_ROW = """## Product Pulse (as of 2026-09-01)
_7-day window._

| Signal | Value (7d) | Flip? |
|--------|-----------:|-------|
| Prestarts created | 12 | |
| Toolbox talks created | 0 | |
| Active users | 5 | |

_No flips this run._
"""

# ── extract_pulse_rows ──
check(
    "extracts every data row, skips header/separator",
    extract_pulse_rows(PULSE_A),
    {"Prestarts created": "12", "Toolbox talks created": "0"},
)
check("no section at all returns {}", extract_pulse_rows("# nothing here\n"), {})

# ── hand_edited_rows ──
check("identical before/after: nothing flagged", hand_edited_rows(PULSE_A, PULSE_A), [])
check(
    "a changed value IS flagged (this is the exact case the guard exists for)",
    hand_edited_rows(PULSE_A, PULSE_A_TAMPERED),
    ["Prestarts created"],
)
check(
    "a brand-new row not present at base IS flagged — a PR can't assert a value the bot never wrote",
    hand_edited_rows(PULSE_A, PULSE_A_NEW_ROW),
    ["Active users"],
)
check(
    "no prior section at all (base predates the feature): every row in after is new, all flagged",
    hand_edited_rows("", PULSE_A),
    ["Prestarts created", "Toolbox talks created"],
)
check(
    "a row REMOVED from after is not itself flagged (only value-cell mismatches on rows present in after are)",
    hand_edited_rows(PULSE_A_NEW_ROW, PULSE_A),
    [],
)

print(f"\n{passed} passed, {failed} failed")
if failed:
    raise SystemExit(1)
