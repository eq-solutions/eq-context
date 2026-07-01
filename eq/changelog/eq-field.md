## 2026-07-02
- Fixed Schedule page 404 for SKS tenant — canonical roster reads (`roster-adapter.js` `rewriteReadPath`) hit nonexistent `app_data.schedule` instead of `app_data.schedule_entries`; writes were already correct. `2c374cb`.
