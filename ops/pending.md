---
title: OPS Tier — Pending Actions
owner: Royce Milmlow
last_updated: 2026-05-13
scope: Operational support to-do list — Webb, infra, substrate
read_priority: standard
status: live
---

# OPS Tier — Pending

EQ items in `eq/pending.md`. SKS items in `sks/pending.md`. This file is
for operational support: tax, entities, infrastructure, substrate.

---

## Substrate Discipline

- [ ] **`system/writing-style.md` — awaiting writing samples** —
  File does not yet exist. Identified as a gap in May 2026 substrate
  review. Cannot be drafted from training data — must be built from
  real examples to be useful. Action required from Royce: supply
  5–10 writing samples (emails, Slack messages, docs written in his
  voice). Once supplied: Claude Chat session to analyse → draft
  `system/writing-style.md` → commit to /system tier.

- [ ] **`system/TODAY.md` outcomes — Royce to define** —
  Scaffold landed 2026-05-13 with placeholder outcomes. Royce to
  answer: "What are the three things that, if true on 1 August 2026,
  mean Q3 was a success?" Replace bracketed placeholders, flip
  frontmatter `status` from `scaffold-awaiting-input` to `live`,
  remove the Status section at the bottom.

- [ ] **Orientation file `cowork-eq-context-orientation.md` is stale** —
  Holiday-period orientation file describes the post-refactor layout
  as 5 directories (eq, sks, ops, system, archive) and claims `rules/`
  was removed. Reality (2026-05-13 audit): `rules/` is still present
  with 4 active files referenced by CLAUDE.md §7 and §8. Also claims
  44 rows synced; actual is 47. Orientation file is not in the substrate
  itself — lives wherever Royce stores Cowork session prompts. Update
  it next time it's edited.

- [ ] **VC cull execution prompt (`cowork-prompt-2026-04-29.md`)** —
  Holiday orientation referenced a Chat-generated prompt covering 6
  tasks for the 2026-04-29 product cull (Variations killed, Ops
  killed, Expenses internal-only, Quotes deferred). The cull decisions
  ARE already reflected in CLAUDE.md, eq/products.md, and
  archive/. The prompt itself was not in the substrate at 2026-05-13
  audit and was not uploaded that session. Royce to confirm: either
  (a) cull is fully landed and prompt can be archived as "complete",
  or (b) re-supply the prompt for execution if anything is still
  unapplied.

- [ ] **Calendar event registered** — recurring "Review eq-context rules/* for currency" on 28 April annually, first fires 2027-04-28. Owner: Royce. Outcome logged as session entry. **(Royce manual step.)**

- [ ] **Collapse sync-workflow duplicate state** — `.github/workflows/sync-context.yml` currently has two path lists that must stay in sync manually: the YAML `on.push.paths:` filter (decides workflow triggers) and the Python `SUBDIR_PATTERNS` glob (decides what files the script reads). Drift between them caused `sks-team/*` to silently never sync from 2026-05-04 to 2026-05-07. Worth either deriving one from the other, or adding a CI check that asserts they cover the same folders. Footgun documented in `system/lessons.md` 2026-05-07.

- [ ] **Edge-function checklist for substrate-structure changes** — when adding a new tier folder, the Supabase `context` edge function is on the checklist of things to update alongside the workflow. The 2026-05-04 tier refactor missed this and silently 404'd most tier-deep paths until 2026-05-07. Documented in `system/lessons.md` 2026-05-07. Could be hardened by adding a daily `/context/<random-slug>` smoke test or by parsing the edge function's behaviour against `context_files` rows.

---

## Cross-Tool Consistency — Original Reason for 2026-05-04 Refactor

The 2026-05-04 tier refactor solved tier-bleed and dead-product noise within Claude. It did NOT solve cross-tool consistency between Chat / Cowork / Code / ChatGPT / Grok. The substrate is now canonical for Claude only; ChatGPT and Grok still walk into every session blind. Three follow-up items, prioritised:

- [ ] **(A) ChatGPT and Grok bootstrap prompts** — produce `CHATGPT-PROMPT.md` and `GROK-PROMPT.md` mirroring `COWORK-PROMPT.md` (paste-once-per-session prompts that fetch the same canonical Supabase URLs). Highest-priority, lowest-risk follow-up. Closes the original framing: "consistency across all tools."
- [x] **(C) `TODAY.md` — current-focus surface** — scaffold landed 2026-05-13 at `system/TODAY.md`. Q3 outcomes still need to be defined by Royce (see Substrate Discipline above).
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
