---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-05
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-05 19:15 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-05 19:12 UTC → 2026-07-05 19:15 UTC)

- Merged: eq-shell [#652](https://github.com/eq-solutions/eq-shell/pull/652) 0161: reassert security_invoker on app_data.field_job_number
- Merged: eq-shell [#650](https://github.com/eq-solutions/eq-shell/pull/650) feat(entitlements): writers → canonical + drop legacy (Phase
- Merged: eq-shell [#648](https://github.com/eq-solutions/eq-shell/pull/648) feat(entitlements): app tiles → canonical, Stage A (readers)
- Merged: eq-shell [#647](https://github.com/eq-solutions/eq-shell/pull/647) fix(tenants): auto-join creating admin so new tenants are re
- Merged: eq-shell [#645](https://github.com/eq-solutions/eq-shell/pull/645) feat(field): surface customer name on field_sites + drop dea
- Merged: eq-shell [#634](https://github.com/eq-solutions/eq-shell/pull/634) fix(sync-quotes-nightly): check errors on Flask write-back +
- Merged: eq-shell [#633](https://github.com/eq-solutions/eq-shell/pull/633) docs: correct CLAUDE.md — EQ_SECRET_SALT is the fallback sig
- Merged: eq-shell [#627](https://github.com/eq-solutions/eq-shell/pull/627) fix(provisioning): convert provision-tenant to a background 

## ⚠ Needs you (4)

- 🟠 **Sentry new error** — `eq-field` [ReferenceError: isLeave is not defined](https://eq-solutions.sentry.io/issues/132270778/)
- 🟠 **Sentry new error** — `eq-shell` [Error: HTTP 400](https://eq-solutions.sentry.io/issues/132270381/)
- 🟠 **Sentry new error** — `eq-shell` [Error: events GET 500: internal_error](https://eq-solutions.sentry.io/issues/132197414/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 4 | 1d |
| eq-solves-service | ✓ success | 0d ago | 0 | — |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-field | [ReferenceError: isLeave is not defined](https://eq-solutions.sentry.io/issues/132270778/) | 1 | 2026-07-05 |
| eq-shell | [Error: HTTP 400](https://eq-solutions.sentry.io/issues/132270381/) | 1 | 2026-07-05 |
| eq-shell | [Error: events GET 500: internal_error](https://eq-solutions.sentry.io/issues/132197414/) | 1 | 2026-07-04 |
| eq-cards | [provisionTenantExchange: unexpected HTTP 500](https://eq-solutions.sentry.io/issues/132064194/) | 1 | 2026-07-03 |
| eq-field | [Error: 400: {"code":"23502","details":null,"hint":null,"message":"null value in ](https://eq-solutions.sentry.io/issues/131921038/) | 1 | 2026-07-03 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-05 | eq-shell | [#671](https://github.com/eq-solutions/eq-shell/pull/671) feat(ops): labour hire rates — PDF import + weekly-cost Fares tid |
| 2026-07-05 | eq-shell | [#670](https://github.com/eq-solutions/eq-shell/pull/670) feat(ops): labour hire rates — weekly-cost rollup |
| 2026-07-05 | eq-shell | [#669](https://github.com/eq-solutions/eq-shell/pull/669) feat(field): job-number retire — auto (invoiced) + manual (hide-o |
| 2026-07-05 | eq-shell | [#666](https://github.com/eq-solutions/eq-shell/pull/666) feat(branding): live preview + contrast warnings + detection & sa |
| 2026-07-05 | eq-shell | [#668](https://github.com/eq-solutions/eq-shell/pull/668) chore(drift): allow-list labour_hire_rates_view (security_invoker |
| 2026-07-05 | eq-shell | [#663](https://github.com/eq-solutions/eq-shell/pull/663) feat(ops): labour hire rates — canonical tables + read-only tab |
| 2026-07-05 | eq-shell | [#665](https://github.com/eq-solutions/eq-shell/pull/665) fix(branding): bound logo colour-detection with a load timeout |
| 2026-07-05 | eq-shell | [#664](https://github.com/eq-solutions/eq-shell/pull/664) feat(roles): bump eq-roles to v2.4.0, wire subcontractor everywhe |
| 2026-07-05 | eq-shell | [#662](https://github.com/eq-solutions/eq-shell/pull/662) feat(roles): expose subcontractor as a selectable role (safe subs |
| 2026-07-05 | eq-shell | [#661](https://github.com/eq-solutions/eq-shell/pull/661) feat(branding): one logo + auto-PNG for docs + logo colour detect |
| 2026-07-05 | eq-shell | [#660](https://github.com/eq-solutions/eq-shell/pull/660) fix(staff): decline a worker-initiated application actually persi |
| 2026-07-05 | eq-shell | [#659](https://github.com/eq-solutions/eq-shell/pull/659) fix(entitlements): qualify ambiguous `id` in eq_update_tenant_set |
| 2026-07-05 | eq-shell | [#657](https://github.com/eq-solutions/eq-shell/pull/657) feat(tenants): link to EQ Cards adoption dashboard (PostHog) |
| 2026-07-05 | eq-shell | [#656](https://github.com/eq-solutions/eq-shell/pull/656) fix(provisioning): expose app_data schema over PostgREST for new  |
| 2026-07-05 | eq-solves-service | [#444](https://github.com/eq-solutions/eq-service/pull/444) feat(commercials): asset reconciliation screen for contract-scope |
_Showing 15 of 124 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Duplicate `job_plans` row, SKS tenant** — `name='E1.25'`, `code='LVACB'` has two active rows: one real (`09b028b9-...`, created 2026-04-08) and one stray seed row with a fixture-pattern id (`e0000000-0000-0000-0000-000000000001`, created 2026-04-12, slightly different `type` string). The asset-count fix sums across both ids as a stopgap; the duplicate itself needs Royce's call (delete vs merge) before any cleanup migration. _(added 2026-07-06)_
- **Commercial-sheet → create-assets feature** (`docs/proposals/commercial-sheet-asset-import.md` in eq-solves-service) — brief only, not started. Sheet has counts not identities, so any build creates placeholder stubs, not real imports. Option B (opt-in "create N stub assets for the gap" checkbox) recommended. Needs Royce's shape pick (A/B/C) before any build. _(added 2026-07-05)_
- **Confirm PDF extraction accuracy** on the first real upload — mechanism is the proven quote parser, but accuracy on these matrix rate-cards / role-in-description invoices is unverified headless. Upload a sample PDF; the review table shows exactly what Claude got before anything commits. _(added 2026-07-05)_
- **field_job_numbers provenance** — the view was created out-of-band (not originally in a repo migration); who made it + whether other planes need it tracked as `task_0467f68c`. _(added 2026-07-04)_
- **Favour Perfect first-run config** — switch into it (after one workspace-switch or re-login), configure it, and invite its real customer admin from inside `/favour-perfect/admin/users`. _(added 2026-07-04, needs your call)_
- **Optional: `reconcile_ledger` tidy for `favour-perfect`** — its `_eq_migrations` ledger has 204 rows incl. 39 null-checksum entries (cruft from a messy apply sequence: an 08:14 reconcile-path run stamped rows then failed; the 08:25 apply finished it). Schema is correct — purely cosmetic. A `reconcile_ledger=true` dispatch scoped to `favour-perfect` would tidy it. _(added 2026-07-04, needs your call)_
- **Admin-create zero-member gap** — admin "Add tenant" builds member-less, UI-unreachable tenants (no way to add a first user without a hand-inserted membership). Fix (auto-add creator as manager, or an "Add me as admin" button) running as `task_4f5989fb`. _(added 2026-07-04)_
- **Link the 19 field-enabled SKS sites with no `customer_id`** — Row 29 prestart prefill resolves the customer name only for the 11 (of 30) field-visible ehow sites that have a `customer_id`. The other 19 (Amazon SYD53, Woolworths, Microsoft SYD05/27, Western Sydney Airport, St Vincents, etc.) prefill blank. NOT auto-derivable — `sites.client_name`/`external_customer_id` are null/junk, zero name-matches to `customers.company_name`. Needs a manual ops pass (assign each site its customer in the Customers/Sites editor). Degrades gracefully (blank field) until done. _(added 2026-07-04, needs your call)_
- **Occasional deep game-day (rare, human)** — restore **auth data** into a real Supabase target (the dump excludes the managed auth *schema*, so auth rows only load where Supabase provisions it) + app-repoint smoke test. Not automatable cheaply; do when convenient. _(carried 2026-07-04)_
- **Rows 4 & 8 — resolved by verification, reopen only if they recur** — row 4 (duplicate "From Roster"): structurally only one button exists (the "twice" was the button + a muted-cell "from roster" label); row 8 (`?tab=person-wizard` blank): moot on SKS now that Add Person is hidden. Need a screenshot/repro to reopen either. _(added 2026-07-04)_
_…and 230 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date. **PIN audit 2026-07-05 (Royce-confirmed):** this repo has its own independent login/PIN system, still actively used — a completely different codebase from eq-field, not affected by eq-field's own PIN-gate retirement below.
- **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
- **SKS anon-remediation (nspb)** — exact policy worklist in `cross-app-linkage-remediation-plan-2026-06-07.md` §7a. Separate from ehow work. SKS-live gated.
- **eq-shell** — ~~converge `c2-shell-roles` + `sks-field-host` branches~~ — `c2-shell-roles` no longer exists in eq-shell repo (deleted). Re-assess: verify whether the security-groups work from `sks-live-sprint-2026-06-07.md` Prompt A was folded into main or abandoned before reopening this track.
- **Security groups Phase 2–5** — wire group perms into session, `AdminSecurityGroups` page, first real `user_security_groups` row for a SKS user.
- Person-wizard renders blank content specifically on a cold `?tab=person-wizard` deep-link boot (normal in-app "Add Person" nav works fine) — root cause not found despite exhaustive code trace + live Sentry/entitlement checks; needs Royce's own DevTools session with the Field-iframe console context selected _(added 2026-07-03)_
- At least one SKS person ("Collin ... Toohey") has no record in canonical `app_data.staff`, blocking their leave submissions — data-ops backfill needed, not a code fix _(added 2026-07-03)_
- Royce to independently click-through-confirm the Weekends toggle, roster names, and both safety forms live (smoke-tested remotely, not yet confirmed by Royce beyond the original repros) _(added 2026-07-03)_
- **Reverse-angle gap (independent read-only pass 2026-07-05):** 9 legacy `people` rows have a canonical twin already but `people.canonical_id` is still NULL — matched live by phone+email vs jvkn `workers`: Louisa Cardinale, Matthew Khreich, Andre de Biasi, Damon Francis, Timothy Chapman, Bruno Pedrosa, Eric Nguyen (phone-only), Liam Holmgreen, Sam Powell. Back-link write not yet run; handed to the concurrent console actioning this batch (Royce copy-pasted the id list). Low-risk `UPDATE people SET canonical_id=… WHERE id=…` on nspb _(added 2026-07-05)_
- First **Cards→Field approval for SKS never run** — `cards_field_approvals` has 79 rows across other tenants, **0 for SKS**. When the first SKS worker signs up to Cards + applies, exercise the admin approve + licence-verify path end-to-end (machinery proven elsewhere, unproven for this tenant) _(added 2026-07-04)_
_…and 24 more · [sks/pending.md](sks/pending.md)_

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-06 | [Labour hire rates: PDF import + supersede shipped; feature complete & live](sessions/2026-07-06.md) |
| 2026-07-05 | [eq-shell Sentry triage: tenant PostgREST exposure gap root-caused + fixed live](sessions/2026-07-05.md) |
| 2026-07-05 | [Session — Role Step-Up Charters + generator](sessions/2026-07-05-role-step-up-charters.md) |
| 2026-07-05 | [Session — Labour Hire Rates (canonical design + staged lean build)](sessions/2026-07-05-labour-hire-rates.md) |
| 2026-07-04 | [eq-shell worktree hygiene: stale checkout diagnosed and restored](sessions/2026-07-04.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-05 19:15 UTC._
