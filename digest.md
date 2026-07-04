---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-07-04
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-07-04 05:19 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-07-03 20:26 UTC → 2026-07-04 05:19 UTC)

- Merged: eq-shell [#642](https://github.com/eq-solutions/eq-shell/pull/642) Tenants page: permanently delete an archived tenant
- Merged: eq-shell [#641](https://github.com/eq-solutions/eq-shell/pull/641) fix: clear a stuck data-plane provisioning job from the Tena
- Merged: eq-shell [#638](https://github.com/eq-solutions/eq-shell/pull/638) fix(provisioning): shell_control.provision_tenant never actu
- Merged: eq-shell [#634](https://github.com/eq-solutions/eq-shell/pull/634) fix(sync-quotes-nightly): check errors on Flask write-back +
- Merged: eq-shell [#633](https://github.com/eq-solutions/eq-shell/pull/633) docs: correct CLAUDE.md — EQ_SECRET_SALT is the fallback sig
- Merged: eq-shell [#617](https://github.com/eq-solutions/eq-shell/pull/617) Harden self-serve tenant provisioning: transactional RPC, ph
- Merged: eq-shell [#610](https://github.com/eq-solutions/eq-shell/pull/610) fix(audit): grant audit_log id-sequence to service_role; sur
- Merged: eq-shell [#609](https://github.com/eq-solutions/eq-shell/pull/609) fix(staff): pending-connections roster-name fallback never m

## ⚠ Needs you (4)

- 🟠 **Sentry new error** — `eq-field` [SyntaxError: Unexpected end of input](https://eq-solutions.sentry.io/issues/131931795/)
- 🟠 **Sentry new error** — `eq-field` [ReferenceError: openCleanupCodes is not defined](https://eq-solutions.sentry.io/issues/132094727/)
- 🟠 **Sentry new error** — `eq-cards` [provisionTenantExchange: unexpected HTTP 500](https://eq-solutions.sentry.io/issues/132064194/)
- 🟡 **1 stale worktree** need cleanup — [worktree-registry.md](system/worktree-registry.md)

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ? unknown | ? | 3 | 0d |
| eq-solves-service | ✓ success | 0d ago | 0 | — |
| eq-field | ? unknown | ? | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ? unknown | ? | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-field | [SyntaxError: Unexpected end of input](https://eq-solutions.sentry.io/issues/131931795/) | 2 | 2026-07-03 |
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
| 2026-07-04 | eq-shell | [#641](https://github.com/eq-solutions/eq-shell/pull/641) fix: clear a stuck data-plane provisioning job from the Tenants p |
| 2026-07-04 | eq-shell | [#642](https://github.com/eq-solutions/eq-shell/pull/642) Tenants page: permanently delete an archived tenant |
| 2026-07-04 | eq-solves-service | [#431](https://github.com/eq-solutions/eq-service/pull/431) fix: restore public.canonical_outbox, dropped by mistake on 2026- |
| 2026-07-04 | eq-field | [#390](https://github.com/eq-solutions/eq-field/pull/390) v3.5.227 — QA sheet: middle-name linking + remove 3 redundant but |
| 2026-07-04 | eq-field | [#389](https://github.com/eq-solutions/eq-field/pull/389) v3.5.225 — prestart: full SKS template (export + form capture) |
| 2026-07-03 | eq-shell | [#634](https://github.com/eq-solutions/eq-shell/pull/634) fix(sync-quotes-nightly): check errors on Flask write-back + line |
| 2026-07-03 | eq-shell | [#633](https://github.com/eq-solutions/eq-shell/pull/633) docs: correct CLAUDE.md — EQ_SECRET_SALT is the fallback signing  |
| 2026-07-03 | eq-shell | [#638](https://github.com/eq-solutions/eq-shell/pull/638) fix(provisioning): shell_control.provision_tenant never actually  |
| 2026-07-03 | eq-shell | [#627](https://github.com/eq-solutions/eq-shell/pull/627) fix(provisioning): convert provision-tenant to a background funct |
| 2026-07-03 | eq-shell | [#626](https://github.com/eq-solutions/eq-shell/pull/626) fix(admin): resolve --eq-ink to a real hex value for the worker Q |
| 2026-07-03 | eq-shell | [#623](https://github.com/eq-solutions/eq-shell/pull/623) fix(intake): re-vendor field-name + plain-English fixes from eq-s |
| 2026-07-03 | eq-shell | [#625](https://github.com/eq-solutions/eq-shell/pull/625) feat(security): view security_invoker invariant (CHECK 7) + field |
| 2026-07-03 | eq-shell | [#624](https://github.com/eq-solutions/eq-shell/pull/624) fix(provisioning): tenant_routing NOT NULL columns block every Pr |
| 2026-07-03 | eq-shell | [#620](https://github.com/eq-solutions/eq-shell/pull/620) fix(ci): check-migration-hygiene.mjs skips SQL line comments |
| 2026-07-03 | eq-shell | [#618](https://github.com/eq-solutions/eq-shell/pull/618) fix(security): reassert security_invoker on field_managers + nomi |
_Showing 15 of 127 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Manual click-through of PR #641 once deployed** — load `/_platform/tenants`, confirm no regression on Provision/Retry/Archive/Reactivate **and** the new hard-delete action from PR #642, and (if a stuck row exists, or one is forced) confirm "Stuck — Cancel" appears only past 20 min and Retry re-provisions cleanly afterward. _(added 2026-07-04)_
- **Merge eq-context PR #62.** _(added 2026-07-04)_
- **Arm the Phase 1 + Phase 2 backups (needs Royce)** — supplementary detail verified live via `gh` just now: eq-context's `production-ops` **GitHub Environment does not exist yet** (Phase 1 isn't armed either, not just Phase 2). Repo secrets currently present: `EQ_CONTEXT_PAT`, `EQ_SHELL_JWT_SECRET`, `SENTRY_AUTH_TOKEN`, `SUPABASE_ACCESS_TOKEN`, `SUPABASE_SERVICE_ROLE_KEY` (= ehow key) — that's all. None of `R2_ACCESS_KEY_ID/SECRET/ENDPOINT/BUCKET_NAME`, `SENTRY_DSN`, ehow's `SUPABASE_DB_URL`, or the 4 `EQ_CANONICAL*`/`EQ_CANONICAL_INTERNAL*` secrets exist in eq-context yet. **`eq-service` repo already has live `R2_ACCESS_KEY_ID`/`R2_SECRET_ACCESS_KEY`/`R2_ENDPOINT`/`R2_BUCKET_NAME` + its own `SUPABASE_DB_URL`** — reusable by copying the values across, no Cloudflare-dashboard trip needed for R2. `SENTRY_DSN` doesn't exist anywhere yet — genuinely needs creating fresh in Sentry. _(supplementary detail added 2026-07-04, needs your call)_
- **Orphaned Supabase project `eq-tenant-favour-perfect` (`jzjzpgaablnppoimdnip`)** — DB rows are gone (above), but the project itself is still `ACTIVE_HEALTHY`. No MCP tool can delete/pause it (`pause_project` failed again: "not free-tier, downgrade first"); needs Royce via the Supabase dashboard directly — org `sqjyblkiqonyrdobaucn` → project "eq-tenant-favour-perfect" → Settings → General → Delete project. _(added 2026-07-04, needs your call)_
- **Test the Add-tenant → data-plane Provision button flow fresh** — this session verified the *self-serve invite-link* path end-to-end; the *admin manually creates a tenant, then clicks Provision* path (same PR #627 fix) was never independently walked start-to-finish on a brand-new tenant. _(added 2026-07-04)_
- **Leave submit-path** — never load-tested a real leave submission this session (real-email side effect); still open ahead of Royce's stress-testing week. _(added 2026-07-04)_
- **QR/join-code worker flow** — `JoinContextNotifier`'s keepalive fix (PR #120) was applied by exact code-pattern match to the provision-context bug, not independently reproduced/verified live. Worth a live pass before the 15th. _(added 2026-07-04)_
- **Set a code-freeze date before 15 July** — not yet decided. _(added 2026-07-04, needs your call)_
- **206 Supabase security advisories on ehow** — Royce's call from earlier this session: keep for a dedicated session, not folded into this one. _(added 2026-07-03, needs your call)_
- **Arm the ehow backup (needs Royce)** — create eq-context `production-ops` env (main-only, no reviewers) + add secrets `SUPABASE_DB_URL` (ehow pooler), `R2_ACCESS_KEY_ID/SECRET/ENDPOINT/BUCKET_NAME`, `SENTRY_DSN`; run once via `workflow_dispatch`; confirm green + R2 contents + Sentry check-in. _(added 2026-07-04)_
_…and 220 more · [eq/pending.md](eq/pending.md)_

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
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-07-04 05:19 UTC._
