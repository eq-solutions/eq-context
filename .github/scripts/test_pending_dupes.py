#!/usr/bin/env python3
"""
Unit tests for refresh_digest.find_possible_duplicate_pending() — the
"possible duplicate pending items" digest section.

Built 2026-08-17 after finding two real duplicate pairs by hand while
reviewing the eq/pending.md split ("Send Huon the email" logged twice,
"gitleaks pre-commit hook" logged twice). This locks the similarity
threshold against those two real positives plus a set of items that share
words but are genuinely different work, so a future tuning pass can't
silently make the section noisy (too many false positives) or useless
(too few true positives).

Run: python .github/scripts/test_pending_dupes.py
"""
from refresh_digest import find_possible_duplicate_pending, _normalize_for_dedupe

passed = failed = 0


def check(name, items, expect_pairs):
    """expect_pairs: set of frozenset({text1, text2}) that MUST appear
    somewhere in the result, matched on the raw text regardless of which
    side of the pair it landed on or its score."""
    global passed, failed
    got = find_possible_duplicate_pending(items)
    got_pairs = {frozenset({t1, t2}) for _, t1, _, t2, _ in got}
    ok = expect_pairs.issubset(got_pairs)
    print(("PASS" if ok else "FAIL") + f" {name}")
    if ok:
        passed += 1
    else:
        failed += 1
        print(f"     expected pairs (subset): {expect_pairs}")
        print(f"     got pairs: {got_pairs}")


def check_no_match(name, items):
    global passed, failed
    got = find_possible_duplicate_pending(items)
    ok = len(got) == 0
    print(("PASS" if ok else "FAIL") + f" {name}")
    if ok:
        passed += 1
    else:
        failed += 1
        print(f"     expected no matches, got {got}")


# Real duplicate pairs found by hand 2026-08-17 — the actual bug this exists to catch.
check(
    "Send Huon the email — logged twice, different wording",
    items=[
        ("eq-shell", "- [ ] Send Huon the email about the licence renewal deadline"),
        ("eq-shell", "- [ ] Send Huon an email re: licence renewal deadline"),
        ("eq-field", "- [ ] Add an index on schedule_entries.tenant_id"),
    ],
    expect_pairs={
        frozenset({
            "- [ ] Send Huon the email about the licence renewal deadline",
            "- [ ] Send Huon an email re: licence renewal deadline",
        })
    },
)

check(
    "gitleaks pre-commit hook — logged twice under different repos",
    items=[
        ("eq-context", "- [ ] Add gitleaks pre-commit hook to catch secrets before they're committed"),
        ("cross-repo", "- [ ] Add a gitleaks pre-commit hook to catch secrets before commit"),
    ],
    expect_pairs={
        frozenset({
            "- [ ] Add gitleaks pre-commit hook to catch secrets before they're committed",
            "- [ ] Add a gitleaks pre-commit hook to catch secrets before commit",
        })
    },
)

# Genuinely different items that share words — must NOT match, or the
# section becomes noise nobody reads.
check_no_match(
    "same repo prefix, unrelated work",
    items=[
        ("eq-shell", "- [ ] Fix the Staff table filter for Type column"),
        ("eq-shell", "- [ ] Fix the Contacts table sort order on Name column"),
    ],
)

check_no_match(
    "both mention Royce but different asks",
    items=[
        ("eq-field", "- [ ] Royce to confirm the deploy went out clean"),
        ("eq-shell", "- [ ] Royce to decide whether to widen the pilot cohort"),
    ],
)

check_no_match(
    "short generic bullets below min_len are never compared",
    items=[
        ("eq-shell", "- [ ] Fix it"),
        ("eq-field", "- [ ] Fix it too"),
    ],
)

check_no_match(
    "empty input",
    items=[],
)


def check_normalize(name, text, expect):
    global passed, failed
    got = _normalize_for_dedupe(text)
    ok = got == expect
    print(("PASS" if ok else "FAIL") + f" {name}")
    if ok:
        passed += 1
    else:
        failed += 1
        print(f"     got {got!r} expected {expect!r}")


check_normalize(
    "strips markdown link, bold, code, checkbox punctuation",
    "- [ ] **Fixed** in [eq-shell PR #900](https://github.com/x/y/pull/900) via `cn()`",
    "fixed in eq shell pr 900 via cn",
)

print(f"\n{passed} passed, {failed} failed")
if failed:
    raise SystemExit(1)
