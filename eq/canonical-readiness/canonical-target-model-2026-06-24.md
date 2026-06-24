---
title: Canonical Target Model — one Supabase per tenant, canonical = a schema inside it
owner: Royce Milmlow
last_updated: 2026-06-24
scope: The go-forward data-architecture model for the EQ suite, locked + substrate-verified
read_priority: high
---

# Canonical Target Model (locked 2026-06-24)

Locked with Royce, verified against the live substrate via Supabase MCP. This is the
go-forward target **and** the correct mental model — it resolves the recurring
"is canonical a separate database?" confusion. Context: Field and Service were built
standalone first, so wiring is clunky and entities are duplicated; this is what
everything converges to.

## The model

- **One Supabase per tenant.** `ehow` (SKS) is the reference implementation. A tenant's
  whole suite (Cards / Field / Service) lives in **one** database, so cross-app read/write
  is just a cross-*schema* query — trivial, no sync, no federation.
- **"Canonical" = the shared, DEFINED schema (`app_data`) *inside* the tenant DB — NOT a
  separate database.** On ehow: `app_data` = canonical spine (people / sites / customers /
  assets / licences); `public` = EQ Field app-only (schedule / timesheets / prestarts /
  toolbox); `service` = EQ Service app-only + `security_invoker` bridge views over `app_data`.
- **jvkn (`jvknxcmbtrfnxfrwfimn`) = control plane / switchboard ONLY** — registry
  (`organisations` → which tenant DB) + Cards onboarding (`workers`) + `shell_control`. It is
  **not** operational data (its `app_data` is 2 junk gm_report tables). Do not mistake jvkn
  for "the canonical database."
- **Canonical TRUTH = definition/ownership, not colocation.** Colocation makes it *easy*;
  "**defined throughout**" — one agreed table per entity, one ID scheme, a clear writer,
  everyone else references — makes it *true*. That is governance, and it is why unreviewed
  migrations to the shared layer are dangerous: they erode "defined."

## ktmj is legacy — to be deleted

`ktmj` (`ktmjmdzqrogauaevbktn`) is **one DB shared by three tenants** (eq / demo-trades /
melbourne) — the *old* shared-multi-tenant model the target replaces. Still load-bearing:
the registry routes those three → ktmj, EQ Field connects to it for them (605 people / 2417
schedule), and Cards approvals write to it. **SKS never touches ktmj.** So "delete ktmj" =
retire/migrate the demo tenants first, not a no-op. `zaap` (EQ canonical) migration is stalled.

## Build implication

"Canonical-direct" for Field = point Field at the shared `app_data` schema in the tenant DB
it is **already in** (ehow) — same database, different schema. **SKS first** (only it has the
spine). It is small and mostly *deletes* the copy/sync layer (`syncAllToCanonical`,
`canonical_synced_at`, the import copy). Auth nuance: `app_data` RLS needs a per-tenant JWT or
a SECURITY DEFINER RPC — Field already uses the RPC pattern for the Cards panel
(`eq_field_get_worker_summary`). EQ tenants follow once each has its own per-tenant Supabase + spine.

## Verified topology (2026-06-24, BASE TABLE / VIEW)

| Project | app_data | public | service | shell_control |
|---|---|---|---|---|
| ehow (SKS tenant) | 110 / 12 | 61 / 3 | 30 / 24 | 5 / 0 |
| ktmj (EQ demo tenants) | — | 48 / 2 | — | — |
| jvkn (control plane) | 2 / 0 (junk) | 17 / 0 | — | 28 / 0 |

## Open next step — DONE (2026-06-25)

Entity double-up audit completed and turned into the sequenced consolidation plan:
**`canonical-consolidation-roadmap-2026-06-25.md`**. Key finding: Field is already
~80% on canonical for SKS (JWT data-plane + `app_data.field_*` twins over the spine —
NOT cosmetic pass-throughs). Remaining gaps + the phased path (governance → finish SKS
Field → consolidate Quotes/Licence → person passport/badge → consent layer → retire
ktmj) live in the roadmap. Related: `service-consumes-canonical-spine-2026-06-16.md`,
`spine.md`.
