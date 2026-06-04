---
title: OPS — Weekend Security Execution Sheet
owner: Royce Milmlow
last_updated: 2026-06-05
scope: Copy-paste-ready, precondition-verified steps for the two weekend-safe security fixes (SEC-2 zaap RLS; SEC-1 nspbm interim anon-disable). Staged 2026-06-05 — NOT yet applied.
read_priority: critical
status: live
---

# Weekend Security Execution Sheet

Two fixes, **staged and verified against live on 2026-06-05, not applied.** Run
them yourself in the weekend window. Each has: precondition (already checked),
exact SQL/step, post-apply verification, and rollback. Tracking:
`ops/security-register.md`.

> **Nothing here has been executed.** SEC-1 touches **SKS-live** (`nspbm`); SEC-2
> touches Field's live DB (`zaap`). Both are yours to fire.

---

## SEC-2 — Fix the `user_metadata` RLS hole on `zaap` (P1, advisor ERROR)

**What:** `app_data.eq_intake_rate_limits` policy `tenant_isolation` derives the
tenant from `user_metadata` (end-user-editable → tenant isolation bypassable).

**Precondition — VERIFIED 2026-06-05:** every other tenant-isolated table on `zaap`
(24+ policies: `customers`, `contacts`, `assets`, `field_people`,
`field_timesheets`, …) already uses `app_metadata.tenant_id`. This table is the
lone outlier. The fix below makes it match the proven pattern — low risk.

**Apply (run on `zaap` = `zaapmfdkgedqupfjtchl`):**
```sql
-- before: USING (tenant_id = ((auth.jwt() -> 'user_metadata' ->> 'tenant_id')::uuid))
drop policy if exists tenant_isolation on app_data.eq_intake_rate_limits;
create policy tenant_isolation on app_data.eq_intake_rate_limits
  for all to public
  using (tenant_id = ((auth.jwt() -> 'app_metadata' ->> 'tenant_id')::uuid));
```

**Verify (expect `app_metadata`, no `user_metadata`):**
```sql
select qual from pg_policies
where schemaname='app_data' and tablename='eq_intake_rate_limits';
```
Then re-run advisors → the `rls_references_user_metadata` ERROR should clear.

**Rollback:** re-create the policy with `user_metadata` (the line in the comment
above). Only needed if rate-limiting breaks for legitimate users — which would
mean JWTs don't carry `app_metadata.tenant_id` (they do; 24 working policies prove it).

**After it's confirmed:** remove the `rls_references_user_metadata_…` entry from
`scripts/security_audit.py` `ACCEPTED_ERRORS`.

---

## SEC-1 — Interim-disable anon reads on SKS Labour (`nspbm`) (P0, LIVE PII)

**What:** the SKS Labour public key reads live staff PII. **Run the moment the NSW
team is off SKS Labour** (i.e. once they're on Field) — this breaks the legacy
app's anon reads *on purpose*. Do not run while the team still depends on it.

**Leak surface — VERIFIED 2026-06-05 (broader than the 4 spot-probed tables):**
~40 `public` tables grant anon SELECT; 19 have literal always-true anon policies
(`app_config`, `nominations`, `tenders`, `pending_schedule`, `teams`,
`team_members`, `site_diaries`, …) and others (`people`, `timesheets`,
`leave_requests`, `audit_log`, `schedule`, `sites`, `managers`, `sks_quotes_*`)
leak via conditional-but-permissive policies. **Per-table REVOKE is fragile — use
one of the blunt, complete options below.**

### Option A — kill all anon reads in one statement (recommended interim)
Keeps the project alive (in case anything still references it) but closes the
entire read leak. **Reversible.**
```sql
-- run on nspbm = nspbmirochztcjijmcrx, AFTER the team is on Field
revoke select on all tables in schema public from anon;
-- (optional, fuller lockdown if nothing legit uses anon writes anymore:)
-- revoke insert, update, delete on all tables in schema public from anon;
```
**Verify:**
```
RLS_PROBE_PROJECT=sks-labour python3 scripts/rls_probe.py   # expect all 401/empty
```
**Rollback (instant):** `grant select on all tables in schema public to anon;`

### Option B — full decommission (cleanest for a retiring app)
Pause the whole project — total stop, reversible via restore.
- Dashboard → project `nspbmirochztcjijmcrx` → Settings → **Pause project**
- or Management API `POST /v1/projects/{ref}/pause`.
Use this once you're confident nothing references `nspbm` anymore (it's
off-registry — nothing in the control plane points at it).

**After the leak is closed (either option):** remove the four `sks-labour.public.*`
entries from `scripts/rls_probe.py` `KNOWN_LEAKS` so the probe goes fully green.

---

## SEC-3 — F1 ehowg key rotation (optional this window)

Full ready-to-run steps live in **`f1-ehowg-key-rotation-runbook-2026-06-03.md`** —
do **not** duplicate them here. Re-verified 2026-06-05: still OPEN (the `sks`
routing row's `status_changed_at` is unchanged at 2026-05-24 → never re-keyed).
Coordinated rotation (Supabase JWT secret → Quotes Fly secret → re-encrypt
`tenant_routing` → verify legacy = 401). **Only attempt with the two secrets in
hand** (eq-shell `TENANT_ROUTING_MASTER_KEY` + a Supabase `sbp_` token) and
accept a ~1-min Quotes blip. If unsure, defer to the cutover's Phase C (you're in
`ehowg`'s auth lane there).

## Order & timing

1. **SEC-2** — any time in the window (independent of cutover; `zaap` is live so
   apply during low traffic + smoke-test Field after).
2. **SEC-1** — *after* the team has moved onto Field for real. If full Phase-E
   decommission isn't happening this weekend, Option A is the interim that closes
   the live PII exposure without waiting.
3. **SEC-3 (F1)** — optional; only with both secrets in hand. Else defer to Phase C.

All three are tracked in `ops/security-register.md` and referenced from
`CUTOVER-RUNBOOK.md` §6.
