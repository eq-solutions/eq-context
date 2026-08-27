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
twice more asking to sprint whatever was still flagged as "next." Re-verified against
live GitHub state and the current `check-tenant-drift.mjs`/`tenant-drift.yml` on
`origin/main` before writing anything each pass — the local eq-context clone has been
1-150+ commits behind `origin/main` at the start of every pass so far (this incident
drew an unusually large number of concurrent sessions), so nothing here is trusted
from a prior read without re-checking.

**The short version, as of this pass: everything is fixed, merged, and live —
including CHECK 11, which this doc spent a whole section on as an open architecture
question two passes ago. Two small things remain, neither a design question anymore:
one manual credential step to finish the eq-cards half of the cross-repo gap, and one
~15-minute live test to prove CHECK 7's new exception logic actually catches a real
violation (only simulated so far). Both scoped below.**

---

## What's left

### 1. Mint `EQ_SHELL_CHECKOUT_TOKEN` + add 2 secrets to eq-cards, then merge eq-cards#328

The only remaining piece of the cross-repo consumer-check gap (full history in §A
below). [eq-shell#1638](https://github.com/eq-solutions/eq-shell/pull/1638) — the
reusable `jvkn-control-plane-check.yml` — is merged and live.
[eq-cards#328](https://github.com/eq-solutions/eq-cards/pull/328) — the advisory job
that calls it — is still open, blocked on:

1. A new fine-grained PAT (`EQ_SHELL_CHECKOUT_TOKEN`, Contents: Read-only, scoped to
   `eq-solutions/eq-shell` only) for the checkout step that fetches
   `check-tenant-drift.mjs` — GitHub has no create-fine-grained-PAT API endpoint, so
   this is a manual step in the GitHub UI, not something a session can do.
2. Adding that PAT + `CONTROL_PROJECT_REF` as secrets on eq-cards (`SUPABASE_ACCESS_
   TOKEN` already exists there).
3. Merging eq-cards#328 once both secrets exist.
4. After a burn-in period with no false positives, revisit promoting it into eq-cards'
   required-checks list — deliberately advisory-only on day one, Royce's call.

### 2. Prove CHECK 7's reviewed-exception logic against a real live violation

`VIEW_INVOKER_REVIEWED_DEFINER` (the content-verified exception PR #1642 added — full
history in §B) has only ever been exercised two ways: a standalone Node simulation,
and the two legitimate entries it was built for (`app_data.field_managers`,
`app_data.field_people_directory`, both currently passing). It's never actually caught
a real violation in live CI. Read the mechanism directly
(`check-tenant-drift.mjs`, `VIEW_INVOKER_REVIEWED_DEFINER` + `checkViewInvoker`) to
scope this precisely: an entry is keyed by exact view name and requires (a) the live
`pg_get_viewdef` output to contain `requiredWhereFragment`, (b) none of
`forbiddenGrantees` to hold a grant, checked fresh via `mgmtRows` on every run — not a
one-time snapshot.

**Don't test this against the two real entries** — `field_managers`/`field_people_
directory` are live, load-bearing views for Field's actual supervisor picker;
temporarily breaking them to prove a CI check works is not a reasonable trade.
Pending.md's own scoping is the right shape: create a disposable **scratch** view
(not touching the real two) on a non-production project, give it `security_invoker=
false` with no matching `VIEW_INVOKER_REVIEWED_DEFINER` entry, confirm CHECK 7 fails
with the expected reason, drop it. `zaap` (EQ tenant) is the natural candidate — it's
already documented elsewhere in this repo's own memory as disposable demo data, not
live, unlike `ehow`/SKS. ~15 minutes. Not attempted this pass — creating even a scratch
object on a live Supabase project is a real action, flagging it rather than doing it
unprompted.

---

## Already fixed — no action needed

| Item | Outcome |
|---|---|
| `organisations_anon_bootstrap_read` dropped a 3rd time (10:34 UTC, out-of-band via eq-cards PR #324) | Restored live, paper-trailed — [PR #1618](https://github.com/eq-solutions/eq-shell/pull/1618), merged |
| `CONTROL-PLANE-LEDGER.md`'s stale "confirmed live" claim on the 08-23 fix | Corrected — [PR #1622](https://github.com/eq-solutions/eq-shell/pull/1622), merged |
| CHECK 10 (`intentional_anon_reads`) wasn't wired to the auto-filed security issue | Fixed — [PR #1623](https://github.com/eq-solutions/eq-shell/pull/1623), merged |
| CHECK 10's own verbose printer crashed on a real violation | Fixed, same PR — [#1623](https://github.com/eq-solutions/eq-shell/pull/1623), merged |
| Unrelated `eq_cards_admin_sync_tenant_access` drift blocking every merge repo-wide | Fixed — [PR #1629](https://github.com/eq-solutions/eq-shell/pull/1629), merged |
| `0162`/`0163`/`0164` mis-attributed to an unidentified out-of-band actor | Corrected — eq-cards' own tracked migrations, not drift. [PR #1627](https://github.com/eq-solutions/eq-shell/pull/1627), merged |
| `CHECK 12`/`13` — stacked-permissive-policy + RLS invariants ported to jvkn | Built and merged — [PR #1628](https://github.com/eq-solutions/eq-shell/pull/1628) |
| `CHECK 14` — tenant/self/org isolation invariant for jvkn | Built and merged — [PR #1633](https://github.com/eq-solutions/eq-shell/pull/1633). Own investigation surfaced the 13-table finding below |
| 13 jvkn tables with an inert `deny_all` policy, no matching grant | Fixed + applied live — [PR #1634](https://github.com/eq-solutions/eq-shell/pull/1634) (`fb7d9c9f`), Royce's explicit go |
| Issue-filer wiring gap — CHECK 6/7/8/9/12/13/14 never reached the auto-filed issue (§A) | Built and **merged** — [PR #1639](https://github.com/eq-solutions/eq-shell/pull/1639) (`70712a97`) |
| `app_data.field_managers` tripped CHECK 7 repo-wide, `security_invoker=false` (§B) | Root-caused as a deliberate reviewed eq-field fix, not drift — see §B |
| CHECK 7 had no allow-list mechanism for a legitimate reviewed exception | Fixed — [PR #1642](https://github.com/eq-solutions/eq-shell/pull/1642) (`bd0127ed`), content-verified not a bare name-match |
| Cross-repo consumer-check gap — architecture decided, jvkn-plane check built | Decided + built — [PR #1638](https://github.com/eq-solutions/eq-shell/pull/1638) (`7771026b`), merged. eq-cards half still open — see "What's left" #1 |
| CHECK 11 — jvkn migration-identity, blocked on "jvkn has no ledger" (§C) | Blocker fixed ([PR #1641](https://github.com/eq-solutions/eq-shell/pull/1641)) then the check itself built — [PR #1646](https://github.com/eq-solutions/eq-shell/pull/1646) (`fbc7b85e`), merged |

`scripts/check-tenant-drift.mjs` is no longer being actively edited by anyone as of
these merges — the earlier "don't touch it" coordination note is stood down.

---

## Full history (reference — everything below is resolved, kept for why)

### §A. The issue-filer wiring gap was wider than first scoped — 7 checks, not 2

`eq/pending/eq-shell.md`'s original note (`task_f5c61eb9`) scoped this as CHECK 7/8
only. The issue-filing step in `tenant-drift.yml` only read 4 of the report's 11 check
groups into the `$ALL` string that becomes the auto-filed GitHub issue —
`function_exec`/`view_invoker`/`column_grants`/`stacked_policy`/`control_plane_
stacked_policy`/`control_plane_rls`/`control_plane_isolation` (CHECK 6/7/8/9/12/13/14)
all already failed CI correctly but never reached the issue on a schedule-only catch,
the exact blind spot #1623 closed for CHECK 10.

Resolution turned out messier than the gap itself: spawned as background task
`task_e2eed444`, which two peer sessions (including this one) each mistakenly believed
was already running in `work-wiring-priorities-0150f3-c8` — a coincidental session-name
match ("wiring" in both) never actually verified by messaging the session directly.
That session, asked directly, confirmed it was an unrelated eq-field task.
`task_e2eed444` genuinely was started by Royce at some point (a `dismiss_task` call
returned "already started, can't be withdrawn"), but left no GitHub trace and its real
session was never identified. Royce, asked directly, had a different session
(`eq-shell-2a`) build it instead: [PR #1639](https://github.com/eq-solutions/eq-shell/pull/1639),
same `jq` pattern #1623 used, all 11 filters tested against a synthetic fixture before
committing, merged (`70712a97`). **Lesson kept for next time:** a session-name pattern
match plus a plausible timestamp is not a verified collision check — message the peer
session directly before telling anyone else "already in progress."

### §B. `app_data.field_managers` tripped CHECK 7 repo-wide — root cause and fix

A different peer session (`documents-to-sign-feature-3035a3-38`) reported CHECK 7
(view `security_invoker` invariant) failing on both tenant planes, blocking every open
eq-shell PR. Root-caused by `eq-shell-d4` (live with Royce): not drift — eq-shell's own
SEC-33 fix (migration 0256, [PR #1510](https://github.com/eq-solutions/eq-shell/pull/1510))
had added a RESTRICTIVE policy on `app_data.staff` that silently broke Field's
Supervision/Leave-approver picker for every non-manager, for 6 days. eq-field's
[PR #813](https://github.com/eq-solutions/eq-field/pull/813) fixed it correctly by
setting `app_data.field_managers` to `security_invoker=false` and re-implementing
tenant isolation inline in the view's own `WHERE` clause — safe (verified live:
`tenant_id` sourced from the caller's JWT, authenticated-only grant, no sensitive
columns) but it trips CHECK 7's zero-allow-list-by-design rule. A second flagged
object, `roster_presence_sks`, was unrelated — eq-field
[PR #812](https://github.com/eq-solutions/eq-field/pull/812)'s own feature, also
already committed properly.

Royce's go was a **content-verified exception**, not a bare allowlist — CHECK 7's own
header comment documents `field_managers` as the object that already hid inside a
stale name-match allowlist through two prior silent regressions, so a static allowlist
would reopen exactly the hole CHECK 7 exists to close. Built:
[PR #1642](https://github.com/eq-solutions/eq-shell/pull/1642) (`bd0127ed`) —
`VIEW_INVOKER_REVIEWED_DEFINER` re-fetches each exempted view's live definition and
grants every run, re-verifying the tenant filter and grantee list rather than skipping
the object by name. Also caught a second view needing the same treatment,
`app_data.field_people_directory` (eq-field PR #814), found while fixing the first.
A third, competing PR (#1643, same idea) existed and was closed in favour of #1642 once
found. Unblocked #1638/#1639 (merged past this via admin-override before #1642 landed)
and #1635 (branch updated post-merge to pick up the fix).

**Still open, see "What's left" #2**: the new exception logic has only been simulated,
never proven against a real live violation in CI.

### §C. CHECK 11 — jvkn migration-identity, and why it took two "real blocker" findings

#1628's PR body scoped this as needing "a cutoff-date/strictness design call." The
first investigation (this doc, earlier the same day) found that framing understated
the problem: **jvkn had no equivalent at all of the ledger table CHECK 3 diffs
against** (`app_data._eq_migrations` on tenant planes) — checked `_eq_migrations` and
`migration_baseline` specifically, found neither on jvkn via `list_tables`, and wrote
up 3 architecture options for coping with that absence (live-schema verification,
treating `CONTROL-PLANE-LEDGER.md` as source of truth, or detection-only on the
out-of-band direction — this doc leaned option 3).

**That premise was itself incomplete**, found by a later session the same day: jvkn
*does* have a native ledger, Supabase's own `supabase_migrations.schema_migrations` —
missed because this doc only checked for an `_eq_migrations`-style custom table, never
Supabase's built-in one. But a live diff of eq-shell's 144 `supabase/migrations/*.sql`
against it found 86-92 with no matching entry under any naming scheme tried —
including migrations confirmed applied and live that same day. Not a data-entry gap:
jvkn had no *governed apply path* at all (unlike the tenant planes'
`tenant-migrate.yml`), so nothing was ever consistently writing to that table in the
first place. Same structural absence this doc originally reasoned about, just a
different specific table than the one first checked.

Royce's call: build the apply-path runner first, hold CHECK 11 itself. Shipped:
[PR #1641](https://github.com/eq-solutions/eq-shell/pull/1641) (`c3bf2c8f`) —
`scripts/migrate-control-plane.mjs` + `control-plane-migrate.yml`, mirroring the
proven `migrate-tenants.mjs` pattern, writing to a new dedicated ledger
(`shell_control._eq_control_plane_migrations`). `--bootstrap` dispatched and verified
live: all 144 files stamped with real checksums, zero gaps, zero out-of-band at
cutover. With a trustworthy ledger finally in place, CHECK 11 itself became a much
more ordinary build — this doc's earlier 3-option framing (written for a world with no
ledger at all) turned out to be moot rather than decided from. Shipped same day:
[PR #1646](https://github.com/eq-solutions/eq-shell/pull/1646) (`fbc7b85e`) — three
dimensions (gaps and out-of-band both informational for now via `--strict-identity`;
checksum drift ABSOLUTE, no grandfather needed since this ledger's writer always
stamps a real checksum, unlike CHECK 3's legacy hand-insert history).

### §D. The cross-repo consumer-check gap — decision and build

`CHECK 10`/`12`/`13`/`14` all ran inside eq-shell's own CI, against eq-shell's own
files or jvkn's own live state — nothing made an **eq-cards** migration (the actual
source of all 3 `organisations_anon_bootstrap_read` regressions) check any of them
before merging. Investigated the real cost of each of 3 scoped options before asking
Royce to pick: found eq-cards' CI already carried a Supabase Management API PAT of the
right kind, which undercut the stated blocker for cross-repo coupling and made the
reusable-workflow shape worth just building rather than picking between near-equal-cost
options.

Royce picked the reusable-workflow shape. One correction mid-build: GitHub's Actions
`access_level` API is `none | user | organization` only, no per-repo allowlist (no
"selected-repo" setting exists, despite that being the first-choice framing) —
re-asked, Royce's call given the corrected options was org-wide `access_level:
organization` over minting a second PAT to avoid it, applied live via `gh api`.
Built: [PR #1638](https://github.com/eq-solutions/eq-shell/pull/1638) — new
`jvkn-control-plane-check.yml`, `workflow_call`, runs CHECK 2/6/7/8/10/12/13/14 by
omitting the tenant-plane secrets (verified live every tenant-plane check skips clean
on its own missing-ref guard). Merged (`7771026b`, admin-override past the CHECK 7
block in §B, unrelated to this PR's own diff).

[eq-cards#328](https://github.com/eq-solutions/eq-cards/pull/328) (the advisory
consumer job) is still open — see "What's left" #1 for the exact remaining steps.

A sibling gap, the same shape one plane over (eq-field can also break a jvkn/tenant-
plane invariant with zero pre-merge signal, same as eq-cards could), was found and
decided separately: [eq/sprints/2026-08-27-tenant-plane-cross-repo-consumer-check.md](../sprints/2026-08-27-tenant-plane-cross-repo-consumer-check.md).
