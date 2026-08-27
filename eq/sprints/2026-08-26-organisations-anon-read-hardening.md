---
title: Sprint — hardening after the 3rd organisations_anon_bootstrap_read regression
owner: Royce Milmlow
last_updated: 2026-08-27
scope: What's left after the 3rd organisations anon-read regression (eq-shell) — sequences in-flight PRs against what's genuinely still unbuilt, so nothing gets duplicated. Every item live-verified (gh pr view, gh api contents-at-ref against current origin/main, ListAgents) immediately before writing, not restated from pending.md.
read_priority: high
status: live
---

# Sprint — hardening after the 3rd organisations_anon_bootstrap_read regression

Triggered by Royce asking to turn this incident's outstanding items into a sprint, then
(this pass) asking to sprint whatever was still flagged as "next." Re-verified against
live GitHub state and the current `check-tenant-drift.mjs`/`tenant-drift.yml` on
`origin/main` before writing anything — the local eq-context clone was 134+ commits
behind `origin/main` at the start of this pass, so nothing here was trusted from a
prior read without re-checking.

**The short version: everything originally scoped is fixed and live. One follow-up PR
(#1634) is open and CI-green but deliberately not applied to live jvkn yet. Live
re-verification of the issue-filer wiring gap found it's bigger than first scoped — 7
checks share it, not 2. Three things are left: that widened wiring gap (mechanical,
ready to build whenever), CHECK 11's design call, and the cross-repo consumer check —
still the only real architecture decision in this whole incident.**

---

## Already fixed — no action needed

| Item | Outcome |
|---|---|
| `organisations_anon_bootstrap_read` dropped a 3rd time (10:34 UTC, out-of-band via eq-cards PR #324) | Restored live, paper-trailed — [PR #1618](https://github.com/eq-solutions/eq-shell/pull/1618), merged |
| `CONTROL-PLANE-LEDGER.md`'s stale "confirmed live" claim on the 08-23 fix | Corrected — [PR #1622](https://github.com/eq-solutions/eq-shell/pull/1622), merged |
| CHECK 10 (`intentional_anon_reads`) wasn't wired to the auto-filed security issue — a schedule-caught drop never surfaced anywhere | Fixed — [PR #1623](https://github.com/eq-solutions/eq-shell/pull/1623), merged |
| CHECK 10's own verbose printer crashed on a real violation (bad `array_agg` handling) | Fixed, same PR — [#1623](https://github.com/eq-solutions/eq-shell/pull/1623), merged |
| Unrelated `eq_cards_admin_sync_tenant_access` drift blocking every merge repo-wide | Fixed — [PR #1629](https://github.com/eq-solutions/eq-shell/pull/1629), merged |
| Duplicate CHECK 10 fix sitting on branch `claude/check10-drift-printer-fix` | Resolved — branch no longer existed on origin |
| `0162`/`0163`/`0164` mis-attributed to an unidentified out-of-band actor | Corrected in the ledger — they're eq-cards' own tracked migrations (PR eq-cards#323/#324), not drift. [PR #1627](https://github.com/eq-solutions/eq-shell/pull/1627), merged (`02a9b405`) |
| `CHECK 12`/`13` — stacked-permissive-policy + RLS invariants ported to jvkn | Built and merged — [PR #1628](https://github.com/eq-solutions/eq-shell/pull/1628), merged (`ea3d649a`) |
| `CHECK 14` — tenant/self/org isolation invariant for jvkn (analog of CHECK 5) | Built and merged — [PR #1633](https://github.com/eq-solutions/eq-shell/pull/1633), squash-merged (`ef075d5f`). Its own investigation found and fixed a reachability-definition bug (13 false positives from a "policy roles alone" test) before shipping, and separately surfaced the 13-table finding below |

`scripts/check-tenant-drift.mjs` is no longer being actively edited by anyone as of
these merges — the earlier "don't touch it" coordination note is stood down.

---

## In flight — open, not yet applied

### PR #1634 — scope 13 inert `deny_all` policies to `service_role`

Follow-up to CHECK 14's own investigation (row above), which found 13 jvkn tables
carrying a `deny_all` policy scoped to `{public}` instead of `service_role` — inert
today (no matching grant on any of them, confirmed via `pg_policies` +
`role_table_grants` + `get_advisors` + a full `src/` grep, all redone live before the
fix was written), but a footgun if a future stray `GRANT` (e.g. fixing an unrelated
permission error) ever lands on one without someone re-checking the policy text first.
Migration narrows `roles` to `service_role` and re-asserts the already-absent `REVOKE`.
Affected tables: `shell_control.tenant_routing`, `.platform_config`,
`.security_groups`, `.provision_tokens`, `.rate_limit_buckets`, `.tenant_config`,
`.tenant_role_overrides`, `.pin_reset_tokens`, `.cards_field_approvals`, `.audit_log`,
`.security_group_perms`, `.user_security_groups`, `public.revoked_agent_tokens`.

Live-verified via `gh pr view 1634` at the start of this pass: **OPEN,
`mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`, every check green** (typecheck/
test/lint, gitleaks, migration-ledger hygiene, the drift-check workflow itself).
Merging it is low-risk — it only adds a migration file and a ledger-adjacent doc note,
no CI or script change, and CHECK 9/12/13/14 all already treat the post-fix state as
correct by their own existing logic.

**Merging ≠ applying.** jvkn control-plane migrations are hand-apply-only (no CI path
— `supabase/CONTROL-PLANE-LEDGER.md`). The PR's own checklist leaves the live
`apply_migration` step for Royce explicitly, per eq-shell CLAUDE.md non-negotiable #6
(auth-adjacent changes need explicit approval before deployment) — this touches RLS on
tables adjacent to credential reset (`pin_reset_tokens`) and tenant role overrides
(`tenant_role_overrides`), so it stays gated even though the change itself is inert
today. **Two separate decisions, not one**: merge the PR (safe, mechanical), and apply
the migration live (Royce's call, whenever convenient — nothing is exposed today, so
not urgent).

---

## The actual sprint

### 1. The issue-filer wiring gap is wider than first scoped — 7 checks, not 2

`eq/pending/eq-shell.md`'s existing note (`task_f5c61eb9`) scoped this as CHECK 7
(`view_invoker`) and CHECK 8 (`column_grants`) only. Re-verified live against the
current `.github/workflows/tenant-drift.yml` and `scripts/check-tenant-drift.mjs` on
`origin/main` for this pass, and the gap is bigger: the issue-filing step (workflow
lines 236–261) only reads four of the report's eleven check groups into the `$ALL`
string that becomes the auto-filed GitHub issue body:

```
ANON=...          # anon_grants
SPINE=...         # spine_rls
POLICY=...        # policy_lint
INTENTIONAL=...   # intentional_anon_reads  (fixed in #1623)
```

Confirmed by reading the `_report` object's own key list (`check-tenant-drift.mjs`
~line 1753) against the workflow step. Every one of these already fails CI correctly
(all folded into `anyFailure`) — they just never reach the auto-filed issue on a
**schedule-only** catch (the 3-hourly cron with no PR attached), the exact blind spot
#1623 closed for CHECK 10:

| Report key | Check | What it guards |
|---|---|---|
| `function_exec` | CHECK 6 | anon-reachable SECURITY DEFINER functions |
| `view_invoker` | CHECK 7 | view `security_invoker` |
| `column_grants` | CHECK 8 | sensitive column grants |
| `stacked_policy` | CHECK 9 | stacked-permissive-policy, tenant planes |
| `control_plane_stacked_policy` | CHECK 12 | same invariant, jvkn control plane |
| `control_plane_rls` | CHECK 13 | RLS-on invariant, jvkn control plane |
| `control_plane_isolation` | CHECK 14 | tenant/self/org isolation, jvkn control plane |

**Fully scoped, no design call needed** — it's the identical 5-line `jq` pattern
`INTENTIONAL` already uses in #1623, extended to these 7 more keys. Their shapes aren't
all identical (`.projects[]` vs `.planes[]` vs a bare `.result`), so each needs its own
short `jq` filter mirrored off the closest existing one rather than one copy-pasted
across all seven. Not built this pass — the ask this round was to sprint what's
flagged, not implement — spawned as a background task for whenever it's picked up.

### 2. CHECK 11 — jvkn migration-identity (deferred by #1628 itself, not forgotten)

#1628's own PR body explicitly scopes this out: a `CHECK 11` mirroring `CHECK 3`
(tenant-plane migration-identity, which derives its expected-object list from
`tenant-migrations/*.sql`) needs a cutoff-date/strictness design call jvkn doesn't have
yet — jvkn's migrations tree has its own grandfather-cutoff precedent (2026-07-03, per
`check-tenant-drift.mjs`'s existing comments) that a jvkn-scoped version would need to
either reuse or deliberately diverge from. Whoever picks this up should read #1628's
reasoning first and coordinate rather than re-deriving the cutoff question from
scratch — it's the same file, same author's already-stated open question. Re-verified
this pass: still absent from `check-tenant-drift.mjs` (no "CHECK 11" text anywhere in
the current file) — not quietly built by anyone since.

### 3. The real gap: nothing stops another repo from re-breaking this

**This is the one item in this whole incident that isn't closed and isn't in flight.**
`CHECK 10`/`12`/`13`/`14` all run inside eq-shell's own CI, against eq-shell's own
migration files or jvkn's own live state. Nothing makes an **eq-cards** migration —
the actual source of all 3 organisations_anon_bootstrap_read regressions so far —
check any of them before merging. Eq-cards' own consumer-trace before PR #324 was
thorough within eq-cards, and still missed EQ Field's cross-repo dependency, because
nothing in that process could see it. That's a structural gap, not a diligence
failure, and none of CHECK 10/12/13/14 touch it — they harden jvkn's *state*, not who's
allowed to *change* it from outside this repo.

Three shapes this could take, none built, none obviously right — **Royce's call, not
decided here:**

1. **Cross-repo CI call.** eq-cards' own migration-touching PRs call out to eq-shell's
   `check-tenant-drift.mjs` (or just the relevant control-plane checks) before merge.
   Catches it pre-merge, which is strictly better than catching it post-merge. Needs
   eq-cards' CI to reach eq-shell's script and jvkn credentials it may not currently
   have wired — real cross-repo CI coupling, not a small change.
2. **Shared package or reusable workflow.** Extract the positive-assertion checks into
   something every jvkn-touching repo (eq-shell, eq-cards, and whichever others end up
   writing to the control plane) pulls in as a required check of their own — a
   `workflow_call` reusable Action, or a small versioned npm package. Each repo already
   needs `SUPABASE_ACCESS_TOKEN`/`CONTROL_PROJECT_REF`-equivalent access to touch jvkn
   at all, so this doesn't add a new credential-sharing problem, just a shared-code
   one. Leans the same direction #1628 already leans (porting checks so the same
   reasoning travels with the code) — **the option this doc would lean toward if asked
   to pick**, but genuinely Royce's call given the setup cost.
3. **Don't prevent it — make it recoverable in minutes, not hours.** Trust the
   already-fixed 3-hourly schedule + auto-filed issue (#1623, and item #1 above once
   built) as the safety net, and spend the effort on mean-time-to-recovery instead: a
   one-command restore runbook, maybe a Slack/PagerDuty ping on that filed issue rather
   than relying on someone noticing it in the GitHub Issues tab. Cheapest option, zero
   cross-repo engineering — but guarantees a 4th occurrence will still happen someday,
   just caught fast instead of slow.

Not attempting any of these unprompted — this is a real architecture decision with
cross-repo implications, not a mechanical fix.

---

## Summary

| # | Item | Status | Action |
|---|---|---|---|
| 1 | 3rd regression, ledger, CHECK 10's 2 bugs, unrelated drift block, duplicate branch | **All fixed** | Nothing |
| 2 | PR #1627 — ledger correction | **Merged** (`02a9b405`) | Nothing |
| 3 | PR #1628 — CHECK 12/13 | **Merged** (`ea3d649a`) | Nothing |
| 4 | PR #1633 — CHECK 14 | **Merged** (`ef075d5f`) | Nothing |
| 5 | PR #1634 — 13 inert `deny_all` policies → `service_role` | **Open, CI green, mergeable** | Merge is mechanical; live apply is Royce's call, not urgent |
| 6 | Issue-filer wiring gap — CHECK 6/7/8/9/12/13/14 never reach the auto-filed issue | Scoped, ready to build | Mechanical — same pattern as #1623, no design call needed |
| 7 | CHECK 11 — jvkn migration-identity | Scoped, not started | Needs the cutoff/strictness call #1628 already flagged |
| 8 | Cross-repo consumer-check gap | Unscoped, not started | **Royce's call** — 3 options above, none built |

**What's actually left: #5 (merge/apply decision), #6 (ready whenever), #7 (design
call), #8 (Royce's call).**
