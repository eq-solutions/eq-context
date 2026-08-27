---
title: Sprint — hardening after the 3rd organisations_anon_bootstrap_read regression
owner: Royce Milmlow
last_updated: 2026-08-27
scope: What's left after the 3rd organisations anon-read regression (eq-shell) — sequences in-flight work against what's genuinely still unbuilt, so nothing gets duplicated. Every item live-verified (gh pr view, gh api contents-at-ref against current origin/main, ListAgents) immediately before writing, not restated from pending.md.
read_priority: high
status: live
---

# Sprint — hardening after the 3rd organisations_anon_bootstrap_read regression

Triggered by Royce asking to turn this incident's outstanding items into a sprint, then
(a later pass) asking to sprint whatever was still flagged as "next." Re-verified
against live GitHub state and the current `check-tenant-drift.mjs`/`tenant-drift.yml`
on `origin/main` before writing anything each pass — the local eq-context clone has
been 130-140+ commits behind `origin/main` at the start of every pass so far, so
nothing here is trusted from a prior read without re-checking.

**The short version: everything originally scoped is fixed, merged, and (where
applicable) applied live — including PR #1634, merged and its migration applied to
jvkn on Royce's explicit go. The issue-filer wiring gap turned out bigger than first
scoped (7 checks, not 2) and is now being built in a separate session. The cross-repo
consumer-check gap has a decision and two open PRs now (2026-08-27, this session) —
Royce picked option 2 (reusable workflow), eq-shell PR #1638 + eq-cards PR #328, not
yet merged, two manual secrets still needed. One thing is still fully open: CHECK 11's
design call.**

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
| 13 jvkn tables with an inert `deny_all` policy (`{public}` instead of `service_role`, no matching grant) — CHECK 14's own follow-up finding | Fixed: eq-shell [PR #1634](https://github.com/eq-solutions/eq-shell/pull/1634) squash-merged (`fb7d9c9f`) on Royce's explicit "merge it," migration **applied to live jvkn same session** after Royce gave the explicit go (a `/decide` pass recommended waiting given no urgency, but Royce authorized it anyway) |

`scripts/check-tenant-drift.mjs` is no longer being actively edited by anyone as of
these merges — the earlier "don't touch it" coordination note is stood down.

---

## The actual sprint

### 1. The issue-filer wiring gap is wider than first scoped — 7 checks, not 2

`eq/pending/eq-shell.md`'s original note (`task_f5c61eb9`) scoped this as CHECK 7
(`view_invoker`) and CHECK 8 (`column_grants`) only. Re-verified live against
`.github/workflows/tenant-drift.yml` and `scripts/check-tenant-drift.mjs` on
`origin/main`, and the gap is bigger: the issue-filing step (workflow lines 236–261)
only reads four of the report's eleven check groups into the `$ALL` string that
becomes the auto-filed GitHub issue body:

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

Fully scoped, no design call needed — it's the identical 5-line `jq` pattern
`INTENTIONAL` already uses in #1623, extended to these 7 more keys (their shapes
aren't all identical — `.projects[]` vs `.planes[]` vs a bare `.result` — so each needs
its own short `jq` filter mirrored off the closest existing one).

**Status: in progress, not this session's build.** Spawned as a background task
(`task_e2eed444`). Two separate peer sessions independently proposed building it
afterward and both stood down after a live collision check (`ListAgents` + `gh pr
list`, no PR open yet either time) found it already running in
`work-wiring-priorities-0150f3-c8`. Check that session's outcome before restarting
this — only pick it back up if it stalled or failed, not as a fresh build.

### 2. CHECK 11 — jvkn migration-identity (deferred by #1628 itself, not forgotten)

#1628's own PR body explicitly scopes this out: a `CHECK 11` mirroring `CHECK 3`
(tenant-plane migration-identity, which derives its expected-object list from
`tenant-migrations/*.sql`) needs a cutoff-date/strictness design call jvkn doesn't have
yet — jvkn's migrations tree has its own grandfather-cutoff precedent (2026-07-03, per
`check-tenant-drift.mjs`'s existing comments) that a jvkn-scoped version would need to
either reuse or deliberately diverge from. Whoever picks this up should read #1628's
reasoning first and coordinate rather than re-deriving the cutoff question from
scratch — it's the same file, same author's already-stated open question. Re-verified
live: still absent from `check-tenant-drift.mjs` (no "CHECK 11" text anywhere in the
current file) — not quietly built by anyone since.

### 3. The real gap: nothing stops another repo from re-breaking this — DECIDED 2026-08-27, PRs open

**Update 2026-08-27 (this session):** investigated the real cost of each option before
asking Royce to pick — found eq-cards' CI already carries `SUPABASE_ACCESS_TOKEN` (same
kind eq-shell's own drift-check job uses: a Supabase Management API PAT), already used
against jvkn in its `deploy.yml` edge-function-deploy step. That undercut option 1's
stated blocker ("credentials it may not currently have wired"), which pulled options 1
and 2 close enough together to just build the reusable-workflow shape (option 2) rather
than pick between them as if they were far apart in cost.

Royce picked: **selected-repo access on eq-shell, advisory-first on eq-cards.** One
correction mid-build: "selected-repo" isn't a real GitHub setting — the Actions
`access_level` API is `none | user | organization` only, no per-repo allowlist (checked
against GitHub's own docs before applying anything). Re-asked; Royce's call given the
corrected options was org-wide `access_level: organization` over minting a second new
PAT just to avoid it — applied live via `gh api`. Separately, and not something either of
those two options avoided: the default `GITHUB_TOKEN` inside a called reusable workflow
is scoped to the *caller* repo only, so a **third** credential is unavoidable either way
— a new fine-grained PAT (`EQ_SHELL_CHECKOUT_TOKEN`, Contents: Read-only, scoped to
eq-solutions/eq-shell alone) for the checkout step that fetches `check-tenant-drift.mjs`
itself. That one can't be minted via API (GitHub has no create-fine-grained-PAT
endpoint) — it's a manual step, flagged in both PRs.

**Open PRs:**
- [eq-shell#1638](https://github.com/eq-solutions/eq-shell/pull/1638) — new
  `jvkn-control-plane-check.yml`, `workflow_call`, runs CHECK 2/6/7/8/10/12/13/14 by
  omitting the tenant-plane secrets (no new CLI flag — verified live that every
  tenant-plane check skips clean on its own missing-ref guard, and the file's one
  `process.exit(1)` is unrelated). `access_level: organization` already applied, not
  gated on this PR.
- [eq-cards#328](https://github.com/eq-solutions/eq-cards/pull/328) — one new advisory
  job calling it. Not in branch protection's required-checks list.

**Still needed before either check actually runs (not done this session — needs
Royce or repo-admin access this session didn't exercise on eq-cards' secrets):**
1. Merge eq-shell#1638 to `main` first (eq-cards' `uses:` reference needs the file to
   exist there).
2. Mint `EQ_SHELL_CHECKOUT_TOKEN` (fine-grained PAT, Contents: Read-only,
   eq-solutions/eq-shell only) and add it + `CONTROL_PROJECT_REF` as secrets on
   eq-cards. `SUPABASE_ACCESS_TOKEN` already exists there.
3. Merge eq-cards#328.
4. After a burn-in period with no false positives, revisit promoting it into eq-cards'
   required-checks list (deliberately not done on day one — Royce's advisory-first call).

Original framing preserved below for the reasoning trail (three options, cost
comparison) — superseded by the decision above, not rewritten.

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
| 5 | PR #1634 — 13 inert `deny_all` policies → `service_role` | **Merged + applied live** (`fb7d9c9f`) | Nothing |
| 6 | Issue-filer wiring gap — CHECK 6/7/8/9/12/13/14 never reach the auto-filed issue | **In progress** (separate session) | Check its outcome; restart only if stalled/failed |
| 7 | CHECK 11 — jvkn migration-identity | Scoped, not started | Needs the cutoff/strictness call #1628 already flagged |
| 8 | Cross-repo consumer-check gap | **Decided, 2 PRs open** (eq-shell#1638, eq-cards#328) | Merge #1638 first, mint `EQ_SHELL_CHECKOUT_TOKEN` + add `CONTROL_PROJECT_REF` on eq-cards, then merge #328 |

**What's actually left: #6 (confirm outcome), #7 (design call), #8 (merge + 2 manual secrets).**
