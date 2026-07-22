---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-22
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-22 10:36 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-22 10:32 UTC → 2026-07-22 10:36 UTC)

- Merged: eq-shell [#954](https://github.com/eq-solutions/eq-shell/pull/954) docs(scripts): mark the staff-pointer repair as APPLIED
- Merged: eq-shell [#941](https://github.com/eq-solutions/eq-shell/pull/941) EQ Ops Setup: add Save all for the preset line-item library
- Merged: eq-shell [#940](https://github.com/eq-solutions/eq-shell/pull/940) chore: retire the certificates-migrate endpoint (Phase C cle
- Merged: eq-shell [#939](https://github.com/eq-solutions/eq-shell/pull/939) docs: correct licence-photos RLS mechanism (segment 2, not s
- Merged: eq-shell [#938](https://github.com/eq-solutions/eq-shell/pull/938) Suppliers: role-gate login/password behind manager/superviso
- Merged: eq-shell [#933](https://github.com/eq-solutions/eq-shell/pull/933) Security: any org invitee could activate as admin (control p
- Merged: eq-shell [#932](https://github.com/eq-solutions/eq-shell/pull/932) Extend identity-collision gate to the invite-path approval
- Merged: eq-shell [#931](https://github.com/eq-solutions/eq-shell/pull/931) Suppliers.tsx: add per-column filters to the desktop table

## ⚠ Needs you (6)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-07-21.md](sessions/2026-07-21.md) · [failures.md](system/failures.md)
- 🟠 **Sentry new error** — `eq-shell` [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/)
- 🟠 **Sentry new error** — `eq-solves-service` [TypeError: Cannot read properties of null (reading 'localeCo](https://eq-solutions.sentry.io/issues/135850902/)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 1d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [EQ Field handoff auto-recovery (rejected)](https://eq-solutions.sentry.io/issues/133584980/) | 6 | 2026-07-19 |
| eq-shell | [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/) | 2 | 2026-07-22 |
| eq-solves-service | [TypeError: Cannot read properties of null (reading 'localeCompare')](https://eq-solutions.sentry.io/issues/135850902/) | 1 | 2026-07-22 |
| eq-shell | [EQ Field handoff timeout — no postMessage in 30s](https://eq-solutions.sentry.io/issues/129554465/) | 1 | 2026-07-19 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-22 | eq-shell | [#954](https://github.com/eq-solutions/eq-shell/pull/954) docs(scripts): mark the staff-pointer repair as APPLIED |
| 2026-07-22 | eq-shell | [#955](https://github.com/eq-solutions/eq-shell/pull/955) fix(field-iframe): retry the handoff timeout path instead of dead |
| 2026-07-22 | eq-shell | [#953](https://github.com/eq-solutions/eq-shell/pull/953) chore: fold orphan iframe-mint Sentry alert into setup-sentry-ale |
| 2026-07-22 | eq-shell | [#951](https://github.com/eq-solutions/eq-shell/pull/951) fix(cards): Cards-approved staff got a Shell membership born inac |
| 2026-07-22 | eq-shell | [#952](https://github.com/eq-solutions/eq-shell/pull/952) fix(ci): CHECK 2 anon-grant invariant excludes views — fixes the  |
| 2026-07-22 | eq-shell | [#949](https://github.com/eq-solutions/eq-shell/pull/949) Detect dangling cross-plane workers.staff_id pointers (22 of 93 l |
| 2026-07-22 | eq-shell | [#950](https://github.com/eq-solutions/eq-shell/pull/950) fix(ci): allowlist app_data.field_team_supervisors (safe invoker  |
| 2026-07-22 | eq-shell | [#947](https://github.com/eq-solutions/eq-shell/pull/947) fix(ui): attachment spinners referenced an undefined spin keyfram |
| 2026-07-22 | eq-shell | [#948](https://github.com/eq-solutions/eq-shell/pull/948) Retire backfill-auth-users.ts — dead code, only live target was d |
| 2026-07-22 | eq-shell | [#945](https://github.com/eq-solutions/eq-shell/pull/945) fix(staff): admin licence PDF upload failed on every PDF in produ |
| 2026-07-22 | eq-shell | [#944](https://github.com/eq-solutions/eq-shell/pull/944) Account deletion left the Shell identity row behind (6 orphans on |
| 2026-07-22 | eq-solves-service | [#580](https://github.com/eq-solutions/eq-service/pull/580) fix(sort): guard localeCompare against null name+email |
| 2026-07-22 | eq-field | [#537](https://github.com/eq-solutions/eq-field/pull/537) feat: Incidents / Near Miss reporting (v3.5.355) |
| 2026-07-22 | eq-field | [#536](https://github.com/eq-solutions/eq-field/pull/536) Security: same tenant-isolation gap in teams + team_members |
| 2026-07-22 | eq-field | [#535](https://github.com/eq-solutions/eq-field/pull/535) v3.5.355 — boot week-window ±4 → ±1, the actual scale lever |
_Showing 15 of 107 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **A version-numbering collision happened again mid-session — 4th time this has come up.** Two of these narrow, independent EQ Field changes get worked on in parallel worktrees and both grab the "next" version number before either merges; whoever merges second has to notice, rebase, and renumber. Caught and handled cleanly every time so far, no lost work, but worth a look if it keeps recurring — a small script/lock to hand out the next version number would remove the manual "check right before merging" step. _(added 2026-07-22)_
- **Couldn't get a real click-through on this one either** — same browser-tool issue as the crew-toggle entry above (screenshots timed out, clicks weren't registering), unrelated to the code. Verified instead via the automated test suite, the build, and reading the deployed files directly. Worth a real look at Forecast and Calendar next time you're in Field, since those two screens changed the most structurally. _(added 2026-07-22)_
- **Cloudflare account has no 2FA.** `royce@eq.solutions` is the sole Super Administrator over DNS for the entire suite, and account access alone was the only thing separating the whole suite from an outage like this. Worth turning on next time you're in the Cloudflare dashboard. _(added 2026-07-22)_
- **DMARC record for `eq.solutions` was never added** — Resend's auto-configure only pushed MX/SPF/DKIM and marked those optional; verification succeeded without it. Not required, but a `p=none` starter record would give visibility into anyone spoofing `@eq.solutions`, if that's ever worth doing. _(added 2026-07-22)_
- **Build kicked off as its own chip session** (`task_bac795b3`), running independently in its own eq-field worktree — briefed to verify eq-field's actual current Safety/prestart architecture live before building (it's drifted from SKS's — prestart moved to a different file there recently), reuse eq-field's own existing docx/signature/offline-queue mechanisms rather than importing SKS's, and get Royce's go before any live migration or push. _(added 2026-07-22)_
- **Field still writes to the SKS database through its own door, outside the governed pipeline.** Two of today's changes went in by hand because Field has no approval pipeline of its own, following existing precedent. That's the same pattern named elsewhere as the cause of an earlier drift incident. Now that the governed pipeline has been seen working cleanly several times today, Field's database changes should move into it — otherwise there are permanently two ways in, one of them unaudited. _(added 2026-07-21)_
- **The timesheet and leave approval rules have never been exercised by a real person.** The logic went live without ever having been run — there's no safe place to rehearse it. Worth putting one real timesheet and one real leave request through the full path (submit → approve → try to approve your own → try to reopen) next time you're in Field, to confirm the blocks and the wording behave as intended. _(added 2026-07-21)_
- **Six leftover records still need clearing — needs your hand.** A prepared script is sitting in the repo (`scripts/cleanup-orphaned-shell-users.sql`). It snapshots first, re-checks six safety conditions before touching anything, and won't save changes unless you confirm the numbers look right. It can't be automated — that database has no automatic update path. Nobody is affected in the meantime; none of these accounts can be signed into. _(added 2026-07-22)_
- **The old admin button should be guarded or retired.** It still exists and would still do the wrong thing if pointed at records like these. Its original job was finished off by fixes that went live a week ago, so it may simply be dead. Separate task, chip raised. _(added 2026-07-22)_
- **One thing not checked: a real click-through with a live login.** The sandbox this was built in has no working sign-in to the real system, so the code was verified by reading + a syntax/lint pass + a no-login load test, not by actually opening a prestart and clicking the button. Worth a real click-through next time you're in the app at a site with prior prestart history. _(added 2026-07-22)_
_…and 407 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 3179 | 420 | 517 |
| [SKS](sks/pending.md) | 495 | 72 | 79 |
| [SKS active](sks/active.md) | 108 | 0 | 0 |
| [OPS](ops/pending.md) | 252 | 30 | 6 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-22 | [SKS Safety: Incidents/Near Miss tab + Prestart copy-from-last, EQ Field regression found & fixed](sessions/2026-07-22.md) |
| 2026-07-21 | [eq-shell had its own copy of the licence-privacy gap; found, fixed, deployed, and smoke-tested](sessions/2026-07-21.md) |
| 2026-07-20 | [invite-accept duplicate-identity follow-up: root cause disproven, hardening shipped + deployed, then a real lead found via Sentry](sessions/2026-07-20.md) |
| 2026-07-19 | [Digest sweep: two Sentry issues root-caused, one real fix shipped + verified live](sessions/2026-07-19.md) |
| 2026-07-17 | [AI brief's quote signals were silently zero for SKS; realigned to the live enum, guarded, shipped live](sessions/2026-07-17.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-22 10:36 UTC._
