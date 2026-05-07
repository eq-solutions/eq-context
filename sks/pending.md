---
title: SKS Tier — Pending Actions
owner: Royce Milmlow
last_updated: 2026-05-08
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
