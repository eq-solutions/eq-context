# EQ Context — Master Index

> This is the first file Claude reads in every session.
> It is a map, not a document. Detail lives in subfiles.
> When updating: edit the relevant subfile, not this one.
> Last updated: 2026-04-05

---

## Who & What

**Royce Milmlow** — founder of EQ Solutions, NSW Operations Manager at SKS Technologies.
**Emma Curth** — co-director, EQ Property Solutions and CDC Solutions.
**Entity trading as EQ:** CDC Solutions Pty Ltd (ACN 651 962 935).
**Accountant:** Webb Financial (Andrew, agent 25818815).
**Primary email:** royce@eq.solutions

---

## How We Work

- Deliver complete drafts first. Explain briefly after. No preamble.
- Working before refactoring. Never restructure while fixing.
- One step at a time on deployments. Confirm before proceeding.
- End every session: "update the MD" → commit only changed files.
- Log decisions when made. Log lessons when the pain is fresh.

---

## File Map

| File | What it contains | Update frequency |
|------|-----------------|-----------------|
| `rules/deployment.md` | Deployment guardrails, branch rules, cross-deploy prohibitions | Rarely |
| `rules/brand.md` | Colours, fonts, logo rules for EQ and subsidiaries | Rarely |
| `rules/non-negotiables.md` | Hard rules Claude never breaks | Rarely |
| `state/products.md` | Every product — current version, status, URLs, architecture | Each session |
| `state/pending.md` | Active to-do list across all workstreams | Every session |
| `state/entities.md` | Business entities, bank accounts, key contacts, credentials index | When things change |
| `knowledge/architecture.md` | Why things are built the way they are | When decisions are made |
| `knowledge/lessons.md` | Technical gotchas and hard-won learnings | When pain is fresh |
| `knowledge/decisions.md` | Key decisions made and the reasoning behind them | When decisions are made |
| `sessions/YYYY-MM-DD.md` | What was worked on, what changed, what's next | Each session |

---

## Non-Negotiables (full detail in rules/non-negotiables.md)

1. Never deploy without explicit instruction
2. Never expose Anthropic API key in frontend
3. Never cross-deploy between EQ and SKS codebases
4. Never spin up a new Supabase project — use eq-field-app always
5. Never remove DEMO_FLAG comments
6. Never reference GKE Lawyers or Gilbert + Tobin
7. Never include 173 Chuter Ave in marketing materials

---

## Current Focus (detail in state/pending.md)

- SKS Receipt Tracker: deploy Cloudflare Worker, battle-test
- AHD: first property acquisition, solicitor engagement
- FY24/25 tax lodgement across all entities
- EQ trademark: monitor post August 2026
