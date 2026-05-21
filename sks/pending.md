---
title: SKS Tier — Pending Actions
owner: Royce Milmlow
last_updated: 2026-05-21
scope: SKS Technologies to-do list; overwrite in place
read_priority: critical
status: live
---

# SKS Tier — Pending

SKS Technologies work only. EQ items in `eq/pending.md`. OPS items
(entities, tax, infra, substrate) in `ops/pending.md`.

---

## SKS Operations — Infrastructure (HIGH RISK)

- [ ] SKS Labour Supabase backup strategy — automated JSON-per-table dumps now landing in Cloudflare R2 `sks-assets/backups/YYYY-MM-DD/` (verified 2026-05-07: people, schedule, timesheets, leave_requests, managers, sites, organisations, audit_log, job_numbers + `_manifest.json`). Outstanding: (a) document the backup script location and schedule in `system/infrastructure.md`, (b) test restore path end-to-end, (c) decide retention policy
- [ ] Audit + download R2 backup `sks-assets/backups/2026-05-07/` from Beelink (12 May+) — no bulk-download in R2 dashboard; use wrangler / rclone / S3 SDK. Confirms backup integrity and gives an offline copy
- [ ] Resend email deliverability issue — unresolved
- [ ] Netlify rollback tagged release for SKS Labour

---

## SKS Commercial — Live

- [ ] DigiCo busway/busduct dispute — consolidate defensive position (VAR-003 15 Dec + Feb parts list)
- [ ] NEXTDC S3 tender — pricing workbook / submission
- [ ] AirTrunk SYD3 transformer commissioning — documentation pack
- [ ] Equinix SY6 CUFT — programme structure finalisation
- [ ] AWS SYD053 — ongoing WHIP install programme (3,220+)

---

## SKS Receipt Tracker

- [ ] Deploy Cloudflare Worker (anthropic-proxy) — follow DEPLOY.md
- [ ] Battle-test: receipt scanning, Excel export, data persistence
- [ ] Broader SKS staff testing

---

## SKS Brand — Lockdown Deployment Follow-ups (2026-05-21)

- [ ] Verify SKS ABN canonical source (resolved 2026-05-21 → 51 168 906 956; confirm against ASIC / ABN Lookup and reconcile the two other ABNs that appeared in past sources — `80 006 455 699` previously in `sks/templates.md`, `24 004 554 929` in the PDF Style Guide v1.0 footer)
- [ ] Verify NSW office address canonical source (resolved 2026-05-21 → 27/10 Gladstone Rd, Castle Hill NSW 2154; the SKS PDF Style Guide listed Unit 18, 7-9 Percy Street, Auburn NSW 2144 — confirm Auburn isn't a current second site before deleting it from any internal reference)
- [ ] Monitor first 5 SKS outputs after brand kit deployment — check `rules/brand-check.md` is actually being run (single-line "Brand check: ✓ ..." should appear before each customer-facing output)
