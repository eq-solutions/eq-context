---
title: Changelog — EQ Expenses
owner: Royce Milmlow
last_updated: 2026-04-10
scope: Append-only history of changes to the EQ Expenses tool
read_priority: reference
status: live
---

# Changelog — EQ Expenses

## [2026-04-05] Bug Fixes - 60/60 Checks Passing
**Built by:** Royce Milmlow + assistant
**Changes:**
- Fixed receipt-preview hardcoded local file path
- Fixed profile summary card hardcoded static HTML
- Removed Cloudflare email decode script
- Rewrote renderProfileSummary using string concatenation
- Fixed FY stats sidebar hardcoded zero rows
- Fixed header sub-title hardcoded name
- Full 60-point audit: all checks passing
**Status:** File ready - Cloudflare Worker deploy + end-to-end test pending

## [2026-04-05] Cloudflare Worker Proxy - API Key Bound
**Built by:** Royce Milmlow + assistant
**Changes:**
- Diagnosed scan failure: scan-error div hardcoded display
- Confirmed Cloudflare Worker has ANTHROPIC_API_KEY bound
**Status:** Worker live with key bound - full deploy test pending

## [2026-04-04] AI Receipt Scanning Architecture Decision
**Built by:** Royce Milmlow + assistant
**Changes:**
- Decision: move API key to Cloudflare Worker server-side
- Single HTML file + vanilla JS - no build steps
**Status:** Architecture locked
