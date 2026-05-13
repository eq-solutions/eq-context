---
title: OPS — Decisions Log
owner: Royce Milmlow
last_updated: 2026-05-13
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

## 2026-05-13 — Path C: Absorb sks-field-reports workflows into EQ Field as a Sub-Module

**Status:** Accepted

**Decision:** Workflows from Ben Ritchie's standalone `sks-field-reports.netlify.app` (v29) — Prestart, Toolbox Talk, Daily Site Diary, Weekly Site Report — fold into EQ Field's new "Site Reports" sub-module rather than continuing as a separate SKS internal tool. Treat this as collaboration with Ben, not replacement: his MVP shapes the EQ implementation, and `sks-field-reports.netlify.app` retires only once EQ Field reaches parity on all four workflows AND Ben + Royce sign off on the cutover. Prestart MVP shipped to EQ Field demo as v3.4.69 on 2026-05-13.

**Why:** Two separate apps maintaining the same workflows is the failure mode the substrate audits keep flagging in other places. Folding the workflows into EQ Field (a) gives the commercial product real operational depth (Site Reports becomes a flagship sub-module, not just timesheets), (b) keeps a single canonical data store (`prestarts` table on both Supabases as of 2026-05-13), (c) avoids the dual-source confusion that already required a yellow banner on the EQ Prestart page directing users away from Ben's app, and (d) sets up the commercial unlock — a Friday compliance pack export bundling staff + licences + prestarts + toolbox + weekly into Hammertech/Aconex/Procore format — which only works against one canonical dataset.

**Alternatives considered:**

- **Path A — keep both apps running indefinitely** (rejected — duplicate maintenance, dual-source data, no path to the compliance pack export commercial unlock).
- **Path B — rebuild EQ Field's version independently, ignoring Ben's MVP** (rejected — Ben's app is battle-tested with SKS supervisors; throwing away tacit operational knowledge would re-introduce bugs already squashed in v29).
- **Path D — deprecate sks-field-reports immediately and force migration** (rejected — SKS supervisors currently rely on Ben's tool; pulling the rug before EQ Field parity would break their daily workflow).

**Implications:**

- EQ Field's Site Reports module ships workflows in the order Prestart → Toolbox Talk → Daily Diary → Weekly Report. Toolbox Talk is next (v3.4.74).
- Hub/dashboard restructure deferred until ≥2 workflows ship (no premature abstraction with only Prestart).
- Sub-module lives in "Testing (DO NOT USE)" sidebar section with BETA chips until each workflow soaks on demo.
- Demo → main merge for Site Reports is gated on Ben Ritchie sign-off (not just Royce go) — Ben is a stakeholder, not just an information source.
- Ben Ritchie credit / consulting engagement / role in EQ team to be resolved by Royce + Webb Financial (open coordination item).
- Test prestart rows Ben writes during trial must be cleaned before retirement: `DELETE FROM prestarts WHERE works_scope LIKE 'Test%' OR created_by = '<test name>';`
- Retirement of `sks-field-reports.netlify.app` requires communication window to SKS supervisors — not a silent cutover.
- Compliance pack export (DOCX/PDF generator bundling all 4 workflows for Hammertech/Aconex/Procore) is the demo that closes EQ customer #2 — pre-built only after all 4 workflows exist.

---

## 2026-05-13 — Demo Version Numbers: Second-to-Merge Bumps, Both Shapes Coexist

**Status:** Accepted

**Decision:** When two parallel Claude sessions target the same `demo` branch with the same version number, the second-to-merge bumps to the next number rather than blocking, and both shapes coexist on demo for soak. The branch name keeps its original label (so `claude/v3.4.67-prestart` can ship as v3.4.69 after rebase) — the ship version is what's in the banner/APP_VERSION/sidebar/sw.js tuple, not the branch name.

**Why:** On 2026-05-13 two workstreams collided: Phase B+C role system (`claude/v3.4.68-role-system-clean`) and Site Reports / Prestart MVP (`claude/v3.4.67-prestart`). Both wanted v3.4.68. Role system landed first as v3.4.68 (PR #63); Prestart rebased on top and bumped to v3.4.69 (PR #62). Both ship together because gating either workstream on the other's soak would have delayed customer-visible value by 5-7 days for no defensible reason.

**Alternatives considered:**

- **Serialise via lock file or coordination doc** (rejected — overhead for a 2-3x/year event; Claude sessions are short enough that the rebase cost is small).
- **Pre-allocate version ranges per workstream** (deferred — could revisit if this collision happens twice more; not worth pre-building for an N=1 case).
- **Block second-to-merge until first-to-merge passes soak** (rejected — couples otherwise-independent workstreams; soaks routinely take 5-7 days which would freeze parallel work).

**Implications:**

- Always run `git log origin/demo --oneline -3` before claiming a version number — the brief assumed v3.4.69 was the tip on 2026-05-13 but v3.4.70-73 had already shipped behind it.
- Outstanding brief documents that name a target version (e.g. "Toolbox v3.4.70") become stale fast — confirm the actual next-free number at session start.
- Version bumps are a 4-file tuple per the global feedback memory (banner + APP_VERSION + sidebar span + sw.js CACHE); the rebase-and-bump path must update all four, not just the banner.
- When two parallel worktrees run, confirm worktree paths before multi-step git ops — the working-directory header in a brief can refer to a different worktree than the one the new session is in.

---

## 2026-05-13 — eq-field-app Repo Canonical Org is Milmlow (Personal Account)

**Status:** Accepted

**Decision:** The `eq-field-app` GitHub repo lives at `github.com/Milmlow/eq-field-app` (Royce's personal account). One repo, two long-lived branches: `main` = SKS Labour App (live, deploys to sks-nsw-labour.netlify.app), `demo` = EQ Field demo. References to `eq-solutions/eq-field-app` are stale.

**Why:** A 2026-05-13 substrate audit found `eq/products.md` (Milmlow) and `sks/products.md` (eq-solutions) disagreed about the org prefix on the same repo. Confirmed with Royce 2026-05-13 that the personal account is canonical. Deploy pattern (push to main → Netlify CD to sks-nsw-labour) currently runs from the personal-account repo; migrating to the org would require redoing Netlify integration, which is not on the priority list.

**Alternatives considered:**

- Migrate to `eq-solutions/eq-field-app` (rejected — Netlify integration would need to be redone; no business reason to move it; an SKS live product depends on it deploying cleanly).
- Maintain a fork in eq-solutions and mirror (rejected — duplicate state, the exact failure mode this audit was fixing).

**Implications:**

- `sks/products.md` patched to use Milmlow prefix (2026-05-13).
- Future repo references in any file MUST use `Milmlow/eq-field-app`.
- If the repo ever does migrate to the org, this entry gets superseded — do not silently move references.

---

## 2026-05-13 — EQ Solves Service is Next.js, Documented as Exception to Vite Default

**Status:** Accepted

**Decision:** `rules/stack.md` declares Vite + React as the default frontend for new work. EQ Solves Service is built on **Next.js 16** (App Router, TypeScript strict, Tailwind v4) and is logged as a deliberate exception. Confirmed via direct inspection of `github.com/Milmlow/eq-solves-service` README and `next.config.ts` 2026-05-13.

**Why:** A 2026-05-13 substrate audit found `rules/stack.md` (Vite default) and `eq/products.md` (EQ Solves Service "Next.js + Supabase + Netlify serverless functions") disagreed. Both files were correct in isolation — Vite IS the default, AND EQ Solves Service IS Next.js. The fix was to make the exception explicit in `rules/stack.md`, not to change either underlying fact.

**Alternatives considered:**

- Change `rules/stack.md` default from Vite to Next.js (rejected — most prototypes and the legacy single-HTML apps are vanilla / Vite-shaped; making Next.js the default would mis-direct future small tools).
- Migrate EQ Solves Service to Vite (rejected — production app with 169 commits, 80+ Vitest tests, 22 sprints, first paying customer; Next.js features in use include App Router, server actions, image optimisation, edge middleware — a Vite migration is a multi-week rewrite with no business case).
- Leave the contradiction in `eq/products.md` and `rules/stack.md` (rejected — every audit re-flags it; ambiguity in `rules/` files compounds quietly).

**Implications:**

- `rules/stack.md` now lists EQ Solves Service as the first Exception entry alongside the legacy single-HTML apps.
- Future EQ products should default to Vite unless a Next.js-specific feature (SSR, ISR, server actions) is genuinely required — and if so, document the choice in `ops/decisions.md` before scaffolding.

---

## 2026-05-04 — Decline ChatGPT Structural Expansion Proposal (Operations / Contracts / Modes / START.md)

**Status:** Accepted

**Decision:** Decline ChatGPT's "EQ Context — System Review & Next-Step Plan" proposal in full, with two minor exceptions noted below for possible future revisit. The proposal would have added four new structural elements to the substrate (`/operations/`, `/contracts/`, `/modes/`, `/START.md`) plus rewrites of "loaders into execution contracts" and a JSON schema layer for output standardisation. Rejected as speculative architectural expansion against a substrate that is < 2 hours old in its current form and has not yet been used in a single real-world session. The proposal solves theoretical gaps, not observed ones.

**Why:** The substrate underwent a major refactor on 2026-05-04 specifically to *reduce* structural complexity (state/, knowledge/, drafts/, four root files → tier-separated four-tier model + thin pointers). ChatGPT's review, while correctly diagnosing the system as "behaviourally strong but executionally weak," prescribed re-introducing complexity under different names. Accepting it would have undone the day's consolidation work. The actual remedy for the diagnosed gap is *templates*, not *architecture* — and templates grow organically as operational outputs are produced (one currently exists: SKS Quote v3). Speculative pre-building of operations, contracts, and mode files is the exact failure mode the refactor was designed to escape.

**Alternatives considered:**

- **Accept full ChatGPT proposal** (rejected — restores complexity just deconstructed; introduces 4 new folders and a JSON schema layer; speculative against zero real-world session evidence).
- **Accept "drift correction" rule (item 7) only** (deferred — useful idea but small enough to add organically the first time a real session shows the problem; not worth a commit on its own).
- **Accept "minimum session-close fallback" (item 9) only** (deferred — same reasoning; the existing 5-step §10 has not been used enough to know if a fallback is needed).
- **Accept "structured exploration output pattern" (item 4)** (rejected — risks making exploration formulaic, which defeats its purpose; revisit only if real exploration outputs feel inconsistent in practice).

**Implications:**

- The substrate stays as deployed at session close 2026-05-04: tier-separated repo, single CLAUDE.md behavioural contract, two thin pointer files, no `/operations/`, no `/contracts/`, no `/modes/`, no `/START.md`.
- The original ChatGPT proposal text is logged here for future revisit. Items 7 (drift correction) and 9 (minimum session-close) remain candidates for organic adoption if real-world use surfaces the gaps they predict.
- Re-evaluation trigger: if after ~2 weeks of real-world use across Chat/Cowork/Code, operational outputs are still inconsistent OR sessions are skipping the start protocol, revisit ChatGPT's proposal with felt-need evidence rather than theoretical critique.
- General principle: do not expand substrate structure speculatively. Wait for observed gaps. Theoretical gaps are not gaps.

---

## 2026-05-04 — Real Client Names Permitted in Substrate, Forbidden in Outputs

**Status:** Accepted

**Decision:** Rule #19 ("real client names MUST NOT appear in outputs — use generic placeholders") applies to outputs only. The substrate (`eq-context` repo) MAY contain real client names because operational fidelity is the substrate's whole purpose. The assistant MUST redact to generic placeholders ("Data Centre Client A", "Tier 1 Client") whenever substrate content is carried into outputs.

**Why:** A 2026-05-04 audit found 5 substrate files containing real client names (Equinix, AirTrunk, AWS, DigiCo, Schneider, Telstra, Microsoft) — surfacing the ambiguity in the original rule. Two failure modes were possible: (1) scrub all names from substrate, losing operational fidelity ("Equinix SY6 CUFT" carries protocol/facility/expectation context that "Data Centre Client A SY6" does not); (2) leave the contradiction in place, accepting that every audit re-flags it. Carve-out resolves both: substrate keeps its fidelity, outputs stay clean.

**Alternatives considered:**

- **Strict scrub of substrate** (rejected — loses real operational context that makes the substrate useful; recurring cleanup cost as new names get added; the eq-context repo is private with low leak risk).
- **Leave the contradiction in place** (rejected — every audit will flag this as a violation; ambiguity in non-negotiables compounds quietly).
- **Move client names to a separate encrypted file** (rejected — over-engineered for the actual risk; adds reading-friction to the highest-value tier).

**Implications:**

- Rule #19 in `rules/non-negotiables.md` clarified with substrate carve-out.
- The assistant MUST redact substrate-sourced client names to generic placeholders before any output (document, email, presentation, public artefact).
- "Outputs" defined as: anything sent to, shown to, or seen by parties outside Royce.
- This entry exists so future audits don't re-flag the substrate as a rule violation.

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

**Why:** localStorage removes all backend complexity during battle-testing. Real usage will reveal actual data model needs — designing for Supabase upfront risks building the wrong schema.

**Alternatives considered:** Supabase from day one (rejected — adds auth complexity before value is proven); no persistence (rejected — data loss between sessions kills the use case).

**Implications:** Users must use Export → Backup JSON regularly to protect data until migration. Migration path is clean: data shape stays identical, only read/write functions swap out.

---

## 2026-04-05 — One Shared Cloudflare Worker for All Apps

**Status:** Accepted

**Decision:** Single `anthropic-proxy` worker shared across EQ Expenses, SKS Receipt Tracker, and all future tools needing Anthropic API access.

**Why:** The worker is stateless and generic — it has no app-specific logic. One worker means one API key, one deployment, one place to rotate credentials.

**Alternatives considered:** Per-app workers (rejected — multiplies maintenance for no benefit).

**Implications:** Every new tool that needs AI points at the same URL. Never create a new worker.

---

## 2026-04-05 — eq-context Folder in GitHub (not Supabase)

**Status:** Accepted — reinforced by 2026-04-28 "GitHub is the Source of Truth" decision.

**Decision:** Store the living project context (CLAUDE.md + subfiles) in a GitHub repo, not in Supabase or Claude Project files.

**Why:** GitHub provides version history (every update is a commit), is portable, readable as raw files, and works natively with Claude Code when that enters the workflow. Supabase is better for structured data, not documents. Claude Project files are read-only for Claude — can't be updated programmatically.

**Alternatives considered:**

- Supabase (rejected — no version history, overkill for documents)
- Claude Project files (rejected — read-only, can't be updated in-session)
- Single flat file (rejected — doesn't scale; mixes stable rules with fast-changing state)

**Implications:** Every session that produces new knowledge or changes state ends with "update the MD" → Claude commits only changed files with meaningful commit messages.

---

## 2026-03-14 — EQ Property Solutions Incorporated as Wholly-Owned CDC Subsidiary

**Status:** Accepted

**Decision:** EQ Property Solutions Pty Ltd incorporated as a wholly-owned subsidiary of CDC Solutions.

**Why:** Separates property risk from the trading entity. CDC retains ownership and control. Cleaner for lending, cleaner for future equity/investor conversations.

**Implications:** Intercompany Services Agreement needed between CDC and EQ Property Solutions. All AHD property acquisition goes through EQ Property Solutions, not CDC directly.

---

## 2026-03 — AHD Targets New Build Over Established Property

**Status:** On Hold — AHD parked from public-facing materials; EQ Solves is sole public focus. Decision remains valid for re-activation in 2027 capital window.

**Decision:** Prefer new build / house-and-land packages over established property for AHD acquisitions.

**Why three reasons compound:**

1. Stamp duty savings (significant at $500K+)
2. Stronger depreciation (Division 40/43 on new build)
3. Housing crisis narrative alignment for future government engagement

**Key finding:** Two $500K new builds outperform one $750K established property on every employee-relevant metric — yield, depreciation, per-employee bonus impact.

**Alternatives considered:** Established property (rejected on above metrics); commercial property (rejected — outside Class 36 trademark scope and higher complexity).

---

## 2026-03 — AHD Primary Market: Adelaide North Corridor

**Status:** On Hold — same reason as the AHD New Build decision above.

**Decision:** Adelaide North corridor (SA) as primary target; Toowoomba (QLD) as fallback.

**Why:** Price point suits 90% LVR corporate lending; new build supply available; rental yields sufficient for AHD bonus distribution; lower entry cost than Sydney/Melbourne.

**Alternatives considered:** Sydney (rejected — price point too high for LVR strategy); Brisbane inner (rejected — oversupplied); Melbourne (rejected — stamp duty, land tax exposure).

---

## 2025 — CDC Solutions: PSI Results Test Pass on Delta Elcom

**Status:** Accepted

**Decision:** No further PSI testing required for CDC Solutions consulting income.

**Why:** CDC passes the Results Test on the Delta Elcom engagement: milestone-based fees (not time), liability sits with CDC (not Royce personally). Results Test pass makes all other PSI tests irrelevant.

**Implications:** CDC consulting income is legitimately company income, not personal services income. Personal tax treatment of Royce's drawings from CDC follows normal Division 7A / loan account rules.
