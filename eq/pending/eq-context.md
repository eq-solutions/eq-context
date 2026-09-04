---
title: EQ Context (substrate/tooling) — Pending Actions
owner: Royce Milmlow
last_updated: 2026-09-04
scope: EQ Context (substrate/tooling) engineering backlog, split out of eq/pending.md (2026-08-17) so a session working in this repo isn't wading through the other 8 repos' items too. Same conventions as before: "- [ ]" open, "- [x]" done (rotated out nightly by scripts/rotate_pending.py), "- [~]" in progress.
read_priority: critical
status: live
---

# EQ Context (substrate/tooling) — Pending

Split out of `eq/pending.md` (2026-08-17) — see `eq/pending.md` for why. SKS items live in `sks/pending.md`. OPS items (entities, tax, infra) in `ops/pending.md`.

---

## eq-context: the nightly digest went blind on a dead PAT — made loud and partial; "active users" pulse row wired to jvkn (2026-09-04)

*Found during the EQ Core go-live review: `digest.md` had shown `? unknown` CI, 0 open PRs and "No merges in the last 7 days" for every repo in every refresh since ~2 Sep — all three false, none flagged. The suite-state run log (run 33855557988) shows `GitHub API 401` on every cross-repo call: `EQ_CONTEXT_PAT` (set 2026-08-03; a 30-day fine-grained token) has expired or been revoked, and `refresh_digest.py`'s `gh_get()` turned every failure into "unknown" with no trace — the exact silent-degradation shape `refresh_suite_state.py`'s own 2026-08-03 comment warns about. Second time a dead token has blinded the nightly (first: 2026-07-21 → 08-03, 13 days). Shipped on branch `claude/eq-core-launch-review-99f33a` (PR opened the same day).*

**Shipped (PR):** `refresh_digest.py` records every 401/403 in `GH_AUTH_FAILURES`, warns to stderr, retries once with the runner's own `GITHUB_TOKEN` (`GH_FALLBACK_TOKEN`, enough for eq-context + the public repos), adds a 🔴 "GitHub token rejected" Needs-you item, labels CI cells "token error" instead of "unknown", and says "unavailable — token rejected" instead of "No merges in the last 7 days". `refresh_suite_state.py` gains `fetch_active_users_7d()` — a single read-only count of jvkn `shell_control.users.last_login_at >= now() − 7 days` via the Supabase Management API (`SUPABASE_ACCESS_TOKEN`, already a repo secret; same endpoint `scripts/check_shared_object_drift.py` uses) — replacing the hard-coded "Active users | blocked" row that pointed at `service.profiles.last_login_at` on ehow, a column Shell SSO never writes. Row joins `PULSE_ROWS` so flip detection covers it; `None` renders as "unavailable", never a false 0 (F4). Both workflows pass the extra env var. All 73 generator unit tests green; the fallback path was exercised live with an invalid primary token (401 recorded, fallback served the request); the jvkn path was exercised only as far as a 401 from an invalid token (the real token is CI-only).

- [ ] **Royce to regenerate `EQ_CONTEXT_PAT`** — fine-grained PAT with read access to Actions, Pull requests and Contents on eq-shell, eq-service, eq-field, eq-cards and eq-solves-intake; store as the `EQ_CONTEXT_PAT` repo secret, then `workflow_dispatch` `suite-state-refresh.yml` and `digest-refresh.yml`. Pick a longer expiry or calendar the renewal — the digest now says so loudly, but only a new token clears it. _(added 2026-09-04)_
- [ ] **Royce to create a Netlify personal access token and store it as `NETLIFY_TOKEN`** — the Deploys section of `suite-state.md`/`digest.md` has never rendered because the secret was never set. Netlify PATs are account-wide (no read-only scope), so treat it as a SEC-9-class credential: repo secret only, never a `dev`-context Netlify value. _(added 2026-09-04)_
- [ ] **First nightly run after merge verifies the two new paths** — expect the pulse row "Active users (Shell sign-ins, jvkn)" to read ~46 (the live number on 2026-09-04) and the digest's Needs-you to carry the 🔴 token item until the PAT is replaced. If the row reads "unavailable" with a `Supabase Management API 4xx` warning in the run log, the token's scope is the first thing to check. _(added 2026-09-04)_
- [ ] **`refresh_suite_state.py` still has no fallback token** — its `gh_get()` already warns loudly, but its "Open PRs" section stays empty on a dead PAT; the same `GH_FALLBACK_TOKEN` pattern would cover eq-context + the public repos. Deliberately not done this pass. _(added 2026-09-04)_

---

## eq-context: guard-flag investigation turned up 3 follow-ups, not built this pass (2026-08-30)
*Byproduct of directly investigating digest.md's 5 rung-4 "possibly recurred" flags (F1/F9/F10/F12/F14) against their actual cited session logs, rather than trusting the regex hit at face value — full writeup in `system/failures.md`'s F1/F9/F10/F12/F14 entries and eq-context PR #188.*

- [ ] **Regex-tightening for F1 and F10's false-positive shapes** — both entries' `signal` regex matches incidental mentions (a lesson correctly applied, a guard's own diagnostic firing as designed) as readily as a real incident. Identified, not built: the F6/F7 precedent for safely tightening a signal regex involved building a dedicated adversarial test run against a full day's worth of real session logs before shipping, which this pass didn't have scope for. Until tightened, both will keep re-flagging on every future digest run — expected, not a bug. _(added 2026-08-30)_
- [ ] **A real F15-shaped incident found in `sessions/2026-08-25.md`, not investigated with full rigor** — while checking an F9 flag, found a genuine bare-commit sweep on **eq-cards'** shared checkout (not eq-context's), which is F15's territory. F15's own entry already names this exact git-verb gap as a stated, deliberate scope boundary left open. Worth a pass with the same rigor this session gave F1/F9/F10/F12/F14; not attempted here. _(added 2026-08-30)_
- [ ] **Design question: should `review_clock.py`'s `generated`-file classification account for hand-maintained sub-sections?** — the exact gap F14's newest recurrence exposed: `suite-state.md` is classified `generated` (3-day freshness clock, since most of it is nightly-rebuilt tables), but its Key Decisions log is hand-appended prose the regen never re-verifies against live state — so the file passing its freshness check said nothing about whether an individual narrative claim inside it was still true. Not obviously right either way (Key Decisions does get appended/evicted by the same process, just not content-checked) — Royce's call whether it's worth a narrower guard. _(added 2026-08-30)_

---

## eq-context: Claude's hosted GitHub connector can read but not write — known open Anthropic bug, not a config issue (2026-08-24)
*Surfaced twice, a month apart, at real cost both times: a 2026-07-16 Chat session diagnosed "a GitHub connector installation gap causing session context to fail silently" and got no further (found via a 45-day chat-activity export, not the substrate); this session independently re-derived the same root cause from zero, across roughly two hours of GitHub org/OAuth/Copilot-settings investigation, before finding it was already a filed, open bug on Anthropic's own tracker.*

- [ ] **Not yet extended to EQ-tier chat work** — the same 45-day sample shows EQ-side conversations lose facts the identical way (this entry's own root-cause finding, plus the entity-linking item below, are both EQ-side examples). `chat-gateway.md` is currently SKS-scoped by design; whether it's worth an EQ equivalent is Royce's call, not decided this session. _(added 2026-08-24)_
- **Considered and explicitly declined**: self-hosting `github-mcp-server` on the Beelink with a personal PAT, which would sidestep this bug entirely (confirmed working by another user on the linked issue). Royce's call, based on the real chat-volume data above: the cadence doesn't justify the standing cost of a second internet-facing, broadly-scoped write credential — see [SEC-57](../../ops/security-register.md) for what that risk shape actually costs when it goes wrong.
- [ ] **Whether Code's GitHub MCP write-403s are the SAME bug — unconfirmed (2026-09-01)** — today, from Claude Code (not Chat), the GitHub MCP connector 403'd identically on 3 separate write calls against this repo: `create_or_update_file` (content write to `main`), `create_branch`, `create_pull_request`. Local `git push` + `gh pr create`/`gh pr merge` — a different credential path — succeeded seconds later on the same repo, same session. **This wasn't cross-checked against this existing entry before being used to spawn `task_d45603b4`** (independently checking the App installation's permission scope) — that task doesn't know this prior ~2-hour investigation or its Anthropic-tracker citation exist yet; caught only while writing this close, too late to redirect it (couldn't reliably identify which peer session it is via `ListAgents` to send a correction). Two real open questions for whoever reads `task_d45603b4`'s report: (1) is Code's connector the same GitHub App installation as Chat's hosted one (making this the already-filed, already-declined-to-route-around bug above), or a separately-scoped installation (a plain fixable permission grant, unrelated to the self-hosting cost tradeoff already declined)? (2) either way, local `git`/`gh` clearly has real write access to this repo from Claude Code — worth writing down as the working path for eq-context writes from Code, independent of how the connector question resolves. _(added 2026-09-01)_
- [ ] **Whether to harden the chat-gateway Drive-relay pattern mechanically — deliberately held, pending `task_d45603b4`** — a same-session critique found real gaps: no authentication beyond format-recognition on the patch doc itself, human approval often lands on a Code session's summary rather than the source doc, "verify before write" is a norm in a `.md` file, not a hook (unlike this repo's brief-gate/reflection-gate), no consumption marker on an applied patch. `/decide`'d: don't commit to keep/harden/retire until `task_d45603b4` reports whether the write-403 is a fixable scope grant or a genuine bug. If unfixable, the stakes-asymmetry argument favours a small hook (this mechanism's own routing table already names `ops/security-register.md`/`ops/entities.md` as future targets, not just document templates); if fixable, Chat may be able to write directly, changing the shape of the question entirely. _(added 2026-09-01)_

---

## eq-context: a substrate architecture upgrade was scoped in Chat and is now nowhere — needs recovery from the original conversation (2026-08-24)
*Found via the same 45-day Claude Chat activity export: a 2026-07-26 conversation "compared the substrate architecture against an external productivity framework and scoped a lightweight entity-linking upgrade." Checked this repo directly — no trace anywhere (only a false-positive substring hit on the unrelated term "identity-linking" in a session log). Whatever was actually scoped never reached a pending file, a session log, or a decision record.*

- [ ] **Recover the actual scope from the original 2026-07-26 conversation** — this entry can't say what "entity-linking upgrade" means beyond the one-line description above; writing more than that here would be inventing detail that was never verified. Royce would need to pull the original conversation (or ask Chat to re-summarise it) before this is buildable. _(added 2026-08-24)_

---

## eq-context: concurrent Claude sessions repeatedly duplicating work on the same digest items — pattern, not a one-off (2026-08-23)
*One session worked digest.md's "Needs you" security findings top-to-bottom (SEC-41/42/45/46/47/50), spawning 3 sub-agents plus 3 more follow-on chips along the way. Five separate times across that one sitting, a DIFFERENT concurrent session had already independently picked up and fixed the exact same finding: SEC-41/42's dispatch, SEC-45 (PR #291), SEC-46 (PR #1541), SEC-50 (PR #803). Every instance was caught by live re-verification before anything got duplicated or clobbered — no harm done — but it's real wasted session time, repeatedly, on the same short list of P1 findings every session reads at start.*

- [ ] **Consider a claim mechanism for digest-surfaced findings** — `system/TODAY.md`'s `CLAIMS` block already exists as a concept (empty tonight: `claims: []`) but doesn't appear to be used for this. A session picking up a "Needs you" security finding could stake a short-lived claim there before starting, so a second session reads "already claimed" instead of independently re-deriving the same fix. Needs Royce's call on whether this is worth the mechanism, given the actual cost tonight was low (idempotent migrations, nothing broke) — this is a real pattern, not an emergency. _(added 2026-08-23)_

---

## eq-context: ~80 leftover scratch clones found across other sessions' temp folders — found, scope-checked with Royce, left alone (2026-08-21)
*Asked to delete "the leftover eq-context scratch clones" left behind by an eq-solves-service session's own workaround for the shared-checkout guards (clone eq-context into a session's own scratchpad, commit and push from there instead of the shared root checkout). That session's own two clones were already gone — cleaned up immediately after each push. A broader search turned up roughly 80 more of the same pattern, scattered across other sessions' scratchpad folders (eq-shell, eq-field, eq-cards, eq-intake, eq-solves-service, and eq-context itself) — the same guard-workaround being independently rediscovered and repeated session after session, with nobody cleaning up afterward.*

- [x] **Sweep run 2026-09-04: 112 of 119 deleted, 6 left for individual review.** Re-verified fresh immediately before deleting (not reused from the count-only check above) — each was `git status --porcelain` clean AND had zero commits ahead of its upstream at delete time. This session's own then-active clone was excluded regardless of status. Local disk cleanup only: every deleted clone was already fully pushed, so nothing exists only in a deleted copy — restorable by re-cloning `origin/main` any time. 6 left untouched pending individual review (see below). _(added 2026-09-04)_
- [x] **The 6 reviewed individually — none held unique at-risk work; all 6 deleted, sweep fully closed.** Correcting the characterization above: `eq-context-reg2`'s 3 uncommitted files and `eq-context-close`'s 1 "ahead" commit (misread at first as 4 — that was actually 4 *behind*, 0 ahead, from a `rev-list --left-right` sign confusion) were both independent write-ups of the *same* PR #1712 (Pending-invites tab) session close, already merged and already pushed to `origin/main` via a different session's clone that won the race — confirmed by grepping the live content before deleting either. Neither was unique. `eq-context-close-wt` had no real changes at all, just one empty untracked folder. **New finding, worth keeping:** the other 3 (`eq-context-fresh`, `eq-context-sprint-update`, `eq-context-sprint`) each had their *entire* working tree deleted — 400+ tracked files gone from disk, `.git` itself untouched — within a 54-second window, all three sharing the same 5-day-stale last-commit date (2026-08-30) while the fresher three were unaffected. Nothing was lost (`.git` intact, nothing ever committed reflecting the deletion, fully `git restore`-able), and this wasn't any session/agent action — the pattern (age-correlated, `.git`-preserving, OS-Temp-scoped) points to Windows' own Temp-folder housekeeping (Storage Sense or a scheduled cleanup) rather than anything in this repo's own tooling. So leftover clones don't just accumulate disk debris — left long enough, the OS quietly guts their working copy too (harmlessly, but it's a second, previously-undocumented failure shape). **Also found**: mid-sweep, 5 more brand-new eq-context scratch clones had already appeared under entirely different, unrelated session IDs — direct, same-day confirmation that this is a continuously-regenerating pattern, not a fixed backlog any one-time sweep clears for good. _(added 2026-09-04)_
- [x] **Built: the periodic sweep now exists.** `C:\Users\EQ\.claude\scripts\eq-context-scratch-janitor.ps1` (committed locally in the `~/.claude` config repo, not pushed — that repo has unrelated pre-existing dirty state, left untouched) runs the exact same check-then-delete logic proven above: skip anything touched in the last hour (dodges a live commit/push race), then skip anything dirty or with no configured upstream, then skip anything with unpushed commits, delete everything left. Registered as the Windows Scheduled Task "EQ Context Scratch-Clone Janitor," daily at 3am. First real run (manual, immediately after building): found 6, deleted 2, correctly left 4 alone as too-fresh-to-touch. Logs to `~/.claude/logs/eq-context-scratch-janitor.log`. Deliberately does NOT auto-write to this pending file or attempt any eq-context git write of its own — it only ever touches files under the local Temp folder, never this repo's tracked content. `/decide`'d 2026-09-04: check-then-delete over blunt age-only reaping, since the safer version was already built and proven at zero extra cost, not a hypothetical trade. _(added 2026-09-04)_

---

## Substrate: a wrong note said Shell changes don't go live when you merge — corrected everywhere (2026-08-15)
*A "waiting on you" item claimed a finished piece of Staff-list work was merged but not published, and that you needed to trigger the publish yourself. That was wrong — Shell publishes automatically the moment a change is merged, about two seconds later. The note had spread from the to-do list into the daily digest, which every session reads on startup.*

- [ ] **That automated guard is not built — deliberately.** A check that scans wording across 600+ open items and every session log could easily misfire, and a false alarm on this repo blocks every session from saving work. Wants a proper test pass against the real files first, not a quick add. _(added 2026-08-15)_
- [ ] **A safety guard is misfiring three different ways and pushing sessions toward workarounds.** The rule meant to block risky git operations in the shared folder also blocks them in a fresh isolated copy where they're completely safe — it checks the wrong location — and it then blocked a session-log write purely because the log *text* quoted the command while describing this very problem. A guard that blocks you for writing about it can't be reported from inside a session. Cost three blocked attempts and two workarounds today. The same bug class was noted about a sibling guard on 2026-08-14 and never fixed. _(added 2026-08-15)_

---

## eq-context: `/close` skill's own archive-rule text is stale (2026-08-08)

- [ ] **`/close`'s Step 2 says to manually move a fully-closed pending.md section to `pending-archive.md`** — but that file's own frontmatter states done items have been rotated out automatically, per-item, nightly by `scripts/rotate_pending.py` since 2026-07-27 (confirmed live: the script + its CI workflow `pending-rotate.yml` both exist, with their own test suite). Found while closing a fully-ticked eq-field section this session — didn't manually archive it, to avoid duplicating/conflicting with the automation. The skill's own text should point at the script instead of describing the pre-automation manual process. _(added 2026-08-08)_

---

## eq-context: production-readiness review + 3 backup-workflow reliability fixes, ledger loop closed (2026-08-06)
*Royce asked for a warts-and-all review across onboarding/licences/security/backup/code-integrity/UX, then a follow-up sprint of whatever was safe to fix solo while he's overseas — substrate-only, no live-app merges.*

**Corrections to this session's own earlier claims, logged so they don't get quoted as fact later:**
- **EQ-SHELL-1A was NOT "just a network blip, no action needed"** — that was my own under-verified conclusion, based on checking one event's timestamp against ehow's logs without checking the occurrence count (46, escalating) or prior history. A different concurrent session (see [sessions/2026-08-06.md](../../sessions/2026-08-06.md), "two hotfixes, then a durable fix") found the real pattern (multi-browser, hotspot-only-worked), root-caused it to the legacy direct-to-Supabase browser path, and shipped a real proxy fix, confirmed live with Royce ("success — Simon is unblocked"). My single-event check was factually accurate as far as it went (that one request never reached ehow) but the conclusion I drew from it was wrong. Nothing further needed from me here — already fixed by other work, just not for the reason I said.
- **The "44 never-invited workers" I flagged as a fresh action item is the same item already logged 2026-08-02** (`§eq-cards: workers can now self-report...` below) — Royce already looked at this and said "leave this alone for now." Not a new finding; presented incorrectly as one.

---

## eq-context: `jwt-contract-drift.yml` canary fixed — eq-shell not yet migrated to `@eq-solutions/contracts` (2026-08-06)

**Deferred:**
- [ ] **eq-shell's own migration to `@eq-solutions/contracts`** (replacing its local `SupabaseJwtClaims` with the shared `ShellHandoffClaims` type) — the canary's originally-envisioned "durable fix" endpoint. `/decide`d 2026-08-06: not worth doing as a drive-by — touches live auth-minting code, gated behind explicit chat review before deploy per CLAUDE.md's hard rule. Do as its own deliberately-scoped, reviewed piece of work next time eq-shell's JWT code is touched, not bundled into an unrelated fix. _(added 2026-08-06)_
- [ ] **Version-pin skew between eq-shell's and eq-service's independent `@eq-solutions/contracts` pins has no guard.** No live risk today — both pin the identical tag. `/decide`d 2026-08-06: not worth building yet — it would guard a risk that can't occur until the migration above ships; add it in the same pass as that migration, not before. _(added 2026-08-06)_

---

## eq-context: agentic-coding rules landed — follow-ups the rules themselves opened (2026-08-04)

- [ ] **`C:\Projects\CLAUDE.md` is still the only home for Rule 0, Rule 0.5 and the load-bearing-facts list.** Rule 0.6 and the effort threshold were moved into governed substrate; the rest wasn't. That file isn't version-controlled, has no CI, and is only read by a session started in that folder. Same shadow-memory class as failure F5. _(added 2026-08-04)_
- [ ] **Deleting the shadowed `.git/hooks/pre-commit` is held, not done.** Repointing every worktree's `core.hooksPath` to `.githooks` was tried and reverted for 4 of 5 open worktrees (`agent-af31fd71dc13a91c7`, `silly-noether-ec8a81`, `skills-list-html-908d61`, `eq-context-reflection-protocol-wt`) — their branches predate today's secret-guard delegation, so their own `.githooks/pre-commit` has zero secret-scanning in it. Repointing them would have silently removed their only secret guard, so they're back on `.git/hooks` until their branches merge or rebase past `main` (`1059f85`). Safe to repoint + delete at that point, not before. _(added 2026-08-04)_

---

## eq-context: added eq/progress/ substrate for year-end EQ tracking (2026-08-03)
*A prompt drafted by Grok, handed to this session to build a lightweight tracking layer for the 2026 year-end EQ evaluation.*

**Deferred:**
- [ ] **`eq/progress/` is unproven** — `current.md`/`customers.md` depend on manual discipline with no CI gate (unlike `TODAY.md`'s `claim-expiry.yml`). Worth checking in a few weeks whether it's actually being kept up or going quiet. _(added 2026-08-03)_

---

## eq-context: ACCESS-MODEL-PLAN.md Phase 3 fix actually landed — the 2026-07-27 close's claim was premature (2026-07-28)
*The 2026-07-27 session close logged this doc as already corrected, but `git log` on the file itself showed no such commit ever landed — the edit was lost somewhere, not just stale. Re-verified the underlying claim against eq-shell's live git history (PRs #1016/#1021/#1022, all merged 2026-07-26) before re-doing the edit, per Rule 0.5.*

**Deferred:**
- [ ] **SEC-9 rotation runbook** — no runbook exists yet for rotating the jvkn (eq-canonical) service_role key exposed 2026-07-12 in a chat transcript; offered to draft one (docs only, no keys touched) but session closed before Royce answered. _(added 2026-07-28)_

---

## eq-context: Reflection Protocol built + EQ Field commits mechanically gated (2026-07-24)
*Royce dictated a mandatory pre-finalization self-critique (4 checks: substrate conflict, vagueness, domain pushback, EQ Field scope) for EQ Field build decisions, SKS ops/commissioning docs, and any output read outside the session. Persisted as `rules/reflection-protocol.md` (PR [#118](https://github.com/eq-solutions/eq-context/pull/118)). Steelmanned before building: a first design (block every `Edit` under `/eq-field/`) was rejected as the wrong moment — it fires on trivial edits and can't see the chat discussion where the actual decision gets made. Redesigned to gate at `git commit` instead, paired with a durable, PR-visible log.*
- [ ] **Follow-up: `guard.js` itself is unversioned and untested.** It lives at `~/.claude/hooks/guard.js`, outside any git repo, with zero test coverage (beyond the ad hoc verification above) — unlike `hooks/*.py` in this repo, which are governed/versioned/CI-checked (`hooks/README.md`). Its own header cites a spec file (`system/operating-model-roadmap.md`) that doesn't exist. Worth eventually mirroring guard.js into this repo (versioned source of truth, deployed copy on the Beelink) so it gets the same test-before-trust discipline as the Python hooks. Not fixed this session — separate, larger scope. _(added 2026-07-24)_

---

Fully-closed write-ups get moved to `eq/pending-archive.md` to keep this
file scannable (trimmed 2026-07-24, 568KB → 298KB) — check there for
history, not here. When closing a section here, either archive it wholesale
(if every item is done) or trim it to just the still-open line(s) — don't
let a done item's full explanation sit here forever, that's what the
changelog and session logs are for.

---

## eq-context substrate — closed 4 of the 5 deferred items from last close, then chased the digest CI-status gap into an unresolved GitHub PAT approval issue (2026-07-21)
*Continuation of last close's deferred list: digest.md's CI-status blind spots, the pre-existing drift trio, and the unmerged product changelogs.*
- [ ] **`EQ_CONTEXT_PAT` still can't read Actions runs on eq-shell/eq-service/eq-field/eq-cards for the automated nightly/on-merge digest refresh.** Spent a long back-and-forth on this: confirmed it's a fine-grained token, walked through adding the 4 repos + Actions/Contents permissions, clicked Update — API still returns `403 "Resource not accessible by personal access token"` on all 3 repos added this session (eq-context, added at token creation, works fine). Most likely an org-approval step never completed, but not confirmed. **Royce's call: leave it** — not worth more time right now. Stopgap in place: I can run `refresh_digest.py` locally with my own working GitHub access any time current numbers are needed (did this once today — all 5 repos show real CI status as of this session). _(added 2026-07-21)_
- [ ] **Root-caused the eq-cards notify-substrate failure — a different, unrelated secret to everything else this session.** It's the ORG-level `EQ_CONTEXT_PAT` (visibility: selected → eq-cards/eq-field/eq-service/eq-shell, created 2026-06-28 "notify-substrate use only") — separate from the repo-level `EQ_CONTEXT_PAT` on eq-context fixed earlier today. Confirmed via live log: `Authorization: Bearer ` is genuinely empty, not a permissions error — the org secret has never had a value set. **Needs you**: `github.com/organizations/eq-solutions/settings/secrets/actions` → `EQ_CONTEXT_PAT` → paste a value (any PAT with write access to eq-context works) → Save. Not a build gate, but substrate is missing merge notifications from eq-cards/eq-field/eq-service/eq-shell until it's set. _(added 2026-07-21, root-caused 2026-07-21)_
- [ ] **Re-checked digest CI-status automation — confirmed still blocked, no change since the "leave it" call.** Re-ran the refresh; same "? unknown" result for all 4 repos via the automated path. Manual refresh (`refresh_digest.py` run locally) remains the working stopgap. _(added 2026-07-21)_

## eq-context — pending.md dedup pass: 865 → 372 done items, cross-checked against every product changelog (2026-07-20)
*digest.md's Queue health signal flagged this file as bloated with 865 unrotated "done" items. Investigation found the real problem wasn't missing rotation — most of that history already existed in the product changelogs, just never trimmed here after. A 5-agent pass (one per product) checked every done item against its matching changelog before deleting anything.*
- [ ] **~250 bullets across the 5 products were deliberately left in this file** — ambiguous product ownership, investigation-only findings with no shipped fix, or genuinely cross-cutting content. Not a backlog in the usual sense; full per-product breakdown is in today's session log. _(added 2026-07-20)_

---

## ⏩ Session close — 2026-07-04 (platform DR / backups, issue #60) — ehow offsite backup moved into eq-context; three real defects fixed; Phase 2 + arming deferred

*Own disaster recovery at the platform level: move the shared canonical DB (ehow) offsite backup out of a consuming app (eq-service) and into eq-context. Verified live against Supabase before building.*

**Completed (merged to `main`, `ca9ae0c`):**

**Deferred:**
- [ ] **Retire `eq-service/.github/workflows/backup.yml`** — separate eq-service PR, only after the eq-context job runs green once (avoid double-backup). _(added 2026-07-04)_
- [ ] **Repoint eq-service `SUPABASE_DB_URL`** (env `production-ops`) urjh→ehow if keeping the old job alive during cutover — Royce owns the secret; moot once eq-context is green. _(added 2026-07-04)_
- [ ] **Run the first restore drill** per `system/runbooks/supabase-restore-drill.md`; record achieved RTO/RPO in the drill log. _(added 2026-07-04)_

**Notes (load-bearing, verified live 2026-07-04):**
- Org `sqjyblkiqonyrdobaucn` has **5** live Supabase projects, not 6 — issue #60's list included `vjvamvfpbwcqfudousmg` ("EQ Context"), which is **gone**. Treat that line as stale.
- **eq-canonical (`jvknxcmbtrfnxfrwfimn`) is a live identity/control plane** — 50 `auth.users`, `shell_control` tenants/memberships, 2454 token-mint audit rows, 213 storage objects, 6 buckets. **No offsite backup** today.
- **eq-canonical-internal (`zaapmfdkgedqupfjtchl`)** holds real operational data (500 schedule entries, 323 tenders, timesheets, customers, sites). No offsite.
- **eq-tenant-favour-perfect (`jzjzpgaablnppoimdnip`)** — empty, system migrations only (created 2026-07-03).
- ehow storage = **6** buckets: `attachments`, `logos`, `licence-photos`, `sks-quote-attachments`, `job-plan-references`, `compliance-packs`.
- The retired eq-service Weekly Backup **failed 6 consecutive runs since 2026-05-24** (last green 2026-05-17), predating the urjh deletion (2026-06-22) — no alert. Its dump was also schema-only.
---

## ⏩ Session close — 2026-06-28 — Brain 10/10: substrate coherence + automation layer

**Completed:**

**Open / next:**
- [ ] **Update C:\Projects\.git-credentials** files with new PAT after rotation
---

## 🟦 Autonomous Sprint — SOURCE OF TRUTH (read first if running sprint work)

> **⚠ SUPERSEDED (2026-07-12) — the Autonomous Sprint coordination mode is retired.**
> Work now runs as normal PRs; current state lives in `suite-state.md` (auto-refreshed
> nightly) and `digest.md` (what needs attention). `SPRINT-BOARD.md` and `STATE.md`
> are archived (`archive/sprints/`) — kept for history, not live. Section below kept
> for record only.

Parallel autonomous agents coordinate through three root files (added 2026-05-30):
- `SPRINT-BOARD.md` — full backlog + claim/ownership (claim before you start)
- `AUTONOMOUS-SPRINT-RULES.md` — diverge-proof conventions (branch from origin/main, **timestamp migrations**, SKS-live untouchable, full-auto EQ deploy, auth gated)
- `STATE.md` — per-repo + Supabase reality + known hazards

Autonomy policy: `ops/decisions.md` 2026-05-30. Session log: `sessions/2026-05-30.md`.

**Drift resolved (2026-06-02):** the GTM gate was killed (we build for ourselves — see `ops/decisions.md` 2026-06-02) and the stale gate language was purged from the forward docs. The "two-Supabase obsolete / single canonical" framing is also stale — reality is the two-plane split (`eq-canonical` + `eq-canonical-internal`). `STATE.md` carried current reality at the time (now archived — see `suite-state.md`).

---

## eq-context: backlog overwhelm fixed at the source — nightly rotation + personal queue (2026-07-27)
*Royce reacted to the 478-open-item backlog workbook and said "help me fix it." The number was mostly bookkeeping, not engineering debt: done items never rotated (one manual chore ever), one trailing "Royce to confirm" line trapped whole finished sessions, and ~79 items across the three tiers are personally his (confirms/click-throughs/calls), buried in the engineering noise.*

- [ ] **Royce to work through the "Your queue" artifact** (81 items: SEC-9/SEC-10 key rotations first, then 79 confirm/decide items) — telling any session "confirmed: X" closes items properly. _(added 2026-07-27)_
- [ ] **Stale-cull sweep of the ~90 open items older than 30 days** (including the restored May section) — close dead ones, merge duplicate threads. Good multi-agent session on its own; not run this session. _(added 2026-07-27)_

---

## eq-context: 32 stale stashes in the shared checkout audited and cleared to 1, one real security gap recovered (2026-08-20)
*Investigating "close the loop on eq-context" (a plain sync request) surfaced a much bigger, undocumented problem: 32 git stashes sitting in the shared checkout since 2026-06-03, most labeled "concurrent session's uncommitted X — not mine, do not resolve" by past sessions that hit the same dirty-checkout wall and never came back to reconcile it. Audited via 3 parallel agents (read-only, each stash diffed against live `origin/main` before any drop) plus direct review — every one of the 31 acted on was independently verified, not assumed.*

- [ ] **1 remaining (was #16) needs Royce's own read, not a session's guess.** Its `eq/pending.md` half already landed; its `system/lessons.md` half proposes "re-authorize the GitHub App installation" to fix the GitHub MCP's 404s on private EQ repos — live-retested this session, the 404 still reproduces exactly as described. But `sessions/2026-07-20.md` already tested and disproved that exact theory (a live side-effect test: making `eq-shell` private broke access identically regardless of collaborator changes, then confirmed the connector is GitHub's own Copilot MCP server, OAuth-based — there's no "App installation" screen for this connector type to begin with) and landed on Copilot licensing as the actual cause. Landing the stash's fix as-is would point a future session at an already-falsified theory. Options offered, not yet answered: rewrite pointing at the real conclusion, or drop and let the 07-20 investigation stand as the record. _(added 2026-08-20)_

---

## eq-context: F12 partially closed — dirty-checkout guard for the substrate sync, plus a detect-fake-worktree bug fixed (2026-08-17)
- [ ] **F12 ratchet still below target** — `guard-ratchet.yml`'s own rule (`recurrences >= 2 AND rung < 4`) now flags F12 as PROMOTION DUE: rung 2, target 4. Root cause fixed this session (`hooks/substrate_sync.py` now skips its automatic `pull --ff-only` on the shared checkout whenever it's dirty, closing the mechanism that actually caused this session's own staged edits to vanish — eq-context [PR #164](https://github.com/eq-solutions/eq-context/pull/164), merged; also fixed live-only wiring drift, `C:/Users/EQ/.claude/settings.json` was still running a pre-2026-08-15 inline PowerShell pull blob instead of calling the governed script). The originally-proposed GENERAL guard — diff a side-clone's freshly-pulled content against the local copy before any copy-back, refuse anything that isn't a strict superset/merge — is still not built, deliberately deferred both times as adversarial-test-grade work. Also found and fixed while recovering from the incident: `guard.js`'s `detect-fake-worktree` rule didn't resolve the Git-Bash `/tmp` MSYS mount (only `/c/...` drive-letter paths), so F9's own recommended recovery path failed on the first attempt against a real, valid worktree under the OS temp dir — extended the normalizer to resolve `/tmp` via `os.tmpdir()` (local-only file, no PR). Propose-only per Royce's 2026-07-11 ruling on the ratchet; needs his call on scope/timing for the general guard, not a default next-session pickup. _(added 2026-08-17)_

---

