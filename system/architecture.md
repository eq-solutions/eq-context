---
title: SYSTEM — Tech Architecture
owner: Royce Milmlow
last_updated: 2026-05-04
scope: Current state of how systems are built and how they fit together
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
| `urjhmkhbgaxrofurpbgc` | eq-solves-service-dev | Canonical context store (`context_files` table) + EQ Solves Service product data (co-tenant) |

**Why the split:** SKS live data hitting the same project as EQ demo experiments
is an unacceptable blast radius — one bad DELETE on a demo table becomes an
SKS outage. Separating projects creates hard boundaries that tenant prefixes alone cannot.

**Operational rule:** Always confirm which project before connecting. **Never
touch `nspbmirochztcjijmcrx` unless Royce explicitly says "SKS live"**.

**Implication:** Do not spin up a fourth project without a clear risk-segmentation
reason. Four was not the goal — three is the current equilibrium.

---

## eq-context Substrate

**Table:** `context_files` inside Supabase project `urjhmkhbgaxrofurpbgc`
(eq-solves-service-dev), co-tenant with EQ Solves Service product data.
No `tenant_id` on the row — `context_files` is not part of the
multi-tenant data plane, so co-tenancy is acceptable.

**Schema:** `id (uuid)`, `slug (text, unique)`, `filename (text)`,
`content (text)`, `updated_at (timestamptz, default now())`. Trigger
`context_files_set_updated_at` fires `BEFORE UPDATE FOR EACH ROW` and
stamps `updated_at = NOW()` — without this trigger, the column's
`DEFAULT now()` only fires on INSERT and the freshness signal is
structurally unreliable.

**Sync flow:** Push to `main` on `github.com/eq-solutions/eq-context` →
GitHub Action `.github/workflows/sync-context.yml` reads each MD file →
PostgREST UPSERT (`Prefer: resolution=merge-duplicates`) against
`context_files` keyed by `slug` → trigger refreshes `updated_at` →
action's verification job fails the workflow if any synced slug isn't
fresh within 60 seconds.

**Why co-tenant, not a dedicated project:** ~30 rows total. Splitting
context into its own paid Supabase project would multiply MCP targets
and admin overhead for no functional gain. See `ops/decisions.md`
2026-04-28 for full reasoning.

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
