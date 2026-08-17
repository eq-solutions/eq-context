---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-17
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-17 12:18 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-17 12:06 UTC → 2026-08-17 12:18 UTC)

- Merged: eq-shell [#1414](https://github.com/eq-solutions/eq-shell/pull/1414) feat(notifications): fire the connect-request email for auto
- Merged: eq-shell [#1412](https://github.com/eq-solutions/eq-shell/pull/1412) chore(roles): bump @eq-solutions/roles to v2.7.3
- Merged: eq-shell [#1409](https://github.com/eq-solutions/eq-shell/pull/1409) fix(security): origin-guard 3 misc upload endpoints
- Merged: eq-shell [#1408](https://github.com/eq-solutions/eq-shell/pull/1408) chore(ci): triage can_assign_worker_role into KNOWN_UNSOURCE
- Merged: eq-shell [#1406](https://github.com/eq-solutions/eq-shell/pull/1406) fix(dashboard): remove Today's Actions from the Shell home p
- Merged: eq-shell [#1405](https://github.com/eq-solutions/eq-shell/pull/1405) fix(security): origin-guard 4 quotes/ops/briefing endpoints
- Merged: eq-shell [#1402](https://github.com/eq-solutions/eq-shell/pull/1402) fix(security): origin-guard 4 GM Reports mutation endpoints
- Merged: eq-shell [#1401](https://github.com/eq-solutions/eq-shell/pull/1401) fix(security): origin-guard 4 CRM/suppliers/labour-hire muta

## ⚠ Needs you (4)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-08-16.md](sessions/2026-08-16.md) · [failures.md](system/failures.md)
- 🟠 **Sentry new error** — `eq-shell` [Degraded UI Performance](https://eq-solutions.sentry.io/issues/141127922/)
- 🟠 **Sentry new error** — `eq-shell` [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/)

## 🙋 Waiting on you (160)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Not yet seen working on Royce's own screen** — confirmed the code is correct and the production build deployed clean, but couldn't click through it personally (no login for this environment). Worth two minutes next time Royce is in Staff. _(added 2026-08-17)_
- **EQ** · **Two adjacent staff-approval screens require different levels of permission to do very similar things** — one needs a manager, another needs only a much more junior permission to view/act on the same underlying approval data. Doesn't look deliberate. Needs your call on whether they should match. _(added 2026-08-16)_
- **EQ** · **Quote records (create/edit/delete) were deliberately left open to everyone** — Royce's call, not a gap. Worth a second look later if quote data starts needing tighter control. _(added 2026-08-15)_
- **EQ** · **Nothing alerts on this yet.** Recording a lockout is not the same as being told about one. The two questions worth alerting on — who got locked out in the last 24 hours, and who had the password right but never cleared the second step — are written and tested, but have to be run by hand. Turning either into a real alert is separate work and needs your call on where it should land. _(added 2026-08-15, needs your call)_
- **EQ** · **Not click-tested in a browser** — both sign-in doors were checked by calling them directly on production (an unknown mobile and an unknown email each return an identical "no" with no extra detail; the unauthed session check still refuses correctly) plus full CI, but nobody signed in through the actual page. Worth Royce trying two things on his phone: a *wrong* PIN, and a number that has *no* PIN set — both should now show the same "That number and PIN didn't match. If you haven't set a PIN yet, use 'Text me a code instead'". Then sign in by text on an account with no PIN and confirm the "Set a PIN" prompt still appears on the Home screen — that prompt is now the only place that guidance is given. _(added 2026-08-15)_
- **EQ** · **Today's Actions vs Outstanding Works can still contradict each other for up to 10 minutes** — found while reviewing the same screenshots (separate issue from the compliance-card redundancy, not addressed by this build): Today's Actions is cached 10 min per user (`ai-briefing.ts`), Outstanding Works refetches every 60s off the same table. Resolving a Service item mid-cache-window shows "overdue" in one card and "nothing overdue" in the other, same screen, same moment. Needs Royce's call: shrink the cache TTL, or add a "generated Xm ago" stamp so it reads as expected staleness rather than a bug. _(added 2026-08-14)_
- **EQ** · **Not click-tested live on a real tenant** — verified via `tsc -b --force`, eslint (clean except pre-existing tolerated patterns already present identically in `Suppliers.tsx`/`LabourHireRates.tsx`, not introduced by this change), full CI, and the Netlify deploy preview build succeeding. A local click-through attempt hit a pre-existing sandbox limitation (`VITE_FIELD_URL` unset crashes the app at module scope, unrelated to this change) and was abandoned per the standing "default browser only" rule rather than switched to Chrome for a low-value local check. Worth Royce opening Suppliers, Compliance report, and the mobile Home on his phone once. _(added 2026-08-14)_
- **EQ** · **Not click-tested live** — verified via `tsc -b --force`, eslint, full CI (all green), and the Netlify deploy preview build succeeding — not by clicking through a real signed-in session. _(added 2026-08-14)_
- **EQ** · **Not click-tested live** — same sandbox limitation as everything else this session; built against `tsc`/lint/the permission-drift guard only. _(added 2026-08-14)_
- **EQ** · **Royce's own click-through, still not done** — nobody has logged a conversation, added a rating, or assigned someone off the Unassigned list through the real UI yet, and the new Table view is unverified live. Every fix above should make this work now; only a live session can confirm it. _(added 2026-08-11, carried through every entry above)_
- **EQ** · **Proactive "overdue for review" nudges** — deliberately held per `/decide`: there's no conversation data yet for staleness to mean anything. Worth building once the click-through above happens and some real data exists. _(added 2026-08-12)_
- **EQ** · **Compliance click-through only covers Staff and Ops today.** EQ Field has no record-level deep-linking (only `?tab=`), EQ Service has an unused `?return=` path mechanism Shell never constructs a specific path for, and EQ Cards has no deep-link support at all — out of scope for this pass since it wasn't asked for, but the next domain to add if Ask Anything grows past licences/quotes. _(added 2026-08-11)_
_…and 148 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 2 | 0d |
| eq-solves-service | ✓ success | 0d ago | 5 | 0d |
| eq-field | ✓ success | 0d ago | 1 | 0d |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 1d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 3 | 2026-08-17 |
| eq-shell | [Degraded UI Performance](https://eq-solutions.sentry.io/issues/141127922/) | 1 | 2026-08-17 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 1 | 2026-08-17 |
| eq-solves-service | [Error: An unexpected response was received from the server.](https://eq-solutions.sentry.io/issues/139724869/) | 1 | 2026-08-09 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-17 | eq-shell | [#1425](https://github.com/eq-solutions/eq-shell/pull/1425) feat(access-control): unify Field's role and person-only permissi |
| 2026-08-17 | eq-shell | [#1424](https://github.com/eq-solutions/eq-shell/pull/1424) feat(staff): extend Excel-style multiselect filters to Name and S |
| 2026-08-17 | eq-shell | [#1423](https://github.com/eq-solutions/eq-shell/pull/1423) fix(licences): repair the Shell OCR page's save call, point it at |
| 2026-08-17 | eq-shell | [#1420](https://github.com/eq-solutions/eq-shell/pull/1420) fix(access-control): Ops label consistency + searchable diffed cu |
| 2026-08-17 | eq-shell | [#1421](https://github.com/eq-solutions/eq-shell/pull/1421) feat(staff): Excel-style multiselect filters on Type, Job Title,  |
| 2026-08-17 | eq-shell | [#1422](https://github.com/eq-solutions/eq-shell/pull/1422) fix(ci): teach orphan-perms gate about eq-field's vendored fine-g |
| 2026-08-17 | eq-shell | [#1419](https://github.com/eq-solutions/eq-shell/pull/1419) feat(staff): show a PDF thumbnail preview instead of a plain link |
| 2026-08-17 | eq-shell | [#1418](https://github.com/eq-solutions/eq-shell/pull/1418) fix(observability): close account-inactive blind spot on magic-li |
| 2026-08-17 | eq-shell | [#1417](https://github.com/eq-solutions/eq-shell/pull/1417) fix(observability): surface silent PIN-reset lockouts on inactive |
| 2026-08-17 | eq-solves-service | [#751](https://github.com/eq-solutions/eq-service/pull/751) fix(security): pin search_path on service.tg_pm_calendar_iud |
| 2026-08-17 | eq-solves-service | [#750](https://github.com/eq-solutions/eq-service/pull/750) fix(identity): canonicalize the supervisor-digest DB functions |
| 2026-08-17 | eq-solves-service | [#749](https://github.com/eq-solutions/eq-service/pull/749) fix(notifications): authenticate via getApiUser() instead of raw  |
| 2026-08-17 | eq-solves-service | [#748](https://github.com/eq-solutions/eq-service/pull/748) fix(identity): resolve Service's user/supervisor lookups from the |
| 2026-08-17 | eq-solves-service | [#747](https://github.com/eq-solutions/eq-service/pull/747) fix(ui): Export button font-size actually applying now (tailwind- |
| 2026-08-17 | eq-solves-service | [#746](https://github.com/eq-solutions/eq-service/pull/746) fix(reports): drop masthead caption on NSX + Work Order Details t |
_Showing 15 of 118 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-shell** (198 open) · [eq/pending/eq-shell.md](eq/pending/eq-shell.md)
- **eq-cards** (47 open) · [eq/pending/eq-cards.md](eq/pending/eq-cards.md)
- **eq-field** (95 open) · [eq/pending/eq-field.md](eq/pending/eq-field.md)
- **eq-solves-service** (74 open) · [eq/pending/eq-solves-service.md](eq/pending/eq-solves-service.md)
- **eq-solves-intake** (21 open) · [eq/pending/eq-solves-intake.md](eq/pending/eq-solves-intake.md)
- **eq-design-tokens** (1 open) · [eq/pending/eq-design-tokens.md](eq/pending/eq-design-tokens.md)
- **eq-ui** (2 open) · [eq/pending/eq-ui.md](eq/pending/eq-ui.md)
- **eq-receipts** (4 open) · [eq/pending/eq-receipts.md](eq/pending/eq-receipts.md)
- **eq-context** (21 open) · [eq/pending/eq-context.md](eq/pending/eq-context.md)
- **cross-repo** (181 open) · [eq/pending/cross-repo.md](eq/pending/cross-repo.md)
- **sks** (8 open) · [eq/pending/sks.md](eq/pending/sks.md)

## Pending (SKS)

- **Still not applied to the live database — checked directly, and Royce turned down the shortcut that would have unblocked it today.** Confirmed merging the PR didn't secretly switch it on. Turning it on for real right now would lock the people who haven't signed in yet out of their own timesheet and leave the moment they do, since the fix depends on their login already being linked to their staff record — 37 of 83 active SKS staff, checked again today. A workaround exists (let just those specific people keep today's wider access until they sign in, instead of holding up everyone else) but Royce said no — waiting for them to actually sign in through the real onboarding process instead, however long that takes. _(added 2026-08-16, decision confirmed 2026-08-16)_
- **The disposable EQ-side tenant doesn't have this fix** — lower priority, since that tenant holds no real data, but the identical gap exists there too and needs some prerequisite pieces built first before it can be ported. _(added 2026-08-16)_
- **Run the first real weekly export/import test** — SKS NSW Labour → Export Schedule CSV → EQ Field (logged in as the SKS org) → Import Schedule CSV. Discussed and confirmed safe; not actually run this session. _(added 2026-08-14)_
- **Deactivate the two stale site rows in ehow** — `Erilyan` (`site_id 6c221319…`, code EC6) and `Microsoft SYD27` (`site_id 7fb2d662…`, code SYD27). Single-column `active=false` flip each, no code change, no deploy — Royce hasn't given the explicit go to execute it yet. _(added 2026-08-14)_
- **~7 SKS staff missing from EQ Field's staff table** (hired since the 5 Jul snapshot): Ahmed Masaud, Amir Farid, Callum Treharne, Jhon Jairo Velasquez Meneses, Nabeel Hussain, Paul Bolger, Timothy Sue — plus a handful of name-string mismatches (e.g. "Bruno Pedrosa" vs "Bruno Vita Pedrosa", "Jose Quintanilla" vs "Jose Luis Quintanilla Rodriguez"). Royce said he'll manage this himself via EQ Field's People admin. _(added 2026-08-14)_
- **Leave sync parked deliberately** — an imported leave code lands on `schedule_entries.leave_type` directly, not in `app_data.leave_requests`, so it displays but carries no approver/audit trail. Royce explicitly scoped this session to roster only; leave is its own future task. _(added 2026-08-14)_
- **Optional code fix, not required**: the roster site-map query in `eq-field/scripts/supabase.js` (~line 992) filters on `active=eq.true` only, not `field_enabled` — a small latent gap (found live) unrelated to the SYD27/EC6 fix above; deactivating the stale rows sidesteps it, so this is cosmetic cleanup only if ever revisited. _(added 2026-08-14)_
- **Richard needs to re-add his LV Rescue photo** — none of the 6 attempts ever actually captured one; the surviving row has the licence details but no photo. _(added 2026-08-13)_
- **Underlying Cards mobile bug not yet fixed** — a licence "renewal" can silently save nothing if on-device OCR can't read the card and the user doesn't notice the date field still shows the old value. Worth watching for other workers hitting the same silent failure until eq-cards ships the fix. _(added 2026-08-11)_
- **Declined this session, still open if wanted:** widen the Prestart tab past its hardcoded 7-day window, or add a "Show older → Records" link — Royce picked "fix the cap only" via AskUserQuestion; the tab itself is unchanged. _(added 2026-08-04)_
_…and 70 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise. Open splits engineering backlog from Royce's own queue (a confirm, a click-through, a call) — the two used to be counted together here, which made the number look worse than the real engineering backlog actually is; the split matches 'Waiting on you' above._

| File | Lines | Open (eng / you) | Done (unrotated) | Aging 45d+ |
|------|------:|------------------:|------------------:|------------:|
| [eq-shell](eq/pending/eq-shell.md) | 1160 | 150 / 50 | 72 | 29 |
| [eq-cards](eq/pending/eq-cards.md) | 331 | 36 / 12 | 22 | 3 |
| [eq-field](eq/pending/eq-field.md) | 615 | 84 / 14 | 5 | 11 |
| [eq-solves-service](eq/pending/eq-solves-service.md) | 423 | 60 / 18 | 19 | 7 |
| [eq-solves-intake](eq/pending/eq-solves-intake.md) | 161 | 15 / 6 | 7 | 11 |
| [eq-design-tokens](eq/pending/eq-design-tokens.md) | 23 | 1 / 0 | 0 | 1 |
| [eq-ui](eq/pending/eq-ui.md) | 22 | 2 / 0 | 0 | 0 |
| [eq-receipts](eq/pending/eq-receipts.md) | 44 | 3 / 1 | 0 | 0 |
| [eq-context](eq/pending/eq-context.md) | 169 | 19 / 2 | 9 | 2 |
| [cross-repo](eq/pending/cross-repo.md) | 932 | 141 / 42 | 14 | 18 |
| [sks](eq/pending/sks.md) | 53 | 3 / 5 | 0 | 6 |
| [SKS](sks/pending.md) | 432 | 81 / 9 | 1 | 15 |
| [SKS active](sks/active.md) | 109 | 0 / 0 | 0 | 0 |
| [OPS](ops/pending.md) | 421 | 33 / 4 | 3 | 1 |

## Possible recurring failures (unconfirmed)

_Session logs mention a pattern matching a known failure below, dated after its last recorded occurrence. Not yet counted — if it's real, bump `recurrences` in [failures.md](system/failures.md) and `guard-ratchet.yml` proposes promotion on its own next run._

- **F5** (rung 0) — An ungoverned shadow memory overrode the canonical contract · 1 session since last recorded, most recent [2026-08-16.md](sessions/2026-08-16.md)

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-17 | [Full Sentry sweep + Richard Brown's jvkn identity actually merged, silent PIN-reset lockout found and fixed](sessions/2026-08-17.md) |
| 2026-08-16 | [built a personal task register for Royce (OneDrive), cross-checked it live twice, found and cleared a false alarm on eq-context's git state](sessions/2026-08-16.md) |
| 2026-08-15 | [staff-update was gating an HR write on a read permission; fixed, shipped, and corrected the repo's deploy model on the way](sessions/2026-08-15.md) |
| 2026-08-14 | [SKS → EQ Field weekly roster CSV sync: investigated live, confirmed feasible with zero new code](sessions/2026-08-14.md) |
| 2026-08-13 | [eq-shell PR #1316: misdiagnosed build error, real cause was a pdfjs-dist v6 type break, fixed + merged + deployed clean](sessions/2026-08-13.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-17 12:18 UTC._
