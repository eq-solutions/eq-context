---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-24
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-24 11:19 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-24 11:10 UTC → 2026-08-24 11:19 UTC)

- Merged: eq-shell [#1561](https://github.com/eq-solutions/eq-shell/pull/1561) docs(security): close SEC-58 — control-plane ledger 54-file 
- Merged: eq-shell [#1560](https://github.com/eq-solutions/eq-shell/pull/1560) feat(staff): show pending labour-hire credentials on the Sta
- Merged: eq-shell [#1555](https://github.com/eq-solutions/eq-shell/pull/1555) fix(identity): push date_of_birth/address_* upward; receive 
- Merged: eq-shell [#1554](https://github.com/eq-solutions/eq-shell/pull/1554) fix(security): reattach field_people_iud trigger + close 2 p
- Merged: eq-shell [#1552](https://github.com/eq-solutions/eq-shell/pull/1552) fix(equipment): hide Archive/Delete bulk actions from view-o
- Merged: eq-shell [#1550](https://github.com/eq-solutions/eq-shell/pull/1550) fix(security): sync staff deactivation to the linked Shell l
- Merged: eq-shell [#1549](https://github.com/eq-solutions/eq-shell/pull/1549) docs: sprint plan for the access-control sweep follow-up ite
- Merged: eq-shell [#1548](https://github.com/eq-solutions/eq-shell/pull/1548) feat(identity): alert when a worker's org_membership goes mi

## ⚠ Needs you (6)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-57 (P1) — An org-wide GitHub App installation (`grok-by-xai`, `repository_selection: all`) · [security-register.md](ops/security-register.md)
- 🔴 **Cron failing** — `index-drift.yml` 3 consecutive scheduled run(s) failed, last success 2026-08-20 · [failures.md](system/failures.md) F11
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-08-23.md](sessions/2026-08-23.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F12: Side-clone reconciliation blind-overwrote a concurrent session's already-pushed shared-fil · possibly recurred in [2026-08-21.md](sessions/2026-08-21.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-08-23.md](sessions/2026-08-23.md) · [failures.md](system/failures.md)

## 🙋 Waiting on you (218)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **eq-shell** · **Not click-tested for real user-perceived speed** — both fixes verified via commit-ancestry + deploy state, not a fresh Staff-page load timed by a person. _(added 2026-08-24)_
- **eq-shell** · **Nelson Sareto's Resend click reproduced the identical duplicate-key error after the fix was confirmed live.** No fresh Postgres duplicate-key log entry appears after the deploy's publish time, and Nelson's `worker_invites` row is unchanged — pointing toward a stale/leftover error banner rather than a genuinely new failure, but **not confirmed**. Asked Royce to refresh and retry; no response yet. If it still fails post-refresh: leading unverified hypothesis is the new `unclaimed` SELECT's `error` being silently discarded, falling through to the old broken `INSERT` path — needs Netlify function-log evidence or a defensive fix (surface `unclaimedErr` explicitly). _(added 2026-08-24)_
- **eq-shell** · **S2 (sprint doc) still open** — `entity-actions.ts`/`entity-patch.ts` gate asset writes on `entity.edit`/`entity.delete` (the CRM tier) rather than `equipment.edit`/`equipment.view`, aligned by coincidence today, not design. Needs Royce's call: re-point the keys, or document the CRM-tiering as deliberate. _(added 2026-08-23)_
- **eq-shell** · **S6 (sprint doc), now larger** — not click-tested live: the original two fixes (`staff_conversations`, GM Reports) plus this round's three (`invite-users-batch.ts`'s guard, both Intake fixes). All verified via live grants/policy/function-body queries and full CI, not an actual signed-in session attempting the blocked action. _(added 2026-08-23)_
- **eq-shell** · **Not click-tested live** — verified via the deploy's exact commit match, not by anyone actually opening `core.eq.solutions/sks/staff` and looking at Conor's/Nelson's rows. _(added 2026-08-23)_
- **eq-shell** · **Add and hard-delete still not click-tested live; restore's own bugs are now believed fully fixed but still awaits its first actual successful click.** Edit confirmed 2026-08-23 (Royce's own manager session in the real SKS Field UI, Emergency Contact field on a real person, hard-reload-confirmed both the save and the revert — not just the post-save optimistic UI). Archive confirmed 2026-08-23 (Royce archived a real test person, "Jordan Sample," on the SKS Field Contacts page — verified via direct DB query: `active` flipped to `false` within 25 seconds of the click). Restore itself was live-tested 2026-08-24 and found broken twice more, both now fixed (see the field_people_iud() section below for both). Still unverified by an actual UI session: `savePersonToSB` (add), `restorePersonInSB` (restore — underlying bugs fixed, pending a real click), hard-delete.
- **eq-shell** · **Not yet click-tested live** — job_title, structured emergency contact, and the upward push all need a real edit on a linked SKS person to confirm end-to-end. Tracked in `eq/pending/eq-field.md`. Full detail: `eq/changelog/eq-shell.md`, `sessions/2026-08-24.md`. _(added 2026-08-24)_
- **eq-shell** · **Not click-tested live** — both new fixes verified via live grants/policy queries and full CI, not an actual signed-in non-permission-holder attempting either blocked action. _(added 2026-08-23)_
- **eq-shell** · **Not click-tested live** — an Employee's quote list, and confirming they can't open another employee's quote by pasting its ID into the URL. _(added 2026-08-23)_
- **eq-shell** · **Sentry access still not sorted** — both the Sentry MCP connector and Royce's own logged-in Chrome hit an auth wall this session, which is why the exact click-by-click trigger for the reported occurrences couldn't be pinned down with full certainty (the fix covers the whole class of failure regardless of the precise trigger). Worth revisiting once either is authorized. _(added 2026-08-23)_
- **eq-shell** · **Not click-tested live** — verified via eslint/tsc and commit-ancestry against the live deploy, not an actual `?open=<id>` link clicked by a person. Worth confirming next time someone opens a Staff deep-link from the "Ask anything" bar or a Resourcing row click. _(added 2026-08-23)_
- **eq-shell** · **`0258`-`0261` (the 4 ehow-only migrations) still not dispatched** — dispatching each (with `--slug=<tenant>` matching its declared plane) remains explicitly Royce's call. _(added 2026-08-23, narrowed from "none of the 5" — one of the five is now done)_
_…and 206 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 0 | — |
| eq-solves-service | ✓ success | 0d ago | 6 | 4d |
| eq-field | ✓ success | 0d ago | 1 | 0d |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 6d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [TypeError: Failed to fetch dynamically imported module: https://core.eq.solution](https://eq-solutions.sentry.io/issues/141714696/) | 37 | 2026-08-21 |
| eq-shell | [Error: app_data.staff.cards_worker_id pointing at missing jvkn workers: 4](https://eq-solutions.sentry.io/issues/138175643/) | 5 | 2026-08-23 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 4 | 2026-08-20 |
| eq-shell | [phone-otp: requested for inactive account](https://eq-solutions.sentry.io/issues/141933696/) | 2 | 2026-08-20 |
| eq-shell | [EQ Field handoff auto-recovery (timeout)](https://eq-solutions.sentry.io/issues/141463602/) | 2 | 2026-08-20 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 2 | 2026-08-19 |
| eq-shell | [Degraded UI Performance](https://eq-solutions.sentry.io/issues/141127922/) | 2 | 2026-08-18 |
| eq-shell | [Error: Active org_memberships held by non-members: 14](https://eq-solutions.sentry.io/issues/142429897/) | 1 | 2026-08-23 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-24 | eq-shell | [#1575](https://github.com/eq-solutions/eq-shell/pull/1575) record(access): backfill Field access for nine Cards-door claims |
| 2026-08-24 | eq-shell | [#1574](https://github.com/eq-solutions/eq-shell/pull/1574) feat(onboarding): chase unclaimed invites, and explain the login  |
| 2026-08-24 | eq-shell | [#1573](https://github.com/eq-solutions/eq-shell/pull/1573) feat(staff): surface mobilisation readiness on the staff list |
| 2026-08-24 | eq-shell | [#1572](https://github.com/eq-solutions/eq-shell/pull/1572) fix(field-people): job_title dead-write + emergency contact struc |
| 2026-08-24 | eq-shell | [#1571](https://github.com/eq-solutions/eq-shell/pull/1571) fix(field-people): stamp activated_by/activated_at on reactivatio |
| 2026-08-24 | eq-shell | [#1570](https://github.com/eq-solutions/eq-shell/pull/1570) perf(token-exchange): bound the audit-log write |
| 2026-08-24 | eq-shell | [#1569](https://github.com/eq-solutions/eq-shell/pull/1569) feat(migrate-tenants): warn on shared cross-repo function replace |
| 2026-08-24 | eq-shell | [#1568](https://github.com/eq-solutions/eq-shell/pull/1568) docs(security): SEC-60 status update |
| 2026-08-24 | eq-shell | [#1567](https://github.com/eq-solutions/eq-shell/pull/1567) fix(field-people): restore identity push dropped by 0270/0271 |
| 2026-08-24 | eq-shell | [#1566](https://github.com/eq-solutions/eq-shell/pull/1566) docs(security): SEC-63 status update |
| 2026-08-24 | eq-shell | [#1565](https://github.com/eq-solutions/eq-shell/pull/1565) docs(security): mark SEC-61 closed in the sprint doc |
| 2026-08-24 | eq-shell | [#1564](https://github.com/eq-solutions/eq-shell/pull/1564) perf(warm-ping): warm the tenant-client cache, not just the conta |
| 2026-08-24 | eq-shell | [#1563](https://github.com/eq-solutions/eq-shell/pull/1563) docs(security): sprint doc for SEC-61/SEC-63/SEC-60 |
| 2026-08-24 | eq-solves-service | [#809](https://github.com/eq-solutions/eq-service/pull/809) fix(security): close anon access on get_assets_for_grouping + get |
| 2026-08-24 | eq-field | [#769](https://github.com/eq-solutions/eq-field/pull/769) v3.5.550 — Edit Person: reject a locked birthday edit instead of  |
_Showing 15 of 119 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-shell** (269 open) · [eq/pending/eq-shell.md](eq/pending/eq-shell.md)
- **eq-cards** (57 open) · [eq/pending/eq-cards.md](eq/pending/eq-cards.md)
- **eq-field** (127 open) · [eq/pending/eq-field.md](eq/pending/eq-field.md)
- **eq-solves-service** (96 open) · [eq/pending/eq-solves-service.md](eq/pending/eq-solves-service.md)
- **eq-solves-intake** (17 open) · [eq/pending/eq-solves-intake.md](eq/pending/eq-solves-intake.md)
- **eq-design-tokens** (1 open) · [eq/pending/eq-design-tokens.md](eq/pending/eq-design-tokens.md)
- **eq-ui** (2 open) · [eq/pending/eq-ui.md](eq/pending/eq-ui.md)
- **eq-receipts** (4 open) · [eq/pending/eq-receipts.md](eq/pending/eq-receipts.md)
- **eq-context** (30 open) · [eq/pending/eq-context.md](eq/pending/eq-context.md)
- **cross-repo** (184 open) · [eq/pending/cross-repo.md](eq/pending/cross-repo.md)
- **sks** (8 open) · [eq/pending/sks.md](eq/pending/sks.md)

## Pending (SKS)

- **Affects 45 of 81 active SKS staff** (everyone Cards-linked with no wizard-entered full date of birth) — fixed going forward, but nobody's birthday has actually been re-entered yet. No action needed unless Royce wants a nudge to re-save. _(added 2026-08-24)_
- **Aiden's own birthday (18 Feb) was tested then reverted to blank** — unclear if that's his real date or just what was typed while reproducing the bug; needs a real re-save to confirm either way. Separately, his record still carries the *earlier* session's own trial data (job title, emergency contact, start date) that was meant to be trial-then-undo and never was — untouched by this session, still open. _(added 2026-08-24)_
- **A second, unidentified path also creates blank-name logins** — proven by timing, not guessed: Todd Wilson's and David Boyd's shell logins were created 7 weeks *after* their Cards approval, which rules out the path just patched as their cause. Spawned as background task `task_d904d388`, Royce started it in a separate session; running independently, not yet reported back as of this session's close. _(added 2026-08-23)_
- **Not verified live by a person** — the specific pill-click behavior needs a real Core+SKS session to exercise (Teams is SKS-only, gated behind Core auth, not reachable from a standalone deploy-preview session). Confirmed the fix mirrors an already-shipped, working code pattern (the crew-supervisor picker), not watched working fresh. _(added 2026-08-23)_
- **SKS's own number, for reference: 6 of 32 active SKS members are currently missing White Card** — visible today in Shell's Training Matrix; nothing blocks them from working while missing it (soft-flag by design, not an oversight). Worth a look if Royce wants a harder rule for SKS specifically. _(added 2026-08-19)_
- **A reported roster-grid "alignment" issue (one person's row looked off) couldn't be reproduced from the code** — most likely just placeholder text in blank cells reading like real data at a glance, not an actual bug, but left open rather than guessed at. _(added 2026-08-19)_
- **Still not applied to the live database — checked directly, and Royce turned down the shortcut that would have unblocked it today.** Confirmed merging the PR didn't secretly switch it on. Turning it on for real right now would lock the people who haven't signed in yet out of their own timesheet and leave the moment they do, since the fix depends on their login already being linked to their staff record — 37 of 83 active SKS staff, checked again today. A workaround exists (let just those specific people keep today's wider access until they sign in, instead of holding up everyone else) but Royce said no — waiting for them to actually sign in through the real onboarding process instead, however long that takes. _(added 2026-08-16, decision confirmed 2026-08-16)_
- **The disposable EQ-side tenant doesn't have this fix** — lower priority, since that tenant holds no real data, but the identical gap exists there too and needs some prerequisite pieces built first before it can be ported. _(added 2026-08-16)_
- **Run the first real weekly export/import test** — SKS NSW Labour → Export Schedule CSV → EQ Field (logged in as the SKS org) → Import Schedule CSV. Discussed and confirmed safe; not actually run this session. _(added 2026-08-14)_
- **Deactivate the two stale site rows in ehow** — `Erilyan` (`site_id 6c221319…`, code EC6) and `Microsoft SYD27` (`site_id 7fb2d662…`, code SYD27). Single-column `active=false` flip each, no code change, no deploy — Royce hasn't given the explicit go to execute it yet. _(added 2026-08-14)_
_…and 75 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise. Open splits engineering backlog from Royce's own queue (a confirm, a click-through, a call) — the two used to be counted together here, which made the number look worse than the real engineering backlog actually is; the split matches 'Waiting on you' above._

| File | Lines | Open (eng / you) | Done (unrotated) | Aging 45d+ |
|------|------:|------------------:|------------------:|------------:|
| [eq-shell](eq/pending/eq-shell.md) | 1723 | 193 / 78 | 221 | 44 |
| [eq-cards](eq/pending/eq-cards.md) | 431 | 44 / 14 | 49 | 8 |
| [eq-field](eq/pending/eq-field.md) | 836 | 101 / 28 | 51 | 17 |
| [eq-solves-service](eq/pending/eq-solves-service.md) | 662 | 73 / 26 | 93 | 20 |
| [eq-solves-intake](eq/pending/eq-solves-intake.md) | 152 | 13 / 6 | 5 | 14 |
| [eq-design-tokens](eq/pending/eq-design-tokens.md) | 23 | 1 / 0 | 0 | 1 |
| [eq-ui](eq/pending/eq-ui.md) | 29 | 2 / 0 | 2 | 0 |
| [eq-receipts](eq/pending/eq-receipts.md) | 44 | 3 / 1 | 0 | 0 |
| [eq-context](eq/pending/eq-context.md) | 263 | 25 / 5 | 27 | 5 |
| [cross-repo](eq/pending/cross-repo.md) | 977 | 143 / 42 | 28 | 40 |
| [sks](eq/pending/sks.md) | 53 | 3 / 5 | 0 | 6 |
| [SKS](sks/pending.md) | 484 | 85 / 15 | 5 | 25 |
| [SKS active](sks/active.md) | 119 | 0 / 0 | 0 | 0 |
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
_…and 166 more — see each file's Queue health row above._

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
| 2026-08-24 | [SEC-58 (control-plane ledger) and SEC-65 (AUDIT_SB_KEY label) closed](sessions/2026-08-24.md) |
| 2026-08-23 | [Labour-hire live-trial bugs: licence/compliance-pack gap root-caused and fixed (PR #1513), cropping issue diagnosed](sessions/2026-08-23.md) |
| 2026-08-21 | [eq-service worktree/branch/stash graveyard cleared: 8 branches, 23 folders, 3 stashes, all confirmed already-shipped before removal](sessions/2026-08-21.md) |
| 2026-08-20 | [Staff page load-time root-caused: staff-bootstrap missing from the keep-warm ping](sessions/2026-08-20.md) |
| 2026-08-19 | [Cards iframe Web Share fix (eq-shell) + Wallet banner repeat fix (eq-cards)](sessions/2026-08-19.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-24 11:19 UTC._
