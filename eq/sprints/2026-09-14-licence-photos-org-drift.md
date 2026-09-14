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
  `organisations.id` (org.id) — a deliberately different, stable sentinel ID.

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

### Done this session
- [x] Root cause identified and live-confirmed (memory file has the full trail).
- [x] Scale quantified against jvkn (table above).

### Staged, ready for a go/no-go (not yet applied/merged — each is a separate ask, see "Decisions needed")
- [ ] **Detection-gap migration** (eq-shell, control plane jvkn): extend
  `eq_sweep_orphaned_licence_photos()` (or a sibling function) to also flag "licence row exists,
  but this object's path doesn't match any of its current evidence columns" — today it only
  checks "does any licence row match this id at all," which is the exact reason this has gone
  unnoticed for 3 months (first sighted in eq-cards migration `0050`'s own comment, 2026-06-26).
  Written as a migration file in eq-shell; control-plane DDL here is hand-applied via Supabase
  MCP with explicit go each time (this repo's standing convention, not a one-off ask).
- [ ] **Dry-run audit/repair script** (eq-shell `scripts/`): reports every orphan and every
  stale-pointer row (the 113 + 6, re-queried fresh at run time), and — only in a second,
  explicit non-dry-run invocation — repairs each stale-pointer row the same way migration
  `0137`'s own incident response did by hand: copy the object to the path the row's current
  org/tenant would produce today, verify byte-identical, repoint the column, delete the old
  object. Dry-run output only so far; no writes executed.
- [ ] **PR #1908 merge** (eq-shell) — merging `main` auto-deploys core.eq.solutions. Already
  reviewed, already correct as far as it goes (see "PR #1908" above). Standing alone since it
  doesn't depend on anything else in this sprint.

### Deferred — needs a design decision before any code gets written
**Unifying what Cards writes for segment 1.** Cards currently has no cheap way to learn
`organisations.id` at upload time — the JWT's `app_metadata` only carries `tenant_id` /
`eq_role` / `is_platform_admin` (injected by jvkn's `custom_access_token_hook`,
`eq-cards/lib/core/utils/jwt_app_metadata.dart`). Two ways to close that gap, neither attempted
today:
1. Add an `org_id` claim to the access-token hook. Touches the shape of every JWT issued
   suite-wide — an auth-adjacent change requiring its own explicit review, not something to
   fold into this sprint's "go."
2. Have Cards resolve org.id via a live, narrowly-scoped read/RPC at upload time (extra
   round-trip; needs its own RLS check — unconfirmed whether `authenticated` can already read
   `organisations.id` by tenant_id, or whether a new RPC is needed).
Recommendation: don't block the detection-gap fix or the data repair on this — those two make
the *existing* problem visible and fixable without touching auth. This piece only prevents
*new* drift of the "which writer wrote it last" flavor (the write-convention mismatch), not the
Personal-Wallet-onboarding flavor, which even a unified convention wouldn't stop on its own
(segment 1 would still change the moment the worker's tenant changes) — so its payoff is
smaller than it looks. Needs Royce's call on which approach, if either, is worth it.

## Decisions needed from Royce

1. Apply the detection-gap migration to jvkn? (hand-apply via Supabase MCP, standard
   control-plane convention)
2. Merge PR #1908 to `main`? (= production deploy to core.eq.solutions)
3. Run the data repair (113 rows + 6 orphans) after reviewing the dry-run report?
4. Cards write-convention: JWT-hook claim, live RPC lookup, or leave as-is?

## Status log

- 2026-09-14 — Sprint opened, brief run and confirmed ("Go"). Proceeding with the two staged,
  non-destructive items (detection-gap migration file, dry-run audit script) and preparing
  PR #1908 for a merge decision. No DDL applied, no data touched, no merge clicked yet — each
  still needs its own explicit go per the constraints above.
