---
title: Canonical Consolidation Roadmap — the EQ suite onto one defined spine
owner: Royce Milmlow
last_updated: 2026-06-25
scope: The sequenced, verified to-do list to reach "canonical layer of truth, referenced throughout" + the portable worker-owned Cards vision
read_priority: high
builds_on: canonical-target-model-2026-06-24.md, service-consumes-canonical-spine-2026-06-16.md
status: live
verified: 2026-06-25 against ehow (ehowgjardagevnrluult)
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
| Contact | `contacts` (230) + `contact_customer_links` + `contact_site_links` | — | 🔴 `service.contacts` VIEW exists but **UNUSED** — `/contacts` + edit flows read/write service-local **base tables** `customer_contacts` (109) + `site_contacts` (0); no triggers, no sync. NB `customer_contacts` is a BASE TABLE, not a view | `sks_quotes_contacts` (338) + `_contact_links` (13,936) | — | 🔴 NOT DONE — Service reads a local fork. Step 1 data reconcile done 2026-07-02 (208→230); read/write cutover (views+triggers, notif-prefs FK remap, repoint, drop) is a dedicated PR. Quotes unconsolidated; `public.sks_contacts` bridge view exists |
| Tender | `tenders` (51) | `public.tenders` (366, in-place via `JWT_INPLACE_TABLES`) | — | — | — | ⚠️ SPLIT — no `app_data.field_tenders` twin |
| Person/Staff | `staff` (74) | `public.people` (75, legacy) + `field_people`/`field_managers` views | `profiles`/`tenant_members` (5) | — | `jvkn.workers` pool → `cards-approve-staff` photocopy | 🔴 MESSIEST — 3 person tables + pool |
| Licence | `licences` (0) | — | — | — | `worker_credentials` (jvkn) | ⬜ NOT STARTED — greenfield |

### Sync machinery present (to be retired, not extended)
`public.canonical_outbox` (0), `app_data.canonical_events` (127),
`cards-approve-staff.ts` photocopy. The target is **read-in-place**, so these are
transitional — they go away as each entity converges, they don't grow.

---

## 2b. Audit 2026-06-25 — what's already BUILT (the surprise)

A read-only substrate + repo audit (jvkn pool data, eq-cards, eq-shell) found the suite
is far closer to done than §1 implies. **EQ Cards has shipped the passport + consent +
multi-tenant model end-to-end, on live data; EQ Field is the laggard.**

**Built and IN USE:**
- **Consent layer (I had called this "Phase 4, the hard 90%, not started") — SHIPPED in
  Cards, user-reachable:** worker requests an employer's access → respond → revoke.
  Live data: `jvkn.org_access_requests`=5, `org_memberships`=15,
  `shell_control.user_tenant_memberships`=26. RPCs `eq_cards_submit/respond/revoke_*` +
  Flutter UI (`ConnectToCompanyScreen`, `PendingConnectionsBanner`, revoke in settings).
- **Multi-tenant / one-card-many-companies — BUILT + used:** `eq_cards_list_my_tenants` /
  `set_active_tenant`; worker switches active org, JWT re-mints. Many memberships per
  worker; only *simultaneous* multi-org view is absent (likely unneeded).
- **Passport self-service (Decision A) — BUILT:** worker self-edits profile + licences in
  Cards. Pool is the identity SoR; Field reads it via `eq_field_get_worker_summary`.
- **Licences = pool (Decision D) — ALREADY the model.** Live `jvkn.licences`=14,
  `licence_types`=21, `certificates`=4. **Correction: the SoR is `licences`/`certificates`,
  NOT `worker_credentials`** (that table is empty/legacy). Worker self-service licence edit
  shipped.
- **canonical-api gateway — production-grade:** 5 app keys, `external_id` idempotent PUT +
  email/ABN secondary identity match + 23505 race recovery; fronts customers/contacts/
  sites/staff/licences/jobs/assets/events.
- **cards-approve-staff (Phase 3 projection) — rich:** `cards_worker_id`-first match +
  phone fallback, dedup guard, **additive** licence merge, provisions shell membership +
  `org_memberships` + a `canonical_events` heartbeat. (Still projection-at-approval, not a
  live sync — Decision C target stands.)
- **Governance (Phase 0) — BUILT:** `tenant-migrate.yml` One Pipe + `check-tenant-drift.mjs`;
  `--strict-identity` flips informational→failure. (This is the in-flight security work — coordinate.)

**The genuine remaining backlog:**
1. **EQ Field is the laggard.** It reads the spine and *receives* approved workers via the
   cards-approve projection, but: its gateway WRITE ACL is empty by design
   (`canonical-api.ts:114 field: new Set([])` — "Field writes app_data directly; no
   canonical-api PUT path yet"), and it does **not** surface the worker's live pool
   licences/credentials or consent state. → **Decision B is net-new, and it's all in Field.**
2. **Org-admin side of consent is ABSENT** — the loop is worker-side only; an employer
   *initiating* a request / an admin request-inbox isn't built (`request_worker_access` has
   zero callers). Likely lands in Shell/Cards, not Field.
3. **Field finishers** — tender split, leave-canonical flip, `public.people` retire (Phase 3 repoint).

**Reframe:** the program is much smaller than §4 implied. It's mostly **bring Field up to
the line Cards already set, build the employer side of consent, and verify the seams** —
not build the model from scratch. The honest-read in §8 still holds, but Phase 4 is largely
*done*, not pending.

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
| **E** | Calendar / schedule SoR | **UNIFY on canonical — one calendar across all EQ apps** (Royce, 2026-07-02). Target end-state: a single canonical schedule entity every app reads/writes via views, spanning Service PM planning (`service.pm_calendar`, 0 rows) and Field dispatch (`app_data.schedule_entries`, Field's new canonical schedule as of 2026-07-02). Not "link two calendars" — one calendar. Workflow-scale; Field's `schedule_entries` is brand-new so the spine is still settling. Sequence after contacts + the person/staff consolidation land. | Future phase |

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
      **⚠️ Coordinate:** this is the same drift-CI / security surface as the in-flight
      Sentry/security update (2026-06-25, separate console). Sequence with that work —
      do not start `--strict-identity` blind while the drift baseline is being changed.
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
- [x] **Service**: customer/site/asset consolidated (view + INSTEAD OF triggers). **Contact is NOT** —
      `service.contacts` canonical view exists but the app reads/writes service-local base tables
      `customer_contacts`/`site_contacts` (found 2026-07-02 live audit; roadmap's "contact done" was wrong).
      Step 1 (data reconcile) done; read/write cutover is a dedicated PR (notif-prefs FK remap is the blocker).
- [x] **Drift check BUILT** (2026-07-02) — `consistency.sor_drift.shadow_contact_tables` in eq-service
      `audits/run.sql`: flags any `service.*` base table with an `email` column shadowing a canonical entity.
      Fires 2 (the contact forks); WARN → ERROR once contacts consolidated. This is the check this line asked
      for — it was never built, which is exactly why the contact fork went undetected for weeks.
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

## 9. Why this direction holds (steelman — 2026-06-25)

**Thesis (strongest form):** the suite should converge on a two-tier canonical spine —
a shared, worker-owned identity/credential **pool** above the tenants, a per-tenant
`app_data` spine beneath — with every app reading/writing in place, never copying. This
is the *only* data shape in which EQ's actual product (a credential that follows a
worker across employers) can exist. The architecture decision and the product decision
are the same decision.

**The case for:**
1. **Substrate already wants this; the risk is retired.** Field reads/writes the SKS
   spine in-place today; Service reads+writes canonical via views; the pool holds 71
   linked identities. "Does cross-app in-place work on a live customer?" is already
   answered yes. The cheapest path forward is also the strategically correct one.
2. **Duplication is an N² tax that compounds.** One person in 4 tables, one customer in
   2; every new app adds another copy. One customer = the cheapest this ever gets.
3. **The pool is the product, not the plumbing.** Portable credentials only exist as a
   shared pool above tenants. Per-tenant identity = choosing not to build the product.
4. **It's the EQ philosophy in schema form** — pool = the worker's data; the value is
   encoded in the model, which is why it resists drift.
5. **Category change, not increment** — the pool is the substrate the trust/network moat
   grows on; consolidation turns a feature competitor into a platform.

**Objections it survives (with honest concessions):**
- **Coupling** ("one migration breaks three apps") → why governance is Phase 0. The
  coupling is chosen; loose-coupling-via-copies is the worse problem. *Concession:* only
  holds because the apps genuinely share entities — they do.
- **Pool = SPOF + latency** → Decision A's write-through projection keeps the hot path
  in-DB; "shared" is inherent to a passport, so the answer is HA, not avoidance.
  *Concession:* a real availability dependency; the projection must be engineered well.
- **"Premature for one customer"** (the serious one, half-right) → lock the *direction*
  now so features stop adding copies; do the cheap/greenfield pieces now; **defer** the
  expensive phases until a second employer *pulls* them. *Concession:* the whole case is
  conditional on the portable-Cards thesis being real (Royce: it is).
- **Consent is the hard 90%** → the plan *names* it (Phase 4) and sequences it last; the
  architecture doesn't solve consent but is the only one that *permits* it. *Concession:*
  the business risk lives in Phase 4; a correct model de-risks it not at all.

**Where it would be wrong:** correct iff (1) the portable-credential product is the real
goal; (2) governance actually gets installed (else "canonical" → "shared mess"); (3) the
expensive phases stay demand-driven, not pushed ahead of need.

**Verdict:** given those three, this is not a refactor being *chosen* — it's the latent
shape the data and the product thesis already pull toward. The risk was never the
architecture; it's governance discipline and the Phase-4 consent problem — both named
and sequenced here, not hidden.
