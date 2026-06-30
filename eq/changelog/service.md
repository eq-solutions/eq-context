---
title: Changelog — EQ Solves Service
owner: Royce Milmlow
last_updated: 2026-06-30
scope: Append-only history of changes to the EQ Solves Service product
read_priority: reference
status: live
---

# Changelog — EQ Solves Service

## [2026-06-30] Shell→Service handoff: shared contract + auth canaries + fail-closed (PRs #371, #373, #374, #376)
- **Adopted `@eq-solutions/contracts`** (#374) — `ServiceJwtClaims.app_metadata` is now the shared `ShellHandoffClaims` type; `verifyServiceJwt` + `validateSupabaseJwt` runtime-validate the full contract (was email-only). `tsc` now fails if the Shell→Service claim shape drifts.
- **Auth-handoff Sentry canaries** (#373) — `captureAuthHandoff(reason)` on every handoff failure; `validateSupabaseJwt` returns a discriminated reason (signature checked before expiry → distinguishes a rotated secret from a stale token). `layout.tsx` flags `cookie_unusable`.
- **Fail closed on unresolved tenant slug** (#376) — 403 `service-account-not-found` instead of minting a JWT with Shell's tenant UUID (which matched no RLS rows → blank app). Reuses the existing `/shell` client error surface.
- **RPC return-shape drift gate + JWT type dedupe** (#371) — `canonical-types-drift` also diffs `Functions` return columns; the inbound JWT interface deduped onto `ServiceJwtClaims`.

## [2026-06-29] Parallelize maintenance check detail page (PR #365)

- Restructured ~10 sequential `await` calls into 3 `Promise.all` waves in `app/(app)/maintenance/[id]/page.tsx`. No logic changes — data-fetching only. Expected ~60% load-time reduction on EU Supabase.

## [2026-06-28] Shell JWT token refresh + Admin nav link (PR #364)

- `ShellTokenRefresh`: new client component. Fires `REQUEST_SHELL_TOKEN` 5 min before the 4h `eq_service_jwt` expires, handles `SHELL_TOKEN_RESPONSE`, re-exchanges via `/api/shell-auth`. Keeps Shell iframe sessions alive past the initial 4h window.
- Admin link added to Shell iframe inline nav for manager-role users. Service sidebar is hidden when embedded — this was the only missing path to `/admin` for Shell users.

## [2026-06-10] Shell SSO — ROOT CAUSE found + fixed (eq-shell PR #306)
**Built by:** Royce Milmlow + Claude Code

After 4 Service-side bugs fixed, Service still showed login page. Root cause was in Shell, not Service.

**Root cause:** `COOKIE_AUTH = true` in Shell's `ServiceIframe.tsx` was set whenever `VITE_SERVICE_URL` ended in `.eq.solutions`. In COOKIE MODE, Shell skips token minting entirely and loads the iframe at the root URL, relying on `eq_shell_session` being auto-sent. But Shell restores from Supabase cookies on refresh without re-minting `eq_shell_session` — so the cookie was absent at iframe-load time. proxy.ts never saw it → never called shell-sso.

**Fix:** `const COOKIE_AUTH = false` — TOKEN MODE always (eq-shell PR #306, commit `16d3f19`, deploy `6a285d53`).

TOKEN MODE (proven path): `token-exchange?aud=service` → Supabase JWT → `/shell#sh=<jwt>` → `/api/shell-auth` validates → `eq_shell_bridge=1` + redirect to `/` → `ShellReadySignal` fires `EQ_SERVICE_READY` → Shell reveals iframe.

**Cleanup:** diagnostic console.logs removed from proxy.ts + shell-sso (eq-service PR #274).

**Status:** Shell deployed. Smoke test pending.

---

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
