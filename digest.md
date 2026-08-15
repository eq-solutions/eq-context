---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-15
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-15 04:36 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-15 04:26 UTC → 2026-08-15 04:36 UTC)

- Merged: eq-shell [#1372](https://github.com/eq-solutions/eq-shell/pull/1372) docs(migrations): record 2026_08_15c as applied + the one-ti
- Merged: eq-shell [#1356](https://github.com/eq-solutions/eq-shell/pull/1356) perf(shell): self-host Plus Jakarta Sans, drop the render-bl
- Merged: eq-shell [#1354](https://github.com/eq-solutions/eq-shell/pull/1354) fix(auth): link_pending_invites writes the tenant membership
- Merged: eq-shell [#1353](https://github.com/eq-solutions/eq-shell/pull/1353) fix(security): gate staff-update on field.manage_people, not
- Merged: eq-shell [#1350](https://github.com/eq-solutions/eq-shell/pull/1350) fix(auth): dual-key shell-login's rate limit on IP + email, 
- Merged: eq-shell [#1348](https://github.com/eq-solutions/eq-shell/pull/1348) feat(reports): compliance report + mobile Home quick links, 
- Merged: eq-shell [#1347](https://github.com/eq-solutions/eq-shell/pull/1347) fix(auth): admin phone change now updates the login identity
- Merged: eq-shell [#1345](https://github.com/eq-solutions/eq-shell/pull/1345) fix(auth): default self-join QR/link codes to 7-day expiry

## ⚠ Needs you (4)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-24 (P1 — OPEN, found 2026-08-08) — `QUOTES_CRON_SECRET` on eq-shell stored `is_secret: false` — full plaintext retu · [security-register.md](ops/security-register.md)
- 🟠 **Sentry new error** — `eq-shell` [Error: workers.staff_id shared by multiple workers on jvkn: ](https://eq-solutions.sentry.io/issues/140574570/)

## 🙋 Waiting on you (163)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Quote records (create/edit/delete) were deliberately left open to everyone** — Royce's call, not a gap. Worth a second look later if quote data starts needing tighter control. _(added 2026-08-15)_
- **EQ** · **The email sign-in door reaches 22 of 73 accounts, and none of the six apprentices.** Shipping it didn't change that and can't: a worker still has no way to add an email to their own account. The email on the profile screen is a contact detail that travels with the street address — 73 of 101 worker records have one, but only 17 of those match an actual login. The remaining 58 were typed by admins and never verified, so they must never become logins without the worker proving they own the address. A verified add-an-email flow is the only thing that moves the 22. _(added 2026-08-15, needs your call on priority)_
- **EQ** · **Real gap found, not fixed: a "deactivated" account can still sign in and write data.** Flipping the deactivated switch on Richard's duplicate account didn't actually stop it — it kept authenticating and pushing profile updates for two days afterward, because at least one sync endpoint only checks "is this a valid session" and never checks whether the account was deactivated. Needs its own look at how many places have this gap and what "deactivated" should actually do to a live session — not something to patch as a side effect of one cleanup. _(added 2026-08-15, needs your call on priority)_
- **EQ** · **Nothing alerts on this yet.** Recording a lockout is not the same as being told about one. The two questions worth alerting on — who got locked out in the last 24 hours, and who had the password right but never cleared the second step — are written and tested, but have to be run by hand. Turning either into a real alert is separate work and needs your call on where it should land. _(added 2026-08-15, needs your call)_
- **EQ** · **Neither half click-tested on a real phone** — verified by `flutter analyze`, 283 passing tests, full CI on both repos and the ancestry check, not by actually scanning an old `/claim?tenant=sks` poster or walking a fresh sign-in. Worth Royce doing both once. _(added 2026-08-15)_
- **EQ** · **Not click-tested in a browser** — both sign-in doors were checked by calling them directly on production (an unknown mobile and an unknown email each return an identical "no" with no extra detail; the unauthed session check still refuses correctly) plus full CI, but nobody signed in through the actual page. Worth Royce trying two things on his phone: a *wrong* PIN, and a number that has *no* PIN set — both should now show the same "That number and PIN didn't match. If you haven't set a PIN yet, use 'Text me a code instead'". Then sign in by text on an account with no PIN and confirm the "Set a PIN" prompt still appears on the Home screen — that prompt is now the only place that guidance is given. _(added 2026-08-15)_
- **EQ** · **Today's Actions vs Outstanding Works can still contradict each other for up to 10 minutes** — found while reviewing the same screenshots (separate issue from the compliance-card redundancy, not addressed by this build): Today's Actions is cached 10 min per user (`ai-briefing.ts`), Outstanding Works refetches every 60s off the same table. Resolving a Service item mid-cache-window shows "overdue" in one card and "nothing overdue" in the other, same screen, same moment. Needs Royce's call: shrink the cache TTL, or add a "generated Xm ago" stamp so it reads as expected staleness rather than a bug. _(added 2026-08-14)_
- **EQ** · **Not click-tested live on a real tenant** — verified via `tsc -b --force`, eslint (clean except pre-existing tolerated patterns already present identically in `Suppliers.tsx`/`LabourHireRates.tsx`, not introduced by this change), full CI, and the Netlify deploy preview build succeeding. A local click-through attempt hit a pre-existing sandbox limitation (`VITE_FIELD_URL` unset crashes the app at module scope, unrelated to this change) and was abandoned per the standing "default browser only" rule rather than switched to Chrome for a low-value local check. Worth Royce opening Suppliers, Compliance report, and the mobile Home on his phone once. _(added 2026-08-14)_
- **EQ** · **Not click-tested live** — the 4-hour session cap and its background-refresh recovery were verified by full test suite + source tracing + a live production version-banner check, not by actually leaving a real signed-in Field session open past 4 hours and watching it recover. _(added 2026-08-14)_
- **EQ** · **Not click-tested live** — verified via `tsc -b --force`, eslint, full CI (all green), and the Netlify deploy preview build succeeding — not by clicking through a real signed-in session. _(added 2026-08-14)_
- **EQ** · **Not click-tested against a real generated NSX report** — fix verified via typecheck + code trace only; worth Royce pulling a real NSX Test Report next time one's generated to eyeball the CB Details table looks right. _(added 2026-08-14)_
- **EQ** · **Decide the long-term fix for nav-visibility drift.** Three real drift incidents found and fixed this session (Cards' duplicate workspace-switcher/join-QR widgets, Field's ungated desktop Add Person, Service's stale embedded nav bar) all trace to the same root cause: no shared source of truth for "what's in the nav and who can see it" across the four apps. `eq/identity/nav-access-matrix.md` lays out two options — a shared roles-derived config each app imports, or a lighter review checklist — not decided, Royce's call. _(added 2026-08-14)_
_…and 151 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 1 | — |
| eq-solves-service | ✓ success | 0d ago | 0 | — |
| eq-field | ✓ success | 0d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 1 | — |
| eq-solves-intake | ✓ success | 3d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: staff-licence-ocr: ocr-licence returned 504](https://eq-solutions.sentry.io/issues/135986280/) | 5 | 2026-08-14 |
| eq-shell | [Error: Unresolved identity collisions detected on jvkn: 1](https://eq-solutions.sentry.io/issues/136887159/) | 3 | 2026-08-14 |
| eq-shell | [Error: workers.staff_id shared by multiple workers on jvkn: 1](https://eq-solutions.sentry.io/issues/140574570/) | 2 | 2026-08-14 |
| eq-cards | [minified:a42: FunctionException(status: 502, details: {error: anthropic_upstream](https://eq-solutions.sentry.io/issues/140383786/) | 1 | 2026-08-13 |
| eq-solves-service | [Error: An unexpected response was received from the server.](https://eq-solutions.sentry.io/issues/139724869/) | 1 | 2026-08-09 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-15 | eq-shell | [#1372](https://github.com/eq-solutions/eq-shell/pull/1372) docs(migrations): record 2026_08_15c as applied + the one-time se |
| 2026-08-15 | eq-shell | [#1371](https://github.com/eq-solutions/eq-shell/pull/1371) fix(security): refuse writes from a deactivated account's live se |
| 2026-08-15 | eq-shell | [#1370](https://github.com/eq-solutions/eq-shell/pull/1370) fix(security): revoke the Supabase Auth session when Shell deacti |
| 2026-08-15 | eq-shell | [#1369](https://github.com/eq-solutions/eq-shell/pull/1369) docs(auth): active-user-guard claimed the cookie path was covered |
| 2026-08-15 | eq-shell | [#1368](https://github.com/eq-solutions/eq-shell/pull/1368) chore(cards-api): retire the lookup_invite_by_phone op, dead sinc |
| 2026-08-15 | eq-shell | [#1367](https://github.com/eq-solutions/eq-shell/pull/1367) fix(security): a deactivated shell_control.users account can stil |
| 2026-08-15 | eq-shell | [#1362](https://github.com/eq-solutions/eq-shell/pull/1362) fix(security): role-gate 21 CRM/staff RPCs that only checked tena |
| 2026-08-15 | eq-shell | [#1360](https://github.com/eq-solutions/eq-shell/pull/1360) chore(identity): remove 7 orphaned test identities from the June  |
| 2026-08-15 | eq-shell | [#1366](https://github.com/eq-solutions/eq-shell/pull/1366) chore(security): retire staff-update.ts |
| 2026-08-15 | eq-shell | [#1365](https://github.com/eq-solutions/eq-shell/pull/1365) fix(security): gate timesheet/licence reads on the split-out keys |
| 2026-08-15 | eq-shell | [#1364](https://github.com/eq-solutions/eq-shell/pull/1364) fix(security): revoke authenticated EXECUTE on eq_update_staff |
| 2026-08-15 | eq-shell | [#1363](https://github.com/eq-solutions/eq-shell/pull/1363) docs(migrations): retire the stale tenant migration ledger |
| 2026-08-15 | eq-shell | [#1359](https://github.com/eq-solutions/eq-shell/pull/1359) refactor(auth): fold the login timing-burn hash into one shared m |
| 2026-08-15 | eq-cards | [#249](https://github.com/eq-solutions/eq-cards/pull/249) chore(auth): revoke the dead invite-lookup RPC anon grant, delete |
| 2026-08-14 | eq-shell | [#1357](https://github.com/eq-solutions/eq-shell/pull/1357) feat(audit): make login outcomes queryable across all three doors |
_Showing 15 of 115 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **One low-traffic function on the EQ side accepts an org ID as a plain parameter instead of reading it from the login session** — the table it writes to is empty today so there's nothing to lose, but it's a different shape of risk from everything else fixed here and wasn't touched. _(added 2026-08-15)_
- **Global CLAUDE.md still says eq-shell is manual-deploy-only.** It isn't — merging to main starts a production deploy that is live 2-3 seconds later, unattended, confirmed again this session by matching merge times against deploy times. That file is yours to edit. Until it's corrected every session starts from a false deploy posture, and this is the guard the ratchet has now flagged for promotion after failing twice (F13). _(added 2026-08-15, needs your edit)_
- **Where the 7 deleted test logins came from was never explained.** Each had a Core identity naming SKS but no company invite, so the sign-up fault repaired this session cannot have created them. Creation stopped on its own at the end of June and none have appeared since. Harmless now they're gone, but the door that made them is still unidentified. _(added 2026-08-15)_
- **The new standalone-worker tool has never been used on a real account.** It has tests and clean CI, but the first genuine run will be someone's actual login. Richard Brown was the obvious safe first case since he was already a known duplicate — that's since been cleaned up separately, so the next candidate is whoever asks first. Worth doing one deliberate supervised run before it's needed under pressure. _(added 2026-08-15)_
- **Cards carries a fully built licence card component that nothing displays** — 404 lines across six classes, plus a maintained test file, superseded by the tiles built into the wallet screen. Safe to delete, but it is not a one-liner and wasn't in scope here. _(added 2026-08-15)_
- **Shell's intake review flow has no buttons.** Both halves — approve and reject staged rows — are fully written and reachable over the network, but nothing in the app calls either. Reviewers can stage rows and then cannot act on them. Either wire it up or retire it. _(added 2026-08-15)_
- **No skill exists for the drift audit this session ran by hand.** Worth encoding, with one caveat learned the hard way: 4 of 6 "dead code" candidates were false positives (factory constructors, static helpers, same-file use). The pattern-matching is trivial; the verification is the entire job, and a skill that emits candidates without forcing the check would generate confident nonsense at scale. _(added 2026-08-15)_
- **That automated guard is not built — deliberately.** A check that scans wording across 600+ open items and every session log could easily misfire, and a false alarm on this repo blocks every session from saving work. Wants a proper test pass against the real files first, not a quick add. _(added 2026-08-15)_
- **A safety guard is misfiring three different ways and pushing sessions toward workarounds.** The rule meant to block risky git operations in the shared folder also blocks them in a fresh isolated copy where they're completely safe — it checks the wrong location — and it then blocked a session-log write purely because the log *text* quoted the command while describing this very problem. A guard that blocks you for writing about it can't be reported from inside a session. Cost three blocked attempts and two workarounds today. The same bug class was noted about a sibling guard on 2026-08-14 and never fixed. _(added 2026-08-15)_
- **Further squeezing is possible but lower value** — a smaller vendor library could be deferred too (~80KB), the Staff page's functions could be kept artificially warm to dodge the cold-start delay entirely (ongoing cost, not a one-off fix), and one more internal database lookup could be cached. None built — diminishing returns after the fixes above, and each has its own trade-off worth weighing on its own. _(added 2026-08-15)_
_…and 461 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 3629 | 480 / 154 | 119 | 59 |
| [SKS](sks/pending.md) | 432 | 81 / 8 | 1 | 15 |
| [SKS active](sks/active.md) | 109 | 0 / 0 | 0 | 0 |
| [OPS](ops/pending.md) | 409 | 32 / 4 | 0 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-15 | [staff-update was gating an HR write on a read permission; fixed, shipped, and corrected the repo's deploy model on the way](sessions/2026-08-15.md) |
| 2026-08-14 | [SKS → EQ Field weekly roster CSV sync: investigated live, confirmed feasible with zero new code](sessions/2026-08-14.md) |
| 2026-08-13 | [eq-shell PR #1316: misdiagnosed build error, real cause was a pdfjs-dist v6 type break, fixed + merged + deployed clean](sessions/2026-08-13.md) |
| 2026-08-12 | [EQ UI design sprint (EmptyState, density mode, DateRangePicker) shipped and rolled out to eq-shell + eq-service](sessions/2026-08-12.md) |
| 2026-08-11 | [EQ Cards: removed dead CardScreen (710 lines), merged live](sessions/2026-08-11.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-15 04:36 UTC._
