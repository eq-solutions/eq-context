---
title: EQ Field — Changelog
owner: Royce Milmlow
last_updated: 2026-07-04
scope: Per-product change history — EQ Field
read_priority: reference
status: live
---

## 2026-07-04
- **PR #386 (MERGED, deployed live)**: Roster cell popover (pill remove, Clear button, site search/select) was fully dead — built on `innerHTML` + inline `onclick=""` string construction, which silently no-ops on this page. Rewritten with `document.createElement`/`appendChild`/`addEventListener` throughout. Found during a pre-pass bug sweep ahead of Royce's planned week of personally stress-testing Roster/Timesheets/Leave.

## 2026-07-02
- Fixed Schedule page 404 for SKS tenant — canonical roster reads (`roster-adapter.js` `rewriteReadPath`) hit nonexistent `app_data.schedule` instead of `app_data.schedule_entries`; writes were already correct. `2c374cb`.
