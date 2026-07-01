# EQ Cards — Changelog

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
