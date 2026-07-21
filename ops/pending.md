---
title: OPS Tier — Pending Actions
owner: Royce Milmlow
last_updated: 2026-07-21
scope: Operational support to-do list — Webb, infra, substrate
read_priority: standard
status: live
---

# OPS Tier — Pending

EQ items in `eq/pending.md`. SKS items in `sks/pending.md`. This file is
for operational support: tax, entities, infrastructure, substrate.

---

## Brief-gate flag made per-session (2026-07-21)

The `/brief` flag that unlocks `guard.js`'s brief-gate was a single global
file per day, shared by every concurrent agent on this machine. One session's
`/close` deleted it and silently re-blocked every other live session mid-work;
one session's `/brief` waived the gate for sessions that never ran one. Now
named `eq-brief-<date>-<session_id>.flag`, read from the hook's `session_id`.
Fixed in `~/.claude` (`hooks/guard.js`, `commands/brief.md`, `commands/close.md`)
— not a repo change, so there's no PR.

**Needs Royce:** nothing — but two follow-ups worth knowing:
- [ ] Verify the per-session flag across a **real concurrent pair** — only
  single-session behaviour was tested (block without flag, allow with).
  Two agents at once is the case it exists for. _(added 2026-07-21)_
- [ ] `echo '<json>' | node guard.js` returns a **false all-clear** — exits 0
  with empty stdout even when the rule should deny. Calling `evaluate()`
  directly on the same payload denies correctly. Any future gate test using
  the piped form will silently pass; worth root-causing so the hook is
  testable from the CLI. _(added 2026-07-21)_

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

Full build/fix history (7 PRs across three follow-up sessions, #94–#108,
covering both real incidents caught — a silent truncation of
`rules/non-negotiables.md`, an orphaned `ops/security-register.md` — and the
routine doc-drift fixes) is recorded in `sessions/2026-07-19.md` and
`sessions/2026-07-20.md`; not repeated here.

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

Execution history (gate bug fix, hooks wiring, F3/F4 guards, the Autonomous
Sprint cluster archive, `lessons.md` trim, and the rest of this queue's
done items) is recorded in `sessions/2026-07-12.md` and
`sessions/2026-07-12-substrate-plan-v2.md`; not repeated here.

- [~] **Product pulse — DROPPED.** Premise was the false F4 alarm. Revive only if a goal needs it.
- [ ] **Courier (P5) — PARKED**, not dropped. Manual `git checkout main && git pull` suffices.
- [ ] **Chat** — GitHub connector on + fresh session to read corrected main (hygiene).
- [ ] **P2+P3 — product pulse (lean, build-next)** — nightly workflow: ~6 live `verify: sql`
  signals (checks created/completed, non-Royce writes excl. `source='system'`, prestarts/
  toolbox/audits, active users) + goal-expiry check + morning push on zero↔nonzero flips.
  **One promotion guard kept:** an agent may not mark its own claim `verified`. **Dropped:** the
  general typed `claims.yml` system (duplicated the pulse). (2026-07-12)
- [ ] **P5 — courier install** — Beelink-native scheduled git sync, eq-context/main only
  (approved `ops/decisions.md` 2026-07-12); gate reports courier age. (2026-07-12)
- [ ] **Deferred (P4 hygiene)** — `memory-coverage.yml`; consolidate workflows 17→≤8;
  CLAUDE.md diet ≤200 lines. Not urgent; each carries refactor risk. (2026-07-12)
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

- [ ] **Orientation file `cowork-eq-context-orientation.md` updated 2026-05-13** —
  Holiday-period orientation file was stale (claimed `rules/` removed,
  44 rows, 3 unfixed bugs). Refreshed version produced this session
  describing current state: 49 rows, all 4 tier dirs + `rules/`/`sks-team/`/
  `sessions/` present, all 3 bugs resolved, TODAY.md live, VC cull closed.
  Lives outside the substrate (wherever Royce stores Cowork session
  prompts). Royce to drop in the updated copy.

- [ ] **Calendar event registered** — recurring "Review eq-context rules/* for currency" on 28 April annually, first fires 2027-04-28. Owner: Royce. Outcome logged as session entry. **(Royce manual step.)**

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

- [ ] **(A) ChatGPT and Grok bootstrap prompts** — produce `CHATGPT-PROMPT.md` and `GROK-PROMPT.md` mirroring `COWORK-PROMPT.md` / `CHAT-PROMPT.md` (paste-once-per-session prompts fetching the raw GitHub URLs — the "canonical Supabase URLs" in the original framing are gone; edge cache retired 2026-06-22). Highest-priority, lowest-risk follow-up. Closes the original framing: "consistency across all tools."
- [ ] **(B) Session-end discipline as a hard rule** — current rule says "update the substrate at session end"; lessons.md confirms the rule isn't being followed (17 of 30 stale at 2026-04-27). Revise to: every session ends with a written delta to a tier file (even "no changes today, status confirmed"), assistant refuses to close otherwise. Decision-grade change to non-negotiables.

---

## Infrastructure — Live Blockers

- [ ] **OAuth GitHub MCP connector** — consent-screen auto-login loop blocks org-picker flow for `claude.ai` chat. Cowork writes are unblocked via PATs (2026-04-19); this item only gates the chat surface. Fix: revoke prior OAuth grant at `github.com/settings/applications`, sign out, reconnect from Claude desktop. **As of 2026-07-03 this gates the connector-first Chat bootstrap (`CHAT-PROMPT.md`)** — until the connector connects cleanly, Chat has no self-serve substrate path.
- [ ] **Restart the held Chat session on the new bootstrap** — enable/verify the GitHub connector on claude.ai, then open a **fresh** chat with `CHAT-PROMPT.md` pasted (connector tools don't load mid-session). The 2026-07-03 Chat thread that was stuck on the fetch wall can be abandoned — its held "substrate fix" was this same issue, closed by PR #59. **(Royce manual step.)** _(added 2026-07-03)_
- [x] **PAT rotation — DONE 2026-06-28** — new PATs generated and deployed, old ones confirmed revoked. See `sessions/2026-06-28-brain-10-10.md` (date corrected 2026-07-21 — was misdated 2026-06-15, no session log existed for that date; 06-28 is the actual confirming log).

---

## Multi-Repo Push Automation

`.githooks/post-commit` + `scripts/install-hooks.ps1` is the current
auto-push mechanism on eq-context (install/hardening history in
`sessions/2026-05-14.md`, `sessions/2026-05-24.md`, `sessions/2026-05-30.md`).
After running `.\scripts\install-hooks.ps1` once per clone, every commit on
`main` auto-pushes to `origin/main`; branches other than `main` skip the
hook. Docs: `system/git-automation.md`.

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

The eq-field → SKS Live GitHub split (repo creation, Netlify re-link, the
eq-solves-field local-clone `demo`→`main` rename, and the eq-solves-field
Netlify branch rewire — all completed 2026-05-20) is recorded in
`sessions/2026-05-20-part-b.md`; full reasoning in `ops/decisions.md`
"2026-05-20 — Split SKS Live Out of eq-field Into Dedicated Repo".

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
