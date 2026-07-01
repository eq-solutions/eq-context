# EQ Intake — Changelog

## 2026-07-02
- Fixed health-score dashboard bug: entities with zero rows (e.g. Assets before first record) were scoring 100% complete, inflating the composite score. Added `started` flag; empty entities excluded from dimension averages and shown as "No records yet" instead of a false 100%. PR #53.
