# EQ Cards — Changelog

## 2026-07-01
- fix(auth): `handle_phone_dedup` SECURITY DEFINER — all new signups were 500ing (migration 0066, applied live)
- fix(auth): "No internet connection" → "Unable to connect…" + Sentry capture for NetworkFailure
- fix(photos): bottom sheet camera/gallery choice on web — Android users no longer dropped straight to library
- fix(workers): `eq_cards_upsert_my_worker` adopts orphan shells before inserting — prevents duplicate worker rows (migration 0067, applied live)
