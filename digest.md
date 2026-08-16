---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-16
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-16 05:40 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-16 04:57 UTC → 2026-08-16 05:40 UTC)

- Merged: eq-shell [#1379](https://github.com/eq-solutions/eq-shell/pull/1379) fix(perms): re-vendor Field fine-grained perms — 3 new keys 
- Merged: eq-shell [#1378](https://github.com/eq-solutions/eq-shell/pull/1378) feat(staff): let a manager scope a required ticket to one ro
- Merged: eq-shell [#1366](https://github.com/eq-solutions/eq-shell/pull/1366) chore(security): retire staff-update.ts
- Merged: eq-shell [#1363](https://github.com/eq-solutions/eq-shell/pull/1363) docs(migrations): retire the stale tenant migration ledger
- Merged: eq-shell [#1359](https://github.com/eq-solutions/eq-shell/pull/1359) refactor(auth): fold the login timing-burn hash into one sha
- Merged: eq-shell [#1357](https://github.com/eq-solutions/eq-shell/pull/1357) feat(audit): make login outcomes queryable across all three 
- Merged: eq-shell [#1356](https://github.com/eq-solutions/eq-shell/pull/1356) perf(shell): self-host Plus Jakarta Sans, drop the render-bl
- Merged: eq-shell [#1354](https://github.com/eq-solutions/eq-shell/pull/1354) fix(auth): link_pending_invites writes the tenant membership
- ⚠ Needs you: 4 → 5 (new items)

## ⚠ Needs you (5)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-24 (P1 — OPEN, found 2026-08-08) — `QUOTES_CRON_SECRET` on eq-shell stored `is_secret: false` — full plaintext retu · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-08-13.md](sessions/2026-08-13.md) · [failures.md](system/failures.md)
- 🟠 **Sentry new error** — `eq-shell` [auth-stall: render-crash](https://eq-solutions.sentry.io/issues/140924723/)

## 🙋 Waiting on you (153)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

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
- **EQ** · **Not click-tested against a real generated NSX report** — fix verified via typecheck + code trace only; worth Royce pulling a real NSX Test Report next time one's generated to eyeball the CB Details table looks right. _(added 2026-08-14)_
- **EQ** · **Decide the long-term fix for nav-visibility drift.** Three real drift incidents found and fixed this session (Cards' duplicate workspace-switcher/join-QR widgets, Field's ungated desktop Add Person, Service's stale embedded nav bar) all trace to the same root cause: no shared source of truth for "what's in the nav and who can see it" across the four apps. `eq/identity/nav-access-matrix.md` lays out two options — a shared roles-derived config each app imports, or a lighter review checklist — not decided, Royce's call. _(added 2026-08-14)_
_…and 141 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 3 | 0d |
| eq-solves-service | ✓ success | 0d ago | 3 | 0d |
| eq-field | ✓ success | 0d ago | 2 | 0d |
| eq-cards | ✓ success | 1d ago | 1 | — |
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
| 2026-08-16 | eq-shell | [#1379](https://github.com/eq-solutions/eq-shell/pull/1379) fix(perms): re-vendor Field fine-grained perms — 3 new keys not i |
| 2026-08-16 | eq-shell | [#1378](https://github.com/eq-solutions/eq-shell/pull/1378) feat(staff): let a manager scope a required ticket to one role |
| 2026-08-16 | eq-shell | [#1376](https://github.com/eq-solutions/eq-shell/pull/1376) feat(staff): scope credential requirements by role |
| 2026-08-16 | eq-shell | [#1374](https://github.com/eq-solutions/eq-shell/pull/1374) fix(security): gate EQ Ops Setup on ops.view_rates |
| 2026-08-16 | eq-solves-service | [#733](https://github.com/eq-solutions/eq-service/pull/733) fix(settings): defer Profile/Password to Shell for embedded sessi |
| 2026-08-16 | eq-field | [#704](https://github.com/eq-solutions/eq-field/pull/704) v3.5.503 — Email Templates: own permission key + moved to Manage |
| 2026-08-16 | eq-field | [#702](https://github.com/eq-solutions/eq-field/pull/702) v3.5.502 — access-control cleanup: Pipeline opt-in-only, Teams +  |
| 2026-08-16 | eq-solves-intake | [#117](https://github.com/eq-solutions/eq-solves-intake/pull/117) fix(intake): correctness fixes found reviewing #116's review-queu |
| 2026-08-16 | eq-solves-intake | [#116](https://github.com/eq-solutions/eq-solves-intake/pull/116) fix(intake): review-queue polish — already-merged bug, change-ans |
| 2026-08-15 | eq-shell | [#1373](https://github.com/eq-solutions/eq-shell/pull/1373) fix(staff): stop cards-approve-staff.ts from creating duplicate w |
| 2026-08-15 | eq-shell | [#1370](https://github.com/eq-solutions/eq-shell/pull/1370) fix(security): revoke the Supabase Auth session when Shell deacti |
| 2026-08-15 | eq-shell | [#1372](https://github.com/eq-solutions/eq-shell/pull/1372) docs(migrations): record 2026_08_15c as applied + the one-time se |
| 2026-08-15 | eq-shell | [#1371](https://github.com/eq-solutions/eq-shell/pull/1371) fix(security): refuse writes from a deactivated account's live se |
| 2026-08-15 | eq-shell | [#1369](https://github.com/eq-solutions/eq-shell/pull/1369) docs(auth): active-user-guard claimed the cookie path was covered |
| 2026-08-15 | eq-shell | [#1368](https://github.com/eq-solutions/eq-shell/pull/1368) chore(cards-api): retire the lookup_invite_by_phone op, dead sinc |
_Showing 15 of 118 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **No admin screen yet to add a role-specific requirement** — the groundwork supports it, but today the UI can only add a requirement that applies to everyone. Someone would need it done by hand until that control gets built. _(added 2026-08-16)_
- **The practice/demo account is still broken** — unrelated to this fix, but found while trying to test it. Sign-in intentionally hides the "try the demo" option because it fails every time; worth reseeding if the demo link is still wanted. _(added 2026-08-16)_
- **The original question — what Shell's access-control screen looks like for Service permissions — wasn't followed up.** This session only got as far as the settings-page bug that jumped out first; the permissions-matrix screenshot Royce shared is still unreviewed. _(added 2026-08-16)_
- Once resolved, update `punch-list.md` item 4's note to match reality — it currently still reads as if nothing shipped. _(added 2026-08-16)_
- **Write down the trade-off we accepted** — the new per-account limit means someone who knows a person's email address can deliberately lock that person out of Core for 15 minutes at a time by getting the PIN wrong five times. That is the normal, accepted cost of this kind of protection, and the phone sign-in door has always worked the same way, but it isn't recorded anywhere yet. Belongs in the security register so nobody "discovers" it later and treats it as a bug. _(added 2026-08-15)_
- **One low-traffic function on the EQ side accepts an org ID as a plain parameter instead of reading it from the login session** — the table it writes to is empty today so there's nothing to lose, but it's a different shape of risk from everything else fixed here and wasn't touched. _(added 2026-08-15)_
- **None of it has been tried on a real switched-off account.** Everything above is verified by tests and by calling the live endpoints unauthenticated, not by taking a real person's session and watching it get refused. Three switched-off accounts still attached to a company are available to test with whenever you want to spend ten minutes on it. _(added 2026-08-15)_
- **33 data-changing endpoints don't use the shared permission check** and so didn't get the new guard. Several are actually reads that a crude scan mislabelled, and a couple are internal background jobs — they need looking at one by one rather than a blanket fix, which is why they weren't swept in. _(added 2026-08-15)_
- **Where the 7 deleted test logins came from was never explained.** Each had a Core identity naming SKS but no company invite, so the sign-up fault repaired this session cannot have created them. Creation stopped on its own at the end of June and none have appeared since. Harmless now they're gone, but the door that made them is still unidentified. _(added 2026-08-15)_
- **The new standalone-worker tool has never been used on a real account.** It has tests and clean CI, but the first genuine run will be someone's actual login. Richard Brown was the obvious safe first case since he was already a known duplicate — that's since been cleaned up separately, so the next candidate is whoever asks first. Worth doing one deliberate supervised run before it's needed under pressure. _(added 2026-08-15)_
_…and 467 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Run the first real weekly export/import test** — SKS NSW Labour → Export Schedule CSV → EQ Field (logged in as the SKS org) → Import Schedule CSV. Discussed and confirmed safe; not actually run this session. _(added 2026-08-14)_
- **Deactivate the two stale site rows in ehow** — `Erilyan` (`site_id 6c221319…`, code EC6) and `Microsoft SYD27` (`site_id 7fb2d662…`, code SYD27). Single-column `active=false` flip each, no code change, no deploy — Royce hasn't given the explicit go to execute it yet. _(added 2026-08-14)_
- **~7 SKS staff missing from EQ Field's staff table** (hired since the 5 Jul snapshot): Ahmed Masaud, Amir Farid, Callum Treharne, Jhon Jairo Velasquez Meneses, Nabeel Hussain, Paul Bolger, Timothy Sue — plus a handful of name-string mismatches (e.g. "Bruno Pedrosa" vs "Bruno Vita Pedrosa", "Jose Quintanilla" vs "Jose Luis Quintanilla Rodriguez"). Royce said he'll manage this himself via EQ Field's People admin. _(added 2026-08-14)_
- **Leave sync parked deliberately** — an imported leave code lands on `schedule_entries.leave_type` directly, not in `app_data.leave_requests`, so it displays but carries no approver/audit trail. Royce explicitly scoped this session to roster only; leave is its own future task. _(added 2026-08-14)_
- **`SKS-FIELD-PARALLEL-RUN-LOG.md` and the "EQ Field parallel-run restarted" entry below are now stale** — both assume manual entry hadn't started; live data shows it has, informally. Worth a proper reconcile pass — out of scope for this session's /close. _(added 2026-08-14)_
- **Optional code fix, not required**: the roster site-map query in `eq-field/scripts/supabase.js` (~line 992) filters on `active=eq.true` only, not `field_enabled` — a small latent gap (found live) unrelated to the SYD27/EC6 fix above; deactivating the stale rows sidesteps it, so this is cosmetic cleanup only if ever revisited. _(added 2026-08-14)_
- **Richard needs to re-add his LV Rescue photo** — none of the 6 attempts ever actually captured one; the surviving row has the licence details but no photo. _(added 2026-08-13)_
- **Underlying Cards mobile bug not yet fixed** — a licence "renewal" can silently save nothing if on-device OCR can't read the card and the user doesn't notice the date field still shows the old value. Worth watching for other workers hitting the same silent failure until eq-cards ships the fix. _(added 2026-08-11)_
- **Declined this session, still open if wanted:** widen the Prestart tab past its hardcoded 7-day window, or add a "Show older → Records" link — Royce picked "fix the cap only" via AskUserQuestion; the tab itself is unchanged. _(added 2026-08-04)_
- **Stale SKS brand color found in the incident-alert email** (`#1F335C` vs. the corrected `#203060`) — spun off as a background task, ran in a separate session; outcome not visible from this session. _(added 2026-07-31)_
_…and 70 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise. Open splits engineering backlog from Royce's own queue (a confirm, a click-through, a call) — the two used to be counted together here, which made the number look worse than the real engineering backlog actually is; the split matches 'Waiting on you' above._

| File | Lines | Open (eng / you) | Done (unrotated) | Aging 45d+ |
|------|------:|------------------:|------------------:|------------:|
| [EQ](eq/pending.md) | 3597 | 486 / 145 | 125 | 64 |
| [SKS](sks/pending.md) | 432 | 81 / 8 | 1 | 15 |
| [SKS active](sks/active.md) | 109 | 0 / 0 | 0 | 0 |
| [OPS](ops/pending.md) | 421 | 33 / 4 | 3 | 1 |

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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-16 05:40 UTC._
