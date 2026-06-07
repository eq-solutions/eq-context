---
title: Auth Phase 4 — HMAC Retirement Runbook
owner: Royce Milmlow
last_updated: 2026-06-07
scope: Runbook for retiring the HMAC auth path (Sprint 6, Phase 4)
read_priority: reference
status: live
---

# Auth Phase 4 — HMAC Retirement Runbook

**Sprint:** 6
**Author:** EQ Solutions
**Status:** DRAFT — not yet approved for execution
**Estimated effort:** 1 day coding + 1 day soak

---

## Background

Phases 0–3 of the EQ Shell auth re-platform replaced the legacy HMAC session and iframe token system with Supabase-native JWTs carrying `eq_role` and `tenant_id` claims. Phase 4 is the cleanup step: remove the HMAC machinery so it cannot be used as a fallback and so `EQ_SECRET_SALT` can be retired.

### What HMAC is today

| Artifact | Location | Purpose |
|---|---|---|
| `EQ_SECRET_SALT` | Netlify env (Shell, Field, Service) | HMAC key for session cookies + iframe tokens |
| `_shared/token.ts` | eq-shell repo | Signs/verifies HMAC tokens |
| `mint-iframe-token.ts` | eq-shell `netlify/functions/` | Mints 60-second HMAC tokens for iframe embeds |
| `shell-login.ts` | eq-shell `netlify/functions/` | PIN + bcrypt login; mints HMAC session cookie |
| `verify-shell-session.ts` | eq-shell `netlify/functions/` | Reads and verifies HMAC session cookie |
| `verify-pin.js` (action=verify-shell-token) | eq-solves-field | Verifies inbound HMAC iframe token |
| `shell-auth/route.ts` (legacy path) | eq-solves-service | Legacy HMAC token acceptance path |

After Phase 3 all iframe embeds use `token-exchange.ts` (issues Supabase JWT) and the PIN login path is unused. Phase 4 removes the HMAC surface.

---

## Prerequisites Checklist

All items must be confirmed before execution begins. DRI signs off each line.

- [ ] **R1** — `SUPABASE_JWT_SECRET` set in Netlify env for **eq-solves-field** (matches Supabase project JWT secret)
- [ ] **R2** — `SUPABASE_JWT_SECRET` set in Netlify env for **eq-solves-service** (matches Supabase project JWT secret)
- [ ] **R3** — Zero PIN-only logins observed for **14 consecutive days** (confirm via Supabase auth.users + PostHog/Sentry login event query; no `provider = 'email'` with PIN flag)
- [ ] **R4** — Parity check script (`scripts/parity-check.ts`) shows **0 orphaned users** (users with no Supabase magic-link identity)
- [ ] **R5** — `token-exchange.ts` is the sole iframe token path in all three apps (grep confirms no remaining calls to `mint-iframe-token`)
- [ ] **R6** — Phase 4 retirement plan reviewed and approved by Royce Milmlow
- [ ] **R7** — Rollback window confirmed: execution during business hours with at least 2 hours of soak time before EOD

---

## Go / No-Go Criteria

### Go
- All 7 prerequisites checked off with date + DRI signature
- No Sentry errors containing `HMAC`, `verify-shell-token`, or `mint-iframe-token` in the prior 7 days
- Staging deploy of eq-shell passes smoke test (login, iframe load in Field + Service) before production

### No-Go — stop and reschedule
- Any prerequisite unchecked
- Active PIN login traffic in the prior 14 days
- Parity check shows orphaned users (run remediation first; see `auth-spike-2026-05-30.md`)
- Any `EQ_SECRET_SALT`-signed token rejected in production in the prior 48 hours that was not from a test account

---

## Files to Remove

### eq-shell repo

| File | Action | Notes |
|---|---|---|
| `netlify/functions/mint-iframe-token.ts` | Delete | Replaced entirely by `token-exchange.ts` |
| `netlify/functions/shell-login.ts` | Delete PIN path OR delete file | See note below |
| `_shared/token.ts` | Delete | HMAC sign/verify utilities — no longer referenced after removals |

**shell-login.ts note:** If a magic-link fallback button lives in this file that is still needed, extract it first. The PIN authentication block (`bcrypt.compare`, `EQ_SECRET_SALT` session cookie write) must be removed. If the entire file is PIN-only, delete it. Confirm with `grep -n 'magic' netlify/functions/shell-login.ts` before deleting.

**Netlify redirect / function routing:** Remove any `[[redirects]]` or `[functions]` entries in `netlify.toml` that route to `mint-iframe-token` or the PIN path of `shell-login`.

### eq-solves-field repo

| File | Action |
|---|---|
| `netlify/functions/verify-pin.js` (or equivalent) | Remove the `action=verify-shell-token` handler block. If `verify-pin.js` has no remaining handlers after removal, delete the file. |

### eq-solves-service repo

| File | Action |
|---|---|
| `src/app/api/shell-auth/route.ts` | Remove the legacy HMAC acceptance branch. Keep only the Supabase JWT verification path. If the file becomes trivially thin, fold it into the main auth middleware. |

---

## Files to Modify (Keep, Edit)

### eq-shell — `verify-shell-session.ts`

This function reads the HMAC session cookie set by `shell-login.ts`. Once `shell-login.ts` PIN path is removed, no new HMAC cookies are minted. However, existing browser sessions may still hold an HMAC cookie until they expire (typically 7 days).

**Approach:**
1. Do NOT delete `verify-shell-session.ts` on Day 1.
2. Add a deprecation log: `console.warn('[DEPRECATED] HMAC session cookie presented — user has stale session')`.
3. Return a `401` with body `{ error: 'session_expired', reason: 'legacy_hmac' }` instead of honouring the cookie.
4. After a 14-day soak with zero hits on that warn log, delete the file and remove its Netlify function entry.

This two-step removal prevents hard-locking users with cached sessions on Day 1.

### eq-shell — `_shared/token.ts`

Can only be deleted after `verify-shell-session.ts` is also removed (second deletion, after soak). Block it with a TODO comment until then.

---

## Environment Variable Retirement

### `EQ_SECRET_SALT`

| App | Current use | Safe to remove? |
|---|---|---|
| eq-shell (Netlify) | `shell-login.ts` mint, `verify-shell-session.ts` verify | Remove after soak period confirms zero HMAC sessions active |
| eq-solves-field (Netlify) | `verify-pin.js` HMAC block | Remove after Field PR merged + deployed |
| eq-solves-service (Netlify) | `shell-auth/route.ts` legacy path | Remove after Service PR merged + deployed |

**Removal order:**
1. Remove from Field + Service Netlify env immediately after their PRs deploy (they will have no code reading it).
2. Remove from Shell Netlify env only after the `verify-shell-session.ts` soak period (14 days, zero HMAC hits).

**Do NOT rotate `EQ_SECRET_SALT` — remove it.** Rotating creates a new signing key but the old verify path still exists; it only changes which tokens validate. Removing the env var causes any remaining code path that tries to use it to fail loudly, which is the desired outcome.

---

## Step-by-Step Execution Plan

### Day 1 — Code + Deploy

1. **Create feature branch** off `main` in each affected repo: `git checkout -b chore/retire-hmac`.
2. **eq-solves-field PR:**
   - Remove `action=verify-shell-token` block from `verify-pin.js`.
   - Run field smoke test (assignment load, iframe embed resolves via `token-exchange`).
   - Merge + deploy. Remove `EQ_SECRET_SALT` from Field Netlify env.
3. **eq-solves-service PR:**
   - Remove legacy HMAC branch from `shell-auth/route.ts`.
   - Run service smoke test (defect create, report load, iframe resolves).
   - Merge + deploy. Remove `EQ_SECRET_SALT` from Service Netlify env.
4. **eq-shell PR:**
   - Delete `mint-iframe-token.ts`.
   - Delete `shell-login.ts` PIN block (or whole file).
   - Modify `verify-shell-session.ts` to return 401 with deprecation log (do NOT delete yet).
   - Update `netlify.toml` to remove function registrations for deleted files.
   - Run shell smoke test: magic-link login, token exchange to Field iframe, token exchange to Service iframe.
   - Merge + deploy. Do NOT remove `EQ_SECRET_SALT` from Shell Netlify env yet.
5. **Monitor Sentry** for 2 hours post-deploy. Confirm zero new HMAC-related errors.

### Day 2 — Soak

6. Check Sentry + application logs at start of business: confirm zero hits on the `[DEPRECATED] HMAC session cookie presented` warning.
7. If clean at EOD: record pass in this doc and start the 14-day clock on `verify-shell-session.ts` full removal.

### Day 14+ — Final cleanup

8. Confirm zero HMAC session hits over the 14-day soak.
9. Delete `verify-shell-session.ts` and `_shared/token.ts` from eq-shell. Remove their Netlify function entries.
10. Remove `EQ_SECRET_SALT` from Shell Netlify env.
11. Close the Phase 4 tracking ticket.

---

## Rollback Plan

| Scenario | Rollback action |
|---|---|
| Field or Service breaks post-deploy (iframe fails to load) | Revert the merge commit (`git revert <sha>`), redeploy. `EQ_SECRET_SALT` is still set on shell, so HMAC path can still be temporarily reinstated. |
| Shell deploy breaks magic-link login | Revert eq-shell merge, redeploy. |
| Stale HMAC session users locked out | `verify-shell-session.ts` returns 401 with `session_expired` — user sees login screen. This is expected behaviour. No code rollback needed; advise user to log in via magic link. |
| `EQ_SECRET_SALT` already removed from Field/Service but rollback needed | Re-add the env var from 1Password (stored under `EQ Shell — HMAC Secret Salt`) before redeploying the reverted code. |

**1Password note:** Do not delete the `EQ_SECRET_SALT` entry from 1Password until Day 14+ cleanup is fully signed off. Keep it available for emergency rollback.

---

## Testing Checklist (Pre-merge, per app)

### eq-solves-field
- [ ] Assignment list loads for a logged-in user
- [ ] Iframe embed resolves (check browser network: `token-exchange` returns 200, no call to `mint-iframe-token`)
- [ ] `verify-pin.js` no longer accepts an HMAC token (send a crafted token; expect 401 or 400)

### eq-solves-service
- [ ] Defect create/edit works
- [ ] Maintenance report loads
- [ ] `shell-auth` no longer accepts an HMAC token (expect 401)

### eq-shell
- [ ] Magic-link login flow end-to-end
- [ ] Successful token exchange to Field iframe
- [ ] Successful token exchange to Service iframe
- [ ] `mint-iframe-token` endpoint returns 404 (function removed)
- [ ] PIN login endpoint returns 404 or 410 (function removed)
- [ ] No build errors (TypeScript compile clean)

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| User with cached HMAC cookie gets locked out | Low (after 14 days of zero PIN logins) | Medium | `verify-shell-session.ts` returns 401 with clear error; user re-authenticates via magic link |
| `_shared/token.ts` still imported elsewhere | Low | High | `grep -r '_shared/token'` across all repos before deleting |
| `EQ_SECRET_SALT` referenced in an undiscovered code path | Low | Medium | Remove env var after deploy; any missed path fails loudly with a clear missing-env error in Sentry |
| Sprint 6 work introduces new HMAC calls | Very low | High | Add lint rule or `grep` in CI: block any new import of `_shared/token` on the main branch |

---

## Approval Sign-off

| Role | Name | Date | Signature |
|---|---|---|-