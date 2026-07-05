---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-05
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-05 08:46 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-05 08:10 UTC → 2026-07-05 08:46 UTC)

- Merged: eq-shell [#665](https://github.com/eq-solutions/eq-shell/pull/665) fix(branding): bound logo colour-detection with a load timeo
- Merged: eq-shell [#663](https://github.com/eq-solutions/eq-shell/pull/663) feat(ops): labour hire rates — canonical tables + read-only 
- Merged: eq-shell [#644](https://github.com/eq-solutions/eq-shell/pull/644) refactor(branding): one canonical copy in organisations.bran
- Merged: eq-shell [#643](https://github.com/eq-solutions/eq-shell/pull/643) feat(branding): self-serve tenant document branding editor
- Merged: eq-shell [#627](https://github.com/eq-solutions/eq-shell/pull/627) fix(provisioning): convert provision-tenant to a background 
- Merged: eq-shell [#626](https://github.com/eq-solutions/eq-shell/pull/626) fix(admin): resolve --eq-ink to a real hex value for the wor
- Merged: eq-shell [#625](https://github.com/eq-solutions/eq-shell/pull/625) feat(security): view security_invoker invariant (CHECK 7) + 
- Merged: eq-shell [#624](https://github.com/eq-solutions/eq-shell/pull/624) fix(provisioning): tenant_routing NOT NULL columns block eve

## ⚠ Needs you (4)

- 🟠 **Sentry new error** — `eq-shell` [Error: events GET 500: internal_error](https://eq-solutions.sentry.io/issues/132197414/)
- 🟠 **Sentry new error** — `eq-cards` [provisionTenantExchange: unexpected HTTP 500](https://eq-solutions.sentry.io/issues/132064194/)
- 🟠 **Sentry new error** — `eq-field` [Error: 400: {"code":"23502","details":null,"hint":null,"mess](https://eq-solutions.sentry.io/issues/131921038/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 5 | 1d |
| eq-solves-service | ✓ success | 0d ago | 1 | 0d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 1d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: events GET 500: internal_error](https://eq-solutions.sentry.io/issues/132197414/) | 1 | 2026-07-04 |
| eq-cards | [provisionTenantExchange: unexpected HTTP 500](https://eq-solutions.sentry.io/issues/132064194/) | 1 | 2026-07-03 |
| eq-field | [Error: 400: {"code":"23502","details":null,"hint":null,"message":"null value in ](https://eq-solutions.sentry.io/issues/131921038/) | 1 | 2026-07-03 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-05 | eq-shell | [#663](https://github.com/eq-solutions/eq-shell/pull/663) feat(ops): labour hire rates — canonical tables + read-only tab |
| 2026-07-05 | eq-shell | [#665](https://github.com/eq-solutions/eq-shell/pull/665) fix(branding): bound logo colour-detection with a load timeout |
| 2026-07-05 | eq-shell | [#664](https://github.com/eq-solutions/eq-shell/pull/664) feat(roles): bump eq-roles to v2.4.0, wire subcontractor everywhe |
| 2026-07-05 | eq-shell | [#662](https://github.com/eq-solutions/eq-shell/pull/662) feat(roles): expose subcontractor as a selectable role (safe subs |
| 2026-07-05 | eq-shell | [#661](https://github.com/eq-solutions/eq-shell/pull/661) feat(branding): one logo + auto-PNG for docs + logo colour detect |
| 2026-07-05 | eq-shell | [#660](https://github.com/eq-solutions/eq-shell/pull/660) fix(staff): decline a worker-initiated application actually persi |
| 2026-07-05 | eq-shell | [#659](https://github.com/eq-solutions/eq-shell/pull/659) fix(entitlements): qualify ambiguous `id` in eq_update_tenant_set |
| 2026-07-05 | eq-shell | [#657](https://github.com/eq-solutions/eq-shell/pull/657) feat(tenants): link to EQ Cards adoption dashboard (PostHog) |
| 2026-07-05 | eq-shell | [#656](https://github.com/eq-solutions/eq-shell/pull/656) fix(provisioning): expose app_data schema over PostgREST for new  |
| 2026-07-05 | eq-solves-service | [#441](https://github.com/eq-solutions/eq-service/pull/441) fix(analytics): filter React #418 hydration noise from error_thro |
| 2026-07-05 | eq-field | [#408](https://github.com/eq-solutions/eq-field/pull/408) v3.5.241 — job numbers: fetch on tab-open (fixes permanently-empt |
| 2026-07-05 | eq-field | [#407](https://github.com/eq-solutions/eq-field/pull/407) docs: correct stale tenant references (eq→zaap, ktmj deleted, dem |
| 2026-07-05 | eq-cards | [#121](https://github.com/eq-solutions/eq-cards/pull/121) fix(sentry): surface real provision error, drop unactionable brow |
| 2026-07-04 | eq-shell | [#653](https://github.com/eq-solutions/eq-shell/pull/653) chore(drift): allow-list field_job_numbers (security_invoker view |
| 2026-07-04 | eq-shell | [#651](https://github.com/eq-solutions/eq-shell/pull/651) 0160: eq_merge_sites RPC — governed site-dedup (QA row 29 follow- |
_Showing 15 of 123 · full record in [sessions/](sessions/)_

## Pending (EQ)

- Add a hydration-error pattern (e.g. `Hydration failed|mismatch|missing attribute`) to `NOISE_PATTERNS` in `eq-solves-service/app/providers.tsx` to quiet the (confirmed non-blocking) `error_thrown` noise. _(added 2026-07-05)_
- eq-cards branch `claude/blissful-wing-44892b` (commit `0ce536c`, the Sentry real-error-surfacing + noise-filter fix) is committed but not yet pushed/PR'd/merged. _(added 2026-07-05)_
- **field_job_numbers provenance** — the view was created out-of-band (not originally in a repo migration); who made it + whether other planes need it tracked as `task_0467f68c`. _(added 2026-07-04)_
- **Favour Perfect first-run config** — switch into it (after one workspace-switch or re-login), configure it, and invite its real customer admin from inside `/favour-perfect/admin/users`. _(added 2026-07-04, needs your call)_
- **Optional: `reconcile_ledger` tidy for `favour-perfect`** — its `_eq_migrations` ledger has 204 rows incl. 39 null-checksum entries (cruft from a messy apply sequence: an 08:14 reconcile-path run stamped rows then failed; the 08:25 apply finished it). Schema is correct — purely cosmetic. A `reconcile_ledger=true` dispatch scoped to `favour-perfect` would tidy it. _(added 2026-07-04, needs your call)_
- **Admin-create zero-member gap** — admin "Add tenant" builds member-less, UI-unreachable tenants (no way to add a first user without a hand-inserted membership). Fix (auto-add creator as manager, or an "Add me as admin" button) running as `task_4f5989fb`. _(added 2026-07-04)_
- **Link the 19 field-enabled SKS sites with no `customer_id`** — Row 29 prestart prefill resolves the customer name only for the 11 (of 30) field-visible ehow sites that have a `customer_id`. The other 19 (Amazon SYD53, Woolworths, Microsoft SYD05/27, Western Sydney Airport, St Vincents, etc.) prefill blank. NOT auto-derivable — `sites.client_name`/`external_customer_id` are null/junk, zero name-matches to `customers.company_name`. Needs a manual ops pass (assign each site its customer in the Customers/Sites editor). Degrades gracefully (blank field) until done. _(added 2026-07-04, needs your call)_
- **Occasional deep game-day (rare, human)** — restore **auth data** into a real Supabase target (the dump excludes the managed auth *schema*, so auth rows only load where Supabase provisions it) + app-repoint smoke test. Not automatable cheaply; do when convenient. _(carried 2026-07-04)_
- **Rows 4 & 8 — resolved by verification, reopen only if they recur** — row 4 (duplicate "From Roster"): structurally only one button exists (the "twice" was the button + a muted-cell "from roster" label); row 8 (`?tab=person-wizard` blank): moot on SKS now that Add Person is hidden. Need a screenshot/repro to reopen either. _(added 2026-07-04)_
- **Visual SKS click-through** of the Job Numbers screen (OPS badge on Ops rows, manual-add still works) — needs a live `?tenant=sks#sh=` Shell session (can't mint headless). DB + routing verified. _(added 2026-07-04)_
_…and 231 more · [eq/pending.md](eq/pending.md)_

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
| 2026-07-05 | [eq-shell Sentry triage: tenant PostgREST exposure gap root-caused + fixed live](sessions/2026-07-05.md) |
| 2026-07-05 | [Session — Role Step-Up Charters + generator](sessions/2026-07-05-role-step-up-charters.md) |
| 2026-07-04 | [eq-shell worktree hygiene: stale checkout diagnosed and restored](sessions/2026-07-04.md) |
| 2026-07-03 | [eq-shell: batch site delete/archive built (PR #613 open, merge blocked)](sessions/2026-07-03.md) |
| 2026-07-02 | [Token lint ratchet merged; staff licence resync endpoint shipped](sessions/2026-07-02.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-05 08:46 UTC._
