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
scoped (7 checks, not 2) and is now built — PR #1639, open. The cross-repo
consumer-check gap has a decision and two open PRs now — Royce picked option 2
(reusable workflow), eq-shell PR #1638 + eq-cards PR #328, not yet merged, two manual
secrets still needed. One thing is still fully open: CHECK 11 — re-scoped 2026-08-27,
and it's a deeper architecture question than "pick a cutoff date" (see §2) — jvkn has
no migration ledger at all for CHECK 11 to diff against, unlike every tenant plane.**

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

**Status: built and shipped by `eq-shell-2a`** — eq-shell
[PR #1639](https://github.com/eq-solutions/eq-shell/pull/1639), same `jq` pattern #1623
used, extended per-check; all 11 filters tested against a synthetic fixture before
committing. Open, not yet merged. Spawned as a
background task (`task_e2eed444`); its resolution turned out messier than the first
write-up here suggested. `work-wiring-priorities-0150f3-c8` — the session two peer
sessions independently stood down for, believing it was already building this — was a
coincidental name match ("wiring" in both names) that was never actually verified by
messaging it directly. It confirmed to `eq-shell-2a` it's an unrelated eq-field task.
`task_e2eed444` genuinely was started by Royce at some point (a `dismiss_task` call
returned "already started, can't be withdrawn" rather than withdrawing it), but left no
GitHub trace and its real session couldn't be identified. Asked directly, Royce said to
have `eq-shell-2a` build it instead. **Lesson for next time:** a session-name pattern
match plus a plausible timestamp is not a verified collision check — message the peer
session directly before telling anyone else "already in progress."

### 2. CHECK 11 — jvkn migration-identity — re-scoped 2026-08-27, deeper than "pick a cutoff date"

#1628's own PR body scoped this as needing "a cutoff-date/strictness design call." Dug
into it properly this pass (read CHECK 3's actual mechanism end to end, then checked
live whether jvkn has the thing CHECK 3 depends on) rather than take that framing at
face value, and the real blocker isn't a date — **jvkn has no equivalent of the thing
CHECK 3 diffs against.**

**How CHECK 3 actually works** (`check-tenant-drift.mjs` ~line 1027): for each tenant
plane, it queries `app_data._eq_migrations` (name, checksum, applied_at) and diffs that
against `supabase/tenant-migrations/*.sql`. Three outputs: `gaps` (repo files never
applied), `outOfBand` (applied rows matching no repo file — the dangerous direction),
and `handInserted` (NULL-checksum rows on/after 2026-07-03 — proof of a hand-INSERT,
since "the runner is the single ledger writer and always stamps a checksum"). The
2026-07-03 date isn't a strictness dial — it's the day the ledger-integrity sub-check
was *introduced*; everything hand-inserted before that is grandfathered as known
history, everything after fails outright.

**Checked live whether jvkn has an equivalent table to diff against — it doesn't.**
`mcp__supabase__list_tables` against jvkn (`public` + `shell_control`, 60 tables) has
no `_eq_migrations`, no `migration_baseline`, nothing migration-shaped. This isn't a
gap in the script — jvkn genuinely has no governed, runner-stamped ledger. The *only*
place "was migration X applied to jvkn" is recorded at all is
`supabase/CONTROL-PLANE-LEDGER.md` — a hand-maintained markdown file, not a queryable
table. That's the same document this whole incident has repeatedly found stale or
wrong (the 2026-08-23 "confirmed live" claim this sprint's own root PR corrected; the
0162/0163/0164 mis-attribution PR #1627 corrected). Confirmed jvkn's own migration
source directory too, while here: `supabase/migrations/*.sql` (not `tenant-migrations`,
not a "control-plane" name — verified by listing it and finding #1634's and the
2026-08-26 `organisations_anon_bootstrap_read` restore migration both there).

**So CHECK 11 can't be "port CHECK 3, pick a date" — there's nothing to port it onto.**
Three real shapes, genuinely different tradeoffs, not decided here:

1. **Live-schema verification (CHECK 13's approach, extended).** Per migration file,
   verify its expected end-state object(s) exist live in the expected shape — no ledger
   table needed, matches how CHECK 13 already handles jvkn (RLS, live-enumerated).
   Needs either fragile SQL-parsing per file, or a hand-maintained manifest mapping
   file → expected object(s) — a new maintenance burden on every future jvkn migration,
   the same kind of burden `CONTROL_PLANE_STACKED_POLICY_ALLOW`/CHECK 9's allow-list
   already carries.
2. **Ledger-file-as-source-of-truth.** Parse `CONTROL-PLANE-LEDGER.md`'s own ✅/❌
   column, diff against `supabase/migrations/*.sql`. Directly automates the exact
   cross-check this session has been doing by hand all day (does the ledger's claim
   match the repo's file list) — which is appealing, but stakes an ABSOLUTE check's
   correctness on a hand-maintained markdown doc that has proven unreliable multiple
   times this same incident. Parsing markdown reliably is also its own fragility.
3. **Detection-only, narrower scope.** Don't try to prove full parity (which needs a
   baseline that doesn't exist) — instead, periodically enumerate jvkn's live schema
   and flag any table/policy/function that doesn't correspond to *any* committed
   migration file (the `outOfBand` direction only, since that's the direction that's
   actually caused every incident so far — a missing *apply* is annoying, an
   *unrecorded* live change is the security-relevant one). Weaker guarantee than a true
   CHECK 3 port, but the part that's actually been recurring, and needs no manifest.

**This doc's lean, if asked:** option 3. It targets the exact failure mode that's
happened 4 times now (organisations_anon_bootstrap_read ×3, field_managers as of this
same day — see pending.md) without inventing a new maintenance burden or trusting a
document already shown to drift. But this is a real architecture call given the
tradeoffs above, not a mechanical one — flagging it with the same weight as the
cross-repo gap got, not deciding it here. Re-verified live: still absent from
`check-tenant-drift.mjs` (no "CHECK 11" text anywhere in the current file) — not
quietly built by anyone since #1628.

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
| 6 | Issue-filer wiring gap — CHECK 6/7/8/9/12/13/14 never reach the auto-filed issue | **Built, PR #1639 open** (`eq-shell-2a`, after an attribution mix-up — see §1) | Merge when ready |
| 7 | CHECK 11 — jvkn migration-identity | **Re-scoped 2026-08-27** — jvkn has no ledger table to diff against at all, 3 real shapes in §2 | Architecture call, not a cutoff date — this doc leans option 3 (detection-only) |
| 8 | Cross-repo consumer-check gap | **Decided, 2 PRs open** (eq-shell#1638, eq-cards#328) | Merge #1638 first, mint `EQ_SHELL_CHECKOUT_TOKEN` + add `CONTROL_PROJECT_REF` on eq-cards, then merge #328 |

**What's actually left: #6 (merge #1639), #7 (architecture call — 3 options, this doc
leans option 3), #8 (merge #1638, mint + add 2 secrets, merge #328). Plus, unrelated to
this incident but found the same day: `app_data.field_managers` tripped CHECK 7
repo-wide — root-caused (a deliberate reviewed cross-repo fix, not drift) and a
content-verified exception is being built now — see `eq/pending/eq-shell.md`.**
