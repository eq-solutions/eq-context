---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-09-09
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-09-09 18:17 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-09-09 18:09 UTC → 2026-09-09 18:17 UTC)

- Merged: eq-shell [#1870](https://github.com/eq-solutions/eq-shell/pull/1870) Fix crash on outgoing connect requests with a revoked status
- Merged: eq-shell [#1859](https://github.com/eq-solutions/eq-shell/pull/1859) docs(shared): explain the active=false/is_personal overlap i
- Merged: eq-shell [#1858](https://github.com/eq-solutions/eq-shell/pull/1858) feat(staff): backdate signal on conversations, Casual attach
- Merged: eq-shell [#1856](https://github.com/eq-solutions/eq-shell/pull/1856) fix: idempotency guards for 0256/0267 policies + registry ar
- Merged: eq-shell [#1852](https://github.com/eq-solutions/eq-shell/pull/1852) Add Multi screen for group-adding workers
- Merged: eq-shell [#1851](https://github.com/eq-solutions/eq-shell/pull/1851) fix(field-iframe): pause the 30s handoff watchdog while the 
- Merged: eq-shell [#1850](https://github.com/eq-solutions/eq-shell/pull/1850) fix(token-exchange): stop gating a caller's own tenant slug 
- Merged: eq-shell [#1848](https://github.com/eq-solutions/eq-shell/pull/1848) feat(workers): redesign the Add worker screen (follow-up to 
- ⚠ Needs you: 8 → 9 (new items)

## ⚠ Needs you (9)

- 🔴 **CI failure** — eq-solves-service `main`
- 🔴 **CI failure** — eq-solves-intake `main`
- 🔴 **Sentry new error** — `eq-field` [TypeError: Failed to fetch](https://eq-solutions.sentry.io/issues/145909030/)
- 🔴 **Open security finding** — SEC-71 (P1 — deliberate, review 2026-12-04) — Two-factor authentication is switched off for everyone by two hard-coded constan · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F9: Concurrent-session git races corrupt the shared eq-context checkout · possibly recurred in [2026-09-09.md](sessions/2026-09-09.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-09-07.md](sessions/2026-09-07.md) · [failures.md](system/failures.md)
- 🟠 **Sentry new error** — `eq-field` [Error: canon-read: body.tenant_slug fallback used](https://eq-solutions.sentry.io/issues/146010412/)
- 🟠 **Deploy building** — eq-shell (core.eq.solutions)
- 🟠 **Cron failing** — `index-drift.yml` 1 consecutive scheduled run(s) failed, last success 2026-09-08 · [failures.md](system/failures.md) F11

## 🙋 Waiting on you (226)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **eq-shell** · **Not merged or deployed** — waiting on Royce's explicit sign-off (auth-adjacent JWT-minting code; the edit itself was flagged by the Claude Code auto-mode classifier and only applied after explicit confirmation). _(added 2026-09-09)_
- **eq-shell** · **Three §0 items from the same doc explicitly need Royce's call, not spawned:** eq-field's Apprentice-module unrecognized-tenant fallback (item 4), `sites.js`/`managers.js` gating Shell-ownership on the literal string `'sks'` (item 5), and `check-tenant-drift.mjs`'s own fixed 3-project `CANONICAL_PROJECTS` list (item 6) — all deferred pending his input, all in eq-field where 3 other worktrees are already active on adjacent code. _(added 2026-09-09)_
- **eq-shell** · **Dispatch `0311` to madagins via `tenant-migrate.yml`** — merge landed the file; the apply itself is still a separate, not-yet-run dispatch (confirmed via the merge commit's own CI: "Apply to all tenants"/"Reconcile tenant ledgers" both `skipped`). Closes the CMMS-tables gap for real once run. Royce's call on timing. _(added 2026-09-09)_
- **eq-shell** · **`madagins`'s ledger needs correcting before any real apply can succeed on it** — the 314 falsely-stamped rows have to be cleared/reset first, or every future apply attempt will keep trusting them and skipping real work. Not done here — Royce's call on timing/ownership, and who ran the original bootstrap (and why) is still unknown. **Spawned as a background task 2026-09-09** (via pending-items triage) — briefed to re-verify current state first, since the ledger count and eq-field's own schema layer have both moved since this finding. _(added 2026-09-09, spawned 2026-09-09)_
- **eq-shell** · **EQ-SHELL-23 residual** — re-checked live in Sentry as of this restore: issue still `unresolved`/`new`, exactly 1 occurrence (2026-09-08T21:50 UTC), no re-fire since. Silencing it for good needs the jvkn-side shell account/tenant-membership closed too — Royce's call whether that's worth doing; not requested yet. **Spawned as a background task 2026-09-09** (via pending-items triage) — low-risk test-data cleanup, worth doing even without an explicit prior ask. _(added 2026-09-09, restored 2026-09-09, spawned 2026-09-09)_
- **eq-shell** · **Live click-test (2026-09-09) — page verified correct; badge widget itself not visually confirmable with the accounts available.** Royce's own SKS account is Manager-tier (has `documents.assign`), so the nav badge correctly does not render for him — confirmed absent from the sidebar, consistent with the tier gate working as designed, not a defect. Navigating directly to `/sks/admin/documents/mine` (not linked in his nav, but not route-blocked either) shows his own real data correctly: 1 document (SWMS-005), status SIGNED, 0 outstanding — so there's nothing to alert on for his account right now even if the badge were visible to him. Confirming the *positive* case (badge rendering with a real nonzero count) needs either a genuine Viewer-tier account or a moment when a Viewer-tier person has something outstanding — neither available this pass.
- **eq-shell** · **Live click-test (2026-09-09) — CSS confirmed deployed; visual behaviour unconfirmable from this environment; found one real boundary bug.** Confirmed live via `document.styleSheets` inspection on the deployed bundle: 18 media-query blocks matching `(pointer: coarse) and (hover: none) and (width <= 1024px)` OR'd with `(width <= 767px)` are genuinely present across the 4 touched files — the CSS shipped as described. Could not visually trigger it: Claude in Chrome's `resize_window` didn't change this tab's `innerWidth` at all (stayed 1912px regardless of the size requested), and the underlying hardware (Royce's Beelink) has no touch input (`navigator.maxTouchPoints: 0`), so `pointer: coarse` can never be genuinely true there — the same wall a same-day eq-field click-test already hit and documented two sections below (`sessions/2026-09-09.md` ~line 134: "this environment's Browser pane only emulates touch below 768px width"). Independently re-confirmed live rather than assumed from that note. **Real boundary bug found despite the visual block**: the literal rule is `width <= 1024px` — inclusive of exactly 1024px. A real landscape iPad reports exactly 1024px CSS width, so by this rule it would still match the touch condition and get the tablet treatment — contradicting the stated intent (eq-field PR #942's own record: "Landscape iPad (1024–1366px) intentionally out of scope"). If 1024 itself is meant to be excluded, all 4 files need `width < 1024px` (or `<= 1023px`), not `<= 1024px`. Needs an actual iPad or a tool with real device emulation to confirm the visual behaviour; the boundary math doesn't need one.
- **eq-shell** · **Bulk backfill still blocked on Royce** — `scripts/import-sks-manager-lines.mjs` exists (double-gated dry-run/`--apply`, reuses the identity-bridge resolver from `etl-nspbmir-to-ehow.mjs`) but its `parseExport()` shape is provisional — nobody has seen a real export from `SKS_NSW_Org_Chart_Interactive.html`'s own Export function yet. Needs Royce to supply the file; run dry-run first, review the unmatched/ambiguous report with him before `--apply`. _(added 2026-09-07)_
- **eq-shell** · **None of tonight's 4 fixes have been click-tested live by a person** — verified via full test suite + lint + an independent merge-readiness audit only. Worth a real pass once convenient: try resetting a platform_admin's PIN as a regular manager (should 403 `cannot-reset-platform-admin`); try switching tenant on a session that's been logged out/revoked elsewhere (should 401, not succeed).
- **eq-shell** · **#711/SEC-71 — mandatory TOTP enforcement is genuinely client-side only**, reconfirmed live (`shell-login.ts:476-495` issues a full session regardless of the flag). The issue itself says it needs Royce's call on intended grace-period semantics before anyone implements a fix — not built.
- **eq-shell** · **The one piece not done: actually clicking Grant/Revoke platform admin end-to-end.** Deliberately not tested against a real employee — granting or revoking "every permission, in every tenant," even briefly and reversibly, is real enough that it needs either Royce's own hands or a disposable test account named for the purpose. Nobody's pointed at one yet. Full detail on what WAS confirmed live: `sessions/2026-09-05.md`. _(added 2026-08-17, 2026-08-18, 2026-08-25; consolidated 2026-09-05; click-tested 2026-09-05; deferred again 2026-09-07 via `/triage` — still nobody pointed at a disposable test account)_
- **eq-shell** · **3 of the 4 fixes verified only via `tsc -b --force` + eslint + `pnpm test` (including a negative-proof test per fix: fails on the pre-fix code, passes on the fix) — not a real click-through.** Only PR #1760's rate-limit reordering got an end-to-end live check (real HTTP requests against its deploy preview, cross-checked against the live `rate_limit_buckets`/`audit_log` tables). Worth a real pass on the other three: trigger `update_site`/`add_site` with an inactive contact and confirm it's rejected before any write lands; delete a user with linked staff/worker records and confirm the purge stays inside one tenant; open a PR with a deliberately colliding migration prefix and confirm CI fails it. _(added 2026-09-04)_
_…and 214 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 4 | 0d |
| eq-solves-service | ✗ failure | 0d ago | 6 | 4d |
| eq-field | ✓ success | 0d ago | 1 | 0d |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✗ failure | 0d ago | 0 | — |

## Deploys

| Site | State | Last deploy |
|------|-------|-------------|
| eq-shell | building | 2026-09-09 |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-field | [TypeError: Failed to fetch](https://eq-solutions.sentry.io/issues/145909030/) | 13 | 2026-09-09 |
| eq-field | [Error: canon-read: body.tenant_slug fallback used](https://eq-solutions.sentry.io/issues/146010412/) | 9 | 2026-09-09 |
| eq-shell | [EQ Field handoff stalled at "booted" (38s, no 'accepted' yet)](https://eq-solutions.sentry.io/issues/145052767/) | 8 | 2026-09-09 |
| eq-field | [AbortError: Fetch is aborted](https://eq-solutions.sentry.io/issues/143320850/) | 7 | 2026-09-09 |
| eq-shell | [auth-stall: render-crash](https://eq-solutions.sentry.io/issues/140924723/) | 4 | 2026-09-09 |
| eq-field | [TypeError: Load failed](https://eq-solutions.sentry.io/issues/145900945/) | 2 | 2026-09-09 |
| eq-shell | [EQ Field handoff auto-recovery (timeout)](https://eq-solutions.sentry.io/issues/141463602/) | 2 | 2026-09-09 |
| eq-solves-service | [auth handoff: expired](https://eq-solutions.sentry.io/issues/135281279/) | 2 | 2026-09-09 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-09-09 | eq-shell | [#1870](https://github.com/eq-solutions/eq-shell/pull/1870) Fix crash on outgoing connect requests with a revoked status |
| 2026-09-09 | eq-shell | [#1871](https://github.com/eq-solutions/eq-shell/pull/1871) fix(control-plane): mirror liveness off the data plane, not DNS |
| 2026-09-09 | eq-shell | [#1875](https://github.com/eq-solutions/eq-shell/pull/1875) fix(cards): let a worker cancel their own pending access request |
| 2026-09-09 | eq-shell | [#1878](https://github.com/eq-solutions/eq-shell/pull/1878) fix(security): close 2 more RLS gaps found while checking tender_ |
| 2026-09-09 | eq-shell | [#1877](https://github.com/eq-solutions/eq-shell/pull/1877) chore(deps): bump @eq-solutions/ui to v1.16.5 |
| 2026-09-09 | eq-shell | [#1876](https://github.com/eq-solutions/eq-shell/pull/1876) fix(documents): warm push-document-audience's tenant-client cache |
| 2026-09-09 | eq-shell | [#1873](https://github.com/eq-solutions/eq-shell/pull/1873) Make Multi the Add-workers homepage, fold agency links into uploa |
| 2026-09-09 | eq-shell | [#1867](https://github.com/eq-solutions/eq-shell/pull/1867) feat(mobile): add workspace switcher to the mobile account sheet |
| 2026-09-09 | eq-shell | [#1869](https://github.com/eq-solutions/eq-shell/pull/1869) docs(onboard): catch the runbook up to step 6 + --field-hostname |
| 2026-09-09 | eq-shell | [#1865](https://github.com/eq-solutions/eq-shell/pull/1865) Rebuild Add worker to the Claude Design spec |
| 2026-09-09 | eq-shell | [#1866](https://github.com/eq-solutions/eq-shell/pull/1866) fix(security): add authenticated read policy for zaap's organisat |
| 2026-09-09 | eq-shell | [#1864](https://github.com/eq-solutions/eq-shell/pull/1864) fix(documents): actually stop clipping the "..." menu (#1828 didn |
| 2026-09-09 | eq-shell | [#1863](https://github.com/eq-solutions/eq-shell/pull/1863) fix(security): add missing tenant-scoped RLS policies on zaap's t |
| 2026-09-09 | eq-shell | [#1862](https://github.com/eq-solutions/eq-shell/pull/1862) fix(onboard): stop stamping a guessed EQ Field hostname by defaul |
| 2026-09-09 | eq-shell | [#1861](https://github.com/eq-solutions/eq-shell/pull/1861) chore(intake): auto re-vendor eq-intake/eq-platform |
_Showing 15 of 83 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-shell** (293 open) · [eq/pending/eq-shell.md](eq/pending/eq-shell.md)
- **eq-cards** (65 open) · [eq/pending/eq-cards.md](eq/pending/eq-cards.md)
- **eq-field** (233 open) · [eq/pending/eq-field.md](eq/pending/eq-field.md)
- **eq-solves-service** (70 open) · [eq/pending/eq-solves-service.md](eq/pending/eq-solves-service.md)
- **eq-solves-intake** (20 open) · [eq/pending/eq-solves-intake.md](eq/pending/eq-solves-intake.md)
- **eq-design-tokens** (1 open) · [eq/pending/eq-design-tokens.md](eq/pending/eq-design-tokens.md)
- **eq-ui** (2 open) · [eq/pending/eq-ui.md](eq/pending/eq-ui.md)
- **eq-receipts** (4 open) · [eq/pending/eq-receipts.md](eq/pending/eq-receipts.md)
- **eq-context** (41 open) · [eq/pending/eq-context.md](eq/pending/eq-context.md)
- **cross-repo** (178 open) · [eq/pending/cross-repo.md](eq/pending/cross-repo.md)
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
| [eq-shell](eq/pending/eq-shell.md) | 1733 | 230 / 64 | 20 | 78 |
| [eq-cards](eq/pending/eq-cards.md) | 365 | 48 / 17 | 0 | 8 |
| [eq-field](eq/pending/eq-field.md) | 1356 | 195 / 40 | 38 | 48 |
| [eq-solves-service](eq/pending/eq-solves-service.md) | 403 | 51 / 20 | 2 | 20 |
| [eq-solves-intake](eq/pending/eq-solves-intake.md) | 182 | 14 / 6 | 2 | 17 |
| [eq-design-tokens](eq/pending/eq-design-tokens.md) | 25 | 1 / 0 | 0 | 1 |
| [eq-ui](eq/pending/eq-ui.md) | 24 | 2 / 0 | 0 | 0 |
| [eq-receipts](eq/pending/eq-receipts.md) | 46 | 3 / 1 | 0 | 3 |
| [eq-context](eq/pending/eq-context.md) | 242 | 29 / 12 | 1 | 9 |
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
| 2026-09-10 | [F14's signal regex restructured (directional bug fix, pending.md/substrate anchors dropped); completes the F1/F9-adjacent precision pass started 2026-09-09](sessions/2026-09-10.md) |
| 2026-09-09 | [guard.js worktree-naming gap closed (rules 1/1b/1c/10, `-wt-` infix)](sessions/2026-09-09.md) |
| 2026-09-08 | [Customers/Staff/Equipment gained their own URL; 3 PRs merged + live (work done 2026-09-07, closed after midnight)](sessions/2026-09-08.md) |
| 2026-09-07 | [Labour-hire licence-photo fix re-verified live; full roster audited, no other worker exposed](sessions/2026-09-07.md) |
| 2026-09-06 | [Resumed and shipped the `?tenant=demo` fix, caught two more bugs in the same class before merge](sessions/2026-09-06.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-09-09 18:17 UTC._
