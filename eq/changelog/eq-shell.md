# eq-shell changelog

## 2026-07-02
- Maps address autocomplete **verified working live end-to-end** (browser, core.eq.solutions/sks Add-site): typed address → New Places dropdown → Suburb + State auto-fill. Correction to the #600/#596 notes below: `VITE_GOOGLE_MAPS_KEY` was NOT set before this session — live `getEnvVars` on eq-shell (and all 9 EQ/SKS sites) showed no maps/places key; set it this session via `netlify api createEnvVars` (context=all, non-secret). The #600 migration + this key together are what made it work.
- PR #603 (merged + deployed + verified live): fix first-open mount race in `useGooglePlacesAutocomplete` — `loadScript` polls `google.maps.importLibrary` readiness instead of a one-shot `load` event a re-mount can miss (widget silently didn't appear until the modal was reopened on a fresh page load). Verified in-browser: on a fresh page the widget now mounts on the first Add-site open.
- PR #602: pending-count badge on the Admin-hub "Number reuse checks" tile (via `eq_list_recycle_reviews`) so held recycled-phone signups surface at a glance instead of piling up unseen. Best-effort fetch — a failure/empty just renders no badge.
- PR #600: address autocomplete migrated from the legacy `google.maps.places.Autocomplete` (un-enableable on the 2026 GCP project — Google only offers "Places API (New)" on new projects) to `PlaceAutocompleteElement` + CSP `places.googleapis.com`. This was the REAL root cause of the blank Suburb/State — not the key (set 2026-07-01) or the loader (#596); the legacy widget simply can't run on the new project. Supersedes an error-surfacing attempt (branch `claude/maps-autocomplete-surface-errors`, dropped as redundant).
- PR #598: new admin screen "Number reuse checks" (`NumberReviewsPage` at `/admin/number-reviews` + Admin-hub tile), gated `admin.list_users`. Surfaces `shell_control.identity_recycle_review` (recycled-phone signups held by the 90-day guard) so a manager can approve (grant the prior account's access) or reject (keep separate) via `eq_list_recycle_reviews`/`eq_resolve_recycle_review`. Empty until a >90-day-stale number is reused. Part of Track B (worker-identity resolver).
- PR #597: create-worker-invite Netlify fn routed through `eq_cards_find_or_create_worker_for_invite` (normalised phone OR email match, prefers a claimed row, else creates) instead of an exact-phone lookup that missed 46/73 local-format stubs on jvkn and 406'd on a shared phone. Depends on eq-cards migration 0073 (applied to jvkn same day). Part of Track B.
- PR #596: shared `useGooglePlacesAutocomplete` hook — the Add-site modal now loads the Google Maps script itself instead of only attaching when `window.google` already existed (which left Suburb/State blank on a fresh page load). Both Add-site and Edit-site forms use the hook. `VITE_GOOGLE_MAPS_KEY` was already set (2026-07-01, production context); this loader bug — not a missing key — was the real cause of the blank-address report.
- PR #594: worker onboarding — mobile-only phone normaliser (rejects landlines, the root cause of duplicate worker stubs) across `_shared/phone.ts` + 4 auth doors + `LoginPage` + new `phone.test.ts`; `confirmed_staff_id` tenant/active guard in `cards-approve-staff`; collapsed the three admin worker doors into one "Add workers" surface (QR self-serve + connect-by-phone), retired the name+phone create-worker form (the stub-minter), nav "Worker invites" → "Add workers". Model: worker owns their Cards identity, employer only asks. Also cleaned the live Anthony Hartley duplicate (soft-deleted the landline `app_data.staff` row on ehow).
- PR #595: Access Control "Recent activity" panel — reuses previously-dead-code `admin-audit.ts` (added optional `prefix` filter + `checkShellOrigin`) to show `access.*`/`security_group.*` events in plain English at the bottom of `/admin/access-control`
- PR #591: profile settings page removed — `ProfileSettings.tsx`, `netlify/functions/update-profile.ts`, route `settings/profile`, and "Your profile" sidebar link all deleted; names are admin-managed via Staff page
- PRs #590/#592/#593 merged (sequential rebase; #592 worktree conflict resolved by rebasing from `.claude/worktrees/objective-bell-bc744d`)
- PR #593: `0154_assets_delete_attribution_guard.sql` — `BEFORE DELETE` trigger on `app_data.assets` blocking hard-deletes with no PostgREST request context (JWT/headers), with an explicit `SET LOCAL app_data.allow_direct_delete = 'on'` override for reviewed migration-time bulk deletes. Root-caused the 2026-07-01 unattributed 13-row delete to a hand-run direct-SQL cleanup mid-migration-session (falls between the 0164/0165 migration-apply timestamps on ehow), not any app/cron/script. **Deployed and verified live 2026-07-02** — `tenant-migrate.yml` dispatched with `allow_checksum_drift=true` (unrelated pre-existing drift on `0072`/`0084`), approved through the `production` environment gate, `guard_assets_delete` confirmed enabled on both ehow and zaap.
- PR #590: Access Control security sprint — blocked admin/audit perm-key escalation in role overrides (`OVERRIDABLE_PERM_KEYS` allowlist), added `checkShellOrigin` CSRF guard (report-only) to `security-groups.ts`/`tenant-role-perms.ts`/`admin-tenants.ts`/`cards-export-licences.ts`/`comms-jobs.ts`, fixed un-awaited audit-log writes, fixed permission-preview panel to include live `tenant_role_overrides`
- PR #592: equipment table "Assigned to" column gets an inline dropdown (editors only) for reassigning custodians without opening the detail drawer; drawer button relabelled "Reassign custodian" → "Assign to staff member"
- Data recovery: 13 `app_data.assets` (plant_equipment) rows on ehow/SKS restored from `audit_log.old_record` after an unattributed direct-SQL delete on 2026-07-01 — not a code change, noted here for the record
- PR #589: ARMADA lighthouse budget bump (`maxIssuesPerRun` 3→6, `maxRuntimeSec` 300→600, `maxFindings` 20→30). Config-only, no code change. Daily 8am scheduled lighthouse task added, routed through the main checkout to avoid the worktree skill-resolution gap.
- PR #588: token lint ratchet (no-restricted-syntax warn→error); 24 legacy file-level eslint-disable markers; `staff-resync-licences.ts` endpoint; SplitPanel "Re-sync from Cards" button
- PR #587: `worker_dedup_archive_20260630` RLS lockdown on jvkn
- PR #586: semantics pass — raw semantic hex → CSS token vars
- PR #585: StaffPage Phase E — MatrixView/SplitPanel extracted to `src/pages/staff/`

## 2026-07-01
- PR #584: PDF import fixes — real spinner + auto-apply default markup on both paths
- PR #583: GM Reports forecasts tab — per-job "Mark done" self-report
- PR #582: Warm Sand mobile chrome (MobileTabBar/Drawer + App/comms/gm-reports/CoreHome CSS)
- PR #581: Warm Sand repo-wide neutral hex → --eq-gray ramp (242 files, 21 components)
- PR #580: Warm Sand StaffPage pilot
- PR #579: Sentry fixes — approval dedup upsert, CardsIframe load-timeout race, PDF fetch catch
- PR #578: StaffPage Phase D — staffLib.ts pure logic + 9 tests, suite 85→94
- PR #577: Cert import background fn async → sync payload fix
- PR #576: PostgrestBuilder type fix (as unknown as)
- PR #575: Training matrix — filter by employment type, sort columns, multi-select, column width fixes
- PR #573/571: URL-per-tab Shell side (buildFieldSrc tab param + FieldIframe postMessage)
- PR #572: Remove dead cert-import-parse.ts
- PR #570: Google Maps key prefix fix + dead Sentry fallback removed
- PR #569: Invite-path rejection email (worker notified on admin reject)
- PR #568: Pending connections — worker rejection email + rejection reason on org_access_requests
- PR #567: Blank worker name fallback from app_data.staff by phone
- PR #566: iOS CSS spinner fix (will-change: transform on @keyframes rotate)
- PR #565: Training matrix full licence names + mobile polish
- PR #563: Cert import 500 root-caused + fixed (async payload wall → sync upload + background JSON)
- PR #560: EQ Ops — age badge, attachment types (supplier_quote/drawing/quality_doc), migration 0152
- PR #559: Real CI gate (tsc+test+lint on PRs) + auth-hub test suite (66→85 tests)
- PR #557: Training matrix licence numbers + CSV export + employment-type select
- PR #556: Signed URL TTL raised 1hr → 7 days
- PR #555: field_teams RLS view fix (42809 — views can't ENABLE RLS; no-op replacement)
- PR #553: Audit log — team/access events + link-event name resolution + stub-match block
- PR #552: Training matrix licence numbers + CSV export (merged after drift check fix)
- PR #551: Actor coverage — update-data-activation + asset-calibration use audited client
- PR #549: Issues/Attachments Phase 1 — issues table, RPCs, index, bucket private, signed URLs

## 2026-06-30
- PR #547: Tenant Activity Log link-event triggers (contact_customer_links/contact_site_links)
- PR #543: ShellHandoffClaims adopted; runtime validation on service-mint path
- PR #539: Tenant Activity Log MVP (0146, audit_log, writeTenantAudit helper)
- PR #537: Contacts UX overhaul — inline delete for sites + contacts
- PR #534: Cert import async rework (background fn + Blobs polling)
- PR #562: Brand-hex burndown phase 1 — 105 brand hexes → CSS vars (19 files)
