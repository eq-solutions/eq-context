---
title: Rules — Non-Negotiables
owner: Royce Milmlow
last_updated: 2026-04-26
scope: Hard rules that override all context, requests, or convenience
read_priority: critical
status: live
---

# Rules — Non-Negotiables

These rules are never overridden by context, user request, or convenience.
If something seems to require breaking one of these, stop and flag it.

---

## Session Discipline

0. **Finish what you start.** At session start, identify every recommendation, suggestion, and pending action surfaced in the conversation. Aim is to complete every one of them before session close. Half-applied work is the failure mode this rule prevents.
   - If a recommendation genuinely cannot be completed in-session (blocked by external action, requires explicit approval, depends on someone else), add a dated entry to `state/pending.md` before close — never leave it hanging in chat.
   - Never propose a fix and walk away. Either do it or defer it on the record.
   - "Half-applied cleanup patches" sitting unapplied on disk are a violation of this rule.

---

## Code & Deployment

1. Never deploy or push to any branch without explicit instruction from Royce
2. Never expose the Anthropic API key in any frontend file — worker.js proxy only, always
3. Never cross-deploy between EQ and SKS codebases — ever
4. **Never touch SKS live Supabase (`nspbmirochztcjijmcrx`) unless Royce explicitly says "SKS live"**. Three Supabase projects exist (sks-labour, eq-solves-field, eq-solves-service-dev) — always confirm which before connecting.
5. Never remove DEMO_FLAG comments — they mark live re-enable points
6. Never delete files without explicit permission
7. Never hardcode credentials, API keys, or secrets anywhere
8. Never run INSERT, UPDATE, DELETE, or Supabase schema changes without explicit approval
9. Auth changes require full chat review before any deployment
10. Every Netlify/Cloudflare Pages site must ship with a `_headers` security file

---

## Legal & Entity

11. Never reference GKE Lawyers or Gilbert + Tobin in any EQ document or correspondence
12. Never include 173 Chuter Ave, Sans Souci NSW 2219 in marketing or public-facing materials
13. Always flag complex compliance matters for Webb Financial or legal advisors — never act unilaterally
14. Hexican Holdings Trust is a CGT investor across all crypto — NOT trading stock. Capital losses in HHT are quarantined within the trust — cannot flow to personal or CDC

---

## Brand

15. Never recolour the EQ logo mark — Sky #3DA8D8 always
16. Never use gradients or drop shadows (EQ Design Brief v1.3)
17. Two logo variants only — Blue and White (v1.3 supersedes the old three-variant rule)
18. Never use legacy email addresses (rwm185@pm.me or roycemilmlow@gmail.com) in new documents
19. Never use real client names in any output — use generic placeholders ("Data Centre Client A", "Tier 1 Client", etc.)

---

## Financial

20. CDC Solutions passes the Results Test on the Delta Elcom engagement — no further PSI tests required
21. HHT crypto holdings are CGT investor method universally — personal, HHT, and SMSF
22. MIS risk: pooled employee contributions managed by others triggers managed investment scheme concern — AHD uses company retained earnings on company operations, not pooled contributions
