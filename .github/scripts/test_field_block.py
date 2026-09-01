#!/usr/bin/env python3
"""
Unit tests for refresh_suite_state.render_field_block / splice_field_block —
the pure logic behind the Field Data Plane section of suite-state.md.

Locks in two things found and fixed 2026-09-01:
1. Every rendered line must be flush-left. The previous version indented
   continuation lines 4 spaces, which Markdown reads as an indented code
   block — the table silently rendered as unstyled code, not a table.
2. splice_field_block() must self-heal three shapes: heading already present
   (steady state), the exact heading-less shape live in suite-state.md since
   2026-08-16 (one-time repair), and neither present (cold start) — so a
   stripped heading can never again cause a silent, unlogged no-op refresh
   the way it did for three weeks.

Run: python .github/scripts/test_field_block.py
"""
import os

# refresh_suite_state.py reads SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY /
# GH_TOKEN as bare os.environ[...] at import time — stubbed here only so this
# test can import the module's pure functions without touching that.
os.environ.setdefault("SUPABASE_URL", "http://test.invalid")
os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "test")
os.environ.setdefault("GH_TOKEN", "test")

from refresh_suite_state import render_field_block, splice_field_block

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


FULL_COUNTS = {
    "people": 83, "sites": 53, "managers": 21,
    "schedule": 1310, "timesheets": 138,
    "prestarts": 35, "toolbox_talks": 1, "site_audits": 0,
}

# ── render_field_block ──

block = render_field_block(FULL_COUNTS, "2026-09-01")

check("heading carries the as-of date", block.startswith("## Field Data Plane — SKS tenant (as of 2026-09-01)\n"), True)
check(
    "every line is flush-left (the exact bug: 4-space indent reads as a Markdown code block)",
    [line for line in block.split("\n") if line.startswith(" ") or line.startswith("\t")],
    [],
)
check("thousands separator on a real row", "| Operational | app_data.field_schedule | 1,310 | ✓ 1,310 |" in block, True)
check("empty operational table reads 'empty', not 'no data yet'", "| Safety | public.site_audits | 0 | ⚠ empty" not in block, True)
check("zero non-operational (Safety) table reads 'no data yet'", "public.site_audits | 0 | ⚠ no data yet |" in block, True)
check("missing key defaults to 0 via fc.get(...)", "app_data.field_people | 83 |" in render_field_block({"people": 83}, "2026-09-01"), True)
check("a genuinely missing (None) count reads 'missing'", "✗ missing" in render_field_block({"people": None}, "2026-09-01"), True)
check("ends with the auto-refreshed note, no trailing newline", block.endswith("✗ = table missing_"), True)

# ── splice_field_block ──

STEADY_STATE = """## System Health (as of 2026-09-01)
stuff here

---

## Field Data Plane — SKS tenant (as of 2026-08-31)
| Layer | View / Table | Rows | Status |
|-------|-------------|------|--------|
| Directory | app_data.field_people | 80 | ✓ 80 |
_Auto-refreshed nightly. ✓ = has data · ⚠ = empty (no data yet) · ✗ = table missing_

---

## Architecture: What Owns What
stuff after
"""

LEGACY_SHAPE = """## System Health (as of 2026-09-01)
**Migrations:** eq-service has 245 (latest: 0239) applied

---

| Layer | View / Table | Rows | Status |
|-------|-------------|------|--------|
| Directory | app_data.field_people | 66 | ✓ 66 |
_Auto-refreshed nightly. ✓ = has data · ⚠ = empty (no data yet) · ✗ = table missing_

---

## Architecture: What Owns What
stuff after
"""

COLD_START = """## System Health (as of 2026-09-01)
stuff here

---

## Architecture: What Owns What
stuff after
"""

NEW_BLOCK = "## Field Data Plane — SKS tenant (as of 2026-09-01)\n| new | table | here | ✓ |\n_Auto-refreshed nightly. ✓ = has data · ⚠ = empty (no data yet) · ✗ = table missing_"

steady_result = splice_field_block(STEADY_STATE, NEW_BLOCK)
check("steady state: old heading/date is gone", "2026-08-31" in steady_result, False)
check("steady state: new block is in", NEW_BLOCK in steady_result, True)
check("steady state: System Health above it is untouched", "## System Health (as of 2026-09-01)\nstuff here" in steady_result, True)
check("steady state: Architecture below it is untouched", steady_result.endswith("## Architecture: What Owns What\nstuff after\n"), True)
check("steady state: only one Field Data Plane heading survives", steady_result.count("## Field Data Plane"), 1)

legacy_result = splice_field_block(LEGACY_SHAPE, NEW_BLOCK)
check(
    "legacy shape (this repo's actual live state since 2026-08-16): heading-less table is repaired in place",
    NEW_BLOCK in legacy_result,
    True,
)
check("legacy shape: stale count (66) is gone", "66" in legacy_result, False)
check("legacy shape: System Health content above it survives untouched", "**Migrations:** eq-service has 245" in legacy_result, True)
check("legacy shape: exactly one heading after repair", legacy_result.count("## Field Data Plane"), 1)

cold_result = splice_field_block(COLD_START, NEW_BLOCK)
check("cold start: block gets inserted", NEW_BLOCK in cold_result, True)
check("cold start: inserted before Architecture, not after", cold_result.index(NEW_BLOCK) < cold_result.index("## Architecture"), True)

print(f"\n{passed} passed, {failed} failed")
if failed:
    raise SystemExit(1)
