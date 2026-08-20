---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-20
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-20 17:42 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-20 12:36 UTC → 2026-08-20 17:42 UTC)

- Merged: eq-shell [#1480](https://github.com/eq-solutions/eq-shell/pull/1480) feat(labour-hire): partner-agency self-service candidate int
- Merged: eq-shell [#1479](https://github.com/eq-solutions/eq-shell/pull/1479) feat(customers): cross-customer contacts in EQ Ops + bottom 
- Merged: eq-shell [#1476](https://github.com/eq-solutions/eq-shell/pull/1476) chore(deps): bump @eq-solutions/ui to v1.16.4
- Merged: eq-shell [#1473](https://github.com/eq-solutions/eq-shell/pull/1473) chore(nav): remove orphaned Storage page
- Merged: eq-shell [#1470](https://github.com/eq-solutions/eq-shell/pull/1470) fix(documents): revoke authenticated grants on documents/doc
- Merged: eq-shell [#1468](https://github.com/eq-solutions/eq-shell/pull/1468) chore(nav): remove 2 more orphaned pages (Field roster + She
- Merged: eq-shell [#1466](https://github.com/eq-solutions/eq-shell/pull/1466) chore(deps): bump @eq-solutions/ui to v1.16.1
- Merged: eq-solves-service [#793](https://github.com/eq-solutions/eq-service/pull/793) test(maintenance): component tests for the check list and de
- ⚠ Needs you: 4 → 5 (new items)

## ⚠ Needs you (5)

- 🔴 **Sentry new error** — `eq-shell` [TypeError: Failed to fetch dynamically imported module: http](https://eq-solutions.sentry.io/issues/141714696/)
- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-29 (P1 — OPEN, found 2026-08-20) — `service.hard_delete_archived_entity` (ehow) has no role/`eq_role` check — any a · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-08-19.md](sessions/2026-08-19.md) · [failures.md](system/failures.md)
- 🟠 **Sentry new error** — `eq-shell` [EQ Field handoff auto-recovery (timeout)](https://eq-solutions.sentry.io/issues/141463602/)

## 🙋 Waiting on you (187)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **eq-shell** · **Consider a lightweight confirmation of what the client-RFQ autofill actually filled in** — today it silently overwrites the create-form's fields with no summary. Not a correctness gap (nothing saves until "Create Quote," so the form itself is the review step) but possibly worth it if the parse is often wrong in practice — needs Royce's read on that, not a guess. _(added 2026-08-20)_
- **eq-shell** · **Not click-tested live** — the final consolidated shape (single button, drag-and-drop, section picker) is verified via typecheck/lint/CI/deploy-preview, and the *previous* Excel-only version was click-tested live, but the new shape specifically hasn't been. _(added 2026-08-20)_
- **eq-shell** · **Not click-tested live** — verified via typecheck/lint/376 tests and confirmed production deploys (exact commit match) for both PRs, not an actual admin session. Worth two minutes: open the Reference library (should show 16 documents, not 44) and try "Push to more people" on an existing Register document. _(added 2026-08-20)_
- **eq-shell** · **Storage browser (`/storage`) has zero nav link anywhere, confirmed still true** — its open-to-all-roles access is your own 2026-08-16 call. Asked what it's for: a generic empty per-tenant file bucket, nothing currently writes to it. Real open question whether it's worth keeping findable or retiring — no lean given either way. _(added 2026-08-20, needs your call)_
- **eq-shell** · **Not click-tested live by a person** — verified via typecheck, lint, and exact commit-ancestry against the live production deploy, not by watching a real QR joiner's row actually change on `/sks/admin/users`. Worth a look next time someone joins via a self-join link. _(added 2026-08-20)_
- **eq-shell** · **Not click-tested live** — verified via typecheck, lint, and full CI; no signed-in manager session available to confirm the Login column and filter render correctly, or to spot-check the 24 names against who's actually still active. _(added 2026-08-20)_
- **eq-shell** · **Not clicked through live** — confirmed by typecheck, the permission-drift guard, and a direct jvkn query proving the Comms fix is a no-op today, not by an actual signed-in click-through. Worth two minutes on NSW Comms, the Ops tile as apprentice/labour_hire/subcontractor, and the mobile Reports row. _(added 2026-08-19)_
- **eq-shell** · **No live click-through yet** — the fix is confirmed genuinely deployed, but nobody has tapped "Save" on an export through `core.eq.solutions/sks/cards` on an actual iOS device since it landed. _(added 2026-08-18)_
- **eq-shell** · **Not click-tested live by a person** — verified via typecheck, lint, the full test suite, and confirmed production deploys (exact commit match against what's actually serving), not an actual signed-in click-through. Worth two minutes next time Royce is in Shell: click through Staff → Customers → Field → Admin from the sidebar (should feel instant, no white-flash reload), and confirm ctrl/cmd-click still opens a link in a new tab. _(added 2026-08-18)_
- **eq-shell** · **Not click-tested live** — verified via eslint (0 errors) and the deploy-preview build succeeding, not by scanning a real QR/join-code link and watching an admin's inbox + the Staff badge. _(added 2026-08-18)_
- **eq-shell** · **Not yet seen working on Royce's own screen** — confirmed the code is correct and the production build deployed clean, but couldn't click through it personally (no login for this environment). Worth two minutes next time Royce is in Staff. _(added 2026-08-17)_
- **eq-shell** · **Two adjacent staff-approval screens require different levels of permission to do very similar things** — one needs a manager, another needs only a much more junior permission to view/act on the same underlying approval data. Doesn't look deliberate. Needs your call on whether they should match. _(added 2026-08-16)_
_…and 175 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 0 | — |
| eq-solves-service | ✓ success | 0d ago | 3 | 0d |
| eq-field | ✓ success | 0d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 2d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [TypeError: Failed to fetch dynamically imported module: https://core.eq.solution](https://eq-solutions.sentry.io/issues/141714696/) | 31 | 2026-08-20 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 3 | 2026-08-20 |
| eq-shell | [EQ Field handoff auto-recovery (timeout)](https://eq-solutions.sentry.io/issues/141463602/) | 2 | 2026-08-20 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 2 | 2026-08-19 |
| eq-shell | [Degraded UI Performance](https://eq-solutions.sentry.io/issues/141127922/) | 2 | 2026-08-18 |
| eq-cards | [minified:yU: PostgrestException(message: permission denied for function eq_cards](https://eq-solutions.sentry.io/issues/137739023/) | 2 | 2026-08-18 |
| eq-field | [ReferenceError: Can't find variable: _ensureRequirementsForList](https://eq-solutions.sentry.io/issues/141820135/) | 1 | 2026-08-20 |
| eq-solves-service | [Error: An unexpected response was received from the server.](https://eq-solutions.sentry.io/issues/139724869/) | 1 | 2026-08-09 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-20 | eq-shell | [#1496](https://github.com/eq-solutions/eq-shell/pull/1496) feat(labour-hire): review each licence individually before approv |
| 2026-08-20 | eq-shell | [#1495](https://github.com/eq-solutions/eq-shell/pull/1495) chore: remove eq-shell's dead duplicate of workers-canonical-sync |
| 2026-08-20 | eq-shell | [#1494](https://github.com/eq-solutions/eq-shell/pull/1494) fix(labour-hire): batch flow never captured an employer name; spi |
| 2026-08-20 | eq-shell | [#1493](https://github.com/eq-solutions/eq-shell/pull/1493) fix(quotes): clarify client-RFQ vs supplier-quote PDF button labe |
| 2026-08-20 | eq-shell | [#1492](https://github.com/eq-solutions/eq-shell/pull/1492) feat(quotes): drag-and-drop + one import button + per-row section |
| 2026-08-20 | eq-shell | [#1491](https://github.com/eq-solutions/eq-shell/pull/1491) fix(labour-hire): batch cleanup deletes staging docs before commi |
| 2026-08-20 | eq-shell | [#1490](https://github.com/eq-solutions/eq-shell/pull/1490) fix(labour-hire): employment_type never protected from Cards resy |
| 2026-08-20 | eq-shell | [#1489](https://github.com/eq-solutions/eq-shell/pull/1489) feat(labour-hire): drag-and-drop for the batch intake file picker |
| 2026-08-20 | eq-shell | [#1488](https://github.com/eq-solutions/eq-shell/pull/1488) fix(labour-hire): staging-object cleanup is fire-and-forget, neve |
| 2026-08-20 | eq-shell | [#1487](https://github.com/eq-solutions/eq-shell/pull/1487) fix(labour-hire): zip-slip check false-positives on every entry,  |
| 2026-08-20 | eq-shell | [#1486](https://github.com/eq-solutions/eq-shell/pull/1486) feat(labour-hire): batch intake — group upload for admin and the  |
| 2026-08-20 | eq-shell | [#1485](https://github.com/eq-solutions/eq-shell/pull/1485) feat(quotes): Excel labour/materials breakdown import + Category  |
| 2026-08-20 | eq-shell | [#1484](https://github.com/eq-solutions/eq-shell/pull/1484) fix(documents): 0253 inserted reminder_count mid-view, PG rejects |
| 2026-08-20 | eq-shell | [#1483](https://github.com/eq-solutions/eq-shell/pull/1483) fix(routing): swallow rejected hover-prefetch of a lazy route chu |
| 2026-08-20 | eq-shell | [#1481](https://github.com/eq-solutions/eq-shell/pull/1481) fix(documents): reminder cron respects due_at, backs off on deliv |
_Showing 15 of 124 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-shell** (232 open) · [eq/pending/eq-shell.md](eq/pending/eq-shell.md)
- **eq-cards** (53 open) · [eq/pending/eq-cards.md](eq/pending/eq-cards.md)
- **eq-field** (112 open) · [eq/pending/eq-field.md](eq/pending/eq-field.md)
- **eq-solves-service** (87 open) · [eq/pending/eq-solves-service.md](eq/pending/eq-solves-service.md)
- **eq-solves-intake** (17 open) · [eq/pending/eq-solves-intake.md](eq/pending/eq-solves-intake.md)
- **eq-design-tokens** (1 open) · [eq/pending/eq-design-tokens.md](eq/pending/eq-design-tokens.md)
- **eq-ui** (2 open) · [eq/pending/eq-ui.md](eq/pending/eq-ui.md)
- **eq-receipts** (4 open) · [eq/pending/eq-receipts.md](eq/pending/eq-receipts.md)
- **eq-context** (25 open) · [eq/pending/eq-context.md](eq/pending/eq-context.md)
- **cross-repo** (182 open) · [eq/pending/cross-repo.md](eq/pending/cross-repo.md)
- **sks** (8 open) · [eq/pending/sks.md](eq/pending/sks.md)

## Pending (SKS)

- **SKS's own number, for reference: 6 of 32 active SKS members are currently missing White Card** — visible today in Shell's Training Matrix; nothing blocks them from working while missing it (soft-flag by design, not an oversight). Worth a look if Royce wants a harder rule for SKS specifically. _(added 2026-08-19)_
- **A reported roster-grid "alignment" issue (one person's row looked off) couldn't be reproduced from the code** — most likely just placeholder text in blank cells reading like real data at a glance, not an actual bug, but left open rather than guessed at. _(added 2026-08-19)_
- **Still not applied to the live database — checked directly, and Royce turned down the shortcut that would have unblocked it today.** Confirmed merging the PR didn't secretly switch it on. Turning it on for real right now would lock the people who haven't signed in yet out of their own timesheet and leave the moment they do, since the fix depends on their login already being linked to their staff record — 37 of 83 active SKS staff, checked again today. A workaround exists (let just those specific people keep today's wider access until they sign in, instead of holding up everyone else) but Royce said no — waiting for them to actually sign in through the real onboarding process instead, however long that takes. _(added 2026-08-16, decision confirmed 2026-08-16)_
- **The disposable EQ-side tenant doesn't have this fix** — lower priority, since that tenant holds no real data, but the identical gap exists there too and needs some prerequisite pieces built first before it can be ported. _(added 2026-08-16)_
- **Run the first real weekly export/import test** — SKS NSW Labour → Export Schedule CSV → EQ Field (logged in as the SKS org) → Import Schedule CSV. Discussed and confirmed safe; not actually run this session. _(added 2026-08-14)_
- **Deactivate the two stale site rows in ehow** — `Erilyan` (`site_id 6c221319…`, code EC6) and `Microsoft SYD27` (`site_id 7fb2d662…`, code SYD27). Single-column `active=false` flip each, no code change, no deploy — Royce hasn't given the explicit go to execute it yet. _(added 2026-08-14)_
- **~7 SKS staff missing from EQ Field's staff table** (hired since the 5 Jul snapshot): Ahmed Masaud, Amir Farid, Callum Treharne, Jhon Jairo Velasquez Meneses, Nabeel Hussain, Paul Bolger, Timothy Sue — plus a handful of name-string mismatches (e.g. "Bruno Pedrosa" vs "Bruno Vita Pedrosa", "Jose Quintanilla" vs "Jose Luis Quintanilla Rodriguez"). Royce said he'll manage this himself via EQ Field's People admin. _(added 2026-08-14)_
- **Leave sync parked deliberately** — an imported leave code lands on `schedule_entries.leave_type` directly, not in `app_data.leave_requests`, so it displays but carries no approver/audit trail. Royce explicitly scoped this session to roster only; leave is its own future task. _(added 2026-08-14)_
- **Richard needs to re-add his LV Rescue photo** — none of the 6 attempts ever actually captured one; the surviving row has the licence details but no photo. _(added 2026-08-13)_
- **Underlying Cards mobile bug not yet fixed** — a licence "renewal" can silently save nothing if on-device OCR can't read the card and the user doesn't notice the date field still shows the old value. Worth watching for other workers hitting the same silent failure until eq-cards ships the fix. _(added 2026-08-11)_
_…and 71 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise. Open splits engineering backlog from Royce's own queue (a confirm, a click-through, a call) — the two used to be counted together here, which made the number look worse than the real engineering backlog actually is; the split matches 'Waiting on you' above._

| File | Lines | Open (eng / you) | Done (unrotated) | Aging 45d+ |
|------|------:|------------------:|------------------:|------------:|
| [eq-shell](eq/pending/eq-shell.md) | 1470 | 174 / 62 | 163 | 39 |
| [eq-cards](eq/pending/eq-cards.md) | 396 | 40 / 13 | 41 | 3 |
| [eq-field](eq/pending/eq-field.md) | 746 | 90 / 25 | 34 | 12 |
| [eq-solves-service](eq/pending/eq-solves-service.md) | 543 | 67 / 24 | 47 | 7 |
| [eq-solves-intake](eq/pending/eq-solves-intake.md) | 152 | 13 / 6 | 5 | 14 |
| [eq-design-tokens](eq/pending/eq-design-tokens.md) | 23 | 1 / 0 | 0 | 1 |
| [eq-ui](eq/pending/eq-ui.md) | 29 | 2 / 0 | 2 | 0 |
| [eq-receipts](eq/pending/eq-receipts.md) | 44 | 3 / 1 | 0 | 0 |
| [eq-context](eq/pending/eq-context.md) | 223 | 22 / 3 | 23 | 5 |
| [cross-repo](eq/pending/cross-repo.md) | 949 | 142 / 42 | 20 | 30 |
| [sks](eq/pending/sks.md) | 53 | 3 / 5 | 0 | 6 |
| [SKS](sks/pending.md) | 454 | 81 / 10 | 4 | 20 |
| [SKS active](sks/active.md) | 109 | 0 / 0 | 0 | 0 |
| [OPS](ops/pending.md) | 404 | 31 / 2 | 0 | 1 |

## Aging open items (45d+, unconfirmed)

_Open items sitting under a section header this old or older — not necessarily wrong, just gone quiet under its own dated write-up. Worth a look before it reads as done-and-forgotten._

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
- **eq-shell** (2026-07-02) · **Confirm the activity panel actually renders an event** — needs Royce to make one real change on `/admin/access-control` and check the panel. Can't be faked or tested without a real user action (see the zero-exceptions rule above). _(needs your call)_
- **eq-shell** (2026-07-02) · **Live-verify `cards-export-licences`, `comms-jobs`, `admin-audit` return 403 on a disallowed Origin** — 3 of 6 endpoints confirmed by curl/real-traffic already; these 3 hit a sandbox DNS failure mid-check. Same code as the confirmed 3, not suspected broken, just not directly proven. _(low priority, needs a retry)_
- **eq-shell** (2026-07-02) · **Fix `AdminWorkerQR` QR-colour crash** — Sentry `Error: Invalid hex color: var(--eq-ink)` (eq-shell, 4 events 2026-07-02) is the `qrcode` lib being passed `color.dark: 'var(--eq-ink)'` (a CSS var, not hex) in `AdminWorkerQR.tsx`. More frequent now #594 made that page the primary "Add workers" landing. Fix = pass a real hex (e.g. `#1A1A2E`). _(added 2026-07-02)_
- **eq-shell** (2026-07-02) · **EQ Cards address autocomplete = greenfield** — Cards worker address entry (`profile_edit_screen.dart` + `profile_fill_from_licence_screen.dart`) is manual text + static state dropdown; NO Places, no package, no key. "Should already be done" = it isn't. Flutter web, so the Shell JS pattern doesn't port directly. _(added 2026-07-02)_
- **eq-shell** (2026-07-02) · **Full governed apply-pipeline for jvkn control-plane migrations** — the guardrails above (dup-guard + runbook) landed, but a One-Pipe-style governed/automated apply for eq-cards→jvkn is still not built. Architectural decision. _(added 2026-07-02, needs Royce's call)_
_…and 123 more — see each file's Queue health row above._

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
| 2026-08-20 | [Staff page load-time root-caused: staff-bootstrap missing from the keep-warm ping](sessions/2026-08-20.md) |
| 2026-08-19 | [Cards iframe Web Share fix (eq-shell) + Wallet banner repeat fix (eq-cards)](sessions/2026-08-19.md) |
| 2026-08-18 | [Fixed a real bug behind a suspected-hardcoded-path guard.js gate report](sessions/2026-08-18.md) |
| 2026-08-17 | [Full Sentry sweep + Richard Brown's jvkn identity actually merged, silent PIN-reset lockout found and fixed](sessions/2026-08-17.md) |
| 2026-08-16 | [built a personal task register for Royce (OneDrive), cross-checked it live twice, found and cleared a false alarm on eq-context's git state](sessions/2026-08-16.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-20 17:42 UTC._
