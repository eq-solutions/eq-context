#!/usr/bin/env python3
"""
Unit tests for refresh_digest.ROYCE_QUEUE_RE and _count_queue_health — the
pure logic behind eq-context's "Waiting on you" / "Queue health" split.

Extended 2026-08-14 (eq-context PR #158): the original ROYCE_QUEUE_RE caught
only 7 of 50 real open items in eq/pending.md that describe needing a human
click-through/live-test, because those items use too many verb/tense
variations around "click-through"/"click-test" to enumerate as exact
suffixes. This test locks in the broadened pattern against real phrasings
pulled from the live file, plus a couple of near-miss cases that should NOT
match, so a future edit can't silently widen the pattern too far.

Run: python .github/scripts/test_pending_queue_health.py
"""
from refresh_digest import ROYCE_QUEUE_RE, _count_queue_health, _aging_section_items

passed = failed = 0


def check_re(name, text, expect_match):
    global passed, failed
    got = bool(ROYCE_QUEUE_RE.search(text))
    ok = got == expect_match
    print(("PASS" if ok else "FAIL") + f" {name}")
    if ok:
        passed += 1
    else:
        failed += 1
        print(f"     text: {text!r}\n     expected match={expect_match}, got {got}")


# Original patterns — must keep matching after the extension.
check_re("Royce to <verb>", "- [ ] Royce to confirm the deploy", True)
check_re("Royce's confirmation", "- [ ] Needs Royce's confirmation before merging", True)
check_re("needs Royce", "- [ ] This needs Royce to decide the pricing tier", True)
check_re("your call on", "- [ ] Your call on whether to widen the pilot", True)

# Real phrasings pulled from the live file (2026-08-14) that the original
# pattern MISSED — this is the actual bug being fixed.
check_re("not click-tested live", "- [ ] Not click-tested live — verified via CI only", True)
check_re("live click-test still not done",
         "- [ ] Live click-test still not done anywhere across this thread", True)
check_re("no live click-through", "- [ ] No live click-through was possible this session", True)
check_re("royce's own click-through", "- [ ] Royce's own click-through, still not done", True)
check_re("live phone click-through not done",
         "- [ ] Live phone click-through not done — open the More drawer", True)
check_re("manual click-through of PR", "- [ ] Manual click-through of PR #641 once deployed", True)
check_re("not confirmed working", "- [ ] Not yet confirmed working end-to-end", True)

# Should NOT match — real engineering backlog with no "waiting on Royce" signal.
check_re("plain engineering item", "- [ ] Add an index on service.assets.tenant_id", False)
check_re(
    "mentions Royce in passing, not asking him for anything",
    "- [ ] Follows the pattern Royce used in PR #900 for the retry logic",
    False,
)


def check_counts(name, lines, cutoff, expect):
    global passed, failed
    got = _count_queue_health(lines, cutoff)
    ok = got == expect
    print(("PASS" if ok else "FAIL") + f" {name}")
    if ok:
        passed += 1
    else:
        failed += 1
        print(f"     got {got} expected {expect}")


check_counts(
    "royce_open_count is a subset of open_count, not additive",
    lines=[
        "## 2026-08-14 (some section)\n",
        "- [ ] Royce to confirm the deploy\n",
        "- [ ] Add an index on service.assets.tenant_id\n",
        "- [x] Already done, doesn't count\n",
    ],
    cutoff="2026-06-01",
    expect=(4, 2, 1, 1, 0),  # total_lines, open, royce_open, done, aging
)

check_counts(
    "aging counts only sections whose header date is before cutoff",
    lines=[
        "## 2026-01-01 (old section)\n",
        "- [ ] Stale item nobody's touched\n",
        "## 2026-08-14 (fresh section)\n",
        "- [ ] Brand new item\n",
    ],
    cutoff="2026-06-01",
    expect=(4, 2, 0, 0, 1),
)

check_counts(
    "royce-queue item in an aging section counts toward both",
    lines=[
        "## 2026-01-01 (old section)\n",
        "- [ ] Royce to confirm this old thing\n",
    ],
    cutoff="2026-06-01",
    expect=(2, 1, 1, 0, 1),
)

check_counts("empty file", lines=[], cutoff="2026-06-01", expect=(0, 0, 0, 0, 0))


def check_aging(name, lines, cutoff, expect):
    global passed, failed
    got = _aging_section_items(lines, cutoff)
    ok = got == expect
    print(("PASS" if ok else "FAIL") + f" {name}")
    if ok:
        passed += 1
    else:
        failed += 1
        print(f"     got {got}\n     expected {expect}")


check_aging(
    "aging section with open items is returned",
    lines=[
        "## eq-shell: some old thing (2026-01-01)\n",
        "- [ ] Still not done\n",
        "- [x] This part is done\n",
    ],
    cutoff="2026-06-01",
    expect=[("eq-shell: some old thing (2026-01-01)", "2026-01-01", ["Still not done"])],
)

check_aging(
    "fresh section is excluded even with open items",
    lines=["## brand new (2026-08-14)\n", "- [ ] Not aging\n"],
    cutoff="2026-06-01",
    expect=[],
)

check_aging(
    "aging section with zero open items left is excluded — nothing to act on",
    lines=["## old, fully done (2026-01-01)\n", "- [x] Already done\n"],
    cutoff="2026-06-01",
    expect=[],
)

check_aging(
    "undated section is never aging, matches _count_queue_health",
    lines=["## Parked — revisit later\n", "- [ ] Deliberately parked\n"],
    cutoff="2026-06-01",
    expect=[],
)

check_aging(
    "in-progress items count as open in an aging section",
    lines=["## old (2026-01-01)\n", "- [~] Partially applied\n"],
    cutoff="2026-06-01",
    expect=[("old (2026-01-01)", "2026-01-01", ["Partially applied"])],
)

print(f"\n{passed} passed, {failed} failed")
if failed:
    raise SystemExit(1)
