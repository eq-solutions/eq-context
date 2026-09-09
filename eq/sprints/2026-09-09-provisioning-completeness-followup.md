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

**pg_cron half — [PR #1834](https://github.com/eq-solutions/eq-shell/pull/1834), MERGED
(`d9d8c89a`).** `provision-tenant-background.ts`'s new `ensureExtensions()` (idempotent
`CREATE EXTENSION IF NOT EXISTS pg_cron`, Step 4 of new-tenant provisioning) +
`tenant-routing.ts`'s `KNOWN_TENANT_SLUGS` warm-cache bump. Rebased clean onto current `main`,
`pnpm run build` clean, merged on your go. **Confirmed live** — auto-deploy stalled for about
an hour after merge (a same-day recurring gap, self-resolved, see `eq/pending-archive.md`),
but `d9d8c89a` is confirmed (via `git merge-base --is-ancestor`) in the history of the current
production deploy. Note: this only prevents the pg_cron gap from recurring on the *next*
tenant provisioned — it does not
retroactively touch madagins (handled directly by the eq-field session working that tenant).

**Legacy-baseline half — still uncommitted, still in `eq-shell-wt-pgcron`, not part of #1834.**
`0308_legacy_public_schema_baseline.sql` (37 objects) and
`0309_app_data_legacy_baseline_and_tenant_members.sql` (63 objects). A dedicated review pass
(subagent, isolated worktree) has now been done — findings below supersede the earlier
one-paragraph flag.

- **Numbering, re-verified again**: `0308`/`0309`/`0310` all taken on `main` (PRs #1829/#1833/
  #1835, all merged). `0311`/`0312` free as of the review — **re-check once more immediately
  before actually renaming the files**, this number has moved three times in one afternoon and
  will likely have moved again. The files are still sitting under their original `0308_`/`0309_`
  names, uncommitted. (A same-day eq-context commit, `49f38487`, claimed they were already
  "renumbered to 0310/0311" — confirmed false against the actual worktree; don't trust that
  line.)
- **Scoping decision — confirmed real, and wider than first flagged.** Spot-checked ~20 of
  0308's 80 policies directly: every one hardcodes ehow's tenant_id (`7dee117c-...`) and/or
  org_id (`00000000-...-000000000002`) as a literal — permanent zero-access for any other
  tenant, exactly as the header said. **Not just 0308's 37 objects** — 0309 claims to have
  audited every policy for this and come back mostly clean, but never audited function
  *bodies*: `app_data.sync_staff_to_field()` (dead — its trigger is disabled, not even captured
  by 0309) and `app_data.field_job_numbers_src()` (live, backs a Field UI panel — silently
  returns zero rows on any other tenant) both carry the same hardcoded literals. Your call
  (SKS-only forever vs. real parameterisation) now covers both files, not just one.
- **Ordering bugs — one confirmed real for a new tenant, one was a false alarm, plus a real
  third.** `0257`'s unguarded `REVOKE ALL ON public.app_config, public.organisations FROM
  anon;` genuinely crashes a from-scratch tenant before this pair ever runs — confirmed, no
  Plane header, applies fleet-wide by default. **`0260` does not apply here — corrected same
  day (see madagins verification below).** It carries `-- Plane: ehow ONLY` and REVOKEs
  grants on `app_data.field_teams`/`field_team_members`, views that only exist on ehow
  (created by eq-field's own separate pipeline) — `migrate-tenants.mjs` skips it entirely for
  any non-ehow tenant, so it can't crash a genuinely new tenant; it was never going to run
  there. **Real third blocker, from 0309's own header**: 0308's `app_settings` policy needs
  `service.tenant_members`, which only 0309 creates — but 0308 is numbered lower, so it fails
  before 0309 ever runs either. Two interlocking blockers for a new tenant (0257, and the
  internal 0308-vs-0309 ordering), not three. Useful mechanical fact either way:
  `migrate-tenants.mjs` sorts by filename and skips only already-ledgered files — genuinely
  reordering the sequence (not just appending) is mechanically possible, confirmed by reading
  the runner directly.
- **Two unverified `service.*` dependencies — confirmed real, but ehow-safe.** Grepped all 310
  tracked migrations for `service.tenants` / `service.set_updated_at()`: zero hits either way —
  neither is created by any tracked migration, and `provision-tenant-background.ts`'s automatic
  bootstrap doesn't touch the `service` schema at all. Checked live on ehow directly: both
  objects exist there, so 0309 is safe against ehow specifically. Any *other* tenant plane
  without these hand-applied out-of-band will roll back the entire ~2,900-line file on its last
  statement before `COMMIT`.
- **New, not in either file's own notes**: `roster_presence`'s read policy (0308) checks
  `org_id` only, with no JWT tenant_id comparison, unlike its own write policy and every other
  table in the file — an asymmetric, quietly-weaker SELECT grant.

**Decisions needed from you before this goes further:**
1. Scoping — 37 legacy objects (0308) + 2 hardcoded functions (0309): SKS/ehow-only forever, or real per-tenant parameterisation?
2. Ordering — **`0257`'s half is done and merged**: [PR #1843](https://github.com/eq-solutions/eq-shell/pull/1843) (`27006acf`) guards its unconditional REVOKE behind an existence check, live-verified against ehow via `BEGIN...ROLLBACK` before merge (guard short-circuits cleanly on nonexistent tables; full body against ehow's real schema reproduces the original's exact `anon: SELECT`-only result). Merged via admin-override past an unrelated, confirmed-pre-existing jvkn control-plane drift failure on the required schema-drift check (`task_98d5e636` tracking that separately — not this migration's doing). **Real remaining follow-up**: this file is already applied on every tenant, so `migrate-tenants.mjs`'s checksum-drift guard will block the *next* dispatch to sks/eq/zaap/ehow until `--reconcile-ledger` runs against each plane (ledger-only, no schema/data change) — not run yet, holding for your go. The internal 0308-vs-0309 dependency (this pair's own ordering issue, separate from 0257) is still open — `0260` remains correctly out of scope, ehow-only.
3. The 2 missing `service.*` objects need their own capture migration before this pair is safe on any tenant but ehow.
4. `sync_staff_to_field()` is dead with a live landmine in it (hardcoded org_id) — drop it from the capture, or keep it as-is?

Not built or merged pending those calls — kept separate from #1834 deliberately, same as before.

**Update — largely resolved by the eq-field session working this tenant, verified live
directly against madagins's database (not from any session's self-report):** `public` and
`app_data` are both now fully populated (34 + ~120 tables), with real seed-data rows in
several tables and ledger `applied_at` timestamps spanning real hours (07:12-07:57 UTC) —
genuine applies, not a repeat of the earlier fake-stamp bootstrap. One good sign for the
scoping question above: `public.organisations`'s RLS policy uses madagins's own org id
(`dd5d8622-...`), not ehow's hardcoded literal — whoever built this adapted it per-tenant
rather than reusing the uncommitted draft verbatim.

**Correction, same day: the "11 missing migrations" below were a false alarm — not a gap.**
First pass diffed the ledger against every tracked migration file and found 11 absent:
`0258`-`0262`, `0266`, `0270`, `0273`, `0290`, `0303` — flagged as a backlog needing a
decision, including `0260` (wrongly connected to this doc's own ordering-bug finding above).
Checked each file's own header before proposing to dispatch any of them: **all 11 carry an
explicit `-- Plane: ehow ONLY` (ten of them) or `-- Plane: zaap ONLY` (`0262`) header** — this
repo's real mechanism for scoping a migration to fewer than all tenants. None of them were
ever meant to reach madagins. `0260` specifically REVOKEs grants on `app_data.field_teams`/
`field_team_members` — views that only exist on ehow, created by eq-field's own separate
migration pipeline, not eq-shell's. Dispatching any of these 11 to madagins would be a
mistake, not a fix — madagins's migration state is already complete for its own tenant scope.
Nothing to land here. (The one earlier check that WAS valid: `wipe_backup` schema doesn't
exist on madagins, so `0309`'s absence is separately fine, unrelated to Plane scoping.)

## 2. Re-run `check-provisioning-completeness.mjs`

PR #1834 is confirmed live (see item 1 above) — this can now run against a fresh tenant
provisioned after it. Expect the `pg_cron` extension finding to clear.
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
| 1a | pg_cron fix | **[PR #1834](https://github.com/eq-solutions/eq-shell/pull/1834) merged and confirmed live** — done | — |
| 1b | Legacy-baseline migrations (0308/0309, renumber to 0311/0312 — re-verify at land time) | **Reviewed.** `0257`'s ordering bug fixed — [PR #1843](https://github.com/eq-solutions/eq-shell/pull/1843) **merged** (`27006acf`, admin-override past an unrelated pre-existing jvkn drift failure — `task_98d5e636` tracking that separately). **`--reconcile-ledger` still needs to run against sks/eq/zaap/ehow before the next real tenant-migrate.yml dispatch**, or that dispatch throws checksum drift and refuses to run anything — not done yet, holding for your go. 3 more decisions needed from you (scoping now covers 2 files, internal 0308-vs-0309 ordering, 2 missing `service.*` objects, 1 dead function to keep-or-drop) | — |
| 1c | madagins's migration backlog | **Resolved — was never real.** eq-field session's fix landed the genuine gap; the remaining "11 missing" are all Plane-scoped away from madagins (ehow/zaap only) and correctly absent | — |
| 2 | Re-run `check-provisioning-completeness.mjs` | Blocked | 1a merged + dispatched |
| 3 | Triage ~71 tables / ~65 functions / 2 extensions / 2 schemas | Not started | Independent — can run anytime |
