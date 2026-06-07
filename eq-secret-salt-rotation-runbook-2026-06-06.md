---
title: EQ_SECRET_SALT rotation runbook
owner: Royce Milmlow
scope: Coordinated rotation of the platform-wide EQ_SECRET_SALT HMAC key
read_priority: critical
status: live
created: 2026-06-06
last_updated: 2026-06-06
---

# EQ_SECRET_SALT rotation runbook

## Why (do this BEFORE onboarding real users)
`EQ_SECRET_SALT` is the **platform-wide HMAC key** that signs:
- EQ Field session tokens + the EQ Shell iframe handoff tokens (`verify-pin.js`
  `signToken` / `verifyShellToken`), and
- the cross-app **`eq_shell_session` cookie** (`Domain=.eq.solutions`) that powers
  SSO from `core.eq.solutions` into Field/Service.

The current value is the **demo salt `eq-field-demo-2026-xR7kP9`**, which was
exposed in a chat transcript (flagged in the eq-field CLAUDE.md TODO) and is now
**shared across Shell + Field (+ Service)**. Anyone who holds it can **forge a
session/cookie as any user or tenant — including platform admin**. With real SKS
staff about to onboard, rotate it first.

## Consumers (set the SAME new value on ALL of these — a mismatch silently breaks SSO)
Confirm each before rotating (search each repo's Netlify env for `EQ_SECRET_SALT`):
- **eq-shell** (`core.eq.solutions`) — signs the `eq_shell_session` cookie + shell tokens.
- **eq-solves-field** (`field.eq.solutions` / `field.sks.eq.solutions`) — verifies the
  cookie/shell token; signs Field session tokens.
- **eq-solves-service** (`service.eq.solutions`) — the go-live runbook flags
  "EQ_SECRET_SALT parity Shell vs Service" as the silent #1 go/no-go. Confirm it uses it.
- **eq-quotes** — confirm whether it verifies shell handoffs (if so, include it).
Set on **all deploy contexts** (production + branch-deploy + deploy-preview) on each
site, or previews/smoke break (see the Netlify preview-env-scoping note).

## Method A — coordinated swap (RECOMMENDED while user count is ~0)
A hard swap invalidates every existing session/cookie → everyone re-logs-in. That's
**harmless now** (only a few admin sessions exist pre-onboarding) and needs **no code
change**. Do it before broad onboarding.

1. Generate a new high-entropy secret (do NOT reuse the demo pattern):
   `openssl rand -hex 32`  → `NEWSALT`.
2. In a single short window, set `EQ_SECRET_SALT = NEWSALT` (all deploy contexts) on
   **every** consumer site above (Netlify dashboard or `netlify env:set`).
3. Trigger a redeploy of each site so functions pick up the new env (Netlify functions
   read env at cold start; a redeploy guarantees it).
4. Verify (see Verification). Expect: existing sessions are now invalid → re-login once.

## Method B — zero-downtime (needed AFTER real users exist)
Once invalidating sessions is disruptive, do a dual-accept rotation (pattern already
shipped for `EQ_SHELL_BRIDGE_SECRET` in eq-shell #188):
1. Code change: have the verifiers accept **either** `EQ_SECRET_SALT` (new) **or**
   `EQ_SECRET_SALT_OLD` (previous) during a transition window. (verify-pin.js
   `verifyToken`/`verifyShellCookie`/`verifyShellToken` + the Shell cookie verifier.)
2. Deploy that everywhere; set `EQ_SECRET_SALT_OLD = current`, `EQ_SECRET_SALT = NEWSALT`.
3. After the max session/cookie TTL (7 days) elapses, remove `EQ_SECRET_SALT_OLD` +
   the dual-accept code. Old tokens are now gone.

## Verification (after either method)
1. `core.eq.solutions` → log in fresh → open `/sks/field`: SSO lands you authenticated
   (no PIN gate), supervisor (post eq-field #202), real SKS data.
2. `field.sks.eq.solutions` direct → PIN gate still mints a working session.
3. Confirm Service SSO still works (`service.eq.solutions` via Shell) — the parity item.
4. Check function logs for `EQ[auth] … verify failed` / 401 spikes (= a site missed the
   new value).

## Rollback
Re-set `EQ_SECRET_SALT` to the previous value on all sites + redeploy. (Method A: keep
the old value recorded until verification passes. Method B: the dual-accept window IS
the rollback.)

## Notes
- Treat the new value as a real secret — Netlify env only, mark it secret, never in chat
  or committed files. Also rotate the other exposures found 2026-06-06: the
  `GOOGLE_DOC_AI_CREDENTIALS` GCP private key (currently marked not-secret on the
  eq-shell Netlify site) and any service_role keys with unmasked dev-context values.
