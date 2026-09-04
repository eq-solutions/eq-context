---
title: EQ Field — Active State (Rolling)
owner: Royce Milmlow
last_updated: 2026-09-04
scope: Current live state of EQ Field product
read_priority: critical
status: live
---

# EQ Field — Active State

**Current version:** v3.5.673 · **Deployed:** `field.eq.solutions` (Netlify site `eq-field`, which also answers on `eq-field.netlify.app`) + the Shell embed at `core.eq.solutions/sks/field`
**Repo:** `eq-solutions/eq-field` — vanilla HTML/JS, no build step; `main` auto-deploys via Netlify

> **Re-verified line-by-line 2026-09-04** against live: `field.eq.solutions/sw.js` (`CACHE` const) and eq-field `origin/main`; eq-shell `origin/main` (`src/pages/FieldIframe.tsx`, `src/lib/fieldTenants.ts`); jvkn (`shell_control.tenant_routing`, `public.organisations` + `module_entitlements`, the edge-function list, `pg_trigger`); ehow (row counts, the `app_data.field_*` view inventory, table locations). The previous version of this file (last_updated 2026-07-21) was pinned at v3.5.334 — 339 versions behind — and its "Gated" list still said the roster was empty. Every section below was rewritten from what was found, not bumped. Older dated snapshots that used to live here (2026-06-13 sync counts, the 2026-06-18 apprentice/acknowledgments launches) are records, not state — they live in `eq/changelog/eq-field.md`.

---

## Live tenants

| Tenant | Way in | Data plane | State |
|---|---|---|---|
| `sks` | `core.eq.solutions/sks/field` (Shell iframe — the only way in; Field's standalone PIN gate is code-blocked for SKS, `IDENTITY-MODEL.md` §7.1) | `ehowgjardagevnrluult` (ehow / sks-canonical) — **SKS LIVE**, the only tenant with rows on that plane | Live — the only live customer data in this product |
| `eq` | `field.eq.solutions/?tenant=eq` (legacy PIN gate) | `zaapmfdkgedqupfjtchl` (zaap / eq-canonical-internal) — demo/disposable, NOT a customer | Live (sandbox data) |

Routing source of truth is jvkn `shell_control.tenant_routing`: `sks → ehow [active]`, `eq → zaap [active]`, `favour-perfect → nxojbntrpxfnbhbyaspp [suspended]` (that Supabase project was deleted; the row is left suspended on purpose — suite-state Incidents). Field reads each tenant's config and module entitlements from jvkn `public.organisations` / `module_entitlements` at boot (`scripts/app-state.js`); no per-tenant map exists in code.

**Retired:** `demo-trades` / `melbourne` DB-backed demo tenants — deleted from canonical 2026-06-28 and no longer resolve (eq-shell's `fieldTenants.ts` still lists them in its picker; nothing is behind them). `ktmj`, the old `eq` data plane, was deleted 2026-07-04. The only remaining demo surface is `?tenant=demo` — an in-memory URL-override slug with hardcoded gate codes and no DB.

**Shell embed (eq-shell `origin/main`, 2026-09-04):** `core.eq.solutions/sks/field` iframes **`https://eq-field.netlify.app/?tenant=sks#sh=<jwt>`** — the SKS URL is hardcoded in `fieldTenants.ts` and must not inherit `VITE_FIELD_URL` (which points the `eq` tenant at `field.eq.solutions`). `field.sks.eq.solutions`, the host named in the 2026-06-06 cutover doc, no longer resolves in DNS (curl exit 6, 2026-09-04) and nothing in eq-shell references it any more.

---

## Auth model

**SKS (Shell embed) — token mode only.** Shell mints a **60-second Supabase JWT** in `netlify/functions/token-exchange.ts` (HS256 on `SUPABASE_JWT_SECRET`, `source_app = field:sks`) and hands it to Field in the `#sh=` hash. Field's `netlify/functions/verify-pin.js` (action `verify-shell-token`) verifies it, skips the PIN gate, and mints the per-tenant **data JWT** (`mint-data-jwt`, gated by the `DATA_JWT_ENABLED` env flag) that every ehow query rides on. When the 60 s token expires Field asks Shell for a fresh one over postMessage (`REQUEST_SHELL_TOKEN`) and Shell re-mints it. **Cookie mode (`?shell=1` + the `verify-shell-cookie` action) was retired 2026-07-11 (eq-shell #756)** — the `eq_shell_session` cookie is not reliably delivered to the cross-origin iframe. The `verify-shell-cookie` branch still exists in `verify-pin.js`; Shell no longer calls it.

**`eq` / `demo` (standalone) — legacy PIN gate:** gate code → `verify-pin.js` → HMAC-signed session token (7-day — `signToken()` in `verify-pin.js`). This gate is the *only* way into the demo tenant, which is why the ~1,300 lines behind it cannot be deleted yet (`IDENTITY-MODEL.md` §7.1, 2026-07-05 callout).

Full model and history: `eq/identity/IDENTITY-MODEL.md` §7.1.

---

## SKS canonical state (ehow — verified live 2026-09-04)

**Data path:** data JWT → the `app_data.field_*` adapter views. **18 `field_*` views present** (this file said "all 11" as of 2026-06-13): `field_audit_log`, `field_job_numbers`, `field_leave_requests`, `field_managers`, `field_people`, `field_people_directory`, `field_people_removed`, `field_prestarts`, `field_schedule`, `field_site_diaries`, `field_site_projects`, `field_sites`, `field_team_members`, `field_team_supervisors`, `field_teams`, `field_timesheet_locks`, `field_timesheets`, `field_toolbox_talks`. Adapter architecture: `field_people` / `field_managers` → `app_data.staff` and `field_sites` → `app_data.sites` (read-only — Shell owns the canonical rows); the operational views pass through to Field's own tables, which now sit in both `app_data.*` (Design B: `timesheets`, `leave_requests`, `teams`, `team_members`, `documents`, `document_signoffs`, `site_projects`, `timesheet_locks`) and `public.*` (`prestarts`, `toolbox_talks`, `site_diaries`, `site_audits`, `job_numbers`, `roster_presence`). SKS traffic reaches the Design B base tables directly via `JWT_INPLACE_TABLES`; the six operational views are the fallback path, not the hot path (field PR #498). `field_people_directory` and `field_managers` are SECURITY DEFINER views with the tenant predicate inside the definition (advisor finding, 2026-09-04 go-live review).

**Counts (direct query, ehow, 2026-09-04):**

| What | Count | Note |
|---|---|---|
| `app_data.staff` | 107 (73 active) | Direct 63 (50 active · 22 supervisors · 21 off-roster) · Labour Hire 25 (11 active) · Apprentice 12 (11 active) · Subcontractor 7 (1 active). All 107 carry a `cards_worker_id`; 77 are linked to a Shell user. `field_people` = the 73 active. |
| `app_data.sites` | 255 | `field_sites` view = 58 (the view's own filter; not re-derived this pass) |
| `app_data.licences` | 221 | synced from Cards (`cards_credential_id`) |
| `field_schedule` | 1,974 | |
| `field_timesheets` | 353 | |
| `field_leave_requests` | 48 | |
| `public.prestarts` / `toolbox_talks` / `site_audits` | 233 / 7 / 0 | site audits: page live, no data yet |
| `field_job_numbers` | 56 | Ops-sourced job numbers + Field-local manual rows — `eq/ops/EQ-OPS-ARCHITECTURE.md` §3 |
| `field_managers` | 0 | has never populated — suite-state Field Data Plane |

**Canonical sync (jvkn ↔ ehow):**
- **Workers — live.** `workers-canonical-sync` edge function on jvkn (now v23), fired by the `worker_canonical_sync` trigger on jvkn `public.workers` (present in `pg_trigger`, 2026-09-04). Shell side: `cards-approve-staff.ts` at approval time + `staff-resync-licences.ts` on demand.
- **Licences — live, different mechanism to the one this file used to describe.** The dead `credentials-canonical-sync` v1 (never wired, wrong tenant const) **has been deleted** — it is absent from jvkn's function list on 2026-09-04, so the 2026-07-26 "still needs manual deletion" item is closed. Licences now flow Cards → eq-shell `licence-push.ts` (PR #1076; revocations since PR #1080), with the jvkn `licence-canonical-sync` edge function (created 2026-08-13 — a service-secret-authenticated re-fire path, eq-cards changelog) and Shell's `eq_reconcile_licence_sync` / `eq_audit_licence_sync_dispatch` RPCs (PR #1431) behind it. Known limit: hardcoded to ehow/SKS, not generic tenant routing (`eq/pending/eq-cards.md`).
- **Identity stub retired.** The v3.5.147 `_tryLinkPersonToWorker()` scaffolding is gone from `people.js`; `syncAllToCanonical()` and its helpers were removed 2026-07-06 as confirmed dead code — no caller since the UI button was pulled in v3.5.227 (comment at `people.js:1572`). Cards/Shell are the creators of jvkn `workers` rows now, which is the condition that scaffolding was waiting on.

---

## Modules live (nav pages in `index.html` v3.5.673; gating = jvkn `module_entitlements` where the table is in `MODULE_UNIVERSE`, otherwise Field's `permission-matrix.js`)

| Module | Tenants | Notes |
|---|---|---|
| Dashboard · Roster / Schedule · Calendar · Contacts (People) · Sites · Map · Leave · Timesheets · Managers · Site Diary · Site Audits · Job Numbers · Sign Documents | All | Core pages, not entitlement-gated; role-gated per `permission-matrix.js` |
| Safety (Prestarts · Toolbox talks · Incidents · Safety dashboard + records) | `sks`, `eq` | `prestarts` / `toolbox_talks` entitlements enabled for both orgs. Prestart/Toolbox create is open to every Field role except subcontractor since 2026-08-24 (failure ledger F14) |
| Teams | `sks`, `eq` | `teams` / `team_members` entitlements |
| Apprentices | `sks`, `eq` | `apprentice_*` + skills / competencies / feedback / rotations / buddy-checkins / quarterly-reviews entitlements; those tables are split across `public.*` and `app_data.*` on ehow |
| SKS Pipeline (tenders · nominations · resource allocation · accounts) | `sks`, `eq` | `tenders` / `tender_*` / `nominations` / `nomination_clashes` / `pending_schedule` entitlements |
| Projects / Forecast | `eq` only | `projects` / `regions` / `project_targets` — **not** enabled for `sks`; the "Melbourne demo" that carried this is gone |
| Acknowledgments (peer recognition) | All | `public.acknowledgments` on ehow (v3.5.159) |
| Admin pages: Data · Editor · Email templates · Feature toggles · Calibration · Trial · PINs | role-gated | |

Source of truth for entitlements: jvkn `public.module_entitlements` (positive set per org; Field computes disabled = universe − enabled at boot).

---

## Open (Royce-gated)

1. **Standalone `sks-nsw-labour` retirement** — still live at `sks-nsw-labour.netlify.app` (own repo, own PIN, own Supabase `nspbmirochztcjijmcrx`). Royce, 2026-08-30: "SKS NSW LABOUR is about to be retired — ignore anything relating to that." Usage is draining to Field — go-live week 31 Aug–4 Sep: Labour app active people 50 → 24 and timesheet saves 618 → 153 while Field-in-Core rose 58 → 106 (2026-09-04 go-live review). What remains is the rollout of the last workers off it, not a code change (`sessions/2026-09-01.md`, P5). SEC-1 (the Labour app's public-key PII exposure) closes with the retirement, by design — no engineering changes to that app in the meantime.
2. **Track 2 RLS step 2 (anon SELECT lockdown on the Labour app's Supabase)** — same dependency; lands when the standalone app is retired.

**Closed since the previous version of this file:**
- ~~Roster data entry on ehow~~ — done: 1,974 schedule rows / 353 timesheets / 48 leave requests live.
- ~~Collin Toohey fresh invite~~ — done: active `app_data.staff` row on ehow (Direct, Shell-user-linked, 7 licences, last updated 2026-08-23) pointing at Cards worker `7514e57d…`. **Live observation 2026-09-04:** jvkn `public.workers` holds a *second* Collin Toohey row again — `bf26e8c4…`, created 2026-07-26, user-linked but with no `staff_id`, no role and 0 licences, never updated since. Its `user_id` is `38859cae…` — exactly the empty stub user from the EQ-SHELL-Z incident in `sessions/2026-08-02.md`, which Royce had deactivated; that user still exists in `auth.users` and `shell_control.users`, and this worker row was never removed alongside it. **Fully resolved 2026-09-05** — the second `public.workers` row (`bf26e8c4…`) was re-verified live: still zero references anywhere across jvkn/ehow/zaap, but `auth.sessions` showed the stub account (`38859cae…`) had minted a new session 2026-09-04, 20s after a normal session on Collin's real account from the same device — the 2026-08-07 `handle_phone_dedup`/`link_pending_invites` trigger fix stops *new* duplicates but doesn't stop this *already-existing* account from still authenticating. Royce chose full deletion over ban-only: deleted `auth.users` `38859cae`, `ON DELETE CASCADE` removed the worker row, its stub profile, and the `identity_collision_flags` audit row in one action; confirmed 0 rows remaining for all three plus `auth.identities`/`auth.sessions`. Collin's real account/worker/staff records confirmed untouched throughout. Full detail: `eq/pending/eq-shell.md` and `eq/changelog/eq-shell.md`, both 2026-09-05.
