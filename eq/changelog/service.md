---
title: Changelog — EQ Solves Service
owner: Royce Milmlow
last_updated: 2026-06-09
scope: Append-only history of changes to the EQ Solves Service product
read_priority: reference
status: live
---

# Changelog — EQ Solves Service

## [2026-06-09] Shell SSO — 4 bugs found and fixed (PRs #267–#270)
**Built by:** Royce Milmlow + Claude Code

Service was showing its own login page instead of auto-authenticating when loaded as a Shell iframe. Four root causes found and fixed:

**Bug 1 — Edge runtime crypto failure (proxy.ts)**
All HMAC verification, `generateLink`, and `verifyOtp` logic was in `proxy.ts` which runs in the Netlify edge (Deno) runtime. `node:crypto` silently fails on Deno. SSO always fell through to login page. Fix: moved all auth logic to a new Node.js API route `/app/api/shell-sso/route.ts`. `proxy.ts` now only detects the cookie and redirects.

**Bug 2 — Wrong redirect hostname**
`/api/shell-sso` built its success redirect by cloning `request.nextUrl`. On Netlify, `nextUrl.host` is an internal handler hostname. Fix: `new URL(safePath, process.env.NEXT_PUBLIC_SITE_URL)`.

**Bug 3 — HMAC key mismatch (EQ_SESSION_SALT vs EQ_SECRET_SALT)**
Shell signs `eq_shell_session` with `EQ_SESSION_SALT`. Service was reading `EQ_SECRET_SALT` only. Fix: `const salt = process.env.EQ_SESSION_SALT ?? process.env.EQ_SECRET_SALT`.

**Bug 4 — Infinite redirect loop on SSO failure (PR #270)**
`proxy.ts` intercepted ALL non-bridged requests including `/auth/signin`. When shell-sso fails → redirects to `/auth/signin` → proxy intercepts → shell-sso → ... → ERR_TOO_MANY_REDIRECTS. Fix: `isSsoExempt = alreadyBridged || pathname === '/api/shell-sso' || isPublicPath(pathname)`.

**Commits:** `9d26b85` (Bug 1), `5e5046e` (Bug 2), `4155abf` (Bug 3), `f3b1c5e` (Bug 4)
**Latest deploy:** `6a27f277` — state=ready, 2026-06-09

---

## [2026-06-09] Sprint 7 — DB migration to ehow + env var cutover (PR #257)
**Built by:** Royce Milmlow + Claude Code

Migrated EQ Service from `urjhmkhbgaxrofurpbgc` (old) to `ehowgjardagevnrluult` (new). Schema (28 CMMS tables), data, and 9 storage files migrated. Netlify env vars updated. Code domain refs updated.

Migration 0123 (site_credentials encryption) also shipped — three schema bugs fixed (public→app_data, wrong RPC name). `SITE_CREDENTIALS_KEY` set in Netlify.

**Status:** Deploy ready. Pending smoke test before PR #257 merge.
