---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-23
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-23 01:26 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-23 01:12 UTC → 2026-07-23 01:26 UTC)

- Merged: eq-shell [#952](https://github.com/eq-solutions/eq-shell/pull/952) fix(ci): CHECK 2 anon-grant invariant excludes views — fixes
- Merged: eq-shell [#949](https://github.com/eq-solutions/eq-shell/pull/949) Detect dangling cross-plane workers.staff_id pointers (22 of
- Merged: eq-shell [#945](https://github.com/eq-solutions/eq-shell/pull/945) fix(staff): admin licence PDF upload failed on every PDF in 
- Merged: eq-shell [#944](https://github.com/eq-solutions/eq-shell/pull/944) Account deletion left the Shell identity row behind (6 orpha
- Merged: eq-shell [#941](https://github.com/eq-solutions/eq-shell/pull/941) EQ Ops Setup: add Save all for the preset line-item library
- Merged: eq-shell [#940](https://github.com/eq-solutions/eq-shell/pull/940) chore: retire the certificates-migrate endpoint (Phase C cle
- Merged: eq-shell [#939](https://github.com/eq-solutions/eq-shell/pull/939) docs: correct licence-photos RLS mechanism (segment 2, not s
- Merged: eq-shell [#933](https://github.com/eq-solutions/eq-shell/pull/933) Security: any org invitee could activate as admin (control p

## ⚠ Needs you (6)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-07-21.md](sessions/2026-07-21.md) · [failures.md](system/failures.md)
- 🟠 **Sentry new error** — `eq-solves-service` [UnrecognizedActionError: Server Action "40dbe95a25df946d13db](https://eq-solutions.sentry.io/issues/122209933/)
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
| eq-shell | [EQ Field handoff auto-recovery (rejected)](https://eq-solutions.sentry.io/issues/133584980/) | 6 | 2026-07-19 |
| eq-solves-service | [UnrecognizedActionError: Server Action "40dbe95a25df946d13dbc7a303f98a6b660211ea](https://eq-solutions.sentry.io/issues/122209933/) | 4 | 2026-07-23 |
| eq-shell | [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/) | 3 | 2026-07-22 |
| eq-shell | [Error: staff-licence-ocr: ocr-licence returned 401](https://eq-solutions.sentry.io/issues/135986280/) | 1 | 2026-07-22 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-23 | eq-shell | [#974](https://github.com/eq-solutions/eq-shell/pull/974) fix(staff): compliance pack export stuck re-downloading the first |
| 2026-07-23 | eq-solves-service | [#591](https://github.com/eq-solutions/eq-service/pull/591) fix(testing): ACB/NSX checks use canonical frequency slugs, not l |
| 2026-07-23 | eq-solves-service | [#590](https://github.com/eq-solutions/eq-service/pull/590) fix(assets,maintenance): surface Asset # on the record + fix ID-b |
| 2026-07-22 | eq-shell | [#972](https://github.com/eq-solutions/eq-shell/pull/972) fix(ops): Suppliers column widths + stale cross-tenant JWT cache  |
| 2026-07-22 | eq-shell | [#967](https://github.com/eq-solutions/eq-shell/pull/967) feat(identity-health): detect duplicate Shell accounts across sig |
| 2026-07-22 | eq-shell | [#969](https://github.com/eq-solutions/eq-shell/pull/969) fix(quotes): job-sync calls to canonical-api always 401'd from th |
| 2026-07-22 | eq-shell | [#968](https://github.com/eq-solutions/eq-shell/pull/968) fix(staff): resync from Cards can no longer skip already-synced l |
| 2026-07-22 | eq-shell | [#960](https://github.com/eq-solutions/eq-shell/pull/960) Security: gate Ops-exclusive backend functions on the ops entitle |
| 2026-07-22 | eq-shell | [#957](https://github.com/eq-solutions/eq-shell/pull/957) ci: one-time workflow to apply Sentry alert rules |
| 2026-07-22 | eq-shell | [#959](https://github.com/eq-solutions/eq-shell/pull/959) docs(scripts): record the William Brown identity merge as APPLIED |
| 2026-07-22 | eq-shell | [#958](https://github.com/eq-solutions/eq-shell/pull/958) Security: enforce module entitlement at the iframe-SSO minters |
| 2026-07-22 | eq-shell | [#956](https://github.com/eq-solutions/eq-shell/pull/956) fix(list-members): include phone, mark email/name nullable |
| 2026-07-22 | eq-shell | [#954](https://github.com/eq-solutions/eq-shell/pull/954) docs(scripts): mark the staff-pointer repair as APPLIED |
| 2026-07-22 | eq-shell | [#955](https://github.com/eq-solutions/eq-shell/pull/955) fix(field-iframe): retry the handoff timeout path instead of dead |
| 2026-07-22 | eq-shell | [#953](https://github.com/eq-solutions/eq-shell/pull/953) chore: fold orphan iframe-mint Sentry alert into setup-sentry-ale |
_Showing 15 of 112 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **New: the automatic "read the certificate for me" step failed once on a PDF upload, rejected by the server that does the reading.** Didn't affect the person uploading — it just quietly fell back to typing the details in by hand, same as if no reading happened at all. Only happened once so far. Task chip spawned to check whether the two systems' shared password has gotten out of sync (which would keep failing) or it was a one-off. _(added 2026-07-23)_
- Royce to click through a workspace switch + the Suppliers page once live to confirm the fix. _(added 2026-07-23)_
- **The tripwire fix eq-solves-service got today (see that entry below) hasn't been built for eq-shell, and eq-shell needs it too.** This session's assigned private folder had nothing in it — ended up doing all its real work in the one shared master copy instead, same mechanism as eq-solves-service's bug. Confirmed live mid-session: a second, unrelated concurrent session's own work-in-progress (a database list-loading improvement) was sitting there uncommitted where this session could see it, and that session's own folder-switch changed what this session was pointed at partway through, without warning. Nothing was lost either time — caught before anything got mixed up — but it's luck, not a safeguard. _(added 2026-07-23)_
- **Separately: PR #973 (the other session's database list-loading work, opened while this session was mid-review) got a partial review before that session took over — worth a second look before merge.** The new database logic correctly matches the existing rules, no issues there. One real thing: the "Overdue follow-up" filter button will start showing fewer results than before once this ships (it'll now match the same, stricter rule the on-screen count already uses) — arguably a fix, not a bug, but nobody explicitly decided it should change. Not urgent, just flag it before merge. _(added 2026-07-23)_
- Email-in capture and the Phase 3 gate remain open — see the 2026-07-22 entry below, unchanged.
- **The mojibake asset-name corruption (47 rows across 3 sites, stray "Â" characters from an old import) still isn't fixed.** Tried the one-line SQL fix twice, including once on your direct "go run it now" — both times it silently didn't take, a known non-deterministic quirk of the DB tool blocking certain live writes without erroring. Cosmetic only (the corrupted name still displays, nothing else is affected). **Needs you to run this once in the Supabase SQL editor on ehow:** `UPDATE app_data.assets SET name = replace(name, 'Â ', ' ') WHERE name ~ 'Â';` _(added 2026-07-23)_
- **Email-in capture still needs Royce to finish 2 things** in his own Resend and Supabase logins before it actually turns on (add a receiving domain, create a webhook, add 4 secret values) — code side is done and waiting. _(added 2026-07-22)_
- **Phase 3 gate still open** — clearing one real week of receipts end-to-end in under 10 minutes, to prove the whole thing actually works day-to-day. Only Royce can run this one. _(added 2026-07-22, carried over from earlier)_
- **CONFIRMED REAL, re-checked same day — the 2 remaining warnings genuinely can't be fixed right now, not even by choosing to accept a breaking change.** Re-queried the package registry directly today: the newest available release of both the framework and the spreadsheet library still carry the vulnerable piece — nothing shipped upstream since yesterday. True accepted risk, not a "we just haven't gotten to it" item. Nothing to do until the two library authors update their own dependency; re-check next time either one releases. _(confirmed 2026-07-23)_
- **CONFIRMED REAL, still actively happening — eq-solves-service's checkout is shared with other concurrent sessions, same as eq-shell.** Caught it live again while re-checking the item above: the checkout had switched to a 4th different branch with 6 more uncommitted files from a session that turned out to be doing its own separate multi-PR work (Asset # display fixes, a duplicate-account cleanup, a new feature) — not a one-off glitch, a structural fact about how this environment runs sessions. 4 occurrences across 2 days now. Real fix, not another workaround note: eq-shell already solves this with a registered-worktree convention (`eq-context/system/worktree-registry.md`) — eq-solves-service has no equivalent, so sessions default to the shared root instead of an isolated worktree. Worth setting up the same registry entry/convention for this repo. _(confirmed 2026-07-23)_
_…and 425 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 3328 | 439 | 586 |
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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-23 01:26 UTC._
