---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-23
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-23 05:29 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-23 03:24 UTC → 2026-07-23 05:29 UTC)

- Merged: eq-shell [#958](https://github.com/eq-solutions/eq-shell/pull/958) Security: enforce module entitlement at the iframe-SSO minte
- Merged: eq-shell [#957](https://github.com/eq-solutions/eq-shell/pull/957) ci: one-time workflow to apply Sentry alert rules
- Merged: eq-shell [#955](https://github.com/eq-solutions/eq-shell/pull/955) fix(field-iframe): retry the handoff timeout path instead of
- Merged: eq-shell [#951](https://github.com/eq-solutions/eq-shell/pull/951) fix(cards): Cards-approved staff got a Shell membership born
- Merged: eq-shell [#950](https://github.com/eq-solutions/eq-shell/pull/950) fix(ci): allowlist app_data.field_team_supervisors (safe inv
- Merged: eq-shell [#948](https://github.com/eq-solutions/eq-shell/pull/948) Retire backfill-auth-users.ts — dead code, only live target 
- Merged: eq-shell [#947](https://github.com/eq-solutions/eq-shell/pull/947) fix(ui): attachment spinners referenced an undefined spin ke
- Merged: eq-shell [#943](https://github.com/eq-solutions/eq-shell/pull/943) chore: remove dead mint-cards-iframe-token.ts

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
| eq-shell | ? unknown | ? | 4 | 0d |
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
| 2026-07-23 | eq-shell | [#974](https://github.com/eq-solutions/eq-shell/pull/974) fix(staff): compliance pack export stuck re-downloading the first |
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
| 2026-07-22 | eq-shell | [#967](https://github.com/eq-solutions/eq-shell/pull/967) feat(identity-health): detect duplicate Shell accounts across sig |
| 2026-07-22 | eq-shell | [#969](https://github.com/eq-solutions/eq-shell/pull/969) fix(quotes): job-sync calls to canonical-api always 401'd from th |
| 2026-07-22 | eq-shell | [#968](https://github.com/eq-solutions/eq-shell/pull/968) fix(staff): resync from Cards can no longer skip already-synced l |
_Showing 15 of 114 · full record in [sessions/](sessions/)_

## Pending (EQ)

- None of this session's UI changes (the check page's Site fix/inline editors, the Kanban card titles) were eyeballed live in a real browser — verification was code-level (type-checking + full build) only, since these pages sit behind Royce's own login. Worth a quick click-through next time he's in the app. _(added 2026-07-23)_
- **2 of the leftover folders from the cleanup above are still stuck** — something else on this machine currently has them open, so they couldn't be deleted this session. Safe to remove once whatever's using them finishes; matches the same known bug pattern, not a new issue. _(added 2026-07-23)_
- **New: the automatic "read the certificate for me" step failed once on a PDF upload, rejected by the server that does the reading.** Didn't affect the person uploading — it just quietly fell back to typing the details in by hand, same as if no reading happened at all. Only happened once so far. Task chip spawned to check whether the two systems' shared password has gotten out of sync (which would keep failing) or it was a one-off. _(added 2026-07-23)_
- Royce to click through a workspace switch + the Suppliers page once live to confirm the fix. _(added 2026-07-23)_
- **The tripwire fix eq-solves-service got today (see that entry below) hasn't been built for eq-shell, and eq-shell needs it too.** This session's assigned private folder had nothing in it — ended up doing all its real work in the one shared master copy instead, same mechanism as eq-solves-service's bug. Confirmed live mid-session: a second, unrelated concurrent session's own work-in-progress (a database list-loading improvement) was sitting there uncommitted where this session could see it, and that session's own folder-switch changed what this session was pointed at partway through, without warning. Nothing was lost either time — caught before anything got mixed up — but it's luck, not a safeguard. _(added 2026-07-23)_
- **Separately: PR #973 (the other session's database list-loading work, opened while this session was mid-review) got a partial review before that session took over — worth a second look before merge.** The new database logic correctly matches the existing rules, no issues there. One real thing: the "Overdue follow-up" filter button will start showing fewer results than before once this ships (it'll now match the same, stricter rule the on-screen count already uses) — arguably a fix, not a bug, but nobody explicitly decided it should change. Not urgent, just flag it before merge. _(added 2026-07-23)_
- Email-in capture and the Phase 3 gate remain open — see the 2026-07-22 entry below, unchanged.
- **The mojibake asset-name corruption (47 rows across 3 sites, stray "Â" characters from an old import) still isn't fixed.** Tried the one-line SQL fix twice, including once on your direct "go run it now" — both times it silently didn't take, a known non-deterministic quirk of the DB tool blocking certain live writes without erroring. Cosmetic only (the corrupted name still displays, nothing else is affected). **Needs you to run this once in the Supabase SQL editor on ehow:** `UPDATE app_data.assets SET name = replace(name, 'Â ', ' ') WHERE name ~ 'Â';` _(added 2026-07-23)_
- **Email-in capture still needs Royce to finish 2 things** in his own Resend and Supabase logins before it actually turns on (add a receiving domain, create a webhook, add 4 secret values) — code side is done and waiting. _(added 2026-07-22)_
- **Phase 3 gate still open** — clearing one real week of receipts end-to-end in under 10 minutes, to prove the whole thing actually works day-to-day. Only Royce can run this one. _(added 2026-07-22, carried over from earlier)_
_…and 427 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 3405 | 443 | 617 |
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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-23 05:29 UTC._
