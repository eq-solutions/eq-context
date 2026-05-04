---
title: OPS Tier — Pending Actions
owner: Royce Milmlow
last_updated: 2026-05-04
scope: Operational support to-do list — Webb, infra, substrate
read_priority: standard
status: live
---

# OPS Tier — Pending

EQ items in `eq/pending.md`. SKS items in `sks/pending.md`. This file is
for operational support: tax, entities, infrastructure, substrate.

---

## Substrate Discipline

- [ ] **Calendar event registered** — recurring "Review eq-context rules/* for currency" on 28 April annually, first fires 2027-04-28. Owner: Royce. Outcome logged as session entry. **(Royce manual step.)**

---

## Cross-Tool Consistency — Original Reason for 2026-05-04 Refactor

The 2026-05-04 tier refactor solved tier-bleed and dead-product noise within Claude. It did NOT solve cross-tool consistency between Chat / Cowork / Code / ChatGPT / Grok. The substrate is now canonical for Claude only; ChatGPT and Grok still walk into every session blind. Three follow-up items, prioritised:

- [ ] **(A) ChatGPT and Grok bootstrap prompts** — produce `CHATGPT-PROMPT.md` and `GROK-PROMPT.md` mirroring `COWORK-PROMPT.md` (paste-once-per-session prompts that fetch the same canonical Supabase URLs). Highest-priority, lowest-risk follow-up. Closes the original framing: "consistency across all tools."
- [ ] **(C) `TODAY.md` — current-focus surface** — a 500-char file at repo root that captures the current week's priority and any blocked items. Auto-prepended to every session via the entry-point files. Cheap, high-signal, doesn't replace anything.
- [ ] **(B) Session-end discipline as a hard rule** — current rule says "update the substrate at session end"; lessons.md confirms the rule isn't being followed (17 of 30 stale at 2026-04-27). Revise to: every session ends with a written delta to a tier file (even "no changes today, status confirmed"), assistant refuses to close otherwise. Decision-grade change to non-negotiables.

Defer to: Beelink return (12 May+) for proper test coverage. Holiday-laptop work has higher risk of introducing new issues we can't test rigorously.

---

## Infrastructure — Live Blockers

- [ ] **OAuth GitHub MCP connector** — consent-screen auto-login loop blocks org-picker flow for `claude.ai` chat. Cowork writes are unblocked via PATs (2026-04-19); this item only gates the chat surface. Fix: revoke prior OAuth grant at `github.com/settings/applications`, sign out, reconnect from Claude desktop.
- [ ] **PAT rotation** — Milmlow + eq-solutions fine-grained PATs expire 2026-05-19. Calendar reminder set for 2026-05-16.

---

## Tax & Entities (Webb Financial)

- [ ] FY24/25 lodgements — personal, CDC, HHT, MFT/Allcraft
- [ ] Personal vehicle depreciation amendment (~$33,800 refund)
- [ ] Emma FY23/24 ITR amendment
- [ ] EQ Property Solutions TFN receipt
- [ ] Milmlow Holdings / MFT / Allcraft review — September 2026

---

## Parked — AHD (revisit 2027)

Australian Housing Dividend parked from public-facing materials; revisit
for capital activation by 2027. Keep structure warm but not active.
Changelog at `archive/changelog-ahd.md`.

- [ ] TFN receipt from ATO
- [ ] Correct ABR business activity code to 6711
- [ ] Engage solicitor for ISA, MIS Position Paper, EISP sign-off
- [ ] First property acquisition — Adelaide North corridor / SE QLD fallback
- [ ] Government engagement letter (NSW Treasurer) — post first bonus paid
