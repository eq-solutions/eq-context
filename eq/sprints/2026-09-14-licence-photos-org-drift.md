---
title: Sprint — licence-photos path segment-1 drift (Personal Wallet onboarding)
owner: Royce Milmlow
last_updated: 2026-09-14
scope: Close the org/tenant-id drift in the licence-photos bucket found during PR #1908 verification — detection gap, existing bad data, and the underlying write-convention split
read_priority: standard
status: live
---

# Sprint: licence-photos path segment-1 drift — 2026-09-14

## Where this came from

A PR #1908 (eq-shell, "delete superseded storage objects on photo/PDF replace") verification
session found 6 orphaned objects in the `licence-photos` bucket that PR #1908's own
side/type/extension mechanism doesn't explain. Root-caused live against jvkn the same session
(memory: `project_licence_photos_path_segment1_dual_convention.md` in the eq-shell memory
store — read that first for full file:line citations; this doc is the action plan, not the
investigation).

## The mechanism, in short

The bucket's storage path is `{segment1}/{user_id}/{licence_id}/{slot}`. Two writers disagree
on what segment 1 means:
- **eq-cards** (`lib/core/utils/photo_upload.dart`) writes the worker's *current session
  tenant_id* — read fresh off the JWT on every upload.
- **eq-shell** (`staff-licence-backfill.ts` / `staff-licence-replace-photo.ts`) writes
  `organisations.id` (org.id) — assumed at the time to be a more stable, session-independent ID.
  **Corrected below (see "Convention decided"): it isn't** — org.id turns out to be exactly as
  session-dependent as tenant_id, since `organisations.tenant_id` is 1:1. The fix in progress
  standardizes both writers on `tenant_id` instead.

Neither writer checks the other, and no RLS policy ever validates segment 1 — it has been
purely cosmetic since it was introduced (Cards Unit 4, 2026-05-21).

**The actual trigger, confirmed live 2026-09-14:** every Cards signup who uploads a licence
before their employer link resolves is auto-parked in a placeholder "Personal Wallet" tenant
(`shell_control.tenants.slug = '__personal__'`, id `279a6da0-0b54-4da8-8eac-499dffaa44cb`)
first, then moves to their real tenant (SKS, in every case seen) within hours. Nothing ever
revisits the licence-photo path written during that window.

## Scale (live counts, 2026-09-14 — re-run before trusting these later)

| Metric | Count |
|---|---:|
| Workers who have ever held Personal Wallet | 51 |
| ...and later joined a real tenant | 49 |
| ...within 48 hours of joining Personal Wallet | 44 |
| Licence rows whose **current** (non-orphaned) evidence URL still points at the Personal Wallet path | **113** |
| Confirmed true storage orphans (object exists, nothing points at it) | 6 |

Not access-broken — `licence_photos_owner_select`/`_insert`/etc. (migration `0137`, eq-cards)
already key off `licences.user_id = auth.uid()` via the licence-id join, segment-1-agnostic.
This is a data-hygiene / future-tooling exposure, not a live security gap: `photo_upload.dart`'s
own header names "a future all-licences-for-a-tenant admin tool" as segment 1's reason to
exist, and that tool would silently miss these 113 rows today.

**PR #1908, once merged, only closes part of this.** Of the 6 confirmed orphans, whoever wrote
the *current* pointer last splits 2 ways:
- 2 of 6 — Cards re-uploaded (current segment 1 = SKS tenant_id). #1908 never runs for a
  Cards-originated write; this half stays open regardless of #1908's fate.
- 4 of 6 — an eq-shell admin call wrote the replacement (current segment 1 = SKS org.id
  sentinel). #1908's diff logic (DB's old value vs. this call's new path) is convention-agnostic,
  so it *would* have caught and deleted the stale object here. This half self-heals going
  forward once #1908 merges — it does not retroactively clean the existing 6, and does nothing
  for the 113 whose evidence has never been touched again at all.

## Plan

### Done
- [x] Root cause identified and live-confirmed (memory file has the full trail).
- [x] Scale quantified against jvkn (table above).
- [x] **Convention decided: `tenant_id`, not `organisations.id`.** This sprint originally
  deferred that choice assuming org.id was the more stable option — checked live and that's
  wrong: `organisations.tenant_id` is `NOT NULL UNIQUE` (1:1), so org.id is exactly as
  session-dependent as tenant_id. `tenant_id` also won on churn (every writer already has it
  in scope). See the eq-shell memory file's corrections section for the full trail.

### Three efforts now exist on this bug — reconciled here so a future session doesn't start a fourth
1. **Convention fix (stops NEW drift)** — two worktree branches named
   `worktree-licence-photos-segment1-fix`, one in each repo, not yet committed/pushed/PR'd as of
   this update:
   - eq-cards: `photo_upload.dart` gained a `remove()` helper; `licence_edit_screen.dart` now
     deletes a slot's superseded old path once its row update commits the new one. New migration
     `0169_licence_photos_sweep_path_mismatch.sql` extends `eq_sweep_orphaned_licence_photos()`
     with the "row exists but points elsewhere" detection class (that function's real home is
     eq-cards — `0149`/`0150`/`0151` — not eq-shell's backfill-documentation-only migration file).
     **Re-verify migration number `0169` is still free before landing** — `0168` was taken by a
     concurrent merge mid-session once already.
   - eq-shell: `staff-licence-backfill.ts` / `staff-licence-replace-photo.ts` changed segment 1
     from org.id to tenant_id, deliberately with no cleanup logic added (left to PR #1908, which
     already has the diff-and-delete mechanism on these exact lines — composes rather than
     duplicating).
2. **Repair (cleans up the EXISTING 113 + 6)** — [eq-shell PR #1913](https://github.com/eq-solutions/eq-shell/pull/1913),
   `scripts/repair-licence-photo-segment-drift.mjs`. Dry-run by default; repairs a drifted row
   via copy → verify (size match) → repoint → delete (same shape migration `0137` used by hand);
   deletes a true orphan only if both `--apply` and `--delete-orphans` are passed. Deliberately
   self-contained (queries `public.licences` directly, no dependency on `0169` landing or its
   migration number). Not run with `--apply` anywhere yet.
3. `task_7d7d8b41` — spawned background task, eq-cards. Status not verified as part of this
   update — check before assuming it's still needed or still pending.

**Recommended sequencing** (not required for safety, just avoids the count growing between
report and repair): land the two segment1-fix branches first, then PR #1913. #1913 only touches
rows that already exist today either way.

### PR #1908 — unrelated decision, still standing on its own
Merging `main` auto-deploys core.eq.solutions. Already reviewed, already correct for the narrower
side/type/extension case it targets (see "The mechanism" above). Doesn't depend on, or block,
anything else in this sprint.

## Decisions needed from Royce

1. Land PR #1912 (eq-shell, segment1-fix) — CI green on every substantive check as of this
   update. Merging it deploys core.eq.solutions; needs your explicit go regardless of CI colour.
2. Apply migration `0169` (or whatever the landed detection fix ends up being) to jvkn?
   (hand-apply via Supabase MCP, standard control-plane convention) — blocked on #1912 landing
   first per the recommended sequencing above.
3. ~~Merge PR #1908 to `main`?~~ **Done — #1908 merged.** This put PR #1912 into a git conflict
   (both touch the same lines in `staff-licence-backfill.ts` / `staff-licence-replace-photo.ts`);
   resolved by composing the two changes (tenant_id convention + #1908's delete-after-write
   cleanup) rather than picking one, re-verified clean (`tsc`/`eslint`), pushed.
4. Run PR #1913's `--apply` (and separately, `--delete-orphans`) after reviewing its dry-run
   output — still open, still unrun, still needs your review first.
5. **New**: `task_7d7d8b41` (spawned by this sprint's own originating session, cwd eq-cards, per
   the eq-shell memory file's earlier text) is very likely superseded by PR #355 (now merged) —
   circumstantial evidence only (same originating session, "cwd eq-cards" matches exactly what
   #355 delivered), not confirmed. Needs a yes/no from you before dismissing it, not an assumption.

## Status log

- 2026-09-14 — Sprint opened, brief run and confirmed ("Go"). Started building a
  detection-migration + repair script in eq-shell before discovering — via a memory-file
  change-notification mid-session — that a concurrent session had already solved the detection
  half more completely (and caught this sprint's own wrong assumption that org.id was the
  stable choice). Dropped the duplicate migration, corrected the repair script to the agreed
  `tenant_id` convention and made it self-contained, opened PR #1913 for just that piece, and
  reconciled all three now-known efforts here rather than letting a future session rediscover
  the collision. No DDL applied, no data touched, no merge or `--apply` run — every item above
  still needs its own explicit go.
- 2026-09-14 (later same day) — A different concurrent session (the one that opened PR #355)
  picked up the closeout: merged #355, then found #1908 had merged in the meantime and put #1912
  into conflict with it — resolved by composing both changes rather than re-litigating either,
  re-verified, pushed. Confirmed #1913 is still clean/mergeable. Opened eq-cards PR #356 (doc-only:
  RUNBOOK.md's 403-troubleshooting line still implied RLS enforces segment 1; corrected). Checked
  for eq-cards/eq-shell test coverage this new logic could slot into — neither repo has a
  low-effort slot-in point (eq-cards' widget tests all terminate before reaching the
  upload/cleanup code path via the pre-existing currentUser gate; eq-shell's test pattern only
  covers extracted pure functions, and #1908's cleanup logic isn't extracted — extracting it
  would mean touching #1908's already-merged code, out of bounds). Did not action `--apply` on
  #1913, did not merge #1912, did not dismiss `task_7d7d8b41` — all three still need your word,
  restated in "Decisions needed" above.
