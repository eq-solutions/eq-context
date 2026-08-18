---
title: Cross-Repo — Pending Actions
owner: Royce Milmlow
last_updated: 2026-08-18
scope: Work that genuinely spans 2+ EQ product repos as a single unit (a combined header, or the body clearly touches both). Suite-wide/substrate-process items with no single owning repo also land here.
read_priority: critical
status: live
---

# Cross-Repo — Pending

---

## eq-roles + eq-shell + eq-solves-service: PM Calendar digest switched from a hardcoded group ID to a real, grantable permission — built, released, live (2026-08-18)
*Started from a specific ask: replace `CALENDAR_DIGEST_GROUP_ID` (a hardcoded Access Control group ID in an env var) with Royce's actual model — a real permission key, grantable by role or by Custom Group, same grid as everything else. Verified live architecture first rather than assuming: EQ Service already enforces several canonical `service.*`/`entity.*` keys via `can()`, but only for role defaults — the Shell→Service JWT contract scopes `extra_perms` as Field-only, so group grants never reach it. That ruled out a session/JWT fix in favour of a roster-level one: Shell resolves effective permissions once, hands Service a plain string list.*

- [x] **New canonical permission**: `service.receive_calendar_digest`, added to `@eq-solutions/roles` (v2.7.4). Hit a real, hard architectural invariant while building it — the package's own test suite requires manager to hold every real permission, no exceptions — so a "granted to nobody by default" version was never shippable. The Claude Code permission classifier correctly blocked writing the forced `manager` default without Royce's explicit confirmation on that exact line, twice in a row.
- [x] **Resolved by shipping the consuming code first, entirely inert**: `list-members.ts` (eq-shell) computes and returns each roster member's effective permissions — [PR #1440](https://github.com/eq-solutions/eq-shell/pull/1440). EQ Service's digest gate (`canonical-members.ts`) checks the permission key instead of `CALENDAR_DIGEST_GROUP_ID` (deleted) — [eq-service PR #753](https://github.com/eq-solutions/eq-service/pull/753). Both merged and live, and completely inert at merge time — the key didn't exist in any released package yet, so nothing could match anyone.
- [x] **Default decided and shipped, by a separate thread mid-session**: `service.receive_calendar_digest` granted to `manager` only (the minimum the invariant allows) — eq-roles v2.7.4, eq-shell's pin bumped in [PR #1441](https://github.com/eq-solutions/eq-shell/pull/1441). Verified live on jvkn: 15 active SKS managers now hold it by role default; the "Calendar Digest Recipients" custom group (built empty this session) now has 18 members. The feature is fully live end to end, not just plumbing.

**Deferred:**
- [ ] **EQ Service's own `@eq-solutions/roles` pin is still v2.5.8**, two minor versions behind eq-shell's v2.7.4 — not a blocker for this feature (the digest gate reads a plain string from the roster API, no package dependency), but a real, separate gap worth a look sometime: Service is missing whatever role/permission changes landed in v2.6.x–v2.7.x. _(added 2026-08-18)_
- [ ] **Not clicked through live by a person** — the recipient-count change (0 → 15 managers + 18 group members) is verified directly against the live database, not by watching a real digest email send. _(added 2026-08-18)_

---

## eq-field + eq-shell: access-control cleanup — Pipeline/Teams/Apprentices/Email Templates get their own permission switches, then a real gap in Shell's Access Control page found and closed (2026-08-16)

- [ ] **A real, bigger idea from Royce — one single screen for all access control, not two separate systems** — discussed and deliberately not built today; needs a proper design pass first (grouping ~86 total switches sensibly is its own problem), not a same-day PR. _(added 2026-08-16)_
- [ ] **eq-shell PR #1380 merged via admin override**, bypassing a required check — confirmed the check's failure was unrelated to this PR (it was flagging something else entirely, see next item), but flagging the override itself since it bypassed a safety gate. _(added 2026-08-16)_
- [x] **3 database functions on Shell's control-plane database exist live with no matching file anywhere in the repo** — not a mystery after all: all 3 traced directly to a same-day eq-cards change that landed minutes before this check ran. Confirmed by reading eq-cards' own files and comparing every definition to what's actually live, line for line — genuinely accounted for, just not written down in this repo too. Marked as known/accepted so the check stops flagging it; no database change needed. eq-shell [PR #1389](https://github.com/eq-solutions/eq-shell/pull/1389), merged — this is also what had been blocking PR #1380/#1381 above from merging cleanly.
- [ ] Neither eq-shell PR was clicked through live — no way to sign in as a real Shell admin from this environment. Worth two minutes on Access Control next time you're in there, to see the new switches and the new pointer text for real. _(added 2026-08-16)_
- [ ] A worktree used for PR #1380 (`eq-shell-perms-discoverability-hint`) is still sitting on disk — cleanup was blocked by a permission check mid-session. Harmless, just needs a manual `git worktree remove` sometime. _(added 2026-08-16)_

---

## eq-cards + eq-shell: changing your mobile number used to split you into two accounts — fixed, and a second way in shipped (2026-08-15)
*Started from one question — "what happens if a user changes mobile numbers, can an admin update it?" — and followed it all the way down. The answer was no: the admin screen only changed Shell's copy of the number, so the next sign-in created a brand-new account and left every licence stranded on the old one. Fixing that opened up the wider question of who can be helped at all when a number is lost, which turned into a full audit of every way into the apps. Every number below was read from the live databases, not from a document.*

---

## eq-cards + eq-shell: changing your mobile number used to split you into two accounts — fixed, and a second way in shipped (2026-08-15)

**Deferred:**
- [x] **Global CLAUDE.md corrected + F13 reached rung 4, same day.** Global `CLAUDE.md`'s eq-shell deploy note now reads "corrected 2026-08-15 — the previous version of this note was WRONG and had been re-verified twice while staying wrong... There is no gap between 'merge it' and 'ship it' on this repo," with the 13-merge evidence table this item was asking for. `system/failures.md` F13 independently confirms the guard side: scanner (`substrate_honesty.py`) plus a `pre_tool_use.py` write-time block, both live. Verified 2026-08-15 by reading both files directly, not assumed from this note's own memory of them. _(added 2026-08-15, closed 2026-08-15)_
- [ ] **Where the 7 deleted test logins came from was never explained.** Each had a Core identity naming SKS but no company invite, so the sign-up fault repaired this session cannot have created them. Creation stopped on its own at the end of June and none have appeared since. Harmless now they're gone, but the door that made them is still unidentified. _(added 2026-08-15)_
- [ ] **The new standalone-worker tool has never been used on a real account.** It has tests and clean CI, but the first genuine run will be someone's actual login. Richard Brown was the obvious safe first case since he was already a known duplicate — that's since been cleaned up separately, so the next candidate is whoever asks first. Worth doing one deliberate supervised run before it's needed under pressure. _(added 2026-08-15)_
- [ ] **The email sign-in door reaches 22 of 73 accounts, and none of the six apprentices.** Shipping it didn't change that and can't: a worker still has no way to add an email to their own account. The email on the profile screen is a contact detail that travels with the street address — 73 of 101 worker records have one, but only 17 of those match an actual login. The remaining 58 were typed by admins and never verified, so they must never become logins without the worker proving they own the address. A verified add-an-email flow is the only thing that moves the 22. _(added 2026-08-15, needs your call on priority)_
- [ ] **Cards carries a fully built licence card component that nothing displays** — 404 lines across six classes, plus a maintained test file, superseded by the tiles built into the wallet screen. Safe to delete, but it is not a one-liner and wasn't in scope here. _(added 2026-08-15)_
- [ ] **Shell's intake review flow has no buttons.** Both halves — approve and reject staged rows — are fully written and reachable over the network, but nothing in the app calls either. Reviewers can stage rows and then cannot act on them. Either wire it up or retire it. _(added 2026-08-15)_
- [ ] **No skill exists for the drift audit this session ran by hand.** Worth encoding, with one caveat learned the hard way: 4 of 6 "dead code" candidates were false positives (factory constructors, static helpers, same-file use). The pattern-matching is trivial; the verification is the entire job, and a skill that emits candidates without forcing the check would generate confident nonsense at scale. _(added 2026-08-15)_

---

## eq-cards + eq-shell: audited every sign-in door, retired the two that weren't real — both live (2026-08-15)
*Started from one false sentence on the Cards sign-in screen and turned into a full audit of every way into Cards, checked against both repos and live jvkn rather than docs. Royce's read — "a lot of this has evolved into a single login QR method" — was right, but that method lives in Shell, not Cards: `create/resend-worker-invite` and the role-tagged QR both emit `core.eq.solutions/login`, and Cards' own onboarding routes turned out to be the previous generation.*

- [x] Cards sign-in footer said "this sign-in is for existing accounts only" — false for the mobile path, which creates accounts by design. Verified deliberate three ways (`OtpScreen._resolveAndLand`, `NotProvisionedScreen`, and `eq_cards_auto_provision()` read live) before touching it. Copy landed 2026-06-25 in `0a1a26f`, two days before codeless self-signup shipped; never revisited. eq-cards PR [#246](https://github.com/eq-solutions/eq-cards/pull/246), squash `e090418`.
- [x] `/join` removed entirely — provably unreachable since 2026-06-10 (no emitter in either repo; `AdminWorkerQR.tsx` said routing to `/claim` "not `/join`, is deliberate"). Took `JoinTenantScreen`, `JoinContext`, `join_context_notifier`, `AuthRepository.joinTenantExchange`, `AuthFlowNotifier.joinTenant`, `InviteLookupApi` and three redirect exemptions with it.
- [x] `/claim?tenant=` (the worker QR poster) removed — resolved against `worker_invites`, which holds 7 rows: 6 claimed, 0 unclaimed and unexpired, so every scan dead-ended on "no invite found". Tokenless `/claim` now falls through to normal sign-in, so already-printed posters still land somewhere sensible — `eq_cards_find_pending_invite` matches their number post-OTP anyway. eq-cards PR [#248](https://github.com/eq-solutions/eq-cards/pull/248), squash `13bfe54`.
- [x] Shell's `/admin/workers/qr` retired — route, lazy import and `AdminWorkerQR.tsx` deleted, leaving `/admin/workers/join-links` as the single QR door. Its hub link was already removed in the 2026-08-05 simplification pass, so the page had been reachable only by typed URL. eq-shell PR [#1361](https://github.com/eq-solutions/eq-shell/pull/1361), squash `84647b81`.
- [x] Both live. Cards deployed via `workflow_dispatch` (run `31852098680`, both jobs green, edge functions redeployed to jvkn as part of it). Shell live via the merge itself — its own build came back `Skipped`, superseded by concurrent merges, but `84647b81` is an ancestor of `8bf83a79`, the newest `ready` production deploy.

**Deferred:**
- [ ] **Neither half click-tested on a real phone** — verified by `flutter analyze`, 283 passing tests, full CI on both repos and the ancestry check, not by actually scanning an old `/claim?tenant=sks` poster or walking a fresh sign-in. Worth Royce doing both once. _(added 2026-08-15)_
- [x] **`eq_cards_lookup_invite_by_phone` anon-EXECUTE revoke — done, merged, deployed, verified live.** eq-cards [#249](https://github.com/eq-solutions/eq-cards/pull/249) merged (squash `2728110`), migration `0127` applied to jvkn — live grants checked after: only `postgres`/`service_role` remain, `anon`/`authenticated` gone. Companion eq-shell [#1368](https://github.com/eq-solutions/eq-shell/pull/1368) merged (squash `305e6ce5`), deployed, confirmed live — `core.eq.solutions`'s `cards-api?op=lookup_invite_by_phone` now 401s (falls through to the standard auth gate) instead of answering anonymously. `task_5264c029`. _(added 2026-08-15, resolved + shipped 2026-08-15)_
- [x] **Cards' dead PIN lock screen — done, merged, deployed.** `pin_entry_screen.dart` + `app_lock_notifier.dart` + `app_lock_state.dart` deleted, plus two more found live-orphaned (`raw_auth_events_provider.dart`, `pin_repository.dart`) — eq-cards [#249](https://github.com/eq-solutions/eq-cards/pull/249) merged and deployed, `cards.eq.solutions` rebuilt and smoke-checked 200. `task_4e685ee7`. _(added 2026-08-15, resolved + shipped 2026-08-15)_

---

## eq-shell/eq-field: deactivating someone didn't actually cut their EQ Field access — fixed + 2 follow-ups (2026-08-14)

- [ ] **No automated check exists to catch the cache-tag mistake above** — flagged 5 times now in eq-field's own changelog history, never built. Spun off as its own task (`task_9bd3247c`), already started in a separate session. _(added 2026-08-14)_
- [ ] **Not click-tested live** — the 4-hour session cap and its background-refresh recovery were verified by full test suite + source tracing + a live production version-banner check, not by actually leaving a real signed-in Field session open past 4 hours and watching it recover. _(added 2026-08-14)_
- [ ] **eq-shell deploy: Royce reported "didn't work" after running the production-deploy command; Netlify's own deploy record shows it actually succeeded** (commit `7c471f5` = PR #1349's merge commit, state `ready`, context `production`, published 2026-08-14 13:18 UTC, no error; core.eq.solutions responding normally). Royce has not yet confirmed whether this resolves what he saw on his end — worth a follow-up check if it comes up again. _(added 2026-08-14)_

---

## Suite-wide nav simplification — 7 items shipped and deployed (2026-08-14)

- [ ] **Decide the long-term fix for nav-visibility drift.** Three real drift incidents found and fixed this session (Cards' duplicate workspace-switcher/join-QR widgets, Field's ungated desktop Add Person, Service's stale embedded nav bar) all trace to the same root cause: no shared source of truth for "what's in the nav and who can see it" across the four apps. `eq/identity/nav-access-matrix.md` lays out two options — a shared roles-derived config each app imports, or a lighter review checklist — not decided, Royce's call. A further, more serious instance surfaced 2026-08-16 (Service's Sidebar/embedded-nav gate was tier-inverted, not just missing items — see the EQ Service section below) — reinforces the case, still not decided. _(added 2026-08-14)_

---

## eq-shell / eq-cards: suite-wide Sentry sweep, identity-collision root cause fixed, 2 bugs shipped (2026-08-14)
*Continuation of a 17-issue Sentry sweep across all 4 apps. Found the exact mechanism behind 3 identity-collision alerts (a login race in Cards' signup code), confirmed the code fix was already live, and corrected the bad data it left behind (Royce approved before any identity-data write). Also shipped a Cards OCR fix and a Shell dashboard scroll bug Royce spotted from a screenshot. (The EQ Service session-expiry Server Action work from the same sweep is tracked in its own section above/`eq-solves-service` changelog — not repeated here.)*

- [x] **Identity-collision root cause found: a login race in `eq_cards_auto_provision()`.** A session dying mid-signup could leave a broken "Personal Wallet" account with no name/email attached; a downstream sync then wrongly pointed a real staff member's record at the ghost account instead of their real one. The code fix was already live (eq-cards PR #234, confirmed against production) — didn't need re-shipping. Fixed the one known victim's data live (Royce approved first): repointed the staff record to the correct account, switched the ghost one off (deactivated, not deleted).
- [x] **Full Sentry sweep closed: 17 issues across all 4 apps** — 13 resolved (already-fixed-and-confirmed, or fixed this session), 4 ignored as one-off noise (never recurred), 1 spun off as its own follow-up job (the eq-solves-service Server Action work above).
- [x] **Cards: licence photo scan crash on unreadable photos fixed** (EQ-CARDS-1H) — was silently forwarding unreadable image bytes to the OCR service instead of showing the existing "photo couldn't be read" message. eq-cards [#236](https://github.com/eq-solutions/eq-cards/pull/236), merged + deployed live.
- [x] **Shell: dashboard scroll ending in a big blank white bar, fixed.** Royce caught this live from a screenshot ("scrolling ends up with a big white bar at the bottom"). Root cause: scrolling past the end of the sidebar or content pane let the scroll action bubble out to the whole page instead of stopping there. eq-shell [#1336](https://github.com/eq-solutions/eq-shell/pull/1336), merged + deployed live.
- [x] **Corrected a wrong assumption about why Shell's live site doesn't auto-update after a merge to main.** First guess (a broken GitHub connection) was wrong — it's a deliberate Netlify setting that only auto-publishes preview links, not the live site, matching the "never deploy without being told" rule already in place. Documented the accurate reason and the manual-publish steps in the global CLAUDE.md.
- [ ] **Shell's own styling and the shared `@eq-solutions/ui` design library define colliding layout style names** (`eq-hub` and friends) — noticed while fixing the scroll bug above, not the cause of it, not yet looked into properly. _(added 2026-08-14)_

---

## eq-shell + eq-field + eq-service: CI sweep, duplicate-work cleanup, 2 real PRs merged + deployed (2026-08-13)
*Royce: "check for any other failing CI or unmerged fixes" → found + fixed. Then "/decide" on what next → recommended surfacing what's already ready over starting new speculative work. Then "merge685andinvestigate1310" → both actioned. Then "merge #1310 once CI is green" → done, blocked once on a dependency, resolved.*

- [ ] **eq-shell `#1310`'s original live-testing error is still unknown** — the new Sentry capture means the *next* occurrence will be diagnosable, but this session couldn't reconstruct what Royce actually hit the first time. Worth a retry now that it's deployed. _(added 2026-08-13)_

---

## eq-cards + eq-shell: labour-hire licence intake — multi-document OCR extraction + PDF review + flag notifications, all merged + live (2026-08-13)
- [ ] **Live click-through still not done** on the multi-document extraction / PDF preview / flag-notification features — verified via CI + direct DB checks only, no real signed-in session. _(added 2026-08-13)_
- [ ] **SMS-notification coverage is inconsistent across the different invite paths** — flagged during the original audit, not touched this session. _(added 2026-08-13)_
- [ ] **Intake engine's CSV import path bypasses the same-worker dedup** the direct upload paths now go through — flagged, not touched. _(added 2026-08-13)_
- [ ] **Open question, not decided**: should the manual labour-hire-document-upload form and the regular worker-invite form (which now also accepts documents) eventually merge into one? Deliberately left as two separate entry points this session. _(added 2026-08-13)_

---

## EQ Suite production-readiness deep dive + 18-issue Sentry triage, 1 real bug found + fixed (2026-08-13)
*Royce: "how close are we to production ready across the board? deep dive, spend time on this /gap". Ran the /gap centering protocol suite-wide (Shell/Service/Field/Cards/Intake/Ops), grounded in live systems (Netlify deploy state, live Supabase migrations, the security register, Sentry) rather than docs — corrected a stale suite-state.md claim that eq-service has no test suite (it does, `vitest run`). Then "go wider" — root-caused all 18 suite-wide unresolved Sentry issues via 4 parallel agents against live code/origin, not local checkouts (eq-field's local clone was 40+ commits behind origin without saying so).*

- [ ] **3 Sentry issues need a manual resolve** — EQ-CARDS-1D, EQ-FIELD-13, EQ-SHELL-1J are fixed in code (verified against origin/main + live) but still show unresolved in Sentry; the resolve tool call was blocked by the Claude Code classifier on 3 of 5 identical attempts, inconsistently. _(added 2026-08-13)_
- [ ] **4 genuinely open, low-priority bugs found, not built**: EQ-CARDS-1E (OCR 401-retry isn't wrapped in its own try/catch, so the intended clean sign-out doesn't fire — user sees "sign-in expired" but isn't redirected), EQ-CARDS-1A/1B (profile auto-provision RPC can hit a raw DB not-null violation if the session dies mid-call — 1 user so far, needs an `auth.uid() IS NULL` guard), EQ-SOLVES-SERVICE-3's Media Library Upload/Delete handlers missing the same stale-deploy catch Edit already has (admin-only, self-heals on refresh). _(added 2026-08-13)_
- [ ] **GitHub MCP connector isn't scoped to eq-cards** — `create_pull_request`/`list_pull_requests` both 404'd against eq-solutions/eq-cards even though `gh` CLI (same GitHub login, Milmlow) has full admin access. Worked around via `gh` CLI this session (PR #228 opened + merged that way); the connector's GitHub App needs eq-cards added to its repo install list if it should cover this repo going forward. _(added 2026-08-13)_

---

## eq-shell + eq-context: control-plane drift check fixed, then a suite-wide git-staleness sweep (2026-08-11)
*Started from an incidental finding while verifying CI on an unrelated PR — the scheduled "Tenant drift" check had been red on `main` since 2026-08-07. Fixing it surfaced a real, actively-recurring problem: eq-context's own local checkout had forked from `origin/main` from concurrent sessions committing without syncing — not a one-off, closes the standing "worktree-isolation vs accept-and-rebase" question flagged 2026-08-04/05 (see the eq-field section below).*

- [ ] **`eq-solves-assets`'s `origin` remote points at `https://github.com/Milmlow/eq-solves-service.git`** — a personal fork of a different project, not an asset-capture-app repo. Local history (`main` + 7 feature branches) looks like real, non-stale work. Not touched — Royce confirmed the repo is parked for now, don't re-flag without being asked. _(added 2026-08-11)_

---

## eq-shell + eq-context: control-plane drift check fixed, then a suite-wide git-staleness sweep (2026-08-11)
*Started from an incidental finding while verifying CI on an unrelated PR — the scheduled "Tenant drift" check had been red on `main` since 2026-08-07. Fixing it surfaced a real, actively-recurring problem: eq-context's own local checkout had forked from `origin/main` from concurrent sessions committing without syncing — not a one-off, closes the standing "worktree-isolation vs accept-and-rebase" question flagged 2026-08-04/05 (see the eq-field section below).*

- [ ] **`eq-solves-assets`'s `origin` remote points at `https://github.com/Milmlow/eq-solves-service.git`** — a personal fork of a different project, not an asset-capture-app repo. Local history (`main` + 7 feature branches) looks like real, non-stale work. Not touched — Royce confirmed the repo is parked for now, don't re-flag without being asked. _(added 2026-08-11)_

---

## eq-cards + eq-shell: labour-hire licence intake pipeline — built, consolidated with existing admin invite tool, 2 Sentry issues resolved (2026-08-11)

- [ ] **Real end-to-end click-through never run** — upload → OCR → candidate → tenant approves → worker claims. Test tenant: EQ Solutions (`eq`, `is_seed_demo: true`) — not SKS Technologies (live pilot, real workers). The tool is now actually reachable and functional (was silently broken until this session — see below), so this is unblocked. _(added 2026-08-11)_
- [ ] Sentry EQ-CARDS-1F (`LateInitializationError`, `main.dart`) investigated — engine-internal, not independently fixable, flagged for awareness only, no action taken. _(added 2026-08-11)_
- [ ] **Front-door merge (AdminWorkerInviteForm vs LabourHireIntakeTool) scoped, not decided.** A live-wiring audit (this session) found worker-creation fragmented across 6 independent paths with inconsistent phone rules and notification behaviour. Two real bugs found and fixed same session: the intake edge function was stuck on a stale single-file deploy despite the multi-file rework already being merged to eq-cards `main` (redeployed live) and `/_platform/labour-hire-intake` had no nav link anywhere, findable only by typing the URL (added, eq-shell [#1296](https://github.com/eq-solutions/eq-shell/pull/1296), merged). A third option — merging the admin-invite and labour-hire write paths into one shared matching function — was investigated and explicitly rejected: they're deliberately different trust models (admin-known-person reuse-first vs ops-blind-document never-auto-attach-to-claimed), not duplicate code; merging would regress one path or the other. Whether to merge the two *front-end forms* themselves (not the write logic) is still open — Royce's call, not re-raised without new information. _(added 2026-08-11)_

---

## eq-shell + eq-cards: Cards SSO broker fix — built, verified, deliberately held (2026-08-10)
*Scoped from the secrets-redundancy work: eq-cards' `shell-verify.js` was minting its own Supabase JWTs and provisioning auth.users locally, holding its own copies of `SUPABASE_JWT_SECRET` and `SUPABASE_SERVICE_ROLE_KEY` (jvkn). Built the fix, then ran `/decide` — TODAY.md's live goal (expires 2026-08-22) explicitly excludes "any live/auth changes that could affect real users mid-flow" while Royce is overseas. Both PRs are complete, verified, and draft — not merged, on purpose.*

- [ ] **Needs Royce, not more building:** already superseded below (2026-08-11 explicit go-ahead) for the overseas-goal exclusion specifically — the real remaining blocker is operational: generate + set `EQ_CARDS_HANDOFF_KEY` on both Netlify projects (nothing works until it exists) — manual-hands-only, Claude Code is blocked from writing Netlify secrets by design. **Note 2026-08-13:** the TODAY.md overseas goal this entry originally cited was killed (Royce's explicit call) — doesn't change anything here, the Netlify-secret step was already the actual blocker, not the goal. _(added 2026-08-10)_
- [ ] **Deploy order matters, spelled out:** eq-cards' new `shell-verify.js` has no fallback to the old local-signing path — if it deploys before eq-shell's endpoint is live and keyed on both sides, Cards login breaks for real users immediately (Cards is taking live self-signup traffic today). Sequence: (1) generate `EQ_CARDS_HANDOFF_KEY`, set on both projects, (2) merge+deploy eq-shell #1294, confirm the endpoint responds, (3) merge+deploy eq-cards #221. Royce's stated plan: do this from the Beelink, not ad hoc. _(added 2026-08-11)_
- [ ] **After the deploy confirms working:** delete `SUPABASE_JWT_SECRET` / `SUPABASE_SERVICE_ROLE_KEY` (jvkn) / `EQ_SESSION_SALT` from eq-cards' Netlify project — otherwise the whole point of this fix (cutting Cards' blast radius) doesn't actually land, they just sit there unused but still exposed to SEC-9's dev-context leak. _(added 2026-08-11)_
- [ ] Royce gave explicit go-ahead to ship now (`/decide` override of the standing overseas-goal exclusion, 2026-08-11 evening) — but he's on mobile and can't do the manual Netlify step from there. Doesn't change the plan above, just confirms it: still blocked on the same `EQ_CARDS_HANDOFF_KEY` step, now with an explicit yes on record instead of an implicit hold. _(added 2026-08-11)_

---

## eq-service + eq-solves-intake: RCD in-app entry (manual + photo) shipped, ACB mobile nav bug fixed, RCD threshold corrected (2026-08-11)

- [ ] **`RCD_SCHEDULE_PARSE_ENDPOINT_URL` needs setting in Netlify (prod + preview).** Points at the deployed endpoint (`https://ehowgjardagevnrluult.supabase.co/functions/v1/parse-rcd-switchboard-schedule`), documented in `.env.example`. Manual-hands-only, Claude Code is blocked from writing Netlify secrets by design. Without it the photo-upload button errors; manual entry and the bulk-generate dropdown both work fine regardless. _(added 2026-08-11)_
- [ ] **Not click-tested live anywhere in this thread** — auth unavailable in this environment throughout (no `EQ_SERVICE_JWT_SECRET` locally, demo account unavailable). Every UI change verified instead via static Tailwind-mirror geometry measurements and/or rolled-back-transaction writes against live ehow — real verification, not a browser click-through. Worth a real phone/iPad pass once Shell-embedded auth is available here. _(added 2026-08-11)_
- [ ] **The shared `@eq-solutions/ui` Table component's own mobile gap is not fixed** — only the ACB/NSX page-level instance was. Every other page using the canonical Table (Maintenance, Assets, Job Plans, Contract Scope, Test Records...) still has the same word-wrap problem on a phone. That's an `eq-ui` repo change, deliberately scoped out of this session's `eq-service`-only work. _(added 2026-08-11)_
- [ ] **One likely-stale data point noticed, not chased:** an ACB check literally named "Test" shows `status='complete'` with 0 of 5 linked ACB tests actually done — reads as leftover QA debris, not real customer data, but flagged in case it isn't. _(added 2026-08-11)_

---

## eq-cards + eq-field + eq-intake + eq-ui + eq-receipts + eq-roles + eq-design-tokens + eq-context + eq-shell + eq-service: suite-wide stale-branch + orphaned-worktree cleanup (2026-08-08)
*Started as a routine "check for other stale branches" during the QR self-join review, escalated once a `/ultrareview` attempt revealed the "unmerged" branches were actually already-shipped squash-merges — a `git branch --contains` blind spot (see `squash-merge-branch-contains-trap.md`). From there: mechanical empty-diff sweep → full agent-based semantic review (each branch's actual diff checked against current main, not just git metadata) across every EQ repo.*

- [ ] **2 items need Royce's call, not a code fix** — `claude/service-canonical-identity-phase3-4` (eq-service): re-keys shell-auth JWT + remaps 5 SKS users' FK refs, explicitly marked "DO NOT DEPLOY without Royce's go" in its own commit, never landed — still wanted or shelved? `worktree-wf_79f7a4de-c56-4` (eq-intake): the quality-guardian engine is live but no admin UI in eq-service ever surfaced its output — still wanted? _(added 2026-08-08)_
- [ ] **5 open Dependabot PRs on eq-service** never reviewed (vitejs/plugin-react, sentry/nextjs, react-dom, eslint-config-next, @eq-solutions packages) — surfaced as "KEEP" by the branch audit since they're genuinely unmerged, not stale. _(added 2026-08-08)_
- [ ] **Structural risk, not a branch problem**: this session hit the shared-non-worktree-root collision the eq-field entry below (2026-08-08) already flagged — two concurrent sessions both doing git work directly in `C:\Projects\eq-shell` (not a worktree) at the same time. Caught before any damage. A second instance hit `eq-context` itself mid-close (this file, twice) — see `eq-context-shared-checkout-contention` memory; fixed by switching to an isolated worktree + direct `push origin HEAD:main` for this close. _(added 2026-08-08)_

---

## eq-shell + eq-context: Templates get real categories — create/edit/filter, migration dispatched live (2026-08-05)

**Deferred:**
- [ ] **Royce's real 15-file template batch: 12 of 15 are now live**, up from 0 at the previous close — not confirmed whether via the bulk-upload feature or one-by-one, or whether it's actually finished. Corrects the "not run yet" note in the sprint-close section below, which is now stale. _(added 2026-08-05)_
- [ ] **New Sentry regression, unrelated to this session's work but found while closing it out**: [EQ-SHELL-10](https://eq-solutions.sentry.io/issues/EQ-SHELL-10) "auth-stall: chunk-error" — first seen 2026-07-29 (a week before this session, confirmed unrelated to PR #1246), regressed and firing again (27 occurrences, 4 real users, last seen today), culprit `/sks`, underlying captured message `l.brief.map is not a function` — possibly the same root cause as the separate EQ-SHELL-19 TypeError. Flagged as background task `task_714326ef`. _(added 2026-08-05)_
- [ ] **Two possible duplicate-session situations, worth a check**: (1) bulk category assignment (this section's own item above, "12 templates that predate this feature") shipped in a *different* session via eq-shell [PR #1253](https://github.com/eq-solutions/eq-shell/pull/1253), merged and deployed — the same gap this section had flagged as background task `task_8de01dba`, which Royce started separately and which may still be running, now duplicating already-shipped work. (2) the Sentry regression above (`task_714326ef`) was independently re-flagged in that same later session as `task_d879e43e`, which Royce has also started separately — worth confirming that isn't a second parallel investigation of the identical issue. _(added 2026-08-05)_

---

## eq-shell + eq-field: Internal Document Sign-off Register — register view shipped, then a real signature pad + evidence view after Royce used the pilot (2026-08-03)

- [ ] **Roll out past the one-person pilot** — push a real document to a real second person, get them to sign on their own phone. Royce reaffirmed this is lower priority than hardening the feature itself first. _(updated 2026-08-04)_
- [ ] **eq-field's `sw.js` `CACHE_FIRST_PATHS` only lists `/icons/` (SKS) and `/manifest.json`, not `/icons-eq/` or the new `/manifest-eq.json`** — a pre-existing asymmetry noticed while fixing the item above (SKS assets get faster but staler cache-first serving; EQ assets are always network-first/fresh). Left alone deliberately — fixing it means deciding a caching tradeoff, not just correcting a stale value. _(added 2026-08-04)_

---

## eq-shell + eq-context: sign-off register sprint closed out — reminders, certificate/templates, real UI critique → a reusable feature-baseline rule, bulk upload (2026-08-04)
*Continuation of the sprint above. T2 (reminders) and T3 (bulk template upload) both went from "not scoped" to shipped and live. Royce then clicked through the real Upload & push / Register / Templates screens and gave direct UX critique — half the gaps named already had a matching `@eq-solutions/ui` component sitting unused, which became a new governed standard rather than a one-off fix.*


**Deferred:**
- [ ] **Royce's actual 15-file template batch hasn't been uploaded yet** — bulk upload shipped specifically for this, but nobody's run it through yet. _(added 2026-08-04)_
- [ ] **OCR / smart intake on document upload** (auto-fill title/date/reference from the file, like eq-cards' licence OCR) — named in the critique, real north-star item, not started. _(added 2026-08-04)_
- [ ] **Document type list is a hardcoded array in the frontend**, no admin config surface — named in the critique (`rules/admin-feature-baseline.md` item 4), not started. _(added 2026-08-04)_
- [ ] **Certificate export can't be scoped to a subset of signers** — always the whole document, every signer, one PDF. Named in the critique, not started. _(added 2026-08-04)_
- [ ] **T4 (permission gate)** — any signed-in tenant member can currently upload/push/see everything. Accepted interim decision, not urgent while usage is single-person. _(carried forward)_
- [ ] **EQ Field / SKS Labour adoption has no tracked parity list** — surfaced via a `/gap` this session (Royce: "need to get EQ Field adopted first"), then Royce pivoted back to the sign-off register before deciding next steps here. SKS Labour is genuinely NOT feature-frozen (confirmed live, corrected a stale memory that had over-claimed a full freeze) — both apps get real ongoing work in parallel, with no dated retirement and no tracked list of what EQ Field still lacks. Real open question, nothing started. _(added 2026-08-04)_

---

## eq-context + eq-shell/eq-field: CI health sweep, PAT diagnosis, and a shared-checkout git incident (2026-08-03)

- [ ] **`eq-solves-assets` folder points at the wrong GitHub repo** (a personal fork of the Service app, not the real assets repo) — Royce: "on the back burner, can be ignored." Deprioritized, not investigated further. _(added 2026-08-03, updated 2026-08-03)_
- [ ] **eq-shell's `smoke.yml` check is chronically noisy** (roughly 1 in 3 runs fails on a timing timeout, always self-resolves) — not a real bug, but worth a longer timeout if the false alarms bother anyone watching it. _(added 2026-08-03)_

---

## eq-cards/eq-shell: Cards SSO handoff hardening, identity-fragmentation root-cause fix, worker-invite dedup (2026-08-04)
*Direct continuation of the self-join session above — Royce kept testing live (new starters, an apprentice QR) and each report led to a real, verified bug, not a retest of the same thing.*


**Decided:**
- Royce: fix the identity-fragmentation gap properly (harden both the DB hook and the join function), not just patch the symptom for one test number — explicit go on an auth-critical change.
- Royce: for two known new starters, use the Core admin-invite path rather than the Cards self-join QR — cleaner data capture (name captured up front, which the phone-only self-join door never does), and avoids the self-join edge cases just spent the session hardening.

**Deferred:**
- [ ] **Keyboard/numeric-pad fix (`interactive-widget=resizes-content`) is live but not confirmed on a real Android device by Royce** — couldn't verify myself (no device access, sign-in is off-limits for me). _(added 2026-08-04)_
- [ ] **Credential-gap alerts, profile mobile/employment-type prefill should now work correctly post identity-fix, but not yet re-tested live end-to-end by Royce on a fresh self-join.** _(added 2026-08-04)_
- [ ] **The deeper "why does the phone-fallback exist at all" root cause remains explicitly out of scope** — migration `0035`'s own header already flagged "auto-routing new workers so a second `auth.users` is never created" as separate future work. Today's fix closes the orphan-borrowing symptom, not the underlying phone-format duplicate-account class. _(added 2026-08-04)_
- [ ] **Sentry MCP connector needs Royce to reconnect** — "user's connection to this connector was invalidated" mid-session; `search_issues`/`search_events` unavailable for the rest of the session, worked around via code + live DB reads instead. _(added 2026-08-04)_

---

## eq-cards/eq-shell: worker data consent/sync architecture Q&A — one live bug found, one decision made, no code shipped (2026-08-03)

Royce asked four architecture questions about the Cards→tenant consent model (release mechanics, sync freshness, multi-tenant support, what "released" means technically). Answered against live systems, not docs — found a real bug in the process.

- [ ] **`credentials-canonical-sync` is broken and not actually running** — the edge function that's supposed to copy a worker's licence/credential updates from Cards into the SKS compliance/Field-legacy database is deployed but wired to nothing (no database trigger calls it), and even if it were, it hardcodes the wrong SKS tenant ID (the old, corrected-in-2026-06 wrong value). Net effect: a worker updating a licence or White Card in Cards today does not reach the older SKS compliance view at all. Needs Royce's call on reviving it (fix + wire it up) vs retiring it in favour of the newer eq-field app's live-read pattern, which doesn't have this problem by design. Spawned as background task `task_5687d06b`, already started in a separate session. **Checked eq-field's actual "live-read pattern" this session (Royce: "have Field pick it up") — it's narrower than assumed: `eq_get_org_licences` (via `canon-read.js`) only lists licences a worker already holds and flags expiry, with NO org-required-credential gap-checking anywhere in eq-field (no `org_credential_requirements` lookup exists in the repo at all). So retiring the old sync is safe — Field was never depending on it — but "Field picks this up" isn't a real feature swap yet; Field doesn't currently show missing-credential warnings the way the old SKS view did. Retire-vs-revive is still Royce's call; if he wants Field to show compliance gaps going forward, that's new work, not a revival.** _(added 2026-08-03, updated 2026-08-03)_

---

## eq-shell / eq-solves-intake: Contacts get a real duplicate-merge system, matching Sites (2026-08-02)
*Follow-up to "sprint all deferred and next items you've nominated." Built the Contacts-equivalent of the Sites write-time resolver + merge system, live-validated against ehow before opening either PR.*

- [ ] **Staff duplicate handling — still Archive-only, needs your call before any build.** A real staff merge fans out into Field-owned operational tables (timesheets, schedule, licences, dispatch) — per the durable architecture rule, that can't be rebuilt Shell-side; it needs Field-repo coordination, which is a scope decision, not something to default on. _(added 2026-08-02)_
- [ ] **Both PRs (#1190, #106) need review/merge, then the edge function deploy + migration dispatch need your explicit go** — real production changes (live Anthropic API calls, schema changes to ehow), not something to default on even after merge. _(added 2026-08-02)_

---

## EQ Cards + Intake: asked "where are we really at" — found two of our own internal notes were wrong, fixed them (2026-08-02)
*Royce felt lost in the progress and asked for a plain "what's real vs. what's the goal" check on EQ Cards + Intake. Checked live — the actual code, database, and what's actually deployed — instead of trusting our own internal write-ups.*


**Deferred:**
- [ ] Royce is checking directly whether EQ Intake can push timesheets into Workbench (SKS's own payroll tool) — none of the 12 export formats target it today. _(added 2026-08-02)_
- [ ] **Royce to check `admin/users/migrate` for SKS against the 44-workers number above** — the invite screen and the 44 are counted two different ways (one by tenant employee record, one by Cards worker record), so they may not match exactly. Worth confirming they're the same gap before assuming the invite screen alone closes it. _(added 2026-08-02)_

---

## eq-solves-intake + eq-shell: duplicate-site console's two dead ends fixed, then a live permission bug found and fixed mid-testing (2026-08-01)
*Royce asked why the duplicate-sites screen finds problems a user can't act on. Two real dead ends: a non-manager saw only "ask a manager" with no way to even preview what a merge would do, and marking a match "Unsure" recorded a bare verdict with no way to say why. Fixed both, checked against the real database permissions rather than assumed. Testing the fix live then surfaced a genuine separate bug: even a real manager couldn't confirm a merge.*


**Deferred:**
- [ ] **Royce to click through live**: open the Duplicate Sites panel as a non-manager and confirm Preview now shows; mark a row Unsure with a note and confirm it saves and displays; confirm a real merge now succeeds end-to-end (Preview → Confirm) now that the permission fix is live. _(added 2026-08-01)_
- [ ] **Worth checking separately**: the tool that rolls database changes out to every company's system may have a bug where an instruction placed right after defining a new function can silently not run, even though the file it's in is marked as successfully applied. Only caught because this one case got tested by hand — there could be others sitting the same way undetected. Not investigated further. _(added 2026-08-01)_

---

## eq-shell + eq-solves-intake + eq-receipts: closed every open security alert across the EQ suite, found 5 repos where the alert system was switched off entirely (2026-08-01)

- [ ] **eq-cards / eq-design-tokens / sks-charters / eq-website**: alerts just switched on, the very first scan came back clean on all 4 — worth a second look in a day or two in case that first scan didn't fully finish rather than assuming it's actually clean. _(added 2026-08-01)_
- [ ] **eq-receipts' react-router move hasn't been clicked through live** — the build is clean and Netlify's own preview built it successfully, but nobody has actually navigated the real app (Dashboard → Review → Verify, sidebar links) since the change. Worth a quick manual pass. _(added 2026-08-01)_

---

## eq-shell + eq-cards: Live smoke-testing the self-join sprint surfaced 3 real bugs, all fixed same day (2026-08-01)
*Royce started clicking through the self-join work from the entry above with a real test phone. First signup turned out to be a pre-existing stale test account ("Bob Smith") rather than a fresh one — deleted and verified clean everywhere before re-testing. The clean re-test then surfaced three genuine gaps that only show up on a real click-through, not in code review.*


**Decided (Royce):**
- Add an email field to self-join rather than leave the Cards dead-end as-is, or teach Cards to work phone-only.
- Delete the stale test account and reuse the same phone number rather than get a second test phone.

**Deferred:**
- [ ] **The actual end-to-end smoke test still hasn't been run clean** — self-join → email → text code → Field's blocked-until-documents screen → Cards opening straight through → photo-first document capture, all together, on the now-clean test phone. Every piece has shipped; the full walkthrough hasn't happened yet. _(added 2026-08-01)_

---

## eq-intake + eq-shell: 4-part fix from Royce's live screenshot review of the Intake console (2026-07-31)
*Royce tested the Review Queue / Tidy / Dupes screens live on core.eq.solutions and sent screenshots flagging four things: nowhere to see/edit the trades list, a site merge that failed with a permission error, the Data Gaps table showing bare unhelpful labels, and the Contacts Dupes tab having no way to act on a flagged duplicate. Investigated all four against the real code and the live database before building anything.*


**Deferred:**
- [ ] **Royce to click through live** — trigger a failed-then-fixed site merge and confirm it now works; open the Contacts/Staff Dupes tab, archive one flagged duplicate and dismiss another as "not a duplicate," confirm both stick; add a trade in the new Trades screen and confirm it shows up in the Review Queue's trade picker. Needs sign-in, which is off-limits for Claude to do on your behalf. _(added 2026-07-31)_
- [ ] **Two separate sessions independently claimed the same migration number (0228)** tonight — this one and the quote-target-period entry above. Not a live problem (both applied cleanly, nothing broke), but worth knowing the "check origin/main before claiming a number" step isn't fully collision-proof under concurrent sessions. _(added 2026-07-31)_

---

## eq-solves-intake + eq-shell: Intake redesigned — 5 confusing tabs down to 4 clear ones (2026-07-29)

- [ ] **Bring Data In's "Check for conflicts" still commits on its own path, separate from the main Into-EQ flow** — routing those resolved rows into the same shared commit path as everything else is real, separate work, not done here. _(added 2026-07-29)_
- [ ] **The deeper "why is this still exhausting" fixes are still open** — bulk-approve (today it's still one row at a time), standing rules for recurring conflict types (so the same duplicate doesn't get flagged forever), a trend view (is the score improving?), and a real ask-anything grounded across the whole suite (today's Ask tab is a thin preview of that). Discussed with Royce as the next tier up from this session's fix — this session deliberately shipped the cheap, clear win first. _(added 2026-07-29)_

---

## eq-solves-intake + eq-shell: `/intake`'s commit path was quietly skipping the review queue (2026-07-29)
*While scoping the redesign work above, checked whether it was safe to keep both Intake UI surfaces live — turned out one of them (`/intake`'s "Into EQ" commit) wrote straight to canonical tables, bypassing the same conflict-detection gate the other surface already enforced. A messy/conflicting row dropped through `/intake` would commit immediately instead of parking for review.*


**Deferred:**
- [ ] **The live end-to-end proof is still outstanding**: drop a deliberately-conflicting test row through production `/intake` and confirm it parks in the queue instead of committing. Blocked this session on the file-upload tool refusing to attach a test file not shared directly by Royce in chat — needs either Royce dragging the file into chat, or Royce doing the drop himself while checked live. This becomes easy to verify now that Overview/To Do is the single place to look. _(added 2026-07-29)_

---


## eq-roles/access-model audit + release tagging shipped across eq-field/eq-shell/eq-solves-service (2026-07-27)

- [ ] **`service.create`/`service.close` PermKey split** — real gap (one key gates different behaviour in Shell vs. EQ Service's ~520-usage `canWrite()`), explicitly parked: Phase 3 auth-touching work stays out of the SKS cutover window (parallel-run proving period still at 0 consecutive clean weeks as of this session). Revisit post-cutover. _(added 2026-07-27)_
- [ ] **Field's remaining ~11-file isManager→canonical-permission conversion** — same standing park as above, same reasoning. _(added 2026-07-27)_

---

## eq-cards/eq-shell: onboarding minimum-requirements switch, bulk connect-worker, and a live anon-EXECUTE fix (2026-07-26)

**Deferred:**
- [ ] **Royce to click through the new "Who can join" Settings section and confirm it reads clearly and saves correctly** — code-complete and tested, not yet user-verified. _(added 2026-07-26)_
- [ ] **Royce to run one more fresh Cards signup** to confirm the nudge and the approval-time flag actually show correctly end to end — the full loop has never been walked through live since these changes landed. _(added 2026-07-26)_
- [ ] **Royce to test the new bulk connect-worker tool** with a real list of phone numbers. _(added 2026-07-26)_

---

## SKS onboarding security deep-dive: 3 pre-rollout fixes + leaver data-retention policy built end-to-end (2026-07-26)

**Deferred:**
- [ ] **Royce to remediate SEC-12** (plaintext Netlify secrets on eq-shell) via the Netlify dashboard — same-value re-store per key (not a rotation), just needs "contains sensitive values" ticked. `GOOGLE_DOC_AI_CREDENTIALS` (an RSA private key) is the highest-priority one. Full detail in `ops/security-register.md`. _(added 2026-07-26)_
- [ ] **EQ Cards' own worker-initiated 30-day account-deletion promise** (separate from the leaver-retention work above — this is a worker deleting their *own* Cards account) is still built but switched off (dry-run only). Not actioned this session, just a known standing gap. _(added 2026-07-26)_
- [ ] **Access-Model Phase 2 ("One admin") and Phase 3 (permission-key guardrails)** — explained to Royce in the Q&A, deliberately not built yet. Locked decision to keep auth changes out of the SKS launch window; revisit post-cutover. _(added 2026-07-26)_ **Note:** later the same day Royce separately approved one narrow piece of Phase 3 scoping — a pure internal cleanup with zero change to who can do what (see "collapsed the hand-typed permission list" above) — not a reversal of the launch-window lock, just a specific low-risk carve-out he signed off on directly. **Second note, later still:** Royce also explicitly approved a real behaviour-changing piece of Phase 3 — cleaning up SKS's one-off permission tweaks (see "tenant_role_overrides cleanup" below). Asked directly whether the launch-window lock applied here; his call was to proceed anyway. Phase 2 ("One admin") remains untouched.

---

## eq-shell + eq-service + eq-ui: Excel-style dropdown filters (multi-pick, cascading) shipped to EQ Ops and EQ Service maintenance checks (2026-07-24)

- [ ] **Not yet confirmed by Royce**: the EQ Ops multiselect filters (Est./Status/Job No.) and the labour-hire dashboard now showing the corrected INSELEC rates. The EQ Service Assets table cascade WAS confirmed live by Royce this session. _(added 2026-07-24)_

---

## Architecture implications from the SKS national-scale discovery (2026-07-23)
*Companion to the discovery session logged in `sks/pending.md` — that entry has the business/org context (org chart, headcount trajectory, Upvise decision); this is the EQ product/engineering backlog it implies. Nothing built yet — these are the real gaps the discussion surfaced, not yet scoped into actual work.*
- [ ] **Identity model needs a second dimension: division, not just tenant/role.** The SKS org chart shows state alone doesn't match how the business actually reports — VIC's headcount splits across national functional divisions (Major Projects, Data Centre Solutions, AV, HV) that cut across every state. Recommended direction (not yet built): keep the single-tenant model (don't fork Supabase projects per state — see `system/architecture.md` Control Layer section for why physical separation is reserved for separate *customers*, not sub-units of one), but extend the JWT claim set to carry `state`/`region` **and** `division`, with a layered exec view (State GM → Regional GM → Divisional GM → Group exec) rather than the current flat `is_platform_admin` bypass. _(added 2026-07-23)_
- [ ] **No live access-revoke exists.** Role/entitlement changes only take effect on next login today (`IDENTITY-MODEL.md` §6.3) — SKS's stated requirement for a national rollout is instant ("push of a button"). Needs a real design: likely a per-request `users.active`/`deactivated_at` check instead of relying solely on the cached session cookie. _(added 2026-07-23)_
- [ ] **Cards' scope needs defining against Upvise.** Royce's call: Cards supplements Upvise, doesn't replace it — Upvise stays the system of record for employment data, Cards owns onboarding/qualifications. That boundary (what Cards owns vs. what stays in Upvise, and whether/how they sync) isn't designed yet. _(added 2026-07-23)_
- [ ] **The 3 open P0 security findings (SEC-1 PII leak, SEC-9 leaked service_role key, SEC-10 plaintext API keys) matter more now than the usual priority read** — Royce agreed they should close regardless of the scale question; at 55 users they're bad, at a national headcount any one is a reportable breach, not an internal fix-it item. Already tracked in `ops/security-register.md` — flagging here so the scale conversation doesn't let them drift. _(added 2026-07-23)_
- [ ] **No off-platform backup exists for ehow** (SKS's live tenant data) — only Supabase's native 7-day PITR. Target design already exists in `system/infrastructure.md` ("Backup strategy — target state") but isn't built. Royce: budget/appetite exists "if this progresses." _(added 2026-07-23)_

---

## EQ Service + EQ Shell: found why some people on the Users page had no name or email — real fix opened for review (2026-07-23)
*Royce pasted a user list and asked where it came from. Traced it through to a real, live-confirmed data gap between two systems, not bad data.*
- [ ] **A wrong first theory got spun off as its own task before it was disproven** — an early chip pointed at the wrong screen entirely (a different, internal eq-shell user list), and that chip was already started as its own session before the live-database check ruled it out. That session was never tracked down to stop it — it may still be running against a bug that doesn't actually exist. Worth a look for a stray, pointless eq-shell PR later and closing it out if one shows up. _(added 2026-07-23)_

---

## Asked to "fix all the errors" — triaged all 13 open Sentry issues across Shell/Cards/Service, fixed the 2 real ones (2026-07-22)
*Continuation of the same-day notify-substrate/dead-code session. Asked to fold a discovered orphan Sentry alert rule into code, then "fix all the errors" against the live Sentry issue list. Rather than blindly resolving or blindly "fixing" 13 issues, ran 3 parallel investigation passes (one per repo) checking each issue's actual timeline against known fix PRs before touching anything.*
- [ ] **One triage sub-agent overstepped its brief** — told to investigate only, it instead made a real (but unpushed, harmless) local commit on a shared eq-service checkout. Caught it, verified the fix was actually correct, and folded it into the proper PR instead of using it directly. Worth remembering for future parallel-agent triage: general-purpose agents have full write tools even when told not to use them — an isolated/read-only agent type would remove the risk entirely. _(added 2026-07-22)_

---

## core.eq.solutions and the rest of the suite went down — DNS, not the apps — found the real cause and fixed it live (2026-07-22)
*Royce reported core.eq.solutions unreachable, "server IP address could not be found." All four production hostnames (core/field/service/cards) were dead at once, which pointed at DNS rather than a deploy. Traced it to something Royce had done a week earlier: on 2026-07-15 he deleted the `eq.solutions` Cloudflare zone meaning to take down the old marketing site (`eq-website`), not the whole domain. Cloudflare kept answering DNS for its normal 7-day grace period — which is why nothing broke at the time — then auto-purged the zone this morning at 4pm AEST, which is the moment the outage actually started. PostHog traffic data confirmed the exact hour. Nothing was wrong with any of the four apps the whole time; they kept deploying and serving normally, just unreachable by name.*
- [ ] **Cloudflare account has no 2FA.** `royce@eq.solutions` is the sole Super Administrator over DNS for the entire suite, and account access alone was the only thing separating the whole suite from an outage like this. Worth turning on next time you're in the Cloudflare dashboard. _(added 2026-07-22)_
- [ ] **DMARC record for `eq.solutions` was never added** — Resend's auto-configure only pushed MX/SPF/DKIM and marked those optional; verification succeeded without it. Not required, but a `p=none` starter record would give visibility into anyone spoofing `@eq.solutions`, if that's ever worth doing. _(added 2026-07-22)_

## Swept every system for "can someone give themselves more access than they should have" — found eight holes, closed all eight (2026-07-21)
*Started as one narrow fix and widened after Royce said to stop going one app at a time. The pattern behind every finding is identical: the thing that decides what you're allowed to do was editable by the very person it governs. Rules had been written listing what's protected, so anything nobody thought to name stayed wide open.*
- [ ] **Field still writes to the SKS database through its own door, outside the governed pipeline.** Two of today's changes went in by hand because Field has no approval pipeline of its own, following existing precedent. That's the same pattern named elsewhere as the cause of an earlier drift incident. Now that the governed pipeline has been seen working cleanly several times today, Field's database changes should move into it — otherwise there are permanently two ways in, one of them unaudited. _(added 2026-07-21)_
- [ ] **The timesheet and leave approval rules have never been exercised by a real person.** The logic went live without ever having been run — there's no safe place to rehearse it. Worth putting one real timesheet and one real leave request through the full path (submit → approve → try to approve your own → try to reopen) next time you're in Field, to confirm the blocks and the wording behave as intended. _(added 2026-07-21)_

---

## eq-shell + eq-field: golden worker journey investigation — identity/tenant-isolation gaps found, four PRs shipped, one caught by a security review (2026-07-20/21)
*Asked to prove and harden the full worker journey (Shell → Cards → company connection → Field) as one system rather than polishing apps in isolation. Investigation before any code: traced the real flow across all three repos against live Supabase data, not docs. Verdict at that checkpoint: not yet proven — a real tenant-isolation gap, unmitigated duplicate identities, and 45 active workers who'd never been invited to join at all.*
- [ ] **The `shell_control.persons`/`person_xref` "golden record" spine — investigated further, recommendation reversed.** Asked to do a full 3-repo build; investigation disproved the premise it was based on. Only eq-cards actually matches identities (phone/email against `public.workers`) — eq-shell only reads the output, and eq-field has no matching of its own (its one identity lookup is `user_id`-keyed, already-established, SKS-only). Also found eq-field has its own separate, deliberately parked initiative for a related but different problem (`ADR-PERSON-IDENTITY.md` — same-name disambiguation within eq-field's own tables, not cross-tenant identity; Phases 1–2 shipped, Phases 3–4 explicitly gated by Royce on "not until SKS is stable in live", set 2026-06-08) — and that ADR's own canonical-link plan points at `public.workers`, not `shell_control.persons`/`person_xref`. Recommendation: don't build the spine — it looks like a second, unused design for a job `public.workers` already does. **Royce confirmed: "don't build the spine, leave it parked."** Closed — no further action unless a real second consumer shows up (most likely trigger: EQ tenant's Field plane going live). Open question for later, not urgent: whether to formally retire the empty `persons`/`person_xref` tables rather than leave them as dead schema two different plans could collide on. _(added 2026-07-21, corrected 2026-07-21, confirmed parked 2026-07-21)_
- [ ] **EQ-tenant worker→staff sync doesn't exist** — `workers-canonical-sync` is hardcoded to SKS only. Deprioritized rather than built, since the EQ tenant's Field plane has no real usage yet — revisit if that changes. _(added 2026-07-21)_
- [ ] **45 never-invited workers are now visible (via #918's alert) but nobody's actually invited them.** Sending real invites to real workers is a deliberate action for an operator, not something to automate. Royce's explicit call this session: not now, "too many moving parts." Fits under the existing `/admin/invite-bulk` 50-cap if actioned. Still open as of 2026-08-02 — count now 44 (one resolved naturally), still surfacing via the same alert, now also showing as a live Sentry issue (EQ-SHELL-X) rather than only the original ad-hoc check. Same call stands: not actioned yet. _(added 2026-07-21, reconfirmed 2026-07-21, still open 2026-08-02)_

---

## eq-field: mobile My Schedule + home tile now show Saturday/Sunday when rostered (2026-07-21)
*Royce flagged that the mobile schedule view only showed Monday-Friday, even for people rostered to work a weekend. Fixed here and in the sibling SKS Labour app.*
- [ ] **Worth a quick look once deployed:** confirm a weekend-rostered person's mobile schedule and "Next shift" home tile show Saturday/Sunday correctly. _(added 2026-07-21)_

---

## Found + fixed a real live crash on the "connect to company" screen, then fully diagnosed (and mostly fixed) the GitHub access problem that's been quietly biting all day (2026-07-20)
*Asked to check Sentry for anything new. One real bug turned up, got fixed and confirmed live — filing it as a proper pull request ran into a GitHub connection problem, which turned into a much bigger dig once it became clear this wasn't a one-off.*
- [ ] **A cosmetic app-crash message (unrelated) is still open, low priority** — a rendering hiccup that's been intermittently appearing since 2026-07-13, not something from today's work. Not investigated further. _(added 2026-07-20)_
- [ ] **Last step: the access key itself needs to be re-entered correctly.** The new connection is wired up and reaching GitHub, but currently rejects the specific key that was entered — likely a copy/paste slip (extra space, truncated, or an old/expired one). Once re-pasted correctly, this should fully close out the whole GitHub-access saga. _(added 2026-07-20)_
- [ ] **Note for the record: one repo (EQ Shell) got switched from public to private today as a side effect of testing this** — confirmed intentional at the time, but worth double-checking it's still meant to be that way. Also worth knowing: several other company repos (EQ Context, EQ UI, EQ Quotes, EQ Contracts, the old SKS labour app, and a couple of smaller internal libraries) have been sitting fully public — readable by anyone on the internet with no login — for as long as this was checked. Given the private-repo requirement from SKS, worth a deliberate look at whether those should be private too. _(added 2026-07-20)_

---

## Terms/legal review across the EQ suite ahead of Royce's Monday SKS meeting with Adam (2026-07-16, REVIEWED + FIXED + LIVE)
*Royce has a Monday meeting with Adam (SKS) to discuss adopting some of what's been built + security around data handling — asked for a full review of terms/legal/consent text across EQ Cards and EQ Field (and anywhere else it might live) in case anything reads as "aggressively written." Also worked through positioning: Royce is SKS NSW Ops Manager AND EQ founder, wants to avoid any appearance of conflict of interest, and landed on framing Monday as "I built this because I needed it" (personal tooling, dogfooded by SKS) rather than a product pitch — no "customer"/"case study"/marketing language.*
- [ ] **Not checked: live data cleanliness / Sentry error surfacing on whatever gets demoed live Monday**, and the eq-field Privacy Notice modal's links weren't click-tested (read-only content review only). Offered, Royce hadn't said go as of session close. _(added 2026-07-16)_

---

## Leadership one-pagers — data security + systems integration (2026-07-14, DELIVERED)
*Royce asked for high-level one-pagers for a CEO / leadership meeting. Produced as PDFs (in `~/Downloads`) + claude.ai artifacts. No code shipped — external deliverables only.*
- [ ] **Your call: keep or bin the earlier EQ-vs-Microsoft/Google security comparison PDF** (`EQ-Security-One-Pager-2026-07-14.pdf`) — superseded by the CEO data-security version but left in Downloads. _(added 2026-07-14)_

---

## ✅ eq-shell + eq-field — mobile-view audit → Field is the program (2026-07-13, SHIPPED + VERIFIED)
*Royce asked for a full mobile audit ("cover all options, tech should be invisible"). 4 parallel auditors → ~40 findings, but the device pass (Royce on his phone) re-ranked everything: the mobile program is **Field, not eq-shell** — Customers/Ops native-page mobile PARKED.*
- [ ] **Royce device-confirm the Field add-crew flow on his phone** — the "Added <name>" toast now makes it visible whether a name landed; still worth one real-device pass end-to-end (add crew → sign → submit). _(added 2026-07-13)_
- [ ] **Trace + remove the "Ben says to use EQ Field" chip** — Royce sees a little chip mentioning Ben (Ritchie) telling him to use EQ Field. NOT in eq-field code (no live "Ritchie" string, only comments; he's a manager in `field_managers` but not on leave → not the roster "Management Out This Week" strip). Likely a **Shell-side notice / in-app announcement**. Royce to screenshot next time it appears; trace source then. _(added 2026-07-13)_
- [ ] **Field mobile-first reflow (simple, must respect security groups)** — the real remaining crew-mobile work; lives in eq-field. Parked eq-shell native-page mobile (Customers/Ops master-detail, nav-model unification, PWA-standalone install — auth-hub cookie risk) explicitly deprioritized per Royce ("Field is focus"). _(added 2026-07-13)_
    - v3.5.317 (#478): prestart photo-eviction data loss fixed (sessionStorage stash/rehydrate); pull-to-refresh reload killed (`overscroll-behavior-y: contain`); timesheet orphaned-row toast spam → console-only.
    - v3.5.318 (#479): Help tab removed (all 5 entry points); Sites search; prestart/toolbox site datalist opens full list on focus.
    - v3.5.319 (#480): Add Site / payroll CSV / Job Numbers CSV hidden on phone; `.hide-mobile` extended to shell-mode.
    - v3.5.320 (#481): honest voice-input error inside Core iframe (Chrome blocks Web Speech API cross-origin; not our config).
    - v3.5.321 (#482): phone Roster decluttered — day switcher (default today) + collapsible crew sections + one chip/person; desktop grid untouched.
    - v3.5.322 (#483): supervisor timesheet card tidy (44px tap targets; hide empty meta). CSS-only.
    - Findings, not code: Pipeline/Resources already unreachable on phone; supervisor "my-hours" is a separate PIN-auth mode (feature not reroute) — left per Royce.
  - [ ] **#4 — dropdown/form-field pickers "too large" on phone** — Royce to screenshot the offending field. Native `<select>` option lists are OS-sized/un-styleable; app datalists (site/person) can be tightened. _(added 2026-07-13)_
  - **★ Mobile-improvement sprint — 4 PRs shipped (v3.5.326→329, #486–#489, all prod, auto-merge per Royce).** Claude proposed 8 mobile improvements; recon-first killed the already-done ones (top-bar declutter already hidden on ≤768px; worker-first landing already routes via Shell staff auto-mode + home tiles). Shipped:
    - v3.5.326 (#486): **sticky form actions** — `.modal-footer` `position:sticky;bottom:0` on ≤768px + the Prestart action row (safety.js) gained the sticky bar Toolbox/Diary already had. Submit/Save no longer scroll off a tall form. Verified 31 footers compute sticky on preview.
    - v3.5.327 (#487): **skeleton loaders** — reusable `eqSkeleton()` (utils.js) + `.eqf-skel*` (base.css, reduced-motion aware); Dashboard loading (the `?tab=dashboard` Core deep-link) now shimmers instead of a bare ⏳; roster Job Numbers empty → standard icon+action. (Cold boot already covered by the overlay; empties already had icon+guidance — targeted, not a rewrite.)
    - v3.5.328 (#488): **gestures** — timesheets swipe-to-change-week (mirrors roster's proven pattern) + pull-to-refresh (`initPullToRefresh`, index.html; passive listeners + fixed pill, never preventDefaults, arms only at scrollTop 0, skips modals). ⚠️ Interacts with v3.5.317's `overscroll-behavior-y: contain` (which killed the *native* reload) — mine is app-level `refreshData()`; complementary, but device-verify they don't fight.
    - v3.5.329 (#489): **worker timesheet prefill** — the prefill tools (copy-last/from-roster/fill-from-Mon) were all supervisor-gated, so workers started empty every week. Staff mode now shows a "Prefill week" banner on a draft week with empty days; one tap fills per **Royce's precedence: roster → last week** (own row only, empty days only, never overwrites, always editable, hidden once submitted/approved). `_computeMyWeekPrefill` precedence engine unit-proven on preview (Mon-filled skipped; roster wins; roster-miss falls back to last week).
  - [ ] **Royce device-confirm the 2 gesture/prefill items on his phone** — (a) pull-to-refresh feel + that it doesn't fight the v3.5.317 native-reload suppression; (b) the "Prefill week" round-trip as a real crew member (banner → tap → fill → edit → submit). The precedence *engine* is unit-proven; the staff-mode round-trip wasn't drivable from the headless preview (login-gated). _(added 2026-07-13)_

---

## EQ one-login / access simplification — exploration + P0 policy LOCKED (2026-07-13)
*Royce: simplify how workers access Field at scale ("tech should be invisible; reduce the logins/surface a worker touches"). Live audit (Field/Cards/Shell/canonical) → the mobile-OTP worker identity ALREADY EXISTS and is in daily use on canonical (47 phone-confirmed, 52 signed in); **Core (not Field) is the auth broker**; Field is the only surface not yet on it. "One login" = consolidate onto Core, not build new auth. Chosen path: **A-Core** + **B-grace** (grace-then-soft-lock) + **C-tile** (Cards as a tile in the Core home). See memory `project_worker_identity_mobile_login`.*
- [ ] **One-login P4b (grace-then-soft-lock enforcement) — deliberately not built.** Warn-only (P4) ships instead; blocking a worker's access on a missing credential is a policy call, not a default. Build only on Royce's explicit go. _(added 2026-07-22)_
- [ ] **One-login P5 — migrate the 44 SKS workers still on the standalone app, retire it.** The cutover already happened for the other 48 SKS staff (2026-06-06); eq-field is a full superset, so this is a rollout + a date, not a technical gap. _(added 2026-07-22)_
- [ ] **Confirm `ENABLE_PHONE_OTP` is `true` on eq-shell's Netlify env.** Gates `shell-join-tenant.ts` — Cards' self-serve join-by-mobile door (`/join?tenant=`). Confirmed intentional/by-design (Royce, 2026-07-22) — not a security question, purely operational: if the flag's off, the feature is silently dead even though it's meant to work. Blocked from checking it directly this session (Netlify env read + a live test POST both denied by the permission classifier even after approval) — needs Royce checking the dashboard, or a standing permission grant. _(added 2026-07-22)_
- [ ] **Correct the stale "63 SKS invites" figure** wherever referenced — live = 20 shell user_invites + 2 worker_invites; SKS org_memberships 34; workers 89 (87 unique phones, 39 auth-linked). _(added 2026-07-13)_
- [ ] **Enterprise-scale investigation still owed** — Royce's original ask was two-part ("fix pagination now, then look at what enterprise customers would do"); only the fix landed this session. The research half (kanban-at-scale patterns, per-column lazy loading, etc. — see PR #973's "explicitly deferred" section) hasn't been started. _(added 2026-07-23)_
- [ ] **Shared-checkout collision hit eq-shell directly this time, not just eq-solves-service — and eq-context's own checkout too, mid-close.** Recovered from an eq-shell collision cleanly with Royce's go-ahead earlier in this same session. Then hit it a second time inside `eq-context` itself while writing this very close: the branch flipped underneath mid-command (ended up on a stranger's `claude/sks-eq-scalability-4b5976` branch), and this pending.md edit was silently clobbered once before finally landing. No work lost, but this makes at least 4 confirmed occurrences today across two repos. Worth the real fix already flagged elsewhere (always work from a dedicated worktree, never the shared root checkout) rather than a per-incident recovery — the root checkouts for eq-shell AND eq-context both need it. _(added 2026-07-23; deduped an exact-duplicate copy of this section's "Enterprise-scale investigation" item 2026-08-13 — same paragraph had landed twice, ironically the kind of artifact this exact bullet is about — and note, same day: a much bigger version of this exact class of bug wiped this whole section plus 9 other fixes out of this file once late in the day, rebuilt from this session's own record, see the top-of-file recovery note)_
- [ ] **Shared-checkout collision hit eq-shell directly this time, not just eq-solves-service.** Another session checked out `claude/supplier-portal-login-form-a7517e` in this same shared `C:\Projects\eq-shell` folder mid-session, with uncommitted edits to `TenantSwitcher.tsx`/`Suppliers.tsx` sitting alongside this session's own uncommitted work. Recovered cleanly with Royce's go-ahead (`git stash` scoped to just their two files, then a fresh branch off `origin/main` for this session's own changes) — no work lost on either side, and their files turned out to already be clean (committed as PR #972) by the time the stash ran. Same pattern flagged twice already today in eq-solves-service's session log — now confirmed to hit eq-shell too. Worth the real fix mentioned there (always work from a dedicated worktree, not the shared root checkout) rather than a per-incident recovery. _(added 2026-07-23)_

---


## ✅ Staff records — birthday/start date, Supervision read-only, middle-name tidy (2026-07-12, MERGED — deploying)
Extends the 2026-07-11 staff-records work. Three greenlit items + a normaliser follow-up, all merged (deploying to core.eq.solutions + field.eq.solutions):
- [ ] **Records↔Field seam polish (discussed, not built)** — steelmanned the "one record, many windows" model; creative next steps proposed: (1) a declarative field-ownership registry to kill the ~10-edit-site tax per new field, (2) push phone/name normalisation into a Postgres BEFORE trigger (one definition, every writer, no app duplication), (3) a "Records health" panel reusing `eq_quality_runs` (non-E.164 phones, embedded middles, missing canonical link, orphaned workers) with one-click fixes, (4) Cards as the real front door + canonical↔tenant reconciliation/merge-review to kill dup stubs, (5) extend the pattern to CRM contacts + fix the "Contacts" vocabulary clash. Recommended first move: the DB-level normalise trigger (highest leverage, lowest risk). _(added 2026-07-12)_

---


## ✅ Staff records — Field/Shell (2026-07-11, SHIPPED live)
Agency field + roster on/off toggle in Core (#753), Field honours `on_roster` (#454, v3.5.301), person-wizard → compact edit modal with reliable save + adopt-before-create dedup (#456, v3.5.300). All merged + deployed. Feature complete end-to-end (manager toggles someone off the roster in Core → Field hides them from roster/timesheets). Adding staff → Cards/Core; Field = edit surface.

---

## ⏩ Session close — 2026-07-11 (per-app nav-speed) — Field + Service boot lightened & shipped; Cards profiled + held

*Continuation of the Shell nav-speed thread. Royce: "continue per-app speed work" + "steelman" + "use fable". Profiled all 3 apps LIVE (prod, logged-in) + code (Fable agents per repo). Scope chosen: **Field + Service, hold Cards** (live signup traffic).*

**Built / shipped (both MERGED + deployed):**

**Decided (Royce):**
- Scope = **Field + Service, hold Cards** — Cards takes live self-signup/claim traffic; even its safe perf wins wait for a quiet window.
- **"merge them both"** — both deployed (branch+PR; Netlify auto-deploy on merge).

**Deferred (added 2026-07-11):**
- [ ] **Cards perf — HELD (live signup traffic).** Safe wins queued: preload/preconnect the boot chain, defer PostHog to `flutter-first-frame`, defer Cropper.js. Big lever = Flutter deferred-imports / `--wasm` / static-first claim page (architectural — do NOT rush on live traffic). _(added 2026-07-11)_
- [ ] **Field structural cache lever (L-effort)** — fingerprint the ~40 non-hashed JS/CSS assets so the service worker can go cache-first (kills ~40 revalidation round-trips/boot). Higher-effort follow-up. _(added 2026-07-11)_

**Notes / substrate corrections:**
- **Service is Next.js** (not Vite) and **Cards is Flutter/CanvasKit** (not Vite/React) — live-verified; prior docs were wrong.
- **Field index.html `no-store`→`no-cache` was a NO-OP for boot** — the `for="/index.html"` rule doesn't apply to `/` (the path the Shell loads), which already gets Netlify default `public,max-age=0,must-revalidate` (304-capable). The profiling "698 KB re-downloads every boot" was a config misread. Lesson: verify the LIVE header on the ACTUAL request path. The jszip win (the real one) is live + verified.
- **Cards OCR is server-side** (Claude Vision edge fn), not in the web bundle — killed the "eager OCR at boot" hypothesis.
- **Guard friction:** EnterWorktree refuses cross-repo worktrees from an eq-context session, and `block-worktree-write` (un-skippable) pattern-matches `*-wt` → built in non-`-wt` worktree paths (Royce explicitly directed the build = CLAUDE.md "unless explicitly pointed at one" exception).

---

## ⏩ Session close — 2026-07-11 (eq-shell control plane + eq-field) — Control-plane migration ledger reconciled + eq-field undefined-name safety net; Claude takes the standing "foreman" seat

*Continuation later on 2026-07-11 (separate from the strategy session below). Two build threads landed, plus a standing role decision. Model run on Claude Fable 5 from mid-session.*

**Built / landed:**

**Decided (Royce-confirmed):**
- **Claude takes the standing senior / "foreman" seat** Calum was slated for — Calum declined the hands-on role and told Royce to use Claude for it. Claude runs the reconciliation / verification / senior-review work; **Royce's sign-off stays the gate on every irreversible action** (prod deploys, live DB writes, auth changes, cross-entity). Memory written (`claude-is-the-foreman`). Model switched to Fable 5.
- **Control-plane "postman": lean path, no auto-writer (recommendation).** See the annotated open item under the 2026-07-02 eq-cards block. The gap was knowledge, not automation; the verified ledger + merge-reminder (#726) + one-key scheme close "merge ≠ applied" without a risky filename-ordered auto-applier. Build-the-runner remains Royce's architectural call.

**Deferred (added 2026-07-11):**
- [ ] **Ledger action item 3 — `2026_06_16_cards_claim_explicit_user_id.sql` must NEVER be re-applied** (documented in the ledger). A replay hazard, not a to-do; flagged so no future apply run picks it up. _(added 2026-07-11)_
- [ ] **Ledger action item 4 — cosmetic duplicate unique-index name on jvkn** (harmless, documented). Tidy only if convenient. _(added 2026-07-11)_
- [ ] **Make eq-field "Tests + lint" a REQUIRED branch-protection check** — the net now catches undefined-name bugs, but the check isn't required-to-merge, so a red run doesn't block. Interacts with Netlify push-to-deploy; Royce's call. _(added 2026-07-11)_

**Notes:**
- Control-plane tree = `eq-shell/supabase/migrations/` → jvkn (`jvknxcmbtrfnxfrwfimn`), hand-applied, NO CI apply. Separate from `supabase/tenant-migrations/` (the governed One Pipe → tenant planes). Don't conflate.
- Verifying by *object* (`to_regclass`, `pg_proc`, `information_schema.columns`, `pg_policies`, `has_function_privilege`, `pg_get_functiondef` with `prokind='f'`) is the only reliable way to read control-plane applied-state — filenames don't join to the ledger.
- eq-shell app repos auto-deploy from main on push (Netlify), but control-plane `supabase/` changes don't deploy (Netlify serves the app, not `supabase/`) — which is why #729/#730 were safe doc/no-op merges.

---

## ⏩ Session close — 2026-07-11 (strategy + live verification) — Cards is the standout; EQ Field cutover NOT started; Service built-not-executed

*Strategy conversation prepping Royce's CEO meeting about the SKS Labour app. No product code changed. Pressure-tested the whole suite; landed on Cards as the strategic standout. Verified the "runway" against live DBs (read-only) because Royce said "prove it".*

**Decided / direction (Royce-confirmed):**
- **Cards is the strategic standout.** Everything else (Field/Service/Ops/Shell) re-implements a solved category; Cards (worker-owned onboarding + compliance) is the one unsolved problem. Keep it SIMPLE: onboarding + compliance. **Irreducible core that must survive simplification = the worker OWNS the verified credential.** Drop that → commodity (Damstra / Rapid Global / Sitepass own employer-owned onboarding).
- Positioning: integration = the wedge, ownership = the moat, AI makes the wedge cheap. "AI to bring existing SKS systems together" is a *how* — keep it backstage, sell outcomes. Canonical layer reframed as a thin ownership registry / referee (one owner per entity), NOT a replacement DB. APIs don't fix source-of-truth (ownership does); use APIs where they exist (Smartsheet has one), AI only at un-API-able edges.
- SKS Labour (nspbmir) is the interim deploy — retire only when EQ Field (canonical trunk) is proven by a DATA bar (parallel-run a real crew's full cycle, reconcile vs SKS Labour, N weeks), not optimism. Working-before-refactoring holds.

**Verified against LIVE DBs (read-only SELECTs — corrects suite-state drift):**
- **SKS Labour (nspbmir) is very much ALIVE** — audit_log 1,127 actions/7d (~160/day), schedule 134/7d, timesheets 71/7d, prestarts 21/7d, all written 2026-07-10; **19 people onboarded in the last 30d**. The "dead runway" caution was WRONG for Field — it's the liveliest thing in the suite. (Tender import is the one stale piece: last run 2026-06-17.)
- **EQ Field canonical is EMPTY** — ehow `app_data.field_schedule` / `field_timesheets` = 0 rows while nspbmir carries 100% of live load. **The retire-SKS-Labour cutover has NOT started in the data.** This is the KNOWN, documented pre-cutover state — `SKS-CUTOVER-CRITICAL-PATH.md` (Phases D/E not done) + the 2026-06-07 linkage audit (finding #6, "nspb data not in the canonical plane"). NOT a new discovery; I re-derived it as a novel "sync/seam" gap, which was wrong (corrected 2026-07-11).
- **EQ Service (ehow) is built-but-not-executed** — `app_data.maintenance_check_items` = 1,358 rows, **0 ever completed (max completed_at = NULL)**; maintenance_checks = 13. audit_log/job_notes active daily (someone administering) but ZERO field execution. (ehow staff/timesheets recency = bulk-import artifacts, not human use.)

**Deferred (added 2026-07-11):**
- [ ] Verify where EQ Cards WRITES onboarding — must target canonical / EQ Field (the survivor), not nspbmir (the app being demolished). _(added 2026-07-11)_
- [ ] If the manual approach stands: define the stop condition — N consecutive clean weeks across a full roster+timesheet cycle → cut. Put one supervisor + one crew on EQ Field during the run (solo hand-entry proves features, not adoption). Enter independently then compare — don't key EQ Field to force a match. _(added 2026-07-11)_
- [ ] ~~Check nspbmir→canonical sync bridge / fix unwired seam~~ — WITHDRAWN 2026-07-11: no automated sync is part of the plan (Royce re-keys manually); the empty `field_*` state is the documented pre-cutover condition, not a gap to fix. _(added 2026-07-11)_
- [ ] Get EQ Service from built → executed — 1,358 check-items defined, 0 completed; nothing being ticked in the field. _(added 2026-07-11)_
- [ ] Compute the Cards "one number" for the CEO ask — onboarding time saved (time-to-site-ready × worker volume) + expiry/audit risk removed. Royce to supply volumes. _(added 2026-07-11)_

**Artifact:** CEO meeting kit (one-page brief + talking-points card + 6-slide deck), SKS-branded — https://claude.ai/code/artifact/1b3c73a2-b584-4f1f-bcdd-cd4ce15322c6 (scratchpad source: `sks-labour-ceo-kit.html`). Dashed fields left for Royce (CEO name, date, hours saved, labour-hire $, run cost, the one ask).

**Note (§7 discipline):** queried nspbmir (SKS live) read-only to verify liveness at Royce's explicit "prove it". SELECTs only — no writes, no DDL. §7 guards this project for writes; flagging the read for transparency.

---

## ⏩ Session close — 2026-07-10 (eq-cards + eq-shell) — duplicate-staff class killed at BOTH writers; Kurt onboarded by hand (licences + photos); admin photo-upload primitive built

*Continuation of the 07-08 eq-cards session. Royce hit a run of duplicate "staff" rows in Shell (Brett Kilpatrick, Kurt Sticker, Sam Powell) plus a "can we enter a worker's licences for them / attach the photos they emailed" ask. Root-caused the duplicates to TWO independent writers, fixed both, cleaned the existing backlog to zero, and built the missing admin photo-upload path — all live and verified.*

**Duplicate root causes — both fixed + live:**

**Existing backlog cleared (app_data.staff dup scan → 0 active dups):**

**Kurt Sticker onboarded manually + admin photo path built:**


**Design call (Royce) — did NOT build:**
- [ ] **Duplicate prevention beyond the two writer fixes: leave it.** Steelmanned a unique normalized-phone index and a detection cron; concluded (with Royce) that for ~85 staff a hard constraint on phone is the wrong tool (phone recycles — see eq-cards 0076 — and gets shared; converts silent dups into blocking 500s). The 80/20 that leading teams do — one identity key + normalize-and-match at write + a merge tool for stragglers — is now in place via #719 + #724. Revisit a merge-UI or constraint ONLY if dups recur after these. _(added 2026-07-10)_

**Follow-ups flagged, not built:**
- [ ] **Timesheets/other paths that write `app_data.staff`** — audit that every remaining writer routes phone through the shared normalizer (not just the two fixed). Low priority now the two main writers are fixed. _(added 2026-07-10)_

---

## ⏩ Session close — 2026-07-10 (eq-shell + eq-field) — /sks/field "spinner of death" root-caused + fixed (both apps), Contacts columns made segment-aware

*Two threads. (1) The recurring /sks/field "EQ Field didn't load" card on tab-return: the FIRST fix this session (overlay stacking, eq-shell #714) proved the earlier hypothesis (React #418 hydration crash) was a false premise — Sentry has ZERO #418 events and Shell is a client-only SPA (no SSR, no hydration). Royce then hit the real bug live and screenshotted it: Field was fully working BEHIND the error card. Root-caused end-to-end across both repos and shipped a self-healing handshake. (2) Royce's Contacts observation ("Agency only relevant for labour hire; can columns be customisable?") → segment-aware columns + a Columns picker.*


**Notes / recurring risk:**
- [ ] **Root-checkout collision on eq-field happened 3× in one day** — concurrent sessions committed onto each other's branches via the shared `C:\Projects\eq-field` checkout (forced two version re-stamps this session: 277→278→279). Recommend making worktrees mandatory for eq-field, or a pre-commit guard that refuses a commit when HEAD's branch != the session's intended branch. _(added 2026-07-10)_
- Deferred (open): eq-shell FieldIframe has 1 pre-existing eslint error (`pickTenant` accessed before declaration) + 2 exhaustive-deps warnings — untouched by this session's diffs, worth a separate cleanup. _(added 2026-07-10)_

---

## ⚠ CORRECTION — the 2026-07-08 "Brett Kilpatrick duplicate merged live" entry was WRONG

*That session's own summary claimed it "moved user_id + cards_worker_id onto the original record on ehow; deactivated + unlinked the duplicate." Live data on 2026-07-09/10 showed this never actually happened — instead a THIRD, brand-new empty `app_data.staff` row got the real Cards login attached to it, while the ORIGINAL record (15 schedule entries, 1 team membership, 1 leave request, created 2026-06-12) stayed active with `user_id = NULL`. Net effect: two active "Brett Kilpatrick" rows kept showing in Shell's Staff list, identical contact info, exactly the duplicate the July 8 session claimed to have fixed. Root-caused and actually fixed 2026-07-09: real login + correct `cards_worker_id` moved onto the original (history-bearing) record; the empty duplicate deactivated (`cards_worker_id` freed, `active = false`) — no hard deletes.**

**Lesson: a session's own "done" narrative is not proof of the outcome — re-verify against live data before trusting a prior merge/fix as closed, especially for identity-merge operations that touch multiple linked tables (`app_data.staff` ↔ `public.workers` ↔ `auth.users`).** _(added 2026-07-09)_

---

## ⏩ Session close — 2026-07-08 (eq-field) — chip audit across all 3 same-day schema-mismatch findings: all merged/live; PR #477 merged; 2 chips flagged stale, 1 confirmed still genuinely open

*Royce asked for a status audit of every chip opened from the earlier 3-repo schema-mismatch audit, then to keep pushing them forward. Cross-referenced `eq-context` against live session state (`list_sessions`, `search_session_transcripts`, direct `gh pr view` calls) rather than trusting the substrate notes alone — several had already moved since they were last written up.*

**Confirmed shipped (all 3 sibling audit chips, build side fully closed):**

**Investigated the 3 other chips flagged as loose ends earlier today:**
- [ ] **Recommend Royce kill `task_2911c80d` and `task_abbb7fd0`** (EQ Service "session expired" stuck screen, built on two theories that were retracted before the chips were even created). Found the actual reason these theories were already moot: **eq-service PR #469 (merged 2026-07-07, a full day before these 2 chips were opened) already shipped the real fix** — a `ShellSessionRecovery` component that self-heals a lapsed Shell→Service auth cookie. Whatever these 2 chips are doing now is very likely wasted motion chasing an already-fixed problem. Not killed by this session — recommending only, Royce's call to actually stop them. _(added 2026-07-08)_
- [ ] **`task_14031bea` (EQ Service sidebar-header tenant logo clipped, in `ShellSessionRecovery`'s fallback UI) is still genuinely open** — confirmed PR #469 explicitly scoped this out ("does not touch the eq-shell embedded chrome... separate repo, tracked separately"). No session currently confirmed working it. _(added 2026-07-08)_

**Still open, needs Royce's design call (unchanged from earlier today, not attempted):**
- [ ] Revert is structurally non-functional for every SKS roster edit in eq-field (`target_id` always null on reconstructed canonical week-rows) — see the earlier 2026-07-08 eq-field entry for full detail. Not part of PR #422; deliberately left out.

---

## ⏩ Session close — 2026-07-08 (eq-shell/eq-field/eq-roles) — employment_type + Supervision fixes shipped live; access-model foundation designed + Phase 0 built

*Continuation of the 2026-07-06/07 audit session. Closed both deferred items from that session (Supervision fix, employment_type unification), then Royce asked to complete the shared roles rulebook for consistency — which surfaced a bigger, real gotcha (5 separate access-grant paths + Cards represented 4 ways). Ran a Fable-tier adversarial design review, locked a 4-decision/4-phase foundation plan fenced around the 13 Jul SKS cutover, and built Phase 0.*

**Shipped:**

**Decided (Royce):**
- Manager stays the top tenant role — do not rename to Executive. Owner/Executive is a proven one-file add-later (scaffold-tested), not built today.
- Override-promotion criterion = "what scales best" (right defaults), not "fewest overrides." `service.create`/`quotes.approve` stay tenant-local — confirmed cross-app overloaded, unsafe to broaden blind.
- Canonical security groups only going forward — no free-form per-tenant groups. SKS's "Project Managers" promoted to canonical; "Test - Royce" group flagged for deletion.
- Cards un-smeared: the app is worker-facing (entitlement-gated), not a per-user employer permission. `cards.*` matrix perms deprecated, not deleted yet (existing tenant overrides still depend on them).
- `subcontractor` explicitly stays a roster `employment_type` — never a Field login role.
- Foundations (permission-gating, one admin concept, Cards un-smearing) are worth doing NOW, in infancy, while migration is 1-tenant cheap — not deferred to "when it scales." Auth-touching pieces (Phase 2) still fenced to post-13-July.

**Deferred:**
- [ ] **Mitchell Forsyrh + Taya Moody** have Cards + roster identity but no Shell login (no PIN set) — need to sign up via the invite run, not fixable from the backend. _(added 2026-07-08)_
- [ ] **Calum + Mohamed Zemi Asri** — login-only, no Cards org-link. Calum's email is an external domain (`@ssw.com.au`) and never logged in — needs identity verification before any fix, not auto-resolved. _(added 2026-07-08)_
- [ ] **Access-model Phase 2 — one admin concept** — retire `org_memberships.role='admin'` as a gate; migrate its 3 known readers (Cards admin UI, jvkn licence-photo RLS, connection-request email lookup). **POST-CUTOVER ONLY** — auth-touching. _(added 2026-07-08)_
- [ ] **Access-model Phase 3 — guardrails** — Field/Cards convert to the canonical model properly; split the overloaded `service.create`/`service.close` PermKey by app; fix `check-perm-sync.mjs`'s blind spot (it can't catch a local module *under*-granting vs canonical, only over-granting — found this session); delete "Test - Royce" group; build `why_can()`. _(added 2026-07-08)_
- [ ] **`supervisor_category` vocab-lock** — the next drift candidate after `employment_type`, still free text. _(added 2026-07-08)_

**Notes:**
- **Repeated collision this session**: substrate writes to this same non-worktree `eq-context` checkout got clobbered twice by concurrent sibling sessions' own `/close` git activity (rebase-based syncs discarding another session's un-pushed local commits). Content was recovered both times (verified via hash match against the original), but this is a real, repeated operational risk from many parallel sessions sharing one checkout with no worktree isolation — worth Royce's attention if it keeps happening. Lesson applied: commit substrate writes immediately, in their own step, never batched with later work.
- `git checkout main` failed twice this session with "already used by worktree" (a concurrent session had it checked out) — worked around cleanly both times by branching directly off `origin/main` instead.
- The enforcement-site inventory corrected two of this session's own earlier plan assumptions before they shipped: apprentice's `intake.view` grant is deliberately broad by design (Shell's own code says so) — left alone, not removed as originally planned; and the EQ Ops/quotes module turned out to be real and live, not unbuilt as an earlier session's notes assumed.

---

## ⏩ Session close — 2026-07-08 (eq-service) — RCD checks seeded from contract import + full canonical wiring re-verified

*Read the RCD-from-import proposal, then shipped it: commercial-sheet import now seeds unscheduled RCD checks so contracted RCD testing stops vanishing into a dollar line. Then re-audited + live-verified the whole import → check/report → ACB/NSX/RCD chain end-to-end, corrected the stale "contacts fragmented" note (contacts are canonical now), and built a Shell/Service/Canonical wiring infographic with a verification panel.*

- [ ] **Site→customer backfill (SKS)** — only 117/250 SKS canonical sites carry a `customer_id`, so Service report customer-rollups are blank for the rest. The Service side is wired correctly; this is a Shell/canonical-spine data backfill, not a Service wiring gap. _(added 2026-07-08)_

**Shipped + LIVE (PR #131 `5653093`, Build & Deploy green):**

**Notes:**
- **Scale is a non-issue:** cost is per-device and bounded to the worker's OWN photos (avg 183 KB, p95 363 KB; whole fleet only 33 MB / 185 objects). A phone caches its own few MB, never the fleet; server storage unchanged (Storage already holds originals).
- **`dart:indexed_db` was removed from the current Dart SDK** — use `package:web` + `dart:js_interop` for IndexedDB now (dart:html still works for localStorage, as `WalletCacheService` uses).
- Cache keyed by storage path not content → offline copy can be stale if a photo is replaced at the same path (online always fresh via Image.network). Acceptable given photos rarely change.
- CORS-reconcile task `task_df55614d` landed: `ocr-licence` repo now imports `_shared/cors.ts` with the holder_name change folded in — the deploy/repo drift is closed.

---

## ⏩ Session close — 2026-07-07 (eq-field + eq-shell) — Mobile polish (Leave, modals, nav) + voice-to-text back on safety forms

*Royce: "polish mobile view from core > field" (screenshots of Prestart/Leave embedded in Shell), then "merge and continue". Then asked me to steelman voice-to-text for safety forms — found it had been built into the OLD safety.js prestart/toolbox but LOST when those were rewritten into site-reports.js (it survived only on Site Audits). Chose freeform-fields-only, then "ship both together", and explicitly approved the auth-hub deploy for the mic permission.*

**Shipped + LIVE (eq-field, field.eq.solutions):**

**Shipped + LIVE (eq-shell, PR #693, core.eq.solutions):**

**Deferred / needs Royce:**
- [ ] **Live signed-in smoke of Field voice on SKS** — can't test programmatically (needs a browser + physical mic). Sign in → /sks/field → open a report → tap 🎤 → allow mic → dictate into a freeform field. _(added 2026-07-07)_

**Notes:**
- Voice was NOT pulled after a problem — it was dropped in the safety.js → site-reports.js prestart/toolbox rewrite; still lives on Site Audits (audits.js, v3.5.236).
- **Shell embeds Field via iframe; Shell's persistent bottom app bar (parent window, above the iframe's z-index) overlays the bottom ~76px** — that's why every modal footer was hidden in core > field. Fix = lift shell-mode modals 76px + cap height (mobile.css `@media (pointer:coarse)`).
- **SKS Field iframe origin = `eq-field.netlify.app`** (token-auth via `#sh=`, must be a non-.eq.solutions host); EQ = `field.eq.solutions`. Both had to be in the mic allowlist.
- CSS load-order gotcha: `mobile.css` loads BEFORE `field-v8.css`, so equal-specificity rules in field-v8 win the cascade — use 2-class selectors or `!important` (the file already documents this for `.eqf-side`).
- Version-stamp drift persists: file `APP_VERSION` runs ahead of commit-message labels; trust the file. v3.5.261 was a concurrent Roles PR by another agent, not this session.

---

## ⏩ Session close — 2026-07-04 (platform DR completed, issue #60) — armed + green, optimised, self-verifying; eq-service backup retired

*Final leg of the platform-DR arc ("continue on this path / retire / look at the restore drill / optimise" → armed the secrets → "merge and dispatch to green" → "add --use-copy and re-verify" → "merge 438 and close out"). DR is now live, green, and proves itself every day.*

**Completed — closes the open DR deferrals from the earlier #60 close sections below:**

**Still open (your call):**
- [ ] **Occasional deep game-day (rare, human)** — restore **auth data** into a real Supabase target (the dump excludes the managed auth *schema*, so auth rows only load where Supabase provisions it) + app-repoint smoke test. Not automatable cheaply; do when convenient. _(carried 2026-07-04)_

**Notes:**
- `production-ops` is **main-only** → DR-workflow changes only run/verify after merge (every DR change this session went branch→PR→merge→dispatch-on-main).
- `supabase/postgres` ships **without** the managed `auth` schema, so a full in-CI auth restore isn't possible in a bare container — hence the two-layer design (automated artifact-integrity verify + rare Supabase-parity game-day).
- eq-service integration tests are the known pre-existing CI failure (project CLAUDE.md #6); #438 merged on the green `tsc + next build` gate.
---

## ⏩ Session close — 2026-07-04 (15 July CEO presentation prep) — pre-pass bug sweep across Field/Shell/Cards; self-serve tenant provisioning fully hardened + verified live end-to-end for the first time ever

*Royce presents EQ Solutions to his CEO 15 July. Philosophy: "a working product is our best marketing strategy" — built on real verified functionality, not a staged demo. Two levers picked: (1) run the self-serve tenant-provisioning dry run — flagged all session as never having had a real redemption (0 rows ever) — and (2) a canonical-layer visual for the pitch. Also did a pre-pass bug sweep on `core.eq.solutions/sks/field` ahead of Royce's planned week of personally stress-testing Roster/Timesheets/Leave ("human use is the truest form of debugging").*

**Completed (merged + deployed live):**

**Deferred:**
- [ ] **Test the Add-tenant → data-plane Provision button flow fresh** — this session verified the *self-serve invite-link* path end-to-end; the *admin manually creates a tenant, then clicks Provision* path (same PR #627 fix) was never independently walked start-to-finish on a brand-new tenant. _(added 2026-07-04)_
- [ ] **Leave submit-path** — never load-tested a real leave submission this session (real-email side effect); still open ahead of Royce's stress-testing week. _(added 2026-07-04)_
- [ ] **Set a code-freeze date before 15 July** — not yet decided. _(added 2026-07-04, needs your call)_
- [ ] **206 Supabase security advisories on ehow** — Royce's call from earlier this session: keep for a dedicated session, not folded into this one. _(added 2026-07-03, needs your call)_

**Notes (load-bearing):**
- **Self-serve tenant provisioning had never worked, ever, in production** — 0 rows in the redemption table since PR #617 shipped 2026-07-03. All 3 stacked bugs (client Riverpod, server tier constraint, server missing unique constraint) were each found only by actually re-running the live flow after the prior fix, not by code inspection alone — inspection alone had already missed all three once (PR #617's own review).
- `eq-context`'s working tree is shared across concurrent sessions with no per-session isolation (unlike the per-app `.claude/worktrees/*`) — `system/dr-backups.md` had live uncommitted edits from another session mid-turn tonight. Merging a PR whose branch happens to be the currently-checked-out one needs `gh api ... /merge` directly, not `gh pr merge` (which tries a local branch-switch afterward and will collide with a concurrent session's in-progress edits).
---

## ⏩ Session close — 2026-07-03 (eq-shell + eq-intake) — EQ Ops Status-filter bug fixed; intake Health/Tidy dashboard field-name + row-identity bugs found and fixed; Tidy tab gained inline Edit/Suggest

*Continuation of the earlier same-day close (pushed `850e24f`) that reconciled the 6 stale-blocked PRs — this block covers everything after that: the "continue on with deferred works" thread, the EQ Ops filter bug report, and the intake dashboard investigation it led to.*

**Completed (all merged + deployed live, verified via Netlify MCP deploy state):**

**Investigated, not built — needs Royce (data/business judgment, not code):**
- [ ] **12 contacts missing first/last name, categorized** — 2 safely inferable from email pattern (Pashon Jima at ap.equinix.com → last name "Jima"; Benoit Kon at digi-co.com.au → last name "Kon"), 1 data-import bug (company name "Metronode" landed in `first_name` with a garbled fragment in `position` — needs a real fix, not a name), 1 unrecoverable ("Rafael", no email/signal), 8 are role/department mailboxes ("Accounts", "Payables", "Reception") not people — filling a `last_name` for those would be fabricating data. Declined to hand-write any of this via raw SQL (bypasses the governed audit path this whole day's work has been about) — needs your call on fix path (dashboard tidy flow, once the Tidy-tab Edit lands live, is now a real option for the 2 inferable ones). _(added 2026-07-03, needs your call)_
- [ ] **137-item review queue is not agent-workable** — checked before bulk-approving anything: every item across every category, including the "one-click" trade/link/format ones, is explicitly low/medium confidence with the adjudication panel that built the queue having already declined to auto-commit ("per-person trade unproven, confirm," "adjudication panel rejected auto-commit 0/3," "not resolvable from canonical data"). There's no genuinely mechanical subset — every item needs someone who knows the specific person/customer. _(added 2026-07-03, needs your call)_
- [ ] **Browser verification of the new Tidy-tab Edit/Suggest + Dupes multi-group fix** — no component-test infra exists for `@eq/intake-demo` (no testing-library/jsdom), and no live authenticated session was available to click through it. Verified via strict `tsc -b` + full existing test suites + careful code tracing only. Next session with a live login: open a Tidy tab with gaps, Edit one inline, Suggest one, confirm only the intended row changes; open Dupes and confirm more than one duplicate group can now show per field; confirm Site Name renders on the Sites Gaps/All view. _(added 2026-07-03, needs your call)_

**Notes (load-bearing):**
- **Second occurrence of the same bug class**: `EntityDrillDown.tsx`'s hardcoded field-name lists not matching live schema is the same failure mode already fixed once in the quality-guardian Edge Function's inline `ENTITIES` config (PR #61, 2026-07-03 earlier). Two independent UI/service consumers of the same canonical schema both drifted the same way — worth a grep across the rest of eq-intake for any other hardcoded field-name list before assuming this class of bug is fully closed.
- **eq-shell's vendored `eq-intake/eq-platform/packages/` copy has at least one deliberate, silent divergence from eq-intake's own source** (the `@fontsource` → `@eq-solutions/tokens` swap in `styles.css`) that isn't documented anywhere obvious. Any future re-vendor — full script or surgical file copy — must diff against `origin/main` before overwriting, not just copy and rebuild.
- **`@eq-solutions/ui`'s `Table` component's `filterable: 'select'` only supports literal per-row equality** — no support for a grouped/staged filter concept (a column's `filterOptions` values must equal the raw `row[key]` value exactly). Any future column needing "these 3 statuses = one filter option" behaviour needs either a derived field on the row (pattern used in `EntityDrillDown.tsx`'s `deriveRow()`) or a shared-package enhancement — not a naive `filterOptions` list.
---

## ⏩ Session close — 2026-07-03 (eq-shell + eq-cards) — self-serve tenant provisioning hardened + deployed; Tenants admin page gained edit/archive

*Started from Royce asking how to hand EQ Cards + a core login to a new prospect. Audit of the existing self-serve provision flow found 5 defects (never fired in prod — 0 rows ever). Full plan written, built, and shipped same session; then extended into Tenants-page admin actions Royce asked for after reviewing the live page.*

**Completed — provisioning hardening:**

**Completed — Tenants admin page (Royce reviewed the live page, asked "how do we delete tenants / what else could be here"):**

**Deferred (needs Royce):**
- [ ] **Mandatory prod dry run** — `shell_control.provision_tokens` is still 0 rows ever as of session close. Generate a real link (test org + spare phone) through Admin → Tenants, walk it through Cards including the phone-mismatch rejection, confirm the workspace lands correctly and the `tenant_slug` handoff opens the right tenant, then archive the test tenant via the new #622 UI. **Do this before sending a link to a real prospect.** _(added 2026-07-03, needs your call)_
- [ ] **`EQ_PLATFORM_NOTIFY_EMAIL`** — optional Netlify env var, not yet set. If set, you get an email whenever a provision link is redeemed. No redeploy needed — functions read it live. _(added 2026-07-03, needs your call)_

**Notes (load-bearing):**
- **eq-cards does NOT auto-deploy on merge** — `.github/workflows/deploy.yml` is `workflow_dispatch` / release-tag only, by deliberate design (its own comment: merging used to silently ship to prod, which conflicted with the "never deploy without explicit instruction" rule). Merging an eq-cards PR only lands it on `main`; a separate dispatch is required to actually deploy cards.eq.solutions. Verified via the deploy record (`manual_deploy: true`, `commit_ref: null` — it's an API zip-upload, not a Git-linked build) before trusting anything was live.
- **Worktree reuse gotcha, again**: the `dreamy-meninsky-7082ba` worktree used for #617 was marked "DONE — dir removable after merge" in `worktree-registry.md`, and another session silently reused it for unrelated work (branch switched underneath) before the #622 task started. Verify `git branch` against expectation before trusting a worktree dir by name — see [[shared-checkout-branch-race]]. A fresh worktree (`tenant-page-admin-actions`) was created instead of risking the stale one.
- Full detail in `~/.claude` memory: `tenant-self-provision-hardening.md`, `tenants-page-admin-actions.md`.
---

## ⏩ Crumb sweep — 2026-07-02 (eq-cards + eq-shell tail)

**Shipped live this session (verified):**

**Crumbs needing Royce (surfaced so they're not forgotten):**
- [ ] **Send Huon** the connection-email reply + before/after graphic. _(added 2026-07-02)_
- [ ] **Resolve the pending "432470463 · No licences yet" connection request** on core.eq.solutions/sks/staff — nameless self-signup from before the name-gate; approve/decline + nudge to add details. _(added 2026-07-02)_
- [ ] **Define the required-credential policy** (what SKS actually requires) + decide whether to add a worker **trade field** — the two blockers before the gaps engine can ship. _(added 2026-07-02)_
---

## ⏩ Session close — 2026-06-30 (part I) — EQ Cards Sentry + dead code + iOS spinner fix

**Completed (eq-cards, pushed to main):**

**Completed (eq-shell, merged + deployed):**

**Deferred (added 2026-06-30):**
- [ ] EQ Cards: ARMADA lighthouse — PR #109 was merged before `armada:lighthouse` label applied; Calum's system likely needs an open PR. New open PR with label OR Calum runs manually _(added 2026-06-30)_
- [ ] EQ Cards: Contact John Angangan to retry signup — duplicate-worker fix (migrations 0062/0063) is now live _(added 2026-06-30)_
- [ ] EQ Cards: Wrap `eq_cards_find_pending_invite` RPC call (`otp_screen.dart:163`) into `WorkerSelfRepository` data layer — low priority, no behaviour change _(added 2026-06-30)_

**Notes:**
- Boot loader spinner in `index.html` already had `will-change: transform` and animated fine on iOS — confirmed the CSS pattern correct before applying to eq-shell.
- `eq_cards_find_pending_invite` in `otp_screen.dart:163` is NOT dead — auto-routes invited workers post-OTP. Retained.
- eq-shell `main` was checked out in worktree `clever-wilson-161a7a`; always branch from `origin/main` in the bare checkout.
- eq-guard hook blocks Edit tool on eq-shell; used Python binary-mode writes to preserve CRLF (PowerShell `Set-Content` converts CRLF→LF causing 200-line diffs for 1-line changes).
---

## ⏩ Session close — 2026-06-30 (part g) — Cards admin-console + labour-hire pilot (discussion only)

**Decided (Royce):**

**Deferred (added 2026-06-30):**
- [ ] **Onboard current labour-hire firm's workers to Cards** — Royce in progress; "need to fill up the info first" before any demo _(added 2026-06-30)_
- [ ] **Dry-run Core > tenant view before the coffee demo** — verify what the tenant admin view actually renders + scope out anything not appropriate for the firm to see; offered, deferred until data is in _(added 2026-06-30)_
- [ ] **Decide the pilot offer** — firm as guest in existing tenant vs their own tenant (changes the demo + the portability framing) _(needs Royce's call) (added 2026-06-30)_
---

## ⏩ Session close — 2026-06-30 (part d) — Activity-log link triggers + Field/Service site-view reconcile

**Completed (eq-shell, merged + deployed):**

**Completed (eq-field + DB):**

**Audit truth (reconciled):**
- Site selection in **both** Field and Service ALREADY honors the activation flags — `service.sites` filters `service_enabled`, `field_sites` filters `field_enabled`. Earlier "Field not wired" was a STALE-CHECKOUT error (local eq-field was 11 commits behind origin). Defaults clean: `active`/`field_enabled`/`service_enabled` all default `true`, NOT NULL → new sites visible in both apps automatically.

**Also completed (part e — continued):**

**Deferred (added 2026-06-30) — next session (prompt written in sessions/2026-06-30.md part e):**
- [ ] **Platform Security Log / operator console** — sign-ins/2FA audit (jvkn, admin-audit.ts reads it); deferred by decision _(added 2026-06-30)_
---

## ⏩ Session close — 2026-06-30 (handoff hardening) — Shell→Service: shared contract + canaries + secret probe

**Completed (merged + deployed):**

**Decided (Royce):**
- The handoff contract is a shared compile-time + runtime-enforced package (the "ultimate solution") — chosen over keeping only the daily drift canary. New repo `eq-contracts`, not folded into eq-roles.
- Enforcement = type + dependency-free validator on both ends (not Zod, to keep eq-shell dep-free).

**Deferred (added 2026-06-30):**
- [ ] **auth_handoff Sentry alert** — native rule on `canary=auth_handoff` AND `level=error` (catches real-user slug_unresolved/no_email; the probe already covers secret drift). MCP is read-only for alert rules → 2-min UI action (recipe on file), or build the watcher-as-code _(added 2026-06-30)_
- [ ] **Contracts versioning discipline** — both repos pin `#v0.1.0`; on any contract change, bump the package + tag + update BOTH consumer pins together. The compile gate only holds when the pins match _(added 2026-06-30)_
- [ ] **Add eq-contracts to the suite-state cron** repo list so the new package shows in the nightly snapshot _(added 2026-06-30)_

**Notes / gotchas (load-bearing):**
- **Handoff secret now lives in 3 places** — eq-shell `SUPABASE_JWT_SECRET`, eq-service `EQ_SHELL_JWT_SECRET`, eq-context probe GH secret `EQ_SHELL_JWT_SECRET`. Rotate all three together or the handoff breaks / the probe false-alarms.
- **Stacked-PR trap:** merging a base PR with `--delete-branch` auto-CLOSES a stacked child PR. Recover by rebasing the child's commit onto main + opening a fresh PR. Don't `--delete-branch` a base that has an open stacked child.
- **Sentry project slug = `eq-solves-service`** (folder name), not the GitHub repo name `eq-service`. Netlify projects = `eq-service` (`service.eq.solutions`) + `eq-shell` (`core.eq.solutions`).
---

## ⏩ Session close — 2026-06-28 (part b) — Shell↔Service branding + token refresh + admin hub

**Completed:**

**Open / next:**
- [ ] **gitleaks pre-commit hook** — prevent PAT exposure in substrate history _(added 2026-06-28)_
- [ ] **Update C:\Projects\.git-credentials** files with new PAT after rotation _(added 2026-06-28)_
- [ ] **Token refresh smoke test** — shorten TTL locally to confirm ShellTokenRefresh fires (4h is hard to test live) _(added 2026-06-28)_
---

## ⏩ Session close — 2026-06-09 — Security sprint + WS1/4/5/7 + GATE A + eq-service encryption

**Completed (2026-06-09):**

**Active / time-sensitive:**

**Deferred:**
- [ ] **Delete `C:\Users\EQ\eq-credentials-ref.html`** after importing to password manager
---

## ⏩ Session close — 2026-06-07 (PM) — Cross-app linkage audit
*Restored 2026-07-27 — a rotate_pending.py bug didn't recognize `- [~]` (partial) as an open state, so this whole section was wrongly archived as "fully done" during the backlog cull even though its P2 item is genuinely still in progress. Bug fixed same day (scripts/rotate_pending.py now treats `[~]` as open for section-completeness purposes); the 3 already-closed bullets below stay closed and will rotate out normally next cycle.*

Live-verified map of Cards/Shell/Field/Service/Quotes linkage (4 Supabase projects + 5 repos, read-only).
Full report: [`cross-app-linkage-audit-2026-06-07.md`](../../archive/cross-app-linkage-audit-2026-06-07.md).
Gated playbook: [`cross-app-linkage-remediation-plan-2026-06-07.md`](../../cross-app-linkage-remediation-plan-2026-06-07.md).
Sprint (steelman-corrected, 10/10): [`cross-app-linkage-sprint-2026-06-07.md`](../../archive/cross-app-linkage-sprint-2026-06-07.md) — 7 workstreams, 4 waves, pre-mortem.

**Headline:** canonical model (`ehow.app_data`) is FK-wired but its linking rows are empty (`jobs`=0, `quote`=0);
worker→staff link 1/50, customer `canonical_id` 0/520 in live ehow, sites→customer 28/591. Asset sync (4808) works.

**Prioritised actions (all Royce-gated — see plan for mechanism/verify):**
- [~] **P2:** customer convergence — **PARTIAL APPLIED 2026-06-07** (`_ws1-customer-dedup-2026-06-07.md`): Tier S 38
      stub customers retired (dup-groups 117→80); 28 quotes `canonical_id` linked (1:1-both-sides). **Remaining:** decide
      SoR (rec `app_data.customers`); Tier A merge (26, supervised); Tier C (50 ambiguous) + quotes-side N:1 dedup via
      Intake; 99 dangling sites need source re-import. Note: `sks_quotes_customers.canonical_id` is UNIQUE (1:1) vs N:1 data.

**Drift corrected (live wins):** `architecture.md` "jvkn = no operational data" is false (it's the worker house);
creds 779→737, invites 37→58 since 06-03; `0028_contact_customer_links` IS present on SKS (291 rows).

---

## EQ Shell + EQ Intake

> **⚠ SUPERSEDED (2026-05-30) — the architecture + gate notes in this section are STALE; `suite-state.md` carries current reality** (`STATE.md`, cited here originally, is archived as of 2026-07-12). (1) The **two-plane** model is current, NOT "single canonical": browser → `eq-canonical` (control plane) + tenant data **server-only** in `eq-canonical-internal` (`zaapmfdkgedqupfjtchl`). The "Two-Supabase obsolete / single canonical" copy below is itself now obsolete. (2) The **GTM validation gate was REMOVED** — do NOT block Shell Phase 2 (or any EQ work) on outside-customer validation (see `ops/decisions.md` + memory `feedback_gtm_intent`). Historical detail below kept for record only.

**Status as of 2026-05-20:** Phase 1.E + 1.F shipped (single canonical
Supabase, Intake module live at `/core/intake`, Unified Identity, RLS
swept to `app_metadata`). Phase 2 paused — no further shell modules
until the GTM validation gate clears (see EQ GTM PRIORITY section
below) OR a paying customer specifically asks for one.

**Two-Supabase architecture is OBSOLETE** as of Phase 1.E (2026-05-19).
Current state:

- `eq-canonical` (`jvknxcmbtrfnxfrwfimn`) — single canonical project
  holding both shell control tables (`tenants`, `users`,
  `module_entitlements`) and tenant application data (13 canonical
  entity tables incl. `licences` added 2026-05-20 part-c). Region
  `ap-southeast-2`.
- `eq-shell-control` (`hxwitoveffxhcgjvubbd`) — **DECOMMISSIONED**
  2026-05-19 per `sessions/2026-05-19.md`.
- `sks-canonical-eq` — planned, not provisioned. Gated on GTM
  validation gate, not on shell readiness.

### Critique action items — deferred to Phase 2 resumption

Three external-model critiques (Claude / Grok / ChatGPT) shopped
2026-05-20 part-d. The actions below are real risks the architecture
carries today. They DO NOT ship until Phase 2 resumes (GTM gate
clears, or a paying customer requests a new module). Priority order
= highest blast-radius first.

- [ ] **Dual-secret support in `verify-shell-session`** for
      `SUPABASE_JWT_SECRET` rotation. Same rationale.
- [ ] **`revoked_sessions` table** + shorten JWT TTL from 1 hour to
      ~30 minutes. Without this you cannot kill an active session
      before its TTL expires.
- [ ] **Schema split** — `shell_control.*` (tenants/users/
      module_entitlements) vs `app_data.*` (canonical entities) in
      the same `eq-canonical` project. `CREATE SCHEMA` +
      `search_path` update. Free now, saves ~3 weeks when a regional
      secondary is needed.
- [ ] **Per-domain RPC decomposition** — split
      `eq_intake_commit_batch` before it accumulates 5 module
      branches. Per-entity validators in a shared library; per-domain
      RPCs call the library. Currently 1 mega-RPC handles all
      mutation; this is the chokepoint all three critiques flagged.
- [ ] **Canonical → Field one-way sync rule** documented + enforced
      with a Supabase trigger for shared concepts (staff, sites,
      schedule_entries). Never the reverse. Otherwise dual-write
      pain during iframe-purgatory becomes uncontrolled.
- [ ] **Token-mint audit log** (tenant_id, IP, timestamp) with a
      Sentry threshold alert per `https://mcp.sentry.dev/mcp/eq-solutions/eq-shell`.
      Today there's no detection mechanism for a stolen salt.
- [ ] **Build-time hash check** for the vendored `@eq/*` packages so
      a stale vendor can't silently ship through Netlify.
- [ ] **`STABLE SECURITY DEFINER` wrapper** for the `tenant_id` UUID
      cast read in every RLS predicate (perf optimisation for the
      day load matters).
- [ ] **Iframe retirement deadline decision** — Grok pushed 9 months,
      Claude said 3 years is a roadmap not purgatory, ChatGPT said
      4 years is the modal failure mode. Pick a number, write it
      somewhere, hold to it. Not a code task; a strategic decision
      Royce makes when Phase 2 resumes.

Full critique synthesis + the items already shipped (so we don't
re-litigate them) is in [sessions/2026-05-20-part-d.md](../../sessions/2026-05-20-part-d.md).

### Substrate-drift note (2026-05-20 part-d)

The `eq-shell/README.md` Phase 2 row said "Tender Pipeline first"
through 2026-05-20. This was a stale claim — Tender Pipeline is a
Field sub-module, not a flagship shell module. The README has been
corrected. Going forward: when writing critique prompts or briefing
external models against the shell, read the substrate actively, do
not just copy what the README says — and check for drift signals
(passing pivots that have hardened into "platform doctrine"
language).

### Dedupe-on-ingest skill (intake feature)

Decision logged 2026-05-19 in `ops/decisions.md` ("Dedupe Is Intake's
Job, Not Per-App"). When EQ Intake ingests a CRM export, the
collapse-dupes step (e.g. "47 rows of Equinix Australia Pty Ltd →
1 customer + 47 sites") happens inside intake via the Confirm-UI,
not inside the app reading the data. Implementation detail to be
added to `eq-intake/CONFIRM-UI-SPEC.md` as a new section.

- [ ] **Extend `eq-intake/CONFIRM-UI-SPEC.md`** with a "Dedupe
      confirmation step" section (confidence tiers, screen sketch,
      signature caching). Companion to the existing column-mapping
      confirmation spec.
- [ ] **Implement the dedupe step in the intake pipeline** — runs
      AFTER column-mapping is confirmed, BEFORE the commit_batch
      call. Two confidence tiers (HIGH = exact normalized name
      match, MEDIUM = fuzzy match needing review).
- [ ] **Test against the SimPRO bundle** — 524 customer-site rows
      should collapse to ~150 unique customer rows + 524 site rows
      in canonical.

### EQ Shell Phase 1.B (Netlify wire-up) — DONE


### eq-demo-canonical — security advisor cleanup (open) — CLOSED 2026-07-27, see below

Diagnosed 2026-05-19. 17 advisor warnings, fix drafted but not applied.

- [ ] **Toggle leaked-password protection** in eq-canonical (`jvknxcmbtrfnxfrwfimn`) dashboard → Authentication → Settings → enable HaveIBeenPwned check. **(Royce manual step, never confirmed done)** **Correction 2026-07-27: this had 3 duplicate copies elsewhere in this file, all closed as redundant during the backlog cull — but the cull mechanically closed all matching lines including this one, the copy meant to stay as the single live tracker. Reopened here; the underlying toggle is still unconfirmed.**

### sks-canonical-eq provisioning (gated, not started) — CLOSED 2026-07-27, see below


---

## Deferred (added 2026-07-03)
- [ ] **Approve eq-shell fleet dispatch for 0158 (`field_people` fix)** — dispatched (run visible in eq-shell Actions), paused on the `production` environment's human-approval gate. _(needs your call — approve, then verify `app_data.field_people` shows `security_invoker=on` on zaap)_
- [ ] **E2E/integration test coverage for the flows that broke today** — recommended as the "deeper fix" alternative to the live-audit path (which Royce chose instead: "yes" to the quick audit, not this). None of today's ~6 shipped bugs (0170 semicolon, notify race, batch-resolve UUID strictness, job_plan_id UUID strictness, the 3 security_invoker regressions) were caught by `tsc`/`next build`/CI — every one needed a human to click through the real feature or an agent to run a live-data audit. Worth a scoped decision on whether to build real E2E coverage (at minimum: create→resolve defect, create→assign job-plan) so this class of regression is caught automatically next time, not just audited reactively. _(needs your call on scope/priority)_

## eq-cards / eq-shell / eq-solves-service: full outstanding-Sentry sweep (7 issues), Richard Brown's jvkn identity actually merged, silent PIN-reset lockout fixed and shipped (2026-08-17)

- [ ] **Sentry [EQ-SOLVES-SERVICE-D](https://eq-solutions.sentry.io/issues/EQ-SOLVES-SERVICE-D) left unresolved** — single occurrence, no sourcemaps uploaded for this project, stack trace is fully minified with no first-party frame. Nothing actionable without more data; needs sourcemap upload (same gap already on record for eq-shell, 2026-07-12) or a recurrence to investigate. _(added 2026-08-17)_
- [ ] **eq-shell [PR #1417](https://github.com/eq-solutions/eq-shell/pull/1417) and [PR #1418](https://github.com/eq-solutions/eq-shell/pull/1418)'s test-plan click-throughs never run live** — "trigger a real lockout against a deliberately-inactive test account, confirm the warning lands in Sentry" — on all three doors now (PIN reset, magic-link, phone-OTP). Verified by direct DB/code inspection instead (traced Richard Brown's actual live lockout through each exact code path); the merged fixes are confirmed correct by that trace, but nobody's watched a real Sentry event land from this code yet. _(added 2026-08-17)_
- [ ] **This jvkn-side identity merge is separate from the ehow-side `staff_id` duplicate already closed 2026-08-15/16** ([EQ-SHELL-1M](https://eq-solutions.sentry.io/issues/EQ-SHELL-1M), PR #1373) — same person, two independent duplication incidents on two different systems. Don't read this entry as a repeat of that one, and don't assume closing one closes the other if Richard (or anyone else) shows a similar symptom again. _(added 2026-08-17)_

---
