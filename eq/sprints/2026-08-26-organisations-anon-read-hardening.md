---
title: Sprint — hardening after the 3rd organisations_anon_bootstrap_read regression
owner: Royce Milmlow
last_updated: 2026-08-28
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

**The short version, as of this pass (still 2026-08-28 — Royce came back twice more
the same day, first with an explicit go to run the live tests, then to finish the
credential step himself): the core incident is fully closed, the live-testing item is
fully closed, and the cross-repo consumer-check gap is now fully closed end-to-end.
Only one tail item remains, not blocking anything: eq-cards' own jvkn migrations still
have no governed apply path (3 shapes scoped, Royce's call — §4 below).**

---

## What's left

### ~~1. Mint `EQ_SHELL_CHECKOUT_TOKEN` + add 2 secrets to eq-cards, then merge eq-cards#328~~ — DONE

The last piece of the cross-repo consumer-check gap (full history in §A below).
Royce minted the fine-grained PAT (`EQ_SHELL_CHECKOUT_TOKEN`, Contents: Read-only,
scoped to `eq-solutions/eq-shell` only — GitHub has no API for this, had to be done
by hand in the GitHub UI) and added it plus `CONTROL_PROJECT_REF` as secrets on
eq-cards, confirmed live via `gh secret list` (both added 2026-08-27, ~18:42-43 UTC).

The PR's own original CI run predated both secrets and came back a `startup_failure`
that GitHub refuses to retry — pushed an empty commit to `feat/jvkn-control-plane-
check-advisory` to force a fresh `pull_request` run instead. That run came back clean
across all 4 jobs, including the new one:
**`jvkn control-plane checks (advisory)` — success** — confirms the whole mechanism
end-to-end, not just that the secrets exist: the PAT actually checked out eq-shell's
private repo, ran the jvkn-scoped checks (2/6/7/8/10/12/13/14) against eq-cards' own
footprint, found nothing (expected — the CHECK 6/9/12/13/14 scratch objects from §2
were already cleaned up by this point), and reported success cleanly.

Merged: [eq-cards#328](https://github.com/eq-solutions/eq-cards/pull/328)
(`23abf7a3`), squash, branch deleted.

**Not done, not urgent, Royce's call for later**: after a burn-in period with no
false positives, promote this from advisory into eq-cards' required-checks list.
Deliberately advisory-only on day one — no reason to revisit yet.

### ~~2. Prove the other 6 newly-wired checks against real live violations~~ — 5 of 6 DONE

Royce's explicit go ("run all 5 now") to actually execute what this section had only
scoped. Read each check's exact live-query logic straight from `check-tenant-drift.mjs`
on current `origin/main` first — not assumed to be the same shape as CHECK 7 — then
built one scratch object per check, matched precisely to its SQL (e.g. CHECK 6 checks
`has_function_privilege('anon', …)` specifically, so the grant had to be to `anon`, not
just `authenticated`; CHECK 13 has no allow-list at all, so a bare table with RLS
untouched was enough):

| Check | Scratch object | Plane |
|---|---|---|
| CHECK 6 (`function_exec`) | `zz_scratch_check6_livetest()` — `SECURITY DEFINER`, `EXECUTE` granted to `anon` | zaap |
| CHECK 9 (`stacked_policy`) | `zz_scratch_check9_livetest` — 2 `SELECT` policies, different `qual` text, both `TO authenticated` | zaap |
| CHECK 12 | same shape as CHECK 9 | jvkn |
| CHECK 13 (`control_plane_rls`) | `zz_scratch_check13_livetest` — RLS left disabled | jvkn |
| CHECK 14 (`control_plane_isolation`) | `zz_scratch_check14_livetest` — reachable (real `GRANT` + an admitting policy) but `USING (true)`, no tenant/self/org/PK-self/`is_platform_admin` key | jvkn |

All 5 created together, one `workflow_dispatch` of `tenant-drift.yml` (dispatching once
runs the whole suite — no reason to burn 5 separate CI runs for 5 independent checks
that all report into the same run). **All 5 correctly flagged**, each under its own
line with the right table/policy names,
[issue #1650](https://github.com/eq-solutions/eq-shell/issues/1650) — including one
bonus catch: CHECK 14's table also tripped the existing anon-grant check (CHECK 2)
under a separate label for the same physical jvkn database. Expected, not a bug — a
`USING (true)` policy is by definition an "open policy" to that check too, so two
independent checks catching the same real gap from different angles is exactly the
point of running more than one. All 5 objects dropped immediately after confirming,
`tenant-drift.yml` re-dispatched, confirmed clean and the issue auto-closed itself —
same clean teardown as CHECK 7's test, nothing left behind on either plane.

**CHECK 8 (`column_grants`) is a real exception, not just an unscoped one — stays
simulation-only.** Read its source directly: it isn't a general column-grant scanner
with an allow-list — it's hardcoded to exactly one target, `public.organisations`'s
`supabase_url` / `supabase_anon_key` / `tenant_id` / `tier` columns on jvkn (the
tenant-routing secrets stripped out of the anon-readable column set by
`2026_07_12b_organisations_anon_column_scope.sql`). There's no scratch table to
substitute — the check doesn't watch anything else. Proving it live would mean actually
granting one of those 4 columns to `anon` on the real `organisations` table, even
briefly — not a reasonable trade for a verification exercise, then or now. Leave this
one simulation-only, or (if ever genuinely needed) test in a disposable Supabase project
seeded with an identically-named/shaped table, not live jvkn.

### ~~3. Prove CHECK 7's reviewed-exception logic against a real live violation~~ — DONE

Royce's explicit go to actually run the test this section had scoped. Created a
disposable scratch view, `public.zz_scratch_check7_livetest` (`SELECT 1`, no
`security_invoker`, granted to `authenticated`), on `zaap` via Supabase MCP
`execute_sql` — not `field_managers`/`field_people_directory` themselves, which are
live and load-bearing; a genuinely throwaway object instead. Manually dispatched
`tenant-drift.yml` (it supports `workflow_dispatch`) rather than reasoning about it in
the abstract:

- **Correctly failed**: `public.zz_scratch_check7_livetest reloptions=NONE` flagged on
  the EQ tenant.
- **Correctly discriminated**: the same run's SKS-tenant output shows both real
  entries still passing — "2 reviewed exception(s), content-verified this run:
  app_data.field_managers, app_data.field_people_directory." Proves the logic
  distinguishes a real violation from a legitimate exception in the same live run, not
  just that CHECK 7 still fires in general.
- **Bonus, unplanned**: the issue-filer (§A/PR #1639) fired for real too, opening
  [#1649](https://github.com/eq-solutions/eq-shell/issues/1649) — incidentally
  exercises that fix's own still-open verification item for CHECK 7 specifically. The
  other 6 wired checks remain unproven this way — scoped in "What's left" #2 above.
- **Cleanup verified, not assumed**: dropped the scratch view, re-dispatched, clean
  pass, issue auto-closed itself ("Drift check passed — all violations resolved") with
  no manual intervention. Nothing left behind on `zaap`, no lingering GitHub issue.

### 4. eq-cards' own jvkn migrations still have no governed apply path

Noted in passing by another session yesterday; investigated properly this pass rather
than left as an unquantified suspicion. eq-shell had the identical gap until #1641 —
worth checking whether eq-cards' is actually the same shape, not just assumed to be.

**eq-cards' own documented process** (`supabase/MIGRATIONS.md`, written 2026-07-02):
migrations are applied to jvkn manually, one file at a time, via the Supabase MCP
`apply_migration` — a careful, documented runbook (drift-check the live function body
first, apply, verify, prefer a rolled-back transaction as a dry run first). `ci.yml`
only checks migration-*numbering* hygiene (no duplicate `NNNN`); there is no CI step
that applies anything, by the doc's own admission.

**Checked live whether that manual process is actually keeping the ledger reliable.**
eq-cards has 161 tracked `.sql` files in `supabase/migrations/`. jvkn's native ledger
(`supabase_migrations.schema_migrations`) doesn't store the filename verbatim — it
strips the `.sql` extension, and roughly a third of entries also drop the `NNNN_`
number prefix (inferred from live samples, e.g. `0161_promote_labour_hire_photo_on_
claim.sql` → ledger name `promote_labour_hire_photo_on_claim`). Comparing all 161
files against both naming shapes: **132 matched, 29 did not**, under either
convention. That's not proof those 29 are missing — a third naming variant used for
some entries would produce the same false signal, the same caveat CHECK 11's own
`--strict-identity` flag exists to soften for eq-shell's version of this — but it's a
concrete, live number where "no governed path" was previously just a category
statement, and it's the same shape of problem (silently-unreliable ledger) that #1641
was built to fix for eq-shell.

Three shapes, not decided here — **Royce's call**, same as the cross-repo gap in §D:

1. **eq-cards gets its own runner**, mirroring `migrate-control-plane.mjs`, writing to
   the SAME shared ledger eq-shell's now uses (`shell_control._eq_control_plane_
   migrations`). Straightforward to build, but a second copy of near-identical
   apply-and-stamp logic to keep in sync across two repos.
2. **eq-cards' migrations route through eq-shell's existing runner** — e.g. eq-cards'
   CI calls eq-shell's `control-plane-migrate.yml` as a reusable workflow, the same
   architectural shape Royce already picked for the *check* side of this exact
   incident (§D, PR #1638). One runner, one ledger, no duplicated logic — the option
   this doc would lean toward if asked, for the same reason §D's option 2 was leaned
   toward: the reasoning and the code travel together. Real cross-repo coupling to
   build, same category of work as §D's still-open eq-cards half.
3. **Leave the manual process as-is, re-verify periodically** — cheapest, but doesn't
   change the underlying fact: the ledger this repo would build CHECK-11-for-eq-cards
   against is exactly as unreliable today as eq-shell's was before #1641.

Not urgent — eq-cards' migration volume against jvkn is low, and nothing found this
pass indicates any of the 29 unmatched files represent an actual applied-but-unrecorded
security-relevant change, only that the record-keeping can't currently prove either way.

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
| CHECK 7's exception logic never proven against a real live violation | Live-tested on `zaap`, clean pass + clean teardown — see "What's left" §3 |
| CHECK 6/9/12/13/14 never proven against a real live violation | Live-tested on `zaap` + jvkn, all 5 correctly flagged, clean pass + clean teardown — see "What's left" §2. CHECK 8 confirmed not safely testable this way (see same section) |
| Cross-repo consumer-check gap — architecture decided, jvkn-plane check built, eq-cards half wired up | Fully closed — [PR #1638](https://github.com/eq-solutions/eq-shell/pull/1638) (`7771026b`) + [eq-cards#328](https://github.com/eq-solutions/eq-cards/pull/328) (`23abf7a3`), both merged, live-confirmed end-to-end (not just secrets-present) — see "What's left" §1 |
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
