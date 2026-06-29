---
title: Changelog — EQ Shell
owner: Royce Milmlow
last_updated: 2026-06-30
scope: Append-only history of changes to EQ Shell (core.eq.solutions)
read_priority: reference
status: live
---

# Changelog — EQ Shell

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
