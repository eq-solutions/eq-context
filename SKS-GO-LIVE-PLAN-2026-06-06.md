# SKS Go-Live — Field on Core, with Onboarded Users

**Prepared:** 2026-06-06 · **Owner:** Royce Milmlow · **Status:** proposed, pre-execution
**Supersedes framing of:** `SKS-CUTOVER-CRITICAL-PATH.md` (2026-06-04) — same goal, corrected against live.
**Ties in:** `eq/identity/onboarding-portable-identity-2026-06-04.md`, `eq/identity/gate-a-decision-2026-06-03.md`.

> Royce's framing: (1) build what's required to export live → EQ Field, (2) ensure it integrates within core → EQ Field, (3) settle the correct way to create user profiles, (4) execute. This plan maps that onto the verified system and steelmans it.

---

## 0. Verified ground truth (live, 2026-06-06)

The architecture is **per-tenant project**: control plane holds identity; each tenant gets its own Supabase project as its operational data plane. **Confirmed from the authoritative source — `shell_control.tenant_routing`:**

| Tenant (routed) | Data-plane project | Status |
|---|---|---|
| `core` (EQ Solutions) | `zaapmfdkgedqupfjtchl` (eq-canonical-internal) | active |
| `sks` (SKS Technologies) | **`ehowgjardagevnrluult` (sks-canonical)** | active |

| Project | ID | Role in this migration | `field_*` state |
|---|---|---|---|
| eq-canonical | `jvknxcmbtrfnxfrwfimn` | **control plane** (`shell_control`: identity, memberships, routing, entitlements) | n/a |
| eq-canonical-internal (`zaap`) | `zaapmfdkgedqupfjtchl` | **EQ/`core` tenant data plane** (not a shared spine) | 22 `field_*` in `app_data` |
| **sks-canonical** | `ehowgjardagevnrluult` | **SKS tenant data plane — the MIGRATION TARGET** | **0 `field_*`**; un-prefixed `app_data` schema (`staff`,`timesheets`,`schedule_entries`,`tenders`…), already **partly populated** — see below |
| sks-labour (legacy) | `nspbmirochztcjijmcrx` | **legacy SKS NSW Labour app — the MIGRATION SOURCE** (read-only; not in routing) | 0 `field_*`; legacy labour schema; anon-OPEN (§1) |
| eq-solves-field | `ktmjmdzqrogauaevbktn` | EQ Field app dev/demo only — **not** the spine | 2 `field_*` in `public` |

**⚠ Two findings that change Step 1 (verified live 2026-06-06):**

1. **EQ and SKS data planes use *different* schema conventions.** EQ (`zaap app_data`) = **22 `field_*` tables**. SKS (`sks-canonical app_data`) = **un-prefixed** (`staff`, `timesheets`, `schedule_entries`, `tenders`, `leave_requests`, `site_diaries`…). There is **no unified baseline** yet (this is the open gap from `sessions/handoff-canonical-tenant-baseline.md`). So "roll the canonical schema to SKS" is **not** a clean One-Pipe apply — the canonical shape itself isn't reconciled across tenants. **New decision required (§2a).**
2. **SKS canonical is already partly populated — the migration is a MERGE, not an import into empty tables.** Populated on `sks-canonical app_data`: `assets` 4,808 · `asset_test_results` 713 · `sites` 591 · `customers` 389 · `gm_report_jobs` 391 · `contacts` 333 · **`staff` 50** · `licences` 3 (this looks like live **EQ Service / CMMS + Quotes** data — SKS is *already* on core for those modules). The labour transactional tables are **empty and awaiting data**: `timesheets` 0 · `schedule_entries` 0 · `tenders` 0 · `leave_requests` 0 · `rotations` 0. **Critical:** legacy `people` (60) must reconcile against the **existing `staff` (50)** — overlap unknown — so identity reconciliation is needed in the *data plane* too, not only the control plane.

**SKS live rows (source `nspbmirochztcjijmcrx`):** `people` 60 · `schedule` 761 · `timesheets` 195 · `tenders` 383 · `leave_requests` 60 · `sites` 34 · `teams`/`team_members` 6/48. **Plus** SKS quotes: `sks_quotes_*` incl. `sks_quotes_contact_links` 13,929, `sks_quotes_customers` 518.

**Identity state (control plane):** `shell_control.users` = 5 (managers only) · `user_tenant_memberships` = 5 · `public.workers` = 38. **The 38 workers have no control-plane profile → GATE A.**

**Volume verdict:** the labour dataset is *tiny*. The mechanical move is trivial. **Every gram of risk is in correctness, identity, and auth — not throughput.** Royce's "it's basically export/import" instinct is right about effort distribution; this plan puts the effort where the risk actually is.

---

## 1. The security flag (urgent, independent of everything else)

On `nspbmirochztcjijmcrx`, RLS is *enabled* but the policies on `people`, `timesheets`, `schedule`, `tenders`, `leave_requests` grant role **`public`** (= anon key) full **SELECT/INSERT/UPDATE/DELETE** with `USING (org_id IS NOT NULL)` — always true.

> **Anyone holding the public anon key can read and write all live worker PII and timesheets.** App-level PIN/JWT is a front door; the database is unlocked.

The 2026-05-31 audit remediated **sks-*canonical*** (`ehowgjardagevnrluult`, the new routed data plane) — a *different* project. The **legacy source** (`nspbmirochztcjijmcrx`) was never done. `sks_quotes_customers` is the lone exception there (RLS on, 0 policies = deny-all, correctly locked).

**This is the legacy app's live DB** — still reachable with its anon key until the old SKS NSW Labour app is decommissioned (Step 4, end). Two valid responses: (a) lock it now (grant/revoke + tenant-RLS), or (b) accelerate decommission of the legacy app. Either way it should not sit open for the duration of the cutover. **Re-confirm the new target (`sks-canonical`) is still locked** before migrating into it.

---

## 2. Architecture — SETTLED (control vs data plane)

**Resolved by live `shell_control.tenant_routing`, not by doc-picking.** The earlier "shared spine into zaap" idea was wrong — `zaap` is the *EQ/core* tenant's data plane, not a shared home.

**The two-plane split (this is the answer to "is employee data in the control layer?"):**

| Plane | Project | Holds | In this migration |
|---|---|---|---|
| **Control** | `eq-canonical` `shell_control` | **Identity & access only** — `users`, `user_tenant_memberships`, `user_invites`, `security_groups`, `tenants`, `tenant_routing`, `module_entitlements` | **user profiles** (Step 3) land here |
| **Data (per-tenant)** | SKS → `sks-canonical` `app_data` | **Operational data** — `field_*` (people/schedule/timesheets/tenders) | **labour data** (Step 1) lands here |

> **Employee *operational* data is NEVER in the control layer.** The control plane stores only the employee's *identity* — one `users` row + `user_tenant_memberships` row(s) + entitlements. Their work records (timesheets, schedule, tenders) live in the SKS tenant's own data plane (`sks-canonical app_data`). The two link by `user`/`worker` id + `tenant_id`. This split is already implemented live; we are conforming to it, not inventing it.

**So the migration is, concretely:**
- **Source:** `nspbmirochztcjijmcrx` (legacy SKS NSW Labour app) — read-only.
- **Target (operational):** `ehowgjardagevnrluult` (`sks-canonical`) `app_data` — the routed SKS data plane. Target tables are the **un-prefixed** ones (`staff`, `timesheets`, `schedule_entries`, `tenders`, `leave_requests`…), **not** `field_*`. Several already hold data → **merge, not clean import**.
- **Target (identity):** `eq-canonical` `shell_control.users` + `user_tenant_memberships` (tenant = sks) — via the claim flow (Step 3).

Per-tenant isolation is structural (separate project per tenant) **and** RLS-enforced. SKS quotes (`sks_quotes_*`) are a separate module on the SKS plane and out of scope for the labour cutover.

### §2a — OPEN decision: schema convention for SKS (gates the ETL mapping)
EQ uses `field_*`; SKS uses un-prefixed. The labour ETL (Step 1b) can't be mapped until this is picked:
- **Map to SKS's existing un-prefixed tables (lowest friction):** `people→staff`, `schedule→schedule_entries`, `timesheets→timesheets`, `tenders→tenders`. Accepts the cross-tenant convention divergence; defers the unified baseline.
- **Adopt `field_*` on SKS first (consistency):** roll the EQ `field_*` shape onto SKS, migrate into it, retire the un-prefixed tables. More work; pays down the baseline-drift debt; but `staff`/`sites`/`assets` are already populated under the old names → a second internal migration.
### §2b — Schema diff findings (live, 2026-06-06) — the decision is really about *target shape*, not naming

Column-level diff of the five labour domains across all three schemas reveals two **different families**:

- **Legacy source ≈ EQ `field_*`** — the *same* "weekly-grid" shape. `schedule`/`field_schedule` = one row per person per **week** with `mon..sun` + `mon_job..sun_job` text columns. `timesheets`/`field_timesheets` = one row per week with `mon..sun` hours. `people`/`field_people` = single `name` text. Near-identical column-for-column; `field_*` just adds `tenant_id` + uuid ids + `person_id`/`cards_staff_id` hooks.
- **SKS un-prefixed = a different, normalized next-gen shape.** `staff` = `first_name`/`last_name`/`preferred_name`, rates, address, emergency contact, `user_id`, **`cards_worker_id`**. `schedule_entries` = one row **per date** with `staff_id`+`site_id` FKs. `timesheets` = one row **per date** with `start_time`/`end_time`, `hours`, `break_minutes`, FKs. `tenders` = `customer_id` FK, `estimated_value_cents`. All carry `intake_id`/`imported_from`/`schema_version` → this is the **EQ Intake canonical target**, not the legacy Field shape.

| Domain | legacy → SKS un-prefixed | Effort |
|---|---|---|
| `people → staff` | split `name`→first/last; dedupe vs existing **50**; map to `cards_worker_id`/`user_id` | **Hard** |
| `schedule → schedule_entries` | **de-pivot** week-grid → per-date rows; resolve `staff_id`+`site_id` FKs | **Hard** |
| `timesheets → timesheets` | **de-pivot** week hrs → per-date rows; FKs; derive status | **Hard** |
| `tenders → tenders` | rename cols; resolve `customer_id` FK; enum→text | Medium |
| `leave_requests → leave_requests` | resolve `staff_id` FK; date-text→date | Medium |
| *(any) → EQ `field_*`* | near-1:1 column copy; bigint→uuid; add `tenant_id` | **Trivial** |

**The real fork (bigger than naming):** the trivial path (`field_*`) lands data in the **legacy** shape — a regression from what SKS already runs, and a guaranteed *second* migration later. The correct path (SKS un-prefixed) is the **mature, normalized, FK'd, intake-aligned** target with the identity hooks (`cards_worker_id`, `user_id`) the claim model (D2) needs — but the ETL is a genuine **reshape** (de-pivot weekly grids into per-date rows, split names, resolve FKs), not a copy.

**This depends on a question the diff can't answer:** *which app surface do SKS users open at go-live, and which schema does it read?* The current Field app (sks-nsw-labour) reads the **wide** shape; the normalized `staff`/`schedule_entries` schema looks built for a **newer canonical Field / Intake** surface. That answer decides A vs B. **→ surface to Royce before writing ETL.**

*Prior recommendation (map to existing un-prefixed tables) still stands as the "do it right" target — but only if the go-live surface reads that schema. Confirm the surface first.*

---

## 3. The plan (Royce's 4 steps × verified phases)

### Step 1 — Build what's required to export live → EQ Field
- **1a. Settle §2a (schema convention)** then audit the target tables on `sks-canonical app_data`. Confirm which already hold data (`staff` 50, `sites` 591 — merge targets) vs empty (`timesheets`, `schedule_entries`, `tenders`, `leave_requests` — clean inserts).
- **1b. Build the transform (ETL = merge, not copy)** — source `nspbmirochztcjijmcrx` (legacy) → target `sks-canonical app_data` (un-prefixed, pending §2a). Column maps: `people → staff` (**reconcile against existing 50**), `schedule → schedule_entries`, `timesheets → timesheets`, `tenders → tenders`, `leave_requests → leave_requests`. Includes `org_id → tenant_id` rewrite and **identity reconciliation** in both planes (§Step 3). Idempotent, re-runnable, with a row-count + spot-check reconciler. Cross-project move (old app DB → routed tenant plane).
- **Deliverable:** reviewed mapping doc + idempotent migration scripts + a dry-run reconciliation report (incl. `people` 60 ↔ `staff` 50 overlap). No live writes yet.

### Step 2 — Ensure integration works within core → EQ Field
- **2a. Schema available to SKS tenant** per §2 architecture (roll/confirm `field_*`).
- **2b. Phase C — secure auth** (the §1 fix): grant `authenticated` per surface behind tenant-isolation RLS; revoke anon; close the `app_config`/codes exposure. **Auth change → explicit Royce approval before deploy (global rule #6).**
- **2c. Wire the core → Field surface for the SKS tenant on per-user JWT.** Today `core.eq.solutions/sks/field` is served by `sks-nsw-labour` (v3.10) with a PIN re-prompt (likely a missing `SUPABASE_JWT_SECRET`). Target: canonical Field reading `field_*` under a tenant-scoped JWT.
- **Canary:** one real SKS user, end-to-end through core, sees their own data and nothing else.

### Step 3 — The correct way to create user profiles
- This is the onboarding / portable-identity work (Phase 1) + **GATE A**.
- **Reconcile three identity sets:** 60 SKS `people` (labour tenant) ↔ `public.workers` (38, canonical) ↔ `shell_control.users`. Overlap is currently unknown — **produce a reconciliation report before migrating anyone.**
- **Provision-at-claim (Option A, already decided** in `gate-a-decision-2026-06-03.md`): a worker becomes a `shell_control.users` row + `tenant_id` at claim, so profiles are canonical from creation — no second migration.
- **Settle the identity-resolution rule** (onboarding doc §5.1): claim-code binds to identity; **phone is a hint, not the key** (recycled numbers → wrong person sees aggregated licences = the top data-exposure risk).
- **Reconcile onto the in-flight branch** `eq-cards/claude/otp-tenant-fix` (migrations 0010–0015, `eq_cards_claim_invite`). **Do not fork a parallel claim flow.**

### Step 4 — Execute (gated, each phase its own session)
Order, with the safe-now step pulled forward:
1. **Phase C anon lockdown** on `nspbmirochztcjijmcrx` (independent; security; approval-gated).
2. Settle §2 architecture + §Step 3 identity-resolution rule.
3. Step 1 (finalize canonical schema + build ETL + dry-run reconcile).
4. Onboarding Phase 1 pilot (claim flow + provision-at-claim) — can run in parallel with 3.
5. Step 2 integration + canary one SKS user through core.
6. Data cutover (PITR snapshot → migrate → reconcile → soak) → decommission legacy labour access.

---

## 4. Steelman — why this sequence is the strong one

1. **It's execution on proven rails, not greenfield.** One Pipe (gated fleet migrations), semantic guard, ledger reconciler, the claim flow, and the token hook all already exist and are live. The cutover is *careful sequencing of working tools.*
2. **It front-loads the only urgent item** (the anon hole) and decouples it from the slow migration — value + de-risk on day one, no waiting.
3. **Profiles are canonical from creation** (provision-at-claim), so onboarding doesn't create a future migration debt.
4. **Reversible at every step** — keep legacy tables read-only until the new side is proven; rollback = repoint.
5. **It matches the data's real risk profile.** Volume is trivial; the plan spends its effort on identity reconciliation and auth, which is exactly where a real incident would originate.
6. **Pilot can run ahead of cutover** — onboard a couple of SKS users on the identity rails before the bulk data moves, surfacing resolution bugs at low blast radius.

## 5. Adversarial stress-test — what breaks it

1. **Architecture — RESOLVED (§2).** Target is `sks-canonical app_data.field_*` (routed), profiles to `shell_control`. Risk retired by verifying `tenant_routing` live rather than trusting the conflicting 06-02/06-03 docs. *Residual: re-confirm routing at the top of the cutover session — it can change.*
2. **Identity reconciliation is the real bug surface.** 60 SKS people vs 38 canonical workers — overlap unknown; phone collisions; recycled numbers → wrong person sees licences aggregated across employers (bigger blast radius than single-employer). *Mitigation: reconciliation report + manual sign-off before migrating identities; phone-as-hint not key.*
3. **SKS quotes co-located** (`sks_quotes_*`, 14k+ rows) in the same project as the labour data. The labour cutover must not touch them, and **decommissioning the project would kill quotes** — so `nspbmirochztcjijmcrx` survives for quotes regardless. *Mitigation: explicit scope guard; quotes-home decision is out of scope for this plan but must be acknowledged.*
4. **Auth change is live + customer-facing.** *Mitigation: global rule #6 — explicit approval before deploy; canary one surface; coordinate with any concurrent auth-remediation lane.*
5. **Multiple "EQ Field" homes** invite confusion: `core`→`zaap app_data`, `sks`→`sks-canonical app_data`, plus `eq-solves-field` (dev-only). *Mitigation: read `tenant_routing` for the authoritative per-tenant project; `ktmjmdzqrogauaevbktn` is never a prod target — state it in every migration.*
6. **Drift between this snapshot and live** (it already bit the cutover doc). *Mitigation: re-verify each project's state at the top of each execution session; live wins.*

## 6. Standing safety rules (every phase)
- PITR snapshot + row-count baseline before any data migration. Non-negotiable for live customer data.
- Canary one tenant / one domain, verify, then proceed — never fleet-first.
- All schema via the gated One Pipe; no hand-applied single-tenant SQL.
- Per-domain reversibility: old table read-only until the new side is proven.
- Auth/deploy changes: explicit Royce approval (global rule #6); never cross-deploy EQ↔SKS.

---

## 7. Decisions log (Royce, 2026-06-06)
- **D1 — Architecture: SETTLED** (§2). Per-tenant data plane; SKS operational data → **`sks-canonical app_data`** (routed); user profiles → control plane `shell_control`. Operational employee data is **not** in the control layer. *Caveat: the data-plane *project* is settled; the **schema convention** within it is NOT — see D4.*
- **D4 — Target shape / go-live surface (§2a, §2b): SETTLED.** SKS users go live on the **new canonical Field reading the normalized schema** (`staff`, `schedule_entries`, `timesheets`, `tenders`, `leave_requests` on `sks-canonical app_data`). **Not** the legacy `field_*` wide shape. Accepts the hard reshape ETL; avoids a second migration; gives the identity hooks (`cards_worker_id`, `user_id`) the claim model needs.
- **D5 — ETL mechanism (proposed, confirm):** the target tables carry `intake_id` / `imported_from` / `schema_version` → they are the **EQ Intake** canonical-emit target. Strongly prefer routing the legacy→normalized reshape **through EQ Intake** (parse/emit) rather than a bespoke one-off SQL ETL — it's what the columns are for and keeps the suite's Cards→Intake→canonical pipeline as the single path. *Verify against how Intake actually ingests before committing; do not assume.*
- **D2 — Identity-resolution rule: SETTLED.** **Claim-code binds to identity; phone is a hint, not the key.** Admin issues a per-worker claim code (the authorisation event); phone may pre-fill but never auto-matches; worker confirms; provision-at-claim into `shell_control.users` + `user_tenant_memberships` (tenant=sks). Second-employer match requires worker confirmation. **Reconcile onto `eq-cards/claude/otp-tenant-fix` (migrations 0010–0015) — do not fork.**
- **D3 — Legacy anon exposure (§1): ACCEPTED RISK for now, revisit.** Royce's explicit call: leave `nspbmirochztcjijmcrx` anon access as-is during the cutover window rather than spend effort locking a DB that's being retired. **Revisit triggers:** (a) before any new external exposure of that DB, (b) at the latest, immediately before legacy decommission (Step 4). Documented, accepted, owner Royce. *Note: live worker PII remains anon-reachable until then.*

**Next build step (when ready):** Step 1a — audit `sks-canonical app_data` against the canonical baseline (`push-tenant-migration.mjs --tenant sks --dry-run`). No live writes.
