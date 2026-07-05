---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-05
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-05 07:46 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-05 07:27 UTC → 2026-07-05 07:46 UTC)

- Merged: eq-shell [#661](https://github.com/eq-solutions/eq-shell/pull/661) feat(branding): one logo + auto-PNG for docs + logo colour d
- Merged: eq-shell [#642](https://github.com/eq-solutions/eq-shell/pull/642) Tenants page: permanently delete an archived tenant
- Merged: eq-shell [#641](https://github.com/eq-solutions/eq-shell/pull/641) fix: clear a stuck data-plane provisioning job from the Tena
- Merged: eq-shell [#638](https://github.com/eq-solutions/eq-shell/pull/638) fix(provisioning): shell_control.provision_tenant never actu
- Merged: eq-shell [#634](https://github.com/eq-solutions/eq-shell/pull/634) fix(sync-quotes-nightly): check errors on Flask write-back +
- Merged: eq-shell [#633](https://github.com/eq-solutions/eq-shell/pull/633) docs: correct CLAUDE.md — EQ_SECRET_SALT is the fallback sig
- Merged: eq-shell [#621](https://github.com/eq-solutions/eq-shell/pull/621) fix(ops): remove broken per-column Status filter in table vi
- Merged: eq-shell [#620](https://github.com/eq-solutions/eq-shell/pull/620) fix(ci): check-migration-hygiene.mjs skips SQL line comments

## ⚠ Needs you (4)

- 🟠 **Sentry new error** — `eq-shell` [Error: events GET 500: internal_error](https://eq-solutions.sentry.io/issues/132197414/)
- 🟠 **Sentry new error** — `eq-cards` [provisionTenantExchange: unexpected HTTP 500](https://eq-solutions.sentry.io/issues/132064194/)
- 🟠 **Sentry new error** — `eq-field` [Error: 400: {"code":"23502","details":null,"hint":null,"mess](https://eq-solutions.sentry.io/issues/131921038/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 4 | 1d |
| eq-solves-service | ✓ success | 0d ago | 0 | — |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 1d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: events GET 500: internal_error](https://eq-solutions.sentry.io/issues/132197414/) | 1 | 2026-07-04 |
| eq-cards | [provisionTenantExchange: unexpected HTTP 500](https://eq-solutions.sentry.io/issues/132064194/) | 1 | 2026-07-03 |
| eq-field | [Error: 400: {"code":"23502","details":null,"hint":null,"message":"null value in ](https://eq-solutions.sentry.io/issues/131921038/) | 1 | 2026-07-03 |
| eq-cards | [: Unable to load asset: "NOTICES".](https://eq-solutions.sentry.io/issues/131717362/) | 1 | 2026-07-02 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/131636027/) | 1 | 2026-07-02 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-05 | eq-shell | [#661](https://github.com/eq-solutions/eq-shell/pull/661) feat(branding): one logo + auto-PNG for docs + logo colour detect |
| 2026-07-05 | eq-shell | [#660](https://github.com/eq-solutions/eq-shell/pull/660) fix(staff): decline a worker-initiated application actually persi |
| 2026-07-05 | eq-shell | [#659](https://github.com/eq-solutions/eq-shell/pull/659) fix(entitlements): qualify ambiguous `id` in eq_update_tenant_set |
| 2026-07-05 | eq-shell | [#657](https://github.com/eq-solutions/eq-shell/pull/657) feat(tenants): link to EQ Cards adoption dashboard (PostHog) |
| 2026-07-05 | eq-shell | [#656](https://github.com/eq-solutions/eq-shell/pull/656) fix(provisioning): expose app_data schema over PostgREST for new  |
| 2026-07-05 | eq-field | [#408](https://github.com/eq-solutions/eq-field/pull/408) v3.5.241 — job numbers: fetch on tab-open (fixes permanently-empt |
| 2026-07-05 | eq-field | [#407](https://github.com/eq-solutions/eq-field/pull/407) docs: correct stale tenant references (eq→zaap, ktmj deleted, dem |
| 2026-07-04 | eq-shell | [#653](https://github.com/eq-solutions/eq-shell/pull/653) chore(drift): allow-list field_job_numbers (security_invoker view |
| 2026-07-04 | eq-shell | [#651](https://github.com/eq-solutions/eq-shell/pull/651) 0160: eq_merge_sites RPC — governed site-dedup (QA row 29 follow- |
| 2026-07-04 | eq-shell | [#652](https://github.com/eq-solutions/eq-shell/pull/652) 0161: reassert security_invoker on app_data.field_job_numbers (RL |
| 2026-07-04 | eq-shell | [#650](https://github.com/eq-solutions/eq-shell/pull/650) feat(entitlements): writers → canonical + drop legacy (Phase 2 St |
| 2026-07-04 | eq-shell | [#647](https://github.com/eq-solutions/eq-shell/pull/647) fix(tenants): auto-join creating admin so new tenants are reachab |
| 2026-07-04 | eq-shell | [#648](https://github.com/eq-solutions/eq-shell/pull/648) feat(entitlements): app tiles → canonical, Stage A (readers) |
| 2026-07-04 | eq-shell | [#644](https://github.com/eq-solutions/eq-shell/pull/644) refactor(branding): one canonical copy in organisations.branding  |
| 2026-07-04 | eq-shell | [#645](https://github.com/eq-solutions/eq-shell/pull/645) feat(field): surface customer name on field_sites + drop dead cus |
_Showing 15 of 122 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **field_job_numbers provenance** — the view was created out-of-band (not originally in a repo migration); who made it + whether other planes need it tracked as `task_0467f68c`. _(added 2026-07-04)_
- **Favour Perfect first-run config** — switch into it (after one workspace-switch or re-login), configure it, and invite its real customer admin from inside `/favour-perfect/admin/users`. _(added 2026-07-04, needs your call)_
- **Optional: `reconcile_ledger` tidy for `favour-perfect`** — its `_eq_migrations` ledger has 204 rows incl. 39 null-checksum entries (cruft from a messy apply sequence: an 08:14 reconcile-path run stamped rows then failed; the 08:25 apply finished it). Schema is correct — purely cosmetic. A `reconcile_ledger=true` dispatch scoped to `favour-perfect` would tidy it. _(added 2026-07-04, needs your call)_
- **Admin-create zero-member gap** — admin "Add tenant" builds member-less, UI-unreachable tenants (no way to add a first user without a hand-inserted membership). Fix (auto-add creator as manager, or an "Add me as admin" button) running as `task_4f5989fb`. _(added 2026-07-04)_
- **Link the 19 field-enabled SKS sites with no `customer_id`** — Row 29 prestart prefill resolves the customer name only for the 11 (of 30) field-visible ehow sites that have a `customer_id`. The other 19 (Amazon SYD53, Woolworths, Microsoft SYD05/27, Western Sydney Airport, St Vincents, etc.) prefill blank. NOT auto-derivable — `sites.client_name`/`external_customer_id` are null/junk, zero name-matches to `customers.company_name`. Needs a manual ops pass (assign each site its customer in the Customers/Sites editor). Degrades gracefully (blank field) until done. _(added 2026-07-04, needs your call)_
- **Occasional deep game-day (rare, human)** — restore **auth data** into a real Supabase target (the dump excludes the managed auth *schema*, so auth rows only load where Supabase provisions it) + app-repoint smoke test. Not automatable cheaply; do when convenient. _(carried 2026-07-04)_
- **Rows 4 & 8 — resolved by verification, reopen only if they recur** — row 4 (duplicate "From Roster"): structurally only one button exists (the "twice" was the button + a muted-cell "from roster" label); row 8 (`?tab=person-wizard` blank): moot on SKS now that Add Person is hidden. Need a screenshot/repro to reopen either. _(added 2026-07-04)_
- **Visual SKS click-through** of the Job Numbers screen (OPS badge on Ops rows, manual-add still works) — needs a live `?tenant=sks#sh=` Shell session (can't mint headless). DB + routing verified. _(added 2026-07-04)_
- **Tenant logo/branding editor in EQ Shell** — upload-or-link → store in R2 → write canonical `organisations.branding.{gateLogo,palette}`; every app inherits. Running as spawned task `task_925f8842`. _(added 2026-07-04)_
- **eq demo tenant is logo-less in docs until the Shell editor ships** — or seed `eq`'s `branding.gateLogo` with a `.png` URL as a stopgap (Royce's call). _(added 2026-07-04)_
_…and 229 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date.
- **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
- **SKS anon-remediation (nspb)** — exact policy worklist in `cross-app-linkage-remediation-plan-2026-06-07.md` §7a. Separate from ehow work. SKS-live gated.
- **eq-shell** — ~~converge `c2-shell-roles` + `sks-field-host` branches~~ — `c2-shell-roles` no longer exists in eq-shell repo (deleted). Re-assess: verify whether the security-groups work from `sks-live-sprint-2026-06-07.md` Prompt A was folded into main or abandoned before reopening this track.
- **Security groups Phase 2–5** — wire group perms into session, `AdminSecurityGroups` page, first real `user_security_groups` row for a SKS user.
- Person-wizard renders blank content specifically on a cold `?tab=person-wizard` deep-link boot (normal in-app "Add Person" nav works fine) — root cause not found despite exhaustive code trace + live Sentry/entitlement checks; needs Royce's own DevTools session with the Field-iframe console context selected _(added 2026-07-03)_
- At least one SKS person ("Collin ... Toohey") has no record in canonical `app_data.staff`, blocking their leave submissions — data-ops backfill needed, not a code fix _(added 2026-07-03)_
- Royce to independently click-through-confirm the Weekends toggle, roster names, and both safety forms live (smoke-tested remotely, not yet confirmed by Royce beyond the original repros) _(added 2026-07-03)_
- First **Cards→Field approval for SKS never run** — `cards_field_approvals` has 79 rows across other tenants, **0 for SKS**. When the first SKS worker signs up to Cards + applies, exercise the admin approve + licence-verify path end-to-end (machinery proven elsewhere, unproven for this tenant) _(added 2026-07-04)_
- **SKS staff data-entry rule** — enter each person **once** with an accurate mobile (+ email where held); no DB uniqueness on `workers.phone`, so two stubs sharing a number = only the best-credentialed one gets adopted, the other dangles. 0 phones on multiple worker rows today — keep it that way _(added 2026-07-04)_
_…and 23 more · [sks/pending.md](sks/pending.md)_

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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-05 07:46 UTC._
