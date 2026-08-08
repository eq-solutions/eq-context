---
title: OPS Tier — Pending Actions Archive
owner: Royce Milmlow
last_updated: 2026-08-08
scope: Done items rotated out of ops/pending.md nightly by scripts/rotate_pending.py to keep the live doc scannable. Nothing here is actionable — pure historical record (also covered in changelogs and sessions/*.md). Append-only, in rotation order.
read_priority: reference
status: archived
---

# OPS Tier — Pending (Archive)

Done items and fully-closed session write-ups rotated out of `ops/pending.md`.
If you're looking for something to action, it's not here — check `ops/pending.md`.
A "(rotated YYYY-MM-DD ...)" note on a section header means only that
section's done items live here; its open items stayed in `ops/pending.md`.

---

## index-drift CI check red on main since 2026-08-01 — orphaned doc, one-line fix (2026-08-05, rotated 2026-08-05)

Found while checking PR #128's CI: the scheduled "Index drift check" workflow had been
failing on `main` since 2026-08-01, independent of any specific PR. Cause:
`eq/documents/internal-signoff-register-sprint-2026-08-04.md` existed but was never added
to `eq/README.md`'s index.

- [x] Added the file to `eq/README.md`'s index; verified with
  `INDEX_DRIFT_STRICT=1 python scripts/index_drift.py` — all 7 tiers clean, `eq` now
  64/64 indexed. Committed `b51da2fd`.

---

## Digest F6/F7 recurrence-signal false positives — one real bug, one stale citation (2026-08-05, rotated 2026-08-05)

Both flags fired the same day: F6 ("Append (>>) NUL-fills...") and F7 ("git merge/
stash-pop round-trip NUL-fills..."). Investigated both rather than treating them as one
issue — turned out to be two different mechanisms.

**F6 — real, fixable precision bug.** Its `signal:` regex (`NUL.?(fill|byte)s?|nul-fill`)
matched a session log merely citing "the open F7 NUL-fill risk" as workflow rationale, not
a new incident. Tightened to require an incident verb (corrupted/destroyed/wrote/written/
found N/became binary/turned binary) near the phrase — tested against all ~22 of that
day's real session logs (0 false positives after, vs 1 before) and against F6's own
historical incident text verbatim (still matches). Committed `f93dcef`.

**F7 — not a precision bug, left unchanged.** The old regex matched zero times across
every session log that day; the digest's citation of `sessions/2026-08-05.md` was stale —
that file had zero "NUL" mentions at check time, so the citation reflected content from a
highly volatile, frequently-rewritten base file that had already changed by the time it
was checked. Tightening the regex the same way as F6 was tested and found to measurably
hurt recall without fixing anything real (compounds an already-narrow 80-char proximity
window). No change made.

- [x] Both investigated and resolved (F6 fixed + tested + committed; F7 investigated,
  correctly left alone). Spawned task `task_5b1d3d56` closed.

---

## Adversarial suite (F2/F7) false-failed on a clean clone — not F9, two harness bugs (2026-08-05, rotated 2026-08-05)

3 cases in both `hooks/adversarial_test.py` and `.sh` were reported failing against
origin/main, suspected to be the F9 hardening commits interacting badly with F2/F7's
sandbox simulation. Root-caused instead to two pre-existing, unrelated bugs in the test
harness itself — confirmed the F9 hypothesis is wrong by running commit `37989be`
(pre-dating today's F9 work) from a bad clone location and getting the identical 3
failures; a `/Projects`-pathed clone at origin/main passed 75/0 clean.

**Bug 1 — location-dependence.** `targets_mount()` in `hooks/pre_tool_use.py` requires a
literal `/projects/` path segment. The suite's own F2/F7 fixtures (`CLAUDE_MD`, `LESSONS`,
the F7 NUL-scan repo) are built from wherever the test file itself is checked out — so a
clean-room clone placed anywhere without that segment spuriously fails, on any commit.

**Bug 2 — a Git-Bash/MSYS quirk in `adversarial_test.sh` specifically**, found while
wiring up the fix for Bug 1: launching a native `python3.exe` from bash auto-translates
POSIX-looking env vars to Windows-style paths, but not the same-looking text inside a
JSON payload piped over stdin — so `EQ_MOUNT_ROOT` (env var) and a `$R`-based file path
(JSON text) stopped matching each other.

- [x] Added an `EQ_MOUNT_ROOT` override to `targets_mount()`/`resolve()`, mirroring the
  existing `EQ_CONTEXT` pattern for F9 — inert in every real session, set only by the two
  test files. Fixed Bug 2 by routing `$R` through `cygpath -w` once in
  `adversarial_test.sh` and using that consistently for JSON-embedded paths.
- [x] Verified 0 failures across all four combinations (good/bad location × `.py`/`.sh`):
  75/0 and 36/0 throughout, no change to real-session behavior.
- [x] **Merged**: [eq-context#128](https://github.com/eq-solutions/eq-context/pull/128) —
  squash-merged to `main` (`7ffb0d6`), branch deleted. CI: adversarial suite + health +
  honesty passed; `index-drift` failed but was independently confirmed pre-existing on
  `main` since 2026-08-01, unrelated to this change (tracked as a fresh item in
  `pending.md`).

---

## Infrastructure — Live Blockers (rotated 2026-07-27 — open items remain in pending.md)

- [x] **PAT rotation — DONE 2026-06-28** — new PATs generated and deployed, old ones confirmed revoked. See `sessions/2026-06-28-brain-10-10.md` (date corrected 2026-07-21 — was misdated 2026-06-15, no session log existed for that date; 06-28 is the actual confirming log).

---

## Tax & Entities (Webb Financial) (rotated 2026-07-27)

- [x] FY24/25 lodgements — personal, CDC, HHT, MFT/Allcraft — CLOSED 2026-06-15
- [x] Personal vehicle depreciation amendment (~$33,800 refund) — CLOSED 2026-06-15
- [x] Emma FY23/24 ITR amendment — CLOSED 2026-06-15
- [x] EQ Property Solutions TFN receipt — CLOSED 2026-06-15
- [x] Milmlow Holdings / MFT / Allcraft review — September 2026 — CLOSED 2026-06-15

---

## Multi-Repo Push Automation (rotated 2026-07-27 — open items remain in pending.md)

- [x] **eq-solves-field push blocked on `demo` branch** — **[CLOSED 2026-07-27 — moot — the 2026-05-20 eq-field/SKS-Live split renamed local demo->main and rewired Netlify; eq-field's origin is now eq-solutions/eq-field, not the old Milmlow/eq-field-app:demo remote]**
  2026-05-14 `push-all.bat` attempted push of local `demo` to
  `Milmlow/eq-field-app:demo`, rejected as non-fast-forward (remote has
  commits we don't). §11 hard rule also says never push `demo` without
  explicit instruction. Decisions needed: (a) `git pull --rebase origin
  demo` and re-push, or (b) switch local to `main` for the SKS labour
  app surface and push there, or (c) skip until the EQ Field branch
  strategy is settled. **Royce to call.**
- [x] **Personal global rules `C:\Users\EQ\.claude\CLAUDE.md` **[CLOSED 2026-07-27 — already corrected — this session's own loaded global CLAUDE.md shows the fixed table (field.eq.solutions -> eq-field -> main, sks-nsw-labour.netlify.app -> SKS NSW Labour -> main)]**
      deployment table is stale (post-split)** —
  Royce's personal global rules still show
  `sks-nsw-labour.netlify.app` as deploying from "EQ Field (demo)"
  repo on `demo` branch. After today's split that row should read
  `eq-solutions/sks-nsw-labour` on `main`, and the eq-solves-field
  row should read `eq-solutions/eq-field` on `main` (renamed from
  demo 2026-05-20). Not substrate-visible — Royce-manual edit in
  his personal global rules.

---

## Cross-Tool Consistency — Original Reason for 2026-05-04 Refactor (rotated 2026-07-27 — open items remain in pending.md)

- [x] **(A) ChatGPT and Grok bootstrap prompts** — produce `CHATGPT-PROMPT.md` and `GROK-PROMPT.md` mirroring `COWORK-PROMPT.md` / `CHAT-PROMPT.md` (paste-once-per-session prompts fetching the raw GitHub URLs — the "canonical Supabase URLs" in the original framing are gone; edge cache retired 2026-06-22). Highest-priority, lowest-risk follow-up. Closes the original framing: "consistency across all tools." **[CLOSED 2026-07-27 — both files written, root-exempt list updated in `scripts/index_drift.py`]**

---

## rls_introspection() anon-EXECUTE leak (2026-07-28, rotated 2026-07-28 — fully closed)

Two sessions independently fixed the identical live exposure via two separate
governed pipelines, ~85s apart, no conflict (both idempotent REVOKE/GRANT):
eq-shell [#1061](https://github.com/eq-solutions/eq-shell/pull/1061)
(`0219_revoke_anon_rls_introspection.sql` via `tenant-migrate.yml`) and
eq-service [#622](https://github.com/eq-solutions/eq-service/pull/622)
(`0194_revoke_rls_introspection_anon_grant.sql` via `apply-service-migrations.yml`).
Both merged and live-verified. Real cost was duplicate engineering effort
across two repos, not a live risk.

- [x] **Root-cause default-privilege gap — CLOSED 2026-07-28 (SEC-16), via a different mechanism than first attempted.** `ALTER DEFAULT PRIVILEGES ... REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC` was confirmed a no-op (see above investigation — real, reproducible, not a known Supabase event-trigger conflict). Root cause holds; the fix doesn't have to be a "default privilege" though. Shipped a `ddl_command_end` event trigger (`eq_enforce_function_privacy`) instead — re-runs the same explicit REVOKE/GRANT idiom SEC-4/13/15 already used, on every function landing in a guarded schema, immediately after creation. Verified live on all 3 planes (real test functions, not just rolled-back transactions): `anon=false`, `service_role=true`. Confirmed compatible with the existing convention of an explicit follow-up `GRANT` for a legitimate anon/authenticated RPC. eq-shell [#1070](https://github.com/eq-solutions/eq-shell/pull/1070) (tenant migration `0220`, zaap+ehow via `tenant-migrate.yml`) + [#1072](https://github.com/eq-solutions/eq-shell/pull/1072) (control-plane ledger, jvkn applied via Supabase MCP). Full detail: `ops/security-register.md` SEC-16.

---

## Chat's 3 discipline recommendations built (2026-07-30 — one follow-up remains in pending.md)

Chat rated /clothes-skill discipline 82/100 and named 3 fixes. All three landed
this session (order revised via steelman: value first, not cost first).

- [x] **SEC-10 closed** — `ANTHROPIC_API_KEY`/`RESEND_API_KEY` on sks-nsw-labour
  rotated by Royce and re-stored `is_secret:true`; `EQ_SECRET_SALT`'s `dev`-context
  plaintext leftover cleared via the Netlify MCP. Commit `ef41f55`. See
  `ops/security-register.md` SEC-10.
- [x] **DDL-without-migration Stop gate built** — `guard.js` tags every `gate-sql`
  log line with session_id+cwd; new `~/.claude/hooks/ddl_migration_gate.py` Stop
  hook flags (never blocks) a session that applied live DDL with no matching
  migration file committed or uncommitted. Tested 4 scenarios. Machine-local
  config, not git-versioned (same as `guard.js`).
- [x] **Incident-claims registry built** — `system/incident-claims.md` (claim/lock
  table) + `hooks/session_start.py` cross-references it against the digest's
  Needs You list every session, flagging possible duplicate investigation.
  Tested (fresh/stale/empty). Commit `8087b7a` — recovered from a live shared-
  checkout collision with a concurrent session via a clean throwaway clone,
  no content lost either side.
- [x] **Pre-existing `guard.js` bug found + spun off** — `selftest.js`'s inline-
  password case denies when it should warn-allow; confirmed pre-existing, not
  a regression. Background task `task_19efbbf8`, running independently.

---

## Root cause of the recurring worktree-orphan pattern found + fixed (2026-07-27) (rotated 2026-07-30 — open items remain in pending.md)

- [x] 22 orphaned folders deleted (all confirmed empty/build-cruft, no
  `.git`, no real content). _(added + closed 2026-07-27)_

---

## Worktree cleanup round 3 — suite-wide orphan sweep (2026-07-27) (rotated 2026-07-30 — open items remain in pending.md)

- [x] ~~`eq-shell/.claude/worktrees/app-naming-wt` has real content...~~
  Resolved above — confirmed already-merged, deleted along with its
  sibling `766-wire-check-perms`.

---

## Worktree-registry cleanup + broken PreToolUse hook fixed (2026-07-27) (rotated 2026-07-30)

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

## Security register triage: SEC-1 checklist, SEC-9 runbook, false-alarm guard fixed (2026-07-27) (rotated 2026-07-30, fully closed 2026-08-01)

- [x] **SEC-1 turned into a real gated decommission checklist**, not touched — Royce's own standing decision (2026-06-05, reaffirmed 2026-07-20) is that sks-nsw-labour stays untouched until Field replaces it. Live-verified Field's parallel-run proving is at 0/3-4 clean weeks, so a retirement date would be premature regardless of the other open gates (VIC scale-jump question, no sign-off owner, 44 workers with no migration date, 2 untriaged eq-field errors — since fixed, see `eq/pending.md` 2026-07-27). Checklist lives in `ops/security-register.md`'s SEC-1 row.
- [x] **SEC-9 rotation runbook drafted** (`sec9-jvkn-key-rotation-runbook-2026-07-27.md`) — mapped all 4 live consumers (eq-shell primary, eq-field, eq-cards, eq-solves-service). Rotation itself is credential handling — hard-blocked for Claude Code to execute, Royce-gated.
- [x] **SEC-10/SEC-12 exact manual steps handed to Royce** — both are "re-store as masked, same value, no rotation" fixes in the Netlify dashboard, a few minutes each; also credential handling, can't be done by Claude Code (confirmed: a same-value re-store attempt was blocked by the safety classifier in an earlier session, logged in SEC-12's row).
- [x] **F1 "guard bypass?" flag in digest.md was a false positive, not a real recurrence** — the detector (`refresh_digest.py`'s `failure_recurrence_signals()`) was re-flagging `sessions/2026-07-21.md`'s own sentence confirming the already-known 2026-07-19 hit, because its date-only filter can't distinguish "narrating a confirmed past incident" from "it happened again." Added a `confirmed_in` field to `failures.md`'s schema + patched the detector to skip those files; verified live (empty result, no real recurrence hiding elsewhere). Struck the stale line from the tracked `digest.md` directly rather than rebuilding it locally (no `GH_TOKEN`/`NETLIFY_TOKEN`/`SENTRY_AUTH_TOKEN` in this session — a token-less rebuild would've blanked real PR/deploy/Sentry data).
- [x] **Royce's call: does the possible SEC-9 second exposure push "rotate whenever convenient" to "rotate soon"? [CLOSED 2026-08-01 — no.** Reviewed a materially safer, non-disruptive rotation path found 2026-08-01 (jvkn already has newer-style keys independent of the JWT secret, so the leaked key can very likely be swapped with zero signed-out sessions, unlike the runbook's original "rotate the JWT secret" step, which would sign out every live session suite-wide). Given the fix is now near-free, Royce was offered "do it now" and explicitly chose to defer anyway — same low-real-risk calibration already applied to SEC-3 (local-machine-only exposure, never confirmed to have left that trust boundary). Stays "rotate whenever convenient." See `ops/security-register.md` SEC-9 row and `sec9-jvkn-key-rotation-runbook-2026-07-27.md`.]**

---

## F7 — git-merge NUL corruption: guard built, real wiring question still open (2026-07-31) (rotated 2026-08-05)

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

## SEC-19 — sks-labour PIN credential leak: CLOSED. SEC-1 residual risk: still open, next step offered (2026-07-30) (rotated 2026-08-05 — open items remain in pending.md)

- [x] **Code fix shipped and live**: `people?select=*` → explicit column list excluding `pin`. sks-nsw-labour PR [#73](https://github.com/eq-solutions/sks-nsw-labour/pull/73) (v3.10.106, `c846374`), merged by Royce, live-verified via Netlify (`production`, deploy `ready`). Neither real login path touched — main gate uses the server-side `verify-pin` function, staff-timesheet gate does its own scoped fetch.
- [x] **DB hardening closed, live-verified**: revoked anon/authenticated EXECUTE on 3 unused RPCs (`verify_staff_pin`, `trigger_shift_events`, `bump_rate_limit` — confirmed unused by the app, Netlify functions, and all 7 `pg_cron` jobs before touching), pinned `search_path` on those 3 plus `eq_field_shift_payload`/`incidents_set_updated_at`. Royce ran the SQL himself — blocked from Claude Code by the "modifying security settings" classifier, same as SEC-12/SEC-18.

---

## eq-context: shared checkout (`C:\Projects\eq-context`) needed a manual sync — RESOLVED (2026-08-05) (rotated 2026-08-08)

- [x] **Closed.** A later session picked this up directly: the shared checkout had drifted further by then (4 local-only "session close" commits, `git cherry origin/main HEAD` confirmed genuinely unpushed, not just under a different SHA). Reconciled in a fresh isolated clone in the scratchpad, cherry-picking each of the 4 onto current `origin/main` one at a time. Real conflicts hit on nearly every file (changelog/pending append-point clashes, session-log filename collisions) — resolved by hand, checking actual content each time rather than blindly taking one side. **Key finding: every one of the 4 commits' genuine unique content was already independently present on `origin/main`** — the same underlying sessions had their own later "redo after a lost-update race" pushes that got the content there through different commit objects first. The reconciled scratch branch ended up with **zero diff** against `origin/main` — nothing was ever actually at risk, it just took a different path there. `git cherry` kept showing the 4 as `+` throughout (patch-ID comparison, not final-content comparison — a known blind spot, not a sign of danger; confirmed via direct tree-diff instead). Also found and removed 3 genuinely-redundant session-log duplicates (`sessions/2026-08-05-k/-l/-m.md`) that the cherry-picks would have re-introduced as stale early drafts of the same sessions' own later, fuller close-outs already at `-e`/`-f`/`-h`.
- [x] **Shared checkout brought back in line with `origin/main`.** Since content-safety was verified directly (not assumed), and the working tree was confirmed clean immediately before, ran the exact fetch + `reset --hard` this item already flagged as the safe fix — this time it went through without the earlier permission-classifier block. `git status` now shows clean, up to date, zero divergence; `git cherry origin/main HEAD -v` returns empty.

---
