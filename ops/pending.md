---
title: OPS Tier — Pending Actions
owner: Royce Milmlow
last_updated: 2026-05-14 (Cowork — git automation)
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

---

## Cross-Tool Consistency — Original Reason for 2026-05-04 Refactor

The 2026-05-04 tier refactor solved tier-bleed and dead-product noise within Claude. It did NOT solve cross-tool consistency between Chat / Cowork / Code / ChatGPT / Grok. The substrate is now canonical for Claude only; ChatGPT and Grok still walk into every session blind. Three follow-up items, prioritised:

- [ ] **(A) ChatGPT and Grok bootstrap prompts** — produce `CHATGPT-PROMPT.md` and `GROK-PROMPT.md` mirroring `COWORK-PROMPT.md` (paste-once-per-session prompts that fetch the same canonical Supabase URLs). Highest-priority, lowest-risk follow-up. Closes the original framing: "consistency across all tools."
- [x] **(C) `TODAY.md` — current-focus surface** — landed live 2026-05-13 at `system/TODAY.md` with three Q3 outcomes defined. Wired into CLAUDE.md §1 Step 4 as universal always-load — commit `e2cf57a` 2026-05-13.
- [ ] **(B) Session-end discipline as a hard rule** — current rule says "update the substrate at session end"; lessons.md confirms the rule isn't being followed (17 of 30 stale at 2026-04-27). Revise to: every session ends with a written delta to a tier file (even "no changes today, status confirmed"), assistant refuses to close otherwise. Decision-grade change to non-negotiables.

Defer to: Beelink return (12 May+) for proper test coverage. Holiday-laptop work has higher risk of introducing new issues we can't test rigorously.

---

## Infrastructure — Live Blockers

- [ ] **OAuth GitHub MCP connector** — consent-screen auto-login loop blocks org-picker flow for `claude.ai` chat. Cowork writes are unblocked via PATs (2026-04-19); this item only gates the chat surface. Fix: revoke prior OAuth grant at `github.com/settings/applications`, sign out, reconnect from Claude desktop.
- [ ] **PAT rotation** — Milmlow + eq-solutions fine-grained PATs expire 2026-05-19. Calendar reminder set for 2026-05-16. **When rotating: also update `%USERPROFILE%\.git-credentials` on every machine that pushes (Beelink + laptop).** The post-commit hook will silently start failing the moment PATs expire.

---

## Multi-Repo Push Automation

- [x] **eq-context post-commit auto-push — INSTALLED 2026-05-14** —
  `hooks/post-commit` + `install-hooks.bat` shipped this session. After
  running `install-hooks.bat` once per clone, every commit on `main`
  auto-pushes to `origin/main`. Substrate sync follows within ~30s.
  Docs: `system/git-automation.md`. Branches other than `main` skip the
  hook; failed pushes don't undo the commit.

- [ ] **eq-solves-field push blocked on `demo` branch** —
  2026-05-14 `push-all.bat` attempted push of local `demo` to
  `Milmlow/eq-field-app:demo`, rejected as non-fast-forward (remote has
  commits we don't). §11 hard rule also says never push `demo` without
  explicit instruction. Decisions needed: (a) `git pull --rebase origin
  demo` and re-push, or (b) switch local to `main` for the SKS labour
  app surface and push there, or (c) skip until the EQ Field branch
  strategy is settled. **Royce to call.**

- [ ] **eq-solves-assets remote doesn't exist on GitHub** —
  2026-05-14 `push-all.bat` got `Repository not found` for
  `Milmlow/eq-solves-assets`. Browser-verified — Milmlow has
  `eq-field-app`, `eq-solves-service`, `eq-cards` and no
  `eq-solves-assets`. Likely either (a) the local clone is a rename of
  `eq-solves-service` and the remote URL was never updated, or (b) the
  GitHub repo was never created. **Action:** `cd C:\Projects\eq-solves-assets
  && git remote -v` to confirm the URL, then either retarget remote or
  create the GitHub repo. **Royce to call.**

- [ ] **Per-repo post-commit hooks for eq-cards, eq-solves-field,
  eq-solves-assets** — only eq-context has the auto-push hook installed.
  The other three still need manual `git push`. Replicate the pattern
  once the two blockers above are resolved. Each repo's `demo`/`main`
  branch semantics differ — hook needs per-repo branch logic.

- [ ] **Delete stale `setup-and-push.bat`** at eq-context repo root —
  created earlier this session, points at a Cowork-internal upload path
  that doesn't resolve on Windows. Superseded by `install-hooks.bat`.
  Royce to `del C:\Projects\eq-context\setup-and-push.bat`.

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
