---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-15
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-15 02:12 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-15 02:07 UTC → 2026-08-15 02:12 UTC)

- Merged: eq-shell [#1346](https://github.com/eq-solutions/eq-shell/pull/1346) feat(staff): apprentice year badge + multi-select Trade on S
- Merged: eq-shell [#1344](https://github.com/eq-solutions/eq-shell/pull/1344) feat(nav): Reports landing page — GM Reports as the first op
- Merged: eq-shell [#1341](https://github.com/eq-solutions/eq-shell/pull/1341) chore(ci): triage eq_cards_admin_list_stale_invites into KNO
- Merged: eq-shell [#1338](https://github.com/eq-solutions/eq-shell/pull/1338) fix(staff): surface documents_not_extracted from ocr-licence
- Merged: eq-shell [#1337](https://github.com/eq-solutions/eq-shell/pull/1337) feat(admin): hard-delete for archived user accounts
- Merged: eq-shell [#1335](https://github.com/eq-solutions/eq-shell/pull/1335) feat(staff): step through every document found in a multi-ca
- Merged: eq-shell [#1334](https://github.com/eq-solutions/eq-shell/pull/1334) feat(documents): move document-version uploads to direct-to-
- Merged: eq-solves-service [#731](https://github.com/eq-solutions/eq-service/pull/731) fix(reports): drop dead ACB-only fields from NSX Test Report

## ⚠ Needs you (4)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-24 (P1 — OPEN, found 2026-08-08) — `QUOTES_CRON_SECRET` on eq-shell stored `is_secret: false` — full plaintext retu · [security-register.md](ops/security-register.md)
- 🟠 **Sentry new error** — `eq-shell` [Error: workers.staff_id shared by multiple workers on jvkn: ](https://eq-solutions.sentry.io/issues/140574570/)

## 🙋 Waiting on you (162)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Nothing alerts on this yet.** Recording a lockout is not the same as being told about one. The two questions worth alerting on — who got locked out in the last 24 hours, and who had the password right but never cleared the second step — are written and tested, but have to be run by hand. Turning either into a real alert is separate work and needs your call on where it should land. _(added 2026-08-15, needs your call)_
- **EQ** · **Neither half click-tested on a real phone** — verified by `flutter analyze`, 283 passing tests, full CI on both repos and the ancestry check, not by actually scanning an old `/claim?tenant=sks` poster or walking a fresh sign-in. Worth Royce doing both once. _(added 2026-08-15)_
- **EQ** · **`eq_cards_lookup_invite_by_phone` still has anon EXECUTE on jvkn** — this session removed its last caller, so it is now an unused anon phone-enumeration surface. Revoking it needs a live DB migration plus removing the `cards-api` op and updating `check-tenant-drift.mjs` (~line 599), so it was raised as a chip (`task_5264c029`) rather than done in passing. _(added 2026-08-15, needs your call)_
- **EQ** · **Not click-tested in a browser** — both sign-in doors were checked by calling them directly on production (an unknown mobile and an unknown email each return an identical "no" with no extra detail; the unauthed session check still refuses correctly) plus full CI, but nobody signed in through the actual page. Worth Royce trying two things on his phone: a *wrong* PIN, and a number that has *no* PIN set — both should now show the same "That number and PIN didn't match. If you haven't set a PIN yet, use 'Text me a code instead'". Then sign in by text on an account with no PIN and confirm the "Set a PIN" prompt still appears on the Home screen — that prompt is now the only place that guidance is given. _(added 2026-08-15)_
- **EQ** · **Today's Actions vs Outstanding Works can still contradict each other for up to 10 minutes** — found while reviewing the same screenshots (separate issue from the compliance-card redundancy, not addressed by this build): Today's Actions is cached 10 min per user (`ai-briefing.ts`), Outstanding Works refetches every 60s off the same table. Resolving a Service item mid-cache-window shows "overdue" in one card and "nothing overdue" in the other, same screen, same moment. Needs Royce's call: shrink the cache TTL, or add a "generated Xm ago" stamp so it reads as expected staleness rather than a bug. _(added 2026-08-14)_
- **EQ** · **Not click-tested live on a real tenant** — verified via `tsc -b --force`, eslint (clean except pre-existing tolerated patterns already present identically in `Suppliers.tsx`/`LabourHireRates.tsx`, not introduced by this change), full CI, and the Netlify deploy preview build succeeding. A local click-through attempt hit a pre-existing sandbox limitation (`VITE_FIELD_URL` unset crashes the app at module scope, unrelated to this change) and was abandoned per the standing "default browser only" rule rather than switched to Chrome for a low-value local check. Worth Royce opening Suppliers, Compliance report, and the mobile Home on his phone once. _(added 2026-08-14)_
- **EQ** · **Not click-tested live** — the 4-hour session cap and its background-refresh recovery were verified by full test suite + source tracing + a live production version-banner check, not by actually leaving a real signed-in Field session open past 4 hours and watching it recover. _(added 2026-08-14)_
- **EQ** · **Not deployed** — merged to `main`, but core.eq.solutions production deploys are explicit-only (merging doesn't auto-deploy on this repo, by design). Royce to trigger when ready. _(added 2026-08-14)_
- **EQ** · **Not click-tested live** — verified via `tsc -b --force`, eslint, full CI (all green), and the Netlify deploy preview build succeeding — not by clicking through a real signed-in session. _(added 2026-08-14)_
- **EQ** · **Not click-tested against a real generated NSX report** — fix verified via typecheck + code trace only; worth Royce pulling a real NSX Test Report next time one's generated to eyeball the CB Details table looks right. _(added 2026-08-14)_
- **EQ** · **Decide the long-term fix for nav-visibility drift.** Three real drift incidents found and fixed this session (Cards' duplicate workspace-switcher/join-QR widgets, Field's ungated desktop Add Person, Service's stale embedded nav bar) all trace to the same root cause: no shared source of truth for "what's in the nav and who can see it" across the four apps. `eq/identity/nav-access-matrix.md` lays out two options — a shared roles-derived config each app imports, or a lighter review checklist — not decided, Royce's call. _(added 2026-08-14)_
- **EQ** · **Not live-tested today** — this was code-level assurance (plus an old "confirmed live" comment already in the code from an earlier check), not a fresh click-through with a real pre-existing Cards account before the mass send goes out. _(added 2026-08-14)_
_…and 150 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 5 | 0d |
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
| 2026-08-15 | eq-shell | [#1364](https://github.com/eq-solutions/eq-shell/pull/1364) fix(security): revoke authenticated EXECUTE on eq_update_staff |
| 2026-08-15 | eq-shell | [#1363](https://github.com/eq-solutions/eq-shell/pull/1363) docs(migrations): retire the stale tenant migration ledger |
| 2026-08-15 | eq-shell | [#1359](https://github.com/eq-solutions/eq-shell/pull/1359) refactor(auth): fold the login timing-burn hash into one shared m |
| 2026-08-14 | eq-shell | [#1357](https://github.com/eq-solutions/eq-shell/pull/1357) feat(audit): make login outcomes queryable across all three doors |
| 2026-08-14 | eq-shell | [#1358](https://github.com/eq-solutions/eq-shell/pull/1358) perf(staff): one staff-bootstrap request instead of eight cold st |
| 2026-08-14 | eq-shell | [#1356](https://github.com/eq-solutions/eq-shell/pull/1356) perf(shell): self-host Plus Jakarta Sans, drop the render-blockin |
| 2026-08-14 | eq-shell | [#1361](https://github.com/eq-solutions/eq-shell/pull/1361) chore(admin): retire the redeem-an-invite worker QR, leaving one  |
| 2026-08-14 | eq-shell | [#1354](https://github.com/eq-solutions/eq-shell/pull/1354) fix(auth): link_pending_invites writes the tenant membership row, |
| 2026-08-14 | eq-shell | [#1352](https://github.com/eq-solutions/eq-shell/pull/1352) feat(auth): platform-admin endpoint to correct a standalone user' |
| 2026-08-14 | eq-shell | [#1353](https://github.com/eq-solutions/eq-shell/pull/1353) fix(security): gate staff-update on field.manage_people, not the  |
| 2026-08-14 | eq-shell | [#1355](https://github.com/eq-solutions/eq-shell/pull/1355) fix(auth): close account-enumeration oracle on the phone+PIN logi |
| 2026-08-14 | eq-shell | [#1350](https://github.com/eq-solutions/eq-shell/pull/1350) fix(auth): dual-key shell-login's rate limit on IP + email, close |
| 2026-08-14 | eq-shell | [#1351](https://github.com/eq-solutions/eq-shell/pull/1351) perf(shell): route-split admin pages, load pdf.js on demand, cach |
| 2026-08-14 | eq-shell | [#1347](https://github.com/eq-solutions/eq-shell/pull/1347) fix(auth): admin phone change now updates the login identity, not |
| 2026-08-14 | eq-shell | [#1349](https://github.com/eq-solutions/eq-shell/pull/1349) fix(audit): log user.deactivated/reactivated in edit-user.ts |
_Showing 15 of 117 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **No sign-in has happened yet since it went live, so nothing has been recorded in practice.** The code is live on core.eq.solutions and it writes the same way sign-ins are already recorded today, so there's no reason to expect trouble — but the first real proof arrives with the next actual sign-in. Worth a look at the log once a few people have signed in tomorrow. _(added 2026-08-15)_
- **Cards has a fully built PIN lock screen that nothing mounts** — `pin_entry_screen.dart` + `app_lock_notifier.dart` + `app_lock_state.dart`, not registered in the router and imported by nothing. Either wire it up or delete it; chip raised (`task_4e685ee7`). _(added 2026-08-15)_
- **#1365's rough edge**: `StaffPage.tsx`'s licence query has no client-side gate for excluded roles — degrades to a silent "No licences recorded" rather than an informative message. `EntityBrowserPage.tsx`'s timesheet view does surface a clear error. Real polish, not scoped into the security fix. Chip `task_e97a18c2` is unrelated (Dependabot) — this doesn't have a chip yet. _(added 2026-08-15)_
- **2 high-severity Dependabot alerts on eq-shell's default branch** — surfaced on push, not yet triaged. Chip `task_e97a18c2`. _(added 2026-08-15)_
- **No automated check exists to catch the cache-tag mistake above** — flagged 5 times now in eq-field's own changelog history, never built. Spun off as its own task (`task_9bd3247c`), already started in a separate session. _(added 2026-08-14)_
- **Follow-up question raised, being checked now**: if a worker's phone number genuinely changes, is there an admin-facing way in eq-shell to update it on their existing account (so OTP login works with the new number under the same identity), or would that need an out-of-band fix today? _(added 2026-08-14)_
- **Not yet confirmed by Tom actually retrying** — the fix is live, but nobody's re-tested his specific photo since deploy. _(added 2026-08-14)_
- **Shell's own styling and the shared `@eq-solutions/ui` design library define colliding layout style names** (`eq-hub` and friends) — noticed while fixing the scroll bug above, not the cause of it, not yet looked into properly. _(added 2026-08-14)_
- **Minor, unrelated gap noticed in passing**: `admin.deactivate_user` is declared in the permission matrix but never actually checked anywhere — `edit-user.ts`'s archive/restore action (and now `delete-user.ts`) both gate on `admin.edit_user` instead. Harmless today since the two keys are granted to the same roles, but if they're ever meant to diverge, deactivate silently wouldn't. _(added 2026-08-14)_
- **No manual browser smoke test yet** — need to actually expire a session mid-form-submit on a few touched pages and confirm the friendly "sign in again" message renders, rather than just type/unit verification. _(added 2026-08-14)_
_…and 455 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 3590 | 475 / 153 | 110 | 59 |
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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-15 02:12 UTC._
