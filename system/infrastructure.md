---
title: SYSTEM — Infrastructure Accounts
owner: Royce Milmlow
last_updated: 2026-05-19
scope: Supabase project IDs, Cloudflare, Netlify, GitHub, Beelink workstation
read_priority: standard
status: live
---

# SYSTEM — Infrastructure Accounts

Where things run. Account ownership and project IDs. Quick reference
for AIs needing to confirm "which Supabase / which Netlify / which
account" before connecting.

---

## Infrastructure Accounts

| Service | Account | Notes |
|---------|---------|-------|
| Supabase | Five projects (see table below) | Do NOT assume one project anywhere |
| GitHub | eq-solutions org + milmlow user | All repos private; MCP is read-only (403 on writes). PATs stored in `C:\Projects\.git-credentials.*` — see table below |
| Cloudflare | royce@eq.solutions | Pages + Workers + R2 (sks-assets, eq-assets buckets) |
| GoDaddy | — | Domain registrar only |
| Netlify | dev@eq.solutions | All Netlify sites (EQ + SKS) |
| Beelink | beelink.eq.solutions (Cloudflare Tunnel) | Ryzen 7 7735HS, 32GB RAM, 1TB NVMe; Chrome Remote Desktop |

---

## Supabase Projects — confirm before connecting

| Project ID | Name | Purpose | Access rule |
|---|---|---|---|
| `nspbmirochztcjijmcrx` | sks-labour | **Live SKS staff production data** | **Never touch unless "SKS live" is explicit** |
| `ktmjmdzqrogauaevbktn` | eq-solves-field | EQ Field demo backend | Demo environment |
| `urjhmkhbgaxrofurpbgc` | eq-solves-service-dev | Canonical context store (`context_files` table) — co-tenant with EQ Solves Service product data | Paid/active; primary path for context reads/writes |
| `hxwitoveffxhcgjvubbd` | eq-shell-control | **Shared shell control plane.** Holds `tenants`, `users`, `module_entitlements` — the "who is who" lookup that routes logged-in users to their per-tenant data plane. Read by the 3 EQ Shell Netlify functions (`shell-login`, `verify-shell-session`, `mint-iframe-token`) using the service-role key. | One shared project across all tenants. Not a data plane. Service-role only (used by Netlify functions, never client-side). |
| `jvknxcmbtrfnxfrwfimn` | eq-demo-canonical | EQ Intake Phase 2 canonical spine + the **demo tenant's data plane**. Hosts `eq_schema_registry`, `eq_intake_events`, `eq_intake_templates`, plus the `eq_intake_*` / `eq_set_imported_at` / `eq_schema_registry_one_current` functions deployed via `eq-intake/sql/001-003_*.sql`. | **Authenticated-callable per-tenant data plane.** The commit RPC enforces tenant isolation via in-function `auth.jwt() → user_metadata.tenant_id` check (see `eq-intake/sql/003_schema_version_columns.sql:111`). Migration 004 (search_path pin + revoke PUBLIC, grant authenticated) rewritten 2026-05-19 — **uncommitted in eq-intake, not yet applied to DB**. |

### Shared tables across sks-labour + eq-solves-field

Both Supabase projects share the same EQ Field codebase (one repo, two branches → two sites → two databases). Most schema changes get applied to both projects on the same day.

| Table | Project(s) | Applied | Purpose |
|---|---|---|---|
| `toolbox_talks` (+ RLS + realtime + photos jsonb) | sks-labour + eq-solves-field | 2026-05-14 | Site Reports v2 — toolbox talk submissions. v3.4.75. SKS apply per explicit "SKS live" so Ben can preview via `eq-solves-field.netlify.app/?tenant=sks`. |
| `prestarts` (+ RLS + realtime) | sks-labour + eq-solves-field | 2026-05-13 | Site Reports v1 — prestart submissions |
| `prestarts.photos` (jsonb) | sks-labour + eq-solves-field | 2026-05-13 | Up to 8 base64 photos per prestart, inline |
| `managers.dob_day/dob_month/start_date/archived` | sks-labour + eq-solves-field | 2026-05-13 | Supervisor DOB + start_date + reversible archive |
| `people.archived` | sks-labour + eq-solves-field | 2026-05-13 | Reversible archive on people (parallel to managers) |
| `sites.track_hours/budget_hours` | eq-solves-field only | 2026-04-27 | Project Hours panel (panel removed v3.4.71, columns retained) |

---

## GitHub PATs

Fine-grained PATs. All verified active 2026-05-15. Credential files in `C:\Projects\`.

**Active repos on disk with GitHub remotes:**

| Local folder | GitHub remote | Deploy method |
|---|---|---|
| `eq-context/` | `eq-solutions/eq-context` | git push |
| `eq-solves-field/` | `Milmlow/eq-field-app` | git push |
| `eq-cards/` | `Milmlow/eq-cards` (GitHub exists but not used for deploy) | zip → Netlify (no git remote on local clone) |

(Other folders — `eq-intake`, `eq-quotes`, `eq-solves-service`, `eq-solves-assets`, `eq-solves-jobs`, `eq-website`, `eq-analytics-v2` — are local-only, no git remote.)

**Token inventory:**

PAT values are NEVER substrate-tracked. They live in `C:\Projects\.git-credentials.*` files on the workstation, scope-limited per the table below. If you need a token value, read it from disk on the Beelink — do not paste it into substrate, chat, or any AI session.

| Token label | Credential file | Repos accessible | Status |
|---|---|---|---|
| EQ Solutions | `.git-credentials` + `.git-credentials.eq-solutions` | eq-context, eq-cards, eq-field-app, eq-solves-service | ⚠️ **Compromised — rotate.** Token value was inadvertently committed to substrate 2026-05-15 → 2026-05-19; GitHub push-protection caught it on 2026-05-19. Assume value is exposed in pushed commits prior to the catch. |
| Milmlow | `.git-credentials.milmlow` | eq-context, eq-cards, eq-field-app, eq-solves-service | ⚠️ **Compromised — rotate.** Same exposure as EQ Solutions (token was identical anyway — redundant). Revoke + don't reissue (kept only because identical to EQ Solutions). |
| Milmlow alt | removed from `.git-credentials` 2026-05-15 | eq-context, eq-website, eq-field-app, eq-solves-service | ⚠️ **Compromised — revoke.** Already removed from local credential store, but value was committed to substrate during the same exposure window — must be revoked in GitHub Settings to be safe. |

**Action remaining (rotate sequence):**
1. Revoke all 3 tokens in GitHub Settings → Developer settings → Personal access tokens. Assume compromised.
2. Issue ONE new fine-grained PAT (replaces "EQ Solutions" — the other two were duplicates / stale).
3. Update `C:\Projects\.git-credentials.eq-solutions` and `C:\Projects\.git-credentials` with the new value.
4. Verify push works on eq-context (`git push origin main` against this commit if the post-commit hook didn't already).
5. Don't recommit token values to substrate. Pointer-only.

---

## Beelink Workstation

Primary AI workstation for serious work. Chrome Remote Desktop from
work PC because ThreatLocker blocks Tailscale.

- Hardware: Ryzen 7 7735HS, 32 GB RAM, 1 TB NVMe
- Cloudflare Tunnel: `beelink.eq.solutions` (for exposing local dev servers)
- Local context repo: `C:\Projects\eq-context`
- Local EQ Field repo: `C:\Users\EQ\eq-field-app-demo`
- Global CLAUDE.md: `C:\Users\Royce\.claude\CLAUDE.md`

---

## R2 Asset Buckets

### SKS Logo Assets (R2 — sks-assets bucket)

| File | URL |
|------|-----|
| Colour + Text | `https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/SKS_Logo_Colour_Text_Clean.png` |
| White + Text | `https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/SKS_Logo_White_Text_Clean.png` |
| Colour Arrows | `https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/SKS_Logo_Colour_Arrows_Clean.png` |
| White Arrows | `https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/SKS_Logo_White_Arrows_Clean.png` |

### EQ Logo Assets (R2 — eq-assets bucket, dev@eq.solutions)

Base URL: `https://pub-409bd651f2e549f4907f5a856a9264ae.r2.dev/`

| File | Use |
|------|-----|
| `EQ_logo_blue_transparent.svg` | Web (primary) |
| `EQ_logo_white_transparent.svg` | Web (reversed) |
| `EQ_logo_blue_transparent.png` / `@2x.png` | Raster fallback |
| `EQ_logo_white_transparent.png` / `@2x.png` | Raster reversed |

(Full brand spec, including colours and typography, in `rules/brand.md`.)

---

## Monthly ops

- Supabase → Account → Access Tokens → revoke all but the most recent OAuth token
