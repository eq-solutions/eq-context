---
title: SKS → Field Cutover — Execution Runbook
owner: Royce Milmlow
last_updated: 2026-06-05
scope: Turnkey, verified, phase-gated runbook to put EQ Field on the SKS tenant and retire SKS Labour. Companion to SKS-CUTOVER-CRITICAL-PATH.md (the why/what); this is the how.
read_priority: critical
status: live
---

# SKS → Field Cutover — Execution Runbook

**Prepared 2026-06-05, grounded in a live read of all four projects (not the
2026-06-04 plan, which had stale assumptions — corrections below).** Companion to
`SKS-CUTOVER-CRITICAL-PATH.md`. Security items tracked in `ops/security-register.md`.

> **Verdict (unchanged, now re-confirmed against live): this is a multi-session
> mini-sprint, not a weekend flip.** The three structural prerequisites are still
> unmet today. The good news: the live data is tiny (22 MB) and the rails exist —
> it's careful sequencing, not heavy lifting.

---

## 0. Scope reconciliation — read first

Two different things are being called "go-live". Confirm which you mean before executing:

| "Field is live this weekend" | "SKS cutover" (this runbook) |
|---|---|
| NSW team uses **EQ Field on the EQ tenant (`zaap`)** — already live, used daily. Nothing in this runbook blocks it. | **Field on the SKS tenant (`ehowg`)** + migrate SKS's live data + secure SKS auth + retire SKS Labour (`nspbm`). The phased project below. |

If the team simply adopts Field-on-`zaap` this weekend and SKS Labour keeps
running, **SEC-1 (live PII leak on `nspbm`) persists** — see §6. The cutover
phases A–E are the real "SKS redundant" work and are not weekend-sized.

---

## 1. Verified current state (2026-06-05) — corrects the plan

Three corrections to the mental model in `SKS-CUTOVER-CRITICAL-PATH.md`:

1. **`nspbm` (SKS Labour live) is OFF-REGISTRY.** The control plane
   (`jvkn.shell_control.tenants` + `tenant_routing`) already routes
   **`sks` → `ehowg` (sks-canonical)**. `nspbm` appears nowhere. So the cutover is
   **NOT** "repoint sks from nspbm". It is: build `field_*` + auth + load legacy
   data **into `ehowg`**, then populate `field_org_id` for `sks` (currently `null`).
2. **The live data is small and Quotes-dominated.** `nspbm` is **22 MB**. Labour/
   Field data to migrate is modest (see §3). ~15.4k of the rows are `sks_quotes_*`
   — likely already served by the Quotes app on `ehowg`; **do not blindly
   double-migrate Quotes** (separate decision, §3).
3. **The plan's labour-table list was wrong.** `rotations`, `tafe_calendars`,
   `skills_ratings`, `weekly_reports` **do not exist** on `nspbm`. Migrate what
   actually exists (§3).

**Prerequisite status (re-verified):**

| Prerequisite | Live state 2026-06-05 |
|---|---|
| A. `field_*` schema canonical on `zaap` | ❌ **0** `field_*` tables on `zaap` (tenders 323 still on un-prefixed `tenders`; timesheets/schedule ~0) |
| B. SKS tenant (`ehowg`) has `field_*` | ❌ **0** `field_*` tables on `ehowg` (and `nspbm`) |
| C. SKS auth secured (`ehowg`) | ⚠️ **partial** — only **5** of 56 `app_data` tables granted `authenticated` (EQ/`zaap` is at **28**); anon SELECT = 0 (good) |
| D. SKS live data migrated | ❌ still on `nspbm` (legacy app), not in `ehowg.field_*` |

Project refs: `zaap`=eq-canonical-internal, `ehowg`=sks-canonical,
`nspbm`=sks-labour (LIVE), `jvkn`=eq-canonical (control plane).

---

## 2. Pre-flight — DO BEFORE PHASE A (non-negotiable)

- [ ] **Backups.**
  - Confirm **PITR enabled** on `nspbm` and `ehowg` (Dashboard → Project →
    Database → Backups; not visible via SQL).
  - Take a logical snapshot of `nspbm` (22 MB, trivial):
    `pg_dump "$NSPBM_DB_URL" -Fc -f sks-labour-pre-cutover-2026-06-XX.dump`
    (connection string: Dashboard → Project Settings → Database). **Store offline —
    do NOT commit the dump (binary + live data).**
  - Capture the **row-count baseline** (§7 query) for `nspbm` and save it — this is
    the reconciliation oracle for Phase D.
- [ ] **Secret/env inventory.** Per `WEEKEND-MERGE-RUNBOOK.md` P1: confirm whether
  Field/Service need `SUPABASE_JWT_SECRET` or have moved to `ZAAP_JWT_SECRET` /
  per-tenant. For `ehowg` to serve Field, it needs its own JWT-secret + per-tenant
  auth wiring. Inventory `ehowg`'s Netlify/edge secrets before Phase C.
- [ ] **Coordinate** with the concurrent auth-remediation lane (`focused-brattain`)
  — Phase C overlaps it. Don't duplicate.
- [ ] **One Pipe ready.** Confirm the gated migration runner + `--strict-spine`
  check are green on main before introducing `field_*` migrations.

---

## 3. Data to migrate (verified `nspbm` footprint)

**Field/labour domain → migrate to `ehowg.field_*`:**

| Table | rows | | Table | rows |
|---|--:|---|---|--:|
| schedule | 760 | | managers | 27 |
| pending_schedule | 523 | | job_numbers | 26 |
| tenders | 383 | | tender_enrichment | 15 |
| timesheets | 183 | | teams | 6 |
| people | 60 | | nominations | 4 |
| leave_requests | 59 | | tender_import_runs | 3 |
| team_members | 48 | | organisations | 2 |
| sites | 34 | | (refs: app_config 13, rate_limits 10) |

- **`audit_log` (5,751)** = history; archive, don't necessarily port to live Field.
- **`sks_quotes_*` (~15.4k rows)** = SKS Quotes data. **Separate decision:** these
  tables also exist on `ehowg` (Quotes app). Confirm whether `ehowg` already holds
  the canonical Quotes data before migrating — likely **do not** move these here.
- Zero-row tables (schema only, nothing to migrate): leave_balances, site_diaries,
  prestarts, toolbox_talks, tender_review_decisions, timesheet_locks, checkins,
  roster_presence, ts_reminders_sent, pipeline_events.

---

## 4. The phases (each = its own gated session)

### Phase A — Canonicalize `field_*` on the EQ tenant (`zaap`)
**Goal:** one canonical Field schema (`field_*`) so it can be rolled to `ehowg`.
1. Decide canonical shape per domain → **recommend `field_*` everywhere** (newer model).
2. For each domain on an old un-prefixed table (tenders 323; timesheets/schedule are ~0 so trivial): author an **idempotent** migration that creates the `field_*` table (if absent) and migrates live rows old→new; verify counts; leave the old table read-only.
3. Capture the `field_*` schema as **canonical One-Pipe migrations** (so fresh tenants + `ehowg` inherit it).
- **Gate:** `--strict-spine` green; Field app reads/writes `field_*` on `zaap`; row counts reconcile (old = new).
- **Rollback:** old tables still present + read-only → repoint app to old; revert the migration via inverse One-Pipe migration.

### Phase B — Roll `field_*` to SKS (`ehowg`), schema-only/empty
1. Apply the canonical `field_*` migrations to `ehowg` via the **gated One Pipe** (additive — `ehowg` has none of these tables; low risk).
- **Gate:** `ehowg` has the `field_*` schema (empty); spine green.
- **Rollback:** additive-only → drop the new empty tables via inverse migration.

### Phase C — Secure `ehowg` auth (5 → full, anon→authenticated)
1. Apply the EQ remediation pattern to `ehowg`: per surface, `GRANT` to `authenticated` behind tenant-isolation RLS keyed on **`app_metadata.tenant_id`** (NOT `user_metadata` — see SEC-2, §6); `REVOKE` anon; close any `app_config`/codes exposure.
2. Wire `ehowg`'s JWT secret + per-tenant auth so Field can issue tenant-scoped JWTs.
- **Gate:** `ehowg` `app_data`/`field_*` anon-reachable = 0 (run `scripts/rls_probe.py` against `ehowg`); authenticated surfaces work with a tenant-scoped JWT; advisor ERROR count on `ehowg` = 0.
- **Rollback:** re-grant prior state via inverse migration; runner halts on failure so nothing half-applies.

### Phase D — Migrate SKS's live labour data (`nspbm` → `ehowg.field_*`)
1. **Snapshot first** (Pre-flight §2 done) + fresh row-count baseline.
2. Migrate the §3 Field-domain tables `nspbm` → `ehowg.field_*`, tenant-stamped to the `sks` org. ETL approach (small data): `pg_dump --data-only --table=...` per table → transform → load, OR a scripted copy. One domain at a time.
3. **Reconcile** old→new counts (§7) + spot-check records; Field renders SKS's real data.
- **Gate:** every migrated table's count on `ehowg` = baseline on `nspbm`; spot-checks pass; no data on the new side unaccounted for.
- **Rollback:** `nspbm` untouched (source of truth until cutover proven) → re-run load; truncate the `ehowg` target and reload.

### Phase E — Cut over + decommission
1. Populate `shell_control.tenants.field_org_id` for `sks` (currently `null`); repoint the SKS Field surface at `ehowg.field_*` on per-user auth.
2. **Parallel-run / soak** (team uses Field-on-`ehowg`; `nspbm` kept read-only).
3. **Decommission SKS Labour (`nspbm`)** — see SEC-1, §6. Drop old labour tables only after soak proves cutover.
- **Gate:** team operating on Field-on-`ehowg`; no errors (watch Sentry); `nspbm` anon access disabled; `rls_probe.py` SEC-1 entries clear.
- **Rollback:** repoint the Field surface back to `nspbm` (kept read-only through soak).

---

## 5. Master go / no-go

Per phase: **all gates green before the next phase. Stop at the first red.**
Overall start gate:
- [ ] Pre-flight §2 complete (backups verified, secrets inventoried, One Pipe green).
- [ ] Scope confirmed (§0) — this is the SKS-tenant cutover, scheduled as a mini-sprint.
- [ ] Rollback for the active phase open in a tab.

---

## 6. Security tasks folded in (see ops/security-register.md)

- **SEC-1 (P0, `nspbm` live PII leak)** → closed by Phase E decommission. **If the
  team moves to Field before Phase E, interim-disable `nspbm` anon access / pause
  the project** the moment they're off it — the leak is live until then.
- **SEC-2 (P1, `zaap` `eq_intake_rate_limits` RLS trusts `user_metadata`)** →
  staged SQL in §7. Apply during the change window (it's on `zaap`, Field's live DB).
- **SEC-3 (P0, F1 — exposed `ehowg` service_role key)** → `ehowg` is the cutover
  target, so rotate the key **as part of Phase C** (you're already in `ehowg`'s
  auth lane). Staged per `f1-ehowg-key-rotation-runbook-2026-06-03.md`: new key →
  propagate to Quotes Fly secret + re-encrypt `tenant_routing` → disable legacy →
  re-test legacy GET = 401. **Never disable legacy before both consumers hold the new key.**

---

## 7. Staged artifacts (copy-paste ready — verify live before running)

**Row-count baseline / reconciliation** (run on `nspbm`, then on `ehowg` post-load):
```sql
select relname, n_live_tup
from pg_stat_user_tables
where schemaname = 'public'
order by n_live_tup desc;
```

**SEC-2 fix** — `zaap.app_data.eq_intake_rate_limits` (current policy uses
`user_metadata`; switch to server-controlled `app_metadata`). **Verify first** that
issued JWTs carry `app_metadata.tenant_id` (the `sks_safety_rpc_jwt_tenant_guard`
pattern), else this denies legit callers:
```sql
-- current (insecure): tenant_id = ((auth.jwt() -> 'user_metadata' ->> 'tenant_id')::uuid)
drop policy if exists tenant_isolation on app_data.eq_intake_rate_limits;
create policy tenant_isolation on app_data.eq_intake_rate_limits
  for all to public
  using (tenant_id = ((auth.jwt() -> 'app_metadata' ->> 'tenant_id')::uuid));
-- then remove SEC-2 from scripts/security_audit.py ACCEPTED_ERRORS
```

**Anon-leak gate** (run after Phase C to prove `ehowg` is locked):
```
RLS_PROBE_PROJECT=sks-canonical python3 scripts/rls_probe.py   # add ehowg targets to PROJECTS first
```

**`nspbm` logical backup** (pre-flight):
```
pg_dump "$NSPBM_DB_URL" -Fc -f sks-labour-pre-cutover-2026-06-XX.dump   # store offline, do not commit
```

---

## 8. Sizing

Five gated phases, each a session with verification + soak between. **Mini-sprint,
not a weekend.** Data is 22 MB (small); the cost is care and sequencing, not volume.
Phases A–C are schema/auth (no live customer data moves); D is the only live-data
move and it's tiny; E is the soak + decommission.
