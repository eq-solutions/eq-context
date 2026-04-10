---
title: CLAUDE.md — EQ Solutions Global Rules
owner: Royce Milmlow
last_updated: 2026-04-10
scope: All assistants working on EQ / SKS / AHD context (tool-neutral)
read_priority: critical
status: live
---

# CLAUDE.md — EQ Solutions Global Rules

> This file governs all assistant sessions across EQ Solutions, SKS Technologies, and related entities.
> Read this first. Apply all rules below throughout the session.
> `AGENTS.md` is an equivalent entry point for non-Claude tools.
> Style standard for writing/updating any file in this repo: see `MD_BEST_PRACTICES.md`.

---

## Session Start Protocol
1. Read this file in full
2. Read state/pending.md - know what's outstanding
3. Confirm what you've read, then ask what we're working on today

---

## Live Context Rule (Non-Negotiable)

This repo (eq-solutions/eq-context) is the single source of truth for all project context.

### How to access (tool-specific):
- Claude Cowork: Use Claude in Chrome to navigate to GitHub and read/edit files
- Claude Chat: Use GitHub MCP tools (get_file_contents, create_or_update_file)
- Claude Code / Cursor / Codex: Use git CLI (pull, commit, push)
- Perplexity / other read-only tools: Read raw files from GitHub web view

### At session start:
1. Read this file + state/pending.md + relevant changelog/ files
2. Confirm context before starting work

### At session end:
1. Update all relevant changelog/[PROJECT].md files
2. Update state/pending.md with any new outstanding items
3. Commit changes to eq-solutions/eq-context on main
4. Commit message format: chore(context): [date] session update - [short description]

### Between sessions:
- Never assume context from memory - always read the repo files
- If GitHub access is unavailable, produce a zip for manual commit (fallback only)

---

## Changelog Rule (Non-Negotiable)
At the end of every session where code, documents, or decisions were produced:

1. Identify which project(s) were touched
2. Write a changelog entry with: date, session URL, who built it, what changed, current status
3. Append to the relevant changelog/[PROJECT].md file
4. If multiple projects were touched, update all relevant changelogs
5. Never skip this step - it is the permanent audit trail proving development history and IP origin

Changelog files:
- changelog/EQ-FIELD.md
- changelog/EQ-EXPENSES.md
- changelog/EQ-QUOTES.md
- changelog/EQ-OPS.md
- changelog/SKS-LABOUR.md
- changelog/AHD.md
- changelog/EQ-CONTEXT.md

---

## Deployment Rules (Non-Negotiable)
- eq.solutions: Cloudflare Pages as zip bundle (EQ Quotes, EQ Ops, website)
- EQ Field demo: Netlify via GitHub, demo branch ONLY
- SKS live app: sks-nsw-labour.netlify.app, main branch ONLY
- Never cross-deploy between these targets
- Never push to demo branch without explicit instruction from Royce
- Never deploy to eq-solves-field.netlify.app directly

---

## Supabase Guardrails
- Always confirm which project/DB before connecting
- Never run INSERT, UPDATE, DELETE, or schema changes without explicit approval
- Read-only SELECT is fine - state query before executing
- Never touch SKS live data unless Royce explicitly says SKS live

---

## Cowork Guardrails
- Never delete files without permission
- Never hardcode API keys
- Never push to GitHub branches without explicit per-session approval
- Auth changes require Chat review before deployment
- State intended actions and wait for go-ahead before proceeding
- Working before refactoring - always

---

## Self-Critique
Triggers: stress test this, devils advocate, give me the 10/10 version
Apply on complex, strategic, or high-stakes tasks only.

---

## Design Standard (EQ Design Brief v1.2)
- Font: Plus Jakarta Sans
- Primary: #3DA8D8 (Sky Blue)
- Background: #EAF5FB (Ice)
- Text: #1A1A2E (Ink)

---

## Entity Structure
- Milmlow Holdings (trustee) > Milmlow Family Trust > Allcraft Solutions (beneficiary)
- CDC Solutions (trustee) > Hexican Holdings Trust (crypto, consulting, EQ ventures)
- EQ Property Solutions (directors: Royce Milmlow + Emma Curth)
- EQ Solutions (not yet incorporated)
- Hexican SMSF
- All entities: Australian FY (1 Jul - 30 Jun)
- Accountant: Webb Financial

---

## Key People
- Royce Milmlow - NSW Operations Manager, SKS Technologies / Director, EQ Solutions
- Emma Curth - Co-director, CDC Solutions + EQ Property Solutions / Owner, Favour Perfect
- Simon Bramall - Project Manager, SKS
- Leif Lundberg, Jack Cluff, Federico Sander, Nathan Anderson - Job Managers, SKS
