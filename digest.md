---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-17
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-17 09:59 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-17 09:27 UTC → 2026-08-17 09:59 UTC)

- Merged: eq-shell [#1408](https://github.com/eq-solutions/eq-shell/pull/1408) chore(ci): triage can_assign_worker_role into KNOWN_UNSOURCE
- Merged: eq-shell [#1405](https://github.com/eq-solutions/eq-shell/pull/1405) fix(security): origin-guard 4 quotes/ops/briefing endpoints
- Merged: eq-shell [#1402](https://github.com/eq-solutions/eq-shell/pull/1402) fix(security): origin-guard 4 GM Reports mutation endpoints
- Merged: eq-shell [#1398](https://github.com/eq-solutions/eq-shell/pull/1398) fix(security): origin-guard 5 worker-linking/org-config endp
- Merged: eq-shell [#1394](https://github.com/eq-solutions/eq-shell/pull/1394) fix(security): origin-guard 4 session/account-lifecycle endp
- Merged: eq-shell [#1393](https://github.com/eq-solutions/eq-shell/pull/1393) fix(security): origin-guard 5 account-credential endpoints (
- Merged: eq-shell [#1387](https://github.com/eq-solutions/eq-shell/pull/1387) fix(security): close the admin.manage_groups escalation path
- Merged: eq-shell [#1386](https://github.com/eq-solutions/eq-shell/pull/1386) fix(security): origin-guard 2 Cards mutation/PII endpoints +

## ⚠ Needs you (2)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-08-16.md](sessions/2026-08-16.md) · [failures.md](system/failures.md)

## 🙋 Waiting on you (157)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Live click-through still not observed** — same caveat as the 2026-08-14 entry further down this file, now scoped to this specific batch. Resolves once Royce sends the link and the first person scans. _(added 2026-08-17)_
- **EQ** · **Max-uses cap on self-join codes — scoped, not built, Royce's call to hold.** Would need a `max_uses` column (mirrors `expires_at`'s existing shape), an atomic check-and-reject in `shell-join-tenant.ts`, and a field on the Join Links admin page. Estimated under an hour for a working version. Revisit if a link ever actually leaks past its intended recipients, or this becomes a recurring worry. _(added 2026-08-17)_
- **EQ** · **Root cause #1's precise backfill not attempted** — real archaeology (reconstructing minimal table shapes from ~32 migrations, no live table left to verify against) on a shared prod-adjacent project. Royce's call: document only for now. _(added 2026-08-16)_
- **EQ** · **Two adjacent staff-approval screens require different levels of permission to do very similar things** — one needs a manager, another needs only a much more junior permission to view/act on the same underlying approval data. Doesn't look deliberate. Needs your call on whether they should match. _(added 2026-08-16)_
- **EQ** · **A merged duplicate can still show up looking "active" again after a page reload** — the screen doesn't fully know a pair was already merged until it's clicked into once. The real fix needs a small database change in EQ Shell (not this app), so it's fully scoped (exact change, which table, which migration number) but deliberately not built yet — spun off as its own follow-up rather than done inside this session, per Royce's call to leave it for that follow-up to pick up. _(added 2026-08-16)_
- **EQ** · **Not clicked through live in either state.** No safe way to produce a working Shell login locally to test the fixed version, and the standalone side has no working test account — the practice/demo login has been broken since a database move in June and was never reconnected. Worth Royce opening `core.eq.solutions/sks/service/settings` once to eyeball it for real. _(added 2026-08-16)_
- **EQ** · **Quote records (create/edit/delete) were deliberately left open to everyone** — Royce's call, not a gap. Worth a second look later if quote data starts needing tighter control. _(added 2026-08-15)_
- **EQ** · **The email sign-in door reaches 22 of 73 accounts, and none of the six apprentices.** Shipping it didn't change that and can't: a worker still has no way to add an email to their own account. The email on the profile screen is a contact detail that travels with the street address — 73 of 101 worker records have one, but only 17 of those match an actual login. The remaining 58 were typed by admins and never verified, so they must never become logins without the worker proving they own the address. A verified add-an-email flow is the only thing that moves the 22. _(added 2026-08-15, needs your call on priority)_
- **EQ** · **Nothing alerts on this yet.** Recording a lockout is not the same as being told about one. The two questions worth alerting on — who got locked out in the last 24 hours, and who had the password right but never cleared the second step — are written and tested, but have to be run by hand. Turning either into a real alert is separate work and needs your call on where it should land. _(added 2026-08-15, needs your call)_
- **EQ** · **Neither half click-tested on a real phone** — verified by `flutter analyze`, 283 passing tests, full CI on both repos and the ancestry check, not by actually scanning an old `/claim?tenant=sks` poster or walking a fresh sign-in. Worth Royce doing both once. _(added 2026-08-15)_
- **EQ** · **Not click-tested in a browser** — both sign-in doors were checked by calling them directly on production (an unknown mobile and an unknown email each return an identical "no" with no extra detail; the unauthed session check still refuses correctly) plus full CI, but nobody signed in through the actual page. Worth Royce trying two things on his phone: a *wrong* PIN, and a number that has *no* PIN set — both should now show the same "That number and PIN didn't match. If you haven't set a PIN yet, use 'Text me a code instead'". Then sign in by text on an account with no PIN and confirm the "Set a PIN" prompt still appears on the Home screen — that prompt is now the only place that guidance is given. _(added 2026-08-15)_
- **EQ** · **Today's Actions vs Outstanding Works can still contradict each other for up to 10 minutes** — found while reviewing the same screenshots (separate issue from the compliance-card redundancy, not addressed by this build): Today's Actions is cached 10 min per user (`ai-briefing.ts`), Outstanding Works refetches every 60s off the same table. Resolving a Service item mid-cache-window shows "overdue" in one card and "nothing overdue" in the other, same screen, same moment. Needs Royce's call: shrink the cache TTL, or add a "generated Xm ago" stamp so it reads as expected staleness rather than a bug. _(added 2026-08-14)_
_…and 145 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 2 | 0d |
| eq-solves-service | ✓ success | 1d ago | 6 | 0d |
| eq-field | ✓ success | 1d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 1d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-solves-service | [Error: An unexpected response was received from the server.](https://eq-solutions.sentry.io/issues/139724869/) | 1 | 2026-08-09 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-17 | eq-shell | [#1418](https://github.com/eq-solutions/eq-shell/pull/1418) fix(observability): close account-inactive blind spot on magic-li |
| 2026-08-17 | eq-shell | [#1417](https://github.com/eq-solutions/eq-shell/pull/1417) fix(observability): surface silent PIN-reset lockouts on inactive |
| 2026-08-17 | eq-cards | [#262](https://github.com/eq-solutions/eq-cards/pull/262) feat(settings): mirror eq-shell's register columns in licences.cs |
| 2026-08-17 | eq-cards | [#261](https://github.com/eq-solutions/eq-cards/pull/261) feat(licences): show a PDF thumbnail preview instead of an icon-o |
| 2026-08-17 | eq-cards | [#260](https://github.com/eq-solutions/eq-cards/pull/260) feat(wallet): put "Export my data" on the Wallet app bar, not thr |
| 2026-08-17 | eq-cards | [#259](https://github.com/eq-solutions/eq-cards/pull/259) fix(observability): make a silent Safari download failure visible |
| 2026-08-17 | eq-cards | [#258](https://github.com/eq-solutions/eq-cards/pull/258) feat(settings): give workers a real data export — ZIP with photos |
| 2026-08-16 | eq-shell | [#1415](https://github.com/eq-solutions/eq-shell/pull/1415) chore(ci): extend control-plane drift-check to tables, backfill 1 |
| 2026-08-16 | eq-shell | [#1414](https://github.com/eq-solutions/eq-shell/pull/1414) feat(notifications): fire the connect-request email for auto-join |
| 2026-08-16 | eq-shell | [#1411](https://github.com/eq-solutions/eq-shell/pull/1411) fix(dashboard): retire ai-briefing.ts + briefing-action.ts |
| 2026-08-16 | eq-shell | [#1412](https://github.com/eq-solutions/eq-shell/pull/1412) chore(roles): bump @eq-solutions/roles to v2.7.3 |
| 2026-08-16 | eq-shell | [#1413](https://github.com/eq-solutions/eq-shell/pull/1413) fix(sync): close 3 name-propagation gaps found live-testing as an |
| 2026-08-16 | eq-shell | [#1406](https://github.com/eq-solutions/eq-shell/pull/1406) fix(dashboard): remove Today's Actions from the Shell home page |
| 2026-08-16 | eq-shell | [#1410](https://github.com/eq-solutions/eq-shell/pull/1410) fix(security): origin-guard user-preferences.ts |
| 2026-08-16 | eq-shell | [#1409](https://github.com/eq-solutions/eq-shell/pull/1409) fix(security): origin-guard 3 misc upload endpoints |
_Showing 15 of 115 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Root cause #2 (eq-shell's `shell_control` untracked tables) needs eq-shell to trace and fix** — eq-cards has no visibility into their original shape. eq-shell PR #1389 ("triage 3 jvkn functions into KNOWN_UNSOURCED", merged same day) suggests they may already have a related tracking mechanism worth connecting to instead of duplicating. _(added 2026-08-16)_
- **`WORKERS_WEBHOOK_SECRET` rotation** — investigated, confirmed lower-urgency than it first looked, Royce: leave it for now. If picked up later: needs jvkn's vault AND eq-shell's Edge Function secret updated in the same window or the live Cards→SKS staff sync 401s. _(added 2026-08-16)_
- **The "Rollback" button on the activity log still doesn't work** — confirmed still broken, an earlier fix already made it fail with a clear message instead of crashing, and explicitly left the "build it for real, or remove the button" decision for Royce. Not decided again this session. _(added 2026-08-16)_
- **One database function has the same access-group blind spot as the Number Reviews fix above, not yet fixed** — `eq_revoke_session`. Noted, not actioned. _(added 2026-08-16)_
- **Not clicked through live** — verified against real production data directly, not by an actual admin opening the screen and watching Manager disappear from the list. Worth two minutes on a real admin account. _(added 2026-08-16)_
- **Testing this kind of database change on a safe, disposable copy first didn't work** — tried to spin one up before applying anything live, and discovered the database's own history of past changes can't currently rebuild itself from scratch on a fresh copy, unrelated to this fix. Spun off as its own follow-up (already running); until it's fixed, changes like this one have to be verified against the live database directly rather than on a safe copy first. _(added 2026-08-16)_
- **Cards' own copy of the shared role/permission rulebook is a few versions behind** — old enough that it doesn't know about the new narrower "who can change someone's role" permission at all. Not required for this fix (handled a different way instead, described above) but worth catching up eventually so Cards can check permissions the same direct way Shell does. _(added 2026-08-16)_
- **The remaining 46 actions with the same missing check** — spans account-security settings, GM Reports, Labour Hire, Intake, file uploads, and invites. Deliberately not bundled into the same fix (would've been the biggest change of this kind ever made to this app in one go); instead handed off as a prioritised follow-up, account-security actions first. Already picked up and running in separate sessions. _(added 2026-08-16)_
- **Not walked through live by a human.** Verified directly against the real site — as a signed-out visitor, as different roles, on both database checks — and the automated checks are all green, but worth your own two-minute look given how many pages this touches. _(added 2026-08-16)_
- **Not clicked through live** — confirmed by tests and by calling the affected screen's backend directly, not by an actual person building a group in the UI and watching the dangerous options disappear. Worth two minutes on a real admin account. _(added 2026-08-16)_
_…and 490 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Still not applied to the live database — checked directly, and Royce turned down the shortcut that would have unblocked it today.** Confirmed merging the PR didn't secretly switch it on. Turning it on for real right now would lock the people who haven't signed in yet out of their own timesheet and leave the moment they do, since the fix depends on their login already being linked to their staff record — 37 of 83 active SKS staff, checked again today. A workaround exists (let just those specific people keep today's wider access until they sign in, instead of holding up everyone else) but Royce said no — waiting for them to actually sign in through the real onboarding process instead, however long that takes. _(added 2026-08-16, decision confirmed 2026-08-16)_
- **The disposable EQ-side tenant doesn't have this fix** — lower priority, since that tenant holds no real data, but the identical gap exists there too and needs some prerequisite pieces built first before it can be ported. _(added 2026-08-16)_
- **Run the first real weekly export/import test** — SKS NSW Labour → Export Schedule CSV → EQ Field (logged in as the SKS org) → Import Schedule CSV. Discussed and confirmed safe; not actually run this session. _(added 2026-08-14)_
- **Deactivate the two stale site rows in ehow** — `Erilyan` (`site_id 6c221319…`, code EC6) and `Microsoft SYD27` (`site_id 7fb2d662…`, code SYD27). Single-column `active=false` flip each, no code change, no deploy — Royce hasn't given the explicit go to execute it yet. _(added 2026-08-14)_
- **~7 SKS staff missing from EQ Field's staff table** (hired since the 5 Jul snapshot): Ahmed Masaud, Amir Farid, Callum Treharne, Jhon Jairo Velasquez Meneses, Nabeel Hussain, Paul Bolger, Timothy Sue — plus a handful of name-string mismatches (e.g. "Bruno Pedrosa" vs "Bruno Vita Pedrosa", "Jose Quintanilla" vs "Jose Luis Quintanilla Rodriguez"). Royce said he'll manage this himself via EQ Field's People admin. _(added 2026-08-14)_
- **Leave sync parked deliberately** — an imported leave code lands on `schedule_entries.leave_type` directly, not in `app_data.leave_requests`, so it displays but carries no approver/audit trail. Royce explicitly scoped this session to roster only; leave is its own future task. _(added 2026-08-14)_
- **`SKS-FIELD-PARALLEL-RUN-LOG.md` and the "EQ Field parallel-run restarted" entry below are now stale** — both assume manual entry hadn't started; live data shows it has, informally. Worth a proper reconcile pass — out of scope for this session's /close. _(added 2026-08-14)_
- **Optional code fix, not required**: the roster site-map query in `eq-field/scripts/supabase.js` (~line 992) filters on `active=eq.true` only, not `field_enabled` — a small latent gap (found live) unrelated to the SYD27/EC6 fix above; deactivating the stale rows sidesteps it, so this is cosmetic cleanup only if ever revisited. _(added 2026-08-14)_
- **Richard needs to re-add his LV Rescue photo** — none of the 6 attempts ever actually captured one; the surviving row has the licence details but no photo. _(added 2026-08-13)_
- **Underlying Cards mobile bug not yet fixed** — a licence "renewal" can silently save nothing if on-device OCR can't read the card and the user doesn't notice the date field still shows the old value. Worth watching for other workers hitting the same silent failure until eq-cards ships the fix. _(added 2026-08-11)_
_…and 72 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise. Open splits engineering backlog from Royce's own queue (a confirm, a click-through, a call) — the two used to be counted together here, which made the number look worse than the real engineering backlog actually is; the split matches 'Waiting on you' above._

| File | Lines | Open (eng / you) | Done (unrotated) | Aging 45d+ |
|------|------:|------------------:|------------------:|------------:|
| [EQ](eq/pending.md) | 3728 | 508 / 147 | 131 | 89 |
| [SKS](sks/pending.md) | 438 | 83 / 9 | 1 | 15 |
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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-17 09:59 UTC._
