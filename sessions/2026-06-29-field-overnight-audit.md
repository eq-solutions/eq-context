# Session — EQ Field overnight audit + battle-test (2026-06-29)

**Driver:** autonomous overnight run (Royce: "battle test, audit and improve Field — security, shell/canonical integration, code audits, high-value features; tech invisible"). Full autonomy approved.

## Mechanism
Background Workflow `wf7v90s6g` (35 agents, ~700s): 4 audit lenses → adversarial verification of every finding → risk-tiered execution plan. 28 findings, **21 confirmed, 0 uncertain, 7 refuted.** Main loop then applied/serialised git + deploys.

## Shipped (autonomous, live)
**v3.5.199 — PR #356 (squash `3488ac5`), live on field.eq.solutions.** Safe-auto correctness tier, all reversible:
- SKS pipeline person assignment was `parseInt()`-ing a uuid → null (Push-to-Roster silently dropped every assignment). Fixed + String() coercion.
- `_resolveFieldPerson` guarded on `TENANT.SB_URL` (never assigned) → PR #352 identity resolution was dead code. Now `SB_URL`/`SB_KEY`.
- Timesheet writes serialised per `name||week` (canonical delete-then-insert lost-write).
- verify-pin CORS moved off retired `eq-solves-field` host → `field.eq.solutions`/`--eq-field.netlify.app`.

Dropped (deliberate): apprentices/journal id-coercion — conformance only, no demonstrable failure.

**v3.5.200 — PR #357 (squash `dd4b8da`), live.** Security: SKS = Core-only auth. Royce confirmed PINs should be irrelevant (auth via Core). Verified the residual exploit path (frame-ancestors `*.netlify.app` → iframe + bogus `#sh=` → handoff-fail → standalone PIN gate → leaked anon-readable `SKSNSW` → client-side supervisor access; verify-pin validates EQ codes so client `checkPin` was the only path). Fix: `checkPin()` refuses PIN auth for `ORG_SLUG==='sks'`; gate shows a "Sign in through Core" panel instead of PIN entry. EQ demo tenants unchanged. Behaviorally smoke-tested in browser on the deploy preview. → audit finding #2 RESOLVED.

## DB hardening applied (Royce: "Go A")
**Migration `tender_cluster_anon_teardown_canonical_org`** on ehow (repo record PR #358, no app version bump). **DECISION: Option A** — all SKS `public.*` RLS scopes by canonical org `000…002` (read) + JWT tenant claim (write), per the audit_log/acks template. Now the SKS public.* standard.
- Dropped anon policies + `REVOKE anon` on tenders / tender_import_runs / tender_review_decisions / nominations / tender_phases / job_numbers.
- Realigned authenticated policies to `000…002` (the old `field_authed_all` matched JWT `7dee117c…` ≠ the rows' canonical org, so Field had been reading tenders only via the anon policy — a naive revoke would have blanked the Pipeline).
- Added missing `GRANT … TO authenticated` on nominations / tender_phases / job_numbers.
- `app_data.field_people` SECURITY DEFINER → invoker.
- **Verified:** anon REST → 401 on all 6 (was 206/366 on tenders); authenticated SKS-JWT reads 366 tenders / 8 job_numbers (Pipeline intact); 0 anon policies/grants remain.
- Neutralised stale `20260618_acknowledgments.sql` (anon-grant footgun) in place.
→ audit findings #1 (CRITICAL tenders), #3 (field_people), #4 (job_numbers), #7 (stale migration) RESOLVED.

## Still open for Royce (needs-review remainder)
- **#5** audit logging on SKS — set `AUDIT_SB_KEY` → ehow service_role (Royce sets the secret) + stamp `org_id` in verify-pin.js/eq-agent.js.
- **#6** Supervisor Notes — recreate `people_notes`/`supervisor_notes` on ehow (hardened Option A template; worker-first). Recommended; distinct migration.
- `frame-ancestors *.netlify.app` tightening (declined once; left in queue).
- Features: worker-facing recognitions (first), quiet recognition notify, leave-remaining (needs units decision), supervisor tour.

## Incident + fix: SKS Contacts/roster blank (post-deploy)
Royce reported EQ Field → Contacts no longer showed the SKS staff list. **Not the security migration** (column error 42703, not a permission error). Root cause chain:
1. **`window.TENANT` was never set** — `app-state.js` declares `TENANT` as a `let` (not a window property). The canonical roster/timesheets/leave adapters read `GLOBAL.TENANT` (= `window.TENANT`) → `undefined` → no slug → `isCanonical*Tenant` returned false before any allow-list/flag logic. So canonical mode never engaged for SKS.
2. SKS `schedule?…&week=in.(…)` then routed to the `field_schedule` JWT twin (has `date`, not `week`) → **400**.
3. `loadFromSupabase` loaded people/sites/schedule/managers/timesheets in one `Promise.all`; the schedule 400 rejected the batch → `STATE.people` never set → Contacts/managers blank.

**Fixes shipped:**
- **v3.5.201 (PR #359):** `loadFromSupabase` per-fetch resilience (one surface can't blank the directory — this restored Contacts) + adapter allow-list made authoritative (a missing PostHog `roster_canonical_v1` flag no longer disables a migrated tenant — `isEnabled()` returns false for an undefined flag).
- **v3.5.202 (PR #360):** `app-state.js` exposes `window.TENANT = TENANT` (mutated in place, never reassigned → stays in sync). Verified on preview: `window.TENANT` defined + `=== ` lexical TENANT; all three adapters return true for SKS; `week→date` rewrite fires. This makes canonical roster/timesheets actually engage → no 400.

**GOTCHA for future:** canonical adapters (roster/timesheets/leave) read `window.TENANT`; keep it exposed. A missing PostHog feature flag must never be the sole gate for a migrated data path.

## Canonical-wiring audit (2026-06-30, workflow wpz5m18d9)
Full 12-feature audit of Field UI+wiring vs canonical schemas, verified live on ehow. Deliverable: repo `FIELD-CANONICAL-AUDIT-2026-06-30.md` (local-only).
- **Core finding:** Field ~80% canonical CLIENT-side; DB grants unfinished. `app_data.schedule_entries`/`timesheets`/`leave_requests` (+ safety/realtime twins) grant service_role ONLY → the authenticated browser JWT 401s before the (present, correct) tenant RLS evaluates. Empty tables mask it. **#1 = one migration granting authenticated CRUD on those 3 (+ hours_planned DEFAULT 0)** → unblocks Roster+Timesheets+Leave+realtime.
- **Redundant (retire, don't finish):** PIN gate/PIN-mgmt/staff-PIN (Core auth; field_people NULLs pin), Sites CRUD (Shell-owned), full JSON backup/restore, Projects/Forecast (tier-dormant).
- **Works (don't rework):** People writes (INSTEAD OF trigger → app_data.staff), Recognitions, Tender shell create/move/archive, reads, Dashboard.
- **Outstanding after #1:** field_managers write path; Safety grants + CREATE site_audits (don't exist despite v3.5.193 changelog); digest→app_data.staff; tender enrichment grant + ORG_TABLES; Job Numbers dead-call cleanup; user_id backfill (14/75); apprentices cluster (largest debt); decide create-vs-retire pending_schedule/roster_presence/teams/people_notes.
- **9 open decisions for Royce** (grant scope, hours_planned, manager-writes-needed?, people_notes drift-signal call, pending_schedule, tender_enrichment org_id reconcile, site_audits home, user_id Core dependency, teams/presence gate-off).

### Execution pass 1 (2026-06-30, v3.5.203, PR #361 — Royce: "go")
- **#1 DONE (the headline):** migration `field_operational_tables_authenticated_crud` on ehow — granted authenticated SELECT/INSERT/UPDATE/DELETE on app_data.schedule_entries/timesheets/leave_requests + `hours_planned` DEFAULT 0. Verified: authenticated SKS-JWT INSERT lands (hours=0, tenant_id from JWT, RLS WITH CHECK passes). **Unblocks Roster + Timesheets + Leave write paths** (were service_role-only → 401 before RLS). Recorded at supabase/migrations/20260630_field_operational_tables_authenticated_crud.sql.
- **PIN subsystem retired for SKS:** openPinManagement (people.js) + checkStaffTsLogin (auth.js) no-op for ORG_SLUG==='sks'. EQ demo keeps PINs.
- **Job Numbers:** removed 3 dead populateJobNumberDatalist() calls (spurious "Save failed").
- **Deferred:** digest re-point (coupled to field_managers/app_data.staff write surface → needs the "do supervisors edit managers in Field?" decision).

### Execution pass 2 (2026-06-30, v3.5.204, PR #362 — "continue")
- **Tender writes DONE:** migration `tender_enrichment_canonical_org_authenticated` (enrichment was service_role-only + JWT-tenant-scoped policy → hardened to canonical org 000…002, anon torn down, authenticated CRUD) + ORG_TABLES gains tender_enrichment/nominations/tender_phases (carry org_id; client now stamps 000…002 → was 403). Enrich/nominate/set-phases work on the live 366-tender pipeline now.
- **Recon notes for next:** realtime — schedule_entries/leave_requests are NOT in the supabase_realtime publication (needs ALTER PUBLICATION add, separate from grants). Safety — the 3 twins (field_prestarts/toolbox_talks/site_diaries) are definer + service_role-only; bases are split (field_prestarts→public.prestarts [authenticated granted]; toolbox/diary→app_data.* [service_role only], with redundant public.* copies [authenticated granted]). Needs view-def analysis before granting. site_audits/site_audit_items still don't exist (need creation + schema from audits.js).
- Still open per FIELD-CANONICAL-AUDIT-2026-06-30.md: Safety, realtime publication, field_managers write path (+digest), apprentices, supervisor-notes, presence/teams gate-off, user_id backfill, worker_id mirror removal.

### Execution pass 3 (2026-06-30, v3.5.205+206 — "continue" x2)
- **v3.5.205 (PR #363):** Presence OFF + Supervisor Notes RETIRED for SKS (both dead/absent on ehow; Notes per worker-first). Code-only.
- **v3.5.206 (PR #364):** Managers + Sites read-only for SKS (Shell-owned; field_managers/field_sites SELECT-only). Gated 8 write entry points to "managed in Core". Code-only.
- **DIGEST surfaced as a product decision:** app_data.staff.digest_opt_in DEFAULTS false but client defaults opted-IN → fixing wiring silently flips SKS supervisors from "all get Friday digest" to "none until opt in". Needs opt-in-vs-opt-out call + backfill decision before wiring.
- **Still next:** Teams wire (twin migration), Safety grants + CREATE site_audits (view-def tangle), realtime publication add. apprentices/user_id-backfill/worker_id-mirror remain.

## Earlier staging (now mostly resolved — see above)
Full writeup + ready SQL: `eq-field/OVERNIGHT-AUDIT-2026-06-29.md` (LOCAL ONLY — contains live PINs + exploit steps; never commit/deploy).
1. **CRITICAL** anon read/write/DELETE on live `public.tenders` (366 rows) + tender cluster. **Org-scoping mismatch found:** rows = canonical `000…002`, authenticated policy = JWT `7dee117c…` → Field reads tenders only via anon today; naive revoke blanks the Pipeline. Needs canonical-vs-JWT org-model decision.
2. **HIGH** anon-readable gate PINs in `public.app_config` (coupled to gate code re-route + PIN rotation).
3. **HIGH** `app_data.field_people` SECURITY DEFINER (low risk — only SKS on ehow).
4. **MEDIUM** `job_numbers` latent anon CRUD + missing authenticated grant/policy.
5. **MEDIUM** SKS auth audit logging silently fails (AUDIT_SB_KEY→service_role + stamp org_id).
6. **HIGH** Supervisor Notes write to non-existent `people_notes`/`supervisor_notes` on ehow.
7. **MEDIUM** stale `20260618_acknowledgments.sql` re-opens anon PII if replayed (neutralise-in-place).

Clean: CSP parity, auth HMAC/rate-limit/CORS core.

## Features proposed (product calls, pass recognition filter)
Worker-facing recognitions surface; quiet recognition notification; leave-remaining (needs units decision); first-run supervisor tour.

## Decisions pending (Royce)
Org-scoping model (A: realign policies to `000…002` [rec] / B: re-stamp rows); new PIN values; AUDIT_SB_KEY→service_role; recreate Supervisor Notes now?; neutralise stale acks migration OK?; migration bundling.
