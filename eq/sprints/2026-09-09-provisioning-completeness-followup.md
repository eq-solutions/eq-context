---
title: Provisioning-completeness follow-up — land the pg_cron fix, triage live-only findings
owner: Royce Milmlow
created: 2026-09-09
last_updated: 2026-09-09
scope: The 2 items deferred out of PR #1832 (scripts/check-provisioning-completeness.mjs, merged 2026-09-09) — landing the in-progress pg_cron provisioning fix and triaging the live-only inventory the new check's first run surfaced. Supersedes the equivalent bullets originally logged in eq/pending/eq-shell.md the same day (see Notes on provenance below) — this doc is now the sole record for both.
read_priority: high
status: live
---

# Provisioning-completeness follow-up

## How this was built

PR #1832 (merged 2026-09-09) shipped a read-only audit script that diffs everything actually
live on ehow against what eq-shell's tracked migration pipeline (`supabase/tenant-migrations/*.sql`
+ `provision-tenant-background.ts`) can reproduce. Its first run, verified live before merging,
found more than the 2 known incident gaps it was built to catch (pg_cron never enabled; ~37
legacy `public`-schema tables predating the migration system) — those two were already being
fixed on a separate, uncommitted branch. This doc is the "next" side of that session's close-out
card: the 2 items deferred rather than built same-session.

**Note on provenance:** the original write-up of these items lived as its own section in
`eq/pending/eq-shell.md` (commit `76d7e4d8`). By the time this sprint was started, that section
no longer appeared in the live file — and isn't in `eq/pending-archive.md` either, so it wasn't
a normal archive. Flagged separately as a possible gap in the `safe_commit.py` concurrent-edit
guard rather than investigated here (this repo is seeing heavy same-day concurrent-session
traffic). Nothing is actually lost: this doc reconstructs the content from that commit plus a
fresh live check of the branch below, so it's more current than the original would have been.

---

## 1. Land `fix/tenant-provisioning-pg-cron`

### Split in two, on purpose — pg_cron half is now a PR, legacy-baseline half is not

The branch's uncommitted work was actually two independent fixes for two independent gaps
sharing one worktree. Landing "the pg_cron fix" as asked did not mean landing all of it —
splitting it out let the small, well-understood half ship without dragging in ~4,700 lines of
SQL that self-documents real unresolved correctness questions (see below).

**pg_cron half — [PR #1834](https://github.com/eq-solutions/eq-shell/pull/1834), open, not
merged.** `provision-tenant-background.ts`'s new `ensureExtensions()` (idempotent
`CREATE EXTENSION IF NOT EXISTS pg_cron`, Step 4 of new-tenant provisioning) +
`tenant-routing.ts`'s `KNOWN_TENANT_SLUGS` warm-cache bump. Rebased clean onto current `main`
(no unique commits existed on the branch — everything was uncommitted working-tree state,
so this was a straight commit + rebase, no conflict). `pnpm run build` (`build:packages` +
`tsc -b` + `vite build`) clean. **Holding at PR per this repo's merge-is-the-deploy rule** —
needs your explicit go before merge/deploy. Note: this only prevents the pg_cron gap from
recurring on the *next* tenant provisioned — it does not retroactively touch madagins (already
being handled directly, per the eq-field session working that tenant today).

**Legacy-baseline half — still uncommitted, still in `eq-shell-wt-pgcron`, not part of #1834.**
`0308_legacy_public_schema_baseline.sql` (37 objects) and
`0309_app_data_legacy_baseline_and_tenant_members.sql` (63 objects) — read in full before
landing these, they're higher-risk than they look:
- **Numbering collision keeps getting worse, not better — third update to this same note.**
  `0308`, `0309`, AND NOW `0310` are all taken on `main` (`0308_sites_deleted_at.sql` #1829,
  `0309_wipe_backup_schema_rls_lockdown.sql` #1833, `0310_eq_migrations_ledger_rls_lockdown.sql`
  — [PR #1835](https://github.com/eq-solutions/eq-shell/pull/1835), open). Target is now
  `0311`/`0312` — **re-check yet again at actual land time**, this file's own numbers are stale
  within hours every time someone checks. The files themselves are still sitting under their
  original `0308_`/`0309_` names, uncommitted, in `eq-shell-wt-pgcron` — a same-day
  eq-context commit (`49f38487`) describes them as already "renumbered to 0310/0311," which
  the actual worktree does not bear out; don't trust that line over a live check.
- **Both files' own headers flag real, unresolved correctness bugs**, not just style nits: most
  RLS policies in the first file hardcode ehow's own tenant/org UUIDs as literals, so on any
  *other* tenant these ~37 objects become permanently zero-access for real users (service_role
  only) — the header calls this out explicitly as "Royce's call" whether that's acceptable or
  needs real parameterisation. Separately, at least 3 migration-ordering bugs are self-documented
  (`0257` and `0260` both still crash a from-scratch tenant *before* either of these two files
  ever runs — landing this pair does not, by itself, fix the crash that motivated it) plus two
  unverified `service.*` dependencies (`service.set_updated_at()`, `service.tenants`) that could
  roll back the entire second file if either is missing on a target project.
- These need a real review pass and Royce's input on the specific open questions above, not a
  default merge — kept separate from #1834 deliberately.

**Also still open, independent of either half:** `madagins` is **50 migrations behind `main`**
(back to `0257`) — a blank dispatch would silently apply 49 other, unreviewed migrations
(security/RLS/role-gate changes among them). Needs a deliberate decision (batch-dispatch after
review, or fold into whichever of the two halves above ends up touching madagins directly) —
**Royce's call, not this doc's.**

## 2. Re-run `check-provisioning-completeness.mjs`

Depends on PR #1834 actually merging and a fresh tenant being provisioned after it (or a direct
live check against the next provisioning run). Expect the `pg_cron` extension finding to clear.
**Won't clear** (separate, still open — see #3): `vector`, `pg_net`. The legacy-baseline half
(0308/0309→0311/0312, re-verify at land time) is a separate re-run trigger of its own once/if it lands.

## 3. Triage the live-only inventory

Independent of #1/#2 — can run anytime. The check's first run (informational only,
`KNOWN_LIVE_ONLY` ships empty on purpose) found, beyond the 2 known incident gaps:

- **2 extensions**: `vector`, `pg_net` — confirmed live on ehow, absent from a same-day fresh
  tenant project, absent from every tracked source.
- **2 live-only schemas**: `shell_control` (5 tables), `wipe_backup` (4 tables) — on ehow, the
  *tenant* plane; `shell_control` is otherwise a control-plane (jvkn) concept, so its presence
  here specifically is worth confirming isn't itself a mistake, not just an unsourced-but-fine
  finding.
- **~71 live-only tables / ~65 live-only functions** in total — a meaningful share of this is
  very likely `eq-field`'s own separate, hand-applied migration pipeline writing into this same
  ehow database (same cross-repo-attribution shape `check-control-plane-drift.mjs`'s
  `KNOWN_UNSOURCED` already handles for jvkn), not yet confirmed item-by-item.

**Process** (same one `check-control-plane-drift.mjs`'s `KNOWN_UNSOURCED` already uses): per
item, confirm live against the owning repo (eq-shell vs. eq-field vs. genuinely orphaned) — then
either backfill a real migration, or accept into `KNOWN_LIVE_ONLY` with a citation. Only once
this list triages to a clean baseline does `--strict` become safe to turn on in
`tenant-drift.yml`.

---

## Explicitly excluded

- **`wipe_backup.*` RLS-disabled finding** (4 tables, Supabase advisor flags it critical —
  anon/authenticated-writable, 0 rows today) — spun off as its own task (`task_e9a26fb7`),
  now **done**: [PR #1833](https://github.com/eq-solutions/eq-shell/pull/1833) merged. Don't
  re-triage it as part of #3 above.

---

## Summary

| # | Item | Status | Depends on |
|---|---|---|---|
| 1a | pg_cron fix | **[PR #1834](https://github.com/eq-solutions/eq-shell/pull/1834) open, not merged** — awaiting your go | — |
| 1b | Legacy-baseline migrations (0308/0309, renumber to 0311/0312 — re-verify at land time) | Uncommitted, needs review + your calls on the open questions above | — |
| 1c | madagins's 50-migration backlog | Needs your decision | — |
| 2 | Re-run `check-provisioning-completeness.mjs` | Blocked | 1a merged + dispatched |
| 3 | Triage ~71 tables / ~65 functions / 2 extensions / 2 schemas | Not started | Independent — can run anytime |
