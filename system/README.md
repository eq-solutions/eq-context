---
title: SYSTEM Tier — Index
owner: Royce Milmlow
last_updated: 2026-05-04
scope: The substrate itself — how the AI context system works
read_priority: reference
status: live
---

# SYSTEM Tier

Files that run the substrate, not the work. Read by AIs to understand
*how* to use the repo, not *what* the work is.

## Files

| Path | Purpose |
|---|---|
| `architecture.md` | Tech architecture (Cloudflare, Supabase, substrate, single-file HTML pattern) |
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
