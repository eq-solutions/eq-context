---
title: Autonomous Sprint — Rules
owner: Royce Milmlow
last_updated: 2026-05-30
scope: Diverge-proof conventions for all parallel autonomous agent work across EQ repos
read_priority: critical
status: live
---

# Autonomous Sprint — RULES (read before doing anything)

These are the hard conventions that make parallel autonomous work **diverge-proof**. Every one exists because we hit the failure on 2026-05-30. Breaking one re-introduces a known break. If a task seems to require breaking a rule, STOP and flag it — don't work around it.

## 0. The one hard line — SKS LIVE IS UNTOUCHABLE
Autonomy is **full-auto build → PR → merge → deploy on green**, EXCEPT:
- **Never deploy to `sks-nsw-labour.netlify.app`.** No pushes/merges that trigger a build of the SKS live site.
- **Never write to the SKS live database** (`sks-labour`, Supabase `nspbmirochztcjijmcrx`). Read-only at most, and prefer not at all.
- **Never run the Field-merge CUTOVER** (repointing the SKS Netlify site at the merged repo) — that is a Royce-gated step (board item B5).
- The merged Field codebase is built/tested **EQ-side only** (`eq-solves-field.netlify.app` + deploy previews). SKS validation is via previews, never the live site.
- **EQ and SKS are separate entities** — never mix code, credentials, or data across them.

## 1. Standing gates (still require Royce, despite full-auto)
- **Auth-flow / MFA / session / password changes** — build + green PR is fine, but **do not deploy** without Royce's explicit OK (his standing non-negotiable; preserved deliberately). Relaxable only by Royce saying so for this sprint.
- **New public GitHub repos** — outward-facing; flag before `gh repo create`.
- Anything sending data to an external/3rd-party service.

## 2. Git hygiene (kills the diverged-main + lost-work failures)
- **Branch from `origin/main`, never local `main`.** `git fetch origin main && git checkout -b <branch> origin/main`. Local mains are routinely ahead/behind with other sessions' commits.
- **Work in your own isolated worktree.** `git worktree add -b <branch> <path> origin/main`. **Never touch, prune, or commit another session's worktree** — it may hold uncommitted work (we saw 85 uncommitted files in one).
- **Stage explicitly** (`git add <files>`), never `git add -A`. **Verify the PR diff contains ONLY your files** before merge (a diverged branch once showed 8 files instead of 3).
- **Gate on the green deploy-preview** before any merge. No merging red required checks.
- Commit-message + PR trailers per repo convention; `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.

## 3. Migrations (kills the dup-version collisions — `0097`, `0110`)
- **Name migrations with a UTC timestamp prefix, NEVER a sequential `00xx`.** Format `YYYYMMDDHHMMSS_description.sql` (generate via `date -u +%Y%m%d%H%M%S` at creation time). Sequential numbers race across parallel branches and collide — this is the single biggest divergence we hit.
- **Never renumber an already-applied migration** without checking the remote `schema_migrations` (use the Supabase MCP `list_migrations`); the remote tracks by recorded version.
- Run Supabase advisors (security + performance) after any migration; zero new ERROR-level findings.
- **Claimed numbers:** `eq-solves-service` `0110` is taken (`0110_performance_level_hf.sql`, #204) — the `charming-dirac` canonical_id back-ref must use a timestamp, not `0110`.

## 4. Coordination (kills two-sessions-in-one-repo)
- **Claim before you start.** In `SPRINT-BOARD.md`, set the item's `owner` + `branch` + `status: in-progress` before touching code. If an item or its repo is already claimed and you'd edit the same files, pick another item or coordinate.
- **One owner per repo-area at a time** where files overlap. Hotspots seen: `eq-shell/src/pages/TenantHome.tsx` (PRs #64/#65/#68/#69).
- **Re-vendor protocol:** changes to `@eq/*` packages (in `eq-intake`) must be re-vendored into `eq-shell` to take effect — do the re-vendor *after* in-flight `eq-shell` PRs settle, and as its own commit.

## 5. Consume, don't copy (kills drift)
- Use `@eq-solutions/tokens` (public, git-dep) for all design tokens — never vendor or hardcode brand colours. CI drift-guards enforce this where copies are unavoidable (Field, Cards).
- Use `@eq-solutions/roles` for the role model once wired — never re-define the 5 tiers or the matrix.
- Plain-English UI copy (no `canonical`/`tenant`/`schema` jargon in labels).

## 6. CI guards (catch divergence automatically — see STATE.md "guards" for status)
- Token drift-guard (Field: shipped; add to other vendored copies).
- **Dup-migration guard** (spec: fail CI if two migration files share a version prefix) — build for `eq-solves-service` first; it broke twice.
- Build + typecheck must pass; `tsc --noEmit` at 0 errors before closing any task.

## When in doubt
Stop and write the question into the board item's `notes`. A blocked-and-flagged item beats a divergent merge.
