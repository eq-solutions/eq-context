# Handoff: Canonical Tenant Baseline + Migration Runner

**Date written:** 2026-06-02  
**Target session:** New Claude session, Sonnet 4.6 + High effort  
**Estimated scope:** Half-day build

---

## Background

EQ Shell uses a per-tenant Supabase architecture. Every tenant (EQ, SKS, future customers) gets their own Supabase project as their operational data plane. The control plane (`eq-canonical`, `jvknxcmbtrfnxfrwfimn`) holds auth and `shell_control` (tenant registry, routing, entitlements). Each tenant's data lives in their own project.

**Current live tenant projects:**
| Tenant slug | Supabase project | Contents |
|---|---|---|
| `core` (EQ) | `zaapmfdkgedqupfjtchl` (eq-canonical-internal) | Full Field stack + worker-house — 47 tables |
| `sks` | `ehowgjardagevnrluult` (sks-canonical) | SKS quotes + contacts only — 20 tables |

These two databases have completely different schemas. The weekly drift CI (`eq-shell/.github/workflows/tenant-drift.yml`) flags this as "drift" — but it's partly intentional and partly a gap: there's no defined baseline that every tenant canonical is supposed to have.

---

## The problem

1. **No baseline spec.** There's no definition of what tables/functions every tenant canonical must have on day one. As EQ adds features, some things are being applied to one tenant but not others.

2. **No migration runner.** When a schema change needs to go to all active tenants (e.g. a new worker-house column, a security fix), the only mechanism is to manually apply it to each project via the Supabase dashboard or MCP. The `supabase/tenant-migrations/` folder exists in eq-shell but there's nothing that actually *pushes* those files to the live tenant projects.

3. **Drift CI is too broad.** The current drift check compares full schema fingerprints across tenant databases, which produces noise because tenants legitimately have different module tables (SKS has quotes tables, EQ has Field tables). The CI should only assert that the baseline is present everywhere.

---

## What this session should build

### Task 1 — Audit + define the baseline

Read and compare the schemas of the two active tenant projects:
- `zaapmfdkgedqupfjtchl` (eq-canonical-internal)
- `ehowgjardagevnrluult` (sks-canonical)

Cross-reference with `eq-shell/supabase/tenant-migrations/` (existing migration files 0001–0019).

Produce a clear breakdown:
- **Baseline** — tables/functions every tenant must have (worker-house, audit_log, app_config, rate_limit_buckets, and any shared RPCs)
- **Module: Field** — tables only present when tenant uses Field (people, sites, schedule, etc.)
- **Module: Quotes** — tables only present when tenant uses Quotes (sks_quotes_*, contacts)
- **Tenant-specific** — legitimately divergent per tenant

Write this as `eq-context/architecture/canonical-tenant-baseline.md`.

### Task 2 — Write the baseline migration file

Create `eq-shell/supabase/tenant-migrations/0020_baseline_hardening.sql` — an idempotent SQL file that brings any tenant canonical up to the baseline:
- Creates missing baseline tables with `CREATE TABLE IF NOT EXISTS`
- Adds missing baseline functions/RPCs with `CREATE OR REPLACE`
- Enables RLS on baseline tables
- Safe to re-run on a tenant that already has all of it

The SQL must be idempotent (safe to run multiple times). Use `IF NOT EXISTS` everywhere.

### Task 3 — Write the migration runner script

Create `eq-shell/scripts/push-tenant-migration.mjs`.

The script should:
1. Read `SUPABASE_ACCESS_TOKEN` and `CONTROL_PROJECT_REF` from env
2. Query `shell_control.tenant_routing` (via the Supabase Management API) to get all active tenant project refs
3. Accept a `--file <path>` argument pointing to the SQL to apply
4. For each tenant ref, POST the SQL to the Management API (`/v1/projects/{ref}/database/query`)
5. Print per-tenant success/failure
6. Support `--dry-run` flag (prints what would be applied, no writes)
7. Support `--tenant <slug>` flag to target a single tenant

Usage pattern:
```bash
node scripts/push-tenant-migration.mjs --file supabase/tenant-migrations/0020_baseline_hardening.sql
node scripts/push-tenant-migration.mjs --file supabase/tenant-migrations/0020_baseline_hardening.sql --dry-run
node scripts/push-tenant-migration.mjs --file supabase/tenant-migrations/0020_baseline_hardening.sql --tenant sks
```

The script should share the `mgmtRows` / `requireAccessToken` / `controlRef` helpers already in `eq-shell/scripts/_mgmt.mjs`.

### Task 4 — Apply the baseline to sks-canonical

Once the baseline migration file and runner are ready:
1. Run with `--dry-run` first to preview
2. Apply to sks-canonical: `--tenant sks`
3. Re-run the drift CI to confirm the baseline assertions pass

### Task 5 — Update the drift CI

Update `eq-shell/scripts/check-tenant-drift.mjs` so the cross-tenant diff:
- Only compares **baseline tables** (not module tables or tenant-specific tables)
- Loads the baseline table list from a config (e.g. the same list defined in Task 1 or a constants array in `_mgmt.mjs`)
- Still runs the anon-grant invariant check across all three infrastructure projects unchanged

The drift CI should pass green after Task 4 without ignoring legitimate security issues.

---

## Key files to read before starting

```
eq-shell/scripts/_mgmt.mjs                          ← shared Management API helpers
eq-shell/scripts/check-tenant-drift.mjs             ← existing drift CI logic
eq-shell/supabase/tenant-migrations/                ← existing 0001–0019 tenant migration files
eq-shell/.github/workflows/tenant-drift.yml         ← CI workflow
eq-context/STATE.md                                 ← current state context
C:\Users\EQ\.claude\CLAUDE.md                       ← global rules (read first)
C:\Projects\CLAUDE.md                               ← workspace rules (read first)
```

---

## Supabase project refs (DO NOT MIX)

| Project | ID | Role |
|---|---|---|
| eq-canonical | `jvknxcmbtrfnxfrwfimn` | Control plane (auth + shell_control) |
| eq-canonical-internal | `zaapmfdkgedqupfjtchl` | EQ tenant data plane |
| sks-canonical | `ehowgjardagevnrluult` | SKS tenant data plane |
| SKS live (old) | `nspbmirochztcjijmcrx` | **READ-ONLY. Do not touch.** |

---

## Non-negotiables

- Never cross-deploy EQ ↔ SKS code or credentials
- Never touch `nspbmirochztcjijmcrx` (SKS live old DB)
- All migrations must be idempotent (safe to re-run)
- Commit everything to eq-shell — scripts and migration files should be in git
- Run `--dry-run` before any live apply
- The runner must never apply control-plane migrations to tenant projects or vice versa
- Auth changes require explicit Royce approval before deployment

---

## Definition of done

- [ ] `eq-context/architecture/canonical-tenant-baseline.md` written and committed to eq-context
- [ ] `eq-shell/supabase/tenant-migrations/0020_baseline_hardening.sql` written, idempotent
- [ ] `eq-shell/scripts/push-tenant-migration.mjs` written with --dry-run and --tenant flags
- [ ] Baseline applied to sks-canonical (`ehowgjardagevnrluult`) successfully
- [ ] Drift CI passes green (or passes `--anon-only` while cross-tenant diff is reconfigured)
- [ ] Everything committed to eq-shell main via a clean PR
