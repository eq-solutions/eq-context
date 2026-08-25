---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-25
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-25 10:47 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-25 10:39 UTC → 2026-08-25 10:47 UTC)

- Merged: eq-shell [#1594](https://github.com/eq-solutions/eq-shell/pull/1594) chore(deps): bump @eq-solutions/roles to v2.7.5
- Merged: eq-shell [#1580](https://github.com/eq-solutions/eq-shell/pull/1580) feat(sites): surface internal contacts on the field_sites vi
- Merged: eq-shell [#1578](https://github.com/eq-solutions/eq-shell/pull/1578) fix(field-job-numbers): prefer site name over code in Ops-so
- Merged: eq-shell [#1575](https://github.com/eq-solutions/eq-shell/pull/1575) record(access): backfill Field access for nine Cards-door cl
- Merged: eq-shell [#1573](https://github.com/eq-solutions/eq-shell/pull/1573) feat(staff): surface mobilisation readiness on the staff lis
- Merged: eq-shell [#1570](https://github.com/eq-solutions/eq-shell/pull/1570) perf(token-exchange): bound the audit-log write
- Merged: eq-shell [#1569](https://github.com/eq-solutions/eq-shell/pull/1569) feat(migrate-tenants): warn on shared cross-repo function re
- Merged: eq-shell [#1568](https://github.com/eq-solutions/eq-shell/pull/1568) docs(security): SEC-60 status update

## ⚠ Needs you (7)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-57 (P1) — An org-wide GitHub App installation (`grok-by-xai`, `repository_selection: all`) · [security-register.md](ops/security-register.md)
- 🔴 **Cron failing** — `index-drift.yml` 4 consecutive scheduled run(s) failed, last success 2026-08-20 · [failures.md](system/failures.md) F11
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-08-23.md](sessions/2026-08-23.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F9: Concurrent-session git races corrupt the shared eq-context checkout · possibly recurred in [2026-08-25.md](sessions/2026-08-25.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F12: Side-clone reconciliation blind-overwrote a concurrent session's already-pushed shared-fil · possibly recurred in [2026-08-21.md](sessions/2026-08-21.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-08-25.md](sessions/2026-08-25.md) · [failures.md](system/failures.md)

## 🙋 Waiting on you (226)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **eq-shell** · **Not click-tested live** — no live SKS credentials in this environment. _(added 2026-08-25)_
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment. Worth a real click-through on the Staff list: turn Supervisor on for a test person via the pill, confirm the category popover appears, pick one, confirm it saves. _(added 2026-08-25)_
- **eq-shell** · **None of this round's UI changes have a full click-through beyond what Royce's own screenshots already confirmed** (collapse chevrons, archive-days field existing/saving). The Estimator autocomplete specifically (now sourced from quote history) hasn't been exercised live yet. _(added 2026-08-25)_
- **eq-shell** · **Not click-tested live** — no login credentials this session. Handed Royce the exact steps (Customers page → Convergint → Link site → search "Equinix SY3" → confirm badge/Unlink-only controls → confirm it appears in a Convergint quote's site picker). Not yet confirmed done. _(added 2026-08-25)_
- **eq-shell** · **Cost/charge-rate fix not click-tested live** — verified via `tsc -b --force` and code-path tracing only; local Netlify/Vite dev tooling is documented broken under Node 24 in this repo, and the feature is auth-gated (EQ Ops). Worth a real click-through next time someone edits a quote line's Rate with a Cost already entered. _(added 2026-08-25)_
- **eq-shell** · **Not click-tested for real user-perceived speed** — both fixes verified via commit-ancestry + deploy state, not a fresh Staff-page load timed by a person. _(added 2026-08-24)_
- **eq-shell** · **Nelson Sareto's Resend click reproduced the identical duplicate-key error after the fix was confirmed live.** No fresh Postgres duplicate-key log entry appears after the deploy's publish time, and Nelson's `worker_invites` row is unchanged — pointing toward a stale/leftover error banner rather than a genuinely new failure, but **not confirmed**. Asked Royce to refresh and retry; no response yet. If it still fails post-refresh: leading unverified hypothesis is the new `unclaimed` SELECT's `error` being silently discarded, falling through to the old broken `INSERT` path — needs Netlify function-log evidence or a defensive fix (surface `unclaimedErr` explicitly). _(added 2026-08-24)_
- **eq-shell** · **S2 (sprint doc) still open** — `entity-actions.ts`/`entity-patch.ts` gate asset writes on `entity.edit`/`entity.delete` (the CRM tier) rather than `equipment.edit`/`equipment.view`, aligned by coincidence today, not design. Needs Royce's call: re-point the keys, or document the CRM-tiering as deliberate. _(added 2026-08-23)_
- **eq-shell** · **S6 (sprint doc), now larger** — not click-tested live: the original two fixes (`staff_conversations`, GM Reports) plus this round's three (`invite-users-batch.ts`'s guard, both Intake fixes). All verified via live grants/policy/function-body queries and full CI, not an actual signed-in session attempting the blocked action. _(added 2026-08-23)_
- **eq-shell** · **Not click-tested live** — verified via the deploy's exact commit match, not by anyone actually opening `core.eq.solutions/sks/staff` and looking at Conor's/Nelson's rows. _(added 2026-08-23)_
- **eq-shell** · **Add and hard-delete still not click-tested live; restore's own bugs are now believed fully fixed but still awaits its first actual successful click.** Edit confirmed 2026-08-23 (Royce's own manager session in the real SKS Field UI, Emergency Contact field on a real person, hard-reload-confirmed both the save and the revert — not just the post-save optimistic UI). Archive confirmed 2026-08-23 (Royce archived a real test person, "Jordan Sample," on the SKS Field Contacts page — verified via direct DB query: `active` flipped to `false` within 25 seconds of the click). Restore itself was live-tested 2026-08-24 and found broken twice more, both now fixed (see the field_people_iud() section below for both). Still unverified by an actual UI session: `savePersonToSB` (add), `restorePersonInSB` (restore — underlying bugs fixed, pending a real click), hard-delete.
- **eq-shell** · **Not yet click-tested live** — job_title, structured emergency contact, and the upward push all need a real edit on a linked SKS person to confirm end-to-end. Tracked in `eq/pending/eq-field.md`. Full detail: `eq/changelog/eq-shell.md`, `sessions/2026-08-24.md`. _(added 2026-08-24)_
_…and 214 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 4 | 0d |
| eq-solves-service | ✓ success | 1d ago | 6 | 4d |
| eq-field | ✓ success | 0d ago | 1 | 0d |
| eq-cards | ✓ success | 0d ago | 3 | 0d |
| eq-solves-intake | ✓ success | 7d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [TypeError: Failed to fetch dynamically imported module: https://core.eq.solution](https://eq-solutions.sentry.io/issues/141714696/) | 37 | 2026-08-21 |
| eq-shell | [Error: app_data.staff.cards_worker_id pointing at missing jvkn workers: 4](https://eq-solutions.sentry.io/issues/138175643/) | 6 | 2026-08-24 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 4 | 2026-08-20 |
| eq-shell | [Error: Active org_memberships held by non-members: 15](https://eq-solutions.sentry.io/issues/142429897/) | 2 | 2026-08-24 |
| eq-field | [TypeError: Failed to fetch](https://eq-solutions.sentry.io/issues/141259049/) | 2 | 2026-08-24 |
| eq-shell | [phone-otp: requested for inactive account](https://eq-solutions.sentry.io/issues/141933696/) | 2 | 2026-08-20 |
| eq-shell | [EQ Field handoff auto-recovery (timeout)](https://eq-solutions.sentry.io/issues/141463602/) | 2 | 2026-08-20 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 2 | 2026-08-19 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-25 | eq-shell | [#1594](https://github.com/eq-solutions/eq-shell/pull/1594) chore(deps): bump @eq-solutions/roles to v2.7.5 |
| 2026-08-25 | eq-shell | [#1589](https://github.com/eq-solutions/eq-shell/pull/1589) fix(quotes): shorten archive-days label so Default Rates fields l |
| 2026-08-25 | eq-shell | [#1588](https://github.com/eq-solutions/eq-shell/pull/1588) fix(staff): quick-toggle Supervisor ON needs a category |
| 2026-08-25 | eq-shell | [#1587](https://github.com/eq-solutions/eq-shell/pull/1587) feat(quotes): auto-derive estimators from history, make archive w |
| 2026-08-25 | eq-shell | [#1586](https://github.com/eq-solutions/eq-shell/pull/1586) feat(quotes): collapse rate library by category, remove broken By |
| 2026-08-25 | eq-shell | [#1585](https://github.com/eq-solutions/eq-shell/pull/1585) fix(migrations): 0280 was about to clobber 0279's eq_list_sites c |
| 2026-08-25 | eq-shell | [#1584](https://github.com/eq-solutions/eq-shell/pull/1584) fix(quotes): keep markup% in sync when rate is edited with cost s |
| 2026-08-25 | eq-shell | [#1583](https://github.com/eq-solutions/eq-shell/pull/1583) fix(customers): clear 4 react-hooks/set-state-in-effect errors |
| 2026-08-25 | eq-field | [#780](https://github.com/eq-solutions/eq-field/pull/780) v3.5.562 — week picker: pin "Current: ..." row when paged away |
| 2026-08-25 | eq-field | [#785](https://github.com/eq-solutions/eq-field/pull/785) v3.5.564 — People save: only patch fields that actually changed |
| 2026-08-25 | eq-field | [#787](https://github.com/eq-solutions/eq-field/pull/787) v3.5.565 — fix Ctrl+Enter losing focus on Monday in Edit Roster |
| 2026-08-25 | eq-field | [#783](https://github.com/eq-solutions/eq-field/pull/783) v3.5.563 — People editor: settable Preferred Name |
| 2026-08-25 | eq-field | [#784](https://github.com/eq-solutions/eq-field/pull/784) v3.5.563 — Edit Roster paste (Tier 2) |
| 2026-08-25 | eq-field | [#782](https://github.com/eq-solutions/eq-field/pull/782) v3.5.562 — Edit Roster keyboard flow + row-batched save (Tier 1) |
| 2026-08-25 | eq-field | [#781](https://github.com/eq-solutions/eq-field/pull/781) v3.5.562 — feature-toggles.js: name the two adjustable-thing patt |
_Showing 15 of 116 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-shell** (281 open) · [eq/pending/eq-shell.md](eq/pending/eq-shell.md)
- **eq-cards** (62 open) · [eq/pending/eq-cards.md](eq/pending/eq-cards.md)
- **eq-field** (135 open) · [eq/pending/eq-field.md](eq/pending/eq-field.md)
- **eq-solves-service** (96 open) · [eq/pending/eq-solves-service.md](eq/pending/eq-solves-service.md)
- **eq-solves-intake** (18 open) · [eq/pending/eq-solves-intake.md](eq/pending/eq-solves-intake.md)
- **eq-design-tokens** (1 open) · [eq/pending/eq-design-tokens.md](eq/pending/eq-design-tokens.md)
- **eq-ui** (2 open) · [eq/pending/eq-ui.md](eq/pending/eq-ui.md)
- **eq-receipts** (4 open) · [eq/pending/eq-receipts.md](eq/pending/eq-receipts.md)
- **eq-context** (30 open) · [eq/pending/eq-context.md](eq/pending/eq-context.md)
- **cross-repo** (185 open) · [eq/pending/cross-repo.md](eq/pending/cross-repo.md)
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
- **~7 SKS staff missing from EQ Field's staff table** (hired since the 5 Jul snapshot): Ahmed Masaud, Amir Farid, Callum Treharne, Jhon Jairo Velasquez Meneses, Nabeel Hussain, Paul Bolger, Timothy Sue — plus a handful of name-string mismatches (e.g. "Bruno Pedrosa" vs "Bruno Vita Pedrosa", "Jose Quintanilla" vs "Jose Luis Quintanilla Rodriguez"). Royce said he'll manage this himself via EQ Field's People admin. _(added 2026-08-14)_
_…and 75 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise. Open splits engineering backlog from Royce's own queue (a confirm, a click-through, a call) — the two used to be counted together here, which made the number look worse than the real engineering backlog actually is; the split matches 'Waiting on you' above._

| File | Lines | Open (eng / you) | Done (unrotated) | Aging 45d+ |
|------|------:|------------------:|------------------:|------------:|
| [eq-shell](eq/pending/eq-shell.md) | 1807 | 199 / 83 | 239 | 45 |
| [eq-cards](eq/pending/eq-cards.md) | 506 | 50 / 14 | 66 | 11 |
| [eq-field](eq/pending/eq-field.md) | 882 | 109 / 30 | 57 | 25 |
| [eq-solves-service](eq/pending/eq-solves-service.md) | 662 | 73 / 26 | 93 | 23 |
| [eq-solves-intake](eq/pending/eq-solves-intake.md) | 152 | 13 / 6 | 5 | 14 |
| [eq-design-tokens](eq/pending/eq-design-tokens.md) | 23 | 1 / 0 | 0 | 1 |
| [eq-ui](eq/pending/eq-ui.md) | 29 | 2 / 0 | 2 | 0 |
| [eq-receipts](eq/pending/eq-receipts.md) | 44 | 3 / 1 | 0 | 0 |
| [eq-context](eq/pending/eq-context.md) | 263 | 25 / 5 | 27 | 5 |
| [cross-repo](eq/pending/cross-repo.md) | 977 | 143 / 42 | 28 | 43 |
| [sks](eq/pending/sks.md) | 53 | 3 / 5 | 0 | 6 |
| [SKS](sks/pending.md) | 488 | 85 / 14 | 5 | 26 |
| [SKS active](sks/active.md) | 119 | 0 / 0 | 0 | 0 |
| [OPS](ops/pending.md) | 509 | 44 / 3 | 0 | 1 |

## Aging open items (45d+, unconfirmed)

_Open items sitting under a section header this old or older — not necessarily wrong, just gone quiet under its own dated write-up. Worth a look before it reads as done-and-forgotten._

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
- **eq-shell** (2026-07-03) · **Commit eq-intake/CLAUDE.md** — left untracked (eq-intake tree dirty on `feat/armada-sprint-polish`); fold into whichever branch lands next. _(added 2026-07-03)_
- **eq-shell** (2026-07-03) · **Coordinated `--reconcile-ledger`** — after go-live settles: renames/stamps the 16 bare 0103–0116/0141 rows, drops `057` + go-live hand rows. Run only WITH eq-intake (their numbering reads the live ledger). _(added 2026-07-03)_
_…and 185 more — see each file's Queue health row above._

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
| 2026-08-25 | [Canonical wiring map: jvkn/Shell/Field read-write capabilities, verified live end-to-end](sessions/2026-08-25.md) |
| 2026-08-24 | [SEC-58 (control-plane ledger) and SEC-65 (AUDIT_SB_KEY label) closed](sessions/2026-08-24.md) |
| 2026-08-23 | [Labour-hire live-trial bugs: licence/compliance-pack gap root-caused and fixed (PR #1513), cropping issue diagnosed](sessions/2026-08-23.md) |
| 2026-08-21 | [eq-service worktree/branch/stash graveyard cleared: 8 branches, 23 folders, 3 stashes, all confirmed already-shipped before removal](sessions/2026-08-21.md) |
| 2026-08-20 | [Staff page load-time root-caused: staff-bootstrap missing from the keep-warm ping](sessions/2026-08-20.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-25 10:47 UTC._
