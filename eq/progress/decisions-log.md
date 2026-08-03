---
title: EQ Progress — Decisions Log (Portfolio / FDE Narrative)
owner: Royce Milmlow
last_updated: 2026-08-03
scope: Append-only log of hard empirical judgment calls and production scars worth remembering for the year-end/portfolio narrative — narrower than ops/decisions.md
read_priority: standard
status: live
---

# EQ Progress — Decisions Log

**Scope, so this doesn't become a third copy of the same thing:**
- `ops/decisions.md` — the ADR log: technical/architectural decisions,
  suite-wide, formal Status/Decision/Why/Alternatives/Implications shape.
- `suite-state.md` "Key Decisions" — auto-derived nightly from merged PRs,
  suite-wide, engineering-facing.
- **This file** — the subset of those (or things too informal for an ADR)
  that matter for *telling the story later*: what the empirical evidence
  actually forced, not just what shipped. If it's a routine technical
  call, it belongs in `ops/decisions.md` instead — link to it rather than
  copying it here.

Append-only. Format: date + one-line context + the decision.

---

## 2026-08-03 — Built the EQ progress-tracking substrate

**Context:** the decision to put 100% effort into EQ for the rest of 2026,
evaluated at year-end, needed a durable way to track commercial/strategic
signal — not just engineering pending items.

**Decision:** extend the existing git-native substrate (`eq/progress/`)
rather than adopt an external tracking tool. Kept the year-end-criteria
mechanism singular — proposals live in `year-goals.md`, the one live goal
object stays in `system/TODAY.md`'s CI-gated GOALS block, not duplicated.

**Why:** `CLAUDE.md` §1's own lesson (`system/lessons.md` "The Substrate
Contained a Goal Nobody Owned") is exactly the failure mode a second goals
file would risk. One mechanism, one gate.
