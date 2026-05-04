---
title: EQ Solutions — Master AI Context
owner: Royce Milmlow
last_updated: 2026-05-04
scope: Project entry point. Navigation index — points at authoritative files, does not restate them.
read_priority: critical
status: live
---

# EQ Solutions — Master AI Context

> Read this file first. Read `AGENTS.md` second (cross-LLM behaviour rules).
> At session end: update the relevant tier's `pending.md`, write `sessions/YYYY-MM-DD.md`,
> push to `main`. The sync action + DB trigger guarantee Supabase freshness.

This file is a **navigation index**. Per `rules/non-negotiables.md`
Substrate section: each fact has one home. Update facts in their home,
not here. This file points; the homes carry the content.

---

## Who I Am

Royce Milmlow — NSW Operations Manager at SKS Technologies (electrical
contractor: data centre + healthcare). Founder of EQ Solutions (SaaS
suite for trade subcontractors). Co-director of EQ Property Solutions
with Emma Curth.

Full entity tree, accounts, contacts: **`ops/entities.md`**.
Supabase project IDs and infra accounts: **`system/infrastructure.md`**.

---

## Tier Loading

This repo is tier-separated. At session start, the assistant MUST ask:
**"Is this an EQ session or an SKS session?"** before loading context
beyond `CLAUDE.md` and `AGENTS.md`.

| Tier | Default load |
|---|---|
| **EQ session** | `eq/README.md` + `eq/pending.md` |
| **SKS session** | `sks/README.md` + `sks/pending.md` + `sks/active.md` |
| **Cross-tier task** | Both — state explicitly which tier owns the work |
| **OPS task** (entities, tax, finance) | `ops/` files, only when explicitly relevant |
| **System/substrate work** | `system/` files |

Default load NEVER includes both tiers. The whole point of separation
is that EQ work doesn't surface SKS noise and vice versa.

`/archive/` is read ONLY when the user explicitly references parked or
deferred content (EQ Quotes, AHD).

---

## Read order at session start

0. **`system/onboarding.md`** — first-time read only. Skip if you've worked
   in this repo before. ~5 minute walkthrough of the substrate.
1. **This file** (`CLAUDE.md`) — entry point.
2. **`AGENTS.md`** — cross-LLM rules (asking-questions convention,
   working principle, finish-what-you-start).
3. **Ask the tier question** above.
4. **Load tier defaults** based on the answer.
5. **`system/md-style.md`** — before writing or updating any MD file.

Then confirm what you have, ask what we're working on.

---

## Where things live

| Topic | Authoritative file |
|---|---|
| Hard rules that override everything | `rules/non-negotiables.md` |
| Brand standard (EQ Design Brief v1.3) | `rules/brand.md` |
| Deployment guardrails | `rules/deployment.md` |
| Default tech stack | `rules/stack.md` |
| Entities, accounts, registrations | `ops/entities.md` |
| Supabase project IDs, Cloudflare, Netlify, Beelink | `system/infrastructure.md` |
| EQ pending work | `eq/pending.md` |
| EQ products | `eq/products.md` |
| EQ Field multi-tenancy plan | `eq/field/multi-tenancy/` |
| EQ Field permissions matrix | `eq/field/permissions/` |
| SKS pending work | `sks/pending.md` |
| SKS active projects (rolling) | `sks/active.md` |
| SKS team | `sks/team.md` |
| SKS products | `sks/products.md` |
| SKS templates (quote v3, client blocks) | `sks/templates.md` |
| OPS pending (Webb, infra, substrate) | `ops/pending.md` |
| Tech architecture (Cloudflare, Supabase, substrate) | `system/architecture.md` |
| Financial architecture (AHD, Delta cliff, CDC PSI) | `ops/financial-architecture.md` |
| Decisions (append-only) | `ops/decisions.md` |
| Tech lessons (append-only) | `system/lessons.md` |
| Per-product changelogs | `eq/changelog/`, `sks/changelog/` |
| Dated session logs | `sessions/YYYY-MM-DD.md` |
| MD style standard | `system/md-style.md` |
| Parked / deferred content | `archive/` |

Do not duplicate content from these files into this one. Add facts in
their home; this index just points.

---

## Killed / deferred — do not reference as live products

(From the 2026-04-29 cull and 2026-05-04 refactor.)

- **EQ Variations** — killed. Removed from products map.
- **EQ Compliance / EQ Ops** — killed. Removed from products map.
- **EQ Quotes** — deferred ~6 months. Changelog at `archive/changelog-eq-quotes.md`.
- **EQ Expenses** — demoted to internal SKS tool. No longer an EQ product.
- **AHD** — parked to 2027 capital activation review. Changelog at `archive/changelog-ahd.md`.

---

## Session End Protocol (non-negotiable)

1. **Verify every recommendation surfaced this session was either
   applied or explicitly deferred to the relevant `pending.md` with a
   date.** No half-applied work. (See `rules/non-negotiables.md` §0.)
2. Update the active tier's `pending.md` — tick completed, add new items.
3. Insert `sessions/YYYY-MM-DD.md` — log what was built/decided.
4. Update relevant `*/changelog/*.md` if a product changed.
5. Push to GitHub `main`. The sync action propagates to Supabase
   within ~20 s; the DB trigger + verification job guarantee
   `updated_at` freshness on every synced row.

---

## How I work

- Direct and concise — skip preamble, deliver first.
- Push back if something is wrong.
- Build fast and iterate — match that pace.
- Self-critique mode on: "stress test this" / "devil's advocate" /
  "10/10 version".
- Pre-mortem required before any build session: 3 risks, mitigations,
  then go.
- Questions get clickable cards, never open-ended. Briefing in chat
  text *before* the card. Recommended option first; free-text fallback
  always present. Full rule: `AGENTS.md` "Asking questions".

### Output preferences (was AI-RULES.md)

- **Documents and specs:** Markdown.
- **Customer-facing deliverables (SKS quotes, O&M):** Word or PDF.
- **Code:** Write in full. Never use `// rest of the file stays the same`.
- **Prompts:** Copy-paste ready.
- **Specs:** Written for a founder, not an enterprise team.

### What Royce hates

- Being asked obvious follow-up questions before the task is attempted.
- Responses that restate the question before answering.
- Suggestions to hire someone or use a different tool without compelling reason.
- Hedging everything with overly cautious disclaimers.
- Unnecessary complexity.

---

## Workstation note

Primary AI workstation: **Beelink** (Ryzen 7 7735HS, 32 GB RAM, 1 TB
NVMe), exposed via Cloudflare Tunnel as `beelink.eq.solutions`. Chrome
Remote Desktop from the work PC because ThreatLocker blocks Tailscale.
Global CLAUDE.md path: `C:\Users\Royce\.claude\CLAUDE.md`.
