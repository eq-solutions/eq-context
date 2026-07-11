---
title: Changelog — EQ Solves Field
owner: Royce Milmlow
last_updated: 2026-07-11
scope: Append-only history of changes to the EQ Solves Field product
read_priority: reference
status: live
---

# Changelog — EQ Solves Field

## [2026-07-11] v3.5.298 — Safety offline queue unwedged: stale sks_rep payload + poison-pill replay (SHIPPED, PR #451, live)
- **BUG:** Safety showed "1 pending offline write" permanently on SKS. A prestart queued offline ~25 June (pre-v3.5.220 build) still carried the old `sks_rep` field name; the live `prestarts` column is `site_rep` (renamed client-side in v3.5.220, but entries already in the queue kept the stale key). Every replay 400'd (`PGRST204: could not find the 'sks_rep' column`) and went straight back in the queue — a poison pill re-firing on every Safety open, with no exit because the replay loop treated all failures as retryable.
- **FIX (`safety.js _qReplay`):** (1) queued payloads are normalised on replay (`sks_rep`→`site_rep`), so the stuck June prestart actually lands in the DB — the record is rescued, not discarded; (2) entries that fail with a permanent 400/404 are parked in a `<queueKey>_dead` localStorage key (payload + error + timestamp kept, Sentry-captured with the full payload) and removed from the live queue, so the pending pill can no longer wedge. Transient failures (network/401/403/5xx) still retry as before. Same permanent-4xx dead-letter guard added to `site-reports-shared.js replay()` (site_reports/diaries/toolbox v2 queues had the identical retry-forever flaw; no rename there — `site_reports` genuinely has an `sks_rep` column).
- No DB change — live `prestarts` schema verified correct on ehow first.
- **Renumbered v3.5.296→298 at merge:** a concurrent session's JSZip boot-perf PR #452 took v3.5.296 and the capacity panel PR #453 took v3.5.297 while this was open; conflicts resolved by hand. Prod verified serving v3.5.298.

## [2026-07-11] v3.5.297 — Resource Allocation capacity panel: labour-curve jobs light it up + demand-scaled chart (SHIPPED, PR #453, live)
- **BUG:** the Capacity Planning panel (SKS Resource Allocation) stayed on the "Set start dates and worker counts on Won jobs…" empty state for jobs planned with a **Labour Curve** (phases). The chart's demand builder fully supported phases, but the render GATE only checked the flat `peak_workers` + `duration_weeks` enrichment fields — so SKS-16310 (confirmed, start date + 3 phases, flat fields empty) never rendered the chart, the roster strip, or its WORKERS/WEEKS table numbers.
- **FIX:** new `_isAllocated()` gate matches the builder (start date + phases OR peak+duration). WORKERS/WEEKS columns, the mini-timeline and the job colour chip now derive from the curve (max phase headcount / total phase weeks) when the flat fields are empty.
- **Design (reviewed live-data "Mock B" before build):** panel reads **roster-first** — the THIS WEEK strip (N on the roster · N free · N jobs live · N needed) moved above the stat tiles. Chart **scales to demand, not headcount** — with 90 on the books vs 4–12-crew jobs the old `max(HC, demand)` y-scale rendered every real job as near-flat bars under an HC line pinned to the top; the HC dashed line now draws only when demand is within reach of headcount, otherwise it rides in the legend as an "HC N — no week exceeds it" chip (per-week exceeds-HC red outlines unchanged). Peak-demand tile names its week.
- **"Save phases" now rebuilds the unpushed labour plan** (`pending_schedule`) to match the current curve — previously slots were generated once at Save & Confirm, so a phase added later diverged silently (SKS-16310 showed "66 to assign" from its confirm-time curve while the edited curve implied 114). Same safety rule as details-edit: rows already pushed to the live roster are never touched.
- SKS-only surface (`sks-pipeline-resource.js`), no DB change. Design-review artifact: https://claude.ai/code/artifact/160c2243-ae48-43ca-8c7e-bcadb4343659

## [2026-07-11] v3.5.295 — SKS auth audit trail now visible in-app: stamp CANONICAL org_id (SHIPPED, PR #450, live)
- **BUG:** every server-side auth event on SKS (`verify-pin` logins, `eq-agent` calls) was stored in `audit_log` but INVISIBLE in the in-app Audit view. The Netlify functions stamped `org_id = TENANT_ORG_UUID` (the legacy field_org_id `1eb831f9-…`), while `audit_log`'s RLS + the Audit view read as the SKS `authenticated` JWT filtered to the canonical org `000…002` — the org the client and every hardened `public.*` table use. Mismatch → 600+ login rows since 2026-06-30 landed (service_role bypasses RLS) yet never showed. Drift from the 06-25/06-30 canonical hardening: migrations moved SKS `public.*` to `000…002`; the Netlify env was never updated.
- **The documented diagnosis was STALE** (verified live on ehow 2026-07-11): schema is complete, `AUDIT_SB_KEY` is already `service_role`, verify-pin DOES stamp org_id, writes land daily. The fault was the org_id *value*, not the key/columns. CLAUDE.md schema-gotcha note corrected in the same PR.
- **FIX (code, per-tenant):** `logAttempt()`/`logAgentCall()` resolve `AUDIT_ORG_BY_TENANT` (`sks:000…002`) from the request's tenant slug and stamp THAT. Shell-handoff paths (token/cookie/supabase-jwt) pass the slug; the standalone PIN path (EQ sandbox) omits it → falls back to `TENANT_ORG_UUID`, so EQ behaviour is unchanged. One Netlify site serves both tenants, so this MUST resolve per-request — a single `TENANT_ORG_UUID` env flip was rejected because it would misroute the EQ demo gate's PIN lookup. Override via `AUDIT_ORG_BY_TENANT_JSON`.
- **Forward-only (Royce's call):** the 743 historical mis-stamped rows are left as-is (stored, not lost). No env change, no data migration.
- Bonus finding (not fixed, moot): the same wrong env makes `fetchPinCodesFromDB()` miss every `app_config` row (all `000…002`) → env-PIN fallback; harmless on SKS (Core-only, PIN gate disabled).
- Prod verified serving v3.5.295. Runtime proof (a new `Auth` row on `000…002`) pending the first post-deploy SKS sign-in — deterministic map lookup; not yet observed live at time of merge.

## [2026-07-11] v3.5.294 — mark "SKS leave shows 0" formally RESOLVED in the changelog banner (SHIPPED, PR #449, live)
- Doc-only: added a ✅ RESOLVED status marker to the in-HTML changelog banner (the canonical changelog for v3.5+). No behaviour change. Prod verified serving the marker. Closes the multi-session leave-shows-0 saga in-repo.

## [2026-07-11] Timesheets tab — checked, NO fix needed (no release)
- Asked to apply the leave fix to timesheets. Verified it does NOT have the same gap: timesheets are fetched at BOOT inside `loadFromSupabase`'s main Promise.all (`sbFetch('timesheets?select=*'+weekFilter)`, index.html:8295) → `STATE.timesheets` is populated before any tab renders. Leave was the exception (moved out of the boot fetch into the lazy `loadLeaveRequests()`); timesheets never left the boot path. Verified live on `core.eq.solutions/sks/field?tab=timesheets` (deep-linked, no other tab first): full grid, 88 staff tracked, real hours/codes. No dead `_ensureTimesheetsLoaded` shipped.

## [2026-07-11] v3.5.293 — Dashboard leave strip loads authoritative leave data (SHIPPED, PR #448, live & VERIFIED)
- Follow-up to v3.5.291. The home Dashboard "Leave & Absences This Week" strip read the global `leaveRequests`, but that array was only populated by the Leave tab's `_ensureLeaveLoaded()` (leave.js is lazy → boot-time `loadLeaveRequests()` skipped). On a deep-linked `?tab=dashboard` (how Core lands users) the strip showed only the roster A/L overlay fallback, never the real `leave_requests`.
- Fix: `renderDashboard()` kicks the SAME cached one-shot — lazy-loading leave.js first if needed — and re-renders when data lands. Once per session (`renderDashboard._leaveKicked`); shared `_leaveInitialLoad` promise = single fetch, no double-load with the Leave tab; degrades to the roster overlay on failure; leave.js stays lazy (no boot-parse regression).
- **Verified live on `core.eq.solutions/sks/field?tab=dashboard`** (no Leave-tab visit first): full A/L/RDO/OFF absences list + a "PENDING LEAVE 1" card (Tadhg Byrne). Pending status comes only from `leave_requests`, so that card proves the authoritative data loaded.

## [2026-07-11] v3.5.291/292 — ✅ THE leave-shows-0 fix: leave list was never fetched on a deep-linked open (SHIPPED, PRs #446/#447, live & VERIFIED)
- **RESOLVED the multi-session "SKS leave shows 0" bug. Verified live on `core.eq.solutions/sks/field?tab=leave`: PENDING 1 / OFF THIS WEEK 10 / APPROVED 15; on-screen diagnostic confirmed `status:200, leaveCanon:true, rows:31`.**
- **True root cause (proven, not inferred):** routing was correct all along (BOOT_DIAG banner read `slug=sks, SB_URL=ehow, canon=TRUE`). The leave READ never ran: `leave.js` is lazy-loaded so `initApp()`'s boot `loadLeaveRequests()` is skipped (undefined then); `renderLeave()` only renders; realtime does no initial read; the 30s poll is suppressed under realtime. On a deep-linked `?tab=leave` (how Core embeds Field) `leaveRequests` was never populated. The panel's "↺ Refresh" was `onclick=renderLeave()` — a pure re-render. 31 rows never lost, never fetched.
- **Fix (v3.5.291, PR #446):** `renderLeave()` → `_ensureLeaveLoaded()`, a cached-promise one-shot that fetches on first tab open and re-renders when data lands.
- **v3.5.292 (PR #447):** removed all temporary diagnostics (BOOT_DIAG/LEAVE_DIAG banners, `__eqDiag`, Sentry LEAVE_DIAG) — they were user-visible on the leave screen.
- **Diagnostic method that finally worked:** an on-screen banner read off a screenshot — the only channel that pierces a cross-origin + storage-partitioned embedded iframe (console needs the user; localStorage is partitioned; Sentry is silent from the embedded frame).

## [2026-07-11] v3.5.286/287 — canonical gate keyed on the resolved DB + window.SB_URL refresh (SHIPPED, PRs #439/#440, live) — necessary, not sufficient
- **v3.5.286 (PR #439):** leave/roster/timesheets canonical-mode gates now return true when the resolved tenant DB (`window.SB_URL`) is the SKS plane (ehow), as well as when `TENANT.ORG_SLUG==='sks'`. Removes the single-point-of-failure slug dependency so an embedded-restore slug hiccup can't route SKS to the service_role-only twin (→401→empty). `window.SB_URL` exposed in app-state.js. `app_data.leave_requests` (with data) exists only on ehow so the DB match can't over-trigger on eq/zaap. (Verified in isolation: gate returns true for an ehow URL even with a broken slug.)
- **v3.5.287 (PR #440):** `sbFetch` refreshes `window.SB_URL` from the lexical `SB_URL` on every call — closes any resolve-path that set SB_URL without re-exposing it.
- These were real fragility fixes (canon WAS slug-fragile) but did not fix leave — because the read never fired (see v3.5.291). v3.5.288–290 were temporary diagnostics, all removed in v3.5.292.

## [2026-07-10] v3.5.283 — honor ?tenant= override whenever iframe-embedded (SHIPPED, PR #434, live) — DID NOT FIX SKS LEAVE
- Intended as THE root-cause fix for "SKS leave shows 0": a live diagnostic showed the leave adapter was loaded but its canonical gate returned false (`TENANT.ORG_SLUG` ≠ 'sks'). Theory: Shell embeds Field at `eq-field.netlify.app` (matches no canonical tenant hostname) so `?tenant=sks` is the only thing making it SKS, and a backgrounded iframe reboots with the `#sh=` hash stripped → the override was rejected → session fell back to 'eq'. Fix honors the override whenever `window!==window.top`.
- **STATUS: did NOT resolve the symptom.** Leave was still 0 after deploy + fresh reload. Root cause is confirmed (`canon:false`) but this fix didn't correct it — the exact reason ORG_SLUG lands wrong is still unknown (needs the runtime `TENANT.ORG_SLUG` value). See `eq/pending.md` 🔴 UNRESOLVED entry.
- ⚠️ Also: spinner-of-death recurred on SKS after this merge (likely rapid SW-cache churn across 4 same-day deploys, not this code). Revert candidate if it persists.

## [2026-07-10] v3.5.282 — leave_requests is the single source of truth; roster overlays it live (SHIPPED, PR #433, live)
- Model change: retired the approve→`writeLeaveToSchedule` write-back. The roster and dashboard now COMPUTE approved leave at render from `leave_requests` (new `overlayApprovedLeave()` in roster.js — read-only, never mutates STATE.schedule). Leave wins for display; a site rostered under approved leave shows a ⚠ conflict marker instead of being silently hidden.
- `dashboard.js` "Leave & Absences This Week" reads `leave_requests` (approved, overlapping the week), unioned with manual roster absences so typed A/L/OFF still show.
- Fixes the SKS symptom where 30 bulk-imported approved-leave records never appeared on the roster (the old write-back only fired on UI approval). No DB change.

## [2026-07-10] v3.5.281 — SKS leave showed 0: precache the canonical adapters (SHIPPED, PR #432, live)
- Root cause: `leave-adapter.js`/`timesheets-adapter.js`/`roster-adapter.js` were network-only (not in the SW precache). When `leave-adapter.js` failed to execute, `EQ_LEAVE_ADAPTER` was undefined → supabase.js's leave read silently fell through to the `app_data.field_leave_requests` twin, which is service_role-only (`authenticated` → 401) → empty Leave surface with no error, while 31 real records sat in the DB.
- Fix: precache all three adapters so their globals can never be missing; add a loud `canonical-adapter-missing` breadcrumb in supabase.js if a leave/timesheets/schedule read ever runs without its adapter. Verified live: the authenticated JWT reads all 31 rows from `app_data.leave_requests` directly (data, grants, RLS, tenant isolation all correct). No DB change.

## [2026-07-10] v3.5.278 — migrated SKS site deployments now render their code (SHIPPED, PR #429, live)
- Fix: 704 real SKS roster deployments (across 19 sites) were invisible — blank cells. The canonical migration wrote `schedule_entries` rows with a real `site_id` but no free-text `task`, and `roster-adapter.js` reads the wide cell text from `task` with no `site_id`→code resolver wired (the documented `_warnSiteGapOnce` "site linkage is a follow-up" gap). Built the read-side resolver: `app_data.sites` (site_id→short code) is loaded alongside the staff map on the same JWT, and `cellFromRow()` renders the site's code (SYD53/ARN/STG/…) for a row with a site_id but no task. `scripts/roster-adapter.js`, `scripts/supabase.js`.
- Precedence preserved + tested (8 new golden tests, 87 pass): typed `task` still wins (lossless carrier), leave markers still win (on-leave ≠ deployed), unresolved/codeless site_id → blank as before. Site read is non-fatal (failure leaves cells blank, never breaks the staff map or boot).
- Spot-checked live before building (Royce's call): the 704 rows are sound — real staff, 19 real sites all with clean codes, weekdays only, 0 double-bookings, 0 orphans. `app_data.sites` read verified: `authenticated` has SELECT, `sites_tenant_isolation` RLS uses the identical JWT qual as the working `staff_tenant_isolation`.
- Read-only sugar: write path unchanged, so a first edit converts a newly-visible cell to a normal text cell (site code preserved). A full read+write canonical roster model is a larger, post-cutover follow-up. **Not visually confirmed on a live SKS session** (no SKS creds in-session) — Royce to eyeball the roster for w/c 2026-07-06.

## [2026-07-09] v3.5.273 — Revert now works for SKS roster edits (SHIPPED, PR #424, live)
- Fix: Revert on an SKS roster audit entry did nothing but silently show "can't be reverted" — closes the "structurally non-functional" gap deferred in v3.5.271. Canonical (SKS) roster rows carry no `target_id` (a reconstructed wide WEEK row spans up to 7 separate `schedule_entries` rows, one per day). `revertAuditEntry()` now resolves `staff_id` + `date` from the name/week/day already on every roster audit row, and reuses the same `classifyCell()` the save path trusts to compute the reverted write. `scripts/audit.js`, `scripts/supabase.js`.
- The Revert button's own visibility gate still hard-required `target_id` after the above landed, so it never rendered for SKS and the fixed click handler was unreachable — caught on a deliberate adversarial self-review before shipping; both now share one `_auditRowCanRevert()` gate. Reverting a cell to blank is deliberately out of scope for SKS (declines with a message) — the canonical DELETE path has a tenant-wide-purge fallback not safe to extend in the same pass.

## [2026-07-10] v3.5.277 — paginate the remaining capped reads that should be complete (SHIPPED, PR #428, live)
- Completes the pagination sweep (after v3.5.274's no-limit reads and v3.5.276/#427's pipeline tables). Split the `limit=N` reads by intent: paginate the completeness-critical ones, leave the deliberate recency caps.
- Paginated via `sbFetchAll()`: `audit_log` (audit.js — full trail; order switched to `id.desc`, a monotonic bigint, so identical newest-first but stable across page boundaries; old limit=500 hid older history), safety dashboard `prestarts`+`toolbox_talks` (aggregate counts), import-reconciliation `tenders` (sks-pipeline-import.js), and pipeline board/resource `tenders`+`people` (sks-pipeline.js, sks-pipeline-resource.js). Non-unique orders got an `,id` tiebreaker for stable offset paging.
- Left as-is (deliberate caps): tender_import_runs (latest/recent-10), tender_review_decisions (only slice(0,8) shown), scoped single/multi-week schedule reads, recent-history list screens (prestarts/toolbox/diary 200, site_audits 50). No behaviour change below the old caps.

## [2026-07-10] v3.5.276 — SKS pipeline: paginate stopgap-capped table reads (SHIPPED, PR #427, live)
- Swapped `tender_enrichment`/`nominations`/`pending_schedule`/`tender_phases` reads in sks-pipeline.js + sks-pipeline-resource.js from `limit=N` stopgaps to `sbFetchAll()` (`tender_enrichment` ordered by `tender_id` — no id column). Left `tenders`/`people` (bounded by a real filter). (Concurrent session; v3.5.277/#428 later extended this to tenders/people + audit_log + safety dashboard.)

## [2026-07-10] v3.5.275 — instrument dashboard anniversaries widget (SHIPPED, PR #426, live)
- Added `dashboard_anniversaries_viewed` (fires once per distinct set of upcoming events, deduped against re-renders) and `dashboard_anniversary_person_clicked` PostHog events to the dashboard "Birthdays & Anniversaries" widget, which had zero usage instrumentation since it shipped in v3.4.16.
- Rows are now clickable through to the person's profile modal (`openPersonProfile()`, same as the roster eye icon), landing on the Acknowledgments section.
- Goal: get a real usage signal before investing further (e.g. auto-suggesting a Recognition on a work anniversary).

## [2026-07-10] v3.5.274 — paginate unbounded full-table fetches (1000-row cap fix) (SHIPPED, PR #425, live)
- Added `sbFetchAll(path, orderBy, pageSize)` to `scripts/supabase.js` (pattern ported from sks-nsw-labour v3.10.89) — pages through with an explicit `order` so a full-table read is actually full, instead of PostgREST silently truncating at its 1000-row default cap and dropping the newest (highest-id) rows.
- Swapped the 6 confirmed-unbounded `select=*` reads to it: `_loadFullDataForExport()` (schedule + timesheets) + `team_members` (index.html); `project_targets` (supabase.js); `timesheet_locks` (timesheets.js); `tender_enrichment` (order `tender_id`, no `id` PK) + `nominations` (tender-pipeline.js). `nomination_clashes` left as-is (view, no id-equivalent, absent live). No behaviour change below 1000 rows — pure headroom.

## [2026-07-08] v3.5.271 — SKS roster/site schema-mismatch fixes (SHIPPED, PR #422, live)
- Fix: Resource Allocation's "deployed this week" stat silently showed 0 for SKS — a `schedule_entries` query asked for wide-table-only columns (`name,mon,tue,wed,thu,fri`) that don't exist on the normalized table. Now `select=*`; the roster adapter rebuilds the wide shape. `sks-pipeline-resource.js`.
- Fix: clicking Revert on an SKS roster audit entry would 400 — same narrow-select bug on the pre-revert read. Now `select=*`. `audit.js`.
- Fix: pushing a job to the SKS roster from Resource Allocation would 400 — a `name=in.(...)` filter on `schedule_entries` has no matching column (the canonical routing shim only translates `week=`/`id=`, not `name=`). Now filters names client-side. `sks-pipeline-resource.js`.
- Fix: `/api/eq-service/sites` (EQ Quotes/Service's site-data pull from Field) was completely dead — pointed at ehow (SKS) but queried a `public.sites` table that doesn't exist there at all (every call 404'd, PGRST205). Rewired to the canonical `app_data.field_sites` adapter view via `Accept-Profile: app_data`. `eq-service-sites.js`. **Verified live:** `AUDIT_SB_KEY` is the ehow service_role key; the view returns 40 active SKS sites. Endpoint deploys clean (401 on unauthenticated smoke, not 500).
- Found, not fixed: Revert is structurally non-functional for every SKS roster edit (not just the 400 above) — `target_id` is always null because reconstructed wide week-rows have no single id to point at. Needs a design decision. See `eq/pending.md` 2026-07-08 (eq-field) entry.

## [2026-07-08] v3.5.270 — CSP: canonical Supabase host allowed in img-src (SKS logo renders)
- Fix: the SKS tenant logo (canonical branding, served from `jvknxcmbtrfnxfrwfimn.supabase.co/storage/.../tenant-logos`) was blocked by Content-Security-Policy — `img-src` never listed the canonical Supabase host, so the browser refused the image on `field.eq.solutions/?tenant=sks`. Added the specific host to `img-src` in both `netlify.toml` and `_headers` (the host was already trusted in `connect-src`; this extends it to `<img>` loads). Not a wildcard: Field's only Supabase-hosted images are canonical logos. Verified live on production. PR #421.

## [2026-07-08] v3.5.269 — People: agency is Labour-Hire-only (SKS lane v3.10.87)
- Fix: an `agency` / hire-company tag no longer lingers when someone is moved off Labour Hire. Saving a person as any other group now clears it, so a former labour-hire worker no longer still reads as labour hire (shown against them + leaking into the v3.5.268 Timesheets agency filter). Guarded at the single write path (`savePersonToSB`) so it covers both the Add-Person modal and the person wizard; the Agency field is also hidden + cleared for non-LH groups on both forms. Surfaced by Jose Quintanilla (was moved to Direct but kept "Madagins" — record cleared, EQ/canonical was already correct).

## [2026-07-08] v3.5.268 — Timesheets: filter by labour-hire agency (SKS lane v3.10.86)
- New **Agency** dropdown on the Timesheets filter bar (next to Group). Pick a labour-hire business and the list narrows to just their people — so you can print or export that agency's sheet and send it to them. Options are built from the `agency` tag on active Labour Hire workers (case-folded to merge stray case variants); the selection persists across re-renders.
- **Exports now honour the on-screen filters.** `↓ Export CSV` and `↓ Payroll Report` previously dumped everyone; both now use the filtered set (group / agency / search on eq-field; + team on SKS), and the filename gains an agency suffix (e.g. `EQ_Timesheets_06-07-26_Atom.csv`). The eq-field exports were unified onto the filtered set and now also include Direct (matching the on-screen view + SKS). Top-right Print already prints the filtered view.
- SKS data tidy: merged two look-alike agency tags — `Madigans`→`Madagins` and `core`→`Core`.

## [2026-07-08] v3.5.263→267 — Timesheets: TAFE days prefilled but editable (SKS lane v3.10.82→85)
Four iterative ships turning apprentice TAFE days from a locked cell into a prepopulated-but-editable one. Shipped to both the eq-field product (v3.5.263→267) and the standalone SKS lane (`sks-nsw-labour` v3.10.82→85).
- **v3.5.263** — the timesheet stopped muting an apprentice's TAFE day during a configured TAFE holiday, so payroll could enter real on-site hours (apprentices work through school breaks). `_tsDayStatus` made holiday-aware.
- **v3.5.264** — soft "TAFE break" hint so the unmuted holiday cell didn't look like the prefill had vanished.
- **v3.5.266** — superseded the above: **every** apprentice TAFE day renders as an editable cell pre-filled with `TAFE`/8h — looks done, counts 8h to the 40h week, reads complete untouched, but you can type a real job straight over it. Stays `workable:false` so completion logic is unchanged; the 8h count (`_tafeHrs`) is entry-aware so overwriting never double-counts.
- **v3.5.267** — the prefill is driven by each apprentice's **nominated TAFE day** (`people.tafe_day`), not just cells where a manager hand-typed TAFE — so their TAFE day prepopulates **every** week, including future weeks the roster isn't built for. Roster content still wins (rostered to a site → shows the site; on leave → mutes); the nominated-day default only fills an empty cell.

## [2026-07-07] v3.5.265 — Prestart Word export back + SW resilience + iOS export (PR #420)
- **Prestart Word export re-added** (`site-reports.js exportPrestartDocx`). It was dropped when Prestart moved from `safety.js` into `site-reports.js` (same rewrite that dropped voice) — the live Prestart had NO Word export on any device. Rebuilt on the shared `SiteReportsShared.docx` builder, mirroring Toolbox: "↓ Word" button in a submitted prestart's locked footer; doc includes site/date/supervisor, prev-day issues, works scope, HRCW, SWMS refs, hazards, permits, crew sign-off (signatures), photos, tenant logo + palette. (Diary export still absent.)
- **Service worker hardened** (`sw.js`) after a stuck-loading report: precache is now per-file (`Promise.allSettled`) not atomic `addAll` — one file's 404/mobile blip can no longer wipe the whole offline cache and strand the app on a dead loader; navigation fallback serves the cached `/index.html` shell when a page request fails.
- **iOS export fallback** (`site-reports-shared.js buildPackage`): installed iOS app (standalone) silently no-ops `<a download>` — now routes the `.docx` to the Web Share sheet, else opens it. Android/desktop/iOS-Safari-tab download unchanged.

## [2026-07-07] v3.5.262 — voice-to-text back on safety-form freeform fields (PR #419)
- 🎤 dictation re-added to the FREEFORM textareas of Prestart, Toolbox and Diary (11 fields). The feature existed in the old `safety.js` forms but was lost when those were rewritten into `site-reports.js`; it had survived only on Site Audits (`audits.js`, v3.5.236).
- New shared `SiteReportsShared.voice` helper (mirrors the audits recogniser): `en-AU`, feature-detected (no mic where unsupported), one recogniser at a time, transcript **appends + stays editable**, draft syncs via the field's own `onchange`, hidden on locked/submitted forms. NOT on structured/code fields (SWMS refs, site/date).
- Needs the Shell iframe mic grant to work in core > field — see eq-shell changelog same date.

## [2026-07-07] v3.5.260 — mobile section nav unified to Lucide line icons (PR #417)
- The mobile nav mixed monochrome symbol glyphs (Home/Schedule/Roster/More) with colour emoji (`⏱` Hours, `🏖` Leave) that stuck out and never tinted on the active item. Replaced all six with inline Lucide line icons; `stroke:currentColor` greys when idle, tints navy when active.

## [2026-07-07] v3.5.259 — all modal footers clear Shell's bottom bar (PR #416)
- Generalised v3.5.258's report-modal fix to EVERY modal in shell-mode. Shell paints its persistent bottom app bar (parent window, above the iframe z-index) over the bottom ~76px, so bottom-sheet footers (Submit/Approve/Save/Done) were hidden. `@media (pointer:coarse)`: overlays bottom-pin + lift 76px, sheet capped to `calc(100dvh - 76px)`.

## [2026-07-07] v3.5.258 — Leave dashboard mobile polish + report-modal footers (PR #415)
- Leave supervisor toolbar (`.eqf-toolbar`) wraps on mobile instead of running its action buttons off the right edge; stat row 4-across → 2×2 at ≤560px; Prestart/Toolbox/Diary sticky Save/Submit footers lifted clear of Shell's bottom app bar.

## [2026-07-05] docs — stale-tenant-reference audit (no version, PR #407)
- Corrected repo docs/comments that described a defunct tenant topology (verified live: canonical `organisations` = eq/sks/favour-perfect; `eq`→zaap live; `ktmj` deleted; demo-trades/melbourne gone). `CLAUDE.md` (tenant list, the inverted "ktmj is live" correction, Stack DB map, resolution wording), `DATA-PLANES-SOURCE-OF-TRUTH.md` (SUPERSEDED banner), two code comments. No runtime change.

## [2026-07-04] v3.5.240 — lazy-loader: never evaluate a lazy script twice (Sentry EQ-FIELD-Q)
- **PR #406, merged + live** (verified `field.eq.solutions/sw.js` = v3.5.240). `scripts/audits.js` is the only script referenced by **two** lazy-load tab groups (`audits` + `safety`), so a double-injection re-ran its top-level `const AUDIT_SECTIONS` (+4 more `const`/`let`) → `SyntaxError: Identifier already declared`, which aborts the whole audit/safety module (the safety area is the flagged-empty Q3 gap).
- **Fix:** `lazy-loader.js loadScript` now skips injection when a `<script>` for that src is already in the DOM — not only when its in-memory `_loaded`/`_loading` maps say so — covering the map-reset / cross-instance races the maps miss. Pure guard, no normal-path behaviour change; protects every lazy script.
- **Also resolved 2 stale Sentry issues** (no code change): EQ-FIELD-P (`openCleanupCodes is not defined` — button removed v3.5.227; event was a user on a cached 3.5.223 bundle) and EQ-FIELD-N (`Unexpected end of input` — old release 3.5.221, transient, no recurrence).

## [2026-07-04] v3.5.239 — job numbers: one board, EQ Ops is the source of truth (rows 26/36)
- **PR #404, merged + live.** SKS job numbers had two drifting lists: Field's local `public.job_numbers` (14) and — separately — EQ Ops's won-quote workbench numbers (`app_data.quote.workbench_job_no`, 32 distinct). Verified live on ehow: **all 14 Field numbers already existed in Ops** — Field was a stale hand-maintained mirror. Comms (`sks_comms_jobs`) is a disjoint Microsoft-only **beta** workstream and is NOT a source (Royce's call).
- **New canonical read view `app_data.field_job_numbers`** (migration `20260704_field_job_numbers_canonical_view`, applied live to ehow) — Ops workbench numbers (source of truth) `UNION` Field-local manual numbers not on any Ops quote (dedup incl. soft-deleted, so closed jobs don't resurface). `SECURITY DEFINER` + column-limited by design: exposes job#/project/customer/site/status only, never quote financials; `authenticated` keeps no SELECT on `app_data.quote`. Live: 23 rows, all Ops-sourced, zero duplicates.
- **`scripts/supabase.js`** — `job_numbers` GET routes to the twin view (data JWT + `app_data` profile), **scoped to `TENANT.ORG_SLUG==='sks'`** (eq/zaap is also data-JWT-provisioned but has no twin → would 404). Writes stay on local `public.job_numbers` (Option A: Ops wins on overlap; manual-add preserved).
- **`scripts/jobnumbers.js`** — Ops rows render read-only with an "OPS" lock badge; mutation paths guarded by `_isOpsJob()`; CSV import replaces only Field-local manual rows and reloads the merged view.

## [2026-07-04] v3.5.236–v3.5.238 + TAFE enablement — QA sheet part 2 (rows 30/31/34/36)
- **TAFE weekly autofill ENABLED on SKS (PR #399, backend-only, no version bump)** — Row 34. The `tafe-weekly-fill` Edge Function was deployed on ehow since v3.5.216 but never switched on (no pg_cron, no `app_config` config) — so the manual "Apply TAFE Day" button was the only trigger, and it 500'd on a missing `TENANT_UUID` secret. Redeployed the function to read the tenant from `body.tenantId` (env fallback kept), set `app_config` `tafe_fn_url` + `tafe_fn_token` (**public anon key** — app_config has an anon SELECT grant so a secret there would leak; the function writes with its own service-role env, gateway `verify_jwt=false`), and scheduled the cron (Sunday 06:00 UTC = 16:00 AEST) with the tenant in the body. Dry-runs verified: fills apprentices on clear weeks, skips holiday weeks. Reversible via `cron.unschedule`.
- **v3.5.236 (PR #401)** — Row 30: voice input (🎤) on every Site Audit comment field, matching prestart/toolbox. Self-contained `_auMicBtn`/`_auSpeechToggle` in audits.js (mirrors `_auSiteDatalist`); en-AU SpeechRecognition, one recogniser at a time, hidden where unsupported or on submitted audits. Live-updates the input (no full re-render). Pure client change.
- **v3.5.237 (PR #402, concurrent session)** — Row 29: prestart auto-fills the customer from the selected site's canonical `customer_name` (blank-only). Dormant until Shell migration 0159 applies on the tenant planes.
- **v3.5.238 (PR #403)** — Row 31: prestart + toolbox photo **bytes** now persist to a private `safety-photos` Storage bucket instead of inline base64 in the row JSON (keeps rows small as usage grows). base64 stays the in-memory format so the photo grid + the .docx embed are **unchanged**; save uploads + stores `{storage_path}` (base64 stripped from the DB payload), open/export hydrates the bytes back. Bucket RLS scopes every object to the caller's own `{tenant_id}/` folder via the data-JWT claim (private, no anon). **Graceful fallback + timeout-bounded**: no data JWT / offline / RLS deny / slow network → photo stays inline base64 exactly as before and the save never hangs. Bucket + policies applied to ehow + zaap (migration `2026-07-04_safety_photos_storage.sql`). No-regression path + infra verified live; the SKS authenticated round-trip activates only with the Shell JWT (protected by the fallback).
- **Decided:** rows 26/36 (job numbers → Ops) — "Comms is very much a trial now, only worried about ops"; NO Field change (`public.job_numbers` stays local). "Ops" = the in-Shell Quotes replacement (`EqOps → QuotesNative`), not a jobs hub. Linking prompt banked (`task_1a8e00fd`).

## [2026-07-04] v3.5.234–v3.5.235 — Row 21: app_config writes 401 on SKS (leave CC list)
- **v3.5.234 (PR #398)** — `app_config` writes (leave CC list, TAFE holidays) 401'd on SKS (`42501 permission denied`): the table wasn't in `JWT_TABLES`/`JWT_INPLACE_TABLES`, so writes used the anon path where anon has SELECT-only. Two premises in the brief were wrong (verified live): (1) a **DB change WAS required** — RLS was enabled with a SELECT-only policy, so authenticated writes would still fail; (2) the eq tenant is **NOT on the anon path** — it runs the authenticated JWT twin path on zaap, so the global client change had to cover both DBs. Fix: added `app_config` to both JWT sets (client), plus governed migration `app_config_authenticated_write` applied to **both** provisioned DBs (ehow/SKS org `000…002`+tenant `7dee117c…`; zaap/EQ org `a0000000-…-001`+tenant `dcb71d03…`) — authenticated `ALL` policy scoped by org_id + JWT `app_metadata.tenant_id` (acknowledgments/audit_log template), `org_id` column DEFAULT for inserts, service_role parity. RLS-verified on both DBs (correct-tenant writes pass, wrong-tenant blocked, anon gate reads intact). demo-trades/melbourne (anon-only seed orgs in zaap) unaffected.
- **v3.5.235 (PR #400)** — Follow-up: with writes now persisting, the leave CC panel could still show empty because `openLeaveCCConfig()` rendered the in-memory list without re-reading. `loadLeaveCCList()` runs once at `initApp`, so a row written after that (first save this session) or edited by another supervisor showed a stale/empty modal even though the DB was correct. `openLeaveCCConfig()` now re-reads `app_config` on every open and re-renders. Pure client change.

## [2026-07-04] v3.5.225–v3.5.233 — QA sheet (EQ Field 4.7.26.xlsx): all 35 rows worked through
- **v3.5.225 (PR #389)** — Prestart .docx rebuilt to match the SKS template exactly (12 sections); logo + palette + "<TENANT> DAILY PRE-START" title all canonical-driven. Form now captures every section (project#, affects-trades, Controls repeater, 8 tickable Measures Yes/No/NA, Other-Hazards repeater, Permit checkboxes). +6 nullable columns on `public.prestarts` on **ehow AND zaap** (project_number, affects_trades, controls, other_hazards, permits_selected, measures). Row 32.
- **v3.5.226 (PR #390)** — Middle-name approver linking: canonical full legal names never matched the first+last staff index, so leave approvals silently unlinked. `leave-adapter.js nameToStaffId` now indexes + looks up a middle-dropped form both directions (covers leave/timesheets/roster). Rows 7/10/14.
- **v3.5.227 (PR #390)** — Removed 3 redundant buttons: Contacts "⬆ Canonical", Sites "🧹 Clean Up Codes" (also kills the `openCleanupCodes is not defined` console error), Edit-Roster "🖨 Weekly Site Report". Rows 16/17/33.
- **v3.5.228 (PR #391)** — Leave "← Back to Leave" bar on the View-All-Requests list; Contacts now excludes anyone in the Supervision list (email-then-name match) via shared `_peopleExMgrs`/`_contactsCount` in utils.js (always-loaded; badge runs at boot before people.js). Rows 22/11.
- **v3.5.229 (PR #392)** — Labour-hire "DID NOT WORK" pill fills Mon–Fri with `DNW` (added to the **spans renderer** — the 5-col table in timesheets.js is dead-code fallback); Add Person/Contact hidden on SKS via `body.tenant-sks .js-add-person`. Rows 24/37.
- **v3.5.230 (PR #393)** — Supervisor-only "✏ Edit Roster" button bridges the read-only Weekly Roster to the editor. Row 19.
- **v3.5.231 (PR #394)** — Middle-name display sweep across the remaining surfaces (timesheet name col, Contacts card+table, Leave list/table + CC chips); display-only, data keeps full name. Rows 7/14.
- **v3.5.232 (PR #395)** — Site Audit "Project/Site" field is now a canonical site dropdown + free-type (self-contained `_auSiteDatalist`), matching prestart/toolbox. Row 27.
- **v3.5.233 (PR #396)** — Prestart "↺ Use last for <SITE>" fills standing setup (contractor/project#/SWMS/HRCW/Controls/Hazards/Permits) from the most recent prestart at the selected site; not per-day content or crew. Row 28.
- Deferred: Row 29 (auto-fill customer from site — needs the customer name in the Shell-owned `field_sites` view); Row 21 sub-bug (`app_config` writes 401 on SKS — anon lacks UPDATE; route via authenticated JWT, spawned `task_9942e427`); Row 30 (audit talk-to-text). Resolved by verification: row 4 (one "From Roster" button), row 8 (person-wizard moot on SKS now Add Person is hidden), row 23 (spans renderer already preserves scroll). Deliverable: annotated `EQ Field 4.7.26 - outcomes.xlsx`.

## [2026-07-03] v3.5.218–v3.5.222 — SKS QA batch: leave/timesheets/roster/safety fixes
- **v3.5.218 (PR #382)** — leave submit's real error now logged (console + Sentry) instead of a generic toast; person names in Roster/Editor/mobile/batch-fill display "First Last" only (new `shortName()` helper, display-only); removed a duplicate static "Pre-fill from Roster" button on Timesheets.
- **v3.5.219 (PR #383)** — Timesheets "Weekends" toggle now actually shows Sat/Sun columns (was wired to a table renderer superseded by the live "spans" renderer, which never read the toggle at all); Roster no longer shows "(unknown)" staff names on cold boot (staff-map load-order race — `loadCanonicalStaffMap()` moved ahead of the schedule fetch in `loadFromSupabase()`).
- **v3.5.220–221 (PR #384)** — Prestarts: `sks_rep`→`site_rep` client column typo fixed (every prestart save had been failing with PGRST204). Toolbox Talks: migration `toolbox_talks_add_missing_form_columns` applied to ehow — 4 real form fields (Key safety message, Hazards discussed, SWMS references, Next meeting) had no matching DB columns. Site Audits audited, already correct. Leave: pre-check staff_id resolvability before the network call so the specific "no matching staff record" toast survives instead of being overwritten.
- **v3.5.222 (PR #385)** — `showPage()`'s error handling split: a failed lazy-load script vs. a thrown render exception were previously conflated under one misleading label with a blind retry; now reported distinctly via console + Sentry.
- **eq-shell PR #619** (separate repo) — `FieldIframe.tsx`'s tenant auto-select was clearing a deep-linked `?tab=` param before first use; `?tab=person-wizard` and similar deep links now correctly hold instead of falling back to Dashboard.
- Known open issue: person-wizard still renders blank content on a cold `?tab=person-wizard` deep link specifically (works via normal in-app navigation) — root cause not yet found, see `sks/pending.md` 2026-07-03 block.

## [2026-07-01] v3.5.216–v3.5.217 — Canonical edge fn rewrite + URL-per-tab Field side
- **v3.5.216 (PR #380)** — 4 Supabase edge functions rewritten for `app_data.*` canonical schema (ehow compatibility): `supervisor-digest`, `ts-reminder`, `tafe-weekly-fill`, `shift-events`. All 4 deployed to ehow for the first time (were not previously deployed there). `ts_reminders_sent` table created on ehow.
- **v3.5.217 (PR #381)** — URL-per-tab Field side: `showPage()` emits `{ type: 'EQ_TAB_CHANGE', tab: <slug> }` postMessage to Shell on every tab switch; `initApp()` reads `?tab=` from the iframe src and activates the named tab after role routing. Feature is inert until the Shell-side PR lands.

## [2026-06-30] Security — zaap worker-PII anon-grant revoke (no version bump — DB migration)
- **PR #379** (`18b17b8`) — defense-in-depth on the Field data plane (`zaapmfdkgedqupfjtchl`, eq-canonical-internal). `REVOKE ALL FROM anon` on `public.workers`, `worker_credentials`, `worker_inductions`, `worker_assignments`. Migration `supabase/migrations/20260630_zaap_worker_cluster_anon_revoke.sql`, applied live via Supabase MCP (`zaap_worker_cluster_anon_revoke`). DB-only, no app version bump.
- These tables already had RLS on with `auth.uid()`-scoped owner policies (anon got 0 rows; all empty) — the anon GRANT was latent risk only. Now closed-by-default at the privilege layer. `authenticated` (worker self-service) + `service_role` retained; RLS/policies untouched. Verified anon→permission-denied post-apply. eq-shell drift baseline unchanged (tables were never anon-reachable per the drift checker).

## [2026-06-30] v3.5.212 — audit_log: org_id stamp + manager_name fix
- **verify-pin.js** `logAttempt()`: stamps `org_id: TENANT_ORG_UUID` in the POST body. `org_id` is NOT NULL on `audit_log` — the missing field caused every auth sign-in row to 401 silently and be dropped. Guard: skipped when `TENANT_ORG_UUID` is null (fallback deployments keep working).
- **eq-agent.js** `logAgentCall()`: same `org_id` fix. Also renames wrong column `who` → `manager_name` (`audit_log` schema uses `manager_name` throughout — the mismatch caused agent-call rows to also drop). Added `TENANT_ORG_UUID` env var read.

## [2026-06-30] v3.5.207 → v3.5.211 — Canonical wiring sprint (Roster/Teams/Safety/Apprentices/cleanup)
**Built by:** Royce Milmlow + Claude Code
**Sprint covered:** 2026-06-30 (full day, continuation of v3.5.199–206 wiring execution)

- **v3.5.207** — Roster/Leave realtime + Teams canonical wire + worker_id column cleanup. `field_teams`/`field_team_members` views created on ehow (org_id RLS, INSTEAD OF triggers). Realtime publication populated (schedule_entries + leave_requests). `realtime.js` subscribes by canonical base-table name.
- **v3.5.208** — Safety module fully wired for SKS. `prestarts`/`toolbox_talks`/`site_diaries`/`site_audits`/`site_audit_items` granted authenticated CRUD; `site_audits`+`site_audit_items` created on ehow; JWT_INPLACE routing wired; BEFORE INSERT trigger fills tenant_id on the 3 public.* safety tables.
- **v3.5.209** — JWT routing gaps fixed. Bucket-B tables (`job_numbers`, `regions`, `projects`, `project_targets`, `roster_presence`) restored to JWT_TABLES (v3.5.195 regression). `tender_phases`/`nomination_clashes` added; `GRANT SELECT ON nomination_clashes TO authenticated`.
- **v3.5.210** — Apprentice cluster fully wired. 7 new `public.*` tables on ehow (`competencies`, `skills_ratings`, `feedback_entries`, `feedback_requests`, `rotations`, `quarterly_reviews`, `apprentice_journal`); `apprentice_profiles` granted + org_id RLS; 6 electrical competencies seeded; two direct anon-fetch calls in `apprentices.js` replaced with sbFetch.
- **v3.5.211** — Canonical cleanup. `public.pending_schedule` created on ehow (Tender Pipeline Push-to-Roster staging table). `field_schedule`/`field_timesheets`/`field_leave_requests` converted to SECURITY INVOKER (DEFINER with no role grants was silently blocking Roster/Timesheets/Leave). Data tab gated off for SKS (nav-data + ditem-data hidden — import/restore would overwrite canonical data). Dead `worker_id` mirror PATCH removed; `roster_presence` removed from ORG_TABLES.

**Action required (Royce):** update `AUDIT_SB_KEY` in Netlify eq-solves-field to the ehow service_role key so auth audit rows land in `audit_log`.

## [2026-06-30] field_sites honours `active` (archived sites retire from Field)
- `app_data.field_sites` view tightened to `WHERE field_enabled = true AND active = true` (was `field_enabled` only). An archived site (active=false) now drops out of EQ Field even if field_enabled is still true. Applied live to ehow; migration `20260630_field_sites_filter_active.sql` merged via PR #367. Zero rows affected at apply time. Mirror fix for `service.sites` also done (eq-service migration 0163).

## [2026-06-30] v3.5.199 → v3.5.206 — Overnight security audit + canonical-wiring execution
**Built by:** Royce Milmlow + Claude Code
**Security (migrations on ehow):**
- Closed CRITICAL anon read/write/DELETE on live `public.tenders` (366 rows) + the tender cluster — Option A canonical-org (`000…002`) scoping, anon torn down, authenticated CRUD. `field_people` definer→invoker; `job_numbers` hardened; stale `20260618_acknowledgments.sql` neutralised.
- **SKS = Core-only auth** (v3.5.200): standalone PIN gate + whole PIN subsystem retired for SKS.
**Incident fix (v3.5.201–202):** SKS Contacts/roster blanked — `window.TENANT` was never exposed so the canonical adapters couldn't detect the tenant → schedule reads 400 → boot cascade. Fixed (expose `window.TENANT`, adapter allow-list authoritative, per-fetch load resilience).
**Canonical wiring (from the 12-feature audit):**
- v3.5.203 — **#1 unlock:** authenticated CRUD granted on `app_data.schedule_entries/timesheets/leave_requests` (+ `hours_planned` DEFAULT 0) → Roster/Timesheets/Leave write-capable. Job Numbers dead-call fix.
- v3.5.204 — Tender Pipeline enrichment/nominations/phases writes unblocked (`tender_enrichment` hardened + `ORG_TABLES` stamping).
- v3.5.205 — Presence + Supervisor Notes retired for SKS (dead/absent surfaces).
- v3.5.206 — Managers + Sites read-only for SKS (Shell-owned; write entry points gated).
- Digest opt-out (DB migration, no version bump): `field_managers.digest_opt_in` writable via a digest-only INSTEAD OF trigger; 19 supervisors backfilled opted-in.
**Deferred:** Teams wire, Safety grants + create `site_audits`, Apprentices cluster, realtime publication, `user_id` backfill (see `eq/pending.md`).

## [2026-06-26] v3.5.191 — Safety docs: footer parity (page numbers + EQ Solves credit)
**Built by:** Royce Milmlow + Claude Code
**Changes:**
- Footer across all safety `.docx` exports (Prestart / Toolbox / Site Audit) now renders `<label>  |  Page N of M  |  Generated by EQ Solves — Field` using live Word PAGE/NUMPAGES fields (not static text).
- Centralised footer assembly in `buildPackage(opts)` via `opts.footerLabel`; callers (`safety.js`, `audits.js`, `toolbox.js`) pass the document type label. `opts.footerText` kept as a backward-compat alias.
- Helper fns `_fRPr` / `_fRun()` / `_fField()` isolate font/size/colour from the field structs — Arial 7pt #AAAAAA, consistent across all templates.
**Status:** Live on field.eq.solutions (PR #345, merge `673f94f`)

---

## [2026-06-25] v3.5.190 — Safety docs: tenant brand palette (SKS navy)
**Built by:** Royce Milmlow + Claude Code
**Changes:**
- Prestart/Toolbox/Audit `.docx` exports colour from canonical `organisations.branding.palette` ({primary,deep,ice,ink}) instead of hardcoded EQ blue; SKS = navy, tenants without a palette fall back to EQ blue. Read-only consume.
- Shared builder: validated `setPalette()` + `_hex()` + `declaration()` helper + fail-fast guard (`buildPackage` throws if unprimed, commit `7efec20`). Seeded canonical palette for `sks` (navy) + `eq` (blue).
- Suite brand-palette write-path consolidation (Shell/Service) DEFERRED to 2nd-tenant onboard (design banked, shape B).
**Status:** Live on field.eq.solutions (PR #342, merge `c29b292`)

## [2026-06-18] v3.5.163 — Apprentices: fix year level pre-fill on setup (PR #305, merged)
**Built by:** Royce Milmlow + Claude Code

`openSetupProfile` was hardcoding year level to `'1'` before the person lookup. Added one line to read `person.year_level` from STATE.people after the lookup — modal now opens pre-filled to match the contacts card.

---

## [2026-06-18] v3.5.162 — Apprentices: SKS tenant unlock (PR #304, merged)
**Built by:** Royce Milmlow + Claude Code

- 11 apprentice tables created in SKS tenant DB (ehowgjardagevnrluult): `apprentice_profiles`, `apprentice_journal`, `skills_ratings`, `competencies`, `feedback_entries`, `feedback_requests`, `rotations`, `buddy_checkins`, `quarterly_reviews`, `engagement_log`, `checkins`
- `person_id`/`supervisor_id`/`buddy_id` in `apprentice_profiles` adapted to `bigint` (SKS `people.id` = bigint, unlike EQ uuid)
- 11 standard electrical competencies seeded
- `module_entitlements` flipped to `enabled=true` in jvkn for all 11 apprentice modules on SKS org
- GRANT SELECT/INSERT/UPDATE/DELETE on all tables to anon role (captured in migration `grant_apprentice_tables_to_anon`)
- Nav: removed `nav-apprentices` + `ditem-apprentices` from SKS hide list

**Human Recognition context:** Apprentice module is the first full expression of the EQ recognition philosophy — journal (private by default, apprentice-owned), peer acknowledgments, skills growth tracking, feedback on apprentice's terms. Worker-first design verified before SKS unlock.

---

## [2026-06-18] v3.5.161 — Nav: Safety group + hide PIN Management (PR #303, merged)
**Built by:** Royce Milmlow + Claude Code

- Site Audits, Safety (Prestarts/Toolbox), and Safety Report collapsed into collapsible "Safety ▾" group. Auto-expands for SKS tenant.
- PIN Management hidden (`nav-pins`) — individual worker PIN feature is orphaned without the labour hire login tier.

---

## [2026-06-15] v3.5.147 — Canonical worker write (PR #288, merged)
**Built by:** Royce Milmlow + Claude Code

Extends v3.5.146: `_canonicalWorkerUpsert()` creates a stub in jvkn.workers (first_name, last_name, email, phone, role) when no canonical worker exists for the email. SELECT-first prevents duplicates. `syncAllToCanonical()` bulk supervisor action seeds all unlinked people at once. Fire-and-forget throughout — canonical failures never block UI. Deployed 2026-06-15T02:38Z.

**Note:** Stub creation from Field is transition scaffolding. Target architecture has Cards/Shell as the sole creator of jvkn.workers rows. Remove create-path when Cards onboarding is live.

---

## [2026-06-15] v3.5.146 — Canonical worker-link bridge (PR #287, merged)
**Built by:** Royce Milmlow + Claude Code

Phase 2 canonical wiring. `_tryLinkPersonToWorker()` fires on every person save: looks up jvkn.workers by email, patches `people.worker_id` if found. Signature extended to pass name/phone/group. Three call sites wired (modal save, wizard new, wizard edit). Fire-and-forget.

---

## [2026-06-13] v3.5.139 — CSP `_headers` sync + Sentry T3 scrubbing (PR #277, merged)
**Built by:** Royce Milmlow + Claude Code

Sync `_headers` CSP with `netlify.toml` (wildcards, wss://, api.anthropic.com, c.bing.com, R2 img-src, worker-src). Add T3 secret scrubbing in `netlify/functions/_shared/sentry.js` — `EQ_SECRET_SALT`, `AUDIT_SB_KEY`, `RESEND_API_KEY`, `ANTHROPIC_API_KEY` replaced with `[T3:SCRUBBED]` in Sentry error payloads to prevent secret leakage through error reporting. Production commit `068920b`, deployed 2026-06-13T03:16:59Z.

---

## [2026-06-13] eq-shell fix — EQ Service iframe loading (PR #334, merged)
**Built by:** Royce Milmlow + Claude Code

No EQ Field version bump — change is in eq-shell. EQ Service (`core.eq.solutions/sks/service`) was showing "Loading EQ Service…" indefinitely. Root cause: `ServiceIframe.tsx` fallback timer was 12s with a stale OTP comment; TOKEN MODE handshake completes in ~2-3s. Fixed: 12s → 4s + Sentry breadcrumbs. PR #334 merged + deployed 2026-06-13T00:44:57Z.

---

## [2026-06-11] v3.5.125 — SKS canonical DB: full JWT coverage + RLS hardening (PR #267, merged)
**Built by:** Royce Milmlow + Claude Code

SKS Field (`core.eq.solutions/sks/field`) was showing all zeros + permanent loading spinners after the v3.5.120 greenfield cut-over to ehow. Root cause: 7 of 11 `app_data.field_*` views were missing → PGRST205 on every data load.

**DB changes (applied to ehow `ehowgjardagevnrluult`):**
- Created `public.organisations` stub (eliminates 404 boot noise)
- Created `public.site_diaries` table (completes `JWT_TABLES` coverage)
- Created 7 missing `app_data.field_*` views (pass-through, writable)
- Hardened RLS WITH CHECK on all 14 write policies (org_id + authenticated + JWT tenant claim)
- Fixed `audit_log` RLS policies (nspb UUID → correct SKS org_id; SELECT scoped)
- Cleared 109 legacy audit_log rows (clean slate)

**Migration:** `supabase/migrations/20260611_sks_canonical_field_sync.sql` (idempotent)

**Result:** SKS Field dashboard loads. Staff (58) + sites (591) via adapter views. Roster empty — start fresh.

**PR:** [#267](https://github.com/eq-solutions/eq-field/pull/267) — merged, live.

---

## [2026-06-09] v3.5.119 — v8 navy → ink/sky token cleanup — JS stragglers (PR #260, merged)
**Built by:** Royce Milmlow + Claude Code

Swept all remaining `color:var(--navy)` bare inline styles across five JS files that the v3.5.116 v8 CSS pass hadn't touched. Text heading contexts → `var(--ink,var(--navy))`; dollar/stat accent contexts → `var(--sky,var(--navy))`. Backward-compatible fallback pattern throughout (old `--navy` token still resolves on any deploy that hasn't loaded `field-v8.css`).

Files changed: `scripts/apprentices.js` (19), `scripts/auth.js` (1), `scripts/audit.js` (2), `scripts/teams.js` (2), `scripts/sks-pipeline.js` (9 — split treatment). No schema/auth changes.

**PR:** [#260](https://github.com/eq-solutions/eq-field/pull/260) — merged, live.

---

## [2026-06-08] v3.5.100 — Sentry EQ-FIELD-5: complete dashboard lazy-load guard (PR #230, merged)
**Built by:** Royce Milmlow + Claude Code

`siteColor()`, `getSiteName()`, and `isAbsence()` all live in lazy-loaded `roster.js`
but are called from core-loaded `dashboard.js` before `roster.js` loads. Added inline
fallbacks for all three using eagerly-loaded `app-state.js` constants (SITE_COLOR_MAP,
EDUCATION_TERMS, LEAVE_TERMS, STATE.sites). Fixes Sentry EQ-FIELD-5 (`siteColor is not
defined`, seen via `field.sks.eq.solutions`). Pre-empts the next two crashes in the same
render path. Combined with v3.5.99, fully closes the dashboard lazy-load race for all
`roster.js` dependants. No schema/data/auth changes.

**PR:** [#230](https://github.com/eq-solutions/eq-field/pull/230) — merged, live.

---

## [2026-06-07] v3.5.99 — Sentry EQ-FIELD-3 + EQ-FIELD-4: lazy-load ReferenceErrors (PR #227, merged)
**Built by:** Royce Milmlow + Claude Code

**EQ-FIELD-3** `isLeave is not defined` (dashboard.js:77, 15 events, escalating): dashboard
site-count loop called `isLeave()` from lazy-loaded `roster.js` before it loaded. Added
`_isLeave` inline fallback using `LEAVE_TERMS` from `app-state.js` (same pattern as v3.5.84
`updateTopStats` guard).

**EQ-FIELD-4** `auditLog is not defined` (timesheets.js:419): `auditLog()` called unguarded
from 14+ modules; `audit.js` was lazy (Audit tab only). `audit.js` (233 lines) moved to
core-loaded scripts in `index.html`; removed from `TAB_SCRIPTS` to prevent duplicate `let`
redeclare crash. Kills the entire class of auditLog crashes. No schema/data/auth changes.

**PR:** [#227](https://github.com/eq-solutions/eq-field/pull/227) — merged, live.

---

## [2026-06-06] v3.5.86 — Fix team delete (FK violation) (PR #203, merged)
**Built by:** Royce Milmlow + Claude Code

**Summary:** Deleting a team on SKS failed ("Could not delete team"). `deleteTeam` (`scripts/teams.js`) deleted the `teams` row directly, relying on an `ON DELETE CASCADE` that the SKS `team_members → teams` FK doesn't have → foreign-key violation on any team with members (all 6 SKS teams). **Fix:** delete the `team_members` links first, then the team (robust regardless of the FK; people rows untouched). Live-verified `field.sks.eq.solutions/sw.js` = v3.5.86.

## [2026-06-06] v3.5.85 — SSO supervisor mapping (cookie path) + Teams org_id stamping (PR #202, merged)
**Built by:** Royce Milmlow + Claude Code

**Summary:** Two pre-go-live fixes. (1) **Auth** — `verify-pin.js` `verify-shell-cookie` now grants Field `supervisor` to platform admins (parity with `verify-shell-token`); previously the cookie SSO path ignored `is_platform_admin`, so an admin whose tenant-membership role wasn't manager/supervisor landed in **view-only** on the `core.eq.solutions` front door. (2) **Teams** — `teams` + `team_members` added to `ORG_TABLES` (both `org_id NOT NULL`, no default) so `sbFetch` stamps `org_id` on POST; without it, team/member creates 400'd on SKS.

**Companion live DB hardening (same pass, not app versions):**
- **SKS prod `nspbmi`:** added nullable `people.employment_type/rto/hire_company` + `sites.project_id` (EQ Field writes them; SKS lacked them → person/site edits 400'd + silently dropped on the dual-write soak).
- **SKS-canonical `ehow`:** `eq_check/increment_intake_rate_limit` DEFINER fns — pinned `search_path` + revoked EXECUTE from public/anon/authenticated (sole caller = api-intake edge fn on service_role); they had trusted a caller-supplied `p_tenant_id`.
- **Control-plane drift (earlier same day):** `app_data.eq_intake_rate_limits` RLS gate `user_metadata`→`app_metadata` on `ehow` (unblocked eq-shell schema-drift CI).
- Audited safe: 17/19 ehow DEFINER RPCs JWT-scoped; the 4 anon control-plane Cards DEFINER fns are auth.uid()/token-gated.

## [2026-06-06] v3.5.84 — Boot-crash guard: updateTopStats isLeave ReferenceError
**Built by:** Royce Milmlow + Claude Code

**Summary:** `updateTopStats()` (called from `initApp()` on every boot) referenced an undefined `isLeave`, throwing a `ReferenceError` on the EQ tenant at boot. Guarded/fixed so boot stats compute clean.

## [2026-06-06] v3.5.83 — Data carrier: anon fallback fixes SKS gate lock-out on EQ Field (PR #199, merged)
**Built by:** Royce Milmlow + Claude Code

**Summary:** Fixed the cutover blocker where the **SKS tenant on the EQ Field build** (`field.sks.eq.solutions`) showed an **empty "who are you" gate** — nobody could log in. The gate's pre-login name fetch (`sbFetch('people'/'managers')`) hits `JWT_TABLES`, so the carrier tried to mint a data-JWT; pre-auth there's no session → it threw → empty list → lock-out.

**Fix (`scripts/supabase.js`):** `sbFetch` now **falls back to the anon path** when the data-JWT can't be minted (no-session / disabled / tenant-not-provisioned) instead of throwing; `_getDataJwt` latches *stable* failures but never `no-session`, so the JWT path still activates the moment a session exists. Post-login the authed path is unchanged.

**Verified live:** gate now lists **69 SKS names**; `DATA_JWT_ENABLED` is **on**, so post-login SKS reads its own data via the STEP-1 in-place authed policies. Also fixed `melbourne`/`demo-trades` (not in `DATA_TENANT_IDS`) throwing on the JWT path. EQ demo tenants unaffected (SEED gate).

**PR:** [#199](https://github.com/eq-solutions/eq-field/pull/199) — **merged**, live (prod sw.js = `eq-field-v3.5.83`).

---

## [2026-06-06] v3.5.82 — SKS pipeline → authenticated JWT + RLS (B5 Track 2, staged dormant) (PR #195, merged)
**Built by:** Royce Milmlow + Claude Code

**Summary:** Generalised the dormant PIN→Supabase-JWT carrier so the **SKS** tenant can be secured **in-place** (on SKS's own Supabase `nspbmirochztcjijmcrx`) rather than via the canonical `app_data.field_*` twins EQ uses (zaap twins are empty; SKS data is live in its own project). Ships **DORMANT behind `DATA_JWT_ENABLED` (off)** — code is live on eq-solves-field but inert; EQ stays twin-mode, behaviour unchanged.

- **verify-pin.js** — single `ZAAP_JWT_SECRET` replaced by a per-tenant secret resolver (`eq`→`ZAAP_JWT_SECRET`, `sks`→`SKS_JWT_SECRET`, extensible via `TENANT_JWT_SECRETS_JSON`). `signSupabaseJwt()` takes the resolved secret; `DATA_TENANT_IDS` gains `sks → 1eb831f9-…` (= `org_id` on SKS rows).
- **supabase.js** — JWT table rewrite + `app_data` profile header now conditional on `JWT_INPLACE_TENANTS = {sks}`: in-place tenants keep `public.<name>` on their own project + minted JWT; twin tenants unchanged. RPC path guarded.
- **realtime.js** — in-place tenants stream `realtime:public:<table>` (socket already JWT-authed since v3.5.64).

**RLS migration AUTHORED, NOT applied:** `migrations/2026-06-06_sks_pipeline_rls.sql` — `authenticated`-role + tenant isolation (`org_id = jwt app_metadata.tenant_id`; `nominations`/`tender_enrichment` via parent `tender_id → tenders.org_id`), `nominations` supervisor-vs-`confirmed` visibility (the `person_id::text = sub` clause is text-safe + inert under shared-PIN auth), anon revoked on carrier tables, `audit_log` carve-out keeps a narrowed anon INSERT for verify-pin's server logger. Narrows the `rls_policy_always_true` advisor WARNs.

**⚠ Still gated on Royce (SKS LIVE):** apply the migration + add `SKS_JWT_SECRET` to the SKS Netlify site + flip `DATA_JWT_ENABLED=on` — each needs a snapshot + per-action OK. Merging only landed dormant code; nothing touched SKS.

**Live-system note (recon):** the Tender Pipeline IS already promoted to SKS live + populated (CLAUDE.md's "not yet promoted" TODO is stale). SKS carrier tables key on `org_id`, not `tenant_id`. Canonical `organisations.hostname` for `sks` was also repointed to `sks-field.netlify.app` this session so EQ Field resolves SKS at the new host.

**PR:** [#195](https://github.com/eq-solutions/eq-field/pull/195) — **merged**, live (prod sw.js = `eq-field-v3.5.82`). Rebumped 3.5.80→3.5.82 (3.5.81 taken by #196).

---

## [2026-06-06] v3.5.81 — Teams: id-type fix for uuid tenants (PR #196, merged)
**Built by:** Royce Milmlow + Claude Code

**Summary:** `scripts/teams.js` was numeric-id-native, so the whole Teams feature broke on uuid-id tenants (EQ / melbourne / demo-trades): filter pills emitted unquoted uuid ids into `setTeamFilter(...)` (invalid JS), and Manage-Teams member checkboxes used `Number(uuid)=NaN`, so no member could be added. All team/person ids now coerce to strings via a `_sid()` helper before any compare, and onclick handler ids are quoted — works on bigint (SKS) AND uuid tenants; SKS unchanged.

**PR:** [#196](https://github.com/eq-solutions/eq-field/pull/196) — **merged**, live. (A parallel duplicate, #197, was closed in favour of this one.)

---

## [2026-06-05] v3.5.74 — Job number per roster assignment (menu + pin) (PR #187, merged)
**Built by:** Royce Milmlow + Claude Code
Multi-job sites. In Edit Roster, a cell whose site carries >1 job number shows a per-day job pick-list; the supervisor pins which job that person is on. The pin shows under the site code on the roster grid and as "🔢 Job …" on My Schedule, **overriding** the project primary for that cell. Single-/no-job sites unchanged (primary auto-shows, no picker); leave cells none. Resolution per cell: pin (`schedule.{day}_job`) > project primary (v3.5.73) > none. Stores the plain job **number string** — the value direct workers carry into Workbench. **LH/apprentice timesheet auto-fill from the pin deliberately deferred** (next step). DB: `schedule.mon_job…sun_job` (nullable text) on **ktmj.public.schedule** (live) + forward-compat zaap twins. Realtime propagates pins. PR [#187](https://github.com/eq-solutions/eq-field/pull/187) — **merged**, prod sw.js = `eq-field-v3.5.74`.

## [2026-06-05] v3.5.73 — Job numbers on the weekly schedule (PR #186, merged)
**Built by:** Royce Milmlow + Claude Code
Roster grid + My Schedule show a project's job number under each site assignment. **Derived, not entered:** a project links to one row in the Job Numbers list (Projects → edit → "Job Number"), inherited by every site in the project. No `schedule`-table change, no per-cell entry; loose free-text reminder cells untouched. DB: `projects.job_number_id` (nullable, no FK) on **ktmjmdzqrogauaevbktn.public.projects** (the LIVE EQ plane — NOT zaap) + forward-compat zaap twins. PR [#186](https://github.com/eq-solutions/eq-field/pull/186) — **merged**, prod sw.js = `eq-field-v3.5.73`.

**Operating model (captured this session):** the Weekly Roster is the single surface every worker reads. Direct staff book hours in **Workbench**; Field timesheets are a tracking/reconciliation surface (execs reconcile Field vs Workbench). Labour-hire & apprentices are entered into Field timesheets for **invoice reconciliation by accounts**. So the roster job number is the *communicated truth* direct workers carry into Workbench.

> **⚠ Data-plane correction (live > docs):** `ktmjmdzqrogauaevbktn` is still the live EQ read/write plane (12 projects / 48 sites / 11 job_numbers / 605 people / 2417 schedule rows). The zaap `app_data.field_*` twins are **empty**, so the JWT routing in `supabase.js` isn't serving EQ data at runtime — reads/writes hit `public.*` via anon. Any EQ schema change must target **ktmj.public.\*** or `saveX-to-SB` 400s on deploy. This contradicts the Phase-2 "secured on JWT" wording; reconcile before acting on it. **Do NOT pause/downgrade `ktmjmdzqrogauaevbktn`** (a carried-forward `pending.md` action) — it would take EQ Field down.

## [2026-06-04] v3.5.72 — Remove the "Pick a demo tenant" workspace picker (PR #185, merged)
**Built by:** Royce Milmlow + Claude Code

**Summary:** A plain load of eq-solves-field.netlify.app no longer shows the v3.5.18 "Pick a demo tenant" overlay — it boots straight into EQ Field (the default `eq` tenant resolved by `_detectTenantSlug` on the Field host). EQ Field is the front door for tenants now; the tiered demo chooser is gone. Removed the `tenant-picker-overlay` HTML + boot IIFE (index.html) and the `#tenant-picker-overlay` / `.tpo-*` CSS (styles/base.css). Nothing read `__EQ_TENANT_PICKER_ACTIVE__`.

**No loss of reach:** the Advanced/Enterprise demo tenants are still reachable on demand via `?tenant=demo-trades` / `?tenant=melbourne`; the `#sh=` shell handoff is unchanged. Enterprise surface to be built out later.

**Note:** this changelog had drifted — v3.5.60–v3.5.71 shipped without entries here (the in-HTML banner in index.html is the canonical changelog for v3.5+). This entry resumes the log at v3.5.72.

**PR:** [#185](https://github.com/eq-solutions/eq-field/pull/185) — **merged**, live (prod sw.js = `eq-field-v3.5.72`).

---

## Catch-up — v3.5.66–v3.5.71 (compact; in-HTML banner is canonical)

> These six releases shipped without per-version entries here. The canonical,
> full-detail changelog for v3.5+ is the in-HTML banner at the top of `index.html`
> in eq-field. One line each below for narrative continuity:

- **v3.5.71** — Mobile: Staff-home "Team week" read-only crew view + "Who's with me"; My Schedule day cards list the site crew. Ported from SKS v3.10.55. (PR #184)
- **v3.5.70** — Timesheets: education codes (TAFE/TRAINING) only mute the sheet for apprentices, not direct employees; in-place row-stripe + live weekly-stats sync on cell edit. Ported from SKS v3.10.54. (PR #183)
- **v3.5.69** — Resources: "Supervisor" → "Person in charge", now lists Direct employees too; `nominations.capacity_tag` source-tag stops the people/managers id-space collision. Ported from SKS v3.10.53. (PR #181)
- **v3.5.68** — Forecast: "suggest N workers" now divides by a 40-hour work week (was 38), so the hint no longer runs high. Ported from SKS v3.10.52. (PR #178)
- **v3.5.67** — sw.js: "Update available" toast only fires on a genuine update (a prior `eq-field-*` cache existed), killing the first-install nag.
- **v3.5.66** — Design tokens re-vendored to @eq-solutions/tokens v1.3.1 (additive); tenant-tier theming — `applyTenantBranding` sets `data-tier` on `<html>`, Enterprise (melbourne) gets the deeper-teal accent. Mirrors Shell's brand.tsx.

---

## [2026-06-03] v3.5.65 — Sync from SKS NSW Labour v3.10.50–51 (PR #173, merged)
**Built by:** Royce Milmlow + Claude Code
Manual cross-repo port (shared codebase). No DB changes. (1) Timesheets jump-to-top fix (live bug): `renderCurrentPage` split into `_renderCurrentPageDispatch()` + a wrapper that preserves scroll/focus/caret across the rebuild that fires on every realtime echo/poll/post-write refresh. (2) Resources "This week" strip in `sks-pipeline-resource.js`: jobs live · allocated · on the roster · free (non-fatal schedule fetch). Aggregate only.

## [2026-06-03] v3.5.64 — Phase 2 (Goal 1): close anon leak + bucket-B + realtime (PR #172, merged)
**Built by:** Royce Milmlow + Claude Code
REVOKED anon on the 22 migrated `public.*` tables (incl. `public.tenders`) — leak closed, prod anon→401 (edge fns use service_role, unaffected). `public.app_config` left anon (gate reads PINs pre-login → separate auth refactor). Bucket-B secured (field_* twins): job_numbers, regions, projects, project_targets, roster_presence. `realtime.js` repointed to `app_data.field_*` via the data JWT (publication + replica identity full; degrades to poll). Carrier now stamps `org_id` on JWT POSTs (twins keep org_id for composite PKs). Migration: `field_bucketb_realtime_closeleak`.

## [2026-06-03] v3.5.63 — Phase 2 (Goal 1): secure Tender Pipeline + retire 9 dead tables (PR #171, merged)
**Built by:** Royce Milmlow + Claude Code
Tender Pipeline secured onto the JWT (in active use → 323 rows copied into field_* twins; `public.*` kept as fallback): tenders, tender_enrichment, tender_import_runs, tender_review_decisions, nominations, pending_schedule. Dropped 9 dead/empty Field tables on EQ (staff_availability, unavailability, leave_balances, checkins, field_customers, field_waitlist, buddy_checkins, quarterly_reviews, engagement_log). Foreign tables (workers/worker_*/qualifications, organisations) intentionally untouched. Apprentices deferred. Migrations: `field_retire_bucket_d_dead_tables`, `field_secure_tender_pipeline_goal1`.

## [2026-06-03] v3.5.62 — Phase 2 (Goal 1): secure same-shape cutover, first 11 surfaces (PR #170, merged)
**Built by:** Royce Milmlow + Claude Code
Anon-exposure remediation Phase 2, "Goal 1 — secure same-shape": move surfaces off the anon key onto the authenticated data-plane JWT WITHOUT re-homing onto canonical (lossy — canonical app_data.staff/sites aren't supersets; deferred as B5). Each surface = `app_data.field_<name>` (`LIKE public.* INCLUDING ALL` + tenant_id RLS, anon revoked, granted authenticated). people, sites, schedule, timesheets, timesheet_locks, leave_requests, managers, audit_log, prestarts, toolbox_talks, site_diaries. Migrations: `field_secure_homes_phase2_goal1`, `field_secure_homes_org_id_nullable`.

## [2026-06-03] v3.5.61 — Phase 1 auth carrier: data-plane Supabase JWT (PR #168, merged)
**Built by:** Royce Milmlow + Claude Code
Security remediation Phase 1 (carrier only, dormant). verify-pin gains `signSupabaseJwt` + `mint-data-jwt` (signs a per-tenant zaap JWT with `ZAAP_JWT_SECRET`, ~1h TTL); supabase.js gains a dual-mode JWT path (JWT_TABLES, started EMPTY) for app_data access. No surface migrated. EQ app_data tenant_id = `dcb71d03` ("core"). Prod-smoked.

## [2026-06-03] v3.5.60 — revert licence admin (redundant vs canonical worker-home) (PR #167, merged)
**Built by:** Royce Milmlow + Claude Code
Reverted the licence-admin screen — redundant against the canonical worker-home model.

## [2026-06-03] v3.5.59 — Pipeline import: normalise email-form estimators (PR #166, merged)
**Built by:** Royce Milmlow + Claude Code

**Summary:** Estimator dedupe. The Smartsheet 'SKS Estimator' cell sometimes arrives as an email, so one person showed as several filter options (e.g. Matthew Miller / matthew.miller@sks.com.au / Matthew.Miller@sks.com.au). `tender-parser.js` now converts email-form values to name form on import; name-form values left as typed.

**One-time SQL cleanup applied** (collapses existing rows) to EQ `zaapmfdkgedqupfjtchl` + SKS `nspbmirochztcjijmcrx` tenders: `update tenders set estimator = initcap(replace(split_part(estimator,'@',1),'.',' ')) where estimator like '%@%'`. Verified: Matthew Miller→6, Simon Bramall→16, zero '@' estimators remain.

**SKS:** shipped as **v3.10.49** (PR #23), live.

**Housekeeping:** old EQ DB `ktmjmdzqrogauaevbktn` (cold backup since v3.5.50) — Royce chose to pause it, but Supabase only pauses free-tier projects and it's paid. **Action for Royce:** downgrade it to free tier in the Supabase dashboard, then it can be paused / auto-pauses. Not done.

**PR:** [#166](https://github.com/eq-solutions/eq-field/pull/166) — **merged**, live.

---

## [2026-06-03] v3.5.58 — Resources: editing workers/duration rebuilds the labour plan (PR #165, merged)
**Built by:** Royce Milmlow + Claude Code

**Summary:** Closes the v3.5.57 limitation — changing start/workers/duration on a confirmed job saved the numbers but the labour plan (Assign-to-Roster tracks/slots) didn't reflow. `saveConfirmedDetails` now calls `_rebuildLabourPlan`, which regenerates `pending_schedule` from the new numbers. Roster-safe: if any slots were already pushed (`confirmed_at` set) it leaves the plan untouched and the toast warns to adjust manually; clears the plan if start/workers/duration are incomplete.

**SKS:** shipped to standalone repo as **v3.10.48** (PR #22), live.

**PR:** [#165](https://github.com/eq-solutions/eq-field/pull/165) — **merged**, live.

---

## [2026-06-03] v3.5.57 — Resources: edit confirmed-job details; pipeline shows start date (PR #164, merged)
**Built by:** Royce Milmlow + Claude Code

**Summary:** Confirmed jobs on the Resources screen now have an 'Edit details' block — start date / est hours / duration / peak workers / PM / supervisor / notes — so dates/hours can be amended after confirmation. Writes to `tender_enrichment` (+ `nominations`), the same tables the pipeline board reads, so changes flow through. Pipeline cards now also show a Start date tag.

**Changes:**
- `scripts/sks-pipeline-resource.js` — shared `_detailsFields` helper (Needs-Alloc panel + confirmed Edit block); `_editDetailsSection` / `toggleEditDetails` / `saveConfirmedDetails`.
- `scripts/sks-pipeline.js` — Start date tag on cards.
- **Known limit:** structural changes (workers/duration/start) save + warn but do NOT auto-rebuild the labour plan (protects already-pushed roster). Possible follow-up.

**SKS:** shipped to standalone repo as **v3.10.47** (PR #21) — which also carried the estimator/builder filters (the held #20 was superseded/closed). SKS now live with estimator/builder + edit-confirmed + start-date tag.

**PR:** [#164](https://github.com/eq-solutions/eq-field/pull/164) — **merged**, live.

---

## [2026-06-03] v3.5.56 — Pipeline: filter by estimator + builder (PR #163, merged)
**Built by:** Royce Milmlow + Claude Code

**Summary:** Two more header dropdowns on the pipeline board — Estimator (`tenders.estimator`) and Builder (`tenders.client`) — alongside department/vertical, applied together with the value/probability sliders.

**Notes:** No literal 'builder' column; `client` holds the head-contractors (126 distinct). `estimator` has import dupes (e.g. name vs email) that show as separate options until cleaned.

**SKS:** sibling PR sks-nsw-labour #20 (v3.10.46) raised + green, **held** (not merged) pending Royce smoke.

**PR:** [#163](https://github.com/eq-solutions/eq-field/pull/163) — **merged**, live.

---

## [2026-06-03] v3.5.55 — Pipeline: value+probability sliders + Keep/Discard triage (PR #162, merged)
**Built by:** Royce Milmlow + Claude Code

**Summary:** Two pipeline-board features. (1) The value-preset dropdown is replaced by two range sliders — Min value ($, dynamic max from data) and Min probability (%, backed by `tenders.probability_pct`, 0–100). Both apply together; labels update live on drag, filter on release. (2) Keep/Discard triage on every card — user decides (no auto-stale rule yet).

**Changes:**
- `scripts/sks-pipeline.js` — sliders (`setProbFilter`/`lblVal`/`lblProb`), `keepJob` (stamps `tenders.reviewed_at`, card shows ✓ Reviewed), `discardJob` (archives via `tenders.archived_at`, confirm via shared `#modal-confirm`). Buttons stopPropagation.
- **Migration:** `tenders.reviewed_at` (timestamptz, additive/nullable) applied to ktmjmdzqrogauaevbktn (EQ active), zaapmfdkgedqupfjtchl (canonical-internal), nspbmirochztcjijmcrx (SKS live).
- Version bump 3.5.54 → 3.5.55.

**Also shipped to SKS standalone:** sks-nsw-labour v3.10.45 (PR #19, live) — same feature in `scripts/pipeline.js`.

**Flag:** EQ pipeline tenders (333) live in the *original* `ktmjmdzqrogauaevbktn`, NOT eq-canonical-internal (1 row). The v3.5.50 registry flip didn't migrate pipeline data — reconcile before declaring the canonical cutover complete.

**PR:** [#162](https://github.com/eq-solutions/eq-field/pull/162) — **merged**.

---

## [2026-06-03] v3.5.54 — Resources: Remove job confirm fix (BUG-009) (PR #161, merged)
**Built by:** Royce Milmlow + Claude Code

**Summary:** The v3.5.53 "Remove job" button appeared but did nothing — `removeProject()` gated on `window.confirm()`, which is silently swallowed inside the eq-shell iframe and in iOS PWA standalone (returns false), so it bailed with no dialog. Fixed by routing through the shared `#modal-confirm` dialog.

**Changes:**
- `scripts/sks-pipeline-resource.js` — new `_raConfirm()` helper (promise-based, uses `#modal-confirm`, falls back to `window.confirm`); `removeProject()` now awaits it. Same BUG-009 pattern as timesheets/leave/apprentices.
- Version bump 3.5.53 → 3.5.54.

**PR:** [#161](https://github.com/eq-solutions/eq-field/pull/161) — **merged**.

**Note:** Resources (sks-pipeline-resource) remove/archive is being trialled on the **eq** tenant and is intended for **SKS live** once validated — track for the SKS-side merge.

---

## [2026-06-03] v3.5.53 — Resources: remove/archive a job (PR #160, merged)
**Built by:** Royce Milmlow + Claude Code

**Summary:** The Resources (Resource Allocation) screen could add jobs ("+ Add Active Job") but never remove them. Added a **Remove job** action on both Needs Allocation and Confirmed jobs. Shipped to trial on the eq tenant.

**Changes:**
- `scripts/sks-pipeline-resource.js` — `removeProject()` sets `tenders.archived_at` (reversible soft-remove, matching the pipeline "kill" pattern). Job disappears from Resources + Pipeline; roster entries already pushed to `schedule` are left in place. Confirm dialog before archiving.
- Remove buttons added to the Needs Allocation panel footer and the Confirmed labour-curve panel footer.
- Confirmed rows with no labour slots now still open a panel (`_emptyConfirmedPanel`) so they can be removed.
- Version bump 3.5.52 → 3.5.53 (app-state.js, sw.js, index.html banner).

**PR:** [#160](https://github.com/eq-solutions/eq-field/pull/160) — **merged**.

---

## [2026-06-02] v3.5.52 — Licence admin surface (PR #158, merged)
**Built by:** Royce Milmlow + Claude Code

**Summary:** Licence administration panel on the Supervision page — type toggle, expiry reminders, gap alerts, and an admin review gate for imported licences (Phase 3). Degrades gracefully until the migration is applied.

**Changes:**
- `scripts/licence-admin.js` + `migrations/2026-06-02_licence_admin.sql`.
- RLS policies for the licence admin tables.

**PR:** [#158](https://github.com/eq-solutions/eq-field/pull/158) — **merged**.

---

## [2026-06-02] v3.5.51 — Lazy loader dependency fixes
**Built by:** Royce Milmlow + Claude Code

**Summary:** Fixed first-visit lazy-load gaps on the contacts and sites tabs.

**Changes:**
- `lazy-loader.js`: contacts tab now loads managers.js alongside people.js (Add Contact calls a managers.js fn); sites tab now loads roster.js before sites.js (renderSites → getWeekSchedule lives in roster.js).
- `sites.js`: defensive typeof guard on getWeekSchedule().

---

## [2026-06-02] v3.5.50 — eq-canonical-internal live as EQ tenant DB (PR #155, merged)
**Built by:** Royce Milmlow + Claude Code

**Summary:** EQ Field operational data now lives in eq-canonical-internal (`zaapmfdkgedqupfjtchl`). The eq-canonical registry was flipped so all three EQ demo tenants (eq, demo-trades, melbourne) resolve to eq-canonical-internal at boot. eq-solves-field (`ktmjmdzqrogauaevbktn`) becomes cold backup — no data deleted, no code changes required.

**Changes:**
- `migrations/2026-06-02_eq_canonical_internal_schema.sql` — 49-table schema + 5 enums + all indexes + RLS policies applied to eq-canonical-internal (exact mirror of eq-solves-field as of 2026-06-02).
- eq-canonical `organisations` table: `supabase_url` + `supabase_anon_key` updated for eq/demo-trades/melbourne → `zaapmfdkgedqupfjtchl.supabase.co`.
- Netlify `LEAVE_SB_URL` + `LEAVE_SB_KEY` env vars updated on eq-solves-field site → eq-canonical-internal; `approve-leave.js` and `send-email.js` magic-link mode now resolve against the live tenant DB.
- Version bump 3.5.49 → 3.5.50; v3.5.49 banner entry (SW auto-update toast + PIN from app_config) backfilled.

**Note:** eq-canonical-internal starts clean. All new data (roster entries, timesheets, leave requests) writes there. The 605 people + 2417 schedule rows previously in eq-solves-field were also migrated for reference but are not needed — the operational DB is authoritative.

**PR:** [#155](https://github.com/eq-solutions/eq-field/pull/155) — **merged**.

---

## [2026-05-30] v3.5.34 — On-screen chrome is tenant-aware (PR #147, merged)
**Built by:** Royce Milmlow + Claude Code

**Summary:** On-screen counterpart to the v3.5.33 print brand fix. `styles/base.css` used `--navy` (SKS `#1F335C`, `:root`-flagged "no EQ token") as EQ Field's primary on-screen colour in ~30 places — primary buttons, section/modal titles, active pills/tabs, table headers, the EQ Agent panel, the sidebar — so EQ-tenant chrome rendered in SKS navy.

**Changes:**
- `styles/base.css` — one override `body:not(.tenant-sks) { --navy / --navy-2 / --navy-3 }` remaps the navy accent family to EQ deep `#2986B4` for every tenant except SKS, flipping all ~30 usages at once. Dark chrome surfaces (`.sidebar`, `#eq-agent-fab`, `#eq-agent-header`) carved to EQ ink `#1A1A2E` per the design profile (not blue). `:root` untouched → SKS byte-identical (keeps navy).
- Version stamps → v3.5.34 (`APP_VERSION`, `sw.js` CACHE + banner, in-HTML banner).

**Verified:** computed styles on the deploy preview, both tenants — EQ deep accents + ink sidebar/FAB/header; SKS navy throughout.
**PR:** [#147](https://github.com/eq-solutions/eq-field/pull/147) — **merged** (`3f02cc1`).
**Note:** PR #146 was a same-fix duplicate of #145 (print) built concurrently; closed unmerged.

## [2026-05-30] v3.5.33 — Print/PDF brand fix + 3 core features (PR #145, merged)
**Built by:** Royce Milmlow + Claude Code

**Summary:** `styles/print.css` (shared EQ/SKS sheet) hardcoded SKS navy → EQ roster PDFs printed navy. Made the roster `<thead>`, print-header underline, and "Weekly Roster" title tenant-aware: EQ deep `#2986B4` default, SKS navy under `body.tenant-sks` (the class is present in `@media print`, unlike runtime CSS vars). Also shipped the weekly site-attendance report, roster bulk assign/clear, and mobile roster week-swipe. SKS print output unchanged.
**PR:** [#145](https://github.com/eq-solutions/eq-field/pull/145) — **merged** (`509c6a3`). Full detail in `sessions/2026-05-30.md`.

> v3.5.24–v3.5.32 shipped via the in-HTML banner (the canonical changelog for the v3.5.x series per eq-field CLAUDE.md) and are not backfilled here.

## [2026-05-29] v3.5.23 — Phase 1 eq_role wiring (PR #135, pending merge)
**Built by:** Royce Milmlow + Claude Code

**Summary:** All three auth paths (PIN, shell-token, shell-cookie) now derive and propagate `eq_role` to `window.EQ_SESSION.app_metadata.eq_role`, wiring the Phase D slot in `permissions.js` so `EQ_PERMS.getRole()` resolves the full role tier without a DB lookup.

**Changes:**
- `netlify/functions/verify-pin.js` — PIN success path: derives `eq_role` from `role` (supervisor → `'supervisor'`, else `'employee'`); passes as 4th arg to `signToken()`; returns in response body
- `scripts/auth.js` — after successful login on all 3 paths, stores `data.eq_role` into `window.EQ_SESSION.app_metadata.eq_role`
- `scripts/app-state.js` — `APP_VERSION` `3.5.22` → `3.5.23`
- `sw.js` — CACHE `eq-field-v3.5.22` → `eq-field-v3.5.23`; banner bumped
- `index.html` — CHANGES IN v3.5.23 block prepended

**PR:** [#135](https://github.com/eq-solutions/eq-field/pull/135) — **pending Royce smoke test + squash-merge**  
**Preview:** `https://deploy-preview-135--eq-solves-field.netlify.app/`

## [2026-05-19 PM] Project-folder audit (HTML showcase) + stale substrate drafts reverted

**Built by:** Royce Milmlow + assistant

**Context:** Evening Code session after the morning Phase 1.B audit-review merge pass. Royce asked for an overnight interactive HTML audit of every project folder in `C:\Projects\` with brutal-mode ratings, then later asked about "finishing" EQ Shell. The session produced the showcase, drafted a migration plan + `@eq/shell-contract` skeleton, and proposed substrate updates positioning Shell as a "canonical layer" alongside Field-as-lead-build. Pre-flight against actual `eq-shell` repo state revealed the drafts were built on a stale "Phase 1.B in flight" model — reality (verified at evening pre-flight): Phase 1.A + 1.B + 1.B-followup + Phase 2 spike all merged via PRs #1 / #2 / #3, PR #4 open with the handoff runbook, autonomous session in flight on `claude/phase-2-import-screen`. Drafts discarded; this entry captures only what was actually preserved.

**Shipped:**

- `C:\Projects\eq-showcase.html` — single-file interactive audit of 17 project folders + loose files at the C:\Projects root. Brutal-mode ratings (S → F), filterable card grid, EQ Shell hero panel (rated A+ as canonical-layer thesis), three-column verdict (strong / weak / waste), `localStorage`-persisted comment box. Dark gallery aesthetic — `Instrument Serif` headings, `Space Grotesk` body, `JetBrains Mono` annotations. Deliberately ignores EQ brand colours per brief ("ignore EQ design, get creative"). Not committed to any repo — lives at C:\Projects root as a build artefact.

**Reverted (working-tree only, never pushed):**

- 4 edits in `eq-context` (`ops/decisions.md` proposed "Shell as canonical layer" decision entry; `eq/products.md` proposed Shell section; `eq/pending.md` proposed Shell phase items; `eq/changelog/eq-context.md` self-changelog entry) — all `git checkout`-ed back to origin.
- `sessions/2026-05-19.md` — deleted (file was new, untracked).

**Deleted:**

- `C:\Projects\eq-shell-migration\` — entire folder removed (`SHELL-MIGRATION-PLAN.md` + `packages/shell-contract/` skeleton + README). The plan's §1 simplification critique flagged 5 mechanisms as premature for current scale (React.lazy code splitting, 60s HMAC iframe tokens, separate `shell-control` Supabase, three Netlify functions with service-role-key isolation, brand-from-DB at runtime). Reality: all 5 already shipped cleanly in Phase 1.B — the critique was too late to re-litigate. The `@eq/shell-contract` skeleton was unnecessary; Shell is shipping with inline types and the team isn't experiencing the type-drift the package would have prevented. Folder served its purpose as an exploration exercise; not worth preserving.

**Audit-surfaced cull findings (logged here, not yet escalated to PRs):**

- `eq-website/` — 42,647 files, undeployed, last touched April. Either ship to `eq.solutions` via Cloudflare Pages or `rm -rf`.
- `flutter/` — 17,130 files of upstream Flutter SDK clone. Belongs in `~/dev/sdks/flutter/`, not project root.
- `eq-solves-jobs/` — single HTML commissioning page in a folder. Promote to a doc, delete folder.
- `akko-jobsetup/`, `sks-nsw-labour/` — client/staging material in dev workspace. Belongs in OneDrive / client storage.
- `For upload/` — staging entropy. Figure out and delete.
- Stack inconsistency: `eq-cards` is the only Flutter project across the EQ portfolio. Open decision — commit to mobile-first (Cards drives Intake confirm-UI) or kill.
- `eq-analytics-v2` — placeholder `phc_REPLACE_ME` config dormant for 29 days. Provision PostHog (EU) + Clarity accounts or delete folder.

**Decisions punted:**

- Cull execution on the 6 folders above — surfaced only, no PRs opened.
- The Shell "simplification" architectural read from the deleted migration plan — too late to re-litigate, Phase 1.B already shipped the architecture as scoped.
- Whether to formally document "Shell as canonical layer" in `eq/products.md` — deferred until Shell has a real entry shape worth committing. Morning changelog entry already covers Shell work as Field-side; treating Shell as its own product line in substrate can wait until Phase 1.D unblocks and a non-Field module ships under it.

**Look at this first next session:**

- **PR #4 on `eq-solutions/eq-shell`** (`HANDOFF-PHASE-1-A-B.md`) — 3 Royce-only manual handoffs (Netlify env vars, GitHub→Netlify repo link, `*.eq.solutions` wildcard DNS). These are the only thing blocking Phase 1.D smoke test per the morning entry; nothing in the evening session moved them.
- **Active autonomous session on `claude/phase-2-import-screen`** — WIP on `src/modules/tender-pipeline/pages/Import.tsx`, new `lib/`, new `styles.css`, `package.json` changes. Do not touch this branch from a new session unless Royce explicitly confirms it's stale.
- **`C:\Projects\eq-showcase.html`** — review at leisure; the comment box is `localStorage`-only so scratch notes don't leave the browser.

## [2026-05-19] Phase 1.B audit-review merge pass + scope-reduce
**Built by:** Royce Milmlow + assistant
**Context:** Morning review of the overnight build (eq-field-app PR #106 #107 #108 + eq-shell #1 #2) and the overnight audit (eq-field-app PR #108 / [OVERNIGHT-AUDIT-2026-05-19.md](https://github.com/Milmlow/eq-field-app/blob/demo/OVERNIGHT-AUDIT-2026-05-19.md)).
**Merged:**
- `eq-field-app` **PR #106** (Phase 1.C v3.5.9 — Field-side handshake token) — auth-surface, merged as-is after audit verdict LGTM.
- `eq-field-app` **PR #107** (docs hygiene) — placeholder `PR # — fill in after merge` patched to `PR #2` on the branch before merge.
- `eq-field-app` **PR #108** (overnight audit summary doc — `OVERNIGHT-AUDIT-2026-05-19.md`) — preserved as audit-trail artefact on demo.
- `eq-solutions/eq-shell` **PR #1** (Phase 1.B wire-up — shell auth + iframe handoff) — auth-surface, merged as-is per Royce's call. 8 audit should-fixes deferred to follow-up rather than blocking this merge.
**Follow-up PRs on eq-shell (also merged in this session):**
- **PR #3 — Phase 1.B follow-up** addressing all 8 audit should-fixes: timing-safe HMAC sig comparison (`crypto.timingSafeEqual` via `sigsEqual()` helper), display-name stopgap (`user.email.split('@')[0]` so Field sidebar shows `test` not `test@eq.solutions`), structured stdout audit log on every shell-login attempt (`logShellLogin()` helper), DB error message no longer leaked in 500 response body, `last_login_at` update error captured + console.warn'd, `referrerPolicy="no-referrer"` on the EQ Field iframe, `allow-popups` dropped from the iframe sandbox, role mapping comment expanded. 87+/14-, 4 files. Type-checked clean. Merged 2026-05-19. Deliberately defers: `users.name` column migration, rate limiting on `shell-login`, real `audit_log` table, timing-safe HMAC fix on eq-field-app side.
- **PR #2 — Phase 2 spike**, force-pushed (`b302ea7` → `4af3993`) and scope-reduced: branched off post-Phase-1.B main (d822af8), deletes only the 10-line `src/modules/tender-pipeline.tsx` stub from PR #1, and adds the directory tree with 5 lazy-loaded placeholder pages (Import / Kanban / Review / Enrichment / Curve). No App.tsx touch. The audit's auth-bypass risk (the original commit removed `SessionProvider` / `RequireSession`) is eliminated. Merged 2026-05-19.
- **PR #4 — `HANDOFF-PHASE-1-A-B.md`** one-page runbook documenting the three manual steps Royce needs to do by hand before Phase 1.D smoke testing unblocks: set 3 Netlify env vars (`EQ_SECRET_SALT` from eq-solves-field, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`), link `eq-solutions/eq-shell` GitHub repo to `eq-shell` Netlify project, configure `*.eq.solutions` wildcard CNAME + Netlify domain alias. Each step has exact dashboard URLs, copy sources, secret flags, and verification curls. Plus a 4-line smoke test (seed SQL + login + iframe handshake) and a failure-mode reading guide. Also includes a rollback section. Doc-only (197 lines, 1 file). Merged 2026-05-19.
**New-window prompt:** `C:\Users\EQ\Desktop\NEW-WINDOW-PROMPT-eq-shell.md` written 2026-05-19. Successor to NEW-WINDOW-PROMPT-melbourne-ready.md (Melbourne-ready closed out on the Field side). Captures pre-flight, what's-shipped, pending manual handoffs, four next-session paths (A: Phase 1.D smoke; B: Phase 2 proper starting with Import; C: 5 deferred follow-ups; D: NVDA), active parallel work flag (`claude/phase-2-import-screen` WIP), hard rules, auto-merge bar.
**README update (eq-shell main):** companion-infrastructure table refreshed; required env-var matrix added; auth contract documented inline.
**Pending Royce manual handoffs (carried forward):**
- Set Netlify env vars on `eq-shell` project: `EQ_SECRET_SALT` (must match eq-solves-field's value), `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`.
- Link `eq-solutions/eq-shell` GitHub repo to the `eq-shell` Netlify project for auto-deploy.
- Configure `*.eq.solutions` wildcard custom-domain DNS.
- NVDA spot-check on EQ Field v3.5.8 (modal focus + aria-live) — owed since 2026-05-18.
**Status:** EQ Field demo HEAD now includes PR #106 (Field-side shell handshake) — pure no-op on direct visits; activates only when a shell iframe ships a `#sh=<token>` hash. EQ Shell main now includes the Phase 1.B wire-up. Two open PRs (#2, #3) extend that foundation and are awaiting your review. Phase 1.D smoke test unblocks once the three manual handoffs are done.

## [2026-05-18 overnight] Phase 1.B wire-up + docs hygiene + Phase 2 spike
**Built by:** Claude (autonomous overnight run, Royce reviews in the morning)
**Brief:** "EQ Shell" overnight prompt — Phase 1.B + docs hygiene + Phase 2 spike, open PRs only, NEVER merge.
**Branches:**
- `claude/phase-1-b-wire-up` on `eq-solutions/eq-shell` → [PR #1](https://github.com/eq-solutions/eq-shell/pull/1)
- `claude/audit-doc-hygiene-2026-05-18` on `Milmlow/eq-field-app` → [PR #107](https://github.com/Milmlow/eq-field-app/pull/107)
- `claude/phase-2-spike-tender-pipeline` on `eq-solutions/eq-shell` → [PR #2](https://github.com/eq-solutions/eq-shell/pull/2)
**Companion changes (no new infra; uses Phase 1.A's provisioned resources):**
- Supabase migration `2026_05_18_phase_1b_pin_hash_and_service_role_policies` applied to `eq-shell-control` (`hxwitoveffxhcgjvubbd`): adds `users.pin_hash TEXT`, plus service-role-only ALL policies on `tenants` / `users` / `module_entitlements`. HONEST CAVEAT in migration header — not the long-term `auth.uid()` shape; precedent set in `2026-05-13_roster_presence_rls_tighten.sql` + `2026-05-18_tender_rls_tighten.sql`.

**Changes:**
- **Phase 1.B wire-up (PR #1 on eq-shell):** Three TS Netlify functions — `shell-login` (POST email + bcrypt PIN → sets `eq_shell_session` cookie on `.eq.solutions`, signed with shared `EQ_SECRET_SALT`), `verify-shell-session` (GET → hydrates user/tenant/entitlements; 401 on invalid; rejects if cookie tenant_id no longer matches canonical), `mint-iframe-token` (POST → 60s shell-token in the exact shape Phase 1.C's `verifyShellToken` expects). React Router shell: `SessionProvider` hydrates on mount, `RequireSession` guards `/:tenantSlug/*`, `ModuleGate` enforces entitlements per route. `BrandProvider` writes tenant `brand_color` to `--eq-brand` CSS custom property (Q6 lock). `FieldIframe` POSTs to `mint-iframe-token` and embeds `https://eq-solves-field.netlify.app/#sh=<token>`. Cards / Intake / Quotes / Service / Tender Pipeline ship as separate lazy chunks per Q5 (vite build verified). Shared HMAC helpers + lazy service-role Supabase client in `netlify/functions/_shared/`. **Do NOT auto-merge** — auth surface change.
- **Docs hygiene (PR #107 on eq-field-app):** AUDIT-REVIEW.md — moved FINDING #S1 + FINDING #S2 from open to closed with full per-PR breakdowns (PRs #89/#91/#92/#95 for the four phases / three workstreams), added new "Session — 2026-05-18 → 2026-05-19" iteration log entry covering Phase A+B+C+D + EQ Shell pivot + 1.A/1.B/1.C work. SPRINT-PLAN.md — ticked the four "Order to tackle" workstreams as shipped (S1/U2/SEC2/S2), updated U2 + S2 status blocks, added new "EQ Shell" section pointing at `EQ-SHELL-DESIGN.md`. DEMO-VS-LIVE.md — refreshed deploy-snapshot table to HEAD `7249833` post-PR #104, added v3.5.7 → v3.5.9 / EQ Shell Phase 1.C section. ~157 lines net; within auto-merge bar but left open per the brief.
- **Phase 2 spike (PR #2 on eq-shell):** 5 placeholder routes under `/<tenant>/tender-pipeline/{import|kanban|review|enrichment|curve}`, each a `React.lazy()` chunk. Each stub documents the vanilla source line range in `scripts/tender-pipeline.js` (import: 276-540, kanban: 542-750, enrichment: 752-961, review: 963-1455, curve: 1457-1900) + the deps to use during the proper migration. Added Phase 2 stack deps: `@dnd-kit/core`, `@dnd-kit/sortable`, `@tanstack/react-table`, `react-hook-form`. Branched off `main` (NOT off Phase 1.B) so the two PRs are reviewable independently.

**Decisions punted to Royce (morning):**
1. **Netlify env vars on the `eq-shell` project** — must set before functions run: `EQ_SECRET_SALT` (SAME value as eq-solves-field; HMAC handshake breaks if different), `SUPABASE_URL` (`https://hxwitoveffxhcgjvubbd.supabase.co`), `SUPABASE_SERVICE_ROLE_KEY` (from Supabase dashboard — service-role key not readable via MCP).
2. **Netlify ↔ GitHub link on `eq-shell`** — project provisioned empty in Phase 1.A, still not connected. Royce wires after reviewing PR #1.
3. **Logout endpoint on eq-shell** — Phase 1.B's logout button just navigates to `/`; the HttpOnly cookie expires in 7d. Adding `shell-logout` that sends `Set-Cookie: ...; Max-Age=0` is a small follow-up.
4. **Rate limiting on `shell-login`** — same gap eq-solves-field's verify-pin had pre-SEC2 (PR #99). Extend the same `rate_limit_buckets` RPC pattern to this surface in a follow-up.

**Deferred / out-of-scope:**
- DNS for `*.eq.solutions` — per the brief guardrail (no DNS changes).
- NVDA / VoiceOver U2 verification — outside the Claude harness.
- SKS prod ports (S1 / U2 / SEC2 etc.) remain in PR #93 + DEMO-VS-LIVE.md decision matrix; left for explicit Royce instruction.
- Per-user `auth.uid()`-based RLS on the canonical Supabase — waits for the day client-side Supabase access matters (Phase 2+).
- End-to-end smoke (Phase 1.D) — needs Netlify deploy live + env vars set. Royce runs after morning review.

**Status:** Three PRs open, none merged. eq-field-app/demo HEAD unchanged (`7249833`). eq-solutions/eq-shell main unchanged. `eq-shell-control` Supabase has one new migration applied (pin_hash + service-role policies). No version banner / APP_VERSION / sw.js bumps on EQ Field — overnight run touched only the docs files on demo, and the v3.5.9 banner ship is still PR #106 (Phase 1.C). Next session resumes from Royce's morning review of PRs #1, #107, #2 — with env vars set + Netlify GitHub link wired, Phase 1.D end-to-end smoke can run.

## [2026-05-18] Phase D EQ Shell — design locked + Phase 1.A scaffold provisioned
**Built by:** Royce Milmlow + assistant
**Brief:** Phase D of `NEW-WINDOW-PROMPT-melbourne-ready.md` (design pivot per the cowork EQ Shell architecture)
**Branches:** `claude/phase-d-eq-shell-design` (PR #104, merged 13:25Z)
**Companion repos / projects (new):**
- GitHub: [`eq-solutions/eq-shell`](https://github.com/eq-solutions/eq-shell) (private, main branch, Vite + React + TS scaffold pushed)
- Supabase: `eq-shell-control` (id `hxwitoveffxhcgjvubbd`, region ap-southeast-2, EQ Solutions org, $10/mo)
- Netlify: `eq-shell` (id `a3473f83-7c82-4f1e-872d-aa96eaa55172`, milmlow team, `eq-shell.netlify.app`)
**Changes:**
- **Design locked (PR #104):** All 10 architecture questions resolved. EQ Shell is Vite + React + TypeScript, hosted at `*.eq.solutions` on Netlify with a canonical Supabase (`eq-shell-control`) for tenants / users / module_entitlements / branding. Cookie auth on `*.eq.solutions` for React modules; URL-hash HMAC token for the cross-domain EQ Field iframe. EQ Field stays vanilla and embedded via iframe initially; Tender Pipeline migration to React shell-routes is Phase 2 (the wedge); surface-by-surface Field migration is Phase 3+ as each needs rework. Auto-merge bar declined; Royce reviewed + merged manually.
- **Phase 1.A scaffolding provisioned:** Three real-world resources created in one pass — (1) `eq-solutions/eq-shell` GitHub repo (private, default Vite react-ts template plus a real README documenting the design + companion infra), (2) `eq-shell-control` Supabase project in Sydney (Royce confirmed $10/mo cost; canonical schema v1 applied with `tenants` / `users` / `module_entitlements` tables + `_touch_updated_at` trigger function with explicit `search_path = ''` to satisfy the database linter; RLS enabled on all three with no policies yet — deny-by-default until Phase 1.B's auth model lands), (3) `eq-shell` Netlify project on the milmlow team (empty container; needs GitHub integration + custom domain configured via dashboard — manual handoff to Royce per Netlify UI's better DX for these settings).
- **Substrate observation:** the cowork message Royce surfaced mid-session about Tender Pipeline's fortnightly review meeting being "the product, not the screen" reframed Phase D's scope. Adoption signal of "6 fortnightlies + 30 notes at month 3" is now preserved in the design doc as the Phase 2 success metric. Tender Pipeline's existing vanilla implementation (v3.4.79-83) lives on until the React port is shipped + soaked for ~2 weeks — no cutover risk.
**Status:** PR #104 merged to demo. Three new infra resources alive. Phase 1.B (wire-up: shell-login + verify-shell-session + mint-iframe-token Netlify functions + React shell with login + tenant-home + iframe-Field route) is the natural next session. Two open items deliberately handed off to Royce: (1) link the `eq-solutions/eq-shell` GitHub repo to the `eq-shell` Netlify project via the dashboard's auto-deploy integration, (2) configure the `*.eq.solutions` wildcard custom domain DNS. Both are 2-minute UI flows that the Netlify MCP doesn't cleanly cover.

## [2026-05-18] Phase C Melbourne prep — U2 accessibility cleared + Phase D design opened
**Built by:** Royce Milmlow + assistant
**Brief:** `NEW-WINDOW-PROMPT-melbourne-ready.md` (Phase C of 5 + Phase D design pivot)
**Branches:** `claude/v3.5.7-u2-axe-fixes` (PR #102, merged), `claude/v3.5.8-u2-manual-pass` (PR #103 closed → re-opened as PR #105, merged), `claude/phase-d-eq-shell-design` (PR #104 open — design doc only)
**Changes:**
- **v3.5.7 — U2 Phase 2 (PR #102, merged 12:52Z):** axe-core 4.11.4 auto-flagged WCAG 2.1 AA findings against the live demo landing — 23 violations across 2 rules (21 × color-contrast serious, 2 × select-name critical). New text-safe CSS vars (`--green-text` #15803D, `--amber-text` #B45309, `--purple-text` #5B53A8 — brand variables kept for backgrounds and accents). Class-level updates to `.pill-green` / `.pill-amber` / `.stat-card-sub` / `.nav-label` + `.sidebar-footer`. Inline contrast bumps on sidebar dark-navy text (rgba(.32–.4) → rgba(.7–.75)), Pipeline/Trial NEW badges (cyan-500 → cyan-300), Job Numbers/Apprentices BETA badges. `aria-label` on `#globalWeek` and `#dash-group-filter` selects. Re-ran axe-core against the deploy preview — **0 violations**, 21 passes. Behaviour-preserving + additive; qualified for the brief's auto-merge bar but Royce reviewed and merged manually.
- **v3.5.8 — U2 Phase 3 (PR #105, merged 12:53Z; originally PR #103 stacked on #102, GitHub auto-closed when #102's branch was deleted, rebased + re-opened):** the manual-pass portion that axe-core can't catch. `scripts/utils.js` — `openModal`/`closeModal` refactored with `_modalTriggerStack`: stash trigger on open, restore focus to it on close, nested-modal aware (LIFO). `role="dialog"` + `aria-modal="true"` stamped lazily on first open. Tab keydown handler cycles focus inside the top-most open `.modal-overlay` (WCAG 2.4.3 + 2.1.1). Backdrop-click + ESC-to-close route through `closeModal` so focus restore fires. `#toast` in index.html gets `role="status"` + `aria-live="polite"` + `aria-atomic="true"`. NVDA spot-check explicitly flagged as owed to Royce — the one verification step that can't run from the Claude harness.
- **Netlify env-var updates (out-of-PR, Royce-authorised):** set `RATE_LIMIT_V2=on` (functions scope, production context) to activate PR #99's distributed rate-limit RPC path on the EQ Netlify deploy. Then surfaced a pre-existing config bug: `verify-pin.js` reads `AUDIT_SB_URL` / `AUDIT_SB_KEY` env vars but only `LEAVE_SB_URL` / `LEAVE_SB_KEY` had been set — audit logging from the gate function had been silently no-op for some time, and the new `bumpRateLimitRPC` inherited the same short-circuit. Added `AUDIT_SB_URL` + `AUDIT_SB_KEY` env vars (same values as `LEAVE_*`, scope=functions, context=all). Next verify-pin cold start activates both audit logging and the RPC path. Long-term: rename in code to a single source-of-truth name (separate small PR).
- **Phase D design pivot — `EQ-SHELL-DESIGN.md` (PR #104 open):** the brief's Phase D framing (tenant onboarding admin flow inside EQ Field) is materially obsolete. Royce surfaced a different architecture mid-session: EQ Shell at `<tenant>.eq.solutions` hosting Cards / Intake / Quotes / Service / Field as lazy-loaded modules, with a "canonical layer per tenant" managing config + entitlements + branding at the shell layer. Drafted 177-line design doc capturing: ASCII topology, 10 open questions (Q1-Q10) that block code (highest-stakes: Q2 — EQ Field as React port vs iframe vs Web Component embed), proposed MVP shape (3-5 sessions, EQ Field as iframe child initially, canonical Supabase for tenant config only, no wizard MVP), explicit "what this doc does NOT propose". Doc-only PR; Royce reviews + answers Q1-Q4 (the four that unblock everything) before code starts.
- **AUDIT-REVIEW.md / SPRINT-PLAN.md / DEMO-VS-LIVE.md NOT updated** in this PR set — the Phase A+B summary PR #101 already covered through Phase B. A separate hygiene pass (Phase C closures + Phase D pivot recorded) is recommended when convenient; left for a future session to keep these PRs scoped.
**Status:** Demo on v3.5.8 (HEAD = `83cad05`). axe-core auto-flagged WCAG 2.1 AA = 0 violations on landing. Behind-gate surfaces (modal flows, etc.) wired with focus/aria semantics but await NVDA spot-check. Phase D design PR #104 open; awaiting Royce's Q1-Q4 answers before code. Phase E (post-Phase D) not started.

## [2026-05-18] Phase A+B Melbourne prep — security backlog cleared on demo
**Built by:** Royce Milmlow + assistant
**Brief:** `NEW-WINDOW-PROMPT-melbourne-ready.md` (Phases A + B of 5)
**Branches:** `claude/melbourne-scale-verify` (Phase A, PR #97 open), `claude/sec3-tender-rls-rewrite` (PR #98, merged), `claude/sec2-phase-d-rate-limit` (PR #99, merged), `claude/sec1-magic-link-ttl-48h` (PR #100, merged), `claude/melbourne-session-2026-05-18-summary` (this doc-update PR)
**Changes:**
- **Phase A — Scale verification (PR #97 open):** Drove Claude-in-Chrome against `eq-solves-field.netlify.app/?seed500`. Verified live: Contacts virtualisation (498 people / 43 `<tr>` in DOM via `EQVirtualTable`), Edit Roster + Roster view `content-visibility: auto` on 498 rows each, sliding-window helpers wired (`_getVisibleWeekRange` returns 9 weeks), Tender Pipeline `EQ_TENDER_PIPELINE.loadAll()` returns 323 tenders + 12 nominations, mobile home tile flag default-on. Limitations recorded honestly: EQ tenant short-circuits Supabase so live `week=in.(...)` only exercised on SKS port (PR #93); supervisor home variant deferred (requires supervisor unlock). New doc `MELBOURNE-VERIFY-2026-05-18.md`.
- **Phase B1 — FINDING #SEC3 closed (PR #98, merged 11:33:17Z):** New migration `migrations/2026-05-18_tender_rls_tighten.sql`. All 24 placeholder `_anon_*` policies on the 6 tender tables replaced. 4 tables with direct `org_id` (tenders/tender_import_runs/tender_review_decisions/pending_schedule) gated on `org_id IS NOT NULL`. 2 tables without (nominations/tender_enrichment) gated on `EXISTS (tender_id → tenders.org_id IS NOT NULL)`. HONEST CAVEAT in migration header (mirrors `2026-05-13_roster_presence_rls_tighten.sql` precedent): EQ Field's anon-key auth model can't enforce `auth.uid()`-based RLS — cross-tenant read by anyone with the anon key remains structural until Wave 5+ SSO. The brief's prescribed `TO authenticated USING (auth.uid()...)` pattern was a wrong premise; surfaced and adjusted mid-session. Migration applied to EQ Supabase via MCP; app post-tighten still reads 323 tenders + 12 nominations.
- **Phase B2 — FINDING #SEC2 Phase D closed (PR #99, merged 11:33:29Z):** Migration `2026-05-15_rate_limit_buckets_v1.sql` activated — applied to EQ demo Supabase via MCP, RPC sanity-tested (5x true, 6th false), header updated from "DO NOT APPLY" to "Applied 2026-05-18". `netlify/functions/verify-pin.js` wired with env-var feature flag `RATE_LIMIT_V2`: when off (current state), serves the in-memory `attempts={}` path unchanged; when on, distributed `bump_rate_limit` RPC bucket lockout supersedes in-memory (kills the cold-start bypass that was the original finding). Belt-and-braces fallback: RPC blip falls through to in-memory. Tenant derived from request Origin (`sks` / `eq` / `unknown`). New client helper `bumpRateLimit(key, max, windowSeconds)` in `scripts/supabase.js` for future defence-in-depth use. **Activation requires setting `RATE_LIMIT_V2=on` in eq-solves-field Netlify env vars** — not auto-flipped by the merge.
- **Phase B3 — FINDING #SEC1 closed (PR #100, merged 11:33:38Z):** `LEAVE_ACTION_TTL_MS` dropped from `7 * 24 * 60 * 60 * 1000` to `48 * 60 * 60 * 1000` in both `netlify/functions/send-email.js` and `supabase/functions/supervisor-digest/index.ts`. `approve-leave.js` header comment updated to match. Was parked 2026-05-13 with risk accepted; unparked for Melbourne procurement posture. Newly-minted approve/reject links expire after 48h; already-minted links keep their original `exp` until they hit it.
- `AUDIT-REVIEW.md` — session log entry appended; #SEC1/#SEC2/#SEC3 moved to Closed/shipped findings.
- `SPRINT-PLAN.md` — §SEC2 status block updated (Phase D ✅ shipped). §SEC1 in out-of-scope list updated (✅ shipped via PR #100).
- `DEMO-VS-LIVE.md` — Tender Pipeline SEC3 section rewritten (closed), §9 SEC2 section rewritten (closed pending env-var flip), "Risks on live" section updated, deploy snapshot table updated to post-#100 HEAD (`c9cde43`).
**Status:** Phase A doc PR (#97) still open — Royce's call. Phases B1/B2/B3 all merged to `demo`. Phase B GATE passed. `RATE_LIMIT_V2` env var NOT set; Phase D's RPC path is dormant code until that flip. SKS prod unaffected by any of this work — separate rollout decision per finding when Royce calls "SKS live". Phase C (FINDING #U2 accessibility, ~5-6h split across axe-core auto-fixes + manual focus/keyboard/aria-live pass) awaiting green-light. Phase D (tenant onboarding admin flow) is design-first; brief has four open questions (E1-E4) requiring Royce decisions.

## [2026-05-15] SEC2 design — rate-limit-buckets migration file (PENDING)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/sec2-rate-limit-buckets-design` → `demo` (PR #90)
**Changes:**
- New `migrations/2026-05-15_rate_limit_buckets_v1.sql` — `public.rate_limit_buckets` table + `public.bump_rate_limit(p_key, p_max, p_window_seconds)` RPC + RLS denial-by-default (service-role bypass). SQL lifted verbatim from `SPRINT-PLAN.md` §SEC2 per SPRINT-QUESTIONS Q9 default.
- File marked **PENDING** in top-comment header: DO NOT call `mcp__*__apply_migration` / `mcp__*__execute_sql`. Phase D consumes it when server-side role checks land, alongside wiring `bump_rate_limit()` into `netlify/functions/verify-pin.js` (replaces in-memory `attempts = {}` map flagged as FINDING #SEC2).
- `SPRINT-PLAN.md` §SEC2 — status block: Phase 1 ✅ shipped, Phase D ⏳ pending.
- `AUDIT-REVIEW.md` — FINDING #SEC2 moved from Open → Tracked findings with pointer to the migration file.
**Status:** SQL file on demo `migrations/` directory. **Not applied to EQ demo or SKS prod Supabase.** Phase D unblocks the actual fix.

## [2026-05-15] v3.5.3 — S1 sliding-window queries (Melbourne scaling unblocked)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.5.3-s1-sliding-window` → `demo` (PR #89, merge `8890efd`; supersedes closed PR #88)
**Changes:**
- Resolves AUDIT-REVIEW FINDING #S1 (HIGH severity) — the single biggest Melbourne scaling blocker. `schedule?select=*` and `timesheets?select=*` were unscoped; at 577 ppl × 52 weeks (~30k rows) the page load + every 30s poll pulled 5–10MB. Unusable above ~100 users.
- All 5 phases bundled. Phase 1 — `STATE.loadedWeeks = new Set()` + `_getVisibleWeekRange()` helper (9-week window centred on current week). Phase 2 — `loadFromSupabase` + `loadTimesheets` now use `&week=in.(visibleWeeks)`. Phase 3 — `_loadWeeks(weekKeys)` lazy-loads on `onWeekChange` with adjacent ±4 prefetch + inline "↻ Loading…" indicator. Phase 4 — `_evictDistantWeeks()` caps `loadedWeeks` at 16, drops furthest-from-current first. Phase 5 — dashboard investigation confirmed no-op (renderDashboard + updateTopStats both scope to `STATE.currentWeek`).
- Bulk exports split off — `_loadFullDataForExport()` returns un-scoped snapshot; `exportScheduleCSV` pre-fetches via the helper. Single-week exports untouched (already scoped).
- Defaults applied per SPRINT-QUESTIONS: Q1 (±4 weeks / 9 visible), Q2 (always prefetch adjacent), Q3 (bulk-exports full-fetch on demand), Q4 (investigate dashboard first), Q5 (DEMO ONLY — SKS port after 3–5 days clean soak).
- Realtime channel still org-scoped (FINDING #S3 parked) — out-of-window updates dropped client-side; user sees them on next nav to that week.
**Status:** Live on demo. SKS prod (sks-nsw-labour) untouched, still on v3.4.73 — soak clock for v3.5.4 SKS port starts 2026-05-15.

## [2026-05-15] v3.5.2 — Site Reports HUB (collapses Prestart / Toolbox / Diary)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.5.2-site-reports-hub` → `demo` (PR #85, merge `e4985c5`)
**Changes:**
- New `scripts/site-reports-hub.js` — single "Site Reports" sidebar entry lands on a HUB page with three status cards (Prestart · today / Toolbox · this week / Diary · today). Tap-through routes to the existing workflow via `showPage('prestart' | 'toolbox' | 'diary')`. Pre-loads all three caches in parallel on first render so counts are live.
- Three original sidebar entries (Prestart / Toolbox / Diary) **hidden** (inline `style="display:none"`), not deleted — deep-links + v3.5.0 staff home-tile Pre-starts tile still work.
- Count accessors added to each workflow module: `window.eqGetPrestartsTodayCount()`, `window.eqGetToolboxWeekCount()`, `window.eqGetDiariesTodayCount()`. SKS Prestart card suppressed via `TENANT_DISABLED_TABLES.sks`.
- Permissions: HUB always renders. Each card tap-through hits the underlying workflow which already enforces `reports.{prestart,toolbox,diary}.view` via `EQ_PERMS` — no double-gating needed in HUB.
**Status:** Live on demo. Weekly Site Report (next Site Reports milestone, ~6–8 days work) gated on at least one supervisor actually using all three workflows weekly.

## [2026-05-15] v3.5.1 — Mobile-first home tile screen: supervisor variant
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.5.1-supervisor-home` → `demo` (PR #83, merge `c215571`)
**Changes:**
- Phase 2 of the mobile-first nav rollout (Phase 1 was v3.5.0 staff). Supervisors on mobile (viewport <768px, `isManager === true`, `home_screen_v1` flag on) land on a six-tile home screen plus action strip: "Needs you today · N leave to approve · N pre-start". Empty state shows a green "All clear" panel.
- TILES — Schedule, Timesheets, Leave, Pre-starts, Team, Reports. Decision G1: STATUS badges only on tiles (e.g. "New" on Pre-starts) — counts live exclusively on the action strip.
- COG DRAWER — supervisor variant adds Edit roster / Sites / Job numbers / Apprentices / Supervision / Import-Export / Audit log on top of the staff drawer.
- Action-strip data: `window.eqGetPendingLeaveCount()` (in leave.js) + `window.eqGetPrestartsDraftCount()` (in site-reports.js, distinct from HUB's `eqGetPrestartsTodayCount` — different semantics). "Timesheets to review" count **dropped** from MVP — timesheets have no review-state column.
- ROUTING — `initApp()` gets a parallel supervisor branch mirroring v3.5.0 staff. Desktop supervisor (≥768px) or flag-off keeps existing sidebar shell — no regression for the 90% of supervisor work happening at a desk.
- Reuses `home_screen_v1` flag (no separate flag). Draft `_proposals/mobile-first-nav/phase-2-supervisor-home.js` stamped SHIPPED IN v3.5.1 header.
**Status:** Live on demo. SKS sees this on mobile too since flag default-on for both tenants.

## [2026-05-15] Audit + CI chores (no version bump)
**Built by:** Royce Milmlow + assistant
**Branches:** `claude/audit-slash-command` (PR #86, merge `e8ff20c`), `claude/u2-axe-ci-scaffold` (PR #87, merge `a005104`), `claude/audit-session-summary-2026-05-15` (PR #84, merge `067576c`)
**Changes:**
- `.claude/commands/audit-multi-lens.md` (PR #86) — on-demand `/audit-multi-lens` replacement for the dead cloud `/schedule`. Mirrors `REVIEW-MULTI-LENS.md` v1 three-perspective format, produces dated artifact in `_reviews/multi-lens/`.
- `.github/workflows/accessibility-audit.yml` (PR #87) — U2 Phase 1. Manual `workflow_dispatch` (no cron). Tenant dropdown `eq` | `sks`. axe-core CLI via npx; WCAG 2.0/2.1 A/AA; JSON + HTML reports uploaded as artifacts. CI report doubles as procurement-gate documentation.
- `AUDIT-REVIEW.md` Session entry for 2026-05-15 (PR #84) — captures state-of-the-world corrections + schema-correction table for the supervisor home draft.
**Status:** All three merged into demo same session. Axe workflow available to trigger manually any time; no auto-runs.


## [2026-05-14] v3.5.0 — Mobile-first home tile screen (staff role, flag-gated)
**Built by:** Royce Milmlow + assistant (separate session)
**Branch:** `claude/v3.5.0-mobile-home` → `demo` (commits `6fe968c`, `89072b6`, `375a72f`, `b512c84`)
**Changes:**
- New `scripts/home.js` (~362 lines) — mobile-first tile screen for STAFF role. Four tiles: My Schedule, Timesheets, Leave, Pre-starts. Next-shift pill (decision B1). Cog drawer (slide-up sheet) for everything-else nav. PostHog page-view fires from here.
- New `styles/home.css` (~315 lines) — tile grid, pill, drawer, loading skeleton, offline banner. Hidden on viewport ≥ 768px (desktop staff keep existing shell).
- New PostHog flag `home_screen_v1` in `scripts/flags.js`. Default ON as of `b512c84` (after eyeballing the staff flow on phone). Routing fires only when (a) flag enabled (b) `role==='staff'` (c) viewport <768px.
- New `index.html` mount `<div id="page-home">`, `PAGE_TITLES.home`, dispatch in `renderCurrentPage`, routing in `initApp()` to choose home vs schedule landing.
- EQ blue diamond favicons (recoloured from navy `#1F335C` to EQ blue `#3DA8D8` gradient) shipped in same version.
- **v3.4.84 pipeline UI polish FOLDED IN** (commit message confirms): PM/Supervisor dropdowns now pull from `STATE.managers` (was `STATE.people`); Pipeline Dashboard + Review queue Stage/Dept filters; nomination name lookups check managers first then people. The orphan `CHANGELOG-v3.4.84.md` file remained on disk as historical doc; no separate version was published.
- Decisions baked in per `_proposals/mobile-first-nav/MOBILE-FIRST-NAV-PROPOSAL.md` v1.1: A1 (staff mobile only), B1 (next-shift pill), C1 (Pre-starts hidden on SKS via `TENANT_DISABLED_TABLES`), D (labels), E (greeting personality), H1 (greeting once per day then date), I1 (live counts on schedule + timesheets only).
**Status:** Live on demo. SKS prod still on v3.4.73 (flag default-on for both tenants but supervisor variant not in v3.5.0 — Phase 2 in #83).

## [2026-05-14] v3.4.83 — Tender Pipeline: onclick fix + Dashboard + job fields + session close + Promote UX
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.83-pipeline-polish` → `demo` (commit `82123ff`)
**Changes:** Quality-of-life cleanup on the Tender Pipeline kanban: card onclick fixed for some edge cases, dashboard refinements, additional job fields surfaced, review-session close UX clarified, Promote-to-Schedule flow tightened. Pure UX polish — no schema changes.
**Status:** Live on demo. SKS untouched (Tender Pipeline is demo-only).

## [2026-05-14] v3.4.82 — Tender Pipeline: drag-and-drop kanban + Review = decision queue
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.82-pipeline-dnd` → `demo` (commits `0ca5956`, `36bd23e` for the missed changelog)
**Changes:** Drag-and-drop on the Tender Pipeline kanban (stage transitions via DnD). "Review" surface restructured into a decision queue rather than a list. The v3.4.82 changelog commit was missed in the original push (sandbox /tmp path quirk) and landed in a follow-up `36bd23e`.
**Status:** Live on demo.

## [2026-05-14] v3.4.81 — Tender Sync actually working + What's New refresh
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.81-tender-sync-fix` → `demo` (commit `36e4009`)
**Changes:**
- Tender Sync (Excel import) was DOA after v3.4.80 because the cdnjs URL pointed at xlsx 0.20.3 which cdnjs doesn't host. Pinned to xlsx 0.18.5 (last cdnjs-hosted build, same API surface).
- "What's New" banner refreshed — was stuck on v3.4.22-era content (digest, birthdays, timesheet bar). Now surfaces recent shipments: Tender Pipeline, Daily Site Diary, Toolbox Talks. WHATSNEW_KEY bumped to v3.4.81 so every user sees the banner once.
**Status:** Live on demo.

## [2026-05-14] v3.4.80 — CSP hotfix: unblock SheetJS for Tender Sync
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.80-csp-fix` → `demo` (commit `9e7d901`)
**Changes:** Tender Sync (v3.4.79) was DOA on live demo — SheetJS CDN script blocked by CSP. Two CSP definitions live in the repo (`_headers` and inline meta tag); both relaxed to permit the SheetJS cdnjs origin. Real fix but not THE fix — v3.4.81 had to pin the actual cdnjs URL since the original 0.20.3 path 404'd.
**Status:** Live on demo.

## [2026-05-14] v3.4.79 — Tender Pipeline module (new workstream)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.79-tender-pipeline` → `demo` (PR #82, squash merge `b587b78`)
**Changes:**
- New `scripts/tender-pipeline.js` (~1900 lines at ship time, ~2000 after the v3.4.80-84 patches landed) — kanban for tracking tender opportunities through stages (watch → confirmed → likely → won/lost). Drag-and-drop transitions, enrichment slide-over, nomination model, review queue.
- New `scripts/tender-parser.js` — Excel ingestion via SheetJS (xlsx). Parses tender intake spreadsheets into `tender_import_runs` rows. CSP needed v3.4.80 hotfix before this actually worked end-to-end.
- New Supabase migration creating `tenders`, `tender_enrichment`, `nominations`, `nomination_clashes` (view), `tender_import_runs`, `tender_review_decisions`, `pending_schedule`. DEMO ONLY — SKS tenant has these in `TENANT_DISABLED_TABLES.sks` so the fetches no-op.
- New sidebar entries: Pipeline Dashboard, Pipeline (kanban), Fortnightly Review, Tender Sync. Pipeline Dashboard surfaces stage-by-stage counts + filters.
**Status:** Live on demo. Not in any earlier brief — was Royce's mid-week pivot. Five subsequent versions of polish (v3.4.80–84) landed within 36 hours.

## [2026-05-13] v3.4.77 — Site Reports v3: Daily Site Diary MVP (DEMO ONLY)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.77-diary` → `demo` (PR #81, squash merge `ceec471`)
**Changes:**
- New `scripts/diary.js` (~700 lines) — third workflow in Site Reports, sibling to Prestart and Toolbox. Consumes `scripts/site-reports-shared.js` (v3.4.76) for photo / signature / offline-queue controllers; only diary-specific logic remains in this file: weather JSONB, shift_type (day / night / split), repeating sections for work_areas / delays / incidents / visitors, free-text materials_received / equipment_status / notes.
- New migration `2026-05-13_site_diaries_v1.sql` — `site_diaries` table with same RLS + realtime pattern as `prestarts` and `toolbox_talks`. Photos JSONB included from day 1.
- `permission-matrix.js` updated — `reports.diary.{view,create,submit,sign}` added.
- New sidebar entry "Diary" under "Testing (DO NOT USE)", BETA chip, next to Prestart and Toolbox.
- Hub/dashboard restructure DEFERRED again (now three workflows exist — trigger condition reached — but soak first; HUB ships in PR #85 not yet merged).
**Status:** Live on demo. SKS untouched (diary tables not yet applied to SKS Supabase).

## [2026-05-13] v3.4.76 — Site Reports refactor: extract shared photos / signature / queue
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.76-shared-refactor` → `demo` (PR #80, squash merge `306525d`)
**Changes:**
- New `scripts/site-reports-shared.js` (~470 lines) — factory functions extracting the helpers that had been copy-pasted between Prestart (v3.4.69) and Toolbox (v3.4.75):
  - `createPhotoController(config)` — photo upload, list render, captions, lightbox, max-N enforcement.
  - `createSignatureController(config)` — canvas-based signature pad, attendance roster, sign / unsign / clear.
  - `createOfflineQueue(config)` — localStorage-backed write queue with replay listener.
  - `injectMobileStyle(prefix)` — mobile responsive CSS, one-shot per prefix.
- `scripts/site-reports.js` — Prestart drops ~310 lines of duplicated helpers. Keeps Prestart-specific: HRCW categories, crew shape, dual-source notice.
- `scripts/toolbox.js` — Toolbox drops ~290 lines of duplicated helpers. Keeps Toolbox-specific: topic / safety_message / items_reviewed / attendance.
- Refactor lands BEFORE Diary (v3.4.77) so the third workflow starts lean.
**Status:** Live on demo. No schema or behaviour change — purely structural cleanup.

## [2026-05-14] v3.4.75 — Site Reports v2: Toolbox Talk MVP (DEMO ONLY)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.75-toolbox` → `demo` (PR #77, squash merge `66e03a9`)
**Changes:**
- New `scripts/toolbox.js` (~810 lines) — sibling to `scripts/site-reports.js`. Photo / signature pad / offline write queue copy-pasted with `toolbox` / `_tbx` prefixes. Refactor target: extract shared helpers to `site-report-shared.js` once Daily Diary (v3) lands.
- New migration `2026-05-14_toolbox_talks_v1.sql` — `toolbox_talks` table with same RLS + realtime pattern as `prestarts`. Photos JSONB included from day 1 (Prestart needed a follow-up — not repeating).
- `permission-matrix.js` v1.2 — `reports.toolbox.{view,create,submit,sign}` added. Manager + supervisor get all four; employee / apprentice / labour_hire get `.sign` only (mirrors prestart shape).
- New sidebar entry "Toolbox" under Testing (DO NOT USE), BETA chip, next to Prestart.
- Version bump tuple: `index.html` banner + `scripts/app-state.js` `APP_VERSION` + `sw.js` CACHE all → `v3.4.75`. `sw.js` PRECACHE list includes `/scripts/toolbox.js`.
- **Migrations applied 2026-05-14 to BOTH Supabase projects:**
  - `ktmjmdzqrogauaevbktn` (eq-solves-field) ✓
  - `nspbmirochztcjijmcrx` (sks-labour) ✓ — applied per Royce's explicit "SKS live" go so Ben Ritchie can preview via `eq-solves-field.netlify.app/?tenant=sks`

**Schema differences from `prestarts` (deliberate):**
- `facilitator` (not `sks_rep`) — toolbox column names must be tenant-neutral. Prestart's `sks_rep` is a legacy leak not repeated in new tables.
- `meeting_date` / `meeting_time` (not `briefing_date` / `briefing_time`) — toolbox = scheduled meeting, not pre-shift briefing.
- `attendance` (not `crew`) — toolbox audiences include subbies, clients, visitors. Same JSONB shape as `prestarts.crew` so signature pad code is reusable.
- Toolbox-specific fields: `topic`, `safety_message`, `items_reviewed`, `open_actions`, `next_meeting`.

**Why:** Path C absorption (see `ops/decisions.md` 2026-05-13) — second workflow folded in from Ben Ritchie's `sks-field-reports.netlify.app` v29. Prestart shipped as v3.4.69; Toolbox is the second of four (Diary + Weekly to follow). Lessons applied: v3.4.54 per-action inflight guards, v3.4.55 id-coercion via `String()` for tenant-portable PKs, v3.4.56 audit failures surfaced via `console.warn` (offline queue).

**Brief drift caught:** The outstanding-build brief claimed v3.4.69 was demo's tip; reality was v3.4.74. Branch renumbered mid-session from `claude/v3.4.74-toolbox` → `claude/v3.4.75-toolbox`. The `ops/decisions.md` 2026-05-13 entry about demo version-number coordination now has two same-day events confirming the pattern (v3.4.67→v3.4.69 rebase AND v3.4.74→v3.4.75 rename).

**Status:** Live on demo (`eq-solves-field.netlify.app`) post-Netlify-deploy. Hub/dashboard restructure deferred (≥2 workflows now exist but each soaks separately first). NOT deployed to SKS prod (`sks-nsw-labour.netlify.app`) — `main` branch untouched.

## [2026-05-13] v3.4.74 — ESC-to-close on modals (accessibility quick-win)
**Built by:** Royce Milmlow + assistant (Night 1 audit auto-merge)
**Branch:** `claude/audit-night1-all-angles` → `demo` then `main` (PR #73)
**Changes:**
- Global `keydown` listener added in `scripts/utils.js`. Closes only the TOP-MOST open modal per press so confirm-on-top-of-edit stacks peel back rather than blowing both away.
- Behaviour-preserving, <50 lines, no auth / no RLS change — auto-merge bar met.
**Why:** Surfaced by the Night 1 manual audit run (`AUDIT-REVIEW.md`, usability angle, FINDING #U1). Modals already closed on backdrop-click and ✕-button; ESC did nothing — standard keyboard convention violation. First step of a broader accessibility pass needed for Melbourne enterprise procurement (FINDING #U2 covers `aria-*` coverage gap).
**Status:** Live on both demo and SKS prod. 7 other audit findings opened for Royce review (see `AUDIT-REVIEW.md`).

## [2026-05-13] v3.4.73 — widen week-picker so "(this week)" no longer truncates
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.73-week-pill-width` → `demo` then cherry-picked to `main` (PR #69)
**Changes:**
- Removed `max-width:80px` on `#globalWeek`; `<select>` now sizes to widest option (~150px).
- Mobile unaffected — `.topbar-week` still uses `flex:1`.
**Why:** SKS topbar dropdown was cutting "◉ DD.MM.YY (this week)" to "(t...s)" on prod.
**Status:** Live on both demo and SKS prod.

## [2026-05-13] v3.4.72 — skip render when polled data hasn't changed (kills flash)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.72-skip-render-on-unchanged` → `demo` then `main` (PR #67)
**Changes:**
- New `_computeStateSignature()` builds sort-stable signature over people / managers / sites / schedule / timesheets / leaveRequests.
- `refreshData()` diffs post-load signature against last rendered; only calls `renderCurrentPage` on actual change.
- Manual ↻ Sync still renders unconditionally for visual feedback. Signature seeded after initial load so first poll doesn't fake-trigger.
**Why:** Constant flashing on SKS prod — 30-second background poll was doing full innerHTML swap unconditionally, causing scroll jump + focus drop even with no data delta.
**Status:** Live on both demo and SKS prod. Idle background poll is now a silent no-op.

## [2026-05-13] v3.4.71 — remove Project Hours panel + fix EQ→SKS logo flash
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.70-supervisor-fixes` → `demo` then `main` (PR #64; bundled with v3.4.70)
**Changes:**
- Removed `#project-hours-panel` + script tag. Kept `scripts/project-hours.js` (parked) + `sites.track_hours` column on EQ.
- New `earlyBootBranding()` IIFE in `scripts/app-state.js` fires on DOMContentLoaded, detects slug synchronously, applies `TENANT_BRANDING` before first paint.
- `loadTenantConfig` still runs at onload for Supabase-driven access codes; `applyTenantBranding` idempotent so second call just refreshes.
**Why:** (1) Project Hours panel surfaced 'schema not applied' warnings on SKS where the migration hadn't run, added nothing useful. (2) SKS users saw EQ sky-blue logo for 200-600ms before SKS dark-blue snapped in — cause was async `loadTenantConfig()` from `window.onload` despite branding data being static per tenant.
**Status:** Live on both demo and SKS prod.

## [2026-05-13] v3.4.70 — supervisor dob/start_date + Excel date import + archive
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.70-supervisor-fixes` → `demo` then `main` (PR #64)
**Changes:**
- `migrations/2026-05-13_managers_dob_start_date_archived.sql` adds `dob_day`, `dob_month`, `start_date`, `archived` on `managers`; `archived` on `people`. **Applied to BOTH Supabase projects on 2026-05-13.**
- `import-export.js`: `_parseCsvBirthday` now matches DD/MM/YYYY; new `_parseStartDate` handles ISO + DD/MM/YYYY + Excel serial numbers.
- Supervisor modal exposes DOB + start_date. Both filter rows get "Show archived" toggle. Active/archived render-tint + handlers wired in `managers.js` / `people.js`. Badges count active rows only.
- `supabase.js`: `saveManagerToSB` sends new columns; `savePersonToSB` sends `archived`; new `archiveManagerInSB` + `archivePersonInSB` helpers via PostgREST PATCH.
**Why:** Royce CSV review 2026-05-13 surfaced: supervisors had no DOB/start_date (people had since v3.4.16), Excel uploads rejected DD/MM/YYYY + serial dates, no reversible archive (only hard delete via `deleted_at`). Contacts↔Supervisors double-up confirmed by design (Wave 4).
**Status:** Live on both demo and SKS prod. Behaviour-preserving for existing rows.

## [2026-05-13] v3.4.69 — Site Reports module + Prestart MVP (DEMO ONLY)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.67-prestart` → `demo` (PR #62) — rebased on top of v3.4.68 role-system, so the branch name keeps the original v3.4.67 label but the merge ships as v3.4.69. v3.4.67 was never released.
**Changes:**
- New "Site Reports" sidebar entry under "Testing (DO NOT USE)" section with BETA chip. v1 ships Prestart only — toolbox / diary / weekly follow the same pattern.
- Photos: max 8 per record, camera+gallery on mobile, resized to 1600px / JPEG-q70, stored inline as base64 in `prestarts.photos` JSONB. Lightbox + captions.
- Signature pad: HTML5 canvas modal, touch + mouse, DPR-aware. Saved as base64 PNG into `crew[i].signature_image`; idempotent re-tap preserved (v3.4.54 lesson).
- Offline write queue: `navigator.onLine` + try/catch around `sbFetch`; localStorage-backed queue replays on `'online'` event + page load. Per-tenant scoped. Visible pending pill in form footer.
- Mobile responsive: form grid collapses to 1 column < 640px; modal goes full-screen; signature canvas bumps to 260px for finger signing.
- Dual-source notice: dismissible yellow banner directing users away from `sks-field-reports.netlify.app`.
- **Migrations applied 2026-05-13 to BOTH Supabase projects:**
  - `2026-05-13_site_reports_v1.sql` — `prestarts` table + RLS + realtime
  - `2026-05-13_prestarts_photos.sql` — `ADD COLUMN photos jsonb`
**Why:** Path C absorb (see `ops/decisions.md` 2026-05-13) — workflows from Ben Ritchie's `sks-field-reports.netlify.app` v29 fold into EQ Field as a commercial sub-module. Prestart is the first of four (Toolbox / Diary / Weekly to follow). Lessons applied: v3.4.54 per-action inflight guards, v3.4.55 id-coercion for bigint/uuid PK portability, v3.4.56 audit failures surfaced via `console.warn` not silenced.
**Status:** Live on demo only (`eq-solves-field.netlify.app`). NOT deployed to SKS prod — gated on Ben Ritchie sign-off + Royce explicit go. 5 modified, 3 new files, ~1130 line diff.

## [2026-05-13] v3.4.68 — Phase B + C role system foundation (DEMO ONLY soak)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/v3.4.68-role-system-clean` → `demo` (PR #63)
**Changes:**
- `scripts/permissions.js`: new `resolveSessionRole()` (Phase C).
- Call wired into `initApp()` + supervisor PIN unlock + lock-out.
- 5 handler gates migrated to `EQ_PERMS.can()` (Phase B v1):
  - `leave.js`: `respondLeave` / `archiveLeaveRequest` / `unarchiveLeaveRequest`
  - `timesheets.js`: `fillTsWeekFromMon` / `sendTsReminder`
- All 5 perms behaviour-preserving in both supervisor + manager tiers.
- Phase A schema applied to BOTH Supabase projects on 2026-05-13.
**Why:** Royce flagged Phase B+C risk on SKS prod; chose to ship to demo this week for a 5-7 day soak before porting. PIN-unlock-wins rule preserves today's behaviour — anyone with the supervisor PIN keeps full supervisor access regardless of DB role. Phase D will tighten this server-side later (~2 weeks, planned early June).
**Status:** Demo only. SKS stays on `isManager` binary model until demo soak passes. Plan ref: `MELBOURNE-SCALE-DESIGN.md §7 Q3`.

## [2026-04-28] Add Contact button cherry-picked to main (SKS) — PR #25
**Built by:** Royce Milmlow + assistant
**Branch:** `fix/add-contact-main` → `main` (merge commit `4f03227`,
cherry-pick of `f372a43` from demo)
**Why:** Same repo Milmlow/eq-field-app; demo branch deploys to
eq-solves-field.netlify.app (EQ Field demo), main branch deploys to
sks-nsw-labour.netlify.app (SKS LIVE — ~55 staff). The button only
shipped to demo via PR #24, so SKS staff didn't get it. Cherry-pick
brings just that one-line UX fix to main without dragging the rest
of Phase 1 (flags, perms, project-hours, role enum) onto SKS.
**Status:** Merged. Netlify auto-deploy to sks-nsw-labour.netlify.app
in flight at 2026-04-28.

## [2026-04-28] Add Contact button wired into Contacts page (PR #24)
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/hopeful-wright-058c8b` → `demo` (merge commit `5105517`)
**Changes:**
- `index.html` page-contacts filter row gets a "＋ Add Contact"
  button calling existing `openAddManager()` (managers.js:109).
  No new code paths — reuses the existing modal-manager + saveManager
  flow that already lived on the Supervision page.
- Both demo (SEED) and live (eq) tenants get the button — `managers`
  is in `ORG_TABLES`, not in any `TENANT_DISABLED_TABLES` entry.
- One-line diff to a single file. No JS changes, no migration, no
  permission shape change.

**Why:** The page-contacts page (nav: "Contacts" ◉) showed staff/people
but lacked an Add affordance — anyone looking for "where do I add a
contact" landed there and saw nothing. Add button only existed on
page-managers (nav: "Supervision" ☎). UX parity fix.

**Status:** Live on eq-solves-field.netlify.app post-Netlify-deploy
(~1 min after merge).

## [2026-04-27] Phase 1 implementation kickoff — flags, perms helper, migrations
**Built by:** Royce Milmlow + assistant
**Branch:** `claude/hopeful-wright-058c8b` (not merged to demo — awaiting review)
**Changes (5 commits past `0145c78`):**
- `e9b4706` — `scripts/flags.js` PostHog feature-flag wrapper exposing
  `window.EQ_FLAGS.isEnabled()` + `variant()`. Safe defaults, no-op until
  a flag is created in the EQ PostHog project (`phc_zXpRxm6Q…`).
- `f2d0e91` — `scripts/permission-matrix.js` + `scripts/permissions.js`.
  Matrix v1 embedded as static JS; `window.EQ_PERMS.can(permKey)` reads
  the current role.
- `8b6bdb1` — Two SQL migrations written (NOT applied):
  - `migrations/2026-04-27_sites_track_hours.sql` — `track_hours` boolean
    + `budget_hours numeric` on `public.sites`
  - `migrations/2026-04-27_eq_role_enum_people_role.sql` — `eq_role`
    Postgres enum + `people.role` column with manager-table backfill
    pattern. Header includes verification queries to run before applying.
- `b367eb1` — `EQ_PERMS.getRole()` reads `window.isManager` as primary
  today-path role signal (durable for page lifetime), falling back to
  sessionStorage flags. Plan revised: 97 `isManager` references across
  `scripts/`/`index.html` rules out a wholesale refactor — strangler
  pattern instead, migrate opportunistically when touching files.
- `89f96dc` — `scripts/project-hours.js` + placeholder div before
  `</body>`. Self-mounting "Project Hours" burn-down panel — activates
  only when `feat_project_hours_v1` flag is on AND `EQ_PERMS.can('ph.view_dashboard')`
  is true. Renders per-site Budget / Used / Remaining / % used with
  colour treatment (sky / amber / red). Graceful states for "migration
  not applied yet", "no tracked sites", and network errors. Client-side
  aggregation over timesheets for v1.

**Next manual steps required (Royce):**
- Create `feat_project_hours_v1` flag in EQ PostHog project (default off,
  cohort = your `distinct_id` only)
- Apply both migrations to `ktmjmdzqrogauaevbktn` via Supabase MCP /
  Studio after running the verification queries in the role-enum header.
  Do NOT apply to `nspbmirochztcjijmcrx` (SKS live).
- Open PR `claude/hopeful-wright-058c8b` → `demo` when ready to merge.

**Status:** Code shipped to feature branch only. No Netlify deploy. No
Supabase changes. SKS Labour untouched.

## [2026-04-27] Multi-tenancy + dev-workflow plan locked (planning only, no code shipped)
**Built by:** Royce Milmlow + assistant
**Changes:**
- Living plan document captured at
  `eq-solves-field/.claude/worktrees/hopeful-wright-058c8b/MULTI-TENANCY-PLAN.md`.
- Three strategic decisions locked:
  - Sprint scope = Phase 1 only (PostHog flags + project-hours feature + 5-tier
    role system). Phase 2 deferred to first self-serve trial signup OR ~3
    customers manually provisioned.
  - Tenancy lives inside `ktmjmdzqrogauaevbktn` only; SKS Labour
    (`nspbmirochztcjijmcrx`) untouched.
  - Auth: Supabase-native JWT minted in `verify-pin.js` with
    `app_metadata.tenant_id` and `app_metadata.eq_role`; PIN UX preserved.
- Tenant URL convention locked: `eq.solutions/field/<slug>/`. Path-based slug
  resolution, single shared Netlify site, no subdomains.
- 5-tier role system designed (`manager > supervisor > employee > apprentice >
  labour_hire`) with `eq_role` Postgres enum and `people.role` column.
- Single PIN per tenant on `organisations.tenant_pin`; per-role PIN env var
  pattern dropped.
- Permission matrix HTML built at
  `eq-context/eq/field/permissions/permission-matrix.html` plus v1
  JSON snapshot at `permissions-by-role-v1.json` (manager 56 / supervisor 36 /
  employee 13 / apprentice 17 / labour_hire 5).
- First PostHog flag designed: `feat_project_hours_v1` gates new project-hours
  burn-down feature with `sites.track_hours` + `sites.budget_hours`.

**Status:** Plan complete. No code touched. Phase 1 implementation pending
explicit Royce go-ahead.

## [2026-04-05] Demo Mode, Seed Data and Network Error Suppression
**Built by:** Royce Milmlow + assistant
**Changes:**
- Demo mode implemented - bypasses Supabase auth when tenant slug is eq
- 18 generic staff, 7 generic sites, 5 weeks of schedule seeded
- Network error toasts suppressed in demo mode
- Cowork guardrail issue documented
**Status:** Live on eq-solves-field.netlify.app (demo branch)

## [2026-04-05] Cloudflare Pages Deployment Architecture Locked
**Built by:** Royce Milmlow + assistant
**Changes:**
- Deployment architecture confirmed and locked
- Rule: never cross-deploy between targets
**Status:** Architecture documented

## [2026-04-04] Redundancy and Failover Gap Assessment
**Built by:** Royce Milmlow + assistant
**Changes:**
- Full infrastructure assessment across Netlify, Supabase, Resend, GitHub
- Gaps identified: Supabase single point of failure, no backups, no tagged release
**Status:** Gaps identified - NOT yet resolved

## [2026-03-31] White-Label Commercialisation Review
**Built by:** Royce Milmlow + assistant
**Changes:**
- EQ Field Ops commercialisation roadmap built (85-item Excel workbook)
- White-label conversion estimated at 2-3 hours
**Status:** Planning complete - not yet executed

## 2026-07-11
- v3.5.299 (PR #455) — Sidebar: hide the orphaned "Pipeline" section header in employee view. The section wrapper was ungated while all three children (Pipeline/Resources/Accounts) are manager-only, so employee logins saw an empty "Pipeline" label. Marked `#nav-section-pipeline` `.edit-only` + added a matching `.nav-section.edit-only` CSS rule. Live.
