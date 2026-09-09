---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-09-09
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-09-09 10:45 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-09-09 10:43 UTC → 2026-09-09 10:45 UTC)

- Merged: eq-shell [#1848](https://github.com/eq-solutions/eq-shell/pull/1848) feat(workers): redesign the Add worker screen (follow-up to 
- Merged: eq-shell [#1830](https://github.com/eq-solutions/eq-shell/pull/1830) test(staff): add coverage for staff-resourcing's pure rollup
- Merged: eq-shell [#1829](https://github.com/eq-solutions/eq-shell/pull/1829) fix(schema): add app_data.sites.deleted_at, missing on every
- Merged: eq-shell [#1825](https://github.com/eq-solutions/eq-shell/pull/1825) feat(documents): add an outstanding-count badge to My docume
- Merged: eq-shell [#1824](https://github.com/eq-solutions/eq-shell/pull/1824) feat(staff): let a conversation carry a reminder date
- Merged: eq-shell [#1697](https://github.com/eq-solutions/eq-shell/pull/1697) chore(deps): bump unpdf from 0.12.1 to 0.12.2
- Merged: eq-field [#968](https://github.com/eq-solutions/eq-field/pull/968) fix: fold pg_net extension check into tenant-provision gener
- Merged: eq-field [#967](https://github.com/eq-solutions/eq-field/pull/967) feat: auto-create the ~18-object prerequisite block for new-

## ⚠ Needs you (7)

- 🔴 **Open security finding** — SEC-71 (P1 — deliberate, review 2026-12-04) — Two-factor authentication is switched off for everyone by two hard-coded constan · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-08-23.md](sessions/2026-08-23.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F9: Concurrent-session git races corrupt the shared eq-context checkout · possibly recurred in [2026-09-09.md](sessions/2026-09-09.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F12: Side-clone reconciliation blind-overwrote a concurrent session's already-pushed shared-fil · possibly recurred in [2026-08-30.md](sessions/2026-08-30.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-09-09.md](sessions/2026-09-09.md) · [failures.md](system/failures.md)
- 🟠 **Sentry new error** — `eq-field` [TypeError: Failed to fetch](https://eq-solutions.sentry.io/issues/145909030/)
- 🟠 **Deploy new** — eq-shell (core.eq.solutions)

## 🙋 Waiting on you (224)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **eq-shell** · **Not merged or deployed** — waiting on Royce's explicit sign-off (auth-adjacent JWT-minting code; the edit itself was flagged by the Claude Code auto-mode classifier and only applied after explicit confirmation). _(added 2026-09-09)_
- **eq-shell** · **Three §0 items from the same doc explicitly need Royce's call, not spawned:** eq-field's Apprentice-module unrecognized-tenant fallback (item 4), `sites.js`/`managers.js` gating Shell-ownership on the literal string `'sks'` (item 5), and `check-tenant-drift.mjs`'s own fixed 3-project `CANONICAL_PROJECTS` list (item 6) — all deferred pending his input, all in eq-field where 3 other worktrees are already active on adjacent code. _(added 2026-09-09)_
- **eq-shell** · **`madagins`'s ledger needs correcting before any real apply can succeed on it** — the 314 falsely-stamped rows have to be cleared/reset first, or every future apply attempt will keep trusting them and skipping real work. Not done here — Royce's call on timing/ownership, and who ran the original bootstrap (and why) is still unknown. **Spawned as a background task 2026-09-09** (via pending-items triage) — briefed to re-verify current state first, since the ledger count and eq-field's own schema layer have both moved since this finding. _(added 2026-09-09, spawned 2026-09-09)_
- **eq-shell** · **EQ-SHELL-23 residual** — re-checked live in Sentry as of this restore: issue still `unresolved`/`new`, exactly 1 occurrence (2026-09-08T21:50 UTC), no re-fire since. Silencing it for good needs the jvkn-side shell account/tenant-membership closed too — Royce's call whether that's worth doing; not requested yet. **Spawned as a background task 2026-09-09** (via pending-items triage) — low-risk test-data cleanup, worth doing even without an explicit prior ask. _(added 2026-09-09, restored 2026-09-09, spawned 2026-09-09)_
- **eq-shell** · **The structural gap itself is still open** — every future Dependabot PR in this repo will hit the identical `SUPABASE_ACCESS_TOKEN` failure and need the same admin-override, until one of: (a) grant the token to Dependabot secrets (security trade-off, declined for now), or (b) change the workflow to skip this check gracefully when triggered by Dependabot AND the diff touches no schema-relevant files. Neither built — Royce's call which way, if either. **Spawned as a background task 2026-09-09** (via pending-items triage) building option (b), since (a) was already declined. _(added 2026-09-09, spawned 2026-09-09)_
- **eq-shell** · **Bulk backfill still blocked on Royce** — `scripts/import-sks-manager-lines.mjs` exists (double-gated dry-run/`--apply`, reuses the identity-bridge resolver from `etl-nspbmir-to-ehow.mjs`) but its `parseExport()` shape is provisional — nobody has seen a real export from `SKS_NSW_Org_Chart_Interactive.html`'s own Export function yet. Needs Royce to supply the file; run dry-run first, review the unmatched/ambiguous report with him before `--apply`. _(added 2026-09-07)_
- **eq-shell** · **None of tonight's 4 fixes have been click-tested live by a person** — verified via full test suite + lint + an independent merge-readiness audit only. Worth a real pass once convenient: try resetting a platform_admin's PIN as a regular manager (should 403 `cannot-reset-platform-admin`); try switching tenant on a session that's been logged out/revoked elsewhere (should 401, not succeed).
- **eq-shell** · **#711/SEC-71 — mandatory TOTP enforcement is genuinely client-side only**, reconfirmed live (`shell-login.ts:476-495` issues a full session regardless of the flag). The issue itself says it needs Royce's call on intended grace-period semantics before anyone implements a fix — not built.
- **eq-shell** · **The one piece not done: actually clicking Grant/Revoke platform admin end-to-end.** Deliberately not tested against a real employee — granting or revoking "every permission, in every tenant," even briefly and reversibly, is real enough that it needs either Royce's own hands or a disposable test account named for the purpose. Nobody's pointed at one yet. Full detail on what WAS confirmed live: `sessions/2026-09-05.md`. _(added 2026-08-17, 2026-08-18, 2026-08-25; consolidated 2026-09-05; click-tested 2026-09-05; deferred again 2026-09-07 via `/triage` — still nobody pointed at a disposable test account)_
- **eq-shell** · **3 of the 4 fixes verified only via `tsc -b --force` + eslint + `pnpm test` (including a negative-proof test per fix: fails on the pre-fix code, passes on the fix) — not a real click-through.** Only PR #1760's rate-limit reordering got an end-to-end live check (real HTTP requests against its deploy preview, cross-checked against the live `rate_limit_buckets`/`audit_log` tables). Worth a real pass on the other three: trigger `update_site`/`add_site` with an inactive contact and confirm it's rejected before any write lands; delete a user with linked staff/worker records and confirm the purge stays inside one tenant; open a PR with a deliberately colliding migration prefix and confirm CI fails it. _(added 2026-09-04)_
- **eq-shell** · **3 directories left on disk, OS-locked, not deletable from this session** — `git worktree remove` unregistered them from git (2 errored "Result too large" but still unregistered; 1 confirmed via `git worktree prune`), but the physical folders survived both `Remove-Item -Force` and `rm -rf` ~10 minutes apart, both failing with "device or resource busy" / "being used by another process." Locking process not identified (`Get-CimInstance Win32_Process` showed nothing obviously relevant). Needs Royce to close whatever has them open (or a reboot) before they're actually reclaimable: `.claude\worktrees\contact-auto-site-ops-download-325f25`, `.claude\worktrees\list-user-invites-existing-user-filter`, `.claude\worktrees\simplified-interface-users-764a0d`. _(added 2026-09-01)_
- **eq-shell** · **SEC-67's env-var half still needs Royce** — 4 confirmed-dead Netlify env vars (`FIELD_SUPABASE_URL`/`_SERVICE_ROLE_KEY`, `NEXT_PUBLIC_SUPABASE_URL`/`_ANON_KEY`), zero code references, ready to delete — blocked by Claude Code's own classifier on unattended env-var writes. Commands in `sessions/2026-08-30.md`. _(added 2026-08-30)_
_…and 212 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 5 | 0d |
| eq-solves-service | ✓ success | 0d ago | 8 | 4d |
| eq-field | ✓ success | 0d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 2 | 0d |
| eq-solves-intake | ✓ success | 1d ago | 0 | — |

## Deploys

| Site | State | Last deploy |
|------|-------|-------------|
| eq-shell | new | 2026-09-09 |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [EQ Field handoff stalled at "booted" (38s, no 'accepted' yet)](https://eq-solutions.sentry.io/issues/145052767/) | 8 | 2026-09-09 |
| eq-field | [AbortError: Fetch is aborted](https://eq-solutions.sentry.io/issues/143320850/) | 7 | 2026-09-09 |
| eq-field | [TypeError: Failed to fetch](https://eq-solutions.sentry.io/issues/145909030/) | 5 | 2026-09-09 |
| eq-shell | [EQ Field handoff auto-recovery (timeout)](https://eq-solutions.sentry.io/issues/141463602/) | 2 | 2026-09-09 |
| eq-solves-service | [auth handoff: expired](https://eq-solutions.sentry.io/issues/135281279/) | 2 | 2026-09-09 |
| eq-cards | [minified:B2: AuthRetryableFetchException(message: ClientException: Failed to fet](https://eq-solutions.sentry.io/issues/144338444/) | 2 | 2026-09-08 |
| eq-field | [Error: Setting up fake worker failed: "undefined is not an object (evaluating 'W](https://eq-solutions.sentry.io/issues/145901414/) | 1 | 2026-09-09 |
| eq-field | [TypeError: Load failed](https://eq-solutions.sentry.io/issues/145900945/) | 1 | 2026-09-09 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-09-09 | eq-shell | [#1848](https://github.com/eq-solutions/eq-shell/pull/1848) feat(workers): redesign the Add worker screen (follow-up to #1844 |
| 2026-09-09 | eq-shell | [#1849](https://github.com/eq-solutions/eq-shell/pull/1849) fix(migrations): scope 0311 to ehow only |
| 2026-09-09 | eq-shell | [#1847](https://github.com/eq-solutions/eq-shell/pull/1847) fix(entitlements): allowlist modules in upsertAppEntitlements |
| 2026-09-09 | eq-shell | [#1845](https://github.com/eq-solutions/eq-shell/pull/1845) fix(migrations): add missing UNIQUE constraint on licences.cards_ |
| 2026-09-09 | eq-shell | [#1842](https://github.com/eq-solutions/eq-shell/pull/1842) fix(provisioning): recover and land the app_data legacy-baseline  |
| 2026-09-09 | eq-shell | [#1840](https://github.com/eq-solutions/eq-shell/pull/1840) fix(dev): allow Vite's React-refresh preamble under the CSP |
| 2026-09-09 | eq-shell | [#1844](https://github.com/eq-solutions/eq-shell/pull/1844) feat(workers): merge Invite worker + Connect existing into one do |
| 2026-09-09 | eq-shell | [#1843](https://github.com/eq-solutions/eq-shell/pull/1843) fix(migrations): guard 0257's REVOKE against a from-scratch tenan |
| 2026-09-09 | eq-shell | [#1841](https://github.com/eq-solutions/eq-shell/pull/1841) docs(env): document VITE_FIELD_URL, the one undocumented required |
| 2026-09-09 | eq-shell | [#1839](https://github.com/eq-solutions/eq-shell/pull/1839) fix(control-plane): keep tenants mirrored from organisations, bac |
| 2026-09-09 | eq-shell | [#1838](https://github.com/eq-solutions/eq-shell/pull/1838) fix(field): add madagins to the Field tenant allowlist + picker |
| 2026-09-09 | eq-shell | [#1837](https://github.com/eq-solutions/eq-shell/pull/1837) fix(sidebar): open workspace switcher menu upward, not down off-s |
| 2026-09-09 | eq-shell | [#1835](https://github.com/eq-solutions/eq-shell/pull/1835) fix(security): enable RLS on app_data._eq_migrations (all tenant  |
| 2026-09-09 | eq-shell | [#1834](https://github.com/eq-solutions/eq-shell/pull/1834) fix(provisioning): enable pg_cron on new tenant projects |
| 2026-09-09 | eq-shell | [#1833](https://github.com/eq-solutions/eq-shell/pull/1833) fix(security): enable RLS on 4 dead wipe_backup tables (ehow) |
_Showing 15 of 78 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-shell** (282 open) · [eq/pending/eq-shell.md](eq/pending/eq-shell.md)
- **eq-cards** (63 open) · [eq/pending/eq-cards.md](eq/pending/eq-cards.md)
- **eq-field** (225 open) · [eq/pending/eq-field.md](eq/pending/eq-field.md)
- **eq-solves-service** (71 open) · [eq/pending/eq-solves-service.md](eq/pending/eq-solves-service.md)
- **eq-solves-intake** (19 open) · [eq/pending/eq-solves-intake.md](eq/pending/eq-solves-intake.md)
- **eq-design-tokens** (1 open) · [eq/pending/eq-design-tokens.md](eq/pending/eq-design-tokens.md)
- **eq-ui** (2 open) · [eq/pending/eq-ui.md](eq/pending/eq-ui.md)
- **eq-receipts** (4 open) · [eq/pending/eq-receipts.md](eq/pending/eq-receipts.md)
- **eq-context** (43 open) · [eq/pending/eq-context.md](eq/pending/eq-context.md)
- **cross-repo** (180 open) · [eq/pending/cross-repo.md](eq/pending/cross-repo.md)
- **sks** (8 open) · [eq/pending/sks.md](eq/pending/sks.md)

## Pending (SKS)

- **Rhys Scott + Wayne Rowe may need a `team_supervisors` row too, not just `team_members`** — both now flagged `is_supervisor=true` on `app_data.staff`, matching the "player-coach" pattern already live for David Boyd/Amazon Syd 53, John Angangan/Comms+Vans, Matthew Miller & Simon Bramall/Equinix+Vans. Needs Collin to confirm which team each actually runs. _(added 2026-09-09)_
- **Cam has nothing rostered Nov 23–27 now** — the leave that covered those days is gone, but nobody re-rostered him to a site. If he's meant to be working, needs an actual roster entry. _(added 2026-09-09)_
- **The anon-CRUD/secrets-exposure vulnerability from 2026-07-20 (below) is still fully open — explicitly NOT fixed this session, Royce's deliberate call after being told it doesn't go away on its own.** Confirmed live: `app_config`'s exposed `canonical_api_key_field` is a bearer token for `core.eq.solutions/.netlify/functions/canonical-api` (the ACTIVE Shell/Field system, not the retiring app) and `digest_fn_token` is seeded as a raw Supabase service-role JWT for nspbmir itself — both readable by anyone with the still-public, still-served anon key, regardless of the app's retirement status. The zero-risk, no-soak Step 0 patch (`~/.claude/plans/nspbmir-EMERGENCY-anon-select-narrowing.sql`) remains un-run. Royce was walked through the distinction (token exposure into the *active* system ≠ the retiring app's own roster data) and chose to stop spending time on this repo entirely rather than run even the isolated Step 0 fix. His call to make; flagging plainly so nobody assumes this was closed out. _(added 2026-09-07)_
- **Cross-reference: "Track 2 RLS STEP 2" (anon SELECT lockdown on ehow, further down this file) was deferred "until standalone retired."** Ops has moved off sks-nsw-labour as of today, even though the app/DB itself is still technically live (archived repo, active DB, no hard redirect). Worth whoever picks up ehow RLS work checking whether that's enough to count as "retired" for that gate, rather than assuming either way. _(added 2026-09-07)_
- **Affects 45 of 81 active SKS staff** (everyone Cards-linked with no wizard-entered full date of birth) — fixed going forward, but nobody's birthday has actually been re-entered yet. No action needed unless Royce wants a nudge to re-save. Most should self-resolve as people go through Cards' own licence-scan step, which fills a real date of birth in automatically. _(added 2026-08-24)_
- **Aiden's own birthday (18 Feb) was tested then reverted to blank** — unclear if that's his real date or just what was typed while reproducing the bug; needs a real re-save to confirm either way. Separately, his record still carries the *earlier* session's own trial data (job title, emergency contact, start date) that was meant to be trial-then-undo and never was — untouched by this session, still open. _(added 2026-08-24)_
- **A second, unidentified path also creates blank-name logins** — proven by timing, not guessed: Todd Wilson's and David Boyd's shell logins were created 7 weeks *after* their Cards approval, which rules out the path just patched as their cause. Spawned as background task `task_d904d388`, Royce started it in a separate session; running independently, not yet reported back as of this session's close. _(added 2026-08-23)_
- **Not verified live by a person** — the specific pill-click behavior needs a real Core+SKS session to exercise (Teams is SKS-only, gated behind Core auth, not reachable from a standalone deploy-preview session). Confirmed the fix mirrors an already-shipped, working code pattern (the crew-supervisor picker), not watched working fresh. _(added 2026-08-23)_
- **SKS's own number, for reference: 6 of 32 active SKS members are currently missing White Card** — visible today in Shell's Training Matrix; nothing blocks them from working while missing it (soft-flag by design, not an oversight). Worth a look if Royce wants a harder rule for SKS specifically. _(added 2026-08-19)_
- **A reported roster-grid "alignment" issue (one person's row looked off) couldn't be reproduced from the code** — most likely just placeholder text in blank cells reading like real data at a glance, not an actual bug, but left open rather than guessed at. _(added 2026-08-19)_
_…and 85 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise. Open splits engineering backlog from Royce's own queue (a confirm, a click-through, a call) — the two used to be counted together here, which made the number look worse than the real engineering backlog actually is; the split matches 'Waiting on you' above._

| File | Lines | Open (eng / you) | Done (unrotated) | Aging 45d+ |
|------|------:|------------------:|------------------:|------------:|
| [eq-shell](eq/pending/eq-shell.md) | 1659 | 228 / 63 | 5 | 78 |
| [eq-cards](eq/pending/eq-cards.md) | 348 | 47 / 16 | 0 | 8 |
| [eq-field](eq/pending/eq-field.md) | 1304 | 187 / 40 | 35 | 48 |
| [eq-solves-service](eq/pending/eq-solves-service.md) | 412 | 51 / 21 | 3 | 20 |
| [eq-solves-intake](eq/pending/eq-solves-intake.md) | 164 | 13 / 6 | 2 | 17 |
| [eq-design-tokens](eq/pending/eq-design-tokens.md) | 25 | 1 / 0 | 0 | 1 |
| [eq-ui](eq/pending/eq-ui.md) | 24 | 2 / 0 | 0 | 0 |
| [eq-receipts](eq/pending/eq-receipts.md) | 46 | 3 / 1 | 0 | 3 |
| [eq-context](eq/pending/eq-context.md) | 251 | 31 / 12 | 1 | 9 |
| [cross-repo](eq/pending/cross-repo.md) | 943 | 134 / 46 | 3 | 77 |
| [sks](eq/pending/sks.md) | 55 | 3 / 5 | 0 | 6 |
| [SKS](sks/pending.md) | 515 | 95 / 15 | 0 | 62 |
| [SKS active](sks/active.md) | 119 | 0 / 0 | 0 | 0 |
| [OPS](ops/pending.md) | 627 | 52 / 3 | 1 | 13 |

## Aging open items (45d+, unconfirmed)

_Open items sitting under a section header this old or older — not necessarily wrong, just gone quiet under its own dated write-up. Worth a look before it reads as done-and-forgotten._

- **eq-shell** (2026-07-24) · **What's the actual remaining pain point for direct employees, now that the Cards→Field pipe is confirmed live end-to-end?** Asked Royce directly — is it that head office doesn't trust/re-checks Field data before their manual Upvise upload, or a different gap not yet found. Not answered yet this session. _(added 2026-07-24)_
- **eq-shell** (2026-07-24) · **An automatic check is scheduled for the morning of 2026-07-25 to confirm the fix actually held overnight** — will look at the 5 originally-reported people directly, check for any suspicious mass-reactivation pattern across staff generally, and report back. Not yet confirmed by Royce himself. _(added 2026-07-24)_
- **eq-shell** (2026-07-24) · **`eq_reconcile_worker_sync()` (the nightly dispatcher itself, jvkn `pg_cron` job id 2) still isn't tracked in any repo migration** — a governance gap independent of the bug above, not touched by this fix. Not urgent now that the harmful write is gone, but worth bringing under the normal migration pipeline at some point. _(added 2026-07-24)_
- **eq-shell** (2026-07-24) · **Not yet click-tested against the newest version** — the tick/cross feedback and the job title column are live, but nobody has run a fresh file through *this* version of the screen yet. _(added 2026-07-24)_
- **eq-shell** (2026-07-24) · **A second, older bookkeeping mismatch of the same kind (two database updates sharing one tracking number, from an earlier session) is still sitting there unresolved** — spotted in passing while fixing the pair above, deliberately left untouched since it wasn't part of what Royce asked for this time. Same fix pattern would apply. _(added 2026-07-24)_
- **eq-shell** (2026-07-23) · **Royce hasn't yet re-pulled a fresh export to eyeball the fixed cells himself** — the fix was confirmed via direct RPC call, not a real export download; he asked for this exact check but got redirected before it happened. _(added 2026-07-26)_ **Checked 2026-09-07 via `/triage`: still genuinely needs Royce's own eyes on a real download — that's the whole point, a second automated check wouldn't satisfy it. No live Shell session in this environment to pull one on his behalf either. Where to do it: open the quote in Job Creation and export — server-side generator is `eq-shell/netlify/functions/job-creation.ts`. Still open.**
- **eq-shell** (2026-07-23) · **The tripwire fix eq-solves-service got today (see that entry below) hasn't been built for eq-shell, and eq-shell needs it too.** This session's assigned private folder had nothing in it — ended up doing all its real work in the one shared master copy instead, same mechanism as eq-solves-service's bug. Confirmed live mid-session: a second, unrelated concurrent session's own work-in-progress (a database list-loading improvement) was sitting there uncommitted where this session could see it, and that session's own folder-switch changed what this session was pointed at partway through, without warning. Nothing was lost either time — caught before anything got mixed up — but it's luck, not a safeguard. _(added 2026-07-23)_
- **eq-shell** (2026-07-21) · **Worth a quick look once deployed:** confirm the Company field shows/saves correctly for Labour Hire and Subcontractor (desktop + mobile), and re-export SKS-17386 to confirm Clarifications now sits left-aligned without needing a manual fix in Word. _(added 2026-07-21)_ **Checked 2026-09-07 via `/triage`: same blocker as the rest of this bucket — no live Shell session in this environment for either the UI click-test or the SKS-17386 doc re-export (`quoteDocGenerator.ts` needs an authed session). Still open; needs a real Shell sign-in to close out.**
- **eq-shell** (2026-07-21) · **The third — a simple "how sure are we this credential is real" label on licences — is deliberately parked**, not forgotten: Royce's 90/10 decision (90% on the SKS career, company-scale Cards parked) puts this on the wrong side of the line, since it's a cross-company trust signal SKS's own onboarding doesn't need. Revisit only if the company-scale question reopens. Full detail in the audit doc (`eq-context/eq/cards/portable-trade-identity-audit-2026-07-20.md`). _(added 2026-07-21)_
- **eq-shell** (2026-07-19) · **Still open, not urgent:** the exact reason EQ Field was slow to load for that one person on 2026-07-19 is unconfirmed — likely just a poor connection, but couldn't fully rule out anything worse. Nothing else has reported it since. _(added 2026-07-19)_
- **eq-shell** (2026-07-17) · **Deferred: who should get the weekly summary email?** Built and ready, just needs a recipient list from Royce before it's switched on. _(added 2026-07-17)_
- **eq-shell** (2026-07-17) · **Declined for now (Royce's call): a personal calendar feed per crew member, and a weather warning near Microsoft dock dates.** Offered as options alongside the above; not built. _(added 2026-07-17)_
- **eq-shell** (2026-07-16) · **Deferred: bigger first-load speedup** — breaking one large file into smaller pieces that only load when needed. Real win, but a bigger change that needs a hands-on check, not just automated tests. _(added 2026-07-19)_
- **eq-shell** (2026-07-16) · **Deferred: extend the "you'll lose this" warning** to other forms — site details, invites, admin settings. Currently only on quotes. _(added 2026-07-19)_
- **eq-shell** (2026-07-16) · **Deferred: make long lists load a page at a time** instead of everything at once (quotes, comms roster, staff, customers). _(added 2026-07-19)_
_…and 327 more — see each file's Queue health row above._

## Possible recurring failures (unconfirmed)

_Session logs mention a pattern matching a known failure below, dated after its last recorded occurrence. Not yet counted — if it's real, bump `recurrences` in [failures.md](system/failures.md) and `guard-ratchet.yml` proposes promotion on its own next run._

- **F5** (rung 0) — An ungoverned shadow memory overrode the canonical contract · 1 session since last recorded, most recent [2026-08-16.md](sessions/2026-08-16.md)

## Recent sessions

| Date | Session |
|------|---------|
| 2026-09-09 | [guard.js worktree-naming gap closed (rules 1/1b/1c/10, `-wt-` infix)](sessions/2026-09-09.md) |
| 2026-09-08 | [Customers/Staff/Equipment gained their own URL; 3 PRs merged + live (work done 2026-09-07, closed after midnight)](sessions/2026-09-08.md) |
| 2026-09-07 | [Labour-hire licence-photo fix re-verified live; full roster audited, no other worker exposed](sessions/2026-09-07.md) |
| 2026-09-06 | [Resumed and shipped the `?tenant=demo` fix, caught two more bugs in the same class before merge](sessions/2026-09-06.md) |
| 2026-09-05 | [SEC-53 verified live, closed in the register, and merged](sessions/2026-09-05.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-09-09 10:45 UTC._
