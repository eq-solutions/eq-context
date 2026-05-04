---
title: SYSTEM — Infrastructure Accounts
owner: Royce Milmlow
last_updated: 2026-05-04
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
| Supabase | Three projects (see table below) | Do NOT assume one project anywhere |
| GitHub | eq-solutions org + milmlow user | All repos private; MCP is read-only (403 on writes) |
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
