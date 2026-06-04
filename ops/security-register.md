---
title: OPS — Security Register
owner: Royce Milmlow
last_updated: 2026-06-05
scope: Single tracked register of open security findings across the EQ/SKS Supabase surface — advisor output + live probes + known P0s
read_priority: critical
status: live
---

# Security Register

One place for every open security finding across the six Supabase projects.
Generated 2026-06-05 from live `get_advisors` + `scripts/rls_probe.py` +
`scripts/security_audit.py`, merged with the known P0 runbooks. Re-run those
tools to refresh; close items here as they're fixed.

**Gating:** `.github/workflows/security-audit.yml` runs the probe (no secret)
and the advisor audit (`SUPABASE_ACCESS_TOKEN` secret — not yet set) weekly +
on demand. The probe baselines known leaks (`rls_probe.py` `KNOWN_LEAKS`) so CI
fails on **new** exposure while keeping the open ones visible.

## Priority list

| ID | Severity | Finding | Project | Status |
|---|---|---|---|---|
| SEC-1 | **P0 — live PII leak** | Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` | sks-labour (LIVE) | OPEN — fix in B5 (review_by 2026-06-09) |
| SEC-3 | **P0** | Exposed `ehowg` service_role key still live (F1) | sks-canonical (LIVE) | OPEN — Royce-gated, runbook ready |
| SEC-2 | P1 | RLS policy `tenant_isolation` trusts end-user-editable `user_metadata` (advisor ERROR) | eq-canonical-internal | OPEN (review_by 2026-06-12) |
| SEC-4 | P1 — verify | `anon`-executable SECURITY DEFINER fns incl. `eq_cards_get_worker_hr_record`, `eq_cards_claim_invite` | eq-canonical | OPEN — verify anon can't extract/mutate |
| SEC-5 | P1 — verify | Permissive RLS (`USING/WITH CHECK = true`) write policies | eq-solves-field (27 tbl, LIVE), eq-canonical-internal (22), sks-labour | OPEN — confirm role (anon vs auth) + scope |
| SEC-6 | P2 | `context_proposals` anon INSERT has length caps but no volume throttle | eq-substrate | OPEN — needed before the queue has a consumer |
| SEC-7 | P3 | `function_search_path_mutable` (search_path not pinned) | several projects | OPEN — hygiene, fix at next touch |
| SEC-8 | P3 | `pg_net` extension installed in `public` schema | sks-labour | OPEN — move to `extensions` schema |

## Detail

### SEC-1 — sks-labour public key reads staff PII (P0, LIVE)
`scripts/rls_probe.py` 2026-06-05: a `GET` with the **public** publishable key
returned rows from `public.people`, `public.timesheets`, `public.leave_requests`,
and `public.audit_log` (5,752 rows). The anon key ships in the SKS Labour
browser app, so anyone who extracts it can read staff personal data. Root cause:
SKS Labour is the pre-canonical anon-model app (the "I1 access codes / B5" debt).
**Fix:** enable RLS + scoped policies (or move the app off the anon read path) as
part of the **B5 cutover** this weekend. ⚠️ This is **SKS-live** — enabling RLS on
tables the running app reads via anon can break the app; stage and test. Do NOT
"quick-fix" on live. Tracked in `rls_probe.py` `KNOWN_LEAKS` until closed.

### SEC-2 — eq-canonical-internal RLS trusts user_metadata (P1, advisor ERROR)
`app_data.eq_intake_rate_limits` policy `tenant_isolation` references
`auth.user_metadata`, which end users can edit — so a user can forge their tenant
and bypass isolation on that table. **Fix:** rewrite the policy to derive tenant
from `app_metadata` (server-controlled) or a trusted claim, matching the
`sks_safety_rpc_jwt_tenant_guard` pattern already used. Baselined in
`security_audit.py` `ACCEPTED_ERRORS` until fixed.

### SEC-3 — F1: exposed ehowg service_role key still live (P0)
Full runbook: `f1-ehowg-key-rotation-runbook-2026-06-03.md`. The leaked
sks-canonical service_role key is still valid. Rotate the JWT secret / disable
the legacy key — but only after propagating the new key to BOTH consumers
(Quotes Fly secret + `tenant_routing` re-encrypt), or live Quotes + canonical
routing break. Royce-gated.

### SEC-4 — anon-executable SECURITY DEFINER functions (P1, verify)
eq-canonical exposes 4 functions to the **anon** role as SECURITY DEFINER incl.
`eq_cards_get_worker_hr_record`, `eq_cards_claim_invite`, `eq_cards_preview_invite`,
`eq_cards_delete_account`. SECURITY DEFINER runs as the owner, bypassing RLS — if
any returns/mutates data for an unauthenticated caller, it's a hole. **Not probed
automatically** (calling unknown functions can mutate). **Action:** manually
confirm each requires a valid invite token / is safe for anon, else `REVOKE
EXECUTE ... FROM anon` or switch to SECURITY INVOKER.

### SEC-5 — permissive write-RLS clusters (P1, verify)
`rls_policy_always_true` on 27 tables (eq-solves-field, LIVE), 22
(eq-canonical-internal), and several on sks-labour (incl. `audit_log` anon insert,
`nominations` full anon CRUD). A `true` write policy can mean cross-tenant or anon
writes. **Action:** confirm the granted role and intended scope per cluster;
tighten any that allow `anon` or cross-tenant writes. Field is daily-used and
live — prioritise it.

### SEC-6 — context_proposals volume throttle (P2)
Length caps applied (migration `context_proposals`), but anon can still insert
many small rows. Add a per-session/IP throttle (edge function) before the queue
gets a consumer, or restrict INSERT to authenticated.

### SEC-7 / SEC-8 — hygiene (P3)
`function_search_path_mutable` on assorted functions — add `SET search_path =
public, pg_temp` at next edit (see `system/lessons.md`). `pg_net` in `public` on
sks-labour — relocate to an `extensions` schema.

## Clean projects (probe + advisors, 2026-06-05)
- eq-canonical, eq-canonical-internal, sks-canonical, eq-solves-field,
  eq-substrate: public-key reads all `401`/empty (no anon read leak).
- ERROR-level advisors: only SEC-2. All other advisor output is WARN/INFO
  (SECURITY DEFINER-callable-by-authenticated, permissive policies, search_path).
