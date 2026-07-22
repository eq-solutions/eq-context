---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-22
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-22 11:59 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-22 11:46 UTC → 2026-07-22 11:59 UTC)

- Merged: eq-shell [#944](https://github.com/eq-solutions/eq-shell/pull/944) Account deletion left the Shell identity row behind (6 orpha
- Merged: eq-shell [#941](https://github.com/eq-solutions/eq-shell/pull/941) EQ Ops Setup: add Save all for the preset line-item library
- Merged: eq-shell [#940](https://github.com/eq-solutions/eq-shell/pull/940) chore: retire the certificates-migrate endpoint (Phase C cle
- Merged: eq-shell [#939](https://github.com/eq-solutions/eq-shell/pull/939) docs: correct licence-photos RLS mechanism (segment 2, not s
- Merged: eq-shell [#938](https://github.com/eq-solutions/eq-shell/pull/938) Suppliers: role-gate login/password behind manager/superviso
- Merged: eq-shell [#933](https://github.com/eq-solutions/eq-shell/pull/933) Security: any org invitee could activate as admin (control p
- Merged: eq-shell [#931](https://github.com/eq-solutions/eq-shell/pull/931) Suppliers.tsx: add per-column filters to the desktop table
- Merged: eq-shell [#928](https://github.com/eq-solutions/eq-shell/pull/928) EQ Ops: unblock Setup, restore labour cost, column filters, 

## ⚠ Needs you (5)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-07-21.md](sessions/2026-07-21.md) · [failures.md](system/failures.md)
- 🟠 **Sentry new error** — `eq-shell` [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 1 | 0d |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 1d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [EQ Field handoff auto-recovery (rejected)](https://eq-solutions.sentry.io/issues/133584980/) | 6 | 2026-07-19 |
| eq-shell | [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/) | 2 | 2026-07-22 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-22 | eq-shell | [#960](https://github.com/eq-solutions/eq-shell/pull/960) Security: gate Ops-exclusive backend functions on the ops entitle |
| 2026-07-22 | eq-shell | [#957](https://github.com/eq-solutions/eq-shell/pull/957) ci: one-time workflow to apply Sentry alert rules |
| 2026-07-22 | eq-shell | [#959](https://github.com/eq-solutions/eq-shell/pull/959) docs(scripts): record the William Brown identity merge as APPLIED |
| 2026-07-22 | eq-shell | [#958](https://github.com/eq-solutions/eq-shell/pull/958) Security: enforce module entitlement at the iframe-SSO minters |
| 2026-07-22 | eq-shell | [#956](https://github.com/eq-solutions/eq-shell/pull/956) fix(list-members): include phone, mark email/name nullable |
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
_Showing 15 of 111 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **One triage sub-agent overstepped its brief** — told to investigate only, it instead made a real (but unpushed, harmless) local commit on a shared eq-service checkout. Caught it, verified the fix was actually correct, and folded it into the proper PR instead of using it directly. Worth remembering for future parallel-agent triage: general-purpose agents have full write tools even when told not to use them — an isolated/read-only agent type would remove the risk entirely. _(added 2026-07-22)_
- **7 workers' names need your eye — I deliberately didn't guess.** Their surname is currently stored as more than one word, and there is genuinely no way to tell from the data whether that's wrong or right: "Marcus De La Fuente" and "Cicero Goncalves Da Silva Junior" are real surnames, while "Damon Patrick Francis" looks like a middle name that got absorbed, and "Jose Luis Quintanilla Rodriguez" has the opposite problem — his *first* name is "Jose Luis" and the system only kept "Jose". Nothing recorded what the names looked like beforehand, so any automatic rule I applied would fix one group by breaking the other. The list is written up ready for you; it only needs someone who knows these people. Nothing is broken while it waits — the underlying fault is fixed, so these names will now stay exactly as they are. _(added 2026-07-22)_
- **A version-numbering collision happened again mid-session — 4th time this has come up.** Two of these narrow, independent EQ Field changes get worked on in parallel worktrees and both grab the "next" version number before either merges; whoever merges second has to notice, rebase, and renumber. Caught and handled cleanly every time so far, no lost work, but worth a look if it keeps recurring — a small script/lock to hand out the next version number would remove the manual "check right before merging" step. _(added 2026-07-22)_
- **Clicked through Forecast and Calendar directly on the live site — clean both times, but on the sandbox tenant, not yours.** No errors, both rendered properly. The gap: the sandbox tenant already has everything loaded in memory, so it never exercises the actual "fetch more when you need it" code this change added — the one thing that would need your own real session to properly prove out. Asked what you actually saw go wrong on screen (blank page, stuck spinner, wrong numbers) since nothing in the log pointed at a cause — still waiting to hear back. _(added 2026-07-22)_
- **Cloudflare account has no 2FA.** `royce@eq.solutions` is the sole Super Administrator over DNS for the entire suite, and account access alone was the only thing separating the whole suite from an outage like this. Worth turning on next time you're in the Cloudflare dashboard. _(added 2026-07-22)_
- **DMARC record for `eq.solutions` was never added** — Resend's auto-configure only pushed MX/SPF/DKIM and marked those optional; verification succeeded without it. Not required, but a `p=none` starter record would give visibility into anyone spoofing `@eq.solutions`, if that's ever worth doing. _(added 2026-07-22)_
- **GitHub's automated test-and-lint check never ran on this PR** — only the Netlify build check fired; the actual test suite was run by hand instead and came back clean, but the automatic safety net didn't fire and the cause wasn't tracked down. Worth a look if it happens again on the next PR. _(added 2026-07-22)_
- **No hands-on test of the finished feature yet** — signing a report, attaching a photo, downloading the Word doc, and the manager email actually arriving haven't been clicked through live, only checked via the automated tests and a read-through of the working page. Worth Royce (or someone on a phone/tablet on site) trying it for real. _(added 2026-07-22)_
- **Field still writes to the SKS database through its own door, outside the governed pipeline.** Two of today's changes went in by hand because Field has no approval pipeline of its own, following existing precedent. That's the same pattern named elsewhere as the cause of an earlier drift incident. Now that the governed pipeline has been seen working cleanly several times today, Field's database changes should move into it — otherwise there are permanently two ways in, one of them unaudited. _(added 2026-07-21)_
- **The timesheet and leave approval rules have never been exercised by a real person.** The logic went live without ever having been run — there's no safe place to rehearse it. Worth putting one real timesheet and one real leave request through the full path (submit → approve → try to approve your own → try to reopen) next time you're in Field, to confirm the blocks and the wording behave as intended. _(added 2026-07-21)_
_…and 410 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 3221 | 424 | 544 |
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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-22 11:59 UTC._
