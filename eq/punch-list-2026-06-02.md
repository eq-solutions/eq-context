---
title: EQ — Owner Punch List (resume after break)
owner: Royce Milmlow
last_updated: 2026-06-04
scope: Owner-only actions (Royce must do these by hand). Pick up here after the break.
read_priority: critical
status: live
---

# EQ — Owner Punch List

These are the **owner-only** actions that unblock value already built and switched off,
plus the security items. None need a dev — they're dashboard/secret/toggle actions.
Work top-down; CRITICAL first.

## ✅ Status (re-verified against LIVE systems 2026-06-02 — mostly DONE)

- ✅ **Field migrations** (#2/#5/#12/#15/#10/#11) — applied on `ktmjmdzqrogauaevbktn`.
- ✅ **Drift-CI secrets** — all set in eq-shell.
- ✅ **Fly deploy** — done.
- ✅ **Netlify `TENANT_ORG_UUID`** — done-per-Royce (MCP connector was down at recheck).
- ✅ **`supabase-env.txt`** — now gitignored.
- ✅ **Spine coherence** — FK integrity confirmed + `ON DELETE` normalised (migration 048, both tenant DBs).
- 🅿️ **GitHub PAT rotation** — parked.
- ⚪ **HIBP toggle** — optional.
- 🟡 **`ehowg` service-role key** — NOT rotated, BUT investigated: no evidence of real exposure (every committed JWT is an *anon* key; the service-role key is never committed, lives encrypted in `tenant_routing`). The "exposed" flag looks stale. Low priority — rotate lazily unless a *non-git* leak (chat/email/screenshot/contractor) is recalled.

Detailed steps below kept for reference.

> ⚠️ **Migration safety:** for the dormant-feature items (§3), apply the **actual
> migration from `field-feature-backlog-2026-05-30.md`** — confirm the columns against
> the live table first. Do NOT run hand-typed DDL from memory; the indicative columns
> below are a guide to *what* the migration adds, not a verified script.

---

## CRITICAL — unblocks built features / closes a real security hole

### 1. Set `TENANT_ORG_UUID` in Netlify (EQ Field)
- **Where:** Netlify → `eq-solves-field` site → Settings → Environment variables → Add.
- **Name:** `TENANT_ORG_UUID`
- **Value:** `1eb831f9-aeae-4e57-b49e-9681e8f51e15` (documented in `eq-solves-field/netlify/functions/verify-pin.js` header).
- **Verify first:** this value is the `org_id` in the **Field** DB (`ktmjmdzqrogauaevbktn`) `app_config` rows — confirm it matches before saving. (Note: eq-canonical's "EQ Solutions" org/tenant UUIDs are *different* control-plane IDs — don't use those here.)
- **Unblocks:** U6 — PIN read from Supabase `app_config` instead of plaintext env vars. Without it `verify-pin.js` silently skips the lookup.

### 2. Rotate the exposed sks-canonical service_role key
- **Where:** Supabase → `sks-canonical` (`ehowgjardagevnrluult`) → Settings → API → Service role key → **Rotate**.
- **Then propagate the new key to its 2 consumers:**
  - **eq-shell tenant routing** — re-encrypt + UPDATE the SKS row in `shell_control.tenant_routing` (needs `TENANT_ROUTING_MASTER_KEY`; pattern in `eq-shell/scripts/provision-tenant.mjs`).
  - **eq-quotes Fly secret** — `flyctl secrets set CANONICAL_SUPABASE_KEY=<new_key>` for app `eq-quotes-sks`.
- **Rule:** never echo or commit the key.
- **Unblocks:** closes the exposed-credential hole; keeps quotes write-through working.

### 3. ~~Apply the dormant Field migrations~~ — ✅ VERIFIED ALREADY DONE / N/A (2026-06-03)

> **Live-checked `information_schema` on `ktmjmdzqrogauaevbktn` (ACTIVE_HEALTHY). Do NOT re-run — existing columns will error:**
> - #12 `people.licence_expiry` ✅ exists · #2 `timesheets.approved`/`approved_by`/`approved_at` ✅ all exist · #10 `unavailability` table ✅ exists · #11 `staff_availability` table ✅ exists. **These are live at the data layer** — verify the UIs surface them rather than applying anything.
> - #5 `people.leave_balance_days` — MISSING, **but no Field code reads it (grep: zero `leave_balance`/`balance` refs). The feature is unbuilt, not migration-gated.** Net-new scope, not a dormant unlock. Adding the column is a no-op.
> - #15 `audit_log.target_name` — MISSING, **but the audit silent-fail was already fixed differently in v3.5.31** (`verify-pin.js` writes `manager_name`; `audit.js` uses `target_id`). Nothing writes `target_name` → adding it = dead column. No action.
>
> **Net: nothing to apply here.** This contradicted the §Status block above (which correctly said ✅ applied) — now reconciled. Original instruction retained below for history only.

Apply via Supabase Studio SQL editor (or MCP `apply_migration`). Source of truth: `field-feature-backlog-2026-05-30.md`. The UI for each already ships and degrades gracefully until the columns exist.

- **#12 Licence-expiry alerts** — adds licence-expiry date to people. → expiring/expired badges + dashboard compliance card.
- **#2 Timesheet approval** — adds `approved` / `approved_by` / `approved_at` to timesheets. → supervisor sign-off before payroll (also unblocks #18 supervisor tile).
- **#15 Audit-log UI** — adds `target_id` / `target_name` to `audit_log`. → searchable in-app audit page.
- **#5 Leave balance** — leave-balance columns (confirm exact schema in backlog). → remaining-balance display.
- **#10 / #11 Unavailability + self-serve portal** — unavailability schema + RLS (confirm exact schema in backlog). → staff self-mark availability.

---

## HIGH — security + CI

### 4. Rotate GitHub PATs
- **Where:** github.com/settings/tokens → revoke the 3 compromised PATs → issue **1** fine-grained PAT → update local `.git-credentials`.
- **Ref:** `eq/pending.md` "CRITICAL — Rotate GitHub PATs".

### 5. Set tenant-drift CI secrets (eq-shell repo)
- **Where:** GitHub → `eq-solutions/eq-shell` → Settings → Secrets and variables → Actions → New repository secret (×4):
  - `SUPABASE_ACCESS_TOKEN` = a PAT from supabase.com/dashboard/account/tokens
  - `CONTROL_PROJECT_REF` = `jvknxcmbtrfnxfrwfimn`
  - `CANONICAL_INTERNAL_PROJECT_REF` = `zaapmfdkgedqupfjtchl`
  - `SKS_CANONICAL_PROJECT_REF` = `ehowgjardagevnrluult`
- **Unblocks:** the `tenant-drift.yml` workflow (the guard that keeps tenants from silently diverging).

### 6. Enable HaveIBeenPwned check
- **Where:** Supabase → `eq-canonical` (`jvknxcmbtrfnxfrwfimn`) → Authentication → Settings → Security → toggle **Enable HaveIBeenPwned check** ON → Save.

---

## READY TO DEPLOY (when you choose)

### 7. Deploy EQ Quotes
- `cd eq-quotes-port && flyctl deploy` (app `eq-quotes-sks`, region `syd`). Live immediately; check `flyctl status` / `flyctl logs`. Confirm `CANONICAL_API_KEY_QUOTES` secret is set.

---

## HOUSEKEEPING (non-urgent)
- Clear `public.rate_limits` on `ktmjmdzqrogauaevbktn` (demo) if it's noisy.
- Write the Cowork brief for EQ Field (guardrails + branch rules) — `eq/pending.md`.

---

## After the punch list — the next BUILD step
With the gate dead, the spine mapped, and the operating model locked, Rung 0 (coherence) is the next build move, in this order:
1. **Spine `ON DELETE` normalisation** — the spine is *already* FK-enforced (correction 2026-06-02), so this is NOT a from-scratch build. The real task: make `ON DELETE` consistent on the spine, esp. `licences.staff_id` → `RESTRICT` so compliance history can't be silently deleted. Small surgical migration + a design call. (See `eq/canonical-readiness/spine.md`.)
2. **Drift guard** — wire `tenant-drift.yml` to enforce *structural identity* across tenants (uniform-schema operating model, see `ops/decisions.md` 2026-06-02).
3. **Then Rung 1** — the §3 migrations above turn the surfacing features on, over now-trusted data.
