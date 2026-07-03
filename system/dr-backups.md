# Disaster Recovery — platform backups

**Owner:** Royce
**Status:** ⚠️ DRAFT — ehow + eq-canonical + eq-canonical-internal jobs authored, **none armed** (secrets + Sentry monitors pending)
**Scope:** the shared EQ platform substrate. SKS-only DBs are out of scope (SKS owns their DR).
**Last reviewed:** 2026-07-04 (issue [#60](https://github.com/eq-solutions/eq-context/issues/60), verified live)

This doc decides DR once, at the platform level, and points at the jobs that back it.
It replaces the arrangement where a single consuming app (eq-service) ran the offsite
backup for the whole shared database.

---

## Decision in one line

**eq-context owns platform DR.** It runs one offsite backup **per irreplaceable platform DB**
— **ehow** (shared canonical), **eq-canonical** (identity/control plane) and
**eq-canonical-internal** (tenant data plane) — to Cloudflare R2, weekly, each monitored by
Sentry. The per-app copy in eq-service is retired once the ehow job is proven green. Other
live DBs are assessed per-project below.

---

## Why here (not eq-service, not eq-shell)

- ehow is the **shared** substrate: it holds Service's `service.*` data **and** the canonical
  `app_data.*` records Shell owns (sites, customers, assets) used across the platform. Backing
  it up from inside one consuming app means the platform silently loses its offsite copy if that
  app is archived or restructured. The identity and tenant-data planes have the same property —
  no single app owns them, so their DR belongs at the platform layer too.
- eq-context already **holds the ehow service-role key** (`SUPABASE_SERVICE_ROLE_KEY`, confirmed
  in `suite-state-refresh.yml`), a Supabase PAT, and **runs the nightly cron fleet** — it is the
  natural, lowest-friction home for scheduled platform jobs.

---

## Per-project inventory (verified live 2026-07-04, org `sqjyblkiqonyrdobaucn`)

Phase column: **1**/**2** = which phase authored the offsite job; ✓ = job authored (see
Status above for armed state).

| Project | Ref | Holds (live) | Offsite copy needed? | Phase |
|---|---|---|---|---|
| **ehow** (sks-canonical) | `ehowgjardagevnrluult` | Shared prod: `service.*`, `app_data.*` (241 sites / 41 customers), **6 storage buckets** | **Yes** — crown-jewel shared DB | **1 ✓** |
| **eq-canonical** | `jvknxcmbtrfnxfrwfimn` | Shell identity/control plane: **50 `auth.users`**, `shell_control` (29 tables — tenants/memberships, ~2 454 token-mint audit rows), `public` (18), `app_data` (2); **6 buckets / 213 objects** | **Yes** — irreplaceable identity plane | **2 ✓** |
| **eq-canonical-internal** | `zaapmfdkgedqupfjtchl` | Tenant data plane: `app_data` (**104 tables** — 500 schedule entries, 323 tenders, timesheets, customers, sites), `public` (39), `service` (3); **2 buckets / 0 objects**; **0 `auth.users`** | **Yes** — real operational data | **2 ✓** |
| eq-tenant-favour-perfect | `jzjzpgaablnppoimdnip` | **Empty** — system migrations only (created 2026-07-03) | No — nothing to lose yet; Supabase daily suffices | Watch |
| sks-labour | `nspbmirochztcjijmcrx` | SKS entity app DB | **Out of scope** — SKS owns its DR; never cross-entity. (Also retiring.) | — |

> Note: issue #60 listed a 6th project, `vjvamvfpbwcqfudousmg` ("EQ Context"). It exists but
> under a **different org** (`hdkclwpzrmusfqpfahnu`), not the platform org — it is not a platform
> data plane and is out of scope here. (Phase 1 recorded it as "no longer present"; corrected
> 2026-07-04 — it's in a separate org, not gone.)

**Phase 1: ehow.** **Phase 2 (this change): eq-canonical + eq-canonical-internal** — both were a
real coverage gap (the identity plane holds `auth.users` with no offsite copy), now closed with
the same workflow parameterised per project.

---

## Recovery tiers, RTO & RPO

Two independent tiers. Restore from the cheapest that covers the incident.

| Tier | Mechanism | Covers | RPO (max data loss) | RTO (target) |
|---|---|---|---|---|
| **1 — Supabase managed** | Supabase automatic **daily** backup (dashboard restore / PITR if enabled) | Accidental delete, bad migration, table corruption | **24 h** (daily cadence; PITR is a paid add-on, currently **off**) | **4 h** |
| **2 — Offsite R2** | The weekly workflows' `db_backup.tar.gz` + storage, restored into a fresh project | **Supabase account/project loss**, provider-side disaster | **≤ 7 days** (weekly cadence) | **8 h** (manual restore into new project + repoint apps) |

RPO/RTO are **targets until a drill proves them.** The first drill records achieved figures in
`system/runbooks/supabase-restore-drill.md`.

### Per-project recovery ownership

| Project | Tier-1 (managed daily) | Tier-2 (offsite R2, weekly) | Notes |
|---|---|---|---|
| ehow | ✓ all schemas | ✓ `db_backup.tar.gz` + 6 buckets | `auth.users` here is verified by the drill; managed-daily is the secondary net for auth |
| eq-canonical | ✓ all schemas | ✓ `db_backup.tar.gz` (incl. **`auth_data.sql`**) + 6 buckets / 213 objects | **auth.users is captured in the offsite dump on purpose** — see below |
| eq-canonical-internal | ✓ all schemas | ✓ `db_backup.tar.gz` (no auth — 0 users) + storage when present | Storage tolerated-empty today (2 buckets, 0 objects) |

⚠️ **Why eq-canonical's offsite copy explicitly includes `auth`.** `supabase db dump` **excludes
the managed `auth` schema by default**, so a plain three-file dump of an identity plane silently
omits `auth.users` — its crown jewel. Tier-1 (Supabase managed daily) dies **with** the account
in the exact total-account-loss disaster Tier-2 exists for; relying on it for auth would leave the
identity plane with **no** account-loss recovery. So the eq-canonical job adds an explicit
`--schema auth --data-only` capture (`auth_data.sql`), guarded to be non-empty (50 live users).
Auth **restore** mechanics (the auth schema is Supabase-managed) are worked out and recorded by the
drill — but the data is now offsite either way, which is the point.

---

## What the backups capture

Workflows (all weekly, read-only against live — dump = `pg_dump`, storage = GET):

| Project | Workflow | Schedule | Sentry monitor slug | R2 prefix |
|---|---|---|---|---|
| ehow | [`backup-ehow.yml`](../.github/workflows/backup-ehow.yml) | Sun 02:00 UTC | `ehow-weekly-backup` | _(bucket root)_ |
| eq-canonical | [`backup-eq-canonical.yml`](../.github/workflows/backup-eq-canonical.yml) | Sun 03:00 UTC | `eq-canonical-weekly-backup` | `eq-canonical/` |
| eq-canonical-internal | [`backup-eq-canonical-internal.yml`](../.github/workflows/backup-eq-canonical-internal.yml) | Sun 04:00 UTC | `eq-canonical-internal-weekly-backup` | `eq-canonical-internal/` |

Jobs are **staggered an hour apart** so the three weekly runs don't contend on the runner/R2.
The Phase-2 jobs share ehow's R2 bucket, separated by a per-project **key prefix** (so one bucket
holds all three without collision); each job's prune is scoped to its own prefix. Point
`R2_BUCKET_NAME` at separate buckets instead if you prefer hard isolation — the prefix is harmless
either way.

Every job produces a **complete logical DB dump** — three files per Supabase's own recipe:
`roles.sql` (`--role-only`), `schema.sql`, `data.sql` (`--data-only --use-copy`) → `db_backup.tar.gz`.

- ⚠️ **This fixes a real defect.** The retired eq-service job ran a **bare `supabase db dump`,
  which is schema-only** — it never captured rows. Its "green" runs backed up an empty schema.
- **eq-canonical additionally** captures `auth_data.sql` (see the recovery-ownership note above).
- **Every storage bucket, recursively** — buckets are discovered dynamically, so a newly-added
  bucket is never silently missed. ⚠️ The old ehow job synced only **2** of 6 buckets.
- **Silent-empty guards** — a job fails loudly if the DB dump is < 2 KB (or, for eq-canonical, if
  `auth_data.sql` is < 512 B), rather than uploading an empty "backup" and reporting success.
  - **Storage guard is per-project.** ehow and eq-canonical set `EXPECT_STORAGE=true` — 0 buckets
    or 0 objects means a broken key → **fail**. eq-canonical-internal sets `EXPECT_STORAGE=false`
    (it has buckets but 0 objects today), so an empty storage sync is a **clean skip**, not a
    failure; real objects landing later are picked up automatically.
- **Retention** — last 8 weeks in R2; older prefixes pruned (within each project's prefix).

---

## Monitoring / alerting

**One Sentry cron check-in monitor per job** (org `eq-solutions`), slugs:
`ehow-weekly-backup`, `eq-canonical-weekly-backup`, `eq-canonical-internal-weekly-backup`.
Each job checks in `in_progress` → `ok`/`error` and declares its own crontab schedule, so Sentry
alerts on **both**:

- a **failed run** (`error` check-in), and
- a run that **never happens** (missed check-in past the margin) — the exact failure mode that hid a
  **7-week silent outage** on the old ehow job (6 consecutive failed runs from 2026-05-24; last green
  2026-05-17; nobody paged).

Until `SENTRY_DSN` is set the jobs run but print a loud `UNMONITORED` warning (arm cleanly, like
`handoff-probe.yml`). All three reuse the **same** `SENTRY_DSN` (eq-context Sentry project); only
the monitor slug differs.

---

## Arming checklist (Royce — nothing here is auto-applied)

1. **Create the `production-ops` Environment** in eq-context → Settings → Environments:
   deployment-branch rule = `main` only, **no required reviewers**. (All three jobs use this one
   environment.)
2. **Add the shared secrets** (Environment-scoped) — used by all three jobs. Treat as
   production-grade sensitive (the dumps contain `auth.users`):
   - `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ENDPOINT`, `R2_BUCKET_NAME`
   - `SENTRY_DSN` — client ingest DSN for the eq-context Sentry project (arms alerting)
   - _(already present in eq-context: `SUPABASE_SERVICE_ROLE_KEY` = **ehow** key,
     `SUPABASE_ACCESS_TOKEN` = org-wide PAT)_
3. **Add the ehow DB URL** (Phase 1):
   - `SUPABASE_DB_URL` — ehow session-pooler URI (`postgresql://postgres.ehowgjardagevnrluult:…@…pooler.supabase.com:5432/postgres`)
4. **Add the Phase-2 project secrets** (each project needs its **own** DB URL + service-role key —
   do **not** reuse the ehow `SUPABASE_SERVICE_ROLE_KEY`, which is the ehow key):
   - `EQ_CANONICAL_DB_URL`, `EQ_CANONICAL_SERVICE_ROLE_KEY` (eq-canonical / `jvknxcmbtrfnxfrwfimn`)
   - `EQ_CANONICAL_INTERNAL_DB_URL`, `EQ_CANONICAL_INTERNAL_SERVICE_ROLE_KEY` (eq-canonical-internal / `zaapmfdkgedqupfjtchl`)
5. **Run each once manually** (`workflow_dispatch`) → confirm green, confirm `db_backup.tar.gz`
   and `storage/` land under the right R2 prefix, confirm each Sentry monitor shows a check-in.
   - **eq-canonical first run — confirm `auth_data.sql` is present and non-empty in the tarball.**
     This is the one part not yet proven against live (no armed run): if `supabase db dump
     --schema auth` behaves unexpectedly, the guard fails the run loudly (read-only, no damage).
6. **Run the first restore drill** (`system/runbooks/supabase-restore-drill.md`) — record RTO/RPO;
   for eq-canonical specifically, verify the **auth restore** path.
7. **Retire the eq-service copy** — delete `eq-service/.github/workflows/backup.yml` in a separate
   eq-service PR **after** the ehow run is green (avoid the double-backup trap). Not done from eq-context.

---

## Follow-ups (not in this change)

- **eq-tenant-favour-perfect** (`jzjzpgaablnppoimdnip`) — empty today; add a job (same template,
  parameterised) if/when it takes real data. On the Watch list.
- **Immediate, orthogonal:** eq-service's own `SUPABASE_DB_URL` (env `production-ops`) still points
  at the deleted `urjh` pooler host; repoint to ehow if you want the old job alive during cutover.
  Royce owns this secret. Once eq-context is green, the eq-service job is retired regardless.
- **PITR:** if a project moves to the paid plan, add a PITR section here (tightens Tier-1 RPO below 24 h).
  Most valuable for the identity plane (eq-canonical) if account-loss RPO ever needs to be < 7 days.
