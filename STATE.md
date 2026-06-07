---
title: Autonomous Sprint — State
owner: Royce Milmlow
last_updated: 2026-06-03
scope: Per-repo + Supabase reality snapshot, CI guards, and known hazards for the sprint
read_priority: critical
status: live
---

# Autonomous Sprint — STATE (current reality; refresh at sprint start)

> ## ✅ LIVE-VERIFIED RECONCILIATION — 2026-06-03 (supersedes the "left/⛔" framing in all blocks below)
> Royce flagged that the board under-reports completion → causing duplicate builds (Rule 0.5). Re-verified against live Supabase + source this session. **Result: the platform spine is built, populated, and RLS-locked. The ONLY genuinely-open item is B5 (SKS-live cutover, Royce-gated).**
>
> | Claim | Live check (2026-06-03) | Verdict |
> |---|---|---|
> | Tenant registry flipped (eq/demo-trades/melbourne → eq-canonical-internal) | `organisations` table confirms; SKS still → `nspbmirochztcjijmcrx` **by design** (B5 pending) | ✅ |
> | eq-canonical-internal has EQ Field schema | 48 public tables | ✅ |
> | sks-canonical live data | `app_data`: customers 389 / sites 591 / assets 4808; `sks_quotes_customers` 520 | ✅ |
> | **I2** RLS holes (was "Quotes off / SKS permissive") | **every** `app_data.*` + `sks_quotes_*` table on sks-canonical: `rls_enabled=true` | ✅ done |
> | **G1** worker_* schema (board said ⛔⚪ not-started) | `workers, worker_credentials, worker_inductions, worker_assignments` exist | ✅ built |
> | Held migration: timesheet-approval | `timesheets.approved` present on eq-canonical-internal | ✅ applied |
> | Held migration: audit-log-UI | `audit_log.target_id/target_name` present | ✅ applied |
> | Held migration: licence-expiry | superseded by `worker_credentials` (worker-house model) | ✅ moot |
> | **I1** plaintext access codes — Field | codes now from `app_config` (`__TENANT_CODES_DB__`), none in committed JS | ✅ done |
> | **I1** plaintext access codes — SKS Labour | still hardcoded in live app — **= part of B5 cutover** | ⛔ folds into B5 |
> | **TENANT_ORG_UUID** Netlify env (eq-solves-field) | set = `1eb831f9-aeae-4e57-b49e-9681e8f51e15` (matches documented EQ org UUID) | ✅ done |
> | **F1** rotate exposed `ehowg` service_role key | **legacy service_role JWT STILL LIVE** (read live SKS row, HTTP 200; bad-key control 401). Key `iat`≈2026-05-24 unchanged → no JWT-secret rotation. Both consumers (Quotes Fly `SUPABASE_SERVICE_ROLE_KEY`; `tenant_routing` row, anon `eyJhbGci…`, `status_changed_at` 2026-05-24) still hold the legacy key. | ❌ **NOT done** |
>
> **F1 remediation (Royce-gated, P0):** rotate JWT secret / disable legacy keys on `ehowg`, but ONLY after propagating the new key to BOTH consumers (Quotes Fly secret + `tenant_routing` re-encrypt) — disabling legacy blind breaks live Quotes + canonical-api routing. Re-test: legacy service_role GET → 401.
>
> **Bottom line: stop rebuilding the spine. Open code/infra work = B5 + F1 (both Royce-gated). Everything else verified done.**

> ## ⏩ POST-SPRINT UPDATE — 2026-06-07 (suite security pass + OCR / canonical-RLS findings)
> - **Suite security pass DONE.** Read-only audit of all EQ+SKS repos; safe fixes merged in 5 PRs; eq-service came back clean. Detail: `eq-solves-service/docs/security/2026-06-07-suite-key-security-audit.md` + `docs/runbooks/secrets-rotation-and-scoping.md`.
>   - **eq-shell #198** — `ocr-parse` was **UNAUTHENTICATED** (ran paid Google Document AI for any caller). Now session-gated + CORS allow-list; verified 401 on preview. Admin-override merged (blocked by the canonical drift check, unrelated).
>   - Also merged: sks #33 (constant-time HMAC compare), eq-quotes #29 (webhook fail-closed in prod), eq-cards #39 (RLS comment), eq-service #248 (security docs + `backup.yml` → `production-ops` GitHub Environment).
>   - **Royce-action:** Google Document AI quota cap; eq-service CSP report-only→enforce; eq-field demo-PIN rotation (if real data); finish `production-ops` env in eq-shell repo settings; confirm trust models (cards `share-licence`, quotes `QUOTES_SKIP_PASSWORD`). **Never run `netlify env:list --json` in a session — it dumps values.**
> - **OCR is triplicated → consolidate onto EQ Intake.** Shell (Google Doc AI) + Cards (Claude Vision) + the **package-only** Intake vision engine all do "photo→fields". Design (build POST-go-live): `eq-intake` branch `claude/ocr-consolidation-design`. Full finding: `ocr-consolidation-and-canonical-rls-2026-06-07.md`. **Don't build a 4th bespoke OCR.**
> - **Canonical RLS drift-check seam.** eq-shell `scripts/check-tenant-drift.mjs` IS built + enforcing — it fails ANY eq-shell PR on canonical spine drift (the "CI guards" table below still says "not built" — **stale**). `app_data.migration_baseline` RLS oscillated on zaap 2026-06-07 (likely `rls_auto_enable()`); migration `0037` should `ENABLE RLS` to match the on-everywhere norm. Don't blind-toggle canonical prod.

Snapshot 2026-05-30. **Verify before relying on the git/worktree lines** — they drift. The Supabase map + SKS-live flags are stable.

> ## ⏩ POST-SPRINT UPDATE — 2026-06-02 (eq-canonical-internal LIVE as EQ Field tenant DB)
> - **Registry flipped:** eq-canonical `organisations.supabase_url` for eq/demo-trades/melbourne now points to `zaapmfdkgedqupfjtchl` (eq-canonical-internal). All EQ Field operational data writes there.
> - **Schema complete:** 49-table EQ Field operational schema applied to eq-canonical-internal (PR #155, v3.5.50). Exact mirror of eq-solves-field schema.
> - **eq-solves-field (`ktmjmdzqrogauaevbktn`) is now cold backup.** No data deleted. Registry no longer points there for EQ tenants.
> - **Netlify LEAVE_SB_URL/LEAVE_SB_KEY** updated on eq-solves-field site → eq-canonical-internal.
> - **eq-canonical-internal starts clean** — app_config access codes + org rows seeded; people/schedule copied for reference only.
>
> ## ⏩ POST-SPRINT UPDATE — 2026-06-02 (security hardening — 4 migrations applied)
> - **eq-canonical PIN RPC hardening LIVE:** `set_pin_for_user`, `verify_pin_for_user`, `has_pin_for_user` (shell_control) revoked from anon + authenticated; service_role only. `eq_recent_auth_events` anon grant revoked. Migration: `auth_rpc_hardening_pin_service_role_only`. Verified: anon/auth → false, service_role → true.
> - **eq-canonical-internal `_eq_migrations` RLS enabled:** Migration tracker table now has RLS on (was critical advisory). service_role bypasses RLS — migration runner unaffected.
> - **sks-canonical overlay fn revoke LIVE:** 5 `sks_*` trigger functions revoked from anon/authenticated/PUBLIC. Migration: `sks_overlay_fn_revoke`.
> - **sks-canonical safety RPC JWT guard LIVE:** `approve_safety_record` + `submit_safety_record` rewritten to derive tenant from JWT (`app_metadata.tenant_id`) instead of trusting caller-supplied param. Latent cross-tenant write hole closed. Migration: `sks_safety_rpc_jwt_tenant_guard`.
> - **Staged files applied:** archive `eq-shell/supabase/staged/jvkn_auth_rpc_hardening.sql`, `sks_overlay_fn_revoke.sql`, `sks_safety_rpc_hardening.sql`.
> - **`0029_safety_rpcs` committed** to `eq-shell/supabase/tenant-migrations/` — runner will apply to eq-canonical-internal on next migration run. Staged files deleted from `eq-shell/supabase/staged/`.
- **eq-roles v1.3.0 confirmed merged** — `d0fa143` on main; eq-shell already bumped to consume it (`d58513a`).
>
> ## ⏩ POST-SPRINT UPDATE — 2026-06-02 (eq-roles v1.3.0 SHIPPED)
> - **`@eq-solutions/roles` v1.3.0 LIVE** — merged to main, tagged `v1.3.0`, worktree + branch cleaned. Changes shipped: `canAny()` + `canAll()` helpers; 21-test suite (all pass); `package.json` version synced; `prepublishOnly` runs tests; CHANGELOG complete. eq-shell bumped to `#v1.3.0` (commit `d58513a`).
> - **Tenant canonical migration strategy decided** — split migrations into `core/` (applied to every tenant) and `tenants/{eq,sks}/` (tenant-specific extensions). Migration folder doesn't exist yet — create in eq-context or thin `tenant-schema` repo before landing first core schema change.
> - **Direction review complete** — eq-roles architecture sound. Remaining: `labour_hire` perm granularity (before Field labour hire portal), `reports` module gating, `service.assign` perm, tier-gating mechanism.
>
> ## ⏩ POST-SPRINT UPDATE — 2026-06-02 (eq-shell build fix)
> - **eq-shell build fixed** — `@eq/confirm-ui` DTS was failing: (1) `cap_exceeded` missing from `ValidationError` union in `eq-validation/validate.ts` — added; (2) exhaustive switch then made `e: never` in `default:` branch — cast to `{ kind: string }`. Commits `ecd75c2` + `163d799`. Build green, `core.eq.solutions` live.
> - **Session logged:** `sessions/2026-06-02.md`
>
> ## ⏩ POST-SPRINT UPDATE — 2026-06-02 (canonical-api routing live)
> - **tenant_routing LIVE:** `tenants` + `tenant_routing` tables created in eq-canonical. SKS tenant registered → sks-canonical (`ehowgjardagevnrluult`). `TENANT_ROUTING_MASTER_KEY` rotated (new key) + set in eq-shell Netlify. eq-shell redeployed. **canonical-api can now route `X-Tenant: sks` PUT requests to sks-canonical.** Service `syncCustomer`/`syncSite`/`syncAsset`/`syncDefect` and Quotes `write_event` are now live end-to-end.
> - **sks-canonical fully live** — schema was already complete with 60 applied migrations. Live data: customers (389), sites (591), assets (4,808), test results (713), canonical_events (21). EQ Quotes writes directly to `public.sks_quotes_*` (37 documents, 520 customers). `app_data.*` write-through from Service is now unblocked.
>
> ## ⏩ POST-SPRINT UPDATE — 2026-06-02 (tenant model confirmed + quotes/field wiring audit)
> - **Tenant model confirmed by Royce:** `eq-canonical` = control layer only (Cards config, tenant registry). `{tenant}-canonical` = per-tenant Supabase. `eq-canonical-internal` = EQ tenant; `sks-canonical` = SKS tenant. Documented in STATE.md + system/architecture.md + system/infrastructure.md.
> - **eq-context** → merged to main (8 commits from worker-credentials branch). Substrate auto-synced.
> - **eq-solves-field CLAUDE.md** → committed to main (`github.com/eq-solutions/eq-field`). Now references eq-context substrate URL at session start.
> - **EQ Quotes (eq-quotes-sks) audit:** All canonical secrets confirmed deployed ✅ (`CANONICAL_API_KEY`, `CANONICAL_API_KEY_QUOTES`, `CANONICAL_SUPABASE_URL`, `CANONICAL_SUPABASE_KEY`). App wired to `core.eq.solutions` canonical API via `canonical.py`. Fly app name `eq-quotes-sks` = correct (follows `{tenant}` suffix convention). Stale `SUPABASE_URL` env var removed from fly.toml. Live at `quotes.eq.solutions`.
> - **EQ Service canonical wiring audit:** COMPLETE ✅. `canonical-sync.ts` is wired into all key server actions — `syncCustomer` (customers create/update/archive), `syncSite` (sites create/update/archive), `syncAsset` (assets create/update), `syncDefect` + `emitEvent` (maintenance/defects), `syncTestResult` (RCD/ACB/NSX tests). `CANONICAL_API_KEY_SERVICE` confirmed set in BOTH eq-solves-service AND eq-shell Netlify (same value). `GET /api/admin/export` bulk snapshot endpoint fully wired + admin-gated. 4 export stubs remain (contact, attachment, maintenance_plan, maintenance_plan_item) — not blocking. STATE.md "fill stubs" note was misleading — write-through is live.
> - **Royce-action resolved:** (2) fly deploy ✅ done; (3) CANONICAL_API_KEY_QUOTES ✅ confirmed set.
> - **Royce-action still pending:** (1) `TENANT_ORG_UUID` Netlify env var for eq-solves-field; (4) drift CI secrets in eq-shell GitHub repo settings; (5) revoke old `gho_...` PAT.
>
> ## ⏩ POST-SPRINT UPDATE — end of 2026-06-01 (Sprint 4: quality polish + Direction D build wave; supersedes all prior blocks)
> All unblocked code work complete. Royce-action items remain (see bottom).
> - **eq-shell** → **PR #122 on main**. eq-ui v1.1.1 consumed. Quality polish PRs #116–#119 + #122 all merged: L3 briefing lazy, U3 jargon, P5 font, U2, C3, M1, P1 cache, P2 lazy, M2 sidebar, D3.3 icon rail gaps (Q4 Quotes tooltip), D5.1 v1.1.1 bump. Open gated: #80 (⛔ auth), security-groups (#123 merged — B2 groups).
> - **eq-solves-service** → **PR #224 on main**. Quality polish PRs #217–#224 merged: M3, C2, 7 loading.tsx, E5, Z3, P4 RPC, D3.3 calendar, site access edit, defect detail page, eq-ui v1.1.1 bump. Service latest: `003ca22`.
> - **eq-solves-field** → **v3.5.49 on main** (PR #153): L5 SW update toast + U6 PIN from app_config. **PENDING Royce action: `TENANT_ORG_UUID` Netlify env var required for U6 to activate.**
> - **eq-ui** → **v1.1.1 tagged**: ghost Button hover border. Tag live on GitHub. Consumers (Shell #122, Service #222) bumped.
> - **Direction D** → **COMPLETE.** D3.3 all 4 specs built, D5.1/D5.2 adopted, D6.x all done.
> - **Royce-action required (blocking production features):** (1) `TENANT_ORG_UUID` Netlify env var for eq-solves-field EQ site; (2) `fly deploy` from `eq-quotes-port`; (3) verify `CANONICAL_API_KEY_QUOTES` in Fly secrets; (4) drift CI secrets in eq-shell GitHub repo settings; (5) revoke old `gho_...` PAT at github.com/settings/tokens.
> - **Migration-gated (Field):** #2 timesheet approval, #5 leave balance, #10 unavailability, #11 portal, #15 audit-log UI — awaiting Royce-approved DB migration on `ktmjmdzqrogauaevbktn`.

> ## ⏩ POST-SPRINT UPDATE — end of 2026-05-30 (Sprint 1 + Sprint 2 Waves 1–2 ALL MERGED; supersedes the table rows below where they conflict)
> The "everything-then-cutover" fan-out + Sprint 2 completed. Current reality:
> - **eq-solves-field** → **v3.5.33 on `main`**, clean. SKS-only modules ported + **triple tenant-gated to `sks`** (EQ provably unaffected): `safety` (#138), `teams` (#139), `sks-pipeline*` (#140) + 10 B3 reconcile fixes (#141). **Wave 1 #143 (v3.5.31):** timesheet pre-fill, multi-week export, hard-delete leave, roster copy-week, audit-log field-fix. **Wave 2 #144 (v3.5.32):** roster PDF/print, dashboard gap-card, calendar person-filter, apprentice year auto-advance. **Batch #145 (v3.5.33):** weekly site-attendance report, roster bulk assign/clear, mobile roster swipe (pages the *week*), + **print.css EQ/SKS tenant-brand fix** (EQ deep default, navy only under `body.tenant-sks`). Worktrees cleaned. **EQ-tenant no-migration backlog now ~exhausted** — next Field work needs a parked migration, the #20 PIN/auth fix, or net-new scope (see `field-feature-backlog-2026-05-30.md` BUILD STATUS).
> - **eq-shell** → consumes **`@eq-solutions/roles`** (C2 #70 — perms verified identical) **and `@eq-solutions/ui` fully** (#71 Table+Skeleton; **#73 Button across all 14 surfaces** + eq-ui v1.0.1 bordered ghost). **Wave 2 #75:** iframe errors→`EqError`, retry loading-state, null-tenant notice, NotFound plain-English + aria. `claude/c3-auth-spike` (#72) = no-deploy reference (live auth untouched).
>   - **2026-05-31 (C4 console):** **PR #79 MERGED → main `9905be5`, LIVE + smoke-verified** (`core.eq.solutions/.netlify/functions/verify-shell-session` → 401): intake-commit server-authz (was wide open to any signed-in user), 3 UI button/token bugs, `friendlyError`, `docs/cross-app-audit.md`. Added `netlify/functions/_shared/permissions.ts` (re-defines matrix = Rule §5 divergence, identical-to-canonical, reconcile via C8). **PR #80 OPEN/MERGEABLE — ⛔ auth-gated:** TS strict + TOTP rate-limit. **PR #78 (canonical reconciliation) also MERGED → main.** Open eq-shell PRs: #80 (auth-gated), #72 (spike, no-merge), #69 (equipment), #64 (AI briefing).
> - **eq-solves-service** → consumes `@eq-solutions/ui` (#205). **Wave 1 #206:** pre-visit tech-brief + 4 quality fixes. **Wave 2 #207:** defect detail+photos, analytics cuts (in-app, not RPC), canonical-export fill stubs, asset detail `/assets/[id]`, calibration reminders, skip-nav, detail loading. `npm run check` clean, 201/201 vitest.
> - **eq-cards** → tokens consolidated (#10). Cards worker-first rebuild (E1) deferred → now directed by the worker-credentials model (below).
> - **2026-05-31 — WORKER-CREDENTIALS MODEL DECIDED (design):** worker data lives in the **worker-house** (`eq-canonical-internal` `worker_*`), first-class `worker_id`, SKS-seed-via-Intake as the verification event (evidence-on-file → top trust tier). Build order: worker-house + reminders FIRST, snapshot/live-link/grant SECOND. **Supersedes the Cards-rewire per-business-tenant assumption — do NOT flip Cards `gateway` yet.** Record: `eq/identity/worker-credentials-model-2026-05-31.md`; sprint: SPRINT-BOARD Stream G.
> - **Packages:** **`@eq-solutions/roles`** (public — consumed by Shell) + **`@eq-solutions/ui` v1.0.1** (public, bordered ghost — consumed by Shell+Service) + `@eq-solutions/tokens`. Design pillar = COMPLETE. ⚠ A concurrent session is tagging these (`eq-roles v1.0.0`, `eq-ui v1.0.1`) + moving consumers `#main`→consume-by-tag (also owns the literal `STATE.md` row-33 fix this round).
> - **Branch tidy-up:** 108 old merged branches + all Wave-2 branches deleted across eq-field/shell/service/cards; unmerged/open + reference branches kept.
> - **HELD — Royce-gated (features ship dormant until you act):** 3 DB migrations NOT run — licence-expiry (`people.licence_expiry` @ `ktmjmdzqrogauaevbktn`), timesheet-approval (`approved`/`approved_by`/`approved_at` on `timesheets`), audit-log-UI (`target_id`/`target_name` on `audit_log`). Plus B4 canonical wiring, ⛔ C4 auth cutover, **B5 cutover = LAST (SKS-live)**. SKS-live (`nspbmirochztcjijmcrx`) untouched throughout.
> - **EYEBALL (low-risk, post-merge):** (1) F-W2-4 apprentice auto-advance batch-mutates real rows — test on one apprentice before broad use; (2) **#145 print colours** — confirm browser Print-preview shows EQ-deep on an EQ tenant + navy on SKS (cascade-verified via `body.tenant-sks`, but browser print pixels not machine-provable); (3) **#145 mobile swipe** pages the *week* (the one-day-view premise was stale) — isolated ~70-line block, easy to retune. (print.css SKS-navy follow-up = DONE in #145.)

## Repos
| repo | GitHub | prod target | branch state @ snapshot | notes |
|------|--------|-------------|--------------------------|-------|
| **eq-shell** | eq-solutions/eq-shell (public) | **core.eq.solutions** (auth hub) on `main` | main synced; **ACTIVE other sessions** | worktrees: `affectionate-yonath` (85 uncommitted!), `equipment-finish`, `festive-burnell`, `naughty-heyrovsky`, `equipment-qr-hierarchy`(#69). Build `pnpm run build`. Hotspot file: `src/pages/TenantHome.tsx`. |
| **eq-solves-field** | eq-solutions/eq-field (public) | eq-solves-field.netlify.app on `main` | idle ~17h; main behind 2 | EQ-side of the merge. Stale worktree `musing-mcnulty` (5 uncommitted). My `claude/field-merge-phase1` worktree staged. Vanilla HTML/JS/CSS; version-stamp every release. |
| **sks-nsw-labour** | eq-solutions/sks-nsw-labour | **sks-nsw-labour.netlify.app = SKS LIVE — DO NOT DEPLOY** | idle ~18h; ahead1/behind3 | 5 stale worktrees incl `pipeline-ui`. Source of the SKS-only modules to PORT (read from `origin/main`). |
| **eq-solves-service** | Milmlow/eq-solves-service | eq-solves-service.netlify.app on `main` | #203/#204 merged; local main diverged (leave) | Next 16. `npm run check` before push. CI `data-quality audit` fails on expired `SUPABASE_ACCESS_TOKEN` (known, unrelated). Worktree `charming-dirac` dormant (committed). |
| **eq-cards** | Milmlow/eq-cards | (Flutter app) | **clean**, idle ~18h, no worktrees | safest repo to work in. NOT SKS. |
| **eq-intake** | (home of `@eq/*`) | n/a (vendored into eq-shell) | **main ahead 23 unpushed**; active worktree `clever-roentgen` (6 uncommitted) | changes here must be **re-vendored into eq-shell**. |
| **eq-roles** | eq-solutions/eq-roles (public) | n/a (package) | **v1.3.0 on main** — tag live, branch cleaned | consumed by eq-shell `#v1.3.0` (d58513a). `canAny`/`canAll` + 21-test suite. No open PRs. |
| **eq-design-tokens** | eq-solutions/eq-design-tokens (**public**) | n/a (package) | v1.0.0 tag | consumed by Shell/Field/Service via git-dep. |

## Supabase projects (org `sqjyblkiqonyrdobaucn`, ap-southeast-2)
| ref | name | role | access |
|-----|------|------|--------|
| `jvknxcmbtrfnxfrwfimn` | eq-canonical | **Control layer** — Cards config, tenant registry, app settings. Browser-accessible via `VITE_SUPABASE_URL`. | browser via VITE_SUPABASE_URL |
| `zaapmfdkgedqupfjtchl` | eq-canonical-internal | **EQ tenant Supabase** — all EQ Solutions operational/tenant data (workers, identity, ops). Pattern: `{tenant}-canonical`. | EQ tenant data |
| `ktmjmdzqrogauaevbktn` | eq-solves-field | **Cold backup** — EQ Field was here pre-2026-06-02. Registry now points to eq-canonical-internal. | cold backup |
| `urjhmkhbgaxrofurpbgc` | eq-solves-service-dev | Service DB + context substrate (`context_files`) | per repo |
| `ehowgjardagevnrluult` | sks-canonical | **SKS tenant Supabase** — all SKS operational/tenant data. Pattern: `{tenant}-canonical`. SKS tenant id `7dee117c-98bd-4d39-af8c-2c81d02a1e85`. | SKS tenant data |
| `nspbmirochztcjijmcrx` | sks-labour | **SKS LIVE operational DB** | **READ-ONLY / AVOID — SKS live** |

**Tenant model:** `eq-canonical` = control layer only (config, registry). Each tenant gets their own `{tenant}-canonical` Supabase with all their data. EQ Field boots from eq-canonical to resolve the tenant's Supabase connection, then all data ops go direct to that tenant's project. `eq-canonical-internal` = EQ's tenant; `sks-canonical` = SKS's tenant.

## CI guards
| guard | repo | status |
|-------|------|--------|
| token drift-guard | eq-solves-field | ✅ `.github/workflows/tokens-drift.yml` |
| token drift-guard | eq-cards (dart) | ⚪ not built (deferred w/ A4) |
| **dup-migration guard** | eq-solves-service | ⚪ **spec'd, not built** (RULES §6) — broke twice; build first |
| **tenant canonical drift guard** | eq-context (or tenant-schema repo) | ⚪ **strategy agreed, not built** — CI job to confirm `eq-canonical-internal` + `sks-canonical` have applied all `core/` migrations. Blocker: migration folder doesn't exist yet. |

## Known hazards (don't re-trip these)
- Sequential `00xx` migrations collide across parallel agents → **timestamps only** (RULES §3). `eq-solves-service 0110` taken.
- Branching from local `main` drags other sessions' commits → **branch from `origin/main`** (RULES §2).
- Stale worktrees hold uncommitted work → **never prune without confirming committed** (RULES §2).
- `eq-shell src/pages/TenantHome.tsx` edited by PRs #64/#65/#68/#69 → coordinate.
