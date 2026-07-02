# EQ Intake — Changelog

## 2026-07-03
- Licence strip fail-open fixed (PR #56): "All N licences current" was rendering over expired licences because severity counters only incremented after a successful `eq_quality_upsert_alert` call, and that RPC was never executable by `authenticated` on ehow (053 shipped no GRANT — zero alerts ever written). Counters now come from the licence data itself; new `alerts_failed` field; sql/058 adds caller-tenant guard + grant (merged, NOT yet applied to ehow).
- quality-guardian fixed end-to-end (PR #57): service-role tenant-context RPCs (sql/059), nightly cron registration via Vault (sql/060), Edge Function rewritten — explicit-tenant reads, fixed tenant listing + run bookkeeping, exact service-role-key auth check. Merged, NOT yet applied/deployed to ehow — production go pending.

## 2026-07-02
- Fixed health-score dashboard bug: entities with zero rows (e.g. Assets before first record) were scoring 100% complete, inflating the composite score. Added `started` flag; empty entities excluded from dimension averages and shown as "No records yet" instead of a false 100%. PR #53.
