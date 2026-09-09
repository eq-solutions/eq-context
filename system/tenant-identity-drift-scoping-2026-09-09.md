---
title: Tenant identity drift — hardcoded lists across the suite (scoping)
owner: Royce Milmlow
last_updated: 2026-09-09
scope: Inventory every place tenant identity (slug/ID) is hardcoded outside the control-plane database, across eq-shell, eq-field, eq-cards, eq-service, and eq-solves-intake. Judge which are completeness gaps vs legitimate variance, and propose which should move to table-backed dynamic sourcing vs. gain a drift-detection check vs. neither. Scoping only — no fixes built here.
read_priority: high
status: live
---

# Tenant identity drift — hardcoded lists across the suite

Asked 2026-09-09 after onboarding Madagins hit the same failure shape four separate times in one
day, in four different repos, via four different mechanisms: `netlify/functions/token-exchange.ts`'s
`ALLOWED_FIELD_TENANT_SLUGS` (eq-shell, silently blocked Field access for hours, fixed in
[eq-shell#1838](https://github.com/eq-solutions/eq-shell/pull/1838)), `TENANT_ROUTES` in
`workers-canonical-sync` (eq-cards, fixed independently the same day in
[eq-cards#348](https://github.com/eq-solutions/eq-cards/pull/348)), `public.tenants`/
`public.organisations` falling out of sync (eq-shell control plane, fixed with a new
`trg_sync_tenants` trigger in [eq-shell#1839](https://github.com/eq-solutions/eq-shell/pull/1839)),
and — found only while scoping this doc, not fixed by anyone today — a schema-provisioning
collision class in eq-field's own migration replay (see [§6.4](#64-concurrent-work-already-in-flight-eq-field-tenant-provision-generator)).
Four independent teams(-of-one) hit the same root cause on the same day and each built a
local fix. This doc is the suite-wide look none of those four had time for.

**Live-verified 2026-09-09** — seven parallel research passes (two over eq-shell's
`netlify/functions/**`, one over eq-shell's `src/**`, one over eq-shell's migrations/scripts/config
plus a read of the reference patterns below, and one each over eq-field, eq-cards, and
eq-solves-intake), each repo re-synced against `origin/main` before searching where safe to do so,
plus a live query against the jvkn control-plane database — not assumed. eq-service (see naming
note in [§4](#4-eq-service)) was also swept. **~40 hardcoded tenant-identity references found
across 6 repos.** Findings and honest gaps below.

---

## 0. Fix now — independent of whatever gets decided below

These aren't waiting on an architecture decision. Three already have a spawned task (all three
started by Royce in separate sessions as of this writing); the rest are flagged here because
spawning more into eq-field right now would collide with the concurrent work in
[§6.4](#64-concurrent-work-already-in-flight-eq-field-tenant-provision-generator).

| # | Repo | Finding | Why it's urgent | Status |
|---|------|---------|------------------|--------|
| 1 | eq-service | `getCanonicalMembers()`/`getCanonicalMemberMap()` default to SKS's roster; ~17 call sites (incl. the pre-visit-brief email cron) never pass a tenant | Silent wrong-tenant data today, not a future risk | Task running: "Fix ~17 eq-service call sites defaulting to SKS's staff roster" |
| 2 | eq-service | SKS's tenant ID hardcoded into 2 RLS `WITH CHECK` policies (`acknowledgments`, `app_config`); true footprint may be larger and isn't fully knowable from the repo | Silent security-layer denial — Postgres just refuses the write, no app error | Task running: "Investigate hardcoded SKS tenant ID in eq-service RLS policies" |
| 3 | eq-cards | 3 comments in the just-merged PR #348 describe "shared DB by default" as a settled decision you explicitly reversed the same session; the tracked follow-up to fix them never landed | Code behavior is already correct — only the comments misdescribe a non-negotiable | Task running: "Fix stale shared-DB-default comments in eq-cards" |
| 4 | eq-field | Apprentice module: an unrecognized tenant falls back to the **pre-fix, unfiltered legacy read** — the exact hole an August security fix closed for SKS. Backwards fail-safe. | Dormant today (only SKS + disposable demo content exist); becomes a real vulnerability the moment a real tenant turns Apprentices on | Not spawned — flagging for your call given 3 active worktrees already in this repo on adjacent code |
| 5 | eq-field | `sites.js`/`managers.js` (~11 sites) gate Shell-canonical-ownership write-protection on the literal string `'sks'`, not "is this tenant Shell-integrated" | A second Shell-integrated tenant gets **full write access** to Field-side sites/managers Shell is supposed to own — a data-corruption path, not just a missing feature | Not spawned — same reason as #4 |
| 6 | eq-shell | `scripts/check-tenant-drift.mjs`'s own `CANONICAL_PROJECTS` list is fixed at 3 entries; an unset project ref is **skipped, not failed** | Madagins' own dedicated Supabase project currently gets **zero** of this script's anon-grant/RLS/policy-lint security checks until someone hand-adds a 4th entry — the security guard has the exact disease it's guarding against. (Independently corroborated: today's live `digest.md` separately flags an active Supabase-advisor RLS gap on madagins's own `app_data._eq_migrations` table — a second, more urgent open security gap on the same project, not fixed by anything in this doc.) | Not spawned — flagging in this doc since it's the clearest single argument for §8's recommendation |

Items 4–6 are written up in full in their repo sections below. I'd suggest reading this doc before
deciding whether to spawn them individually or fold into existing worktrees.

---

## 1. eq-shell

### 1.1 Application code (`netlify/functions/**`, `src/**`)

| # | File:line | Gates | Current contents | Judgment |
|---|-----------|-------|-------------------|----------|
| 1 | [`netlify/functions/token-exchange.ts:42`](https://github.com/eq-solutions/eq-shell/blob/main/netlify/functions/token-exchange.ts#L42) `ALLOWED_FIELD_TENANT_SLUGS` | Which slugs may mint a Field/Service Supabase JWT | `['eq','demo-trades','melbourne','sks','madagins']` (now fixed) | **Completeness gap, strongest table-backed candidate in the sweep.** The same function already reads `field_tenant_slug` and a dynamic entitlement check (`isModuleEnabledForTenant`) *before* this array is consulted — the array is a redundant second, static gate on facts already sourced dynamically. |
| 2 | [`netlify/functions/_shared/tenant-routing.ts:389`](https://github.com/eq-solutions/eq-shell/blob/main/netlify/functions/_shared/tenant-routing.ts#L389) `KNOWN_TENANT_SLUGS` | Which tenants' Supabase clients get pre-warmed | `['sks','eq','madagins']` — currently missing `demo-trades`, `melbourne` | Completeness gap, but the file's own comment documents this as latency-only (a stale entry costs one cold-start), not correctness. Lower urgency than #1. |
| 3 | [`netlify/functions/mint-tenant-jwt.ts:140`](https://github.com/eq-solutions/eq-shell/blob/main/netlify/functions/mint-tenant-jwt.ts#L140), [`tenant-data-proxy.ts:171`](https://github.com/eq-solutions/eq-shell/blob/main/netlify/functions/tenant-data-proxy.ts#L171), `mint-sks-jwt.ts` | Which JWT secret signs the tenant data-plane token | `if (tenant_slug === 'sks')` × 2, plus a whole dedicated endpoint | **Legitimately varies** — both comments explicitly call it transitional ("drop once ehow's secret is aligned"). But the fact is hand-copied into 3 places with no shared home. Recommend a `getJwtSecretForTenant(slug)` helper so retirement is a one-line change, not a 3-file audit. |
| 4 | [`netlify/functions/quotes-expiry-scheduler.ts:32`](https://github.com/eq-solutions/eq-shell/blob/main/netlify/functions/quotes-expiry-scheduler.ts#L32), `quotes-auto-archive-scheduler.ts:34`, `quote-job-consumer-scheduler.ts:70`, `licence-expiry-scheduler.ts:695` | Which tenants each scheduled job runs against | `SCHEDULER_TENANT_SLUGS` env var used with **two different meanings**: the first three treat unset as "sks only" (`?? 'sks'`); `licence-expiry-scheduler.ts` treats it as an optional *filter* on a dynamic "every active tenant" query. `quote-job-consumer-scheduler.ts` additionally uses a third, different env var (`QUOTE_JOB_TENANTS`) for the same purpose. | **Mixed — and the sharpest concrete risk in eq-shell.** If `SCHEDULER_TENANT_SLUGS` is ever set for one purpose, it silently also restricts the other two. `licence-expiry-scheduler.ts` already has the correct reference pattern (dynamic discovery + optional override); the fix for the other three is "adopt that function," not invent one. |
| 5 | [`netlify/functions/comms-jobs.ts:25`](https://github.com/eq-solutions/eq-shell/blob/main/netlify/functions/comms-jobs.ts#L25) (×3), `comms-weekly-digest.ts:37` (×2) `SKS_TENANT_ID` | Fast-fails non-SKS sessions (`comms-jobs.ts`); targets the Monday NSW-ops digest (`comms-weekly-digest.ts`) | Literal `'7dee117c-98bd-4d39-af8c-2c81d02a1e85'`, duplicated verbatim | **Legitimately varies** — both self-documented as bespoke SKS-only features, no ambiguity. Only note: raw UUID, not slug, so it won't surface in a future `grep 'sks'` sweep. |
| 6 | [`netlify/functions/_shared/slug.ts:12-15`](https://github.com/eq-solutions/eq-shell/blob/main/netlify/functions/_shared/slug.ts#L12) `RESERVED_SLUGS` | Previews/rejects a colliding slug before a self-serve invite link issues | Mixes generic system routes with 2 stale tenant slugs (`eq`,`sks`) — missing `madagins`, `demo-trades`, `melbourne` | Low-severity completeness gap — the file's own header names the real gate as a SQL twin (`shell_control.provision_tenant()`), so staleness here degrades UX (a wasted OTP on redemption) rather than creating a duplicate tenant. |
| 7 | [`src/pages/AdminTenantSettings.tsx:977-981`](https://github.com/eq-solutions/eq-shell/blob/main/src/pages/AdminTenantSettings.tsx#L977) | Platform-admin "default Field workspace" picker | `sks`, `eq`, `demo-trades`, `melbourne` — missing `madagins` | **A 4th live, unfixed sibling of the original bug — not caught by PR #1838.** Introduced [PR #395](https://github.com/eq-solutions/eq-shell/pull/395) (2026-06-16), three months before today's incident. Doesn't import `fieldTenants.ts` at all — a fully independent literal copy. Narrow blast radius (admin-only setting) is likely why it's gone unnoticed this long. |
| 8 | [`src/modules/quotes/QuotesModule.tsx:4036`](https://github.com/eq-solutions/eq-shell/blob/main/src/modules/quotes/QuotesModule.tsx#L4036) | Portal-share-link tenant segment, fallback only | `?? 'sks'` | Different shape (single literal fallback, not a list) but the same root cause. Low trigger probability — the component is always mounted under a `/:tenantSlug/...` route — but a wrong tenant slug in a copied share link is a real failure mode if it ever does trigger. |
| — | `_shared/token.ts:266-269` | Comment only, no live gate | JSDoc names only 3 of the now-5 valid slugs | Not a live gate — the whole code path is already dead, retained only until `EQ_SECRET_SALT` retires. Worth one line as an in-the-wild illustration of "two homes, one fact," but the fix is deletion alongside the rest of the dead code. |

**Checked and confirmed clean:** `tenant-context.ts`, `tenant-resolution.ts`, `tenant-membership.ts`,
`admin-tenants.ts`, `provision-tenant-background.ts`, `shell-provision-tenant.ts`,
`canonical-api.ts`, `canonical-events.ts`, five background jobs, `TenantPicker.tsx`,
`TenantSwitcher.tsx`, `brand.tsx`, `session.ts`'s `TenantConfig.feature_flags` (a good example of
the *legitimate*-variance pattern done correctly — DB-driven per-tenant flags, not a hardcoded
list). No JSON config, no Zod enum, no TS string-literal union anywhere in `src/**`.

### 1.2 Infrastructure, migrations, config

| # | File:line | Gates | Judgment |
|---|-----------|-------|----------|
| 9 | [`scripts/check-tenant-drift.mjs:732-748`](https://github.com/eq-solutions/eq-shell/blob/main/scripts/check-tenant-drift.mjs#L732) `CANONICAL_PROJECTS` | Which Supabase projects get CHECK 2/7/8/9/10 (anon-grant, view-security-invoker, sensitive-column-grant, stacked-permissive-policy, intentional-anon-read) — most of this file's *security* checks | **Completeness gap, in a security tool.** Fixed at exactly 3 entries (`CONTROL_PROJECT_REF`, `CANONICAL_INTERNAL_PROJECT_REF`, `SKS_CANONICAL_PROJECT_REF`). An unset ref is logged and skipped, not failed. Madagins' own dedicated project (`ornndtbdkxfsewspbrwk`) gets none of these checks until a human adds a 4th `{envKey, ref, label}` entry and a matching CI secret. See [§0](#0-fix-now--independent-of-whatever-gets-decided-below) item 6. |
| 10 | `.env.example:141-147` `SCHEDULER_TENANT_SLUGS`/`QUOTE_JOB_TENANTS` | Documents the vars from finding #4 | Confirms the semantic collision isn't even visible from the repo — the actual values live only in the Netlify dashboard. |
| 11 | `netlify.toml:76` CSP `connect-src`/`img-src` | Which Supabase-project hostnames the **browser** may open a connection to | Completeness gap, confirmed real (not theoretical): `src/lib/sksSupabaseClient.ts` already has the browser creating a direct connection to `ehow` today. A new tenant needing the same pattern is silently CSP-blocked — no thrown error, just a dead-looking network layer. `img-src` is narrower still (only the control-plane project). |
| 12 | [`supabase/migrations/2026_05_28_field_tenant_slug.sql:18-25`](https://github.com/eq-solutions/eq-shell/blob/main/supabase/migrations/2026_05_28_field_tenant_slug.sql#L18) | DB `CHECK` constraint on `shell_control.tenants.field_tenant_slug` | **A 4th independent instance of the exact "known Field slugs" concept** PR #1838 fixed in 3 app-code places — this one's at the schema level, never touched, never widened since 2026-05-28. Setting it to `'madagins'` today hard-fails with a Postgres constraint violation. Loud, at least — but still a miss nobody thought to grep for. |
| 13 | `scripts/sync-field-to-canonical.mjs`, `sync-quotes-to-canonical.mjs`, `sync-service-to-canonical.mjs` | One-shot cutover scripts | Hardcode SKS's tenant ID, one with the explicit comment "hardcoded — update if tenants change." Legitimately historical/one-shot (eq-quotes is retired) — same texture as the bug class, not urgent. |
| 14 | [`supabase/migrations/0257_close_sec30_32_both_planes.sql:59-111`](https://github.com/eq-solutions/eq-shell/blob/main/supabase/migrations/0257_close_sec30_32_both_planes.sql#L59) | A fleet-wide security fix (SEC-30/32) | Branches on exactly 2 known policy "shapes" (zaap, ehow org IDs), asserted at the end via `RAISE EXCEPTION` if neither shape is found. The migration's own header scoped this to "only 3 orgs exist" as of 2026-08-21 — already stale. **Flagging the pattern, not asserting a break** — I can't confirm from the repo alone whether this migration succeeded, no-opped, or hit its own exception against Madagins' plane. Worth a live check. |

**Checked and confirmed clean/legitimate:** the reserved-slug blocklist duplicated across 5
`provision_tenant` RPC migrations (opposite purpose — a signup-collision blocklist, correctly
includes `eq`/`sks`), `check-tenant-drift.mjs`'s other allowlists (`INTENTIONAL_ANON_READS` etc. —
legitimately scoped security-debt lists that fail *safe*, not open), and `shell_control.app_tenant_scope`
missing a `('field','madagins')` row (**not a bug** — `docs/runbooks/add-field-trial-tenant.md`
explicitly documents this as intentional until a separate piece of work lands).

---

## 2. eq-field

**The worst offender in the sweep — at least 13 distinct findings across 5 different mechanisms**,
not one list forgotten in three places. `madagins` doesn't appear anywhere in this repo yet, so
nothing has broken *for it* here specifically — but any new tenant hits every gap below in
sequence the moment it gets Field access.

| # | File:line | Gates | Judgment |
|---|-----------|-------|----------|
| 15 | `netlify.toml:110`, `_headers:23` (2 synced copies) | CSP `connect-src` Supabase-hostname allowlist | **Highest real-world severity found in eq-field.** Same shape as eq-shell #11, but eq-field's own header comment is *already* self-aware of the risk ("add its origin here AND to the analytics.js/supabase.js call sites — don't silently rely on report-only mode") — the fix this doc proposes is already informal tribal knowledge here, just not enforced. |
| 16 | `netlify/functions/verify-pin.js:161-172` `DATA_TENANT_IDS` | Slug→`tenant_id` map for minting a data-plane JWT | Completeness gap. Fails closed at least (`tenant-not-provisioned`), extendable via `DATA_TENANT_IDS_JSON` env override. |
| 17 | `netlify/functions/verify-pin.js:118-129` `TENANT_JWT_SECRETS` | Slug→signing-secret map | Legitimately varies (a secret can't be canonical-sourced the same way) — but the *mechanism* to add one is manual and separate from #16. |
| 18 | `verify-pin.js:72-80` **and** `eq-agent.js:27-35` `AUDIT_ORG_BY_TENANT` | Which canonical `org_id` an audit-log row is stamped with | **Duplicated, not shared — hand-copied.** Get it wrong and the row still writes (service-role bypasses RLS) but is invisible in the Audit view — this exact failure already cost SKS "600+ login events" per the file's own comment history. |
| 19 | `verify-pin.js:189-195` `CORE_ONLY_TENANTS` | Server-side enforcement of "this tenant's PIN gate is disabled, use Shell" | Mixed — a hardcoded mirror of a value that already lives dynamically in canonical (`organisations.branding.coreOnly`). Real drift risk (two sources of truth for one boolean) but fails toward the safer branch. |
| 20 | `verify-pin.js:267-273` `ORIGIN_TENANT_MAP` | Rate-limit bucketing + PIN-gate fail path | Completeness gap, but **fails closed** — an unlisted origin gets a flat refusal, not a misroute. Safest-failing item in the set, still untracked. |
| 21 | 5 independent `ALLOWED_ORIGINS` CORS arrays (`_shared/cors.js`, `eq-agent.js`, `send-email.js`, `tenant-config.js`, `eq-service-sites.js`) | CORS per function | Confirmed inconsistent. `eq-agent.js` is a confirmed live gap — missing `field.eq.solutions` entirely, still lists the retired `eq-solves-field.netlify.app` — currently dormant only because the client-side "EQ Agent" chat is CSS-hidden. `_shared/cors.js` exists precisely because this drift class was already found and fixed once (2026-08-18); 4 functions still don't use it. |
| 22 | ~30 scattered `=== 'sks'` / `!== 'sks'` literals across 16 files, no central list at all | See breakdown below | Worse than a list in one sense — nothing to even audit. |
| 23 | `netlify/functions/apprentice-data.js:22-28`, `apprentice-write.js:468` | Apprentice module tenant scope | **Security regression waiting to trigger** — see [§0](#0-fix-now--independent-of-whatever-gets-decided-below) item 4. |
| 24 | `scripts/analytics.js:32-59` vs `scripts/core-bundle-a1.js:296-323` `_ANALYTICS_CONFIG` | Analytics init keys per tenant | Hand-duplicated, **but already has a proven CI drift-gate** (`build-bundles-drift.yml`, caught 3 real cases on 2026-08-06). Good precedent — though it only checks the two copies agree with each other, not that either is complete. |
| 25 | ~30+ SQL migrations hardcoding SKS's UUID directly into RLS predicates | Historical schema authorship | **Structurally different — not a list that drifts.** See [§6.4](#64-concurrent-work-already-in-flight-eq-field-tenant-provision-generator): already being addressed by a dedicated generator tool, not this doc's recommendation. |
| 26 | `migrations/2026-05-31_canonical_tenant_registry.sql` | — | **The strongest positive precedent in the whole sweep.** See [§6.3](#63-eq-fields-own-precedent-canonical_tenant_registry). |
| 27 | `scripts/app-state.js:970` `earlyBootBranding()` | First-paint branding before the real canonical fetch resolves | Low severity, self-healing — flashes wrong branding for &lt;500ms then corrects. Not worth prioritizing. |

**Finding #22 breakdown — three sub-patterns, not one:**

- **Architecture-ownership checks, wrongly keyed** (`sites.js` ×6, `managers.js` ×5) — see
  [§0](#0-fix-now--independent-of-whatever-gets-decided-below) item 5. The real rule ("Shell owns
  canonical sites/staff for canonical-integrated tenants") applies to *any* Shell-integrated
  tenant; today it's equivalent to `=== 'sks'` only because SKS is currently the only one.
- **Schema-availability checks, legitimately per-tenant but keyed on identity instead of capability**
  (`realtime.js`, `tender-pipeline.js`, `supabase.js:675`, `app-state.js:668`) — comments like "SKS
  doesn't have the pipeline tables yet" describe a real, currently-true fact, just expressed as "is
  this literally sks" instead of "does this tenant's schema have table X." A new tenant's actual
  capability is never consulted.
- **Auth-model / cosmetic** (`people.js:1113`, `trial-dashboard.js`) — low stakes, narrow and
  genuinely SKS-specific (PIN management isn't used by Shell-auth tenants) or purely cosmetic.
  Reasonable to leave as-is.

### 6.3 eq-field's own precedent: `canonical_tenant_registry`

`migrations/2026-05-31_canonical_tenant_registry.sql`'s own header states its purpose in almost the
exact words of this doc's question: *"turn EQ Field's per-tenant config from hardcoded JS maps
(`TENANT_SUPABASE`/`TENANT_BRANDING`/`TENANT_DISABLED_TABLES`) into a canonical, anon-readable
registry so the PWA can boot tenant-agnostically."* Confirmed live: those three JS objects are
**gone** from `scripts/app-state.js` today — only stale comments referencing the old names remain.
The replacement, `netlify/functions/tenant-config.js`, queries canonical per-request with **zero
hardcoded tenant list** — the only hardcode left is a single `STANDALONE_DEFAULT_SLUG = 'eq'`
sentinel for the no-token case. `TENANT_DISABLED_TABLES` is likewise computed live from canonical
`module_entitlements` now.

**This is the single strongest piece of evidence that the fix this doc is scoping already works,
in this exact codebase.** It's just applied to one config surface (routing) and not the other five
(§2's findings 15–21).

---

## 3. eq-cards

Reachable, working tree clean, HEAD fast-forwarded to current `main` during the search.

| # | File:line | Judgment |
|---|-----------|----------|
| 28 | [`supabase/functions/workers-canonical-sync/index.ts:11,17`](https://github.com/eq-solutions/eq-cards/blob/main/supabase/functions/workers-canonical-sync/index.ts#L11) `SKS_TENANT_ID`/`SKS_ORG_ID` | **Now a legitimate, deliberate default, not a completeness gap.** This is what's *left* after [PR #348](https://github.com/eq-solutions/eq-cards/pull/348) removed the actual bug — a hardcoded `TENANT_ROUTES` map that needed a new entry per tenant, flagged as a risk 2026-07-10, and broke exactly that way when Madagins onboarded today. Post-fix, `resolveTenantRoute()` reads `organisations.tenant_id` live — a new shared-ehow tenant needs zero code changes here now. The remaining constants are only the fallback for a worker with no `origin_org_id` stamped (self-signup majority case) — worth a conscious call on whether "unstamped = SKS" should be permanent, but it will not silently break on tenant #3. |
| — | 2 point-in-time data-repair migrations, 1 no-op historical migration, `supabase/seed.sql` (local dev only) | Inert/historical — zero ongoing effect. |

**Self-signup/claim flow (explicitly checked, all four entry points): clean.** Company-picker,
invite-claim, tenant-provision, and agency intake are all dynamic/token-driven, no hardcoded org
list anywhere in the Flutter app.

**Also found, spun off separately (not a tenant-list finding):** see [§0](#0-fix-now--independent-of-whatever-gets-decided-below)
item 3 — stale comments in the same PR describing a database-sharing policy you explicitly reversed
the same session.

---

## 4. eq-service

**Naming note:** the path in eq-context's own repo map, `eq-solves-service`, no longer exists on
disk — the live checkout is `eq-service` (confirmed via `git remote`, `package.json`, and — even
the repo's own `CLAUDE.md` has a stale path line pointing at the old name directly above its
correct git-remote line one row below). The planned rename eq-context still describes as pending
has already happened in reality. Minor, not spawning a task over one stale path reference — noting
here so the next person doesn't lose time on it.

| # | File:line | Judgment |
|---|-----------|----------|
| 29 | `lib/canonical-sync.ts:24`, `canonical-outbox.ts:35`, `lib/canonical-members.ts:35` `CANONICAL_TENANT_SLUG` default | **Completeness gap — see [§0](#0-fix-now--independent-of-whatever-gets-decided-below) item 1.** `canonical-outbox.ts`'s drain has no tenant filter at all and stamps every pending row with one hardcoded tenant. |
| 30 | ~17 call sites passing no tenant to `getCanonicalMembers()`/`getCanonicalMemberMap()` | Same as above — silently resolve to SKS's roster. Proven an oversight, not a design choice: `defects/page.tsx` already has `tenantId` in scope 2 lines above the broken call. |
| 31 | `supabase/migrations/0146b_...sql:36`, `0151_...sql:46` | **See [§0](#0-fix-now--independent-of-whatever-gets-decided-below) item 2.** SKS's tenant ID hardcoded directly into RLS `WITH CHECK` clauses — silent write denial for every other tenant. |
| 32 | `lib/utils/demo.ts:13` `DEMO_TENANT_ID` | **Legitimate variance, textbook case.** Self-documented public fixture, matches the demo-vs-prod carve-out exactly. Only nit: `scripts/seed-demo-attachments.ts:35` redeclares the same literal instead of importing the shared constant — dev-script-only duplication. |
| — | 3 migrations referencing a tenant ID on the deleted `urjh` project | Historical, no ongoing code path reads these. |

**Checked and confirmed clean:** no hardcoded array/switch anywhere in app code (unlike eq-shell's
`fieldTenants.ts` pattern), the tenant-provisioning API, and all 5 real `exceljs` importers.
**The Shell↔Service session handoff is a genuinely good reference pattern** — resolves tenant
identity dynamically from the incoming JWT against the live `tenants` table on every request, and
fails closed (403) on an unresolved slug. `lib/tenant/getTenantSettings.ts`'s module-toggle columns
(`calendar_enabled`, `defects_enabled`, etc.) are exactly the legitimate-variance pattern this doc
is trying to distinguish from a gap.

---

## 5. eq-solves-intake

Reachable, clean tree, fully current against `origin/main`.

| # | File:line | Judgment |
|---|-----------|----------|
| 33 | `eq-platform/packages/eq-intake-demo/src/module/{IntakeModule,ReconcileModule,IntakeHealthHome,EntityDrillDown}.tsx` (4 files) | **Same shape as the eq-shell incident, via a missing prop instead of a missing array entry.** `IntakeModule` is confirmed the real production entry point (its own barrel: "the production deployment lives inside the shell, which imports from here"). `tenantId` is optional; when the shell fails to pass it, these components fall back to a hardcoded "fixture tenant" UUID (`00000000-0000-4000-8000-000000000001`) and keep running — real reads and writes — against it, with only a soft `console.warn` in 2 of 4 sites. If eq-shell ever fails to pass `tenantId` (missing env var, a mount-order race, a bug), this silently reads/writes the wrong tenant instead of failing loudly. |
| 34 | `quick-export/destinations.ts:96` | Minor — CSV export company-name fallback defaults to "SKS Technologies." Low blast radius, worth a one-line fix, not scoping-doc weight. |
| 35 | Per-tenant Supabase project deployment (SQL/cron/edge functions hardcoding project ref `ehowgjardagevnrluult`) | **A structurally different failure class, same root cause.** Legitimate given the "dedicated project per tenant" rule — there's no single running instance branching on tenant identity — but nothing in-repo or in CI tracks which tenants have which pieces deployed. The infra-layer counterpart to eq-field's schema-provisioning gap ([§6.4](#64-concurrent-work-already-in-flight-eq-field-tenant-provision-generator)). |

**No `TENANTS = [...]` array, no switch/if-chain on tenant identity, no JSON tenant registry
anywhere in the repo.** And genuinely good reference patterns worth generalizing from: `eq_quality_list_tenants()`
derives its tenant list live from data specifically "to avoid depending on a tenant registry
table"; `read-entity-columns.ts` uses a try-new-RPC-then-fallback pattern instead of a "which
tenants have this" list; tenant identity is always resolved from the caller's JWT, never a
hardcoded map; `tenant-app-config.schema.json` is a proper one-row-per-tenant data table instead of
code branches; `scripts/test-cross-tenant-rls.mjs` is an actual automated cross-tenant isolation
smoke test.

---

## 6. Existing proven patterns (what to model the fix on)

### 6.1 `shell_control.app_tenant_scope` — the table-backed pattern, verified mechanics

Schema (`supabase/migrations/2026_07_04_app_tenant_scope.sql`): `app text`, `tenant_slug text`
(`'*'` = every tenant), `created_at`, `PRIMARY KEY (app, tenant_slug)`, RLS enabled with no
policies — service-role only via an explicit grant. Seeded: `cards`/`service`/`quotes`/`shell` →
`'*'`; `field` → `eq, sks, demo-trades, melbourne` (a live example of legitimate per-tenant
variance already being table-backed, not hardcoded — see [§9](#9-source-of-truth) for why that
seed list matters to this doc's own recommendation).

Query mechanism (`canonical-api.ts`'s `appMayReachTenant()`): cached only for the lifetime of one
Lambda invocation — a fresh invocation always re-reads, so a control-plane data edit takes effect
on the **next request, no deploy.** Fails **closed** on a query error (403), no fallback to any old
hardcoded map.

This replaced a hardcoded `APP_TENANT_SCOPE` map that used to live directly in `canonical-api.ts` —
exactly the precedent this doc's brief named, now with full mechanics confirmed live.

### 6.2 The two existing drift-check scripts — verified mechanics

**`scripts/check-control-plane-drift.mjs`** — repo-side source of truth is every `.sql` file under
`supabase/migrations/` (control plane only), regex-scanned for `CREATE [OR REPLACE] FUNCTION`/
`CREATE TABLE` statements (existence only, not signature/body). Live side is jvkn via the
Management API — functions across `public`+`shell_control`; tables in `shell_control` **only**
(deliberately narrower — a first pass including `public` found 34 unsourced tables, punted to a
separate, unreviewed project). "Drift" = a live object with no matching `CREATE` anywhere in
tracked migrations. `KNOWN_UNSOURCED` is a curated accepted-debt allowlist, each entry with a full
paper trail. Wired into `.github/workflows/tenant-drift.yml` on every PR to `main`, a 3-hourly
schedule, and manual dispatch — no `continue-on-error`, a required check.

**Important nuance for §9:** `--strict` only gates the *function* side. The *table* side is
informational-only regardless of the flag — there's no `--strict-tables` option yet.

**`scripts/check-provisioning-completeness.mjs`** — written **today** (2026-09-09), directly
motivated by Madagins' own provisioning failing twice for reasons invisible from source (`pg_cron`
never enabled by any tracked step; ~37 `public`-schema tables on `ehow` predating the tracked
migration system). Source of truth: tracked = union of `supabase/tenant-migrations/*.sql`
(respecting `-- Plane:` header exclusions) + a plain-text scan of `provision-tenant-background.ts`
+ fixed platform-scaffolding baselines. Live = **one reference tenant only** (`ehow`/SKS by
default, `--ref` override) — deliberately narrower than `check-control-plane-drift.mjs`'s
cross-tenant diff.

**Why informational, not blocking — a CI-wiring choice, not a script limitation.** The script
supports `--strict` identically to its sibling; the workflow simply never passes it, because — per
the workflow's own comment — there's no clean baseline yet: the first live run already surfaced
real, untriaged gaps. This is the exact same "reconcile to zero, then flip the switch" sequencing
`check-control-plane-drift.mjs` went through on 2026-07-27, just not done yet here.

### 6.3 eq-field's own precedent: `canonical_tenant_registry`

Covered in full at [§2](#2-eq-field) — the strongest positive evidence in the sweep that this
fix pattern already works end-to-end in this exact codebase.

### 6.4 Concurrent work already in flight: eq-field tenant-provision generator

Three active worktrees exist in eq-field right now (`claude/tenant-provision-generator`,
`claude/tenant-provision-hardening`, `claude/tenant-provision-prereq-ddl` — the latter two at the
same HEAD, no open PR yet on any of them as of this writing). **Verified no overlap with this
doc's core recommendation:** the tool (`scripts/generate-tenant-provision-sql.mjs`) generates the
DDL to provision a *new* tenant's dedicated Supabase project by replaying eq-field's ~77 migrations
with literal UUID substitution — the fix for finding #25 (hand-pasted-UUID RLS migrations)
specifically, not for the runtime app-code lists in §2's findings 15–21. The `verify-pin.js` diff
in that branch is an unrelated cleanup (role-string literals → canonical constants).

Worth citing regardless: the tool's own dev log already reaches this doc's conclusion
independently — *"this hardens the generator against symptoms, not the root cause — it doesn't
explain or fix WHY two independent, both-legitimate provisioning paths disagree on org_id vs
tenant_id scoping... if this keeps happening on future tenants, the real fix is coordinating the
two provisioning paths, not an ever-growing pile of runtime checks. Flagged, not fixed here."* A
fourth independent surface of today's Madagins incident — schema-provisioning collisions — found
the same day, same root cause, already on record as unresolved. **Recommend not duplicating this
effort** — extend it (or coordinate with whoever's driving it) for eq-service's RLS-policy finding
(§0 item 2) once its footprint is known, rather than building a second generator.

---

## 7. Live tenant-identity data model on jvkn (verified 2026-09-09)

The task brief that kicked off this doc named `public.tenants` vs `public.organisations` as the two
tables to pick between. Live inspection found the real picture has four tables across two schemas,
not two:

| Table | Schema | Role |
|-------|--------|------|
| `organisations` | `public` | Client/browser-facing — richest record: `branding` (jsonb), `hostname`, `supabase_url`/`supabase_anon_key` for direct-browser connections, `tier`, `accepts_applications` |
| `tenants` | `public` | Slim public lookup: `slug`, `name`, `status` |
| `tenants` | `shell_control` | Server-side operational record — `supabase_project_ref`, `active`, `tier`, `field_org_id`, `field_tenant_slug`, `pipeline_url`/`pipeline_api_key`, `is_personal`, `brief_recipients`. **This is what nearly every server-side gating decision found in this sweep already reads.** |
| `tenant_routing` | `shell_control` | Encrypted infra credentials + provisioning status (`supabase_url`, `service_role_key_ciphertext`/`iv`/`tag`, a `status` enum, `provisioned_at`) |

`trg_sync_tenants` (added in PR #1839) fires `AFTER INSERT OR DELETE OR UPDATE ON public.organisations`
and calls `eq_canonical_sync_tenants()` — i.e. **`organisations` is the write-authoritative side of
the public-schema pair; `public.tenants` is a derived mirror.** The trigger only covers this one
pair. It does **not** touch `shell_control.tenants` or `tenant_routing` at all — a gap between the
public-schema pair and the shell_control pair is a drift surface this trigger doesn't address,
worth naming even though nothing found in this sweep currently depends on it.

**Live snapshot, slug alignment across all three slug-bearing tables today:**

| Slug | `organisations` | `public.tenants` | `shell_control.tenants` |
|------|:---:|:---:|:---:|
| `eq` | ✓ | ✓ | ✓ |
| `sks` | ✓ | ✓ | ✓ |
| `madagins` | ✓ | ✓ | ✓ |
| `favour-perfect` | ✓ | — | ✓ |
| `demo-trades` | — | ✓ | — |
| `melbourne` | — | ✓ | — |
| `__personal__` | — | — | ✓ |

Real tenants (`eq`, `sks`, `madagins`) are fully aligned across all three today. `favour-perfect`
(suspended, per `suite-state.md`) is present in `organisations`/`shell_control.tenants` but absent
from `public.tenants` — worth a footnote to confirm that's intentional (a `status` column exists on
`public.tenants` that could hold `'suspended'` instead of the row being absent; not independently
confirmed which). `demo-trades`/`melbourne` are the clearest finding here: they exist **only** in
`public.tenants`, in neither `organisations` nor `shell_control.tenants` — strong evidence (see
`AdminTenantSettings.tsx`'s picker, [§1.1](#11-application-code-netlifyfunctions-src) finding #7)
that these are Field-side demo/trial **workspaces**, not real tenants at all. `__personal__` exists
only in `shell_control.tenants` — an internal sentinel, correctly absent from both client-facing
tables.

---

## 8. Which treatment for which category

| Category | What it means | Fits |
|---|---|---|
| **A — Table-backed dynamic sourcing** | Server-side code with existing DB access reads the tenant table directly (cached per-invocation, `app_tenant_scope`'s pattern) instead of a hardcoded array | `token-exchange.ts` #1, `tenant-routing.ts` #2, `AdminTenantSettings.tsx` #7 (has DB access, admin-only), eq-field's `DATA_TENANT_IDS`/`AUDIT_ORG_BY_TENANT`/`CORE_ONLY_TENANTS`/`ORIGIN_TENANT_MAP` #16–20, eq-service's `CANONICAL_TENANT_SLUG` default #29–30. Same pattern that already replaced eq-field's `TENANT_SUPABASE`/`TENANT_BRANDING` maps ([§6.3](#63-eq-fields-own-precedent-canonical_tenant_registry)). |
| **B — Drift-detection check** | Can't easily go dynamic (static HTTP-header config, a DB `CHECK` constraint, build-time values) but completeness still matters — compare against live truth in CI, modeled on §6.2 | Both CSP `connect-src` allowlists (#11, #15), the `field_tenant_slug` DB constraint (#12), `check-tenant-drift.mjs`'s own `CANONICAL_PROJECTS` (#9 — yes, the checker needs checking), `RESERVED_SLUGS` (#6), the CORS-array family (#21, once consolidated onto `_shared/cors.js`) |
| **C — Schema/codegen tooling** | Not a registry-lookup problem — a "generate correct new artifacts for a new tenant" problem | The ~30+ hardcoded-UUID RLS migrations (#25, #35) — already underway via eq-field's generator ([§6.4](#64-concurrent-work-already-in-flight-eq-field-tenant-provision-generator)); recommend extending that tool's approach rather than building a second one |
| **D — Leave as-is** | Genuinely legitimate variance, or low-value/historical | `TENANT_JWT_SECRETS` #17 (a real secret, can't be table-sourced the same way — revisit only if it becomes a maintenance pain), `comms-jobs.ts`/`comms-weekly-digest.ts` #5 (bespoke SKS features), `sync-*-to-canonical.mjs` #13 (historical one-shot tools), demo tenant IDs (#32 and eq-cards/eq-solves-intake equivalents) |
| **E — Fix now** | Independent of the above | [§0](#0-fix-now--independent-of-whatever-gets-decided-below) |

**Tradeoffs, A vs B:** Table-backed sourcing removes the drift risk entirely (nothing to keep in
sync) but costs a DB round-trip and only works where the consuming code already has service-role
DB access — true for every server-side item above. Drift-checking is cheaper to add and works
anywhere (static config included) but never actually closes the gap between onboarding a tenant and
the check next running — it converts a silent failure into a loud CI failure, which is strictly
better but still requires a human to act on the finding. Where both are possible (nearly everything
in Category A), prefer A; reserve B for the genuinely-can't-go-dynamic cases in Category B above.

---

## 9. Source of truth

**For "does tenant X exist and is it real" — `shell_control.tenants WHERE active = true AND
is_personal = false`.** This is already what the one correctly-built consumer
(`licence-expiry-scheduler.ts`) uses, and [§7](#7-live-tenant-identity-data-model-on-jvkn-verified-2026-09-09)'s
live snapshot confirms it's the table nearly every other server-side gating decision in this sweep
already reads — not `public.tenants` (confirmed today to have inconsistent membership: missing
`favour-perfect`, includes two non-tenant pseudo-slugs) and not `organisations` alone (aligned with
`shell_control.tenants` for real tenants today, but it's the client-facing mirror, not the
operational source).

**Exception — Field-specific checks need one more input.** `demo-trades`/`melbourne` are real,
legitimate entries in `ALLOWED_FIELD_TENANT_SLUGS` (finding #1) but aren't rows in
`shell_control.tenants` at all — per [§7](#7-live-tenant-identity-data-model-on-jvkn-verified-2026-09-09),
the evidence points to these being Field demo/trial workspaces, not tenants. A Field-specific
completeness check should be: `shell_control.tenants.field_tenant_slug` (for real tenants) **UNION**
a small, explicitly-named static set of demo-workspace slugs — not a blind "every tenant must
appear" rule. This is exactly the nuance the original brief asked not to assume past.

**For anything needing browser-facing connection info** (CSP allowlist entries specifically need
`supabase_url`/hostname) — **`public.organisations`**, which is the write-authoritative side of the
now-synced public pair.

**What "drift" means, concretely, per category:**
- *Category A items, post-migration:* nothing ongoing — they read live truth directly, no separate
  check needed.
- *Category B items:* canonical set = query above (± the Field exception); drift = a slug in the
  canonical set absent from the static list (the common case — a new tenant missed) **or** a slug
  in the static list with no matching active tenant (a stale/removed entry — check both
  directions, since `favour-perfect`'s suspension is exactly this in reverse).

**Blocking or informational to start?** **Informational first, unconditionally.** This sweep found
~40 findings across 6 repos on its first pass — a bigger first run than either existing script had.
`check-provisioning-completeness.mjs` shipped informational-only for exactly this reason ("no clean
baseline yet... enforce once triaged"), and `check-control-plane-drift.mjs` only went `--strict`
after its own 2026-07-27 baseline exercise reconciled 111 pre-existing entries down to zero. Follow
the same sequencing: ship informational, triage every finding above into a `KNOWN_INCOMPLETE`-style
allowlist (this doc has effectively already done that triage — Category D findings are the
allowlist's first draft), then flip to `--strict` once a clean run is achieved.

**Sketch of the check itself:** rather than building a generic parser for every config format,
split by how cheaply each list's current members can be read:
- **The TypeScript/JS array-literal cases** (`ALLOWED_FIELD_TENANT_SLUGS`, `KNOWN_TENANT_SLUGS`,
  `RESERVED_SLUGS`, and Category A items not yet migrated) can be imported and read directly at
  Node runtime — no regex parsing needed, same trick `check-control-plane-drift.mjs` doesn't use
  but could.
- **The handful of non-JS cases** (2 CSP configs, 1 DB `CHECK` constraint, 2 env vars) are few
  enough to hand-write one small check each rather than build a generic format parser.
- Reuse `check-control-plane-drift.mjs`'s existing conventions directly: the `KNOWN_*` accepted-debt
  allowlist shape, the `--strict` flag, the JSON `--output-file` option, and the same
  `tenant-drift.yml` workflow (new step, not a new workflow).

---

## 10. Effort estimate

| Piece | Estimate | Notes |
|---|---|---|
| §0 immediate fixes (3 running + 3 flagged) | Hours each, ~2–3 days total if all six are picked up | Independent of everything below; already individually scoped |
| Category A migrations (~10 call sites across eq-shell, eq-field, eq-service) | 2–4 days | Mechanical once the pattern's proven — swap a hardcoded array for a cached `app_tenant_scope`-style read. Parallelizable per repo. |
| Category B check tool (new, first informational version) | 1–2 days | Reusing existing conventions (§9) keeps this small — most of the design decisions are already made by the two scripts it's modeled on |
| Baseline triage → clean informational run → flip `--strict` | 0.5–1 day | Substantially de-risked by this doc having already done the Category-D triage |
| Category C (schema codegen) | Not new effort for this project | Already in flight ([§6.4](#64-concurrent-work-already-in-flight-eq-field-tenant-provision-generator)); only new work is extending it to eq-service once §0 item 2's footprint is known |

**Total: roughly 1–1.5 weeks of focused engineering across eq-shell/eq-field/eq-service**, not
counting the already-independently-scoped §0 items. Sequencing matters more than the total:
§0 first (independent, urgent), then the Category A migrations (removes most of the drift surface
outright), then the Category B check (catches whatever's left, and guards against regression).

---

## Bottom line

The pattern this doc was asked to scope already works — twice, independently, in this exact
codebase (`app_tenant_scope`, `canonical_tenant_registry`) — and the drift-check convention to
guard whatever can't go dynamic already exists and has a proven rollout sequence
(`check-control-plane-drift.mjs`'s baseline-then-`--strict` history). Nothing here needs inventing.
What's missing is applying both patterns to the ~35 remaining findings above, roughly half of which
(Category A) are mechanical once someone starts, plus building one more check tool that's smaller
than either of its two models because it can borrow their conventions wholesale.

The six items in [§0](#0-fix-now--independent-of-whatever-gets-decided-below) are the actual
priority — three are already running as tasks Royce started independently, three are flagged here
because eq-field currently has three concurrent worktrees on adjacent code and spawning blind risks
collision. Read this doc before deciding how those three get picked up.

Nothing above has been built. This is the scoping pass asked for.
