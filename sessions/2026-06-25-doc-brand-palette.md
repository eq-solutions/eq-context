---
title: EQ Field — Doc brand palette (WS4) shipped; suite write-path consolidation deferred
date: 2026-06-25
owner: Royce Milmlow + Claude Code
scope: EQ Field v3.5.190 + suite brand-palette consolidation decision
read_priority: reference
---

# 2026-06-25 — Doc brand palette: Field consumer shipped, write-path deferred

## Shipped — v3.5.190 (PR #342 → main `c29b292`, LIVE on field.eq.solutions)
- Prestart / Toolbox / Audit `.docx` exports now colour from the tenant's canonical brand palette
  (`organisations.branding.palette` → `{primary, deep, ice, ink}`) instead of hardcoded EQ blue.
  **SKS docs render SKS navy;** tenants without a palette fall back to EQ blue (byte-identical to before).
- `scripts/site-reports-shared.js`: validated `setPalette()` + `_hex()` guard + `declaration()` helper;
  `_BLUE/_DEEP/_ICE/_INK` tenant-driven; **fail-fast guard** — `buildPackage()` throws if a palette
  wasn't primed (commit `7efec20`), so a future exporter that forgets fails in dev / surfaces in Sentry.
- `scripts/{safety,audits,toolbox}.js`: each exporter calls `setPalette(brand.palette)` before building.
- `scripts/app-state.js`: `palette` added to the canonical branding allowlist.
- Verified: `node --check` clean; functional harness (navy swap, EQ fallback for null/partial/invalid,
  hex normalisation, guard throws-unprimed / passes-primed / re-arms). Deploy-preview green; prod on v3.5.190.

## DB — canonical eq-canonical / jvkn (`jvknxcmbtrfnxfrwfimn`)
- Seeded `public.organisations.branding.palette` (direct UPDATE, **not a migration**):
  `sks` = `1F335C/16284A/EAEEF4/1A1A2E` (navy); `eq` = `3DA8D8/2986B4/EAF5FB/1A1A2E` (current blue).
  `demo-trades` / `melbourne` left `null` on purpose (exercise fallback).
- Finding: `public.organisations` is RLS **read-open** (`organisations_read`, USING true) / **write-closed**
  (no write policy → only `service_role` / `SECURITY DEFINER`). Reads are free suite-wide; only writes need a path.

## Decision — write-path consolidation (Shell/Service → canonical) DEFERRED
Verified the three brand stores are divergent:
- **Shell** = `shell_control.tenants.brand_color` (jvkn) via admin RPC `eq_update_tenant_settings`.
- **Service** = `tenant_settings.{primary,deep,ice,ink}` on **EHOW — NO jvkn connection at all**.
- **Field** = reads `organisations.branding.palette` (jvkn).
Neither app writes `organisations.branding` today; `public.organisations` is a provisioning-time mirror
(`shell_control.tenants` is authoritative). Canonical-write convention (IDENTITY-MODEL §6.2) = `SECURITY DEFINER`
RPC callable by `authenticated`, gated on JWT `app_metadata` (tenant_id / eq_role / is_platform_admin).

**Royce's call: DEFER WS1.5/2/3** — payoff is self-serve palette for NEW tenants and only SKS is live
(already hand-seeded + branded), and the canonical TARGET model is still in flux. Pick up at the 2nd-tenant
onboard using **shape B**: palette lives in `shell_control.tenants` (reuse Shell's admin RPC) → sync to
`organisations.branding` for Field; Service reads canonical. The bound-builder refactor for Field+Service
docx builders is likewise deferred to the builder-unification seam (interim fail-fast guard already shipped).

## Open / next
- v3.5.190 live; SKS navy not yet eyeballed in live Shell context (avoided polluting live SKS data) —
  confirms on the next real SKS export.
- Worktree `sad-black-76cc32` stale (merged); self-deleting cleanup at
  `C:\Projects\eq-field\cleanup-sad-black-76cc32.ps1` — run after the holding session closes.
