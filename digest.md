---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-13
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-13 01:31 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-13 00:31 UTC → 2026-07-13 01:31 UTC)

- Merged: eq-shell [#802](https://github.com/eq-solutions/eq-shell/pull/802) fix(labour-hire): modal focus loss + wide weekly-cost table 
- Merged: eq-shell [#778](https://github.com/eq-solutions/eq-shell/pull/778) feat(canonical): DB-level AU phone normalisation trigger (01
- Merged: eq-shell [#775](https://github.com/eq-solutions/eq-shell/pull/775) chore(quotes): remove retired Flask→canonical quote ETL
- Merged: eq-shell [#774](https://github.com/eq-solutions/eq-shell/pull/774) feat(staff): drop onboarding middle names from the surname o
- Merged: eq-shell [#773](https://github.com/eq-solutions/eq-shell/pull/773) feat(staff): manager UI to define required tickets (minimum 
- Merged: eq-shell [#771](https://github.com/eq-solutions/eq-shell/pull/771) feat(staff): birthday + start date on the staff record
- Merged: eq-shell [#769](https://github.com/eq-solutions/eq-shell/pull/769) fix(crm): normalise contact mobile to E.164 on every write p
- Merged: eq-shell [#765](https://github.com/eq-solutions/eq-shell/pull/765) feat(comms): bulk-import from Ops — tick boxes + select all

## ⚠ Needs you (2)

- 🟠 **PR aging 7d** — eq-shell [#658](https://github.com/eq-solutions/eq-shell/pull/658) "fix(dashboard): surface pending staff connections on home sidebar"
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 2 | 7d |
| eq-solves-service | ✓ success | 0d ago | 5 | 6d |
| eq-field | ✓ success | 0d ago | 2 | 0d |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-solves-service | [auth handoff: cookie_absent](https://eq-solutions.sentry.io/issues/132832684/) | 19 | 2026-07-08 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/132643934/) | 2 | 2026-07-07 |
| eq-solves-service | [Error: COALESCE types uuid and text cannot be matched](https://eq-solutions.sentry.io/issues/132618557/) | 1 | 2026-07-07 |
| eq-shell | [Error: HTTP 400](https://eq-solutions.sentry.io/issues/132270381/) | 1 | 2026-07-05 |
| eq-cards | [provisionTenantExchange: unexpected HTTP 500](https://eq-solutions.sentry.io/issues/132064194/) | 1 | 2026-07-03 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-13 | eq-shell | [#802](https://github.com/eq-solutions/eq-shell/pull/802) fix(labour-hire): modal focus loss + wide weekly-cost table + tol |
| 2026-07-13 | eq-shell | [#801](https://github.com/eq-solutions/eq-shell/pull/801) feat(labour-hire): Redundancy in the weekly cost + agency/rate-ty |
| 2026-07-12 | eq-shell | [#799](https://github.com/eq-solutions/eq-shell/pull/799) feat(labour-hire): add 'week' rate unit for once-a-week charges ( |
| 2026-07-12 | eq-shell | [#800](https://github.com/eq-solutions/eq-shell/pull/800) fix(auth): create auth.users before shell user on invite accept |
| 2026-07-12 | eq-shell | [#792](https://github.com/eq-solutions/eq-shell/pull/792) feat(comms): crew-gaps strip — where the labour issues are, by si |
| 2026-07-12 | eq-shell | [#791](https://github.com/eq-solutions/eq-shell/pull/791) fix(comms): job list fills the window + job numbers never truncat |
| 2026-07-12 | eq-shell | [#790](https://github.com/eq-solutions/eq-shell/pull/790) fix(security): protect plant_equipment from customer-asset import |
| 2026-07-12 | eq-shell | [#787](https://github.com/eq-solutions/eq-shell/pull/787) fix(security): scope anon's read of public.organisations to safe  |
| 2026-07-12 | eq-shell | [#788](https://github.com/eq-solutions/eq-shell/pull/788) fix(comms): make the job list readable — wrap Work, wider page, f |
| 2026-07-12 | eq-shell | [#786](https://github.com/eq-solutions/eq-shell/pull/786) fix(security): revoke anon write grants on jvkn control-plane tab |
| 2026-07-12 | eq-shell | [#785](https://github.com/eq-solutions/eq-shell/pull/785) feat(comms): Excel-style inline editing on the job list + KPI-til |
| 2026-07-12 | eq-shell | [#782](https://github.com/eq-solutions/eq-shell/pull/782) feat(canonical): one-active-staff-per-person lock (0175) |
| 2026-07-12 | eq-shell | [#783](https://github.com/eq-solutions/eq-shell/pull/783) ci: wire the check:css coverage gate into the PR gate |
| 2026-07-12 | eq-shell | [#780](https://github.com/eq-solutions/eq-shell/pull/780) ci: wire the check:perms permission-matrix drift guard into the P |
| 2026-07-12 | eq-shell | [#751](https://github.com/eq-solutions/eq-shell/pull/751) fix(security): migrate eq-intake xlsx reader off vulnerable xlsx@ |
_Showing 15 of 118 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **No sourcemaps uploaded for eq-shell** (`@sentry/vite-plugin`/`sentry-cli` absent from the build) — Sentry events are exactly as minified as the console, so it isn't a shortcut here. Optional follow-up if prod JS errors keep needing manual decode: wire up sourcemap upload in its own PR. _(added 2026-07-12)_
- **Rotate the jvkn (eq-canonical) service_role key** — pasted into chat this session to fix canon-read. Roll it (Supabase → jvkn → API), update everywhere used; same class as the EQ_SECRET_SALT-in-chat rotation item. _(added 2026-07-12)_
- **Field gate PIN inputs not wrapped in a `<form>`** — browser "password field is not contained in a form" warning ×5; password-manager UX nit. Low priority. _(added 2026-07-12)_
- **Timesheet "(unknown)" staff-map load-order race (v3.5.219)** — pre-existing; a timesheet row can render a beat before the canonical staff map is ready (verified 0 orphaned timesheets, data intact). Self-heals on re-render; fix only if it becomes visibly annoying. _(added 2026-07-12)_
- **`project_targets` (supabase.js:1765)** also calls `sbFetchAll` without `orderBy` — left as-is; normal entity table that should have an `id`. Verify if paranoid. _(added 2026-07-12)_
- **Android OTP autofill (WebOTP)** — SMS template binding line `@cards.eq.solutions #{{ .Code }}` NOW ADDED by Royce (2026-07-12); SMS confirmed carrying it. Android re-tested: the autofill chip did NOT fire — WebOTP needs the PAGE to call `navigator.credentials.get({otp})`, which Flutter/CanvasKit doesn't do out of the box, so the SMS line is necessary-but-not-sufficient. Remaining = a JS shim (read the code → inject into the OTP field; the CanvasKit injection is the fiddly + auth-critical part) + Android device re-test. **PARKED** (Royce: "probably not end of the world") — pick up only if Android login friction becomes a real complaint; the SMS line is already in place for a quick pickup. _(updated 2026-07-12)_
- **59 SKS staff_id-without-membership** — 53 are unclaimed roster (no login yet — normal backlog); rest logged-in-never-connected or declined. No action unless they surface. _(added 2026-07-12)_
- **Post-merge cleanup:** drop the `eq_set_workbench_job_no` wrapper once no caller remains — the last trace of the word. _(added 2026-07-12)_
- **Optional (declined for now):** rename GM `job_code` → `job_number` across the 3 GM tables (+ unique constraints, parser, UI) for strict one-name-in-the-schema. _(added 2026-07-12)_
- **"Damon Patrick Francis"** — title-case, so the middle-name rule correctly left it alone. Confirm whether "Patrick" is a middle name → should be "Damon Francis" (one-row manual fix). _(added 2026-07-12)_
_…and 316 more · [eq/pending.md](eq/pending.md)_

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
_…and 50 more · [sks/pending.md](sks/pending.md)_

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-13 | [SKS plant & equipment restored after a manual asset-register wipe; 2FA grace unchanged](sessions/2026-07-13.md) |
| 2026-07-12 | [Shell→Field handoff: cookie mode retired, recurring Sentry issues cleared](sessions/2026-07-12.md) |
| 2026-07-12 | [Session — Substrate Plan v2 (the notebook that tells the truth)](sessions/2026-07-12-substrate-plan-v2.md) |
| 2026-07-11 | [CEO meeting prep for SKS Labour → Cards is the strategic standout](sessions/2026-07-11.md) |
| 2026-07-11 | [The read path lied, and NSW isn't finishing work](sessions/2026-07-11-substrate-delivery-and-nsw-audit.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-13 01:31 UTC._
