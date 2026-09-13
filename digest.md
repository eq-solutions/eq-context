---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-09-13
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-09-13 07:13 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-09-13 07:04 UTC → 2026-09-13 07:13 UTC)

- Merged: eq-shell [#1878](https://github.com/eq-solutions/eq-shell/pull/1878) fix(security): close 2 more RLS gaps found while checking te
- Merged: eq-shell [#1876](https://github.com/eq-solutions/eq-shell/pull/1876) fix(documents): warm push-document-audience's tenant-client 
- Merged: eq-shell [#1871](https://github.com/eq-solutions/eq-shell/pull/1871) fix(control-plane): mirror liveness off the data plane, not 
- Merged: eq-shell [#1867](https://github.com/eq-solutions/eq-shell/pull/1867) feat(mobile): add workspace switcher to the mobile account s
- Merged: eq-shell [#1865](https://github.com/eq-solutions/eq-shell/pull/1865) Rebuild Add worker to the Claude Design spec
- Merged: eq-shell [#1864](https://github.com/eq-solutions/eq-shell/pull/1864) fix(documents): actually stop clipping the "..." menu (#1828
- Merged: eq-shell [#1862](https://github.com/eq-solutions/eq-shell/pull/1862) fix(onboard): stop stamping a guessed EQ Field hostname by d
- Merged: eq-shell [#1860](https://github.com/eq-solutions/eq-shell/pull/1860) fix(admin): add Madagins to the Field workspace dropdown
- ✅ Needs you: 8 → 7

## ⚠ Needs you (7)

- 🔴 **CI failure** — eq-solves-intake `main`
- 🔴 **Open security finding** — SEC-71 (P1 — deliberate, review 2026-12-04) — Two-factor authentication is switched off for everyone by two hard-coded constan · [security-register.md](ops/security-register.md)
- 🔴 **Cron failing** — `index-drift.yml` 4 consecutive scheduled run(s) failed, last success 2026-09-08 · [failures.md](system/failures.md) F11
- 🔴 **Cron failing** — `shared-object-drift.yml` 3 consecutive scheduled run(s) failed, last success 2026-09-09 · [failures.md](system/failures.md) F11
- 🔴 **Guard bypass? rung 4** — F9: Concurrent-session git races corrupt the shared eq-context checkout · possibly recurred in [2026-09-09.md](sessions/2026-09-09.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-09-07.md](sessions/2026-09-07.md) · [failures.md](system/failures.md)
- 🟠 **PR aging 8d** — eq-solves-service [#829](https://github.com/eq-solutions/eq-service/pull/829) "fix(defects): consolidate raise-defect duplication, close ACB/NSX vali"

## 🙋 Waiting on you (226)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **eq-shell** · **Not merged or deployed** — waiting on Royce's explicit sign-off (auth-adjacent JWT-minting code; the edit itself was flagged by the Claude Code auto-mode classifier and only applied after explicit confirmation). _(added 2026-09-09)_
- **eq-shell** · **Three §0 items from the same doc explicitly need Royce's call, not spawned:** eq-field's Apprentice-module unrecognized-tenant fallback (item 4), `sites.js`/`managers.js` gating Shell-ownership on the literal string `'sks'` (item 5), and `check-tenant-drift.mjs`'s own fixed 3-project `CANONICAL_PROJECTS` list (item 6) — all deferred pending his input, all in eq-field where 3 other worktrees are already active on adjacent code. _(added 2026-09-09)_
- **eq-shell** · **Dispatch `0311` to madagins via `tenant-migrate.yml`** — merge landed the file; the apply itself is still a separate, not-yet-run dispatch (confirmed via the merge commit's own CI: "Apply to all tenants"/"Reconcile tenant ledgers" both `skipped`). Closes the CMMS-tables gap for real once run. Royce's call on timing. _(added 2026-09-09)_
- **eq-shell** · **`madagins`'s ledger needs correcting before any real apply can succeed on it** — the 314 falsely-stamped rows have to be cleared/reset first, or every future apply attempt will keep trusting them and skipping real work. Not done here — Royce's call on timing/ownership, and who ran the original bootstrap (and why) is still unknown. **Spawned as a background task 2026-09-09** (via pending-items triage) — briefed to re-verify current state first, since the ledger count and eq-field's own schema layer have both moved since this finding. _(added 2026-09-09, spawned 2026-09-09)_
- **eq-shell** · **EQ-SHELL-23 residual** — re-checked live in Sentry as of this restore: issue still `unresolved`/`new`, exactly 1 occurrence (2026-09-08T21:50 UTC), no re-fire since. Silencing it for good needs the jvkn-side shell account/tenant-membership closed too — Royce's call whether that's worth doing; not requested yet. **Spawned as a background task 2026-09-09** (via pending-items triage) — low-risk test-data cleanup, worth doing even without an explicit prior ask. _(added 2026-09-09, restored 2026-09-09, spawned 2026-09-09)_
- **eq-shell** · **Live click-test (2026-09-09) — CSS confirmed deployed; visual behaviour unconfirmable from this environment; found one real boundary bug.** Confirmed live via `document.styleSheets` inspection on the deployed bundle: 18 media-query blocks matching `(pointer: coarse) and (hover: none) and (width <= 1024px)` OR'd with `(width <= 767px)` are genuinely present across the 4 touched files — the CSS shipped as described. Could not visually trigger it: Claude in Chrome's `resize_window` didn't change this tab's `innerWidth` at all (stayed 1912px regardless of the size requested), and the underlying hardware (Royce's Beelink) has no touch input (`navigator.maxTouchPoints: 0`), so `pointer: coarse` can never be genuinely true there — the same wall a same-day eq-field click-test already hit and documented two sections below (`sessions/2026-09-09.md` ~line 134: "this environment's Browser pane only emulates touch below 768px width"). Independently re-confirmed live rather than assumed from that note. **Real boundary bug found despite the visual block**: the literal rule is `width <= 1024px` — inclusive of exactly 1024px. A real landscape iPad reports exactly 1024px CSS width, so by this rule it would still match the touch condition and get the tablet treatment — contradicting the stated intent (eq-field PR #942's own record: "Landscape iPad (1024–1366px) intentionally out of scope"). If 1024 itself is meant to be excluded, all 4 files need `width < 1024px` (or `<= 1023px`), not `<= 1024px`. Needs an actual iPad or a tool with real device emulation to confirm the visual behaviour; the boundary math doesn't need one.
- **eq-shell** · **Bulk backfill still blocked on Royce** — `scripts/import-sks-manager-lines.mjs` exists (double-gated dry-run/`--apply`, reuses the identity-bridge resolver from `etl-nspbmir-to-ehow.mjs`) but its `parseExport()` shape is provisional — nobody has seen a real export from `SKS_NSW_Org_Chart_Interactive.html`'s own Export function yet. Needs Royce to supply the file; run dry-run first, review the unmatched/ambiguous report with him before `--apply`. _(added 2026-09-07)_
- **eq-shell** · **None of tonight's 4 fixes have been click-tested live by a person** — verified via full test suite + lint + an independent merge-readiness audit only. Worth a real pass once convenient: try resetting a platform_admin's PIN as a regular manager (should 403 `cannot-reset-platform-admin`); try switching tenant on a session that's been logged out/revoked elsewhere (should 401, not succeed).
- **eq-shell** · **#711/SEC-71 — mandatory TOTP enforcement is genuinely client-side only**, reconfirmed live (`shell-login.ts:476-495` issues a full session regardless of the flag). The issue itself says it needs Royce's call on intended grace-period semantics before anyone implements a fix — not built.
- **eq-shell** · **The one piece not done: actually clicking Grant/Revoke platform admin end-to-end.** Deliberately not tested against a real employee — granting or revoking "every permission, in every tenant," even briefly and reversibly, is real enough that it needs either Royce's own hands or a disposable test account named for the purpose. Nobody's pointed at one yet. Full detail on what WAS confirmed live: `sessions/2026-09-05.md`. _(added 2026-08-17, 2026-08-18, 2026-08-25; consolidated 2026-09-05; click-tested 2026-09-05; deferred again 2026-09-07 via `/triage` — still nobody pointed at a disposable test account)_
- **eq-shell** · **3 of the 4 fixes verified only via `tsc -b --force` + eslint + `pnpm test` (including a negative-proof test per fix: fails on the pre-fix code, passes on the fix) — not a real click-through.** Only PR #1760's rate-limit reordering got an end-to-end live check (real HTTP requests against its deploy preview, cross-checked against the live `rate_limit_buckets`/`audit_log` tables). Worth a real pass on the other three: trigger `update_site`/`add_site` with an inactive contact and confirm it's rejected before any write lands; delete a user with linked staff/worker records and confirm the purge stays inside one tenant; open a PR with a deliberately colliding migration prefix and confirm CI fails it. _(added 2026-09-04)_
- **eq-shell** · **3 directories left on disk, OS-locked, not deletable from this session** — `git worktree remove` unregistered them from git (2 errored "Result too large" but still unregistered; 1 confirmed via `git worktree prune`), but the physical folders survived both `Remove-Item -Force` and `rm -rf` ~10 minutes apart, both failing with "device or resource busy" / "being used by another process." Locking process not identified (`Get-CimInstance Win32_Process` showed nothing obviously relevant). Needs Royce to close whatever has them open (or a reboot) before they're actually reclaimable: `.claude\worktrees\contact-auto-site-ops-download-325f25`, `.claude\worktrees\list-user-invites-existing-user-filter`, `.claude\worktrees\simplified-interface-users-764a0d`. _(added 2026-09-01)_
_…and 214 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 1 | 3d |
| eq-solves-service | ✓ success | 3d ago | 7 | 8d |
| eq-field | ✓ success | 0d ago | 2 | 3d |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✗ failure | 3d ago | 0 | — |

## Deploys

| Site | State | Last deploy |
|------|-------|-------------|
| eq-shell | ready | 2026-09-13 |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-field | [Error: canon-read: body.tenant_slug fallback used](https://eq-solutions.sentry.io/issues/146010412/) | 15 | 2026-09-09 |
| eq-field | [TypeError: Failed to fetch](https://eq-solutions.sentry.io/issues/145909030/) | 15 | 2026-09-09 |
| eq-shell | [EQ Field handoff stalled at "booted" (162s, no 'accepted' yet)](https://eq-solutions.sentry.io/issues/145052767/) | 13 | 2026-09-11 |
| eq-shell | [Error: Active org_memberships held by non-members: 1](https://eq-solutions.sentry.io/issues/142429897/) | 9 | 2026-09-12 |
| eq-shell | [EQ Field accepted the handoff but never reported 'rendered' (101s)](https://eq-solutions.sentry.io/issues/145332293/) | 6 | 2026-09-11 |
| eq-field | [AbortError: Fetch is aborted](https://eq-solutions.sentry.io/issues/143320850/) | 6 | 2026-09-09 |
| eq-shell | [Error: Workers missing an active org_membership: 1 (1 already hiding licences)](https://eq-solutions.sentry.io/issues/145797834/) | 5 | 2026-09-12 |
| eq-shell | [auth-stall: render-crash](https://eq-solutions.sentry.io/issues/140924723/) | 5 | 2026-09-11 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-09-13 | eq-shell | [#1893](https://github.com/eq-solutions/eq-shell/pull/1893) fix(security): revoke superfluous anon grant on madagins's field_ |
| 2026-09-13 | eq-field | [#979](https://github.com/eq-solutions/eq-field/pull/979) fix(ci): stop 8 scripts truncating their own report |
| 2026-09-13 | eq-cards | [#353](https://github.com/eq-solutions/eq-cards/pull/353) fix(ci): stop check-function-grants.mjs truncating its own report |
| 2026-09-10 | eq-shell | [#1892](https://github.com/eq-solutions/eq-shell/pull/1892) fix(ci): apply the exit-truncation fix to check-shell-staff-activ |
| 2026-09-10 | eq-shell | [#1891](https://github.com/eq-solutions/eq-shell/pull/1891) fix(ci): apply the #1886 exit-truncation fix to 12 more scripts |
| 2026-09-10 | eq-shell | [#1885](https://github.com/eq-solutions/eq-shell/pull/1885) docs(control-plane-ledger): record #1875's cancel-my-access-reque |
| 2026-09-10 | eq-shell | [#1890](https://github.com/eq-solutions/eq-shell/pull/1890) fix(documents): site labels a certificate, it no longer filters i |
| 2026-09-10 | eq-field | [#976](https://github.com/eq-solutions/eq-field/pull/976) fix(csp): allowlist madagins's Supabase project in connect-src/ws |
| 2026-09-09 | eq-shell | [#1889](https://github.com/eq-solutions/eq-shell/pull/1889) feat(documents): let a certificate's site pick combine with team/ |
| 2026-09-09 | eq-shell | [#1888](https://github.com/eq-solutions/eq-shell/pull/1888) feat(documents): let a certificate export pick a team or signers |
| 2026-09-09 | eq-shell | [#1887](https://github.com/eq-solutions/eq-shell/pull/1887) fix(connect): fall back instead of crashing on an unmapped reques |
| 2026-09-09 | eq-shell | [#1882](https://github.com/eq-solutions/eq-shell/pull/1882) fix(field): make the Field-workspace picker read tenants live |
| 2026-09-09 | eq-shell | [#1886](https://github.com/eq-solutions/eq-shell/pull/1886) fix(ci): stop tenant-drift/control-plane-drift scripts truncating |
| 2026-09-09 | eq-shell | [#1884](https://github.com/eq-solutions/eq-shell/pull/1884) fix(token-exchange): scope platform-admin Field JWT to the picked |
| 2026-09-09 | eq-shell | [#1879](https://github.com/eq-solutions/eq-shell/pull/1879) fix(security): lock field_tenant_slug to a tenant's own slug |
_Showing 15 of 75 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-shell** (296 open) · [eq/pending/eq-shell.md](eq/pending/eq-shell.md)
- **eq-cards** (65 open) · [eq/pending/eq-cards.md](eq/pending/eq-cards.md)
- **eq-field** (234 open) · [eq/pending/eq-field.md](eq/pending/eq-field.md)
- **eq-solves-service** (70 open) · [eq/pending/eq-solves-service.md](eq/pending/eq-solves-service.md)
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
| [eq-shell](eq/pending/eq-shell.md) | 1692 | 234 / 63 | 3 | 94 |
| [eq-cards](eq/pending/eq-cards.md) | 365 | 48 / 17 | 0 | 11 |
| [eq-field](eq/pending/eq-field.md) | 1292 | 195 / 40 | 0 | 60 |
| [eq-solves-service](eq/pending/eq-solves-service.md) | 401 | 51 / 20 | 0 | 26 |
| [eq-solves-intake](eq/pending/eq-solves-intake.md) | 179 | 13 / 6 | 0 | 17 |
| [eq-design-tokens](eq/pending/eq-design-tokens.md) | 25 | 1 / 0 | 0 | 1 |
| [eq-ui](eq/pending/eq-ui.md) | 24 | 2 / 0 | 0 | 0 |
| [eq-receipts](eq/pending/eq-receipts.md) | 46 | 3 / 1 | 0 | 4 |
| [eq-context](eq/pending/eq-context.md) | 241 | 31 / 12 | 0 | 12 |
| [cross-repo](eq/pending/cross-repo.md) | 949 | 136 / 47 | 0 | 88 |
| [sks](eq/pending/sks.md) | 55 | 3 / 5 | 0 | 6 |
| [SKS](sks/pending.md) | 515 | 95 / 15 | 0 | 66 |
| [SKS active](sks/active.md) | 119 | 0 / 0 | 0 | 0 |
| [OPS](ops/pending.md) | 619 | 52 / 3 | 0 | 17 |

## Aging open items (45d+, unconfirmed)

_Open items sitting under a section header this old or older — not necessarily wrong, just gone quiet under its own dated write-up. Worth a look before it reads as done-and-forgotten._

- **eq-shell** (2026-07-29) · **Royce to re-review Bruno Vita Pedrosa, Luke Wheeler, and Mohamed Ahmed** — their current flags trace to the confirmed false-positive batch touches; reviewing them now (post-#1101) records a real fingerprint so they won't be falsely re-flagged again. _(added 2026-07-29)_
- **eq-shell** (2026-07-28) · **Separate, lower-priority finding: 53 of 88 active SKS staff have a Cards worker link but zero credentials captured in Cards at all** (checked the pre-promotion `worker_credentials` table too — genuinely empty, not stuck mid-migration). Only 34 of 88 active staff have any licence data flowing through Shell. This is a Cards onboarding-completion gap, not a sync bug — no action taken, logging only per Royce's call. _(added 2026-07-28)_
- **eq-shell** (2026-07-28) · **Royce to export a real org's compliance pack and eyeball the new layout in Excel** — verified in code and with a test run, not yet checked against a real export. _(added 2026-07-28)_
- **eq-shell** (2026-07-28) · **Royce to re-download a compliance pack once the deploy lands** and confirm the filename reads correctly, Rhys Scott's email now shows current, and the spinner shows while it builds. _(added 2026-07-28, updated 2026-07-29)_
- **eq-shell** (2026-07-28) · **Rhys to re-upload a distinct back photo for his electrical licence** if the duplicate was accidental — his call, not a system fix. _(added 2026-07-28)_
- **eq-shell** (2026-07-28) · **Royce to re-enter Ben Ritchie's correct email one more time** via the Staff page — his last correction was reverted by the old bug before the fix went live, so the stale value is still sitting in the database. It will stick this time. _(added 2026-07-28)_
- **eq-shell** (2026-07-28) · **Royce to click through the Edit Roster grid on field.eq.solutions once the deploy lands** and confirm Ben Ritchie (or any off-roster person) no longer appears there — code-fixed and pushed, not yet eyeballed live. _(added 2026-07-28)_
- **eq-shell** (2026-07-28) · **Royce to check SKS-17489 in EQ Ops** once the deploy lands — confirm the badge and board agree, then enter a Job No. to actually advance it out of Open (that's why it was stuck). _(added 2026-07-28)_
- **eq-shell** (2026-07-28) · **CRON_SECRET rotation** — the one real hit: a plaintext credential in vendored git history (`eq-intake/eq-platform/apps/eq-service/CHANGELOG.md`, commit `b116e4430c8`, 2026-06-10, file since deleted from the tree), described in that commit as "already set" in Netlify. Deliberately left un-allowlisted in `.gitleaks.toml` so it keeps surfacing on a full-history scan rather than going silent. Needs a decision: rotate the value in Netlify, and note the same value likely sits in `eq-solves-intake`'s own git history too, not just here. _(added 2026-07-28)_
- **eq-shell** (2026-07-28) · **Remaining audit findings not yet triaged into work** — the 6-perspective "vs industry" audit that prompted this surfaced 4 P0 / 11 P1 / 9 P2 findings across auth, authorization, multi-tenant data, frontend composition, security ops, and DX tooling. Only the secret-scan gate (above) and the field_people drift (separate section) have been acted on so far. Full findings are in a Claude.ai artifact from this session, not yet copied into repo docs — worth deciding whether it needs a permanent home before the artifact is the only record of it. _(added 2026-07-28)_
- **eq-shell** (2026-07-27) · **Habit note, not a task**: after pulling any `@eq-solutions/*` package-version bump, run `pnpm install` before trusting a local `tsc -b` failure as a real regression — this one cost investigation time chasing a phantom code bug. _(added 2026-07-27)_
- **eq-shell** (2026-07-26) · **Hit the recurring "two sessions, one folder" hazard again mid-task** — another concurrent session was actively working in the same shared eq-shell folder at the same time, on a different branch, with its own unsaved work in progress. Worked around it safely (moved to an isolated copy, touched nothing of theirs) — no data lost, but this is the same known hazard logged elsewhere in this file, not a new one. _(added 2026-07-26)_
- **eq-shell** (2026-07-26) · **Real end-to-end confirmation still open**: re-archived the 4 originally-affected people (Aaron Clohessy, Emma Curth, Jack Fitzpatrick, Ross Davidson) as a live test. Need to check after tomorrow's nightly run (and ideally after their Cards profile syncs in real time) that they're still archived — that's the actual proof the fix holds, not just a clean deploy. _(added 2026-07-26)_
- **eq-shell** (2026-07-26) · **Bob Smith** (one of the 5 originally reported) still doesn't match any current staff record in the SKS tenant by name — never resolved, possibly a name-spelling mismatch or a different tenant. Worth a quick manual look. _(added 2026-07-26)_
- **eq-shell** (2026-07-26) · **The old, now-unused sync function is still sitting in Supabase** (edge function `credentials-canonical-sync`) — harmless since nothing calls it anymore, but there's no way to delete an edge function via a migration; would need a manual removal via the Supabase dashboard if Royce wants it gone entirely. _(added 2026-07-26)_
_…and 387 more — see each file's Queue health row above._

## Possible recurring failures (unconfirmed)

_Session logs mention a pattern matching a known failure below, dated after its last recorded occurrence. Not yet counted — if it's real, bump `recurrences` in [failures.md](system/failures.md) and `guard-ratchet.yml` proposes promotion on its own next run._

- **F5** (rung 0) — An ungoverned shadow memory overrode the canonical contract · 1 session since last recorded, most recent [2026-08-16.md](sessions/2026-08-16.md)

## Recent sessions

| Date | Session |
|------|---------|
| 2026-09-13 | [eq-solves-intake schema drift closed out; eq-shell JWT-secret root cause traced, fix drafted then lost to shared-checkout drift](sessions/2026-09-13.md) |
| 2026-09-10 | [F14's signal regex restructured (directional bug fix, pending.md/substrate anchors dropped); completes the F1/F9-adjacent precision pass started 2026-09-09](sessions/2026-09-10.md) |
| 2026-09-09 | [guard.js worktree-naming gap closed (rules 1/1b/1c/10, `-wt-` infix)](sessions/2026-09-09.md) |
| 2026-09-08 | [Customers/Staff/Equipment gained their own URL; 3 PRs merged + live (work done 2026-09-07, closed after midnight)](sessions/2026-09-08.md) |
| 2026-09-07 | [Labour-hire licence-photo fix re-verified live; full roster audited, no other worker exposed](sessions/2026-09-07.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-09-13 07:13 UTC._
