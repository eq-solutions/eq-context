---
title: Changelog — EQ Shell
owner: Royce Milmlow
last_updated: 2026-06-28
scope: Append-only history of changes to EQ Shell (core.eq.solutions)
read_priority: reference
status: live
---

# Changelog — EQ Shell

## [2026-06-29] cert-import background function fix (PR #535)

Fixed `cert-import-parse-background`: read + materialise all file `ArrayBuffer[]` synchronously before returning 202, then pass owned byte arrays to `runJob`. Previously passed `req.clone()` which failed when Netlify closed the request body stream after the 202 response. Added `withSentry` wrapping so errors are now captured in Sentry.

## [2026-06-28] EQ Service admin tiles in Shell Admin hub (PR #518)

Adds an EQ Service section to the Admin hub with 8 tiles: Report settings, Media library, Archive, Imports, Backup, Activity feed, Today, Connected apps. Each tile deep-links to `/<tenant>/service/admin/<page>` via the existing `ServiceIframe` URL-sync path. Section gated on `moduleEnabled(session, 'service')` — hidden for tenants without Service.
