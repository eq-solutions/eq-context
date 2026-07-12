---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-12
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-12 00:45 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-12 00:30 UTC → 2026-07-12 00:45 UTC)

- Merged: eq-shell [#770](https://github.com/eq-solutions/eq-shell/pull/770) fix(crm): add_site links the chosen site contact so it stick
- Merged: eq-shell [#750](https://github.com/eq-solutions/eq-shell/pull/750) fix(crm-write/entity-patch): 404 on zero-row / cross-tenant 
- Merged: eq-shell [#749](https://github.com/eq-solutions/eq-shell/pull/749) fix(invite-users-batch): await entitlement upsert so dropped
- Merged: eq-shell [#748](https://github.com/eq-solutions/eq-shell/pull/748) feat(comms): crew = the Field "Comms" team (retire the paral
- Merged: eq-shell [#746](https://github.com/eq-solutions/eq-shell/pull/746) chore(armada): set maxConcurrentBuilds=3 for parallel fleet 
- Merged: eq-shell [#745](https://github.com/eq-solutions/eq-shell/pull/745) fix(crm-write): narrow bare catch on link-table writes to mi
- Merged: eq-shell [#744](https://github.com/eq-solutions/eq-shell/pull/744) feat(comms): Move 5 — the comms crew (scope the grid + picke
- Merged: eq-shell [#743](https://github.com/eq-solutions/eq-shell/pull/743) fix(security): remove anon cross-tenant access on tender_enr

## ⚠ Needs you (1)

- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 4 | 6d |
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
| 2026-07-12 | eq-shell | [#770](https://github.com/eq-solutions/eq-shell/pull/770) fix(crm): add_site links the chosen site contact so it sticks wit |
| 2026-07-12 | eq-shell | [#769](https://github.com/eq-solutions/eq-shell/pull/769) fix(crm): normalise contact mobile to E.164 on every write path |
| 2026-07-12 | eq-shell | [#768](https://github.com/eq-solutions/eq-shell/pull/768) fix(field-iframe): retire cookie-mode handoff — token mode for ev |
| 2026-07-12 | eq-shell | [#765](https://github.com/eq-solutions/eq-shell/pull/765) feat(comms): bulk-import from Ops — tick boxes + select all |
| 2026-07-12 | eq-solves-service | [#499](https://github.com/eq-solutions/eq-service/pull/499) fix(scope): reconciliation to service-enabled sites; scope groupe |
| 2026-07-12 | eq-cards | [#149](https://github.com/eq-solutions/eq-cards/pull/149) feat(connections): smart re-apply cooldown after a decline |
| 2026-07-12 | eq-cards | [#148](https://github.com/eq-solutions/eq-cards/pull/148) fix(connections): dedup declined cards to latest per org |
| 2026-07-11 | eq-shell | [#764](https://github.com/eq-solutions/eq-shell/pull/764) feat(comms): custom columns + tick-list crew picker — more power  |
| 2026-07-11 | eq-shell | [#763](https://github.com/eq-solutions/eq-shell/pull/763) feat(comms): door polish — money across, Ops count, Melbourne PO  |
| 2026-07-11 | eq-shell | [#762](https://github.com/eq-solutions/eq-shell/pull/762) feat(comms): the Melbourne door — import the Working Job List wor |
| 2026-07-11 | eq-shell | [#761](https://github.com/eq-solutions/eq-shell/pull/761) fix(staff): E.164 phone normalisation on edit + carry #681 eq_upd |
| 2026-07-11 | eq-shell | [#760](https://github.com/eq-solutions/eq-shell/pull/760) feat(comms): the Ops door — import won EQ Ops jobs into the comms |
| 2026-07-11 | eq-shell | [#755](https://github.com/eq-solutions/eq-shell/pull/755) fix(field-iframe): cookie-mode handoff falls back to token mode o |
| 2026-07-11 | eq-shell | [#759](https://github.com/eq-solutions/eq-shell/pull/759) fix(comms): job table fits its width — no cut-off columns |
| 2026-07-11 | eq-shell | [#753](https://github.com/eq-solutions/eq-shell/pull/753) feat(staff): labour-hire agency + roster on/off toggle on the Sta |
_Showing 15 of 116 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-shell #758 — CI guard for invalid `netlify/functions` filenames** (fail on dotted/`*.test.ts` at the functions root, which silently breaks all deploys). Filed, not built. _(added 2026-07-12)_
- **Service-side SameSite gap** — SERVICE-9 `cookie_absent` is the Service twin of the Field cookie issue; Service already auths via token mode so it's residual canary noise, but worth confirming the canary can be muted/removed rather than left firing. _(added 2026-07-12)_
- **Plan saved 2026-07-11:** [`eq/field-eq-core-only-plan.md`](field-eq-core-only-plan.md). 3-phase, single-repo (eq-field). Decided: role-based supervision, **full strip**; keep `?tenant=demo` in-memory slug.
- **Cards perf — HELD (live signup traffic).** Safe wins queued: preload/preconnect the boot chain, defer PostHog to `flutter-first-frame`, defer Cropper.js. Big lever = Flutter deferred-imports / `--wasm` / static-first claim page (architectural — do NOT rush on live traffic). _(added 2026-07-11)_
- **Field structural cache lever (L-effort)** — fingerprint the ~40 non-hashed JS/CSS assets so the service worker can go cache-first (kills ~40 revalidation round-trips/boot). Higher-effort follow-up. _(added 2026-07-11)_
- **Residual "switching feels slow" = Shell-side pre-warm TIMING**, not per-app boot. With persistent hidden iframes each app boots ~once/session (pre-warm ~2.5 s) + on memory-saver re-mount — measure that if these boot cuts don't resolve the feel. _(added 2026-07-11)_
- **Arm/build the queued fleet bugs** — #736 (invite-users-batch entitlements), #737 (zero-row 404), #705 (eq-intake xlsx) armed, not yet built. #734 (quote-job-consumer) + #735 (RLS `(select)` wrapping) filed UNARMED — Royce's call to arm. _(added 2026-07-11)_
- **zaap tender tables are now service_role-only** (no `authenticated` tenant policies — the create migration's `field_authed_all_*` never reached zaap). Fine if the EQ app reads them via service_role; add the authenticated tenant policy if Field ever needs authed access there. _(added 2026-07-11)_
- **Ledger action item 3 — `2026_06_16_cards_claim_explicit_user_id.sql` must NEVER be re-applied** (documented in the ledger). A replay hazard, not a to-do; flagged so no future apply run picks it up. _(added 2026-07-11)_
- **Ledger action item 4 — cosmetic duplicate unique-index name on jvkn** (harmless, documented). Tidy only if convenient. _(added 2026-07-11)_
_…and 304 more · [eq/pending.md](eq/pending.md)_

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
_…and 34 more · [sks/pending.md](sks/pending.md)_

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-12 | [Shell→Field handoff: cookie mode retired, recurring Sentry issues cleared](sessions/2026-07-12.md) |
| 2026-07-11 | [CEO meeting prep for SKS Labour → Cards is the strategic standout](sessions/2026-07-11.md) |
| 2026-07-08 | [eq-shell: Brett Kilpatrick duplicate profile merged live + Cards-onboarding dedup root-caused and fixed](sessions/2026-07-08.md) |
| 2026-07-07 | [eq-cards: onboarding shipped live, approval-flow audit, offline ID card + install nudge](sessions/2026-07-07.md) |
| 2026-07-06 | [eq-shell: command palette + skeleton loading + optimistic archive shipped, live; unrelated drift fixed same session](sessions/2026-07-06.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-12 00:45 UTC._
