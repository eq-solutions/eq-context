---
title: eq-context — Repository README
owner: Royce Milmlow
last_updated: 2026-07-19
scope: Human-readable entry point for the eq-context repository
read_priority: reference
status: live
---

# eq-context

Private context repository for EQ Solutions, SKS Technologies, and related entities —
used by any LLM assistant (Claude chat, Cowork, Code; Cursor; Codex; Perplexity;
ChatGPT; Gemini; future tools) to maintain continuity across sessions.

**Tier-separated as of 2026-05-04** — `/eq`, `/sks`, `/sks-team`, `/ops`, `/system`, `/archive`.
Sessions ask "EQ or SKS focus?" at the start so context loads cleanly.

**Entry points:**
- `CLAUDE.md` — master context (Claude Code auto-loads this)
- `AGENTS.md` — equivalent entry point for non-Claude tools
- `COWORK-PROMPT.md` — Cowork session starter (paste at start of each session)
- `system/md-style.md` — style guide for writing or updating any MD in this repo

## How it works

Every assistant conversation that produces new knowledge, decisions, or state changes
ends with "update the MD". The assistant commits only the files that changed, with a
clear commit message describing what was added. Once pushed to `main`, the change is
live: the repo is public, so assistants read these files directly from it via raw URLs
(`https://raw.githubusercontent.com/eq-solutions/eq-context/main/<path>`). A merged
commit is the deliverable — there is no separate cache to sync.

## Structure

```
CLAUDE.md                    ← Master index — assistants read this first, always
AGENTS.md                    ← Tool-neutral equivalent entry point
COWORK-PROMPT.md             ← Cowork session starter
CHAT-PROMPT.md               ← Claude Chat session starter
README.md                    ← This file (human-focused)
digest.md                    ← Push-style health feed — read every session, all tiers
suite-state.md                ← Full nightly-refreshed suite snapshot

rules/
  non-negotiables.md         ← Hard rules that override everything
  brand-eq.md                ← EQ colours, fonts, logo rules (Design Brief v1.3)
  brand-sks.md                ← SKS colours, fonts, logo rules
  brand-check.md              ← Final-gate brand checklist for outputs
  deployment.md              ← Deployment guardrails
  stack.md                   ← Default technology stack

eq/                          ← EQ Solutions tier
  README.md                  ← EQ tier index
  pending.md                 ← EQ-only to-do list
  products.md                ← EQ live products (Field, Service)
  field/
    multi-tenancy/           ← MT plan + explainer (active reference)
    permissions/             ← Role/permission matrix
  changelog/
    field.md                 ← EQ Field history
    eq-context.md            ← Substrate self-changelog

sks/                         ← SKS Technologies tier
  README.md                  ← SKS tier index
  pending.md                 ← SKS-only to-do list
  products.md                ← SKS live products (Labour, Receipt Tracker)
  active.md                  ← Rolling active projects
  team.md                    ← NSW team
  templates.md               ← Quote v3 + client context blocks
  changelog/
    labour.md                ← SKS Labour app history

sks-team/                    ← SKS team-facing AI guidance (different audience)
  README.md                  ← SKS-team tier index + rules of the tier
  quoting.md                 ← Canonical router for SKS team quoting

ops/                         ← Operational support
  README.md                  ← OPS tier index
  pending.md                 ← Webb, infra, substrate-discipline items
  entities.md                ← Entity register, accounts, registrations
  decisions.md               ← Append-only decisions (ADR format)
  financial-architecture.md  ← AHD, Delta cliff, CDC PSI

system/                      ← Substrate itself
  README.md                  ← System tier index
  architecture.md            ← Tech architecture (Cloudflare, Supabase)
  infrastructure.md          ← Project IDs, accounts, Beelink
  lessons.md                 ← Tech gotchas (append-only)
  md-style.md                ← MD writing standard (slimmed)
  onboarding.md              ← First-time tutorial

archive/                     ← Parked or deferred — not loaded by default
  README.md                  ← What's in here and why
  changelog-eq-quotes.md     ← EQ Quotes (deferred 6mo)
  changelog-ahd.md           ← AHD (parked to 2027)

sessions/
  YYYY-MM-DD.md              ← Append-only daily logs
  archive/                   ← Older than 30 days

scripts/
  install-hooks.ps1          ← Pre-commit hook installer

.github/workflows/            ← 17 workflows as of 2026-07-16 — no GitHub→Supabase
                                 sync (that path was retired 2026-06-22, see
                                 CLAUDE.md §1). Key ones: digest-refresh.yml +
                                 suite-state-refresh.yml (nightly substrate
                                 regen), claim-expiry.yml + guard-ratchet.yml +
                                 substrate-honesty.yml + index-drift.yml +
                                 frontmatter-check.yml + md-health.yml (CI
                                 gates), backup-*.yml + verify-backup-*.yml
                                 (offsite DR)

hooks/                        ← Session-start/pre-tool-use guards (Python) —
                                 see hooks/README.md
.claude/                      ← Claude Code project config + worktrees
.githooks/                    ← Git-level hooks (installed via scripts/install-hooks.ps1)
supabase/                     ← Local Supabase CLI config, if used
AUTONOMOUS-SPRINT-RULES.md    ← Diverge-proof conventions from the 2026-05-30
                                 sprint — coordination mode retired, conventions
                                 still cited as the origin of the ground-truth-
                                 before-trust rule
```

## Root scratch docs

A number of one-off working docs — sprint plans, audits, runbooks — accumulate
directly at repo root rather than in a tier folder, because they were written
for a single dated piece of work rather than as living substrate. They're not
indexed individually above; this section exists so `scripts/index_drift.py`
has somewhere to point and so they're not simply invisible.

**Archival pass done 2026-07-20** — each of the 22 files previously listed
here was checked individually (read in full, cross-referenced against every
live pointer doc, not just guessed from date) rather than assumed from "most
predate 2026-06-08." 15 were genuinely done and moved into `archive/` (see
`archive/README.md`); the 7 below are still cited as live by something
current and stay at root until whatever cites them is itself resolved:

`SKS-CUTOVER-CRITICAL-PATH.md` — cited by `eq/pending.md` as the current
pre-cutover state; Phases A–C not yet started.
`auth-phase4-hmac-retirement-runbook.md` — cited by
`eq/identity/IDENTITY-MODEL.md` §7.1 as the authority for the completed
HMAC→JWT cutover.
`cross-app-linkage-remediation-plan-2026-06-07.md` — `digest.md` still points
to its §7a for the open SKS anon-remediation policy worklist.
`eq-platform-verified-state-2026-06-03.md` — named explicitly in this
repo's own `CLAUDE.md` as the Rule 0.5 starting snapshot.
`eq-secret-salt-rotation-runbook-2026-06-06.md` — `eq/pending.md` records
the rotation as "DECLINED for now," runbook explicitly kept on file.
`field-feature-backlog-2026-05-30.md` — named "source of truth" in
`eq/punch-list-2026-06-02.md` for still-parked, migration-gated Field items.
`sks-live-sprint-2026-06-07.md` — `digest.md` still lists its Security
Groups Phase 2–5 work as open.

Plus 2 not re-checked this pass (2026-07-16, too recent for the "most predate
2026-06-08" heuristic to apply, actively tied to a program that shipped this
week — needs its own check, not bundled into this one):
`access-model-cluster1-build-plan-2026-07-16.md`,
`dashboard-signals-build-plan-2026-07-16.md`.

## Update frequency

| File / folder | How often |
|---|---|
| `CLAUDE.md`, `AGENTS.md` | Only when structure or rules change |
| `rules/*` | Rarely — annual review (28 April) |
| `*/pending.md` | Every session in the relevant tier |
| `*/products.md` | When product status changes |
| `sks-team/*` | Rarely — only when canonical language or template references change. Single writer (Royce). |
| `ops/entities.md` | When entity/infrastructure changes |
| `system/architecture.md` | When how something is built changes |
| `ops/decisions.md` | Append when a decision is made |
| `system/lessons.md` | Append when a lesson is learned |
| `*/changelog/*.md` | Append when product code is touched |
| `sessions/*` | Every session (new file per ISO date) |
| `archive/*` | Almost never — only on reactivation |

## Never do

- Edit main branch directly for large changes — use a session update workflow
- Delete old session logs — they are the audit trail
- Merge state and rules — they have different update frequencies for a reason
- Cross-pollute tiers — EQ context goes in `/eq`, SKS in `/sks`. Don't mix.
- Reference parked products as live — see `eq/products.md` "Killed / Deferred"
  section (CLAUDE.md §9 is a pointer only, as of 2026-07-19 — don't restate
  facts there, that's the exact bug this rule exists to prevent)
  
