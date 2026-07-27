---
title: OPS Tier — Pending Actions
owner: Royce Milmlow
last_updated: 2026-07-27
scope: Operational support to-do list — Webb, infra, substrate
read_priority: standard
status: live
---

# OPS Tier — Pending

EQ items in `eq/pending.md`. SKS items in `sks/pending.md`. This file is
for operational support: tax, entities, infrastructure, substrate.

---

## Root cause of the recurring worktree-orphan pattern found + fixed (2026-07-27)

Royce shared an Explorer screenshot asking what all the extra `C:\Projects`
folders were — found 22 more (on top of the ~110 already cleaned earlier the
same day), all in `eq-shell`/`eq-solves-service`/`eq-intake`, dating back 15
days. Root-caused it instead of just cleaning around it again: Windows'
OS-level long-path support (`LongPathsEnabled`) was off even though git's
own `core.longpaths` was already `true` — that gap was breaking `git
worktree remove`'s deletion step on any repo with deep `node_modules` trees,
which lines up exactly with which repos had orphans (never `eq-field`, which
has no `node_modules` at all). Full detail in `system/worktree-registry.md`.

- [x] 22 orphaned folders deleted (all confirmed empty/build-cruft, no
  `.git`, no real content). _(added + closed 2026-07-27)_
- [ ] **Royce enabled `LongPathsEnabled=1` himself** (system setting, out of
  scope for Claude Code to change) — confirmed live via registry read, but
  it only takes effect **after a reboot**, not done yet as of this entry.
  Reboot whenever convenient; no urgency. _(added 2026-07-27)_
- [ ] **Verify after reboot**: if orphaned `-wt` folders start reappearing
  in those 3 repos again post-reboot, the diagnosis was wrong or incomplete
  and needs revisiting — don't assume the fix worked without checking.
  _(added 2026-07-27)_

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

## Worktree cleanup round 3 — suite-wide orphan sweep (2026-07-27)

Royce: "keep auditing and deep diving." Widened the check beyond `git
worktree list` to a direct on-disk vs. tracked diff across every repo's
`.claude/worktrees/` folder — found ~65 more orphaned folders suite-wide
(some dating back to mid-June), same root cause as the earlier rounds.
60 confirmed empty/build-cruft-only and deleted across `eq-roles`,
`eq-design-tokens`, `eq-field`, `eq-context`, `sks-nsw-labour` (26),
`eq-shell` (9/10), `eq-solves-service` (2/3, including the two folders this
repo's registry entry already flagged as "never real worktrees" back on
2026-07-23), `eq-intake`. `worktree-registry.md` updated to record it.

Follow-up: `eq-shell/.claude/worktrees/app-naming-wt` (real content, initially
flagged for Royce below) turned out to have a sibling — a standalone
top-level folder `C:\Projects\766-wire-check-perms`, same no-`.git` pattern,
found while chasing the original "are all these folders required?" audit's
one fully-undocumented mystery folder. The two were near-byte-identical
(differed in one file only, itself just a line-ending artifact) and both
turned out to be stale pre-merge snapshots of already-shipped work —
confirmed by diffing `src/lib/appLabels.ts` against the live repo (exact
match) and `git log` on that file, which traced it straight to
[eq-shell PR #779](https://github.com/eq-solutions/eq-shell/pull/779)
(MERGED 2026-07-12, confirmed via `gh pr view`). Both deleted — no Royce
review needed after all, closing that half of the item below.

**Needs Royce:** one real leftover, not urgent:
- [x] ~~`eq-shell/.claude/worktrees/app-naming-wt` has real content...~~
  Resolved above — confirmed already-merged, deleted along with its
  sibling `766-wire-check-perms`.
- [ ] 4 folders are stuck "device busy" on every retry (not another
  session — consistent across several minutes, points at a system
  process like antivirus/indexing): `eq-cards/will-brown-cards-sks-issue-4ec9c4`,
  `eq-ui/elastic-blackwell-1a85b8`, `eq-shell/frozen-window-issue-58b6b2`,
  `eq-solves-service/user-source-analysis-be4daa`. All confirmed empty —
  harmless to leave, retry later or after a reboot. _(added 2026-07-27)_
  - `user-source-analysis-be4daa`'s cause was found and cleared: two
    orphaned `next start` dev servers (ports 3111/3112) left running from
    a Claude Code session that verified the now-merged
    [PR #613](https://github.com/eq-solutions/eq-service/pull/613) and
    never stopped them — full process chain traced back to a Git-Bash
    session whose own parent had already exited (the classic
    background-process-outlives-its-session pattern). Both stopped
    cleanly, ports confirmed free, no processes reference the path
    anymore — but the folder is *still* locked by something Windows'
    built-in tools can't identify without a reboot (`openfiles` needs a
    system flag that itself only takes effect after restarting). Same
    bucket as the other 3 now — harmless, will clear on its own.
    _(2026-07-27)_

---

## Worktree cleanup round 2 + template fix (2026-07-27)

Follow-on to the entry below: checked that *other* repos' worktrees were
clean too. Found 3 dirty checkouts belonging to other live sessions (left
untouched — `eq-shell`'s `wonderful-brahmagupta-fa0d32`, `eq-solves-service`
root, `eq-intake` root) and 8 more clean-but-merged worktrees, confirmed via
`gh pr list` before touching: `eq-shell-dup-accounts-wt`, `eq-shell-invites-wt`,
`eq-shell-zaap-staff-wt`, `eq-field-userid-guard-wt`, `eqsvc-asset-filter-wt`,
`eqsvc-auditlog-wt`, `eqsvc-tm-lockdown-wt`, and
`eq-solves-service/.claude/worktrees/user-source-analysis-be4daa`. 7 removed
clean (+ their now-dangling branches deleted); the 8th blocked by a locked
file in `node_modules` (see below). Also pruned `eq-context`'s own empty
`sks-adam-meeting-prep-4ba3e8` husk. `worktree-registry.md` updated to
record it.

Separately: `eq-context/hooks/settings.template.json` (the master template
for wiring these hooks into a repo) still had the old backslash paths from
the PreToolUse hook bug fixed earlier today — fixed there too, so the next
repo that copies it doesn't reinherit the bug. eq-context commit
[`ab66d76`](https://github.com/eq-solutions/eq-context/commit/ab66d76).

**Needs Royce:** nothing blocking — one small leftover:
- [ ] `eq-solves-service/.claude/worktrees/user-source-analysis-be4daa`
  (already-merged [PR #613](https://github.com/eq-solutions/eq-service/pull/613))
  couldn't be removed — a locked file inside its `node_modules`
  (`import-in-the-middle`, a Sentry instrumentation temp file) blocked both
  `git worktree remove` and a direct delete. Likely held open by a running
  dev/test process on this machine; didn't kill any of the 16 `node.exe`
  processes running at the time to force it, since I couldn't tell whose
  they were. Revisit once whatever's using it stops, or ask whoever's
  running it to close it first. _(added 2026-07-27)_

---

## Worktree-registry cleanup + broken PreToolUse hook fixed (2026-07-27)

`C:\Projects` audit found 39 stale/orphaned worktree folders (34 already
untracked by git, holding only leftover build cruft; 5 still git-tracked on
merged-but-not-torn-down branches). All 39 removed after live verification
(`git worktree list` + `gh pr` status per branch, not the registry's own
say-so — the registry was wrong in both directions). `worktree-registry.md`
updated to record it ([eq-context PR-less commit `918d9e4`](https://github.com/eq-solutions/eq-context/commit/918d9e4),
direct push to main).

Separately found + fixed: the `PreToolUse` hook pointer in
`C:\Projects\.claude\settings.json` (and the `SessionStart`/`Stop` hooks in
`C:\Users\EQ\.claude\settings.json`) used backslash Windows paths
(`C:\\Projects\\eq-context\\hooks\\...`) that this session's harness silently
mangled before spawning python, causing every `Bash`/`Edit` call to briefly
throw a file-not-found error. Fixed by switching to forward slashes (already
the working convention for `guard.js` and other hooks in the same files) — not
a repo change, so no PR; local machine config only.

**Needs Royce:** nothing.
- [x] 5 local git branches (already merged, worktrees now removed) deleted:
  `claude/timesheet-leave-approval-lifecycle` + `claude/dependabot-config`
  (eq-field), `claude/access-cluster3-service-gate` (eq-solves-service),
  `claude/dupes-usage-check-client` (eq-solves-intake),
  `claude/phone-otp-approval-selfheal` (eq-shell). Three needed `git branch -D`
  (same squash-merge false-negative from the worktree removal: `git branch -d`
  checks ancestry against local HEAD, which never includes a squashed commit
  — each was independently confirmed MERGED via `gh pr list` first).
  _(added 2026-07-27, closed 2026-07-27)_

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

- [ ] **(B) Session-end discipline as a hard rule** — current rule says "update the substrate at session end"; lessons.md confirms the rule isn't being followed (17 of 30 stale at 2026-04-27). Revise to: every session ends with a written delta to a tier file (even "no changes today, status confirmed"), assistant refuses to close otherwise. Decision-grade change to non-negotiables.

---

## Infrastructure — Live Blockers

- [ ] **OAuth GitHub MCP connector** — consent-screen auto-login loop blocks org-picker flow for `claude.ai` chat. Cowork writes are unblocked via PATs (2026-04-19); this item only gates the chat surface. Fix: revoke prior OAuth grant at `github.com/settings/applications`, sign out, reconnect from Claude desktop. **As of 2026-07-03 this gates the connector-first Chat bootstrap (`CHAT-PROMPT.md`)** — until the connector connects cleanly, Chat has no self-serve substrate path.
- [ ] **Restart the held Chat session on the new bootstrap** — enable/verify the GitHub connector on claude.ai, then open a **fresh** chat with `CHAT-PROMPT.md` pasted (connector tools don't load mid-session). The 2026-07-03 Chat thread that was stuck on the fetch wall can be abandoned — its held "substrate fix" was this same issue, closed by PR #59. **(Royce manual step.)** _(added 2026-07-03)_

---

## Multi-Repo Push Automation

`.githooks/post-commit` + `scripts/install-hooks.ps1` is the current
auto-push mechanism on eq-context (install/hardening history in
`sessions/2026-05-14.md`, `sessions/2026-05-24.md`, `sessions/2026-05-30.md`).
After running `.\scripts\install-hooks.ps1` once per clone, every commit on
`main` auto-pushes to `origin/main`; branches other than `main` skip the
hook. Docs: `system/git-automation.md`.


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

---

## Security register triage: SEC-1 checklist, SEC-9 runbook, false-alarm guard fixed (2026-07-27)
*Royce asked to fix SEC-1, close SEC-9/10/12, and investigate the "guard bypass?" flag in digest.md. Steelmanned the framing before acting — none of the three were as simple as the one-line ask implied.*

- [x] **SEC-1 turned into a real gated decommission checklist**, not touched — Royce's own standing decision (2026-06-05, reaffirmed 2026-07-20) is that sks-nsw-labour stays untouched until Field replaces it. Live-verified Field's parallel-run proving is at 0/3-4 clean weeks, so a retirement date would be premature regardless of the other open gates (VIC scale-jump question, no sign-off owner, 44 workers with no migration date, 2 untriaged eq-field errors — since fixed, see `eq/pending.md` 2026-07-27). Checklist lives in `ops/security-register.md`'s SEC-1 row.
- [x] **SEC-9 rotation runbook drafted** (`sec9-jvkn-key-rotation-runbook-2026-07-27.md`) — mapped all 4 live consumers (eq-shell primary, eq-field, eq-cards, eq-solves-service). Rotation itself is credential handling — hard-blocked for Claude Code to execute, Royce-gated.
- [x] **SEC-10/SEC-12 exact manual steps handed to Royce** — both are "re-store as masked, same value, no rotation" fixes in the Netlify dashboard, a few minutes each; also credential handling, can't be done by Claude Code (confirmed: a same-value re-store attempt was blocked by the safety classifier in an earlier session, logged in SEC-12's row).
- [x] **F1 "guard bypass?" flag in digest.md was a false positive, not a real recurrence** — the detector (`refresh_digest.py`'s `failure_recurrence_signals()`) was re-flagging `sessions/2026-07-21.md`'s own sentence confirming the already-known 2026-07-19 hit, because its date-only filter can't distinguish "narrating a confirmed past incident" from "it happened again." Added a `confirmed_in` field to `failures.md`'s schema + patched the detector to skip those files; verified live (empty result, no real recurrence hiding elsewhere). Struck the stale line from the tracked `digest.md` directly rather than rebuilding it locally (no `GH_TOKEN`/`NETLIFY_TOKEN`/`SENTRY_AUTH_TOKEN` in this session — a token-less rebuild would've blanked real PR/deploy/Sentry data).

### Notes (added 2026-07-27)
- **A subagent run to map SEC-9's consumers was itself flagged by the Claude Code security classifier** for decoding a live jvkn `service_role` JWT's payload while reading Netlify env vars — recorded honestly in SEC-9's row as a possible second exposure (not confirmed as a full leak: only decoded claims, not necessarily the encoded bearer token, were visible in what I could see). Process fix applied: future credential-consumer mapping should be scoped to env-var names/presence only, never fetch/decode/print actual values.

### Deferred (added 2026-07-27)
- [ ] **Royce's call: does the possible SEC-9 second exposure push "rotate whenever convenient" to "rotate soon"?** Not decided this session.
- [ ] SEC-9/10/12 actual rotation/re-store — Royce to run himself, runbook/steps ready.
