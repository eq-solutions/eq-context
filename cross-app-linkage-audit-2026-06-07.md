---
title: Cross-App Linkage Audit — EQ Suite
date: 2026-06-07
status: archived
method: Supabase MCP queries (4 projects) + code-seam audit (5 repos) on 2026-06-07
verifies: cross-repo-contracts, eq-platform-verified-state-2026-06-03, identity-convergence-target-2026-06-04
rule: live system is ground truth; design docs are leads. Where they disagree, live wins (noted inline).
owner: Royce Milmlow
last_updated: 2026-06-07
scope: Cross-app linkage audit across 4 Supabase projects and 5 repos — 2026-06-07 snapshot
read_priority: reference
---

# Cross-App Linkage Audit — EQ Suite (2026-06-07)

How EQ Cards, Shell, Field, Service and Quotes are **actually** wired together, verified against the live
databases and code — not the design docs. Every row count and link % below was pulled live on 2026-06-07.

**One-line conclusion:** the apps are linked by **soft UUID/`external_id` references + HTTP sync through Shell's
`canonical-api`**, never by cross-database foreign keys (impossible across separate Supabase projects). A
fully-wired canonical model exists (`ehow.app_data`), but the operational apps still run on their own stores and
sync up **unevenly** — so single-ID traceability holds *inside* the canonical plane and **breaks at three app
seams**: quote→job (no job data exists), worker→field-person (~0% populated), and customer identity (3–4 copies).

---

## 0. SECURITY FLAGS (read first)

Ordered by severity. RLS is **enabled on every public table in all four audited projects** — the risk is *permissive
policies*, *anon-callable definer functions*, and *key concentration*, not RLS-off.

| # | Severity | Project | Finding | Detail |
|---|---|---|---|---|
| S1 | **CRITICAL** | `ktmj` eq-solves-field (legacy DB) | ~30 tables **anon-writable** via always-true RLS policies | `people`, `managers`, `timesheets`, `leave_requests`, `sites`, `schedule`, `field_customers` are INSERT/UPDATE/DELETE-able by the **anon** role (policies `anon_*` + `*_tenant` policies whose USING/CHECK = `true`). Holds **605 people rows (staff PII)**. `verify_staff_pin` is anon-executable. Tenant-named policies give **no** tenant isolation (clauses are literally `true`). |
| S2 | **HIGH** | `nspb` sks-labour (**SKS LIVE**) | Anon write policies on live SKS data | `nominations`, `prestarts`, `site_diaries`, `toolbox_talks`, `tender_enrichment`, `roster_presence`, `audit_log` accept anon INSERT/UPDATE/DELETE (always-true). `verify_staff_pin` + `bump_rate_limit` anon-callable (PIN gate — brute-force surface, partly mitigated by rate-limit). App is mid-migration (Phase 1 JWT-securing tables); these are the not-yet-migrated legacy surfaces. |
| S3 | **MEDIUM** | `jvkn` eq-canonical (identity house) | 4 anon-executable `SECURITY DEFINER` RPCs | `eq_cards_get_worker_hr_record` (**reads HR records**), `eq_cards_delete_account` (**deletes accounts**), `eq_cards_claim_invite`, `eq_cards_preview_invite`. These *should* gate on a token/invite internally — **audit that internal authz**, especially the HR-record getter. Otherwise clean: no RLS-off, no anon write policies, no worker/credential table exposed to anon. |
| S4 | **MEDIUM** | `ehow` sks-canonical | 16 `SECURITY DEFINER` funcs executable by `authenticated`; extensions in `public` | `eq_upsert_customer/site/contact`, `eq_archive_*`, `eq_delete_*`, `app_data.approve_safety_record/submit_safety_record`. `vector` + `pg_net` installed in `public`. `sks_customers` etc. are RLS-enabled-no-policy → **service-role-only = safe** (default deny). |
| S5 | **MEDIUM (structural)** | `jvkn` shell_control | **Key concentration** | `shell_control.tenant_routing` stores the **encrypted `service_role_key` for every tenant data-plane** (`service_role_key_ciphertext/iv/tag`). Compromise of the jvkn control plane + the routing master key = access to all tenant DBs. By design, but it's the single highest-value target in the suite. |
| S6 | **LOW** (audited 2026-06-07) | `urjhmkhbgaxrofurpbgc` eq-solves-service | Audited — **clean baseline**; co-hosts the eq-context substrate | Service runs on a project **not in the canonical topology**, and this **same project hosts the eq-context substrate** (`context_files` 124, `context_proposals`, `briefs`, `_meta`) alongside the CMMS (`assets` 4801, `acb_tests` 468, `maintenance_check_items` 7086, `customers` 12, `profiles` 16, `mfa_recovery_codes` 40). **RLS ON for all 56 public tables** (no RLS-off). Only anon-write policies are intentional append-only patterns: `estimates`/`estimate_events`/`briefs` anon INSERT, `context_proposals` public INSERT, `context_files`/`_meta` anon SELECT. **No anon UPDATE/DELETE on PII/asset/test tables.** Worth a glance: confirm the anon-INSERT on `estimates`/`estimate_events` is a deliberate public estimate-accept surface. |

**Cross-tenant ID leakage:** none structurally possible (no cross-DB FKs). The realistic leakage path is the S1/S2
anon-write policies, which let an anon-key holder mutate other people's rows within those tenant DBs.

---

## 1. Executive summary

1. **Mechanism:** all cross-app links are soft `*_id`/`canonical_id`/`external_id` columns + **HTTP POST to
   `https://core.eq.solutions/.netlify/functions/canonical-api`** (per-app Bearer keys `CANONICAL_API_KEY_*`).
   No cross-database FKs. No Realtime/webhook bus. The "event bus" is `canonical_events` written via that HTTP hop.
2. **The canonical model is real but mostly empty of the linking entities.** `ehow.app_data` is fully FK-wired
   (customer→site→contact→quote→job→asset→timesheet→staff). But **`app_data.jobs` = 0 rows** and
   **`app_data.quote` = 0 rows**. Assets (4808) and customers (389) are populated; jobs/quotes are not.
3. **Quote → Job → Timesheet cannot be traced** — there is no job/work-order data anywhere, and the live quotes
   live in a *different* table (`ehow.public.sks_quotes`, Flask app) than the canonical `app_data.quote`.
4. **Worker → Field-person cannot be traced** — `app_data.staff.cards_worker_id` = **1/50**, legacy
   `ktmj.people.worker_id` = **0/605**. The columns exist; the data doesn't.
5. **Identity is broken at GATE A** — only **4 of 38 workers** have a `user_id`; `shell_control.users` has **5 rows**
   (managers only). 50+ worker invites can't be claimed. Unresolved (decision recorded, fix on a branch).
6. **Customer identity is fragmented across 3–4 stores** (`sks_customers` 520, `sks_quotes_customers` 520,
   `app_data.customers` 389, + nspb copies). The `canonical_id` back-link is **0/520** in the live ehow public store.
7. **What *does* work:** Service→canonical **asset sync is live** (4808 assets, 100% linked to a site);
   Quotes→canonical **customer dual-write + event emission** works; Shell **SSO + tenant routing** is solid;
   `nspb.people.canonical_id` is **49/60** populated (the SKS field roster *is* partially bridged).
8. **Service runs off-topology** on `urjhmkhbgaxrofurpbgc` (shared with the substrate), linked only by `eq-service:*`
   external_ids resolved at the canonical-api layer.
9. **Drift from docs:** worker-credential count dropped 779→737, invites 37→58 since 2026-06-03;
   `architecture.md`'s "jvkn holds no operational data" is **false** (it holds the worker HR house);
   `0028_contact_customer_links` is now present on SKS (`app_data.contact_customer_links` = 291), contradicting the
   06-02 "missing on SKS" claim. Live wins.
10. **Highest-leverage fix:** resolve GATE A + backfill `cards_worker_id` (worker traceability) and decide a single
    canonical customer home + backfill `canonical_id` (customer traceability). Both are MEDIUM effort. The job/quote
    trace is LARGE and needs an architectural decision (who owns "job/work-order").

---

## 1a. Steelman corrections (post red-team + extra live queries, 2026-06-07)

A red-team review + two follow-up queries (the EQ tenant plane `zaap`, and customer name/ABN matching)
corrected five things below. **Where this section conflicts with the body, this section wins.**

1. **Customers are NOT disjoint — they reconcile 519/520 by name.** §5a's "only 49 match → disjoint" tested
   `external_id` (different surrogate schemes). By **exact normalized company name**, `sks_quotes_customers` →
   `app_data.customers` matches **519/520** (`abn` is empty in both — 0 usable). So it's **one customer population
   under different surrogate keys**, not separate populations. **Caveat (dry-run 2026-06-07):** of those 519,
   **481 are *ambiguous*** — `app_data.customers` is itself un-deduped (389 rows, 270 distinct names, **117
   duplicate-name groups**); only ~38 map 1:1, `abn` is 0/unusable. So the real first step is **deduping the canonical
   customer table** (Intake's job); the cross-store backfill is downstream of that. Net: still one population, but
   reconciling it is **MEDIUM-LARGE**, not a plain backfill. Biggest correction (in two layers).
2. **"No job/work-order data anywhere" overclaimed.** Canonical `app_data.jobs` and `app_data.quote` are empty on
   **both** tenants (0/0) — that holds. But job-like data **exists** app-natively: `nspb.job_numbers` 23,
   `nspb.tenders` 380, `zaap.field_tenders` 323, Service `maintenance_checks` 35 / `job_plans` 54. Correct framing:
   **the canonical work-order layer is empty scaffolding; job-like data is fragmented across app-native tables and
   never flows into it.** Quote→job is untraceable *through canonical*, not because no jobs exist.
3. **`zaap` (EQ tenant plane) queried — EQ is largely converged; SKS is the laggard.** `zaap.app_data` has populated
   canonical entities (`customers` 50, `staff` 26, `schedule_entries` 500, `timesheets` 75, `licences` 29) **and** the
   secured `field_*` JWT twins (`field_tenders` 323…). So "model built but empty" is **only true for SKS (`ehow`)**.
   Convergence is **asymmetric** — the gap is SKS, not the suite.
4. **Security severity was inverted — corrected.** **`nspb` (SKS LIVE) anon-write on live PII is the top item**, not
   `ktmj`. But note: `ktmj` is **confirmed `ACTIVE_HEALTHY` (not paused) on 2026-06-07** — so its 605 anon-writable PII
   rows are a **live exposure now**, even though the live app no longer uses it → **MEDIUM-HIGH** (legacy data, but
   reachable); decommission is the fix and is **still pending**. `tenant_routing` key concentration is the **highest
   structural** risk. (Also: the Service DB `urjhmkhbgaxrofurpbgc` is named `eq-solves-service-dev` — a dev project
   that co-hosts the substrate.)
5. **Service DB WAS audited (S6 correct).** The "not audited" lines in §2/Appendix are stale — superseded by S6
   (RLS on all 56 tables; only intentional append-only anon-INSERT; no anon UPDATE/DELETE on PII).

Minor: `sks_quotes` base drifted 34→35 between queries; `app_data.customers` carry `external_id` 100%.

---

## 2. Topology — projects, roles, deploy targets (verified)

| Project ID | Alias | Role (verified) | Schemas of interest |
|---|---|---|---|
| `jvknxcmbtrfnxfrwfimn` | **eq-canonical** | Control plane + **identity/worker house** + SSO | `public` (workers, credentials, licences), `shell_control` (users, tenant_routing) |
| `ehowgjardagevnrluult` | **sks-canonical** | **SKS tenant data plane** (`app_data`) **and** live Flask Quotes store (`public.sks_quotes_*`) | `app_data` (canonical CRM/CMMS), `public` (quotes domain) |
| `nspbmirochztcjijmcrx` | **sks-labour** (SKS LIVE) | SKS NSW Labour / Field app DB — serves `core.eq.solutions/sks/field` | `public` (people, schedule, timesheets, tenders, + legacy quotes copy) |
| `ktmjmdzqrogauaevbktn` | **eq-solves-field** | **Legacy/demo** Field DB — superseded by per-tenant routing | `public` (people, sites, tenders) |
| `urjhmkhbgaxrofurpbgc` | eq-solves-service host (+ substrate) | EQ Service standalone DB — **off canonical topology** | `public` (customers, sites, assets, tests) — *not audited* |
| `zaapmfdkgedqupfjtchl` | eq-canonical-internal | EQ-tenant data plane (`app_data`) — EQ tenants route here | *referenced, not directly queried* |

**Deploy fact (re-confirmed):** `core.eq.solutions/sks/field` is the **sks-nsw-labour** repo on **`nspb`**, NOT
`eq-solves-field`/`ktmj`. `ktmj` is the legacy standalone DB; live Field operational data for EQ tenants routes to
`zaap.app_data`, for SKS to `nspb.public`.

---

## 3. Live database audit (per project)

### 3.1 eq-canonical (`jvkn`) — identity / worker house
RLS: ON for all public tables. `public` row counts (live 2026-06-07):

| Table | Rows | Key linkage cols |
|---|---|---|
| `workers` | **38** | `user_id` (→ auth/shell user; **4/38 populated**), `staff_id` (0/38) |
| `worker_credentials` | 737 | `worker_id`→workers, `promoted_licence_id`→licences |
| `worker_invites` | 58 | `worker_id`→workers, `org_id`→organisations |
| `licences` | 7 | `source_worker_cred_id`→worker_credentials, `source_org_id` |
| `org_memberships` | 5 | `user_id`, `org_id`, `tenant_id` |
| `tenants` / `organisations` | 4 / 4 | `org.id == tenant.id` (1:1, verified) |
| `worker_assignments` | **1** | `tenant_id` + `tenant_supabase_ref` (TEXT) — the cross-tenant "subbie at tenant X" link, **effectively unused** |

`shell_control` schema (the SSO + routing spine): `users` **5**, `user_tenant_memberships` **5**, `user_invites` 3,
`cards_field_approvals` **2**, `tenant_routing` (per-tenant DB registry, encrypted keys), `mint_audit_log` 1279,
`security_groups`/`security_group_perms`/`user_security_groups`, `tenant_config`, `iframe_salt_registry`.

> **GATE A (live):** `workers.user_id` populated 4/38; `shell_control.users` = 5. The worker→identity bridge is
> ~unbuilt in data → onboarding claim is broken for ~all workers.

### 3.2 sks-canonical (`ehow`) — SKS tenant plane + Quotes
Two distinct worlds in one project:

**`app_data` (the canonical tenant plane — fully FK-wired):**

| Table | Rows | Notes |
|---|---|---|
| `customers` | 389 | `external_id` **389/389** (all imported); `tenant_id` scoped |
| `contacts` | 331 | `customer_id`→customers (FK) |
| `contact_customer_links` | 291 | the `0028` link table — **present on SKS** (contradicts 06-02 doc) |
| `sites` | 591 | `customer_id`→customers (FK) — **only 28/591 populated** |
| `staff` | 50 | `cards_worker_id` (→ Cards worker; **1/50**), `user_id` (1/50), `default_site_id`→sites |
| `licences` | 3 | `cards_credential_id` (→ Cards credential; **2/3**), `staff_id`→staff |
| `jobs` | **0** | FK `customer_id`→customers, `site_id`→sites; **`quote_id` is a soft col (no FK)** |
| `quote` / `quote_line_item` | **0** / 11 | canonical quote domain — **empty** (live quotes are in `public.sks_quotes`) |
| `assets` | **4808** | `site_id`→sites **4808/4808 (100%)**; `parent_asset_id` self-FK — **Service sync, populated** |
| `asset_test_results` | 713 | `asset_id`→assets |
| `tenders` | (low) | `customer_id`→customers |
| `schedule_entries`, `timesheets` | (low) | `staff_id`→staff, `site_id`→sites — canonical copies, **separate from nspb live** |
| `canonical_events` | (event log) | `tenant_id` — the cross-app event sink |

**`public` (Flask Quotes domain — the LIVE quotes store):** `sks_quotes` 34, `sks_quotes_customers` 520
(`canonical_id` **0/520**, `canonical_field_id` **0/520**), `sks_quotes_contacts` 331, `sks_customers` 520
(`external_id` 517/520), `sks_staff`, full pricing/materials/rates set. `sks_quotes.customer_id`→`sks_quotes_customers` (FK).

### 3.3 sks-labour (`nspb`) — SKS LIVE Field/Labour
`public` (RLS ON): `people` **60** (`canonical_id` **49/60** ✅), `sites` **34** (`canonical_id` **24/34** ✅),
`schedule` 761, `timesheets` 183, `tenders` 380, `managers` 27, `teams` 2 / `team_members` 11, `pipeline_events`,
`job_numbers` 23, `leave_requests` 60. **Plus a legacy copy of the quotes schema**: `sks_quotes` 14,
`sks_quotes_customers` 518 (`canonical_id` **518/518** ✅) — frozen pre-cutover snapshot. FKs are internal
(person/site/tender). See S2 for anon-write exposure.

### 3.4 eq-solves-field (`ktmj`) — LEGACY demo DB
`public` (RLS ON, but see S1 anon policies): `people` **605** (`worker_id` **0/605**, `cards_staff_id` **0/605**),
`sites` 56, `qualifications` 0 (`cards_licence_id` 0), `field_customers` 0, `projects` 12, `schedule`, `tenders` 333,
`timesheets` 1. The `people.worker_id`/`cards_staff_id`/`qualifications.cards_licence_id` columns are the intended
Cards/canonical bridge — **0% populated**.

---

## 4. Code-seam audit (per repo)

| Repo | Branch (checked out) | Connects to | Reads | Writes | Cross-app mechanism |
|---|---|---|---|---|---|
| **eq-cards** | `claude/cards-otp-fix-minimal` | `jvkn` only (legacy `hshvn…` decommissioned, comment-only) | `profiles`, `licences`, `worker_credentials`, `worker_invites`, `org_memberships`, `licence_types`, `certificates` | same (via `eq_cards_*` RPCs) | **Emits no events.** Phone-OTP → Shell `shell-login-phone-otp` for tenant resolution; `eq_cards_claim_invite` writes `shell_control.users` + `user_tenant_memberships` |
| **eq-shell** | `claude/worker-linker-schema-fix` | `jvkn` (`shell_control`) + every tenant plane via `tenant_routing` + `ktmj` (Field bridge) | tenants, users, memberships, routing; tenant `app_data.*`; `canonical_events` | `canonical-api` writes `customers/contacts/sites/staff/licences/jobs/assets` into tenant `app_data`; **`cards-approve-staff` writes `people`+`qualifications` into `ktmj`** | **SSO authority.** Mints `aud=field` JWT (`#sh=`), CORS-gated iframes. Hosts the `canonical_events` POST endpoint |
| **eq-quotes-port** | `claude/mobile-fixes` | `ehow` (live, per `config.py`; `.env.example` still names `nspb` — pre-cutover) via **service_role** | `sks_quotes_*`, `sks_customers`, `sks_contacts`, `sks_staff` | same + **dual-write customers → `sks_customers` (canonical_id back-write)** | **HTTP**: PUT customer sync + POST `quote.created/sent/accepted/declined/expired` to `canonical-api`; **HMAC GET** Field `/api/eq-service/sites` (links via `canonical_field_id`); ABR lookup |
| **eq-solves-service** | `claude/posthog-canonical-distinct-id` | **`urjhmkhbgaxrofurpbgc`** (off-topology) via anon+service key | own `customers/sites/assets/*_tests/defects/maintenance_checks` | same; stamps `canonical_id` after sync | **HTTP PUT/POST** to `canonical-api` (`eq-service:*` external_ids); emits `defect.created/resolved`, `maintenance_check.completed/overdue`. No DB-to-DB link |
| **eq-solves-field** | `revert/licence-admin` | `jvkn` (boot config) + tenant plane (`zaap` EQ / `nspb` SKS) resolved from `organisations` registry | `people/schedule/sites/timesheets/tenders/...` (tenant-scoped) | same | **postMessage-only** to Shell (`core.eq.solutions`); Realtime on `app_data:field_schedule/leave_requests/roster_presence`; `verify-pin` mints data JWT. Tenders reference sites **within same tenant** (no cross-project ID) |

**The event bus, concretely:** Quotes, Service, Field, Cards, Shell each hold a `CANONICAL_API_KEY_*` and POST events
to Shell's `canonical-api`, which writes `canonical_events` in the target tenant's `app_data`. Read side:
`ai-briefing.ts` (last 72h, per-tenant) and `tenant-dashboard.ts`. **No cross-tenant fan-out, no webhooks, no
Realtime across apps.** Cards emits nothing. (Field's `shift.started` emitter was demo/seed until the 06-07 build.)

---

## 5. Linkage map — every core entity

Legend: **SoR** = system of record. ✅ live & populated · ⚠️ partial · ❌ designed not populated / absent.

| Entity | Created in | Authoritative store(s) — verified rows | Read by | Written by | Cross-app ID | Status & gap |
|---|---|---|---|---|---|---|
| **Worker (HR)** | Cards | `jvkn.public.workers` (38) | Shell, (Field intended) | Cards | `workers.user_id`→shell user **4/38** | ⚠️ identity bridge ~empty (GATE A) |
| **Identity (login)** | Shell | `jvkn.shell_control.users` (5) | all apps (JWT) | Shell, Cards (claim) | JWT `tenant_id`/`eq_role` | ⚠️ 5 users = managers only; workers can't claim |
| **Licence/credential** | Cards | `jvkn` `worker_credentials` (737) / `licences` (7); canonical `app_data.licences` (3, `cards_credential_id` 2/3) | Field (intended) | Cards | `licences.cards_credential_id` | ⚠️ promoted at claim; canonical copy ~empty |
| **Tenant / org** | Shell | `jvkn.public.tenants` (4) = `organisations` (4); `shell_control.tenant_routing` | all | Shell | `org.id == tenant.id` | ✅ built & consistent |
| **Customer** | Quotes / Service / intake | `ehow.public.sks_customers` (520) **+** `sks_quotes_customers` (520) **+** `ehow.app_data.customers` (389) **+** nspb copies | Quotes, Shell, Service | Quotes (dual-write), Service, canonical-api | `external_id` strings; `canonical_id` **0/520** in live store | ❌ **fragmented across 3–4 tables**, back-link unpopulated |
| **Site** | Field / Service / intake | `ehow.app_data.sites` (591); `nspb.public.sites` (34, canonical_id 24/34); `ktmj` (56) | Quotes (HMAC pull), Service, Field | Service, Field, canonical-api | `sites.customer_id` **28/591**; `nspb.sites.canonical_id` 24/34 | ❌ **95% of canonical sites orphaned from customer** |
| **Contact** | Quotes / Shell | `ehow.public.sks_quotes_contacts` (331); `ehow.app_data.contacts` (331) + `contact_customer_links` (291) | Quotes, Shell | Quotes (dual-write) | `external_id` `eq-quotes:{uuid}` | ⚠️ dual store; canonical link table present |
| **Quote** | Quotes (Flask) | `ehow.public.sks_quotes` (34) — **live**; `app_data.quote` = **0** | — (Field/Service do **not** read quotes) | Quotes | `quote.*` events → `canonical_events`; `canonical_id` 6/35 | ❌ **canonical quote table empty**; Field/Service can't see quotes |
| **Job / work-order** | *(no owner)* | `ehow.app_data.jobs` = **0** | — | — | `jobs.quote_id` (soft), `customer_id`/`site_id` (FK) | ❌ **does not exist as data** — no quote→job→timesheet trace |
| **Asset** | Service | `ehow.app_data.assets` (**4808**) | Shell briefings | Service → canonical-api | `external_id` `eq-service:asset:*`; `site_id` **4808/4808** | ✅ **live & fully linked to site** (best-wired seam) |
| **Schedule / timesheet** | Field | `nspb.public.schedule` (761) / `timesheets` (183) [SKS live]; `app_data.*` (separate, low) | Field, Shell briefing | Field | — (siloed in tenant) | ⚠️ live data in `nspb`, not in canonical `app_data` |
| **Tender (pipeline)** | Field | `nspb.public.tenders` (380); `app_data.tenders` | Field | Field | `tenders.customer_id` (app_data only) | ⚠️ siloed; not linked to quotes |

---

## 5a. Reconciliation mechanics — how apps reconcile with the canonical layer (live dry-run)

Two regimes, verified by live joins on `ehow` (2026-06-07):

**Regime 1 — intra-canonical (`app_data`): hard FK, clean.** Inside the tenant plane, entities reconcile by enforced
FK on UUID PKs (`sites.customer_id`→`customers`, `assets.site_id`→`sites`, `jobs`→`customers`/`sites`, etc.). Where
rows exist, the join is exact. This is why `assets`→`sites` is 4808/4808.

**Regime 2 — cross-app (app store → canonical): soft `external_id` + HTTP, lossy.** Each app owns its own UUIDs and
hands canonical a **namespaced `external_id`** through `canonical-api`, which resolves it to a canonical UUID
server-side. Reconciliation only works if the app's `external_id` scheme matches what canonical already holds — and
that is where it breaks:

| Reconciliation question (live) | Result | Reading |
|---|---|---|
| `sks_customers` vs `sks_quotes_customers` (same rows?) | **520/520 identical ids** | One logical set in two tables (Quotes dual-write, same UUID) — **not** two customer populations |
| Quotes customers (520) ↔ canonical `app_data.customers` (389) by `external_id` | **only 49 match** | **Disjoint, differently-keyed populations.** `app_data` ext-ids are hashes (`1842d1a8…`, from intake/SimPRO); Quotes ext-ids are short numerics (`530`). Schemes don't align |
| …by `workbench_customer_id` | **0 match** | Workbench id is not a usable bridge |
| `app_data.sites` resolvable to a customer by `external_customer_id`→`customers.external_id` | **440 / 591** (28 already linked, 50 have no key) | **Clean backfill available** — one UPDATE takes site→customer from 28 → ~468 |
| Worker (`jvkn.workers`) ↔ canonical `app_data.staff` | **1 / 50** | Identity reconciliation, matched by **email** per the approved `worker-identity-linker-spec-2026-06-07.md` |

**Consequences for the backfills:**
- **P2 (customer) is a dedup/merge, not a backfill.** Only ~49/520 auto-resolve by key; the rest need fuzzy
  (name/ABN) matching — which is exactly **EQ Intake's dedupe job** (`eq/pending.md` "Dedupe Is Intake's Job"; the
  SimPRO 524→~150 collapse). Re-scope P2 from MEDIUM to **MEDIUM-LARGE**, route through intake's dedupe, don't
  hand-match 471 customers.
- **P3 (site→customer) is a genuine quick win** — 440 resolvable today by a clean `external_id` join.
- **Identity reconciliation is owned** by the approved worker-identity-linker spec (email-keyed).
- **The canonical-api is the single reconciliation chokepoint** — every cross-app link is resolved there by
  `external_id`. Fixing fragmentation = aligning `external_id` schemes (or adding a crosswalk) so writes land linked
  instead of orphaned.

---

## 6. Gap analysis & priority order

Effort: **S**=1 migration + backfill · **M**=schema + UI/code + backfill · **L**=cross-app event/entity design.

| Pri | Gap | Impact | Effort | Depends on |
|---|---|---|---|---|
| **1** | **GATE A + worker→staff link** — `workers.user_id` 4/38; `app_data.staff.cards_worker_id` 1/50; `ktmj.people.worker_id` 0/605 | Can't trace a worker from Cards → Field roster → timesheet. Onboarding claim broken. | **M** | GATE A decision (already made: provision-at-claim, branch `claude/otp-tenant-fix`) → then backfill `cards_worker_id`/`staff.user_id` |
| **2** | **Single canonical customer + backfill `canonical_id`** — 3–4 customer stores; `sks_quotes_customers.canonical_id` 0/520 in live ehow | Customer identity fragmented; can't join a quote's customer to the CRM/Service customer | **M** | Decide SoR = `app_data.customers` (recommended) vs `sks_customers`; run the dual-write backfill the Quotes app already supports |
| **3** | **Site→customer backfill** — only 28/591 `app_data.sites` carry `customer_id` | Sites (and their 4808 assets) can't roll up to a customer | **S–M** | #2 (need deduped customer ids); map via `sites.external_customer_id` |
| **4** | **Cards→Field approval bridge points at legacy `ktmj`** — Shell `cards-approve-staff` writes `ktmj.people`, but live Field reads `nspb`/`zaap.app_data` | Approved staff land in the wrong DB; `cards_field_approvals` only 2 rows | **S** | Repoint `FIELD_SUPABASE_URL`, or route via `canonical-api` into `app_data.staff` (the real target) |
| **5** | **Quote → Job entity** — `app_data.jobs` = 0 and `app_data.quote` = 0; live quotes sit in `public.sks_quotes` | The headline "quote → job → timesheet" trace is impossible; no work-order concept exists | **L** | Architectural decision: who owns "job/work-order"? Then `quote.accepted` event → create `app_data.jobs` row (`quote_id` link already modelled) |
| **6** | **Field-live (`nspb`) data not in canonical plane** — people/schedule/timesheets in `nspb.public`, separate from `app_data`; `nspb.people.canonical_id` 49/60 is the only bridge | SKS operational reality lives outside the convergence target | **L** | SKS cutover (already a 5-phase gated project — `SKS-CUTOVER-CRITICAL-PATH.md`) |
| **7** | **Security remediation S1–S2** — anon-write policies on `ktmj` + `nspb` | PII tamper / cross-row write with a leaked anon key | **S–M** | Complete Field Phase-1 JWT migration; drop always-true policies on legacy tables |

**Recommended sequence:** **#4 (S, unblocks correctness) → #1 (M, highest leverage for worker trace) → #2+#3
(M, customer/site trace) → #7 (security) → #5 (L, needs the job-owner decision) → #6 (L, SKS cutover).**
The canonical model is already built — the work is **populating the bridge columns and choosing single owners**, not
redesigning schema. Two leverage points (worker identity, customer identity) unlock most of the suite-wide trace.

---

## 7. Drift from the design docs (live wins)

| Doc claim | Live reality (2026-06-07) |
|---|---|
| `verified-state-2026-06-03`: workers 38, creds 779, invites 37 | workers 38, creds **737**, invites **58** (creds −42, invites +21) |
| `worker-credentials-model`: worker house = `eq-canonical-internal` (`zaap`) | Worker house = **`jvkn.public`** (control plane). Confirmed. |
| `architecture.md`: "`jvkn` = control layer only, no operational data" | **False** — `jvkn.public` holds workers/credentials/licences (operational HR data) |
| `platform-architecture-audit-2026-06-02`: `0028_contact_customer_links` "applied on EQ, missing on SKS" | **Present on SKS** — `ehow.app_data.contact_customer_links` = 291 rows |
| Quotes `.env.example` → `nspb` (sks-labour) | Live store is **`ehow`** (sks-canonical) per `config.py`; `nspb` holds a frozen pre-cutover copy |
| Identity-convergence target: app_data is the converged home | Model is built but **`jobs`/`quote` empty, `staff.cards_worker_id` 1/50** — convergence is schema-complete, data-incomplete |

---

## Appendix — method & caveats

- **Tools:** Supabase MCP `execute_sql` (table inventory via `pg_class`, FKs via `information_schema`, `_id`/`canonical`
  columns, targeted `count(*)` population), `get_advisors(security)` on all four; 5 read-only repo code-seam agents.
- **Read-only.** No writes, no DDL, nothing executed against any tenant DB. SKS-live (`nspb`) accessed read-only under
  the explicit instruction to inventory it.
- **Row counts** are exact `count(*)` where cited as N/M; the §3 inventory uses `pg_class.reltuples` estimates
  (shown `-1` where a table was never analyzed) — re-`ANALYZE` for exact figures if needed.
- **Not covered:** `urjhmkhbgaxrofurpbgc` (Service DB, outside the 4 IDs — recommend a follow-up), `zaap`
  (EQ-tenant `app_data`, inferred from routing not queried), storage-bucket grants.
- This snapshot **will drift.** Re-verify against live before relying on any number. When docs and live disagree,
  live wins.
