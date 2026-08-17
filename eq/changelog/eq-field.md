---
title: EQ Field — Changelog
owner: Royce Milmlow
last_updated: 2026-08-17
scope: EQ Field append-only history.
read_priority: reference
status: live
---

# eq-field changelog

## 2026-08-17 (PR #711 MERGED — v3.5.508, roster site-map scoped to field_enabled)
- Roster's site-map query (`scripts/supabase.js`) filtered sites on `active=eq.true` only, missing the `field_enabled` flag that actually gates whether a site should appear in Field — added `&field_enabled=eq.true`. Found during a live-recon pass at session start, not from a prior report. Confirmed additive-safe against live data (doesn't change the one existing duplicate-code collision count) before merging. Confirmed live via `field.eq.solutions/sw.js`.

## 2026-08-17 (PR #710 MERGED — v3.5.507, auth.js file-size debt: split into 5 files)
- `auth.js` (1,508 lines) split into `auth-gate-picker.js`, `auth-shell-handoff.js`, `auth-agency-gate.js`, `auth-staff-ts-gate.js`, and a slimmed `auth.js` (727 lines) — closes the last tracked file over the repo's ~1,500-line file-size convention from this list. `core-bundle-b3.js` MANIFEST widened to the 5 source files, regenerated via `build-bundles.mjs --write`. `eslint.config.js`'s `GRANDFATHERED_MAX_LINES` entry for `auth.js` removed outright, not lowered.

## 2026-08-16 (PR #709 MERGED — v3.5.506, mobile UI pass: schedule layout, login race, apprentice menu)
- Schedule/Roster/Editor/Dashboard week-nav row wrapped onto two lines on real phone widths (orphaned "next week" button) — `.week-nav-label` no longer carries a fixed `min-width:180px` on mobile. `styles/mobile.css`.
- Field login intermittently looked locked on first load, self-fixed by a refresh — auth boot was gated on `window.onload` (waits on every stylesheet/icon), letting Shell's 30s handoff-token window expire on a slow connection before `checkAccess()` ever ran. Swapped to `DOMContentLoaded`. `index.html`.
- Apprentices (and employees/labour hire) saw Timesheets + Records in the MORE menu despite both leading to supervisor/manager-only content — `applyMobileNavPerms()` never gated either item. Wired to existing `ts.view_team`/`reports.incident.view` keys.
- Prestarts opened to everyone (Royce's call) — `reports.prestart.view` added to employee/apprentice/labour_hire in `permission-matrix.js` + its hand-merged runtime copy `core-bundle-a1.js`; drawer button un-hidden.
- `APP_VERSION`/service-worker `CACHE`/changed files' `?v=` tags bumped, `CHANGES IN v3.5.506` banner added, `core-bundle-a1.js` regenerated via `build-bundles.mjs --write`. `permission-enforcement-baseline.json` ratchet tightened (`ts.view_team` no longer dead).
- Found while live-testing as an apprentice on the SKS tenant; full write-up in `sessions/2026-08-16.md`.

## 2026-08-16 (PR #703 MERGED + deployed live — anon-key fallback stopped masking auth failures)
- `scripts/supabase.js` fell back past an anon-key auth failure instead of erroring loud — same silent-fallback shape as the eq-shell/eq-service/eq-cards fixes shipped the same day, found during the 2026-08-16 secrets audit's silent-failure sweep.
- CI's `drift` (cache-buster) check caught a real gap before merge: an earlier fix to `app-state.js`'s internal `APP_VERSION` constant had never bumped that file's own `?v=` tag in `index.html`, independent of the `supabase.js` tag that had already been bumped. Fixed with a follow-up commit (`v3.5.502` → `v3.5.503`) before merging.
- eq-field [PR #703](https://github.com/eq-solutions/eq-field/pull/703), merged, live (Netlify auto-deploy on merge to `main`).

## 2026-08-16 (PR #705 MERGED — timesheets/leave_requests own-row RLS, read + write; NOT yet dispatched)
- Added RESTRICTIVE RLS policies for `app_data.timesheets`/`app_data.leave_requests` on ehow (SKS tenant), closing a P1 gap where `authenticated` had full tenant-wide SELECT/INSERT/UPDATE/DELETE with no per-person predicate — any signed-in SKS session (including labour_hire) could read or edit another worker's timesheet/leave content, undetected by the existing approval-status trigger (which only ever gated `status` transitions, never content edits).
- Write-side migration's first draft (already on the branch before this PR's final push) scoped supervisor writes to "own crew only" (mirroring the read-side model) — corrected before merge: verified against the real client code that `prefillTsFromRoster`/`importTsCSV` are tenant-wide bulk features gated only on `ts.approve`, with no crew check anywhere, so a crew-scoped write policy would have broken both for any non-manager supervisor. Fixed to own-row-or-approver (tenant-wide for approvers) for timesheets specifically; `leave_requests` kept crew-scoped (no equivalent bulk-write feature exists there).
- Both migrations are deliberately `NOT APPLIED` — dispatch via the One Pipe is separately blocked on a pre-existing, re-confirmed gap: 47 of 102 SKS staff have no `staff.user_id` link yet, so a naive own-row check would lock them out of their own rows the moment either migration ships. See `sks/pending.md`.
- eq-field [PR #705](https://github.com/eq-solutions/eq-field/pull/705), squash-merged. Pure migration-file + docs diff (no app code), so the resulting Netlify auto-deploy has no live behavioural effect.
