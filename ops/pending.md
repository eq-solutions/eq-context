---
title: OPS Tier — Pending Actions
owner: Royce Milmlow
last_updated: 2026-07-19
scope: Operational support to-do list — Webb, infra, substrate
read_priority: standard
status: live
---

# OPS Tier — Pending

EQ items in `eq/pending.md`. SKS items in `sks/pending.md`. This file is
for operational support: tax, entities, infrastructure, substrate.

---

## Full substrate audit — 95 findings across the whole eq-context repo (2026-07-19)

Royce asked for a deep-dive, full review of the substrate ("spend the time now
then we can trust our truth") after a Chat-sync friction session surfaced a
CLAUDE.md §9 fact-duplication bug. Five parallel read-only audits (system/,
eq/, sks/, ops+rules/, root+archive) found 95 distinct issues — stale facts,
cross-file contradictions, broken pointers, duplicate/forked files, missing
frontmatter. Built as an interactive triage tool (published Artifact,
localStorage-backed status + notes per finding, export to markdown) rather
than a flat list, since 95 items needs sorting/filtering to be usable.

**Findings that turned out to be real incidents, not just doc drift:**
- [x] `rules/non-negotiables.md` had been **silently truncated** by a
  2026-05-30 commit — rule 21 (HHT CGT) and rule 22 (MIS risk / AHD must use
  retained earnings, not pooled contributions) were deleted; rule 22's content
  existed nowhere else live. Unenforced for 7 weeks, never caught. **Restored
  (PR #97).**
- [x] `ops/security-register.md` (carries the SEC-1 P0 PII-leak finding) was
  **orphaned** — not linked from `ops/README.md` or `CLAUDE.md` §8, so a normal
  session bootstrap would never surface it. **Linked into both maps (PR #97).**
  SEC-1 itself is **NOT closed** — Royce confirmed sks-nsw-labour is still
  live, so the "fix at decommission" plan the register assumed is stale. Needs
  a fresh remediation call from Royce — see "Needs Royce" below.
- [x] `digest.md`/`substrate-facts.yml` were flagging **eq.solutions as a live
  drift** (claimed LIVE, observed DEAD). Resolved — Royce confirmed it's
  intentionally paused while working through SKS's employer adopting the
  software, to avoid drama mid-discussion. **PR #96** sets `status: paused` so
  the checker stops false-alarming; flip back to `live` when the site returns.

**Royce's judgment calls, applied:**
- [x] **sks-nsw-labour is still actively developed, no retirement date set** —
  corrected `sks/README.md`/`sks/products.md`, which wrongly called it
  frozen/decommissioning (PR #98).
- [x] **Full-auto EQ merge+deploy authority (2026-05-30 ADR) has lapsed** now
  that the Autonomous Sprint coordination mode is retired — ADR marked
  Superseded, the sprint-scope carve-out struck from `rules/non-negotiables.md`
  (PR #97). Back to explicit-instruction-required for everything.
- [x] **EQ-03 staff-count discrepancy (58 vs 39 in eq/products.md vs
  active.md)** — Royce's steer (supervision/management counted
  inconsistently) confirmed exactly via live query against ehow: 58 = all
  Direct staff; 39 = Direct AND on_roster AND NOT supervisor. Both numbers
  were correct, just measuring different subsets with no label. Fixed live
  snapshot added to `eq/active.md` (PR #103). Also surfaced: site count
  (591→250) and licence count (171→100) dropped substantially since the
  06-13 snapshot — flagged, not investigated.
- [x] **SKS-09 (two quote templates)** — confirmed deliberately separate, not
  duplicate/stale: `sks/templates.md`'s docx-js template is Royce's own
  full-document generator; `sks-team/quoting.md`'s SharePoint template is for
  the wider team, AI produces paste-in text blocks only. Cross-noted in both
  files, not a fix.

**Shipped:** PRs #94–#100, all merged to `main`. Fixed: circular §9 pointer
(CLAUDE.md ⇄ eq/products.md), a punch-list item instructing deploy to a
deleted Fly.io app, two plan docs that said "not started"/"PR open" for work
that actually shipped/merged weeks ago, a dead-Supabase-table SQL instruction
in `system/onboarding.md`, several incomplete file indexes (archive/README.md,
system/README.md, eq/README.md, ops/README.md), a dead workflow reference in
root README.md, and the CHAT-PROMPT.md freshness-check simplification from
earlier in the session (Royce: "that's annoying, I just want a simple
read-only prompt" — dropped the canary-token verification ritual).

**Follow-up session (2026-07-19, same day) — 4 more PRs, plus a Cowork bug found by asking:**
- [x] **Index-drift CI check shipped** (PR #101) — a GitHub Action that diffs
  each tier README's file index against the real folder contents and fails
  on mismatch. Directly prevents the "file exists but isn't linked anywhere"
  failure class that caused the `ops/security-register.md` orphan above.
  Cleared a 62-file backlog (mostly `eq/README.md`) to get it green.
- [x] **3 of 4 duplicate changelog pairs resolved** (PR #102) —
  `shell.md`/`service.md`/`cards.md` were genuinely abandoned (3-19 days
  stale vs their `eq-*.md` twin, no concurrent activity) — each now carries
  a "Superseded, use eq-*.md" banner rather than a content merge, to avoid
  losing history. **`field.md`/`eq-field.md` deliberately NOT touched** —
  investigation found both were being actively appended to on the same day,
  not one-stale-one-current like the others; merging live-written files
  risks clobbering a concurrent session's work. Needs Royce's call on which
  stays canonical.
- [x] **COWORK-PROMPT.md fixed** (PR #104) — was telling Cowork to fetch
  `CLAUDE.md` via `raw.githubusercontent.com`, the exact CDN-cache mechanism
  (F1) that served this file 8+ days stale with a 200 OK and no error, and
  the reason CHAT-PROMPT.md was moved off that pattern earlier the same
  session. CLAUDE.md's own §1 table already said Cowork should read the
  local clone, same as Code — this file just never matched. Found only
  because Royce asked "do we need to do anything for Cowork and Chat" —
  worth remembering to check tool-bootstrap files specifically after any
  fix to one of them, since they drift independently.

**Third follow-up session (2026-07-20) — 3 more PRs, audit substantively closed:**
- [x] **Field's changelog pair resolved** (PR #105) — `field.md` and
  `eq-field.md` were BOTH live-written for months (not one-stale-one-current
  like the other 3 pairs). 18 PRs that existed only in `eq-field.md` merged
  into `field.md` at their correct dates; `eq-field.md` retired with a
  merge banner. `field.md` is canonical.
- [x] **All 21 items from the first "still open" pass closed** (PR #106) —
  2 generator bugs fixed at the root (suite-state.md frontmatter never
  bumped; digest.md could show a PR as both Merged and pending), TODAY.md
  live-re-verified against ehow directly, several duplicate-fact spots
  trimmed to pointers, a handful confirmed false positives on close read.
- [x] **Round 2 of the "touched but unverified" findings closed** (PR #107)
  — most were already fixed by earlier PRs when checked directly; genuine
  finds: `ops/decisions.md`'s Phone Identity Dedup entry had been shipped
  and live for a month but still marked "Proposed" (verified via
  `pg_get_functiondef` on jvkn, corrected); **SEC-9 discovered** — a
  second, previously untracked service_role key (`jvkn`/eq-canonical,
  distinct from SEC-3's `ehowg` key) was pasted into a chat session
  2026-07-12 and never rotated.
- [x] **SEC-3 investigated and downgraded, SEC-9 confirmed P0** (PR #108)
  — per Royce's explicit "investigate exposure first" call, traced the
  "leaked" claim for SEC-3 back through every substrate file that could
  hold evidence and found none — only that the key is unrotated, not that
  it was ever actually leaked anywhere. A later, more careful 2026-06-07
  analysis (`cross-app-linkage-sprint-2026-06-07.md`) independently reached
  the same conclusion. Downgraded P0→P3/hygiene. SEC-9 stays P0 (confirmed
  chat-paste exposure) — Royce's call: same rotation window as SEC-3, not
  a separate urgent effort.

**Needs Royce:**
- [ ] **SEC-1** — still parked (Royce: "ignore sks nsw labour for now").
  sks-nsw-labour confirmed still live 2026-07-16, no retirement date.
- [ ] **SEC-9 rotation runbook** — doesn't exist yet. Write one (mirror the
  SEC-3/F1 runbook's staged pattern) before either SEC-3 or SEC-9 can
  actually be rotated.
- [ ] **Execute the SEC-3 + SEC-9 rotation** whenever Royce picks a window
  — both are live-secret actions requiring his explicit go, not something
  to do unilaterally.
- [ ] A residual tail of low-severity findings (stale dates on files never
  touched across any of the 4 follow-up PRs — `system/failures.md`,
  `system/lessons.md` narrative detail, `ops/financial-architecture.md`,
  `sks-team/README.md`, `sks/active.md`) — sit in the artifact if Royce
  wants to work through them, genuinely not urgent.

**Artifact:** interactive triage tool, published — Royce has the link from
earlier in the session (not repeated here since Artifact URLs are
account-scoped, not fetchable from a fresh session).

---

## Substrate Plan v2 — execution queue (added 2026-07-12, no deadline, goals UNSET)

Plan: `system/substrate-plan-v2.md` (supersedes substrate-a-plus-plan.md). All propose-only.
**Reshaped to a leaner cut (Royce, in-chat 2026-07-12):** collapse the full typed claims
ledger into the nightly pulse; defer workflow consolidation + memory-coverage CI (hygiene,
not urgent — "working before refactoring").

**Session update 2026-07-12 (cont.) — substrate thread PARKED (rabbit-hole call, Royce):**
- [x] **F4 "0 completions" alarm CORRECTED** — over-read; checks are future-scheduled (first due 2026-08-06), not broken. On main (PR #80).
- [x] **Frontmatter-schema CI check GREENED** — was chronically red (16 pre-existing violations), gates again. On main (PR #81).
- [~] **Product pulse — DROPPED.** Premise was the false F4 alarm. Revive only if a goal needs it.
- [ ] **Courier (P5) — PARKED**, not dropped. Manual `git checkout main && git pull` suffices.
- [x] **Auto-memory prune (F5 residue) — DONE 2026-07-12 (cont.), from Claude Code, not Cowork.**
  Corrects the note below: the auto-memory surface is NOT unreachable from Claude Code —
  it's a plain file directory (`C:\Users\EQ\.claude\projects\<project>\memory\*`),
  read/writable like any other file. Slimmed 3 memory files that copied drift-prone
  substrate facts (project IDs, CI-gate mechanics) instead of pointing at eq-context;
  reshaped 1 completed-sprint memory to just its durable lessons; `MEMORY.md` index updated.
- [ ] **Chat** — GitHub connector on + fresh session to read corrected main (hygiene).

**Done this session (2026-07-12, on branch `claude/substrate-plan-v2-review-bb96aa`):**
- [x] **Gate bug fixed** — `session_start.py` crashed on Windows (cp1252 can't encode the 🟠
  emoji it echoes from digest.md) → forced UTF-8 stdout. Adversarial suite **18/18 green**
  (was 15/18; the 3 gate tests caught it).
- [x] **Hooks wired in** — `C:\Projects\.claude\settings.json` created 2026-07-12 (merges with
  existing `settings.local.json`; does not clobber it). **Gap found + fixed 2026-07-12 (cont.):**
  that wiring only fires `SessionStart` for sessions launched at the `C:\Projects` umbrella
  root — repo-scoped and worktree sessions silently never ran the gate. Moved `SessionStart`
  to user-level `C:\Users\EQ\.claude\settings.json` so it fires for every session; the umbrella
  copy now carries only the (Windows no-op) `PreToolUse` pointer. `hooks/README.md` install
  instructions corrected to match.
- [x] **`auto-bump-frontmatter.yml` retired** — the "beetle" that manufactured false freshness
  (kept the phantom deadline looking current). Dates now come from real commits. Recoverable from git.

**Open:**
- [x] **Day 0 — F5** — RESOLVED 2026-07-12, then RE-OPENED AND ACTUALLY RESOLVED 2026-07-12 (cont.).
  The original "verified clean" claim was wrong on both counts: `~/.claude/CLAUDE.md` was
  NOT clean — its EQ Suite status table was 7 weeks stale and contradicted canonical
  (still called EQ Quotes "Built" after retirement); fixed to point at `suite-state.md`
  instead of restating status, backed up to `CLAUDE.md.bak` first. And the auto-memory
  surface was NOT unreachable from Claude Code — see the item above; done directly.
  Lesson: a "verified clean" claim needs the same live-check discipline as everything else —
  this one wasn't actually tested against the file, just asserted.
- [ ] **P2+P3 — product pulse (lean, build-next)** — nightly workflow: ~6 live `verify: sql`
  signals (checks created/completed, non-Royce writes excl. `source='system'`, prestarts/
  toolbox/audits, active users) + goal-expiry check + morning push on zero↔nonzero flips.
  **One promotion guard kept:** an agent may not mark its own claim `verified`. **Dropped:** the
  general typed `claims.yml` system (duplicated the pulse). (2026-07-12)
- [ ] **P5 — courier install** — Beelink-native scheduled git sync, eq-context/main only
  (approved `ops/decisions.md` 2026-07-12); gate reports courier age. (2026-07-12)
- [ ] **Deferred (P4 hygiene)** — `memory-coverage.yml`; consolidate workflows 17→≤8;
  CLAUDE.md diet ≤200 lines. Not urgent; each carries refactor risk. (2026-07-12)
- [x] Morning pulse — Cowork scheduled task `morning-pulse`, daily 07:05 — DONE 2026-07-12

**Session continuation 2026-07-12 (audit + F3 guard + memory collapse + sprint-cluster archive):**
- [x] **F3 guard actually BUILT** — `claim-expiry.yml` + `scripts/claim_expiry.py` (rung 1→3).
  TODAY.md's goals section previously *claimed* this guard existed when it didn't (the exact
  F3-class doc-honesty bug); now it's real — fails CI on any goal in TODAY.md that's undated,
  unowned, or past `expires_on`. 10/10 unit tests; dogfooded green on its own PR. (PR #82)
- [x] **Two doc-honesty defects fixed** — the F2 block message advised `cat >>` as a remedy,
  which the sibling F6 guard then blocks; and the phantom `claim-expiry.yml` claim above. (PR #82)
- [x] **Dead link in `SPRINT-BOARD.md`** fixed before archiving (pointed at a file already
  moved to `archive/sprints/`). (PR #83)
- [x] **`digest.md`'s persistent broken link fixed at the generator**, not the file —
  `refresh_digest.py` hoists `eq/pending.md`/`sks/pending.md` items verbatim into root-level
  `digest.md`; a link relative to `eq/` 404s once copied to root. `pending_open_items()` now
  re-roots relative links to repo root; self-corrects on next regen. (PR #84)
- [x] **Autonomous Sprint cluster archived** — `GROK.md`, `STATE.md`, `SPRINT-BOARD.md`,
  `direction-d-state.md` → `archive/` (git-renamed, history kept), each confirmed dormant
  first (not blind-archived): Grok isn't part of the active workflow; the sprint-board
  coordination mode is superseded by normal PRs + `suite-state.md`/`digest.md`; Direction D
  had zero inbound references anywhere in governed docs. Kept `AUTONOMOUS-SPRINT-RULES.md`
  (cited live by `CLAUDE.md` §7) with a banner noting §4/§6's board references are historical.
  Rewired every live pointer that treated the archived files as current (`eq/pending.md`,
  `ops/decisions.md`, `system/architecture.md`) — historical mentions in old planning docs
  left alone. A repo-wide re-scan caught one regression I introduced (an inbound link broken
  by the move) before merge. (PR #85)
- [x] **"Type the facts" investigated, no change needed** — `refresh_suite_state.py` already
  calls `raise_for_status()` on the live DB read, so a failed query **aborts the job** rather
  than stamping today's date on a stale count. The F1 trap was already closed by existing
  engineering; building more would have been the opposite of the lean-cut direction.
- [x] **Wire `hooks/adversarial_test.py` into CI — DONE 2026-07-12 (cont.).** `.github/workflows/adversarial-suite.yml`
  (PR #86). Took three iterations to get genuinely right — worth recording why. The naive fix
  (checkout `path:` containing a "/projects/" string segment) satisfied the guard's string-match
  check but not its filesystem check (`mount_roots()` globs for a REAL `/mnt/Projects` etc.);
  real CI caught this at 17/18 where my own local test had shown a false 18/18 — because my dev
  machine has a genuine `C:\Projects` that the guard found instead of my simulated path. Fixed by
  actually creating `/mnt/Projects` in the CI job (needs `sudo` on hosted runners) and relocating
  the checkout there for real. Confirmed on the real CI log (not just the checkmark): **18 passed,
  0 failed**, both standalone and again after merging PR #87's lessons.md trim on top.
- [x] **Trim `system/lessons.md` — DONE 2026-07-12 (cont.), 508 → 381 lines.** PR #87. Four
  incidents (F1, F2/F6, F3, "first guard failed open") were told in full narrative here AND in
  `system/failures.md`/`system/TODAY.md`/`hooks/README.md` — trimmed to a rule + pointer per the
  repo's own "one fact, one home" rule (`AUTONOMOUS-SPRINT-RULES.md` §7); six dead pre-GitHub
  Supabase-substrate entries got the same treatment. Full narratives preserved in new
  `archive/lessons-history.md`, not deleted. Every standalone still-useful gotcha left untouched.
  Caught fallout before committing: `ops/decisions.md:884` pointed at a heading that no longer
  exists (added a superseded-note); `adversarial_test.py`'s fixture name said "508-line" (renamed
  to "200-line" so it can't go stale again).
- [x] **Housekeeping (shared checkout git divergence) — resolved on its own, 2026-07-12 (cont.).**
  No action taken; a concurrent session's routine sync cleared it, exactly as flagged on the prior
  session-close card.
- [ ] **Branch protection on `main` — deliberately NOT done.** Nightly refresh crons push
  directly to `main` as `github-actions[bot]` (some with `[skip ci]`); naive required-checks
  would break them, and it wouldn't have caught F1/F3 anyway (both passed every green check).
  Built `claim-expiry.yml` instead (higher leverage, Royce's call). Revisit only if the crons
  move to a PR-based flow. _(added 2026-07-12)_

---

## Substrate Discipline

- [ ] **`system/writing-style.md` — awaiting writing samples** —
  File does not yet exist. Identified as a gap in May 2026 substrate
  review. Cannot be drafted from training data — must be built from
  real examples. Royce will supply 5–10 writing samples (emails, Slack
  messages, docs written in his voice) in a Claude Chat session from
  his work PC on a future day. Once supplied: Chat to analyse → draft
  `system/writing-style.md` → commit to `/system` tier.

- [x] **`system/TODAY.md` outcomes — DEFINED 2026-05-13** —
  Royce supplied the three Q3 2026 success outcomes (NSW running
  EQ Field / EQ Service in real ops; electrical + comms divisions
  integrated; AI used across all areas of life). TODAY.md promoted
  from scaffold to live status.

- [x] **VC cull execution prompt (`cowork-prompt-2026-04-29.md`) — CLOSED 2026-05-13** —
  Confirmed by Royce: the 2026-04-29 product cull is fully landed.
  Variations killed, Compliance/Ops killed, Quotes deferred, Expenses
  demoted to internal SKS tool. All reflected in CLAUDE.md §9,
  `eq/products.md`, and `archive/`. Prompt itself is archived as
  historical artefact — not needed for any further execution.

- [ ] **Orientation file `cowork-eq-context-orientation.md` updated 2026-05-13** —
  Holiday-period orientation file was stale (claimed `rules/` removed,
  44 rows, 3 unfixed bugs). Refreshed version produced this session
  describing current state: 49 rows, all 4 tier dirs + `rules/`/`sks-team/`/
  `sessions/` present, all 3 bugs resolved, TODAY.md live, VC cull closed.
  Lives outside the substrate (wherever Royce stores Cowork session
  prompts). Royce to drop in the updated copy.

- [ ] **Calendar event registered** — recurring "Review eq-context rules/* for currency" on 28 April annually, first fires 2027-04-28. Owner: Royce. Outcome logged as session entry. **(Royce manual step.)**

- [x] **Collapse sync-workflow duplicate state** — RESOLVED commit `e2cf57a` 2026-05-13. YAML `paths:` filter replaced with `*.md` + `**/*.md` (any MD change triggers). SUBDIR_PATTERNS in Python remains the precise scoped gate. No further drift possible between the two lists.

- [ ] **Edge-function checklist for substrate-structure changes** — when adding a new tier folder, the Supabase `context` edge function is on the checklist of things to update alongside the workflow. The 2026-05-04 tier refactor missed this and silently 404'd most tier-deep paths until 2026-05-07. Documented in `system/lessons.md` 2026-05-07. Could be hardened by adding a daily `/context/<random-slug>` smoke test or by parsing the edge function's behaviour against `context_files` rows.

- [ ] **Cowork cross-repo substrate leak vector** — Cowork sessions
      mounted on a non-eq-context repo (e.g. `eq-solves-field`) produce
      substrate-bound content (session logs, `eq/active.md`, pending
      updates) but cannot push to `eq-context` from the sandbox. The
      assistant drops the content into an `eq-context/` or
      `eq-context-updates/` folder in whatever repo *is* mounted, then
      the session ends. Without a hand-off step the leaked folders sit
      untracked in the wrong repo indefinitely. Confirmed live 2026-05-19
      audit found a 2026-05-14 Cowork session's outputs (4 files,
      ~330 lines including a missing `eq/active.md` and Tender Pipeline
      SKS-promotion blockers) stuck inside `eq-solves-field/eq-context/`
      and `eq-solves-field/eq-context-updates/` for 5 days. Recovered
      the operational facts into `eq/products.md` (infrastructure notes)
      and `eq/pending.md` (Tender Pipeline blockers); deleted the leaked
      folders. **Fix candidates:** (a) Cowork convention — every session
      that touches substrate-class content writes a single
      `SUBSTRATE-UPDATES.md` file at repo root visible at session close,
      so Royce sees the hand-off requirement; (b) per-repo `.gitignore`
      entry for `eq-context/` and `eq-context-updates/` so leaked
      folders never accidentally commit; (c) longer term — a Cowork
      hook that detects substrate-bound content and either pushes
      direct to `eq-context` (via PAT) or refuses to write outside it.
      Current "Cross-Tool Consistency" item (A) below frames this as a
      ChatGPT/Grok bootstrap issue — that's a different gap. This is
      the specific Cowork-from-wrong-repo leak pattern, which is
      live and recurring.

---

## Cross-Tool Consistency — Original Reason for 2026-05-04 Refactor

The 2026-05-04 tier refactor solved tier-bleed and dead-product noise within Claude. It did NOT solve cross-tool consistency between Chat / Cowork / Code / ChatGPT / Grok. The substrate is now canonical for Claude only; ChatGPT and Grok still walk into every session blind. Three follow-up items, prioritised:

- [x] **Claude Chat bootstrap — DONE 2026-07-03** — `CHAT-PROMPT.md` created + CLAUDE.md rewired (PR #59, squash `9a6bde3`): §1 gains a per-tool substrate-load table, the fetch-failure fallback is now a per-tool escalation ladder, §11 Chat row rewritten. Root cause encoded: claude.ai's fetch tool refuses model-constructed URLs and returns link previews, so Chat must read the substrate via the **GitHub connector**, never web fetch. Requires the connector working — see the OAuth item under Infrastructure, which now gates this.
- [ ] **(A) ChatGPT and Grok bootstrap prompts** — produce `CHATGPT-PROMPT.md` and `GROK-PROMPT.md` mirroring `COWORK-PROMPT.md` / `CHAT-PROMPT.md` (paste-once-per-session prompts fetching the raw GitHub URLs — the "canonical Supabase URLs" in the original framing are gone; edge cache retired 2026-06-22). Highest-priority, lowest-risk follow-up. Closes the original framing: "consistency across all tools."
- [x] **(C) `TODAY.md` — current-focus surface** — landed live 2026-05-13 at `system/TODAY.md` with three Q3 outcomes defined. Wired into CLAUDE.md §1 Step 4 as universal always-load — commit `e2cf57a` 2026-05-13.
- [ ] **(B) Session-end discipline as a hard rule** — current rule says "update the substrate at session end"; lessons.md confirms the rule isn't being followed (17 of 30 stale at 2026-04-27). Revise to: every session ends with a written delta to a tier file (even "no changes today, status confirmed"), assistant refuses to close otherwise. Decision-grade change to non-negotiables.

---

## Infrastructure — Live Blockers

- [ ] **OAuth GitHub MCP connector** — consent-screen auto-login loop blocks org-picker flow for `claude.ai` chat. Cowork writes are unblocked via PATs (2026-04-19); this item only gates the chat surface. Fix: revoke prior OAuth grant at `github.com/settings/applications`, sign out, reconnect from Claude desktop. **As of 2026-07-03 this gates the connector-first Chat bootstrap (`CHAT-PROMPT.md`)** — until the connector connects cleanly, Chat has no self-serve substrate path.
- [ ] **Restart the held Chat session on the new bootstrap** — enable/verify the GitHub connector on claude.ai, then open a **fresh** chat with `CHAT-PROMPT.md` pasted (connector tools don't load mid-session). The 2026-07-03 Chat thread that was stuck on the fetch wall can be abandoned — its held "substrate fix" was this same issue, closed by PR #59. **(Royce manual step.)** _(added 2026-07-03)_
- [x] **PAT rotation — DONE 2026-06-15** — new PATs generated and deployed. Confirmed by Royce.

---

## Multi-Repo Push Automation

- [x] **eq-context post-commit auto-push — INSTALLED 2026-05-14, hardened 2026-05-24** —
  `.githooks/post-commit` + `scripts/install-hooks.ps1` are the current
  mechanism (the original `hooks/` + `install-hooks.bat` pair was superseded
  2026-05-24 and removed 2026-05-30). After running `.\scripts\install-hooks.ps1`
  once per clone, every commit on `main` auto-pushes to `origin/main`.
  Substrate sync follows within ~30s. Docs: `system/git-automation.md`.
  Branches other than `main` skip the hook; failed pushes don't undo the commit.

- [ ] **eq-solves-field push blocked on `demo` branch** —
  2026-05-14 `push-all.bat` attempted push of local `demo` to
  `Milmlow/eq-field-app:demo`, rejected as non-fast-forward (remote has
  commits we don't). §11 hard rule also says never push `demo` without
  explicit instruction. Decisions needed: (a) `git pull --rebase origin
  demo` and re-push, or (b) switch local to `main` for the SKS labour
  app surface and push there, or (c) skip until the EQ Field branch
  strategy is settled. **Royce to call.**

- [ ] **Per-repo post-commit hooks for eq-cards and eq-solves-field** —
  only eq-context has the auto-push hook installed. The other two still
  need manual `git push`. Replicate the pattern once the eq-solves-field
  `demo` branch blocker above is resolved. Each repo's `demo`/`main`
  branch semantics differ — hook needs per-repo branch logic.

- [ ] **eq-solves-assets `feat/calm-capture` branch — parked 2026-05-20** —
  Local clone `C:\Projects\eq-solves-assets` (origin: `Milmlow/eq-solves-service`)
  has the `feat/calm-capture` branch with 2 unpushed commits last touched
  2026-05-13: `675ba1b Add .gitattributes` and `b15cd19 WIP: md-health
  sweep 2026-05-13`. File delta vs `origin/main`: new
  `ACB Asset Capture.html` (~1265 lines), new `.gitattributes`, removed
  70 lines from `src/lib/fillTemplate.ts`. Confirmed there's no remote
  tracking branch yet (work exists only in this folder). Royce decided
  2026-05-20 to park rather than action — "enough happening". Revisit
  when the EQ Solves Service surface is back on the active list. **Risk:**
  the 1265-line single-file capture tool is real work that will be lost
  if the clone is ever deleted without first pushing the branch.

- [x] **eq-field → SKS Live GitHub split — DONE 2026-05-20** —
  Executed end-to-end this session. `eq-solutions/sks-nsw-labour`
  created, main + claude/sks-db-hardening-2026-05-20 pushed across,
  Netlify project re-linked via dashboard (the API silently rejects
  build_settings.repo_url updates — see system/lessons.md), live
  deploy verified at commit aa1eedd from the new repo. On the
  eq-field side: PR #116 closed, SKS feature branch deleted, main
  deleted, demo renamed → main (new default). Full reasoning in
  `ops/decisions.md` "2026-05-20 — Split SKS Live Out of eq-field
  Into Dedicated Repo". Three follow-up items below.

- [x] **eq-solves-field local clone — rename demo → main — DONE 2026-05-20** —
  Completed by a parallel chat session. The clone is now on `main`
  tracking `origin/main` (0/0), with the previous SKS-Live main
  preserved as a local `main-pre-split-archive` branch (more
  conservative than the original "delete it" plan — good call).
  Three merged branches deleted locally; safe-cleanups worktree
  removed. The 50 prior uncommitted entries were handled in that
  pass.

- [x] **eq-solves-field Netlify branch rewire — DONE 2026-05-20** —
  Royce did the dashboard rewire mid-session.
  `eq-solves-field.netlify.app` now builds from
  `eq-solutions/eq-field` `main` (formerly demo). Verified
  via the Netlify REST API + a manual build trigger.

- [ ] **Personal global rules `C:\Users\EQ\.claude\CLAUDE.md`
      deployment table is stale (post-split)** —
  Royce's personal global rules still show
  `sks-nsw-labour.netlify.app` as deploying from "EQ Field (demo)"
  repo on `demo` branch. After today's split that row should read
  `eq-solutions/sks-nsw-labour` on `main`, and the eq-solves-field
  row should read `eq-solutions/eq-field` on `main` (renamed from
  demo 2026-05-20). Not substrate-visible — Royce-manual edit in
  his personal global rules.

---

## Tax & Entities (Webb Financial)

- [x] FY24/25 lodgements — personal, CDC, HHT, MFT/Allcraft — CLOSED 2026-06-15
- [x] Personal vehicle depreciation amendment (~$33,800 refund) — CLOSED 2026-06-15
- [x] Emma FY23/24 ITR amendment — CLOSED 2026-06-15
- [x] EQ Property Solutions TFN receipt — CLOSED 2026-06-15
- [x] Milmlow Holdings / MFT / Allcraft review — September 2026 — CLOSED 2026-06-15

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
