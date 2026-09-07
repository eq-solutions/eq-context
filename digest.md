---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-09-07
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-09-07 10:25 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-09-07 10:23 UTC → 2026-09-07 10:25 UTC)

- Merged: eq-shell [#1800](https://github.com/eq-solutions/eq-shell/pull/1800) fix(security): bump fast-uri past 4 newer SSRF/host-confusio
- Merged: eq-shell [#1781](https://github.com/eq-solutions/eq-shell/pull/1781) fix(quotes): give closed-lost quotes a lane on the EQ Ops bo
- Merged: eq-shell [#1779](https://github.com/eq-solutions/eq-shell/pull/1779) fix(auth): re-check tenant membership at JWT mint time, not 
- Merged: eq-shell [#1777](https://github.com/eq-solutions/eq-shell/pull/1777) fix(onboarding): daily sweep catches starters whose Shell lo
- Merged: eq-shell [#1774](https://github.com/eq-solutions/eq-shell/pull/1774) fix(cards): fill staff.user_id when Cards worker link resolv
- Merged: eq-shell [#1773](https://github.com/eq-solutions/eq-shell/pull/1773) fix(auth): revoke org_memberships when a shell login is deac
- Merged: eq-shell [#1756](https://github.com/eq-solutions/eq-shell/pull/1756) chore(intake): auto re-vendor eq-intake/eq-platform
- Merged: eq-field [#935](https://github.com/eq-solutions/eq-field/pull/935) v3.5.689 — FIX: Timesheets day/date header text was low-cont

## ⚠ Needs you (9)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-71 (P1 — deliberate, review 2026-12-04) — Two-factor authentication is switched off for everyone by two hard-coded constan · [security-register.md](ops/security-register.md)
- 🔴 **Cron failing** — `shared-object-drift.yml` 6 consecutive scheduled run(s) failed, no success in recent history · [failures.md](system/failures.md) F11
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-08-23.md](sessions/2026-08-23.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F9: Concurrent-session git races corrupt the shared eq-context checkout · possibly recurred in [2026-09-04.md](sessions/2026-09-04.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F10: core.hooksPath silently resolves to the wrong location — four distinct mechanisms, one sym · possibly recurred in [2026-09-07.md](sessions/2026-09-07.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F12: Side-clone reconciliation blind-overwrote a concurrent session's already-pushed shared-fil · possibly recurred in [2026-08-30.md](sessions/2026-08-30.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-09-07.md](sessions/2026-09-07.md) · [failures.md](system/failures.md)
- 🟠 **Deploy new** — eq-shell (core.eq.solutions)

## 🙋 Waiting on you (272)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **eq-shell** · **Migration 0303 not yet dispatched** — same boat as the open 0302 item below: merging lands the file, but `tenant-migrate.yml`'s apply is a separate, explicit `workflow_dispatch` with no approval gate, fleet-wide by default unless scoped via `slug`. Both 0302 and 0303 are now pending the same dispatch. Recommend `slug=ehow` for a first run given 0303 was purpose-built for SKS's data volume, though it's schema-only and safe fleet-wide too. Royce's call. _(added 2026-09-07)_
- **eq-shell** · **Not click-tested live** — same standing gap as the PR's own test plan: nobody has backgrounded a real tab mid-handoff past 10s and confirmed no notice/Sentry event fires while hidden, and that a still-stuck handoff still alarms promptly (with accurate elapsed time) on return to the tab. No Shell session/credentials in this environment.
- **eq-shell** · **None of tonight's 4 fixes have been click-tested live by a person** — verified via full test suite + lint + an independent merge-readiness audit only. Worth a real pass once convenient: try resetting a platform_admin's PIN as a regular manager (should 403 `cannot-reset-platform-admin`); try switching tenant on a session that's been logged out/revoked elsewhere (should 401, not succeed).
- **eq-shell** · **#711/SEC-71 — mandatory TOTP enforcement is genuinely client-side only**, reconfirmed live (`shell-login.ts:476-495` issues a full session regardless of the flag). The issue itself says it needs Royce's call on intended grace-period semantics before anyone implements a fix — not built.
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment. Worth a real pass: push a document to a crew and confirm it can't resolve another tenant's crew; approve a Cards application with a start date and confirm onboarding documents land automatically; confirm an archived document can't be pushed/republished via the UI. _(added 2026-09-05)_
- **eq-shell** · **Quotes-search fix ([PR #1754](https://github.com/eq-solutions/eq-shell/pull/1754)) — list/table view not click-tested**, only board view. Confirmed live: with the "Open" tab active, searching `SKS-17512` (Invoiced-stage only) still surfaced it under Invoiced, with the "search covers every stage, not just the tab selected" notice showing correctly. _(added 2026-09-05)_
- **eq-shell** · **The one piece not done: actually clicking Grant/Revoke platform admin end-to-end.** Deliberately not tested against a real employee — granting or revoking "every permission, in every tenant," even briefly and reversibly, is real enough that it needs either Royce's own hands or a disposable test account named for the purpose. Nobody's pointed at one yet. Full detail on what WAS confirmed live: `sessions/2026-09-05.md`. _(added 2026-08-17, 2026-08-18, 2026-08-25; consolidated 2026-09-05; click-tested 2026-09-05; deferred again 2026-09-07 via `/triage` — still nobody pointed at a disposable test account)_
- **eq-shell** · **3 of the 4 fixes verified only via `tsc -b --force` + eslint + `pnpm test` (including a negative-proof test per fix: fails on the pre-fix code, passes on the fix) — not a real click-through.** Only PR #1760's rate-limit reordering got an end-to-end live check (real HTTP requests against its deploy preview, cross-checked against the live `rate_limit_buckets`/`audit_log` tables). Worth a real pass on the other three: trigger `update_site`/`add_site` with an inactive contact and confirm it's rejected before any write lands; delete a user with linked staff/worker records and confirm the purge stays inside one tenant; open a PR with a deliberately colliding migration prefix and confirm CI fails it. _(added 2026-09-04)_
- **eq-shell** · **Not click-tested live** — verified via `pnpm exec tsc -b --force` and `eslint` (both clean) plus an independent merge-readiness audit before merging. This machine's Node 24 breaks `vite build`/`netlify dev` for this repo (pre-existing, unrelated to this change), so no live click-through was possible. Worth a real pass: KPI numbers match the table's own counts, per-team rows sum to the roster totals, mobile view unchanged. _(added 2026-09-02)_
- **eq-shell** · **Not click-tested live** — PR #1708's own test plan flags this: build/tests/lint clean, but nobody's archived a real staff-linked account and watched the new checkbox clear it. _(added 2026-09-01)_
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment, and Vite/`netlify dev` are unreliable under this machine's Node 24 (existing memory), so no attempt was made to fake it. Worth a real pass: open a customer with a Field-enabled site and confirm the pill now shows on; toggle the pill off and confirm every owned site follows; check a customer with zero sites shows the toggle disabled with the right tooltip; same 3 checks on the separate App activation admin page. _(added 2026-09-01; re-attempted 2026-09-07 — still blocked, in-app Browser shows the sign-in screen and Claude in Chrome has zero connected browsers in this environment; `/decide` recommended Royce run the 6 checks himself (~5 min) and report back, or connect Claude in Chrome so a session can test it directly next time)_
- **eq-shell** · **3 directories left on disk, OS-locked, not deletable from this session** — `git worktree remove` unregistered them from git (2 errored "Result too large" but still unregistered; 1 confirmed via `git worktree prune`), but the physical folders survived both `Remove-Item -Force` and `rm -rf` ~10 minutes apart, both failing with "device or resource busy" / "being used by another process." Locking process not identified (`Get-CimInstance Win32_Process` showed nothing obviously relevant). Needs Royce to close whatever has them open (or a reboot) before they're actually reclaimable: `.claude\worktrees\contact-auto-site-ops-download-325f25`, `.claude\worktrees\list-user-invites-existing-user-filter`, `.claude\worktrees\simplified-interface-users-764a0d`. _(added 2026-09-01)_
_…and 260 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 6 | 6d |
| eq-solves-service | ✓ success | 0d ago | 6 | 2d |
| eq-field | ✓ success | 0d ago | 3 | 4d |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Deploys

| Site | State | Last deploy |
|------|-------|-------------|
| eq-shell | new | 2026-09-07 |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 14 | 2026-09-06 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 13 | 2026-09-06 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-09-07 | eq-shell | [#1800](https://github.com/eq-solutions/eq-shell/pull/1800) fix(security): bump fast-uri past 4 newer SSRF/host-confusion adv |
| 2026-09-07 | eq-shell | [#1799](https://github.com/eq-solutions/eq-shell/pull/1799) fix(customers): update the customer Field/Service pill live when  |
| 2026-09-07 | eq-shell | [#1798](https://github.com/eq-solutions/eq-shell/pull/1798) feat(staff): reframe Resourcing around conversations happening, n |
| 2026-09-07 | eq-shell | [#1797](https://github.com/eq-solutions/eq-shell/pull/1797) feat(intake): add eq_tidy_read_entity_columns for column-projecte |
| 2026-09-07 | eq-shell | [#1796](https://github.com/eq-solutions/eq-shell/pull/1796) feat(staff): add a real Manager (reporting-line) field, SKS only |
| 2026-09-07 | eq-shell | [#1794](https://github.com/eq-solutions/eq-shell/pull/1794) fix(shell): extract HubSidebar's icon maps into their own module |
| 2026-09-07 | eq-shell | [#1791](https://github.com/eq-solutions/eq-shell/pull/1791) fix(security): a revoked session can no longer mint credentials o |
| 2026-09-07 | eq-shell | [#1790](https://github.com/eq-solutions/eq-shell/pull/1790) fix(security): block reset-user-pin from targeting a platform_adm |
| 2026-09-07 | eq-shell | [#1789](https://github.com/eq-solutions/eq-shell/pull/1789) fix(security): warn loudly when ENFORCE_IFRAME_ORIGIN isn't 'true |
| 2026-09-07 | eq-shell | [#1788](https://github.com/eq-solutions/eq-shell/pull/1788) docs(env): document the full .env.example surface, including two  |
| 2026-09-07 | eq-shell | [#1793](https://github.com/eq-solutions/eq-shell/pull/1793) feat(staff): redesign Teams (formerly Org Chart) for scale and ac |
| 2026-09-07 | eq-shell | [#1785](https://github.com/eq-solutions/eq-shell/pull/1785) fix(field-iframe): don't alarm on stall/draw notices while the ta |
| 2026-09-07 | eq-shell | [#1792](https://github.com/eq-solutions/eq-shell/pull/1792) chore(intake): re-vendor eq-intake to eq-solves-intake@6e1e2f2 |
| 2026-09-07 | eq-solves-service | [#831](https://github.com/eq-solutions/eq-service/pull/831) fix(security): allow EQ's R2 logo bucket in the report-only CSP i |
| 2026-09-07 | eq-field | [#936](https://github.com/eq-solutions/eq-field/pull/936) fix(security): supervisor role gets tenant-wide read on Timesheet |
_Showing 15 of 78 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-shell** (277 open) · [eq/pending/eq-shell.md](eq/pending/eq-shell.md)
- **eq-cards** (65 open) · [eq/pending/eq-cards.md](eq/pending/eq-cards.md)
- **eq-field** (240 open) · [eq/pending/eq-field.md](eq/pending/eq-field.md)
- **eq-solves-service** (68 open) · [eq/pending/eq-solves-service.md](eq/pending/eq-solves-service.md)
- **eq-solves-intake** (21 open) · [eq/pending/eq-solves-intake.md](eq/pending/eq-solves-intake.md)
- **eq-design-tokens** (1 open) · [eq/pending/eq-design-tokens.md](eq/pending/eq-design-tokens.md)
- **eq-ui** (2 open) · [eq/pending/eq-ui.md](eq/pending/eq-ui.md)
- **eq-receipts** (4 open) · [eq/pending/eq-receipts.md](eq/pending/eq-receipts.md)
- **eq-context** (34 open) · [eq/pending/eq-context.md](eq/pending/eq-context.md)
- **cross-repo** (180 open) · [eq/pending/cross-repo.md](eq/pending/cross-repo.md)
- **sks** (8 open) · [eq/pending/sks.md](eq/pending/sks.md)

## Pending (SKS)

- **Retirement work spun off as background task `task_1b21e268`, Royce started it in a separate session — running independently, not yet reported back as of this session's close.** Scoped to: check current usage, back up `nspbmirochztcjijmcrx` before anything destructive, propose (not auto-deploy) a redirect to field.eq.solutions, propose repo/DB disposition (archive/pause, never delete without separate explicit permission). _(added 2026-09-07)_
- **Cross-reference: the 2026-07-20 "real security hole" entry below is still open** — sks-nsw-labour's public web address reportedly allows reading/wiping roster/schedule/timesheet data with no login, and the drafted fix stages were never run ("not risking any changes" on a live app). Worth the retirement task treating this as a reason to prioritise taking it offline/redirecting rather than leaving it dormant-but-still-reachable. _(added 2026-09-07)_
- **Cross-reference: "Track 2 RLS STEP 2" further down this file was explicitly DEFERRED "until standalone retired"** — now potentially unblocked; worth revisiting once (or as) the retirement actually lands. _(added 2026-09-07)_
- **Affects 45 of 81 active SKS staff** (everyone Cards-linked with no wizard-entered full date of birth) — fixed going forward, but nobody's birthday has actually been re-entered yet. No action needed unless Royce wants a nudge to re-save. Most should self-resolve as people go through Cards' own licence-scan step, which fills a real date of birth in automatically. _(added 2026-08-24)_
- **Aiden's own birthday (18 Feb) was tested then reverted to blank** — unclear if that's his real date or just what was typed while reproducing the bug; needs a real re-save to confirm either way. Separately, his record still carries the *earlier* session's own trial data (job title, emergency contact, start date) that was meant to be trial-then-undo and never was — untouched by this session, still open. _(added 2026-08-24)_
- **A second, unidentified path also creates blank-name logins** — proven by timing, not guessed: Todd Wilson's and David Boyd's shell logins were created 7 weeks *after* their Cards approval, which rules out the path just patched as their cause. Spawned as background task `task_d904d388`, Royce started it in a separate session; running independently, not yet reported back as of this session's close. _(added 2026-08-23)_
- **Not verified live by a person** — the specific pill-click behavior needs a real Core+SKS session to exercise (Teams is SKS-only, gated behind Core auth, not reachable from a standalone deploy-preview session). Confirmed the fix mirrors an already-shipped, working code pattern (the crew-supervisor picker), not watched working fresh. _(added 2026-08-23)_
- **SKS's own number, for reference: 6 of 32 active SKS members are currently missing White Card** — visible today in Shell's Training Matrix; nothing blocks them from working while missing it (soft-flag by design, not an oversight). Worth a look if Royce wants a harder rule for SKS specifically. _(added 2026-08-19)_
- **A reported roster-grid "alignment" issue (one person's row looked off) couldn't be reproduced from the code** — most likely just placeholder text in blank cells reading like real data at a glance, not an actual bug, but left open rather than guessed at. _(added 2026-08-19)_
- **Still not applied to the live database — checked directly, and Royce turned down the shortcut that would have unblocked it today.** Confirmed merging the PR didn't secretly switch it on. Turning it on for real right now would lock the people who haven't signed in yet out of their own timesheet and leave the moment they do, since the fix depends on their login already being linked to their staff record — 37 of 83 active SKS staff, checked again today. A workaround exists (let just those specific people keep today's wider access until they sign in, instead of holding up everyone else) but Royce said no — waiting for them to actually sign in through the real onboarding process instead, however long that takes. _(added 2026-08-16, decision confirmed 2026-08-16)_
_…and 85 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise. Open splits engineering backlog from Royce's own queue (a confirm, a click-through, a call) — the two used to be counted together here, which made the number look worse than the real engineering backlog actually is; the split matches 'Waiting on you' above._

| File | Lines | Open (eng / you) | Done (unrotated) | Aging 45d+ |
|------|------:|------------------:|------------------:|------------:|
| [eq-shell](eq/pending/eq-shell.md) | 1439 | 201 / 85 | 6 | 76 |
| [eq-cards](eq/pending/eq-cards.md) | 355 | 48 / 17 | 0 | 9 |
| [eq-field](eq/pending/eq-field.md) | 1286 | 176 / 71 | 50 | 48 |
| [eq-solves-service](eq/pending/eq-solves-service.md) | 393 | 49 / 20 | 0 | 20 |
| [eq-solves-intake](eq/pending/eq-solves-intake.md) | 164 | 14 / 7 | 0 | 17 |
| [eq-design-tokens](eq/pending/eq-design-tokens.md) | 25 | 1 / 0 | 0 | 1 |
| [eq-ui](eq/pending/eq-ui.md) | 24 | 2 / 0 | 0 | 0 |
| [eq-receipts](eq/pending/eq-receipts.md) | 46 | 3 / 1 | 0 | 2 |
| [eq-context](eq/pending/eq-context.md) | 209 | 26 / 8 | 0 | 8 |
| [cross-repo](eq/pending/cross-repo.md) | 914 | 133 / 47 | 0 | 76 |
| [sks](eq/pending/sks.md) | 55 | 3 / 5 | 0 | 6 |
| [SKS](sks/pending.md) | 493 | 95 / 13 | 0 | 62 |
| [SKS active](sks/active.md) | 119 | 0 / 0 | 0 | 0 |
| [OPS](ops/pending.md) | 600 | 51 / 4 | 2 | 13 |

## Aging open items (45d+, unconfirmed)

_Open items sitting under a section header this old or older — not necessarily wrong, just gone quiet under its own dated write-up. Worth a look before it reads as done-and-forgotten._

- **eq-shell** (2026-07-23) · **Royce hasn't yet re-pulled a fresh export to eyeball the fixed cells himself** — the fix was confirmed via direct RPC call, not a real export download; he asked for this exact check but got redirected before it happened. _(added 2026-07-26)_ **Checked 2026-09-07 via `/triage`: still genuinely needs Royce's own eyes on a real download — that's the whole point, a second automated check wouldn't satisfy it. No live Shell session in this environment to pull one on his behalf either. Where to do it: open the quote in Job Creation and export — server-side generator is `eq-shell/netlify/functions/job-creation.ts`. Still open.**
- **eq-shell** (2026-07-23) · **The tripwire fix eq-solves-service got today (see that entry below) hasn't been built for eq-shell, and eq-shell needs it too.** This session's assigned private folder had nothing in it — ended up doing all its real work in the one shared master copy instead, same mechanism as eq-solves-service's bug. Confirmed live mid-session: a second, unrelated concurrent session's own work-in-progress (a database list-loading improvement) was sitting there uncommitted where this session could see it, and that session's own folder-switch changed what this session was pointed at partway through, without warning. Nothing was lost either time — caught before anything got mixed up — but it's luck, not a safeguard. _(added 2026-07-23)_
- **eq-shell** (2026-07-22) · **Six leftover records still need clearing — needs your hand.** A prepared script is sitting in the repo (`scripts/cleanup-orphaned-shell-users.sql`). It snapshots first, re-checks six safety conditions before touching anything, and won't save changes unless you confirm the numbers look right. It can't be automated — that database has no automatic update path. Nobody is affected in the meantime; none of these accounts can be signed into. _(added 2026-07-22)_
- **eq-shell** (2026-07-22) · **The old admin button should be guarded or retired.** It still exists and would still do the wrong thing if pointed at records like these. Its original job was finished off by fixes that went live a week ago, so it may simply be dead. Separate task, chip raised. _(added 2026-07-22)_
- **eq-shell** (2026-07-21) · **A separate, already-diagnosed cause of people getting logged out unexpectedly** (a background check treats "the server was just slow to answer" the same as "you're not logged in any more," and logs you out either way) is understood but not yet built, since it changes how login/session behaviour works and needs an explicit go-ahead first. _(added 2026-07-21)_ **Checked 2026-09-07 via `/triage` — this framing is stale, not actioned: `App.tsx`'s `SessionProvider` shows this exact problem class has had real, continuous engineering since (#888, #1174, then deadline-bounding #1736/#1764/#1778), and it regressed again as recently as 2026-09-06 (Sentry "EQ-SHELL-T/V"), tracked under the separate "EQ Field white-pane stall" section below. The retry logic reduces false logouts but the final fallback still logs out on a fully-exhausted stall — the underlying tension this bullet names is real and current, just not "not yet built." Did not write a session/auth code change on this click — no explicit go-ahead for a specific approach, and any fix belongs in the already-active thread, not as a second parallel effort. Left open; superseded by the white-pane-stall tracking above as the live record.**
- **eq-shell** (2026-07-21) · **Worth a quick look once deployed:** confirm the Company field shows/saves correctly for Labour Hire and Subcontractor (desktop + mobile), and re-export SKS-17386 to confirm Clarifications now sits left-aligned without needing a manual fix in Word. _(added 2026-07-21)_ **Checked 2026-09-07 via `/triage`: same blocker as the rest of this bucket — no live Shell session in this environment for either the UI click-test or the SKS-17386 doc re-export (`quoteDocGenerator.ts` needs an authed session). Still open; needs a real Shell sign-in to close out.**
- **eq-shell** (2026-07-21) · **The third — a simple "how sure are we this credential is real" label on licences — is deliberately parked**, not forgotten: Royce's 90/10 decision (90% on the SKS career, company-scale Cards parked) puts this on the wrong side of the line, since it's a cross-company trust signal SKS's own onboarding doesn't need. Revisit only if the company-scale question reopens. Full detail in the audit doc (`eq-context/eq/cards/portable-trade-identity-audit-2026-07-20.md`). _(added 2026-07-21)_
- **eq-shell** (2026-07-19) · **Still open, not urgent:** the exact reason EQ Field was slow to load for that one person on 2026-07-19 is unconfirmed — likely just a poor connection, but couldn't fully rule out anything worse. Nothing else has reported it since. _(added 2026-07-19)_
- **eq-shell** (2026-07-17) · **Deferred: who should get the weekly summary email?** Built and ready, just needs a recipient list from Royce before it's switched on. _(added 2026-07-17)_
- **eq-shell** (2026-07-17) · **Declined for now (Royce's call): a personal calendar feed per crew member, and a weather warning near Microsoft dock dates.** Offered as options alongside the above; not built. _(added 2026-07-17)_
- **eq-shell** (2026-07-16) · **Deferred: bigger first-load speedup** — breaking one large file into smaller pieces that only load when needed. Real win, but a bigger change that needs a hands-on check, not just automated tests. _(added 2026-07-19)_
- **eq-shell** (2026-07-16) · **Deferred: extend the "you'll lose this" warning** to other forms — site details, invites, admin settings. Currently only on quotes. _(added 2026-07-19)_
- **eq-shell** (2026-07-16) · **Deferred: make long lists load a page at a time** instead of everything at once (quotes, comms roster, staff, customers). _(added 2026-07-19)_
- **eq-shell** (2026-07-16) · **Now in scope, not yet built: extend the "you'll lose this" warning to more forms** (site details, invites, admin settings — currently only quotes), a plain "you're offline" banner when the connection drops, and re-checking sign-in status automatically when someone comes back to a tab left open a while. _(added 2026-07-19)_
- **eq-shell** (2026-07-17) · **Royce to eyeball the live dashboard signed in** — the endpoint/bundle/error-monitoring checks are all clean, but only a signed-in pass confirms the three bands render correctly and the rostered-but-lapsed join surfaces real people. _(added 2026-07-17)_
_…and 323 more — see each file's Queue health row above._

## Possible recurring failures (unconfirmed)

_Session logs mention a pattern matching a known failure below, dated after its last recorded occurrence. Not yet counted — if it's real, bump `recurrences` in [failures.md](system/failures.md) and `guard-ratchet.yml` proposes promotion on its own next run._

- **F5** (rung 0) — An ungoverned shadow memory overrode the canonical contract · 1 session since last recorded, most recent [2026-08-16.md](sessions/2026-08-16.md)

## Recent sessions

| Date | Session |
|------|---------|
| 2026-09-07 | [Labour-hire licence-photo fix re-verified live; full roster audited, no other worker exposed](sessions/2026-09-07.md) |
| 2026-09-06 | [Resumed and shipped the `?tenant=demo` fix, caught two more bugs in the same class before merge](sessions/2026-09-06.md) |
| 2026-09-05 | [SEC-53 verified live, closed in the register, and merged](sessions/2026-09-05.md) |
| 2026-09-04 | [eq-shell FieldIframe TDZ/lint fix (PR #1752) — merged, confirmed live](sessions/2026-09-04.md) |
| 2026-09-03 | [Document versioning: new-version upload, version history, confirm-then-push republish](sessions/2026-09-03.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-09-07 10:25 UTC._
