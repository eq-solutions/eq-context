---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-22
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-22 20:09 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-22 19:16 UTC → 2026-07-22 20:09 UTC)

- Merged: eq-shell [#972](https://github.com/eq-solutions/eq-shell/pull/972) fix(ops): Suppliers column widths + stale cross-tenant JWT c
- Merged: eq-shell [#945](https://github.com/eq-solutions/eq-shell/pull/945) fix(staff): admin licence PDF upload failed on every PDF in 
- Merged: eq-shell [#944](https://github.com/eq-solutions/eq-shell/pull/944) Account deletion left the Shell identity row behind (6 orpha
- Merged: eq-shell [#941](https://github.com/eq-solutions/eq-shell/pull/941) EQ Ops Setup: add Save all for the preset line-item library
- Merged: eq-shell [#940](https://github.com/eq-solutions/eq-shell/pull/940) chore: retire the certificates-migrate endpoint (Phase C cle
- Merged: eq-shell [#939](https://github.com/eq-solutions/eq-shell/pull/939) docs: correct licence-photos RLS mechanism (segment 2, not s
- Merged: eq-shell [#938](https://github.com/eq-solutions/eq-shell/pull/938) Suppliers: role-gate login/password behind manager/superviso
- Merged: eq-shell [#933](https://github.com/eq-solutions/eq-shell/pull/933) Security: any org invitee could activate as admin (control p

## ⚠ Needs you (5)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-07-21.md](sessions/2026-07-21.md) · [failures.md](system/failures.md)
- 🟠 **Sentry new error** — `eq-shell` [Error: Workers never invited to join, past grace period: 45](https://eq-solutions.sentry.io/issues/135740258/)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 2 | 0d |
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
| 2026-07-22 | eq-shell | [#951](https://github.com/eq-solutions/eq-shell/pull/951) fix(cards): Cards-approved staff got a Shell membership born inac |
| 2026-07-22 | eq-shell | [#952](https://github.com/eq-solutions/eq-shell/pull/952) fix(ci): CHECK 2 anon-grant invariant excludes views — fixes the  |
| 2026-07-22 | eq-shell | [#949](https://github.com/eq-solutions/eq-shell/pull/949) Detect dangling cross-plane workers.staff_id pointers (22 of 93 l |
_Showing 15 of 111 · full record in [sessions/](sessions/)_

## Pending (EQ)

- Email-in capture and the Phase 3 gate remain open — see the 2026-07-22 entry below, unchanged.
- **The mojibake asset-name corruption (47 rows across 3 sites, stray "Â" characters from an old import) still isn't fixed.** Tried the one-line SQL fix twice, including once on your direct "go run it now" — both times it silently didn't take, a known non-deterministic quirk of the DB tool blocking certain live writes without erroring. Cosmetic only (the corrupted name still displays, nothing else is affected). **Needs you to run this once in the Supabase SQL editor on ehow:** `UPDATE app_data.assets SET name = replace(name, 'Â ', ' ') WHERE name ~ 'Â';` _(added 2026-07-23)_
- **Email-in capture still needs Royce to finish 2 things** in his own Resend and Supabase logins before it actually turns on (add a receiving domain, create a webhook, add 4 secret values) — code side is done and waiting. _(added 2026-07-22)_
- **Phase 3 gate still open** — clearing one real week of receipts end-to-end in under 10 minutes, to prove the whole thing actually works day-to-day. Only Royce can run this one. _(added 2026-07-22, carried over from earlier)_
- **CONFIRMED REAL, re-checked same day — the 2 remaining warnings genuinely can't be fixed right now, not even by choosing to accept a breaking change.** Re-queried the package registry directly today: the newest available release of both the framework and the spreadsheet library still carry the vulnerable piece — nothing shipped upstream since yesterday. True accepted risk, not a "we just haven't gotten to it" item. Nothing to do until the two library authors update their own dependency; re-check next time either one releases. _(confirmed 2026-07-23)_
- **CONFIRMED REAL, still actively happening — eq-solves-service's checkout is shared with other concurrent sessions, same as eq-shell.** Caught it live again while re-checking the item above: the checkout had switched to a 4th different branch with 6 more uncommitted files from a session that turned out to be doing its own separate multi-PR work (Asset # display fixes, a duplicate-account cleanup, a new feature) — not a one-off glitch, a structural fact about how this environment runs sessions. 4 occurrences across 2 days now. Real fix, not another workaround note: eq-shell already solves this with a registered-worktree convention (`eq-context/system/worktree-registry.md`) — eq-solves-service has no equivalent, so sessions default to the shared root instead of an isolated worktree. Worth setting up the same registry entry/convention for this repo. _(confirmed 2026-07-23)_
- **Nobody has re-measured real-world load time since the last speed fix landed.** The write-up now says so plainly — worth a real check next time Service feels slow to load, before assuming there's more to fix. _(added 2026-07-23)_
- **One triage sub-agent overstepped its brief** — told to investigate only, it instead made a real (but unpushed, harmless) local commit on a shared eq-service checkout. Caught it, verified the fix was actually correct, and folded it into the proper PR instead of using it directly. Worth remembering for future parallel-agent triage: general-purpose agents have full write tools even when told not to use them — an isolated/read-only agent type would remove the risk entirely. _(added 2026-07-22)_
- **A version-numbering collision happened again mid-session — 4th time this has come up.** Two of these narrow, independent EQ Field changes get worked on in parallel worktrees and both grab the "next" version number before either merges; whoever merges second has to notice, rebase, and renumber. Caught and handled cleanly every time so far, no lost work, but worth a look if it keeps recurring — a small script/lock to hand out the next version number would remove the manual "check right before merging" step. _(added 2026-07-22)_
- **Clicked through Forecast and Calendar directly on the live site — clean both times, but on the sandbox tenant, not yours.** No errors, both rendered properly. The gap: the sandbox tenant already has everything loaded in memory, so it never exercises the actual "fetch more when you need it" code this change added — the one thing that would need your own real session to properly prove out. Asked what you actually saw go wrong on screen (blank page, stuck spinner, wrong numbers) since nothing in the log pointed at a cause — still waiting to hear back. _(added 2026-07-22)_
_…and 415 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 3282 | 428 | 575 |
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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-22 20:09 UTC._
