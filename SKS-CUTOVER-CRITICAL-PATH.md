---
title: SKS Cutover — Critical-Path Plan
owner: Royce Milmlow
last_updated: 2026-07-11
scope: Phased plan to move EQ Field onto the SKS tenant (schema + auth prerequisites; live-data cutover is now MANUAL re-entry — see 2026-07-11 update)
read_priority: reference
status: live
---

# SKS Cutover — Critical-Path Plan (Field on the SKS tenant)

**Prepared:** 2026-06-04
**Verdict: NOT a weekend merge.** This is a multi-step migration of **live customer data** with real prerequisites. Schedule it as its own controlled project (multiple sessions), each phase gated, with backups and a single-tenant canary. Rushing it in a weekend window is the exact failure mode this whole program was built to avoid.

> "Field on SKS" is not flipping a switch — it's: untie a half-finished schema migration on the EQ tenant → make the Field schema canonical → roll it to SKS → **migrate SKS's live labour data into it** → secure SKS's auth → repoint the app → decommission the old labour app.

---

## ⚠ UPDATE 2026-07-11 — cutover METHOD changed: MANUAL re-entry, not automated migration

**Royce's decision (2026-07-11):** SKS NSW Labour stays the live system. EQ Field is proven by **manually re-entering each week's data into EQ Field in parallel** with SKS Labour, until it matches with no issues for a defined run, then cut over. This REPLACES the automated live-data migration in Phase D below.

**What this changes:**
- **Phase D (automated migration of live labour rows) is SUPERSEDED.** Do NOT build the row-migration job. Forward data lands in `field_*` by manual weekly entry during the parallel run.
- **Historical SKS Labour data is NOT migrated.** The old app/DB (`nspbmirochztcjijmcrx`) is kept as a **read-only archive** after cutover; only forward weeks are re-keyed.
- **Phases A–C still stand as prerequisites** — you can't hand-enter into tables that don't exist or aren't secured: canonicalize the `field_*` schema (A), roll it to the SKS tenant (B), secure SKS auth anon→authenticated (C). Unchanged.
- **Phase E still stands** — the manual parallel entry IS the soak; decommission SKS Labour once the run proves out.

**Proving discipline (the manual run is only as good as this):**
- **Not solo.** Put one supervisor + one crew on EQ Field during the parallel weeks. One person hand-entering proves the *features* work, not that 53 staff / 15 supervisors will actually use it — SKS Labour runs ~160 user-actions/day (verified 2026-07-11), and that's the load the new app must carry. Solo entry never tests it.
- **Enter independently, then compare** — don't key EQ Field to *force* a match, or you smooth over the exact divergences the parallel run exists to catch. Log every mismatch.
- **Define the stop condition** — N consecutive clean weeks (recommend 3–4) across a full roster+timesheet cycle → cut. Open-ended dual-entry becomes permanent.

_The Phase A–E plan below remains the reference for the schema/auth prerequisites; treat Phase D as history._

---

## Why it's blocked (verified live, 2026-06-04)

| Prerequisite | Current state |
|---|---|
| EQ Field schema is canonical & in the spine | ❌ **Half-migrated** on the EQ tenant (see map below) |
| SKS tenant has the `field_*` schema | ❌ **0** `field_*` tables on SKS |
| SKS auth is secured (anon→authenticated) | ❌ Only **5** `app_data` tables on `authenticated` (EQ is at 28) |
| SKS live labour data migrated to `field_*` | ❌ SKS runs **7 legacy labour tables** with live data |

Every row is a "no." None is a weekend task.

---

## The half-migration map (EQ tenant `zaap`, approx rows)

The EQ tenant is mid-migration between an old **un-prefixed** schema and the new **`field_*`** schema, and **live data sits on both sides depending on the domain** — so there is no single "just drop the old ones":

| Domain | Old (un-prefixed) | New (`field_*`) | Where the live data is |
|---|---|---|---|
| Tenders | `tenders` (10) | `field_tenders` (**323**) + enrichment/import/review (3/1/5) | **→ `field_*`** (new) |
| Timesheets | `timesheets` (**75**) | `field_timesheets` (0) | **→ un-prefixed** (old) |
| Schedule | `schedule_entries` (**500**) | `field_schedule` (0) | **→ un-prefixed** (old) |
| Everything else | mostly 0 | mostly 0 | empty both sides |

**Implication:** the canonicalization must be decided **per domain** and the live data migrated to the canonical side. Tenders already moved; timesheets and schedule have **not**. This is careful, table-by-table data work — not a schema-only change.

---

## The phased plan (each phase = its own gated session)

### Phase A — Canonicalize the Field schema on the EQ tenant
1. Decide the canonical shape per domain (recommend: `field_*` everywhere, since it's the newer model and tenders already live there).
2. For each domain still on the old tables (timesheets, schedule, …): author an idempotent migration that creates the `field_*` shape (if absent) and **migrates the live rows** old→new; verify row counts; leave the old table in place (read-only) until cutover is proven.
3. Capture the `field_*` schema as **canonical One-Pipe migrations** (so fresh tenants + SKS get it).
4. Gate: `--strict-spine` still green; Field app reads/writes the `field_*` tables.

### Phase B — Roll the Field schema to SKS (empty, schema-only)
1. Apply the `field_*` migrations to the SKS tenant via the **gated One Pipe** (canary: it's additive, SKS has none of these tables yet).
2. Gate: SKS now has the `field_*` schema (empty); spine still green.

### Phase C — Secure SKS auth (anon→authenticated)
1. Repeat the EQ remediation pattern on SKS: grant `authenticated` per surface behind tenant-isolation RLS; revoke anon; close the SKS `app_config`/codes exposure.
2. Gate: SKS `app_data` anon-reachable = 0; authenticated surfaces work with a tenant-scoped JWT.

### Phase D — Migrate SKS's live labour data  ⛔ SUPERSEDED 2026-07-11 (manual re-entry — see top note)
1. **Snapshot SKS first** (Supabase PITR + a row-count baseline of all 7 labour tables).
2. Migrate SKS's live labour rows (`timesheets`, `tenders`, `rotations`, `site_diaries`, `tafe_calendars`, `skills_ratings`, `weekly_reports`) into the corresponding `field_*` tables.
3. Gate: row counts reconcile old→new; spot-check records; Field renders SKS's real data.

### Phase E — Cut over + decommission
1. Repoint the SKS Field surface at the `field_*` schema on the SKS tenant, on per-user auth.
2. Parallel-run / verify for a soak period.
3. Decommission the legacy SKS NSW Labour app + its anon access. Drop the old labour tables only after the soak proves the cutover.

---

## Standing safety rules (every phase)

- **Backups before any data migration** (Supabase PITR + row-count baseline). Non-negotiable for live customer data.
- **Canary one tenant / one domain**, verify, then proceed — never fleet-first. (The `0035` canary catching a real bug is the proof this matters.)
- **All schema via the gated One Pipe.** No hand-applied single-tenant SQL.
- **Per-domain reversibility:** keep the old table read-only until the new side is proven; rollback = repoint to the old table.
- **Coordinate with the concurrent auth remediation** (`focused-brattain`) — Phase C overlaps their lane; don't duplicate.

---

## Rough sizing

Five gated phases, each a session, with verification + soak between. Realistic as a **dedicated mini-sprint**, not a weekend. The good news: the rails (One Pipe, semantic guard, ledger reconciler, the remediation pattern) all exist — this is **execution on proven tooling**, just careful and sequenced.
