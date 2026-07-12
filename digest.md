---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-12
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-12 08:21 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-12 08:18 UTC → 2026-07-12 08:21 UTC)

- Merged: eq-shell [#763](https://github.com/eq-solutions/eq-shell/pull/763) feat(comms): door polish — money across, Ops count, Melbourn
- Merged: eq-shell [#761](https://github.com/eq-solutions/eq-shell/pull/761) fix(staff): E.164 phone normalisation on edit + carry #681 e
- Merged: eq-shell [#755](https://github.com/eq-solutions/eq-shell/pull/755) fix(field-iframe): cookie-mode handoff falls back to token m
- Merged: eq-shell [#753](https://github.com/eq-solutions/eq-shell/pull/753) feat(staff): labour-hire agency + roster on/off toggle on th
- Merged: eq-shell [#750](https://github.com/eq-solutions/eq-shell/pull/750) fix(crm-write/entity-patch): 404 on zero-row / cross-tenant 
- Merged: eq-shell [#749](https://github.com/eq-solutions/eq-shell/pull/749) fix(invite-users-batch): await entitlement upsert so dropped
- Merged: eq-shell [#748](https://github.com/eq-solutions/eq-shell/pull/748) feat(comms): crew = the Field "Comms" team (retire the paral
- Merged: eq-shell [#747](https://github.com/eq-solutions/eq-shell/pull/747) feat(comms): trim the fortnight view — this-week default + h

## ⚠ Needs you (2)

- 🟠 **PR aging 7d** — eq-shell [#658](https://github.com/eq-solutions/eq-shell/pull/658) "fix(dashboard): surface pending staff connections on home sidebar"
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 2 | 7d |
| eq-solves-service | ✓ success | 0d ago | 5 | 5d |
| eq-field | ✓ success | 0d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

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
| 2026-07-12 | eq-shell | [#751](https://github.com/eq-solutions/eq-shell/pull/751) fix(security): migrate eq-intake xlsx reader off vulnerable xlsx@ |
| 2026-07-12 | eq-shell | [#779](https://github.com/eq-solutions/eq-shell/pull/779) refactor(shell): consistent app names — one shared list, fix invi |
| 2026-07-12 | eq-shell | [#778](https://github.com/eq-solutions/eq-shell/pull/778) feat(canonical): DB-level AU phone normalisation trigger (0174) |
| 2026-07-12 | eq-shell | [#776](https://github.com/eq-solutions/eq-shell/pull/776) feat(quotes): job numbers are canonical — one name everywhere |
| 2026-07-12 | eq-shell | [#775](https://github.com/eq-solutions/eq-shell/pull/775) chore(quotes): remove retired Flask→canonical quote ETL |
| 2026-07-12 | eq-shell | [#777](https://github.com/eq-solutions/eq-shell/pull/777) feat(comms): job-list polish — sticky headers, skeleton, filter c |
| 2026-07-12 | eq-shell | [#774](https://github.com/eq-solutions/eq-shell/pull/774) feat(staff): drop onboarding middle names from the surname on ing |
| 2026-07-12 | eq-shell | [#771](https://github.com/eq-solutions/eq-shell/pull/771) feat(staff): birthday + start date on the staff record |
| 2026-07-12 | eq-shell | [#773](https://github.com/eq-solutions/eq-shell/pull/773) feat(staff): manager UI to define required tickets (minimum crede |
| 2026-07-12 | eq-shell | [#772](https://github.com/eq-solutions/eq-shell/pull/772) ci: guard against invalid netlify/functions filenames that break  |
| 2026-07-12 | eq-shell | [#770](https://github.com/eq-solutions/eq-shell/pull/770) fix(crm): add_site links the chosen site contact so it sticks wit |
| 2026-07-12 | eq-shell | [#769](https://github.com/eq-solutions/eq-shell/pull/769) fix(crm): normalise contact mobile to E.164 on every write path |
| 2026-07-12 | eq-shell | [#768](https://github.com/eq-solutions/eq-shell/pull/768) fix(field-iframe): retire cookie-mode handoff — token mode for ev |
| 2026-07-12 | eq-shell | [#765](https://github.com/eq-solutions/eq-shell/pull/765) feat(comms): bulk-import from Ops — tick boxes + select all |
| 2026-07-12 | eq-solves-service | [#513](https://github.com/eq-solutions/eq-service/pull/513) fix(assets): asset external_id unique per site, not per tenant (0 |
_Showing 15 of 118 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Android OTP autofill (WebOTP)** — SMS template binding line `@cards.eq.solutions #{{ .Code }}` NOW ADDED by Royce (2026-07-12); SMS confirmed carrying it. Android re-tested: the autofill chip did NOT fire — WebOTP needs the PAGE to call `navigator.credentials.get({otp})`, which Flutter/CanvasKit doesn't do out of the box, so the SMS line is necessary-but-not-sufficient. Remaining = a JS shim (read the code → inject into the OTP field; the CanvasKit injection is the fiddly + auth-critical part) + Android device re-test. **PARKED** (Royce: "probably not end of the world") — pick up only if Android login friction becomes a real complaint; the SMS line is already in place for a quick pickup. _(updated 2026-07-12)_
- **59 SKS staff_id-without-membership** — 53 are unclaimed roster (no login yet — normal backlog); rest logged-in-never-connected or declined. No action unless they surface. _(added 2026-07-12)_
- **Post-merge cleanup:** drop the `eq_set_workbench_job_no` wrapper once no caller remains — the last trace of the word. _(added 2026-07-12)_
- **Optional (declined for now):** rename GM `job_code` → `job_number` across the 3 GM tables (+ unique constraints, parser, UI) for strict one-name-in-the-schema. _(added 2026-07-12)_
- **"Damon Patrick Francis"** — title-case, so the middle-name rule correctly left it alone. Confirm whether "Patrick" is a middle name → should be "Damon Francis" (one-row manual fix). _(added 2026-07-12)_
- **Records↔Field seam polish (discussed, not built)** — steelmanned the "one record, many windows" model; creative next steps proposed: (1) a declarative field-ownership registry to kill the ~10-edit-site tax per new field, (2) push phone/name normalisation into a Postgres BEFORE trigger (one definition, every writer, no app duplication), (3) a "Records health" panel reusing `eq_quality_runs` (non-E.164 phones, embedded middles, missing canonical link, orphaned workers) with one-click fixes, (4) Cards as the real front door + canonical↔tenant reconciliation/merge-review to kill dup stubs, (5) extend the pattern to CRM contacts + fix the "Contacts" vocabulary clash. Recommended first move: the DB-level normalise trigger (highest leverage, lowest risk). _(added 2026-07-12)_
- **Service-side SameSite gap** — SERVICE-9 `cookie_absent` is the Service twin of the Field cookie issue; Service already auths via token mode so it's residual canary noise, but worth confirming the canary can be muted/removed rather than left firing. _(added 2026-07-12)_
- **Plan saved 2026-07-11:** [`eq/field-eq-core-only-plan.md`](field-eq-core-only-plan.md). 3-phase, single-repo (eq-field). Decided: role-based supervision, **full strip**; keep `?tenant=demo` in-memory slug.
- **Phase 2 (now UNBLOCKED — handoff confirmed live):** extend the `sks` Core-only lock in `checkAccess()` to `eq` + drop the `STAFF_CODE=demo`/`MANAGER_CODE=demo1234` backdoor (still a live fallback if the handoff ever fails). Then Phase 3: strip the dead server PIN code. Safe to proceed now the door works. _(added 2026-07-12)_
- **Security hygiene (chip `task_ed725611`):** several EQ Netlify env vars are `is_secret=false` so full values leak via the API — incl. a **GCP service-account private key** (`GOOGLE_DOC_AI_CREDENTIALS`) + JWT/handoff secrets on eq-shell, and `SKS_JWT_SECRET`/`EQ_FIELD_HANDOFF_KEY`/`RESEND_API_KEY` on eq-field. Flip to secret; consider rotating the exposed GCP key. _(added 2026-07-12)_
_…and 311 more · [eq/pending.md](eq/pending.md)_

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
_…and 44 more · [sks/pending.md](sks/pending.md)_

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-12 | [Shell→Field handoff: cookie mode retired, recurring Sentry issues cleared](sessions/2026-07-12.md) |
| 2026-07-12 | [Session — Substrate Plan v2 (the notebook that tells the truth)](sessions/2026-07-12-substrate-plan-v2.md) |
| 2026-07-11 | [CEO meeting prep for SKS Labour → Cards is the strategic standout](sessions/2026-07-11.md) |
| 2026-07-11 | [The read path lied, and NSW isn't finishing work](sessions/2026-07-11-substrate-delivery-and-nsw-audit.md) |
| 2026-07-08 | [eq-shell: Brett Kilpatrick duplicate profile merged live + Cards-onboarding dedup root-caused and fixed](sessions/2026-07-08.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-12 08:21 UTC._
