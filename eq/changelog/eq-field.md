---
title: EQ Field — Changelog
owner: Royce Milmlow
last_updated: 2026-08-16
scope: EQ Field append-only history.
read_priority: reference
status: live
---

# eq-field changelog

## 2026-08-16 (PR #703 MERGED + deployed live — anon-key fallback stopped masking auth failures)
- `scripts/supabase.js` fell back past an anon-key auth failure instead of erroring loud — same silent-fallback shape as the eq-shell/eq-service/eq-cards fixes shipped the same day, found during the 2026-08-16 secrets audit's silent-failure sweep.
- CI's `drift` (cache-buster) check caught a real gap before merge: an earlier fix to `app-state.js`'s internal `APP_VERSION` constant had never bumped that file's own `?v=` tag in `index.html`, independent of the `supabase.js` tag that had already been bumped. Fixed with a follow-up commit (`v3.5.502` → `v3.5.503`) before merging.
- eq-field [PR #703](https://github.com/eq-solutions/eq-field/pull/703), merged, live (Netlify auto-deploy on merge to `main`).
