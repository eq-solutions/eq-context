---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-23
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-23 06:25 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-23 06:24 UTC → 2026-07-23 06:25 UTC)

- Merged: eq-shell [#976](https://github.com/eq-solutions/eq-shell/pull/976) fix(quotes): simplify EQ Ops quote panel actions + status fi
- Merged: eq-shell [#969](https://github.com/eq-solutions/eq-shell/pull/969) fix(quotes): job-sync calls to canonical-api always 401'd fr
- Merged: eq-shell [#960](https://github.com/eq-solutions/eq-shell/pull/960) Security: gate Ops-exclusive backend functions on the ops en
- Merged: eq-shell [#959](https://github.com/eq-solutions/eq-shell/pull/959) docs(scripts): record the William Brown identity merge as AP
- Merged: eq-shell [#956](https://github.com/eq-solutions/eq-shell/pull/956) fix(list-members): include phone, mark email/name nullable
- Merged: eq-shell [#954](https://github.com/eq-solutions/eq-shell/pull/954) docs(scripts): mark the staff-pointer repair as APPLIED
- Merged: eq-shell [#953](https://github.com/eq-solutions/eq-shell/pull/953) chore: fold orphan iframe-mint Sentry alert into setup-sentr
- Merged: eq-shell [#952](https://github.com/eq-solutions/eq-shell/pull/952) fix(ci): CHECK 2 anon-grant invariant excludes views — fixes

## ⚠ Needs you (6)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-07-21.md](sessions/2026-07-21.md) · [failures.md](system/failures.md)
- 🟠 **Sentry new error** — `eq-solves-service` [UnrecognizedActionError: Server Action "4073d2dc7728208efb4f](https://eq-solutions.sentry.io/issues/122209933/)
- 🟠 **Sentry new error** — `eq-shell` [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 3 | 0d |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 1d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-solves-service | [UnrecognizedActionError: Server Action "4073d2dc7728208efb4febe859b7cd09e6dabc19](https://eq-solutions.sentry.io/issues/122209933/) | 9 | 2026-07-23 |
| eq-shell | [EQ Field handoff auto-recovery (rejected)](https://eq-solutions.sentry.io/issues/133584980/) | 6 | 2026-07-19 |
| eq-shell | [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/) | 3 | 2026-07-22 |
| eq-shell | [Error: staff-licence-ocr: ocr-licence returned 401](https://eq-solutions.sentry.io/issues/135986280/) | 1 | 2026-07-22 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-23 | eq-shell | [#976](https://github.com/eq-solutions/eq-shell/pull/976) fix(quotes): simplify EQ Ops quote panel actions + status filter, |
| 2026-07-23 | eq-shell | [#975](https://github.com/eq-solutions/eq-shell/pull/975) fix(identity): list-members backfills name/email from app_data.st |
| 2026-07-23 | eq-shell | [#974](https://github.com/eq-solutions/eq-shell/pull/974) fix(staff): compliance pack export stuck re-downloading the first |
| 2026-07-23 | eq-solves-service | [#598](https://github.com/eq-solutions/eq-service/pull/598) fix(admin/users): add missing subcontractor entry to role label m |
| 2026-07-23 | eq-solves-service | [#597](https://github.com/eq-solutions/eq-service/pull/597) feat(maintenance): make Site and the check name editable on the c |
| 2026-07-23 | eq-solves-service | [#596](https://github.com/eq-solutions/eq-service/pull/596) fix(errors): gracefully recover from stale server-action IDs post |
| 2026-07-23 | eq-solves-service | [#595](https://github.com/eq-solutions/eq-service/pull/595) fix(maintenance): show check title on Kanban cycle cards |
| 2026-07-23 | eq-solves-service | [#594](https://github.com/eq-solutions/eq-service/pull/594) fix(reports): render tenant logo on Compliance Report |
| 2026-07-23 | eq-solves-service | [#593](https://github.com/eq-solutions/eq-service/pull/593) fix(bulk-actions): chunk bulk delete/deactivate to dodge Postgres |
| 2026-07-23 | eq-solves-service | [#592](https://github.com/eq-solutions/eq-service/pull/592) fix(maintenance,reports): surface site on check detail, editable  |
| 2026-07-23 | eq-solves-service | [#591](https://github.com/eq-solutions/eq-service/pull/591) fix(testing): ACB/NSX checks use canonical frequency slugs, not l |
| 2026-07-23 | eq-solves-service | [#590](https://github.com/eq-solutions/eq-service/pull/590) fix(assets,maintenance): surface Asset # on the record + fix ID-b |
| 2026-07-23 | eq-cards | [#175](https://github.com/eq-solutions/eq-cards/pull/175) feat(admin-attach-licence-photo): support attaching a PDF, not ju |
| 2026-07-23 | eq-cards | [#174](https://github.com/eq-solutions/eq-cards/pull/174) fix(ocr-licence): recognise eq-shell's service-role server-to-ser |
| 2026-07-22 | eq-shell | [#972](https://github.com/eq-solutions/eq-shell/pull/972) fix(ops): Suppliers column widths + stale cross-tenant JWT cache  |
_Showing 15 of 114 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **A wrong first theory got spun off as its own task before it was disproven** — an early chip pointed at the wrong screen entirely (a different, internal eq-shell user list), and that chip was already started as its own session before the live-database check ruled it out. That session was never tracked down to stop it — it may still be running against a bug that doesn't actually exist. Worth a look for a stray, pointless eq-shell PR later and closing it out if one shows up. _(added 2026-07-23)_
- **A completely unrelated, real in-progress session got stopped by accident** while chasing the item above (mistaken identity, caught and corrected same session) — the EQ Ops quotes-screen cleanup (removing old Win/Lost buttons, tidying the status filter, sticky totals on the quote form). Nothing was lost — the changes are sitting safely un-saved in their own folder — but it needs manually reopening from the Archived sessions list to pick back up. _(added 2026-07-23)_
- None of this session's UI changes (the check page's Site fix/inline editors, the Kanban card titles) were eyeballed live in a real browser — verification was code-level (type-checking + full build) only, since these pages sit behind Royce's own login. Worth a quick click-through next time he's in the app. _(added 2026-07-23)_
- **2 of the leftover folders from the cleanup above are still stuck** — something else on this machine currently has them open, so they couldn't be deleted this session. Safe to remove once whatever's using them finishes; matches the same known bug pattern, not a new issue. _(added 2026-07-23)_
- **New: the automatic "read the certificate for me" step failed once on a PDF upload, rejected by the server that does the reading.** Didn't affect the person uploading — it just quietly fell back to typing the details in by hand, same as if no reading happened at all. Only happened once so far. Task chip spawned to check whether the two systems' shared password has gotten out of sync (which would keep failing) or it was a one-off. _(added 2026-07-23)_
- Royce to click through a workspace switch + the Suppliers page once live to confirm the fix. _(added 2026-07-23)_
- **The tripwire fix eq-solves-service got today (see that entry below) hasn't been built for eq-shell, and eq-shell needs it too.** This session's assigned private folder had nothing in it — ended up doing all its real work in the one shared master copy instead, same mechanism as eq-solves-service's bug. Confirmed live mid-session: a second, unrelated concurrent session's own work-in-progress (a database list-loading improvement) was sitting there uncommitted where this session could see it, and that session's own folder-switch changed what this session was pointed at partway through, without warning. Nothing was lost either time — caught before anything got mixed up — but it's luck, not a safeguard. _(added 2026-07-23)_
- **Separately: PR #973 (the other session's database list-loading work, opened while this session was mid-review) got a partial review before that session took over — worth a second look before merge.** The new database logic correctly matches the existing rules, no issues there. One real thing: the "Overdue follow-up" filter button will start showing fewer results than before once this ships (it'll now match the same, stricter rule the on-screen count already uses) — arguably a fix, not a bug, but nobody explicitly decided it should change. Not urgent, just flag it before merge. _(added 2026-07-23)_
- Email-in capture and the Phase 3 gate remain open — see the 2026-07-22 entry below, unchanged.
- **The mojibake asset-name corruption (47 rows across 3 sites, stray "Â" characters from an old import) still isn't fixed.** Tried the one-line SQL fix twice, including once on your direct "go run it now" — both times it silently didn't take, a known non-deterministic quirk of the DB tool blocking certain live writes without erroring. Cosmetic only (the corrupted name still displays, nothing else is affected). **Needs you to run this once in the Supabase SQL editor on ehow:** `UPDATE app_data.assets SET name = replace(name, 'Â ', ' ') WHERE name ~ 'Â';` _(added 2026-07-23)_
_…and 429 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **The 3 already-stuck Cameron Tregoning requests still need manual action** — this fix stops it happening again, it doesn't retroactively fix those. Ian needs to go back and finish confirming them (or Royce/a supervisor approves directly in-app). _(added 2026-07-22)_
- **Confirm a non-manager (employee-level) login actually sees a blank instead of real credentials** — only had a manager session available to test with this session. _(added 2026-07-21)_
- **Confirm the mobile card view on a real phone** (tap-to-call, login/password display, reveal toggle) — couldn't force a reliable mobile browser preview in this session's tooling. _(added 2026-07-21)_
- **Password-manager decision still open** — Royce said "not now" to setting up a shared 1Password/Bitwarden vault this session; the in-app login/password fields are the interim answer. Revisit if the list of stored credentials grows. _(added 2026-07-21)_
- **SKS's standalone Field app (sks-nsw-labour) currently lets anyone with the app's public web address read or wipe roster/schedule/timesheet data for all ~50 SKS people — no login required.** A 4-stage fix plan already exists: Stage 1 (the identity layer) is built and sitting in an unmerged pull request, ready to activate; Stage 2 (locks data to the right company) is drafted but not run; Stage 3 (removes the open door) is drafted but has 3 known gaps that need closing first (a few tables would go offline instead of getting properly locked down); Stage 4 (final cleanup) isn't drafted yet. Nothing on SKS's live system was touched — this needs Royce's own hands per stage (setting secrets, running SQL, flipping a switch), plus review of the gaps before Stage 3 is safe. Handed off as its own task rather than half-finishing it inside an unrelated session. _(added 2026-07-20)_
- Royce to click-through confirm a real weekend-rostered person's mobile schedule + home tile on both apps. _(added 2026-07-21)_
- **Still needed: who should receive the weekly NSW Comms summary email?** Built, just needs a recipient list before it's switched on. _(added 2026-07-17)_
- **Not done: live-demo readiness check** (data cleanliness / no visible errors on whatever screen gets shown) — offered, awaiting Royce's go. _(added 2026-07-16)_
- **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date. **PIN audit 2026-07-05 (Royce-confirmed):** this repo has its own independent login/PIN system, still actively used — a completely different codebase from eq-field, not affected by eq-field's own PIN-gate retirement (see `eq/changelog/field.md` "SKS = Core-only auth", v3.5.200).
- **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
_…and 62 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog._

| File | Lines | Open | Done (unrotated) |
|------|------:|-----:|------------------:|
| [EQ](eq/pending.md) | 3415 | 446 | 619 |
| [SKS](sks/pending.md) | 495 | 72 | 79 |
| [SKS active](sks/active.md) | 108 | 0 | 0 |
| [OPS](ops/pending.md) | 252 | 30 | 6 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-23 | [Closed the crm-write/canonical-api entitlement design pass: no gate needed](sessions/2026-07-23.md) |
| 2026-07-22 | [SKS Safety: Incidents/Near Miss tab + Prestart copy-from-last, EQ Field regression found & fixed](sessions/2026-07-22.md) |
| 2026-07-21 | [eq-shell had its own copy of the licence-privacy gap; found, fixed, deployed, and smoke-tested](sessions/2026-07-21.md) |
| 2026-07-20 | [invite-accept duplicate-identity follow-up: root cause disproven, hardening shipped + deployed, then a real lead found via Sentry](sessions/2026-07-20.md) |
| 2026-07-19 | [Digest sweep: two Sentry issues root-caused, one real fix shipped + verified live](sessions/2026-07-19.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-23 06:25 UTC._
