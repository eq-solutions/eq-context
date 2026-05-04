---
title: Changelog — EQ Context Repo
owner: Royce Milmlow
last_updated: 2026-04-28
scope: Append-only history of changes to the eq-context repository itself
read_priority: reference
status: live
---

# Changelog — EQ Context Repo

## [2026-04-28] Substrate-Discipline Closeout — Trigger Fix, Documentation, Audit Cadence
**Built by:** Royce Milmlow + assistant
**Commits:** `27b7f69` (substrate corrections), `fedfaba` (sync workflow defence-in-depth), plus the closeout commit that includes this entry

**Substrate corrections (3 MD files):**
- `knowledge/decisions.md` — three 2026-04-28 entries: context_files schema authoritative, GitHub canonical, "done" defined as fresh updated_at.
- `knowledge/lessons.md` — three new lessons: memory drift on substrate names, update-discipline lapse, false-implementation pattern + verification SQL pattern.
- `state/pending.md` — new "Substrate Discipline — IMMEDIATE" section captured 6 items.

**Substrate freshness fix (the meat):**
- DB trigger `context_files_set_updated_at` applied to `urjhmkhbgaxrofurpbgc.public.context_files` — `BEFORE UPDATE FOR EACH ROW` stamps `updated_at = NOW()`. Before this, the column's `DEFAULT now()` only fired on INSERT, and the GitHub Action's PostgREST upsert (which only sends slug/filename/content) left `updated_at` frozen forever. The freshness signal was structurally unreliable for any file edited after first sync — including the 2026-04-27 audit's "17/30 stale" finding, which was inflated by this bug masking real edits.
- `.github/workflows/sync-context.yml` — `import datetime` + `updated_at` field now sent in the upsert payload (defence-in-depth if the trigger is ever dropped).
- Verification job appended to the same workflow: after the upsert loop, queries the synced slugs and fails the workflow if any has `updated_at < (now − 60s)`. Machine-enforces "done" semantics.

**Substrate documentation closeout:**
- `rules/non-negotiables.md` — new "Substrate" section between Session Discipline and Code & Deployment: GitHub canonical, updated_at as freshness signal of record.
- `knowledge/architecture.md` — fixed stale row caption (`claude_context table` → `context_files`); added "eq-context Substrate" subsection (schema, sync flow, trigger, co-tenant rationale).
- `AGENTS.md` + `CLAUDE.md` — ported the global "always use clickable card UI for questions" rule into the project substrate so it doesn't depend on a user's machine-local global CLAUDE.md being loaded.
- `knowledge/lessons.md` — annotated "Update Discipline Lapsed" lesson with retroactive note about the trigger bug.

**Scheduled audit:**
- Local scheduled task `eq-context-substrate-audit` registered: Fri 9am AEST cron, runs the substrate audit query, surfaces only stale rows.

**Status:** Trigger live, workflow enhanced, all `state/pending.md` "Substrate Discipline — IMMEDIATE" boxes ticked.

**Late-evening iteration — six commits past `7aa4dfb`:**
- `9643440` — `CLAUDE.md` slimmed 211 → 125 lines (40%). Removed sections duplicating content in `state/entities.md`, `state/products.md`, `rules/deployment.md`, `rules/non-negotiables.md`, `rules/brand.md`. Replaced with a "Where things live" navigation table. The substrate non-negotiable shipped earlier the same day made the duplications a liability rather than redundancy.
- `f45b672` — UTF-8 BOM stripped from 7 `changelog/*.md` files. Cosmetic data cleanup; the pre-commit hook fixed earlier already tolerates the BOM.
- `d0bfd57` — `.claude/settings.json` created with a 4-entry permissions allowlist via the `fewer-permission-prompts` skill: `get_advisors`, `list_migrations`, `mark_chapter`, `netlify-project-services-reader`. Read-only MCP tools that fired ≥3 times in recent transcripts. `execute_sql` (104 prompts — most-used MCP) skipped per skill conservatism, flagged for manual review (not in this commit). Same commit also added a Stop-event hook enforcing Session End Protocol §1.
- `beeaa71` — **Stop hook removed.** External chat-surface review applied Goodhart's law: blocking on "did pending.md change" would manufacture compliance theatre. Substrate freshness (mechanical) and session-end completeness (judgment) are different problems; one mechanism shouldn't enforce both. The trigger + workflow verification job + Friday audit are the right enforcement and were already shipped.
- `7a21a50` — MD_BEST_PRACTICES §17.10 added: tool-attribution drift in substrate prose. Codifies the pre-2026-04-26 "Royce Milmlow + assistant" convention. Pre-commit hook gains a WARN-level check flagging vendor-brand AI tool names in newly-added MD content (full pattern in `.githooks/pre-commit`; example list in MD_BEST_PRACTICES §17.10). Excludes README, MD_BEST_PRACTICES, drafts/, .github/, .githooks/.
- `bb86f24` — Tool-attribution sweep: 7 lines across 5 files restored to "+ assistant". Pre-commit WARN ran clean on the sweep itself (additions don't trigger), proving the hook only catches NEW drift on cleanup commits.

**Audit-trail close (this entry):** the six commits above shipped without corresponding updates to `sessions/2026-04-28.md`, `state/pending.md`, or this changelog. External review caught it. This sub-section + matching updates to the session log and pending.md close the gap. Lesson recorded: the substrate-correcting-self loop has to keep including the substrate logs themselves; otherwise the discipline the work enforces lapses in the meta-process of enforcing it.

**Refined decisions:**
- AGENTS.md has evolved past the "thin pointer" framing of MD_BEST_PRACTICES §1 — it's now the canonical cross-LLM entry point carrying the asking-questions rule. §1 updated to reflect this.
- §17.10 gains a one-sentence slogan ("Substrate prose is tool-neutral. Reference the action, not the actor.") plus an exception clause (Anthropic primitives like `AskUserQuestion` and MCP tool IDs are OK in substrate prose; vendor brands are not).

**Honest score on the night's work:** 9.0–9.3/10 per external review, after the audit-trail and codification gaps closed. Self-graded 9.86 was overstated; external review put it at 8.5/10 before this audit-trail close, which was fair.

**Sync-gap close (post-audit-trail):** verification of the audit-trail commit revealed that `MD_BEST_PRACTICES.md` had never synced to Supabase — the workflow's `ROOT_FILES` dict didn't include it. The file is THE substrate style standard yet wasn't reachable from the assistant-readable cache. Added to `ROOT_FILES` with slug `md_best_practices`. First sync occurs on this commit.

## [2026-04-18] Full Sweep Audit and Rewrite
**Built by:** Royce Milmlow + assistant
**Changes:**
- Supabase section across CLAUDE.md, state/entities.md, rules/deployment.md, rules/non-negotiables.md, knowledge/architecture.md rewritten to reflect three projects (sks-labour live, eq-solves-field demo, eq-solves-service-dev context store) — replaces old "one project" rule
- EQ Design Brief bumped v1.2 → v1.3 in CLAUDE.md; rules/brand.md rewritten around v1.3 (two logo variants, WCAG AA, Aptos Display for print)
- R2 logo URLs (SKS + EQ) captured in rules/brand.md
- SKS active project list added to CLAUDE.md (AWS SYD053, AirTrunk SYD3, NEXTDC S3, Equinix SY6, DigiCo)
- EQ Solves Service promoted to primary build in state/products.md
- AHD moved to Parked status in state/pending.md (revisit 2027)
- GitHub MCP 403 status surfaced as live infrastructure blocker across CLAUDE.md, deployment rules, pending.md
- Beelink workstation spec captured (Ryzen 7 7735HS, 32GB, 1TB NVMe, Chrome Remote Desktop, Cloudflare Tunnel)
- `_headers` security file requirement formalised
- Non-negotiables rule #4 rewritten: "never touch SKS live Supabase" replaces "never spin up new Supabase project"
- Real-client-names rule promoted to non-negotiable
- Two new decision log entries appended (v1.3 adoption, three-project split)
**Status:** Repo rewritten; SKS Labour + EQ Field version numbers pending Royce confirmation before push

## [2026-04-10] MD Best Practices and Cross-LLM Portability Pass
**Built by:** Royce Milmlow + assistant
**Changes:**
- Added `MD_BEST_PRACTICES.md` — cross-LLM style guide (YAML frontmatter, tool-agnostic phrasing, ISO dates, token budgets, Perplexity-specific guidance)
- Added `AGENTS.md` at repo root as a tool-neutral entry point alongside `CLAUDE.md`
- YAML frontmatter added to every MD file in the repo
- Replaced `Claude (Anthropic)` with `assistant` across changelogs for tool-neutrality
- Stripped expired `claude.ai/chat/...` session URLs from changelog entries
- Split responsibility between `knowledge/architecture.md` (what is built) and `knowledge/decisions.md` (why it was chosen)
- Bumped `last_updated` to 2026-04-10 across all files
**Status:** Repo conforms to MD_BEST_PRACTICES v1.0

## [2026-04-06] Live Context System - GitHub MCP Setup
**Session:** Cowork session
**Built by:** Royce Milmlow + assistant
**Changes:**
- GitHub PAT generated for Claude Desktop
- MCP config created for Claude Desktop Chat mode
- CLAUDE.md updated with Live Context Rule
- Changelog folder created and backfilled from session history
- Repo cloned to Beelink at C:\Users\EQ\eq-context
**Status:** Cowork pushing via git, Chat mode MCP pending verification

## [2026-04-05] MD System Built
**Built by:** Royce Milmlow + assistant
**Changes:**
- eq-context folder structure created (CLAUDE.md + rules/ + state/ + knowledge/)
- Four Claude projects created with MD files uploaded
- GLOBAL_CLAUDE.md placed on Beelink
- Self-critique prompts baked into global instructions
**Status:** System live - GitHub auto-sync was pending
