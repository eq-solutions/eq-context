---
title: Sprint scoping — the redundancy review's 3 "needs you" + deferred items
owner: Royce Milmlow
last_updated: 2026-09-09
scope: Triage of the 2026-09-08 redundancy review's session-close card — the 3 items needing Royce directly, plus the genuinely still-open deferred items (not the ones already being handled in a separate session). Live-verified, not restated from the card.
read_priority: high
status: live
---

# Sprint scoping — redundancy review follow-ups

Triggered by Royce asking to "create a sprint for the 5 deferred and 3 need me
items" off the 2026-09-08 session-close card. Same pattern as
[`eq/sprints/2026-08-18-needs-you-triage.md`](2026-08-18-needs-you-triage.md) —
verified live, not just restated.

**Count note:** the card said 5 deferred; this doc scopes 4. The 5th
(this checkout's own git drift) isn't a new action item — Royce is already
handling it directly in a separate session (see `sessions/2026-09-08.md`'s
F16 entry) — so it's named here for completeness and left out of the table.

---

## 1. Netlify — add a second team member, turn on `enforce_mfa`

**Needs you. Not a build task — needs your own hands in the Netlify dashboard,
nothing to scope.**

Confirmed live 2026-09-08: `Milmlow's team` (Pro plan) still has exactly 1
member, `enforce_mfa: "not_enforced"`. No secondary access path exists to any
of the 4 EQ production sites (Shell/Field/Service/Cards) if this one account
is ever locked out. Full detail: `system/redundancy-review-2026-09-08.md` §2.

**Action:** Team settings → Members → Invite (someone you trust for recovery
access, doesn't need to be day-to-day active). Team settings → Security →
require 2FA for all members.

---

## 2. `ops/bus-factor-runbook.md` §1 — "Who to contact"

**Needs you. Not buildable by a session — needs your own knowledge of who
else has access where.**

The runbook itself says so: *"only Royce can complete this section."*
Currently blank across all five rows (GitHub org admin, Netlify, Supabase org,
SKS emergency contact, domain/DNS registrar). This is the single-highest-
priority gap the runbook itself names.

**Action:** fill the checklist, or say the word and a session will walk
through it with you one row at a time.

---

## 3. `backup-code.yml` needs `CODE_BACKUP_PAT`

**Needs you. One secret, then it runs itself.**

The nightly code-backup workflow (item 4 of the review) is built and live on
`main` but cannot do anything yet — every run fails loudly at the first clone
attempt without this secret.

**Action:** create a fine-grained GitHub PAT, read-only "Contents" access
scoped to `eq-shell`/`eq-field`/`eq-service`/`eq-cards`/`eq-solves-intake`/
`eq-context`. Add as the `CODE_BACKUP_PAT` secret in eq-context's
`production-ops` environment (same environment the DB backup jobs already
use).

---

## 4. GitHub org-admin membership — genuinely unknown, needs your own check

**Not buildable — no session has the access to check this.**

The GitHub connector available to sessions this week can read
`eq-context`/`eq-solves-intake`/`eq-roles`/`eq-ui`/`eq-design-tokens`/
`eq-contracts`/`sks-nsw-labour`/`test` but returns a clean `404` on
`eq-shell`/`eq-field`/`eq-service`/`eq-cards` — a scoped App installation, not
evidence those repos don't exist (they're extremely well-evidenced
elsewhere). There is no working "list org members" path from any session.

**Action:** check `github.com/orgs/eq-solutions/people` directly. Feeds §1
above either way.

---

## 5. Registrar-lock + Cloudflare account MFA — genuinely unknown, still open a month later

**Not buildable — dashboard-only, no tool access from any session.**

First flagged in `system/infra-redundancy-scoping-2026-08-11.md`: `eq.solutions`
DNS is confirmed live on Cloudflare (re-checked 2026-09-08, unchanged), but
registrar-lock status (GoDaddy) and Cloudflare account MFA posture have never
been independently verified — only ever "documented," never checked.

**Action:** two dashboard logins, ~5 minutes combined. Feeds §1 above too.

---

## 6. Sentry alert rule on `token-exchange.ts` — blocked by a dead API, still unknown

**Not buildable from here — the tool path itself doesn't work.**

Whether a live alert actually pages anyone if eq-shell's session-mint path
starts failing broadly has never been confirmed either way.
`find_alert_rules` returned `410 Gone` when checked 2026-09-08 — the endpoint
no longer exists, not a permissions block. Not chased further; a different
tool path (Sentry's own dashboard, or a different API version) would need to
answer this.

**Action:** check directly in the Sentry dashboard (Alerts → project
`eq-shell`) — thirty seconds, no tool needed.

---

## 7. Auth-stall watchdog fix didn't hold — real bug, root cause unknown, corrects yesterday's decision log

**This one is genuinely buildable-adjacent — but needs investigation before
a fix, not a re-guess. Also corrects `ops/decisions.md`'s 2026-09-08 entry,
which understated this.**

EQ-SHELL-T (`auth-stall: verify-timeout`) and EQ-SHELL-V
(`auth-stall: session-spinner-timeout`) are the same pair a prior sprint
(`2026-08-18-needs-you-triage.md` item 4) already root-caused via git
archaeology: `App.tsx`'s `BlockingSpinner` watchdog (20s) firing before
`RequireSession`'s up-to-30s two-attempt verify retry could legitimately
finish. Fix shipped same day: raise `WATCHDOG_MS` to 35s
([eq-shell PR #1433](https://github.com/eq-solutions/eq-shell/pull/1433),
confirmed live in `App.tsx` today, 35s, with a comment citing the exact same
30s ceiling).

**What's new, confirmed today (2026-09-09):** both issues kept occurring for
nearly three weeks *after* that fix — through 2026-09-06 (32 and 21 total
occurrences respectively). Yesterday's redundancy-review `/decide` pass read
this as "a narrower, already-partially-addressed mechanism" — that
understated it. The August fix evidently didn't fully close the gap, or a
different trigger now produces the same two error signatures. Which one is
genuinely unknown; nobody has re-run the same git-archaeology approach
against the *current* code path yet.

**Not started** — this touches the Shell auth-loading path on an app that
auto-deploys the instant a PR merges to `core.eq.solutions`, so any actual
code change needs your go per the standing auth-review rule, same as the
August fix did. What's scoped here is the investigation, not a proposed fix
yet — there isn't enough to propose one responsibly.

---

## Summary

| # | Item | Status | Action |
|---|---|---|---|
| 1 | Netlify 2nd admin + MFA | Confirmed gap, cheap fix | **Your hands** — dashboard, ~5 min |
| 2 | Bus-factor runbook §1 | Confirmed gap | **Your knowledge** — fill or walk through it together |
| 3 | `CODE_BACKUP_PAT` | Confirmed blocker | **Your hands** — one PAT, one secret |
| 4 | GitHub org-admin check | Genuinely unknown | **Your check** — no session can see this |
| 5 | Registrar-lock + Cloudflare MFA | Genuinely unknown | **Your check** — two dashboard logins |
| 6 | Sentry alert rule, token-exchange | Genuinely unknown | **Your check** — dead API from here |
| 7 | Auth-stall watchdog recurrence | Real bug, root cause unknown | **Investigation first** — no fix proposed yet, needs your go once scoped |
