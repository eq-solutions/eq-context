---
title: Runbook — Supabase backup restoration drill (ehow)
owner: Royce Milmlow
last_updated: 2026-07-04
scope: Manual restore game-day for the ehow offsite backup — executability + RTO/RPO validation
read_priority: high
status: live
---

# Runbook — Supabase backup restoration drill (ehow)

**Owner:** Royce
**Applies to:** ehow / `ehowgjardagevnrluult` (shared canonical DB) — the offsite backup produced by
[`.github/workflows/backup-ehow.yml`](../../.github/workflows/backup-ehow.yml).
**Cadence:** **Automated quarterly** ([`restore-drill-ehow.yml`](../../.github/workflows/restore-drill-ehow.yml), Sentry `ehow-restore-drill`; 1st of Jan/Apr/Jul/Oct). This manual runbook is the deeper, occasional variant.
**Last drill:** 2026-07-04 — automated, ✅ **pass**, **RTO 6 s** (241 sites / 44 customers / 4 checks restored, RLS intact; auth-data restore is a Supabase-parity step — see the callout below).
**Next drill (automated):** 2026-10-01.
**Estimated time:** automated run ~1 min; the full manual game-day below is 60–90 minutes end to end.
**Severity if this fails in a real incident:** Critical — the whole platform depends on ehow.

> Re-homed to eq-context from eq-service and retargeted from the **deleted** `urjhmkhbgaxrofurpbgc`
> to the live **`ehowgjardagevnrluult`** (issue #60). The old copy in eq-service is being retired.

---

> **Two automated layers now cover most of this — this manual runbook is the deepest, rarest variant.**
> **Daily**, [`verify-backup-ehow.yml`](../../.github/workflows/verify-backup-ehow.yml) (Sentry
> `ehow-backup-verify`) checks the backup's **data integrity** — archive intact, real rows,
> `auth.users` captured. **Quarterly**, [`restore-drill-ehow.yml`](../../.github/workflows/restore-drill-ehow.yml)
> (Sentry `ehow-restore-drill`) proves **executability** — it actually restores the tarball into an
> ephemeral Supabase-parity Postgres and verifies the app-data comes back (241 sites / 44 customers,
> RLS intact) with an RTO number.
>
> What automation still can't cheaply cover, and this runbook is for: (1) restoring **auth data** into
> a true Supabase target — `supabase db dump` excludes the managed auth *schema*, so auth rows only
> load where Supabase provisions that schema (a fresh project/branch), not a bare container; and
> (2) the **app-repoint** smoke test. Run this occasionally to close those two gaps.

## Why this runbook exists

Supabase takes automatic daily backups, and this repo takes a daily offsite copy to R2 — but
**a backup is not a backup until it has been restored successfully at least once.** This runbook
proves, on a recurring basis, that:

1. The backups are actually there (both tiers).
2. We can restore one without reading docs under pressure.
3. The restored DB is structurally sound **and contains rows** (RLS intact, data present).
4. The restore completes inside the recovery objectives we commit to.

**RTO target:** 4 h (Tier 1, Supabase managed) / 8 h (Tier 2, offsite R2 → fresh project).
**RPO target:** 24 h (Tier 1 daily) / ≤ 24 h (Tier 2 daily).
Full rationale + tier table: [`system/dr-backups.md`](../dr-backups.md).

> **Data-presence check is not optional.** The retired eq-service job dumped **schema only** (bare
> `supabase db dump`), so a restore of an old backup would come back with empty tables. Step 5 below
> checks **row counts**, not just table counts, precisely to catch this class of failure.

---

## What this runbook is NOT

- **Not a production restore procedure.** Never run these steps against `ehowgjardagevnrluult`
  unless there is an actual incident. The drill always targets a **Supabase branch** or a
  **throwaway project**, never live.
- **Not a substitute for PITR.** PITR is a paid add-on (currently off). If ehow moves to the paid
  plan, add a PITR section.
- **Not a one-off export procedure.** For customer/accountant exports use `pg_dump` directly.

---

## Pre-flight checklist

- [ ] `supabase` CLI installed and logged in (`supabase login`).
- [ ] `psql` available locally.
- [ ] R2 credentials to hand (or dashboard access to the R2 bucket) to pull `db_backup.tar.gz`.
- [ ] The live project ref is `ehowgjardagevnrluult` — note it but **do not target it for writes**.
- [ ] Permission to create a Supabase branch or throwaway project in the org.
- [ ] 90 minutes uninterrupted. A half-finished drill is worse than no drill.

---

## Procedure

### Step 1 — Confirm both backup tiers exist

**Tier 1 (Supabase managed):**
```powershell
Start-Process "https://supabase.com/dashboard/project/ehowgjardagevnrluult/database/backups"
```
Expected: a daily backup within the last 24 h. Note its timestamp.

**Tier 2 (offsite R2):** confirm the most recent daily folder holds both `db_backup.tar.gz` and a
`storage/` tree, and that the Sentry monitor `ehow-daily-backup` is green. If either the R2 copy or
the Sentry monitor is missing/stale, **that itself is an incident** — the schedule is broken.

Pick which tier you are drilling this quarter (alternate: Tier 1 one quarter, Tier 2 the next).

### Step 2 — Create a restore target (never production)

**Option A — Supabase branch (preferred, free-tier compatible):**
```powershell
cd C:\Projects\eq-context
supabase branches create drill-YYYYMMDD --project-ref ehowgjardagevnrluult
```

**Option B — Fresh throwaway project:** create via dashboard, region `ap-southeast-2`,
name `eq-drill-YYYYMMDD`, free tier.

Record the target ref.

### Step 3 — Get the backup

**Tier 2 (offsite R2) — the three-file logical dump:**
```powershell
# Pull the latest weekly db backup from R2 (adjust prefix to the newest date)
aws s3 cp "s3://<R2_BUCKET>/<YYYY-MM-DD_HHMM>/db_backup.tar.gz" `
  "C:\Projects\eq-context\drill-backup.tar.gz" `
  --endpoint-url "<R2_ENDPOINT>"
tar xzf "C:\Projects\eq-context\drill-backup.tar.gz"   # → roles.sql schema.sql data.sql auth_data.sql
```

**Tier 1 (Supabase managed):** download the daily `.backup`/`.sql.gz` from the dashboard backups page.

### Step 4 — Restore into the drill target

```powershell
# Drill target connection string (Settings → Database → Connection string → URI)
$env:DRILL_DB_URL = "postgresql://postgres:<password>@db.<drill-ref>.supabase.co:5432/postgres"

# Tier 2: restore roles → schema → data, in order
psql $env:DRILL_DB_URL -f roles.sql
psql $env:DRILL_DB_URL -f schema.sql
psql $env:DRILL_DB_URL -f data.sql
# auth users — the tarball now ships auth_data.sql (--data-only over the managed
# `auth` schema, which already exists on a fresh Supabase target). Expect a few COPY
# conflicts on Supabase's own built-in rows; the real user rows are what matter.
# Proving THIS path clean is a primary goal of the drill for any DB with real users.
psql $env:DRILL_DB_URL -f auth_data.sql
```
A healthy restore is mostly `CREATE` / `ALTER` / `COPY` and finishes without `ROLLBACK`.

### Step 5 — Sanity-check the restored DB (row counts, not just tables)

From the drill target's SQL editor:
```sql
-- Tables restored
select count(*) from information_schema.tables where table_schema in ('public','service','app_data');

-- ROW PRESENCE — the check the schema-only bug would fail. Expect non-zero.
select 'app_data.sites' t, count(*) c from app_data.sites
union all select 'app_data.customers', count(*) from app_data.customers
union all select 'service.maintenance_checks', count(*) from service.maintenance_checks
union all select 'auth.users', count(*) from auth.users;

-- RLS coverage on public — expect 0 unprotected tables
select count(*) from pg_class c join pg_namespace n on n.oid=c.relnamespace
where n.nspname='public' and c.relkind='r' and not c.relrowsecurity;
```
Expected: table count ≈ production; **row counts non-zero** for sites/customers/checks; `auth.users`
present (ehow ships ~5, whatever the live count is at backup time). Zero unprotected public tables.

> The Tier-2 dump **does** capture `auth` (`backup-ehow.yml` sets `CAPTURE_AUTH=true` →
> `auth_data.sql`). So if `auth.users` comes back empty after restoring `auth_data.sql`, that is a
> **regression finding** — the auth capture or its restore broke. Record it below and open an issue.

### Step 6 — Tear down

```powershell
# Option A (branch)
supabase branches delete drill-YYYYMMDD --project-ref ehowgjardagevnrluult
# Option B (throwaway) — delete via dashboard → Settings → General → Delete project

Remove-Item "C:\Projects\eq-context\drill-backup.tar.gz","roles.sql","schema.sql","data.sql" -ErrorAction SilentlyContinue
```

### Step 7 — Record the drill

Add a row to the **Drill log** below with the achieved RTO/RPO. Open an issue for any finding.

---

## Drill log

| Date | Tier | Backup timestamp | Target | Outcome | Elapsed (RTO) | Rows present? | Findings | Operator |
|---|---|---|---|---|---|---|---|---|
| _example_ | 2 (R2) | 2026-07-05 02:00 UTC | branch `drill-20260706` | ✅ clean, rows present | 52 min | yes | none | Royce |
| 2026-07-04 | 2 (R2) | `2026-07-04_0812` | ephemeral `supabase/postgres:17.6` (CI) | ✅ app-data restored & sound | **6 s** | yes — 241 sites / 44 customers / 4 checks; 210 tables; public-no-RLS 1 = baseline | auth.users 0/5: the dump excludes the managed auth **schema**, so auth **data** loads only into a real Supabase target (capture proven daily by `verify-backup-ehow`). App-data fully restorable. | Claude — automated `restore-drill-ehow.yml` |

_(Fill in after each drill. Never delete old rows.)_

---

## Known hazards

- **Auth schema is sensitive.** The dump contains `auth.users` (emails, password hashes). Treat the
  drill target as **production-grade sensitive** until deleted. Do not share its URL.
- **Signed backup URLs are short-lived and secret.** Never paste an R2/dashboard backup URL into
  Slack, chats, or commit messages.
- **Free-tier branch caps.** A full restore may exceed free-tier branch limits as data grows; switch
  to Option B and raise a ticket to evaluate paid branching.
- **Ordering matters.** Restore `roles` → `schema` → `data`. Restoring data before schema fails.

---

## Escalation

1. **Abort the drill** — don't push on "to see how far it gets".
2. **Record what failed** in the Drill log and open an issue labelled `backup-restore`.
3. If it suggests the real backups are unrecoverable, **open a Supabase support ticket immediately** —
   P0 for the business.
4. Tag Royce before closing out.

---

## Change log

- 2026-07-04 (later) — Backups flipped weekly → **daily** and armed green; runbook updated to match:
  RPO ≤ 24 h (Tier 2), monitor slug `ehow-daily-backup`, and an explicit `auth_data.sql` restore step
  (the offsite dump now captures `auth`, so auth-empty-on-restore is a regression, not a gap). Same
  procedure applies to `eq-canonical` / `eq-canonical-internal` under their R2 prefixes. Not yet drilled.
- 2026-07-04 — Re-homed to eq-context, retargeted urjh → ehow, added Tier-2 (R2 tarball) restore path
  and a row-count presence check (catches the schema-only-dump class of failure). Not yet drilled.
- 2026-04-16 — Original runbook created in eq-service (roadmap item 14). Never drilled.
