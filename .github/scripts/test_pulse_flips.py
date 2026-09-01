#!/usr/bin/env python3
"""
Unit tests for refresh_digest.pulse_flips() — reads suite-state.md's Product
Pulse table (written by refresh_suite_state.py, F4) and returns the row
labels that flipped zero<->nonzero since the last run, for surfacing into
digest.md's Needs You section.

Run: python .github/scripts/test_pulse_flips.py
"""
import os
import tempfile

from refresh_digest import pulse_flips

passed = failed = 0


def check(name, content, expect):
    global passed, failed
    fd, path = tempfile.mkstemp(suffix=".md")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        got = pulse_flips(path)
    finally:
        os.remove(path)
    ok = got == expect
    print(("PASS" if ok else "FAIL") + f" {name}")
    if ok:
        passed += 1
    else:
        failed += 1
        print(f"     got {got!r} expected {expect!r}")


SECTION_NO_FLIPS = """## Product Pulse (as of 2026-09-01)
_7-day window. Transition-detection, not thresholds._

| Signal | Value (7d) | Flip? |
|--------|-----------:|-------|
| Prestarts created | 12 |  |
| Toolbox talks created | 0 |  |

_No flips this run._
"""

SECTION_ONE_FLIP = """## Product Pulse (as of 2026-09-01)
_7-day window. Transition-detection, not thresholds._

| Signal | Value (7d) | Flip? |
|--------|-----------:|-------|
| Prestarts created | 0 | ⚠ FLIPPED |
| Toolbox talks created | 3 |  |

⚠️ **At least one signal flipped.**
"""

check("no Product Pulse section at all returns empty", "# Just some other file\n", [])
check("no flips this run returns empty", SECTION_NO_FLIPS, [])
check("one flipped row is returned by its label", SECTION_ONE_FLIP, ["Prestarts created"])

# Missing-file case exercised directly (no temp file created at all).
got = pulse_flips("/definitely/does/not/exist.md")
ok = got == []
print(("PASS" if ok else "FAIL") + " missing file returns empty, not an error")
if ok:
    passed += 1
else:
    failed += 1
    print(f"     got {got!r} expected []")

print(f"\n{passed} passed, {failed} failed")
if failed:
    raise SystemExit(1)
