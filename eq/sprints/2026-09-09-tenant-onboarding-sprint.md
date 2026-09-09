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

---

## Decided (2026-09-09, via `/decide`)

### 1. Tenant-isolation model: shared ehow by default, dedicated project as an explicit opt-in

Two mechanisms existed for "where does a tenant's Field roster live," half-built in different directions — **shared, column-scoped** (`workers-canonical-sync` hardcodes a single `EHOW_URL` + a `TENANT_ROUTES` const mapping org → an ehow-side `tenant_id`; every Cards worker gets filed into `ehow.app_data.staff`, scoped by that column) vs. **dedicated project per tenant** (eq-shell's admin "Add tenant" → Provision → fleet tenant-migrate flow, proven once on "Favour Perfect," 2026-07-04; `organisations.supabase_url`/`supabase_anon_key` exist specifically for this). Madagins had a foot in both, wired into neither.

**Call: shared-ehow is the default for every new tenant. Dedicated project stays alive only as an explicit, opt-in escape hatch** for a tenant that specifically needs data isolation — not a parallel default nobody remembers to finish. Reasoning (full six-step pass in session): it matches what's actually running today for the only real tenant that exists, months of proof, zero new infra per tenant; and it doesn't throw away the Provision/tenant-migrate machinery, just stops it being the accidental default. Pure dedicated-project-always was ruled out — it directly undercuts "seamless" (every onboarding now carries the exact infra failure modes Favour Perfect hit) and multiplies ops surface linearly with tenant count for tenants that likely don't need it.

**Non-negotiable guardrail on the build below, surfaced in pre-mortem, not optional:** generalising the shared-ehow scoping logic without a deliberate cross-tenant-leak test is exactly how a real leak happens — same failure shape as the 2026-07 EQ-SHELL-14 incident (a phone-normalisation backfill mis-filed a live worker onto the wrong tenant's roster for ~10 minutes). Ship the test before this touches a second real tenant.

**Crux, if it matters later:** this flips if a real near-term customer (not Madagins) turns out to need guaranteed data isolation — then dedicated-project stops being a rare escape hatch and becomes the thing worth investing in properly. Nothing currently known points that way.

---

## Wave 1 — ship now, no more decisions needed

### 2. Generalise `workers-canonical-sync` beyond the SKS/ehow hardcode

Make `TENANT_ROUTES` data-driven (read off `organisations`/`shell_control.tenants` directly, or a small dedicated mapping table) instead of a const requiring a code deploy per tenant — the literal opposite of "seamless." **Must ship with** a test that deliberately tries to cross tenant boundaries in `findStaffId()`'s phone/email adoption logic and asserts it fails (the guardrail above). Once live, register Madagins as a normal shared-ehow tenant.

### 3. Archive the orphaned `eq-tenant-madagins` Supabase project

Empty, never wired to anything (`organisations.supabase_url` and `shell_control.tenants.supabase_project_ref` both still null), not needed under the shared-ehow-default model. A `/_platform/tenants` admin action, not code — do this once #2 is live so Madagins isn't briefly homeless.

---

## Wave 2 — small decision needed first, each independently buildable, unrelated to the isolation-model call

### 4. Cards-side admin-create zero-member gap

`task_4f5989fb` (eq-shell, 2026-07-04) covers the Shell-side half of "a new tenant has nobody in it" — confirmed still working tonight, Madagins got 3 auto-seeded `shell_control.user_tenant_memberships` managers. But that fix lives in eq-shell and only touches `shell_control`. It never reaches eq-cards' own `org_memberships` table — a separate repo, separate concern — so Madagins still had zero Cards-side admins tonight. Without one, the normal in-app "invite a worker" flow (`eq_cards_request_worker_access`, gated on `is_org_admin`) has nobody able to call it on a brand-new tenant.

**Needs a decision:** should eq-shell's tenant-creation flow call out to eq-cards (webhook/API) to seed the equivalent `org_memberships` admin row, or should eq-cards seed it itself, lazily, the first time someone from that tenant authenticates? Either is a small, scoped build once picked.

### 5. Tier field split-brain

`organisations.tier` = `'Standard'` and `shell_control.tenants.tier` = `'advanced'` — same Madagins org, two different tables, no visible sync between them, no migration or trigger keeping them aligned.

**Needs a decision, and it hasn't been investigated which answer is true:** are these meant to be one source of truth (pick one, have the other read from it), or are they genuinely independent axes — e.g. an EQ-Field-feature tier vs. a platform/billing tier — that just happen to share the word "tier" and read as a bug when they aren't one? Nobody has confirmed intent either way; this sprint is flagging the split, not asserting which it is.

---

## Summary

| # | Item | Status | Action |
|---|---|---|---|
| 1 | Isolation model: shared-ehow default, dedicated project opt-in | **Decided 2026-09-09** | Unblocks #2/#3 below |
| 2 | Generalise `workers-canonical-sync` off the SKS/ehow hardcode + cross-tenant-leak test | Ready to build | Build on your go |
| 3 | Archive orphaned `eq-tenant-madagins` project | Ready, admin action | Your click, after #2 ships |
| 4 | Cards-side admin-create zero-member gap | Needs a small decision | Webhook from eq-shell, or lazy self-seed in eq-cards? |
| 5 | Tier field split-brain (`organisations` vs `shell_control.tenants`) | Needs a small decision | One source of truth, or genuinely two axes?
