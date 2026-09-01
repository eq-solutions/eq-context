---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-09-01
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-09-01 02:33 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-09-01 02:27 UTC → 2026-09-01 02:33 UTC)

- Merged: eq-shell [#1691](https://github.com/eq-solutions/eq-shell/pull/1691) fix(security): entity.view gate on 5 CRM read RPCs called di
- Merged: eq-shell [#1689](https://github.com/eq-solutions/eq-shell/pull/1689) feat(permissions): quotes.view_all now grantable per-person 
- Merged: eq-shell [#1686](https://github.com/eq-solutions/eq-shell/pull/1686) fix(security): tenant_role_overrides denials were silently i
- Merged: eq-shell [#1682](https://github.com/eq-solutions/eq-shell/pull/1682) fix(auth): active-account re-check on 11 endpoints missing i
- Merged: eq-shell [#1681](https://github.com/eq-solutions/eq-shell/pull/1681) fix(security): quotes RPCs had no server-side permission che
- Merged: eq-shell [#1680](https://github.com/eq-solutions/eq-shell/pull/1680) fix(security): upgrade zaap/ehow's function-privacy trigger,
- Merged: eq-shell [#1678](https://github.com/eq-solutions/eq-shell/pull/1678) fix(security): close eq_revoke_session's group-permission bl
- Merged: eq-shell [#1676](https://github.com/eq-solutions/eq-shell/pull/1676) fix(sites): QuotesCustomers' Edit Site panel writes contact_

## ⚠ Needs you (15)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-57 (P1) — An org-wide GitHub App installation (`grok-by-xai`, `repository_selection: all`) · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-08-23.md](sessions/2026-08-23.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F9: Concurrent-session git races corrupt the shared eq-context checkout · possibly recurred in [2026-08-31.md](sessions/2026-08-31.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F10: core.hooksPath silently resolves to the wrong location — three distinct mechanisms, one sy · possibly recurred in [2026-08-26.md](sessions/2026-08-26.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F12: Side-clone reconciliation blind-overwrote a concurrent session's already-pushed shared-fil · possibly recurred in [2026-08-30.md](sessions/2026-08-30.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-08-31.md](sessions/2026-08-31.md) · [failures.md](system/failures.md)
- 🟠 **PR aging 7d** — eq-solves-service [#814](https://github.com/eq-solutions/eq-service/pull/814) "chore(deps): bump resend from 6.18.1 to 6.21.0"
- 🟠 **PR aging 7d** — eq-solves-service [#813](https://github.com/eq-solutions/eq-service/pull/813) "chore(deps-dev): bump @types/leaflet from 1.9.21 to 1.9.22"
- 🟠 **PR aging 7d** — eq-solves-service [#812](https://github.com/eq-solutions/eq-service/pull/812) "chore(deps): bump posthog-node from 5.46.1 to 5.49.2"
- 🟠 **PR aging 7d** — eq-solves-service [#811](https://github.com/eq-solutions/eq-service/pull/811) "chore(deps-dev): bump vitest from 4.1.10 to 4.1.11"
- 🟠 **PR aging 7d** — eq-solves-service [#810](https://github.com/eq-solutions/eq-service/pull/810) "chore(deps): bump the eq-design-system group across 1 directory with 2"
- 🟠 **PR aging 11d** — eq-solves-service [#791](https://github.com/eq-solutions/eq-service/pull/791) "fix(reports): make reissuing a report possible from the UI"
- 🟠 **Cron failing** — `index-drift.yml` 1 consecutive scheduled run(s) failed, last success 2026-08-30 · [failures.md](system/failures.md) F11
- 🟠 **Cron failing** — `security-audit.yml` 1 consecutive scheduled run(s) failed, last success 2026-08-23 · [failures.md](system/failures.md) F11

## 🙋 Waiting on you (233)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment; verified via `tsc -b --force`, `eslint`, and a merge-readiness audit that reproduced the CI run end-to-end. Worth a real pass: open a quote for a customer with existing sites, click "Link existing site," confirm it searches every site in the tenant and auto-fills onto the quote once linked; try "New site" with a name close to an existing one and confirm the duplicate warning shows.
- **eq-shell** · **Not click-tested live by a person** — every PR this session verified via `pnpm run build`/`eslint`/`pnpm run test`/live DB queries only, never an actual signed-in click-through. Worth a real pass: upload a document, assign/change its category from each of the 3 tabs, create a new reference-only category via the new toggle, confirm the routing actually changes. _(added 2026-08-30)_
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment; verified via `tsc -b --force`, the full test suite, and a merge-readiness audit reproducing the production build end-to-end. Worth a real pass: approve a Cards application with a start date set and confirm it lands; add someone via Shell's "Add to roster" with a start date and confirm it lands; confirm the Resourcing page's new count and filter tab work. _(added 2026-08-30)_
- **eq-shell** · **Not click-tested live by a person** — verified via live SQL + deploy-state checks, not by opening the Edit Site modal itself. Worth a real pass on Equinix SY5: confirm Ask for/Backup show Matthew Miller/Scott Hotson, try the inline "+ Add new contact" flow, save, reopen, confirm it stuck. _(added 2026-08-30)_
- **eq-shell** · **SEC-67's env-var half still needs Royce** — 4 confirmed-dead Netlify env vars (`FIELD_SUPABASE_URL`/`_SERVICE_ROLE_KEY`, `NEXT_PUBLIC_SUPABASE_URL`/`_ANON_KEY`), zero code references, ready to delete — blocked by Claude Code's own classifier on unattended env-var writes. Commands in `sessions/2026-08-30.md`. _(added 2026-08-30)_
- **eq-shell** · **SEC-57 — Royce decided "revoke `grok-by-xai`" (2026-08-30), but it can't be done via API.** Confirmed live: `DELETE /orgs/eq-solutions/installations/{id}` doesn't exist (404); `DELETE /app/installations/{id}` needs the app's own JWT auth, not an org member's token (401). Uninstalling a GitHub App from an org is a GitHub-web-UI-only action for a human with org admin rights — Settings → GitHub Apps (or Installed GitHub Apps) → grok-by-xai → Uninstall. Still needs Royce to actually click it. _(added 2026-08-30)_
- **eq-shell** · **Needs Royce's call, security-hardening scope**: SEC-3, SEC-18, SEC-19, SEC-63, SEC-65, SEC-24. Full detail in the sprint doc, not re-listed here. _(added 2026-08-28)_
- **eq-shell** · **Not click-tested live** — same gap as every scope in this arc (site/customer/multi-site all share it): no Shell session/credentials in this environment. Worth one real pass covering all three: push to 2+ sites directly, push to a customer, confirm one signoff + one signature covers the set in both cases, confirm per-site and whole-group certificate exports both render correctly. _(added 2026-08-30)_
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment. Worth a real pass: open the Register tab for a tenant with several signed documents, confirm names now match Staff, open one signer's evidence modal, confirm the signature image still loads (now on demand). _(added 2026-08-28)_
- **eq-shell** · **"Merged, live" above means the code path exists — Gotenberg itself was never actually provisioned.** Checked live 2026-08-28/30: `GOTENBERG_URL` doesn't exist anywhere in eq-shell's Netlify env vars. Every conversion attempt (new upload or the backfill endpoint) silently degrades to `pdf_status='failed'` — confirmed against real data: of 18 pre-pipeline Office documents on ehow, 0 have ever reached `pdf_status='ready'`. Self-hosted on Fly.io per the PR's own recorded decisions (private networking, always-warm); `flyctl` is installed locally but not authenticated, needs Royce's `flyctl auth login` at minimum. Royce's explicit call 2026-08-28: defer — only 2 of the 18 stuck documents actually have signoffs assigned (the rest are unassigned templates nobody's opening), and the one that mattered (Environmental Management Plan) has a zero-infra manual workaround (export to PDF, re-upload as a new version — skips Gotenberg entirely since an already-PDF upload never calls it). Revisit if this starts happening often enough to justify the infra spend. _(added 2026-08-28, reconfirmed 2026-08-30)_
- **eq-shell** · **Duplicate-code 409 and remove-chip specifically still not confirmed live.** Partially overtaken since 2026-08-27: MOD10 on Telstra SLDC is now a real, actively-used code — Field reads it (chips on Sites/My Schedule), writes against it (roster picker + a typed-code alias resolver), and it's been exercised heavily via direct queries this session — so "does a real code exist and get used for real" is answered. What's specifically NOT confirmed: the add-UI's duplicate-code 409 response and the remove-✕ button, neither exercised this session. _(added 2026-08-27, narrowed 2026-08-30)_
- **eq-shell** · **Not click-tested live** — verified via `tsc -b --force`, live DB queries (jvkn/ehow), and production commit-ancestry, not a real signed-in session creating a fresh Labour Hire/Apprentice/Subcontractor invite end-to-end. Worth a real click-through next time someone invites a non-Employee worker: confirm the Staff record shows the correct employment_type immediately, before the invite is ever claimed. _(added 2026-08-26)_
_…and 221 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 5 | 0d |
| eq-solves-service | ✓ success | 0d ago | 7 | 11d |
| eq-field | ✓ success | 0d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 13d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: app_data.staff.cards_worker_id pointing at missing jvkn workers: 2](https://eq-solutions.sentry.io/issues/138175643/) | 12 | 2026-08-31 |
| eq-shell | [Error: Active org_memberships held by non-members: 14](https://eq-solutions.sentry.io/issues/142429897/) | 9 | 2026-08-31 |
| eq-shell | [Error: Unclaimed worker invites past grace period: 2 still valid, 0 expired](https://eq-solutions.sentry.io/issues/142642035/) | 8 | 2026-08-31 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 7 | 2026-08-26 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 5 | 2026-08-31 |
| eq-shell | [phone-otp: requested for inactive account](https://eq-solutions.sentry.io/issues/141933696/) | 2 | 2026-08-20 |
| eq-shell | [EQ Field handoff auto-recovery (timeout)](https://eq-solutions.sentry.io/issues/141463602/) | 2 | 2026-08-20 |
| eq-field | [ReferenceError: _renderTsApprovalQueue is not defined](https://eq-solutions.sentry.io/issues/144087479/) | 1 | 2026-09-01 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-09-01 | eq-shell | [#1700](https://github.com/eq-solutions/eq-shell/pull/1700) fix(crm): compute customer Field/Service status from owned sites |
| 2026-09-01 | eq-shell | [#1704](https://github.com/eq-solutions/eq-shell/pull/1704) fix(permissions): narrow Supervisor's default quote visibility to |
| 2026-09-01 | eq-shell | [#1703](https://github.com/eq-solutions/eq-shell/pull/1703) feat(quotes): link an existing site from EQ Ops, warn on likely-d |
| 2026-09-01 | eq-shell | [#1702](https://github.com/eq-solutions/eq-shell/pull/1702) docs: correct eq_enforce_function_privacy scope + behavior per pl |
| 2026-09-01 | eq-field | [#859](https://github.com/eq-solutions/eq-field/pull/859) fix(security): role-default bypasses tenant_role_overrides deny-c |
| 2026-09-01 | eq-field | [#863](https://github.com/eq-solutions/eq-field/pull/863) v3.5.629 — FIX: Edit Roster site dropdown showed no sites -> fold |
| 2026-09-01 | eq-field | [#862](https://github.com/eq-solutions/eq-field/pull/862) v3.5.628 — Roster: future-start new hires no longer hidden |
| 2026-09-01 | eq-field | [#861](https://github.com/eq-solutions/eq-field/pull/861) fix(ci): normalize line endings in cache-buster drift check |
| 2026-08-31 | eq-shell | [#1701](https://github.com/eq-solutions/eq-shell/pull/1701) fix: add field_job_numbers_src to SHARED_REGISTRY_FUNCTIONS |
| 2026-08-31 | eq-shell | [#1694](https://github.com/eq-solutions/eq-shell/pull/1694) fix(security): thread tenant_role_overrides denials into Quotes/C |
| 2026-08-31 | eq-shell | [#1693](https://github.com/eq-solutions/eq-shell/pull/1693) fix(security): thread tenant_role_overrides denials into the tena |
| 2026-08-31 | eq-shell | [#1692](https://github.com/eq-solutions/eq-shell/pull/1692) fix(security): scope quote status/note writes to created_by |
| 2026-08-31 | eq-shell | [#1688](https://github.com/eq-solutions/eq-shell/pull/1688) fix(records): not-allowed page for direct nav to a denied entity/ |
| 2026-08-31 | eq-shell | [#1690](https://github.com/eq-solutions/eq-shell/pull/1690) fix(security): thread tenant_role_overrides denials into the Fiel |
| 2026-08-31 | eq-solves-service | [#822](https://github.com/eq-solutions/eq-service/pull/822) fix(defects): revalidate /defects on check-item fail/un-fail |
_Showing 15 of 97 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-shell** (249 open) · [eq/pending/eq-shell.md](eq/pending/eq-shell.md)
- **eq-cards** (57 open) · [eq/pending/eq-cards.md](eq/pending/eq-cards.md)
- **eq-field** (186 open) · [eq/pending/eq-field.md](eq/pending/eq-field.md)
- **eq-solves-service** (96 open) · [eq/pending/eq-solves-service.md](eq/pending/eq-solves-service.md)
- **eq-solves-intake** (18 open) · [eq/pending/eq-solves-intake.md](eq/pending/eq-solves-intake.md)
- **eq-design-tokens** (1 open) · [eq/pending/eq-design-tokens.md](eq/pending/eq-design-tokens.md)
- **eq-ui** (2 open) · [eq/pending/eq-ui.md](eq/pending/eq-ui.md)
- **eq-receipts** (4 open) · [eq/pending/eq-receipts.md](eq/pending/eq-receipts.md)
- **eq-context** (29 open) · [eq/pending/eq-context.md](eq/pending/eq-context.md)
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
| [eq-shell](eq/pending/eq-shell.md) | 1324 | 185 / 72 | 27 | 67 |
| [eq-cards](eq/pending/eq-cards.md) | 314 | 43 / 16 | 12 | 6 |
| [eq-field](eq/pending/eq-field.md) | 1060 | 142 / 55 | 28 | 33 |
| [eq-solves-service](eq/pending/eq-solves-service.md) | 489 | 74 / 22 | 0 | 27 |
| [eq-solves-intake](eq/pending/eq-solves-intake.md) | 141 | 13 / 5 | 0 | 17 |
| [eq-design-tokens](eq/pending/eq-design-tokens.md) | 23 | 1 / 0 | 0 | 1 |
| [eq-ui](eq/pending/eq-ui.md) | 22 | 2 / 0 | 0 | 0 |
| [eq-receipts](eq/pending/eq-receipts.md) | 44 | 3 / 1 | 0 | 0 |
| [eq-context](eq/pending/eq-context.md) | 201 | 23 / 6 | 0 | 4 |
| [cross-repo](eq/pending/cross-repo.md) | 888 | 129 / 44 | 0 | 61 |
| [sks](eq/pending/sks.md) | 53 | 3 / 5 | 0 | 6 |
| [SKS](sks/pending.md) | 482 | 92 / 12 | 2 | 54 |
| [SKS active](sks/active.md) | 119 | 0 / 0 | 0 | 0 |
| [OPS](ops/pending.md) | 516 | 44 / 4 | 0 | 8 |

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
| 2026-09-01 | [eq-solves-service: migration-governance review (task_38071324) closed — DB-first PR split adopted, --reconcile tooling shipped (PR #820)](sessions/2026-09-01.md) |
| 2026-08-31 | [Removed staff's historical leave/timesheet rows fixed to show real names, not "(unknown)"](sessions/2026-08-31.md) |
| 2026-08-30 | [SEC-35 merged, deployed, and dispatched live to both tenant planes](sessions/2026-08-30.md) |
| 2026-08-29 | [eq-shell sprint request started, not finished before close](sessions/2026-08-29.md) |
| 2026-08-28 | [Documents to Sign: inline viewer's real bug found and fixed, then mapped audience reach](sessions/2026-08-28.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-09-01 02:33 UTC._
