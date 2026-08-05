#!/usr/bin/env python3
"""
Unit tests for refresh_digest._scan_run_conclusions — the pure counting logic
behind scheduled_workflow_health() (system/failures.md F11).

Only the pure half is tested; the I/O half (gh_get, workflow-file discovery)
is the same untested API boundary every other digest signal (ci_status,
sentry_top_issues, ...) already has — no network, no fixtures on disk.
Run: python .github/scripts/test_scheduled_workflow_health.py
"""
from refresh_digest import _scan_run_conclusions

passed = failed = 0


def check(name, conclusions, expect_fails, expect_success_idx):
    global passed, failed
    fails, idx = _scan_run_conclusions(conclusions)
    ok = fails == expect_fails and idx == expect_success_idx
    print(("PASS" if ok else "FAIL") + f" {name}")
    if ok:
        passed += 1
    else:
        failed += 1
        print(f"     got ({fails}, {idx}) expected ({expect_fails}, {expect_success_idx})")


# Most recent run first, as the GitHub API returns them.
check("all success", ["success", "success", "success"], 0, 0)
check("first run ever fails", ["failure"], 1, None)
check("one failure then success", ["failure", "success"], 1, 1)
check("F10-shaped: four in a row", ["failure", "failure", "failure", "failure", "success"], 4, 4)
check("in-progress runs skipped, not counted as failures", [None, "failure", "success"], 1, 2)
check("cancelled counts as a failure (not a clean success)", ["cancelled", "success"], 1, 1)
check("empty history", [], 0, None)
check("no success anywhere in the window", ["failure", "failure", "timed_out"], 3, None)

print(f"\n{passed} passed, {failed} failed")
if failed:
    raise SystemExit(1)
