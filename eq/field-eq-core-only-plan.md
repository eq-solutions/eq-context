---
title: Plan — Retire the EQ Field PIN gate (EQ tenant → Core-only)
owner: Royce Milmlow
created: 2026-07-11
status: planned (not started)
scope: eq-field (single repo). Core/canonical/shell already ready — no eq-shell build.
read_priority: reference
---

# Plan — EQ Field PIN gate retirement (`eq` tenant → Core-only)

**Goal:** Retire the standalone PIN gate in EQ Field by making the `eq` (sandbox) tenant
authenticate via Core (Shell JWT handoff), exactly like `sks` already does — then delete the
now-dead server PIN code. Decided direction (Royce, 2026-07-11): **role-based supervision, full
strip** (no manual supervisor-password escalation once done). Keep the `?tenant=demo` in-memory
slug for standalone dev.

## Why this came up
Asked to "strip the redundant PIN gate code." On inspection the PIN code is **not** cleanly
redundant — it's three distinct mechanisms, and two are load-bearing:
1. **Gate staff/supervisor PIN** (`checkPin` → verify-pin `code` branch) — SKS disabled (Core-only,
   v3.5.200); **EQ sandbox: still the front door + mints the session token EQ needs for
   send-email / EQ Agent** (`_mintAndStoreEqToken`).
2. **Supervision unlock** (`submitManagerPassword` → same verify-pin `code` branch,
   `role:'supervisor'`) — **load-bearing on both tenants** (staff→supervisor escalation).
3. **Staff-timesheet PIN** (`checkStaffTsLogin` → `verify_staff_pin` RPC, NOT verify-pin) — the one
   documented as redundant, already guard-disabled for SKS; EQ uses the legacy path.
A naive strip breaks EQ login + supervision unlock. The real path is to make `eq` Core-only first.

## Verified readiness (live, 2026-07-11)
**Core / canonical / shell are already `eq`-ready — no eq-shell build needed.**
- Canonical `organisations.eq`: tenant_id `dcb71d03-858d-488a-b8e6-b76b404d25d6`, zaap
  (`zaapmfdkgedqupfjtchl`), `is_seed_demo=true`, tier Standard, branding present.
- Shell `tenant_routing.eq`: status **active**, zaap provisioned (same day as SKS).
- Shell `tenants.eq`: `field_tenant_slug='eq'`, field-scoped (`app_tenant_scope` has field/eq),
  **2 `manager` members with email** (Royce is one).
- eq-shell field route + `token-exchange.ts` are **fully tenant-generic** — `eq` is the *default*
  in every allow-list (`ALLOWED_FIELD_TENANT_SLUGS = ['eq', …]`, `field_tenant_slug` CHECK accepts
  `'eq'`, `TENANT_OPTIONS` has `eq → "EQ Demo"`). SKS is the special-cased one, not eq.
- `verify-pin.js` already knows `eq` (`DATA_TENANT_IDS.eq`, `ZAAP_JWT_SECRET`).

## ⚠️ Phase 0 finding (smoked live via Core, 2026-07-11) — THE DOOR IS BROKEN
Opened `core.eq.solutions/eq/field` signed in as an `eq` manager (Royce). Core resolved the route
and mounted the Field iframe — **but EQ Field fell back to its demo PIN gate** (name "Demo
Supervisor", codes `demo`/`demo1234`) behind the error *"EQ Field lost its sign-in and automatic
recovery didn't work."* Reproduced twice.

**Root cause:** `auth.js` hardwires `eq` into demo-mode (`if (TENANT.ORG_SLUG === 'eq' || 'demo')`),
so the `eq` tenant short-circuits to the local demo gate and **never runs the shell handoff**
(`verify-shell-cookie` / `verify-shell-token`) that SKS uses. Core mints the session; EQ Field
discards it. (Handoff POST is made by the cross-origin `eq-field` iframe → invisible to top-frame
network capture; the on-screen demo gate is the definitive tell.)

**Consequence for sequencing:** the demo PIN gate is currently the **only working auth for `eq`**.
Stripping it first would lock every `eq` user out. **The strip must come last.**

## Plan (single repo: eq-field)

| Phase | Work | Status |
|---|---|---|
| **0** | Prove the door | ✅ DONE — broken (demo-gate fallback) |
| **1 (blocker)** | **Wire the `eq` shell handoff in EQ Field.** Stop `eq` short-circuiting to demo-mode when Shell-embedded; run `verify-shell-cookie`/`token` for `eq` like SKS. Confirm Core cookie-vs-token mode for the `eq` Field URL (`field.eq.solutions` = `.eq.solutions` host → cookie mode). Verify `core.eq.solutions/eq/field` signs in clean (supervisor via `manager` role). | TODO |
| **2** | Make `eq` Core-only. Extend the SKS `_lockGateForCoreOnly()` guard to `eq` in `checkPin()` + `checkStaffTsLogin()`; standalone `field.eq.solutions` → "opens from Core" panel. **Keep `?tenant=demo`** (in-memory) for standalone dev. | TODO |
| **3** | Strip the dead PIN code. Role-based supervision (decided): remove the verify-pin `code` branch, `fetchPinCodesFromDB`, `STAFF_CODE`/`MANAGER_CODE` env, the PIN rate-limit; drop `submitManagerPassword`'s password path (supervision derives from the handoff role). Remove `checkStaffTsLogin` + `verify_staff_pin` usage. | TODO |

**Don't touch:** shell-handoff paths (`verify-shell-token`/`cookie`/`mint-data-jwt`), the
`?tenant=demo` in-memory short-circuit, and the v3.5.295 audit-org stamp fix.

**Risks / open checks for Phase 1:**
- Cookie mode needs the `.eq.solutions` domain — confirm the `eq` Field URL Core embeds is
  `field.eq.solutions` (cookie) vs `eq-field.netlify.app` (token). SKS is pinned to token mode by a
  hardcoded URL override; `eq` should flow the generic path.
- The `eq` demo-mode branch is also what shows the `demo`/`demo1234` hint UI — ensure removing it
  for the embedded case doesn't break the standalone `?tenant=demo` slug (separate code path).
- No staff-role `eq` members exist today (both are managers) — a staff test user must be added in
  Core to exercise view-only + confirm role-based supervision gating.

## Related
- Audit-org fix that surfaced this thread: [changelog v3.5.295] / `field-security-queue` memory.
- Cross-app handoff authority: `eq/identity/IDENTITY-MODEL.md`; field-embed generic route confirmed
  in eq-shell `src/App.tsx` + `src/lib/fieldTenants.ts` + `netlify/functions/token-exchange.ts`.
