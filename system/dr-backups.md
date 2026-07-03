# Disaster Recovery — platform backups

**Owner:** Royce
**Status:** ⚠️ DRAFT — ehow job authored, **not yet armed** (secrets + Sentry monitor pending)
**Scope:** the shared EQ platform substrate. SKS-only DBs are out of scope (SKS owns their DR).
**Last reviewed:** 2026-07-04 (issue [#60](https://github.com/eq-solutions/eq-context/issues/60), verified live)

This doc decides DR once, at the platform level, and points at the one job that backs it.
It replaces the arrangement where a single consuming app (eq-service) ran the offsite
backup for the whole shared database.

---

## Decision in one line

**eq-context owns platform DR.** It runs exactly one offsite backup of the shared canonical
DB (**ehow**) to Cloudflare R2, weekly, monitored by Sentry. The per-app copy in eq-service
is retired once this job is proven green. Other live DBs are assessed per-project below.

---

## Why here (not eq-service, not eq-shell)

- ehow is the **shared** substrate: it holds Service's `service.*` data **and** the canonical
  `app_data.*` records Shell owns (sites, customers, assets) used across the platform. Backing
  it up from inside one consuming app means the platform silently loses its offsite copy if that
  app is archived or restructured.
- eq-context already **holds the ehow service-role key** (`SUPABASE_SERVICE_ROLE_KEY`, confirmed
  in `suite-state-refresh.yml`), a Supabase PAT, and **runs the nightly cron fleet** — it is the
  natural, lowest-friction home for a scheduled platform job.

---

## Per-project inventory (verified live 2026-07-04, org `sqjyblkiqonyrdobaucn`)

| Project | Ref | Holds (live) | Offsite copy needed? | Phase |
|---|---|---|---|---|
| **ehow** (sks-canonical) | `ehowgjardagevnrluult` | Shared prod: `service.*`, `app_data.*` (241 sites / 41 customers), **6 storage buckets** | **Yes** — crown-jewel shared DB | **1 (this)** |
| eq-canonical | `jvknxcmbtrfnxfrwfimn` | Shell identity/control plane: **50 `auth.users`**, `shell_control` tenants/memberships, 2 454 token-mint audit rows, 213 storage objects | **Yes** — irreplaceable identity plane, currently unbacked | 2 |
| eq-canonical-internal | `zaapmfdkgedqupfjtchl` | Tenant data plane: 500 schedule entries, 323 tenders, timesheets, customers, sites | **Yes** — real operational data, unbacked | 2 |
| eq-tenant-favour-perfect | `jzjzpgaablnppoimdnip` | **Empty** — system migrations only (created 2026-07-03) | No — nothing to lose yet; Supabase daily suffices | Watch |
| sks-labour | `nspbmirochztcjijmcrx` | SKS entity app DB | **Out of scope** — SKS owns its DR; never cross-entity. (Also retiring.) | — |

> Note: issue #60 listed a 6th project, `vjvamvfpbwcqfudousmg` ("EQ Context"). It is **no
> longer present** in the org as of 2026-07-04 — treat that line in the issue as stale.

**Phase 1 (this change): ehow only.** Phase 2 (eq-canonical + eq-canonical-internal) is a real
gap, not gold-plating — the identity plane holds `auth.users` with no offsite copy — but is
deferred to keep this change right-sized. It reuses this same workflow parameterised per project.

---

## Recovery tiers, RTO & RPO

Two independent tiers. Restore from the cheapest that covers the incident.

| Tier | Mechanism | Covers | RPO (max data loss) | RTO (target) |
|---|---|---|---|---|
| **1 — Supabase managed** | Supabase automatic **daily** backup (dashboard restore / PITR if enabled) | Accidental delete, bad migration, table corruption | **24 h** (daily cadence; PITR is a paid add-on, currently **off**) | **4 h** |
| **2 — Offsite R2** | This workflow's weekly `db_backup.tar.gz` + storage, restored into a fresh project | **Supabase account/project loss**, provider-side disaster | **≤ 7 days** (weekly cadence) | **8 h** (manual restore into new project + repoint apps) |

RPO/RTO are **targets until a drill proves them.** The first drill records achieved figures in
`system/runbooks/supabase-restore-drill.md`.

---

## What the ehow backup captures

Workflow: [`.github/workflows/backup-ehow.yml`](../.github/workflows/backup-ehow.yml). Weekly,
Sun 02:00 UTC. Read-only against live (dump = `pg_dump`; storage = GET).

- **Complete logical DB dump** — three files per Supabase's own recipe: `roles.sql` (`--role-only`),
  `schema.sql`, `data.sql` (`--data-only --use-copy`) → `db_backup.tar.gz`.
  - ⚠️ **This fixes a real defect.** The retired eq-service job ran a **bare `supabase db dump`,
    which is schema-only** — it never captured rows. Its "green" runs backed up an empty schema.
  - Auth coverage (`auth.users`) is **verified by the drill**; Supabase-managed daily is the
    secondary net for auth.
- **Every storage bucket, recursively** — buckets are discovered dynamically. ehow currently has
  **6** (`attachments`, `logos`, `licence-photos`, `sks-quote-attachments`, `job-plan-references`,
  `compliance-packs`). ⚠️ The old job synced only **2** (`attachments`, `logos`) — the other four
  were unbacked.
- **Silent-empty guards** — the job fails loudly if the dump is < 2 KB or storage returns 0 objects,
  rather than uploading an empty "backup" and reporting success.
- **Retention** — last 8 weeks in R2; older prefixes pruned.

---

## Monitoring / alerting

**Sentry cron check-in monitor**, slug `ehow-weekly-backup` (org `eq-solutions`). The job checks
in `in_progress` → `ok`/`error` and declares its own crontab schedule, so Sentry alerts on **both**:

- a **failed run** (`error` check-in), and
- a run that **never happens** (missed check-in past the margin) — the exact failure mode that hid a
  **7-week silent outage** (6 consecutive failed runs from 2026-05-24; last green 2026-05-17; nobody paged).

Until `SENTRY_DSN` is set the job runs but prints a loud `UNMONITORED` warning (arms cleanly, like
`handoff-probe.yml`).

---

## Arming checklist (Royce — nothing here is auto-applied)

1. **Create the `production-ops` Environment** in eq-context → Settings → Environments:
   deployment-branch rule = `main` only, **no required reviewers**.
2. **Add these secrets** (Environment-scoped). Treat as production-grade sensitive — the dump
   contains `auth.users`:
   - `SUPABASE_DB_URL` — ehow session-pooler URI (`postgresql://postgres.ehowgjardagevnrluult:…@…pooler.supabase.com:5432/postgres`)
   - `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ENDPOINT`, `R2_BUCKET_NAME`
   - `SENTRY_DSN` — client ingest DSN for the eq-context Sentry project (arms alerting)
   - _(already present in eq-context: `SUPABASE_SERVICE_ROLE_KEY` = ehow key, `SUPABASE_ACCESS_TOKEN`)_
3. **Run once manually** (`workflow_dispatch`) → confirm green, confirm `db_backup.tar.gz` and
   `storage/` land in R2, confirm the Sentry monitor shows a check-in.
4. **Run the first restore drill** (`system/runbooks/supabase-restore-drill.md`) — record RTO/RPO.
5. **Retire the eq-service copy** — delete `eq-service/.github/workflows/backup.yml` in a separate
   eq-service PR **after** step 3 is green (avoid the double-backup trap). Not done from eq-context.

---

## Follow-ups (not in this change)

- **Phase 2:** offsite for `eq-canonical` (identity plane, holds `auth.users`) and
  `eq-canonical-internal` — same workflow, per-project. This is a genuine coverage gap.
- **Immediate, orthogonal:** eq-service's own `SUPABASE_DB_URL` (env `production-ops`) still points
  at the deleted `urjh` pooler host; repoint to ehow if you want the old job alive during cutover.
  Royce owns this secret. Once eq-context is green, the eq-service job is retired regardless.
- **PITR:** if ehow moves to the paid plan, add a PITR section here (tightens Tier-1 RPO below 24 h).
