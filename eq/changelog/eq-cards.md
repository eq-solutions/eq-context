# EQ Cards — Changelog

## 2026-07-01
- fix(auth): `handle_phone_dedup` SECURITY DEFINER — all new signups were 500ing (migration 0066, applied live)
- fix(auth): "No internet connection" → "Unable to connect…" + Sentry capture for NetworkFailure
- fix(photos): bottom sheet camera/gallery choice on web — Android users no longer dropped straight to library
- fix(workers): `eq_cards_upsert_my_worker` adopts orphan shells before inserting — prevents duplicate worker rows (migration 0067, applied live)
- chore(workers): migration 0068 — swept 4 at-risk orphans: John Angangan orphan deleted, Cicero/Zemi/Marcus proactively linked
- deploy: run 28489589899 — all 2026-07-01 fixes live
- feat(onboarding): first-scan screen shown once on empty wallet (commit 37f8eb3, deploy pending)
- feat(onboarding): rich empty state — updated headline + employer context copy for connected workers
