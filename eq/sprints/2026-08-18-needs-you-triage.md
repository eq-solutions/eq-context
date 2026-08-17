---
title: Sprint scoping — the 4 "Needs you" items from 2026-08-17 digest
owner: Royce Milmlow
last_updated: 2026-08-18
scope: Triage of the 4 items digest.md flagged as "Needs you" going into 2026-08-18 — what each one actually is, what's genuinely buildable vs. genuinely Royce's call, and one concrete fix proposal.
read_priority: high
status: live
---

# Sprint scoping — the 4 "Needs you" items

Triggered by Royce asking to "sprint the 4 needing me and explain them" off the
2026-08-17 session-close card. Live-verified, not just restated from the digest.

---

## 1. SEC-1 — public key reads `people`, `timesheets`, `leave_requests`, `audit_log` (P0)

**Not a build task. Nothing to sprint here — it's a standing decision, reaffirmed twice.**

This is SKS NSW Labour's live Supabase project (`nspbmirochztcjijmcrx`). Royce
decided 2026-06-05 and reaffirmed 2026-07-20, in person, after a session got as
far as staging an RLS-hardening migration: **no engineering changes land on
sks-nsw-labour, full stop, until Field replaces it.** The fix is
decommission-at-cutover, not interim hardening. Full detail:
`ops/security-register.md` SEC-1.

**Why it still shows red:** it's a real, live, unfixed P0 by definition — that's
correct, not a bug in the tracking. It stays red until SKS NSW Labour is
retired. There's no "needs you" action here beyond the standing instruction
already on record: keep it off-limits.

---

## 2. F14 — "a hand-written claim ages into a lie, and nothing notices" (possible recurrence, `sessions/2026-08-16.md`)

**Checked live just now. The specific claim that triggered this flag is not
present in the file it was reported against.**

`sessions/2026-08-16.md` logged two stale-claim incidents that day:

1. A worktree briefly believed a live security gap existed — caught and
   corrected **within the same session**, before it reached Royce. This is
   the opposite of F14 (vigilance working), not an instance of it.
2. A claim that `system/punch-list.md` item #4's "Active" section was stale
   (showing "unbuilt-with-a-caveat" when PR #235 had already shipped) — flagged
   in the session log and an OneDrive register, but the session explicitly did
   **not** edit `punch-list.md` itself ("that file is Royce's to edit").

I read `system/punch-list.md` directly just now. Item #4 (Cards info density)
currently reads clean: "Needs scoping first... Scoped 2026-08-11, not built" —
no caveat language, no PR #235 reference. Either you fixed it by hand since
the 16th, or the original note was really about the OneDrive register (a
different, non-substrate file this repo can't see) and just cited the wrong
filename.

**Recommendation: don't bump `failures.md`'s F14 recurrence count.** Neither
candidate holds up as "aged into a lie, nothing noticed" — one was self-caught,
the other isn't reproducible in the named file today. Flagging this finding
back into the record rather than silently closing it, since F14's own pattern
is that only a human check catches this class of drift — this is that check.

---

## 3. eq-shell Sentry: "Degraded UI Performance" (EQ-SHELL-1Q, `/login`)

**Low priority — one data point, watch rather than build.**

Sentry's AI performance detector flagged the main thread blocked ~752ms across
two long animation frames during a single `/login` page load, 2026-08-17
11:33 UTC. 1 occurrence, 0 users impacted, first-seen == last-seen (hasn't
repeated in the ~24h since). Not enough signal yet to chase — could be a cold
cache, a slow device, or a one-off GC pause. Worth a second look only if it
recurs.

---

## 4. eq-shell Sentry: "auth-stall: session-spinner-timeout" (EQ-SHELL-V, `/sks/staff`) — real bug, root cause found

**This one is genuinely buildable. Root cause confirmed via git archaeology,
proposal below — holding for your go given it touches the Shell auth-loading
path on core.eq.solutions (auto-deploys on merge).**

7 occurrences since 2026-07-14, status **regressed** (was quiet, came back),
last seen 2026-08-17. Traced to a straightforward timing-constant mismatch,
not a re-break of the original bug:

- `BlockingSpinner` (`eq-shell/src/App.tsx:108-153`) arms a 20-second watchdog
  (`WATCHDOG_MS = 20_000`, set 2026-07-13, never changed) while
  `RequireSession` waits on the shell auth check. If the watchdog fires first,
  the user sees an "This is taking longer than usual… Reload to try again"
  card instead of just... waiting a bit longer for a legitimate response.
- `e4c800bc` (2026-07-14) introduced this watchdog and fixed the *original*
  stall (an unbounded body read) — this is why the issue went quiet after
  that date.
- `2ba589fc` (2026-08-07, PR #1269, "retry-instead-of-logout on
  verify-timeout") changed session verification from one 15s attempt to **up
  to two sequential 15s attempts**, to fix a different problem (logout
  flakiness, EQ-SHELL-T). Legitimate worst-case wait is now ~30s.
- Nobody reconciled the two: the 20s watchdog is shorter than the 30s
  worst-case retry it now has to tolerate. Since 2026-08-07, any session
  verify that legitimately needs the second attempt outlives the spinner
  watchdog and fires a false "stalled" alert mid-recovery — matching the
  regression date and the 7 occurrences since.

**Proposed fix:** raise `WATCHDOG_MS` to comfortably clear the new worst case
(e.g. 35–40s), or make the watchdog retry-aware (reset it when the retry
attempt starts, same pattern already used for the visibilitychange guard).
Either is a small, contained change to `App.tsx`. Not started — this touches
the auth-loading path on an app that deploys the instant a PR merges to
`main`, so it's waiting on your go per the standing auth-change rule, not on
any remaining investigation.

---

## Summary

| # | Item | Status | Action |
|---|---|---|---|
| 1 | SEC-1 | Standing decision, correctly red | None — stays open until Field replaces SKS NSW Labour |
| 2 | F14 possible recurrence | Checked, doesn't hold up | None — don't bump the recurrence count |
| 3 | Degraded UI Performance | Single data point | Watch only |
| 4 | auth-stall: session-spinner-timeout | Real bug, root cause found | **Your call to build** — small `App.tsx` fix, auth-adjacent, needs your go before I touch it |
