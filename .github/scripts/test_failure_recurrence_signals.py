#!/usr/bin/env python3
"""
Precision tests for signal-regex tightening passes in system/failures.md,
read out of the live ledger the same way refresh_digest.failure_recurrence_
signals() does -- not a hardcoded copy -- so a future edit to a regex that
weakens precision fails this test instead of silently drifting.

F1's regex went through two eras: an original three-alternative "shape"
match (raw.githubusercontent/serving-stale/CDN-cache near "stale") that had
no way to tell a genuine eq-context substrate-staleness incident from a
session merely citing the F1 lesson while verifying a push to a DIFFERENT
repo landed -- confirmed live 4 times (2026-08-30, 2026-09-07, 2026-09-09 x2)
against the same false-positive line in sessions/2026-08-23.md. Tightened
2026-09-09 to additionally require a substrate-specific anchor term on the
SAME line as the shape match.

F10 hit the same class of gap the same day: its false positive is the HOOKS
"LATENT SHADOW" diagnostic firing exactly as designed (the effective
core.hooksPath value resolves correctly; the guard is only warning about a
dormant --worktree/--local disagreement), confirmed against
sessions/2026-08-26.md. Tightened by excluding that diagnostic's own
self-description on the same line, rather than requiring a positive anchor
-- F10's genuine incidents don't share one consistent anchor term the way
F1's do, but they never say "resolves correctly" / "working as intended".

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


def test_f1():
    pat = re.compile(load_signal("F1"), re.I)

    # --- must CATCH: real historical incidents, verbatim from session logs -
    check(
        "F1: 2026-07-11 original discovery (names system/lessons.md, 'substrate')",
        pat,
        "The `raw.githubusercontent.com/.../main/` alias served 8–12 day stale "
        "content with a 200 OK. A SHA-pinned fetch of the same commit returned the "
        "correct files. Full write-up: `system/lessons.md` → \"The Substrate Read "
        "Path Lied\".",
        True,
    )
    check(
        "F1: 2026-07-19 recurrence (names CLAUDE.md)",
        pat,
        "`COWORK-PROMPT.md` still told it to fetch `CLAUDE.md` via "
        "`raw.githubusercontent.com` — the exact CDN-cache mechanism that was just "
        "proven to serve this file 8+ days stale with a 200 OK and no error, and the "
        "reason the Chat prompt was changed earlier this same session.",
        True,
    )
    check(
        "F1: 2026-07-21 confirmed_in mention (cites F1 by id)",
        pat,
        "Verified against real data before shipping, not just synthetically: caught "
        "a genuine unlogged recurrence of F1 (`raw.githubusercontent` serving stale "
        "content) in `sessions/2026-07-19.md`.",
        True,
    )
    # Synthetic -- the CDN-cache and serving-stale/no-error alternatives have no
    # real historical incident on record to draw a fixture from.
    check(
        "F1: synthetic CDN-cache alternative, substrate term present",
        pat,
        "eq-context's own CDN-cache in front of raw.githubusercontent.com was still "
        "serving a stale copy of digest.md hours after the fix landed.",
        True,
    )
    check(
        "F1: synthetic serving-stale/no-error alternative, substrate term present",
        pat,
        "hooks/session_start.py's SessionStart gate was serving stale suite-state.md "
        "with no error before the fetch-first fix.",
        True,
    )

    # --- must NOT catch: the real false positive + adversarial near-misses --
    check(
        "F1: 2026-08-23 real false positive (verifying a push to a DIFFERENT repo, "
        "no substrate term anywhere on the line) -- re-flagged live 4 times",
        pat,
        "`raw.githubusercontent.com` served stale content after pushes; the GitHub "
        "Contents API reflected them immediately. Use the API to verify a push "
        "landed, not raw.",
        False,
    )
    check(
        "F1: synthetic CDN-cache shape about an unrelated product, no substrate term",
        pat,
        "Netlify's edge CDN cache kept serving a stale build of the marketing site "
        "for about ten minutes after the deploy went live.",
        False,
    )
    check(
        "F1: synthetic serving-stale/200-ok shape about a different repo, no substrate term",
        pat,
        "eq-field's service worker was serving stale cached assets with a 200 OK "
        "until the cache name was bumped.",
        False,
    )
    check(
        "F1: synthetic bare word 'stale' near 'substrate', no shape match at all",
        pat,
        "The substrate felt a little stale today after a slow week, nothing "
        "regex-shaped about it though.",
        False,
    )
    check(
        "F1: synthetic shape + substrate term, but split across two lines "
        "(no DOTALL in the real compile -- must not bridge a line break)",
        pat,
        "raw.githubusercontent.com is the CDN in front of the repo.\n"
        "substrate content was stale for days after that.",
        False,
    )


def test_f10():
    pat = re.compile(load_signal("F10"), re.I)

    # --- must CATCH: real historical incidents, verbatim from session logs -
    check(
        "F10: 2026-05-24 mechanism 1 (original discovery)",
        pat,
        "1. `system/lessons.md` — added `core.hooksPath` gotcha lesson (pre-commit "
        "silently skipping because hooksPath pointed at `hooks/` not `.githooks/`). "
        "Bumped `last_updated` to 2026-05-24.",
        True,
    )
    check(
        "F10: 2026-08-05-g mechanism 3 title",
        pat,
        "# Session 2026-08-05 (g) — core.hooksPath worktree-scope regression on F8: "
        "root-caused, drift-check proposed",
        True,
    )
    check(
        "F10: 2026-08-05-g mechanism 3 detail (verified wrong effective resolution)",
        pat,
        "Verified a `--worktree`-scope `core.hooksPath` override on the main "
        "checkout was shadowing the correct `--local` value of `.githooks`, "
        "resolving effectively to `.git/hooks` — already fixed before this session "
        "started.",
        True,
    )
    check(
        "F10: 2026-09-07 mechanism 5 (confirmed 5th recurrence)",
        pat,
        "**Possible fresh F10 recurrence, one day after it was marked closed.** "
        "This session's resume hook reported `core.hooksPath` resolving "
        "unexpectedly (\"*** WRONG ***... not .githooks\") on 2026-09-07.",
        True,
    )
    check(
        "F10: synthetic pre-commit silently-skipping shape, fresh wording",
        pat,
        "Noticed the governed pre-commit hook silently skip again on a second "
        "machine — core.hooksPath pointed at the wrong directory.",
        True,
    )

    # --- must NOT catch: the real false positive + its earlier twin ---------
    check(
        "F10: 2026-08-26 real false positive (LATENT SHADOW, guard firing as designed)",
        pat,
        "**HOOKS \"LATENT SHADOW\"** (core.hooksPath: `--worktree` vs `--local` "
        "disagreement on the shared checkout) — informational, print-only by "
        "design (this is F10's own guard working as intended), no action taken; "
        "this session never wrote through the shared checkout itself, only "
        "through isolated clones.",
        False,
    )
    check(
        "F10: 2026-08-05-z earlier instance of the same LATENT SHADOW shape",
        pat,
        "HOOKS now reports a **LATENT SHADOW**: effective `core.hooksPath` "
        "resolves correctly (`.githooks`) right now, but `--worktree` and "
        "`--local` scope disagree on this checkout — worktree silently wins. "
        "Gate flags this as \"the exact shape of F10's 2026-08-05 recurrence\" "
        "(the same core.hooksPath-drift failure class already proposed for rung "
        "promotion earlier today).",
        False,
    )
    check(
        "F10: synthetic guard diagnostic fires, explicitly resolves correctly",
        pat,
        "Session-start's HOOKS check printed a warning, but core.hooksPath "
        "resolves correctly to .githooks right now -- the --worktree/--local "
        "disagreement is dormant, not live.",
        False,
    )
    check(
        "F10: synthetic guard described as working as designed, no live problem",
        pat,
        "core.hooksPath drift-detection is working as designed here -- the "
        "shadow it flagged is informational only, nothing to fix.",
        False,
    )


def main():
    test_f1()
    test_f10()
    print(f"\n{passed} passed, {failed} failed")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
