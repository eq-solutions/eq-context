# GATE A — Worker auth provisioning: DECISION

**Date:** 2026-06-03 · **Owner:** Royce Milmlow · **Streams:** Cards + C-CANON · **Board:** Stream G (auth gate)
**Status:** DECIDED — Option A. Build approved on a branch; **production apply to live eq-canonical still requires explicit Royce deploy sign-off** (auth non-negotiable).

## Problem
`custom_access_token_hook` (live on eq-canonical `jvknxcmbtrfnxfrwfimn`) stamps `tenant_id`/`eq_role` into a user's JWT by reading **`shell_control.users`**. The ~38 SKS workers live in `public.workers` (operational entities), **not** `shell_control.users`. So a worker signing in via email/phone OTP gets a JWT with no `tenant_id` → routed to "No workspace access" → **0 of 37 can claim.** This is the sole blocker to worker adoption.

## Decision — Option A: provision at claim time
When a worker claims their invite, ensure a `shell_control.users` row exists for them: `id = auth.uid()`, `tenant_id =` their org's canonical tenant, `role = 'labour_hire'`, `phone` from the worker record. Implemented **server-side inside `eq_cards_claim_invite`** so it's atomic with the claim and client-agnostic (no Dart change needed).

**Rejected:**
- **Option B (extend the hook to fall back to org_memberships/workers)** — the hook runs on **every token mint for every user across Shell/Field/Cards/Quotes**; a bug locks out the whole platform. Unacceptable blast radius.
- **Option C (broader unified identity)** — already the substrate Phase 1.F shipped; not the gate itself.

## Why Option A
- **Blast radius contained to the claim flow** — worst case is "one worker can't claim," never a platform-wide lockout.
- **Aligns with IDENTITY-MODEL** — `shell_control.users` stays the single auth source of truth; we just provision into it at the moment of claim.
- **Reversible** (delete the row) and **multi-tenant safe** (explicit `tenant_id`).

## Approvals (per Royce "build it", 2026-06-03)
- ✅ Option A (provision at claim)
- ✅ Workers get role `labour_hire`
- ✅ SKS first (38), then widen
- ✅ The claim RPC may write `shell_control.users` (crosses the auth boundary — that's why it was gated)
- ⏳ **Production apply** (run the migration against live eq-canonical) — still requires an explicit deploy instruction.

## In-flight work to reconcile (IMPORTANT — do not fork)
There is already an active branch **`claude/otp-tenant-fix`** in eq-cards (admin onboarding + worker schema + claim flow + an auth fix: commit `0efcf29` *"wire phone OTP → shell-login-phone-otp JWT exchange to inject tenant_id"*). That is a **runtime exchange** approach to the same problem. Option A (provision-at-claim) is **complementary, not competing**: provisioning the `shell_control.users` row at claim makes the native hook stamp `tenant_id` on *every* future login (email/Google too, not just phone) and removes the dependency on the runtime exchange. **The owning stream (Cards/C-CANON) should reconcile the two on `claude/otp-tenant-fix`, not in a parallel branch.**

## Implementation (drop-in)
Add this block inside `public.eq_cards_claim_invite(p_token)` — after the `org_memberships` upsert, before the credential-promotion loop. Grounded against the live function (2026-06-03):

```sql
-- GATE A: provision the claiming worker into the auth directory so future
-- logins carry tenant_id (custom_access_token_hook reads shell_control.users).
-- org.id == tenant.id (1:1, confirmed live 2026-06-03), so org_id IS the tenant_id.
IF v_worker IS NOT NULL THEN
  INSERT INTO shell_control.users (id, tenant_id, role, name, phone, active, last_active_tenant_id)
  VALUES (
    auth.uid(),
    v_invite.org_id,
    'labour_hire',
    NULLIF(btrim(coalesce(v_worker.first_name,'') || ' ' || coalesce(v_worker.last_name,'')), ''),
    v_worker.phone,
    true,
    v_invite.org_id
  )
  ON CONFLICT (id) DO UPDATE
    SET active = true, last_active_tenant_id = EXCLUDED.last_active_tenant_id;
END IF;
```

- No client/Dart change (server-side in the SECURITY DEFINER RPC).
- **Confirm before apply:** (1) `org.id == tenant.id` is an invariant, not just seed coincidence; (2) the `eq_cards_claim_invite` definer role has `INSERT` on `shell_control.users` (cross-schema write) — if not, add a `GRANT` in the same migration.
- Unit/staging smoke test on **one** worker before any production apply: claim → confirm `shell_control.users` row → re-login → JWT carries `tenant_id` → Cards opens (not "No workspace access").

## Rollout
Test one SKS worker → confirm `shell_control` row written + JWT carries `tenant_id` + Cards opens (not "No workspace access") → monitor Sentry (`jwt_missing_tenant`) + Netlify logs → widen. Rollback: delete the row / revert the migration. The hook is fail-open (`EXCEPTION WHEN OTHERS THEN RETURN event`), so a bad insert can't crash logins.

## Sequenced with
1. **GATE A (this)** → workers can claim.
2. **PIN follow-up** (separate, cheap): SKS-Field `verify-pin` already has a Supabase-JWT path; it likely just needs `SUPABASE_JWT_SECRET` set on the SKS-Field Netlify site. Do after GATE A.

## Coordination
Cards-stream item (Stream G). **Claim it on `SPRINT-BOARD.md` before building — do not fork.**
