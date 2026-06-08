---
title: SYSTEM Tier — Index
owner: Royce Milmlow
last_updated: 2026-06-08
scope: The substrate itself — how the AI context system works
read_priority: reference
status: live
---

# SYSTEM Tier

Files that run the substrate, not the work. Read by AIs to understand
*how* to use the repo, not *what* the work is.

## System substrate map

Every canonical system file as a full URL — clickable from `/context/claude`:

- [system/TODAY.md](https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/system/TODAY.md) — Q3 2026 focus filter (always loaded first, every session)
- [system/infrastructure.md](https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/system/infrastructure.md) — Supabase project IDs, Cloudflare, Netlify, Beelink, GitHub orgs
- [system/architecture.md](https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/system/architecture.md) — tech architecture (Cloudflare, Supabase, substrate, single-file HTML pattern)
- [system/lessons.md](https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/system/lessons.md) — tech gotchas (append-only)
- [system/md-style.md](https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/system/md-style.md) — MD writing standard
- [system/onboarding.md](https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/system/onboarding.md) — first-time tutorial

## Files

| Path | Purpose |
|---|---|
| `architecture.md` | Tech architecture (Cloudflare, Supabase, substrate, single-file HTML pattern) |
| `git-automation.md` | Post-commit hook, credential helpers, push-failure recovery |
| `infrastructure.md` | Supabase project IDs, Cloudflare account, Netlify, Beelink, GitHub orgs |
| `lessons.md` | Tech gotchas (append-only) |
| `md-style.md` | MD writing standard (slimmed) |
| `onboarding.md` | First-time tutorial |

## When to load SYSTEM

- Setting up a new AI tool / onboarding a new model
- Substrate audit (eq-context itself needs review)
- Sync issues, GitHub Action problems, Supabase row drift
- Tech architecture questions (which Supabase, which worker, why)
- Writing or updating any MD file (always check `md-style.md`)
