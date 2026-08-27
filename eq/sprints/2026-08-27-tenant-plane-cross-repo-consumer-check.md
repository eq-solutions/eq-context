---
title: Sprint — tenant-plane cross-repo consumer-check gap (field_managers/field_people_directory follow-up)
owner: Royce Milmlow
last_updated: 2026-08-27
scope: What's left after the field_managers/field_people_directory CHECK 7 incident closed. Both live items on the session-close card's "Next" list. Verified live (gh pr view, gh api contents-at-ref, direct workflow-directory listing) immediately before writing, not restated from pending.md.
read_priority: high
status: live
---

# Sprint — tenant-plane cross-repo consumer-check gap

Triggered by Royce saying "sprint this" against the two "Next" items on this session's
close card. Both trace back to the same incident: eq-field's PR #813/#814 (both
legitimate, both merged) tripped eq-shell's CHECK 7 with zero warning to either repo
until eq-shell's own next PR happened to run the drift check — fixed same-day via
[eq-shell#1642](https://github.com/eq-solutions/eq-shell/pull/1642).

---

## Already fixed — no action needed

| Item | Outcome |
|---|---|
| CHECK 7 had no allow-list mechanism for a genuine, reviewed definer-view exception | Fixed — [eq-shell#1642](https://github.com/eq-solutions/eq-shell/pull/1642), merged (`bd0127ed`). Content-verified, not a bare name-match — re-checks the live tenant filter + grant every run. Covers `app_data.field_managers` (eq-field #813) and `app_data.field_people_directory` (eq-field #814) |
| 3 PRs blocked by the above | Confirmed cleared, not assumed from the merge: #1638 and #1639 were already merged directly by Royce (admin override, before #1642 landed) — no action needed. #1635 updated via the GitHub API's update-branch endpoint, CI re-ran green |

---

## The actual sprint

### 1. Tenant-plane cross-repo consumer-check — real gap, Royce's call, not decided here

**This is the same shape as the 2026-08-26 sprint's item 3** (`eq/sprints/2026-08-26-organisations-anon-read-hardening.md` §3) — nothing stops another repo's change to a shared database from re-breaking something eq-shell's CI treats as absolute, with zero pre-merge signal either way. That sprint decided and is mid-build on the **jvkn (control plane)** version of this gap: eq-shell#1638 + eq-cards#328, a `workflow_call` reusable workflow eq-cards' own CI calls before merging anything touching jvkn.

**That mechanism does not cover this incident and can't be trivially extended to.** Confirmed by reading #1638's own description in the prior sprint doc: it runs CHECK 2/6/7/8/10/12/13/14 "by omitting the tenant-plane secrets" — deliberately scoped to jvkn only, verified live that every tenant-plane check skips clean on its own missing-ref guard. `app_data.field_managers`/`field_people_directory` live on ehow and zaap — the **tenant** planes, not jvkn. The #1638 shape is the wrong shape here, not just missing a config flag.

**eq-field is also a structurally different kind of "other repo" than eq-cards, confirmed live (not assumed):** its `.github/workflows/` has 9 workflows — `ci.yml`, `build-bundles-drift.yml`, `cache-buster-drift.yml`, `tokens-drift.yml`, `role-canon-drift.yml`, `accessibility-audit.yml`, `e2e-smoke.yml`, `tag-release.yml`, `notify-substrate.yml` — none touch Supabase, migrations, or database drift in any way. This matches eq-field's own documented model (eq-shell CLAUDE.md, this repo's own memory): it hand-applies `supabase/migrations/*.sql` via the Supabase MCP, with no CI-driven apply step at all. A `workflow_call` reusable workflow triggered the way #328 triggers on eq-cards (from a deploy/apply job) has no equivalent hook point to attach to on eq-field's side — the actual DDL apply happens outside CI entirely, in whichever session's Supabase MCP call did it, sometimes hours or days before the migration file's own PR merges (both #813 and #814's own files say as much: "already applied live... this is the audit-trail commit for a fix already live, not a pending change").

**Three real shapes, genuinely different tradeoffs, not decided here:**

1. **PR-time check, keyed on the migration file, not the apply.** eq-field's own CI (a new job in `ci.yml`, or a new workflow) runs the tenant-plane-scoped subset of `check-tenant-drift.mjs` (CHECK 3/4/5/7/9 — the ones that matter for `supabase/migrations/**` changes) whenever a PR touches that path, using the same reusable-workflow shape #1638 already built as a template. Catches it before merge, matching the intent of the jvkn version — but PR-time still lags the actual apply here (the DDL is often already live before the PR merges), so this catches "did the file match what's live," not "is what's about to go live safe."
2. **Rely on the existing 3-hourly schedule + auto-filed issue, make it faster to act on.** This is what actually caught `field_managers` same-day — the schedule already works, and #1639 (merged) just closed the last gap in it (CHECK 7's own violations weren't reaching the filed issue). The real gap isn't detection, it's that neither repo has a fast, direct channel to the other when the filed issue names an object that traces to a specific commit in a different repo — worth a lightweight addition: have the issue-filer try a `git blame`/`gh api` lookup on the flagged object's likely source and @-mention or link the probable owning repo/PR directly in the filed issue, cutting the investigation this incident needed down from "trace it by hand" to "read the issue."
3. **Documentation/process only — no new CI.** Add a line to eq-field's own migration-authoring guidance (`CLAUDE.md` or a PR template) naming eq-shell's absolute checks (view `security_invoker`, anon grants, RLS) explicitly, so a migration author self-checks before applying rather than eq-shell finding out after the fact. Zero engineering cost, weakest guarantee — depends on someone reading it, same as every other documentation-only mitigation.

**This doc's lean, if asked:** option 2, extended with the small issue-filer improvement described. Both #813 and #814 already came with unusually thorough migration comments explaining exactly the reasoning eq-shell needed to verify safety fast — the actual bottleneck this incident hit wasn't a missing pre-merge gate, it was that tracing "which repo, which PR, which commit" took real investigation time across several cross-session messages before verification could even start. Option 1 (pre-merge CI) is real hardening but pays an ongoing complexity cost (a second reusable workflow, more secrets, more moving parts) to catch something the existing schedule already catches same-day, given eq-field's DDL doesn't apply through CI anyway. Not attempting any of these unprompted — same as the jvkn version, this is a real cross-repo architecture call.

**Decided and built 2026-08-27** (`/decide` pass, then Royce: "build option B"). Feasibility check before building, not assumed: `gh secret list --repo eq-solutions/eq-field` shows exactly one secret (`EQ_CONTEXT_PAT`), zero Supabase credentials — confirming option 1 would need real new credential provisioning (the same bottleneck already stalling #1638/#328), and confirming option 2 genuinely ships with zero new credentials by reusing `FIELD_PERMS_DRIFT_PAT` (already provisioned 2026-08-12 for an unrelated check). Shipped: [eq-shell#1648](https://github.com/eq-solutions/eq-shell/pull/1648) — `scripts/extract-tenant-violation-names.mjs` + `scripts/attribute-violations-to-eq-field.mjs`, wired into `tenant-drift.yml`'s issue-filer as three new best-effort, `continue-on-error` steps. Verified via a 10-case fixture test (both scripts run as real child processes, not simulated) against data shaped like this exact incident, plus a full dry-run of the issue-body-rendering logic confirming the no-match case is byte-identical to the pre-existing output. CI green, including the drift-check job itself. Not yet exercised against a real live violation in production CI (can't force one from a PR) — same open question as item 2 below, now shared infrastructure between them.

### 2. Validate CHECK 7's reviewed-exception logic against a real, live violation

Pre-existing deferred item (`eq/pending/eq-shell.md`), not new this sprint, but worth
scoping since it's small and mechanical — no design call needed, unlike item 1.

`VIEW_INVOKER_REVIEWED_DEFINER`'s hostile-mutation behavior (drop the tenant filter,
widen the grant to anon) is currently verified only two ways: a standalone Node script
simulating the row shapes, and by reasoning about the code. Neither is "a real object,
in a real Postgres database, actually caught by a real CI run." A genuine end-to-end
proof needs: create a disposable scratch view on a non-production project (or a
throwaway table wrapped the same way) that intentionally violates one of the two
guarded properties, run `check-tenant-drift.mjs --no-anon` (or the equivalent narrow
flag) against it, confirm CHECK 7 fails with the expected reason string, then drop the
scratch object. Needs a project it's safe to write throwaway objects to — not ehow or
zaap. Worth 15 minutes whenever someone has Supabase credentials and a spare project;
not blocking anything.

---

## Summary

| # | Item | Status | Action |
|---|---|---|---|
| — | field_managers/field_people_directory CHECK 7 incident | **Fully closed** | Nothing |
| — | 3 PRs it was blocking | **Confirmed cleared** | Nothing |
| 1 | Tenant-plane cross-repo consumer-check gap | **Decided + built** — option 2, [eq-shell#1648](https://github.com/eq-solutions/eq-shell/pull/1648), CI green | Merge when ready |
| 2 | CHECK 7 exception logic not yet exercised against a real live violation | **Scoped, not started** | Whenever convenient — needs a disposable Supabase project |
