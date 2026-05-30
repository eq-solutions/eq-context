---
title: Auth Re-platform Spike — Supabase Auth IdP + Passkeys
owner: Royce Milmlow
last_updated: 2026-05-30
scope: Design + staged migration plan for Supabase-Auth single IdP, passkeys-first, 5-tier roles → JWT/RLS. Design only — review before build.
read_priority: standard
status: live
---

# Auth Re-platform Spike — Supabase Auth IdP + Passkeys

## 0. Problem Statement

EQ Suite today has three auth systems running simultaneously:

| Layer | What it is | Where it lives |
|---|---|---|
| Email + 4-digit PIN + bcrypt | User-facing login | EQ Field (all tenants) |
| Self-signed HMAC tokens | Cross-app handoff | Shell → Field, Shell → Service |
| Supabase JWT (partial) | Shell/canonical data queries | eq-shell, eq-cards |

The result is auth defined in ~5 places, a 5-tier role model that EQ Field lossily squashes to 2 tiers, and no single source of truth for who a user is across the suite.

**Approved target (2026-05-30):** Supabase Auth as the single IdP per entity, passkeys-first, one token model, one role registry via `@eq-solutions/roles`, enforced everywhere by JWT custom claims + RLS. The 4-digit PIN is retired; HMAC tokens are retired; cross-app identity is solved by a single Supabase session + an edge-function token-exchange where needed.

This document is a design and staged migration plan. It is not a build ticket.

---

## 1. Architecture Diagram (Text)

```
User device
  │
  ▼
[Browser / WebAuthn API]
  │  passkey assertion (or magic-link OTP fallback)
  ▼
Supabase Auth (eq-canonical-internal)
  │  issues access_token (JWT) + refresh_token
  │  JWT contains: sub, email, app_metadata.eq_role, app_metadata.tenant_id,
  │                app_metadata.is_platform_admin
  ▼
eq-shell (core.eq.solutions)
  │  holds the session, drives the sidebar, controls navigation
  │
  ├─► Netlify Edge Function: /api/token-exchange
  │     verifies Shell JWT → mints a short-lived project-scoped Supabase JWT
  │     for the embedded app (Field or Service)
  │
  ├─► eq-solves-field (iframe)
  │     receives project-scoped JWT via postMessage
  │     all Supabase calls hit the correct tenant DB
  │
  └─► eq-solves-service (iframe)
        receives project-scoped JWT via postMessage
        Next.js route handlers verify JWT on every server request
```

---

## 2. Role Model → JWT Claims → RLS

### 2.1 Role Model (from @eq-solutions/roles)

Five tiers, one orthogonal override:

| Role | Numeric tier | Description |
|---|---|---|
| `manager` | 1 | Full tenant access |
| `supervisor` | 2 | Site/team management |
| `employee` | 3 | Standard operational access |
| `apprentice` | 4 | Restricted operational |
| `labour_hire` | 5 | Read-only or task-scoped |

`is_platform_admin: true` is an orthogonal boolean, not a sixth role. It grants cross-tenant visibility for EQ Solutions staff and is completely separate from the tenant role hierarchy. A platform admin can still have a tenant role (e.g., `manager` in their own org) — the two concepts do not conflict.

Permission convention: `<module>.<verb>[_<scope>]` — e.g., `intake.write`, `audit.read`, `equipment.write_own`. The full permission matrix lives in `C:\Projects\eq-roles\roles/model.json`.

### 2.2 JWT Custom Claims Shape

The Custom Access Token Hook writes to `app_metadata` (not `user_metadata`) because `app_metadata` is server-controlled and cannot be tampered with by the authenticated user.

Target access token payload (non-standard claims only):

```json
{
  "sub": "<supabase-user-uuid>",
  "email": "royce@eq.solutions",
  "aal": "aal2",
  "app_metadata": {
    "eq_role": "manager",
    "tenant_id": "sks",
    "is_platform_admin": false
  }
}
```

Notes:
- `aal: "aal2"` is set by Supabase when the user completes a second factor. Passkey sign-in counts as `aal2` because WebAuthn is an authenticator-level factor (possession + biometric/PIN). Plain magic-link alone is `aal1`.
- `tenant_id` identifies which Supabase project's data the user may access. The Shell itself routes accordingly.
- `is_platform_admin` is not a role claim — it is a flag that unlocks cross-tenant functions in the Shell and Netlify edge functions. It is never passed into embedded apps as a data-access grant.

### 2.3 Custom Access Token Hook (Design Only)

A PostgreSQL function registered in the Supabase Dashboard under Authentication → Hooks → Custom Access Token Hook. It runs before every token issuance (initial login and every refresh).

Pseudocode:

```
FUNCTION eq_custom_access_token_hook(event JSONB) RETURNS JSONB
  user_id := event->'claims'->>'sub'
  
  SELECT eq_role, tenant_id, is_platform_admin
  INTO r_role, r_tenant, r_admin
  FROM public.tenant_members
  WHERE auth_user_id = user_id
  LIMIT 1
  
  -- Inject into app_metadata (merge, do not overwrite other fields)
  claims := event->'claims'
  claims := jsonb_set(claims, '{app_metadata,eq_role}',     to_jsonb(r_role))
  claims := jsonb_set(claims, '{app_metadata,tenant_id}',   to_jsonb(r_tenant))
  claims := jsonb_set(claims, '{app_metadata,is_platform_admin}', to_jsonb(r_admin))
  
  RETURN jsonb_set(event, '{claims}', claims)
END
```

Key design decisions:
- The function reads from `public.tenant_members`, not `auth.users.raw_app_meta_data`. This keeps roles in a queryable table, not embedded in the auth identity row, enabling bulk role updates without touching the auth system.
- The hook must handle the case where the user has no `tenant_members` row (e.g., during a brand-new invite flow). In that case, it should return `eq_role: null` rather than throwing, so the login completes and the UI can redirect to an onboarding screen.
- SECURITY DEFINER on the function is required to read `public.tenant_members` from the hook context.

### 2.4 RLS Policy Patterns

All tenant-data tables use a two-part policy:

**Read policy (example — work orders in EQ Service):**
```sql
CREATE POLICY "tenant members can read work orders"
ON work_orders FOR SELECT
USING (
  tenant_id = (auth.jwt() -> 'app_metadata' ->> 'tenant_id')
  AND auth.jwt() -> 'app_metadata' ->> 'eq_role' IS NOT NULL
);
```

**Write policy with role gate (example — manager-only):**
```sql
CREATE POLICY "managers can create work orders"
ON work_orders FOR INSERT
WITH CHECK (
  tenant_id = (auth.jwt() -> 'app_metadata' ->> 'tenant_id')
  AND (auth.jwt() -> 'app_metadata' ->> 'eq_role') IN ('manager', 'supervisor')
);
```

**Platform admin bypass (example):**
```sql
CREATE POLICY "platform admin reads all"
ON work_orders FOR SELECT
USING (
  (auth.jwt() -> 'app_metadata' ->> 'is_platform_admin')::boolean = true
);
```

**JWT staleness caveat:** RLS reads the JWT as presented — it does not re-query the database on every row check. If a user's role is changed in `tenant_members`, the change is not reflected in RLS until the user's access token is refreshed (typically within 1 hour, sooner if forced). For high-stakes role revocations, the mitigation is to force-revoke the user's sessions via the Supabase admin API, which invalidates the refresh token and forces re-login.

---

## 3. Passkey Enrollment + Recovery UX

### 3.1 Supabase Passkey Status

Supabase released passkey (WebAuthn) support in beta on 2026-05-28. It requires `@supabase/supabase-js` v2.105.0+. The API is experimental and opt-in; the dashboard ships a configuration panel under Authentication → WebAuthn (Relying Party display name, relying party ID = apex domain, allowed origins). During beta, the API surface may change — this is a design consideration for the migration timeline (Phase 1 should not start until the API is declared stable or EQ explicitly accepts the beta risk).

### 3.2 Enrollment Flow

**Pre-flight check (before showing any passkey UI):**
- Detect `PublicKeyCredential` support and `navigator.credentials.create` availability.
- If the device does not support WebAuthn, skip passkey enrollment entirely and proceed to magic-link-only flow. Never show the enrollment screen and then let the browser produce a cryptic error.

**Primary enrollment path (post-login prompt):**

```
1. User logs in via magic-link (first login, no passkey yet)
2. After successful login, display enrollment prompt:
   "Sign in faster with your fingerprint"
   Subtext: "Use Touch ID, Face ID, or your device PIN next time you sign in.
             Works only on this device."
   [Set up passkey]   [Not now]

3. If "Set up passkey":
   a. Call supabase.auth.enrollPasskey() (beta API)
   b. Browser presents native WebAuthn prompt (biometric/PIN)
   c. On success: show confirmation "Passkey added. You're all set."
   d. On failure: catch error, show "Couldn't set up passkey on this device.
                  You can try again in Settings."
   e. Never retry automatically in the same session.

4. If "Not now":
   a. Dismiss without penalty.
   b. Do not prompt again in the same session.
   c. Re-surface the prompt at next login, max 3 times total across all sessions,
      then move it to Settings only.
```

**Subsequent logins (passkey enrolled):**

```
1. Show email field with autocomplete="webauthn" (Conditional UI)
   - Browser surfaces the passkey in the native autofill dropdown automatically.
2. User taps the passkey suggestion → browser presents biometric/PIN.
3. On success: supabase.auth.signInWithPasskey() returns a session.
4. Shell receives session, sets cookies, loads hub.
```

Copy rule: never use the words "passkey", "WebAuthn", "FIDO2", or "credential" in user-facing strings. Use "your fingerprint", "sign in faster", "this device".

### 3.3 Recovery (Passkey Lost or New Device)

The fallback chain is ordered from strongest to weakest:

| Scenario | Recovery method | Notes |
|---|---|---|
| New device, same account | Magic link to registered email | Standard. Supabase `signInWithOtp` (email). After login, prompt to enroll new passkey on new device. |
| Email inaccessible | Pre-generated recovery codes | 8 one-time codes, shown at first passkey enrollment. User must download/print. |
| Both passkey + email lost | Platform admin reset | Royce (is_platform_admin) can invalidate sessions + send a new magic link from the Shell admin panel. |

**Recovery code UX:**
- Generated on the client at enrollment time using the CSPRNG (`crypto.getRandomValues`), formatted as `XXXX-XXXX-XXXX`.
- 8 codes per user. Each is single-use.
- Displayed once on enrollment success screen with a download button (plain `.txt`).
- Stored as bcrypt hashes in a `recovery_codes` table (server-side), linked to the user's `auth.users.id`.
- On use: code is validated, the matching row is soft-deleted, and the user is prompted immediately to enroll a new passkey on their current device.

**Security note:** magic-link fallback lowers the effective security floor — the account is as secure as the email inbox. This is acceptable for the EQ suite (internal workforce app) and matches industry practice for B2B tools. The alternative (passkey-only, no fallback) would lock employees out on device loss — not viable for a field workforce.

### 3.4 Multiple Passkeys Per User

Users may enroll multiple passkeys (e.g., work laptop + phone). The Supabase passkey API supports this natively — each enrollment registers a distinct credential. The Settings page should show a list of enrolled passkeys (device name + enrollment date) with a revoke button per credential.

---

## 4. Session and Token Model

### 4.1 Supabase Session Mechanics

- **Access token (JWT):** short-lived, default 1 hour. Stored in memory in the Shell (`supabase.auth.getSession()` cached, not re-called on every render).
- **Refresh token:** single-use, does not expire by wall-clock time. Exchanged for a new access + refresh pair automatically by the Supabase client library. The library maintains a background timer keyed to the JWT `exp` field.
- **Session lifetime options configured in Supabase Dashboard:**
  - Inactivity timeout: recommended 8 hours for a workforce app (end of shift).
  - Absolute maximum: 30 days (covers leave periods without forcing re-enrol).
  - Single-session-per-user: NOT recommended for EQ — users legitimately access from a phone and a PC simultaneously (e.g., site super + admin).

### 4.2 Cross-App Token Exchange

The embedded apps (Field, Service) receive identity via a short-lived project-scoped JWT, not the Shell's eq-canonical JWT. This is handled by a Netlify Edge Function (`/api/token-exchange`):

```
1. Shell holds valid Supabase JWT (eq-canonical-internal).
2. When loading an embedded app, Shell calls /api/token-exchange:
   - Passes: Bearer {access_token}
   - Also passes: target_tenant_id (e.g., "sks")
3. Edge function:
   a. Verifies the JWT against eq-canonical-internal's JWKS endpoint.
   b. Reads eq_role, tenant_id, is_platform_admin from claims.
   c. Mints a new short-lived JWT (15 minutes, non-renewable) signed with
      the target app's Supabase JWT secret.
   d. Returns the scoped token.
4. Shell posts the scoped token to the iframe via postMessage (existing
   EQ_SERVICE_READY / EQ_FIELD_READY handshake, extended).
5. The embedded app initialises its Supabase client with this token.
   It is NOT a Supabase refresh-token session — it is a read/write access
   window that expires and must be renewed by the Shell.
```

This keeps the eq-canonical Supabase secret server-only and ensures that a compromise of the Field Supabase instance does not expose the canonical session.

### 4.3 Server-Side Auth in EQ Service (Next.js)

EQ Service uses Next.js route handlers (not client-side Supabase). The scoped token from the exchange is set as an `Authorization: Bearer` header on every fetch from the Shell. Route handlers verify it using `createServerClient` from `@supabase/ssr`, which reads the token from the header without needing a cookie.

---

## 5. Staged Migration Plan

> Auth changes require explicit deploy approval before each phase. This plan documents the design. No phase starts without Royce sign-off on that phase's work.

### Phase 0 — Supabase Auth Project Setup + Custom-Claims Hook

**What changes:**
- Confirm eq-canonical-internal is the target Supabase Auth project (not a new one — it already exists).
- Create `public.tenant_members` table if not already normalised: columns `auth_user_id` (FK → `auth.users.id`), `tenant_id`, `eq_role` (enum), `is_platform_admin` (boolean, default false), `created_at`, `updated_at`.
- Write and register the Custom Access Token Hook SQL function (design in §2.3).
- Enable the hook in the Supabase Dashboard: Authentication → Hooks → Custom Access Token.
- Write integration tests (in a throwaway branch, not prod) that mint a JWT via the hook and assert the claims shape.
- Configure passkey WebAuthn settings: relying party ID = `eq.solutions`, display name = `EQ`, allowed origins = `https://core.eq.solutions`, `https://cards.eq.solutions`.

**What's risky:**
- The hook runs on EVERY token issue and refresh. A bug in the hook silently breaks all logins — Supabase will return an internal error if the hook throws. The mitigation is to add a `BEGIN ... EXCEPTION WHEN OTHERS THEN RETURN event; END` guard that fails open (returns the token without custom claims) rather than blocking login.
- `tenant_members` data must be accurate before the hook goes live; stale or missing rows produce null claims, which RLS policies then reject. Backfill must be verified before enabling.

**Rollback:**
- Disable the hook in the Supabase Dashboard (one toggle). All tokens revert to standard Supabase JWT claims. No code change required.

---

### Phase 1 — Passkey / WebAuthn Enrollment + Login UX

**What changes:**
- Build the passkey enrollment flow (design in §3.2) inside eq-shell, behind a feature flag (`feat_passkeys_beta`).
- Build the magic-link login screen (replaces the current PIN screen for Shell). Magic link is the baseline credential; passkey is the upgrade path.
- Build recovery code generation + download UI (§3.3).
- Build the Settings page passkey list (enrol another, revoke).
- The legacy PIN login screen remains live and unchanged in EQ Field. No field changes in this phase.
- `@supabase/supabase-js` upgraded to v2.105.0+ in eq-shell only.

**What's risky:**
- Supabase passkey API is in beta (as of 2026-05-28). The API surface may change without a major semver bump. Mitigation: pin the exact `supabase-js` version in `package.json`, not a range. Monitor the Supabase changelog before upgrading.
- WebAuthn Conditional UI (`autocomplete="webauthn"`) behaviour differs across browsers. Chrome 108+ and Safari 16+ support it natively; Firefox support arrived in v122. Test on the browsers actually used by SKS site staff (likely Chrome on Android + Safari on iPhone).
- Pre-flight device detection must be correct. If a device passes the detection check but the browser restricts WebAuthn in a non-secure context (e.g., a localhost test or an HTTP iframe), enrollment will fail with a confusing native error. All enrollment must happen in a top-level secure context, never inside an iframe.

**Rollback:**
- Flip `feat_passkeys_beta` flag off. Users see the existing magic-link screen. No database state is corrupted (passkey credentials are stored server-side in Supabase; unenrolling is reversible).

---

### Phase 2 — Shadow-Mode Dual-Run Beside HMAC

**What changes:**
- Introduce a parallel auth path in eq-shell: the new Supabase Auth login flow runs alongside the existing HMAC flow.
- A `feat_shadow_auth` flag (targeting Royce only initially) routes logins through Supabase Auth instead of HMAC.
- Both systems run: a user flagged into shadow mode gets a Supabase session; all other users continue with HMAC.
- The token-exchange edge function is deployed but only called for shadow-mode sessions.
- Structured logging added to both paths: emit a correlation ID on each login; log the auth method used (`hmac` vs `supabase`), time-to-session, and any error. Errors from the shadow path are captured but do not surface to the user — the system falls back to HMAC transparently.
- A parity check script runs nightly: for shadow-mode users, compare the permissions derived from the HMAC session versus the Supabase JWT claims. Log any mismatch.

**What's risky:**
- If the Supabase session and HMAC session diverge in role assignment (e.g., a role update applied to one system but not the other), the parity check catches it but the user might see different behaviour in different parts of the app during the overlap window.
- The token-exchange edge function is a new network hop. Latency must be measured. Budget: <150ms p95. If it exceeds this, optimise with `waitUntil` background refresh rather than blocking the iframe load.
- HMAC and Supabase JWT secrets must not be cross-contaminated. The edge function must only be able to verify eq-canonical-internal JWTs; it must not expose the HMAC secret.

**Rollback:**
- Set `feat_shadow_auth` flag to 0% rollout. All users return to HMAC immediately. No data loss — Supabase sessions are independent of HMAC state.

---

### Phase 3 — App-by-App Cutover

**Recommended cutover order: eq-shell → eq-solves-service → eq-solves-field**

Rationale:

| App | Auth complexity | Why this order |
|---|---|---|
| **eq-shell** first | Lowest: already uses Supabase JWT for canonical queries. Shell is the auth hub — making it the source of truth first simplifies everything downstream. The Shell's HMAC surface is only the outbound iframe handoff, not inbound user login. | Supabase Auth login is already 90% wired in Shell. Shadow mode runs here. Cut Shell over first establishes the canonical session that everything else derives from. |
| **eq-solves-service** second | Medium: Next.js with server route handlers. Does not own login — it receives a token from Shell. Token exchange replaces the HMAC iframe token. Smaller surface area than Field. Service team (Royce) has full control over the codebase. | Once Shell emits Supabase JWT, Service just needs its route handlers updated to verify the scoped token instead of the HMAC token. One edge function + one middleware change. |
| **eq-solves-field** last | Highest: vanilla JS, owns its own login screen (4-digit PIN), multi-tenant, currently lossily maps to 2 roles. Requires the PIN retirement, the 5→5 role mapping, and the tenant-aware token exchange. Has live SKS users. | Field is the highest-risk cutover because it owns user-facing login for field workers who have no tolerance for lock-out. It goes last when the pattern is proven across Shell and Service, and when the Field merge (stream 2) is stable enough to do the auth work in one codebase. |

**Per-app cutover steps:**

**eq-shell:**
1. Ship Supabase Auth login as the default path (magic link + passkey).
2. Remove HMAC token generation for cross-app handoff. Replace with token-exchange edge function calls.
3. Keep the legacy `/auth/hmac-bridge` endpoint live for 2 weeks post-cutover (in case an app is not yet cut over and still expects HMAC).
4. Monitor login success rate for 72 hours. If below 98%, rollback.

**eq-solves-service:**
1. Update `middleware.ts` to verify the scoped Supabase JWT from the token exchange.
2. Remove HMAC verification logic from route handlers.
3. RLS policies on eq-canonical-internal (Service data) updated to use `auth.jwt()` claims pattern (§2.4).
4. Smoke-test: sign in through Shell, navigate to /service, verify work orders load, verify a manager-only action is gated correctly.

**eq-solves-field:**
1. Remove the 4-digit PIN login screen. Replace with a redirect to the Shell login (passkey/magic link). Field operates exclusively as an embedded app — it does not own login state.
2. Update the Supabase client initialisation to accept the scoped token from postMessage instead of its own credentials.
3. Expand the Field role mapping from 2 tiers to the full 5 tiers (uses `@eq-solutions/roles` MATRIX).
4. Apply RLS policies to all Field data tables using the claims pattern (§2.4).
5. Smoke-test with SKS tenant: sign in as manager → verify full access; sign in as labour_hire → verify restricted access.

**Rollback for each app:**
- eq-shell: re-enable `feat_shadow_auth` flag at 0% (reverts to HMAC login). Restore the HMAC iframe token emission.
- eq-solves-service: revert middleware to HMAC verification (git revert the middleware commit).
- eq-solves-field: restore PIN login screen from the last pre-cutover tag. Field is the most rollback-sensitive — keep the pre-cutover build tagged and the Netlify deploy frozen for 2 weeks.

---

### Phase 4 — Retire HMAC

**What changes:**
- Delete the HMAC token generation and verification code from eq-shell.
- Delete the HMAC verification logic from eq-solves-service.
- Delete the 4-digit PIN storage columns from the Field database (or archive them in a separate table for audit purposes — do not hard-delete without a snapshot).
- Remove `EQ_SECRET_SALT` and any other HMAC-related environment variables from Netlify.
- Archive the `/auth/hmac-bridge` endpoint (return 410 Gone with a log message).
- Update `@eq-solutions/roles` README and the eq-context auth docs to mark HMAC as retired.

**What's risky:**
- Any script, webhook, or integration that still sends an HMAC token will silently fail after this point. Audit all Netlify Functions and edge functions for HMAC header parsing before deleting.
- PIN columns contain hashed PINs (bcrypt). Deleting them is irreversible. Take a timestamped database snapshot before running the column drop migration.

**Rollback:**
- At this phase, there is no automated rollback. HMAC retirement is a one-way door. This is why the HMAC bridge endpoint is kept alive for 2 weeks post-Phase 3 before Phase 4 begins. If any app is still sending HMAC tokens at that point, it will be caught in logs and Phase 4 is delayed.

---

## 6. Per-Phase Risk Register

| Phase | Risk | Likelihood | Severity | Mitigation |
|---|---|---|---|---|
| 0 | Hook bug breaks all logins | Low | Critical | EXCEPTION guard; test in staging before prod; one-toggle disable |
| 0 | tenant_members backfill incomplete | Medium | High | Run count check before enabling hook: `SELECT count(*) FROM auth.users LEFT JOIN tenant_members ON ...` |
| 1 | Passkey beta API changes | Medium | Medium | Pin supabase-js version; monitor changelog |
| 1 | WebAuthn blocked in iframe | Low | Medium | Enrollment only in top-level context |
| 2 | Role mismatch between HMAC and Supabase | Medium | Medium | Nightly parity check; correlation ID logging |
| 2 | Token exchange latency | Medium | Low | Measure p95; cache scoped token for iframe lifetime |
| 3 | Field user lock-out on PIN removal | Low | Critical | Field goes last; full rollback tag kept; staff comms before cutover |
| 3 | Service route handler regression | Low | Medium | Full smoke-test before removing HMAC fallback |
| 4 | Undiscovered HMAC consumer | Medium | High | Audit all functions; 2-week bridge window; monitor 410 logs |

---

## 7. Dependency Map

```
Phase 0 (hook + tenant_members)
  └─► Phase 1 (passkey UX) — requires hook to be live and stable
        └─► Phase 2 (shadow mode) — requires Phase 1 Shell login to exist
              └─► Phase 3 (Shell cutover) — requires shadow parity confirmed
                    └─► Phase 3 (Service cutover) — requires Shell cutover complete
                          └─► Phase 3 (Field cutover) — requires:
                                ├─ Service cutover complete (pattern proven)
                                └─ Field merge (stream 2) stable or scoped out
                                      └─► Phase 4 (HMAC retire) — 2 weeks after Field cutover
```

External dependencies:
- `@eq-solutions/roles` pushed to a remote repo (currently local-only, pending Royce OK on visibility).
- Supabase passkey API graduating from beta (or explicit decision to accept beta risk).
- Field merge (stream 2) either complete or explicitly scoped out of this auth work.

---

## 8. What This Solves (Summary)

| Problem today | Solved in phase |
|---|---|
| 5 places to edit a role | Phase 0 (tenant_members + hook = single source) |
| Field lossily maps 5 tiers to 2 | Phase 3 Field cutover |
| 4-digit PIN is brute-forceable | Phase 1 (retired from Shell), Phase 3 (retired from Field) |
| HMAC tokens are self-signed, no federation | Phase 3 (replaced by token exchange) |
| Cross-app SSO is fragile (3 modes) | Phase 3 (one token model via Shell session + exchange) |
| New apps must implement their own auth | Post-Phase 4 (all new apps inherit Supabase IdP for free) |

---

## 9. Open Questions for Review

1. **Supabase passkey beta risk appetite:** Accept beta API now, or wait for GA? Waiting is safer; shipping sooner proves the pattern faster. Decision: Royce.
2. **Field merge timing:** Does the Field cutover (Phase 3c) happen before or after the Field codebase merge (stream 2)? Doing it before means auth work happens twice (once per repo). Recommendation: do Field cutover in the merged codebase, which means Phase 3c is gated on stream 2.
3. **SKS entity auth:** SKS tenant authenticates against `sks-canonical` (its own Supabase project). Does that project also get the Custom Access Token Hook, or does it rely on the eq-canonical hook via the token exchange? Recommendation: SKS gets its own hook instance on sks-canonical for full entity separation. Design doc for SKS auth is a separate spike.
4. **Recovery code storage:** bcrypt hashing of recovery codes is standard. Alternatively, use a HMAC with a server secret (faster to verify, no timing variation). Either is acceptable; decision affects the `recovery_codes` table schema.
5. **Passkey sync across devices:** If a user enrolls a passkey on their phone and the passkey syncs via iCloud Keychain or Google Password Manager, it will also work on their other Apple/Google devices. This is a feature (reduces lock-out risk) but should be documented in the user-facing help text.

---

*End of spike. Review before any code is written. Auth changes require explicit deploy approval per global rules.*
