---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-14
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-14 10:30 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-14 10:29 UTC → 2026-07-14 10:30 UTC)

- Merged: eq-shell [#860](https://github.com/eq-solutions/eq-shell/pull/860) feat(audit): Phase 2b — before/after drill-down on the activ
- Merged: eq-shell [#835](https://github.com/eq-solutions/eq-shell/pull/835) feat(comms): native mobile view for NSW Comms — card list + 
- Merged: eq-shell [#832](https://github.com/eq-solutions/eq-shell/pull/832) fix(canonical): eq_site_advisory_summary authenticated-only 
- Merged: eq-shell [#829](https://github.com/eq-solutions/eq-shell/pull/829) feat(canonical): read RPC for the site-resolver adjudication
- Merged: eq-shell [#824](https://github.com/eq-solutions/eq-shell/pull/824) fix(security): drop vulnerable xlsx from the client bundle —
- Merged: eq-shell [#814](https://github.com/eq-solutions/eq-shell/pull/814) one-login P2 — worker-facing two-tile Core home (My Card + F
- Merged: eq-solves-service [#535](https://github.com/eq-solutions/eq-service/pull/535) chore(migrations): renumber colliding prefixes 0180/0181/018
- Merged: eq-solves-service [#533](https://github.com/eq-solutions/eq-service/pull/533) feat(reports): tenant-branded reports + run-sheet redesign

## ⚠ Needs you (6)

- 🟠 **PR aging 8d** — eq-solves-service [#459](https://github.com/eq-solutions/eq-service/pull/459) "chore(deps-dev): bump @vitejs/plugin-react from 6.0.1 to 6.0.3"
- 🟠 **PR aging 8d** — eq-solves-service [#458](https://github.com/eq-solutions/eq-service/pull/458) "chore(deps): bump tailwind-merge from 3.5.0 to 3.6.0"
- 🟠 **PR aging 8d** — eq-solves-service [#456](https://github.com/eq-solutions/eq-service/pull/456) "chore(deps-dev): bump tailwindcss from 4.2.2 to 4.3.2"
- 🟠 **Sentry new error** — `eq-shell` [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/)
- 🟠 **Sentry new error** — `eq-shell` [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 7 | 0d |
| eq-solves-service | ✓ success | 0d ago | 7 | 8d |
| eq-field | ✓ success | 0d ago | 2 | 2d |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 3 | 2026-07-14 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 2 | 2026-07-14 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/132643934/) | 2 | 2026-07-07 |
| eq-solves-service | [Error: COALESCE types uuid and text cannot be matched](https://eq-solutions.sentry.io/issues/132618557/) | 1 | 2026-07-07 |
| eq-shell | [Error: HTTP 400](https://eq-solutions.sentry.io/issues/132270381/) | 1 | 2026-07-05 |
| eq-cards | [provisionTenantExchange: unexpected HTTP 500](https://eq-solutions.sentry.io/issues/132064194/) | 1 | 2026-07-03 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-14 | eq-shell | [#860](https://github.com/eq-solutions/eq-shell/pull/860) feat(audit): Phase 2b — before/after drill-down on the activity l |
| 2026-07-14 | eq-shell | [#855](https://github.com/eq-solutions/eq-shell/pull/855) feat(equipment): re-point Plant & Equipment calibration onto cano |
| 2026-07-14 | eq-shell | [#854](https://github.com/eq-solutions/eq-shell/pull/854) docs(drift): retruth calibration-view allow-list comment (adoptio |
| 2026-07-14 | eq-shell | [#853](https://github.com/eq-solutions/eq-shell/pull/853) feat(audit): Phase 1c — audit-log retention (13mo hot / 7yr cold, |
| 2026-07-14 | eq-shell | [#848](https://github.com/eq-solutions/eq-shell/pull/848) feat(canonical): site-resolver adjudication — verdict capture (01 |
| 2026-07-14 | eq-shell | [#846](https://github.com/eq-solutions/eq-shell/pull/846) feat(audit): Phase 1d (eq-shell) — attribute worker create/edit t |
| 2026-07-14 | eq-shell | [#850](https://github.com/eq-solutions/eq-shell/pull/850) docs: reflect that Resend email delivery is live in production |
| 2026-07-14 | eq-shell | [#849](https://github.com/eq-solutions/eq-shell/pull/849) fix(drift): allow-list service.instrument_calibration_events (saf |
| 2026-07-14 | eq-shell | [#842](https://github.com/eq-solutions/eq-shell/pull/842) feat(audit): Phase 2a — date/type filters + CSV export on the act |
| 2026-07-14 | eq-shell | [#840](https://github.com/eq-solutions/eq-shell/pull/840) feat(audit): make public.audit_log (credential audit) append-only |
| 2026-07-14 | eq-shell | [#839](https://github.com/eq-solutions/eq-shell/pull/839) feat(audit): Phase 1b — legible activity log (de-noise + identity |
| 2026-07-14 | eq-shell | [#838](https://github.com/eq-solutions/eq-shell/pull/838) feat(mobile): native Ops create/edit form + Comms Fortnight roste |
| 2026-07-14 | eq-shell | [#837](https://github.com/eq-solutions/eq-shell/pull/837) feat(audit): make audit_log append-only - Phase 1a immutability l |
| 2026-07-14 | eq-shell | [#715](https://github.com/eq-solutions/eq-shell/pull/715) feat(access): gate enforcement on can()/useCan() not role names ( |
| 2026-07-14 | eq-solves-service | [#533](https://github.com/eq-solutions/eq-service/pull/533) feat(reports): tenant-branded reports + run-sheet redesign |
_Showing 15 of 113 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **NEXT — Claude as the adjudicator on the "unsure" rows.** Labels now accumulate. Wire the AI to read the full record context (customer, neighbouring sites, import source), propose a verdict + a plain-English reason on the ambiguous middle, human confirms with one tap. This is the jump from classical MDM to the ask-anything brain, and it makes the match-key decision self-calibrating instead of a one-time guess. _(added 2026-07-14)_
- **Core-owned merge/retire RPC over `app_data.sites`.** Adjudication records "same"; ACTING on it (merge/retire the duplicate) is still a separate human-gated step with no RPC yet — the survivorship engine. _(added 2026-07-14)_
- **Cross-app attribution (the rest of it)** — Field / Service / Intake still log their own edits as "system"; making those record the person is a multi-app job with no single choke point. _(added 2026-07-14)_
- **Later audit polish** — before/after values on each change, PDF export, and logging who reads the log; then on-request data erasure and anomaly alerts. _(added 2026-07-14)_
- **Your call: keep or bin the earlier EQ-vs-Microsoft/Google security comparison PDF** (`EQ-Security-One-Pager-2026-07-14.pdf`) — superseded by the CEO data-security version but left in Downloads. _(added 2026-07-14)_
- **Optional later: let an admin edit a worker's licence in-app.** Today an admin can only "Re-review" a worker's licences from the employer view — there's no way to correct a field (e.g. a wrong expiry); the fix path is the worker editing it in their own wallet, or you/us correcting the data. Presented this session; Royce chose the source-guard route instead, so this stays un-built. Would be a Shell change (new admin edit + touches "the worker owns their own data"). **Steelmanned 2026-07-14 (Royce asked) → explicitly PARKED for later** — the case-for (guards only fix lifetime types; the accountable admin is a read-only spectator; both current fix-paths don't scale; it's table-stakes for the Core sales motion) is written up in the session log. **RESOLVED 2026-07-14 — Royce: "let it ride."** Design landed = *flag, don't edit*: tidy data on the way in (ingest guards + onboarding normalisation), and for judgment calls the admin uses the existing decline-with-comment loop → worker fixes in their own wallet. Preserves worker-ownership; no admin-edit build. The only theoretical gap (a soft "flag for fix" nudge on an already-*connected* worker vs a decline) was judged hair-splitting and left alone. _(added 2026-07-14; resolved — not building)_
- **Field/Shell to surface the now-canonical calibration cert chain** — the calibration state + cert history are canonical and cross-app readable now; surfacing them in Field/Shell is their repos' work, not eq-service. _(added 2026-07-14)_
- **Crew retry + Sentry watch** — have the crew reopen via a normal browser tab (their home-screen icon may hold stale code from the day's deploys); if anyone still freezes, the fix now self-tags the exact stall in Sentry (`verify-timeout` / `login-timeout` / `session-spinner-timeout` / `chunk-error`). _(added 2026-07-14)_
- **Material-preset sanity check** — since materials presets now quote at Rate + markup, any entered as already-marked-up sell prices will read higher; worth a glance in the Rate library. _(added 2026-07-14, carried from #820)_
- **Phone-smoke Comms + Ops mobile on a real device** — both deployed and content-verified, but not exercised through a real authenticated session (auth-gated; not reproducible in the sandbox). _(added 2026-07-14)_
_…and 347 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date. **PIN audit 2026-07-05 (Royce-confirmed):** this repo has its own independent login/PIN system, still actively used — a completely different codebase from eq-field, not affected by eq-field's own PIN-gate retirement below.
- **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
- **SKS anon-remediation (nspb)** — exact policy worklist in `cross-app-linkage-remediation-plan-2026-06-07.md` §7a. Separate from ehow work. SKS-live gated.
- **eq-shell** — ~~converge `c2-shell-roles` + `sks-field-host` branches~~ — `c2-shell-roles` no longer exists in eq-shell repo (deleted). Re-assess: verify whether the security-groups work from `sks-live-sprint-2026-06-07.md` Prompt A was folded into main or abandoned before reopening this track.
- **Security groups Phase 2–5** — wire group perms into session, `AdminSecurityGroups` page, first real `user_security_groups` row for a SKS user.
- Royce to independently click-through-confirm the Weekends toggle, roster names, and both safety forms live (smoke-tested remotely, not yet confirmed by Royce beyond the original repros) _(added 2026-07-03)_
- **Reverse-angle gap (independent read-only pass 2026-07-05):** 9 legacy `people` rows have a canonical twin already but `people.canonical_id` is still NULL — matched live by phone+email vs jvkn `workers`: Louisa Cardinale, Matthew Khreich, Andre de Biasi, Damon Francis, Timothy Chapman, Bruno Pedrosa, Eric Nguyen (phone-only), Liam Holmgreen, Sam Powell. Back-link write not yet run; handed to the concurrent console actioning this batch (Royce copy-pasted the id list). Low-risk `UPDATE people SET canonical_id=… WHERE id=…` on nspb _(added 2026-07-05)_
- **Anthony Hartley correction**: not actually a violation of the 2026-07-05 "never touch it" plan — re-checked live. His canonical worker id `098e4bff-…` (the one documented as "dead weight, exclude, no hard-archive field") is still there, untouched, exactly as decided — it's referenced from his current live `app_data.staff` row. What got hard-deleted was a *different* duplicate, at the `app_data.staff` (Service/ehow) layer, not the canonical-worker (jvkn) layer the 2026-07-05 decision was about. No action needed.
- **121 items still pending in `eq_remediation_queue`** (steward-run-001) — unreviewed AI data-quality suggestions for staff/contacts, sitting in EQ Intake's review queue. Breakdown: 54 missing emergency contacts (low confidence — queue's own guidance is dismiss-only, collect via a future Cards prompt), 43 low-confidence trade guesses, 9 more staff duplicates, 11 more email gaps, 8 firmer trade guesses, 1 contact duplicate. Informational, surfaced while auditing the 16 already-committed rows. _(added 2026-07-06)_
- **eq-shell PR #681 needs review + merge** — fix is already live on ehow (applied directly ahead of the PR); the PR just brings the source-controlled migration back in sync. _(added 2026-07-06)_
_…and 53 more · [sks/pending.md](sks/pending.md)_

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-14 | [Merged + deployed the intake vendor-sync and the xlsx security fix](sessions/2026-07-14.md) |
| 2026-07-13 | [SKS plant & equipment restored after a manual asset-register wipe; 2FA grace unchanged](sessions/2026-07-13.md) |
| 2026-07-12 | [Shell→Field handoff: cookie mode retired, recurring Sentry issues cleared](sessions/2026-07-12.md) |
| 2026-07-12 | [Session — Substrate Plan v2 (the notebook that tells the truth)](sessions/2026-07-12-substrate-plan-v2.md) |
| 2026-07-11 | [CEO meeting prep for SKS Labour → Cards is the strategic standout](sessions/2026-07-11.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-14 10:30 UTC._
