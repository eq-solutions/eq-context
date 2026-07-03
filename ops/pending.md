---
title: OPS Tier — Pending Actions
owner: Royce Milmlow
last_updated: 2026-07-03
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
