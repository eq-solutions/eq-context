---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-09-02
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-09-02 11:40 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-09-02 11:11 UTC → 2026-09-02 11:40 UTC)

- Merged: eq-shell [#1748](https://github.com/eq-solutions/eq-shell/pull/1748) fix(customers): hide archived contacts from a customer's con
- Merged: eq-shell [#1747](https://github.com/eq-solutions/eq-shell/pull/1747) perf(token-exchange): parallelize sequential Supabase reads
- Merged: eq-shell [#1738](https://github.com/eq-solutions/eq-shell/pull/1738) feat(documents): bulk-select documents on Register, push to 
- Merged: eq-shell [#1735](https://github.com/eq-solutions/eq-shell/pull/1735) fix(auth): disable forced TOTP enrollment mandate for now
- Merged: eq-shell [#1731](https://github.com/eq-solutions/eq-shell/pull/1731) fix(cards): backfill shell_control.users.email for phone-OTP
- Merged: eq-shell [#1730](https://github.com/eq-solutions/eq-shell/pull/1730) fix(admin): restore pin_set/pin_locked to eq_list_tenant_use
- Merged: eq-shell [#1727](https://github.com/eq-solutions/eq-shell/pull/1727) fix(staff): add previous-licence navigation to review modals
- Merged: eq-shell [#1726](https://github.com/eq-solutions/eq-shell/pull/1726) feat(documents): Unarchive action; move PDF backfill button 

## ⚠ Needs you (15)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-57 (P1) — An org-wide GitHub App installation (`grok-by-xai`, `repository_selection: all`) · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-08-23.md](sessions/2026-08-23.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F9: Concurrent-session git races corrupt the shared eq-context checkout · possibly recurred in [2026-08-31.md](sessions/2026-08-31.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F10: core.hooksPath silently resolves to the wrong location — three distinct mechanisms, one sy · possibly recurred in [2026-08-26.md](sessions/2026-08-26.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F12: Side-clone reconciliation blind-overwrote a concurrent session's already-pushed shared-fil · possibly recurred in [2026-08-30.md](sessions/2026-08-30.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-09-01.md](sessions/2026-09-01.md) · [failures.md](system/failures.md)
- 🟠 **PR aging 9d** — eq-solves-service [#814](https://github.com/eq-solutions/eq-service/pull/814) "chore(deps): bump resend from 6.18.1 to 6.21.0"
- 🟠 **PR aging 9d** — eq-solves-service [#813](https://github.com/eq-solutions/eq-service/pull/813) "chore(deps-dev): bump @types/leaflet from 1.9.21 to 1.9.22"
- 🟠 **PR aging 9d** — eq-solves-service [#812](https://github.com/eq-solutions/eq-service/pull/812) "chore(deps): bump posthog-node from 5.46.1 to 5.49.2"
- 🟠 **PR aging 9d** — eq-solves-service [#811](https://github.com/eq-solutions/eq-service/pull/811) "chore(deps-dev): bump vitest from 4.1.10 to 4.1.11"
- 🟠 **PR aging 9d** — eq-solves-service [#810](https://github.com/eq-solutions/eq-service/pull/810) "chore(deps): bump the eq-design-system group across 1 directory with 2"
- 🟠 **PR aging 13d** — eq-solves-service [#791](https://github.com/eq-solutions/eq-service/pull/791) "fix(reports): make reissuing a report possible from the UI"
- 🟠 **Cron failing** — `security-audit.yml` 1 consecutive scheduled run(s) failed, last success 2026-08-23 · [failures.md](system/failures.md) F11
- 🟠 **Cron failing** — `shared-object-drift.yml` 1 consecutive scheduled run(s) failed, no success in recent history · [failures.md](system/failures.md) F11

## 🙋 Waiting on you (267)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **eq-shell** · **Not click-tested live** — confirming the fix needs a live PostHog project plus a real session left open past two 5-minute poll ticks, watching PostHog's own activity feed for exactly one `$create_alias` instead of one per tick. _(added 2026-09-02)_
- **eq-shell** · **Not click-tested live** — verified via `pnpm exec tsc -b --force` and `eslint` (both clean) plus an independent merge-readiness audit before merging. This machine's Node 24 breaks `vite build`/`netlify dev` for this repo (pre-existing, unrelated to this change), so no live click-through was possible. Worth a real pass: KPI numbers match the table's own counts, per-team rows sum to the roster totals, mobile view unchanged. _(added 2026-09-02)_
- **eq-shell** · **Not click-tested live** — verified via `tsc -b --force` + `eslint` only (both clean). Reproducing the actual pending-approval message needs a real Cards signup mid-approval-queue, not something drivable from this environment. _(added 2026-09-01)_
- **eq-shell** · **Not click-tested live by a person** — verified via `tsc -b --force`, `eslint`, and by actually rendering sample PDFs from the code with mock data (4 variants: with/without logo, all-signed, small site-set) and visually inspecting them — not a live authenticated download. Worth a real pass: open the Register tab for a tenant with an uploaded document logo, pull a multi-site certificate, confirm logo/title/pill render as expected in a real download. _(added 2026-09-01)_
- **eq-shell** · **Not click-tested live** — no Shell/Cards session available in this environment. Worth a real pass: hit `/join?tenant=<slug>` 6× rapidly with the same phone and confirm the 6th returns 429 with `Retry-After`, then confirm a genuine join still succeeds after the window (or immediately for a different phone). _(added 2026-09-01)_
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment. Worth a real pass: open `/admin/users`, switch to Pending, confirm it renders real outstanding invites for a tenant that has some. _(added 2026-09-01)_
- **eq-shell** · **Not click-tested live** — PR #1708's own test plan flags this: build/tests/lint clean, but nobody's archived a real staff-linked account and watched the new checkbox clear it. _(added 2026-09-01)_
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment, and Vite/`netlify dev` are unreliable under this machine's Node 24 (existing memory), so no attempt was made to fake it. Worth a real pass: open a customer with a Field-enabled site and confirm the pill now shows on; toggle the pill off and confirm every owned site follows; check a customer with zero sites shows the toggle disabled with the right tooltip; same 3 checks on the separate App activation admin page. _(added 2026-09-01)_
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment; verified via `tsc -b --force`, `eslint`, and a merge-readiness audit that reproduced the CI run end-to-end. Worth a real pass: open a quote for a customer with existing sites, click "Link existing site," confirm it searches every site in the tenant and auto-fills onto the quote once linked; try "New site" with a name close to an existing one and confirm the duplicate warning shows.
- **eq-shell** · **3 directories left on disk, OS-locked, not deletable from this session** — `git worktree remove` unregistered them from git (2 errored "Result too large" but still unregistered; 1 confirmed via `git worktree prune`), but the physical folders survived both `Remove-Item -Force` and `rm -rf` ~10 minutes apart, both failing with "device or resource busy" / "being used by another process." Locking process not identified (`Get-CimInstance Win32_Process` showed nothing obviously relevant). Needs Royce to close whatever has them open (or a reboot) before they're actually reclaimable: `.claude\worktrees\contact-auto-site-ops-download-325f25`, `.claude\worktrees\list-user-invites-existing-user-filter`, `.claude\worktrees\simplified-interface-users-764a0d`. _(added 2026-09-01)_
- **eq-shell** · **Not click-tested live by a person** — verified via `tsc -b --force`, `eslint`, an 8-angle automated review, and Netlify deploy-preview smoke tests; no Shell session/credentials in this environment. Worth a real pass covering both PRs (#1683, #1685): panel opens in place with a shareable `?open=` URL; a formal entry opens with full detail, rating deltas, and (where attached) a source document; saving without answering "happy and engaged" is blocked and scrolls to the field; engagement tags render with color; a person with no `start_date` is flagged "missing a start date" but NOT also "overdue"; a hollow historical review shows its summary and one "no structured answers" note instead of ~20 blank fields. _(added 2026-08-30)_
- **eq-shell** · **Migration 0298 needs Royce to dispatch it** — see above, command included. _(added 2026-09-01)_
_…and 255 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 6 | 1d |
| eq-solves-service | ✓ success | 0d ago | 6 | 13d |
| eq-field | ✓ success | 23d ago | 2 | 0d |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 11 | 2026-09-02 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 9 | 2026-09-02 |
| eq-field | [AbortError: Fetch is aborted](https://eq-solutions.sentry.io/issues/143320850/) | 5 | 2026-09-02 |
| eq-field | [TypeError: Failed to fetch](https://eq-solutions.sentry.io/issues/141259049/) | 4 | 2026-09-02 |
| eq-field | [ReferenceError: _renderRosterOverviewCard is not defined](https://eq-solutions.sentry.io/issues/144372461/) | 1 | 2026-09-02 |
| eq-cards | [minified:B8: AuthRetryableFetchException(message: ClientException: Failed to fet](https://eq-solutions.sentry.io/issues/144338444/) | 1 | 2026-09-02 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-09-02 | eq-shell | [#1748](https://github.com/eq-solutions/eq-shell/pull/1748) fix(customers): hide archived contacts from a customer's contact  |
| 2026-09-02 | eq-shell | [#1747](https://github.com/eq-solutions/eq-shell/pull/1747) perf(token-exchange): parallelize sequential Supabase reads |
| 2026-09-02 | eq-shell | [#1746](https://github.com/eq-solutions/eq-shell/pull/1746) fix(crm): extend the inactive-contact link guard to update_site/a |
| 2026-09-02 | eq-shell | [#1742](https://github.com/eq-solutions/eq-shell/pull/1742) fix(crm): reject linking an inactive contact to a site or custome |
| 2026-09-02 | eq-shell | [#1745](https://github.com/eq-solutions/eq-shell/pull/1745) fix(observability): stop $create_alias spam from the 5-minute ses |
| 2026-09-02 | eq-shell | [#1744](https://github.com/eq-solutions/eq-shell/pull/1744) fix(home): hoist Date.now() out of render for react-hooks/purity |
| 2026-09-02 | eq-shell | [#1743](https://github.com/eq-solutions/eq-shell/pull/1743) fix(records): gate the Licences tab on field.view_licences |
| 2026-09-02 | eq-shell | [#1736](https://github.com/eq-solutions/eq-shell/pull/1736) fix(auth): bound verify-shell-session's best-effort reads with a  |
| 2026-09-02 | eq-field | [#889](https://github.com/eq-solutions/eq-field/pull/889) v3.5.649 — PERF: Shell→Field boot — stop entitlements blocking ch |
| 2026-09-02 | eq-field | [#888](https://github.com/eq-solutions/eq-field/pull/888) v3.5.648 — Edit Roster: show approved leave while editing |
| 2026-09-02 | eq-field | [#887](https://github.com/eq-solutions/eq-field/pull/887) v3.5.647 -- FIX: Apprentices Quarterly Review modal unstyled and  |
| 2026-09-02 | eq-field | [#886](https://github.com/eq-solutions/eq-field/pull/886) v3.5.646 — Roster/Editor/Contacts/Timesheets: scoped-view banner  |
| 2026-09-02 | eq-field | [#885](https://github.com/eq-solutions/eq-field/pull/885) v3.5.645 — sync_degraded: surface crew-table failures alongside p |
| 2026-09-02 | eq-field | [#884](https://github.com/eq-solutions/eq-field/pull/884) fix(e2e): allowlist Netlify's edge bot-challenge 403 in shell-mod |
| 2026-09-02 | eq-field | [#883](https://github.com/eq-solutions/eq-field/pull/883) v3.5.644 — Correct false PR #878 claim; add E2E coverage for PR # |
_Showing 15 of 86 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-shell** (274 open) · [eq/pending/eq-shell.md](eq/pending/eq-shell.md)
- **eq-cards** (63 open) · [eq/pending/eq-cards.md](eq/pending/eq-cards.md)
- **eq-field** (210 open) · [eq/pending/eq-field.md](eq/pending/eq-field.md)
- **eq-solves-service** (98 open) · [eq/pending/eq-solves-service.md](eq/pending/eq-solves-service.md)
- **eq-solves-intake** (18 open) · [eq/pending/eq-solves-intake.md](eq/pending/eq-solves-intake.md)
- **eq-design-tokens** (1 open) · [eq/pending/eq-design-tokens.md](eq/pending/eq-design-tokens.md)
- **eq-ui** (2 open) · [eq/pending/eq-ui.md](eq/pending/eq-ui.md)
- **eq-receipts** (4 open) · [eq/pending/eq-receipts.md](eq/pending/eq-receipts.md)
- **eq-context** (31 open) · [eq/pending/eq-context.md](eq/pending/eq-context.md)
- **cross-repo** (173 open) · [eq/pending/cross-repo.md](eq/pending/cross-repo.md)
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
| [eq-shell](eq/pending/eq-shell.md) | 1456 | 195 / 84 | 48 | 67 |
| [eq-cards](eq/pending/eq-cards.md) | 374 | 48 / 17 | 24 | 6 |
| [eq-field](eq/pending/eq-field.md) | 1162 | 151 / 67 | 38 | 33 |
| [eq-solves-service](eq/pending/eq-solves-service.md) | 522 | 75 / 24 | 0 | 27 |
| [eq-solves-intake](eq/pending/eq-solves-intake.md) | 141 | 13 / 5 | 0 | 17 |
| [eq-design-tokens](eq/pending/eq-design-tokens.md) | 23 | 1 / 0 | 0 | 1 |
| [eq-ui](eq/pending/eq-ui.md) | 22 | 2 / 0 | 0 | 0 |
| [eq-receipts](eq/pending/eq-receipts.md) | 44 | 3 / 1 | 0 | 0 |
| [eq-context](eq/pending/eq-context.md) | 203 | 25 / 6 | 0 | 4 |
| [cross-repo](eq/pending/cross-repo.md) | 888 | 129 / 44 | 0 | 61 |
| [sks](eq/pending/sks.md) | 53 | 3 / 5 | 0 | 6 |
| [SKS](sks/pending.md) | 493 | 92 / 15 | 2 | 54 |
| [SKS active](sks/active.md) | 119 | 0 / 0 | 0 | 0 |
| [OPS](ops/pending.md) | 530 | 43 / 3 | 0 | 8 |

## Aging open items (45d+, unconfirmed)

_Open items sitting under a section header this old or older — not necessarily wrong, just gone quiet under its own dated write-up. Worth a look before it reads as done-and-forgotten._

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
- **eq-shell** (2026-07-14) · **Later audit polish** — PDF / branded-report export, and logging who reads the log; then on-request data erasure and anomaly alerts. _(added 2026-07-14; before/after values shipped in #860)_
- **eq-shell** (2026-07-14) · **Crew retry + Sentry watch** — have the crew reopen via a normal browser tab (their home-screen icon may hold stale code from the day's deploys); if anyone still freezes, the fix now self-tags the exact stall in Sentry (`verify-timeout` / `login-timeout` / `session-spinner-timeout` / `chunk-error`). _(added 2026-07-14)_
- **eq-shell** (2026-07-14) · **Material-preset sanity check** — since materials presets now quote at Rate + markup, any entered as already-marked-up sell prices will read higher; worth a glance in the Rate library. _(added 2026-07-14, carried from #820)_
- **eq-shell** (2026-07-14) · **Phone-smoke Comms + Ops mobile on a real device** — both deployed and content-verified, but not exercised through a real authenticated session (auth-gated; not reproducible in the sandbox). _(added 2026-07-14)_
_…and 269 more — see each file's Queue health row above._

## Possible recurring failures (unconfirmed)

_Session logs mention a pattern matching a known failure below, dated after its last recorded occurrence. Not yet counted — if it's real, bump `recurrences` in [failures.md](system/failures.md) and `guard-ratchet.yml` proposes promotion on its own next run._

- **F5** (rung 0) — An ungoverned shadow memory overrode the canonical contract · 1 session since last recorded, most recent [2026-08-16.md](sessions/2026-08-16.md)

## Recent sessions

| Date | Session |
|------|---------|
| 2026-09-02 | [Live-meeting kit: sample ID sheet added, QR-at-scale question resolved by finding it already exists](sessions/2026-09-02.md) |
| 2026-09-01 | [eq-solves-service: migration-governance review (task_38071324) closed — DB-first PR split adopted, --reconcile tooling shipped (PR #820)](sessions/2026-09-01.md) |
| 2026-08-31 | [Removed staff's historical leave/timesheet rows fixed to show real names, not "(unknown)"](sessions/2026-08-31.md) |
| 2026-08-30 | [SEC-35 merged, deployed, and dispatched live to both tenant planes](sessions/2026-08-30.md) |
| 2026-08-29 | [eq-shell sprint request started, not finished before close](sessions/2026-08-29.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-09-02 11:40 UTC._
