---
title: SKS-TEAM — Tier README
owner: Royce Milmlow
last_updated: 2026-05-15
scope: Substrate tier providing canonical AI guidance to the SKS NSW Operations team
read_priority: critical
status: live
audience: SKS team members' AI sessions (not Royce's personal sessions)
---

# SKS-TEAM — Tier README

This tier provides **canonical AI guidance to SKS NSW Operations team members** when they use Claude (or any AI) to draft customer-facing documents.

It is deliberately separate from the rest of `eq-context` because the audience is different: this tier is consumed by the team, not by Royce's personal sessions.

---

## What this tier is

A small, focused set of files that a team member's AI session fetches at the start of any document-drafting work. The files act as a **router** — directing the AI to the corporate-approved tools and templates, with canonical language and consistent question flows.

The team doesn't see this folder. They see their AI suddenly being more consistent. The folder is the mechanism behind that consistency.

---

## What this tier is NOT

- Not a replacement for SKS corporate templates or tools — it points to them.
- Not a place for Royce's personal SKS operational notes — those live elsewhere in the repo, outside this tier.
- Not a place for EQ product strategy.
- Not a place for sensitive client data, rates, or financial details — anything in here is potentially read by every team member's AI session.

---

## Rules of this tier

These rules exist to keep the tier extractable. If/when this content graduates to its own substrate (a dedicated SKS-team store, or an EQ product), separation should be mechanical — not a rewrite.

### 1. No cross-references to other tiers

Files in `sks-team/` MUST NOT reference, link to, or assume content from any other tier folder.

If a file in `sks-team/` needs information that currently lives in another tier, the relevant facts get *copied* into `sks-team/` — not linked. The cost of duplication is the price of separability.

The only exception: the master `CLAUDE.md` behavioural contract at the repo root. `sks-team/` files inherit the tone, formatting, and question-asking rules from `CLAUDE.md` because that contract applies to every Claude session everywhere.

### 2. Single writer

Royce is the only person who edits `sks-team/` files. Team members consume; they do not contribute. If a team member identifies a needed change, they raise it with Royce; Royce makes the call and updates centrally.

This isn't a control rule — it's a consistency rule. Multiple writers means drift; drift defeats the entire purpose of the tier.

### 3. Public-readable endpoint; team-safe content only

The files in this tier are served via the public Supabase edge function used by every other tier. Anyone with a URL can read them — by design, that's how the team's AI sessions fetch them.

Implication for what goes in here: **never include anything you wouldn't be comfortable showing every team member directly.**

- No real labour rates.
- No client-specific commercial terms or margins.
- No salary, commission, or individual-staff financial information.
- Generic guidance and canonical language only.

Real client names ARE permitted in this tier (matches the broader substrate carve-out for operational fidelity), but only at the level of "Equinix uses CUFT/IBX terminology" — not "Equinix's negotiated rate is $X". Names yes, commercials no.

### 4. Substrate audit applies

The standard substrate freshness audit covers this tier the same as any other. End-of-week review catches stale files in `sks-team/` the same way it catches stale files anywhere else.

### 5. Content stays self-contained

Each file in `sks-team/` should be readable in isolation. A team member's AI fetching `sks-team/quoting.md` should get everything it needs from that one file — without needing to fetch other files in this tier to make sense of it.

If a piece of guidance applies across multiple document types (e.g. a canonical exclusion list), prefer copying the canonical text into each file that needs it, rather than splitting it into a shared dependency. Same separability principle as Rule 1.

---

## Files in this tier

### Live

- `README.md` — this file
- `gateway.md` — **start here** — single-file master router; handles all document types; designed to be a Claude Project system prompt; rubbish-proof (drives the conversation from any input)
- `quoting.md` — canonical router for SKS team quoting (Client Services template); detailed standalone version
- `variations.md` — canonical router for variation claims; same depth as quoting.md
- `mops.md` — MOP (Method of Procedure) router; functional skeleton; evolving
- `clients/equinix.md` — Equinix terminology, site codes, and language patterns (light reference)
- `clients/schneider.md` — Schneider Electric terminology and project conventions (light reference)

### Planned

- `clients/nextdc.md` — NEXTDC site codes and submission conventions
- `clients/airtruck.md` — AirTrunk site codes and project patterns
- `jsas.md` — JSA / SWMS router (stubs in gateway.md; standalone when justified by usage)
- `itps.md` — ITP router (stubs in gateway.md; standalone when justified by usage)

Files are added when there's evidence of recurring drift in a document type.

---

## How team members access this tier

Team members don't visit GitHub or Supabase directly. Royce sets them up once; after that they just use Claude normally.

### Path A — Claude Project (recommended — set up once, works forever)

1. Team member opens Claude and creates a new Project called "SKS Documents" (or Royce creates it for them).
2. In the Project's system prompt, paste the contents of `gateway.md` — or the bootstrap fetch instruction:
   ```
   Fetch https://raw.githubusercontent.com/eq-solutions/eq-context/main/sks-team/gateway.md and follow its instructions exactly for every conversation in this project.
   ```
3. Done. Every conversation in that Project automatically has the full routing logic. The team member just types what they need — even vague input works.

**gateway.md is designed to handle rubbish input.** The team member doesn't need to know what to type. Claude asks the right questions.

### Path B — Paste the file (for one-off use)

For someone who doesn't want to maintain a Project: paste the full contents of `gateway.md` at the start of any Claude conversation. Same result, less convenient.

### Path C — Direct file load (for specific document types)

A team member who only ever drafts quotes can load `quoting.md` directly (more focused, same quoting quality). Same pattern for `variations.md` or `mops.md`. Only use this if the team member's workload is limited to one document type.

---

## How this tier extracts cleanly later

If/when `sks-team/` graduates to its own substrate (dedicated SKS-team Supabase project, or an EQ product), the migration is mechanical:

1. Copy the entire `sks-team/` folder to the new repo / new Supabase project.
2. Update the team's Project prompts: change the hostname in the fetch URL.
3. Delete `sks-team/` from `eq-context`.

That's it. Three steps, no content rewrites, because the tier was already isolated by Rules 1 and 5.

---

## Update cadence

Same cadence as the rest of the substrate:

- `quoting.md` and other working files: updated whenever Royce identifies a real improvement (canonical language change, new corporate template version, recurring drift pattern caught in spot-checks).
- `README.md`: updated only when the rules of the tier change. Should be stable for months at a time.
