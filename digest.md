---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-09-05
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-09-05 00:57 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## ⚠ Needs you (12)

- 🔴 **GitHub token rejected** — 16 API call(s) returned 401/403 this run, so every CI / open-PR / recently-merged row below is *blind, not clean*. Regenerate `EQ_CONTEXT_PAT` (fine-grained PATs expire) and re-run `digest-refresh.yml`.
- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-57 (P1) — An org-wide GitHub App installation (`grok-by-xai`, `repository_selection: all`) · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-71 (P1 — deliberate, no expiry set) — Two-factor authentication is switched off for everyone by two hard-coded constan · [security-register.md](ops/security-register.md)
- 🔴 **Cron failing** — `jwt-contract-drift.yml` 2 consecutive scheduled run(s) failed, last success 2026-09-02 · [failures.md](system/failures.md) F11
- 🔴 **Cron failing** — `shared-object-drift.yml` 4 consecutive scheduled run(s) failed, no success in recent history · [failures.md](system/failures.md) F11
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-08-23.md](sessions/2026-08-23.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F9: Concurrent-session git races corrupt the shared eq-context checkout · possibly recurred in [2026-09-04.md](sessions/2026-09-04.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F10: core.hooksPath silently resolves to the wrong location — three distinct mechanisms, one sy · possibly recurred in [2026-08-26.md](sessions/2026-08-26.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F12: Side-clone reconciliation blind-overwrote a concurrent session's already-pushed shared-fil · possibly recurred in [2026-08-30.md](sessions/2026-08-30.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-09-04.md](sessions/2026-09-04.md) · [failures.md](system/failures.md)
- 🟠 **Cron failing** — `security-audit.yml` 1 consecutive scheduled run(s) failed, last success 2026-08-23 · [failures.md](system/failures.md) F11

## 🙋 Waiting on you (275)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **eq-shell** · **The one piece not done: actually clicking Grant/Revoke platform admin end-to-end.** Deliberately not tested against a real employee — granting or revoking "every permission, in every tenant," even briefly and reversibly, is real enough that it needs either Royce's own hands or a disposable test account named for the purpose. Nobody's pointed at one yet. Full detail on what WAS confirmed live: `sessions/2026-09-05.md`. _(added 2026-08-17, 2026-08-18, 2026-08-25; consolidated 2026-09-05; click-tested 2026-09-05)_
- **eq-shell** · **3 of the 4 fixes verified only via `tsc -b --force` + eslint + `pnpm test` (including a negative-proof test per fix: fails on the pre-fix code, passes on the fix) — not a real click-through.** Only PR #1760's rate-limit reordering got an end-to-end live check (real HTTP requests against its deploy preview, cross-checked against the live `rate_limit_buckets`/`audit_log` tables). Worth a real pass on the other three: trigger `update_site`/`add_site` with an inactive contact and confirm it's rejected before any write lands; delete a user with linked staff/worker records and confirm the purge stays inside one tenant; open a PR with a deliberately colliding migration prefix and confirm CI fails it. _(added 2026-09-04)_
- **eq-shell** · **Not click-tested live** — Quotes is auth-gated and this environment had no Shell session/credentials; separately, entering credentials directly is off-limits regardless. Worth a real pass once confirmed live: search for a quote outside the default "In Progress" tab (e.g. a draft) and confirm it now surfaces in both list and board layouts, with the new notice showing. _(added 2026-09-03)_
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment. Worth a real pass: upload a new version of a document that already has real signers, confirm the version number bumps, the old signers show as needing to re-sign, "Push to the same N people" actually re-creates outstanding rows for them (and is a no-op, not a duplicate, if clicked/retried), and Version history lists every version with its own signed/outstanding count including one nobody's been pushed to yet. _(added 2026-09-03)_
- **eq-shell** · **Not click-tested live** — confirming the fix needs a live PostHog project plus a real session left open past two 5-minute poll ticks, watching PostHog's own activity feed for exactly one `$create_alias` instead of one per tick. _(added 2026-09-02)_
- **eq-shell** · **Not click-tested live** — verified via `pnpm exec tsc -b --force` and `eslint` (both clean) plus an independent merge-readiness audit before merging. This machine's Node 24 breaks `vite build`/`netlify dev` for this repo (pre-existing, unrelated to this change), so no live click-through was possible. Worth a real pass: KPI numbers match the table's own counts, per-team rows sum to the roster totals, mobile view unchanged. _(added 2026-09-02)_
- **eq-shell** · **Not click-tested live** — PR #1708's own test plan flags this: build/tests/lint clean, but nobody's archived a real staff-linked account and watched the new checkbox clear it. _(added 2026-09-01)_
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment, and Vite/`netlify dev` are unreliable under this machine's Node 24 (existing memory), so no attempt was made to fake it. Worth a real pass: open a customer with a Field-enabled site and confirm the pill now shows on; toggle the pill off and confirm every owned site follows; check a customer with zero sites shows the toggle disabled with the right tooltip; same 3 checks on the separate App activation admin page. _(added 2026-09-01)_
- **eq-shell** · **3 directories left on disk, OS-locked, not deletable from this session** — `git worktree remove` unregistered them from git (2 errored "Result too large" but still unregistered; 1 confirmed via `git worktree prune`), but the physical folders survived both `Remove-Item -Force` and `rm -rf` ~10 minutes apart, both failing with "device or resource busy" / "being used by another process." Locking process not identified (`Get-CimInstance Win32_Process` showed nothing obviously relevant). Needs Royce to close whatever has them open (or a reboot) before they're actually reclaimable: `.claude\worktrees\contact-auto-site-ops-download-325f25`, `.claude\worktrees\list-user-invites-existing-user-filter`, `.claude\worktrees\simplified-interface-users-764a0d`. _(added 2026-09-01)_
- **eq-shell** · **Not click-tested live by a person** — verified via `tsc -b --force`, `eslint`, an 8-angle automated review, and Netlify deploy-preview smoke tests; no Shell session/credentials in this environment. Worth a real pass covering both PRs (#1683, #1685): panel opens in place with a shareable `?open=` URL; a formal entry opens with full detail, rating deltas, and (where attached) a source document; saving without answering "happy and engaged" is blocked and scrolls to the field; engagement tags render with color; a person with no `start_date` is flagged "missing a start date" but NOT also "overdue"; a hollow historical review shows its summary and one "no structured answers" note instead of ~20 blank fields. _(added 2026-08-30)_
- **eq-shell** · **Not click-tested live** — same environment limitation as most of this session's other work (no Shell credentials); `netlify dev` also produced no output at all this time, which may just be the existing known Node-version flakiness rather than a new distinct failure. Verify via each PR's deploy preview or live: Resourcing's two new rating columns render "No ratings yet"; a Check-in entry shows the new weakness-improvement question; Edit pre-fills every field correctly and saves in place; the close/reopen icon toggles the "Open" tag. _(added 2026-09-01)_
- **eq-shell** · **Not click-tested live by a person** — every PR this session verified via `pnpm run build`/`eslint`/`pnpm run test`/live DB queries only, never an actual signed-in click-through. Worth a real pass: upload a document, assign/change its category from each of the 3 tabs, create a new reference-only category via the new toggle, confirm the routing actually changes. _(added 2026-08-30)_
_…and 263 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? token error | ? | 0 | — |
| eq-solves-service | ? token error | ? | 0 | — |
| eq-field | ? token error | ? | 0 | — |
| eq-cards | ? token error | ? | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |
_GitHub API returned 401/403 this run — the CI and PR columns above are unavailable, not clean. Regenerate `EQ_CONTEXT_PAT`._

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: Unclaimed worker invites past grace period: 2 still valid, 0 expired](https://eq-solutions.sentry.io/issues/142642035/) | 12 | 2026-09-04 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 12 | 2026-09-04 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 11 | 2026-09-04 |
| eq-field | [Error: 403: {"code":"42501","details":null,"hint":null,"message":"timesheet: onl](https://eq-solutions.sentry.io/issues/145012264/) | 2 | 2026-09-04 |
| eq-shell | [EQ Field handoff stalled at "minting" (10s, no 'accepted' yet)](https://eq-solutions.sentry.io/issues/145002211/) | 1 | 2026-09-04 |
| eq-field | [ReferenceError: _hookTsResizeOnce is not defined](https://eq-solutions.sentry.io/issues/144831279/) | 1 | 2026-09-04 |
| eq-cards | [minified:B8: AuthRetryableFetchException(message: ClientException: Failed to fet](https://eq-solutions.sentry.io/issues/144338444/) | 1 | 2026-09-02 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-09-04 | eq-solves-intake | [#122](https://github.com/eq-solutions/eq-solves-intake/pull/122) fix(intake-demo): land on the real product screen by default |
| 2026-09-01 | eq-solves-intake | [#121](https://github.com/eq-solutions/eq-solves-intake/pull/121) fix(intake-demo): clear remaining react-hooks/set-state-in-effect |
_2 merges · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-shell** (277 open) · [eq/pending/eq-shell.md](eq/pending/eq-shell.md)
- **eq-cards** (66 open) · [eq/pending/eq-cards.md](eq/pending/eq-cards.md)
- **eq-field** (240 open) · [eq/pending/eq-field.md](eq/pending/eq-field.md)
- **eq-solves-service** (101 open) · [eq/pending/eq-solves-service.md](eq/pending/eq-solves-service.md)
- **eq-solves-intake** (19 open) · [eq/pending/eq-solves-intake.md](eq/pending/eq-solves-intake.md)
- **eq-design-tokens** (1 open) · [eq/pending/eq-design-tokens.md](eq/pending/eq-design-tokens.md)
- **eq-ui** (2 open) · [eq/pending/eq-ui.md](eq/pending/eq-ui.md)
- **eq-receipts** (4 open) · [eq/pending/eq-receipts.md](eq/pending/eq-receipts.md)
- **eq-context** (33 open) · [eq/pending/eq-context.md](eq/pending/eq-context.md)
- **cross-repo** (180 open) · [eq/pending/cross-repo.md](eq/pending/cross-repo.md)
- **sks** (8 open) · [eq/pending/sks.md](eq/pending/sks.md)

## Pending (SKS)

- **Affects 45 of 81 active SKS staff** (everyone Cards-linked with no wizard-entered full date of birth) — fixed going forward, but nobody's birthday has actually been re-entered yet. No action needed unless Royce wants a nudge to re-save. Most should self-resolve as people go through Cards' own licence-scan step, which fills a real date of birth in automatically. _(added 2026-08-24)_
- **Aiden's own birthday (18 Feb) was tested then reverted to blank** — unclear if that's his real date or just what was typed while reproducing the bug; needs a real re-save to confirm either way. Separately, his record still carries the *earlier* session's own trial data (job title, emergency contact, start date) that was meant to be trial-then-undo and never was — untouched by this session, still open. _(added 2026-08-24)_
- **A second, unidentified path also creates blank-name logins** — proven by timing, not guessed: Todd Wilson's and David Boyd's shell logins were created 7 weeks *after* their Cards approval, which rules out the path just patched as their cause. Spawned as background task `task_d904d388`, Royce started it in a separate session; running independently, not yet reported back as of this session's close. _(added 2026-08-23)_
- **Not verified live by a person** — the specific pill-click behavior needs a real Core+SKS session to exercise (Teams is SKS-only, gated behind Core auth, not reachable from a standalone deploy-preview session). Confirmed the fix mirrors an already-shipped, working code pattern (the crew-supervisor picker), not watched working fresh. _(added 2026-08-23)_
- **SKS's own number, for reference: 6 of 32 active SKS members are currently missing White Card** — visible today in Shell's Training Matrix; nothing blocks them from working while missing it (soft-flag by design, not an oversight). Worth a look if Royce wants a harder rule for SKS specifically. _(added 2026-08-19)_
- **A reported roster-grid "alignment" issue (one person's row looked off) couldn't be reproduced from the code** — most likely just placeholder text in blank cells reading like real data at a glance, not an actual bug, but left open rather than guessed at. _(added 2026-08-19)_
- **Still not applied to the live database — checked directly, and Royce turned down the shortcut that would have unblocked it today.** Confirmed merging the PR didn't secretly switch it on. Turning it on for real right now would lock the people who haven't signed in yet out of their own timesheet and leave the moment they do, since the fix depends on their login already being linked to their staff record — 37 of 83 active SKS staff, checked again today. A workaround exists (let just those specific people keep today's wider access until they sign in, instead of holding up everyone else) but Royce said no — waiting for them to actually sign in through the real onboarding process instead, however long that takes. _(added 2026-08-16, decision confirmed 2026-08-16)_
- **The disposable EQ-side tenant doesn't have this fix** — lower priority, since that tenant holds no real data, but the identical gap exists there too and needs some prerequisite pieces built first before it can be ported. _(added 2026-08-16)_
- **Run the first real weekly export/import test** — SKS NSW Labour → Export Schedule CSV → EQ Field (logged in as the SKS org) → Import Schedule CSV. Discussed and confirmed safe; not actually run this session. _(added 2026-08-14)_
- **~7 SKS staff missing from EQ Field's staff table** (hired since the 5 Jul snapshot): Ahmed Masaud, Amir Farid, Callum Treharne, Jhon Jairo Velasquez Meneses, ~~Nabeel Hussain~~, Paul Bolger, Timothy Sue — plus a handful of name-string mismatches (e.g. "Bruno Pedrosa" vs "Bruno Vita Pedrosa", "Jose Quintanilla" vs "Jose Luis Quintanilla Rodriguez"). Royce said he'll manage this himself via EQ Field's People admin. **Correction 2026-08-25: "Nabeel Hussain" was never missing** — he's already in `app_data.staff`, just filed under his legal first name "Mohammed Hussain" (confirmed via matching personal email `nabzhussain95@…` and phone). Likely a name-string-match false positive against whatever hire list this cross-check ran against — same class of gap as the "Bruno Pedrosa" mismatch example earlier in this same bullet. Not investigated further (fixing the matching heuristic wasn't this session's scope); the other 6 names + mismatches remain unverified. _(added 2026-08-14, corrected 2026-08-25)_
_…and 82 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise. Open splits engineering backlog from Royce's own queue (a confirm, a click-through, a call) — the two used to be counted together here, which made the number look worse than the real engineering backlog actually is; the split matches 'Waiting on you' above._

| File | Lines | Open (eng / you) | Done (unrotated) | Aging 45d+ |
|------|------:|------------------:|------------------:|------------:|
| [eq-shell](eq/pending/eq-shell.md) | 1424 | 201 / 78 | 20 | 72 |
| [eq-cards](eq/pending/eq-cards.md) | 365 | 48 / 18 | 10 | 7 |
| [eq-field](eq/pending/eq-field.md) | 1249 | 168 / 72 | 41 | 41 |
| [eq-solves-service](eq/pending/eq-solves-service.md) | 513 | 77 / 24 | 1 | 32 |
| [eq-solves-intake](eq/pending/eq-solves-intake.md) | 162 | 14 / 5 | 0 | 17 |
| [eq-design-tokens](eq/pending/eq-design-tokens.md) | 23 | 1 / 0 | 0 | 1 |
| [eq-ui](eq/pending/eq-ui.md) | 22 | 2 / 0 | 0 | 0 |
| [eq-receipts](eq/pending/eq-receipts.md) | 44 | 3 / 1 | 0 | 0 |
| [eq-context](eq/pending/eq-context.md) | 215 | 25 / 8 | 3 | 8 |
| [cross-repo](eq/pending/cross-repo.md) | 903 | 133 / 47 | 1 | 67 |
| [sks](eq/pending/sks.md) | 53 | 3 / 5 | 0 | 6 |
| [SKS](sks/pending.md) | 486 | 92 / 14 | 0 | 58 |
| [SKS active](sks/active.md) | 119 | 0 / 0 | 0 | 0 |
| [OPS](ops/pending.md) | 530 | 43 / 3 | 0 | 13 |

## Aging open items (45d+, unconfirmed)

_Open items sitting under a section header this old or older — not necessarily wrong, just gone quiet under its own dated write-up. Worth a look before it reads as done-and-forgotten._

- **eq-shell** (2026-07-21) · **A separate, already-diagnosed cause of people getting logged out unexpectedly** (a background check treats "the server was just slow to answer" the same as "you're not logged in any more," and logs you out either way) is understood but not yet built, since it changes how login/session behaviour works and needs an explicit go-ahead first. _(added 2026-07-21)_
- **eq-shell** (2026-07-21) · **Worth a quick look once deployed:** confirm the Company field shows/saves correctly for Labour Hire and Subcontractor (desktop + mobile), and re-export SKS-17386 to confirm Clarifications now sits left-aligned without needing a manual fix in Word. _(added 2026-07-21)_
- **eq-shell** (2026-07-21) · **The third — a simple "how sure are we this credential is real" label on licences — is deliberately parked**, not forgotten: Royce's 90/10 decision (90% on the SKS career, company-scale Cards parked) puts this on the wrong side of the line, since it's a cross-company trust signal SKS's own onboarding doesn't need. Revisit only if the company-scale question reopens. Full detail in the audit doc (`eq-context/eq/cards/portable-trade-identity-audit-2026-07-20.md`). _(added 2026-07-21)_
- **eq-shell** (2026-07-19) · **Still open, not urgent:** the exact reason EQ Field was slow to load for that one person on 2026-07-19 is unconfirmed — likely just a poor connection, but couldn't fully rule out anything worse. Nothing else has reported it since. _(added 2026-07-19)_
- **eq-shell** (2026-07-17) · **Deferred: who should get the weekly summary email?** Built and ready, just needs a recipient list from Royce before it's switched on. _(added 2026-07-17)_
- **eq-shell** (2026-07-17) · **Declined for now (Royce's call): a personal calendar feed per crew member, and a weather warning near Microsoft dock dates.** Offered as options alongside the above; not built. _(added 2026-07-17)_
- **eq-shell** (2026-07-16) · **Deferred: bigger first-load speedup** — breaking one large file into smaller pieces that only load when needed. Real win, but a bigger change that needs a hands-on check, not just automated tests. _(added 2026-07-19)_
- **eq-shell** (2026-07-16) · **Deferred: extend the "you'll lose this" warning** to other forms — site details, invites, admin settings. Currently only on quotes. _(added 2026-07-19)_
- **eq-shell** (2026-07-16) · **Deferred: make long lists load a page at a time** instead of everything at once (quotes, comms roster, staff, customers). _(added 2026-07-19)_
- **eq-shell** (2026-07-16) · **Now in scope, not yet built: extend the "you'll lose this" warning to more forms** (site details, invites, admin settings — currently only quotes), a plain "you're offline" banner when the connection drops, and re-checking sign-in status automatically when someone comes back to a tab left open a while. _(added 2026-07-19)_
- **eq-shell** (2026-07-17) · **Royce to eyeball the live dashboard signed in** — the endpoint/bundle/error-monitoring checks are all clean, but only a signed-in pass confirms the three bands render correctly and the rostered-but-lapsed join surfaces real people. _(added 2026-07-17)_
- **eq-shell** (2026-07-17) · **Gate keys are interim** (`field.view`/`service.view`) — swap to the cluster-1 granular keys (`field.view_licences` etc., PR #885, concurrent session) once that ships. _(added 2026-07-17)_
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
| 2026-09-05 | [SEC-53 verified live, closed in the register, and merged](sessions/2026-09-05.md) |
| 2026-09-04 | [eq-shell FieldIframe TDZ/lint fix (PR #1752) — merged, confirmed live](sessions/2026-09-04.md) |
| 2026-09-03 | [Document versioning: new-version upload, version history, confirm-then-push republish](sessions/2026-09-03.md) |
| 2026-09-02 | [Live-meeting kit: sample ID sheet added, QR-at-scale question resolved by finding it already exists](sessions/2026-09-02.md) |
| 2026-09-01 | [eq-solves-service: migration-governance review (task_38071324) closed — DB-first PR split adopted, --reconcile tooling shipped (PR #820)](sessions/2026-09-01.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-09-05 00:57 UTC._
