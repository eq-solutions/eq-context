---
title: Changelog — SKS Labour
owner: Royce Milmlow
last_updated: 2026-04-28
scope: Append-only history of changes to the SKS Labour scheduling app
read_priority: reference
status: live
---

# Changelog — SKS Labour

## [2026-04-28] Add Contact button on Contacts page (cherry-picked from EQ Field demo)
**Built by:** Royce Milmlow + assistant
**Commit:** `4f03227` on `main` (cherry-pick of `f372a43`); originally PR #25 on Milmlow/eq-field-app
**Changes:** "＋ Add Contact" button added to the Contacts page filter row. Reuses existing modal-manager + saveManager flow; no new code paths, no migration, no permission change. One-line diff to `index.html`. Cherry-picked from EQ Field demo branch where it shipped via PR #24.
**Why:** UX parity — the page-contacts page (nav: Contacts) showed staff/people but had no Add affordance. Add button only existed on page-managers (Supervision).
**Status:** Live on sks-nsw-labour.netlify.app post-Netlify-deploy.

## [2026-04-11] Service Worker Caching and Favicon Set
**Built by:** Royce Milmlow + assistant
**Changes:**
- Service worker caching strategy fixed — network-first for JS/CSS/HTML, cache-first for icons
- Full SKS favicon set built (ico, apple-touch, 192, 512)
**Status:** Live

## [2026-04-04] Connector Guardrails and Redundancy Review
**Built by:** Royce Milmlow + assistant
**Changes:**
- Connector guardrails documented
- Redundancy gaps identified (no Supabase backups, single point of failure)
**Status:** Live at sks-nsw-labour.netlify.app

## [2026-03-01] SKS Labour Forecast Live
**Built by:** Royce Milmlow + assistant
**Changes:**
- Single-file HTML/JS app with Supabase backend
- Supports 50+ field staff scheduling
- Positive day-one reception from field staff
**Status:** Live at sks-nsw-labour.netlify.app (moved from EQ-FIELD.md changelog — this entry always belonged here)
