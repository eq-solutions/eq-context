# EQ Expenses — Changelog

## [2026-04-05] Bug Fixes - 60/60 Checks Passing
**Session:** https://claude.ai/chat/00e8be95-0c56-4964-9dc1-ca2c668c145d
**Built by:** Royce Milmlow + Claude (Anthropic)
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
**Session:** https://claude.ai/chat/00e8be95-0c56-4964-9dc1-ca2c668c145d
**Built by:** Royce Milmlow + Claude (Anthropic)
**Changes:**
- Diagnosed scan failure: scan-error div hardcoded display
- Confirmed Cloudflare Worker has ANTHROPIC_API_KEY bound
**Status:** Worker live with key bound - full deploy test pending

## [2026-04-04] AI Receipt Scanning Architecture Decision
**Session:** https://claude.ai/chat/6a3dd65e-5f9c-43c9-8d11-0f02e0c009de
**Built by:** Royce Milmlow + Claude (Anthropic)
**Changes:**
- Decision: move API key to Cloudflare Worker server-side
- Single HTML file + vanilla JS - no build steps
**Status:** Architecture locked
