---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-21
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-21 09:03 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-21 08:55 UTC → 2026-07-21 09:03 UTC)

- Merged: eq-shell [#938](https://github.com/eq-solutions/eq-shell/pull/938) Suppliers: role-gate login/password behind manager/superviso
- Merged: eq-shell [#920](https://github.com/eq-solutions/eq-shell/pull/920) fix(licences): exclude is_private licences from admin-facing
- Merged: eq-shell [#916](https://github.com/eq-solutions/eq-shell/pull/916) feat(staff): per-column filtering on the Staff table
- Merged: eq-shell [#915](https://github.com/eq-solutions/eq-shell/pull/915) fix(staff): clear on_roster when archiving a staff record
- Merged: eq-shell [#914](https://github.com/eq-solutions/eq-shell/pull/914) fix(auth): format-tolerant phone match on invite-accept stub
- Merged: eq-shell [#901](https://github.com/eq-solutions/eq-shell/pull/901) NSW Comms: cut Dashboard load-time from ~5.4s to ~2 round tr
- Merged: eq-shell [#900](https://github.com/eq-solutions/eq-shell/pull/900) perf(offline): extend the unsaved-changes guard to site and 
- Merged: eq-shell [#899](https://github.com/eq-solutions/eq-shell/pull/899) fix(security): reassert security_invoker on 3 field_* views 

## ⚠ Needs you (4)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-07-21.md](sessions/2026-07-21.md) · [failures.md](system/failures.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 5 | 0d |
| eq-solves-service | ? unknown | ? | 1 | 0d |
| eq-field | ? unknown | ? | 3 | 0d |
| eq-cards | ? unknown | ? | 2 | 0d |
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
| 2026-07-21 | eq-shell | [#938](https://github.com/eq-solutions/eq-shell/pull/938) Suppliers: role-gate login/password behind manager/supervisor |
| 2026-07-21 | eq-shell | [#937](https://github.com/eq-solutions/eq-shell/pull/937) Fix: 0194 left three preset RPCs granted to PUBLIC/anon |
| 2026-07-21 | eq-shell | [#928](https://github.com/eq-solutions/eq-shell/pull/928) EQ Ops: unblock Setup, restore labour cost, column filters, reord |
| 2026-07-21 | eq-shell | [#934](https://github.com/eq-solutions/eq-shell/pull/934) One-shot endpoint: move certificates into licences (Phase B) |
| 2026-07-21 | eq-shell | [#931](https://github.com/eq-solutions/eq-shell/pull/931) Suppliers.tsx: add per-column filters to the desktop table |
| 2026-07-21 | eq-shell | [#932](https://github.com/eq-solutions/eq-shell/pull/932) Extend identity-collision gate to the invite-path approval |
| 2026-07-21 | eq-shell | [#929](https://github.com/eq-solutions/eq-shell/pull/929) Suppliers.tsx: fix stale comment about which perm gates writes |
| 2026-07-21 | eq-shell | [#927](https://github.com/eq-solutions/eq-shell/pull/927) Suppliers directory - EQ Ops (SKS) |
| 2026-07-21 | eq-shell | [#924](https://github.com/eq-solutions/eq-shell/pull/924) Fix: flush Sentry before functions return — server events were si |
| 2026-07-21 | eq-shell | [#925](https://github.com/eq-solutions/eq-shell/pull/925) feat(retention): daily job to finalise deleted Cards accounts |
| 2026-07-21 | eq-shell | [#923](https://github.com/eq-solutions/eq-shell/pull/923) Quote doc: fix Clarifications alignment (justified -> left) |
| 2026-07-21 | eq-shell | [#922](https://github.com/eq-solutions/eq-shell/pull/922) Staff: Company column for Labour Hire + Subcontractor, fix role d |
| 2026-07-21 | eq-shell | [#921](https://github.com/eq-solutions/eq-shell/pull/921) Security fix: cross-org identity-collision metadata leak in worke |
| 2026-07-21 | eq-solves-service | [#575](https://github.com/eq-solutions/eq-service/pull/575) fix(auth): scheduled functions' own trigger URLs get redirected b |
| 2026-07-21 | eq-solves-service | [#574](https://github.com/eq-solutions/eq-service/pull/574) perf: pick up merged load-time PRs + combine duplicate MFA-grace/ |
_Showing 15 of 108 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **One test step is blocked, needs your call:** fast-forwarding that one test account's "deleted" timestamp by 31 days (so the cleanup job can be checked without waiting a real month) got blocked by the safety guardrail, even for a single-column edit on a known test row. Either approve a retry, or just let the real 30 days pass and it'll be checked then. _(added 2026-07-21)_
- **Blocked on Royce**: could not confirm or fix this via API — `gh api orgs/eq-solutions/personal-access-token-requests` and `.../personal-access-tokens` both 404, even with `admin:org` scope. Asked Royce to check [github.com/organizations/eq-solutions/settings/personal-access-tokens](https://github.com/organizations/eq-solutions/settings/personal-access-tokens) directly — either approve a pending request for the new token, or relax a restrictive org policy. **No answer yet — session ended on a handoff prompt instead of continuing to chase it.** _(added 2026-07-21)_
- **Once unblocked**: re-run the diagnostic workflow and confirm HTTP 200, merge the diagnostic branch's error-surfacing improvement (worth keeping regardless — turns a silent exit-22 into a readable error) into all 4 repos' `notify-substrate.yml`, confirm all 4 go green, delete the diagnostic branch. _(added 2026-07-21)_
- **`EQ_CONTEXT_PAT` still can't read Actions runs on eq-shell/eq-service/eq-field/eq-cards for the automated nightly/on-merge digest refresh.** Spent a long back-and-forth on this: confirmed it's a fine-grained token, walked through adding the 4 repos + Actions/Contents permissions, clicked Update — API still returns `403 "Resource not accessible by personal access token"` on all 3 repos added this session (eq-context, added at token creation, works fine). Most likely an org-approval step never completed, but not confirmed. **Royce's call: leave it** — not worth more time right now. Stopgap in place: I can run `refresh_digest.py` locally with my own working GitHub access any time current numbers are needed (did this once today — all 5 repos show real CI status as of this session). _(added 2026-07-21)_
- **Root-caused the eq-cards notify-substrate failure — a different, unrelated secret to everything else this session.** It's the ORG-level `EQ_CONTEXT_PAT` (visibility: selected → eq-cards/eq-field/eq-service/eq-shell, created 2026-06-28 "notify-substrate use only") — separate from the repo-level `EQ_CONTEXT_PAT` on eq-context fixed earlier today. Confirmed via live log: `Authorization: Bearer ` is genuinely empty, not a permissions error — the org secret has never had a value set. **Needs you**: `github.com/organizations/eq-solutions/settings/secrets/actions` → `EQ_CONTEXT_PAT` → paste a value (any PAT with write access to eq-context works) → Save. Not a build gate, but substrate is missing merge notifications from eq-cards/eq-field/eq-service/eq-shell until it's set. _(added 2026-07-21, root-caused 2026-07-21)_
- **Re-checked digest CI-status automation — confirmed still blocked, no change since the "leave it" call.** Re-ran the refresh; same "? unknown" result for all 4 repos via the automated path. Manual refresh (`refresh_digest.py` run locally) remains the working stopgap. _(added 2026-07-21)_
- **Tenant-isolation root fix still open.** A Field session without a `tenant_slug` claim (every plain-PIN login) falls back to a client-supplied tenant, checked only against a static allow-list. The real fix (bind tenant into the session at PIN-mint time) is designed but deliberately deferred pending real frequency data. One-time scheduled check `collision-alert-week1-check` set for 2026-07-27 09:00 AEST to gather it — a manual "Run now" attempt didn't actually trigger; it'll fire on schedule. _(added 2026-07-21)_
- **EQ-tenant worker→staff sync doesn't exist** — `workers-canonical-sync` is hardcoded to SKS only. Deprioritized rather than built, since the EQ tenant's Field plane has no real usage yet — revisit if that changes. _(added 2026-07-21)_
- **The dormant `shell_control.persons`/`person_xref` "golden record" spine (ADR-002)** was found built and never populated — three repos each run their own separate identity-matching heuristic instead. Explicitly parked as a separate, later initiative, not this sprint. _(added 2026-07-21)_
- **`mint-cards-iframe-token.ts` (eq-shell) is confirmed dead code**, superseded by `mint-cards-otp.ts` — never actually removed. Trivial cleanup, not done. _(added 2026-07-21)_
_…and 392 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 2989 | 409 | 429 |
| [SKS](sks/pending.md) | 457 | 68 | 64 |
| [SKS active](sks/active.md) | 108 | 0 | 0 |
| [OPS](ops/pending.md) | 252 | 30 | 6 |

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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-21 09:03 UTC._
