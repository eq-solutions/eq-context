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

### Resolved — architecture question settled, this branch's premise holds

Three sprint docs today (this one, `eq-shell-sentry-sprint.md`, and
`tenant-onboarding-sprint.md`'s Decision #1) all touched the same open question: does this
branch's dedicated-project work on `ornndtbdkxfsewspbrwk` survive, or does madagins move to
shared ehow? **Asked Royce directly — he rejected shared-ehow-as-default. Madagins keeps its
own dedicated Supabase project.** `tenant-onboarding-sprint.md`'s Decision #1 and item #5
("archive eq-tenant-madagins") are corrected in that doc to reflect this. This branch's premise
holds — proceed on the basis below.

### Verified live just now, not carried over stale

Branch/worktree: `eq-shell-wt-pgcron` (`fix/tenant-provisioning-pg-cron`):

- **6 commits behind `main`** (was 3 when first flagged a few hours ago — needs a rebase before
  anything else here).
- **Uncommitted code**: `netlify/functions/_shared/tenant-routing.ts` +
  `netlify/functions/provision-tenant-background.ts` (modified) — the actual pg_cron-enabling
  change.
- **Uncommitted migrations, numbering collision is now real, not hypothetical**:
  `0308_legacy_public_schema_baseline.sql` and
  `0309_app_data_legacy_baseline_and_tenant_members.sql`. `0308` is now taken on `main` by the
  merged `0308_sites_deleted_at.sql` (PR #1829, earlier today) — this pair needs renumbering to
  `0309`/`0310`. Re-check both numbers are still free at land time — `main` has moved 6+ times
  today already and isn't slowing down.

**New wrinkle, surfaced by a later session the same day (not in the original write-up):**
`madagins` isn't just missing pg_cron — it's **50 migrations behind `main`** (back to `0257`).
A blank dispatch would silently apply 49 other, unreviewed migrations (security/RLS/role-gate
changes among them) as a side effect. Needs a deliberate decision, not a default fleet-wide
catch-up:
- Batch-dispatch to `madagins` after review, once this branch lands, **or**
- Fold `madagins`'s catch-up into landing this same fix (same branch, same review pass)

**Royce's call, not this doc's** — and only matters if the architecture question above still
points at keeping `madagins` on its own project at all.

## 2. Re-run `check-provisioning-completeness.mjs`

Depends on #1 actually landing and dispatching. Expect the `pg_cron` extension finding to clear.
**Won't clear** (separate, still open — see #3): `vector`, `pg_net`.

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
  anon/authenticated-writable, 0 rows today) — already spun off as its own task
  (`task_e9a26fb7`) and already running independently. Don't re-triage it as part of #3 above.

---

## Summary

| # | Item | Status | Depends on |
|---|---|---|---|
| 1 | Land `fix/tenant-provisioning-pg-cron` | Architecture question resolved 2026-09-09 (keep dedicated project) — still needs the rebase (6+ behind), the 0308/0309 renumbering, and Royce's call on madagins's 50-migration backlog | Not blocked on architecture anymore |
| 2 | Re-run `check-provisioning-completeness.mjs` | Blocked | #1 |
| 3 | Triage ~71 tables / ~65 functions / 2 extensions / 2 schemas | Not started | Independent — can run anytime |
