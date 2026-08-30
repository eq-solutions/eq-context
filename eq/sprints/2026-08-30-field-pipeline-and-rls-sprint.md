---
title: Field tenant-migration pipeline + timesheet/leave RLS — close-out sprint
owner: Royce Milmlow
created: 2026-08-30
last_updated: 2026-08-30
scope: Everything left open from tonight's Field tenant-migration pipeline build and the two real RLS gaps it surfaced, sorted into an execution order. Built from the session-close card's 4 "needs you" items — one of them (SEC-1) turned out to be sks-nsw-labour and is excluded per Royce's explicit instruction.
read_priority: high
status: live
---

# Field tenant-migration pipeline + timesheet/leave RLS — close-out sprint

## How this was built

Built from the session-close card's 4 "needs you" rows (2026-08-30 close). One row resolved itself on inspection: "the health check flagged something urgent" was SEC-1 (P0, live PII leak) — which lives entirely on sks-nsw-labour, already deliberately held open pending that app's retirement (see `ops/security-register.md`), and excluded here per Royce's live instruction ("SKS NSW LABOUR is about to be retired — ignore anything relating to that"). The remaining 3 rows plus the card's own "Next" item are what's below.

**One correction made while building this**: the card (and the `/decide` pass behind it) said the ehow write-scoping fix was blocked on "eq-field PR #705, drafted." Checked live via `gh pr view 705` — it's **merged** (2026-08-16), and it's the PR that originally shipped both pending migration files below, not an open gate. That framing came from a stale line in eq-shell's own CLAUDE.md, trusted instead of checked. Fixed in `eq/pending/eq-shell.md`, `eq/pending/eq-field.md`, and `sessions/2026-08-30.md`. The real blocker is named correctly in Wave 2 below.

---

## Execution order

### Wave 1 — ship now, no new decisions (all independent, run in any order)
1. **Merge [eq-shell PR #1684](https://github.com/eq-solutions/eq-shell/pull/1684) + [eq-field PR #846](https://github.com/eq-solutions/eq-field/pull/846)** — the governed migration pipeline itself. Both CI-green (typecheck/test/lint, function-grants, migration hygiene, schema-drift/anon-grant/policy-lint, gitleaks, deploy preview). Merging ships code only — no bootstrap, no dispatch, nothing touches live data.
2. **Provision 3 GitHub secrets on eq-field** (`SUPABASE_ACCESS_TOKEN`, `CONTROL_PROJECT_REF`, `EQ_SHELL_CHECKOUT_TOKEN`) — Royce's action only, Claude Code can't set secret values. Pipeline is inert without them regardless of merge state.
3. **Add "do not re-apply" header warnings to 2 migration files** — `20260611_sks_canonical_field_sync.sql` and `20260816_timesheets_leave_own_crew_read.sql` are both live only via a later, superseding migration; running either for real would regress production (stale table refs / broken identity source). A 3rd file in the same boat (`20260823_field_people_iud_identity_upward_push.sql`) already carries this warning ("DO NOT HAND-APPLY THIS FILE AS-IS") — these two don't yet. 10-minute doc-only fix, zero risk.
4. **Dispatch the zaap read-scoping fix** (`20260821_timesheets_leave_zaap_own_manager_read.sql`) — no stated blocker in the file itself. Worth a 2-minute live check first that zaap's `eq` tenant is still non-live demo data (the premise the low-priority call rests on, last confirmed 2026-06-03) before treating it as low-stakes — then dispatch via `tenant-migrate.yml` on your go.

### Wave 2 — two decisions, unblocks everything left (no build waiting on either)
1. **Bootstrap exclude-list approach.** eq-field's first real bootstrap run needs to skip the 4 genuinely-pending files (they'd otherwise get silently stamped "applied"). Two ways to build it: (a) a `--exclude=<file,file>` flag on `migrate-tenants.mjs`'s bootstrap path — reusable, no working-tree changes at dispatch time; (b) temporarily move the 4 files out of `supabase/migrations/` for one bootstrap run, move them back after. Recommend (a) — same shape as the script's existing flag conventions, and leaves no window where the repo's migrations folder doesn't match its own git history. Your call either way.
2. **Unlinked-staff data-readiness call.** The ehow write-scoping migration's own pre-flight check gates on 36 unlinked workers + 6 unlinked supervisors (of 110 total ehow actors, reconfirmed live today) having no linked `staff_id`. Two ways forward: bring the count down first (same population as the long-standing unlinked-worker backlog already sitting at your own pace — no new effort proposed here), or accept the residual risk and dispatch anyway with an equivalent carve-out to the one you already approved for unassigned supervisors on the read-side fix. Not a decision to make around — needs you either way.

### Wave 3 — depends on Wave 1 + 2 landing
1. **Build the exclude-list mechanism** per whichever approach Wave 2.1 lands on — small change to `migrate-tenants.mjs`'s bootstrap path.
2. **Run eq-field's first real bootstrap** (`bootstrap=true`, excluding the 4 pending files) — needs Wave 1.2's secrets and Wave 3.1's mechanism both in place. Brings eq-field's own migrations under the same governed pipeline eq-cards already uses instead of hand-applying via the Supabase MCP.
3. **Dispatch the ehow write-scoping pair** (`20260816_timesheets_leave_own_crew_write.sql` + `20260819_..._actor_identity.sql`) via `tenant-migrate.yml`, live-verify per each file's own embedded pre-/post-apply checklist — once Wave 2.2 resolves.

---

## Explicitly excluded

- **SEC-1 (P0, live PII leak on sks-nsw-labour)** — Royce, live: "SKS NSW LABOUR is about to be retired — ignore anything relating to that." Already deliberately held open pending retirement, not interim hardening; see `ops/security-register.md`.
- **SEC-57 (revoke `grok-by-xai`)** — already fully scoped in `eq/pending/eq-shell.md`, pure manual GitHub-UI click for Royce, not sprint-shaped work.
- **The `index-drift.yml` "3 consecutive failures" gate alarm** — checked live via `gh run list`: the 5 most recent runs are all `success`, most recent today. The alarm looks stale, not current. Not investigated further; flagging in case the gate itself needs a refresh.
