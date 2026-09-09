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

## Wave 3 — needs a bigger decision before anything else here is buildable

### 1. Which tenant-isolation model does EQ Field actually commit to?

Two mechanisms exist for "where does a tenant's Field roster live," and they're only half-built, in different directions:

- **Shared, column-scoped**: `workers-canonical-sync` (eq-cards edge function) hardcodes a single `EHOW_URL` and a `TENANT_ROUTES` const mapping org → an ehow-side `tenant_id`. Every Cards worker signup gets filed into `ehow.app_data.staff`, scoped by that column. Today `TENANT_ROUTES` contains exactly one entry (SKS) — anyone else falls through to SKS by default (if unstamped) or gets silently skipped (`no_tenant_route`, if explicitly stamped to an org with no route — Madagins' exact situation the moment anyone tries to attribute a worker to it).
- **Dedicated project per tenant**: eq-shell's admin "Add tenant" flow actively provisions a brand-new standalone Supabase project (the "Provisioning…" spinner), and a separate "Provision" + fleet tenant-migrate step is supposed to build its schema (confirmed live for tenant "Favour Perfect," 2026-07-04). `organisations.supabase_url` / `supabase_anon_key` exist specifically to point a tenant at its own project instead of the shared fallback. Madagins got the empty project (`eq-tenant-madagins`) but never got the Provision/migrate follow-through — so it's half-built toward *this* model instead.

Madagins currently has a foot in both and is fully wired into neither. Whichever model is the real answer, the other needs to either get finished generically (so it's not a one-off per tenant) or get retired, or every future tenant repeats tonight's audit. This is Royce's call — not a technical question so much as "which of these two already-built mechanisms is the one we're actually committing to."

**Depends on this decision:**
- Whether `TENANT_ROUTES` needs a Madagins entry at all, or whether Madagins should instead get its dedicated project finished (Provision + tenant-migrate, same as Favour Perfect).
- Whether `TENANT_ROUTES` stops being a hardcoded const (requiring a code deploy for every new tenant, which is the literal opposite of "seamless") and becomes data-driven — straightforward once the model is picked, not before.
- What happens to the orphaned `eq-tenant-madagins` project: finish provisioning it, or archive/delete it.

---

## Wave 2 — small decision needed first, each independently buildable once decided, not blocked by Wave 3

### 2. Cards-side admin-create zero-member gap

`task_4f5989fb` (eq-shell, 2026-07-04) covers the Shell-side half of "a new tenant has nobody in it" — confirmed still working tonight, Madagins got 3 auto-seeded `shell_control.user_tenant_memberships` managers. But that fix lives in eq-shell and only touches `shell_control`. It never reaches eq-cards' own `org_memberships` table — a separate repo, separate concern — so Madagins still had zero Cards-side admins tonight. Without one, the normal in-app "invite a worker" flow (`eq_cards_request_worker_access`, gated on `is_org_admin`) has nobody able to call it on a brand-new tenant.

**Needs a decision:** should eq-shell's tenant-creation flow call out to eq-cards (webhook/API) to seed the equivalent `org_memberships` admin row, or should eq-cards seed it itself, lazily, the first time someone from that tenant authenticates? Either is a small, scoped build once picked.

### 3. Tier field split-brain

`organisations.tier` = `'Standard'` and `shell_control.tenants.tier` = `'advanced'` — same Madagins org, two different tables, no visible sync between them, no migration or trigger keeping them aligned.

**Needs a decision, and it hasn't been investigated which answer is true:** are these meant to be one source of truth (pick one, have the other read from it), or are they genuinely independent axes — e.g. an EQ-Field-feature tier vs. a platform/billing tier — that just happen to share the word "tier" and read as a bug when they aren't one? Nobody has confirmed intent either way; this sprint is flagging the split, not asserting which it is.

---

## Not a build — needs your own action, and only after Wave 3 is decided

### 4. Close the loop on Madagins itself

Once the isolation-model call is made: either click Provision on `/_platform/tenants` for Madagins and dispatch the fleet tenant-migrate (same as Favour Perfect) if dedicated-project wins, or add its `TENANT_ROUTES` entry and archive the empty `eq-tenant-madagins` project if shared-ehow wins. Deliberately not pre-built blind — building either path before Wave 3 is decided risks building the wrong one.

---

## Summary

| # | Item | Status | Action |
|---|---|---|---|
| 1 | Which isolation model (shared-ehow vs. dedicated-project) | Needs a bigger decision | Your call — unblocks #3 and #4 |
| 2 | Cards-side admin-create zero-member gap | Needs a small decision | Webhook from eq-shell, or lazy self-seed in eq-cards? |
| 3 | Tier field split-brain (`organisations` vs `shell_control.tenants`) | Needs a small decision | One source of truth, or genuinely two axes? |
| 4 | Close the loop on Madagins itself | Not a build | Your click-through, once #1 is decided |
