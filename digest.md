---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-26
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-26 19:46 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-26 19:33 UTC → 2026-08-26 19:46 UTC)

- Merged: eq-shell [#1630](https://github.com/eq-solutions/eq-shell/pull/1630) feat(customers): let one Site carry multiple project/module 
- Merged: eq-shell [#1610](https://github.com/eq-solutions/eq-shell/pull/1610) fix(auth): stop offering Delete on self-join links that have
- Merged: eq-shell [#1607](https://github.com/eq-solutions/eq-shell/pull/1607) fix(security): audit-log role changes, fail loudly on member
- Merged: eq-shell [#1606](https://github.com/eq-solutions/eq-shell/pull/1606) fix(quotes): stack Commercials summary below the form on mob
- Merged: eq-shell [#1603](https://github.com/eq-solutions/eq-shell/pull/1603) fix(labour-hire): promote licence photos on the other 2 clai
- Merged: eq-shell [#1600](https://github.com/eq-solutions/eq-shell/pull/1600) fix(auth): sign-in mobile placeholder clarity + /login sessi
- Merged: eq-shell [#1599](https://github.com/eq-solutions/eq-shell/pull/1599) fix(access-control): group Preview-a-person's permission lis
- Merged: eq-solves-service [#815](https://github.com/eq-solutions/eq-service/pull/815) chore(deps): bump @eq-solutions/roles to v2.7.5

## ⚠ Needs you (7)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-57 (P1) — An org-wide GitHub App installation (`grok-by-xai`, `repository_selection: all`) · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-08-23.md](sessions/2026-08-23.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F9: Concurrent-session git races corrupt the shared eq-context checkout · possibly recurred in [2026-08-27.md](sessions/2026-08-27.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F10: core.hooksPath silently resolves to the wrong location — three distinct mechanisms, one sy · possibly recurred in [2026-08-26.md](sessions/2026-08-26.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F12: Side-clone reconciliation blind-overwrote a concurrent session's already-pushed shared-fil · possibly recurred in [2026-08-21.md](sessions/2026-08-21.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-08-25.md](sessions/2026-08-25.md) · [failures.md](system/failures.md)

## 🙋 Waiting on you (240)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **eq-shell** · **Not click-tested live by a person** — verified via `tsc -b`, the access-control preview panel, production deploy-ancestry, and (as of this close) Sharon Maroni's own live `nav_scope` row confirmed correct by direct query (`["customer","site","contact","staff","licence","equipment","field","suppliers"]` — Royce confirmed keep Suppliers) — but nobody has actually signed in as a Simple-mode user and watched the sidebar itself narrow. Worth two minutes next time there's a way to see her session or a test account. _(added 2026-08-26)_
- **eq-shell** · **Not click-tested live by a person** — no live Shell session/credentials in this environment. Worth a pass: on the join-links page, confirm a used deactivated link shows "Can't delete — already used" with no button, confirm the "Show deactivated & expired (N)" toggle expands/collapses correctly and the count matches. _(added 2026-08-26)_
- **eq-shell** · **Not click-tested live by a person** — verified via `tsc -b --force`, eslint, live Supabase tracing of the exact chain, and a production commit-ancestry check, not a real join-flow click-through as a brand-new user. _(added 2026-08-26)_
- **eq-shell** · **Not click-tested live** — no live Shell session/credentials in this environment. Worth a real pass: change a test user's role, confirm a `user.role_changed` row lands in `audit_log`, and (harder to stage) confirm a simulated membership-write failure now returns a real error instead of a false "saved." _(added 2026-08-26)_
- **eq-shell** · **Mobile Commercials-layout fix not click-tested live** — verified via `tsc -b --force` only; no live session/credentials in this environment, and this repo's local dev tooling is broken under Node 24 (existing memory). Worth a real look next time someone's on `/ops` → New Quote on a phone. _(added 2026-08-26)_
- **eq-shell** · **S6 — not code.** Neither of the 2026-08-23 sweep's own live fixes (`staff_conversations` write gate, GM Reports direct-API bypass) has been click-tested by a person yet. Whenever convenient, on you or whoever's got a live session. **Click-test steps written and delivered to Royce in chat 2026-08-26** — Fix A (`staff_conversations`): sign in without `staff.manage_conversations`, confirm no write path via the UI *and* via a direct browser-console insert (RLS, not just a hidden button). Fix B (GM Reports): sign in as manager, confirm periods/jobs/invoice-run/forecast screens still load, confirm archive/delete on a report period still works. Still needs an actual person to run it. _(added 2026-08-25)_
- **eq-shell** · **Not click-tested live by a person** — every fix this round verified via `pnpm run build` + `tsc -b --force` + production commit-ancestry, not a real signed-in session. Worth a few minutes each: open Access Control → Preview a person for a real Supervisor and confirm the new "what they actually see" block matches the sidebar, and that the grouped/plain-English permission sections and the Group grants/Role overrides line (both added 2026-08-26) read correctly; confirm a non-platform-admin can't see the new grant/revoke control at all; confirm the control actually works end-to-end against a disposable test user, not a real account. _(added 2026-08-25, extended 2026-08-26)_
- **eq-shell** · **Not click-tested live** — no live SKS credentials in this environment. _(added 2026-08-25)_
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment. Worth a real click-through on the Staff list: turn Supervisor on for a test person via the pill, confirm the category popover appears, pick one, confirm it saves. _(added 2026-08-25)_
- **eq-shell** · **None of this round's UI changes have a full click-through beyond what Royce's own screenshots already confirmed** (collapse chevrons, archive-days field existing/saving). The Estimator autocomplete specifically (now sourced from quote history) hasn't been exercised live yet. _(added 2026-08-25)_
- **eq-shell** · **Not click-tested live** — no login credentials this session. Handed Royce the exact steps (Customers page → Convergint → Link site → search "Equinix SY3" → confirm badge/Unlink-only controls → confirm it appears in a Convergint quote's site picker). Not yet confirmed done. _(added 2026-08-25)_
- **eq-shell** · **Cost/charge-rate fix not click-tested live** — verified via `tsc -b --force` and code-path tracing only; local Netlify/Vite dev tooling is documented broken under Node 24 in this repo, and the feature is auth-gated (EQ Ops). Worth a real click-through next time someone edits a quote line's Rate with a Cost already entered. _(added 2026-08-25)_
_…and 228 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 3 | 0d |
| eq-solves-service | ✓ success | 1d ago | 6 | 6d |
| eq-field | ✓ success | 0d ago | 1 | 0d |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 8d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [TypeError: Failed to fetch dynamically imported module: https://core.eq.solution](https://eq-solutions.sentry.io/issues/141714696/) | 37 | 2026-08-21 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 7 | 2026-08-26 |
| eq-shell | [Error: app_data.staff.cards_worker_id pointing at missing jvkn workers: 4](https://eq-solutions.sentry.io/issues/138175643/) | 7 | 2026-08-25 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 4 | 2026-08-26 |
| eq-shell | [Error: Active org_memberships held by non-members: 15](https://eq-solutions.sentry.io/issues/142429897/) | 3 | 2026-08-25 |
| eq-shell | [Error: Unclaimed worker invites past grace period: 0 still valid, 1 expired](https://eq-solutions.sentry.io/issues/142642035/) | 2 | 2026-08-25 |
| eq-field | [TypeError: Failed to fetch](https://eq-solutions.sentry.io/issues/141259049/) | 2 | 2026-08-24 |
| eq-shell | [phone-otp: requested for inactive account](https://eq-solutions.sentry.io/issues/141933696/) | 2 | 2026-08-20 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-26 | eq-shell | [#1630](https://github.com/eq-solutions/eq-shell/pull/1630) feat(customers): let one Site carry multiple project/module codes |
| 2026-08-26 | eq-shell | [#1625](https://github.com/eq-solutions/eq-shell/pull/1625) fix(security): stop staff-active drift sweep from logging out mul |
| 2026-08-26 | eq-shell | [#1629](https://github.com/eq-solutions/eq-shell/pull/1629) chore(drift): allowlist eq_cards_admin_sync_tenant_access — sourc |
| 2026-08-26 | eq-shell | [#1626](https://github.com/eq-solutions/eq-shell/pull/1626) fix(worker-invite): backfill workers.role so canonical sync stops |
| 2026-08-26 | eq-shell | [#1623](https://github.com/eq-solutions/eq-shell/pull/1623) fix(ci): wire CHECK 10 (intentional-anon-read) into the drift-che |
| 2026-08-26 | eq-shell | [#1622](https://github.com/eq-solutions/eq-shell/pull/1622) docs(security): correct stale organisations_anon_bootstrap_read l |
| 2026-08-26 | eq-shell | [#1621](https://github.com/eq-solutions/eq-shell/pull/1621) feat(identity): sync EQ Field roster removal/re-add to Shell tena |
| 2026-08-26 | eq-shell | [#1619](https://github.com/eq-solutions/eq-shell/pull/1619) feat(staff): accept HEIC licence photos on both upload paths |
| 2026-08-26 | eq-shell | [#1618](https://github.com/eq-solutions/eq-shell/pull/1618) fix(security): restore organisations anon bootstrap-read policy ( |
| 2026-08-26 | eq-shell | [#1609](https://github.com/eq-solutions/eq-shell/pull/1609) fix(entity-patch): derive isProd from request Host, not process.e |
| 2026-08-26 | eq-shell | [#1615](https://github.com/eq-solutions/eq-shell/pull/1615) feat(auth): collapse deactivated & expired self-join links by def |
| 2026-08-26 | eq-shell | [#1617](https://github.com/eq-solutions/eq-shell/pull/1617) feat(access-control): per-person sidebar visibility scope |
| 2026-08-26 | eq-shell | [#1616](https://github.com/eq-solutions/eq-shell/pull/1616) fix(auth): thread an already-resolved Cards name into new workers |
| 2026-08-26 | eq-shell | [#1614](https://github.com/eq-solutions/eq-shell/pull/1614) fix(staff): wrap the licence action row so Remove's confirm state |
| 2026-08-26 | eq-shell | [#1613](https://github.com/eq-solutions/eq-shell/pull/1613) fix(cards-api): derive isProd from request Host, not process.env. |
_Showing 15 of 113 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-shell** (287 open) · [eq/pending/eq-shell.md](eq/pending/eq-shell.md)
- **eq-cards** (50 open) · [eq/pending/eq-cards.md](eq/pending/eq-cards.md)
- **eq-field** (149 open) · [eq/pending/eq-field.md](eq/pending/eq-field.md)
- **eq-solves-service** (94 open) · [eq/pending/eq-solves-service.md](eq/pending/eq-solves-service.md)
- **eq-solves-intake** (18 open) · [eq/pending/eq-solves-intake.md](eq/pending/eq-solves-intake.md)
- **eq-design-tokens** (1 open) · [eq/pending/eq-design-tokens.md](eq/pending/eq-design-tokens.md)
- **eq-ui** (2 open) · [eq/pending/eq-ui.md](eq/pending/eq-ui.md)
- **eq-receipts** (4 open) · [eq/pending/eq-receipts.md](eq/pending/eq-receipts.md)
- **eq-context** (30 open) · [eq/pending/eq-context.md](eq/pending/eq-context.md)
- **cross-repo** (187 open) · [eq/pending/cross-repo.md](eq/pending/cross-repo.md)
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
_…and 75 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise. Open splits engineering backlog from Royce's own queue (a confirm, a click-through, a call) — the two used to be counted together here, which made the number look worse than the real engineering backlog actually is; the split matches 'Waiting on you' above._

| File | Lines | Open (eng / you) | Done (unrotated) | Aging 45d+ |
|------|------:|------------------:|------------------:|------------:|
| [eq-shell](eq/pending/eq-shell.md) | 1924 | 204 / 88 | 266 | 47 |
| [eq-cards](eq/pending/eq-cards.md) | 469 | 37 / 16 | 103 | 5 |
| [eq-field](eq/pending/eq-field.md) | 1004 | 115 / 39 | 77 | 27 |
| [eq-solves-service](eq/pending/eq-solves-service.md) | 662 | 73 / 26 | 93 | 23 |
| [eq-solves-intake](eq/pending/eq-solves-intake.md) | 152 | 13 / 6 | 5 | 14 |
| [eq-design-tokens](eq/pending/eq-design-tokens.md) | 23 | 1 / 0 | 0 | 1 |
| [eq-ui](eq/pending/eq-ui.md) | 29 | 2 / 0 | 2 | 0 |
| [eq-receipts](eq/pending/eq-receipts.md) | 44 | 3 / 1 | 0 | 0 |
| [eq-context](eq/pending/eq-context.md) | 263 | 25 / 5 | 27 | 5 |
| [cross-repo](eq/pending/cross-repo.md) | 998 | 144 / 43 | 33 | 53 |
| [sks](eq/pending/sks.md) | 53 | 3 / 5 | 0 | 6 |
| [SKS](sks/pending.md) | 469 | 85 / 12 | 0 | 40 |
| [SKS active](sks/active.md) | 119 | 0 / 0 | 0 | 0 |
| [OPS](ops/pending.md) | 516 | 44 / 4 | 0 | 1 |

## Aging open items (45d+, unconfirmed)

_Open items sitting under a section header this old or older — not necessarily wrong, just gone quiet under its own dated write-up. Worth a look before it reads as done-and-forgotten._

- **eq-shell** (2026-07-11) · **Arm/build the queued fleet bugs** — #736 (invite-users-batch entitlements), #737 (zero-row 404) armed, not yet built. #734 (quote-job-consumer) + #735 (RLS `(select)` wrapping) filed UNARMED — Royce's call to arm. #705 (eq-intake xlsx) DONE this session — see below. _(added 2026-07-11)_
- **eq-shell** (2026-07-11) · **zaap tender tables are now service_role-only** (no `authenticated` tenant policies — the create migration's `field_authed_all_*` never reached zaap). Fine if the EQ app reads them via service_role; add the authenticated tenant policy if Field ever needs authed access there. _(added 2026-07-11)_
- **eq-shell** (2026-07-10) · eq-shell: fix focus-triggered refetch/hydration crash on Field iframe wrapper so spinner doesn't get stuck on tab return _(added 2026-07-10, in progress in separate eq-shell session — task_b2cf81ea)_
- **eq-shell** (2026-07-08) · **EQ Service "session expired, please reconnect" stuck screen — root cause still genuinely unknown.** Two chased theories were investigated and explicitly REFUTED with hard evidence: React error #418 (hydration mismatch) is a dated, known, confirmed-non-blocking noise pattern (2026-07-05 team note, 705 events/14d, essentially every active user) — NOT the cause. A suspected hanging `token-exchange` call was also refuted — real Netlify function logs showed every invocation completing in under 4s with zero errors; the "pending forever" read came from a flaky automated browser tab (same tab independently threw an unrelated CDP "renderer frozen" error). Two chips built on these now-retracted theories (`task_2911c80d`, `task_abbb7fd0`) were already started by Royce before the retraction landed — worth redirecting or discarding. The actual cause of the stuck-reconnect screen is still open. _(added 2026-07-08)_
- **eq-shell** (2026-07-08) · **EQ Service sidebar-header tenant logo clipped** (in `ShellSessionRecovery`'s fallback UI specifically, not the top bar — top bar renders fine live) — chip `task_14031bea` was already started by Royce before this correction landed; built on a stale "top-bar alignment" framing. _(added 2026-07-08)_
- **eq-shell** (2026-07-08) · Core Talent now shows both an `"Electrician"` role (older invoice, 21 Jun) and a `"NSW Licensed Electrician"` role (newer rate card, 1 Jul) — may be the same job under two labels, inflating the weekly-cost table with a stale row. Left for Royce's own sanity-check pass before the Atom agency upload. _(added 2026-07-08)_
- **eq-shell** (2026-07-06) · **No live browser click-through of PR #686's changes** — bulk "All on/off" buttons and the collapsible customer/site grouping have only been typecheck/lint-verified, never clicked in a real browser session. _(added 2026-07-06, needs your call — or hand it to a session with live credentials)_
- **eq-shell** (2026-07-06) · **`field_people` out-of-band regression provenance** — same open question as the already-tracked `field_job_numbers provenance` item below: migration `0158` confirmed ehow's `field_people` was safe as of 2026-07, and no repo migration touched it since, meaning something changed it live outside the One Pipe. Not investigated this session (scope was the fix, not the "who/what" — same pattern, could be the same root cause as the `field_job_numbers` provenance question). _(added 2026-07-06)_
- **eq-shell** (2026-07-04) · **field_job_numbers provenance** — the view was created out-of-band (not originally in a repo migration); who made it + whether other planes need it tracked as `task_0467f68c`. _(added 2026-07-04)_
- **eq-shell** (2026-07-04) · **Favour Perfect first-run config** — switch into it (after one workspace-switch or re-login), configure it, and invite its real customer admin from inside `/favour-perfect/admin/users`. _(added 2026-07-04, needs your call)_
- **eq-shell** (2026-07-04) · **Optional: `reconcile_ledger` tidy for `favour-perfect`** — its `_eq_migrations` ledger has 204 rows incl. 39 null-checksum entries (cruft from a messy apply sequence: an 08:14 reconcile-path run stamped rows then failed; the 08:25 apply finished it). Schema is correct — purely cosmetic. A `reconcile_ledger=true` dispatch scoped to `favour-perfect` would tidy it. _(added 2026-07-04, needs your call)_
- **eq-shell** (2026-07-04) · **Admin-create zero-member gap** — admin "Add tenant" builds member-less, UI-unreachable tenants (no way to add a first user without a hand-inserted membership). Fix (auto-add creator as manager, or an "Add me as admin" button) running as `task_4f5989fb`. _(added 2026-07-04)_
- **eq-shell** (2026-07-04) · **Link the 19 field-enabled SKS sites with no `customer_id`** — Row 29 prestart prefill resolves the customer name only for the 11 (of 30) field-visible ehow sites that have a `customer_id`. The other 19 (Amazon SYD53, Woolworths, Microsoft SYD05/27, Western Sydney Airport, St Vincents, etc.) prefill blank. NOT auto-derivable — `sites.client_name`/`external_customer_id` are null/junk, zero name-matches to `customers.company_name`. Needs a manual ops pass (assign each site its customer in the Customers/Sites editor). Degrades gracefully (blank field) until done. _(added 2026-07-04, needs your call)_
- **eq-shell** (2026-07-04) · **Manual click-through of PR #641 once deployed** — load `/_platform/tenants`, confirm no regression on Provision/Retry/Archive/Reactivate **and** the new hard-delete action from PR #642, and (if a stuck row exists, or one is forced) confirm "Stuck — Cancel" appears only past 20 min and Retry re-provisions cleanly afterward. _(added 2026-07-04)_
- **eq-shell** (2026-07-03) · **Remove worktree `.claude/worktrees/ops-site-create-edit`** — now that #616 is merged, safe to `git -C C:\Projects\eq-shell worktree remove .claude/worktrees/ops-site-create-edit`. _(added 2026-07-03)_
_…and 207 more — see each file's Queue health row above._

## Possible duplicate pending items (unconfirmed)

_Two open items worded similarly enough that they might be the same thing logged twice. Not auto-merged — check both, close or fold one into the other by hand if they really are the same._

- **eq-context** · **Update C:\Projects\.git-credentials** files with new PAT after rotation
  **cross-repo** · **Update C:\Projects\.git-credentials** files with new PAT after rotation _(added 2026-06-28)_

- **eq-context** · **gitleaks pre-commit hook** — prevent PAT exposure in substrate history
  **cross-repo** · **gitleaks pre-commit hook** — prevent PAT exposure in substrate history _(added 2026-06-28)_

- **eq-cards** · **Send Huon** the connection-email reply + before/after graphic. _(needs your call)_
  **cross-repo** · **Send Huon** the connection-email reply + before/after graphic. _(added 2026-07-02)_

## Possible recurring failures (unconfirmed)

_Session logs mention a pattern matching a known failure below, dated after its last recorded occurrence. Not yet counted — if it's real, bump `recurrences` in [failures.md](system/failures.md) and `guard-ratchet.yml` proposes promotion on its own next run._

- **F5** (rung 0) — An ungoverned shadow memory overrode the canonical contract · 1 session since last recorded, most recent [2026-08-16.md](sessions/2026-08-16.md)

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-27 | [eq-field: leave/incident email fixes shipped (v3.5.580), eq-shell entity-patch CORS bug found](sessions/2026-08-27.md) |
| 2026-08-26 | [Close-out of the 2026-08-25 eq-field/eq-shell session](sessions/2026-08-26.md) |
| 2026-08-25 | [Canonical wiring map: jvkn/Shell/Field read-write capabilities, verified live end-to-end](sessions/2026-08-25.md) |
| 2026-08-24 | [SEC-58 (control-plane ledger) and SEC-65 (AUDIT_SB_KEY label) closed](sessions/2026-08-24.md) |
| 2026-08-23 | [Labour-hire live-trial bugs: licence/compliance-pack gap root-caused and fixed (PR #1513), cropping issue diagnosed](sessions/2026-08-23.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-26 19:46 UTC._
