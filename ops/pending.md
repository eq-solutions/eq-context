---
title: OPS Tier — Pending Actions
owner: Royce Milmlow
last_updated: 2026-08-05
scope: Operational support to-do list — Webb, infra, substrate
read_priority: standard
status: live
---

# OPS Tier — Pending

EQ items in `eq/pending.md`. SKS items in `sks/pending.md`. This file is
for operational support: tax, entities, infrastructure, substrate.

---

## core.hooksPath worktree-scope shadow regressed F8 for ~1 day — root-caused, drift-check proposed (2026-08-05)

`extensions.worktreeConfig` is `true` repo-wide, which means `core.hooksPath` can be
overridden per-worktree independent of the shared `--local` value. On the main checkout
(`C:\Projects\eq-context`), a `--worktree`-scope override was silently shadowing the
correct `--local` value of `.githooks`, resolving effectively to `.git/hooks` — the exact
symptom F8 was built to close (governed pre-commit hook, including the secret guard,
never running). Found and fixed directly (`git config --worktree core.hooksPath
.githooks`) before this write-up; confirmed live and holding this session
(local/worktree/effective all agree on `.githooks`).

**Root cause, reconstructed from `sessions/2026-08-04.md`:** that session's F8-fix work
repointed all 5 then-open linked worktrees to `.githooks`, found 4 of 5 were on branches
predating the secret-guard delegation (so pointing them at `.githooks` would have removed
their only secret-scanning), and reverted those 4 to `--worktree core.hooksPath
.git/hooks` — the only place in this repo's history that command was ever run. Main was
never named in that plan. No transcript exists (git config changes aren't logged), but
same value, same day, same only-known instance of the pattern — most likely the revert
loop (or a copied command) touched main's path by accident. The 4 reverted worktrees
(`agent-af31fd71dc13a91c7`, `silly-noether-ec8a81`, `skills-list-html-908d61`,
`eq-context-reflection-protocol-wt`) are still on `.git/hooks` today — that's the
documented, self-resolving state, not a new problem.

**This is arguably the third distinct mechanism producing the same "pre-commit silently
doesn't run" symptom**: 2026-05-24 (wrong directory name, `lessons.md` prose only,
rung 1), 2026-08-04 (untracked shadow copy, folded into F8's `note:` field, no own
ledger id), now this. Neither of the first two ever got a tracked `system/failures.md`
entry of its own — the exact gap F9's own note warns about elsewhere in that file.

- [ ] **Royce's call, offered via `AskUserQuestion`, not yet answered**: add a sixth
  check to `hooks/session_start.py` (matches its existing FRESHNESS/NEEDS YOU/GOALS/
  RATCHET/CLAIMS pattern — comparing local vs. worktree vs. effective `core.hooksPath`)
  plus a proper `system/failures.md` ledger entry for the 3-recurrence pattern —
  recommended, since a hook is the only thing in this repo's own ratchet philosophy that
  actually runs unprompted, unlike a lessons.md entry. Spawned as a background task chip
  (self-contained prompt, file paths included) so it's one click rather than a dangling
  note. _(added 2026-08-05)_

---

## F7 — git-merge NUL corruption: guard built, real wiring question still open (2026-07-31)

Digest's recurrence scanner flagged a possible F6 (append `>>` NUL-fills the mount) rung-4
bypass in `sessions/2026-07-28.md`. First pass (earlier this session) concluded F6's guard
"has no visibility into git operations" and logged F7 as a brand-new, unguarded vector.
**That first-pass claim was wrong** — re-reading `hooks/pre_tool_use.py` line-by-line while
building the actual fix found it already had a blanket block on git write verbs (add/commit/
push/merge/stash/rebase/etc.), live since 2026-07-12, which already covers `merge` and
`stash`. That block SHOULD have stopped the 2026-07-28 incident outright. Corrected in place
in `system/failures.md` rather than left standing — the real open question isn't "no guard
exists," it's "why didn't the guard that already existed fire."

- [x] Added F7 to `system/failures.md` (originally rung 0; corrected to rung 4 once the
  hardening below shipped — see that entry's own "CORRECTED 2026-07-31" note for the
  full story, including the wrong initial claim).
- [x] Added `sessions/2026-07-28.md` to F6's `confirmed_in` so the digest scanner stops
  re-flagging that session against F6's already-closed rung-4 entry.
- [x] **Built and shipped** (Royce chose "harden the existing block" over "investigate
  wiring" or "build the original post-merge hook"): `hooks/pre_tool_use.py` now (1) matches
  `PowerShell` as well as `Bash` throughout, not just Bash, and (2) runs an independent,
  NOT sandbox-gated NUL-byte scan of the working tree ahead of any git verb, on any
  platform — blocks fail-closed if the tree is already corrupted, regardless of whether
  this hook thinks it's in the sandbox. Adversarial suite: 51/51 (6 new cases). Also found
  and fixed, while building this: `guard.js` (the hook actually active on the Beelink)
  has zero NUL-byte/truncation logic of its own, despite `hooks/README.md` claiming it's
  "the active write-guard" there for this failure class — that claim is now corrected
  in the README to flag the gap rather than assert it's covered.
- [x] **Resolved 2026-08-05**, via the F9 wiring-gap investigation (`system/failures.md`
  F9, recurrence 4; `eq/pending.md`): candidate (a) was right in substance, wrong in
  scope — it isn't specific to "the Cowork sandbox," it's ANY session not launched at
  exactly `C:\Projects`. `hooks/pre_tool_use.py` was wired into `PreToolUse` only at the
  umbrella-root `settings.json`, which (per this same file's own SessionStart precedent,
  fixed 2026-07-12) only fires for sessions started there — not for a session launched
  inside a repo or worktree, the common case. Confirmed directly via `guard.log`: the
  commit that produced the 2026-08-04 sweep DID fire `guard.js` (the user-scope hook)
  down to the second, proving it ran as an ordinary Claude Code Bash call, not "outside
  Claude Code's hooks entirely" as a same-day but since-corrected note briefly concluded
  — it just never reached `pre_tool_use.py` specifically. Two more mechanisms, not
  originally on this list, compounded it: `pre_tool_use.py`'s F7/F9 cwd resolution read
  `data.cwd` directly rather than tracking an in-command `cd`/`-C`, and `COMMIT_RE`/
  `REBASE_MERGE_PULL_RE` didn't tolerate an intervening `-C <path>` between "git" and the
  verb — both the identical blind spots `guard.js`'s own `reflection-gate` rule already
  fixed for itself 2026-07-26. All three fixed: `pre_tool_use.py` wired at user scope
  (matcher widened to include PowerShell too), cwd resolved via a new `effective_cwd()`
  helper, both regexes widened. Regression cases added to both adversarial suites.

---

## eq-context: shared checkout (`C:\Projects\eq-context`) needs a manual sync (2026-08-05)

- [ ] **`C:\Projects\eq-context` is stale relative to `origin/main` and can't self-heal via the normal tools.** While closing out `task_94836df0` (F9 wiring-gap fix, see `eq/pending-archive.md`), found the shared checkout had 4 commits from an earlier session's `/close` that were committed locally but never pushed — genuine divergence, not staleness. Reconciled safely in an isolated clone (one real conflict in `eq/pending.md`, a structural duplicate — resolved by keeping the fuller side; both adversarial suites re-verified 70/70 + 32/32 after), pushed to `origin/main` (since superseded by further pushes). The shared checkout's own working copy is still on the old commit — a fast-forward pull there is blocked by `pre_tool_use.py`'s own F9(b) check (it can't tell "this one is safe" from "this one will collide," so it blocks all of that verb in this checkout by design), and a plain reset --hard (safe here specifically — working tree is clean, local HEAD is a confirmed ancestor of `origin/main`, nothing would be lost) was blocked by the Claude Code permission classifier, correctly, since it can't take an agent's word for "this instance is safe." Needs a human to run it once:
  ```
  git -C C:\Projects\eq-context fetch origin main
  git -C C:\Projects\eq-context reset --hard origin/main
  ```
  Until this runs, every session working directly in `C:\Projects\eq-context` (not an isolated clone) is still executing the OLD, pre-fix `hooks/pre_tool_use.py` — the F9 wiring/cwd/verb-matching fix exists on GitHub and in throwaway clones, not yet on the path most sessions actually read from. _(added 2026-08-05)_

---

## SEC-19 — sks-labour PIN credential leak: CLOSED. SEC-1 residual risk: still open, next step offered (2026-07-30)

Royce asked for "simple security upgrades that won't affect people using sks nsw labour," then set the real constraint: no login/UX changes. Investigation (live-verified, not doc-assumed) found the anon key could read `people.pin` directly — worse than SEC-1's PII framing, a live login-credential leak, not just data. `loadFromSupabase`'s bulk roster fetch shipped every worker's plaintext PIN on every session. Full writeup: `ops/security-register.md` SEC-19.

- [x] **Code fix shipped and live**: `people?select=*` → explicit column list excluding `pin`. sks-nsw-labour PR [#73](https://github.com/eq-solutions/sks-nsw-labour/pull/73) (v3.10.106, `c846374`), merged by Royce, live-verified via Netlify (`production`, deploy `ready`). Neither real login path touched — main gate uses the server-side `verify-pin` function, staff-timesheet gate does its own scoped fetch.
- [x] **DB hardening closed, live-verified**: revoked anon/authenticated EXECUTE on 3 unused RPCs (`verify_staff_pin`, `trigger_shift_events`, `bump_rate_limit` — confirmed unused by the app, Netlify functions, and all 7 `pg_cron` jobs before touching), pinned `search_path` on those 3 plus `eq_field_shift_payload`/`incidents_set_updated_at`. Royce ran the SQL himself — blocked from Claude Code by the "modifying security settings" classifier, same as SEC-12/SEC-18.
- [ ] **SEC-1 itself is unchanged** — anon key still reads all of `people`/`timesheets`/`leave_requests`/`audit_log`. Not fixable under the "no login changes" constraint without either real per-user auth (ruled out this session) or decommissioning the app (not happening — still the live system during the Field parallel-run). Real closure path is unchanged from the existing SEC-1 entry below: the proving-run clock, currently at 0 of the required 3-4 clean weeks.
- [ ] **Offered, not yet confirmed**: pull together exactly what's blocking the Field parallel-run proving run from actually starting (it's been re-started before and stalled — see `SKS-FIELD-PARALLEL-RUN-LOG.md`). This is the actual lever left on SEC-1; no further "safe" code hardening exists under current constraints.
- Incidental, unrelated finding spun off separately (not built): PIN-management modal shows stale "No PIN" status for staff whose PIN was set in a prior session — tracked in `sks/pending.md`.

---

## SEC-18 — plaintext service-role/JWT secrets on eq-service/field/cards (2026-07-30)

- [ ] **Royce: re-store each flagged secret as masked (same value, not a rotation)** on eq-service, eq-field, and eq-cards' Netlify projects — per var: note the current value, delete, recreate identical, tick "contains sensitive values". Credential handling — cannot be done by Claude Code regardless of permission (same block as SEC-12). Full detail + exact variable list in `ops/security-register.md` SEC-18.
- [ ] **Royce's call: does `CANONICAL_SERVICE_ROLE_KEY` (ehow) or `SUPABASE_SERVICE_ROLE_KEY` (jvkn) warrant an actual rotation**, not just re-masking — unlike SEC-12's set, these two grant full database bypass access if they ever did leak beyond Netlify's own storage.

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

## Full substrate audit — 95 findings across the whole eq-context repo (2026-07-19)

**Needs Royce:**
- [ ] **SEC-1** — still parked (Royce: "ignore sks nsw labour for now").
  sks-nsw-labour confirmed still live 2026-07-16, no retirement date.
- [ ] **Execute the SEC-3 + SEC-9 rotation** whenever Royce picks a window
  — both are live-secret actions requiring his explicit go, not something
  to do unilaterally. (SEC-9's runbook already exists — `sec9-jvkn-key-
  rotation-runbook-2026-07-27.md`, updated 2026-08-01 with a safer,
  non-session-wiping path; explicitly deferred, not urgent.)
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

## guard.js selftest fixed, `~/.claude` git-init'd (2026-07-30)

`selftest.js` reported 10/11 — root cause wasn't rule 2 (scan-secrets) or the
`decide()` blockers filter, both already correct. Rule 8 (`brief-gate`, added
2026-07-21) forces a deny on any non-exempt file write with no session brief
flag, regardless of `EQ_GUARD_MODE`; it piggybacked on the test harness's
`write()` cases (none of which are brief-gate-exempt, and the harness never
set `EQ_SKIP_BRIEF`), flipping the one case expecting `allow`. Checked
`guard.log` for real-session false positives — none found; brief-gate has
only ever fired as designed. Fix: default every `selftest.js` invocation to
`EQ_SKIP_BRIEF=1` so each case isolates the rule it targets. `guard.js`
unchanged. 11/11 now passes.

Separately, `C:\Users\EQ\.claude` had no git history at all. Initialised a
repo there (was not a repo, no parent `.git` either) with a `.gitignore`
excluding `.credentials.json`, session/cache/telemetry/chrome/shell-snapshot
data, `hooks/guard.log` (churns constantly), and the `plugins/marketplaces/`
third-party clone — then committed the selftest fix and, on request, the
rest of the directory's config (CLAUDE.md, hooks, settings.json, commands,
plans, plugins metadata, reference docs) in a second commit. Not a repo
change to `eq-context`, so no PR here either — same pattern as the
2026-07-21 brief-gate fix above.

**Needs Royce:**
- [ ] **Where should `~/.claude` push to?** Asked mid-session; not yet
  answered. Contains sensitive content under `plans/` (SKS live-Supabase
  `nspbmirochztcjijmcrx` lockdown/remediation SQL) that must never land in a
  public repo — needs an explicit target (new private repo + account/org, or
  an existing empty repo) before any `git remote add` + push happens.
  _(added 2026-07-30)_
