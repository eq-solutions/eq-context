---
title: Rules — Non-Negotiables
owner: Royce Milmlow
last_updated: 2026-05-04
scope: Hard rules that override all context, requests, or convenience
read_priority: critical
status: live
---

# Rules — Non-Negotiables

These rules are normative and override context, user request, or convenience.
If something seems to require breaking one of these, stop and flag it.

**Modal verbs in this file follow RFC 2119:**

- **MUST / MUST NOT** — absolute requirement / prohibition.
- **SHOULD / SHOULD NOT** — strong default; deviation requires a documented reason.
- **MAY** — permitted; no obligation.

If sharpening the language to fit these verbs would change a rule's meaning, that is a decision-grade change — surface it via the relevant tier's `pending.md` rather than editing this file inline.

---

## Session Discipline

0. **Finish what you start.** At session start, the assistant MUST identify every recommendation, suggestion, and pending action surfaced in the conversation. Every one of them MUST be either completed before session close or deferred to the relevant tier's `pending.md` with a date. Half-applied work is the failure mode this rule prevents.
   - If a recommendation genuinely cannot be completed in-session (blocked by external action, requires explicit approval, depends on someone else), the assistant MUST add a dated entry to the relevant `pending.md` before close and MUST NOT leave it hanging in chat.
   - The assistant MUST NOT propose a fix and walk away. The fix MUST either be applied in-session or deferred on the record.
   - "Half-applied cleanup patches" sitting unapplied on disk are a violation of this rule.

---

## Tier Discipline

**Tier-mixing is the failure mode the 2026-05-04 refactor was built to prevent.**

The repo is tier-separated: `/eq`, `/sks`, `/ops`, `/system`, `/archive`.
At session start the assistant MUST ask "EQ or SKS focus?" and load
defaults from one tier only. Cross-tier loads are explicit, not implicit.

- The assistant MUST NOT surface SKS content unprompted in an EQ session, or vice versa.
- The assistant MUST NOT load `/archive/` content unless the user explicitly references parked or deferred work.
- OPS content (`/ops/`) loads only when the task explicitly touches entities, finance, tax, or substrate-level concerns.

---

## Substrate

**GitHub is canonical for `eq-context`. Supabase is a runtime cache.** Direct chat-to-Supabase writes to the `context_files` table are emergency-only and MUST be reconciled to GitHub the same day. Bypassing GitHub destroys the audit trail that is the actual moat of this repo — once Supabase and the git log drift, every "what did we decide and why" question has two possibly-conflicting answers. The git log is the substrate's value; the Supabase row is just the assistant-readable cache.

**`updated_at` is the freshness signal of record.** A change to `context_files` is not "done" until the row's `updated_at` reflects it. Terminal output, commit hashes, and "looks good" visual confirmation do not count. The assistant MUST verify after every push (the workflow's verification job does this automatically; if it ever fires green but the row is stale, treat it as a substrate incident).

---

## Code & Deployment

1. The assistant MUST NOT deploy or push to any branch without explicit instruction from Royce.
2. The assistant MUST NOT expose the Anthropic API key in any frontend file — worker.js proxy only, always.
3. The assistant MUST NOT cross-deploy between EQ and SKS codebases — ever.
4. **The assistant MUST NOT touch SKS live Supabase (`nspbmirochztcjijmcrx`) unless Royce explicitly says "SKS live".** Three Supabase projects exist (sks-labour, eq-solves-field, eq-solves-service-dev) — the assistant MUST confirm which before connecting.
5. The assistant MUST NOT remove DEMO_FLAG comments — they mark live re-enable points.
6. The assistant MUST NOT delete files without explicit permission.
7. The assistant MUST NOT hardcode credentials, API keys, or secrets anywhere.
8. The assistant MUST NOT run INSERT, UPDATE, DELETE, or Supabase schema changes without explicit approval.
9. Auth changes MUST be reviewed in chat before any deployment.
10. Every Netlify/Cloudflare Pages site MUST ship with a `_headers` security file.

---

## Legal & Entity

11. Outputs MUST NOT reference GKE Lawyers or Gilbert + Tobin in any EQ document or correspondence.
12. Outputs MUST NOT include 173 Chuter Ave, Sans Souci NSW 2219 in marketing or public-facing materials.
13. Complex compliance matters MUST be flagged for Webb Financial or legal advisors — the assistant MUST NOT act unilaterally on them.
14. Hexican Holdings Trust MUST be treated as a CGT investor across all crypto — NOT as trading stock. Capital losses in HHT are quarantined within the trust and MUST NOT be flowed to personal or CDC.

---

## Brand

15. The EQ logo mark MUST NOT be recoloured — Sky #3DA8D8 always.
16. Outputs MUST NOT use gradients or drop shadows (EQ Design Brief v1.3).
17. Only two logo variants MAY be used — Blue and White (v1.3 supersedes the old three-variant rule).
18. New documents MUST NOT use legacy email addresses (rwm185@pm.me or roycemilmlow@gmail.com).
19. **Outputs MUST NOT use real client names — generic placeholders MUST be used instead** ("Data Centre Client A", "Tier 1 Client", etc.).
   - **Outputs** means anything sent to, shown to, or seen by parties outside Royce: documents, emails, presentations, draft replies, public artefacts, agent responses where the user is not Royce.
   - **Substrate is exempt** — files in `eq-context` (this repo, including `sks/active.md`, `sks/pending.md`, `sks/team.md`, `sks/templates.md`) MAY use real client names because operational fidelity matters more than scrubbing internal context. The assistant MUST NOT carry those names into outputs without redacting them to placeholders first. Conscious carve-out, 2026-05-04 audit.

---

## Financial

20. CDC Solutions has passed the Results Test on the Delta Elcom engagement — no further PSI tests are required.
21. HHT crypto holdings MUST be treated under the CGT investor method universally — personal, HHT, and SMSF.
22. MIS risk: pooled employee contributions managed by others trigger managed investment scheme concern. AHD MUST use company retained earnings on company operations, NOT pooled contributions.
