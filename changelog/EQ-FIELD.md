---
title: Changelog — EQ Solves Field
owner: Royce Milmlow
last_updated: 2026-04-10
scope: Append-only history of changes to the EQ Solves Field product
read_priority: reference
status: live
---

# Changelog — EQ Solves Field

## [2026-04-05] Demo Mode, Seed Data and Network Error Suppression
**Built by:** Royce Milmlow + assistant
**Changes:**
- Demo mode implemented - bypasses Supabase auth when tenant slug is eq
- 18 generic staff, 7 generic sites, 5 weeks of schedule seeded
- Network error toasts suppressed in demo mode
- Cowork guardrail issue documented
**Status:** Live on eq-solves-field.netlify.app (demo branch)

## [2026-04-05] Cloudflare Pages Deployment Architecture Locked
**Built by:** Royce Milmlow + assistant
**Changes:**
- Deployment architecture confirmed and locked
- Rule: never cross-deploy between targets
**Status:** Architecture documented

## [2026-04-04] Redundancy and Failover Gap Assessment
**Built by:** Royce Milmlow + assistant
**Changes:**
- Full infrastructure assessment across Netlify, Supabase, Resend, GitHub
- Gaps identified: Supabase single point of failure, no backups, no tagged release
**Status:** Gaps identified - NOT yet resolved

## [2026-03-31] White-Label Commercialisation Review
**Built by:** Royce Milmlow + assistant
**Changes:**
- EQ Field Ops commercialisation roadmap built (85-item Excel workbook)
- White-label conversion estimated at 2-3 hours
**Status:** Planning complete - not yet executed

## [2026-03-01] SKS Labour Forecast Live
**Built by:** Royce Milmlow + assistant
**Changes:**
- Single-file HTML/JS app with Supabase backend
- Supports 50+ field staff scheduling
- Positive day-one reception from field staff
**Status:** Live at sks-nsw-labour.netlify.app
