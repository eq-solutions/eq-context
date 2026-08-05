---
title: SYSTEM — Failure Ledger (the ratchet's memory)
owner: Royce Milmlow
last_updated: 2026-08-05
scope: Every failure that escaped the safeguards, with the rung its guard currently sits at. Machine-read by guard-ratchet.yml. Append-only for entries; rung/count are mutable.
read_priority: high
status: live
---

# SYSTEM — Failure Ledger

**This is the memory of the ratchet.** Every failure that got past the safeguards is recorded here with the rung its guard sits at. When a failure **recurs**, its guard must climb.

The ratchet only tightens. It is driven by reality — a failure that actually happened — never by opinion.

## The enforcement ladder

| Rung | Form | Catches |
|---|---|---|
| **0** | unknown | nothing |
| **1** | lesson in `lessons.md` (prose) | only if the agent reads *and* recalls it at the right instant |
| **2** | session-start checklist item | usually |
| **3** | CI check | **after** the damage |
| **4** | **hook** — enforced at the point of action | **before** the damage. Prevention. |

**The rule:** `recurrences >= 2 AND rung < 4` ⇒ `guard-ratchet.yml` opens an issue proposing promotion.
**Propose-only** (Royce, 2026-07-11) — the ratchet never merges its own changes. It argues; you decide.

> **Why prose is rung 1, not rung 3.** On 2026-07-11 the truncation lesson (F2) *existed* in `lessons.md`. The assistant *read* `lessons.md` that session. It **still truncated `CLAUDE.md`.** Knowledge that requires an agent to have retained 455 lines and recall the right one at the right moment is not a safeguard. It is hope with a timestamp.

---

## Ledger

```yaml
failures:
  - id: F1
    title: Substrate read path served 8-12 day stale content, 200 OK, no error
    first_seen: 2026-07-11
    last_seen: 2026-07-19
    recurrences: 2
    rung: 4
    target_rung: 4
    guard: "hooks/session_start.py — SessionStart gate (rung 4, built 2026-07-11)"
    detected_by: "human — git reflog contradicted the fetched file"
    cost: "near-revert of the 2026-07-03 contract rewrite; two false headline findings"
    note: "The §1 fallback cannot catch this — it triggers on errors, and a stale cache hit is not an error."
    signal: "raw\\.githubusercontent.*stale|serving stale.*(no error|200 ok)|CDN.?cache.*stale"
    confirmed_in: ["sessions/2026-07-21.md"]

  - id: F2
    title: Edit/Write silently truncates long files on the C:\Projects virtiofs mount
    first_seen: 2026-05-24
    last_seen: 2026-07-11
    recurrences: 2
    rung: 4
    target_rung: 4
    guard: "hooks/pre_tool_use.py — PreToolUse block, fail-closed (rung 4, built 2026-07-11)"
    detected_by: "wc -l after the write"
    cost: "CLAUDE.md truncated 308->277 lines, §12/§13/End destroyed. Tool reported success."
    note: "PROMOTED 2026-07-11 — the ratchet's first closed loop. It demanded promotion; the hook was built; it went quiet. Prose failed twice; the hook cannot be forgotten."
    signal: "truncat(e|ed|ion|es).{0,40}(virtiofs|mount)|virtiofs.{0,40}truncat"

  - id: F3
    title: A goal nobody owned governed every session for two weeks from a read_priority critical file
    first_seen: 2026-07-11
    last_seen: 2026-07-11
    recurrences: 1
    rung: 3
    target_rung: 3
    guard: "TODAY.md GOALS UNSET + claim-expiry.yml (rung 3, built 2026-07-12) — fails CI on an unowned/undated/expired goal"
    detected_by: "human — Royce asked 'what's that deadline? why are you mentioning it?'"
    cost: "an assistant repeatedly told Royce to defer work against a phantom deadline"
    note: "Every check passed green. auto-bump-frontmatter was faithfully keeping the phantom looking fresh. Freshness != truth. claim-expiry.yml built 2026-07-12 — F3's guard climbed 1->3; a goal now cannot sit in TODAY.md undated, unowned, or past expiry without failing CI."
    signal: "phantom deadline|unowned goal|goal.{0,20}nobody owned"

  - id: F4
    title: Nothing watches the product — and the metric raised to prove it was itself over-read
    first_seen: 2026-07-11
    last_seen: 2026-07-11
    recurrences: 1
    rung: 0
    target_rung: 3
    guard: "PLANNED, NOT YET BUILT -> product signals in digest.md (rung 3), framed as TRANSITIONS not thresholds"
    detected_by: "human — an ad-hoc live SQL query; corrected 2026-07-12 by a second, due-date-aware query"
    cost: "REAL GAP: zero monitoring of any product signal. But the alarm that surfaced it — '14/16 created, 0 ever completed, the core workflow has never worked' — was OVER-READ. Verified live 2026-07-12: of 16 checks, 10 are live and ALL future-dated (earliest due 2026-08-06; 8 are RCD compliance seeds due 2027); the only past-due rows are soft-deleted; nothing has even been started. 0 completions is a young, forward-scheduled system, not a broken completion path."
    note: "The lesson doubled. (1) Nothing watched the product — still true, still rung 0. (2) The very first metric used to raise the alarm was un-verified against due-dates — the exact 'verified falsehood' the plan (residual risk #1) calls its floor. Mitigation: the pulse must watch TRANSITIONS (did the 2026-08-06 check complete WHEN DUE?), never a pre-due backlog. Real soft signals to watch instead of the completion count: prestarts stalled (30, last 07-04), safety modules at 0, 31 non-Royce writes/14d, last_login_at never written."
    signal: "over-?read.{0,20}(metric|alarm|signal)|nothing (watches|monitors) the product"

  - id: F5
    title: An ungoverned shadow memory overrode the canonical contract
    first_seen: 2026-07-11
    last_seen: 2026-07-11
    recurrences: 1
    rung: 0
    target_rung: 3
    guard: "none -> memory-coverage.yml (rung 3) + collapse shadow memories to thin pointers"
    detected_by: "human — traced backwards from F1"
    cost: "the Cowork preferences patch routed an agent to a stale URL instead of the authoritative local clone"
    note: "Seven memory layers. One governed. The CI audits the memory that was CORRECT. The patch written to prevent drift is what caused it."
    signal: "shadow memory|ungoverned memory"

  - id: F6
    title: Append (>>) NUL-fills files on the C:\Projects virtiofs mount
    first_seen: 2026-07-11
    last_seen: 2026-07-11
    recurrences: 1
    rung: 4
    target_rung: 4
    guard: "hooks/pre_tool_use.py — blocks >> to any mount path (rung 4, built 2026-07-11)"
    detected_by: "NUL-byte scan after the write — wc -l reported a SANE line count"
    cost: "3,955 NUL bytes written into system/lessons.md. Two lessons destroyed. File became binary."
    note: "Found while fixing F2 — and it INVALIDATED the F2 fix. The old lesson said 'prefer cat >> over Edit for appends'. That advice was WRONG and it corrupted the file. Only FULL REWRITE (cat >) is safe. wc -l alone will not catch this: the NUL-fill made the file LARGER. Signal regex tightened 2026-08-05 after a same-day false-positive digest hit — the bare phrase alone matched a session log merely citing 'the open F7 NUL-fill risk' as workflow rationale, not a new incident. Now requires an incident verb (corrupted/destroyed/wrote/written/found N/became binary/turned binary) near the phrase. Tested against all of that day's ~22 session logs (zero false positives before or after, except the one known case, which the new regex correctly drops) and against this entry's own cost text verbatim (still matches). Known tradeoff: no regex distinguishes 'reference' from 'incident' with perfect recall — this trades a little sensitivity for materially better precision, not a perfect fix."
    signal: "(?:corrupt(?:ed|ion)?|destroy(?:ed)?|wrote|written|found\\s+\\d|became\\s+binary|turned?\\s+(?:into\\s+)?binary).{0,60}(NUL.?(fill|byte)s?|nul-fill)|(NUL.?(fill|byte)s?|nul-fill).{0,60}(?:corrupt(?:ed|ion)?|destroy(?:ed)?|wrote|written|found\\s+\\d|became\\s+binary|turned?\\s+(?:into\\s+)?binary)"
    confirmed_in: ["sessions/2026-07-28.md", "sessions/2026-07-31.md", "sessions/2026-08-04-b.md", "sessions/2026-08-04-c.md"]

  - id: F7
    title: git merge/stash-pop round-trip NUL-fills files on the C:\Projects virtiofs mount
    first_seen: 2026-07-28
    last_seen: 2026-07-28
    recurrences: 1
    rung: 4
    target_rung: 4
    guard: "hooks/pre_tool_use.py — (1) a blanket block on git write verbs (add/commit/push/merge/stash/rebase/etc.) in-sandbox, which turned out to ALREADY exist since 2026-07-12 and already covered merge/stash — this entry's original 'guard: none' claim was wrong, corrected below; (2) tool matching widened to Bash + PowerShell (was Bash-only); (3) NEW, NOT sandbox-gated: a pre-git-verb NUL-byte scan of the working tree (git status --porcelain output) that blocks fail-closed if any modified/untracked file already has NUL bytes, on any platform, regardless of in_sandbox(). Built + tested 2026-07-31, adversarial suite 51/51 (6 new cases: 2 proving the widened PowerShell match, 4 proving the scan fires independent of the sandbox flag)."
    detected_by: "human — `file` + a byte-level scan on scripts/sites.js after a git stash pop/merge round-trip; node --check did not catch it"
    cost: "scripts/sites.js corrupted with NUL bytes mid-session; caught and fixed before commit, so no damage landed — but the corruption mechanism is real and currently invisible to every existing guard"
    note: "CORRECTED 2026-07-31: this entry originally claimed 'F6's guard has no visibility into git operations' — that was wrong. hooks/pre_tool_use.py already had a blanket block on git write verbs including merge/stash, live since 2026-07-12, which SHOULD have stopped the 2026-07-28 incident outright. The real open question — never resolved, not fixed by this build — is WHY that didn't fire: either the hook wasn't wired into whatever sandbox ran that session, or the git command reached it through a path this hook's tool-name matching didn't cover. Widening to Bash+PowerShell closes one candidate cause but doesn't prove it was THE cause — nobody can currently inspect that sandbox's actual settings.json from here. What this build DOES provide unconditionally: an independent NUL-byte integrity scan ahead of any future git verb, on any platform, that blocks before corruption (from ANY path, wired-hook-covered or not) can be committed/pushed further. Tracked as a separate open item in ops/pending.md, not closed by this entry."
    signal: "git (stash pop|merge).{0,80}NUL|NUL.{0,80}(stash pop|merge|round-trip)"
    confirmed_in: ["sessions/2026-07-28.md", "sessions/2026-07-31.md"]

  - id: F8
    title: Prose written into the frontmatter status field turned CI red on main, twice in four days
    first_seen: 2026-08-03
    last_seen: 2026-08-04
    recurrences: 2
    rung: 4
    target_rung: 4
    guard: ".githooks/pre-commit check 17.5 — blocks any governed .md whose status: is outside live|draft|archived|deprecated, or is missing the key entirely (rung 4, built 2026-08-04). Exemption list held identical to .github/workflows/frontmatter-check.yml so hook and CI cannot disagree. Adversarial battery 7/7: real defect blocked, all four valid values pass, exempt paths skipped, missing key blocked, secret guard still fires through the new delegation, fail-closed when the guard script is absent, clean file commits."
    detected_by: "CI — Frontmatter validation, i.e. only AFTER the push. Never caught before the damage."
    cost: "Frontmatter validation red on main from 092466d until 2026-08-04, so every branch cut from main inherited a failing required check. The 2026-08-03 session fixed this exact defect on two other files; the very next commit to touch a third file reintroduced it."
    note: "PROMOTED 2026-08-04 on the same day the recurrence was found. The guard existed at rung 3 the whole time and worked exactly as designed — it just cannot fire until the damage is already pushed. This is the ladder's own argument: CI catches AFTER, a hook catches BEFORE. Uncovered while building it: core.hooksPath on the Beelink clone pointed at .git/hooks (an untracked copy of scripts/pre-commit-secrets.sh), so the governed .githooks/pre-commit had never run on this machine at all — a recurrence of the 2026-05-24 core.hooksPath lesson, and the reason a style hook could not have caught this even if the check had existed. Fixed by delegating the secret guard from inside the governed hook, so pointing core.hooksPath at .githooks no longer trades a credential guard for a style guard."
    signal: "status:.{0,40}(must be one of|carried prose)|prose in the status field"
    confirmed_in: ["sessions/2026-08-04-c.md"]

  - id: F9
    title: Concurrent-session git races corrupt the shared eq-context checkout
    first_seen: 2026-07-14
    last_seen: 2026-08-05
    recurrences: 4
    rung: 4
    target_rung: 4
    guard: "hooks/pre_tool_use.py — two checks, both scoped to the ONE shared checkout by exact path (never a private/fresh clone): (1) blocks bare `git commit` with no `--` pathspec — a bare commit records the WHOLE index, not just what was just `git add`ed; (2) redirects `git rebase`/`merge`/`pull` (minus --abort/--continue/--skip, which recover an already-stuck state and must stay allowed) to an isolated clone instead. Not sandbox-gated — every occurrence happened natively on the Beelink. Rung 4, built 2026-08-04, adversarial suite 65/65 (15 new F9 cases: bare-commit block, pathspec/--amend allow, a commit message containing a literal ' -- ' proven not to false-negative, rebase/merge/pull block, --abort/--continue/--skip allow, PowerShell tool-matching, and 3 controls proving none of it fires outside the shared checkout)."
    detected_by: "human — a targeted `git add system/worktree-registry.md && git commit` visibly swept up three files staged by a concurrent session; caught via `git show --stat HEAD` before push, same session also saw a stale mid-rebase read self-resolve"
    cost: "2026-07-14: a session-log append was reset by a concurrent rebase mid-commit, had to be re-added in a follow-up commit. 2026-08-03: three distinct races in ~10 minutes — a stuck rebase, a live conflict-marker (`<<<<<<< HEAD`) committed straight to main, two non-fast-forward push rejections — plus, even after reconciling in an isolated clone, applying the fix back on the shared checkout collided with a SECOND concurrent rebase (HEAD detached, main ref left pointing at a stale commit). 2026-08-04: the sweep described above, then push rejected non-fast-forward, `git rebase` refusing to start (unrelated uncommitted files from another process already in the index), and `git stash` blocked by an unrelated environment permission classifier — resolved via a fresh isolated clone + cherry-pick. No data lost on any occurrence; real time burned untangling each one, and the pattern was accelerating (3 distinct days, escalating to twice in one session)."
    note: "The gap this ledger exists to close had itself gone uncaught here: this exact failure class recurred 3+ times across 3 weeks with NO ledger entry at all — so failure_recurrence_signals() had nothing to scan for and guard-ratchet.yml never had a `recurrences` counter to bump past 2. Two independent mechanisms got two independent, narrowly-scoped checks rather than one blanket rule: (a) index-level — bare `git commit` sweeping up a concurrent session's staged files, fixed unconditionally regardless of whether anyone remembered to check `git status` first; (b) ref-level — rebase/merge/pull mutating HEAD/index/refs across several non-atomic steps while another session touches the same working directory. Considered and rejected: a lock/coordination file (a hook-enforced lock needs reliable cleanup on abnormal session termination or it becomes a new stuck-forever failure class — this ledger already documents that exact shape of damage from imperfect guards, see the Loop of Despair) and blocking ALL git writes to the shared checkout (would break routine, currently-reliable automation — nightly cron commits, single-file pending.md ticks, session close — none of which have ever been the source of the actual damage; only rebase/merge/pull and bare commits have). eq/pending.md's 2026-08-03 entry is closed by this fix, not re-deferred a third time. KNOWN SCOPE BOUNDARY found 2026-08-05, not counted as a recurrence (the guard was never in a position to see this, same as F2/F6's documented Windows/sandbox boundary): the exact sweep mechanism (a) fixes recurred within 24 hours of shipping, this time via a `git commit` authored 'via Cowork' against this same shared checkout — outside Claude Code's own tool-call hook entirely, since Cowork emits scripts for a human to run rather than executing git itself. `pre_tool_use.py` cannot see or block that path by construction; a git-level hook can't reliably substitute — checked empirically 2026-08-05, not just reasoned (eq/pending.md has the full writeup). The literal claim is false as stated: a hook CAN tell whether pathspec/scoping syntax was used (`git commit -- <path>` builds a temp index at `.git/next-index-<pid>.lock`; a bare commit stays on the default `.git/index` — confirmed across 5 scenarios in a throwaway sandbox). But the conclusion holds anyway, for the real reason: that signal detects whether scoping was used, not whether the commit is safe — a safe bare commit and an unsafe one that sweeps a stray are indistinguishable on every hook-visible signal, because git's index has no field for which session staged which file. A git-level reject-bare-commits hook would only relocate F9(a)'s existing rule and its existing blind spot (a lazy `-- .` defeats both equally), while adding a gap F9(a) doesn't have: `core.hooksPath` activation is per-clone, manual, and was found silently drifted on THIS machine mid-investigation — a worktree-scoped override was shadowing the correct value, so F8's own hook had not actually been running here despite F8 being marked closed (fixed as a side effect). `/proc/$PPID/cmdline` and `ps -o args=` are also unavailable on this Windows/Git-Bash target. A weaker commit-msg-stage (not pre-commit — confirmed pre-commit cannot see the message even with `-m`; `COMMIT_EDITMSG` holds the previous commit's stale content at that point) WARN heuristic — flag a staged file sharing no keyword with the commit message — is real and would have caught this incident's actual shape, but isn't built: standing tunable infrastructure is a product call for Royce, proposed in eq/pending.md rather than shipped silently. No git-level hook closes this gap; the recommended fix is process, not detection — extend the existing Cowork-emits-scripts convention to also require pathspec-scoping, the same bar F9(a) already holds Claude Code to. CORRECTED 2026-08-05, same day, same investigation thread (task_94836df0): the premise both notes above share — that commit 2104668 ran outside Claude Code's own tool-call hook entirely — is wrong for THIS incident, and it IS counted as this entry's 4th recurrence, not exempted. guard.log has a matching entry down to the second (gate-outbound fired, warn mode, identical command, identical session): this was an ordinary Claude Code Bash call. The real mechanism was three compounding, fixable bugs, all fixed same day: (1) pre_tool_use.py was wired into PreToolUse only at the umbrella-root settings.json (C:/Projects/.claude/settings.json) — the identical 'guard that isn't wired' shape session_start.py hit and fixed 2026-07-12 by moving to user scope, a fix this hook never got, so a session launched inside a repo or worktree (the common case, and what 2104668's session actually was) never invoked it at all; (2) even when invoked, F7/F9 read data.cwd directly, never an in-command cd or -C — the identical blind spot guard.js's own reflection-gate rule already fixed for itself 2026-07-26; (3) found live while fixing (2): COMMIT_RE/REBASE_MERGE_PULL_RE required git and the verb separated by whitespace only, so git -C <path> commit never matched at all, independent of cwd. Fixed: user-scope wiring (matcher widened to include PowerShell too), effective_cwd(), both regexes widened to tolerate an optional -C <path> prefix. Regression cases added to both suites (70/70 python, 32/32 bash, from a clean, correctly-mount-pathed clone). This does NOT undercut the git-level-hook analysis directly above — that investigation answers a genuinely separate, still-open question (can anything backstop git that truly runs outside Claude Code's tool calls: a human terminal command, or a Cowork-emitted script run by a human) that remains real even though it wasn't what caused this specific commit. ops/pending.md's parallel F7 'still open — why didn't the guard fire' question closed by this same finding."
    signal: "(swept up|sweeping up)\\b.{0,40}(staged|concurrent session)|stuck rebase.{0,60}(shared|eq-context)|HEAD detached.{0,60}(main ref|stale commit)|conflict marker.{0,40}(committed|landed).{0,40}main|concurrent.session.{0,30}(git race|checkout collision|checkout race)"
    confirmed_in: ["sessions/2026-08-04.md", "sessions/2026-08-05.md"]

  - id: F10
    title: core.hooksPath silently resolves to the wrong location — three distinct mechanisms, one symptom
    first_seen: 2026-05-24
    last_seen: 2026-08-05
    recurrences: 3
    rung: 4
    target_rung: 4
    guard: "system/lessons.md's 2026-05-24 entry (rung 1, prose only) plus hooks/session_start.py's HOOKS check (2026-08-05: prints local/--worktree/effective scope, warns loudly on any mismatch, every session, unprompted, same mechanism F1's FRESHNESS check uses) — real signal, but print-only, didn't itself close the gap. PROMOTED to rung 4 same day, same investigation thread: hooks/pre_tool_use.py now BLOCKS an explicit `git config` SET of core.hooksPath to anything but .githooks (no-scope/--local/--worktree/--global all covered; --unset deliberately left alone — see HOOKSPATH_SET_RE's own comment, a --worktree --unset specifically can be the legitimate fix for mechanism (3) below, not a new instance of it), scoped to the ONE shared eq-context checkout via the identical is_shared_eq_context() exact-path check F9 already built and proved out. Adversarial suite: 12 new cases — all 3 real recurrence shapes reproduced and blocked (wrong directory, --worktree override, and the --global case defensively), the correct value plus a differently-spelled normalized-equivalent both proven to NEVER block, a private-clone control (F10's own escape valve, mirroring F9's), a -C-prefix and a backslash-path-separator case. 91/91 python suite, 36/36 bash, 0 regressions."
    detected_by: "none automated, all three incidental — (1) 2026-05-24: a human noticed the auto-bump-frontmatter bot fighting every push and traced it back; (2) 2026-08-04: found while building F8's own status-enum guard, not by the guard itself; (3) 2026-08-05: found by hand mid-investigation into a different question (F9's git-level-hook analysis, throwaway sandbox testing of pre-commit/commit-msg behaviour), not by any standing check."
    cost: "(1) 2026-05-24: the pre-commit date-bump hook silently skipped; the since-retired auto-bump-frontmatter.yml bot kept pushing its own correcting commits, every push needed a pull --rebase first. (2) 2026-08-04: the governed .githooks/pre-commit (secret scanning + F8's new status-enum check) had never run on the Beelink at all — a real exposure window on the secret-scanning guard specifically. (3) 2026-08-05: F8's own guard silently stopped running AGAIN, this time on the shared checkout's own main worktree, despite F8 being marked closed at rung 4 — a rung-4 guard was actually rung 0 in practice, undetected until found by hand mid-investigation into something else entirely."
    note: "Three distinct mechanisms, same symptom, same root shape (core.hooksPath resolves somewhere other than the governed .githooks): (1) 2026-05-24 — hooksPath was set to hooks/ (containing only post-commit), while the real pre-commit hook lived in .githooks/pre-commit, so .githooks was never read at all. Fixed by consolidating both hooks into .githooks and repointing. Captured only as prose in system/lessons.md — no guard, rung 1. (2) 2026-08-04 (F8) — hooksPath pointed at .git/hooks, which held an untracked but load-bearing shadow copy of scripts/pre-commit-secrets.sh, so the governed .githooks/pre-commit had never run on the Beelink at all. Found incidentally while building F8's fix; folded into F8's own note field rather than given its own id — F8's note explicitly calls it 'a recurrence of the 2026-05-24 core.hooksPath lesson.' (3) 2026-08-05 — during the F9 git-level-hook investigation, a --worktree-scope core.hooksPath override of .git/hooks was found live on the shared checkout's own main worktree, silently shadowing a correct --local value of .githooks (--worktree scope wins over --local when extensions.worktreeConfig is true). Root-caused to the F8-fix session's own worktree-repointing loop (sessions/2026-08-04.md 'Notes': repointed all 5 open worktrees' hooksPath to .githooks, checked each for live secret-scanning content, then reverted 4 of 5 back to .git/hooks since their branches predated F8's secret-guard delegation) most likely leaking a --worktree-scope command onto main by accident — main was never named as a target anywhere in that session's plan. Fixed by hand: `git config --worktree core.hooksPath .githooks`. Documented in eq/pending.md's 'Correction, 2026-08-05' note under 'eq-context: shared-checkout git races' (NOT ops/pending.md, which has no core.hooksPath mentions at all) and explicitly flagged there as 'not filed as its own ledger item here' — this entry closes that gap. Partial mitigation shipped same day as this entry: hooks/session_start.py's new HOOKS check (see guard: above) — real signal, but print-only, so target_rung 4 stayed open until something actually prevented a wrong value from taking effect. CLOSED same day, same investigation thread: hooks/pre_tool_use.py now blocks the SET itself (see guard: above for the exact mechanism and test coverage) — exactly the fix this note named as the open gap. The 4 worktrees eq/pending.md documents as deliberately still on .git/hooks (their own .githooks/pre-commit predates the secret-guard delegation, so repointing them would have removed their only secret guard until their branches catch up) are unaffected by construction, not by a special case written for them: the new guard is scoped to the ONE shared checkout by exact path, identical to F9's own is_shared_eq_context(), so a linked worktree — any of them, not just these 4 — was never in scope regardless of what its core.hooksPath happens to be set to."
    signal: "core\\.hooksPath.{0,40}(wrong|shadow|silently|drift)|hooksPath.{0,30}(worktree|shadow)|pre-commit.{0,30}(silently skip|never ran|didn't run|isn't running)"

  - id: F11
    title: A scheduled bot workflow can fail silently for days — nothing watches eq-context's own crons
    first_seen: 2026-08-01
    last_seen: 2026-08-05
    recurrences: 1
    rung: 4
    target_rung: 4
    guard: "refresh_digest.py's new scheduled_workflow_health() (discovers every .github/workflows/*.yml with a schedule: trigger at read time — never a hardcoded list, the exact drift class that caused this bug — and checks each against its own event=schedule GitHub Actions run history) feeds into digest.md's Needs You section, read unconditionally every session by hooks/session_start.py's existing NEEDS YOU parsing — the identical always-on, unprompted-every-session mechanism F1/F3/security-findings/Sentry already rely on for rung 4, not a new pipeline. Fires at >=1 consecutive scheduled-run failure (🟠), escalates to 🔴 at >=2 — deliberately lower bar than the ratchet's own recurrences>=2 promotion threshold, since 'silent for days' was the actual cost here and same-night visibility is the whole point. Pure counting logic (_scan_run_conclusions) unit tested, 8/8, wired as a pre-flight step in digest-refresh.yml (test_scheduled_workflow_health.py) — same 'test before trusting a script that writes the substrate's most-read file' posture pending-rotate.yml already holds itself to."
    detected_by: "human — Royce asked 'is all this extra eq context sessions due to the improvements we recently made?' about the fast-growing Needs You list; traced via `gh run list --workflow=pending-rotate.yml` to 4 consecutive failed nightly runs, not found by any standing check"
    cost: "eq/pending.md grew 368KB -> 500KB over 4 days of zero rotation during the highest-volume session week yet (~100 commits/day in eq-context alone) — the SAME bloat the 2026-08-01 /decide session had just fixed, un-fixed by an adjacent commit 4 minutes later in that same session (see F11's note). More broadly: 18 separate workflows currently carry a schedule: trigger (backups, restore drills, security audits, drift checks) and every one of them was equally invisible to failure — this specific incident is pending-rotate.yml, but the exposure was suite-wide."
    note: "This is not a new bug class in isolation — it's the same 2026-08-01 backlog-bloat incident recurring, caused by the very fix that closed it. Commit c5fbe4f (09:31, /decide with Royce) shipped the verify-queue split that fixed eq/pending.md's 368KB bloat. Commit b8a7bc4 (09:35, four minutes later, same session) wired the new verify-queue.md files into pending-rotate.yml's git add list — unconditionally, including ops/verify-queue.md, which is only ever created once OPS has a verify item to move and had none. `git add` on a nonexistent pathspec is fatal under bash `set -e`, so the workflow's 'Commit if changed' step died before reaching `git diff --staged --quiet`, every night, starting that same day. All 43 rotate_pending.py unit tests kept passing throughout (they test the Python engine, not the YAML step around it) and every commit carries [skip ci], so nothing in CI, digest, or a human scanning `git log` would ever see it fail. Fixed same session as this entry (see eq/pending.md and the 2026-08-05 commit fixing pending-rotate.yml's git-add loop) by only adding files that exist on disk. The guard here is deliberately broader than that one-line fix: it doesn't re-check pending-rotate.yml specifically, it watches every scheduled workflow eq-context has, because the actual lesson is 'an unattended [skip ci] cron has zero human witnesses by construction' — the next silent failure will not be this same line of YAML. KNOWN SCOPE BOUNDARY, stated plainly rather than hidden: this guard runs inside digest-refresh.yml itself; if digest-refresh.yml's own cron ever stops running entirely (as opposed to running and finding nothing), nothing here notices — digest-refresh.yml's repository_dispatch trigger on every EQ-repo push to main is the only mitigation, not a closed guarantee. Not treated as a second recurrence of this same failure — a different, harder 'who watches the watchmen' question, out of scope for this entry."
    signal: "cron.{0,40}(silently|fail(ed|ing)).{0,40}(day|days|undetected)|scheduled workflow.{0,40}fail(ed|ing).{0,40}(silent|undetected|days)|nightly (cron|workflow).{0,60}(broken|failing).{0,40}(day|days|noticed)"
    confirmed_in: ["sessions/2026-08-05-v.md"]

  - id: F12
    title: Side-clone reconciliation blind-overwrote a concurrent session's already-pushed shared-file edits
    first_seen: 2026-08-05
    last_seen: 2026-08-05
    recurrences: 1
    rung: 1
    target_rung: 4
    guard: "none built yet — prose only (this entry). Proposed: before copying any local file back into an isolated-clone reconciliation (the F9-mandated escape valve for rebase/merge/pull on the shared eq-context checkout), diff the clone's freshly-pulled content against the local copy — or against the true parent commit — and refuse a copy-back that isn't a strict superset/merge. Not built today: the real blocker is false-positive risk, not effort — reliably telling 'a correct reconciliation copy-back' apart from 'a blind overwrite' at the pre-tool-use-hook level isn't obvious, and this project's own history (guard.js's leading-slash bug, pre_tool_use.py's cwd-anchoring bug, both found the same week) shows that class of guard needs an adversarial-test-grade build, not a quick add-on."
    detected_by: "human/session self-catch — diffed the push before trusting it ('4 deletions' in what should have been a pure addition), traced against the true parent commit"
    cost: "eq/pending.md briefly lost a core.hooksPath/F10 section and a PR #1254 write-up (4-item deferred list) — both already pushed by a different concurrent session — for one push cycle on main, before being caught and restored in a follow-up commit (e20df0f). No permanent loss (full history stayed in git throughout), but it was live on main for one cycle."
    note: "Happened while reconciling eq/pending.md through an isolated side clone — the F9-mandated escape valve for rebase/merge/pull on the shared checkout, since a direct pull/rebase there is itself blocked by F9's own guard. The reconciliation step needed to copy a local edit into the clone to merge it back, but the first attempt copied the checkout's older local copy OVER the clone's freshly-pulled content instead of merging the two — silently reverting the other session's already-pushed edits for one push cycle. Caught immediately by diffing before trusting the push, not by any guard. Surfaced into this ledger via a /decide pass run on a different question entirely (whether F6/F7's 'possibly recurred' gate flag was real) — that investigation found F6/F7 were both false alarms (single historical incidents, both already at target_rung, zero NUL bytes found on a direct byte-scan of every file touched that session) but turned up this adjacent, genuinely new, not-yet-ledgered gap along the way. Deliberately not given a hook-level guard today (see guard: field) — logged first so a second occurrence has something to increment, per this file's own stated purpose (F9's note: a failure class with no ledger entry has 'nothing to scan for')."
    signal: "(cp|copy)(-| )overwr(o|i)te.{0,60}(clone|checkout)|silently revert(ed)?\\b.{0,80}(already.pushed|pushed edits|concurrent session|another session)|blind.?overwr(o|i)te.{0,40}(pending|shared|clone)"
    confirmed_in: ["sessions/2026-08-05-o.md"]
```

---

## How to add a failure

When something escapes the safeguards — **not** when it is merely annoying, but when a guard that should have caught it did not:

1. Append an entry. `recurrences: 1`, `rung:` = whatever the guard sits at **today** (be honest; prose is rung 1). `last_seen:` = the date of this occurrence (same as `first_seen` on a new entry).
2. If an `id` already exists for this failure class, **increment `recurrences`** and bump `last_seen` to today — do not add a new entry. Recurrence is the whole signal.
3. Add a `signal:` regex — a short, specific phrase pattern that would appear in a session log describing this exact failure recurring (not the general topic area; specific enough that it wouldn't match an unrelated mention). This is what `failure_recurrence_signals()` in `refresh_digest.py` scans `sessions/*.md` for.
4. Add the session file you just wrote this entry into (or bumped it from) to `confirmed_in:` (a list). The date filter alone (`file_date > last_seen`) cannot tell "a session narrating an already-confirmed recurrence" apart from "the failure happening again" — without this, the very session log that reports and closes a recurrence permanently re-triggers itself on every future digest run, since its own file date always stays after `last_seen`. Found live 2026-07-26: F1's confirmation write-up in `sessions/2026-07-21.md` was re-flagging as a "possible guard bypass" in every digest since, purely because it quotes its own signal phrase while being dated after the `last_seen` it set.
5. `guard-ratchet.yml` does the rest. It proposes; Royce disposes.

**Do not close a failure by writing a lesson.** A lesson is rung 1. If it already had a lesson and recurred, the lesson is the thing that failed.

**The recurrence-detection loop (2026-07-21).** `guard-ratchet.yml` has always proposed a rung promotion once `recurrences >= 2` — but nothing ever noticed *when* to bump that counter; a human had to happen to recognise their own past failure in a new session. `failure_recurrence_signals()` closes that gap: it scans every session log dated after a failure's `last_seen` for its `signal` regex and surfaces a candidate in digest.md — a rung-4 hit lands in **Needs you** (the guard was supposed to make this impossible; a hit anyway is a bypass), anything below rung 4 lands in the quieter **Possible recurring failures** section. It never writes to this file — confirming a real recurrence and bumping `recurrences`/`last_seen` stays a human call, same posture as the ratchet itself.
