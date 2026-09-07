---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-09-07
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-09-07 10:12 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-09-07 09:56 UTC → 2026-09-07 10:12 UTC)

- Merged: eq-shell [#1798](https://github.com/eq-solutions/eq-shell/pull/1798) feat(staff): reframe Resourcing around conversations happeni
- Merged: eq-shell [#1787](https://github.com/eq-solutions/eq-shell/pull/1787) fix(auth): pause before verify-shell-session's retry to outl
- Merged: eq-shell [#1784](https://github.com/eq-solutions/eq-shell/pull/1784) feat(documents): add person-first grouping to the signoff re
- Merged: eq-shell [#1782](https://github.com/eq-solutions/eq-shell/pull/1782) docs(auth): clarify tenant-membership.ts's intentional users
- Merged: eq-shell [#1780](https://github.com/eq-solutions/eq-shell/pull/1780) fix(onboarding): exclude personal tenants from the onboardin
- Merged: eq-shell [#1778](https://github.com/eq-solutions/eq-shell/pull/1778) fix(auth): stop tenant_config/tenant_routing timeouts from f
- Merged: eq-shell [#1776](https://github.com/eq-solutions/eq-shell/pull/1776) feat(security): detect drift between tenant rosters and user
- Merged: eq-shell [#1775](https://github.com/eq-solutions/eq-shell/pull/1775) fix(auth): licence-visibility reads no longer trust org_memb

## ⚠ Needs you (9)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-71 (P1 — deliberate, review 2026-12-04) — Two-factor authentication is switched off for everyone by two hard-coded constan · [security-register.md](ops/security-register.md)
- 🔴 **Cron failing** — `shared-object-drift.yml` 6 consecutive scheduled run(s) failed, no success in recent history · [failures.md](system/failures.md) F11
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-08-23.md](sessions/2026-08-23.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F9: Concurrent-session git races corrupt the shared eq-context checkout · possibly recurred in [2026-09-04.md](sessions/2026-09-04.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F10: core.hooksPath silently resolves to the wrong location — four distinct mechanisms, one sym · possibly recurred in [2026-09-07.md](sessions/2026-09-07.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F12: Side-clone reconciliation blind-overwrote a concurrent session's already-pushed shared-fil · possibly recurred in [2026-08-30.md](sessions/2026-08-30.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-09-07.md](sessions/2026-09-07.md) · [failures.md](system/failures.md)
- 🟠 **Deploy building** — eq-shell (core.eq.solutions)

## 🙋 Waiting on you (260)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **eq-shell** · **Not click-tested live** — same standing gap as the PR's own test plan: nobody has backgrounded a real tab mid-handoff past 10s and confirmed no notice/Sentry event fires while hidden, and that a still-stuck handoff still alarms promptly (with accurate elapsed time) on return to the tab. No Shell session/credentials in this environment.
- **eq-shell** · **None of tonight's 4 fixes have been click-tested live by a person** — verified via full test suite + lint + an independent merge-readiness audit only. Worth a real pass once convenient: try resetting a platform_admin's PIN as a regular manager (should 403 `cannot-reset-platform-admin`); try switching tenant on a session that's been logged out/revoked elsewhere (should 401, not succeed).
- **eq-shell** · **#711/SEC-71 — mandatory TOTP enforcement is genuinely client-side only**, reconfirmed live (`shell-login.ts:476-495` issues a full session regardless of the flag). The issue itself says it needs Royce's call on intended grace-period semantics before anyone implements a fix — not built.
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment. Worth a real pass: push a document to a crew and confirm it can't resolve another tenant's crew; approve a Cards application with a start date and confirm onboarding documents land automatically; confirm an archived document can't be pushed/republished via the UI. _(added 2026-09-05)_
- **eq-shell** · **Quotes-search fix ([PR #1754](https://github.com/eq-solutions/eq-shell/pull/1754)) — list/table view not click-tested**, only board view. Confirmed live: with the "Open" tab active, searching `SKS-17512` (Invoiced-stage only) still surfaced it under Invoiced, with the "search covers every stage, not just the tab selected" notice showing correctly. _(added 2026-09-05)_
- **eq-shell** · **The one piece not done: actually clicking Grant/Revoke platform admin end-to-end.** Deliberately not tested against a real employee — granting or revoking "every permission, in every tenant," even briefly and reversibly, is real enough that it needs either Royce's own hands or a disposable test account named for the purpose. Nobody's pointed at one yet. Full detail on what WAS confirmed live: `sessions/2026-09-05.md`. _(added 2026-08-17, 2026-08-18, 2026-08-25; consolidated 2026-09-05; click-tested 2026-09-05)_
- **eq-shell** · **3 of the 4 fixes verified only via `tsc -b --force` + eslint + `pnpm test` (including a negative-proof test per fix: fails on the pre-fix code, passes on the fix) — not a real click-through.** Only PR #1760's rate-limit reordering got an end-to-end live check (real HTTP requests against its deploy preview, cross-checked against the live `rate_limit_buckets`/`audit_log` tables). Worth a real pass on the other three: trigger `update_site`/`add_site` with an inactive contact and confirm it's rejected before any write lands; delete a user with linked staff/worker records and confirm the purge stays inside one tenant; open a PR with a deliberately colliding migration prefix and confirm CI fails it. _(added 2026-09-04)_
- **eq-shell** · **Not click-tested live** — verified via `pnpm exec tsc -b --force` and `eslint` (both clean) plus an independent merge-readiness audit before merging. This machine's Node 24 breaks `vite build`/`netlify dev` for this repo (pre-existing, unrelated to this change), so no live click-through was possible. Worth a real pass: KPI numbers match the table's own counts, per-team rows sum to the roster totals, mobile view unchanged. _(added 2026-09-02)_
- **eq-shell** · **Not click-tested live** — PR #1708's own test plan flags this: build/tests/lint clean, but nobody's archived a real staff-linked account and watched the new checkbox clear it. _(added 2026-09-01)_
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment, and Vite/`netlify dev` are unreliable under this machine's Node 24 (existing memory), so no attempt was made to fake it. Worth a real pass: open a customer with a Field-enabled site and confirm the pill now shows on; toggle the pill off and confirm every owned site follows; check a customer with zero sites shows the toggle disabled with the right tooltip; same 3 checks on the separate App activation admin page. _(added 2026-09-01; re-attempted 2026-09-07 — still blocked, in-app Browser shows the sign-in screen and Claude in Chrome has zero connected browsers in this environment; `/decide` recommended Royce run the 6 checks himself (~5 min) and report back, or connect Claude in Chrome so a session can test it directly next time)_
- **eq-shell** · **3 directories left on disk, OS-locked, not deletable from this session** — `git worktree remove` unregistered them from git (2 errored "Result too large" but still unregistered; 1 confirmed via `git worktree prune`), but the physical folders survived both `Remove-Item -Force` and `rm -rf` ~10 minutes apart, both failing with "device or resource busy" / "being used by another process." Locking process not identified (`Get-CimInstance Win32_Process` showed nothing obviously relevant). Needs Royce to close whatever has them open (or a reboot) before they're actually reclaimable: `.claude\worktrees\contact-auto-site-ops-download-325f25`, `.claude\worktrees\list-user-invites-existing-user-filter`, `.claude\worktrees\simplified-interface-users-764a0d`. _(added 2026-09-01)_
- **eq-shell** · **Not click-tested live by a person** — verified via `tsc -b --force`, `eslint`, an 8-angle automated review, and Netlify deploy-preview smoke tests; no Shell session/credentials in this environment. Worth a real pass covering both PRs (#1683, #1685): panel opens in place with a shareable `?open=` URL; a formal entry opens with full detail, rating deltas, and (where attached) a source document; saving without answering "happy and engaged" is blocked and scrolls to the field; engagement tags render with color; a person with no `start_date` is flagged "missing a start date" but NOT also "overdue"; a hollow historical review shows its summary and one "no structured answers" note instead of ~20 blank fields. _(added 2026-08-30)_
_…and 248 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 7 | 6d |
| eq-solves-service | ✓ success | 0d ago | 6 | 2d |
| eq-field | ✓ success | 0d ago | 3 | 4d |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Deploys

| Site | State | Last deploy |
|------|-------|-------------|
| eq-shell | building | 2026-09-07 |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 14 | 2026-09-06 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 13 | 2026-09-06 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
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
| 2026-09-07 | eq-field | [#934](https://github.com/eq-solutions/eq-field/pull/934) v3.5.689 — FIX: team-less person's roster row (leave included) va |
| 2026-09-07 | eq-field | [#935](https://github.com/eq-solutions/eq-field/pull/935) v3.5.689 — FIX: Timesheets day/date header text was low-contrast  |
_Showing 15 of 77 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-shell** (258 open) · [eq/pending/eq-shell.md](eq/pending/eq-shell.md)
- **eq-cards** (63 open) · [eq/pending/eq-cards.md](eq/pending/eq-cards.md)
- **eq-field** (240 open) · [eq/pending/eq-field.md](eq/pending/eq-field.md)
- **eq-solves-service** (68 open) · [eq/pending/eq-solves-service.md](eq/pending/eq-solves-service.md)
- **eq-solves-intake** (18 open) · [eq/pending/eq-solves-intake.md](eq/pending/eq-solves-intake.md)
- **eq-design-tokens** (1 open) · [eq/pending/eq-design-tokens.md](eq/pending/eq-design-tokens.md)
- **eq-ui** (2 open) · [eq/pending/eq-ui.md](eq/pending/eq-ui.md)
- **eq-receipts** (4 open) · [eq/pending/eq-receipts.md](eq/pending/eq-receipts.md)
- **eq-context** (34 open) · [eq/pending/eq-context.md](eq/pending/eq-context.md)
- **cross-repo** (165 open) · [eq/pending/cross-repo.md](eq/pending/cross-repo.md)
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
| [eq-shell](eq/pending/eq-shell.md) | 1348 | 190 / 77 | 4 | 62 |
| [eq-cards](eq/pending/eq-cards.md) | 351 | 46 / 17 | 0 | 9 |
| [eq-field](eq/pending/eq-field.md) | 1284 | 176 / 71 | 50 | 48 |
| [eq-solves-service](eq/pending/eq-solves-service.md) | 391 | 49 / 20 | 0 | 20 |
| [eq-solves-intake](eq/pending/eq-solves-intake.md) | 140 | 13 / 5 | 0 | 17 |
| [eq-design-tokens](eq/pending/eq-design-tokens.md) | 23 | 1 / 0 | 0 | 1 |
| [eq-ui](eq/pending/eq-ui.md) | 22 | 2 / 0 | 0 | 0 |
| [eq-receipts](eq/pending/eq-receipts.md) | 44 | 3 / 1 | 0 | 2 |
| [eq-context](eq/pending/eq-context.md) | 207 | 26 / 8 | 0 | 8 |
| [cross-repo](eq/pending/cross-repo.md) | 776 | 120 / 45 | 0 | 74 |
| [sks](eq/pending/sks.md) | 53 | 3 / 5 | 0 | 6 |
| [SKS](sks/pending.md) | 493 | 95 / 13 | 0 | 62 |
| [SKS active](sks/active.md) | 119 | 0 / 0 | 0 | 0 |
| [OPS](ops/pending.md) | 600 | 51 / 4 | 2 | 13 |

## Aging open items (45d+, unconfirmed)

_Open items sitting under a section header this old or older — not necessarily wrong, just gone quiet under its own dated write-up. Worth a look before it reads as done-and-forgotten._

- **eq-shell** (2026-07-23) · **Royce hasn't yet re-pulled a fresh export to eyeball the fixed cells himself** — the fix was confirmed via direct RPC call, not a real export download; he asked for this exact check but got redirected before it happened. _(added 2026-07-26)_
- **eq-shell** (2026-07-23) · **New: the automatic "read the certificate for me" step failed once on a PDF upload, rejected by the server that does the reading.** Didn't affect the person uploading — it just quietly fell back to typing the details in by hand, same as if no reading happened at all. Only happened once so far. Task chip spawned to check whether the two systems' shared password has gotten out of sync (which would keep failing) or it was a one-off. _(added 2026-07-23)_
- **eq-shell** (2026-07-23) · **The tripwire fix eq-solves-service got today (see that entry below) hasn't been built for eq-shell, and eq-shell needs it too.** This session's assigned private folder had nothing in it — ended up doing all its real work in the one shared master copy instead, same mechanism as eq-solves-service's bug. Confirmed live mid-session: a second, unrelated concurrent session's own work-in-progress (a database list-loading improvement) was sitting there uncommitted where this session could see it, and that session's own folder-switch changed what this session was pointed at partway through, without warning. Nothing was lost either time — caught before anything got mixed up — but it's luck, not a safeguard. _(added 2026-07-23)_
- **eq-shell** (2026-07-21) · **A separate, already-diagnosed cause of people getting logged out unexpectedly** (a background check treats "the server was just slow to answer" the same as "you're not logged in any more," and logs you out either way) is understood but not yet built, since it changes how login/session behaviour works and needs an explicit go-ahead first. _(added 2026-07-21)_
- **eq-shell** (2026-07-21) · **Worth a quick look once deployed:** confirm the Company field shows/saves correctly for Labour Hire and Subcontractor (desktop + mobile), and re-export SKS-17386 to confirm Clarifications now sits left-aligned without needing a manual fix in Word. _(added 2026-07-21)_
- **eq-shell** (2026-07-21) · **The third — a simple "how sure are we this credential is real" label on licences — is deliberately parked**, not forgotten: Royce's 90/10 decision (90% on the SKS career, company-scale Cards parked) puts this on the wrong side of the line, since it's a cross-company trust signal SKS's own onboarding doesn't need. Revisit only if the company-scale question reopens. Full detail in the audit doc (`eq-context/eq/cards/portable-trade-identity-audit-2026-07-20.md`). _(added 2026-07-21)_
- **eq-shell** (2026-07-19) · **Still open, not urgent:** the exact reason EQ Field was slow to load for that one person on 2026-07-19 is unconfirmed — likely just a poor connection, but couldn't fully rule out anything worse. Nothing else has reported it since. _(added 2026-07-19)_
- **eq-shell** (2026-07-17) · **Deferred: who should get the weekly summary email?** Built and ready, just needs a recipient list from Royce before it's switched on. _(added 2026-07-17)_
- **eq-shell** (2026-07-16) · **Deferred: extend the "you'll lose this" warning** to other forms — site details, invites, admin settings. Currently only on quotes. _(added 2026-07-19)_
- **eq-shell** (2026-07-16) · **Deferred: make long lists load a page at a time** instead of everything at once (quotes, comms roster, staff, customers). _(added 2026-07-19)_
- **eq-shell** (2026-07-16) · **Now in scope, not yet built: extend the "you'll lose this" warning to more forms** (site details, invites, admin settings — currently only quotes), a plain "you're offline" banner when the connection drops, and re-checking sign-in status automatically when someone comes back to a tab left open a while. _(added 2026-07-19)_
- **eq-shell** (2026-07-17) · **Royce to eyeball the live dashboard signed in** — the endpoint/bundle/error-monitoring checks are all clean, but only a signed-in pass confirms the three bands render correctly and the rostered-but-lapsed join surfaces real people. _(added 2026-07-17)_
- **eq-shell** (2026-07-17) · **Phase 2 deferred: crew-demand overlay.** Needs a `crew_required` column added to `app_data.jobs` (One Pipe migration, both planes) so the "can we staff what we've won" verdict has a real demand side — supply side (deployable crew) is live now, demand isn't wired yet. _(added 2026-07-16)_
- **eq-shell** (2026-07-17) · **Phase 3 deferred: the one commercial signal permitted by the scope decision** — "N quotes won but no job number yet," gated behind `quotes.view`, no dollar amount, off the default board. Not built. _(added 2026-07-16)_
- **eq-shell** (2026-07-17) · **Eyeball the next SKS morning brief once signed in** to confirm the signals render as expected end-to-end. The query logic is verified against live data and the deploy is smoke-verified, but the authed brief output itself needs a signed-in SKS session (10-minute per-user cache, or wait for the daily scheduled email). _(added 2026-07-17)_
_…and 307 more — see each file's Queue health row above._

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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-09-07 10:12 UTC._
