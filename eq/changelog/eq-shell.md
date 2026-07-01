# eq-shell changelog

## 2026-07-02
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
