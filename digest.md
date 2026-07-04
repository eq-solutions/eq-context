---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-04
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-04 08:49 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-04 07:16 UTC → 2026-07-04 08:49 UTC)

- Merged: eq-shell [#648](https://github.com/eq-solutions/eq-shell/pull/648) feat(entitlements): app tiles → canonical, Stage A (readers)
- Merged: eq-shell [#645](https://github.com/eq-solutions/eq-shell/pull/645) feat(field): surface customer name on field_sites + drop dea
- Merged: eq-shell [#644](https://github.com/eq-solutions/eq-shell/pull/644) refactor(branding): one canonical copy in organisations.bran
- Merged: eq-shell [#626](https://github.com/eq-solutions/eq-shell/pull/626) fix(admin): resolve --eq-ink to a real hex value for the wor
- Merged: eq-shell [#624](https://github.com/eq-solutions/eq-shell/pull/624) fix(provisioning): tenant_routing NOT NULL columns block eve
- Merged: eq-shell [#620](https://github.com/eq-solutions/eq-shell/pull/620) fix(ci): check-migration-hygiene.mjs skips SQL line comments
- Merged: eq-shell [#619](https://github.com/eq-solutions/eq-shell/pull/619) fix(field-iframe): preserve deep-linked ?tab= on initial ten
- Merged: eq-shell [#618](https://github.com/eq-solutions/eq-shell/pull/618) fix(security): reassert security_invoker on field_managers +

## ⚠ Needs you (4)

- 🟠 **Sentry new error** — `eq-field` [SyntaxError: Unexpected end of input](https://eq-solutions.sentry.io/issues/131931795/)
- 🟠 **Sentry new error** — `eq-field` [SyntaxError: Identifier 'AUDIT_SECTIONS' has already been de](https://eq-solutions.sentry.io/issues/132112850/)
- 🟠 **Sentry new error** — `eq-field` [ReferenceError: openCleanupCodes is not defined](https://eq-solutions.sentry.io/issues/132094727/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 4 | 0d |
| eq-solves-service | ✓ success | 0d ago | 1 | 0d |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-field | [SyntaxError: Unexpected end of input](https://eq-solutions.sentry.io/issues/131931795/) | 2 | 2026-07-03 |
| eq-field | [SyntaxError: Identifier 'AUDIT_SECTIONS' has already been declared](https://eq-solutions.sentry.io/issues/132112850/) | 1 | 2026-07-04 |
| eq-field | [ReferenceError: openCleanupCodes is not defined](https://eq-solutions.sentry.io/issues/132094727/) | 1 | 2026-07-04 |
| eq-cards | [provisionTenantExchange: unexpected HTTP 500](https://eq-solutions.sentry.io/issues/132064194/) | 1 | 2026-07-03 |
| eq-field | [Error: 400: {"code":"23502","details":null,"hint":null,"message":"null value in ](https://eq-solutions.sentry.io/issues/131921038/) | 1 | 2026-07-03 |
| eq-cards | [: Unable to load asset: "NOTICES".](https://eq-solutions.sentry.io/issues/131717362/) | 1 | 2026-07-02 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/131636027/) | 1 | 2026-07-02 |
| eq-shell | [TypeError: Load failed](https://eq-solutions.sentry.io/issues/131334219/) | 1 | 2026-06-30 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-07-04 | eq-shell | [#648](https://github.com/eq-solutions/eq-shell/pull/648) feat(entitlements): app tiles → canonical, Stage A (readers) |
| 2026-07-04 | eq-shell | [#644](https://github.com/eq-solutions/eq-shell/pull/644) refactor(branding): one canonical copy in organisations.branding  |
| 2026-07-04 | eq-shell | [#645](https://github.com/eq-solutions/eq-shell/pull/645) feat(field): surface customer name on field_sites + drop dead cus |
| 2026-07-04 | eq-shell | [#643](https://github.com/eq-solutions/eq-shell/pull/643) feat(branding): self-serve tenant document branding editor |
| 2026-07-04 | eq-shell | [#641](https://github.com/eq-solutions/eq-shell/pull/641) fix: clear a stuck data-plane provisioning job from the Tenants p |
| 2026-07-04 | eq-shell | [#642](https://github.com/eq-solutions/eq-shell/pull/642) Tenants page: permanently delete an archived tenant |
| 2026-07-04 | eq-solves-service | [#438](https://github.com/eq-solutions/eq-service/pull/438) chore(dr): retire eq-service offsite backup — platform DR moved t |
| 2026-07-04 | eq-solves-service | [#436](https://github.com/eq-solutions/eq-service/pull/436) test: add unit tests for lib/api/platform-admin.ts (timing-safe p |
| 2026-07-04 | eq-solves-service | [#435](https://github.com/eq-solutions/eq-service/pull/435) test: add unit tests for propagateCheckCompletionIfReady (check-c |
| 2026-07-04 | eq-solves-service | [#434](https://github.com/eq-solutions/eq-service/pull/434) docs: fix stale role names and add RCD testing to README |
| 2026-07-04 | eq-solves-service | [#433](https://github.com/eq-solutions/eq-service/pull/433) docs: document CLOUDCONVERT_API_KEY and IDENTITY_CLAIMS_ENABLED i |
| 2026-07-04 | eq-solves-service | [#432](https://github.com/eq-solutions/eq-service/pull/432) chore: drop dead GOTENBERG_URL from .env.example (Fly.io retired) |
| 2026-07-04 | eq-solves-service | [#431](https://github.com/eq-solutions/eq-service/pull/431) fix: restore public.canonical_outbox, dropped by mistake on 2026- |
| 2026-07-04 | eq-field | [#404](https://github.com/eq-solutions/eq-field/pull/404) v3.5.239 — job numbers: one board, EQ Ops is the source of truth |
| 2026-07-04 | eq-field | [#403](https://github.com/eq-solutions/eq-field/pull/403) v3.5.237 — safety photos to Storage, not inline base64 (QA row 31 |
_Showing 15 of 124 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Run the first manual restore game-day** — full restore into a Supabase-parity target + app repoint (proves executability + operational RTO). Data-integrity is covered daily by the automated verify; this is the rarer human drill. _(carried 2026-07-04)_
- **Rows 4 & 8 — resolved by verification, reopen only if they recur** — row 4 (duplicate "From Roster"): structurally only one button exists (the "twice" was the button + a muted-cell "from roster" label); row 8 (`?tab=person-wizard` blank): moot on SKS now that Add Person is hidden. Need a screenshot/repro to reopen either. _(added 2026-07-04)_
- **Rows 26/36 — link Field job numbers to the canonical jobs board** — banked as `task_1a8e00fd` (running). Field's `public.job_numbers` (14) and the Shell comms board `app_data.sks_comms_jobs` (20) are two non-syncing lists of the same SKS jobs, **zero overlap**, same 5-digit format → drift. Recommended: reconcile the 28, expose `app_data.field_job_numbers` view over `sks_comms_jobs`, Field reads it (read-only). **Gated on Royce confirming which board is source-of-truth** (comms is a trial today) _(needs your call — added 2026-07-04)_
- **Row 31 — confirm the SKS authenticated Storage round-trip live** — the photo upload/download activates only with the Shell data JWT (couldn't drive standalone; browser preview uncooperative). Fully protected by the verified graceful fallback (fails → stays base64, zero regression). Confirm next time in an SKS Shell session, or by checking `public.prestarts.photos` rows gain `storage_path` after a photo is added. _(added 2026-07-04)_
- **Tenant logo/branding editor in EQ Shell** — upload-or-link → store in R2 → write canonical `organisations.branding.{gateLogo,palette}`; every app inherits. Running as spawned task `task_925f8842`. _(added 2026-07-04)_
- **eq demo tenant is logo-less in docs until the Shell editor ships** — or seed `eq`'s `branding.gateLogo` with a `.png` URL as a stopgap (Royce's call). _(added 2026-07-04)_
- **Manual click-through of PR #641 once deployed** — load `/_platform/tenants`, confirm no regression on Provision/Retry/Archive/Reactivate **and** the new hard-delete action from PR #642, and (if a stuck row exists, or one is forced) confirm "Stuck — Cancel" appears only past 20 min and Retry re-provisions cleanly afterward. _(added 2026-07-04)_
- **Merge eq-context PR #62.** _(added 2026-07-04)_
- **Arm the Phase 1 + Phase 2 backups (needs Royce)** — supplementary detail verified live via `gh` just now: eq-context's `production-ops` **GitHub Environment does not exist yet** (Phase 1 isn't armed either, not just Phase 2). Repo secrets currently present: `EQ_CONTEXT_PAT`, `EQ_SHELL_JWT_SECRET`, `SENTRY_AUTH_TOKEN`, `SUPABASE_ACCESS_TOKEN`, `SUPABASE_SERVICE_ROLE_KEY` (= ehow key) — that's all. None of `R2_ACCESS_KEY_ID/SECRET/ENDPOINT/BUCKET_NAME`, `SENTRY_DSN`, ehow's `SUPABASE_DB_URL`, or the 4 `EQ_CANONICAL*`/`EQ_CANONICAL_INTERNAL*` secrets exist in eq-context yet. **`eq-service` repo already has live `R2_ACCESS_KEY_ID`/`R2_SECRET_ACCESS_KEY`/`R2_ENDPOINT`/`R2_BUCKET_NAME` + its own `SUPABASE_DB_URL`** — reusable by copying the values across, no Cloudflare-dashboard trip needed for R2. `SENTRY_DSN` doesn't exist anywhere yet — genuinely needs creating fresh in Sentry. _(supplementary detail added 2026-07-04, needs your call)_
- **Orphaned Supabase project `eq-tenant-favour-perfect` (`jzjzpgaablnppoimdnip`)** — DB rows are gone (above), but the project itself is still `ACTIVE_HEALTHY`. No MCP tool can delete/pause it (`pause_project` failed again: "not free-tier, downgrade first"); needs Royce via the Supabase dashboard directly — org `sqjyblkiqonyrdobaucn` → project "eq-tenant-favour-perfect" → Settings → General → Delete project. _(added 2026-07-04, needs your call)_
_…and 226 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date.
- **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
- **SKS anon-remediation (nspb)** — exact policy worklist in `cross-app-linkage-remediation-plan-2026-06-07.md` §7a. Separate from ehow work. SKS-live gated.
- **eq-shell** — ~~converge `c2-shell-roles` + `sks-field-host` branches~~ — `c2-shell-roles` no longer exists in eq-shell repo (deleted). Re-assess: verify whether the security-groups work from `sks-live-sprint-2026-06-07.md` Prompt A was folded into main or abandoned before reopening this track.
- **Security groups Phase 2–5** — wire group perms into session, `AdminSecurityGroups` page, first real `user_security_groups` row for a SKS user.
- Person-wizard renders blank content specifically on a cold `?tab=person-wizard` deep-link boot (normal in-app "Add Person" nav works fine) — root cause not found despite exhaustive code trace + live Sentry/entitlement checks; needs Royce's own DevTools session with the Field-iframe console context selected _(added 2026-07-03)_
- At least one SKS person ("Collin ... Toohey") has no record in canonical `app_data.staff`, blocking their leave submissions — data-ops backfill needed, not a code fix _(added 2026-07-03)_
- Royce to independently click-through-confirm the Weekends toggle, roster names, and both safety forms live (smoke-tested remotely, not yet confirmed by Royce beyond the original repros) _(added 2026-07-03)_
- Book monthly check-in cadence with Richo (Michael Richardson)
- Tell Mark about catch-up conversations before starting (casual, no fanfare)
_…and 18 more · [sks/pending.md](sks/pending.md)_

## Recent sessions

| Date | Session |
|------|---------|
| 2026-07-04 | [eq-shell worktree hygiene: stale checkout diagnosed and restored](sessions/2026-07-04.md) |
| 2026-07-03 | [eq-shell: batch site delete/archive built (PR #613 open, merge blocked)](sessions/2026-07-03.md) |
| 2026-07-02 | [Token lint ratchet merged; staff licence resync endpoint shipped](sessions/2026-07-02.md) |
| 2026-06-30 | [EQ Field canonical sprint complete (v3.5.207–212)](sessions/2026-06-30.md) |
| 2026-06-30 | [2026-06-30 (part g) — Field canonical wiring sprint: v3.5.207–v3.5.211](sessions/2026-06-30-field-canonical-sprint-g.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-04 08:49 UTC._
