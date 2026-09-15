---
title: Sprint — licence-photos path segment-1 drift (Personal Wallet onboarding)
owner: Royce Milmlow
last_updated: 2026-09-15
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

1. ~~Land PR #1912 (eq-shell, segment1-fix)?~~ **Done — #1912 merged** 2026-09-14T11:44:46Z,
   by Royce directly. Composed cleanly through a real conflict with #1908 (both changes verified
   intact on main, not just assumed). Deploy confirmed **live** on core.eq.solutions (commit
   `7ce5e009`) via Netlify's `published_deploy` object + `git merge-base --is-ancestor` — not
   inferred from elapsed time or from `deploy_source`/`cdp_enabled_contexts`.
2. ~~Apply migration `0169` to jvkn?~~ **Done**, after Royce's explicit go. **Independently
   re-confirmed 2026-09-15** (second source, direct `execute_sql` against jvkn): `SELECT
   eq_sweep_orphaned_licence_photos(true, 0)` returns exactly `superseded_by_different_path_count:
   6`, `no_licence_row_count: 26` — matches the first report precisely.
3. ~~Merge PR #1908 to `main`?~~ **Done — #1908 merged.** This put PR #1912 into a git conflict
   (both touch the same lines in `staff-licence-backfill.ts` / `staff-licence-replace-photo.ts`);
   resolved by composing the two changes (tenant_id convention + #1908's delete-after-write
   cleanup) rather than picking one, re-verified clean (`tsc`/`eslint`), pushed.
4. ~~Merge PR #1913?~~ **Done — merged 2026-09-15** (Royce: "merge, dry-run, show output").
   **The multi-tenant-membership risk flagged above is checked and doesn't materialize in
   current data**: of the 36 distinct affected users, 35 have exactly 1 real (non-Personal-
   Wallet) tenant membership and 1 has zero (correctly skipped, no real tenant yet) — zero have
   more than one, so `resolveCurrentTenantPath`'s "most recent wins" pick is unambiguous for
   every candidate today. Still worth hardening defensively for a future multi-tenant worker,
   just not a blocker.
   **`--apply` (repair) and `--delete-orphans` (the 6) are still NOT run anywhere.** Dry-run
   replicated 2026-09-15 via direct read-only SQL against jvkn (the script's own
   `CONTROL_SUPABASE_URL`/`CONTROL_SUPABASE_SERVICE_KEY` aren't set in this machine's `.env` —
   same gap as yesterday's script, not sourced from Netlify per Royce's standing preference not
   to put that credential in a session): **169 candidate columns across 115 licences** would
   repoint to SKS's real tenant_id `7dee117c-...`; **1 column (1 licence)** skips (no real
   tenant yet). Matches the live count of 116 distinct mis-pathed licences (115 + 1), up from
   113 on 2026-09-14.
   **New finding, changes the `--delete-orphans` picture**: the repair script's own orphan
   report uses the RPC's combined `orphan_count` (32 = 26 `no_licence_row` + 6
   `superseded_by_different_path`) as its single gate for `--delete-orphans` — it does not
   distinguish the two classes. The 6 `superseded_by_different_path` ones are the
   well-vetted class this whole sprint is about (safe). Of the 26 `no_licence_row` ones,
   sampling turned up 4 objects under `pending-credentials/811eec1a-.../` and
   `pending-credentials/93dc7b3f-.../` (created 2026-08-20 10:11-10:12 UTC) that look
   structurally identical to the exact false-positive class PR #357 just fixed — a different
   candidate under the same prefix, uploaded the same day at 22:55, IS correctly excluded
   (has a `worker_credentials.metadata->>'source_document_url'` match); these two aren't.
   Plausible read: a candidate who never progressed far enough in labour-hire intake to get a
   `worker_credentials` row at all would never get a `source_document_url` to match against,
   regardless of age — meaning #357's fix protects candidates who progressed partway, not ones
   who didn't progress at all. Not confirmed either way from eq-shell. **Spawned `task_b56ada7f`
   (eq-cards) to trace these two candidate ids and confirm safe-to-delete or not, before
   `--delete-orphans` is ever run.** Until that resolves, treat `--delete-orphans` as unsafe at
   its current scope (it would touch all 26, not just the 6). `--apply` alone (the 169-column
   repair, no orphan deletion) has no such data-safety caveat.
   **Tooling correction, 2026-09-15 (caught before running anything, not after):** a Claude
   session cannot actually execute `--apply` itself, even with Royce's go and even with the real
   env vars sourced somehow — the repair's copy step (`sb.storage.from(BUCKET).copy(...)`) is a
   genuine Storage API call, and the Supabase MCP tooling available in these sessions only
   exposes Postgres/project-management operations (`execute_sql`, migrations, edge functions,
   etc.) — no storage-object copy/upload/move. A raw SQL insert into `storage.objects` would
   create a metadata row with no real file behind it — worse than doing nothing. **The script
   must be run by a human (or a non-Claude process) with real shell/Node access and the real
   `CONTROL_SUPABASE_URL`/`CONTROL_SUPABASE_SERVICE_KEY`** — this was offered as a Claude-doable
   action once already this update before being caught; don't repeat the offer.
5. ~~`task_7d7d8b41`~~ **Royce said dismiss it (2026-09-15)** — confirmed superseded by PR #355.
   Could not be actioned programmatically from the eq-cards reconciliation session: `dismiss_task`
   only reaches chips the calling session itself spawned, and this one was spawned by a different
   session (`local_9fa076a4`, "Fix licence-photos path segment-1 dual convention"). Still needs
   Royce (or that originating session, if still open) to clear the chip directly in his own UI —
   the decision is made, the mechanical dismissal isn't done yet.
6. **DONE (2026-09-15)**: the 4th concurrent effort flagged in the previous update ("Fix
   admin-attach-licence-photo's broken 3-segment path", eq-cards) concluded — code committed to
   worktree `admin-attach-licence-photo-path-fix`, 2 commits (including a migration renumbered
   0170→0171 after colliding with #357's own 0170, already live). The discrepancy noted last
   time is resolved: it's genuinely 3-segment, not 2 — `admin-attach-licence-photo` (0083) wrote
   `{user_id}/{licence_id}/{slot}`, missing tenant_id as segment 1 entirely, so migration 0137's
   RLS (which keys off segment 3 = licence id) could never resolve — nothing this function ever
   wrote was readable by its own owner or an org admin. Zero live callers found (grepped
   eq-cards + eq-shell for the function name and its shared secret), so this was a structural
   fix ahead of the bug ever having a real victim, not an active incident. The session ended
   without pushing or opening a PR; picked up from here (eq-cards reconciliation session):
   found [PR #358](https://github.com/eq-solutions/eq-cards/pull/358) already existed (opened
   independently, right around that session's end — not by this session), found its required
   CI check genuinely hung (~10 hours stuck `in_progress`, everything else on the run green),
   cancelled + re-ran just that job (left the 4 already-passing checks alone), came back clean,
   and merged on Royce's explicit go. **Migration `0171` (new RPC `eq_get_user_active_tenant`,
   `shell_control`-touching, read-only) is applied to jvkn (2026-09-15, Royce's explicit go)** —
   verified live: function exists, `SECURITY DEFINER`, `service_role`-only (`anon`/
   `authenticated` both confirmed `false` via `has_function_privilege`), and does not appear in
   `get_advisors(security)`'s output at all — zero new findings. The RPC is still dead code
   yet either way).
7. ~~`task_83d5f0f7`~~ (admin-attach-licence-photo's separate path bug) — underlying fix is
   **merged** (item 6, above). `dismiss_task` still can't reach it from this session (spawned by
   a different one, same limitation as `task_7d7d8b41` in item 5) — Royce still needs to clear
   the chip himself.
8. **RESOLVED (2026-09-15)**: eq-cards' `photo_upload.dart` reads `tenant_id` from the Supabase
   JWT's `app_metadata` claim; eq-shell's `staff-licence-replace-photo.ts` /
   `staff-licence-backfill.ts` read `session.tenant_id` from its own `eq_shell_session` cookie.
   Traced both to source and live-cross-checked against jvkn: **both bottom out in the same
   `shell_control.tenants.id`.** eq-shell side: `shell-login.ts`/`select-tenant.ts` →
   `shell_control.user_tenant_memberships`/`users` → `shell_control.tenants(id)` FK, no hop
   through `organisations`. eq-cards side: `public.custom_access_token_hook` (live definition
   pulled via `pg_get_functiondef`, byte-identical to
   `eq-cards/supabase/manual/custom_access_token_hook.sql`) reads
   `coalesce(shell_control.users.last_active_tenant_id, .tenant_id)` — same FK chain. No code
   path substitutes `organisations.id`. Correction found along the way: Cards' iframe handoff
   does **not** go through `token-exchange.ts` (that's Field/Service-only, its `aud` param
   rejects anything else) — the live Cards mechanism since 2026-06-24 is `mint-cards-otp.ts`,
   which mints nothing itself for either the iframe or standalone path; both go through
   Supabase's native `generateLink`/`verifyOTP` and land on the same hook above. Two narrow,
   non-ID-space caveats, not bugs: (1) the Shell cookie is a snapshot (≤7-day TTL) vs. the
   hook's live read of `last_active_tenant_id` — a tenant switch in a concurrent session could
   leave them briefly disagreeing, but always between two valid `shell_control.tenants.id`
   values, never an `organisations.id` substitution; (2) a brand-new signup with no
   `shell_control.users` row yet gets no claim at all (hook fails open) — `cards-api` 401s
   rather than misfiling. **F18 does not apply to this convention.** It does still apply
   elsewhere: Royce explicitly declined (`CONTROL-PLANE-LEDGER.md` entry `2026_09_10b`,
   2026-09-10) to unify `organisations.id`/`shell_control.tenants.id` because two Cards RPCs
   deliberately key `worker_invites.org_id` off `organisations.id` — a different column,
   untouched by this saga, but confirmation that F18's failure class is a live standing hazard
   elsewhere, not a one-off. Separately: the investigation found
   `eq-context/eq/identity/IDENTITY-MODEL.md` §6.2/§7.2 stale (still describes the pre-2026-06-24
   `mint-supabase-jwt`/postMessage mechanism) — spawned as `task_59002a2e`. **Done (2026-09-15)**:
   corrected directly on `eq-context` main, commit `9b7052e2` ("correct Cards auth-handoff
   mechanism (mint-cards-otp, not mint-cards-iframe-token)") — confirmed via git log, not just
   assumed from the task having run. Only the mechanical chip-clear remains.

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
- 2026-09-14/15 (reconciliation pass, eq-cards session, brief run via `/brief eq-context`) —
  Re-verified everything live rather than trust this doc, the eq-shell memory file, or the task
  brief that pointed here — all three were already stale by the time of reading (the brief said
  #1912 was "open, CI restarted"; it had actually been merged 45+ minutes earlier). Findings
  folded into "Decisions needed" above (items 1, 2, 4, 5 updated; items 6–8 new); process notes
  here:
  - Confirmed **#1912's live deploy** independently (Netlify's `published_deploy` object +
    `git merge-base --is-ancestor`) rather than take the merge alone as proof, per this doc's own
    standing caution against inferring liveness from elapsed time.
  - Migration `0169`'s application was reported by the session that ran it, not independently
    re-queried against jvkn here — no Supabase MCP access in this session. One-source-confirmed.
  - `scripts/safe_commit.py`'s bootstrap threw a confusing "origin/main has no
    scripts/_safe_commit_impl.py" error on first attempt from the shared checkout — not an
    actual break in the script; its internal git calls resolve against process cwd, and the
    shared checkout's cwd was a different repo's context in this multi-repo session. Worked
    immediately once invoked with cwd genuinely inside an eq-context checkout/worktree. Noting
    only because the failure reads as "the safe path is broken," which could push a future
    session toward an unsafe direct commit instead.
  - Found a second pre-existing worktree (`licence-photos-sprint-update`,
    `chore/licence-photos-sprint-update`) with its own uncommitted edit to this exact file,
    likely the originating segment1-fix session's in-progress draft. Left untouched — not this
    session's worktree to edit. Landed this update via a separate, isolated worktree +
    `safe_commit.py`'s own upstream-divergence check instead, per F12/F16/F17.
  - Also hit the brief-gate (Rule 0.6) on the first edit attempt, ran `/brief eq-context`
    properly, and separately hit the gate's flag file expiring mid-session on the midnight
    2026-09-14→15 rollover (flag filename embeds a date) — rewrote it with the correct date.
  Did not merge #1913, did not run any `--apply`/`--delete-orphans`, did not dismiss
  `task_7d7d8b41`, did not touch admin-attach-licence-photo (already being worked live
  elsewhere — see item 6). All still need Royce's word.
- 2026-09-15 — Royce asked "show me what to do with these licenses and which ones they are" in
  the same session that originally opened #1908, resumed a day later. Re-synced against this
  doc + the eq-shell memory file (both had moved since that session closed) before answering.
  Actions taken, each with Royce's explicit go:
  - Merged eq-cards #356 (doc-only) and #357 (the pending-credentials/worker_credentials
    false-positive fix — its underlying DB fix was already live via MCP per its own PR body;
    this just landed the paper trail). #357 needed a branch-update-and-recheck first (`mergeable`
    was `BEHIND` after other same-day merges; GitHub's required-checks gate wants them re-run
    against current main, not just present).
  - Merged eq-shell #1913, then dry-ran its logic (see item 4 above for the numbers and the new
    pending-credentials finding — `task_b56ada7f` spawned for it).
  - Independently re-confirmed migration `0169`'s live application (item 2) and resolved the
    multi-tenant-membership caveat (item 4) — both were open questions in this doc as read.
  Did not run `--apply` or `--delete-orphans` (not asked to — Royce's answer was dry-run only).
  Did not touch `task_7d7d8b41` or admin-attach-licence-photo/`task_83d5f0f7`.
- 2026-09-15 (eq-cards reconciliation session, cont.) — Royce said dismiss `task_7d7d8b41`
  (item 5, above) and asked for a prompt on "the real fix" — read as admin-attach-licence-photo
  given that was the open thread left hanging, but that session (`task_83d5f0f7`'s territory)
  was still actively running (670+ messages) at the time; Royce chose to let it finish rather
  than start a competing attempt. Also dispatched and landed the F18 investigation (item 8,
  above) — resolved clean, plus one doc-staleness finding spawned separately as `task_59002a2e`.
  Landing this specific entry took several attempts: `safe_commit.py`'s own upstream-divergence
  check correctly caught two live races against this same file in a row — first the #356/#357/
  #1913 update logged just above, then Royce's own direct correction to item 4 (Claude sessions
  can't actually run #1913's `--apply`: the repair script's copy step is a Storage API call, and
  the Supabase MCP tooling here only exposes Postgres/project-management operations, no
  storage-object copy — noting this plainly since it's a hard capability limit, not a policy
  one). Re-read fresh and reapplied on top both times rather than force-overwriting either.
  Separately hit the brief-gate flag bug this file's own `/brief` skill got fixed for
  (dateless flag naming, fixed 2026-09-15) mid-session, on the wrong side of the fix — a stale
  cached copy of `/brief`'s instructions had this session still writing the old dated flag
  format after the fix landed; re-ran `/brief eq-context` fresh to pick up the corrected
  format rather than fight it further. Not touched: `--apply`/`--delete-orphans`,
  `task_b56ada7f`, admin-attach-licence-photo.
- 2026-09-15 (eq-cards reconciliation session, cont.) — admin-attach-licence-photo's session
  went idle; found its fix committed to a worktree but never pushed or PR'd. Royce's call:
  push it and open a PR rather than dismiss `task_83d5f0f7` on an unshipped fix. Found
  [PR #358](https://github.com/eq-solutions/eq-cards/pull/358) already existed (opened
  independently around that session's end), blocked on a genuinely hung required CI check
  (~10 hours stuck, everything else on the run green) — cancelled and re-ran just that job,
  came back clean, merged on Royce's go. Details in item 6/7 above.
- 2026-09-15 (eq-cards reconciliation session, cont.) — Royce said apply migration `0171` to
  jvkn. Applied and verified live (see item 6 above for the specifics) — clean, zero new
  advisor findings. `task_83d5f0f7`'s chip still needs Royce's own click (same cross-session
  `dismiss_task` limit as `task_7d7d8b41`). This closes out every thread this session picked
  up except the two mechanical chip-clears and whatever `task_59002a2e` (IDENTITY-MODEL.md,
  running independently as of this entry) and `task_b56ada7f` (pending-credentials trace, per
  item 4) come back with.
