---
title: Worker-Owned Credentials — Model & Phase-1 Sprint
owner: Royce Milmlow
last_updated: 2026-06-07
scope: The mechanics of worker-owned portable credentials (EQ Cards) and how businesses (SKS first) consume them via snapshot + live-link. Reconciles the worker-house data target with the Cards canonical-api rewire and the unified identity model.
read_priority: critical
status: live
---

# Worker-Owned Credentials — Model & Phase-1 Sprint

**Status:** decided (design) — Phase 1 build pending Royce-gated inputs.

Decisions taken 2026-05-31 (Royce + C4 console). This is the **design record — no
code yet.** It supersedes the Cards-rewire assumption that worker data routes to a
per-business-tenant DB (see *Reconciliation with the Cards rewire*).

## The wedge (one paragraph)

A tradie owns their licences / tickets / inductions in their own record (EQ Cards).
It helps **them** — renewal reminders, numbers on their phone. Businesses (SKS
first) pull that data in **on the worker's consent**, so onboarding/compliance
stops being re-keyed into every company's training matrix. The worker maintains
their own data because it benefits them, so the business gets current data for
free. Seed network = SKS's ~60-person workforce.

## Locked decisions

| # | Decision | Call | Consequence |
|---|---|---|---|
| 1 | Worker data home | **Worker-house** (`eq-canonical-internal`, `worker_*`) | Portable across businesses; Cards `gateway` points here, not a business DB |
| 2 | Worker identity | **First-class `worker_id`** in the control plane | Stable target for grants + live-link; survives leaving an employer |
| 3 | Seed strategy | SKS bulk-import **via Intake** = the tenant-verification event | 60 workers land pre-verified, not self-claimed |
| 4 | Trust basis | Evidence on file → **"verified by SKS, evidence on file"** (top tier) | A second business can trust it with no re-check |
| 5 | Build order | Worker-house + self-maintenance **first**; snapshot/live-link/grant **second** | No cross-house plumbing for the seed (SKS = source AND only consumer) |

**Trust tier is per-credential, set by the import** — not a blanket stamp. Where a
scan turns out missing, that credential drops to "sighted" or "asserted, capture
later." The gaps **are** the fault-finding output — a compliance audit for SKS that
pays off even at zero app adoption (the guaranteed floor; adoption is upside).

## Reconciliation with the unified identity model

See [IDENTITY-MODEL.md](./IDENTITY-MODEL.md). The worker is an **operational
entity** (§3.2, `staff`-like), **not** a multi-tenant auth `user`. Therefore:

- The v1 rule "one `user` belongs to one tenant" (§11 q2) is **unbroken** — a
  worker is not a multi-tenant user.
- The §11.2 v2 "multi-tenant membership" backlog item is addressed **not** by
  multi-tenant user rows but by the worker-house + **grant / live-link**: a
  business reads a worker's current status through a scoped, revocable grant; it
  never holds the worker as its own user.
- Cards auth binds an authenticated subject → `worker_id` (the portable
  operational identity). The §6.2 Supabase-JWT / `app_metadata.tenant_id` model
  still governs how Cards talks to Supabase.

## Reconciliation with the Cards canonical-api rewire (eq-cards PR #12)

The rewire assumed worker data routes to the caller's per-**business**-tenant DB
via `tenant_routing`. **Superseded:** worker data lives in the worker-house. The
`gateway` transport (or a dedicated live-link API) points at the worker-house, not
a business DB. **Do NOT flip the Cards `gateway` until G2 lands** — today it is
aimed at the wrong house. The live-link (Phase 2) is the generalisation the
cards-api gateway + a control-plane grant record were already heading toward.

## Phase 1 — build now (seed + self-maintenance)

1. **Mint `worker_id` + phone-keyed claim** for each of the 60 (phone = the binding
   key for tradies).
2. **Import via Intake** (not direct DB, not hand-typed): each credential →
   worker-house with trust stamp + evidence pointer, marked **"held on your behalf
   — confirm to claim."** First real test of the Intake write path.
3. **Claim-on-first-login:** worker opens Cards, phone matches their pre-seeded
   `worker_id`, sees their licences, taps "these are mine." Ownership affirmed;
   data never orphaned.
4. **Reminder engine live at launch — non-negotiable.** Stale seeded data is a
   liability (worker assumes the app has it handled, no reminder fires, gets caught
   on site; SKS's live-link would show "current" when stale). Expiry reminders +
   card-numbers-on-phone are what create the habit.

## Phase 2 — deferred until business #2 wants an SKS-verified worker

Snapshot-into-business-house (frozen, non-revocable legal record), grant-gated
live-link read, revoke + who-saw-what audit, cross-tenant trust policy. **Designed,
not built — no consumer yet.**

## Deferred sub-decisions (not needed for Phase 1)

- Where evidence scans live (shared bucket vs gateway-signed per-house).
- Cross-tenant auto-trust policy (does business #2 trust SKS's stamp, or re-verify?).
- Auth-hook GATE A specifics (OTP/OAuth JWTs carrying `tenant_id` / worker binding).

## Royce-gated inputs (block the Phase-1 build, not the design)

1. **Evidence export** ready — scans/photos + numbers + expiries for the 60. Format?
2. **Phone numbers** for the 60 (the claim binding key).
3. **Auth-hook GATE A** approval (live auth change).
4. **`sks-canonical` security lock** (RLS off + open anon key today) — F1-adjacent.

## Related

- [IDENTITY-MODEL.md](./IDENTITY-MODEL.md) — unified identity (worker = operational entity §3.2; multi-tenant backlog §11.2)
- [../cards/canonical-migration/plan.md](../cards/canonical-migration/plan.md) — Cards-side canonical migration
- eq-intake `EQ-TENANCY-MODEL.md` — tenancy model (separate DB per tenant)
- eq-cards PR #12 — canonical-api rewire (gateway transport seam)
- [SPRINT-BOARD.md](../../SPRINT-BOARD.md) Stream G — Phase-1 work items
