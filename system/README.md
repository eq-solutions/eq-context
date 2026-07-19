---
title: SYSTEM Tier — Index
owner: Royce Milmlow
last_updated: 2026-07-19
scope: The substrate itself — how the AI context system works
read_priority: reference
status: live
---

# SYSTEM Tier

Files that run the substrate, not the work. Read by AIs to understand
*how* to use the repo, not *what* the work is.

## System substrate map

Every canonical system file as a full URL — clickable from `/context/claude`:

- [system/TODAY.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/system/TODAY.md) — session focus filter (always loaded first, every session). **Goals currently UNSET** — see failures.md F3; don't assume it still carries the retracted Q3 2026 goals.
- [system/infrastructure.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/system/infrastructure.md) — Supabase project IDs, Cloudflare, Netlify, Beelink, GitHub orgs
- [system/architecture.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/system/architecture.md) — tech architecture (Cloudflare, Supabase, substrate, single-file HTML pattern)
- [system/lessons.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/system/lessons.md) — tech gotchas (append-only)
- [system/md-style.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/system/md-style.md) — MD writing standard
- [system/onboarding.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/system/onboarding.md) — first-time tutorial
- [system/failures.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/system/failures.md) — the guard-ratchet failure ledger
- [system/worktree-registry.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/system/worktree-registry.md) — active/stale git worktrees, check before creating one
- [system/dr-backups.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/system/dr-backups.md) — offsite backup coverage across projects
- [system/substrate-facts.yml](https://raw.githubusercontent.com/eq-solutions/eq-context/main/system/substrate-facts.yml) — CI-checked live/deleted status manifest, drives digest.md's drift check
- [system/task-brief-template.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/system/task-brief-template.md) — Rule 0.6 session-gate brief template
- [system/tenant-routing-master-key-rotation.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/system/tenant-routing-master-key-rotation.md) — tenant_routing key rotation runbook
- [system/chat-bootstrap.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/system/chat-bootstrap.md) / [system/cowork-bootstrap.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/system/cowork-bootstrap.md) — tool-specific session bootstraps
- [system/substrate-plan-v2.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/system/substrate-plan-v2.md) — active substrate-hardening plan (draft, pending confirmation)
- [system/substrate-a-plus-plan.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/system/substrate-a-plus-plan.md) — **archived**, superseded by substrate-plan-v2.md — kept for history, not live
- [system/runbooks/supabase-restore-drill.md](https://raw.githubusercontent.com/eq-solutions/eq-context/main/system/runbooks/supabase-restore-drill.md) — Supabase restore drill runbook (narrowed 2026-07-05 to auth-restore + app-repoint)

## Files

| Path | Purpose |
|---|---|
| `architecture.md` | Tech architecture (Cloudflare, Supabase, substrate, single-file HTML pattern) |
| `git-automation.md` | Post-commit hook, credential helpers, push-failure recovery |
| `infrastructure.md` | Supabase project IDs, Cloudflare account, Netlify, Beelink, GitHub orgs |
| `lessons.md` | Tech gotchas (append-only) |
| `md-style.md` | MD writing standard (slimmed) |
| `onboarding.md` | First-time tutorial |
| `TODAY.md` | Session focus filter — goals currently UNSET |
| `failures.md` | Guard-ratchet failure ledger |
| `worktree-registry.md` | Active/stale git worktrees |
| `dr-backups.md` | Offsite backup coverage |
| `substrate-facts.yml` | CI-checked live/deleted status manifest |
| `task-brief-template.md` | Rule 0.6 session-gate brief template |
| `tenant-routing-master-key-rotation.md` | tenant_routing key rotation runbook |
| `chat-bootstrap.md` / `cowork-bootstrap.md` | Tool-specific session bootstraps |
| `substrate-plan-v2.md` | Active substrate-hardening plan (draft) |
| `runbooks/` | Operational runbooks |

## When to load SYSTEM

- Setting up a new AI tool / onboarding a new model
- Substrate audit (eq-context itself needs review)
- Sync issues, GitHub Action problems, Supabase row drift
- Tech architecture questions (which Supabase, which worker, why)
- Writing or updating any MD file (always check `md-style.md`)
