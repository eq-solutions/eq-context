---
title: OPS Tier — Pending Actions Archive
owner: Royce Milmlow
last_updated: 2026-07-30
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
