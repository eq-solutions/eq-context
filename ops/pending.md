---
title: OPS Tier — Pending Actions
owner: Royce Milmlow
last_updated: 2026-09-02
scope: Operational support to-do list — Webb, infra, substrate
read_priority: standard
status: live
---

# OPS Tier — Pending

EQ items in `eq/pending.md`. SKS items in `sks/pending.md`. This file is
for operational support: tax, entities, infrastructure, substrate.

---

## CLOSED — "Fabricated incident" claim against eq-field commit 0e7d3956 was itself wrong (2026-09-02)
*This section previously asked Royce to decide whether eq-field PR #878 had fabricated an incident in its commit message + reflection-log entry. It hadn't. The session that raised it had checked `scripts/people-required-credentials.js` for evidence — a file #878 never touched (only `roster.js`). Independently re-verified (both by a separate concurrent session and, separately again, by the original session itself): #878's account is genuine — the version collision with PR #879 and the reflection-log merge-corruption it fixed (a PR #875 bullet duplicated into the wrong section by PR #877's own rebase) both really happened. No `failures.md` decision needed. Full detail: eq-field's `docs/reflection-log.md` (2026-09-02 entries under PR #880 and PR #883), `sessions/2026-09-02.md`.*

---

## SEC-1 — Royce: "we are very close to the change over" (2026-08-21)
*Raised mid-session while confirming, unrelated to any eq-service work, that SEC-1 (the sks-nsw-labour PII leak — anon key reads `people`/`timesheets`/`leave_requests`/`audit_log`) is scoped entirely to sks-nsw-labour, not eq-service or anything else in the suite. Royce's response: ignore it, the Field changeover is close.*

**Deferred:**
- [ ] **Qualitative only — no new date given, not checked against the 4-gate decommission checklist in `ops/security-register.md`** (proving-run streak, VIC scale-jump decision, sign-off owner, the 44 unmigrated workers' own date), which showed 0/4 clear as of its last live verification 2026-07-26. Full detail appended to the SEC-1 entry there is still pending — that file needs its own `/brief` before editing (brief-gate correctly caught this session trying to touch it without one; not bypassed). Worth a fresh live re-check of all 4 gates next time someone's actually working the cutover, rather than assuming this remark alone clears them. _(added 2026-08-21)_
- [ ] Still no interim hardening on sks-nsw-labour, still decommission-at-cutover only — unchanged in kind from the existing 2026-07-20 call, just narrows the likely timeframe. _(added 2026-08-21)_

---

## SEC-1 digest de-escalation gap — `/decide` pass run, needs Royce's steer (2026-08-26)
*The 2026-08-21 "de-escalate from active nagging" call above was never mechanically wired into the digest generator — SEC-1 has fired as an identical top-line P0 across at least 4 sessions since (2026-08-23 through 2026-08-26).*

- [ ] **`eq-context/.github/scripts/refresh_digest.py`'s `security_open_critical()` (~line 565) has no way to mark a register row "open but explicitly de-escalated"** — it surfaces any Status cell starting with OPEN/STILL OPEN as a top-line 🔴, full stop; the function's own docstring already names SEC-1 as the known exemplar of this exact gap. `/decide` verdict: worth adding a dated `DE-ESCALATED (re-escalates YYYY-MM-DD)` token the parser explicitly excludes — but only if Royce wants smart suppression over the current deliberately-blunt "every open P0 always nags forever" behaviour, which may itself be an intentional safety property (same failure class as `system/failures.md` F4/F5: ungoverned state quietly overriding a governed contract). **Needs Royce's steer**: build the convention, leave it blunt on purpose, or just hand-adjust today's display. _(added 2026-08-26)_

---

## SEC-19 — sks-labour PIN credential leak: CLOSED. SEC-1 residual risk: still open, next step offered (2026-07-30)

Royce asked for "simple security upgrades that won't affect people using sks nsw labour," then set the real constraint: no login/UX changes. Investigation (live-verified, not doc-assumed) found the anon key could read `people.pin` directly — worse than SEC-1's PII framing, a live login-credential leak, not just data. `loadFromSupabase`'s bulk roster fetch shipped every worker's plaintext PIN on every session. Full writeup: `ops/security-register.md` SEC-19.

- [ ] **SEC-1 itself is unchanged** — anon key still reads all of `people`/`timesheets`/`leave_requests`/`audit_log`. Not fixable under the "no login changes" constraint without either real per-user auth (ruled out this session) or decommissioning the app (not happening — still the live system during the Field parallel-run). Real closure path is unchanged from the existing SEC-1 entry below: the proving-run clock, currently at 0 of the required 3-4 clean weeks.
- [ ] **Offered, not yet confirmed**: pull together exactly what's blocking the Field parallel-run proving run from actually starting (it's been re-started before and stalled — see `SKS-FIELD-PARALLEL-RUN-LOG.md`). This is the actual lever left on SEC-1; no further "safe" code hardening exists under current constraints.
- Incidental, unrelated finding spun off separately (not built): PIN-management modal shows stale "No PIN" status for staff whose PIN was set in a prior session — tracked in `sks/pending.md`.

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
- [ ] **P2+P3 — product pulse: 1 item left.** 6 signals live 2026-09-01: maintenance
  checks created/completed, prestarts, toolbox talks, site audits, non-`system` writes
  — all 7d, all with zero↔nonzero flip detection (not raw thresholds) — in
  `suite-state.md`'s Product Pulse section, surfaced into `digest.md`'s Needs You, plus
  the one kept promotion guard (`scripts/pulse_promotion_guard.py` — an agent/PR may not
  assert its own signal value). Checks created/completed needed a windowed RPC on
  `service.maintenance_checks` (ehow migration `maintenance_checks_pulse_rpc`,
  EXECUTE granted service_role/postgres only) — Royce approved the schema change via
  `AskUserQuestion` 2026-09-01, applied and advisor-clean same day. First live read
  (2026-09-01): 0 created, **1 completed** in the trailing 7d — the first real completed
  check this substrate has ever seen; won't itself register as a flip on its first
  appearance (no prior row to cross from), so it's recorded here instead. General typed
  `claims.yml` stays dropped (2026-07-12 — duplicated the pulse). Execution record:
  `sessions/2026-09-01.md`; full phase detail: `system/substrate-plan-v2.md` Phase 3.
  Remaining:
  1. **"Active users" signal** — not an RPC gap: `service.profiles.last_login_at` is
     0-of-5 populated because Shell SSO never writes it. Needs an eq-shell
     instrumentation fix first, not a pulse-side change.
  - **Morning push — Royce's call 2026-09-01: leave as pull for now.** `digest.md`'s
    Needs You already surfaces flips at every session start; revisit a proactive push
    once there's a real flip to react to.
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

## stale-main-gate false positive fixed: cd-regex anchor bug (2026-08-14)

`guard.js`'s `stale-main-gate` rule (blocks a direct `git commit` on
`main`/`master` when the checkout is behind its upstream) resolves which
directory a commit targets by parsing the shell command for `cd <path>` /
`git -C <path>` before falling back to the tool-reported cwd. The `cd`
detection regex (shared with `reflection-gate`) was anchored with `^` and no
`m` flag, so it only matched `cd` at the very start of the whole command
string — a multi-line command (`VAR="path"` on one line, `cd "$VAR" && git
commit` on the next) never matched at all and silently fell back to the
tool's default cwd instead of the real target. Concretely: a fully isolated,
freshly-fetched clone that was 0 commits behind got blocked with a stale "10
commits behind" reading. Fixed to match `cd` right after any command
boundary (line break, `;`, `&&`, `||`, `&`, `|`, or string start), and the
previously copy-pasted cd/-C parsing consolidated into one shared
`resolveEffCwd()` helper. Verified end-to-end against the real `evaluate()`
function with throwaway git repos. `~/.claude` commit `4bb4235`.

This is the sibling bug to the worktree-naming gap the "index-drift.yml
cron / guard.js worktree-detection" session already fixed and logged the
same day (`ed72be4`, see `sessions/2026-08-14.md` "part 13") — both in
`stale-main-gate`'s cwd-resolution, found and fixed independently within
hours of each other while the shared checkout was under the same kind of
contention documented throughout today's session log.

Also committed, separately, a pre-existing already-authorized 2026-08-06 fix
that had been sitting uncommitted in the same `~/.claude` working tree the
whole time (`brief-gate`'s eq-context exemption missing eq-context
*worktrees*, not just the bare repo — commit `4ec0363`). Not a repo change
to `eq-context`, so no PR for either — same pattern as the 2026-07-30
`guard.js selftest fixed` entry (now closed and archived).

**Also resolved this session**: the `~/.claude` push-target question that's
been open since 2026-07-30 (see `ops/pending-archive.md`) — Royce's call:
leave it local-only, no remote.

No open items.

---

## stale-main-gate + detect-fake-worktree: second cd-chain resolution bug found and fixed (2026-08-17)

The 2026-08-14 fix above (`resolveEffCwd()` matching `cd` at any command
boundary, not just string start) turned out to be half the fix. It widened
*where* a `cd` could be recognised but never addressed *which* `cd` wins when
a chain has more than one — `cmd.match()` with no `/g` flag only ever returns
the FIRST match. A real, legitimate shape produces exactly that: `cd
"<repo>" && SCRATCH="<isolated-clone-path>" && cd "$SCRATCH" && git commit
...` — cd into a named repo for context, then into an isolated scratch clone
before actually committing. `resolveEffCwd()` resolved to the first,
unrelated repo instead of the clone the commit ran in. `guard.log` showed 6
consecutive false `stale-main-gate` blocks in one session, all reporting the
first repo's own genuinely-behind count instead of the clone's (current)
state — traced from a bug report that suspected a hardcoded path (there
isn't one; `pre_tool_use.py`'s F9 checks are hardcoded by design to the one
shared checkout, a different rule entirely). Fixed to scan every `cd` in the
chain and take the last, matching `pre_tool_use.py`'s own `_CD_CHAIN_RE`
precedent for the identical shape. `~/.claude` commit `315fbc0`.

Same sweep found a second, independent copy of the bug: rule 1c
(`detect-fake-worktree`, the shell-command case) never went through the
shared `resolveEffCwd()` helper — it had its own inline `cd`/`-C` regex, with
both the "first not last" bug on `-C` AND a narrower blind spot on `cd`
(anchored only at the true start of the whole command, so it couldn't see a
`cd` chained after any earlier command at all — worse than
`resolveEffCwd()`'s pre-2026-08-14 bug). A chained `cd "<repo>" && cd
"<fake-worktree>" && git ...` was invisible to it and silently allowed.
Fixed by routing rule 1c through `resolveEffCwd()` instead of a second
hand-rolled copy. `~/.claude` commit `e272da0`.

Both fixes verified by replaying the exact failing command shapes through
old vs. fixed `guard.js` directly (old blocks falsely / misses silently,
fixed doesn't); all 14 existing self-tests (`hooks/selftest.js`) still pass.
Swept the rest of the workspace (every wired hook, every repo's
`.claude/settings.json`, every repo under `C:\Projects`) for the same bug
shape — found nothing else. Neither commit touches `eq-context`, same as the
2026-08-14 entry above — no PR.

No open items.

---

## eq-context's own effective_cwd() got the guard.js relative-cd fix too (2026-08-21)

Same bug family as the two entries directly above (2026-08-14, 2026-08-17)
— a `cd`/`-C` target used without resolving it against the real caller
cwd — but found this time in `eq-context`'s own `hooks/pre_tool_use.py`
(not `~/.claude/hooks/guard.js`), after guard.js's copy was fixed
2026-08-20: `effective_cwd()` returned a RELATIVE `cd`/`-C` target raw
instead of resolving it against `data["cwd"]`, so a relative target
silently pointed F7 (pre-existing NUL-corruption scan) and F9 (this exact
shared-checkout race guard) at the wrong directory — usually not a git
repo at all, so both checks quietly no-op instead of firing. Not a live
incident here (unlike guard.js's, which false-positived on a real
worktree) — found by inspection while porting the fix, before it caused a
miss. 3 new regression cases added to `hooks/adversarial_test.py`,
verified against pre-fix code first to confirm they actually catch the bug.
Full suite 127/127. eq-context
[PR #168](https://github.com/eq-solutions/eq-context/pull/168),
squash-merged on Royce's explicit "merge it", confirmed live on disk in the
shared checkout afterward (function body read directly, not just a name
match).

- [ ] **Fix the MSYS-path `git -C` gap in `repo_root_for()`** — found while
  verifying the fix above, NOT closed by it: `git -C /c/Projects/...`
  (MSYS-style paths) fails outright when git.exe is invoked directly via
  `subprocess.run()`, confirmed empirically. Unlike Node's `fs` calls
  (guard.js needs `normalizeMsysPath()` to translate by hand), git's own
  MSYS path translation only fires for processes launched through a
  Git-Bash-aware shell — not a plain subprocess spawn — so an MSYS-style
  absolute `cd`/`-C` target into the shared checkout still silently
  defeats F7/F9 today. Documented in `effective_cwd()`'s own docstring;
  not filed in `system/failures.md` since it's never escaped to a live
  incident. Flagged as a background task (`task_1a9f2979`), Royce started
  it running in a separate session — not yet complete as of this entry.
  _(added 2026-08-21)_

No other open items.

---

## Suite pressure-test sweep §C-G: 31 findings logged (SEC-39-69) — 4 closed live, 3 more merged, sprint-scoped (2026-08-23)

Full triage + execution runbook: [`eq/sprints/2026-08-23-security-outstanding-triage.md`](../eq/sprints/2026-08-23-security-outstanding-triage.md)
— every item live-verified there, not restated here to avoid a second copy going stale.
The sprint leads with a 3-step ordered runbook for the items below; I offered to
walk Royce through them live or verify after he runs them — declined to execute
SEC-57/61/63 myself even on a direct "complete that sprint" ask, since each has a
specific, different reason it isn't mine to complete (his private knowledge needed,
a classifier-blocked live write across 4 production sites, and repeating the exact
secret-exposure mistake flagged earlier the same session) — not just general caution.

**Needs Royce (see sprint for full detail + exact steps):**
- [ ] **SEC-57 (P1)** — GitHub App permissions, your call (tighten or accept).
- [ ] **SEC-61 (P1)** — Netlify `dev`-context leak, fix procedure known, needs your hands (classifier-blocked for Claude Code, same as every prior secret fix this session).
- [ ] **SEC-63 (P1, possibly P0)** — account-scope Netlify secret scope, needs your 2-minute dashboard check — do this one first, its answer changes SEC-61's urgency.
- [ ] **SEC-60 (P3, 4 sub-items)** — org/repo hardening gaps; some buildable on your go, some your call.

**Merged, not yet applied/dispatched live** (Supabase MCP disconnected mid-session
when these were built — reconnected right at session close, so this may now be
unblocked next session):
- [ ] **SEC-45 (P2)** — eq-cards PR #291 merged. Needs `apply_migration` to jvkn.
- [ ] **SEC-46 (P2)** — eq-shell PR #1541 merged, **not live-dry-run verified** (built from source while MCP was down) — worth a live re-check before dispatch, not just a straight dispatch.
- [ ] **SEC-47 (P2)** — already merged by a concurrent session (migration `0265`), register corrected to match. Needs dispatch.

**Resolved while sprint-scoping:** SEC-51 was NOT a live gap (flag is on, feared breakage doesn't exist in current code) — closing as doc cleanup, not a fix.
_(added 2026-08-23, corrected + sprint-scoped 2026-08-23 — earlier version of this entry incorrectly bundled SEC-60 into the Netlify leak; SEC-60 is unrelated)_

---


---


## ehow (SKS canonical) hardcoded-org_id RLS sweep: 26 tables found + closed, both waves (2026-08-23)

**Different system from the SEC-1 entry above** — that's sks-nsw-labour (`nspbmirochztcjijmcrx`, the standalone legacy app). This is `ehow` (`ehowgjardagevnrluult`, "sks-canonical" — the live SKS tenant plane behind eq-field/core.eq.solutions), a different Supabase project entirely. A separate session's own memory notes used "SEC-1" loosely for this — flagging that so it doesn't get conflated with the real SEC-1 above in a future reconciliation.

Started from the `field_*` compat-view thread (anon grant on `field_people`/`field_timesheets`/`field_leave_requests`, revoked live) which led to `field_audit_log` resolving to `public.audit_log`, whose policy turned out to be one of 11 tables sharing the same hardcoded-org_id-no-JWT-check shape (`eq-field/scripts/app-state.js`'s "Option A RLS" list: `audit_log`, `competencies`, `people_notes`, `supervisor_notes` + 7 more, all closed live). A follow-up suite-wide query (policy qual has a hardcoded UUID literal, no `auth.jwt()`/`auth.uid()` call anywhere) re-run against ehow/zaap/jvkn found **15 more** on ehow alone, never in app-state.js's list and never touched by any existing SEC-30/31/32/33 fix (those only ever covered zaap+jvkn). zaap/jvkn independently confirmed clean for the same pattern — nothing left there.

Of the second wave, 2 tables (`app_config`, `organisations`) had a confirmed live `anon` SELECT grant — the same shape as this sweep's own SEC-30/32 findings elsewhere, just on a plane nobody had checked. Verified via eq-field's own client code (not assumed) that SKS's standalone PIN gate is hardcoded dead (`auth.js _isCoreOnly()`: `TENANT.ORG_SLUG === 'sks'` forces Core-only unconditionally), so the anon path is very likely vestigial — code-level evidence, not a live click-through. The other 12 were `authenticated`-only, full CRUD, any org — business data this time (tenders, site audits, nominations, pending schedule), not just apprentice/audit records.

**Fixed and applied live, both waves, same session:**
- `eq-field/supabase/migrations/20260823_audit_apprentice_tables_jwt_tenant_gate.sql` (4 reachable tables, first wave)
- `eq-field/supabase/migrations/20260823_apprentice_tables_jwt_tenant_gate_inert.sql` (7 inert tables, first wave — closed pre-emptively, no grant existed, zero live behaviour change)
- `eq-field/supabase/migrations/20260823_ehow_second_wave_jwt_tenant_gate.sql` (all 15, second wave — Royce chose "fix all 15 now" over splitting anon from authenticated or holding)

All three AND the caller's JWT `app_metadata.tenant_id` claim onto the existing hardcoded qual — no grant changes, no schema changes. Verified live via each migration's own internal post-condition assertion (all passed).

**Needs Royce:**
- [ ] **Not registered in `ops/security-register.md` yet** — no SEC-N number assigned this session, deliberately, to avoid colliding with the concurrent SEC-38-68 sweep above (same day, still being reconciled). Needs a real number from whoever reconciles both sessions' work.
- [ ] **The click-test — real SKS login needed**, now covering 26 tables across apprentice/audit/tender/site-audit/roster screens. Structurally can't be done by Claude — needs an actual signed-in session. If the JWT `tenant_id` claim doesn't populate for some real login path, this is where it would show up.
- [ ] **`app_config`/`organisations` anon-lockout rests on a code trace, not a live click** — high confidence (SKS's PIN gate is hardcoded off), but worth a deliberate live check if certainty matters more than the code-level evidence already gathered.
- [ ] **`eq-field`'s local checkout is in detached HEAD** with an unrelated modified file and an untracked `.branch_candidates.txt`, pre-existing, not investigated — worth a glance next time someone's in that repo.
_(added 2026-08-23)_
