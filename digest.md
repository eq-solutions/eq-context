---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-21
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-21 08:07 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-21 07:58 UTC → 2026-07-21 08:07 UTC)

- Merged: eq-shell [#920](https://github.com/eq-solutions/eq-shell/pull/920) fix(licences): exclude is_private licences from admin-facing
- Merged: eq-shell [#899](https://github.com/eq-solutions/eq-shell/pull/899) fix(security): reassert security_invoker on 3 field_* views 
- Merged: eq-shell [#898](https://github.com/eq-solutions/eq-shell/pull/898) perf(home): dedupe duplicate dashboard + pending-connections
- Merged: eq-shell [#897](https://github.com/eq-solutions/eq-shell/pull/897) NSW Comms: Start-by estimate from PO+53-day planning rule (P
- Merged: eq-shell [#890](https://github.com/eq-solutions/eq-shell/pull/890) feat(access): gate contact PII in direct-read RPCs (cluster 
- Merged: eq-shell [#889](https://github.com/eq-solutions/eq-shell/pull/889) NSW Comms: parallel jobs-GET + resource dashboard landing vi
- Merged: eq-shell [#888](https://github.com/eq-solutions/eq-shell/pull/888) perf(auth): parallelize verify-shell-session's independent D
- Merged: eq-shell [#887](https://github.com/eq-solutions/eq-shell/pull/887) perf(obs): lazy-load posthog-js off the cold-open critical p

## ⚠ Needs you (4)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-07-21.md](sessions/2026-07-21.md) · [failures.md](system/failures.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 4 | 0d |
| eq-solves-service | ? unknown | ? | 1 | 0d |
| eq-field | ? unknown | ? | 2 | 0d |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 4d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [EQ Field handoff auto-recovery (rejected)](https://eq-solutions.sentry.io/issues/133584980/) | 6 | 2026-07-19 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 5 | 2026-07-16 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/133972818/) | 3 | 2026-07-20 |
| eq-shell | [Error: eq-ops rpc eq_upsert_pricing_config failed: pricing config requires manag](https://eq-solutions.sentry.io/issues/135532286/) | 2 | 2026-07-21 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 2 | 2026-07-14 |
| eq-solves-service | [auth handoff: expired](https://eq-solutions.sentry.io/issues/135281279/) | 1 | 2026-07-19 |
| eq-shell | [EQ Field handoff timeout — no postMessage in 30s](https://eq-solutions.sentry.io/issues/129554465/) | 1 | 2026-07-19 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-21 | eq-shell | [#929](https://github.com/eq-solutions/eq-shell/pull/929) Suppliers.tsx: fix stale comment about which perm gates writes |
| 2026-07-21 | eq-shell | [#927](https://github.com/eq-solutions/eq-shell/pull/927) Suppliers directory - EQ Ops (SKS) |
| 2026-07-21 | eq-shell | [#924](https://github.com/eq-solutions/eq-shell/pull/924) Fix: flush Sentry before functions return — server events were si |
| 2026-07-21 | eq-shell | [#925](https://github.com/eq-solutions/eq-shell/pull/925) feat(retention): daily job to finalise deleted Cards accounts |
| 2026-07-21 | eq-shell | [#923](https://github.com/eq-solutions/eq-shell/pull/923) Quote doc: fix Clarifications alignment (justified -> left) |
| 2026-07-21 | eq-shell | [#922](https://github.com/eq-solutions/eq-shell/pull/922) Staff: Company column for Labour Hire + Subcontractor, fix role d |
| 2026-07-21 | eq-shell | [#921](https://github.com/eq-solutions/eq-shell/pull/921) Security fix: cross-org identity-collision metadata leak in worke |
| 2026-07-21 | eq-solves-service | [#575](https://github.com/eq-solutions/eq-service/pull/575) fix(auth): scheduled functions' own trigger URLs get redirected b |
| 2026-07-21 | eq-solves-service | [#574](https://github.com/eq-solutions/eq-service/pull/574) perf: pick up merged load-time PRs + combine duplicate MFA-grace/ |
| 2026-07-21 | eq-field | [#516](https://github.com/eq-solutions/eq-field/pull/516) v3.5.340 — retire safety.js's duplicate Prestart + Toolbox forms |
| 2026-07-21 | eq-field | [#515](https://github.com/eq-solutions/eq-field/pull/515) Fix Sentry telemetry delivery: await captureServerError, correct  |
| 2026-07-21 | eq-field | [#514](https://github.com/eq-solutions/eq-field/pull/514) fix: mobile My Schedule + home tile show Sat/Sun when rostered (v |
| 2026-07-21 | eq-field | [#513](https://github.com/eq-solutions/eq-field/pull/513) docs: reframe apprentice comments off compliance language |
| 2026-07-21 | eq-field | [#512](https://github.com/eq-solutions/eq-field/pull/512) v3.5.337 — extract + test roster.js approved-leave overlay |
| 2026-07-21 | eq-field | [#511](https://github.com/eq-solutions/eq-field/pull/511) v3.5.336 — extract apprentices.js year-advancement + rating rules |
_Showing 15 of 105 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **`EQ_CONTEXT_PAT` still can't read Actions runs on eq-shell/eq-service/eq-field/eq-cards for the automated nightly/on-merge digest refresh.** Spent a long back-and-forth on this: confirmed it's a fine-grained token, walked through adding the 4 repos + Actions/Contents permissions, clicked Update — API still returns `403 "Resource not accessible by personal access token"` on all 3 repos added this session (eq-context, added at token creation, works fine). Most likely an org-approval step never completed, but not confirmed. **Royce's call: leave it** — not worth more time right now. Stopgap in place: I can run `refresh_digest.py` locally with my own working GitHub access any time current numbers are needed (did this once today — all 5 repos show real CI status as of this session). _(added 2026-07-21)_
- **Found in passing: eq-cards' "Notify substrate on merge" workflow fails on every commit** (exit 22, empty `Authorization: Bearer` token when dispatching to eq-context) — a broken fire-and-forget webhook, not a build gate, but substrate may be missing merge notifications from eq-cards until the secret is fixed. _(added 2026-07-21)_
- **Tenant-isolation root fix still open.** A Field session without a `tenant_slug` claim (every plain-PIN login) falls back to a client-supplied tenant, checked only against a static allow-list. The real fix (bind tenant into the session at PIN-mint time) is designed but deliberately deferred pending real frequency data. One-time scheduled check `collision-alert-week1-check` set for 2026-07-27 09:00 AEST to gather it — a manual "Run now" attempt didn't actually trigger; it'll fire on schedule. _(added 2026-07-21)_
- **EQ-tenant worker→staff sync doesn't exist** — `workers-canonical-sync` is hardcoded to SKS only. Deprioritized rather than built, since the EQ tenant's Field plane has no real usage yet — revisit if that changes. _(added 2026-07-21)_
- **The dormant `shell_control.persons`/`person_xref` "golden record" spine (ADR-002)** was found built and never populated — three repos each run their own separate identity-matching heuristic instead. Explicitly parked as a separate, later initiative, not this sprint. _(added 2026-07-21)_
- **`mint-cards-iframe-token.ts` (eq-shell) is confirmed dead code**, superseded by `mint-cards-otp.ts` — never actually removed. Trivial cleanup, not done. _(added 2026-07-21)_
- **eq-cards `main`'s "Notify substrate on merge" workflow is failing on every commit** (exit 22, empty `Authorization: Bearer` token when dispatching to `eq-context`) — noticed while confirming CI health, unrelated to the migration-number fix. Not a build/test gate, just a broken fire-and-forget webhook, so substrate may be missing merge notifications from eq-cards until the secret is fixed. _(added 2026-07-21)_
- **Not independently confirmed live by Royce yet**: the merged fix above was verified via code review, automated tests, and a clean preview boot — but an actual click-through as an SKS user (Safety → Site Audits/Records, and the Site Reports screens for Prestart/Toolbox/Diary) was blocked by safety guards when tried locally (moving the SKS database key through a file or a browser URL got correctly stopped rather than worked around) and never completed. Worth a real look next time you're in the SKS view. _(added 2026-07-21)_
- **The rest of the "biggest files are untested / too large" list from the review is still open:** Apprentices, Roster, Timesheets are each still well over the size where they need to be split up further (only removed one duplicate section each so far); a few other large files (the Safety area, two Tender-Pipeline-related files) haven't been touched at all yet. _(added 2026-07-21)_
- **Checked Sentry after deploy: still zero events, which is expected, not a new problem.** The warning only fires on a specific real-world request shape (an old-style session hitting the fallback) — the fix makes it capable of reporting, it doesn't manufacture that traffic. Re-check after a normal working day, or after a deliberate test hits that path. _(added 2026-07-21)_
_…and 387 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **SKS's standalone Field app (sks-nsw-labour) currently lets anyone with the app's public web address read or wipe roster/schedule/timesheet data for all ~50 SKS people — no login required.** A 4-stage fix plan already exists: Stage 1 (the identity layer) is built and sitting in an unmerged pull request, ready to activate; Stage 2 (locks data to the right company) is drafted but not run; Stage 3 (removes the open door) is drafted but has 3 known gaps that need closing first (a few tables would go offline instead of getting properly locked down); Stage 4 (final cleanup) isn't drafted yet. Nothing on SKS's live system was touched — this needs Royce's own hands per stage (setting secrets, running SQL, flipping a switch), plus review of the gaps before Stage 3 is safe. Handed off as its own task rather than half-finishing it inside an unrelated session. _(added 2026-07-20)_
- Royce to click-through confirm a real weekend-rostered person's mobile schedule + home tile on both apps. _(added 2026-07-21)_
- **Still needed: who should receive the weekly NSW Comms summary email?** Built, just needs a recipient list before it's switched on. _(added 2026-07-17)_
- **Not done: live-demo readiness check** (data cleanliness / no visible errors on whatever screen gets shown) — offered, awaiting Royce's go. _(added 2026-07-16)_
- **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date. **PIN audit 2026-07-05 (Royce-confirmed):** this repo has its own independent login/PIN system, still actively used — a completely different codebase from eq-field, not affected by eq-field's own PIN-gate retirement (see `eq/changelog/field.md` "SKS = Core-only auth", v3.5.200).
- **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
- **SKS anon-remediation (nspb)** — exact policy worklist in `cross-app-linkage-remediation-plan-2026-06-07.md` §7a. Separate from ehow work. SKS-live gated.
- **eq-shell** — ~~converge `c2-shell-roles` + `sks-field-host` branches~~ — `c2-shell-roles` no longer exists in eq-shell repo (deleted). Re-assess: verify whether the security-groups work from `sks-live-sprint-2026-06-07.md` Prompt A was folded into main or abandoned before reopening this track.
- **Security groups Phase 2–5** — wire group perms into session, `AdminSecurityGroups` page, first real `user_security_groups` row for a SKS user.
- Royce to independently click-through-confirm the Weekends toggle, roster names, and both safety forms live (smoke-tested remotely, not yet confirmed by Royce beyond the original repros) _(added 2026-07-03)_
_…and 57 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog._

| File | Lines | Open | Done (unrotated) |
|------|------:|-----:|------------------:|
| [EQ](eq/pending.md) | 2967 | 405 | 421 |
| [SKS](sks/pending.md) | 457 | 68 | 64 |
| [SKS active](sks/active.md) | 108 | 0 | 0 |
| [OPS](ops/pending.md) | 230 | 28 | 6 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-21 | [eq-shell had its own copy of the licence-privacy gap; found, fixed, deployed, and smoke-tested](sessions/2026-07-21.md) |
| 2026-07-20 | [invite-accept duplicate-identity follow-up: root cause disproven, hardening shipped + deployed, then a real lead found via Sentry](sessions/2026-07-20.md) |
| 2026-07-19 | [Digest sweep: two Sentry issues root-caused, one real fix shipped + verified live](sessions/2026-07-19.md) |
| 2026-07-17 | [AI brief's quote signals were silently zero for SKS; realigned to the live enum, guarded, shipped live](sessions/2026-07-17.md) |
| 2026-07-16 | [verified migration 0185 live, explained the merge feature's location, seeded a real demo pair](sessions/2026-07-16.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-21 08:07 UTC._
