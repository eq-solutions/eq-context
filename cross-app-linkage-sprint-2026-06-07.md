---
title: SPRINT — Cross-App Linkage Convergence
date: 2026-06-07
status: ready — execution gated per item
sources: cross-app-linkage-audit-2026-06-07.md (+ §1a steelman corrections), cross-app-linkage-remediation-plan-2026-06-07.md
owner: Royce Milmlow
rule: every executable step is GATED. Nothing in this sprint has been run. Tenant-plane DDL via the One Pipe
  (eq-shell tenant-migrate.yml); nspb via sks-nsw-labour repo; ktmj via eq-solves-field repo. SKS-live untouchable
  without "SKS live". Auth changes need chat review. No deploy/commit without explicit go.
---

# SPRINT — Cross-App Linkage Convergence

**Goal:** make every core entity traceable across the suite by **one canonical ID** — customer → site → quote → job →
asset/visit → timesheet, and worker → roster → licence — by *populating the bridges and collapsing the duplicate
representations*, not by redesigning the (already-built) canonical schema.

This sprint is built on the **steelmanned** facts (audit §1a). The three corrections that shaped it:
- Customers reconcile **519/520 by name** → keystone backfill is tractable, not a research project.
- The canonical **work-order layer (`jobs`/`quote`) is empty on both tenants** → the one genuine *new-build*.
- Convergence is **asymmetric**: EQ (`zaap`) roster is converged; **SKS (`ehow`/`nspb`) is the laggard**.

---

## The target end-state (the 10/10 architecture)

One identity per entity, every app referencing the canonical UUID; app-local tables become **caches keyed by
`canonical_id`, never parallel sources of truth**:

| Entity | Single SoR | All apps reference | Ingest path |
|---|---|---|---|
| Customer | `app_data.customers.customer_id` | Quotes, Service, Field, Shell | **EQ Intake dedupe** (the only writer of *new* customers) |
| Site | `app_data.sites.site_id` (always has `customer_id`) | all | Intake / Service / Field → canonical-api |
| Contact | `app_data.contacts` (FK `customer_id`) | Quotes, Shell | Intake / Quotes dual-write → canonical |
| Worker / identity | `jvkn.workers.id` (`user_id` + `staff_id` linked) | Cards, Shell, Field | **worker-identity-linker spec** (email-keyed) |
| Quote | `app_data.quote` (FK customer/site/contact) | Quotes owns; canonical mirror | Quotes → canonical-api |
| **Job / work-order** | `app_data.jobs` (`quote_id`, `customer_id`, `site_id`) | Field, Service reference it | **created on `quote.accepted`** (new) |
| Asset | `app_data.assets` (FK `site_id`) | Service owns; Shell reads | Service → canonical-api (already live, 4808) |

**Reconciliation principle:** the `canonical-api` is the single chokepoint. Every cross-app write resolves an
`external_id`/`canonical_id` to a canonical UUID there. Convergence = (a) backfill the resolutions that exist by a
better key (name/email), (b) make apps *read* canonical instead of keeping parallel stores, (c) make the event hop
**durable** so resolutions never silently drop.

---

## Workstreams (10/10 solution per item)

Effort: **S** ≈ 1 migration + backfill · **M** ≈ schema + code + backfill · **L** ≈ new entity / cross-app design.
Each lists the *steelman* (strongest objection) and why the solution still holds.

### WS1 — Customer identity convergence  ·  effort **M–L**  ·  **PARTIAL ✅ 2026-06-07 (safe subset)**
**✅ APPLIED (ehow, reversible — record `_ws1-customer-dedup-2026-06-07.md`):** Tier S = **38 stub customers
retired** (`active=false`; active dup-groups 117→80, 0 emptied); **28** `sks_quotes_customers.canonical_id` linked
(1:1-both-sides only). **Finding:** `canonical_id` is UNIQUE (1:1) but quotes side is N:1 → ~65 more need quotes-side
dedup. **HELD:** Tier A (26 groups, FK-repoint merge — supervised), Tier C (50 ambiguous — Intake/review).
**Now (dry-run verified 2026-06-07):** the same SKS customers exist as `app_data.customers` (389) and
`sks_quotes_customers` (520, = `sks_customers`, same UUIDs); `canonical_id` 0/520. **519/520 match a canonical name —
but 481 are AMBIGUOUS** because `app_data.customers` is itself un-deduped: 389 rows → **270 distinct names**, **117
duplicate-name groups** (`health infrastructure` ×3, `abb australia pty ltd` ×2, fuzzy `bgis anz pty ltd`/`bgis pty
ltd`, empty-name ×3, a `zz Test Company` row). **Only ~38 map 1:1.** A plain name-backfill is therefore unsafe — the
canonical side must be deduped first.
**10/10 solution (dedup canonical FIRST, then backfill):**
1. **Designate `app_data.customers` the single SoR** (decision — recommended).
2. **Dedup `app_data.customers`** — collapse the 117 duplicate-name groups (exact + fuzzy `bgis*`; drop empty/test
   rows) via **EQ Intake's dedupe** (literally its job — the SimPRO 524→~150 collapse). This makes the name key 1:1.
3. **Then backfill** `sks_quotes_customers.canonical_id` against the deduped set (now mostly 1:1; review residual
   ambiguity). Use the Quotes `backfill_customers()` helper, not hand-SQL.
4. **Flip Quotes to *read* canonical**; `sks_quotes_customers` becomes a `canonical_id`-keyed cache.
5. **Route all *new* customers through Intake dedupe** so the fork can't reopen; populate `abn` during dedup as the
   future deterministic key (empty today → unusable now).
**Steelman (CONFIRMED, not hypothetical):** the false-merge risk is **real at 481 ambiguous**, and ABN can't rescue it
(0 populated). That is *why* canonical dedup precedes the backfill — never auto-assign a `canonical_id` where a name
maps to >1 surviving customer.
**Mechanism:** Quotes (Flask) repo + `ehow` backfill. **Gate:** SoR decision + dry-run review. **Verify:**
`sks_quotes_customers.canonical_id` 0→~519; new Quotes customer appears in `app_data.customers` with one UUID.
**DoD:** every quote's customer resolves to exactly one `app_data.customers.customer_id`.

### WS2 — Site → customer + asset rollup  ·  effort S  ·  **✅ APPLIED 2026-06-07 (ehow)**
**✅ DONE (ehow):** 440 sites backfilled → linked **28→468**; **assets→customer 4769/4808 (99.2%)**. Deterministic
(unique `external_id`), FK-validated, reversible — record + rollback in `_ws2-site-customer-backfill-2026-06-07.md`.
Remaining 123 sites (101 quotes-side + 22 keyless) wait on WS1. **`zaap` (EQ, 30 sites) not yet run — small, on request.**
**Pre-state:** `app_data.sites` 591, only **28** carried `customer_id`; **440 resolvable** by `external_customer_id` →
`customers.external_id`; 4808 assets hang off sites (100%).
**10/10 solution:** backfill the 440 (one UPDATE on `ehow`, mirror on `zaap`); triage the ~123 unmatched + 50
keyless via WS1's name crosswalk; add a **NOT-NULL-on-write** rule (canonical-api rejects a site without a customer)
so it stays linked. Once done, **all 4808 assets trace to a customer** for free (asset→site→customer).
**Steelman:** *`external_customer_id` may point at a customer that WS1 is about to merge/retire.* Mitigation: run WS2
**after** WS1's crosswalk so site links land on the surviving canonical id.
**Mechanism:** `ehow`/`zaap` backfill via canonical-api. **Gate:** depends on WS1. **Verify:**
`sites.customer_id` 28→~468; `select count(*) from assets a join sites s using(site_id) where s.customer_id is null` → 0.
**DoD:** every asset rolls up to a customer.

### WS3 — Worker identity  ·  effort M  ·  **DEFER — already owned**
**Owned by** `worker-identity-linker-spec-2026-06-07.md` (APPROVED-FOR-BUILD, concurrent session): M1
`user_invites.worker_id`, M2 FK `workers.user_id`, M3 `workers.staff_id`, unified invite, `accept-invite` linking,
Phase-5 email-keyed backfill of the 35 orphans.
**This sprint's only job:** track it + resolve **one** reconciliation point — `workers.staff_id` (jvkn→ehowg) and
`app_data.staff.cards_worker_id` (ehowg→jvkn) **both exist**; pick which is authoritative (or keep both in sync via
the linker) so the worker↔staff link isn't half-populated each direction.
**Gate:** auth — chat review (that spec's gate). **Verify:** `workers.user_id` 4→~37; `staff.cards_worker_id` →
matched count. **DoD:** a worker traces Cards → `app_data.staff` → roster.

### WS4 — Canonical work-order spine  ·  effort L  ·  **the one real new-build (decision-first)**
**Now:** `app_data.jobs` = 0 and `app_data.quote` = 0 on **both** tenants; job-like data is scattered
(`nspb.job_numbers` 23, `nspb.tenders` 380, `zaap.field_tenders` 323, Service `maintenance_checks` 35/`job_plans` 54).
**10/10 solution:**
1. **Decide the owner** of "job/work-order" (recommended: a thin canonical `app_data.jobs` is the spine; app-native
   tables become *sources/views* into it, not competitors).
2. On `quote.accepted` (Quotes already emits this event → canonical-api), **create an `app_data.jobs` row** with
   `quote_id` + resolved `customer_id`/`site_id` (WS1/WS2 make these resolvable).
3. Map the app-native work tables to it: `field_tenders`/`job_numbers`/`maintenance_checks` reference `job_id`.
**Steelman:** *building a job spine nobody reads is speculative.* Mitigation: scope v1 to **only** the
quote→job→timesheet trace that's actually asked for; don't migrate Service/Field jobs until a workflow consumes the
spine. Empty-by-design is fine until step 2 fires.
**Mechanism:** eq-shell `canonical-api` handler + `app_data` migration via One Pipe. **Gate:** owner decision (Royce)
→ then non-auth deploy. **Verify:** accept a quote → `jobs` row appears with `quote_id` set; timesheet → job → quote
joins. **DoD:** one accepted quote traces to a job to a timesheet.

### WS5 — Durable event bus  ·  effort M  ·  **reliability of everything above**
**Steelman of the current design (and why it matters):** every cross-app link rides a **fire-and-forget HTTP POST to
`canonical-api` whose failures are swallowed** (audit §4; Quotes/Service "never block"). `canonical_events` holds only
**32 rows** per tenant. So the reconciliation fabric **silently drops** events under any canonical-api outage — and
you can't tell what was lost.
**10/10 solution:** **transactional outbox** — each app writes the event into a local `outbox` row *in the same
transaction* as the business change, then a worker delivers to canonical-api with **retry + idempotency key**; mark
delivered on 2xx. Add a tiny **consumer registry** + replay. This converts "best-effort sync" into "eventually
consistent, never lost."
**Steelman of the fix:** *outbox is over-engineering for 32 events.* Counter: it's cheap (one table + a cron worker
each app already has the pattern for), and it's the difference between a traceable suite and one that *looks* linked
until an outage. Scope to the highest-value events first (`quote.accepted`, `customer.upserted`).
**Mechanism:** per-app (Quotes/Service/Field) + canonical-api idempotency. **Gate:** non-auth deploys. **Verify:**
kill canonical-api in staging, raise an event, restore → event delivers on retry, not lost. **DoD:** zero silent drops.

### WS6 — Security remediation (recalibrated)  ·  effort S–M
Ordered by **real** blast radius (corrected from the audit's inversion):
1. **`nspb` (SKS LIVE) anon-write on live PII = top.** Finish the Goal-1 JWT-twin pattern per table, then drop the
   always-true write policies (exact list: plan §7a). **Gate: "SKS live" + sks-nsw-labour repo.** **First verify the
   live SKS app doesn't depend on the anon path for those tables** (it's mid-migration) so the drop doesn't 401 prod.
2. **`tenant_routing` key concentration = highest *structural*.** Add **dual-key rotation** support for the routing
   master key + the per-tenant `service_role_key` (the audit's "single highest-value target"). No live exposure today;
   high cost if it leaks.
3. **`ktmj` = MEDIUM-HIGH (live now), closes on decommission.** Confirmed **`ACTIVE_HEALTHY` 2026-06-07 (not paused)**
   → the 605 anon-writable PII rows are reachable today. After WS7 repoints Cards→Field off it, **pause/decommission**
   (already a pending Royce-action) — that closes it wholesale. Until then it's a live legacy exposure, not moot.
4. **jvkn anon RPCs** — audit internal authz of `eq_cards_get_worker_hr_record` + `eq_cards_delete_account`.
5. **Service** — run `get_advisors` (inventory says clean; confirm with the linter).
**Steelman:** *dropping anon policies breaks the running Field app.* Exactly — hence "after JWT migration, per table,"
never a blanket drop.

### WS7 — Cards→Field bridge repoint  ·  effort S  ·  **do early (unblocks WS6.3 + WS3)**
**Now:** Shell `cards-approve-staff.ts` writes approved staff into **legacy `ktmj`**; live Field reads
`zaap.app_data` (EQ) / `nspb` (SKS). Misdirected (2 approval rows).
**10/10 solution:** route approvals through `canonical-api` into `app_data.staff` (which carries `cards_worker_id`) —
making it *the same write* as WS3's worker→staff link, not a separate path. Then `ktmj` has no consumer → WS6.3 can
decommission it.
**Mechanism:** eq-shell repo, PR + non-auth deploy. **Gate:** confirm live Field plane per tenant first. **Verify:**
test approval lands in `app_data.staff` with `cards_worker_id`; `ktmj` receives nothing.

---

## Execution waves (sequenced for dependencies + leverage)

| Wave | Items | Why this order |
|---|---|---|
| **Wave 0 (now, safe)** | dry-run WS1 name-crosswalk diff; WS6.5 Service advisor; WS6.3 confirm ktmj key state | read-only, zero-risk, de-risks the rest |
| **Wave 1 (small/unblockers)** | **WS7** (bridge repoint) · **WS2** (site backfill, after WS1 crosswalk) | smallest, highest-leverage; WS7 unblocks ktmj decommission + WS3 |
| **Wave 2 (keystone)** | **WS1** (customer convergence) · **WS3** track (worker linker spec lands) | the two identity backbones; everything downstream joins on them |
| **Wave 3 (reliability + security)** | **WS5** (durable bus) · **WS6.1** (SKS anon, gated) · **WS6.2** (key rotation) · **WS6.3** (decommission ktmj) | harden once the data flows are correct |
| **Wave 4 (new-build, decision-first)** | **WS4** (work-order spine) · SKS roster cutover (existing project) | LARGE; needs the owner decision + WS1/WS2 resolutions |

**Two MEDIUM moves (WS1 customer, WS3 worker) unlock the whole trace.** WS4 + SKS cutover are the LARGE,
decision-first tail.

---

## Pre-mortem (3 ways this sprint fails + mitigations)

1. **Name-match false merges corrupt customer identity — CONFIRMED LIVE: 481/520 ambiguous.** `app_data.customers`
   itself has 117 duplicate-name groups, so a naive name-backfill would mis-assign most quotes to the wrong canonical
   customer → wrong invoices/jobs downstream. **Mitigate:** dedup the canonical table FIRST (WS1.2, via Intake);
   backfill only against the 1:1 survivors; populate `abn` as the future deterministic key; never auto-assign where a
   name maps to >1 surviving customer.
2. **Security drop 401s the live SKS app.** Dropping `nspb` anon policies before its Field tables are on the JWT path
   takes prod down. **Mitigate:** per-table, only *after* the Goal-1 twin exists; verify the live app's read/write path
   for each table first; SKS-live gated, one table at a time, lowest-traffic first.
3. **WS4 builds a work-order spine nobody uses.** Effort sunk into `app_data.jobs` with no consumer. **Mitigate:**
   gate WS4 on the owner decision; ship v1 as *only* the quote→job→timesheet trace that's actually requested; leave
   Service/Field job migration until a workflow reads the spine.

---

## Definition of done (sprint-level)

- [ ] A quote's customer resolves to exactly one `app_data.customers.customer_id` (WS1).
- [ ] Every `app_data.asset` traces to a customer via site (WS2).
- [ ] A worker traces Cards → `app_data.staff` → roster (WS3, via the linker spec).
- [ ] An accepted quote produces a job that a timesheet references (WS4).
- [ ] No cross-app event is silently lost (WS5 outbox).
- [ ] SKS-live anon-write on PII closed; `ktmj` decommissioned; key-rotation support landed (WS6).
- [ ] Cards approvals land in the live plane, not `ktmj` (WS7).

## Out of scope / hard-gated (not in this sprint without explicit go)
- Any live DDL/DML, deploy, commit/push beyond the audit docs · auth deploys (WS3 spec's own gate) · **any `nspb`
  write** (needs "SKS live") · the full SKS roster cutover (its own 5-phase project).

---

## Appendix — Wave 0 dry-run results (read-only, 2026-06-07)

Ran the read-only diffs that decide whether the keystone backfills are safe. Verdicts below are live, not estimated.

**WS1 — customer crosswalk (`ehow`):**
- `sks_quotes_customers` 520 · name-match to `app_data.customers` **519** · **ambiguous (name → >1 canonical) 481** ·
  clean **1:1 ~38** · unmatched **1** (`zz Test Company`, a test row — ignore).
- Canonical `app_data.customers` 389 rows → **270 distinct names, 117 duplicate-name groups** (exact dups like
  `abb australia pty ltd` ×2, `health infrastructure` ×3; fuzzy like `bgis anz pty ltd` vs `bgis pty ltd`; empty-name
  ×3). **`abn` is 0-populated both sides → unusable as a key.**
- **Verdict:** the canonical customer table is itself un-deduped → that's the gate. Dedup canonical (WS1.2) **before**
  any quotes backfill. This is genuine Intake-dedup work, not a one-shot UPDATE.

**WS2 — site → customer (`ehow`):** 591 sites · 28 already linked · **440 auto-resolvable** by
`external_customer_id`→`customers.external_id` · **101** carry an ext-key that matches no canonical customer (they
reference quotes-side customers → unblock after WS1 dedup) · **22** have no key (manual).
- **Verdict:** ship the **440** now (clean); the 123 remainder resolve after WS1.

**Sequence implied:** WS2(440) ∥ WS1.2(canonical dedup) → WS1.3(quotes backfill) → WS2(remaining 123). The cleanest
immediate value is WS2's 440 site→customer links (and the 4808 assets that roll up behind them).

### Deeper dry-run findings (2026-06-07, read-only) — three things that change WS1/WS6

1. **WS1 canonical dedup is NOT auto-safe** — confidence tiering of the 117 dup-name groups: **tier-1 (shared non-null
   ABN, provably same) = 1; tier-2 (shared address, no ABN) = 0; tier-3 (name-only, no ABN/address) = 116.** So 116/117
   groups have *no positive evidence* of being the same entity beyond the name. Auto-merging them risks fusing distinct
   customers (financial corruption). **Verdict: WS1.2 must run through Intake's multi-signal dedupe (email/phone/
   contacts/quote-history) or human review — it is NOT a SQL name-merge.** Only the 1 shared-ABN group is trivially
   safe (not worth the FK-cascade machinery alone).
2. **The 123 still-unlinked sites are mostly NOT a dedup problem** — only **2** point at quotes-side customers; **99**
   carry an `external_customer_id` that exists in *neither* customer table (dangling/un-imported refs); 22 have no key.
   → finishing those needs a **source re-import** (Intake) of the missing customers, not WS1 dedup.
3. **WS6.4 security CLEARED** — the two anon-executable jvkn RPCs are self-scoped to `auth.uid()`
   (`eq_cards_get_worker_hr_record` = `WHERE user_id = auth.uid()`; `eq_cards_delete_account` only `WHERE id =
   auth.uid()`). Anon has no `auth.uid()` → harmless. The red-team's "anon HR-record reader" flag is a non-issue.
4. **`zaap` (EQ tenant) WS2 = already done** — 30/30 sites linked, 0 assets. EQ side needs nothing.
