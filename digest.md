---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-21
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-21 10:13 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-21 09:15 UTC → 2026-07-21 10:13 UTC)

- Merged: eq-shell [#941](https://github.com/eq-solutions/eq-shell/pull/941) EQ Ops Setup: add Save all for the preset line-item library
- Merged: eq-shell [#940](https://github.com/eq-solutions/eq-shell/pull/940) chore: retire the certificates-migrate endpoint (Phase C cle
- Merged: eq-shell [#919](https://github.com/eq-solutions/eq-shell/pull/919) Option 3: surface + gate identity collisions in the staff-ap
- Merged: eq-shell [#918](https://github.com/eq-solutions/eq-shell/pull/918) Alert-only visibility: identity collisions + never-invited w
- Merged: eq-shell [#917](https://github.com/eq-solutions/eq-shell/pull/917) feat(staff): admin licence backfill with photo/PDF upload
- Merged: eq-shell [#898](https://github.com/eq-solutions/eq-shell/pull/898) perf(home): dedupe duplicate dashboard + pending-connections
- Merged: eq-shell [#897](https://github.com/eq-solutions/eq-shell/pull/897) NSW Comms: Start-by estimate from PO+53-day planning rule (P
- Merged: eq-shell [#890](https://github.com/eq-solutions/eq-shell/pull/890) feat(access): gate contact PII in direct-read RPCs (cluster 

## ⚠ Needs you (4)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-07-21.md](sessions/2026-07-21.md) · [failures.md](system/failures.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 5 | 0d |
| eq-solves-service | ? unknown | ? | 3 | 0d |
| eq-field | ? unknown | ? | 3 | 0d |
| eq-cards | ? unknown | ? | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

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
| 2026-07-21 | eq-shell | [#939](https://github.com/eq-solutions/eq-shell/pull/939) docs: correct licence-photos RLS mechanism (segment 2, not segmen |
| 2026-07-21 | eq-shell | [#941](https://github.com/eq-solutions/eq-shell/pull/941) EQ Ops Setup: add Save all for the preset line-item library |
| 2026-07-21 | eq-shell | [#940](https://github.com/eq-solutions/eq-shell/pull/940) chore: retire the certificates-migrate endpoint (Phase C cleanup) |
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
_Showing 15 of 112 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **The `production` GitHub Environment on eq-shell has no protection rules** (confirmed directly via the GitHub API — the reviewer list is empty). The documented safety net for every tenant-database migration doesn't actually exist right now. This isn't specific to this session's changes — it means ANY future migration dispatch (by anyone, on any tenant) applies immediately with no approval step, contradicting the "explicit human go before live DDL" design the workflow file describes. Fix is a plain GitHub settings change (repo Settings → Environments → production → add Royce as a required reviewer) — not something fixable by me via API or CLI. _(added 2026-07-21)_
- **A separate, already-diagnosed cause of people getting logged out unexpectedly** (a background check treats "the server was just slow to answer" the same as "you're not logged in any more," and logs you out either way) is understood but not yet built, since it changes how login/session behaviour works and needs an explicit go-ahead first. _(added 2026-07-21)_
- **One test step is blocked, needs your call:** fast-forwarding that one test account's "deleted" timestamp by 31 days (so the cleanup job can be checked without waiting a real month) got blocked by the safety guardrail, even for a single-column edit on a known test row. Either approve a retry, or just let the real 30 days pass and it'll be checked then. _(added 2026-07-21)_
- **eq-shell / eq-field / eq-service still broken** — this session only fixed eq-cards. Same two steps needed on each: (1) swap each repo's `EQ_CONTEXT_PAT` from the 403'ing fine-grained PAT to a classic `repo`-scope PAT (can reuse the same classic token across repos — it's Royce's own credential, not per-repo), (2) port `debug/notify-substrate-diagnostics`'s error-surfacing diff (visible on eq-cards' merged history, commit range ending `0a5fef8`) into each repo's `notify-substrate.yml` so future failures are legible instead of a silent exit-22. _(added 2026-07-21)_
- **`EQ_CONTEXT_PAT` still can't read Actions runs on eq-shell/eq-service/eq-field/eq-cards for the automated nightly/on-merge digest refresh.** Spent a long back-and-forth on this: confirmed it's a fine-grained token, walked through adding the 4 repos + Actions/Contents permissions, clicked Update — API still returns `403 "Resource not accessible by personal access token"` on all 3 repos added this session (eq-context, added at token creation, works fine). Most likely an org-approval step never completed, but not confirmed. **Royce's call: leave it** — not worth more time right now. Stopgap in place: I can run `refresh_digest.py` locally with my own working GitHub access any time current numbers are needed (did this once today — all 5 repos show real CI status as of this session). _(added 2026-07-21)_
- **Root-caused the eq-cards notify-substrate failure — a different, unrelated secret to everything else this session.** It's the ORG-level `EQ_CONTEXT_PAT` (visibility: selected → eq-cards/eq-field/eq-service/eq-shell, created 2026-06-28 "notify-substrate use only") — separate from the repo-level `EQ_CONTEXT_PAT` on eq-context fixed earlier today. Confirmed via live log: `Authorization: Bearer ` is genuinely empty, not a permissions error — the org secret has never had a value set. **Needs you**: `github.com/organizations/eq-solutions/settings/secrets/actions` → `EQ_CONTEXT_PAT` → paste a value (any PAT with write access to eq-context works) → Save. Not a build gate, but substrate is missing merge notifications from eq-cards/eq-field/eq-service/eq-shell until it's set. _(added 2026-07-21, root-caused 2026-07-21)_
- **Re-checked digest CI-status automation — confirmed still blocked, no change since the "leave it" call.** Re-ran the refresh; same "? unknown" result for all 4 repos via the automated path. Manual refresh (`refresh_digest.py` run locally) remains the working stopgap. _(added 2026-07-21)_
- **The `shell_control.persons`/`person_xref` "golden record" spine — investigated further, recommendation reversed.** Asked to do a full 3-repo build; investigation disproved the premise it was based on. Only eq-cards actually matches identities (phone/email against `public.workers`) — eq-shell only reads the output, and eq-field has no matching of its own (its one identity lookup is `user_id`-keyed, already-established, SKS-only). Also found eq-field has its own separate, deliberately parked initiative for a related but different problem (`ADR-PERSON-IDENTITY.md` — same-name disambiguation within eq-field's own tables, not cross-tenant identity; Phases 1–2 shipped, Phases 3–4 explicitly gated by Royce on "not until SKS is stable in live", set 2026-06-08) — and that ADR's own canonical-link plan points at `public.workers`, not `shell_control.persons`/`person_xref`. Recommendation: don't build the spine — it looks like a second, unused design for a job `public.workers` already does. **Royce confirmed: "don't build the spine, leave it parked."** Closed — no further action unless a real second consumer shows up (most likely trigger: EQ tenant's Field plane going live). Open question for later, not urgent: whether to formally retire the empty `persons`/`person_xref` tables rather than leave them as dead schema two different plans could collide on. _(added 2026-07-21, corrected 2026-07-21, confirmed parked 2026-07-21)_
- **EQ-tenant worker→staff sync doesn't exist** — `workers-canonical-sync` is hardcoded to SKS only. Deprioritized rather than built, since the EQ tenant's Field plane has no real usage yet — revisit if that changes. _(added 2026-07-21)_
- **`mint-cards-iframe-token.ts` (eq-shell) is confirmed dead code**, superseded by `mint-cards-otp.ts` — never actually removed. Trivial cleanup, not done. _(added 2026-07-21)_
_…and 395 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Confirm a non-manager (employee-level) login actually sees a blank instead of real credentials** — only had a manager session available to test with this session. _(added 2026-07-21)_
- **Confirm the mobile card view on a real phone** (tap-to-call, login/password display, reveal toggle) — couldn't force a reliable mobile browser preview in this session's tooling. _(added 2026-07-21)_
- **Password-manager decision still open** — Royce said "not now" to setting up a shared 1Password/Bitwarden vault this session; the in-app login/password fields are the interim answer. Revisit if the list of stored credentials grows. _(added 2026-07-21)_
- **SKS's standalone Field app (sks-nsw-labour) currently lets anyone with the app's public web address read or wipe roster/schedule/timesheet data for all ~50 SKS people — no login required.** A 4-stage fix plan already exists: Stage 1 (the identity layer) is built and sitting in an unmerged pull request, ready to activate; Stage 2 (locks data to the right company) is drafted but not run; Stage 3 (removes the open door) is drafted but has 3 known gaps that need closing first (a few tables would go offline instead of getting properly locked down); Stage 4 (final cleanup) isn't drafted yet. Nothing on SKS's live system was touched — this needs Royce's own hands per stage (setting secrets, running SQL, flipping a switch), plus review of the gaps before Stage 3 is safe. Handed off as its own task rather than half-finishing it inside an unrelated session. _(added 2026-07-20)_
- Royce to click-through confirm a real weekend-rostered person's mobile schedule + home tile on both apps. _(added 2026-07-21)_
- **Still needed: who should receive the weekly NSW Comms summary email?** Built, just needs a recipient list before it's switched on. _(added 2026-07-17)_
- **Not done: live-demo readiness check** (data cleanliness / no visible errors on whatever screen gets shown) — offered, awaiting Royce's go. _(added 2026-07-16)_
- **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date. **PIN audit 2026-07-05 (Royce-confirmed):** this repo has its own independent login/PIN system, still actively used — a completely different codebase from eq-field, not affected by eq-field's own PIN-gate retirement (see `eq/changelog/field.md` "SKS = Core-only auth", v3.5.200).
- **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
- **SKS anon-remediation (nspb)** — exact policy worklist in `cross-app-linkage-remediation-plan-2026-06-07.md` §7a. Separate from ehow work. SKS-live gated.
_…and 61 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog._

| File | Lines | Open | Done (unrotated) |
|------|------:|-----:|------------------:|
| [EQ](eq/pending.md) | 3017 | 409 | 444 |
| [SKS](sks/pending.md) | 470 | 71 | 67 |
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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-21 10:13 UTC._
