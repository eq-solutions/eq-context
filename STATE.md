---
title: Autonomous Sprint — State
owner: Royce Milmlow
last_updated: 2026-06-13
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

Snapshot 2026-05-30. **Verify before relying on the git/worktree lines** — they drift. The Supabase map + SKS-live flags are stable.

> ## ⏩ POST-SPRINT UPDATE — 2026-06-13 (EQ Service iframe loading fixed)
> - **EQ Service iframe fixed (eq-shell PR #334, merged + deployed 2026-06-13T00:44:57Z):** `ServiceIframe.tsx` fallback timer 12s → 4s. Root cause: stale OTP comment — TOKEN MODE handshake completes in ~2-3s; 12s timer restarted on every refresh, showing loading screen indefinitely. Sentry breadcrumbs added (`EQ_SERVICE_READY` received = info; fallback fired = warning). Service appears within ~4s at `core.eq.solutions/sks/service`.
> - **Smoke test pending (Royce):** navigate to `/sks/service`, confirm dashboard loads within 5s.

> ## ⏩ POST-SPRINT UPDATE — 2026-06-11 (v3.5.125 — SKS canonical DB full JWT coverage)
> - **SKS Field data plane fixed (ehow):** SKS Field was showing all zeros + loading spinners after v3.5.120 cut-over. Root cause: 7 of 11 `app_data.field_*` views missing → PGRST205 on every data load. All 11 views created. `public.site_diaries` created (completes JWT_TABLES). `public.organisations` stub added (eliminates 404 boot noise). RLS WITH CHECK hardened on 14 write policies. `audit_log` RLS fixed (nspb UUID → correct SKS org_id). 109 legacy audit_log rows deleted.
> - **Data state post-fix:** 58 staff · 591 sites · 0 roster rows (start fresh required).
> - **Migration:** `supabase/migrations/20260611_sks_canonical_field_sync.sql` (idempotent). PR #267 merged + live.
> - **Roster data entry pending** — ehow schedule/timesheets/leave are empty. Royce decision required.

> ## ⏩ POST-SPRINT UPDATE — 2026-06-10 (EQ Service Shell SSO root cause — eq-shell PR #306)
> - **Root cause found (was in Shell, not Service):** `COOKIE_AUTH = true` in `ServiceIframe.tsx` activated whenever `VITE_SERVICE_URL` ended in `.eq.solutions`. Cookie mode skips token minting; Shell restores from Supabase cookies without re-minting `eq_shell_session` — cookie absent at iframe-load → proxy.ts never calls shell-sso.
> - **Fix:** `COOKIE_AUTH = false` → TOKEN MODE always. PR #306 merged, deploy `6a285d53` live.
> - **TOKEN MODE flow (proven):** `token-exchange?aud=service` → Supabase JWT → `/shell#sh=<jwt>` → `/api/shell-auth` validates → `eq_shell_bridge=1` + redirect → `ShellReadySignal` fires `EQ_SERVICE_READY` → Shell reveals iframe.

> ## ⏩ POST-SPRINT UPDATE — 2026-06-09 (v8 design pass + security sprint + Service SSO 4 bugs)
> - **v8 design pass COMPLETE:** All 14 EQ Field screens updated (`styles/field-v8.css` + sidebar, dashboard, leave, timesheets, people, managers, roster, calendar, jobnumbers, apprentices, home, projects, whatsnew). PR #258 squash-merged. Live at eq-solves-field.netlify.app.
> - **EQ Shell v8 warmup COMPLETE:** auth.css, App.css, MobileRecordsDrawer.css, MobileTabBar.css warmed from cool-gray (#F9FAFB) to warm sand (#F6F3EE/#EEECEA). Hub canvas correct. PRs #290 + #293 squash-merged.
> - **Security sprint — ALL S0–S3 DONE:** 5 PRs merged across eq-shell, eq-solves-field, eq-solves-service. All items closed.
> - **EQ Service Shell SSO — 4 bugs fixed (PRs #267–#270):** (1) edge runtime crypto failure — auth logic moved to Node.js API route; (2) wrong redirect hostname — `NEXT_PUBLIC_SITE_URL` used instead of `nextUrl.host`; (3) HMAC key mismatch — `EQ_SESSION_SALT` vs `EQ_SECRET_SALT` aligned; (4) proxy.ts infinite loop — `eq_shell_bridge=1` cookie checked to prevent re-entering SSO. Service deploy `6a27f277`.
> - **Worker identity linker (GATE A) DONE** — PR #278 merged + deployed. Backfill run: 7/39 workers linked, 25 pending invite acceptance (expire 2026-06-15).
> - **WS4 quote-job-consumer DONE** — canonical work-order spine built (`app_data.jobs` now wired).
> - **EQ Field v3.5.119** — JS navy → ink/sky token sweep (5 files). PR #260 merged.

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
- **eq-roles v1.3.0 confirmed merged** — `d0fa143` on main; eq-shell already bumped to consume it (`d58513a`). **Now at v2.3.0** (Sprint 5 — `resolveEffectivePermissions` + C5 split shipped; pull origin/main to get latest).
>
> ## ⏩ POST-SPRINT UPDATE — 2026-06-02 (eq-roles v1.3.0 SHIPPED)
> - **`@eq-solutions/roles` v1.3.0 LIVE** — merged to main, tagged `v1.3.0`, worktree + branch cleaned. Changes shipped: `canAny()` + `canAll()` helpers; 21-test suite (all pass); `package.json` version synced; `prepublishOnly` runs tests; CHANGELOG complete. eq-shell bumped to `#v1.3.0` (commit `d58513a`). **⚠ Now superseded by v2.3.0** (Sprint 5 — C5 split + `resolveEffectivePermissions`; eq-roles main is 1 commit ahead of local).
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
> Last verified: 2026-06-07. Dirty counts reflect `git status --short` output; CRLF noise = line-ending only, no real changes.

| repo | branch (2026-06-07) | dirty | notes |
|------|---------------------|-------|-------|
| **eq-shell** | `claude/worker-linker-schema-fix` | 271 (CRLF noise only) | `.git` repaired 2026-06-07 (config had null bytes; HEAD was truncated). 3 active agent worktrees locked (`wf_f1c4afc6-761-4`, `agent-a3e8cad7de9a023fc`, `agent-a15dd68d59734b633`). Stale unlocked worktrees: `eq-shell-button-wt`, `eq-shell-cleanup-wt`, `eq-shell-w2-wt`, `eq-shell-ocr-wt`. Build: `pnpm run build`. |
| **eq-cards** | `claude/cards-otp-fix-minimal` | 1 (untracked: eq-cards-marketing.html) | clean; safest repo to work in. NOT SKS. |
| **eq-intake** | `revert/intake-matrix-spike` | 0 | upstream gone — dead branch; switch to main before starting new work. |
| **eq-solves-field** | `revert/licence-admin` | 157 (CRLF noise only) | `.git` packed-refs repaired 2026-06-07. Vanilla HTML/JS/CSS; version-stamp every release. |
| **eq-solves-service** | `claude/posthog-canonical-distinct-id` | 0 | 1 commit ahead of origin (unpushed). `npm run check` before push. |
| **eq-roles** | `main` | 0 | 1 commit BEHIND origin — v2.3.0 not pulled yet. `resolveEffectivePermissions` shipped in Sprint 5. No open PRs. |
| **eq-ui** | `claude/component-audit` | 22 (CRLF noise only) | no real changes. |
| **eq-design-tokens** | `main` | 10 (CRLF noise only) | no real changes. Consumed by Shell/Field/Service via git-dep. |
| **sks-nsw-labour** | `claude/sks-field-host` | 5 (untracked) | **sks-nsw-labour.netlify.app = SKS LIVE — DO NOT DEPLOY.** 2 untracked SQL migrations need committing. |
| **eq-context** | `claude/identity-convergence-target-2026-06-04` | 5 | 2 commits ahead of origin; untracked sprint/spec docs need committing. |

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
