---
title: Machinery Index
owner: Royce Milmlow
last_updated: 2026-08-18
scope: Every executable file in the substrate — hooks, scripts, CI workflows — and what each one actually does. The prose tiers have per-file tables enforced by index_drift; until 2026-08-15 the machinery had none.
read_priority: reference
status: live
---

# Machinery Index

The substrate's prose has had a per-file index for months — every tier README
carries a Files table and `index_drift.py` fails CI when a file is missing from
it. **The executable half had no such index**: 18 files in `scripts/`, 22
workflows, 6 CI scripts, and a `hooks/README.md` that had fallen four files
behind. That is the half where a filename tells you least — `substrate_honesty.py`,
`prune_ratchet.py` and `claim_expiry.py` are not self-describing.

This file is that index, and `index_drift.py` now enforces it: add a hook,
script or workflow without a row here and CI fails.

**Do not restate behaviour here.** Every entry is one line — what it does and
when it runs. The *why* lives in each file's own docstring, which is where it
stays accurate. Several of these guards exist because of a specific recorded
failure; those carry the `F-number` so `system/failures.md` remains the one
home for the story.

---

## `hooks/` — rung 4, prevention

Wired into the live session via `hooks/settings.template.json`, copied into
`C:/Users/EQ/.claude/settings.json`. These run whether anyone remembers them or
not, which is the point.

| File | What it does | Fires |
|---|---|---|
| `session_start.py` | The session gate: SYNC (F1), FRESHNESS (F1), NEEDS YOU, GOALS (F3), RATCHET, CLAIMS, HOOKS (F10). Prints unprompted before the tier question. | SessionStart |
| `substrate_sync.py` | Keeps the clone current and says so loudly when it is behind `origin/main`. Replaced an inline blob that swallowed its own pull failures (F1). | UserPromptSubmit |
| `pre_tool_use.py` | Blocks writes that would reproduce a known failure — mount-corruption (F2/F6), F7, F9, F10, and the F13 deploy-posture claim. Prevention, not documentation. | PreToolUse |
| `session_end.py` | Stop gate — the bookend to `session_start.py`; enforces the §10 session-end protocol. | Stop |
| `auto_pr_guard.py` | Leash for an auto-PR-finding agent. Inert for normal sessions — exits before reading stdin unless `EQ_AUTO_PR_MODE=1`. | PreToolUse |
| `ratchet_rules.py` | **Not a hook** — the single definition of "is this guard overdue for promotion", imported by both `session_start.py` and `.github/scripts/guard_ratchet.py`. Two copies had already drifted. | imported |
| `settings.template.json` | The wiring itself. Logic lives in this repo; only wiring lives in the live settings file. | — |
| `adversarial_test.py` | 104 regression tests for every guard above. Standalone runner, not pytest. | CI + local |
| `test_session_start_sync.py` | Proves the gate can never report a clean sync for a diverged clone. Builds real throwaway git repos. | CI |
| `test_ratchet_rules.py` | Pins the promotion rule, including the field-order case that broke the old regex. | CI |

## `scripts/` — checks and engines

Run by CI workflows and by hand. Each `*.py` with a `test_*.py` sibling keeps
its pure logic separable — that is the convention, not an accident.

| File | What it does |
|---|---|
| `index_drift.py` | Verifies every tier README lists its own folder — and now that this file lists every machine. Strict-gates in CI. |
| `session_start_budget.py` | Caps what a session pays to start. Fails when the mandated read chain exceeds its byte budget. |
| `prune_ratchet.py` | Ceilings on the shapes that re-bloat — residue items, loose root files, unindexed archives. Refuses regrowth; does not prune. |
| `review_clock.py` | Classifies every doc `generated`/`record`/`state` from its path, and clocks only the state. Catches a dead refresh cron, a record given a review date, and staleness past its ceiling. |
| `changelog_duplicates.py` | Every `eq/changelog/*.md` duplicate must self-mark (`superseded_by:` or `UNRECONCILED PAIR`) — catches a silent live/live duplicate before it costs another PR #727. |
| `link_check.py` | Every internal markdown link must resolve to a real file. Ratchet at 0, no headroom. |
| `rotate_pending.py` | Moves done items out of the tier `pending.md` files into their archives, per item rather than per session. |
| `substrate_honesty.py` | Verifies load-bearing facts against reality — dead project refs, the F13 deploy-posture claim, liveness probes. |
| `claim_expiry.py` | The F3 guard: expires stale incident claims so a dead claim cannot block a live investigation. |
| `generate_session_index.py` | Regenerates `sessions/INDEX.md`, reverse-chronological. |
| `md-health-daily.py` | Beelink-local cross-repo git audit (uncommitted work, unpushed commits, stale locks, cleanup-patch leftovers) across every repo in `C:\Projects` — structurally cannot run in CI, which checks out only eq-context. Trimmed 2026-08-15: its eq-context-only sub-checks (freshness, broken links, duplicate sessions) moved to gated scripts below; nothing consumes its JSON output. |
| `duplicate_sessions.py` | No two `sessions/*.md` files may hold byte-identical content — extracted whole from `md-health-daily.py`, the one genuinely unique, portable check it had. |
| `security_audit.py` | Cross-project Supabase security-advisor sweep. Needs `SUPABASE_ACCESS_TOKEN`; no-ops cleanly without it. |
| `rls_probe.py` | The public-key data-leak test — proves an anon key returns zero rows where it should. |
| `test_index_drift.py` · `test_session_start_budget.py` · `test_prune_ratchet.py` · `test_rotate_pending.py` · `test_substrate_honesty.py` · `test_claim_expiry.py` · `test_review_clock.py` · `test_changelog_duplicates.py` · `test_link_check.py` · `test_duplicate_sessions.py` · `test_security.py` | Unit tests for the pure logic of their namesakes. No network, no fixtures on disk. |

## `.github/scripts/` — generators

These write files that other things read. All are append- or refresh-style, so
each one needs an eviction story; `refresh_suite_state.py` had none until
2026-08-15.

| File | What it does |
|---|---|
| `refresh_digest.py` | Generates `digest.md` — the push-style "what needs your attention" view, including the **Needs you** block the session gate reads. |
| `refresh_suite_state.py` | Refreshes `suite-state.md` from live systems; evicts Key Decisions past the 30 most recent. |
| `guard_ratchet.py` | The self-improving loop — opens one issue when a guard is overdue. Propose-only; never edits a rung. |
| `fix_frontmatter.py` | One-shot backfill for missing frontmatter keys. Historical. |
| `test_pending_queue_health.py` · `test_scheduled_workflow_health.py` · `test_pending_dupes.py` | Unit tests for `refresh_digest.py`'s pure logic — queue health/scheduled-workflow counting, and possible-duplicate-pending detection. |

## `.github/workflows/` — 22 workflows

**Gates** (block a bad merge):

| Workflow | Trigger |
|---|---|
| `md-health.yml` — markdown style, session-start budget, prune ratchet, review clock, changelog duplicates, link check, duplicate sessions | PR + push |
| `frontmatter-check.yml` — frontmatter schema + line endings | PR + push |
| `index-drift.yml` — strict, every tier plus this file | cron + PR |
| `adversarial-suite.yml` — the 104 guard regressions + hook tests | cron + PR + push |
| `substrate-honesty.yml` — load-bearing facts vs reality (report-only; `SUBSTRATE_HONESTY_STRICT` is Royce's call) | cron + PR |
| `jwt-contract-drift.yml` — JWT contract drift across apps | cron + PR + push |
| `claim-expiry.yml` — F3 stale-claim guard | cron + PR + push |
| `handoff-probe.yml` — handoff secret probe | cron + PR |
| `security-audit.yml` — Supabase advisor sweep | cron + push |

**Refreshers** (keep generated files current):

| Workflow | Trigger |
|---|---|
| `digest-refresh.yml` — rebuilds `digest.md` + `sessions/INDEX.md` | nightly |
| `suite-state-refresh.yml` — rebuilds `suite-state.md` | nightly |
| `pending-rotate.yml` — rotates done items out of the pending queues | nightly |
| `guard-ratchet.yml` — proposes overdue guard promotions | daily 19:00 UTC + push |

**Platform DR** — three databases, each with the same three-stage cycle: take
the backup, verify it restores, then drill the restore end to end. All nightly,
all owned by eq-context rather than by any consuming app (the old
eq-service-owned job was schema-only and covered 2 of 6 buckets). A backup
nobody restores is not a backup, which is why `verify-` and `restore-drill-`
exist as separate workflows rather than as steps.

| Workflow | Database |
|---|---|
| `backup-ehow.yml` · `verify-backup-ehow.yml` · `restore-drill-ehow.yml` | `ehow` — sks-canonical, the live DB for Service + Field |
| `backup-eq-canonical.yml` · `verify-backup-eq-canonical.yml` · `restore-drill-eq-canonical.yml` | `eq-canonical` — browser control plane |
| `backup-eq-canonical-internal.yml` · `verify-backup-eq-canonical-internal.yml` · `restore-drill-eq-canonical-internal.yml` | `eq-canonical-internal` — server-only tenant data plane |

---

## Adding a machine

1. Write it with a real docstring — that is where the *why* lives.
2. Add a one-line row here.
3. If it has pure logic, add a `test_*.py` sibling **and wire it into a workflow
   by name.** CI here invokes every test explicitly; a test file that merely
   exists never runs, and an unrun guard is F10's "rung 4 on paper, rung 0 in
   practice".
4. `index_drift.py` fails if you skip step 2.
