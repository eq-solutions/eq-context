---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-23
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-23 09:24 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-23 09:03 UTC → 2026-08-23 09:24 UTC)

- Merged: eq-shell [#1555](https://github.com/eq-solutions/eq-shell/pull/1555) fix(identity): push date_of_birth/address_* upward; receive 
- Merged: eq-shell [#1547](https://github.com/eq-solutions/eq-shell/pull/1547) docs(security): correct stale mint-supabase-jwt carve-out cl
- Merged: eq-shell [#1540](https://github.com/eq-solutions/eq-shell/pull/1540) fix(staff): resolve the 7 divergent staff/shell login names 
- Merged: eq-shell [#1537](https://github.com/eq-solutions/eq-shell/pull/1537) fix(staff): sync staff record name into the linked Shell log
- Merged: eq-shell [#1535](https://github.com/eq-solutions/eq-shell/pull/1535) fix(security): role-gate + self-approval check on approve_sa
- Merged: eq-shell [#1534](https://github.com/eq-solutions/eq-shell/pull/1534) fix(security): entity-role-gate quote delete/line-item RPCs 
- Merged: eq-shell [#1532](https://github.com/eq-solutions/eq-shell/pull/1532) feat(drift-guard): CHECK 10 -- positive assertion for INTENT
- Merged: eq-shell [#1528](https://github.com/eq-solutions/eq-shell/pull/1528) fix(chunk-loading): catch chunk-load failures that bypass Ch

## ⚠ Needs you (8)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-57 (P1) — An org-wide GitHub App installation (`grok-by-xai`, `repository_selection: all`) · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-61 (P1) — SEC-9's 2026-08-16 closure does not hold: 22 secret-flagged vars across eq-shell · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-63 (P1) — An uninventoried Netlify **account-scope** (team `milmlow`) secret, `SUPABASE_JW · [security-register.md](ops/security-register.md)
- 🔴 **Cron failing** — `index-drift.yml` 2 consecutive scheduled run(s) failed, last success 2026-08-20 · [failures.md](system/failures.md) F11
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-08-23.md](sessions/2026-08-23.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F12: Side-clone reconciliation blind-overwrote a concurrent session's already-pushed shared-fil · possibly recurred in [2026-08-21.md](sessions/2026-08-21.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-08-23.md](sessions/2026-08-23.md) · [failures.md](system/failures.md)

## 🙋 Waiting on you (208)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **eq-shell** · **Not click-tested live** — Zemi's licence confirmed via a direct query replay of the Staff page's own logic, not by opening the actual Staff page in a browser. Worth a 30-second look next time someone's on `core.eq.solutions/sks/staff`. _(added 2026-08-23)_
- **eq-shell** · **Not click-tested live** — no actual compliance-pack download has been run against Conor's/Nelson's real data yet. Worth running one export and checking the new "Pending (Unclaimed)" sheet + zip folder render correctly. _(added 2026-08-23)_
- **eq-shell** · **Add / archive / reactivate / hard-delete still not click-tested live.** Edit IS now click-tested (2026-08-23, Royce's own manager session in the real SKS Field UI, Emergency Contact field on a real person, hard-reload-confirmed both the save and the revert — not just the post-save optimistic UI). The other four actions in this trigger's write surface (`savePersonToSB` add, `archivePersonInSB`/`restorePersonInSB`, hard-delete) are still unverified by an actual UI session.
- **eq-shell** · **Not click-tested live** — both new fixes verified via live grants/policy queries and full CI, not an actual signed-in non-permission-holder attempting either blocked action. _(added 2026-08-23)_
- **eq-shell** · **Not click-tested live** — an Employee's quote list, and confirming they can't open another employee's quote by pasting its ID into the URL. _(added 2026-08-23)_
- **eq-shell** · **Sentry access still not sorted** — both the Sentry MCP connector and Royce's own logged-in Chrome hit an auth wall this session, which is why the exact click-by-click trigger for the reported occurrences couldn't be pinned down with full certainty (the fix covers the whole class of failure regardless of the precise trigger). Worth revisiting once either is authorized. _(added 2026-08-23)_
- **eq-shell** · **Not click-tested live** — verified via eslint/tsc and commit-ancestry against the live deploy, not an actual `?open=<id>` link clicked by a person. Worth confirming next time someone opens a Staff deep-link from the "Ask anything" bar or a Resourcing row click. _(added 2026-08-23)_
- **eq-shell** · **`0258`-`0261` (the 4 ehow-only migrations) still not dispatched** — dispatching each (with `--slug=<tenant>` matching its declared plane) remains explicitly Royce's call. _(added 2026-08-23, narrowed from "none of the 5" — one of the five is now done)_
- **eq-shell** · **Not click-tested live, either claim door** — both #1517 (Shell-join) and #1519 (accept-invite.ts) verified via `tsc -b --force`/eslint and exact commit-ancestry against the live deploy, not an actual claim walked through by a person. Worth confirming once Conor or Nelson claims. _(added 2026-08-23)_
- **eq-shell** · **Not click-tested live** — verified via `tsc -b --force` and eslint (0 new errors), not an actual file landing in a Downloads folder. Worth confirming next time a pack is built — same ask as the still-open 2026-07-28/07-26 "re-download and eyeball" items further down this file. _(added 2026-08-23)_
- **eq-shell** · **None of the at-risk migrations have actually been copied into `supabase/tenant-migrations/` yet** — confirmed live: the directory's newest files are `0256`/`0257`, none of the eq-field migrations. No active dispatch risk today; the guard is preventive for whenever that copy happens. Copying + dispatching remain explicitly Royce's call. _(added 2026-08-23)_
- **eq-shell** · **Consider a lightweight confirmation of what the client-RFQ autofill actually filled in** — today it silently overwrites the create-form's fields with no summary. Not a correctness gap (nothing saves until "Create Quote," so the form itself is the review step) but possibly worth it if the parse is often wrong in practice — needs Royce's read on that, not a guess. _(added 2026-08-20)_
_…and 196 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 0 | — |
| eq-solves-service | ✓ success | 0d ago | 2 | 2d |
| eq-field | ✓ success | 0d ago | 1 | 0d |
| eq-cards | ✓ success | 0d ago | 1 | 0d |
| eq-solves-intake | ✓ success | 5d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [TypeError: Failed to fetch dynamically imported module: https://core.eq.solution](https://eq-solutions.sentry.io/issues/141714696/) | 37 | 2026-08-21 |
| eq-shell | [Error: app_data.staff.cards_worker_id pointing at missing jvkn workers: 4](https://eq-solutions.sentry.io/issues/138175643/) | 5 | 2026-08-22 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 4 | 2026-08-20 |
| eq-shell | [phone-otp: requested for inactive account](https://eq-solutions.sentry.io/issues/141933696/) | 2 | 2026-08-20 |
| eq-shell | [EQ Field handoff auto-recovery (timeout)](https://eq-solutions.sentry.io/issues/141463602/) | 2 | 2026-08-20 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 2 | 2026-08-19 |
| eq-shell | [Degraded UI Performance](https://eq-solutions.sentry.io/issues/141127922/) | 2 | 2026-08-18 |
| eq-solves-service | [Error: An unexpected response was received from the server.](https://eq-solutions.sentry.io/issues/139724869/) | 1 | 2026-08-09 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-23 | eq-shell | [#1547](https://github.com/eq-solutions/eq-shell/pull/1547) docs(security): correct stale mint-supabase-jwt carve-out claim ( |
| 2026-08-23 | eq-shell | [#1555](https://github.com/eq-solutions/eq-shell/pull/1555) fix(identity): push date_of_birth/address_* upward; receive Field |
| 2026-08-23 | eq-shell | [#1553](https://github.com/eq-solutions/eq-shell/pull/1553) fix(field-people): close 4 role-check gaps on field_people_iud +  |
| 2026-08-23 | eq-shell | [#1556](https://github.com/eq-solutions/eq-shell/pull/1556) fix(entity-patch): scope asset edits to equipment-register rows o |
| 2026-08-23 | eq-shell | [#1554](https://github.com/eq-solutions/eq-shell/pull/1554) fix(security): reattach field_people_iud trigger + close 2 permis |
| 2026-08-23 | eq-shell | [#1552](https://github.com/eq-solutions/eq-shell/pull/1552) fix(equipment): hide Archive/Delete bulk actions from view-only r |
| 2026-08-23 | eq-shell | [#1551](https://github.com/eq-solutions/eq-shell/pull/1551) feat(labour-hire): include pending unclaimed candidates in compli |
| 2026-08-23 | eq-shell | [#1550](https://github.com/eq-solutions/eq-shell/pull/1550) fix(security): sync staff deactivation to the linked Shell login |
| 2026-08-23 | eq-shell | [#1549](https://github.com/eq-solutions/eq-shell/pull/1549) docs: sprint plan for the access-control sweep follow-up items |
| 2026-08-23 | eq-shell | [#1548](https://github.com/eq-solutions/eq-shell/pull/1548) feat(identity): alert when a worker's org_membership goes missing |
| 2026-08-23 | eq-shell | [#1546](https://github.com/eq-solutions/eq-shell/pull/1546) fix(security): close GM Reports' direct-API bypass, correct destr |
| 2026-08-23 | eq-shell | [#1545](https://github.com/eq-solutions/eq-shell/pull/1545) fix(security): staff_conversations RLS never re-gated who may wri |
| 2026-08-23 | eq-shell | [#1544](https://github.com/eq-solutions/eq-shell/pull/1544) fix(identity): enforce the control-layer-wins rule — lock bypass, |
| 2026-08-23 | eq-shell | [#1543](https://github.com/eq-solutions/eq-shell/pull/1543) fix(auth): correct #1542's client + close self-join name gap |
| 2026-08-23 | eq-shell | [#1539](https://github.com/eq-solutions/eq-shell/pull/1539) feat(quotes): own-quotes-only row scoping via new quotes.view_all |
_Showing 15 of 118 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-shell** (257 open) · [eq/pending/eq-shell.md](eq/pending/eq-shell.md)
- **eq-cards** (57 open) · [eq/pending/eq-cards.md](eq/pending/eq-cards.md)
- **eq-field** (126 open) · [eq/pending/eq-field.md](eq/pending/eq-field.md)
- **eq-solves-service** (93 open) · [eq/pending/eq-solves-service.md](eq/pending/eq-solves-service.md)
- **eq-solves-intake** (17 open) · [eq/pending/eq-solves-intake.md](eq/pending/eq-solves-intake.md)
- **eq-design-tokens** (1 open) · [eq/pending/eq-design-tokens.md](eq/pending/eq-design-tokens.md)
- **eq-ui** (2 open) · [eq/pending/eq-ui.md](eq/pending/eq-ui.md)
- **eq-receipts** (4 open) · [eq/pending/eq-receipts.md](eq/pending/eq-receipts.md)
- **eq-context** (28 open) · [eq/pending/eq-context.md](eq/pending/eq-context.md)
- **cross-repo** (183 open) · [eq/pending/cross-repo.md](eq/pending/cross-repo.md)
- **sks** (8 open) · [eq/pending/sks.md](eq/pending/sks.md)

## Pending (SKS)

- **A second, unidentified path also creates blank-name logins** — proven by timing, not guessed: Todd Wilson's and David Boyd's shell logins were created 7 weeks *after* their Cards approval, which rules out the path just patched as their cause. Spawned as background task `task_d904d388`, Royce started it in a separate session; running independently, not yet reported back as of this session's close. _(added 2026-08-23)_
- **Not verified live by a person** — the specific pill-click behavior needs a real Core+SKS session to exercise (Teams is SKS-only, gated behind Core auth, not reachable from a standalone deploy-preview session). Confirmed the fix mirrors an already-shipped, working code pattern (the crew-supervisor picker), not watched working fresh. _(added 2026-08-23)_
- **SKS's own number, for reference: 6 of 32 active SKS members are currently missing White Card** — visible today in Shell's Training Matrix; nothing blocks them from working while missing it (soft-flag by design, not an oversight). Worth a look if Royce wants a harder rule for SKS specifically. _(added 2026-08-19)_
- **A reported roster-grid "alignment" issue (one person's row looked off) couldn't be reproduced from the code** — most likely just placeholder text in blank cells reading like real data at a glance, not an actual bug, but left open rather than guessed at. _(added 2026-08-19)_
- **Still not applied to the live database — checked directly, and Royce turned down the shortcut that would have unblocked it today.** Confirmed merging the PR didn't secretly switch it on. Turning it on for real right now would lock the people who haven't signed in yet out of their own timesheet and leave the moment they do, since the fix depends on their login already being linked to their staff record — 37 of 83 active SKS staff, checked again today. A workaround exists (let just those specific people keep today's wider access until they sign in, instead of holding up everyone else) but Royce said no — waiting for them to actually sign in through the real onboarding process instead, however long that takes. _(added 2026-08-16, decision confirmed 2026-08-16)_
- **The disposable EQ-side tenant doesn't have this fix** — lower priority, since that tenant holds no real data, but the identical gap exists there too and needs some prerequisite pieces built first before it can be ported. _(added 2026-08-16)_
- **Run the first real weekly export/import test** — SKS NSW Labour → Export Schedule CSV → EQ Field (logged in as the SKS org) → Import Schedule CSV. Discussed and confirmed safe; not actually run this session. _(added 2026-08-14)_
- **Deactivate the two stale site rows in ehow** — `Erilyan` (`site_id 6c221319…`, code EC6) and `Microsoft SYD27` (`site_id 7fb2d662…`, code SYD27). Single-column `active=false` flip each, no code change, no deploy — Royce hasn't given the explicit go to execute it yet. _(added 2026-08-14)_
- **~7 SKS staff missing from EQ Field's staff table** (hired since the 5 Jul snapshot): Ahmed Masaud, Amir Farid, Callum Treharne, Jhon Jairo Velasquez Meneses, Nabeel Hussain, Paul Bolger, Timothy Sue — plus a handful of name-string mismatches (e.g. "Bruno Pedrosa" vs "Bruno Vita Pedrosa", "Jose Quintanilla" vs "Jose Luis Quintanilla Rodriguez"). Royce said he'll manage this himself via EQ Field's People admin. _(added 2026-08-14)_
- **Leave sync parked deliberately** — an imported leave code lands on `schedule_entries.leave_type` directly, not in `app_data.leave_requests`, so it displays but carries no approver/audit trail. Royce explicitly scoped this session to roster only; leave is its own future task. _(added 2026-08-14)_
_…and 73 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise. Open splits engineering backlog from Royce's own queue (a confirm, a click-through, a call) — the two used to be counted together here, which made the number look worse than the real engineering backlog actually is; the split matches 'Waiting on you' above._

| File | Lines | Open (eng / you) | Done (unrotated) | Aging 45d+ |
|------|------:|------------------:|------------------:|------------:|
| [eq-shell](eq/pending/eq-shell.md) | 1661 | 189 / 74 | 206 | 44 |
| [eq-cards](eq/pending/eq-cards.md) | 418 | 44 / 13 | 45 | 8 |
| [eq-field](eq/pending/eq-field.md) | 830 | 100 / 28 | 52 | 15 |
| [eq-solves-service](eq/pending/eq-solves-service.md) | 644 | 72 / 25 | 87 | 20 |
| [eq-solves-intake](eq/pending/eq-solves-intake.md) | 152 | 13 / 6 | 5 | 14 |
| [eq-design-tokens](eq/pending/eq-design-tokens.md) | 23 | 1 / 0 | 0 | 1 |
| [eq-ui](eq/pending/eq-ui.md) | 29 | 2 / 0 | 2 | 0 |
| [eq-receipts](eq/pending/eq-receipts.md) | 44 | 3 / 1 | 0 | 0 |
| [eq-context](eq/pending/eq-context.md) | 246 | 24 / 4 | 25 | 5 |
| [cross-repo](eq/pending/cross-repo.md) | 958 | 142 / 42 | 23 | 40 |
| [sks](eq/pending/sks.md) | 53 | 3 / 5 | 0 | 6 |
| [SKS](sks/pending.md) | 484 | 83 / 14 | 8 | 25 |
| [SKS active](sks/active.md) | 108 | 0 / 0 | 0 | 0 |
| [OPS](ops/pending.md) | 509 | 44 / 3 | 0 | 1 |

## Aging open items (45d+, unconfirmed)

_Open items sitting under a section header this old or older — not necessarily wrong, just gone quiet under its own dated write-up. Worth a look before it reads as done-and-forgotten._

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
- **eq-shell** (2026-07-03) · **Commit eq-intake/CLAUDE.md** — left untracked (eq-intake tree dirty on `feat/armada-sprint-polish`); fold into whichever branch lands next. _(added 2026-07-03)_
- **eq-shell** (2026-07-03) · **Coordinated `--reconcile-ledger`** — after go-live settles: renames/stamps the 16 bare 0103–0116/0141 rows, drops `057` + go-live hand rows. Run only WITH eq-intake (their numbering reads the live ledger). _(added 2026-07-03)_
- **eq-shell** (2026-07-03) · **Tenant-migrate run 28638433643 was dispatched then CANCELLED** — dispatched from the #608 branch on the stale premise that a live apply was needed to green the gate; the newer session-state showed #608 is code-only, and applying unmerged branch migrations risks checksum/ledger mess. Nothing was applied (cancelled at the production-approval gate, never approved). Post-merge apply of 0155/0156 from main is the normal One Pipe dispatch — separate explicit call. _(added 2026-07-03, needs your call)_
_…and 164 more — see each file's Queue health row above._

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
| 2026-08-23 | [Labour-hire live-trial bugs: licence/compliance-pack gap root-caused and fixed (PR #1513), cropping issue diagnosed](sessions/2026-08-23.md) |
| 2026-08-21 | [eq-service worktree/branch/stash graveyard cleared: 8 branches, 23 folders, 3 stashes, all confirmed already-shipped before removal](sessions/2026-08-21.md) |
| 2026-08-20 | [Staff page load-time root-caused: staff-bootstrap missing from the keep-warm ping](sessions/2026-08-20.md) |
| 2026-08-19 | [Cards iframe Web Share fix (eq-shell) + Wallet banner repeat fix (eq-cards)](sessions/2026-08-19.md) |
| 2026-08-18 | [Fixed a real bug behind a suspected-hardcoded-path guard.js gate report](sessions/2026-08-18.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-23 09:24 UTC._
