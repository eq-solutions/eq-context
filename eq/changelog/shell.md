---
title: Changelog — EQ Shell
owner: Royce Milmlow
last_updated: 2026-07-01
scope: Append-only history of changes to EQ Shell (core.eq.solutions)
read_priority: reference
status: live
---

# Changelog — EQ Shell

## [2026-07-01] staff-resync-licences: on-demand post-approval licence sync from Cards
- New `netlify/functions/staff-resync-licences.ts` — re-syncs `public.licences` (jvkn) → `app_data.licences` (ehow) for a staff member who uploaded licences after approval
- "Re-sync from Cards" button in `SplitPanel` + `MobileSheet` zero-licence empty state; calls `handleMutated` on success to refresh the roster

## [2026-07-01] SMS worker on connection approval + StaffPage Phase E (PR #585, commit 2720f49)
- `cards-approve-staff.ts`: fire-and-forget Twilio SMS on both invite path and application path. Phone from existing row data; tenant name fetched inline for invite path; 24h guard prevents retroactive sends; non-fatal (approval committed first).
- PR #585: StaffPage Phase E — `MatrixView.tsx`, `SplitPanel.tsx`, `staffHelpers.ts`, `staffTypes.ts` extracted into `src/pages/staff/`. StaffPage.tsx slims from 2252 to ~300 net lines; all CI green; deployed.

## [2026-07-01] Warm Sand neutrals + StaffPage Phase D + forecasts mark-done + PDF import fixes (PRs #578 #580 #581 #582 #583 #584)
- **#580 / #581 / #582** — Warm Sand (Direction-D) neutral migration: cool-slate hexes → the warm `--eq-gray` ramp. StaffPage pilot (#580) → repo-wide .tsx (#581, 242 refs/21 files) → CSS incl. mobile chrome (#582, 121 refs/7 files: MobileTabBar.css, MobileRecordsDrawer.css, App.css…). Neutrals fully warm desktop + mobile; brand + status unchanged.
- **#578** — StaffPage Phase D: pure logic (`licStatus`/`matrixCsvCell`/`buildMatrixCsv`) lifted to `src/pages/staff/staffLib.ts` + 9 tests (suite 85→94). Behaviour-identical; unblocks component extraction.
- **#583** — GM Reports forecasts tab: per-job manual "Mark done" self-report. New `app_data.gm_forecast_status` (0153, mirrors gm_invoice_run) + `gm-forecast-status.ts` (GET/PATCH, reports.view). Done = Workbench-derived OR manual. Migration applies via One Pipe (sks slug) — pending Royce dispatch.
- **#584** — EQ Ops "From PDF" import: real `Loader2` spinner while parsing (both entry points); both PDF paths now auto-apply the tenant `defaultMaterialMarkup` (were adding lines at cost with no markup).


## [2026-07-01] Netlify env cleanup — Maps key rename + stale var removal
- `VITE_GOOGLE_MAPS_KEY` set (new key, eq-cards GCP project, HTTP referrer restricted); `NEXT_PUBLIC_GOOGLE_MAPS_KEY` deleted. Address autocomplete now live on next deploy.
- `EQ_FIELD_HANDOFF_KEY` deleted (Field HMAC handoff dead since JWT migration). `EQ_SECRET_SALT` retained — still active session-signing fallback in token.ts.

## [2026-07-01] Sentry fixes — approval dedup, Cards timer race, PDF fetch catch (PR #579)
- `cards_field_approvals` insert → upsert to prevent 23505 on re-approval (EQ-SHELL-E)
- `CardsIframe` 30s timer: `activeRef` guard stops false-positive capture when user navigates away (EQ-SHELL-F)
- `handleDownloadPdf`: added catch so Mobile Safari "Load failed" shows error in UI instead of unhandled rejection (EQ-SHELL-J)

## [2026-07-01] PR batch: URL-per-tab + tsc fixes + training matrix + cleanup (PRs #571 #572 #575 #576)
- **PR #571** (`80c904c`) — Shell URL reflects active Field tab (`?tab=<slug>`). `buildFieldSrc`/`buildFieldCookieSrc` accept `tab` param; `FieldIframe` reads `?tab=` on mount + listens for `EQ_TAB_CHANGE` postMessage → `history.pushState`. Also fixed: `rejection_reason` destructure in `handleApplication`.
- **PR #576** — `PostgrestBuilder as unknown as Promise<...>` hotfix in `cards-approve-staff.ts:131`; unblocked all downstream CI.
- **PR #570** — Google Maps `NEXT_PUBLIC_` key prefix fix; removed dead `NETLIFY_CONTEXT` Sentry fallback.
- **PR #572** — Removed dead `netlify/functions/cert-import-parse.ts` (superseded by async URL flow from #563).
- **PR #575** — Training matrix: employment-type filter, column sort, multi-select rows, column width polish.

## [2026-07-01] Calibration cert import 500 fixed — async payload wall (PR #563)
- Multi-cert import failed with "Import failed (500): Internal Error. ID: …". Root cause: `cert-import-parse-background` is a `-background` function (async Lambda invoke, ~256 KB payload limit vs 6 MB sync); POSTing multipart PDF bytes made Netlify reject the invocation before the handler ran (no function logs; the ID is a Netlify request id, not Sentry).
- Fix: browser uploads each PDF via the synchronous `upload-asset-cert` endpoint, then hands the background parser only JSON `{ url, fileName }`; parser fetches bytes server-side (SSRF-guarded to `SUPABASE_URL`). Parse-time URLs reused at commit so each PDF uploads once.

## [2026-07-01] Invite-path rejection email (PR #569)
- `cards_field_approvals` reject (bulk-imported staff / invite path) now emails the worker. Opens tenant DB, fetches `app_data.staff` email + name by `staff_id`, sends "not approved at this time". Fire-and-forget, non-fatal. Completes the rejection notification coverage started in PR #568 (application path).

## [2026-07-01] Pending connections: blank name fix, rejection email, phone lookup fix (PRs #565 #567 #568)
- PR #565: training matrix column headers show full licence names rotated vertically; pending connection cards stack name + buttons vertically on mobile; employment type shows human label not slug; iOS safe-area footer clearance.
- PR #567: `staff-pending-connections.ts` — fallback to `app_data.staff` on ehow by phone for workers with null names in `public.workers` (phone-only Cards sign-up).
- PR #568: application-path reject now emails worker ("not approved at this time"); `rejection_reason` written to `org_access_requests.note`; phone suffix map lookup bug fixed (was looking up raw phone in a suffix-keyed map). Migration `2026_07_01` adds `notification_sent_at` column to `org_access_requests` on jvkn (reserved).

## [2026-06-30] iOS CSS spinner fix — will-change: transform (PR #566)
- PR #566 (squash merged 17:08 UTC): `will-change: transform` added to 4 spinner selectors across 3 files — `.eq-error__spinner` (`src/App.css`), `.eq-spinner__dot` + `.eq-intake-spinner` (`eq-intake-demo/src/styles.css`), `.spinner` (`eq-format-ui/src/styles.css`). Forces GPU compositing layer on iOS Safari; prevents CSS `@keyframes rotate` from freezing on the main thread. 3 files, 4 insertions only.

## [2026-06-30] Brand-hex → @eq tokens, phase 1 + CI check required (PR #562)
- PR #562: 105 single-quoted brand-hex literals → `var(--eq-sky/-deep/-ink)` across 19 component files. Value-identical (fixed base tokens — `BrandProvider` overrides `--eq-brand`, not `--eq-sky`), zero visual change. Single-quote targeting structurally skipped the var()-incompatible double-quoted `fill=`/alpha cases.
- Made the CI `typecheck · test · lint` check a **required** status check on main (branch protection now requires it alongside `Schema drift + anon-grant + policy-lint`).

## [2026-06-30] EQ Ops pipeline: age badge, attachment types, 0152 migration, PR #552 (PRs #552 #560)
- PR #560: `status_changed_at` on `app_data.quote` (migration 0152 + backfill + RPC rebuild); board time-in-stage badge (amber ≥14d); attachment types `supplier_quote`/`drawing`/`quality_doc` with type picker + TypeBadge; `workbench_job_no` in canonical-api WRITABLE_FIELDS.jobs + syncJobToCanonical. Migrations 0147–0152 applied to both planes.
- PR #552: training matrix licence numbers + CSV export + employment-type select (was blocked by `field_teams`/`field_team_members` not in KNOWN_LEGACY_ANON on branch; fixed `3fa4e5e`).

## [2026-06-30] CI gate + auth-hub tests; training matrix (PRs #557 #559)

PR #557 — training matrix: licence numbers on cells, CSV export, employment-type select (constrained dropdown). PR #559 — first real CI gate (`.github/workflows/ci.yml`: `tsc -b` + `pnpm test` + advisory lint on every PR; repo previously gated only on the Netlify build) and the auth-hub test suite (`token.test.ts`, `supabase-jwt.test.ts` — session/handoff round-trip, per-consumer key isolation, alg-confusion defence, trusted-device binding; suite 66→85). Added a warn-level no-raw-hex eslint rule on `src/**/*.tsx`. Also: set SKS `notification_email` (activates the employer 7-day licence-expiry alert) and deactivated the demo-trades/melbourne tenants.

## [2026-06-30] Attachments bucket private + Issues table (PRs #549 #555)
- `attachments` storage bucket on ehow flipped to private (`public: false`); `tenant_signed_url` RLS policy on `storage.objects` enforces tenant folder isolation.
- `list-attachments.ts` + `upload-attachment.ts` use `createSignedUrl` (1-hour TTL) instead of `getPublicUrl`.
- Migrations 0147–0151 applied to ehow: issues table + RPCs, attachments index, bucket private, field_teams no-op.
- PR #555: `0151_field_teams_rls.sql` replaced with `SELECT 1` no-op — `field_teams`/`field_team_members` are `security_invoker=true` views; can't enable RLS on a view.

## [2026-06-30] Audit log team events + stub-match block + training matrix (PR #553)
- Activity Log now includes team & access events: invites, role changes, group membership — `writeTenantAudit()` writes `source='app'` rows via `invite-user`, `invite-users-batch`, `edit-user`, `security-groups`.
- Link-event name resolution: Activity Log resolves contact/customer/site names for link-table rows (shows "Alex Smith ↔ Acme Corp" not raw IDs).
- Onboarding stub-match block: `cards-approve-staff` returns 422 + candidates when name bigram similarity ≥ 0.5 and `confirmed_staff_id` not sent; `StaffPage` shows `MatchConfirmModal`.
- Compliance pack downloads: descriptive filenames ("Name - Org - date.zip" / "Org Compliance - date.zip") via `a.download`.
- Training Matrix: full licence names rotated 90°, subtitle alignment fix, tooltip uses human name, Export Excel button (SheetJS `.xlsx`).

## [2026-06-30] Licence expiry SMS reminders live
- Twilio env vars set on eq-shell Netlify (`EQ_SMS_PROVIDER=twilio`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER`, `SCHEDULER_TEST_SECRET`). Both email and SMS confirmed delivered via test endpoint. Scheduler runs daily 08:00 AEST.

## [2026-06-30] CRM: sites inline toggle table + apply-all button + A-Z contacts (PR #550)
- Sites section on the customer detail panel replaced with a compact 5-column table (name, address, Field, Service, actions). Field/Service toggles are inline — click fires immediately, no modal or Save button required. Row click still filters contacts. Delete confirm expands as a full-width inline row.
- "Apply to all sites" button in customer header: propagates customer-level Field/Service settings to every site in one click (manager-gated, ≥2 sites).
- Contact picker dropdowns in Edit Site and Add Site modals sorted A-Z.

## [2026-06-30] Activity Log: actor coverage for F/S toggles + calibration (PR #551)
- `x-eq-actor` capture verified working (real shell edits carry `source='shell'` + actor). Closed a coverage gap: `update-data-activation` (per-site/customer Field/Service toggles) and `asset-calibration` mutated the spine via the non-audited client → logged as `source='system'` with no actor. Both swapped to `getAuditedTenantDataClientById(tenant_id, session.user_id)`.

## [2026-06-30] Tenant Activity Log → link tables (PR #547)
- Migration 0147 adds audit triggers to `contact_customer_links` + `contact_site_links` (reuses `fn_audit('link_id')` from 0146). "Linked/unlinked contact to customer/site" now shows in the Activity log. Dispatched + verified both planes. Link events labelled "Contact ↔ customer/site" (id-only; name resolution deferred).

## [2026-06-30] Gate the Service mint with @eq-solutions/contracts (PR #543)
- `token-exchange` (aud=service) now builds the handoff `app_metadata` as the shared `ShellHandoffClaims` and runtime-validates it (`validateHandoffClaims`) before signing — fails closed (500) rather than minting a token eq-service would reject. With eq-service consuming the same type, `tsc` fails on either repo if the contract drifts. Field path + the generic `SupabaseJwtClaims` shape untouched. Dep pinned `github:eq-solutions/eq-contracts#v0.1.0`.

## [2026-06-30] Staff licence-review fixes (PRs #544, #545, #546)
- **#544** — review badge stops flipping to "re-review" for licences that predate the review (`reviewBadgeFor` compares licence `created_at` vs `reviewed_at`).
- **#545** — Cards onboarding matches an existing staff stub (worker-link → exact email → phone) instead of creating a duplicate. Closes the email gap in the auto-detect path.
- **#546** — profile review state matches the table badge (no more "reviewed by Ben" green tick contradicting a "re-review" table).
- Live: archived 4 empty duplicate staff stubs on ehow (Vincent Costa ×2, Rhys Scott, John Angangan).

## [2026-06-30] Customers page — Add Site fix + Field/Service activation (PRs #540, #541, #542)
- **Add Site 500 fixed** (#540) — non-existent `site_contact_id` column removed from the insert; site + address save again.
- **Site street address + per-site Field/Service toggles** (#541) — address was hidden behind suburb/state; the F/S UI had been built in the unrouted CustomersHubPage. Both now on the live CustomersPage, manager-gated.
- **Customer-level Field/Service toggles** (#542) — in the customer header, independent of site flags (no cascade).

## [2026-06-30] Tenant Activity Log + polish fixes (PRs #536, #539)
- **Tenant Activity Log** (PR #539) — "who changed what" on the canonical spine. Migration 0146: `app_data.audit_log` (service-role-only) + `fn_audit()` trigger storing full before/after snapshot, on customers/sites/contacts/staff/assets. Applied to both planes. `x-eq-actor` header → trigger captures the actor; `tenant-audit.ts` reads + enriches; Activity tab on `/sks/admin/audit`. Auth classified by domain not storage; platform security log deferred.
- **Polish fixes** (PR #536) — staff edit 500 (disabled `staff_field_sync` → `public.people`), audit log display, employment-type dropdown, cert-import 500 (formData before 202), Add Site modal.

## [2026-06-29] Licence-expiry notifications: fixed (was querying wrong DB) + hardened (PRs #537 + #538)

The daily `licence-expiry-scheduler` was routing every tenant through `getTenantRpcClient` → the tenant's Field/Service data plane (ehow for SKS), where `public.workers`/`public.licences`/the `eq_get_licences_*` RPCs don't exist — so the RPC errored and was swallowed every run: **zero notifications ever sent.** Repointed to eq-canonical via a new `getPublicServiceClient()` (public schema, same project). Hardened: E.164 phone normalization (`toE164AU`); worker email+SMS in range-based 30-day / 7-day tiers (replaces exact-day matching — survives a missed run and catches licences imported already inside 30 days); per-licence dedup + audit trail in `public.licence_notification_log` (migration 0061, RLS-on); SMS `Reply STOP` opt-out; tenant autodiscovery from `shell_control.tenants`; secret-gated manual test endpoint; humanized licence labels; fixed double-encoded mojibake that was shipping in live email subjects/bodies. Migration 0062 revoked anon EXECUTE on `eq_get/update_tenant_settings` (0060's DROP+CREATE had reset them to PUBLIC, failing the anon-SECDEF CI invariant on every PR). Email already live (resend); SMS log-only until Twilio env vars are set.

## [2026-06-29] CRM: relational site contacts + Google Places address autocomplete (PRs #515 + #517)

Site contact moved from three free-text fields (name/phone/email) on `app_data.sites` to a contact picker backed by `contact_site_links (role='site_contact')`. Legacy columns nulled on every save. Address field (`address_line_1`) exposed in `crm-customers.ts` + edit form. Google Places autocomplete wired on address input (key-gated via `NEXT_PUBLIC_GOOGLE_MAPS_KEY`, degrades to plain text without it). Site card location line is now a Google Maps link. CSP pre-warmed for `maps.googleapis.com` + `maps.gstatic.com`.

## [2026-06-29] cert-import background function fix (PR #535)

Fixed `cert-import-parse-background`: read + materialise all file `ArrayBuffer[]` synchronously before returning 202, then pass owned byte arrays to `runJob`. Previously passed `req.clone()` which failed when Netlify closed the request body stream after the 202 response. Added `withSentry` wrapping so errors are now captured in Sentry.

## [2026-06-28] EQ Service admin tiles in Shell Admin hub (PR #518)

Adds an EQ Service section to the Admin hub with 8 tiles: Report settings, Media library, Archive, Imports, Backup, Activity feed, Today, Connected apps. Each tile deep-links to `/<tenant>/service/admin/<page>` via the existing `ServiceIframe` URL-sync path. Section gated on `moduleEnabled(session, 'service')` — hidden for tenants without Service.
