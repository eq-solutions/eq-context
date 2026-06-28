---
title: SYSTEM — Tech Architecture
owner: Royce Milmlow
last_updated: 2026-06-08
scope: Current state of how systems are built and how they fit together — including tenant migration management pattern
read_priority: standard
status: live
---

# SYSTEM — Tech Architecture

Describes how systems are currently built. For the *decision* behind each
choice (alternatives considered, reasoning at the time), see
`ops/decisions.md`. This file is the "what", decisions.md is the "why".

For the *financial* architecture (AHD, Delta Elcom cliff, CDC PSI), see
`ops/financial-architecture.md`.

---

## One Cloudflare Worker for Everything

**Decision:** Single `anthropic-proxy` worker shared across EQ Expenses, SKS Receipt Tracker,
and any future tools that need Anthropic API access.

**Why:** The worker does exactly one job — receive a request, attach the API key, forward it.
Nothing about that job is app-specific. One worker means one API key to manage, one deployment
to maintain, and zero friction when adding new apps.

**Implication:** Never create a per-app worker. Point new tools at the existing URL.

---

## Three Supabase Projects — Segmented by Risk

**Current state (Apr 2026):** The "one Supabase project for everything" rule
evolved as the risk profile diverged. Three projects now exist, each with a
distinct role:

| Project ID | Name | Role |
|---|---|---|
| `nspbmirochztcjijmcrx` | sks-labour | Live SKS staff production data |
| `ktmjmdzqrogauaevbktn` | eq-solves-field | EQ Field demo backend |
| `urjhmkhbgaxrofurpbgc` | eq-solves-service-dev | **DELETED 2026-06-22.** Was the canonical context store (`context_files` table) + EQ Service product data (migrated to ehow 2026-06-08). Substrate now served from the public GitHub repo directly via raw URLs — no Supabase store. |

**Why the split:** SKS live data hitting the same project as EQ demo experiments
is an unacceptable blast radius — one bad DELETE on a demo table becomes an
SKS outage. Separating projects creates hard boundaries that tenant prefixes alone cannot.

**Operational rule:** Always confirm which project before connecting. **Never
touch `nspbmirochztcjijmcrx` unless Royce explicitly says "SKS live"**.

**Implication:** Do not spin up a new project without a clear risk-segmentation reason. The active footprint is defined in the 'Control Layer' section below — refer to that list for the current project count. This section (Apr 2026) predates the per-tenant model.

---

## Control Layer + Per-Tenant Supabase (confirmed model, Jun 2026)

**Confirmed architecture (2026-06-02):** One Supabase per tenant. The control
layer (`eq-canonical`) holds config and registry only. Every tenant gets their
own `{tenant}-canonical` Supabase with all their operational and identity data.

| Project | Name | Role |
|---|---|---|
| `jvknxcmbtrfnxfrwfimn` | **eq-canonical** | **Control layer only.** Cards config, tenant registry, app settings, module entitlements. Browser-accessible. No operational data. |
| `zaapmfdkgedqupfjtchl` | **eq-canonical-internal** | **EQ tenant Supabase.** All EQ Solutions tenant data — workers, identity, operational records. Pattern: `{tenant}-canonical`. |
| `ehowgjardagevnrluult` | **sks-canonical** | **SKS tenant Supabase.** All SKS tenant data. Same pattern. SKS tenant id `7dee117c-98bd-4d39-af8c-2c81d02a1e85`. |

**Boot flow:** EQ Field (and other apps) read `eq-canonical` at startup to resolve
which tenant Supabase to connect to. All data ops then go direct to that tenant's
`{tenant}-canonical` project. `eq-canonical` is never a data store.

**Why one project per tenant:** physical separation gives a cleaner compliance
narrative, smaller blast radius per tenant, and no RLS-shared-schema complexity.
Cost is ~$25/mo per active tenant — acceptable at trade-subbie scale.

**Adding a new tenant:** provision a new `{tenant}-canonical` Supabase project,
apply the canonical migration set, register the connection in `eq-canonical`, set
`TENANT_ORG_UUID` in the app's Netlify env.

**Active Supabase footprint (as of 2026-06-22):** `eq-canonical` (`jvknxcmbtrfnxfrwfimn`, control), `eq-canonical-internal` (`zaapmfdkgedqupfjtchl`, EQ tenant), `sks-canonical` / ehow (`ehowgjardagevnrluult`, SKS tenant — sole DB for EQ Service + Field), `sks-labour` (`nspbmirochztcjijmcrx`, **SKS LIVE — never touch**). `eq-solves-service-dev` (`urjhmkhbgaxrofurpbgc`): **DELETED 2026-06-22**. `eq-solves-field` (`ktmjmdzqrogauaevbktn`): verify status before use.

**Operational rule:** confirm which project before connecting. Never touch
`nspbmirochztcjijmcrx` (sks-labour) unless "SKS live" is explicitly stated.

---

## Tenant Canonical Migration Management

**Problem:** `eq-canonical-internal` and `sks-canonical` start from identical schema but will
diverge. Two types of change exist — core (every tenant must have it) and tenant-specific
(one tenant only). Without an explicit pattern, core migrations get missed on one tenant,
causing silent app breakage.

**Pattern (agreed 2026-06-02):** Split migrations by scope.

```
tenant-schema/
  core/
    migrations/   ← applied to EVERY {tenant}-canonical project
  tenants/
    eq/
      migrations/ ← EQ Solutions extensions only
    sks/
      migrations/ ← SKS extensions only
```

**Deploy order** (core first, tenant-specific after):
1. Apply `core/migrations/` → `eq-canonical-internal`
2. Apply `core/migrations/` → `sks-canonical`
3. Apply `tenants/eq/migrations/` → `eq-canonical-internal`
4. Apply `tenants/sks/migrations/` → `sks-canonical`

**Intentional divergence is fine** — tenant-specific tables and columns are the whole point of
per-tenant projects. The guard is against *unintentional* divergence: a core migration landing
on one tenant but not the other.

**CI drift guard:** A GitHub Actions job on any change to `core/migrations/` should validate
both tenant projects have applied every migration in the folder. This is the pending CI guard
item in STATE.md. Until it exists, any core migration MUST be manually applied to both tenants
and confirmed before merging.

**Where these files live:** TBD — either a `tenant-schema/` folder in this repo (`eq-context`)
or a thin dedicated repo. Decision needed before the first core migration is written.

**Adding a new tenant:** Apply `core/migrations/` in full, then create `tenants/{name}/`
for any tenant-specific additions. Register in `eq-canonical`.

---

## eq-context Substrate

**Current model (from 2026-06-22):** the substrate *is* the public GitHub repo
`github.com/eq-solutions/eq-context`. Assistants read files directly via raw URLs —
`https://raw.githubusercontent.com/eq-solutions/eq-context/main/<path>` (token-free,
CDN-backed; the legacy `/context/claude` alias maps to `CLAUDE.md`). There is no
database, cache, or sync job. A push to `main` is live immediately; the file on
`main` is the freshness signal of record.

**Retired (historical):** before 2026-06-22 a Supabase edge cache mirrored the repo
into a `context_files` table inside project `urjhmkhbgaxrofurpbgc` (eq-solves-service-dev),
co-tenant with EQ Solves Service product data, kept fresh by a `sync-context.yml` GitHub
Action and an `updated_at` trigger. That project was deleted 2026-06-22, retiring the
whole mechanism (table, trigger, sync Action, and the edge function at
`/functions/v1/context/<slug>`). See `system/lessons.md` for its footguns and
`ops/decisions.md` 2026-04-28 for the original co-tenant rationale.

---

## Single-File HTML as Distribution Format

**Decision:** Internal tools are built as single index.html files with a Cloudflare Worker proxy.

**Why:** Solves three real problems simultaneously:
1. ThreatLocker and corporate endpoint security blocks Python, .exe, .bat files
2. Email security filters flag zip files containing executables
3. No IT involvement needed — open a file in Chrome, done

**Tradeoff:** localStorage instead of a real database, at least initially.
**Migration path:** localStorage → Supabase is a contained change. Data shape stays identical;
only read/write functions change. Design data models for Supabase from day one.

---

## localStorage First, Supabase When Ready

**Decision:** New tools start with localStorage, migrate to Supabase when multi-user
or cross-device sync is genuinely needed.

**Why:** localStorage removes all backend complexity during battle-testing.
Real usage reveals what the data model actually needs — designing for Supabase upfront
often means designing the wrong schema.

**When to migrate:** When any of these are needed:
- Multiple users with separate records
- Cross-device sync (start on work PC, continue on phone)
- Manager/approval workflow
- Automated email submission

---

## EQ Solves Field — URL-Based Tenant Detection

**Decision:** Tenant is detected from the URL subdomain/slug, not from login.

**Why:** Avoids auth complexity for field staff who just need to clock on.
Trade-off is that demo mode is controlled by a tenant slug ("eq") that bypasses Supabase entirely.
DEMO_FLAG comments mark every point that needs to be re-enabled for live tenants.
