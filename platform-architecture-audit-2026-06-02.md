---
title: Platform Architecture Audit
last_updated: 2026-06-08
type: audit
status: live-verified
scope: eq-shell, eq-context, eq-solves-service, eq-solves-field, eq-quotes, eq-cards, eq-roles
method: READ-ONLY — no migrations, no DB writes, no deploys, no PRs
note: This file lives at repo root. Per the F2 finding below, the sync-context
  workflow does NOT ingest root-level working docs, so this audit will NOT appear
  in the Supabase context_files mirror. GitHub (this repo) is the source of truth.
owner: Royce Milmlow
read_priority: reference
---

# EQ Platform Architecture Audit — 2026-06-02

Read-only audit of the multi-tenant platform. Findings were first produced from
repo/code/ledger evidence, then **the two UNVERIFIED items (F1, F2) were re-run
against live Supabase** (read-only `list_migrations` + a `SELECT slug` on
`context_files`). The live pass materially revised F1 and quantified F2. The
`nspbmirochztcjijmcrx` (sks-labour) project was never touched.

## Executive Summary

Overall posture is stronger than the audit's priors suggested: the per-tenant
control-plane model is consistently coded, a tenant-drift CI job and a
tenant-routing health probe both exist, and Cards completed its Path A
consolidation. The highest-risk area is **key + migration governance (F3 / F1)**:
a single `TENANT_ROUTING_MASTER_KEY` decrypts every tenant's service-role key with
**no rotation runbook**, and the two tenant data planes **do not share a migration
lineage** — with same-numbered migrations meaning different things on each tenant.
The suspected eq-context repo↔mirror fork is **not** what was feared: the repo is
canonical and current; the Supabase mirror is a lagging, incomplete subset.

---

## Findings (ranked by runway-to-incident)

### F3 — Control-plane SPOF + key blast radius
- **Status:** CONFIRMED (blast radius) / PARTIAL (SPOF — mitigated for Field, real for Shell) / CONFIRMED-GAP (no rotation runbook)
- **Severity:** HIGH
- **Evidence:**
  - `eq-shell/netlify/functions/_shared/encryption.ts:31-56` — one
    `TENANT_ROUTING_MASTER_KEY` (AES-256-GCM) decrypts the service-role key of
    **every** tenant in `tenant_routing`. The file's own comment concedes
    "A Shell compromise is game-over."
  - `eq-shell/netlify/functions/_shared/tenant-routing.ts:36,86-93,234-249` —
    routing **is cached** (5-min TTL, per warm function instance). Shell hits the
    control plane on cold start / cache miss only, not every request. Decrypt at `:147`.
  - Integrity probe EXISTS but is on-demand only:
    `eq-shell/netlify/functions/tenant-routing-health.ts` (platform-admin; opens
    every tenant data plane, reports reachability + table counts). No scheduled alert.
  - Field SPOF mitigated: `eq-solves-field/scripts/app-state.js:55-123` reads
    eq-canonical at boot with a 1.5s AbortController timeout and falls back to
    hardcoded tenant maps if canonical is down.
  - **Rotation runbook gap:** `eq-context/security-secret-rotation-runbook-2026-05-31.md`
    covers `EQ_SECRET_SALT` only. No runbook exists for `TENANT_ROUTING_MASTER_KEY`.
    `STATE.md:33` records one ad-hoc rotation on 2026-06-02 with no procedure.
- **Recommended next step:** Write a `TENANT_ROUTING_MASTER_KEY` rotation runbook
  (re-encrypt-every-`tenant_routing`-row procedure, referencing `flushRoutingCache()`),
  and schedule `tenant-routing-health` as an alerting cron.

### F1 — Migration drift (tenant DBs) — LIVE-VERIFIED, REVISED
- **Status:** CONFIRMED (drift worse than ledger stated; ledger itself inaccurate)
- **Severity:** HIGH
- **Live evidence (read-only `list_migrations`, 2026-06-02):**
  - **EQ-internal (`zaapmfdkgedqupfjtchl`)** carries ~21 migrations;
    **SKS-canonical (`ehowgjardagevnrluult`)** carries ~90. The two tenants **do
    not share a migration lineage** — SKS runs the full intake-spine + quotes +
    ppm domains; EQ-internal runs a slim worker/service set.
  - **Same-numbered migrations denote different content per tenant:**

    | #    | EQ (`zaap`)                    | SKS (`ehow`)                     |
    |------|--------------------------------|----------------------------------|
    | 0018 | `dashboard_counts_asset`       | `gm_reports`                     |
    | 0019 | `dashboard_asset_service_due`  | `gm_report_archive`              |
    | 0020 | `service_cmms`                 | `canonical_seed_from_eq_quotes`  |
    | 0021 | `service_ppm_rpcs`             | `sites_management_rpcs`          |
    | 0022 | `canonical_write_rpcs`         | `canonical_write_rpcs` (matches) |

  - **The ledger (`eq-shell/supabase/MIGRATION-LEDGER.md`) is inaccurate:** it
    claimed `0028` was "unapplied on both." Live: `0028_contact_customer_links`
    **is applied on EQ** (v20260530113714) and **missing on SKS**.
  - `0012`/`0013`/`0023` present on SKS only (confirmed). Duplicate version rows
    seen within each tenant (`001_worker_profile`, `014_rollback_column_fix`,
    `015_policy_gap_fill` applied twice), indicating a non-idempotent ledger.
- **CI question answered:** A drift job EXISTS —
  `eq-shell/.github/workflows/tenant-drift.yml` runs `scripts/check-tenant-drift.mjs`
  (weekly cron + manual dispatch). It fingerprints live `app_data` **schema shape**,
  **not** migration identity, and is **not a blocking PR check**. It therefore
  cannot catch the number-collisions above. `STATE.md:98` is partially stale (schema
  guard built; ledger-application guard not).
- **Caveat:** Some divergence may be by design (SKS legitimately runs modules EQ
  does not). The finding is that there is no shared, enforced lineage and the ledger
  misreports reality — not that every gap is a defect.
- **Recommended next step:** Add a ledger-**identity** check to
  `check-tenant-drift.mjs` (per-tenant `_eq_migrations` rows vs
  `supabase/tenant-migrations/*.sql`), wire it as a required PR check, and correct
  the `0028` row in `MIGRATION-LEDGER.md`.

### F6 — Cards coupling
- **Status:** PARTIAL (Path A consolidated; standalone email-OTP entry still live)
- **Severity:** MEDIUM
- **Evidence:**
  - Path A consolidated: `eq-cards/ARCHITECTURE.md:654-679` — data moved to
    eq-canonical (`jvknxcmbtrfnxfrwfimn`) via Unit 3 migration + Unit 4 flip; Shell
    mints a JWT (`app_metadata.tenant_id`) passed via `#sh=<jwt>` → `setSession`.
  - **Standalone email-OTP NOT retired:** `ARCHITECTURE.md:670,791` — standalone
    access uses email-OTP directly against eq-canonical (the control plane). Cards'
    Flutter `lib/features/auth/` still ships `email_entry_screen` + `otp_screen`.
  - Legacy project `hshvnjzczdytfiklhojz`: 3 doc references only, no live code
    reference (client reads URL via `--dart-define`, `lib/main.dart:16,54`). Doc
    says kept live for the rollback window only.
- **Recommended next step:** Decide whether standalone email-OTP is an intended
  product surface or a retirement gap; if the latter, gate Cards Shell-only and
  decommission `hshvnjzczdytfiklhojz` (verify zero referenced rows first).

### F2 — Context sync drift — LIVE-VERIFIED, QUANTIFIED
- **Status:** CONFIRMED (UPSERT-only + a second defect: root docs never sync)
- **Severity:** MEDIUM
- **Evidence:**
  - `eq-context/.github/workflows/sync-context.yml:58-101` — sync is **UPSERT-only**
    (`Prefer: resolution=merge-duplicates`, POST `on_conflict=slug`). No
    delete/rename reconciliation → deleted/renamed files leave orphan rows forever.
  - **Live diff (84 `context_files` slugs vs repo tree, 2026-06-02):** the mirror is
    essentially a **subset** of the repo. No clear orphan slugs found. But a whole
    class of current **root-level working docs is absent from the mirror**, including:
    - `STATE.md` (the sprint source of truth)
    - `SPRINT-BOARD.md`, `SPRINT-2-BOARD.md`
    - `security-secret-rotation-runbook-2026-05-31.md` (the F3 runbook)
    - ~14 more (dated audits, backlogs, `AUTONOMOUS-SPRINT-RULES.md`, handoff doc,
      `CHATGPT-PROMPT.md` / `GROK-PROMPT.md` / `COWORK-PROMPT.md`)
  - **Implication:** any agent reading context via the Supabase mirror cannot see
    STATE.md or the rotation runbook. The fork cuts both ways — orphans on delete
    *and* never-ingested root docs — so the mirror is the unreliable copy, not the repo.
- **Recommended next step:** Add a delete-orphans pass AND widen the file glob to
  include root-level `*.md` (or move working docs under a synced directory) in
  `sync-context.yml`.

### F4 — Cross-tenant read model
- **Status:** CONFIRMED (consumed; per-tenant only; no cross-tenant fan-out)
- **Severity:** LOW
- **Evidence:** `canonical_events` is read by
  `eq-shell/netlify/functions/ai-briefing.ts:1-37` (last-48h events scoped to the
  requesting user's single tenant via `getTenantDataClientById`). No fleet/platform-admin
  fan-out across tenant projects for reporting/billing. Multi-tenant fan-out exists
  only operationally (`tenant-routing-health.ts`, `check-tenant-drift.mjs`).
- **Recommended next step:** None now. If platform-admin reporting is built, design
  it as explicit per-tenant fan-out through tenant-routing — never a shared
  cross-tenant table.

### F5 — "canonical" naming overload
- **Status:** CONFIRMED (overloaded); LOW residual risk (code disambiguates)
- **Severity:** LOW
- **Six distinct meanings:** (1) control plane `eq-canonical`/`jvkn`; (2) tenant
  stores `eq-canonical-internal`/`zaap` + `sks-canonical`/`ehow`; (3) `app_data`
  schema; (4) `canonical-api.ts` write API; (5) `canonical_events` table; (6)
  eq-context "canonical context store" (`context_files`).
- **Highest-risk collision:** control plane (`jvkn`) vs EQ tenant (`zaap`).
  Disambiguated in code by distinct env vars (`CONTROL_PROJECT_REF` vs
  `CANONICAL_INTERNAL_PROJECT_REF`). Live risk is to humans/agents doing a blanket
  "canonical" refactor, not to running code.
- **Recommended next step:** Add a "canonical disambiguation" block to
  `system/architecture.md` listing the six meanings.

---

## Step 0 — Canonicality Finding

**The repo file tree is canonical and current. The Supabase mirror is its lagging,
incomplete cache. The prompt's "suspected 2026-04-18 fork to state/ + knowledge/" is
incorrect.**

- `README.md` is `last_updated: 2026-05-07` and describes the 4-tier model
  (`eq/ sks/ ops/ system/` + `rules/ sks-team/ archive/`) as live since 2026-05-04.
  The repo on disk **is** that model. There is no surviving `state/` + `knowledge/`
  structure (retired by `ops/decisions.md:490-510`).
- `CLAUDE.md` and `ops/decisions.md:622` make GitHub the source of truth; Supabase
  syncs from it.
- The F2 live diff confirms the direction: the mirror is missing current repo files,
  so the **mirror** is the unreliable copy.

---

## Unverified Items (remaining)

- **F1 by-design vs accidental split:** whether the EQ/SKS lineage divergence is
  intended (per-tenant module sets) or accidental was not adjudicated — needs an
  owner decision against the intended tenant module matrix.
- **F2 exact unsynced count:** the Glob of the repo tree was truncated, so the
  ~18 unsynced root docs is a floor, not an exact count.
- **F6 product intent:** whether standalone Cards email-OTP is intended is a product
  call, not verifiable from code.

---

## Highest-Priority Action

**Write the `TENANT_ROUTING_MASTER_KEY` rotation runbook and close the
migration-identity CI gap — one combined eq-context + eq-shell change.** Files a
follow-up session would touch:

- `eq-context/system/tenant-routing-master-key-rotation.md` *(new)* — re-encrypt-all-rows
  procedure; reference `eq-shell/netlify/functions/_shared/encryption.ts` and
  `flushRoutingCache()` in `tenant-routing.ts`.
- `eq-shell/scripts/check-tenant-drift.mjs` — add per-tenant `_eq_migrations`
  identity check vs `supabase/tenant-migrations/*.sql`.
- `eq-shell/.github/workflows/tenant-drift.yml` — add a `pull_request` trigger so
  drift blocks merges, not just the weekly cron.
- `eq-shell/supabase/MIGRATION-LEDGER.md` — correct the `0028` row (applied on EQ,
  missing on SKS).
- `eq-context/STATE.md:98` — update the "tenant canonical drift guard / not built"
  row (schema half built; ledger-identity half outstanding).

> Auth-adjacent (touches `TENANT_ROUTING_MASTER_KEY` + tenant routing): per
> non-negotiables, any deploy of these changes needs explicit approval. The runbook
> doc itself is safe; the CI wiring and any key rotation are the gated parts.
