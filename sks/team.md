---
title: SKS-TEAM — Tier README
owner: Royce Milmlow
last_updated: 2026-05-04
scope: Substrate tier providing canonical AI guidance to the SKS NSW Operations team
read_priority: critical
status: live
audience: SKS team members' AI sessions (not Royce's personal sessions)
---

# SKS-TEAM — Tier README

This tier exists to provide **canonical AI guidance to SKS NSW Operations team members** when they use Claude (or any AI) to draft customer-facing documents.

It is deliberately separate from the rest of `eq-context` because the audience is different: this tier is consumed by the team, not by Royce's personal sessions.

---

## What this tier is

A small, focused set of files that a team member's AI session fetches at the start of any document-drafting work. The files act as a **router** — directing the AI to the corporate-approved tools and templates, with canonical language and consistent question flows.

The team doesn't see this folder. They see their AI suddenly being more consistent. The folder is the mechanism behind that consistency.

---

## What this tier is NOT

- Not a replacement for SKS corporate templates or tools — it points to them.
- Not a place for Royce's personal SKS operational notes — those live in `sks/` (one tier up).
- Not a place for EQ product strategy — that lives in `eq/`.
- Not a place for sensitive client data, rates, or financial details — anything in here is potentially read by every team member's AI session.

---

## Rules of this tier

These rules exist to keep the tier extractable. If/when this content graduates to its own substrate (a dedicated SKS-team store, or an EQ product), separation should be mechanical — not a rewrite.

### 1. No cross-references to other tiers

Files in `sks-team/` MUST NOT reference, link to, or assume content from `eq/`, `sks/`, `ops/`, `system/`, or `archive/`.

If a file in `sks-team/` needs information that currently lives in another tier, the relevant facts get *copied* into `sks-team/` — not linked. The cost of duplication is the price of separability.

The only exception: the master `CLAUDE.md` behavioural contract at the repo root. `sks-team/` files inherit the tone, formatting, and question-asking rules from `CLAUDE.md` because that contract applies to every Claude session everywhere.

### 2. Single writer

Royce is the only person who edits `sks-team/` files. Team members consume; they do not contribute. If a team member identifies a needed change, they raise it with Royce; Royce makes the call and updates centrally.

This isn't a control rule — it's a consistency rule. Multiple writers means drift; drift defeats the entire purpose of the tier.

### 3. Public-readable; treat as such

The files in this tier are served via `https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/sks-team/*`. Anyone with the URL can read them. By design, that's how the team's AI sessions fetch them.

Implication: never include in this tier anything you wouldn't be comfortable showing every team member directly. No real labour rates. No client-specific commercial terms. No salary or commission information. Generic guidance and canonical language only.

### 4. Substrate audit applies

The standard substrate audit query (see `system/lessons.md` "Substrate Audit Query") covers this tier the same as any other. End-of-week review catches stale files in `sks-team/` the same way it catches stale files in `sks/` or `eq/`.

### 5. Content stays self-contained

Each file in `sks-team/` should be readable in isolation. A team member's AI fetching `sks-team/quoting.md` should get everything it needs from that one file — without needing to fetch `sks-team/scopes.md` or `sks-team/clarifications.md` to make sense of it.

If a piece of guidance applies across multiple document types (e.g. a canonical exclusion list), prefer copying the canonical text into each file that needs it, rather than splitting it into a shared dependency. Same separability principle as Rule 1.

---

## Files in this tier

### Live

- `README.md` — this file
- `quoting.md` — canonical router for SKS team quoting (Client Services template)

### Planned (not yet built)

- `scopes.md` — canonical scope-of-works language patterns (when justified by usage)
- `mops.md` — Method of Procedure document guidance (when team starts producing them via AI)

Files are added when there's evidence of recurring drift in a document type. No speculative additions — same lesson as the parent `eq-context` substrate.

---

## How team members access this tier

Team members don't visit GitHub or Supabase directly. They use one of two access paths:

### Path A — Claude Project (recommended for AI-fluent users)

The team member sets up a Claude Project called "SKS Quoting" with a specific system prompt (held separately as `PROJECT-PROMPT-SKS-TEAM.md`). The Project's system prompt instructs Claude to fetch `sks-team/quoting.md` at the start of every conversation in that Project, then follow its instructions exactly.

Setup is one-time, ~15 minutes per team member.

### Path B — Paste-the-prompt (for ad-hoc users)

A team member who doesn't want to maintain a Project pastes the same prompt at the start of any Claude conversation when drafting a quote. Less convenient, same result.

Both paths produce identical output because both fetch the same canonical `quoting.md`.

---

## How this tier extracts cleanly later

If/when `sks-team/` graduates to its own substrate (dedicated SKS-team Supabase project, or an EQ product), the migration is mechanical:

1. Copy the entire `sks-team/` folder to the new repo / new Supabase project.
2. Update the team's Project prompts: change the hostname in the fetch URL from `urjhmkhbgaxrofurpbgc.supabase.co` to whatever the new host is.
3. Delete `sks-team/` from `eq-context`.

That's it. Three steps, no content rewrites, because the tier was already isolated by Rules 1 and 5.

---

## Update cadence

Same cadence as the rest of the substrate:

- `quoting.md` and other working files: updated whenever Royce identifies a real improvement (canonical language change, new corporate template version, recurring drift pattern caught in spot-checks).
- `README.md`: updated only when the rules of the tier change. Should be stable for months at a time.

---

## Related decisions

For the architectural reasoning behind this tier, see `ops/decisions.md`:

- 2026-05-04 — Decline ChatGPT Structural Expansion Proposal (the precedent against speculative tier additions; this tier was added with concrete justification, not speculation)
- 2026-05-04 — Real Client Names Permitted in Substrate, Forbidden in Outputs (the carve-out applies to `sks/` files, NOT to `sks-team/` files — see Rule 3 above)
