---
title: Session — substrate delivery-layer hardening
owner: Royce Milmlow
last_updated: 2026-06-04
scope: Security + maintainability fixes to the eq-context sync/CI/hook machinery
read_priority: reference
status: live
---

# 2026-06-04 — Substrate delivery-layer hardening

Review of the eq-context *delivery* code (sync workflow, CI guards, git hooks,
secret scanner, proposals migration) — not the prose. Four fixes landed; all
repo-side, no live-DB change, no deploy.

## Live verification first (Rule 0.5)
- `context_files` on `urjhmkhbgaxrofurpbgc`: **115 rows, healthy**, last sync 2026-06-04 10:25 UTC.
- `context_proposals`: **does not exist** — the 2026-05-14 migration was never
  applied. The proposal queue is aspirational/dead infra, not a live exposure.
  This downgraded the "anon can flood the table" finding from live-High to
  latent (fix the migration before it is ever applied).

## Changes
1. **Proposals migration hardened** (`supabase/migrations/2026-05-14_context_proposals.sql`)
   — per-column length CHECK caps (content/patch ≤256 KiB, rationale/notes ≤8 KiB,
   target_path ≤512); removed the dead `proposer can read own` RLS policy (keyed on
   a JWT claim anon inserts never carry); added a "NOT APPLIED — don't apply without
   a consumer" header. Still NOT applied.
2. **Sync orphan-delete safety cap** (`scripts/sync.py`) — aborts if a delete batch
   exceeds 15 rows or 25% of the store. A bad glob edit can no longer silently wipe
   live slugs. Tunable via `MAX_ORPHAN_DELETE`.
3. **Secret scanner reconciled with its own docs** (`scripts/pre-commit-secrets.sh`)
   — added OpenAI `sk-`/`sk-proj-` and a generic high-entropy `key=value` pattern;
   match is now case-insensitive; coverage-parity rule documented.
4. **Sync engine extracted + tested** — 200-line inline heredoc in
   `sync-context.yml` → `scripts/sync.py` + `scripts/test_sync.py` (10 tests). CI
   runs the tests before syncing. Slug semantics verified identical to the 115 live
   slugs (zero re-keying).

## Validation
- 10/10 unit tests pass (slug mapping + orphan cap).
- Secret hook smoke-tested: JWT / generic `api_key=` / `ghp_` PAT blocked; clean
  prose passes (no FP).
- `py_compile` clean.

## Not done (flagged, deferred)
- `[skip ci]` on the auto-bump commit skips the sync workflow → bumped
  `last_updated` doesn't reach Supabase until the next real edit.
- Rule logic triplicated across `.githooks/pre-commit`, `md-health.yml`,
  `frontmatter-check.yml` — collapse to one shared script.
- State-doc sprawl (multiple SPRINT/STATE files) is the root cause behind the
  duplicate-build failures Rule 0.5 fights — worth a consolidation pass.

Security rating of the delivery layer: 6.5 → 7.5/10. Remaining gap is
detect-after-publish on `main` (only GitHub push-protection truly closes it).
