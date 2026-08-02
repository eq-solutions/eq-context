---
title: EQ Field — Active State (Rolling)
owner: Royce Milmlow
last_updated: 2026-07-21
scope: Current live state of EQ Field product
read_priority: critical
status: live
---

# EQ Field — Active State

**Current version:** v3.5.334 · **Deployed:** `field.eq.solutions` + `core.eq.solutions/sks/field`
**Repo:** `eq-solutions/eq-field` (main branch, auto-deploy via Netlify)

> **Corrected 2026-07-20/21** (this file was stale since 2026-07-19, version pinned at v3.5.211 — 123 versions behind): tenant table below fixed against live data — `demo-trades`/`melbourne` were deleted from canonical 2026-06-28 and no longer resolve (only `?tenant=demo` — an in-memory URL-override slug, no DB — reaches anything demo-shaped now); `eq`'s data plane migrated off `ktmj` (deleted 2026-07-04, no longer a Supabase project) onto `zaapmfdkgedqupfjtchl`. Rest of this file not re-verified line-by-line this pass — treat anything not touched below as unconfirmed until re-checked.

---

## Live tenants

| Tenant | URL | Data plane | State |
|---|---|---|---|
| `eq` | `field.eq.solutions` | `zaapmfdkgedqupfjtchl` (zaap / eq-canonical-internal) — demo/disposable, NOT a customer | Live (sandbox data) |
| `sks` | `core.eq.solutions/sks/field` (Shell iframe) | `ehowgjardagevnrluult` (ehow) — SKS LIVE | Live (SKS canonical) — the only live customer data in this product |

**Retired 2026-06-28:** `demo-trades` / `melbourne` DB-backed demo tenants — deleted from canonical, no longer resolve. The only remaining demo surface is `?tenant=demo` (hardcoded in-memory gate codes, no DB calls, URL-override only).

**Shell embed:** `core.eq.solutions/sks/field` → iframes `field.sks.eq.solutions`

---

## SKS canonical state (ehow — as of 2026-06-13)

**JWT data path active** (`DATA_JWT_ENABLED=on`). All 11 `app_data.field_*` views present.
RLS WITH CHECK hardened on all 14 write policies. Adapter view architecture:
- `field_people` / `field_managers` → `app_data.staff` (read-only, Service owns)
- `field_sites` → `app_data.sites` (read-only, Service owns)
- `field_schedule` / `field_timesheets` / etc. → `public.*` (writable pass-throughs)

**Canonical sync — workers LIVE, licences retired (updated 2026-08-03):** `workers-canonical-sync` (v3) is live via a real trigger on jvkn `public.workers`. `credentials-canonical-sync` (v1) is dead — no trigger ever wired it, and its hardcoded tenant const was wrong (used the EQ id, not SKS's `7dee117c`). Superseded by eq-shell's own pull-based sync (`cards-approve-staff.ts` at approval time + `staff-resync-licences.ts` on demand), which is what actually keeps ehow `app_data.licences` current. The orphaned edge function itself still needs manual deletion via the Supabase dashboard (no MCP/migration path to remove it) — flagged 2026-07-26, still open. 39 staff + 171 licences reflects the 2026-06-13 snapshot, not an ongoing feed from this function.

**v3.5.147 identity stub (2026-06-15):** `_tryLinkPersonToWorker()` in `people.js` — on person save with email, looks up jvkn.workers by email; if found, patches `people.worker_id`; if not found, creates a minimal stub (name, email, phone, role). Transition scaffolding — removes when Cards onboarding is the sole creator of jvkn.workers rows. `syncAllToCanonical()` bulk action available to supervisor role.

**Data counts (2026-06-13, at time of the sync above — historical, see below for current):** 39 staff · 591 sites · 171 licences · 0 roster rows (data entry needed)

**Data counts (live-verified 2026-07-19, direct query against ehow):** 88 active staff total — 58 Direct (39 on-roster non-supervisor + 18 supervisor + 1 off-roster non-supervisor) + 19 Labour Hire + 10 Apprentice + 1 Subcontractor · 250 sites · 100 licences. Resolves the 58-vs-39 discrepancy Royce flagged in the 2026-07-19 substrate audit (EQ-03) — both figures were correct, just counting different subsets (all-Direct vs on-roster-non-supervisor-Direct) with no label saying so. Site count (591→250) and licence count (171→100) also dropped substantially since 06-13 — not investigated further, likely the site-merge/dedup work from the same week, worth a look if it looks wrong.

**Apprentice module (2026-06-18):** 11 tables created (apprentice_profiles, journal, skills_ratings, competencies, feedback_entries, feedback_requests, rotations, buddy_checkins, quarterly_reviews, engagement_log, checkins). 11 standard electrical competencies seeded. All module_entitlements flipped to enabled in jvkn. person_id/supervisor_id/buddy_id are bigint (adapted from EQ uuid pattern). Nav unlocked.

**Acknowledgments (2026-06-18):** `acknowledgments` table live on ehow. One-tap peer recognition working at core.eq.solutions/sks/field → Contacts → profile eye icon.

---

## Modules live

| Module | Tenants | Notes |
|---|---|---|
| Dashboard | All | |
| Roster / Schedule | All | |
| People | All | |
| Sites | All | |
| Leave | All | |
| Timesheets | All | |
| Managers | All | |
| Safety (prestarts / toolbox) | sks | Tenant-gated |
| Teams | sks | Tenant-gated |
| Pipeline (Tender Pipeline) | sks | Tenant-gated |
| Resources (Resource Allocation) | sks | Tenant-gated |
| Site Reports / Diary | All | |
| Projects / Forecast | Enterprise | Melbourne demo |
| Apprentices | All | SKS enabled v3.5.162 — 11 tables + competencies seeded |
| Acknowledgments (peer recognition) | All | v3.5.159 — one-tap, peer-to-peer |
| Site Audits | All | v3.5.112 |

---

## Auth model

PIN gate → `verify-pin.js` (Netlify Function) → HMAC session token (7-day).
`DATA_JWT_ENABLED=on` → per-tenant Supabase JWT minted on sign-in, used for all data queries.
Shell embed uses cookie SSO (`verify-shell-cookie`).

---

## Gated (Royce-gated, not yet active)

1. **Roster data entry on ehow** — schedule/timesheets/leave are empty; start fresh or migrate from nspb standalone
2. **Standalone `sks-nsw-labour` retirement** — after soak confirmation. Confirmed live 2026-07-05: this is a *separate repo/codebase* (`eq-solutions/sks-nsw-labour`, pre-2026-05-20 split) with its own independent PIN login, still actively used in production today — NOT the same as eq-field's standalone PIN gate (that one IS already retired in practice for SKS, see IDENTITY-MODEL.md §7.1). Royce confirmed sks-nsw-labour still uses its own PIN.
3. **Track 2 RLS STEP 2** — anon SELECT lockdown; after standalone retired
4. **Collin Toohey fresh invite** — jvkn duplicate `3d18422d` deleted (2026-06-13); original `7514e57d` retained; needs a new Cards/Shell invite sent
