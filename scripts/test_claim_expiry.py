#!/usr/bin/env python3
"""
Unit tests for claim_expiry.check — the F3 guard.

Cross-platform, no network, no fixtures on disk. Builds synthetic TODAY.md text
and asserts the validator's verdict. Run: python scripts/test_claim_expiry.py
"""
import datetime
import sys

import claim_expiry as ce

TODAY = datetime.date(2026, 7, 12)
passed = failed = 0


def today_md(goals_yaml):
    """Wrap a goals YAML body in a minimal but structurally faithful TODAY.md."""
    return (
        "---\ntitle: TODAY\nstatus: live\n---\n\n"
        "## GOALS — `type: goal` · **status: UNSET**\n\n"
        "```yaml\n" + goals_yaml + "\n```\n\n"
        "---\n\n## FACTS\n\nsome facts here\n"
    )


def expect(name, text, *, fatal, n_violations):
    global passed, failed
    got_fatal, msgs = ce.check(text, TODAY)
    ok = (got_fatal == fatal) and (len(msgs) == n_violations)
    print("  {:<48}{}".format(
        name, "PASS" if ok else f"*** FAIL *** (fatal={got_fatal}, msgs={len(msgs)})"))
    passed += ok
    failed += (not ok)


VALID = (
    "claims:\n"
    "  - type: goal\n"
    "    owner: royce\n"
    "    asserted_on: 2026-07-12\n"
    "    expires_on: 2026-09-01\n"
    "    verify: human\n"
    "    text: Ship EQ Ops MVP\n"
)

# empty section — the honest default; must pass
expect("empty claims (UNSET) passes", today_md("claims: []"), fatal=False, n_violations=0)

# the current real file uses claims: [] with comments — must pass
expect("claims: [] with comments passes",
       today_md("claims: []\n# royce to define\n#   type: goal"),
       fatal=False, n_violations=0)

# a well-formed future goal passes
expect("valid future goal passes", today_md(VALID), fatal=False, n_violations=0)

# missing expires_on -> one violation
expect("goal missing expires_on fails",
       today_md(VALID.replace("    expires_on: 2026-09-01\n", "")),
       fatal=False, n_violations=1)

# expired goal -> one violation
expect("expired goal fails",
       today_md(VALID.replace("2026-09-01", "2026-06-01")),
       fatal=False, n_violations=1)

# missing owner -> one violation
expect("goal missing owner fails",
       today_md(VALID.replace("    owner: royce\n", "")),
       fatal=False, n_violations=1)

# non-ISO expires_on -> one violation
expect("non-ISO expires_on fails",
       today_md(VALID.replace("2026-09-01", "next quarter")),
       fatal=False, n_violations=1)

# two problems (missing verify + expired) -> two violations
expect("two problems -> two violations",
       today_md(VALID.replace("    verify: human\n", "").replace("2026-09-01", "2026-01-01")),
       fatal=False, n_violations=2)

# structure gone (no GOALS section) -> fatal (exit 2), never silent
expect("no GOALS section is fatal",
       "---\ntitle: x\n---\n\n## FACTS\n\nno goals here\n",
       fatal=True, n_violations=1)

# claims not a list -> fatal
expect("claims not a list is fatal",
       today_md("claims: not-a-list"), fatal=True, n_violations=1)

print()
print("  {} passed, {} failed".format(passed, failed))
sys.exit(1 if failed else 0)
