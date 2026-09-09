#!/usr/bin/env python3
"""
Precision tests for F1's `signal` regex in system/failures.md, read out of
the live ledger the same way refresh_digest.failure_recurrence_signals()
does -- not a hardcoded copy -- so a future edit to the regex that weakens
precision fails this test instead of silently drifting (system/failures.md F1).

F1's regex went through two eras: an original three-alternative "shape"
match (raw.githubusercontent/serving-stale/CDN-cache near "stale") that had
no way to tell a genuine eq-context substrate-staleness incident from a
session merely citing the F1 lesson while verifying a push to a DIFFERENT
repo landed -- confirmed live 4 times (2026-08-30, 2026-09-07, 2026-09-09 x2)
against the same false-positive line in sessions/2026-08-23.md. Tightened
2026-09-09 to additionally require a substrate-specific anchor term on the
SAME line as the shape match, same precision-tightening shape F6/F7/F9/F10/
F12 already used for their own signal regexes.

7 of these fixtures are real text pulled verbatim from this substrate's own
session logs (the false positive, plus the 3 genuine historical incidents);
the other 3 are synthetic, called out as such, because the CDN-cache and
serving-stale/no-error alternatives have no real historical incident to
draw a fixture from.

Run: python .github/scripts/test_failure_recurrence_signals.py
"""
import re

import yaml

FAILURES_PATH = "../../system/failures.md"


def load_signal(failure_id, path=FAILURES_PATH):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"```yaml\n(.*?)\n```", content, re.S)
    data = yaml.safe_load(m.group(1))
    entry = next(fl for fl in data["failures"] if fl["id"] == failure_id)
    return entry["signal"]


passed = failed = 0


def check(name, pattern, text, expect_match):
    global passed, failed
    got = bool(pattern.search(text))
    ok = got == expect_match
    print(("PASS" if ok else "FAIL") + f"  {name}")
    if ok:
        passed += 1
    else:
        failed += 1
        print(f"     expected match={expect_match}, got {got}")


def main():
    pat = re.compile(load_signal("F1"), re.I)

    # --- must CATCH: real historical incidents, verbatim from session logs -
    check(
        "2026-07-11 original discovery (names system/lessons.md, 'substrate')",
        pat,
        "The `raw.githubusercontent.com/.../main/` alias served 8–12 day stale "
        "content with a 200 OK. A SHA-pinned fetch of the same commit returned the "
        "correct files. Full write-up: `system/lessons.md` → \"The Substrate Read "
        "Path Lied\".",
        True,
    )
    check(
        "2026-07-19 recurrence (names CLAUDE.md)",
        pat,
        "`COWORK-PROMPT.md` still told it to fetch `CLAUDE.md` via "
        "`raw.githubusercontent.com` — the exact CDN-cache mechanism that was just "
        "proven to serve this file 8+ days stale with a 200 OK and no error, and the "
        "reason the Chat prompt was changed earlier this same session.",
        True,
    )
    check(
        "2026-07-21 confirmed_in mention (cites F1 by id)",
        pat,
        "Verified against real data before shipping, not just synthetically: caught "
        "a genuine unlogged recurrence of F1 (`raw.githubusercontent` serving stale "
        "content) in `sessions/2026-07-19.md`.",
        True,
    )
    # Synthetic -- the CDN-cache and serving-stale/no-error alternatives have no
    # real historical incident on record to draw a fixture from.
    check(
        "synthetic: CDN-cache alternative, substrate term present",
        pat,
        "eq-context's own CDN-cache in front of raw.githubusercontent.com was still "
        "serving a stale copy of digest.md hours after the fix landed.",
        True,
    )
    check(
        "synthetic: serving-stale/no-error alternative, substrate term present",
        pat,
        "hooks/session_start.py's SessionStart gate was serving stale suite-state.md "
        "with no error before the fetch-first fix.",
        True,
    )

    # --- must NOT catch: the real false positive + adversarial near-misses --
    check(
        "2026-08-23 real false positive (verifying a push to a DIFFERENT repo, "
        "no substrate term anywhere on the line) -- re-flagged live 4 times",
        pat,
        "`raw.githubusercontent.com` served stale content after pushes; the GitHub "
        "Contents API reflected them immediately. Use the API to verify a push "
        "landed, not raw.",
        False,
    )
    check(
        "synthetic: CDN-cache shape about an unrelated product, no substrate term",
        pat,
        "Netlify's edge CDN cache kept serving a stale build of the marketing site "
        "for about ten minutes after the deploy went live.",
        False,
    )
    check(
        "synthetic: serving-stale/200-ok shape about a different repo, no substrate term",
        pat,
        "eq-field's service worker was serving stale cached assets with a 200 OK "
        "until the cache name was bumped.",
        False,
    )
    check(
        "synthetic: bare word 'stale' near 'substrate', no shape match at all",
        pat,
        "The substrate felt a little stale today after a slow week, nothing "
        "regex-shaped about it though.",
        False,
    )
    check(
        "synthetic: shape + substrate term, but split across two lines "
        "(no DOTALL in the real compile -- must not bridge a line break)",
        pat,
        "raw.githubusercontent.com is the CDN in front of the repo.\n"
        "substrate content was stale for days after that.",
        False,
    )

    print(f"\n{passed} passed, {failed} failed")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
