---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-16
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-16 09:13 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-16 08:57 UTC → 2026-08-16 09:13 UTC)

- Merged: eq-shell [#1379](https://github.com/eq-solutions/eq-shell/pull/1379) fix(perms): re-vendor Field fine-grained perms — 3 new keys 
- Merged: eq-shell [#1376](https://github.com/eq-solutions/eq-shell/pull/1376) feat(staff): scope credential requirements by role
- Merged: eq-shell [#1373](https://github.com/eq-solutions/eq-shell/pull/1373) fix(staff): stop cards-approve-staff.ts from creating duplic
- Merged: eq-shell [#1372](https://github.com/eq-solutions/eq-shell/pull/1372) docs(migrations): record 2026_08_15c as applied + the one-ti
- Merged: eq-shell [#1371](https://github.com/eq-solutions/eq-shell/pull/1371) fix(security): refuse writes from a deactivated account's li
- Merged: eq-shell [#1370](https://github.com/eq-solutions/eq-shell/pull/1370) fix(security): revoke the Supabase Auth session when Shell d
- Merged: eq-shell [#1368](https://github.com/eq-solutions/eq-shell/pull/1368) chore(cards-api): retire the lookup_invite_by_phone op, dead
- Merged: eq-solves-service [#738](https://github.com/eq-solutions/eq-service/pull/738) fix(security): wire entity.view on job-plans (missed by #716

## ⚠ Needs you (3)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-08-16.md](sessions/2026-08-16.md) · [failures.md](system/failures.md)
- 🟠 **Sentry new error** — `eq-shell` [auth-stall: render-crash](https://eq-solutions.sentry.io/issues/140924723/)

## 🙋 Waiting on you (156)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Two adjacent staff-approval screens require different levels of permission to do very similar things** — one needs a manager, another needs only a much more junior permission to view/act on the same underlying approval data. Doesn't look deliberate. Needs your call on whether they should match. _(added 2026-08-16)_
- **EQ** · **A merged duplicate can still show up looking "active" again after a page reload** — the screen doesn't fully know a pair was already merged until it's clicked into once. The real fix needs a small database change in EQ Shell (not this app), so it's fully scoped (exact change, which table, which migration number) but deliberately not built yet — spun off as its own follow-up rather than done inside this session, per Royce's call to leave it for that follow-up to pick up. _(added 2026-08-16)_
- **EQ** · **Not clicked through live in either state.** No safe way to produce a working Shell login locally to test the fixed version, and the standalone side has no working test account — the practice/demo login has been broken since a database move in June and was never reconnected. Worth Royce opening `core.eq.solutions/sks/service/settings` once to eyeball it for real. _(added 2026-08-16)_
- **EQ** · **Quote records (create/edit/delete) were deliberately left open to everyone** — Royce's call, not a gap. Worth a second look later if quote data starts needing tighter control. _(added 2026-08-15)_
- **EQ** · **The email sign-in door reaches 22 of 73 accounts, and none of the six apprentices.** Shipping it didn't change that and can't: a worker still has no way to add an email to their own account. The email on the profile screen is a contact detail that travels with the street address — 73 of 101 worker records have one, but only 17 of those match an actual login. The remaining 58 were typed by admins and never verified, so they must never become logins without the worker proving they own the address. A verified add-an-email flow is the only thing that moves the 22. _(added 2026-08-15, needs your call on priority)_
- **EQ** · **Nothing alerts on this yet.** Recording a lockout is not the same as being told about one. The two questions worth alerting on — who got locked out in the last 24 hours, and who had the password right but never cleared the second step — are written and tested, but have to be run by hand. Turning either into a real alert is separate work and needs your call on where it should land. _(added 2026-08-15, needs your call)_
- **EQ** · **Neither half click-tested on a real phone** — verified by `flutter analyze`, 283 passing tests, full CI on both repos and the ancestry check, not by actually scanning an old `/claim?tenant=sks` poster or walking a fresh sign-in. Worth Royce doing both once. _(added 2026-08-15)_
- **EQ** · **Not click-tested in a browser** — both sign-in doors were checked by calling them directly on production (an unknown mobile and an unknown email each return an identical "no" with no extra detail; the unauthed session check still refuses correctly) plus full CI, but nobody signed in through the actual page. Worth Royce trying two things on his phone: a *wrong* PIN, and a number that has *no* PIN set — both should now show the same "That number and PIN didn't match. If you haven't set a PIN yet, use 'Text me a code instead'". Then sign in by text on an account with no PIN and confirm the "Set a PIN" prompt still appears on the Home screen — that prompt is now the only place that guidance is given. _(added 2026-08-15)_
- **EQ** · **Today's Actions vs Outstanding Works can still contradict each other for up to 10 minutes** — found while reviewing the same screenshots (separate issue from the compliance-card redundancy, not addressed by this build): Today's Actions is cached 10 min per user (`ai-briefing.ts`), Outstanding Works refetches every 60s off the same table. Resolving a Service item mid-cache-window shows "overdue" in one card and "nothing overdue" in the other, same screen, same moment. Needs Royce's call: shrink the cache TTL, or add a "generated Xm ago" stamp so it reads as expected staleness rather than a bug. _(added 2026-08-14)_
- **EQ** · **Not click-tested live on a real tenant** — verified via `tsc -b --force`, eslint (clean except pre-existing tolerated patterns already present identically in `Suppliers.tsx`/`LabourHireRates.tsx`, not introduced by this change), full CI, and the Netlify deploy preview build succeeding. A local click-through attempt hit a pre-existing sandbox limitation (`VITE_FIELD_URL` unset crashes the app at module scope, unrelated to this change) and was abandoned per the standing "default browser only" rule rather than switched to Chrome for a low-value local check. Worth Royce opening Suppliers, Compliance report, and the mobile Home on his phone once. _(added 2026-08-14)_
- **EQ** · **Not click-tested live** — the 4-hour session cap and its background-refresh recovery were verified by full test suite + source tracing + a live production version-banner check, not by actually leaving a real signed-in Field session open past 4 hours and watching it recover. _(added 2026-08-14)_
- **EQ** · **Not click-tested live** — verified via `tsc -b --force`, eslint, full CI (all green), and the Netlify deploy preview build succeeding — not by clicking through a real signed-in session. _(added 2026-08-14)_
_…and 144 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 7 | 0d |
| eq-solves-service | ✓ success | 0d ago | 0 | — |
| eq-field | ✓ success | 0d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 1 | 0d |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: staff-licence-ocr: ocr-licence returned 504](https://eq-solutions.sentry.io/issues/135986280/) | 5 | 2026-08-14 |
| eq-shell | [Error: Unresolved identity collisions detected on jvkn: 1](https://eq-solutions.sentry.io/issues/136887159/) | 2 | 2026-08-14 |
| eq-shell | [auth-stall: render-crash](https://eq-solutions.sentry.io/issues/140924723/) | 1 | 2026-08-16 |
| eq-shell | [Error: Objects are not valid as a React child (found: object with keys {licence_](https://eq-solutions.sentry.io/issues/140924722/) | 1 | 2026-08-16 |
| eq-cards | [minified:a42: FunctionException(status: 502, details: {error: anthropic_upstream](https://eq-solutions.sentry.io/issues/140383786/) | 1 | 2026-08-13 |
| eq-solves-service | [Error: An unexpected response was received from the server.](https://eq-solutions.sentry.io/issues/139724869/) | 1 | 2026-08-09 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-16 | eq-shell | [#1400](https://github.com/eq-solutions/eq-shell/pull/1400) fix(security): P2 access-control sweep — 5 unchecked read endpoin |
| 2026-08-16 | eq-shell | [#1399](https://github.com/eq-solutions/eq-shell/pull/1399) fix(compliance): restore photo-ID equivalence dropped by role-sco |
| 2026-08-16 | eq-shell | [#1397](https://github.com/eq-solutions/eq-shell/pull/1397) fix(security): permission-model hygiene sweep — drift-test blind  |
| 2026-08-16 | eq-shell | [#1385](https://github.com/eq-solutions/eq-shell/pull/1385) fix(security): gate the Documents module on documents.view/manage |
| 2026-08-16 | eq-shell | [#1387](https://github.com/eq-solutions/eq-shell/pull/1387) fix(security): close the admin.manage_groups escalation path in s |
| 2026-08-16 | eq-shell | [#1386](https://github.com/eq-solutions/eq-shell/pull/1386) fix(security): origin-guard 2 Cards mutation/PII endpoints + 5 cl |
| 2026-08-16 | eq-shell | [#1384](https://github.com/eq-solutions/eq-shell/pull/1384) docs: confirm zaap Field write-guard absence is deliberate, not a |
| 2026-08-16 | eq-shell | [#1381](https://github.com/eq-solutions/eq-shell/pull/1381) fix(security): close 4 PII leaks gated on field.view/entity.view  |
| 2026-08-16 | eq-shell | [#1389](https://github.com/eq-solutions/eq-shell/pull/1389) chore(ci): triage 3 jvkn functions into KNOWN_UNSOURCED (cross-re |
| 2026-08-16 | eq-shell | [#1388](https://github.com/eq-solutions/eq-shell/pull/1388) fix(security): enforce admin.deactivate_user on edit-user.ts's ar |
| 2026-08-16 | eq-shell | [#1383](https://github.com/eq-solutions/eq-shell/pull/1383) chore(roles): finish v2.7.2 bump — enforce admin.assign_role/admi |
| 2026-08-16 | eq-shell | [#1382](https://github.com/eq-solutions/eq-shell/pull/1382) chore(roles): bump @eq-solutions/roles to v2.7.2, wire documents  |
| 2026-08-16 | eq-shell | [#1380](https://github.com/eq-solutions/eq-shell/pull/1380) fix(access-control): surface fine-grained Field perms from the Ba |
| 2026-08-16 | eq-shell | [#1375](https://github.com/eq-solutions/eq-shell/pull/1375) fix(security): stop SKS mint silently falling back to eq-canonica |
| 2026-08-16 | eq-shell | [#1377](https://github.com/eq-solutions/eq-shell/pull/1377) fix(security): gate 5 AI/OCR endpoints beyond session-only, const |
_Showing 15 of 113 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **The remaining 46 actions with the same missing check** — spans account-security settings, GM Reports, Labour Hire, Intake, file uploads, and invites. Deliberately not bundled into the same fix (would've been the biggest change of this kind ever made to this app in one go); instead handed off as a prioritised follow-up, account-security actions first. Already picked up and running in separate sessions. _(added 2026-08-16)_
- **Not walked through live by a human.** Verified directly against the real site — as a signed-out visitor, as different roles, on both database checks — and the automated checks are all green, but worth your own two-minute look given how many pages this touches. _(added 2026-08-16)_
- **Not clicked through live** — confirmed by tests and by calling the affected screen's backend directly, not by an actual person building a group in the UI and watching the dangerous options disappear. Worth two minutes on a real admin account. _(added 2026-08-16)_
- **One narrow follow-up, not urgent:** EQ's sandbox database still allows editing a couple of specific worker fields (licence status, agency, hire company) that SKS's side specifically blocks — nobody's checked whether that matters in practice. Low priority since it's sandbox data with no real customer on it, but worth a look if that database is ever used for anything real. _(added 2026-08-16)_
- **Not merged — needs your explicit go.** Merging this repo deploys to core.eq.solutions within seconds, and this touches who-can-see-what, so it waits for you rather than shipping on its own. _(added 2026-08-16)_
- **Not clicked through live** — worth confirming an apprentice or similar account gets turned away from the compliance report, sees no licence-review badges on Staff, and can no longer find a customer by typing part of a contact's email into search. _(added 2026-08-16)_
- When a company invites a worker to connect (instead of the worker applying to the company), the worker isn't offered the same share-choice — it's always full profile. Worth deciding if that's intentional; already being looked at in its own session. _(added 2026-08-16)_
- **Not clicked through live.** The database change is live on production now — worth two minutes to confirm a low-privilege account (apprentice/labour hire/subcontractor) actually gets blocked from writing, and that an assigned technician can still update their own job. Needs a real signed-in session, not checkable from here. _(added 2026-08-16)_
- **Not clicked through live yet.** Worth two minutes: try the AI import on a real file, look at the home-page briefing/ask bar as a manager vs. a supervisor, and try opening the licence-scan page as an apprentice (should now say you don't have access). _(added 2026-08-16)_
- **A real, bigger idea from Royce — one single screen for all access control, not two separate systems** — discussed and deliberately not built today; needs a proper design pass first (grouping ~86 total switches sensibly is its own problem), not a same-day PR. _(added 2026-08-16)_
_…and 477 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 3725 | 498 / 147 | 156 | 64 |
| [SKS](sks/pending.md) | 439 | 83 / 9 | 2 | 15 |
| [SKS active](sks/active.md) | 109 | 0 / 0 | 0 | 0 |
| [OPS](ops/pending.md) | 421 | 33 / 4 | 3 | 1 |

## Possible recurring failures (unconfirmed)

_Session logs mention a pattern matching a known failure below, dated after its last recorded occurrence. Not yet counted — if it's real, bump `recurrences` in [failures.md](system/failures.md) and `guard-ratchet.yml` proposes promotion on its own next run._

- **F5** (rung 0) — An ungoverned shadow memory overrode the canonical contract · 1 session since last recorded, most recent [2026-08-16.md](sessions/2026-08-16.md)

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-16 | [built a personal task register for Royce (OneDrive), cross-checked it live twice, found and cleared a false alarm on eq-context's git state](sessions/2026-08-16.md) |
| 2026-08-15 | [staff-update was gating an HR write on a read permission; fixed, shipped, and corrected the repo's deploy model on the way](sessions/2026-08-15.md) |
| 2026-08-14 | [SKS → EQ Field weekly roster CSV sync: investigated live, confirmed feasible with zero new code](sessions/2026-08-14.md) |
| 2026-08-13 | [eq-shell PR #1316: misdiagnosed build error, real cause was a pdfjs-dist v6 type break, fixed + merged + deployed clean](sessions/2026-08-13.md) |
| 2026-08-12 | [EQ UI design sprint (EmptyState, density mode, DateRangePicker) shipped and rolled out to eq-shell + eq-service](sessions/2026-08-12.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-16 09:13 UTC._
