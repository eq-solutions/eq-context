---
title: EQ Service — Pending Actions
owner: Royce Milmlow
last_updated: 2026-09-01
scope: EQ Service engineering backlog, split out of eq/pending.md (2026-08-17) so a session working in this repo isn't wading through the other 8 repos' items too. Same conventions as before: "- [ ]" open, "- [x]" done (rotated out nightly by scripts/rotate_pending.py), "- [~]" in progress.
read_priority: critical
status: live
---

# EQ Service — Pending

Split out of `eq/pending.md` (2026-08-17) — see `eq/pending.md` for why. SKS items live in `sks/pending.md`. OPS items (entities, tax, infra) in `ops/pending.md`.

---

## eq-solves-service: /defects list was going stale after auto-created/resolved defects — found, fixed, merged, deployed live (PR #822, 2026-09-01)
*Follow-up task filed by PR #821's own review while narrowing `revalidateMaintenanceSurfaces()` — "defect-count freshness on 2 maintenance actions... `task_3b858742`" — picked up and closed directly here rather than left as a dangling chip.*

- `updateCheckItemAction`/`updateCheckItemResultAction` write `maintenance_check_items.result`, which fires the live `fn_check_item_to_defect` trigger to auto-create/resolve a `defects` row on every fail/un-fail transition — neither action revalidated `/defects`, so the list page could serve stale data until an unrelated action happened to bust it or a hard reload occurred. Fixed with `revalidatePath('/defects')`, matching the pattern already used by the file's other defect-mutating actions.
- Verified live before fixing, not just from the migration file: `service.maintenance_check_items`/`service.defects` are views over `app_data.*` (migration 0147, June canonicalization) — the auto-defect trigger is still correctly attached to the real `app_data.maintenance_check_items` base table, firing end-to-end through the view's INSTEAD OF trigger.
- Merged (landed in the same fast-forward as PR #821 — closes the "P2 items from the review" bullet from the entry below) and confirmed published live via Netlify's deploy record (state `ready`, matched to the exact merge commit) within ~2 minutes of merge.

**Deferred:**
- [ ] **Not click-tested live** — no Shell session/credentials in this environment to actually fail a check item and watch `/defects` update without a hard reload. Confidence is otherwise high: it's a copy of an already-working pattern used 3 other times in the same file. _(added 2026-09-01)_

---

## eq-solves-service: 4-axis service review → full P0/P1 sprint built and shipped live, including a critical cross-tenant leak found and closed (2026-08-31)

- [ ] **Retire the legacy `shell-sso` / `/auth/shell-bridge` path — needs Royce's explicit sign-off, it's an auth change.** Still live per CLAUDE.md (provisioning only inert because of a missing column). _(added 2026-08-31)_
- [ ] **Live authenticated UX click-through never done.** This worktree had no `.env.local`; copying the working credentials from the main checkout was correctly blocked by the permission classifier as a credentials-file action. The UX rating (6/10) is built on a full source-level consistency audit, not hands-on interaction — worth a real pass once a session has working dev credentials. _(added 2026-08-31)_
- [ ] **Relay 2 live ERROR-level advisor findings to whoever owns them — not this repo's fix.** `app_data.field_managers` / `field_people_directory` are SECURITY DEFINER views with no migration in eq-solves-service; they belong to Field or Shell's canonical schema. _(added 2026-08-31)_
- [ ] CLAUDE.md's "DB-verified scope" note still cites migrations `0180-0182/0186` for instruments/calibration — the memory file this traces to already carries the correction (`0183-0186`, renamed by #535), but CLAUDE.md's own summary line was never updated to match. Minor, spotted in passing. _(added 2026-08-31)_

---

## eq-solves-service: CLAUDE.md's StatusBadge description was stale — verified against the live kit, fixed (2026-08-31)
*Royce had already checked the actual `@eq-solutions/ui` v1.15.0 source (the exact version pinned in package.json) and found the doc describing props (`tone`, `size`) that don't exist — the real props are `status`/`label`/`density`. This session independently re-verified against the installed `node_modules` copy before editing, then applied the fix.*

**Deferred:**
- [ ] **Fix committed but not pushed.** `docs(claude-md): fix stale StatusBadge prop description` (`9541e92`) sits on branch `worktree-statusbadge-doc-fix` in an isolated worktree (`.claude/worktrees/statusbadge-doc-fix`), based on current main. Push/PR wasn't requested this session. _(added 2026-08-31)_

---

## eq-solves-service: PR #619 turned out to have 3 migration-number collisions, not 1 — all fixed (PR #806, merged + live 2026-08-23)
*Started as a routine fix for the one known `0192` collision breaking `Integration tests (Supabase local)` CI on every PR to this repo. Fixing it exposed a second, previously-masked collision at `0193` (the bootstrap aborts at the first duplicate-key error, so it never reached the second) — and a full-repo sweep for any OTHER duplicate found a third, unrelated one at `0203`.*

- [~] **Root cause now fully diagnosed (2026-09-01), fix in progress.** `0197_report_settings_per_tier.sql` does `UPDATE service.tenant_settings SET report_show_cover_page_summary = report_show_cover_page, ...` assuming `service.tenant_settings` already has the legacy `report_show_cover_page` column — but that column was only ever added to `public.tenant_settings` (migration `0015`), a different schema. Confirmed reproducing on `main`'s own latest commit, not tied to any specific PR. Production is unaffected (verified live: `service.tenant_settings` on ehow already has both the legacy and new columns — whatever real historical path built it there isn't reproduced by a from-scratch migration replay). Filed as `task_8369a579`; Royce started it running independently in a separate session, not yet reported back as of this close. _(added 2026-08-23, root-caused 2026-09-01)_

## eq-solves-service: automated tests added for the compliance-reports page, merged, live (2026-08-21)
*Continuing the same day's push to get real automated test coverage across the app, one page at a time (maintenance checks, then ACB/NSX/RCD testing pages, now Reports). Built in its own isolated copy of the repo rather than the shared one, since the shared one was busy with another session's database work at the time.*

**Deferred:**
- [ ] Cross-app documentation of the isolated-copy setup (which files a fresh isolated copy is missing by default, like local settings) wasn't updated — worth a note somewhere so the next session doesn't lose time on the same false alarm. _(added 2026-08-21)_

---

## eq-solves-service: found and fixed why the automated test database could never fully build itself from scratch — proof PR open, not merged (2026-08-21)
*Direct continuation of PR #792 (same day, different session) — that PR fixed the first blocker on the path to getting real automated tests running again. This session picked up where it left off: the very next step still failed immediately.*

- eq-service [PR #797](https://github.com/eq-solutions/eq-service/pull/797) — **left open, not merged**, on purpose: it's a proof that the fix is correct, not something that needs to ship (nothing it touches affects the real live app, only what a from-scratch test build looks like). **UPDATE 2026-08-21 (different session):** merged anyway, on Royce's explicit "merge it once it passes" (given mid a different, unrelated fix in the same repo) once CI cleared past the documented pre-existing `Integration tests` exception. The merging session hadn't read this "do not merge" scoping note until after merging — flagged it immediately; Royce reviewed the actual risk (every changed file a guarded `IF NOT EXISTS` no-op against live ehow, no app code touched) and confirmed leaving it merged. Full detail in the new section below and `sessions/2026-08-21.md`.

**Deferred:**
- [ ] **A second, unrelated, pre-existing bug found blocking the very next step** — three pairs of database-update files, going back a while, were accidentally given the same internal ID number as each other, which trips up the test-database tool the moment it tries to record both. Real, but a completely different kind of problem from everything above, and none of the 6 files involved were touched this session. Filed separately as [issue #800](https://github.com/eq-solutions/eq-service/issues/800) rather than fixed here, since the safe fix (renaming already-shipped files) needs someone to first confirm none of those exact files are still mid-flight on the live-database update pipeline — not a call to make blind. _(added 2026-08-21)_
- [ ] **Even past #792 and this session's fixes, the from-scratch test build still can't finish — a third, different wall.** A different session confirmed it live, twice (once on the original PR's branch, once again after rebasing onto main with every fix above already included): the build now dies on a table called `asset_local` instead, same shape of problem — something reaches across to that table before the step that actually creates it runs. Same fix pattern should apply (find which step reaches across too early, compare it against the step that creates the table, guard rather than renumber). Flagged as its own follow-up; a background session picked it up but ended without a PR, issue, or write-up to show for it — next attempt should start fresh rather than assume any progress was made. _(added 2026-08-21)_

---

## eq-solves-service: destructive-delete RPC missing a role check — found, fixed, verified live (2026-08-21)
*Went looking for the next real, non-duplicate piece of work while the fleet's other obvious threads were already covered. Found `service.hard_delete_archived_entity` — the function behind the admin archive page's permanent-delete button — checked which tenant you belonged to but not what role you held: any signed-in team member, any role, could call it directly and permanently destroy an archived customer, site, asset, job plan, or maintenance check. The app's own "admin only" button was doing the right check; the database underneath it wasn't. Caught before duplicating work: another session had already found and fixed the same thing (PR #794) — confirmed that independently rather than building a second copy.*

**Deferred:**
- [ ] Tier C's `service.audit_logs` mystery (why on-site test entries never get an audit trail row) — the theory written into the merged Tier C scoping doc doesn't hold up under closer reading of the actual code: the mechanism it blamed is deliberate and demonstrably works fine elsewhere. Real cause still unknown. The fast way to actually answer it is one error-tracker query rather than more code reading, and that tool wasn't reachable this session. _(added 2026-08-21)_

---

## eq-solves-service: worktree/branch/stash graveyard cleared — 8 stranded branches, 23 orphaned folders, and 3 stale stashes, every one confirmed already-shipped before removal (2026-08-21)
*Asked to check one specific stranded worktree (`fix/session-expiry-suite-wide`) that looked like finished work with no PR. Confirmed by content hash (`git patch-id`), not just ancestry, that it was a byte-for-byte duplicate of already-merged PR #727 — two sessions had done the same fix, one got the PR, the other was left behind under a different commit. Asked to check the rest of the repo's stranded worktrees for the same pattern, then to "complete the survey" against two more branches that were only visible because they still held old stashes. Same result every single time: the content had already shipped, just under a different SHA.*

- No PR, no migration, no product code touched. Pure repo hygiene.

**Deferred:**
- [ ] **One leftover worktree folder (`acb-check-report-wiring-1baa7e`) still can't be deleted** — Windows reports it's in use by a running process. It's empty with no git linkage, so it's inert; delete it once whatever's holding it open is closed. Three attempts across the session all failed the same way. _(added 2026-08-21)_

---

## eq-solves-service: the "don't send the same report twice" guard was dead code — fixed, merged, live; prerequisite for Tier C offline writes (2026-08-20)

**Deferred:**
- [~] **Sending a corrected report is impossible from the app — fix built, PR open, deliberately not merged.** Added a revision-reason box to the Send Report screen (only appears when a report has already gone out once before), backed by a new check so the screen can ask the server whether a reason is needed instead of guessing. 7 new automated tests. eq-service [PR #791](https://github.com/eq-solutions/eq-service/pull/791) — held back on purpose: this path emails real customers, so it needs your explicit go-ahead rather than shipping on a "fix this" instruction. _(added 2026-08-20, updated 2026-08-21)_
- [ ] **Not click-tested live by Royce** — verified by typecheck, full build, 444 unit tests, CI, and Netlify commit-ancestry, not by actually opening the Send Report modal and issuing a report. The path has zero production rows, so a live click-through would be the first real exercise it has ever had. _(added 2026-08-20)_

---

## eq-solves-service: the automated safety-check suite has been unable to fully test itself since April — fixed past two blocking bugs, a third is being fixed live in an open PR (2026-08-20)
*Found while checking whether the report-reissue fix above actually got tested — asked directly "did the integration tests pass?", which surfaced that the CI check which spins up a fresh test database has been broken since migration 0042 (mid-April). Root-caused two separate, stacked bugs and fixed both. That let the test database get built roughly 120 database updates further than before it hit the next thing missing — which turned out to be a bigger, separate gap now being closed in its own follow-up.*

**Deferred:**
- [~] **A third, bigger gap found immediately after the above landed: part of the database was restructured by hand directly on the live system at some point and never went through a proper tracked update at all**, so the from-scratch test builder still can't fully rebuild it even past the two fixes above. Deliberately handed off as its own separate piece of work rather than chased in the same sitting — genuinely bigger, open-ended. Being built as eq-service [PR #797](https://github.com/eq-solutions/eq-service/pull/797), still in progress as of this close (its own description says not to merge yet) — checked for merge-readiness and held back: found one real but currently low-risk mistake in the new fixture (it tries to lock down 10 tables that turn out to already be read-through mirrors of the real data, which isn't allowed and would fail loudly if ever run for real — safely, not silently, but still needs fixing). _(added 2026-08-21)_
- [ ] **The safety-check suite still won't fully pass even once the above lands** — real progress each time, but nobody has checked yet whether there's a fourth gap waiting after this one. _(added 2026-08-21)_

---

## eq-solves-service: Tier B of the offline-first proposal — first slice built and shipped live: real offline read-cache via a service worker (2026-08-20)
*Direct follow-on to the same-day "Tier B scoped" close (PR #781, archived). Initial `/decide` pass leaned against building yet — no incident on record, low real ACB/NSX volume. Reversed when Royce said the field techs are certain they'll need it as usage grows. Built the read-cache slice only — no icon/manifest, no install-to-home-screen, no offline write — per Royce's own scoping call ("start now — we can tidy up a logo quickly anytime").*

**Deferred:**
- [ ] **GitHub Actions' recovery on this repo is real but not fully explained.** PR #783 got full `pull_request`-triggered checks, and its merge commit got a full independent `push`-triggered run too — both genuinely green. But re-checking the run history shows the original problem was narrower than first thought: `push`-to-`main` was never actually broken (PR #782's own merge commit got a complete push-triggered run at merge time) — only `pull_request`-triggered checks were missing while #782 was open. Nobody applied the documented API fix (blocked by the tool classifier all session) and there's no evidence anyone used the UI toggle either, so what actually changed is unknown. GitHub exposes no way to read the `auto_trigger_checks` preference directly (confirmed — 404). Real proof either way is the next PR on this repo. _(added 2026-08-20)_
- [ ] **Icon/manifest (install to home screen) — parked on purpose**, Royce's own call, revisit whenever there's a logo ready. _(added 2026-08-20)_
- [ ] **Tier C (true offline write/save while disconnected) — still entirely unscoped.** _(added 2026-08-20)_

---

## eq-solves-service: PM calendar can now generate itself from contract dates — 3-regime date model, RRULE support, built end-to-end and shipped live in one session (2026-08-19)

**Deferred:**
- [ ] **`pm_roster_coverage` (the "is anyone rostered near this date" view) has no screen yet.** A real, live database view — nothing in the app UI shows it to anyone yet. _(added 2026-08-19)_
- [ ] **The generator was run for real once today (145/145 SKS scopes, all placeholder-dated 18 Oct) and then deliberately cleared same day.** The single real run made the classification gap visible immediately — 145 identical placeholder dates, no real scheduling value yet — so Royce chose to reset the live calendar to empty rather than leave that in front of the team. Cleared via soft-delete (`is_active = false`), not dropped: the generator, its migrations, and all 145 original rows are fully intact and recoverable. Re-run any time — most usefully once scope items actually carry a real hard/window classification (see the classification-gate entry above), at which point each reclassified scope moves off the shared placeholder date to its real one. _(added 2026-08-19)_

---

## eq-shell + eq-solves-service: who gets the calendar digest — rebuilt as a real permission, not a hardcoded list (2026-08-17 → 2026-08-19)

**Deferred (eq-service-specific — live production Netlify setting, needs your say-so):**
- [ ] **Digest sending is still paused on purpose (`SUPERVISOR_DIGEST_PAUSED=true`), until you say go.** Re-verified live 2026-08-19, unchanged since 2026-08-18, all contexts — no send has happened since 2026-08-16. Recipient count as of 2026-08-19: 21 people currently eligible (18 explicit members of the "Calendar Digest Recipients" group + the rest via the `manager` role default, which includes **you** and, per the 2026-08-18 note, `dev@eq.solutions` — still worth deciding if that system/test account should hold `manager` at all) — close to the 20 recorded 2026-08-18, difference not investigated. To add/remove a specific person: `core.eq.solutions/sks/admin/access-control` → Groups tab → "Calendar Digest Recipients". To change who gets it by role instead: same page, Base tab (role matrix) — `service.receive_calendar_digest` is manager-only by default today. Also worth knowing before unpausing: the PM calendar itself is empty right now (see the entry above) — an unpause today would have nothing real to send regardless. _(re-verified 2026-08-19)_

---

## eq-solves-service: notification bell was silently broken for anyone signed in through Shell — found, fixed, reviewed, merged, live (2026-08-17)
*Found while doing unrelated identity-canonicalization work — the notification bell's API route was checking who's signed in using a method that only works for the old, direct sign-in path. Anyone using Service through Shell (the normal way people reach it) has been getting a silent failure: the bell just shows nothing, no error, no explanation.*

**Deferred:**
- [ ] **Not clicked through live on a real Shell sign-in** — no way to produce one in this environment. Worth opening the bell once after this deploys to see it actually populate. _(added 2026-08-17)_
- [ ] **The cosmetic error-code mismatch the reviewer flagged** (wrong error code for a case that can't currently be reached) — left alone on purpose, your call if you want it tidied to match the other routes exactly. _(added 2026-08-17)_

---

## eq-service: ACB/NSX cover masthead + blank page 2 fixed; live Secondary Injection load bug found and fixed (2026-08-17)
*Royce reviewed a generated ACB Test Report (St George Private Hospital) and flagged four formatting issues plus one live-app discrepancy. Two formatting issues were confirmed bugs already fixed once elsewhere and never propagated to ACB/NSX — same recurring pattern as the 2026-08-14 NSX dead-fields fix below. The live-app discrepancy turned out to be a real, tenant-wide bug, not a stale report.*

**Deferred:**
- [ ] **"Approved by" has no real data source to wire to.** The DB carries unused `signature_technician_url` / `signature_site_url` / `signature_initials` columns from migration 0068 (2026-04), explicitly intended for exactly this, but no UI anywhere has ever captured them. Real feature gap, not a wiring fix — needs Royce's call on whether to build signature capture. _(added 2026-08-17)_
- [ ] **Masthead caption redundancy also exists on NSX, Work Order Details, and the Run-Sheet** — only dropped for ACB per Royce's explicit scoping this session. Revisit if he wants it dropped everywhere. _(added 2026-08-17)_
- [ ] **Secondary Injection load fix not click-tested live post-deploy** — verified via code trace (label-prefix mismatch confirmed against live DB data) plus a regenerated sample report, not by an actual technician reopening a check with saved SI data and watching the fields populate. Worth Royce doing that once. _(added 2026-08-17)_
- [ ] **One CI check failed on the merge (Integration tests), confirmed pre-existing and unrelated** — CI's local Supabase bootstrap is missing the `app_data` schema (migration 0152 fails: `schema "app_data" does not exist`), same class of gap PR #737 (merged earlier the same day) was meant to close. Worth checking whether #737's fixture guard actually covers this migration. _(added 2026-08-17)_

---

## eq-solves-service: ACB/NSX check saves could wipe a technician's readings on a dropped connection — fixed and shipped live (2026-08-18)
*A tech reported a check "wouldn't save / then deleted all the info" at site CA1, suspected offline-related. Root-caused: the ACB/NSX visual-check and electrical-reading saves deleted existing readings then inserted the new ones as two separate server calls — a dropped connection between them left the delete committed with nothing to replace it. Existing offline-safety measures (the banner, the pre-save connectivity check) can't catch this, since the failure window is between two server calls, not before the first one.*

**Deferred:**
- [ ] **In-progress form entries still live only in on-screen state with no draft save** — if a tech fills in readings and the page reloads/closes before they hit Save, that data is lost with no trace in the database at all (different from the bug just fixed, which was about data that *had* been saved). Real gap, not yet built. _(added 2026-08-18)_
- [ ] **Not click-tested live by a real technician** — verified via `tsc`/`next build` and a live database check, not by an actual on-site ACB/NSX save. _(added 2026-08-18)_

---

## eq-solves-service: Settings page showed broken account controls to Shell-embedded users — fixed, merged, live (2026-08-16)
*Started from Royce spotting UI on `core.eq.solutions/sks/service/settings` that "shouldn't be there" — a broken "Member Since: Invalid Date" caught the eye. Traced live against both databases: Service's own old sign-in record for the account and Shell's real one are two different IDs, so the settings page was looking up the wrong record every time someone reached it through Shell.*

**Deferred:**
- [ ] **Not clicked through live in either state.** No safe way to produce a working Shell login locally to test the fixed version, and the standalone side has no working test account — the practice/demo login has been broken since a database move in June and was never reconnected. Worth Royce opening `core.eq.solutions/sks/service/settings` once to eyeball it for real. _(added 2026-08-16)_
- [ ] **The practice/demo account is still broken** — unrelated to this fix, but found while trying to test it. Sign-in intentionally hides the "try the demo" option because it fails every time; worth reseeding if the demo link is still wanted. _(added 2026-08-16)_
- [ ] **The original question — what Shell's access-control screen looks like for Service permissions — wasn't followed up.** This session only got as far as the settings-page bug that jumped out first; the permissions-matrix screenshot Royce shared is still unreviewed. _(added 2026-08-16)_

---

## eq-solves-service: session-expiry Server Action crash (EQ-SOLVES-SERVICE-D) — root-caused, fixed suite-wide across ~120 call sites, merged (2026-08-14)

- [ ] **No manual browser smoke test yet** — need to actually expire a session mid-form-submit on a few touched pages and confirm the friendly "sign in again" message renders, rather than just type/unit verification. _(added 2026-08-14)_

---

## eq-service: migrations dispatched live; mobile check-detail header overflow found+fixed+deployed; eq-context accidental-checkout scare investigated (2026-08-13)

- [ ] **Not click-tested on a real phone** — same sandbox limitation as other recent mobile fixes (no path to complete the Shell-iframe auth handoff here). Verified instead via `tsc --noEmit` (clean) and a static Tailwind-class repro at 375px sent directly to Royce, plus confirming the live Netlify production deploy matches the merge commit. _(added 2026-08-13)_
- [ ] **No independent confirmation yet from the other session.** Messaged it directly via `send_message` with the full incident writeup, asking for its own explicit confirmation that nothing is missing — no reply received before this session closed. _(added 2026-08-13)_

---

## eq-service: RCD circuit pass/fail computed + auto-defect on fail — built, shipped, dispatched live (2026-08-10)

- [ ] **Remaining RCD improvements scoped but not built**: restructure the flat single-page circuit grid into the same 3-step wizard ACB/NSX use, and generalize the schema off Jemena's specific shape (hardcoded section labels, per-circuit ID field, calendar-month-driven test cycle) before a second customer needs RCD. _(added 2026-08-10)_

---

## eq-service: canonical-outbox schema-mismatch fixed, merged, verified live (2026-08-06)
*Follow-up on the `canonical_outbox` 404 flagged below — Royce asked for it explained "with pictures" and a solution, which turned diagnosis into a same-session fix.*

- [ ] **The `_health` 404 (a separate keep-warm ping, same ~5-min cadence) is still open** — not part of this fix, not investigated. `_health` genuinely doesn't exist on ehow; low priority, nothing depends on it succeeding. _(added 2026-08-06)_

---

## eq-solves-service: "Canonical types drift" CI check fixed — two live database columns were missing from the code's type definitions (2026-08-03)
*The scheduled CI check that catches "database changed but the code wasn't told" had been red on every run since 2026-08-01 — confirmed against the live database that this was real, not a broken check. Two columns landed by earlier features (a logo-linked-to-multiple-customers fix, and the site-supervisor feature) were never added to the code's committed type definitions. One of them was already being worked around with a type-safety bypass in the upload code.*

**Deferred:**
- [ ] **Confirm the scheduled nightly drift check itself shows green**, not just the one-off PR check — same logic, but hasn't been observed on a real nightly run yet. Should self-resolve. _(added 2026-08-03)_
- [ ] **The Supabase startup failure in CI** (a leftover database setting missing an `id` column, breaking the API's schema cache) is separate, pre-existing, and still red on every run — worth a dedicated fix at some point, not touched this session. _(added 2026-08-03)_
- [ ] **Separate, lower-priority**: one more stale-type warning (`tenant_settings.archive_grace_period_days`) traces to a database change from months ago that was never actually applied live — left alone on purpose, different job. _(added 2026-08-03, carried forward)_

---

## eq-solves-service: your site-supervisor save failure was a 6-day-old bug that had been silently breaking every site/asset edit — found and fixed (2026-08-02)
*Direct follow-up to the supervisor field below — you tried to save a real supervisor assignment (SY3, Pradeep Singh) and got "Could not update site access — please try again." Root-caused instead of just retrying.*

**Deferred:**
- [ ] **Royce to retry the actual save in the browser** to confirm end-to-end — DB-level fix is verified, only the real click-through confirms the full path. _(added 2026-08-02)_
- [ ] **Not swept: whether any of the other ~22 canonical objects (defects, contract_scopes, job_plans, maintenance_checks, etc.) have the same "trigger references a column the view doesn't expose" bug class.** This fix only covered the three objects (`customers`, `sites`, `assets`) touched by the 2026-07-27 change — no broader check across all canonical objects has been done. _(added 2026-08-02)_

---

## eq-solves-service: fixed a broken safety check that was silently skipping every code review, then found the "176,000 findings" it surfaced was almost entirely noise, cleaned up what was real (2026-08-01)
*A prior fix for a security warning (upgrading a bundled tool called "brace-expansion") turned out to also break a different, older tool ("minimatch") that the app's own automated code-quality check depends on. That check had been crashing outright on every fresh install, meaning it wasn't actually reviewing any pull request's code at all. Fixed, then dug into the huge number of findings the now-working check reported.*

**Deferred — two real follow-ups found along the way, each needs its own session:**
- [ ] **Saving/updating records through one part of the database layer has no real type-checking behind it** — turns out this is already known, tracked work (the app's own 30-day plan lists it), not a fresh find: the auto-generated database description file only covers the app's default section, but this data actually lives in a different section the file never describes, so the "trust me" overrides are a deliberate stand-in, not an accident. Confirmed live: the record it reads/writes from isn't a plain table, it's a view with its own custom save-behaviour attached — so even generating a fuller description file may not fully close the gap without extra work. Affects roughly 17 places. Needs the proper database tool run with the right settings (not available through the tools used this session), then each of the 17 spots checked by hand. _(added 2026-08-01, corrected 2026-08-01 — see below)_
- [ ] **Royce to click through live**: sidebar logo and the admin Media Library page (grid + edit modal) for a tenant with a logo set — confirm images still render correctly after the switch above. _(added 2026-08-01)_

---

## eq-solves-service: Found why photo uploads were failing everywhere, then added a link/create/skip option to the paste-import flow (2026-07-31)

**Deferred:**
- [ ] **Royce to click through the new paste-import resolve screen live** — built and type/build-checked clean, but not clicked through in a real browser session (no test login available in this environment). Paste a batch with an unmatched asset ID, try linking one and creating another, confirm the resulting check comes out right. _(added 2026-07-31)_
- [ ] **Two other places still lack any resolve option for unmatched rows**: the maintenance-check screen's own quick work-order paste (the simplest, position-only version) and the plain Assets spreadsheet import. Out of scope this round — same treatment could be added later if wanted. _(added 2026-07-31)_

---

## eq-solves-service: Contacts list now respects Shell's Service toggle + monthly PM sheet now imports directly (2026-07-29)
*Two asks in one session: (1) double-check the Service Users list and Contacts list are sourced from canonical, not a separate list — Users already was; Contacts turned out to leak past a toggle. (2) get "August PM.xlsx", Royce's monthly hand-copied work-order sheet, importing directly instead of manual entry.*

**Deferred:**
- [ ] **First real "August PM"-style import: the "BTCHGR" job plan code on Royce's file doesn't match any existing SKS job plan exactly** (closest is "24VBTCHGR") — the import wizard's existing fuzzy-match step will prompt to confirm or nominate a plan the first time this file type is actually committed. Not a bug, just a heads-up for whoever runs the first real import. _(added 2026-07-29)_

---

## eq-solves-service: Field Run-Sheet asset headers now show the maintenance plan's Job Code (2026-07-29)
*Royce shared a generated Run-Sheet (SY3, standard) and asked for the maintenance plan's Job Code to show on each asset — right now a tech sees ID/Location/WO on the printout but has no way to tell which maintenance plan an asset belongs to without looking it up separately.*

**Deferred:**
- [ ] **ACB/NSX breaker-card run-sheets and RCD test run-sheets don't show the Job Code** — Royce chose to scope this session to the standard maintenance checklist only; same gap exists in those report variants if wanted later. _(added 2026-07-29)_
- [ ] **Two other report types have the same missing-Job-Code gap**: the PM asset report and the work-order-details report already fetch/track job plan info per asset but only surface the plan *name*, never the *code*. Not touched this session — out of scope. _(added 2026-07-29)_
- [ ] **Royce to confirm PR #638 merged + spot-check a freshly generated Run-Sheet shows the Job Code line as expected.** _(added 2026-07-29)_

---

## eq-service: migration ledger reconciled and applied to live ehow (2026-07-28)

- [ ] **Decide whether to actually turn on scheduled notifications.** The groundwork ([PR #619](https://github.com/eq-solutions/eq-service/pull/619), applied to live ehow) is in place but deliberately left switched off — this is a business decision (should the app start emailing/notifying people on a schedule), not a technical one, and hasn't been made. _(added 2026-07-28, restates an earlier still-open item)_

---

## eq-service: finished the security-headers cleanup, cleared the dependency backlog, found the npm audit gate isn't fully fixable (2026-07-27)

- [ ] **Needs Royce's call: what to do about the still-red security scanner check.** Not urgent (verified no live exposure), but it won't turn green on its own — either wait for the linter/spreadsheet-library maintainers to catch up, or change what the check itself looks for so it stops flagging things already confirmed safe. **Re-checked live 2026-07-28: still red, same cause** — eq-solves-service's "CI" workflow, "Typecheck + audit" job, `npm audit` reports 16 high-severity findings, all from devDependency chains (`eslint-plugin-*` → `minimatch`; `exceljs`/`archiver` → `glob`/`readdir-glob` → `minimatch`) — none reachable from production code. Deliberately not touching this myself: loosening what a security gate checks is a policy call on the gate itself, not a same-scope fix, even though today's findings are all false-positive-for-this-app. Two real options if you want it green: (a) `npm audit --omit=dev` in CI (only fails on prod-dependency findings — the correct long-term fix, since dev-tooling CVEs can never be exploited in the shipped app), or (b) leave it red and just know why. _(added 2026-07-27, re-verified 2026-07-28)_

---

## eq-solves-service: branded loading spinner on the Shell sign-in handoff (2026-07-27)

- [ ] **Needs Royce's call: is cold start still bad enough to warrant an infra change?** Everything fixable in code has shipped — the only remaining lever is moving off the serverless runtime model (always-on server or edge) to a materially faster cold start, which is a real infrastructure decision, not a quick fix. Not pursued without Royce's go-ahead. _(added 2026-07-27)_

---

## eq-solves-service: Maintenance check Site/Assigned-To confirmed live + the report logo was the wrong, invisible variant — fixed (2026-07-23)
*Continuation of the same-day PR #599 session — Royce came back with a live screenshot confirming Site and Assigned To now display correctly, then asked why the Field Run-Sheet's logo looked wrong in Word's dark mode and out of position.*
- [ ] **Royce hasn't yet downloaded a fresh Run-Sheet to eyeball the fixed logo himself** — verified by generating and inspecting a sample file directly against the real SKS logo, not by his own click-through. _(added 2026-07-23)_

---

## EQ Service: Compliance Report logo follow-through, worktree bug re-hit and cleaned up, "wrong report" question resolved (2026-07-23)
*Continuation session: built the Compliance Report logo fix flagged above, then hit the exact "fake checkout" bug already tracked two entries up, and finally chased down a real question from Royce about whether the fix landed on the right report.*
- [ ] **2 of the leftover folders from the cleanup above are still stuck** — something else on this machine currently has them open, so they couldn't be deleted this session. Safe to remove once whatever's using them finishes; matches the same known bug pattern, not a new issue. _(added 2026-07-23)_

---

## eq-solves-service: fixed the SKS Thermals check crash, cleaned up a duplicate account, fixed Asset # display + export, and shipped funding-gap visibility on-site (2026-07-22/23)
*Started from a screenshot of a crashed maintenance check page, ran through a duplicate-account cleanup, a batch of asset-display bugs, and a new feature request, all in the same working session.*
- [ ] **The mojibake asset-name corruption (47 rows across 3 sites, stray "Â" characters from an old import) still isn't fixed.** Tried the one-line SQL fix twice, including once on your direct "go run it now" — both times it silently didn't take, a known non-deterministic quirk of the DB tool blocking certain live writes without erroring. Cosmetic only (the corrupted name still displays, nothing else is affected). **Needs you to run this once in the Supabase SQL editor on ehow:** `UPDATE app_data.assets SET name = replace(name, 'Â ', ' ') WHERE name ~ 'Â';` _(added 2026-07-23)_

---

## eq-solves-service: cleared two dead files, then closed out the two HIGH security warnings from the last audit (2026-07-22)
*Asked to double-check a suspected pair of dead files before deleting them, then to fix the security-scanner warnings that PR #582 (the Asset # display fix, built earlier the same day) had picked up along the way.*
- [ ] **CONFIRMED REAL, re-checked same day — the 2 remaining warnings genuinely can't be fixed right now, not even by choosing to accept a breaking change.** Re-queried the package registry directly today: the newest available release of both the framework and the spreadsheet library still carry the vulnerable piece — nothing shipped upstream since yesterday. True accepted risk, not a "we just haven't gotten to it" item. Nothing to do until the two library authors update their own dependency; re-check next time either one releases. _(confirmed 2026-07-23)_
- [ ] **CONFIRMED REAL, still actively happening — eq-solves-service's checkout is shared with other concurrent sessions, same as eq-shell.** Caught it live again while re-checking the item above: the checkout had switched to a 4th different branch with 6 more uncommitted files from a session that turned out to be doing its own separate multi-PR work (Asset # display fixes, a duplicate-account cleanup, a new feature) — not a one-off glitch, a structural fact about how this environment runs sessions. 4 occurrences across 2 days now. Real fix, not another workaround note: eq-shell already solves this with a registered-worktree convention (`eq-context/system/worktree-registry.md`) — eq-solves-service has no equivalent, so sessions default to the shared root instead of an isolated worktree. Worth setting up the same registry entry/convention for this repo. _(confirmed 2026-07-23)_

---

## eq-solves-service: brought the internal load-time write-up up to date with what's actually shipped (2026-07-23)
*Asked what's left on Service's "takes a while to load" issue, then to update the internal write-up to match reality.*
- [ ] **Nobody has re-measured real-world load time since the last speed fix landed.** The write-up now says so plainly — worth a real check next time Service feels slow to load, before assuming there's more to fix. _(added 2026-07-23)_

---

## eq-solves-service: found why two sessions kept colliding on the same files, and closed the door on it happening again (2026-07-23)
*Asked to fix the recurring "another session's changes appeared in my folder" problem this repo's shared checkout has caused several times now.*
- [ ] **The other fake folder (the one this very session was assigned to work in) still isn't a real private copy** — nothing unique lives inside it, so nothing was lost, but it can't be safely rebuilt as a proper private copy while a session is actively using it. Worth converting it properly next time no one's using it. _(added 2026-07-23)_

---

## EQ Service: the automated safety check has been failing on everything, for everyone (2026-07-21)
*Every code change in EQ Service goes through an automated check before it can ship. One part of that check — the one that scans for known security problems in third-party code the app depends on — had started failing on the main copy of the code itself, not on any one person's change. So every change anyone opened was born with a red light against it, regardless of whether anything was actually wrong with it. The real risk isn't the two flaws themselves; it's that a permanently-red light teaches everyone to ignore it, and then a genuine problem slips through unnoticed.*
- [ ] **Four lesser flaws deliberately left alone.** They're rated moderate rather than serious, and fixing them isn't a routine update — it would mean *downgrading* two major pieces of the app (the web framework itself, and the spreadsheet export library) by several major versions. That's a rewrite with real breakage risk, traded against flaws the safety check doesn't even consider serious enough to block on. Not recommended, and not urgent — noting it only so nobody re-discovers it and assumes it was missed. _(added 2026-07-21)_

---

## eq-solves-service: cold-start loading-time deep dive — found + fixed a bug in the app's own anti-slowness system, plus a smaller database-call cleanup (2026-07-21, MERGED + LIVE)
*Follow-up to the loading-time work below: Royce said in-app navigation now feels sharp, but opening the app fresh still takes a long while. Checked Netlify's dashboard for a way to give the app more power to start up faster — no such setting exists — which led to digging into what actually happens on a fresh load, and turned up a real bug along the way.*
- [ ] **Declined for now (Royce's call): make slow pages show a rough shell instantly while the slow parts load behind it.** Looked at it properly first: both pages already fetch their data in one efficient batch (this session's earlier fix), and the page layout itself depends on that data (a technician sees a completely different screen to a manager) — so there's less to gain here than first thought, and the two busiest pages in the app are a risky place to restructure without being able to click-test it signed in first. Presented the tradeoff; Royce said leave it. _(declined 2026-07-21)_

---

## eq-solves-service: full repo audit → database speed-up shipped and confirmed live, then two loading-time fixes, then found and fixed a broken "try the demo" button (2026-07-20)
*Asked for a general outstanding-work audit, which turned into a database performance fix; then asked to focus on loading times and user experience next, which turned into two speed fixes plus finding (and fixing) an unrelated broken feature along the way.*
- [ ] **Demo account/data still needs a proper rebuild whenever there's time for it** — matching what the site used to advertise (a small sample company with a few sites and some completed inspections) so prospects can click "try the demo" and see something real again. Not urgent; the button that pointed to it is gone for now. _(added 2026-07-20)_
- [ ] **Two small, low-value items looked at and deliberately left alone**: a handful of unused database indexes and a couple of overlapping row-check rules — real but minor, and touching them risked more than they'd save. _(added 2026-07-20)_
- [ ] **One dependency has a known minor security note with no real fix available** — fixing it would mean rolling the spreadsheet-import library back several versions, which would break more than it protects. Left as-is and documented. _(added 2026-07-20)_

---

## EQ Service — NSX/ACB testing lists fixed in the Shell iframe + Field Run-Sheet now carries recorded breaker details AND results (2026-07-15, ALL MERGED + LIVE)
*Three fixes on the same thread same day. First: opening NSX or ACB Testing inside Shell showed "No checks yet" even when checks existed — Royce hit this live on a real SKS check (DigiCo Annual NSX). Root cause: those two screens (plus the Test Equipment cert-history panel) fetched data straight from the browser, but inside the Shell frame there's no login session for the browser to use, so the read silently came back empty. Moved those reads onto the server — fixed. Second: the printable Field Run-Sheet was dropping breaker nameplate details (brand/model/serial/etc.) that a tech had already recorded on-site — fetched from the database then thrown away before reaching the printout. Fixed + given a regression test. Third (Royce caught this from a fresh export): the run-sheet's tick-boxes and readings were ALSO always blank even when a step showed Complete in the app — first thought to be deliberate (the existing "print empty, complete on site" design), but Royce confirmed he wants recorded results shown, so that's now wired through too. Also fixed printed asset order (was click-order from setup, now alphabetical/numeric).*
- [ ] **Small, low-risk: rename the "Field Run-Sheet" button** — Royce noticed it's not obvious this is the report/export button (reads as a document name, not an action, and sits next to "Print Blank for Onsite" which does read as an action). Recommended "Download Run-Sheet" or "Export Run-Sheet" — label-only change, no rename of the underlying feature/code/tests. Awaiting Royce's go-ahead. _(added 2026-07-15)_

---

## EQ Service reports — now render each tenant's real brand, and auto-update (2026-07-14, BUILT + MERGED + LIVE)
*Maintenance run-sheets and reports were coming out in EQ's sky-blue with no logo. They now render in SKS's own document colours (navy + purple + grey) with the SKS logo on every page. And it's self-maintaining: change the logo or colours in the admin brand settings and reports pick it up automatically on the next login — no manual step, and it works the same for any future tenant.*
- [ ] **Cleanup, anytime: the old manual colour copy for SKS can be trimmed** now the pipe is self-maintaining — but keep the white on-dark logo, which the admin settings don't carry yet. _(added 2026-07-14)_

---

## ✅ EQ Service — Test Equipment = canonical plant & equipment + calibration canonical + cert chain (2026-07-14, ALL MERGED + LIVE)
*Royce: plant & equipment (test gear — meters, testers, torque wrenches) should appear in Service's Test Equipment register (renamed from Instrument Register), one version wired to the existing canonical schema — they are NOT maintainable assets, don't confuse the two. Then: calibration is canonical (the cert chain is relevant across Field/Shell/Service). Full arc shipped this session.*
- [ ] **Ops-brief "service due" now surfaces only calibration gear.** After Phase 3, `fetchServiceDue` reads `asset_calibration.calibration_due` (plant_equipment/calibration). If maintainable-asset PPM-due should ALSO appear in the morning brief, source it from `maintenance_checks`/`eq_ppm_*` — `assets.next_service_due` is unpopulated (0/2830) so it was never a live signal, not a regression. _(added 2026-07-14)_
- **Substrate correction:** `assets.last_service_date/next_service_due/cert_url` are NOT calibration-only — they're SHARED asset-service columns feeding `eq_ppm_asset_status/overdue/site_summary`, the dashboard, and intake. So "retire the columns" ≠ drop; plant_equipment just stops using them. (Phase 3 respects this — it stops the 3 eq-shell consumers touching them, never drops.)
- **Substrate note:** newly created `service`-schema views inherit `arwd` (INSERT/UPDATE/DELETE for `authenticated`) from an `ALTER DEFAULT PRIVILEGES` rule (granted by postgres). Pure read-through views MUST explicitly `REVOKE` the write grants; views with INSTEAD OF triggers are unaffected (the trigger intercepts all DML).

---

## EQ Service — SY9 import verified correct + "balloon years" feature proposed (2026-07-13)
*Deep-dive audit of the SY9 (Equinix) import against how every other site imports. Everything checks out; one small consistency fix applied; the multi-year-major pricing gap it exposed is now a proposed fleet-wide feature.*
- [ ] **Balloon years — later phases (P2/P3) when you want them.** P2: auto-suggest each asset's balloon year from the source schedule dates (so you confirm rather than type). P3: the scheduler/run-sheet lists the exact units due in the balloon year. P1 (this session) already delivers the funding-correctness + the nomination data those build on. _(added 2026-07-14)_

---

## ⏩ Session close — 2026-07-10 (eq-service) — dashboard + Customers page now respect the App Activation "Service" toggle (3 migrations, all live)

*Continuation of the earlier same-day Shell-embed session. Royce, viewing the live SKS dashboard, asked why a switched-off customer (Jemena) still showed. Traced it to the dashboard's summary reads bypassing the `service_enabled` filter the rest of the app uses; fixed sites, then customers+assets, then discovered+fixed a hidden empty-Customers-page bug. Also confirmed the earlier eq-shell chrome fix is live and answered two architecture questions.*

**Deferred / open:**
- [ ] **Top-bar "SKS Technologies" logo alignment** (Shell chrome) — Royce's original complaint #2 from 2026-07-07, NOT covered by eq-shell #696 (which only touched the collapsed rail), never pixel-audited. Needs a fresh screenshot to trace. _(added 2026-07-10)_
- [ ] **Canonical answer to record: "in-Service" is SITE-driven.** The `service_enabled` switch lives on `app_data.sites`. A customer/asset is in-Service iff it owns / sits on a service-enabled site. The customer-level `app_data.customers.service_enabled` flag is **dead** (0 rows, every tenant) — someday populate it or drop it, but nothing reads it meaningfully now. _(added 2026-07-10)_
- [ ] **`service.assets` vs dashboard off-by-one on `active`:** the assets view has no `active` filter (would show 346 incl. 1 archived asset) while the dashboard tile keeps `active` (345). Cosmetic; noted in case a future "why 345 vs 346" question arises. _(added 2026-07-10)_
- Dashboard slow-load duration canary (from the earlier close) is live — still awaiting its first real event before any optimisation.

---

## ⏩ Session close — 2026-07-07/08 (eq-service) — Shell-embed session bug fully root-caused across 4 shipped PRs; dashboard duration canary added; a live CI-trigger outage found and fixed along the way

*Royce reported the exact "workspace isn't set up" + wrong-chrome screenshot that an earlier same-day session (see the eq-shell chrome-fix entry below) had already partly traced. Ran it to ground across 4 separate deployed fixes, each confirmed live before moving to the next, rather than shipping one guess and declaring victory.*

**Still open (unchanged from the earlier same-day eq-shell session's note, not resolved by this session):**
- [ ] `task_14031bea` — a tenant-logo clip issue is still tracked against `ShellSessionRecovery`'s fallback UI. Correction: the component built in PR #469/#475 renders no logo at all (text + spinner + buttons only) — if a clip is still visible, it's the surrounding Sidebar/Shell chrome rendering around it, not this component itself. _(added 2026-07-08)_
- [ ] **Netlify cold-start as a possible slow-dashboard cause** — proposed (a lightweight scheduled "warm ping", same pattern as the 3 existing Netlify scheduled functions in this repo) but not built; wait for the new duration canary's first real event before spending effort here. _(added 2026-07-08)_
- [ ] **Further dashboard query consolidation** (fold the sequential site-name lookup + maybe upcoming/recent-checks into the counts RPC, one round-trip instead of several) — real DB-migration work, deferred pending real performance data from the new canary. _(added 2026-07-08)_
- [ ] **First-party edge reverse-proxy** (serve `core.eq.solutions/sks/service/*` through a rewrite instead of an iframe) — the architectural endgame if the CHIPS cookie fix (#474) ever fails on another browser; not needed now since CHIPS is confirmed working. _(added 2026-07-08)_

---

## ⏩ Session close — 2026-07-08 (eq-service) — Generic RCD job plan created + Equinix RCD checks seeded live

*Follow-on from the earlier import-audit session, which found Equinix's 4 contracted sites carry RCD scope but zero RCD checks (the RCD-seed feature needs a customer RCD job plan, and only Jemena had one). Royce: "we need to create generic RCD testing... common task" then "seed the RCD checks for Equinix now" — both done live, no code change (data-only, verified via the canonical write path).*

- [ ] **CA1 still not enabled via core** — its 2 new RCD checks exist but are invisible in the app until `service_enabled` is flipped. Royce is handling this himself. _(carried, Royce-owned)_
- [ ] **Whether the EQ tenant (zaap) also needs a generic RCD plan** — not asked, not built. _(added 2026-07-08, needs a decision if EQ ever contracts RCD work)_

---

## ⏩ Session close — 2026-07-08 (eq-service) — Contract-import wiring audit + job-plan coverage report shipped

*Full review of the import → asset-list pipeline (job plans, assets, RCD checks, canonical adherence), with an infographic of what's broken/missing. Shipped the one clear code fix (coverage reporting); the reconcile items (site enablement, missing contracts) Royce is handling directly, not delegated.*

- [ ] **Reconcile (Royce doing directly):** enable CA1 via core (has a contract, currently disabled — 163 contracted units invisible in-app); import approved sheets for SY2/SY6/SY7 (enabled via core, no contract imported yet). _(added 2026-07-08, Royce-owned)_
- [ ] **RCD checks can't seed for Equinix** — 0/4 contracted sites have an RCD check because the RCD-seed feature (PR #465) needs an RCD job plan for the customer, and Equinix has none (only Jemena does). Needs an Equinix (or global) RCD job plan created before re-import will help. _(added 2026-07-08, needs a job-plan decision)_
- [ ] **2 SKS job plans have zero tasks** — `ELGLV` (E1.37) and `SCADA/PLC` (E1.40). Now caught by the new coverage report if a contract matches them, but the plans themselves still have no checklist. _(added 2026-07-08, needs job-plan content)_

---

## ⏩ Session close — 2026-07-06 (eq-solves-service) — asset reconciliation screen built, shipped, migrated live, pilot-verified

*Royce: "important that the commercial sheet adds in the assets" — commercial-sheet imports write contracted job-plan quantities into `app_data.contract_scopes` but had never created a single real asset (verified live: 3,605 contracted units across 4 sites, zero linked assets). Royce picked shape C: a full reconciliation screen, not just an opt-in checkbox. Built, reviewed, fixed, shipped, migrated live, and pilot-verified end-to-end same session.*

**Shipped:**

**Decided:**
- Royce: shape C (full reconciliation screen) over a lighter opt-in checkbox.
- Pilot on CA1 first (smallest of the 4 sites with real contract-scope data) — operational choice via the site picker, not hardcoded.
- Stub `asset_type` = the resolved job plan's own `type` column (real equipment-type text) — never a made-up sentinel like `'unverified'`, which would pollute the existing asset-type filter.
- `isAdmin` gate on the reconciliation screen's read + both commit actions (bulk stub-generation can create hundreds of rows, same blast radius as the import it's downstream of); `markAssetVerifiedAction` stays `canWrite` (routine single-row field verification).

**Deferred:**
- [ ] **Keep-or-clean-up call on the CA1/E1.27 pilot asset** (`cbf535d9-a03f-4952-9396-7ae6c6e765ad`) — asked Royce at session end, no answer yet. It's a real, correctly-created stub asset; leaving it just means one fewer gap for the real UI run. _(added 2026-07-06, needs your call)_
- [ ] **Full CA1 reconciliation** — only 1 of ~19 job-plan gaps closed (the pilot). Remaining ~18 job plans at CA1, then SY1/SY3/Head Office once CA1 is fully reviewed. _(added 2026-07-06)_
- [ ] **SKS "workspace isn't set up yet" screen resurfaced** — Royce hit this live on `core.eq.solutions/sks/service/dashboard` mid-session. Same known, pre-existing issue: SKS tenant's `setup_completed_at` has been NULL since tenant creation (a backfill migration ran 11 days before the tenant existed, missing it by timing). Not caused by this session's work. A fix reportedly already exists on an unshipped branch (migration 0115, per earlier project memory) — not verified or shipped this session, still open. _(carried, resurfaced 2026-07-06)_
- [ ] **Sentry — 2 of the original 5 still open**: `EQ-FIELD-M` (leave_requests null staff_id, eq-field) and `EQ-CARDS-Z` (provisionTenantExchange 500, eq-cards) — not investigated this session, different repos. _(added 2026-07-06, needs a session per repo)_

**Notes:**
- **Durable Postgres lesson, same family as the 0169 security_invoker incident:** `CREATE OR REPLACE VIEW` requires every pre-existing output column to keep both its name AND its ordinal position — new columns can ONLY be appended at the very end of the `SELECT` list, never inserted in the middle. Inserting mid-list gets read as an illegal column rename (`42P16`) and the whole statement is rejected (transaction rolls back atomically — confirmed live, no partial damage). Should probably get the same weight as the security_invoker rule in eq-solves-service's CLAUDE.md given it already bit a migration once.
- **`get_assets_for_grouping` (public schema RPC) is a second, easy-to-miss surface** whenever `service.assets` gains a column — `/assets`'s default view mode (grouped, not flat table) sources from this RPC's explicit `jsonb_build_object` field list, not the flat table's `select('*')`. A column added only to the view/triggers is invisible in the default UI until this RPC is updated too.
- **`service.tenant_members` confirmed EMPTY for SKS, live** (checked while sourcing a real user_id for the pilot's audit-log write) — the canonical roster has fully moved elsewhere; querying `auth.users.raw_app_meta_data->>'tenant_id'` was the only way to find a real SKS-scoped user this session. Worth confirming with the "Service canonical identity" project thread whether `tenant_members` is now safe to formally retire.
- **Testing RLS/trigger-gated writes from raw SQL**: `assert_jwt_tenant()` and similar SECURITY DEFINER guards read `auth.jwt()`, which resolves from the `request.jwt.claims` Postgres GUC. `SET LOCAL request.jwt.claims = '{"app_metadata": {"tenant_id": "..."}}'` inside a transaction is the standard, sanctioned way to exercise a real authenticated code path from an admin SQL connection without fabricating a persistent user or bypassing the tenant check itself (the guard still fully enforces — a mismatched claim still throws). Used for the CA1 pilot since no real browser session/credentials were available in this environment.
- Migration `0171` (`canonical_outbox` restore, unrelated to this session's own work, pre-existing pending item) applied cleanly in the same dispatch run as `0172`/`0173` — its `CREATE TABLE IF NOT EXISTS` was a no-op (table already existed out-of-band) but its ledger row is now correctly backfilled.
---

## ⏩ Session close — 2026-06-30 (ARMADA trial) — pre-baked Calum's fleet on eq-service

**Completed:**

**Config tuning (eq-service `.armada/config.json`):**
- `autoMerge: false` (HARD — main is unprotected + Netlify auto-deploys on push to main; sole rail vs a prod deploy)
- gate = `npm run check` (tsc + next build); `test` omitted (integration suite is a known pre-existing CI failure)
- `armadaRepo: calumjs/ARMADA`; `publicIntake` + `lighthouse` auto-dispatch off

**Deferred (added 2026-06-30):**
- [ ] **Run first `shipwright` build** of #377 — in a dedicated Claude Code session rooted in eq-service (skills load from its `.claude/skills/`; can't be driven from another repo's session). Runbook in SETUP-NOTES + today's session log _(added 2026-06-30)_
- [ ] **crows-nest `/loop`** — needs `CLAUDE_PLUGIN_ROOT` (plugin install, or `export CLAUDE_PLUGIN_ROOT=.claude/armada`); don't arm until one clean manual cycle is observed _(added 2026-06-30)_
- [ ] **Add `test: vitest run`** to eq-service `.armada/config.json` once a clean cycle is seen + unit-test green verified _(added 2026-06-30)_

**Notes (load-bearing):**
- eq-service: GitHub repo = `eq-solutions/eq-service`, local folder = `eq-solves-service`; `.claude/` is gitignored, so vendored skills are **local-only** (not committed — correct for a vendored plugin).
- ARMADA drop-in: `charter`/`shipwright`/`muster`/`lighthouse` are path-clean (work without the plugin); `crows-nest`'s pipeline + foghorn/logbook/spyglass need `${CLAUDE_PLUGIN_ROOT}`, which only the plugin installer sets.
---

## ⏩ Session close — 2026-06-29 — SKS data reset + maintenance check page perf

**Completed:**

**Discovered:**
- `service.assets` view does NOT filter on `active = true` — it only filters by `service_enabled` site. Soft-delete is invisible to the view. Hard-delete was the right call for the reset.

**Deferred:**
- [ ] SKS contract scope reimport — Royce to run via `/sks/service/commercials/contract-scopes/import` _(added 2026-06-29)_
---

## ⏩ Sprint 7 — EQ Service cutover (urjh → ehow) — 2026-06-08

**Done:** Schema (28 CMMS tables) + data + 9 storage files migrated to ehow;
Netlify env vars (Supabase URL/keys, SITE_URL, Sentry) swapped; code domain
refs updated (PR #257 → main, open); repo on `eq-solutions/eq-service`.

**Follow-on tasks:**
- [ ] **`canonical_field_id` gap** — live-checked 2026-07-27: `service.sites` still shows 11/11 rows with `canonical_field_id = NULL` (site count itself has shrunk from the original 37 — worth confirming that's expected). The bridge from EQ Service sites to EQ Field dispatch is still not wired. Separate task, not blocking anything. (Surfaced during Sprint 7 canonical-id audit.)
---

## EQ Solves Service

- [ ] **Delta WO import — live dry-run** on SKS tenant with Aug 2025 file:
      confirm ~250 rows resolve, MVSWBD fuzzy prompt fires, LBS unknown-code
      prompt works, commit succeeds, re-upload triggers duplicate blocker
- [ ] Full-repo file-header backfill (EQ-IP-Register P2 #7 scope A) —
      dedicated session

---

## EQ Service — canonical audit + contacts consolidation (2026-07-02)

- [ ] **Contacts Steps 4-5 (post-soak)** — after ~1-2 weeks green: JSON-backup then DROP `service.customer_contacts_legacy_20260702` + `site_contacts_legacy_20260702`, flip drift guard `consistency.sor_drift.shadow_contact_tables` (audits/run.sql) WARN→ERROR (count must be 0). Watch during soak: /contacts (~229 rows now, was 109), customer/site contact CRUD, portal unsubscribe, notification cron. _(added 2026-07-02)_

## EQ Service — dashboard/defects triage + migration governance (2026-07-03)

- [ ] **Optional backlog surfaced, not started:** (a) ~30 files across eq-service using hard-coded status-pill `<span>` classes instead of the canonical `StatusBadge` component — too broad to sweep unprompted, needs a scoped decision on which pages first; (b) 167 routine Supabase performance-advisor findings on eq-service's own tables (66 `auth_rls_initplan`, 44 `multiple_permissive_policies`, 30 `unindexed_foreign_keys`, 27 `unused_index`) — all WARN/INFO, zero ERROR, a normal RLS/index cleanup backlog not an active problem. _(added 2026-07-03, needs your call on whether either is worth a dedicated pass)_

---

## Suppliers/site-credentials feature — likely never worked, found via a live grant sweep, needs your call before any fix (2026-08-20)

*Prompted by a real question earlier today about a different app (does eq-field have login PINs — it does). Answering it surfaced a known, never-fully-checked risk: a migration can write a `GRANT` right after creating a function and that grant can still end up missing live. Rather than leave that as a vague worry, ran the actual check — every function in the guarded schemas on all three databases (jvkn, zaap, ehow) with no `anon`/`authenticated` grant, cross-referenced against every real call site in eq-cards, eq-shell, eq-field and eq-solves-service to see which of those "locked-down" functions the apps actually try to call directly. Almost everything came back clean — correctly locked to service-role only, exactly as designed. One genuine hit.*

- [ ] **The Suppliers directory (`/api/site-credentials`, built 2026-07-21 — "SKS Ops: Suppliers directory + role-gated credentials") is provably broken today, on all three of its moving parts, and may never have worked.** Checked live, not assumed:
  - **List (`GET /api/site-credentials`)** queries `.from('site_credentials')` through a plain user-session client (no explicit schema), which PostgREST resolves to `public`. **There is no `site_credentials` table in `public` at all** — checked directly, zero rows returned from `information_schema.tables`. This call should error, not just return empty.
  - **Decrypt and create/update** (`decrypt_site_credential()` / `upsert_site_credential()`) are called the same way — real user session, not service-role (confirmed by reading `getApiUser()` directly: every path returns a JWT-scoped client, never an admin one). Both functions currently have **`authenticated_exec: false`** live — checked directly, not inferred. Both calls should 42501 (permission denied).
  - **The migration that built this (`0123_site_credentials_encryption.sql`) was edited after it was already applied.** The live database ran an older version — pulled the actual applied SQL out of the migration ledger and compared it line-by-line against the file on disk. The applied version writes to `app_data.site_credentials`; the current file describes a 2026-06-13 rework moving everything to `public.site_credentials` "because PostgREST can't see app_data" — a real, sound reason, but that rework was never re-run against the live database. Whoever edited the file believed it had shipped; it hadn't.
  - **The functions live today still write to `app_data.site_credentials`** (confirmed via `pg_get_functiondef` on the actual running function, not the file) — **0 rows.** A third table, `service.site_credentials`, also exists with the identical (encrypted-column) structure — also **0 rows** — and isn't wired to either the read or the write path. Three plausible homes for this data (`app_data`, `public`, `service`); the live write path targets one, the live read path expects a different one that doesn't exist, and the schema-convention-correct one (`service.*`, per this repo's own operational-data convention) sits unused.
  - **Net effect: every part of this feature — viewing the list, decrypting a password, saving a new one — is currently non-functional**, and given all three candidate tables are empty, it's plausible nobody has ever completed the flow end-to-end since it shipped a month ago. Consistent with the original 2026-07-21 session's own notes (`sks/pending.md`): both follow-up "confirm this works" items were left unchecked, and the tester only ever had a manager session available.
  - **Not fixed here — this needs a design call before any code changes, not a mechanical grant fix.** Re-adding the missing grants alone would make the RPCs *callable* but they'd still write into `app_data.site_credentials`, disconnected from what the read path expects and from the schema-correct `service.site_credentials` table sitting empty. The real fix is picking ONE schema (almost certainly `service`, matching how the rest of this repo's operational tables are organised) and re-pointing all three pieces (the GET route's query, both RPC function bodies, and the grants) at it together, then applying that as one migration. Live production DDL, current-architecture judgement call — your decision, not a default. _(added 2026-08-20)_

