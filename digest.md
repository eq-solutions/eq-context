---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-30
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-30 10:25 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-30 10:13 UTC → 2026-07-30 10:25 UTC)

- Merged: eq-shell [#1129](https://github.com/eq-solutions/eq-shell/pull/1129) fix(audit): Suite Activity gets real filtering; correct EQ Q
- Merged: eq-shell [#1128](https://github.com/eq-solutions/eq-shell/pull/1128) fix(audit): stop entity.patched canonical_events noise
- Merged: eq-shell [#1111](https://github.com/eq-solutions/eq-shell/pull/1111) feat(ops): make ex-GST the prominent figure across EQ Ops
- Merged: eq-shell [#1109](https://github.com/eq-solutions/eq-shell/pull/1109) fix(mobile): mirror desktop's permission checks (Security Gr
- Merged: eq-shell [#1106](https://github.com/eq-solutions/eq-shell/pull/1106) chore(intake): re-vendor eq-intake/eq-platform — field-impor
- Merged: eq-shell [#1105](https://github.com/eq-solutions/eq-shell/pull/1105) fix(auth): register /login route so ?tenant= survives to Log
- Merged: eq-shell [#1103](https://github.com/eq-solutions/eq-shell/pull/1103) fix(invite): route phone-first worker activation through She
- Merged: eq-shell [#1100](https://github.com/eq-solutions/eq-shell/pull/1100) fix(suppliers): show all columns by default now that fullWid

## ⚠ Needs you (3)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F6: Append (>>) NUL-fills files on the C:\Projects virtiofs mount · possibly recurred in [2026-07-28.md](sessions/2026-07-28.md) · [failures.md](system/failures.md)

## 🙋 Waiting on you (97)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Moahmmed Elsayed's `photo_id`-typed licence row (number `0140988080`) not yet corrected** — unlike Maylin Ung's case (a driver's-licence-format number, fixed directly), this number doesn't match a recognisable pattern; needs Royce to confirm the actual document type before the DB row is corrected. _(added 2026-07-29)_
- **EQ** · **Royce to click through live**: invite a labour-hire worker with the box unchecked, confirm they land on a Field-free home screen and can't reach Field directly; then invite/sign in a normal worker (box left checked) and confirm nothing changed for them. Bundled with the three click-through items below into one live-testing pass — see that section's deferred note. _(added 2026-07-30)_
- **EQ** · **Royce to click through live, all four features shipped today together** (this section's three plus the compliance-roster-only switch above): invite/adjust a worker with Field access off; correct a test worker's phone number and confirm their old passcode stops working while a fresh sign-in + new passcode works; check the passcode-status view and try "Unlock now" on a locked test account; sign in as a phone-only worker and confirm the backup-email reminder shows, dismisses for that sign-in only, and clears once an email is added. None of this has been clicked through live yet — Claude can't perform this step directly (logging in requires entering a passcode, which falls under a hard rule against entering credentials on the user's behalf, even for the user's own product). _(added 2026-07-30)_
- **EQ** · **Royce to click through live**: open a job's detail view, the create-quote form, the kanban board, and each Reports tab, confirm ex-GST reads as the main figure everywhere it should. Verified via build + typecheck only, not yet clicked through live. _(added 2026-07-30)_
- **EQ** · **Royce to clear Brave's site data for cards.eq.solutions on his own phone** — the actual reported symptom (an old email-login screen). A Flutter service worker registered on that device before the phone-OTP flip is still serving its own cached copy of the old build; production itself is correctly configured (verified live). A full close + clear-site-data + reopen forces the fresh navigation the browser's update check needs. _(added 2026-07-29)_
- **EQ** · **Royce to reconcile a customer CSV with a messy phone number/ABN and confirm it now gets cleaned up** — verified in code + typecheck, not yet clicked through live. _(added 2026-07-29)_
- **EQ** · **Royce to click through live**: EQ Ops → "…" → Archived → open a quote via View, confirm it shows a read-only "Archived" badge and only Restore/Download/Delete (no Edit/Mark as Sent/Close/Archive controls), then confirm Restore still works from there. Verified only via the Netlify production deploy record (commit `2b01bf3b` live), not an actual click-through — no production login session in this environment. eq-shell [PR #1093](https://github.com/eq-solutions/eq-shell/pull/1093), merged. _(added 2026-07-29)_
- **EQ** · **Royce to click through the Import screen (`/intake`) on core.eq.solutions once the deploy lands** — confirm it still loads and still commits normally. That screen wasn't touched, but worth a look since it's the app's only working import path now. _(added 2026-07-29)_
- **EQ** · **Royce to click through Assets/Job Plans/Maintenance Checks once the deploy lands** — confirm the Export button's new dropdown offers CSV and Excel, both download the full list, and the Maintenance Checks "tasks completed" count now shows a real number instead of "/0". Not click-tested live this session — no login credentials available in this environment, verified via type-checking + the full automated test suite + code review only. _(added 2026-07-29)_
- **EQ** · **Royce to confirm live**: edit an already-reviewed licence's expiry/number in Cards for an approved worker, confirm the Staff page badge flips to "changed since — re-review needed" without a hard refresh. _(added 2026-07-28)_
- **EQ** · **Royce to confirm live**: reload the Wallet and confirm the Photo ID nag no longer shows for a worker who holds a Driver Licence or Passport. _(added 2026-07-28)_
- **EQ** · **Separate, lower-priority finding: 53 of 88 active SKS staff have a Cards worker link but zero credentials captured in Cards at all** (checked the pre-promotion `worker_credentials` table too — genuinely empty, not stuck mid-migration). Only 34 of 88 active staff have any licence data flowing through Shell. This is a Cards onboarding-completion gap, not a sync bug — no action taken, logging only per Royce's call. _(added 2026-07-28)_
_…and 85 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 1 | 0d |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 1 | 0d |

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-30 | eq-shell | [#1128](https://github.com/eq-solutions/eq-shell/pull/1128) fix(audit): stop entity.patched canonical_events noise |
| 2026-07-30 | eq-shell | [#1129](https://github.com/eq-solutions/eq-shell/pull/1129) fix(audit): Suite Activity gets real filtering; correct EQ Quotes |
| 2026-07-30 | eq-shell | [#1127](https://github.com/eq-solutions/eq-shell/pull/1127) chore(intake): re-vendor eq-intake/eq-platform — Tidy tab enum dr |
| 2026-07-30 | eq-shell | [#1126](https://github.com/eq-solutions/eq-shell/pull/1126) feat(audit): Suite activity tab — canonical_events as plain sente |
| 2026-07-30 | eq-shell | [#1125](https://github.com/eq-solutions/eq-shell/pull/1125) feat(auth): email-capture nudge — Email+PIN fallback for phone-on |
| 2026-07-30 | eq-shell | [#1124](https://github.com/eq-solutions/eq-shell/pull/1124) fix(admin): eq_list_tenant_users no longer drops deactivated user |
| 2026-07-30 | eq-shell | [#1123](https://github.com/eq-solutions/eq-shell/pull/1123) fix(audit): fn_audit() noise guard, take 2 — 0225's WHEN clause i |
| 2026-07-30 | eq-shell | [#1122](https://github.com/eq-solutions/eq-shell/pull/1122) feat(auth): admin PIN-visibility UI — status, not the PIN itself |
| 2026-07-30 | eq-shell | [#1121](https://github.com/eq-solutions/eq-shell/pull/1121) fix(audit): stop logging no-op UPDATEs polluting the Activity log |
| 2026-07-30 | eq-shell | [#1119](https://github.com/eq-solutions/eq-shell/pull/1119) feat(auth): SIM-swap PIN invalidation — admin phone-number change |
| 2026-07-30 | eq-shell | [#1120](https://github.com/eq-solutions/eq-shell/pull/1120) fix(suppliers): free scroll + column toggle; drop BETA from Cards |
| 2026-07-30 | eq-shell | [#1117](https://github.com/eq-solutions/eq-shell/pull/1117) fix(briefing): exclude archived staff from the AI dashboard summa |
| 2026-07-30 | eq-shell | [#1118](https://github.com/eq-solutions/eq-shell/pull/1118) fix(staff): lock email/phone provenance so Cards can update a non |
| 2026-07-30 | eq-shell | [#1113](https://github.com/eq-solutions/eq-shell/pull/1113) chore(intake): re-vendor eq-intake/eq-platform — customers/contac |
| 2026-07-30 | eq-shell | [#1116](https://github.com/eq-solutions/eq-shell/pull/1116) feat(workers): compliance-roster-only workers — has_field_access  |
_Showing 15 of 120 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **`eq` tenant's Leave feature is broken (401)** — the demo tenant can't read its own leave requests (anon lacks a DB grant on zaap); spotted while smoke-testing this unrelated work, spun off as its own background task, not yet resolved. _(added 2026-07-30)_
- **`EQ_SECRET_SALT` rotation still outstanding** — the value was exposed in chat back in April; nothing has forced a rotation since. _(added 2026-07-30)_
- **Not yet visible on core.eq.solutions** — this app is copied into the main Shell app in a separate step (same pattern as recent settings-screen work). A follow-up task had paused itself waiting on the merge above; unblocked and told to proceed once it landed. _(added 2026-07-30)_
- **Zemi Asri's email in core is still the old value** (`zemi.asri@sks.com.au`) — the fix stops this happening to the next worker, it doesn't correct his row. Either have him re-enter his email in Cards now (will take, unlocked), or edit it directly on his Shell Staff page. _(added 2026-07-30)_
- No edit screen yet for switching an *existing* worker's Field access on/off after the fact — today it's invite-time only. _(added 2026-07-30)_
- **The ACB Test Report has been verified correct by code symmetry with the NSX path, not against a real ACB check** — there are currently zero completed ACB checks in the live database to test against. Worth a quick look the first time SKS actually completes one. _(added 2026-07-29)_
- **First real "August PM"-style import: the "BTCHGR" job plan code on Royce's file doesn't match any existing SKS job plan exactly** (closest is "24VBTCHGR") — the import wizard's existing fuzzy-match step will prompt to confirm or nominate a plan the first time this file type is actually committed. Not a bug, just a heads-up for whoever runs the first real import. _(added 2026-07-29)_
- **ACB/NSX breaker-card run-sheets and RCD test run-sheets don't show the Job Code** — Royce chose to scope this session to the standard maintenance checklist only; same gap exists in those report variants if wanted later. _(added 2026-07-29)_
- **Two other report types have the same missing-Job-Code gap**: the PM asset report and the work-order-details report already fetch/track job plan info per asset but only surface the plan *name*, never the *code*. Not touched this session — out of scope. _(added 2026-07-29)_
- **Bring Data In's "Check for conflicts" still commits on its own path, separate from the main Into-EQ flow** — routing those resolved rows into the same shared commit path as everything else is real, separate work, not done here. _(added 2026-07-29)_
_…and 345 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Build the fix**: `openPinManagement()` does a narrow on-demand `people?select=id,pin&group=in.(Apprentice,Labour Hire)` fetch (same pattern as the staff-timesheet PIN gate in `auth.js`), caches it, `renderPinList()` reads from that cache instead of `p.pin`. Keeps raw PINs out of the general bulk load. Branch fresh off `origin/main`, not the stale `claude/loadfromsupabase-resilient-sync` branch. _(added 2026-07-30)_
- **Separate, lower-priority**: the DB's `has_pin` boolean column is stale/unmaintained (verified live 2026-07-30: 32 of 35 people with a set PIN had `has_pin=false`) — would need an INSERT/UPDATE trigger to sync before it's trustworthy. Not needed for the fix above (on-demand fetch sidesteps it), but worth fixing separately if `has_pin` is ever relied on elsewhere. _(added 2026-07-30)_
- Mirror the roster-grid archive + rating feature (SKS v3.10.104/.105) in EQ Field — flagged as a follow-up task; Royce started it in a separate session, result not yet known. _(added 2026-07-28)_
- **Actual weekly entry hasn't started yet** — the log is ready, first week isn't logged. Per the plan's own proving discipline, needs at least one real supervisor entering their own crew's data (not just one person doing it centrally) to actually test the load the new app has to carry. _(added 2026-07-26)_
- **Needs a real-world check**: have a labour-hire worker (or someone who can log in as one) open the Plant & Equipment list on core.eq.solutions and confirm it loads. Confirmed as far as possible from the data side (production is serving the right code, no other access rule is in the way) but nobody has actually clicked through as that kind of user yet. _(added 2026-07-26)_
- **Needs a real-world check**: have a manager get one affected worker (Zemi Asri, approved 2026-06-25) to retry logging into core.eq.solutions and confirm it now works. _(added 2026-07-26)_
- **Still open — who signs off on a rollout this size.** Royce: "no idea about sign-off yet, that will evolve over time." No action needed now, just not resolved. _(added 2026-07-23)_
- **Real risk named, not resolved: the "prove in NSW" plan proves at ~300, but the very next expansion (VIC) is already ~700-1,000** — a materially bigger jump than what NSW will have proven. Worth deciding whether VIC gets its own smaller proof step before full rollout. _(added 2026-07-23)_
- **The 3 already-stuck Cameron Tregoning requests still need manual action** — this fix stops it happening again, it doesn't retroactively fix those. Ian needs to go back and finish confirming them (or Royce/a supervisor approves directly in-app). _(added 2026-07-22)_
- **Confirm a non-manager (employee-level) login actually sees a blank instead of real credentials** — only had a manager session available to test with this session. _(added 2026-07-21)_
_…and 61 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise._

| File | Lines | Open | Done (unrotated) | Aging 45d+ |
|------|------:|-----:|------------------:|------------:|
| [EQ](eq/pending.md) | 2892 | 456 | 113 | 9 |
| [SKS](sks/pending.md) | 432 | 78 | 5 | 16 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 433 | 38 | 9 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-30 | [`__personal__` tenant "retired" doc claim corrected against live data](sessions/2026-07-30.md) |
| 2026-07-30 | [guard.js selftest fixed; ~/.claude brought under version control](sessions/2026-07-30-guard-selftest-claude-git.md) |
| 2026-07-29 | [eq-receipts: fixed a duplicate-detection blind spot, added invoice number as a stronger match](sessions/2026-07-29.md) |
| 2026-07-28 | [Roster: archive Labour Hire from the grid with a rehire rating](sessions/2026-07-28.md) |
| 2026-07-27 | [eq-ui design handoff shipped + propagated to eq-shell/eq-service, real bugs found along the way](sessions/2026-07-27.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-30 10:25 UTC._
