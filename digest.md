---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-21
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-21 05:04 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-21 03:44 UTC → 2026-07-21 05:04 UTC)

- ⚠ Needs you: 3 → 4 (new items)

## ⚠ Needs you (4)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-10 (P0 — confirmed exposure) — `ANTHROPIC_API_KEY` + `RESEND_API_KEY` stored as plaintext Netlify env vars (`is · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-07-21.md](sessions/2026-07-21.md) · [failures.md](system/failures.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 0 | — |
| eq-solves-service | ? unknown | ? | 0 | — |
| eq-field | ? unknown | ? | 0 | — |
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
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/132643934/) | 2 | 2026-07-07 |
| eq-solves-service | [auth handoff: expired](https://eq-solutions.sentry.io/issues/135281279/) | 1 | 2026-07-19 |
| eq-shell | [EQ Field handoff timeout — no postMessage in 30s](https://eq-solutions.sentry.io/issues/129554465/) | 1 | 2026-07-19 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-16 | eq-solves-intake | [#73](https://github.com/eq-solutions/eq-solves-intake/pull/73) feat(intake): usage-based survivor pick for the Sites Dupes tab |
| 2026-07-16 | eq-solves-intake | [#74](https://github.com/eq-solutions/eq-solves-intake/pull/74) fix: backport two eq-shell-only fixes into source |
| 2026-07-16 | eq-solves-intake | [#72](https://github.com/eq-solutions/eq-solves-intake/pull/72) feat(intake): wire the merge-panel UI into IntakeHealthHome |
| 2026-07-16 | eq-solves-intake | [#71](https://github.com/eq-solutions/eq-solves-intake/pull/71) feat(intake): flagSitePairForMerge client wrapper |
| 2026-07-15 | eq-solves-intake | [#70](https://github.com/eq-solutions/eq-solves-intake/pull/70) feat(intake): site merge preview + execute client wrappers |
| 2026-07-14 | eq-solves-intake | [#69](https://github.com/eq-solutions/eq-solves-intake/pull/69) feat(intake): AI adjudicator — Claude suggests a verdict + reason |
| 2026-07-14 | eq-solves-intake | [#68](https://github.com/eq-solutions/eq-solves-intake/pull/68) feat(intake): adjudicable console — capture the human verdict on  |
_7 merges · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Found a real bug: the Safety area's Prestart form (crew sign-off before starting work) existed in two separate places in the code, and they didn't always agree with each other on whether a submission should be allowed** — whichever copy loaded most recently on a person's device silently won, for anyone using either screen. Fixed by removing the duplicate and keeping the one actually in daily use; the reporting/records views and Toolbox Talk's "copy from today's prestart" were carefully preserved. **PR [#516](https://github.com/eq-solutions/eq-field/pull/516) OPEN, deploy preview green, NOT merged** — click through Safety → Toolbox/Records and the separate Prestart screen on the preview before merging, since this touches a live safety form. _(added 2026-07-21)_
- **Toolbox Talks may have the exact same duplicate-copy problem as Prestart did** — spotted in passing (a second, separate "Toolbox" entry point exists alongside the one inside Safety) but not investigated. Worth the same check once Prestart's fix is confirmed working. _(added 2026-07-21)_
- **The rest of the "biggest files are untested / too large" list from the review is still open:** Apprentices, Roster, Timesheets are each still well over the size where they need to be split up further (only removed one duplicate section each so far); a few other large files (the Safety area, two Tender-Pipeline-related files) haven't been touched at all yet. _(added 2026-07-21)_
- **Checked Sentry after deploy: still zero events, which is expected, not a new problem.** The warning only fires on a specific real-world request shape (an old-style session hitting the fallback) — the fix makes it capable of reporting, it doesn't manufacture that traffic. Re-check after a normal working day, or after a deliberate test hits that path. _(added 2026-07-21)_
- **Worth a quick look once deployed:** confirm a weekend-rostered person's mobile schedule and "Next shift" home tile show Saturday/Sunday correctly. _(added 2026-07-21)_
- **Worth a quick look once deployed:** confirm the Company field shows/saves correctly for Labour Hire and Subcontractor (desktop + mobile), and re-export SKS-17386 to confirm Clarifications now sits left-aligned without needing a manual fix in Word. _(added 2026-07-21)_
- **The rest of that audit's recommended fixes still await your decision:** whether the account-deletion feature should actually delete data (it currently just blanks it out) or the privacy policy wording should change instead; adding a way to revoke a licence link once it's been shared; and adding a simple "how sure are we this credential is real" label to licences. Full detail in the audit doc (`eq-context/eq/cards/portable-trade-identity-audit-2026-07-20.md`). _(added 2026-07-21)_
- **Field's mobile-improvement sprint (PRs #486–#489, v3.5.326–329) has no changelog entry.** Real shipped work, but written as plain descriptive bullets rather than checked-off items, so the dedup pass correctly left it alone rather than guess. Worth a manual changelog entry if you want it on record. _(added 2026-07-20)_
- **~250 bullets across the 5 products were deliberately left in this file** — ambiguous product ownership, investigation-only findings with no shipped fix, or genuinely cross-cutting content. Not a backlog in the usual sense; full per-product breakdown is in today's session log. _(added 2026-07-20)_
- **Whether to actually build the "QR code for on-site sign-in" feature, or drop it for good.** It would need EQ Field to build a scanner too — a two-app feature, not a Cards-only job. Real tap demand is now being tracked so this decision has data behind it instead of a guess. _(added 2026-07-20)_
_…and 384 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 2916 | 398 | 395 |
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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-21 05:04 UTC._
