---
title: EQ Cards — Pending Actions
owner: Royce Milmlow
last_updated: 2026-09-02
scope: EQ Cards engineering backlog, split out of eq/pending.md (2026-08-17) so a session working in this repo isn't wading through the other 8 repos' items too. Same conventions as before: "- [ ]" open, "- [x]" done (rotated out nightly by scripts/rotate_pending.py), "- [~]" in progress.
read_priority: critical
status: live
---

# EQ Cards — Pending

Split out of `eq/pending.md` (2026-08-17) — see `eq/pending.md` for why. SKS items live in `sks/pending.md`. OPS items (entities, tax, infra) in `ops/pending.md`.

---

## eq-cards: Wallet screen's Export button had no visible label — fixed, merged, deployed live (2026-09-02)
*Royce flagged it from a screen recording: "1 thing needs a look" was the icon-only download/export button in the Wallet app bar — no visible text, just a tooltip nobody sees on a phone. Same pattern already fixed for the adjacent "Add" button; applied the identical fix.*

- [x] `IconButton` (icon-only, tooltip "Export") → `TextButton.icon` with a visible "Export" label, mirroring the existing "Add" button in the same app bar — [PR #340](https://github.com/eq-solutions/eq-cards/pull/340), squash-merged (`6e6f667`).
- [x] Deployed live via `workflow_dispatch` → Netlify, verified against Netlify's own deploy record (`state: ready`, `published_at` set, flagged as the *current* deploy) — not just the Action's own green checkmark.

**Deferred:**
- [ ] **Not click-tested live** — the Wallet screen sits behind phone-OTP sign-in; no credentials available in this environment. Verified via `flutter analyze` (clean) and a successful `flutter build web` instead. _(added 2026-09-02)_
- [ ] **Unrelated bug found while verifying, not fixed this session**: `flutter test` can't compile locally on Windows — a null-safety bug in the pinned `pdfrx_engine` 0.4.5 package, reproduced on two unrelated test files, confirmed unrelated to any pubspec change made this session. Flagged as background task `task_1310e6b1`; Royce has already started it running in a separate session. _(added 2026-09-02)_

**Notes:**
- Claude Code's auto-mode classifier blocked triggering the deploy workflow directly (`gh workflow run deploy.yml`) — Royce triggered it himself via the Actions UI instead. Same class of classifier wall this file documents elsewhere for direct DB/merge/push actions — worth expecting on any eq-cards deploy attempted from a session rather than assuming it goes straight through.
- `flutter analyze`/`flutter build web` both silently ran `pub get` and auto-edited `analysis_options.yaml` as side effects — reverted both each time to keep the shipped diff scoped to just the one intended file.

---

## eq-cards: product-polish audit → 3 rounds, 4 PRs, all shipped/merged/deployed live (2026-08-30 → 08-31)

- [ ] **Correction, found at close: `worker_house` was never actually given test coverage, contradicting round 3's own "every feature folder now has real coverage, zero exceptions" claim.** Verified directly (`test/features/worker_house/` doesn't exist; every other `lib/features/*` folder now has a matching `test/features/*` one). The round-2 fix to `worker_credentials_notifier.dart` (refresh() capability) itself has no test either. The scorecard artifact's "zero exceptions" line has been corrected to name this gap rather than left standing. _(added 2026-09-01)_
- [ ] The new PWA "update available" banner (round 3) can't be fully verified by `flutter test` — needs a real deployed check: ship two versions, confirm the banner actually appears and "Refresh" actually updates the tab. _(added 2026-08-31)_
- [ ] Real usability sessions with actual tradies — flagged in the 25 Aug review, still not done after 3 further rounds of code-level fixes. No code-level review substitutes for watching one real person use it. _(added 2026-08-25, restated 2026-08-31)_
- [ ] Live click-throughs still owed on specific shipped fixes: PR #331's admin-members error/retry state, and the mobile sign-in layout on an actual phone (both verified via automated tests + code review / a screenshot, not a real signed-in session). _(added 2026-08-30, restated 2026-08-31)_

---

## eq-cards: white-on-sky button text failed WCAG AA everywhere it appeared — new skyAA token, 27 instances fixed across 3 PRs, deployed live (2026-08-31)
*Flagged: `EqButtonVariant.primary`/`.hero` (the app's main shared button style) rendered white text on `EqColours.sky` at ~2.69:1 — fails WCAG AA even at the relaxed 3:1 large-text/UI-component floor, let alone the 4.5:1 normal-text bar. Computed the real contrast math for every candidate (sky/deep/skyAA/ink) against the actual text sizes EqButton and other call sites use, rendered a visual comparison, and let Royce pick the exact shade rather than silently swapping a component used on dozens of screens.*

- [x] Added `EqColors.skyAA` (`#267DA6`, ~4.60:1 white-on-bg — clears AA at every text size the app uses, same blue hue family as sky/deep) to `eq_tokens.dart`/`eq_colours.dart`. Royce chose this over reusing `deep` (partial fix only, still short of 4.5:1 for normal-size text), switching to `ink` (loses the brand-blue identity), or documenting an exception (indefensible — sky fails even the 3:1 floor).
- [x] `EqButtonVariant.primary`/`.hero` switched to `skyAA` — [PR #336](https://github.com/eq-solutions/eq-cards/pull/336).
- [x] Found in passing while fixing the above: `connect_to_company_screen.dart`'s "Apply" button had the identical sky/white fail, missed by an earlier a11y sweep ([PR #313](https://github.com/eq-solutions/eq-cards/pull/313)) that fixed a `Radio` a few lines above it in the same file — fixed in the same PR.
- [x] Broader sweep at Royce's request: 9 more `EqColours.sky`-as-button-background instances across auth/consent/licence-capture/admin screens (background task, folded into #336 via merge-conflict resolution against a same-day, independently-landed `main` PR that had also partially fixed the Apply button — see Notes).
- [x] Second sweep: 14 more sky-contrast spots plus a `TextButtonTheme` default (bare `TextButton`s were inheriting Material's default blue instead of any EQ color) — [PR #339](https://github.com/eq-solutions/eq-cards/pull/339).
- [x] Deployed live (`workflow_dispatch` → Netlify) and verified two ways: the Netlify API shows `state: ready` / `published_at` set (not just "uploaded"), and a live screenshot of `cards.eq.solutions`'s sign-in screen shows the new darker button.

**Deferred:**
- [ ] Not click-tested by a person with actual low vision or a screen reader — verified via computed contrast ratios, a rendered swatch comparison, downloaded golden PNGs, and a live screenshot, not a real assistive-tech session. _(added 2026-08-31)_
- [ ] `EqColors.skyDeep` in `eq_tokens.dart` is a byte-identical duplicate of `EqColors.deep` (both `#2986B4`) — noticed while adding `skyAA` next to it, not cleaned up (out of scope for this pass). _(added 2026-08-31)_
- [ ] 61 remaining `EqColours.sky` references left untouched on purpose (decorative accents, low-alpha borders, transient spinners, icons beside a duplicate visible text label) — documented in PR #339's own commit message rather than silently dropped, but worth Royce's spot-check if he wants zero `sky` left in button-adjacent contexts. _(added 2026-08-31)_

**Notes:**
- A same-day, independently-driven PR (#334, "round 3 of the polish sprint" — see the section above) fixed the same `connect_to_company_screen.dart` Apply button mid-flight (sky → `deep`), landing on `main` while this work was still open as a PR. Caught via `mergeable: CONFLICTING`, resolved in favour of the fuller `skyAA` fix — that PR's own commit message had already named the remaining gap as "its own follow-up."
- A background task spawned from this session (auditing the rest of the app for the same pattern) pushed its finished commit directly onto this session's own PR branch rather than an independent one — not unsafe in the end (re-fetched before every push, no work lost), but worth knowing for next time: a `spawn_task` prompt should say explicitly whether follow-up work should extend the calling session's branch or use its own.
- eq-cards' deploy workflow reports `state: uploaded` on success, not `ready`/published — same "green checkmark ≠ live" gap already documented for eq-shell in global `CLAUDE.md`. Confirmed the same verification method (poll the Netlify API for `state: ready` + `published_at`, don't trust the Action's own exit code alone) applies here too.

---

## eq-cards: live-meeting onboarding kit built for a CEO/executive demo — self-signup verified, EQ Solutions demo org enabled, sprint spun off two real gaps (2026-08-30 → 09-02)
*Asked for a simple onboarding tool, redirected twice by Royce toward what it actually needed to be: a laminated card + live demo for an in-person executive meeting, walking scan → apply → live approval → Field/Service visibility. Verified every claim against live code and the live DB before building anything, catching a dead feature and a phone-binding constraint along the way.*

- [x] **Confirmed self-signup (any phone, no invite) is the right mechanism**, not the admin-generated per-worker invite this session first proposed — invites are phone-bound by design (migration `0124`, a real security fix closing a colleague-invite-theft path), which doesn't fit "hand a laminated card to a room of strangers." Self-signup's built-in onboarding already prompts scan-a-licence → pick-a-company with zero new code needed.
- [x] **`organisations.accepts_applications` flipped to `true` for the existing "EQ Solutions" org** (`a0000000-…001`, slug `eq`, already flagged `is_seed_demo=true` — Royce's own instinct to reuse it instead of creating a new org was correct, confirmed live) — the one flag needed for it to show up in Cards' "Connect to a company" search. Applied by Royce directly after hitting the same Claude Code auto-mode classifier wall as later DB writes this session; verified live from this session afterward.
- [x] **Confirmed the full cross-app propagation live, not assumed**: an approved self-signup application writes `app_data.staff` synchronously (before the approval click's own response returns) on the tenant's own dedicated data-plane project — `zaap` for EQ, `ehow` for SKS, both confirmed against the live `shell_control.tenant_routing` table, not inferred from naming. EQ Service reads the same row live through a `security_invoker` view (`service.staff`, migration `0161`) — no sync delay on either side.
- [x] **Found a real, live, user-facing bug while researching the above, and it's now fully closed**: the Profile tab's manager/supervisor-only "Worker join QR" (captioned "Share this QR at induction") pointed at `/join?tenant=…`, a route that didn't exist anywhere — not in `app_router.dart`/`routes.dart`, not in `web/_redirects`. Spawned as background task `task_63219c0e`; Royce ran it in a separate session, which resolved it the same day — git archaeology there traced it to [PR #248](https://github.com/eq-solutions/eq-cards/pull/248) (2026-08-15) already having deleted the route's whole backend and named Shell's role-tagged self-join QR as the real replacement, just missing this one leftover card. Removed outright rather than rebuilt, [PR #329](https://github.com/eq-solutions/eq-cards/pull/329), merged, deploy-verified live. Full write-up, including the worktree cleanup, already archived to `eq/pending-archive.md` by that session — nothing left open on this thread.
- [x] **Three artifacts published for the live meeting** (not code — Claude Artifacts, referenced by URL in this session's chat history, not duplicated into substrate): a laminated print-and-scan card (front: 3-step instructions; back: a clearly-marked sample licence for the OCR demo), a suite-wide "EQ End to End" marketing one-pager (Cards/Shell/Field/Service, content pulled from each repo's own docs, not guessed), and a presenter-only timed run sheet with the four things that actually trip up a live demo (Field's roster needing a manual sync tap; Prestart's roster-pull not finding an unrostered fresh worker; skip the hazards checklist to avoid an extra confirm dialog; approve the leave request yourself to close the loop on stage).
- [x] **Sprint spun off two gaps found while building the above, steelmanned before planning**: shipped the Prestart/roster-pull fix (see `eq/pending/eq-field.md`, 2026-08-30) after checking it properly first; Field's realtime roster push was costed (not guessed) and explicitly deferred — that repo hand-rolls the Phoenix channel protocol with no SDK, and every existing channel needed its own base-table mapping and merge function, with real history of going silently inert when that mapping's wrong. Not a config toggle; held out rather than forced through.
- [x] **Fourth artifact published, 2026-09-02: "EQ Sample ID Sheet"** — a double-sided A4, one per table rather than per person, with 6 different sample credentials (White Card, Driver Licence, First Aid, Working at Heights, Forklift, EWP) so a room of attendees isn't all scanning the identical fake identity. Same front-side instructions/company link as the laminated card.
- [x] **Investigated Royce's "QR codes for whatever role, via add workers" ask before building anything, 2026-09-02 — it already exists, live and mature.** eq-shell's `AdminSelfJoinLinks.tsx` (`/:tenantSlug/admin/workers/join-links`, linked directly from Worker Invites) generates a per-role QR (all 6 roles), reusable by any number of people — not single-use — with its own expiry and an approval-required toggle, plus regenerate/deactivate/delete lifecycle management. Confirmed via the live table (`shell_control.self_join_codes` on jvkn), not assumed from the code alone: 8 real codes, actively created and used through 2026-08-26 — all for the `sks` tenant. **Zero for `eq`** — the feature has simply never been pointed at this tenant, nothing broken or missing to build.

**Deferred:**
- [ ] **Self-serve tenant provisioning doesn't collect tier/modules upfront** — the provision-link form (eq-shell's `AdminTenantsPage.tsx`) only takes org name/phone/email; tier and modules get set afterward via a separate Edit step. Real gap, wrong sprint — three-tenants-ever doesn't justify the slot right now. _(added 2026-08-30)_
- [ ] **Whether to generate a real EQ self-join link/QR for the meeting, swapped in for the Sample ID Sheet's generic search-and-apply flow** — asked Royce directly; no answer yet as of this close. `AdminSelfJoinLinks.tsx` is ready to use as-is — pick a role/label/expiry and click Create, a 30-second admin action whenever he wants it done. _(added 2026-09-02)_

**Notes:**
- A third live DB write this session (the Prestart fix's two view migrations, tracked under `eq/pending/eq-field.md`) hit the identical auto-mode classifier wall as the `accepts_applications` flip — three for three, consistent, not a fluke. Royce can loosen it via a Bash permission rule if this keeps recurring; not done by default.
- GitHub MCP 404'd on eq-field specifically (separate repo-access gap from this session's eq-field work) — `gh` CLI used throughout for that repo's PR/merge work.
- The `AdminSelfJoinLinks` finding came from querying the live `self_join_codes` table directly rather than trusting the component's own code/comments at face value — same verify-before-recommending discipline as the rest of this thread; the code alone would have said "this exists" but not "and it's actually been used, just never for this tenant."

---

## eq-cards + eq-shell: `/auth/handoff` signup-blocker root-caused, fixed, merged, deployed live (2026-08-27)
*Asked to investigate why `cards.eq.solutions/auth/handoff` — the page Shell's SSO handoff lands new signups on, 99%+ of suite signup traffic — was losing almost everyone who reached it. Given PostHog evidence up front (30d trailing, project 162632): 1,378 pageviews but only 243 (18%) ever resolved to a `shell_handoff_outcome` event at all; of those, 236 were `token_verify_success` (97%); but only 27 of those 236 (11%) ever reached `signup_completed`. A 100-minute session recording showed zero clicks, zero keypresses, no console errors — a silent hang, not a crash. Read-only investigation first, propose a fix only once the actual mechanism was found — not the symptom.*


**Deferred:**
- [ ] **Neither PR was click-tested live by a person** — no live Shell session was available this session. Worth a real click-through of the slow-fallback retry UI, and one genuine new-signup handoff to confirm `is_new_user`/`signup_completed` fire correctly end-to-end. _(added 2026-08-27)_
- [ ] **WHY the `verifyOTP` network call itself stalls server-side was never confirmed** — slow `custom_access_token_hook`? Supabase connection-pool exhaustion on jvkn? No Supabase Auth-log/MCP access was available this session to check GoTrue-side latency directly. The client-side fix (bounded timeout + fallback UI) is correct regardless of the server-side reason, but the underlying mechanism is still open. _(added 2026-08-27)_
- [ ] **Re-query the PostHog funnel again once real traffic has passed through** (hours, not minutes) to confirm the fix actually moved the 82%/11% numbers. _(added 2026-08-27)_

**Notes:**
- Full technical diagnosis (file:line citations, ruled-out causes, exact funnel query shapes) lives in this session's own memory records — eq-cards' `cards_handoff_signup_blocker_diagnosed.md` and the companion eq-shell `cards-auth-handoff-stuck-signup-blocker.md` — not duplicated here.
- Both PRs built in dedicated `.claude/worktrees/` (never the shared bare-root checkouts) per each repo's own established convention.
- GitHub MCP (`mcp__d2708d72...`) returned 404 for both PRs in this org, before and after merge — auth-scope issue, not a PR-state issue. `gh` CLI worked throughout and was used instead; worth knowing if a future session hits the same 404s here.

---

## eq-cards + eq-shell + eq-field: eq-shell's synthetic cards.eq.solutions email — stopped from ever displaying as real, merged + deployed live across all three apps (2026-08-26)
*Royce: a phone-only-signup worker's real email was never captured (`shell_control.users.email` null since signup), and eq-shell's internal GoTrue placeholder (`${user.id}@cards.eq.solutions`, minted so a magic-link token has something to key on — working as designed, Sentry EQ-SHELL-13 context) was silently standing in for it, showing as a real address on his EQ Field/Cards profile. Asked to investigate every place it could display across eq-cards + eq-shell, and check whether PR #1125's existing email-capture nudge already covered it, before writing any code.*

**Deferred:**
- [ ] **Standalone Cards "personal wallet" email nudge — explicitly deferred, Royce's call.** PR #1125's nudge only covers the Shell-login path; the standalone signup path (`autoProvision`) still has no email capture at all. Held on the 90/10 SKS-focus reasoning — PR #1125 already covers the population that matters most today. Revisit if standalone signups grow. _(added 2026-08-26)_
- [ ] **eq-field's pre-existing `build-bundles.mjs --check`/`check-cache-busters.mjs` CI drift**, unrelated to this fix (confirmed reproduces on `origin/main` itself) — flagged as background task `task_bc389479`, which Royce has already started running in a separate session. Not this session's to finish. _(added 2026-08-26)_

**Notes:**
- All three repos' git surgery was done in isolated worktrees/clones (eq-cards + eq-shell via `.claude/worktrees/`, matching each repo's own established convention) — never the shared bare-root checkouts, consistent with every other entry in this file about that failure class.
- Netlify deploy verification used direct commit-ancestry checks (`commit_ref` on the newest `ready`/`context:production` deploy vs. the actual merge SHA) rather than trusting "merge succeeded" alone — per the standing eq-shell deploy-verification method documented in global CLAUDE.md.

---

## eq-cards: deep-dive review (Security/Scalability/UI-UX/Code&Docs/Product-Value) → two-sprint remediation, 10 more PRs merged, branch protection enabled, 3 real bugs caught before shipping (2026-08-25)
*Asked to deep-dive-review EQ Cards and rate it. Published a 5-category scorecard (Security 6, Scalability 6, UI/UX 7, Code&Docs 7, Product Value 7 /10) as an artifact, then a sprint plan to close the gap to 9/10 with an explicit honesty note that Product Value can't be moved by engineering alone. Royce approved starting immediately; this section covers everything built off that plan, continuing past where the sections below (PR #298/#300/#302/#304, already logged by other sessions) leave off.*

**Deferred:**
- [ ] **eq-shell coupling contract** — several `eq_cards_*` `SECURITY DEFINER` functions write directly into eq-shell's `shell_control.users`/`shell_control.user_tenant_memberships` with no API boundary or version pin (migrations 0029-0031). A column rename on eq-shell's side would break eq-cards silently, invisible to this repo's own CI. Needs alignment with whoever owns eq-shell, not something this repo can fix alone. _(added 2026-08-25)_
- [ ] **The 3-way visual "Design" picker (Linear/Wallet/Photo-first) needs Royce's own call**, not a delegated one — triples the maintenance surface of the most-used screens, in real tension with `ARCHITECTURE.md`'s own rule one ("boring beats clever"). Well-executed (accessibility consolidated across all three variants) but the resolve-or-keep decision needs eyes on the actual screens. _(added 2026-08-25)_
- [ ] **External/adversarial security review** — everything above is self- and CI-verified; an outside or adversarial pass on the post-sprint state wasn't attempted and doesn't fit inside a sprint by design. _(added 2026-08-25)_
- [ ] **Real usability sessions with actual SKS tradies** — the accessibility/affordance work above is code-level verified; nobody has watched a real tradie use the fixed flow. Calendar-bound, not a code task. _(added 2026-08-25)_
- [ ] **A recurring doc-freshness check** (a PR-template checkbox, or a scheduled reminder) — proposed, not built. Without one, the ~87-day drift this session found in `ARCHITECTURE.md`/`STATUS.md`/`CHANGELOG.md` (already fixed, see PRs #300/#306/#308) has no guard against recurring. _(added 2026-08-25)_
- [ ] **`copy_field` re-measurement, 2026-08-25 → ~2026-09-22.** Royce's call: fix the affordance bugs first (done, PR #301, deployed), re-measure for 3-4 weeks, *then* decide whether to redefine or keep the app's own ≥5/week success bar — don't redefine against a number a known bug was contaminating. Series has a real discontinuity at the deploy date (see PR #301 above) — don't compare raw pre/post totals. _(added 2026-08-25)_
- [ ] **Retention/purge cron schedules stay disabled** until someone deliberately arms them — dry-run and manual-invoke paths both work today; nightly automatic deletion against real user data is a separate, later decision. _(added 2026-08-25)_

**Notes:**
- **Branch-protection bootstrapping bug, self-inflicted, found and fixed same session.** After enabling protection, [PR #312](https://github.com/eq-solutions/eq-cards/pull/312) got stuck `BLOCKED` despite all 3 checks green, branch up to date, no review required — because that PR *itself* renamed the `function-grants` CI job (to cover modified files too), and protection still required the *old* exact job name, which that branch's own CI could never report again. Root-caused via GraphQL check-run inspection (not assumed to be a GitHub cache glitch), fixed by updating the required-context name to match — merged through the normal path afterward, **not** via the `--admin` override Royce had explicitly authorized once the real cause was found.
- **This session's own worktree got severed mid-task by a concurrent session's cleanup** (`git worktree remove` succeeded git-side; physical folder delete failed on a Windows file lock) — caught by a `detect-fake-worktree` guard before any command could act on it (a different hazard than the bare-root-Edit/Write problem `F15`/PR #309 above targets, same protective family). No work lost — nothing had been committed on that worktree's own branch. Recovered via a fresh `git worktree add`, per the same "don't repair, start fresh" instinct this file's other worktree-collision entries already establish.
- Two artifacts published (not code, not tracked here as PRs): the original 5-category rating scorecard, and the sprint plan with its 3-tier honesty framing (this-sprint / needs-a-decision / needs-calendar-time). Both referenced by URL in the session's own chat history, not duplicated into substrate.

---

## eq-cards: sessions now default to their own worktree — hook-enforced, not just documented (2026-08-25)
*Follow-on to the section below (the duplicate-`0142` verification). Immediately after that close, Royce asked to check who had taken the bare root out from under this session mid-task — traced to a concurrent session (`local_b525bcf3`, owner of PR #300, the PR whose migration created the `0142` collision in the first place) switching the root's branch twice while three sessions shared it. Royce's instruction in response: "make eq-cards sessions default to their own worktree."*

**Deferred:**
- [ ] **git-verb collision protection for the eq-cards bare root** (a commit landing on whichever branch the root happens to be on) — explicitly out of scope for this pass, see F15's own note in `system/failures.md`. Would need F9(a)-grade shell-command parsing (`effective_cwd()`, pathspec/exemption handling) for a smaller, but real, share of the documented damage. _(added 2026-08-25)_
- [ ] **Broken internal link found in passing, unrelated to this task** — `eq/pending-archive.md` line ~9543 links `../../system/worktree-registry.md` (one `../` too many; the file is one directory deep, needs `../system/worktree-registry.md`), failing `MD health check` CI on every push to `eq-context main` since before this session touched it. Spawned as background task `task_c71000f5` rather than fixed inline (unrelated file, unrelated concern). _(added 2026-08-25)_

---

## eq-cards: governance docs (ARCHITECTURE/README/STATUS/CHANGELOG) were 87 days stale and actively wrong — corrected, committed, live on PR #300 (2026-08-25)
*A repo review flagged specific stale claims: auth described as "phone-as-identity retired" (flipped back to mobile-primary 2026-08-15, PR #246); deploy described as auto-on-merge (explicit-only since 2026-08-14); README pointed at a PIN app-lock deleted 2026-08-15 (PR #249) that was never wired into the router; stack table drifted 15+ versions behind `pubspec.yaml`; folder tree still showed 5 feature folders against the current 12. Docs-only task, no code/migration changes, all claims verified against live `pubspec.yaml`/git log/`test/` before rewriting.*

**Deferred:**
- [ ] **PR #300's title/description only describe the security fix** — doesn't mention it also carries this 4-file, 370-line docs correction. Flagged to Royce; not edited (his or the other session's call). _(added 2026-08-25)_
- [ ] **CHANGELOG process change** — recommendation written into the file itself (checkpoint-based updates, or generate a supplementary log from this repo's already-conventional commit messages), not decided. _(added 2026-08-25)_

**Notes:**
- **This branch's local checkout had its upstream tracking misconfigured to `origin/main` instead of its own remote branch** — a bare `git push` here would have pushed a feature branch straight onto `main`, no PR, bypassing review. Caught before pushing (checked `git branch -vv` first), pushed with an explicit `local:remote` refspec instead, then fixed the tracking (`git branch --set-upstream-to`) on request.
- **A concurrent session was actively committing to this exact branch, in this exact shared root, during this session** — its own security fix (migration `0142`) landed while the docs work was staged. One of its commits swept up this session's already-`git add`-staged doc changes (likely via `git commit -a`), producing one commit with both unrelated bodies of work under a security-only message. **Self-corrected without this session's intervention**: that commit was `git reset HEAD~1`'d and re-committed with only the security fix, by whatever was driving the other session — the docs changes came back as clean unstaged working-tree edits, fully intact, then were committed separately and cleanly. New, reassuring data point for eq-cards' version of the concurrent-checkout collision pattern already well-documented for eq-context/eq-field/eq-shell elsewhere in this file and in `sessions/`: at least one class of this failure (staged-change sweep-in) appears to have a working self-correction mechanism here, not just a manual recovery playbook.

**Confirmed from the other side** (security-fix session's own account, added when reconciling this same conflict at close): matches exactly — that session caught its own over-broad local commit via `git show --stat` showing 5 files instead of 1, undid it with a mixed `git reset HEAD~1` (never touching working-tree content), and re-committed with `git commit -- <path>` restricted to just its own file. Independently, this docs commit *also* reached the shared remote branch before the security fix was merged, so both ended up combined in PR #300's squash-merge (`2d2881b7`, verified directly: 5 files, both commit messages present) — not just the local staging near-miss described above.

---

## eq-cards: unauthenticated caller could silently decline/corrupt another worker's pending connection request — found, fixed, applied live (PR #300, merged 2026-08-25)
*Confirmed live via `information_schema.role_routine_grants` + a direct read of the function body: `eq_cards_respond_to_access_request`'s ownership check evaluated to SQL NULL (not FALSE) for an unauthenticated caller, so its `RAISE EXCEPTION` never fired — same NULL-`auth.uid()` bug class already fixed elsewhere in this repo (0058, SEC-30/31/33).*

- [~] **Grant-hygiene follow-up**: those 10 functions still carry unnecessary `anon`/`PUBLIC` EXECUTE (not exploitable, just excess surface). Spawned as a background task, Royce already started it in a separate session. _(added 2026-08-25)_

---

## eq-cards: workers-canonical-sync no longer creates a staff row on a non-INSERT (PR #292) (2026-08-23)
*Closes the mis-filing hazard proven live the same day — a phone backfill on jvkn put a Cards user with no SKS connection onto SKS's roster for ~10 minutes. Full detail in `eq/changelog/eq-cards.md`; the architectural analysis is in [`IDENTITY-MODEL.md` §3.3.1/§3.3.2](../identity/IDENTITY-MODEL.md).*

- [~] **`SKS_TENANT_ID` hardcode made safe, not removed — built, not yet merged/deployed.** Of the three shapes recorded in §3.3.2, chose "carry the tenant with the event": a new nullable `workers.origin_org_id`, stamped by `labour-hire-candidate-intake` (the exact path behind the Conor Horgan/Nelson Sareto incident, already resolves `orgId` synchronously). The sync's INSERT branch now refuses to create a staff row when a stamped org names anyone other than SKS; unstamped rows (self-signup, invite-claim, `eq_cards_admin_upsert_worker`, anything pre-existing) keep today's behaviour. eq-cards [PR #293](https://github.com/eq-solutions/eq-cards/pull/293), CI green (after fixing two real issues along the way: a migration-number collision with a concurrently-merged `0137`, renumbered to `0138`; and a `check-function-grants.mjs` conflict on `eq_cards_admin_upsert_worker` resolved by dropping that function's stamping from this pass entirely rather than guessing at a live grant discrepancy — see the migration's own comment). **Still actively wrong the moment a second tenant exists** — this closes the mis-filing hazard, it doesn't add a second destination; that's real, deliberately deferred future work. `eq_cards_find_or_create_worker_for_invite`/`eq_cards_link_or_create_worker`/`eq_cards_admin_upsert_worker` deliberately not wired to stamp it — neither of the first two reliably has an org at creation time, and the third would require resolving an unrelated live/history grant discrepancy this pass isn't positioned to judge. **That grant discrepancy was resolved the same day, separately — see the grant-restoration entry below.** _(2026-08-23)_
- [~] **`employment_type` structural fix, same PR.** `workers-canonical-sync` no longer derives/overwrites `employment_type` on merge at all — same treatment `field_approved`/`active` already got in this function. `employment_type_locked_by_shell` (eq-shell) left in place, now permanently inert once this ships. _(2026-08-23)_
- [ ] **The `Build & Deploy` workflow deploys ALL jvkn edge functions**, not just the changed one (`supabase functions deploy --project-ref jvknxcmbtrfnxfrwfimn`, no function name). Normal path for this repo, but it means the blast radius of any edge-function deploy is "every function at current main". Worth knowing before a hurried deploy. _(added 2026-08-23)_
- [ ] **Node 20 deprecation warning** on `supabase/setup-cli@v1` in the deploy workflow — forced onto Node 24 by the runner. Unrelated to any change, not failing, but will need bumping. _(added 2026-08-23)_

## eq-cards: Platform console redesigned around a "needs attention" queue instead of a stats wall — merged, deployed, live (2026-08-20)

- [ ] **No real action buttons yet.** Each queue row is tagged which app (Cards/Field) owns the fix, but stays read-only — nothing in this app today can re-invite in bulk or force a sync retry, so a button would have nowhere real to go. Building those is separate follow-on work, your call whether/when. _(added 2026-08-20)_
- [ ] **The Cards↔Field "bridge" is one-directional.** `eq_cards_platform_stats()` only queries jvkn (Cards' own database) — it can say how many Cards workers have been linked into Field, but not give Field's own independent total to reconcile against. A genuine two-sided view needs a second query into ehow, not built this session. _(added 2026-08-20)_

---

## eq-cards: jvkn Supabase branch-replay diagnosed and documented (2026-08-16)
*A routine attempt to branch-test an unrelated eq-cards migration (0131) hit `create_branch` failing `MIGRATIONS_FAILED` on jvkn (eq-canonical) — turned into a full root-cause investigation, since this blocks Supabase's branch-preview workflow for the whole shared control-plane project, not just eq-cards.*

**Deferred:**
- [ ] **Root cause #1's precise backfill not attempted** — real archaeology (reconstructing minimal table shapes from ~32 migrations, no live table left to verify against) on a shared prod-adjacent project. Royce's call: document only for now. _(added 2026-08-16)_
- [ ] **Root cause #2 (eq-shell's `shell_control` untracked tables) needs eq-shell to trace and fix** — eq-cards has no visibility into their original shape. eq-shell PR #1389 ("triage 3 jvkn functions into KNOWN_UNSOURCED", merged same day) suggests they may already have a related tracking mechanism worth connecting to instead of duplicating. _(added 2026-08-16)_
- [ ] **`WORKERS_WEBHOOK_SECRET` rotation** — investigated, confirmed lower-urgency than it first looked, Royce: leave it for now. If picked up later: needs jvkn's vault AND eq-shell's Edge Function secret updated in the same window or the live Cards→SKS staff sync 401s. _(added 2026-08-16)_

---

## eq-cards: role-assignment could hand someone suite-wide manager power with no audit trail — found, fixed, merged, live (2026-08-16)
*A worker's role — including "manager", the top tier every EQ app trusts — could be set from Cards' admin screen through the exact same check used for editing a phone number or address, with nothing recording who did it. eq-shell had already split this into its own separate, narrower permission earlier the same day (the new permission's own description names this exact Cards gap as the reason it was created); Cards had never adopted anything like it.*

**Deferred:**
- [ ] **Not clicked through live** — verified against real production data directly, not by an actual admin opening the screen and watching Manager disappear from the list. Worth two minutes on a real admin account. _(added 2026-08-16)_
- [ ] **Cards' own copy of the shared role/permission rulebook is a few versions behind** — old enough that it doesn't know about the new narrower "who can change someone's role" permission at all. Not required for this fix (handled a different way instead, described above) but worth catching up eventually so Cards can check permissions the same direct way Shell does. _(added 2026-08-16)_

---

## eq-cards: punch-list #4 marked "Active" but partially shipped without its own caveat (2026-08-16)
*`system/punch-list.md`'s item 4 still shows the pre-2026-08-13 note ("reconcile against screenshots before building, don't build from this doc alone"). [PR #235](https://github.com/eq-solutions/eq-cards/pull/235) shipped 2026-08-13 anyway, scoped strictly to the original doc — its own description confirms the screenshots were never incorporated. Not corrected in `punch-list.md` directly (Royce's file, his rule) — flagged here instead. Full detail: `sessions/2026-08-16.md`.*

- [ ] Get Royce's "first-open popup / info overload" screenshots (mentioned as sent separately, never received/incorporated), scope what's still missing against what PR #235 already shipped, build the remainder. _(added 2026-08-16)_
- [ ] Once resolved, update `punch-list.md` item 4's note to match reality — it currently still reads as if nothing shipped. _(added 2026-08-16)_

---

## eq-cards: licence save silently duplicated the row on a failed photo upload — found via Sentry, fixed, merged, deployed live (2026-08-13)
*Royce: "Richard Brown - three of the same certificate have been created." Investigation found 6, not 3 (half were hidden via `is_private`). Root cause: `licence_edit_screen.dart`'s save flow inserts the row, then uploads the photo — if the photo step throws, the screen doesn't remember the row already saved, so retrying inserts a new one instead of updating it. Confirmed via Sentry (`EQ-CARDS-1G`/`1H`, same trace, same user). Luke Wheeler was initially flagged as a second victim of the same pattern — that was a false positive in the blast-radius query (his 3 rows were 3 genuinely different certificates sharing an empty licence number, a normal quick-document quirk); corrected before touching his data.*

- [ ] **Richard Brown needs to re-add his LV Rescue (C40385) photo** — the surviving row has the correct licence details but no photo attached; nothing existed anywhere to recover. The fix means his retry will now update that row cleanly instead of duplicating again. _(added 2026-08-13)_

---

## eq-cards: WebOTP auto-fill for phone sign-in — shipped, and exposed a manual-deploy gate that had gone unnoticed (2026-08-05)

- [ ] **Royce to test on his Samsung/Android Chrome** now that the code and the SMS template are live together for the first time — not yet confirmed working end-to-end. No fix exists for iOS Safari (WebOTP isn't implemented there); manual entry stays as-is on that platform.
- [ ] **Worth a look: `digest.md`'s "Recently built" table shows merge status, not deploy status, for every repo — but eq-cards is the one repo where those two are allowed to diverge for hours by design.** A merged eq-cards PR currently reads identically to a live one on the digest, which is exactly what caused this session's confusion. Might be worth a "manual-deploy pending" flag specific to eq-cards, or a general merged-vs-deployed distinction if other repos ever adopt the same manual-gate pattern.

---

## eq-cards: Shell tenant auto-login bug root-caused and fixed — deployed live, needs your click-through (2026-08-04)

- [ ] **Correction (2026-08-05): PR #212's fix (below) was itself an overcorrection and has been superseded — the click-through owed is now against the newer fix, not #212.** #212 made the splash screen trust any cached local session that passed a live `getUser()` check and skip asking Shell entirely — that's what caused a *different* live bug the same day: Royce (and separately Sonam Gurung) opening Cards from Shell's tile and landing on a stale cached identity (a leftover test account) instead of their own, because a validated-but-wrong session was treated as good enough to skip the handoff. Fixed in eq-cards [PR #216](https://github.com/eq-solutions/eq-cards/pull/216) — removed `_handleShellEntry()` entirely; Cards now always asks Shell first on `?shell=1`, and a validated local session is used only as a fallback when Shell itself can't produce a token, never as a reason to skip asking. Merged and deployed. Original #212 description kept below for history.
- [ ] Auto-login from Shell's tenant tile into Cards was silently skipping the handoff and bouncing to the sign-in screen instead — reported live by Royce, root-caused same session. `cards.eq.solutions` iframes across every open Shell tab share one browser's local storage, and a refresh-token rotation triggered by one tab invalidates the session another tab still has cached. The splash screen only checked whether *a* session object existed in storage, not whether it was still valid, so a stale cached session silently pre-empted the working handoff. Root-caused live against Royce's own SKS account: PostHog showed `shell_handoff_started` never fired on the failing attempt, and eq-canonical's auth logs showed `403 bad_jwt: invalid claim: missing sub claim` at the same second. Fixed in eq-cards [PR #212](https://github.com/eq-solutions/eq-cards/pull/212) (squash-merged `36a23cd`) — `_handleShellEntry()` now validates any cached session with a live `getUser()` call before trusting it, signing out and falling through to the existing handoff on any failure. Merged and deployed (explicit `Build & Deploy` workflow dispatch — Netlify + Sentry source-map upload both succeeded). **Needs Royce's click-through**: his own browser has a bad session already stuck in local storage from before the fix — clearing site data for `cards.eq.solutions` once (or a private window) and reloading the tenant tile is a device-side action only he can do; confirming the clean auto-login after that is the last open step. _(added 2026-08-04)_

---

## eq-cards: profile-save permission bug — PR merged, live grant confirmed and applied (2026-08-03)
*Sentry showed `eq_cards_upsert_my_profile` throwing "permission denied" for every signed-in user (same incident class as the earlier `eq_cards_auto_provision` outage). PR #204 (grant-restoration migration) merged; live check before applying found the grant had already been restored, almost certainly by a concurrent session, but only as an untracked ad-hoc fix — applied the migration anyway so it's now in eq-canonical's tracked ledger instead of silently regressing on a future restore.*

**Deferred:**
- [ ] **Royce (or a real signed-in worker) to confirm live**: save/create a Cards profile and confirm it no longer errors. Off-limits for me to click-test myself. _(added 2026-08-03)_

---

## eq-cards: workers can now self-report their trade/employer, and a new platform-admin console gives Royce a live view of the whole network (2026-08-02)
*Two features, one session: closing the "who's actually using Cards" gap. First let workers tell Cards their trade and who they work through (licence data alone only reveals trade for the regulated minority). Then, since Royce kept asking "can I see this without writing SQL by hand," built him an actual screen for it.*

**Deferred:**
- [ ] **Bridging Cards' new trade/employer data into Shell** — deliberately not built; no rule exists yet for what happens when a worker's own answer disagrees with what an employer has on file. _(added 2026-08-02)_
- [ ] **Letting an admin fill in a worker's trade/employer or licences on their behalf** — deliberately not built. Licences especially: once an employer can write a licence record, it stops being trustworthy proof the worker actually holds it. Royce raised the idea, then dropped the one real case (below) that would have justified even the narrow version. _(added 2026-08-02)_
- [ ] **44 workers who signed up but can never finish claiming their account** (no invite left to do it with) — surfaced for the first time by the new console. Royce said to leave this alone for now. _(added 2026-08-02)_

---

## eq-cards: netlify.toml dead-config cleanup, orphaned welcome.html removed (2026-07-29)
*Investigating a report of an old email-login screen appearing on a phone in Brave. Production itself turned out to be correctly configured — the actual cause was a stuck service worker on that one device, not a server bug — but the investigation surfaced a real, unrelated config problem worth fixing while in the area.*

**Deferred:**
- [ ] **Royce to clear Brave's site data for cards.eq.solutions on his own phone** — the actual reported symptom (an old email-login screen). A Flutter service worker registered on that device before the phone-OTP flip is still serving its own cached copy of the old build; production itself is correctly configured (verified live). A full close + clear-site-data + reopen forces the fresh navigation the browser's update check needs. _(added 2026-07-29)_

---

## eq-cards: worker-reported "my update didn't save" root-caused and fixed, deployed (2026-07-28)
*Royce shared a screenshot of Brian Griffin-Colls' licence list on the Staff page asking why it hadn't updated — he'd said he updated his First Aid/CPR certificate. Checked the live database directly first: that record had zero write activity of any kind, successful or failed, in the 26 days since it was first added — ruling out a save that silently errored. Traced it to an already-known but ignored crash report: when the app's automatic photo-reading step times out, it correctly falls back to letting the person fill the form in by hand, but the only warning was a message that disappears after a few seconds. Easy to miss, and missing it meant walking away believing the update had gone through when the Save button was never actually pressed.*

**Deferred:**
- [ ] **Royce/a worker to trigger a slow or failed photo-read live and confirm the new message shows and stays** — verified in code + automated tests (88/88 passing), not yet clicked through for real. _(added 2026-07-28)_
- [ ] **Brian Griffin-Colls' First Aid/CPR certificate itself still needs updating** — the bug that silently dropped his attempt is now fixed, but his original update was never captured; someone still needs to redo it (himself, or an admin via the Staff page). _(added 2026-07-28)_

**Note:** the earlier eq-shell duplicate-licence fix (PR #1060) and its CI-surfaced `rls_introspection` finding are already fully covered further down this file and in today's session log (resolved as SEC-15/SEC-16) — a follow-up chip spun off for that finding this session was superseded by the time it could run; no separate entry needed here.

---

## EQ Cards — full audit turned into four real fixes, and checking real data instead of guessing corrected a wrong belief about how sign-in actually works (2026-07-20)
*Asked for a general polish/audit of EQ Cards — what's missing, what could be better. Ran a five-angle audit (security, unfinished features, look-and-feel, tech debt, test coverage), then — instead of guessing what to build next — checked real usage numbers and the live database before building anything. That check overturned a long-standing note that a sign-in shortcut was dead, and found three places where the app looked like something worked when it silently didn't.*
- [ ] **Whether to actually build the "QR code for on-site sign-in" feature, or drop it for good.** It would need EQ Field to build a scanner too — a two-app feature, not a Cards-only job. Real tap demand is now being tracked so this decision has data behind it instead of a guess. _(added 2026-07-20)_

---

## ✅ EQ Cards — uploaded PDF certificates now read themselves (2026-07-13, MERGED + DEPLOYED)
*Royce hit the pain live: uploaded a PDF certificate and had to export it as an image just to get the details read. Chose the quick reuse path over a new engine — the existing licence-reader already returns cert-relevant fields, so point the Documents PDF-upload path at it.*
- [ ] **Option B (OCR consolidation onto EQ Intake `api-extract`) — HELD (recon'd 2026-07-13, NOT a swap).** The 2026-07-13 recon killed the "same response shape survives the swap" premise: `api-extract` **does not exist** (design-only in `OCR-CONSOLIDATION-DESIGN.md`, explicitly "Build: post-SKS-go-live"); the `@eq/ai` engine it would wrap has **zero prod callers**; its response is nested (`extracted{}`) vs Cards' flat; its `licence.schema.json` has **no holder/DOB/address** → would kill Cards' profile auto-fill; and its PDF path is **not actually implemented** (hardcodes an image block) → would regress #152/#153. It's a multi-day cross-repo BUILD, not a repoint. Correctly deferred to post-launch — pick up only when the Intake endpoint is real. _(updated 2026-07-13)_

---

## ⏩ Session close — 2026-07-10 (eq-cards) — storage/security review: worker sync made reconcilable (enterprise-grade); Kurt's photos actually fixed; licence-photo admin RLS tightened

*Royce asked about storage limits, then the real risks (photos on the control layer; tenant↔control wiring redundancy / weak link). Review found the sync had no reconciliation backstop and Kurt's photos were silently un-viewable. Both fixed + a loose RLS policy tightened — all live-verified.*

**Done this session:**

**Follow-ups flagged, NOT built (surfaced in the review):**
- [ ] **Storage concentration risk (design):** every worker's licence image for every tenant lives in one private bucket in jvkn — jvkn's service-role key / RLS is the platform's crown-jewels blast radius. Inherent to the worker-owned model. Consider a dedicated storage project fronted by a minting fn + encryption above Supabase default if de-risking is wanted. _(added 2026-07-10)_
- [ ] **Generalise `workers-canonical-sync` beyond SKS/ehow** (still hardcodes `SKS_TENANT_ID` + ehow) before a second tenant onboards — the reconcile is likewise SKS-scoped. _(added 2026-07-10)_

---

## ⏩ Session close — 2026-07-02 (eq-cards part 2) — first-scan photo-pick wiring fixed + spinner copy softened

**Completed (eq-cards, PR #111 merged, deployed run 28541424467):**

**Deferred (added 2026-07-02):**
- [ ] **Manual verification on a real device** that the welcome-scan flow now succeeds on the first attempt (not just on retry). _(added 2026-07-02)_

**Notes (load-bearing):**
- This session's earlier PR #110 (`toBlob()` compression fix) is the cause of the eq-cards CI break a concurrent session found and chipped (`task_468d5ba8`, see the "connection-email deep-link" block below) — `dart:js_interop`/`package:web` in `photo_upload.dart` breaks VM test compilation. Flagging the link here so it isn't mistaken for an unrelated regression.
---

## ⏩ Session close — 2026-07-02 (eq-cards) — connection-email deep-link + Profile-tab 500 fix

**Completed (eq-cards, both live on eq-canonical `jvknxcmbtrfnxfrwfimn`, source in PR #112):**

**Decided:**
- Royce approved the live migration applies + edge-fn deploy step-by-step (audit-first each time). Chose the clean cherry-picked PR over merging the messy worktree branch.
- Connection work owned by this session; worker-name/gate fix left to the concurrent chip session (constraints relayed: use `0070`, preserve `org_slug`).

**Deferred (added 2026-07-02):**
- [ ] **Send Huon** the connection-email reply + before/after graphic. _(needs your call)_
---

## EQ Cards — canonical flip follow-ups (shipped 2026-05-21)
*This section sat corrupted in this file for 67 days — the first bullet was truncated to "**Licence p" mid-sentence. Restored verbatim 2026-07-27 from commit 436b44e (2026-05-24). All three items are from May and may be stale — verify against live before acting.*

- [ ] **This item as scoped ("the 2 licence photos") no longer matches live reality — needs re-scoping, not a quick check.** Queried live 2026-07-28: 22 electrical-licence records and 3 medicare records are missing a photo (23 distinct people, not 2) — no worker name survived from the original May flag to know which 2 this was originally about. Two live possibilities, can't distinguish from the data alone: (a) most staff never had a photo captured for these licence types in the first place (normal gap, not a loss), or (b) a specific pair genuinely lost their only copy when the source project was deleted, buried in this list of 23. Needs Royce's institutional memory (or the original 2026-05-21 source) to say who the "2" were, or this should just be re-filed as the broader "23 licences missing photos" data-completeness gap it actually is. _(added 2026-07-27, re-scoped 2026-07-28 — verified live)_

---

## ⏩ Session close — 2026-07-23 — eq-cards: closed task_d94af51d (ocr-licence 401), fix deployed live; cross-session-message channel identified

### Deferred (added 2026-07-23)
- [ ] **Confirm intent behind the cross-session-message probe.** If it wasn't Royce, it's worth knowing that any session on this machine can read another session's full transcript and inject messages into it that render indistinguishably from a normal turn — a real capability, not a bug, but one worth being deliberate about. _(needs Royce's confirmation)_
- [ ] **Minor: deployed `ocr-licence`'s `_shared/cors.ts` has a one-word comment difference from `eq-cards` `main`** (`access-control-allow-headers` vs `access-control-allow-methods` in a docstring) — purely cosmetic, the actual header-setting code is identical and correct in both. Odd only because a straight `supabase functions deploy` from `main` shouldn't produce any diff at all — suggests whoever ran the deploy had an uncommitted local tweak. Not chased further. _(low priority)_

### Notes (added 2026-07-23)
- Auto-mode classifier hard-blocks `git merge`/`push` and `deploy_edge_function` regardless of in-chat authorization — confirmed twice this session. The only ways through are Royce doing the step himself, or a standing Bash/MCP permission rule (not granted this session).
- This closes the loop opened at the end of session (11) above (`task_d94af51d`, spawned as its own session from a Sentry sweep).

---

## eq-cards + eq-shell: nightly reconciliation for the Cards→tenant licence sync (2026-08-17)
- [ ] **Same scope limitation as `workers-canonical-sync`** — the new `licence-canonical-sync` edge function (jvkn) is hardcoded to ehow/SKS, not eq-shell's generic multi-tenant routing (`getTenantDataClientById`, the pattern `licence-push.ts` itself uses). Matches existing precedent deliberately — SKS is the only tenant with a live EQ Field roster today — but if a second tenant goes live on this sync path, this function and the pg_cron loop calling it (`eq_reconcile_licence_sync()`, [migration 0132](https://github.com/eq-solutions/eq-cards/blob/main/supabase/migrations/0132_licence_sync_reconciliation.sql)) need the same multi-tenant treatment. _(added 2026-08-17)_

---

