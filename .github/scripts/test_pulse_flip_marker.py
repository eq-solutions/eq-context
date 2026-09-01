#!/usr/bin/env python3
"""
Unit tests for refresh_suite_state.pulse_flip_marker / render_pulse_rows —
the pure logic behind F4's Product Pulse zero<->nonzero flip detection
(system/failures.md F4, system/substrate-plan-v2.md P3).

Locks in the one rule this whole section exists to enforce: a flip is a
zero<->nonzero *crossing*, never a raw threshold, and "no prior data" (None)
must never itself read as a flip — the first-ever run of this section, or a
brand-new signal row, must not falsely alarm on its own baseline.

Run: python .github/scripts/test_pulse_flip_marker.py
"""
import os

# refresh_suite_state.py reads SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY /
# GH_TOKEN as bare os.environ[...] at import time — deliberately, so the real
# workflow fails loud on a missing secret instead of silently defaulting.
# Stubbed here only so this test can import the module's pure functions
# without touching that production behaviour.
os.environ.setdefault("SUPABASE_URL", "http://test.invalid")
os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "test")
os.environ.setdefault("GH_TOKEN", "test")

from refresh_suite_state import pulse_flip_marker, render_pulse_rows, parse_content_range_count

passed = failed = 0


def check(name, got, expect):
    global passed, failed
    ok = got == expect
    print(("PASS" if ok else "FAIL") + f" {name}")
    if ok:
        passed += 1
    else:
        failed += 1
        print(f"     got {got!r} expected {expect!r}")


# ── pulse_flip_marker ──
check("zero to nonzero is a flip", pulse_flip_marker(0, 5), "⚠ FLIPPED")
check("nonzero to zero is a flip", pulse_flip_marker(5, 0), "⚠ FLIPPED")
check("nonzero to different nonzero is NOT a flip (transitions, not thresholds)",
      pulse_flip_marker(5, 40), "")
check("zero to zero is not a flip", pulse_flip_marker(0, 0), "")
check("no prior row (None) is never a flip", pulse_flip_marker(None, 5), "")
check("no current value (None) is never a flip", pulse_flip_marker(3, None), "")
check("both None is not a flip", pulse_flip_marker(None, None), "")

# ── render_pulse_rows ──
spec = [("a", "Signal A"), ("b", "Signal B")]

check(
    "first-ever run: no prior values, nothing flips",
    render_pulse_rows(spec, {}, {"a": 3, "b": 0}),
    [("a", "Signal A", 3, ""), ("b", "Signal B", 0, "")],
)

check(
    "one signal flips, the other doesn't",
    render_pulse_rows(spec, {"a": 0, "b": 5}, {"a": 2, "b": 5}),
    [("a", "Signal A", 2, "⚠ FLIPPED"), ("b", "Signal B", 5, "")],
)

check(
    "a signal with no key at all in prev_pulse (not just None) is still treated as no-prior-data",
    render_pulse_rows(spec, {"a": 1}, {"a": 1, "b": 2}),
    [("a", "Signal A", 1, ""), ("b", "Signal B", 2, "")],
)

# ── parse_content_range_count ──
# Found 2026-09-01, first live run after this section shipped: the
# select=count() aggregate this used to send got PGRST123 "Use of aggregate
# functions is not allowed" -- disabled at the PostgREST config level on this
# project, not a syntax mistake. Replaced with the header-based count
# PostgREST has always supported, unrelated to that setting.
check("a normal ranged response", parse_content_range_count("0-24/42"), 42)
check("an empty result set", parse_content_range_count("*/0"), 0)
check("a single-row response", parse_content_range_count("0-0/1"), 1)

print(f"\n{passed} passed, {failed} failed")
if failed:
    raise SystemExit(1)
