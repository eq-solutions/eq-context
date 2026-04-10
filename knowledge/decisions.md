---
title: Knowledge — Decisions
owner: Royce Milmlow
last_updated: 2026-04-10
scope: Append-only log of key decisions and the reasoning at the time
read_priority: standard
status: live
---

# Knowledge — Decisions

Append-only log. Key decisions and the reasoning behind them — reasoning
disappears faster than outcomes, which is why this file is the most
important one to maintain.

Format: Decision → Why → Alternatives considered → Implications.
For the current built state of each system, see `knowledge/architecture.md`.

---

## 2026-04-05 — SKS Receipt Tracker: localStorage over Supabase for v1

**Decision:** Ship with localStorage, migrate to Supabase when multi-user is needed.
**Why:** localStorage removes all backend complexity during battle-testing. Real usage will
reveal actual data model needs — designing for Supabase upfront risks building the wrong schema.
**Alternatives considered:** Supabase from day one (rejected — adds auth complexity before
value is proven); no persistence (rejected — data loss between sessions kills the use case).
**Implications:** Users must use Export → Backup JSON regularly to protect data until migration.
Migration path is clean: data shape stays identical, only read/write functions swap out.

---

## 2026-04-05 — One Shared Cloudflare Worker for All Apps

**Decision:** Single `anthropic-proxy` worker shared across EQ Expenses, SKS Receipt Tracker,
and all future tools needing Anthropic API access.
**Why:** The worker is stateless and generic — it has no app-specific logic. One worker means
one API key, one deployment, one place to rotate credentials.
**Alternatives considered:** Per-app workers (rejected — multiplies maintenance for no benefit).
**Implications:** Every new tool that needs AI points at the same URL. Never create a new worker.

---

## 2026-04-05 — eq-context Folder in GitHub (not Supabase)

**Decision:** Store the living project context (CLAUDE.md + subfiles) in a GitHub repo,
not in Supabase or Claude Project files.
**Why:** GitHub provides version history (every update is a commit), is portable,
readable as raw files, and works natively with Claude Code when that enters the workflow.
Supabase is better for structured data, not documents.
Claude Project files are read-only for Claude — can't be updated programmatically.
**Alternatives considered:**
- Supabase (rejected — no version history, overkill for documents)
- Claude Project files (rejected — read-only, can't be updated in-session)
- Single flat file (rejected — doesn't scale; mixes stable rules with fast-changing state)
**Implications:** Every session that produces new knowledge or changes state ends with
"update the MD" → Claude commits only changed files with meaningful commit messages.

---

## 2026-03-14 — EQ Property Solutions Incorporated as Wholly-Owned CDC Subsidiary

**Decision:** EQ Property Solutions Pty Ltd incorporated as a wholly-owned subsidiary of CDC Solutions.
**Why:** Separates property risk from the trading entity. CDC retains ownership and control.
Cleaner for lending, cleaner for future equity/investor conversations.
**Implications:** Intercompany Services Agreement needed between CDC and EQ Property Solutions.
All AHD property acquisition goes through EQ Property Solutions, not CDC directly.

---

## 2026-03 — AHD Targets New Build Over Established Property

**Decision:** Prefer new build / house-and-land packages over established property for AHD acquisitions.
**Why three reasons compound:**
1. Stamp duty savings (significant at $500K+)
2. Stronger depreciation (Division 40/43 on new build)
3. Housing crisis narrative alignment for future government engagement
**Key finding:** Two $500K new builds outperform one $750K established property on every
employee-relevant metric — yield, depreciation, per-employee bonus impact.
**Alternatives considered:** Established property (rejected on above metrics);
commercial property (rejected — outside Class 36 trademark scope and higher complexity).

---

## 2026-03 — AHD Primary Market: Adelaide North Corridor

**Decision:** Adelaide North corridor (SA) as primary target; Toowoomba (QLD) as fallback.
**Why:** Price point suits 90% LVR corporate lending; new build supply available;
rental yields sufficient for AHD bonus distribution; lower entry cost than Sydney/Melbourne.
**Alternatives considered:** Sydney (rejected — price point too high for LVR strategy);
Brisbane inner (rejected — oversupplied); Melbourne (rejected — stamp duty, land tax exposure).

---

## 2025 — CDC Solutions: PSI Results Test Pass on Delta Elcom

**Decision:** No further PSI testing required for CDC Solutions consulting income.
**Why:** CDC passes the Results Test on the Delta Elcom engagement:
milestone-based fees (not time), liability sits with CDC (not Royce personally).
Results Test pass makes all other PSI tests irrelevant.
**Implications:** CDC consulting income is legitimately company income, not personal services income.
Personal tax treatment of Royce's drawings from CDC follows normal Division 7A / loan account rules.
