---
title: OPS — Decisions Log
owner: Royce Milmlow
last_updated: 2026-05-04
scope: Append-only log of key decisions across all tiers and the reasoning at the time
read_priority: standard
status: live
---

# OPS — Decisions Log

Append-only log. Key decisions and the reasoning behind them — reasoning
disappears faster than outcomes, which is why this file is the most
important one to maintain.

Format: Status → Decision → Why → Alternatives considered → Implications.
Status values: Accepted | Superseded by [date+title] | On Hold | Deprecated | Proposed.
Append-only — never delete an entry. Supersede or deprecate it instead.
For the current built state of each system, see `system/architecture.md`.

---

## 2026-04-28 — Annual `rules/*` Review Cadence

**Status:** Accepted

**Decision:** All files in `rules/` are reviewed for currency once per year. Mechanism: a recurring calendar event on 28 April each year titled "Review eq-context rules/* for currency". The reviewer (Royce) confirms each rule still applies, amends or supersedes any that don't, and logs the review as a session entry with a "no changes" or "changes applied" outcome.
**Why:** ISO 27001 requires annual review of security policies; the same pattern transfers to any normative ruleset that can drift quietly. `rules/` is the lowest-changing folder by design — without an explicit review cadence, files accumulate stale assumptions invisibly.
**Alternatives considered:**
- `last_reviewed` frontmatter field (rejected 2026-04-28 — duplicates `updated_at` semantics; ritual without signal).
- Quarterly review (rejected — overkill for a folder that changes ~3x/year).
- No formal review (rejected — the gap closes here for ~10 minutes/year of work).
**Implications:**
- Calendar event registered on 2026-04-28; first review fires 2027-04-28.
- The Friday substrate audit (`eq-context-substrate-audit` agent) checks freshness, not currency. This decision adds the currency check at annual cadence.
- Out-of-cycle review is permitted whenever a rule is suspected stale — surface via the relevant tier's `pending.md`.

---

## 2026-04-28 — RFC 2119 Modal Verbs Adopted in `rules/`

**Status:** Accepted

**Decision:** Rules in `rules/non-negotiables.md` use RFC 2119 modal verbs (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) for the bolded rule statements. Narrative prose remains conversational.
**Why:** Rules are normative documents. Without standardised modal verbs, "always X" and "never X" can be read as either absolute or aspirational — fine for two readers who share context, ambiguous for automation or new collaborators.
**Alternatives considered:**
- Apply across all `rules/*` files immediately (deferred — start with non-negotiables; expand as other rules files mature).
- Stay informal (rejected — gap against ISO 80000-1 / RFC 2119 conventions, and the substrate is now mature enough to merit formality).
**Implications:**
- New rules added to `rules/non-negotiables.md` MUST use a modal verb.
- Other `rules/*` files (`brand.md`, `deployment.md`, `stack.md`) MAY adopt the same convention when next edited; not retrofitted unless a real change is being made.
- A meaning-altering rewrite (vs vocabulary sharpening) is a decision-grade change — surfaced via the relevant tier's `pending.md`, not committed inline.

---

## 2026-04-28 — ADR Status Field Adopted on decisions.md

**Status:** Accepted

**Decision:** Every entry in `ops/decisions.md` carries a `Status` field — one of Accepted, Superseded by [date+title], On Hold, Deprecated, or Proposed. Inserted between the entry heading and the `Decision` line.
**Why:** Closes the only real gap against the Nygard ADR standard. Without a Status field, superseded decisions sit alongside current ones with no visual signal — the prose handles supersession but the structure doesn't, which means a fresh reader has to parse every entry to know what's still in force.
**Alternatives considered:**
- Move superseded entries to `decisions-archive.md` immediately (rejected — premature at 13 entries; revisit at 30+).
- Add `last_reviewed` frontmatter (rejected 2026-04-28 — adds ritual without signal once `updated_at` is reliable).
**Implications:**
- All future decision entries MUST start with a `**Status:**` line (codified in `system/md-style.md` ADR section).
- When a decision is superseded, the new decision's title is appended to the old entry's Status line; both entries remain in the file.
- At 30+ entries, split into `decisions-archive.md` for non-Accepted entries.

---

## 2026-04-28 — Supabase Context Store Lives in eq-solves-service-dev, Table is `context_files`

**Status:** Accepted

**Decision:** Confirm the runtime context store as table `context_files` (id, slug UNIQUE, filename, content, updated_at) inside the `eq-solves-service-dev` Supabase project (`urjhmkhbgaxrofurpbgc`) — not a separate dedicated context project, and not the table name `claude_context` that earlier memory carried.
**Why:** Live audit of Supabase 2026-04-28 returned the actual schema. The `context_files` table is the canonical runtime read source for all assistants. Creating a second project just for context would split costs and add an MCP target for no functional benefit while the row count is small (~30).
**Alternatives considered:**
- Dedicated `eq-context-store` Supabase project (rejected — context volume is tiny; multi-project sprawl is worse than co-tenancy with the product DB).
- Move to `claude_context` named table for clarity (rejected — rename would break the live sync action and existing MCP reads; the slug column already gives clarity).
**Implications:**
- All future Supabase MCP queries against the context store target table `context_files`, project `urjhmkhbgaxrofurpbgc`.
- The table is co-located with EQ Solves Service product data; tenant separation is by *table*, not project. This is acceptable because `context_files` has no `tenant_id` and is not part of the multi-tenant data plane.
- Update `system/architecture.md` next session to document this co-tenancy explicitly.

---

## 2026-04-28 — GitHub is the Source of Truth; Direct Supabase Writes are Emergency-Only

**Status:** Accepted

**Decision:** Chat (claude.ai web/mobile) drafts MD deltas; Cowork or Code commits them to GitHub; the sync action propagates to Supabase. Direct chat writes to the `context_files` Supabase table are reserved for emergencies only and must be reconciled to GitHub the same day.
**Why:** Bypassing GitHub destroys the audit trail that is the actual moat of eq-context. The git log is the substrate's value — once Supabase and GitHub drift, every "what did we decide and why" question has two possibly-conflicting answers.
**Alternatives considered:**
- Allow chat to write Supabase routinely (rejected — silently demotes git to a backup).
- Block all chat writes period (rejected — emergencies happen and the runtime store should reflect ground truth).
**Implications:**
- Add a non-negotiable: "GitHub is canonical. Supabase is cache." (see `rules/non-negotiables.md` follow-up — separate task).
- Any direct-Supabase write must append a flag to the relevant tier's `pending.md` titled "RECONCILE: <slug> written direct to Supabase on <date>".

---

## 2026-04-28 — "Done" in eq-context Means a Fresh Supabase updated_at, Nothing Else

**Status:** Accepted

**Decision:** A change is not "done" until the row in `context_files` shows a fresh `updated_at`. Terminal output, commit hashes, and "looks good" visual confirmation do not count.
**Why:** Three claims of completion in one session (2026-04-27/28) all turned out to be false on measurement: a wrong table name in memory, a "brief implemented" that hadn't been pushed, and a "push landed" where two of three files weren't actually edited. Each surface signal looked correct. Only the Supabase row's `updated_at` exposed the gap.
**Alternatives considered:**
- Trust git push output (rejected — push can succeed on the wrong content).
- Trust commit message intent (rejected — commit messages and diffs are routinely mismatched).
**Implications:**
- After every eq-context push, run the verification SQL (see `system/lessons.md` "Substrate Audit Query") and confirm the expected files show today's date.
- Stop using "done" as a status word in this repo unless the SQL has been run.

---

## 2026-04-17 — EQ Design Brief v1.3 Supersedes v1.2

**Status:** Accepted

**Decision:** Move to EQ Design Brief v1.3 as the canonical brand reference.
**Why:** v1.2 allowed three logo variants (Blue, White, Black) and had looser accessibility guidance. v1.3 simplifies to two variants (Blue, White), locks Aptos Display as the print companion to Plus Jakarta Sans web, and mandates WCAG AA minimum. Reducing variants reduces production drift.
**Alternatives considered:** Staying on v1.2 (rejected — Black variant was being misused on busy backgrounds; AA compliance was inconsistent).
**Implications:** All new documents use v1.3 palette and type scale. Old Black logo assets retained but flagged legacy — not for new work.

---

## 2026-04 — Three Supabase Projects, Not One

**Status:** Accepted — supersedes the prior non-negotiable "never spin up a new Supabase project" (which never had a discrete decision entry).

**Decision:** Run three Supabase projects — sks-labour (live), eq-solves-field (demo), eq-solves-service-dev (context store) — instead of the original one-project rule.
**Why:** SKS live production data and EQ demo experiments sharing a project is an unacceptable blast radius. Tenant prefixes (`sks_`, `eq_`) protect tables, but don't protect against a rogue schema migration or a bad DELETE run against the wrong table. Hard project boundaries do.
**Alternatives considered:**
- One project with tighter RLS (rejected — RLS doesn't protect against owner-level mistakes)
- Two projects, SKS vs EQ (rejected — context store belongs in its own paid project with its own access pattern)
**Implications:** Always confirm project ID before connecting. Never touch sks-labour without explicit "SKS live" instruction. The old non-negotiable "never spin up a new Supabase project" is retired — replaced by "never touch SKS live without explicit instruction".

---

## 2026-04-05 — SKS Receipt Tracker: localStorage over Supabase for v1

**Status:** Accepted

**Decision:** Ship with localStorage, migrate to Supabase when multi-user is needed.
**Why:** localStorage removes all backend complexity during battle-testing. Real usage will
reveal actual data model needs — designing for Supabase upfront risks building the wrong schema.
**Alternatives considered:** Supabase from day one (rejected — adds auth complexity before
value is proven); no persistence (rejected — data loss between sessions kills the use case).
**Implications:** Users must use Export → Backup JSON regularly to protect data until migration.
Migration path is clean: data shape stays identical, only read/write functions swap out.

---

## 2026-04-05 — One Shared Cloudflare Worker for All Apps

**Status:** Accepted

**Decision:** Single `anthropic-proxy` worker shared across EQ Expenses, SKS Receipt Tracker,
and all future tools needing Anthropic API access.
**Why:** The worker is stateless and generic — it has no app-specific logic. One worker means
one API key, one deployment, one place to rotate credentials.
**Alternatives considered:** Per-app workers (rejected — multiplies maintenance for no benefit).
**Implications:** Every new tool that needs AI points at the same URL. Never create a new worker.

---

## 2026-04-05 — eq-context Folder in GitHub (not Supabase)

**Status:** Accepted — reinforced by 2026-04-28 "GitHub is the Source of Truth" decision.

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

**Status:** Accepted

**Decision:** EQ Property Solutions Pty Ltd incorporated as a wholly-owned subsidiary of CDC Solutions.
**Why:** Separates property risk from the trading entity. CDC retains ownership and control.
Cleaner for lending, cleaner for future equity/investor conversations.
**Implications:** Intercompany Services Agreement needed between CDC and EQ Property Solutions.
All AHD property acquisition goes through EQ Property Solutions, not CDC directly.

---

## 2026-03 — AHD Targets New Build Over Established Property

**Status:** On Hold — AHD parked from public-facing materials; EQ Solves is sole public focus. Decision remains valid for re-activation in 2027 capital window.

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

**Status:** On Hold — same reason as the AHD New Build decision above.

**Decision:** Adelaide North corridor (SA) as primary target; Toowoomba (QLD) as fallback.
**Why:** Price point suits 90% LVR corporate lending; new build supply available;
rental yields sufficient for AHD bonus distribution; lower entry cost than Sydney/Melbourne.
**Alternatives considered:** Sydney (rejected — price point too high for LVR strategy);
Brisbane inner (rejected — oversupplied); Melbourne (rejected — stamp duty, land tax exposure).

---

## 2025 — CDC Solutions: PSI Results Test Pass on Delta Elcom

**Status:** Accepted

**Decision:** No further PSI testing required for CDC Solutions consulting income.
**Why:** CDC passes the Results Test on the Delta Elcom engagement:
milestone-based fees (not time), liability sits with CDC (not Royce personally).
Results Test pass makes all other PSI tests irrelevant.
**Implications:** CDC consulting income is legitimately company income, not personal services income.
Personal tax treatment of Royce's drawings from CDC follows normal Division 7A / loan account rules.
