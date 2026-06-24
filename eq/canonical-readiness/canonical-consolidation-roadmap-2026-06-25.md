---
title: Canonical Consolidation Roadmap — the EQ suite onto one defined spine
owner: Royce Milmlow
last_updated: 2026-06-25
scope: The sequenced, verified to-do list to reach "canonical layer of truth, referenced throughout" + the portable worker-owned Cards vision
read_priority: high
builds_on: canonical-target-model-2026-06-24.md, service-consumes-canonical-spine-2026-06-16.md
status: live — substrate-verified 2026-06-25 against ehow (ehowgjardagevnrluult)
---

# Canonical Consolidation Roadmap (2026-06-25)

The detailed to-do list to get the EQ suite to its final shape: **one canonical
layer of truth, every app feeds into it and references it, defined throughout** —
and the thing that makes the whole bet worth it, **EQ Cards as a portable,
worker-owned credential that follows a person across every employer in the industry.**

This is built on the locked target model (`canonical-target-model-2026-06-24.md`)
and the verified live audit below. It supersedes any earlier note that called
Field's `app_data.field_*` views "cosmetic pass-throughs" — that was wrong (see
Verified State).

---

## 0. The guiding principle (measure every step against it)

> **The worker owns their card.** At every step ask: *does the worker still own and
> control their card?* Get that right and multi-tenant, portability, and the whole
> industry play follow. Lose it and you've built another company's HR database.

And the engineering corollary, from the target model:

> **"Defined throughout."** Canonical truth is not colocation — it's *definition*:
> one agreed table per entity, one ID scheme, one clear writer, everyone else
> references. Colocation (one Supabase per tenant) makes that *easy*; governance
> makes it *true*. Unreviewed migrations to the shared layer erode "defined" — so
> change-control on `app_data` is part of the architecture, not paperwork.

---

## 1. Target outcome (what "done" looks like)

- **One Supabase per tenant.** `app_data` = the canonical spine inside it; `public`
  = app-only (Field roster/prestarts/timesheets); apps read/write the spine
  **in-place, cross-schema** — no copies, no sync jobs.
- **Passport / badge split for people:**
  - **Passport** = the worker's identity, owned by them, living in the shared Cards
    pool (`jvkn.workers` + credentials). Name, right-to-work, licences, contact.
    Follows the person between employers.
  - **Badge** = employment at one tenant, living in that tenant's `app_data.staff`.
    Role, start date, roster eligibility. Linked **live** to the passport (not a
    photocopy).
- **One SoR per shared entity**, defined in a registry (§7), enforced by drift CI.
- **The consent layer** lets one card be active at many companies at once, with the
  worker controlling who sees what.

---

## 2. Verified current state (audit — 2026-06-25, ehow)

This is the entity double-up audit the target-model doc flagged as the open next
step. **Now done.** Counts are live `n_live_tup` estimates on ehow.

### Field is already mostly on canonical (SKS)
`scripts/supabase.js` `JWT_TABLES` routes `people, sites, schedule, timesheets,
timesheet_locks, leave_requests, managers, audit_log, prestarts, toolbox_talks,
site_diaries` through a per-tenant **Supabase JWT** (`verify-pin action=mint-data-jwt`,
`authenticated` role) rewritten to **`app_data.field_<name>`** twins over the spine.
SKS cut over fully 2026-06-15: `public.*` on ehow holds **0 SKS spine rows** and
isn't granted to `authenticated`. `app_data.field_people`/`field_managers` remap
`app_data.staff`; `app_data.field_sites` remaps `app_data.sites` (633). The app-only
twins (`field_schedule`, `field_timesheets`, `field_prestarts`…) correctly point at
`public.*`. Adapters: `roster-adapter.js`, `leave-adapter.js`, `timesheets-adapter.js`.

### The double-up matrix

| Entity | Canonical SoR (`app_data`) | Field | Service | Quotes | Cards | Verdict |
|---|---|---|---|---|---|---|
| Asset | `assets` (4808) | — | `service.assets` view | — | — | ✅ DONE — single SoR |
| Site | `sites` (633) | `field_sites` view; `public.sites`=0 (dead) | `service.sites` view | — | — | ✅ CLEAN — both apps via views |
| Customer | `customers` (266) | — | `service.customers` view | `sks_quotes_customers` (522 raw, ~121 distinct) | — | ⚠️ Service done; Quotes unconsolidated |
| Contact | `contacts` (343) + `contact_customer_links` (350) | — | `service.contacts`/`customer_contacts` (109) views | `sks_quotes_contacts` (338) + `_contact_links` (13,936) | — | ⚠️ Service done; Quotes unconsolidated; `public.sks_contacts` bridge view exists |
| Tender | `tenders` (51) | `public.tenders` (366, in-place via `JWT_INPLACE_TABLES`) | — | — | — | ⚠️ SPLIT — no `app_data.field_tenders` twin |
| Person/Staff | `staff` (74) | `public.people` (75, legacy) + `field_people`/`field_managers` views | `profiles`/`tenant_members` (5) | — | `jvkn.workers` pool → `cards-approve-staff` photocopy | 🔴 MESSIEST — 3 person tables + pool |
| Licence | `licences` (0) | — | — | — | `worker_credentials` (jvkn) | ⬜ NOT STARTED — greenfield |

### Sync machinery present (to be retired, not extended)
`public.canonical_outbox` (0), `app_data.canonical_events` (127),
`cards-approve-staff.ts` photocopy. The target is **read-in-place**, so these are
transitional — they go away as each entity converges, they don't grow.

---

## 3. Decisions — RESOLVED (Royce, 2026-06-25)

All four resolved together. They are coherent: **identity and credentials belong to
the worker (the pool); employment belongs to the tenant (the badge); all shared writes
go through one audited gateway.**

| # | Decision | Resolved | Gates |
|---|---|---|---|
| **A** | Person/Staff source of truth | **Global pool / passport.** Identity (name, DOB, contact, right-to-work) lives in `jvkn.workers`, worker-owned, shared across employers. Tenant `app_data.staff` keeps employment + a live-refreshed identity projection via `cards_worker_id` (write-through, not photocopy). | Phase 3, 4 |
| **B** | Field's canonical write path | **canonical-api gateway now.** Reads + tenant-local writes stay direct on the proven JWT-twin; identity/licence writes route through eq-shell `canonical-api` (per-app bearer, `external_id` idempotent, central audit). Chosen over the lighter pool-RPC to stand the clean multi-app boundary up *before* a second app contends. | Phase 2, 3 |
| **C** | `public.people` (75) | **Retire — Phase 3, after the pool repoint** (moved from Phase 1). Verified: all 75 rows are in a *dead id space* — `canonical_id` matches **no** `app_data.staff.staff_id`; the pool back-references them via `jvkn.workers.staff_id → people.canonical_id`. So the safe path is repoint `workers.staff_id` → `app_data.staff.staff_id` (the badge), then snapshot + drop. | Phase 3 |
| **D** | Licence / credential SoR | **Pool (`worker_credentials`).** Worker-owned, follows the worker; tenants reference via the gateway. `app_data.licences` is empty (greenfield) — no migration. Genuinely site-specific inductions may stay tenant-scoped referencing the pool credential. | Phase 2 |

**Two sequencing corrections from these decisions:** (B) adds gateway provisioning +
an identity-write contract as explicit tasks; (C) moves from Phase 1 to Phase 3 because
the pool still references `public.people` and must be repointed first.

---

## 4. The phased roadmap

Sequenced by dependency and risk. Each phase has a **done-when** gate. SKS (ehow)
leads every phase — it's the only tenant with the spine.

### Phase 0 — Decisions + governance foundation *(unblocks everything; days)*
- [ ] Royce resolves Decisions A–D (§3).
- [ ] **Close the migration change-control hole.** All `app_data` DDL goes through
      the One Pipe (`tenant-migrate.yml`); turn on `check-tenant-drift` `--strict-identity`
      so out-of-band dashboard/MCP DDL fails CI instead of being logged informationally.
      (This is the hole behind "8 migrations nobody recognised.")
- [ ] Seed the **entity-SoR registry** (§7) in eq-context — the machine-readable
      "defined throughout."
- **Done when:** the four decisions are recorded, no one can alter `app_data` without
  a reviewed migration, and the SoR registry exists.

### Phase 1 — Finish SKS Field on canonical *(close the last gaps on the reference tenant; ~1 sprint)*
- [ ] **Tender** (the last in-place Field spine entity): decide SoR between
      `public.tenders` (366, Field pipeline) and `app_data.tenders` (51), then either
      build the `app_data.field_tenders` twin + adapter or converge the pipeline onto
      canonical. Remove from `JWT_INPLACE_TABLES` once twinned.
- [ ] **Leave**: flip `LEAVE_CANONICAL` on for SKS (normalized `app_data.leave_requests`)
      once the "pick days" side-table lands (`leave-adapter.js` already built, flag default-OFF).
- [ ] (`public.people` retire moved to Phase 3 — Decision C: the pool repoint must come first.)
- [ ] **`app_config` PIN-at-gate leak**: the one table that can't be JWT-gated
      (read pre-login). Either the deeper auth refactor (stop the browser reading PINs)
      or document as accepted residual.
- **Done when:** SKS Field touches zero `public.*` spine tables; `public.*` on ehow
  holds only genuinely app-only tables.

### Phase 2 — Consolidate the other apps' spine *(kill the double-ups; ~2 sprints)*
- [ ] **Quotes → canonical customers/contacts**: dedupe `sks_quotes_customers`
      (522 → ~121 distinct) into `app_data.customers`; `sks_quotes_contacts` (338)
      into `app_data.contacts`; keep quote-only fields in a `public` sidecar; point
      Quotes at the canonical entity via views — **mirror Service's proven pattern**
      (`security_invoker` views + INSTEAD-OF triggers; the `public.sks_contacts`
      bridge view already shows the shape).
- [ ] **Licence** (Decision D = pool): wire Cards `worker_credentials` as the SoR;
      tenants reference by `worker_id` and read via the gateway; site-specific inductions
      may stay tenant-scoped referencing the pool credential. `app_data.licences` is empty
      = do it right once, no migration pain.
- [ ] **Service**: already consolidated (customer/site/asset/contact) — add a drift
      check that no local copy is silently diverging.
- **Done when:** customer, contact, asset, site, licence each have exactly one SoR in
  `app_data`, every app reads via views/triggers, no raw second copy.

### Phase 3 — Person/Staff consolidation *(the big one; gated by Decision A; ~2–3 sprints)*
- [ ] Implement passport/badge: `jvkn.workers` = identity SoR; tenant `app_data.staff`
      = employment SoR; linked by `cards_worker_id`, **live** — replace the
      `cards-approve-staff` photocopy with a write-through model (identity reads via the
      projection, identity writes via the **canonical-api gateway**, Decision B).
- [ ] **Provision Field on the gateway** (Decision B): `CANONICAL_API_KEY_FIELD` + a
      non-empty write ACL (identity), and define the identity-write contract
      (`external_id`-keyed idempotent PUT).
- [ ] **Pool repoint** (Decision C): migrate `jvkn.workers.staff_id` from
      `public.people.canonical_id` → `app_data.staff.staff_id` (the badge). Then
      snapshot + drop `public.people` via a reviewed One-Pipe migration.
- [ ] Collapse `public.sks_staff` (19) into `app_data.staff` (+ a `public` sidecar only
      for true Field-only columns).
- [ ] Every app resolves a person through the same canonical id.
- **Done when:** one person = one identity row in the pool + one employment row per
  tenant; no photocopy; `public.people`/`sks_staff` gone; no drift.

### Phase 4 — The consent layer *(the industry moat; gated by going multi-company; sized when Phase 3 lands)*
- [ ] **Worker-controlled sharing**: `org_access_requests` / `sharing_scope` /
      connections — the worker grants each company access to slices of their card,
      first-class, not bolted on.
- [ ] A worker won't put licences in Cards if competing employers can see each other —
      so this is *make-or-break*, and it's the defensible product (anyone can build a
      roster; almost nobody can build a credential network workers trust).
- **Done when:** a worker can be active in 2+ tenants at once, each sees only what the
  worker granted, and the worker can revoke at any time.

### Phase 5 — EQ tenants + ktmj retirement *(housekeeping the old shared model; parallel-safe)*
- [ ] Give each EQ tenant its own Supabase + `app_data` spine (or fold eq/demo-trades/
      melbourne into a single demo tenant), migrate off shared `ktmj`, then delete it.
- [ ] `zaap` (stalled EQ-canonical migration): decide — finish or abandon in favour of
      per-tenant spines.
- **Done when:** no tenant shares a DB; `ktmj` is gone; the registry routes each tenant
  to its own Supabase.

---

## 5. Why this order

1. **Governance first (Phase 0)** or every later phase pours concrete on sand —
   you can't have a canonical layer of truth that anyone can quietly redefine.
2. **Finish the reference tenant (Phase 1)** before copying the pattern — SKS proves
   it end-to-end, cheaply, on real data.
3. **Cheap entities before the hard one** — Quotes/Licence (Phase 2) are smaller and
   teach the pattern before Person (Phase 3), the messiest.
4. **Consent (Phase 4) only once Person is consolidated** — there's no "share my card"
   until there's one card to share.
5. **ktmj (Phase 5) is independent** — it's cleanup of the old model and can run beside
   anything once Phase 0's governance is in place.

---

## 6. Cross-cutting (every phase)

- **Worker-owns-card gate** on every people/credential change (the §0 filter).
- **Defined throughout**: keep the SoR registry (§7) current; drift CI enforces it.
- **One Pipe + Royce approval** for every shared-layer migration; `--strict-identity` on.
- **SKS = live customer data.** Per-action delete/drop OK before any destructive step,
  even on "disposable" EQ tenants.

---

## 7. Entity-SoR registry (the "defined throughout" seed)

The machine-readable contract. One row per shared entity. This is what governance
enforces and what every app references.

| Entity | SoR (target) | ID scheme | Writer | Everyone else |
|---|---|---|---|---|
| Asset | `app_data.assets` | uuid `asset_id` | Service | view |
| Site | `app_data.sites` | uuid `site_id` | Service/Field | view |
| Customer | `app_data.customers` | uuid `customer_id` (+ `external_id`) | Service/Quotes | view |
| Contact | `app_data.contacts` | uuid `contact_id` | Service/Quotes | view |
| Tender | TBD (Decision in P1) | uuid | Field | view |
| Person — identity | `jvkn.workers` (pool) | uuid `worker_id` | Cards | live link |
| Person — employment | tenant `app_data.staff` | uuid `staff_id` → `worker_id` | tenant admin | view (`field_people`/`field_managers`) |
| Licence | Cards `worker_credentials` (pool, Decision D) | uuid | Cards | reference by worker_id |

---

## 8. The honest read

The **architecture is the settled, easy part** — and Field already proves it works on
SKS. The hard, valuable, defensible work is later: the **person consolidation** (Phase
3) and the **consent layer** (Phase 4). That's good news — that's where the business
actually lives. The single most important thing to hold across all of it: *the worker
owns their card.*
