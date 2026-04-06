# EQ Field Ops — Changelog

## [2026-04-05] Demo Mode, Seed Data and Network Error Suppression
**Session:** https://claude.ai/chat/7a125714-3384-4c92-9a09-247cc39a624e
**Built by:** Royce Milmlow + Claude (Anthropic)
**Changes:**
- Demo mode implemented - bypasses Supabase auth when tenant slug is eq
- 18 generic staff, 7 generic sites, 5 weeks of schedule seeded
- Network error toasts suppressed in demo mode
- Cowork guardrail issue documented
**Status:** Live on eq-solves-field.netlify.app (demo branch)

## [2026-04-05] Cloudflare Pages Deployment Architecture Locked
**Session:** https://claude.ai/chat/7a125714-3384-4c92-9a09-247cc39a624e
**Built by:** Royce Milmlow + Claude (Anthropic)
**Changes:**
- Deployment architecture confirmed and locked
- Rule: never cross-deploy between targets
**Status:** Architecture documented

## [2026-04-04] Redundancy and Failover Gap Assessment
**Session:** https://claude.ai/chat/0dae99a5-bf18-4906-8dda-12c80a97ba67
**Built by:** Royce Milmlow + Claude (Anthropic)
**Changes:**
- Full infrastructure assessment across Netlify, Supabase, Resend, GitHub
- Gaps identified: Supabase single point of failure, no backups, no tagged release
**Status:** Gaps identified - NOT yet resolved

## [2026-03-31] White-Label Commercialisation Review
**Built by:** Royce Milmlow + Claude (Anthropic)
**Changes:**
- EQ Field Ops commercialisation roadmap built (85-item Excel workbook)
- White-label conversion estimated at 2-3 hours
**Status:** Planning complete - not yet executed

## [2026-03-01] SKS Labour Forecast Live
**Built by:** Royce Milmlow + Claude (Anthropic)
**Changes:**
- Single-file HTML/JS app with Supabase backend
- Supports 50+ field staff scheduling
- Positive day-one reception from field staff
**Status:** Live at sks-nsw-labour.netlify.app
