---
title: WS1 customer convergence — partial APPLIED (Tier S + safe quotes backfill)
date: 2026-06-07
project: ehowgjardagevnrluult (sks-canonical) · schemas app_data + public
status: archived
scope: EQ-managed canonical plane (NOT nspb/SKS-live). Non-destructive (soft `active=false` + nullable backfill). No deploy, no app code.
approval: Royce "you have my approval, steelman first then go for it" (2026-06-07)
owner: Royce Milmlow
last_updated: 2026-06-07
read_priority: reference
---

# WS1 customer convergence — what was applied (2026-06-07)

Steelmanned the keystone, then executed only the **provably-safe** subset; **held** everything ambiguous.

## Confidence tiering (read-only, 117 dup-name groups)
| Tier | Groups | Action | Status |
|---|---|---|---|
| **S** — unreferenced stub dups (a sibling holds all the refs) | 41 (38 with a referenced survivor) | retire stubs (`active=false`) | **✅ APPLIED — 38 retired** |
| **A** — multi-referenced + shared email/phone (provably same) | 26 | FK-repoint merge to a survivor | **HELD** (complex, needs supervised run) |
| **C** — multi-referenced, no shared contact (ambiguous) | 50 | Intake multi-signal dedupe / human review | **HELD** (do not auto-merge) |

## Applied #1 — Tier S stub retirement (`app_data.customers`)
Non-destructive: `active=false`. Predicate = dup-name member with **0** references (sites+contacts+contact_customer_links)
**and** a referenced sibling exists (guarantees a live survivor; 8 all-stub-group rows correctly skipped).
- **38 rows retired.** Result: active dup-name groups **117 → 80**; **0 groups emptied** (verified).
- Many were cross-source import dups (one UUID `external_id` from intake + a numeric quotes-side twin, e.g.
  "Health Infrastructure" `48`, "Schneider Electric" `228`).

**Rollback (exact — these 38 are the only currently-inactive customers; re-activates them):**
```sql
update app_data.customers set active=true, updated_at=now()
where active=false and customer_id in (
 'd638a851-6b94-4e19-9698-72e362d30455','940064d7-fc56-4d50-9a91-d2e68b38a37e','c190631b-a71b-4cd3-b9fa-94d4161deb15',
 '9ef43d3e-7030-48b5-8b10-916554affb8b','c59286f3-1754-43db-9b9f-73899706958c','9ed34bf2-d1e7-49a4-a46b-f125c5d83f12',
 'ad4e0156-82fe-4e4d-8297-493399f6c1c5','204d5187-b0a6-4edb-81cd-470cf5d376f8','8999cfee-cc08-4b87-bb93-62c453ff3cd7',
 'b72de47e-3b55-490a-a337-2ce6ed4470b4','f6639a62-959a-4a34-aa7e-4534addb98ca','1344fb97-c782-4078-be1d-c1508915e32b',
 'ee9d9fa5-07c5-4f7f-a6b4-deafcdf7ebe9','2a2650ce-be15-41a9-883a-2d5b9e214d69','36572216-7016-4eeb-ab91-2ff11c18b5e7',
 'bfa19b80-0a1b-436f-a08c-a99340fd700f','b22f759b-1620-442f-ac6e-0005bbd69047','5587bf57-c0cb-4e9f-bf85-a6835d63c998',
 'a6942258-5ef7-4bcb-9d93-23422d4d56ec','017031df-0983-475f-95fb-be71a5432c75','75926304-b002-4a32-b94d-237b9abe466c',
 'd44bbea4-e0fd-4ef0-a4a8-27afe52f485d','10edab39-c253-4fba-98a6-40128a74cf24','3d21ab0b-7980-4bef-a613-ea8331ae721c',
 '81ff4338-3f65-4718-be79-3a1c2077686c','adf4ff51-d0a5-4621-ba72-fca969c65515','31171539-e18d-40a2-9bbc-a815e12ea174',
 '178764c5-7890-4ed0-ae41-792aba1531b1','0852d4a9-566f-4004-8a6d-55267a87d298','3b3340f7-4044-474f-ab32-34d0f22bff03',
 'c9bb8456-0cc9-4586-a524-81bca5081a49','92a043b8-3607-4d11-8117-d9b00a5feb90','30740cfa-d63a-4b04-8d3c-1c0b3640081e',
 'bd8258ca-8f58-4319-b248-2d2a96555da7','db353561-6209-4781-b69b-58f9e43df6f0','22634ba8-56b2-4ad7-832f-61bbef716005',
 'de78aca2-29d1-47c6-ac78-a9068b31210a','12cfa167-3c80-4f32-a4cd-5c74771f8c44');
```

## Applied #2 — safe quotes→canonical backfill (`public.sks_quotes_customers.canonical_id`)
Only the **1:1 on both sides** matches (one quote-customer name → one active canonical, no collision). **28 rows** linked
(`canonical_id` 0 → 28).
**Rollback (re-derivable — these 28 are the only non-null `canonical_id`s):**
```sql
update public.sks_quotes_customers set canonical_id = null where canonical_id is not null;
```

## Structural finding (important)
`sks_quotes_customers.canonical_id` carries a **UNIQUE constraint** (`sks_quotes_customers_canonical_id_unique`) →
enforces **1:1** quote-customer ↔ canonical. But the quotes side is **N:1** (multiple quote-customer rows per company).
So the full quotes→canonical link is a **both-sides dedup**, not a one-way backfill — the quotes side must be deduped
(pick one primary per company) before the remaining ~65 can link. Intake/app territory.

## Held (NOT done — gated/complex)
- **Tier A** (26 groups): FK-repoint merge — provably same but multi-table; run supervised.
- **Tier C** (50 groups): ambiguous name-only — Intake multi-signal dedupe or human review.
- **Quotes-side dedup** (N:1) — to unlock the remaining ~65 canonical links.
- **99 dangling sites** — `external_customer_id` in neither table → need a source re-import, not dedup.
