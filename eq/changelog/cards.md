---
title: EQ Cards — Changelog
owner: Royce Milmlow
last_updated: 2026-06-30
scope: Append-only history of changes to EQ Cards through 2026-06-30. Superseded by eq-cards.md going forward — see banner below.
read_priority: reference
status: live
---

> **Superseded 2026-07-19.** This file's last entry is 2026-06-30; `eq-cards.md`
> has been the actively-maintained EQ Cards changelog since, and is current.
> Kept here for history — don't append to this file, use `eq-cards.md`.

# EQ Cards — Changelog

## 2026-06-30
- `licence_edit_screen.dart` — fixed Sentry EQ-CARDS-W: `_PhotoSlot` converted StatelessWidget → StatefulWidget with cached `MemoryImage` to prevent CanvasKit blob URL revocation on Chrome Mobile (AU)
- `web/index.html` — `window.flutterConfiguration = { renderer: 'auto' }` (commit `c159717`): restores HTML renderer on mobile (iOS Safari, Android); Flutter 3.22+ CanvasKit default freezes WebGL animation on iOS Safari
- `eq_button.dart` + `not_provisioned_screen.dart` — `CircularProgressIndicator.adaptive()`: shows `CupertinoActivityIndicator` (CoreAnimation-backed) on native iOS; always animates
- `worker_self_repository.dart` — dead `FoundInvite` class + `findInvitesByPhone()` removed (commit `e2c77f7`); zero usages after "Find my company account" UI button was retired
