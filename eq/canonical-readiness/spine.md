---
title: EQ Canonical — The Trust Spine
owner: Royce Milmlow
last_updated: 2026-08-15
scope: Which canonical app_data tables must be identical/trusted across tenants vs free to vary per tenant
read_priority: critical
status: live
---

# EQ Canonical — The Trust Spine

Re-derived **2026-08-15** from the live `app_data` schema on **sks-canonical**
(`ehowgjardagevnrluult`) by reference-column analysis. First derived 2026-06-02;
**every headline number below changed in the 74 days between**, which is the
reason this doc now carries a review clock (F14).

## Why this doc exists

The roadmap to "ask the system anything and trust the answer" rests on a
**trust ladder**: coherence → surfacing → ask-anything → gating. Rung 0
(coherence) needs a precise answer to one question: *which tables must mean the
same thing in every tenant?* That set is the **spine**. The full schema ships
uniformly to every tenant; anything a specific business needs beyond the
standard lives in extension columns — we build software around the business via
extensions, not by diverging the shared schema.

## What changed since 2026-06-02

The June conclusion was "the must-align set is small — only 6 of 55 tables". The
schema has since **more than doubled**, and the spine grew with it:

| Measure | 2026-06-02 | 2026-08-15 |
|---|---|---|
| `app_data` base tables | 55 | **128** |
| FK constraints | ~70 | **137** |
| Tables carrying `tenant_id` | 53 | **121** (of 128) |
| Tables carrying `intake_id` | 46 | **46** (of 128) |
| Tables carrying `external_id` | 17 | **21** |

The headline claim still holds in spirit — most tables are app-local, the
must-align set is a minority — but "6 of 55" is no longer the number, and one
guarantee below has quietly decayed rather than grown.

## The spine entities

The nouns more than one app joins to, by distinct referencing `app_data` tables.
**The June set of 6 no longer matches this methodology's own output** — three
tables now outrank `contacts`, which was in the original six:

| Entity | Referenced by (Jun → Aug) | Role |
|---|---|---|
| **sites** | 18 → **28** | Biggest hub — field, service, quotes, safety |
| **staff** | 10 → **17** | Identity for HR, licences, scheduling |
| **assets** | 5 → **14** | Service, testing, safety |
| **customers** | 7 → **9** | CRM root — contacts, sites, jobs, quotes, tenders |
| **maintenance_checks** | *(not listed)* → **7** | Service work orders — **new to the spine** |
| **quote** | *(app-local in June)* → **6** | **Promoted:** was classed app-local, now a hub |
| **apprentice_profiles** | *(app-local in June)* → **6** | **Promoted:** same |
| **contacts** | 3 → **3** | CRM — now the smallest of the original six |
| **licences** | →staff | The compliance gate ("who can work where") |

`quote` and `apprentice_profiles` were both filed under "app-local" in June and
are now referenced as widely as the original spine members. Whether they should
be *treated* as spine (i.e. must mean the same thing in every tenant) is a
design call, not a measurement — flagged here rather than decided.

## Referential integrity is enforced; ON DELETE is now mostly settled

`app_data` carries **137 FK constraints**, including every spine edge
(`contacts`/`sites` → `customers`, `assets` → `sites`, `licences` → `staff`).
Referential integrity for the spine is enforced by the database.

> A June draft of this doc claimed "zero enforced FKs". That was wrong — a buggy
> catalog query cast a table OID to `regnamespace` and matched nothing. Left
> recorded because it is the same failure shape as F14: a confident number that
> nobody re-derived.

**The June recommendation has been implemented.** That section asked for
`licences.staff_id` to become `RESTRICT` so deleting a staff row could never
silently wipe a sparkie's licence history. Verified live 2026-08-15:
`confdeltype = 'r'` — it is `RESTRICT` today. 48 of the 137 FKs remain
`ON DELETE CASCADE`; the `contacts`/`customers` cascade review named in June is
still open.

## The structural spine columns

- **`tenant_id`** — 121 of 128 tables. The seven without it: `_eq_migrations`
  (a migration ledger, correctly tenant-less) and six single-tenant tables
  (`gm_report_jobs`, `sks_comms_jobs`, `sks_comms_events`, `sks_comms_po_lines`,
  `sks_comms_labour_rates`, `sks_comms_materials`). **All seven have RLS enabled
  with policies** — verified 2026-08-15, this is a design choice, not an open
  exposure. The `sks_comms_*` set is named for one tenant by construction.
- **`intake_id`** — 46 tables. **This is the one that decayed.** June's claim
  was "carried by nearly every canonical table — the real backbone", true at
  46 of 55 (84%). The count has not moved while the schema more than doubled, so
  it is now 46 of 128 (**36%**). The "no silent drops" provenance guarantee —
  every row knows which intake event created it — **no longer holds for most of
  the schema.** Nothing broke; the guarantee simply stopped being extended to
  new tables, and no check noticed.
- **`external_id`** — 21 tables. Crosswalk to source systems (SimPRO etc).

## App-local tables

NOT spine. Shipped to **every** tenant in the same uniform schema; a tenant
simply doesn't use the clusters that don't apply to it. Per-tenant variation is
the rare exception via extension columns, not divergence of the standard.

Clusters: Quotes · Tenders · Service · Field/HR · Safety · Infra/reports. The
June file listed all ~49 by name; that list is not reproduced here because it
went stale within weeks and the count has since grown to ~119. Query the live
schema instead — that is the lesson this file exists to carry.

## Open coherence work

1. **Decide whether `quote` / `apprentice_profiles` / `maintenance_checks` are
   spine.** They meet the reference-count bar; nobody has ruled on it.
2. **`intake_id` coverage.** Either extend the provenance guarantee to the other
   82 tables or narrow the claim to the subset it actually covers. Today the doc
   and the schema disagree, which is worse than either answer.
3. **Review the `contacts`/`customers` cascade** — still open from June.

The drift-CI guard then keeps the agreed semantics uniform across tenants.
