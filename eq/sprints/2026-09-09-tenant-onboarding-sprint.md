---
title: Tenant onboarding (Madagins) — follow-up sprint
owner: Royce Milmlow
created: 2026-09-09
last_updated: 2026-09-09
scope: Gaps surfaced live while onboarding the Madagins tenant (Nelson Sareto + Conor Horgan) on 2026-09-09 — cross-referenced against two pre-existing, still-open pending entries (eq-cards.md _added 2026-07-10_, eq-shell.md _added 2026-07-04_) rather than treated as fresh discoveries. Scoped from Royce's own framing: "learn from this new tenant, fix known issues, work towards a seamless experience for future expansion."
read_priority: high
status: live
---

# Tenant onboarding (Madagins) — follow-up sprint

## How this was built

Royce asked to add Nelson Sareto and Conor Horgan to a newly-created "Madagins" tenant. What should have been a two-minute admin action turned into a live audit, because the tenant had been created via raw pieces (an `organisations` row, a `shell_control.tenants` row, an auto-seeded set of Shell-side managers, and a standalone empty Supabase project called `eq-tenant-madagins`) without the normal admin flow ever fully completing. Working through it live surfaced that this exact shape of problem was already flagged twice before, months ago, and never closed:

- `eq/pending/eq-cards.md` _(added 2026-07-10)_: "Generalise `workers-canonical-sync` beyond SKS/ehow... before a second tenant onboards." Madagins is now that second tenant.
- `eq/pending/eq-shell.md` _(added 2026-07-04, Favour Perfect session)_: "Admin-create zero-member gap — admin 'Add tenant' builds member-less, UI-unreachable tenants," tracked as `task_4f5989fb`.

Both entries were re-confirmed as still open tonight against a freshly-fetched `origin/main` (not the stale local clone), and are trimmed out of their source pending files below in favour of living here.

Nelson and Conor themselves are sorted — added to Madagins' `org_memberships` and `shell_control.user_tenant_memberships` directly (their existing SKS Technologies membership and Field roster entry are untouched). That per-person fix doesn't need a sprint. The rest of this file is about the fact that it took a live audit to get there, and will again for the next tenant unless something below actually ships.

A follow-up question — "is there anything else to improve multiple tenancies via eq cards" — led to two more finds: a third, already-built tenant-onboarding path in EQ Cards itself (`/provision?token=...` → `shell_control.provision_tenant()`, which folds directly into decision #2 below), and a background sweep of the Flutter client (`lib/`) specifically for multi-org client-side gaps, which is where items #8 and #9 came from.

---

## Decided (2026-09-09, via `/decide`)

### 1. Tenant-isolation model: shared ehow by default, dedicated project as an explicit opt-in

**Correction (2026-09-09, later same day):** Royce reviewed this directly (asked via a separate
session, after this call had already left an eq-field session and the uncommitted
`fix/tenant-provisioning-pg-cron` branch both blocked on which way madagins goes) and
**rejected it — madagins keeps its own dedicated Supabase project.** Shared-ehow-as-default
does not stand. The reasoning below is kept for the record, not as current guidance. Live work
proceeding on the dedicated-project premise: eq-field's schema-provisioning script against
`ornndtbdkxfsewspbrwk`, and `fix/tenant-provisioning-pg-cron` (see
`eq/sprints/2026-09-09-provisioning-completeness-followup.md`). **Item #5 below is retracted.**

Two mechanisms existed for "where does a tenant's Field roster live," half-built in different directions — **shared, column-scoped** (`workers-canonical-sync` hardcodes a single `EHOW_URL` + a `TENANT_ROUTES` const mapping org → an ehow-side `tenant_id`; every Cards worker gets filed into `ehow.app_data.staff`, scoped by that column) vs. **dedicated project per tenant** (eq-shell's admin "Add tenant" → Provision → fleet tenant-migrate flow, proven once on "Favour Perfect," 2026-07-04; `organisations.supabase_url`/`supabase_anon_key` exist specifically for this). Madagins had a foot in both, wired into neither.

**Call: shared-ehow is the default for every new tenant. Dedicated project stays alive only as an explicit, opt-in escape hatch** for a tenant that specifically needs data isolation — not a parallel default nobody remembers to finish. Reasoning (full six-step pass in session): it matches what's actually running today for the only real tenant that exists, months of proof, zero new infra per tenant; and it doesn't throw away the Provision/tenant-migrate machinery, just stops it being the accidental default. Pure dedicated-project-always was ruled out — it directly undercuts "seamless" (every onboarding now carries the exact infra failure modes Favour Perfect hit) and multiplies ops surface linearly with tenant count for tenants that likely don't need it.

**Non-negotiable guardrail on the build below, surfaced in pre-mortem, not optional:** generalising the shared-ehow scoping logic without a deliberate cross-tenant-leak test is exactly how a real leak happens — same failure shape as the 2026-07 EQ-SHELL-14 incident (a phone-normalisation backfill mis-filed a live worker onto the wrong tenant's roster for ~10 minutes). Ship the test before this touches a second real tenant.

**Crux, if it matters later:** this flips if a real near-term customer (not Madagins) turns out to need guaranteed data isolation — then dedicated-project stops being a rare escape hatch and becomes the thing worth investing in properly. Nothing currently known points that way.

### 2. Cards-side admin-create zero-member gap: lazy self-seed, not a webhook

`task_4f5989fb` (eq-shell, 2026-07-04) already seeds the Shell-side half correctly — confirmed live on Madagins: its 3 auto-seeded `shell_control` managers are real contacts (Royce, Michelle Moore `accounts@madagins.com.au`, Aditi Rajbhandari `aditi@madagins.com.au`), not placeholder ops accounts. eq-cards' own `org_memberships` table never gets touched by that fix though — separate repo, separate DB concern — so a brand-new tenant still has zero Cards-side admins, and the in-app "invite a worker" flow (`eq_cards_request_worker_access`, gated on `is_org_admin`) has nobody able to call it.

**Call: eq-cards self-seeds its own `org_memberships` admin row lazily, the first time an authenticated user who already holds `shell_control.user_tenant_memberships.role = 'manager'` for that tenant touches Cards** — not a new webhook from eq-shell. Reasoning: no new cross-repo coupling, no new failure mode (a webhook that can silently fail is exactly how you get a *third* zero-admin gap with a different cause); and the trigger signal is already proven trustworthy rather than assumed — verified live above, not hypothetical.

**Crux:** flips if eq-shell's "Add tenant" form doesn't reliably capture a real intended admin as a `shell_control` manager for every *future* tenant, not just this once — worth a quick look at that form before building, not assumed true by extrapolation from one data point.

**Update, same day:** EQ Cards already has a third, separate onboarding path that does this correctly today — `/provision?token=...` (`provision_tenant_screen.dart`) routes through `shell_control.provision_tenant()`, ONE atomic transaction that creates the Shell identity *and* the Cards-side `organisations` + `org_memberships` admin row together. Its own comment calls the Cards-side insert "FATAL here by design... a tenant whose organisation row is missing looks provisioned but Cards cannot use it" — built specifically to prevent tonight's exact failure. Madagins didn't go through it (it went through the lighter, identity-only "Add tenant" console action instead), and the RPC has a real limitation of its own: it always creates a brand-new `shell_control.tenants` row, with no path to attach a provision-token to a tenant that already exists — so today you can't retroactively send Michelle or Aditi a self-serve link for a tenant "Add tenant" already created; it would just create a duplicate. The lazy-seed call above still stands as the right EQ-Cards-only fix (no eq-shell changes, works regardless of which creation path was used) — this is additional context, not a reversal.

### 3. Tier field split-brain: confirmed bug, not two intentional axes

Checked `AdminTenantsPage.tsx` / `admin-tenants.ts` directly: `shell_control.tenants.tier` (`trial`/`standard`/`advanced`/`enterprise`) is the real field the actual "Add Tenant" admin UI sets and edits — Madagins was deliberately set to `advanced` there. `organisations.tier` is a separate, older, EQ-Field-specific column (its own comment: "drives `tierAtLeast()` UI gating in EQ Field") that was never wired to read from the canonical value — it's sitting at its schema default (`'Standard'`) because nothing ever set it otherwise. Not two intentional axes; a live bug — **EQ Field is currently gating Madagins' features off the wrong, stale tier.**

**Call: sync `organisations.tier` from `shell_control.tenants.tier`** — backfill Madagins now, then either a trigger keeping the two aligned going forward, or stop storing a separate copy on `organisations` and have `tierAtLeast()` read `shell_control.tenants.tier` directly through the existing `organisations.tenant_id` join.

---

## Wave 1 — ship now, no more decisions needed

### 4. Generalise `workers-canonical-sync` beyond the SKS/ehow hardcode — done, [eq-cards#348](https://github.com/eq-solutions/eq-cards/pull/348)

**Merged and deployed 2026-09-09 (`df07f8c`)** — [Build & Deploy run 34316810026](https://github.com/eq-solutions/eq-cards/actions/runs/34316810026), both jobs (`Deploy edge functions`, `deploy`) completed successfully, confirmed independently via `gh run view` rather than trusting the dispatch alone. `TENANT_ROUTES` replaced with `resolveTenantRoute()` (new module `tenant-routing.ts`), reading `organisations.tenant_id` live instead of a const requiring a code deploy per tenant. Guardrail shipped as required: `tenant-routing.test.ts` asserts two different orgs never resolve to each other's tenant, and an org with its own dedicated data-plane project is refused rather than silently mis-routed into shared ehow — 6/6 passing in CI. Also added a `deno test` CI job for edge functions, which had none before. Unstamped workers (`origin_org_id` NULL — the overwhelming majority) keep exactly today's behaviour, unit-tested.

Note: this deploy also shipped whatever else was sitting merged-but-undeployed on `main` at the time — checked first (production was one commit behind main, exactly this PR, so nothing else rode along this time), but worth remembering for next time: `deploy.yml`'s edge-function job and its Netlify web-app job both fire on the same dispatch with no way to select just one.

Madagins itself still isn't registered as a shared-ehow tenant by this alone — that's a data step (setting `origin_org_id` for its workers, or equivalent), not touched here.

### 5. ~~Archive the orphaned `eq-tenant-madagins` Supabase project~~ — RETRACTED

**Retracted (2026-09-09, later same day): do not do this.** Royce explicitly rejected the
shared-ehow-default decision this depended on (see the correction on Decision #1 above) —
madagins keeps its dedicated project. Separately, the premise below no longer holds either:
verified live the same day, `shell_control.tenant_routing.supabase_project_ref` and
`organisations.supabase_url` are both populated for madagins now, not null.

~~Empty, never wired to anything (`organisations.supabase_url` and `shell_control.tenants.supabase_project_ref` both still null), not needed under the shared-ehow-default model. A `/_platform/tenants` admin action, not code — do this once #4 is live so Madagins isn't briefly homeless.~~

### 6. ~~Lazy-seed the Cards-side `org_memberships` admin row~~ — CLOSED, unnecessary

**Closed (2026-09-09, later same day): no code needed.** Checked `is_org_admin()`'s actual live definition rather than assuming from data alone — it already has a third clause checking `shell_control.user_tenant_memberships.role = 'manager'` directly, no `org_memberships` row required. Every admin RPC in the app (`eq_cards_admin_list_workers`, `_upsert_worker`, `_create_invite`, `_revoke_invite`) gates through exactly this function. Michelle and Aditi can already list Madagins' team, invite workers, and manage credentials right now, purely from their existing Shell manager role. The original item was scoped from checking `org_memberships` directly and assuming that was the only path — it isn't.

~~Per decision #2: on a Cards-side authenticated action, if the user holds `shell_control.user_tenant_memberships.role = 'manager'` for a tenant and has no `org_memberships` row for its `organisations` counterpart yet, create one (`role: 'admin'`, `status: 'active'`). No backfill pass needed — self-corrects the first time Michelle or Aditi actually uses Cards for Madagins.~~

### 7. Sync `organisations.tier` from `shell_control.tenants.tier` — done, [eq-cards#352](https://github.com/eq-solutions/eq-cards/pull/352)

**Fully closed (2026-09-09, later same night).** Backfill done earlier for Madagins; the structural half shipped the same night — a trigger on `shell_control.tenants` (fires `AFTER UPDATE OF tier`) pushes the value into `organisations.tier`, case-normalised via `initcap()` since the two columns use different casing conventions (`enterprise` vs `Enterprise`) and a raw copy would have silently broken `tierAtLeast()` instead of fixing it. Shipping it meant actually bootstrapping eq-cards' jvkn migration pipeline for the first time ever (the "never dispatched, no approval gate" risk noted below) — closed properly, not worked around: all 163 pre-existing migrations individually verified safe first (132 by direct live-object match against jvkn, the remaining 31 read and checked by hand), *then* `--bootstrap` dispatched.

**Bigger than Madagins.** The live check run immediately before shipping found SKS — the one real paying tenant, unrelated to tonight's Madagins work — already mismatched (`organisations.tier` showing `Standard` against a canonical `enterprise`). Enterprise-gated EQ Field features (Forecast nav, the apprentice-ratio dashboard widget, the top-bar region picker) had been silently hidden from SKS users. The same migration's backfill corrected it on apply — verified live, SKS now reads `Enterprise`.

### 8. Fix the Cards-side multi-org-admin picker truncation — done, [eq-cards#350](https://github.com/eq-solutions/eq-cards/pull/350)

**Merged and deployed 2026-09-09 (`84d1bb3`)**, confirmed live three independent ways (GitHub Actions conclusion, Netlify's own `state: ready` + `published_at`, and a timestamp cross-match between the two). `org_admin_provider.dart`'s `my_admin_org_ids` truncation (`rows.first`, arbitrary) replaced with a pure `selectActiveAdminOrg()` function that prefers whichever admin org matches the JWT's current `tenant_id` — the workspace already active via the existing switcher — falling back to the first result only when none match. No new picker UI, no signature or call-site changes. 5 new unit tests, no live Supabase client needed (same extraction pattern as `tenant-routing.ts`).

Turned out item 6 closing as unnecessary doesn't reduce this one's value — `is_org_admin()`'s widened predicate means an admin can already be treated as an admin of 2+ orgs purely via Shell manager roles, with no `org_memberships` row at all. This fix was arguably more load-bearing than originally scoped, not less.

### 9. Fix `required_by_org_strip` grouping key — done, same PR as #8

**Merged and deployed 2026-09-09**, same [PR #350](https://github.com/eq-solutions/eq-cards/pull/350) as item 8. Grouping key changed from `orgName` (display string) to `orgId`. 1 new regression test (two orgs sharing a display name now render as separate cards), plus the 3 pre-existing tests still passing.

---

## Summary

| # | Item | Status | Action |
|---|---|---|---|
| 1 | Isolation model: shared-ehow default, dedicated project opt-in | **Corrected 2026-09-09 — rejected; madagins keeps its dedicated project** | #4 unaffected (works either way); #5 retracted |
| 2 | Cards-side admin-create gap: lazy self-seed off `shell_control` manager role | **Decided 2026-09-09 — build found unnecessary** | #6 closed, `is_org_admin()` already covers it |
| 3 | Tier split-brain: confirmed bug, sync from `shell_control.tenants.tier` | **Confirmed 2026-09-09** | Unblocks #7 below |
| 4 | Generalise `workers-canonical-sync` off the SKS/ehow hardcode + cross-tenant-leak test | **Done — [PR #348](https://github.com/eq-solutions/eq-cards/pull/348), live** | — |
| 5 | Archive orphaned `eq-tenant-madagins` project | **Retracted — do not do this** | Madagins keeps its dedicated project |
| 6 | Lazy-seed Cards-side `org_memberships` admin | **Closed — unnecessary**, `is_org_admin()` already covers it | — |
| 7 | Backfill + sync `organisations.tier` | **Done — [PR #352](https://github.com/eq-solutions/eq-cards/pull/352), live** | Also fixed a live SKS tier mismatch found while shipping it |
| 8 | Fix multi-org-admin picker truncation (`org_admin_provider.dart`) | **Done — [PR #350](https://github.com/eq-solutions/eq-cards/pull/350), live** | — |
| 9 | Fix `required_by_org_strip` grouping key (name → id) | **Done — same PR as #8** | — |
