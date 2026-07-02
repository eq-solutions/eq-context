# EQ Cards — Changelog

## 2026-07-02
- feat(identity): Track B worker-identity resolver unification — migrations 0070–0073 applied to jvkn control plane + PR #113 merged. 0070 `link_pending_invites` claims a worker stub by email only on an exactly-one match (was unbounded → double-claim); 0071 `handle_phone_dedup` 90-day recycled-phone guard + `shell_control.identity_recycle_review` queue + admin RPCs; 0072 routes `eq_cards_claim_invite` + `eq_cards_submit_access_request` through the single resolver; 0073 adds `eq_cards_find_or_create_worker_for_invite` (no-user invite resolver). Replay-tested against 74 live workers (0 new dups); applied via MCP (CLI linked to a deleted project). Consumed by eq-shell #597/#598.
- fix(licences): crop screen no longer reallocates a blob URL on every drag-gesture rebuild — `Image.memory()` inline in `build()` swapped for a single `MemoryImage` held in State (same pattern as `_PhotoSlot` in `licence_edit_screen.dart`). Fixes recurring "Could not load Blob from its URL" (Sentry EQ-CARDS-W). Commit `caf91d1`, deployed via manual `deploy.yml` dispatch (run 28579115186)
- fix(ci): web image-compress moved behind a conditional import (`photo_compress_web.dart` + `_io` stub via `if (dart.library.html)`); `photo_upload.dart` no longer pulls `dart:js_interop`/`package:web` into the VM test graph. Fixes "Analyze and test" red since #110. Verified Flutter 3.41.9: analyze clean, 207 tests pass. PR #114 merged, CI green
- fix(notify): connection-request email CTA now "Review the request" → `core.eq.solutions/<slug>/staff` (was "Review in EQ Shell" → homepage); migration `0069` adds `org_slug` to `eq_notify_connection_request_targets`; edge fn v4. Live + verified (test send `sent:1`). PR #112
- fix(profile): `eq_cards_upsert_my_worker` gained 3 no-default params in `0067`, breaking its 12-arg callers → Profile tab "function does not exist" 500. Migration `0071` defaults the trailing params. Live + verified (impersonated upsert, rolled back). Also unblocks credential-save + invite-link. PR #112
- fix(ocr): web compression no longer blocks the main thread — `canvas.toDataURL()` swapped for `canvas.toBlob()` in a new web-only `_compressForWeb`, fixing the frozen OCR spinner on iOS Safari/PWA; native iOS/Android untouched (commit `d9d87a3`, PR #110, run 28540590608)
- fix(ocr): "Fill manually" escape hatch when OCR can't read a photo (e.g. back of card) — was a dead end with only a snackbar
- fix(onboarding): first-scan "welcome" screen now picks the photo synchronously in the tap handler instead of after a Navigator round-trip — browsers were silently refusing to open the camera on the first attempt (commit `617b8de`, PR #111, run 28541424467)
- fix(ocr): OCR loading dialog's "taking longer than usual" message no longer fires at 5s when the same dialog says scans normally take 5–10s — threshold raised to 9s, copy softened
- chore(data): deleted demo/trial account `0466118646` — standalone empty signup, no org/licence data
- fix(notify): connection-request email worker name now sourced from `workers` (was `profiles.full_name`, which self-signup workers never populate) — was rendering as "A worker". Falls back to formatted AU mobile, then "A new worker". Migration `0074`, applied live + verified. PR #115
- fix(licences): `share-licence` edge fn `holder_name` had the same wrong-table bug — sourced from `workers` first, `profiles` fallback. Deployed v8, verified live via curl. PR #115
- chore(data): `0075` backfilled `profiles.full_name` from `workers` for 6 NULL rows (0 conflicts). Applied live
- fix(connections): `P0023` name-gate error (`eq_cards_submit_access_request`) now shows a clean "Add your name…" message instead of `ServerFailure(500): ...`. PR #115, deployed run `28585818154`

## 2026-07-01
- fix(auth): `handle_phone_dedup` SECURITY DEFINER — all new signups were 500ing (migration 0066, applied live)
- fix(auth): "No internet connection" → "Unable to connect…" + Sentry capture for NetworkFailure
- fix(photos): bottom sheet camera/gallery choice on web — Android users no longer dropped straight to library
- fix(workers): `eq_cards_upsert_my_worker` adopts orphan shells before inserting — prevents duplicate worker rows (migration 0067, applied live)
- chore(workers): migration 0068 — swept 4 at-risk orphans: John Angangan orphan deleted, Cicero/Zemi/Marcus proactively linked
- deploy: run 28489589899 — all 2026-07-01 fixes live
- feat(onboarding): first-scan screen shown once on empty wallet (commit 37f8eb3, run 28509766188)
- feat(onboarding): rich empty state — updated headline + employer context copy for connected workers
- feat(onboarding): explicit camera+gallery buttons in FirstScanScreen; worker card hidden on empty wallet; CTAs at top (commit 493d895, run 28511411215)
- feat(onboarding): first-licence success sheet + connection confirmation snackbar + PostHog signup_completed fix (commit 1a141a6, run 28512783582)
- fix(ui): CircularProgressIndicator.adaptive → plain in EqButton + NotProvisionedScreen; worker ID card moved to wallet bottom (commit 9f2b408, run 28513226954)
