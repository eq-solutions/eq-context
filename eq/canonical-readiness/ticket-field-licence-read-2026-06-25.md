---
title: Ticket — EQ Field surfaces worker licences (consent-gated, reuse-first)
owner: Royce Milmlow
last_updated: 2026-06-25
status: SPEC — ready to build. Phase A = zero-backend (ships now). Phase B = post-security.
relates_to: canonical-consolidation-roadmap-2026-06-25.md (Decision D, Field-laggard)
---

# Ticket: EQ Field — surface worker licences (consent-gated)

## Goal
Show, in EQ Field, the licences a worker has **shared with this tenant** (type, number,
expiry) — respecting worker ownership: only licences the worker granted to this org via
`org_memberships`, **never `is_private` ones**. On-brand with "the worker owns their card":
managers see what the worker chose to share, not a surveillance view.

## Audit — what already exists (reuse-first; verified live 2026-06-25)
The whole chain is built **except the Field frontend**:
- **Pool data:** jvkn `licences`(14) / `licence_types`(21) / `certificates`(4), keyed by
  `user_id`; flags `is_private`, `deleted_at`, `never_expires`.
- **Consent gate:** `jvkn.org_memberships` (worker→org grant), 15 active rows; cards-approve
  inserts the membership on approval (`cards-approve-staff.ts:159-202`).
- **THE KEY FIND — an existing anon, org-gated RPC Field can call today:**
  `public.eq_get_licences_expiring_within(p_org_id uuid, p_days_ahead int DEFAULT 30)` —
  SECURITY DEFINER, **granted to anon + authenticated**, joins `licences → workers →
  org_memberships (org=p_org_id, status=active)`, filters `NOT is_private` + `deleted_at IS
  NULL`, returns `(licence_id, licence_type, licence_number, expiry_date, worker_user_id,
  worker_first_name, worker_last_name, worker_email, worker_phone)`. Sibling
  `eq_get_licences_expiring_on(p_org_id, date)` too. **No auth.uid() — so Field's existing
  anon channel works.**
- **Shell precedent (not directly usable):** `eq-shell/netlify/functions/staff-canonical-licences.ts`
  does the same consent gate + `is_private=false` + signed photo URLs, anchored by `staff_id`
  — but it's **Shell-session-gated**, so Field (separate origin, no Shell session) can't call it.
- **Field side ready:** `_loadCanonicalSummary(workerId)` (`scripts/people.js:1085`) already
  fetches jvkn anon for the Cards-record panel; Field holds the tenant's canonical org id from
  `loadTenantConfig` (`scripts/app-state.js`).

## Latent bug surfaced by the audit (fix in Phase B)
The Cards-record panel from PR #292 is **inert in Field today**: `eq_field_get_worker_summary`
guards on `auth.uid()`, but Field calls it with the **anon key** (no user JWT) → guard returns
0 rows → RTW/emergency silently blank. The correct Field gate is tenant→org→`org_memberships`
(what the licence RPCs use), **not `auth.uid()`**. The same org-keyed re-gate that completes
licences also un-inerts the RTW panel.

## Build — phased

### Phase A — ships now · ZERO backend/security overlap
- Field calls `eq_get_licences_expiring_within(<canonical org_id>, 3650)` via the existing
  anon channel (`CANONICAL_URL` + `CANONICAL_ANON_KEY`), cached per session.
- Match licence rows to Field people by **email/phone** (the RPC returns `worker_user_id` +
  email/phone, not a `worker_id`/`staff_id` anchor).
- Render a "Licences" block in the Cards-record panel (per person) + optional people-list
  badge — **reuse the RTW expiry colour logic** (`people.js:1112-1115`: <30d red, <60d amber,
  else green; EXPIRED red).
- **Accepted limitation:** the RPC's `expiry BETWEEN today+1 AND today+N` window excludes
  **already-expired** and **never_expires** licences → Phase A shows current/upcoming only.
  Label the block honestly (e.g. "Active & upcoming licences"), not "all licences".
- Pure frontend + an existing anon RPC ⇒ no migration, no auth bridge, safe during the
  security update.

### Phase B — completeness · apply via One Pipe AFTER the security work
- New RPC `eq_get_org_licences(p_org_id uuid)` — same joins + consent/privacy gates as
  `expiring_within`, **minus** the expiry-window filter, and **returns a `worker_id`/`staff_id`
  anchor** (`workers.id`/`workers.staff_id`) for clean per-person joins (no email/phone
  matching). Grant anon + authenticated.
- Re-gate `eq_field_get_worker_summary` on `org_memberships` instead of `auth.uid()` (or ship
  `_v2`) so the RTW panel works from Field's anon context — fixes the latent bug.
- These are **jvkn (control-plane) migrations → apply via eq-shell's One Pipe, coordinated
  with / after the security update.** Do NOT apply from Field/MCP while security is in flight.

## Constraints
- Worker owns their card: only `is_private=false` licences the worker granted to this org;
  never bypass the `org_memberships` gate.
- No new anon control-plane RPC applied while the security/auth update is in flight.
- Don't add `@sentry/*` or a build step to Field (deliberate — Field is bundler-free).

## Contracts (for the build)
- RPC (existing): `eq_get_licences_expiring_within(p_org_id uuid, p_days_ahead int) → setof
  (licence_id, licence_type, licence_number, expiry_date, worker_user_id, worker_first_name,
  worker_last_name, worker_email, worker_phone)`. Granted anon+authenticated.
- Field org id: canonical `org.id` from `loadTenantConfig` (`app-state.js`) — verify exact
  exposed variable at build time.
- Render reuse: RTW expiry colour logic, `people.js:1108-1118`.
