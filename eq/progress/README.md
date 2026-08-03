---
title: EQ Progress — Index
owner: Royce Milmlow
last_updated: 2026-08-03
scope: How any AI session tracks commercial, product, and strategic progress toward the 2026 year-end EQ evaluation
read_priority: standard
status: live
---

# EQ Progress

Tracks progress against the decision to put 100% effort into EQ for the
rest of 2026, evaluated at year-end — commercial and strategic signal,
not engineering to-do (that's `eq/pending.md`) and not the per-session
build log (that's `sessions/*.md`).

This tier does not duplicate either of those. It answers a narrower
question neither one covers: *is the business case for EQ getting
stronger or weaker, week over week, and why.*

## Files

| File | Purpose | Update discipline |
|---|---|---|
| `year-goals.md` | Draft evaluation criteria. **The live, CI-gated goal lives in `system/TODAY.md`'s GOALS block** — this file only holds proposed criteria until Royce promotes them there. | Overwrite in place |
| `current.md` | Rolling weekly structured update — shipped, commercial signal, blockers, next focus, year-end notes | Append a new `## Week of YYYY-MM-DD` section each week; never edit past weeks |
| `customers.md` | Design partners / pilots / commercial conversations register | Overwrite in place |
| `decisions-log.md` | Hard judgment calls and production scars worth remembering for the portfolio/FDE narrative — narrower lens than `ops/decisions.md` (technical ADRs) or `suite-state.md`'s Key Decisions (suite-wide, auto-derived). Cross-link, don't duplicate. | Append-only |

## How an AI should use this

1. **Read `year-goals.md` first, then `system/TODAY.md`'s GOALS block.** If both say UNSET, there is no year-end target to measure against yet — say so plainly, per `CLAUDE.md` §1's freshness gate.
2. **Never write a goal here or in TODAY.md.** Assistants propose (in `year-goals.md`); only Royce sets the live goal (in `TODAY.md`).
3. **At session end, if EQ commercial/product/strategic ground moved**, add an entry to `current.md`. If a customer/pilot signal changed, update `customers.md`. If a hard judgment call was made that matters for the year-end narrative — not just a technical ADR — append it to `decisions-log.md`. Commit only the changed files with a clear message. This is an on-demand note in `CLAUDE.md` §10, not a mandatory step — populate it when there's something real to log, not on a fixed cadence.
4. **Don't invent commercial signal.** An empty `customers.md` row or a blank week in `current.md` is honest; a filled-in one that didn't happen is the exact failure mode `system/TODAY.md` was burned by once already (see `system/lessons.md`).
