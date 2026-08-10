---
title: Worker & Customer Onboarding — Who Enters What, Per App
owner: Royce Milmlow
last_updated: 2026-08-10
scope: Answers system/punch-list.md item 1 — "one doc states the intended flow per scenario." Who actually gets a new person/customer/site/asset into each EQ app, by what mechanism.
read_priority: standard
status: live
---

# Worker & Customer Onboarding — Who Enters What, Per App

One place that states, per app and scenario, who actually does the work of
getting a new person/customer/site/asset into the system. Written 2026-08-10
from a live cross-repo survey (eq-shell, eq-field, eq-solves-service,
eq-cards) — not from memory or an old doc.

---

## EQ Cards — settled, self-join only

Decided 2026-08-08 (`eq/pending-archive.md`): a worker signs themselves up
via `shell-join-tenant.ts` — scans a tenant QR/join code, verifies their own
phone OTP, self-provisions. `AdminBulkInvite.tsx` solves a different problem
(inviting an already-known person), not a real gap here. No further work
needed on this app for onboarding specifically.

## EQ Shell — admin enters, worker completes

Two mechanisms, both admin-initiated:

- **Admin invite** (`netlify/functions/invite-user.ts`) — a manager/platform_admin
  (permission `admin.invite_user`) types in an email + role. A one-time
  hashed token goes to `user_invites`, emailed via `_shared/email.ts`. The
  recipient finishes via `accept-invite.ts`, setting their own PIN.
- **Worker invite** (`create-worker-invite.ts`) — same admin gate; admin
  types first/last name + phone, creates (or finds) a canonical `workers`
  row, generates a claim link sent via SMS/WhatsApp/email.
  `staff-invite-candidates.ts` / `check-never-invited-workers.ts` surface
  who's missing an invite — tooling finds the gap, an admin still closes it.
- **Bulk:** `invite-users-batch.ts` — same admin-driven shape, CSV-style batch.

**Actor: an admin types in the details; the worker completes the loop
themselves.** Working as intended — not a gap.

## EQ Field — manager enters, entirely independent of Shell

Two mechanisms, **both manager-driven, neither worker self-service, neither
linked to Shell's canonical `workers` registry**:

- **Manual entry** — `openAddPerson()` (`scripts/people.js`), gated on
  `canManagePeople()`. A supervisor/manager types name/phone/group/licence
  straight into the `people` table.
- **CSV bulk import** — `importPeopleToSB()` (`scripts/supabase-entities.js`).
  A manager uploads a CSV; matches existing rows by phone/email and upserts
  in place (fixed 2026-08-06 from an earlier wipe-and-replace bug).

Field does not read from or write to Shell's `workers` table for this.

## EQ Service — customers/sites flow in automatically; assets don't

- **Customers and Sites are not created in Service at all.**
  `app/(app)/customers/actions.ts` / `sites/actions.ts` both say so
  explicitly: Shell owns writes/approvals via the canonical layer; Service
  only reads via `app_data.*`. An EQ admin enters the customer/site once, in
  Shell's CRM (`crm-customers.ts`, `crm-write.ts`, `entity-insert.ts`) — this
  is the suite's one clean single-canonical-source example, no duplication.
  (Site access details — gate code, parking, after-hours phone — are the one
  Service-owned exception, via `updateSiteAccessAction`.)
- **Assets** enter via two EQ-staff-run importers, not customer self-service:
  `CommercialSheetImporter.tsx` (placeholder stub assets from a job-plan
  quantity sheet) and `lib/actions/asset-register-import.ts` (the real,
  named-asset workbook import, built 2026-07-11, replaces stubs). Actor: an
  EQ ops person parsing a client's workbook.
- Manual entry exists only for **contacts** at a customer/site
  (`createCustomerContactAction`) — not for the customer/site/asset entities
  themselves.

---

## The one real gap: worker identity duplicates across Shell and Field

A worker can be entered **independently** in EQ Shell (`workers` table, via
admin/worker invite) **and** EQ Field (`people` table, via manual entry or
CSV) with **no linking key today** — the same "two Matt Millers" problem
named in `ADR-PERSON-IDENTITY.md` at the **eq-field repo root** (not this
repo — verified live, checked before citing it here). The proposed fix
(`people.worker_id → workers.id`) is designed but unbuilt, parked pending
SKS stability ("do not start until the SKS tenant is stable in live");
Cards→Field SSO is explicitly blocked on it (most `workers` rows have a
null `user_id`). Don't re-propose the link without a fresh reason — it's a
known, deliberately parked gap, not an oversight.

## Not a gap: Customers/Sites (Shell → Service, read-only)

Named above — kept here too so this doc has one place that states both the
real gap and the clean counter-example, rather than only the problem.
