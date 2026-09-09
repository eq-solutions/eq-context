---
title: EQ Service — Pending Actions
owner: Royce Milmlow
last_updated: 2026-09-09
scope: EQ Service engineering backlog, split out of eq/pending.md (2026-08-17) so a session working in this repo isn't wading through the other 8 repos' items too. Same conventions as before: "- [ ]" open, "- [x]" done (rotated out nightly by scripts/rotate_pending.py), "- [~]" in progress.
read_priority: critical
status: live
---

# EQ Service — Pending

Split out of `eq/pending.md` (2026-08-17) — see `eq/pending.md` for why. SKS items live in `sks/pending.md`. OPS items (entities, tax, infra) in `ops/pending.md`.

**Budget:** ~500 lines. `- [x]` items already auto-rotate out nightly via `scripts/rotate_pending.py`; past this line count even so, propose moving the oldest stale open items to `eq/pending-archive.md`. (`rules/tidy-protocol.md` Step 5, 2026-09-07.)

---

## eq-solves-service: cross-tenant roster leak found and fixed — MERGED, LIVE (SEC-76, 2026-09-09)
*Surfaced during a research pass scoping a suite-wide tenant-identity-drift doc in eq-context. `lib/canonical-members.ts` defaulted an unset tenant slug to `'sks'`, and 19 call sites across 15 files called the roster functions bare (no tenant argument) — assignee dropdowns, notification recipients (incl. the pre-visit-brief cron), report "tested by"/"assigned to" names, the audit log, and the admin user roster all silently rendered SKS's staff regardless of the actual signed-in tenant. Independently re-verified against live code before touching anything — grep found the same 19 sites, same lines, the handed-in report named. Logged as [SEC-76](../../ops/security-register.md).*

- [x] Made the tenant argument required on `getCanonicalMembers`/`getCanonicalMemberMap` (no more silent default) — turns any missed call site into a `tsc --noEmit` compile error, which is how completeness was verified. Added `getCanonicalMemberMapForTenantId` alongside the existing `getCanonicalMembersForTenantId`, fixed a related edge case in `supervisor-digest.ts`, and threaded `tenantId` through `resolve-user-names.ts`'s 5 callers.
- [x] **[PR #838](https://github.com/eq-solutions/eq-service/pull/838) — merged, live on service.eq.solutions.** Merged via admin override past 2 pre-existing, unrelated failing checks (chronic `npm audit` finding on `js-yaml`/`next`/`sharp`; this repo's chronically-broken integration-test suite) — `tsc + next build`, the real gate, was clean. Live-verified after merge via Netlify + commit ancestry that the fix reached production, not just `main`.
- Was not live-exploitable at the time — only SKS existed as a tenant on ehow — but was a primed landmine for the next one.

**Deferred:**
- [ ] **`lib/canonical-sync.ts` also reads `CANONICAL_TENANT_SLUG`** — separate consumer, deliberately left out of scope for this fix; worth checking whether it has the same class of issue. _(added 2026-09-09)_
- [ ] **No live click-test against a second tenant** — can't be exercised until a second tenant (e.g. a re-provisioned `favour-perfect`) exists; verify then that a non-SKS session shows its own roster, not SKS's. _(added 2026-09-09)_

---

## eq-solves-service: embedded Shell nav bar was unusable on iPad — found via a cross-suite iPad audit, fixed, merged, live (2026-09-08)
*Royce asked what options exist for using Claude/EQ via iPad, which led to checking whether the EQ apps themselves render properly on one. They don't — none of EQ Field, EQ Service, or EQ Shell had ever been designed for a width between phone and desktop. Checked all three live; EQ Field turned out to already be fixed by a parallel session. This repo's specific problem: the nav bar shown when Service is embedded in Shell (Field/Service iframe mode) had no wrap or scroll handling, so every iPad width cut off the last link(s) with no way to reach them.*

- Added `overflow-x-auto` to the embedded nav bar and `shrink-0` to each link so it scrolls instead of silently clipping — the underlying `md:` breakpoint itself was deliberately left untouched, since it's the same boundary Shell's own mobile nav hands off at; moving it would have opened a real gap instead of closing one. [PR #837](https://github.com/eq-solutions/eq-service/pull/837), merged, confirmed live via exact commit-ref match on the Netlify deploy record.
- Verified via an isolated reproduction of the actual classes at real iPad widths (768px and 1400px, before/after comparison) — not a live authenticated click-through, no Shell/demo credentials in this environment.

**Deferred:**
- [ ] **Dashboard's `grid-cols-4` tiles and the shared Table component don't reflow at any width** — a separate, real gap found during the same audit, out of scope for the nav fix. _(added 2026-09-08)_
- [ ] **Not click-tested live by a person** — no Shell/demo credentials in this environment. Worth a real pass at iPad width once convenient. _(added 2026-09-08)_

---

## eq-solves-service: new-PC environment setup + full Dependabot/CI-health batch cleared, PR #791 (report reissue) shipped live (2026-09-07)
*Fresh PC — verified the dev environment (deps, Node/npm, git/gh auth all fine; `.env.local` had to be rebuilt from scratch since it's gitignored and never travels with a clone). Cleared the 5 aging Dependabot PRs (#810–#814), which surfaced two real, unrelated problems along the way: 4 dead permission keys from the `@eq-solutions/roles` v2.7.0 bump (cross-checked live against eq-shell — 3 belong to its user-admin surface, 1 is dead suite-wide, same as eq-shell's own baseline already treats it) and a fresh high-severity `npm audit` advisory against `browserslist` (pre-existing in the lockfile before today, unrelated to any of the bumps — fixed via `overrides` rather than npm's own suggested fix, which would have downgraded the whole service-worker toolkit; PR #830). Also resolved a 16-day-stale merge conflict on #791 and shipped it — that path now sends real customer email in production.*

**Deferred:**
- [ ] **`EQ_SECRET_SALT` / `EQ_SERVICE_JWT_SECRET` exist in Netlify but production-context only** — not pulled into local dev; Royce's call whether local should reuse the real production shared-HMAC value or stay on the `SUPABASE_JWT_SECRET` fallback. _(added 2026-09-07)_
- [ ] **PR #791 is now live in production but its click-through still hasn't happened** — blocked all session on the missing service-role key above; see the 2026-08-20 entry below for the original build's own still-open click-test item. _(added 2026-09-07)_

---

## eq-solves-service: attachment uploads were completely broken for everyone — root-caused, fixed, shipped live; a related security gap in the same feature closed too (2026-09-04/05)

- [ ] **Upload screen trusts the browser's claimed file type — deliberately left as-is.** Royce's call: the risk (a trusted staff member mislabeling a file for another staff member at the same company to open) is real but bounded, and tightening it risks rejecting real uploads in a way that can't be tested here (no working phone-camera-upload test path in this environment). Revisit if there's ever a real incident, or once there's a way to click-test uploads live. _(added 2026-09-05)_
- [ ] **Evidence attachments advertise "Photos / videos" on-screen, but video files are silently rejected today.** Nobody has decided whether to actually support video (which would also need a bigger size limit than the current 10MB). _(added 2026-09-05)_
- [ ] **The file-storage system itself allows bigger files (50MB) with no type restriction at its own level** — the app's own rules (10MB, specific file types only) are tighter, so this only matters if something ever writes to file storage directly instead of through the app. Low priority. _(added 2026-09-05)_
- [ ] **Not click-tested live by a real technician.** The fix was verified against the live database directly (both the broken state and the fixed state), not by an actual person uploading or deleting a file on the maintenance check page. _(added 2026-09-05)_

---

## eq-solves-service: 4-axis service review → full P0/P1 sprint built and shipped live, including a critical cross-tenant leak found and closed (2026-08-31)

- [ ] **Live authenticated UX click-through never done.** This worktree had no `.env.local`; copying the working credentials from the main checkout was correctly blocked by the permission classifier as a credentials-file action. The UX rating (6/10) is built on a full source-level consistency audit, not hands-on interaction — worth a real pass once a session has working dev credentials. _(added 2026-08-31)_
- [ ] **Relay 2 live ERROR-level advisor findings to whoever owns them — not this repo's fix.** `app_data.field_managers` / `field_people_directory` are SECURITY DEFINER views with no migration in eq-solves-service; they belong to Field or Shell's canonical schema. Re-confirmed live 2026-09-07 (Supabase security advisors), still both ERROR. _(added 2026-08-31)_

---

## eq-solves-service: automated tests added for the compliance-reports page, merged, live (2026-08-21)
*Continuing the same day's push to get real automated test coverage across the app, one page at a time (maintenance checks, then ACB/NSX/RCD testing pages, now Reports). Built in its own isolated copy of the repo rather than the shared one, since the shared one was busy with another session's database work at the time.*

**Deferred:**
- [ ] Cross-app documentation of the isolated-copy setup (which files a fresh isolated copy is missing by default, like local settings) wasn't updated — worth a note somewhere so the next session doesn't lose time on the same false alarm. _(added 2026-08-21)_

---

## eq-solves-service: destructive-delete RPC missing a role check — found, fixed, verified live (2026-08-21)
*Went looking for the next real, non-duplicate piece of work while the fleet's other obvious threads were already covered. Found `service.hard_delete_archived_entity` — the function behind the admin archive page's permanent-delete button — checked which tenant you belonged to but not what role you held: any signed-in team member, any role, could call it directly and permanently destroy an archived customer, site, asset, job plan, or maintenance check. The app's own "admin only" button was doing the right check; the database underneath it wasn't. Caught before duplicating work: another session had already found and fixed the same thing (PR #794) — confirmed that independently rather than building a second copy.*

**Deferred:**
- [ ] Tier C's `service.audit_logs` mystery (why on-site test entries never get an audit trail row) — the theory written into the merged Tier C scoping doc doesn't hold up under closer reading of the actual code: the mechanism it blamed is deliberate and demonstrably works fine elsewhere. Real cause still unknown. The fast way to actually answer it is one error-tracker query rather than more code reading, and that tool wasn't reachable this session. _(added 2026-08-21)_

---

## eq-solves-service: the automated safety-check suite has been unable to fully test itself since April — fixed past two blocking bugs, a third is being fixed live in an open PR (2026-08-20)
*Found while checking whether the report-reissue fix above actually got tested — asked directly "did the integration tests pass?", which surfaced that the CI check which spins up a fresh test database has been broken since migration 0042 (mid-April). Root-caused two separate, stacked bugs and fixed both. That let the test database get built roughly 120 database updates further than before it hit the next thing missing — which turned out to be a bigger, separate gap now being closed in its own follow-up.*

**Deferred:**
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

## eq-solves-service: branded loading spinner on the Shell sign-in handoff (2026-07-27)

- [ ] **Needs Royce's call: is cold start still bad enough to warrant an infra change?** Everything fixable in code has shipped — the only remaining lever is moving off the serverless runtime model (always-on server or edge) to a materially faster cold start, which is a real infrastructure decision, not a quick fix. Not pursued without Royce's go-ahead. _(added 2026-07-27)_

---

## eq-solves-service: Maintenance check Site/Assigned-To confirmed live + the report logo was the wrong, invisible variant — fixed (2026-07-23)
*Continuation of the same-day PR #599 session — Royce came back with a live screenshot confirming Site and Assigned To now display correctly, then asked why the Field Run-Sheet's logo looked wrong in Word's dark mode and out of position.*
- [ ] **Royce hasn't yet downloaded a fresh Run-Sheet to eyeball the fixed logo himself** — verified by generating and inspecting a sample file directly against the real SKS logo, not by his own click-through. _(added 2026-07-23)_

---

## eq-solves-service: fixed the SKS Thermals check crash, cleaned up a duplicate account, fixed Asset # display + export, and shipped funding-gap visibility on-site (2026-07-22/23)
*Started from a screenshot of a crashed maintenance check page, ran through a duplicate-account cleanup, a batch of asset-display bugs, and a new feature request, all in the same working session.*
- [ ] **The mojibake asset-name corruption (47 rows across 3 sites, stray "Â" characters from an old import) still isn't fixed.** Tried the one-line SQL fix twice, including once on your direct "go run it now" — both times it silently didn't take, a known non-deterministic quirk of the DB tool blocking certain live writes without erroring. Cosmetic only (the corrupted name still displays, nothing else is affected). **Needs you to run this once in the Supabase SQL editor on ehow:** `UPDATE app_data.assets SET name = replace(name, 'Â ', ' ') WHERE name ~ 'Â';` _(added 2026-07-23)_

---

## eq-solves-service: brought the internal load-time write-up up to date with what's actually shipped (2026-07-23)
*Asked what's left on Service's "takes a while to load" issue, then to update the internal write-up to match reality.*
- [ ] **Nobody has re-measured real-world load time since the last speed fix landed.** The write-up now says so plainly — worth a real check next time Service feels slow to load, before assuming there's more to fix. _(added 2026-07-23)_

---

## eq-solves-service: full repo audit → database speed-up shipped and confirmed live, then two loading-time fixes, then found and fixed a broken "try the demo" button (2026-07-20)
*Asked for a general outstanding-work audit, which turned into a database performance fix; then asked to focus on loading times and user experience next, which turned into two speed fixes plus finding (and fixing) an unrelated broken feature along the way.*
- [ ] **Demo account/data still needs a proper rebuild whenever there's time for it** — matching what the site used to advertise (a small sample company with a few sites and some completed inspections) so prospects can click "try the demo" and see something real again. Not urgent; the button that pointed to it is gone for now. Re-confirmed live 2026-09-07: no demo tenant exists (checked both the known demo tenant ID and name/slug match). _(added 2026-07-20)_

---

## EQ Service — NSX/ACB testing lists fixed in the Shell iframe + Field Run-Sheet now carries recorded breaker details AND results (2026-07-15, ALL MERGED + LIVE)
*Three fixes on the same thread same day. First: opening NSX or ACB Testing inside Shell showed "No checks yet" even when checks existed — Royce hit this live on a real SKS check (DigiCo Annual NSX). Root cause: those two screens (plus the Test Equipment cert-history panel) fetched data straight from the browser, but inside the Shell frame there's no login session for the browser to use, so the read silently came back empty. Moved those reads onto the server — fixed. Second: the printable Field Run-Sheet was dropping breaker nameplate details (brand/model/serial/etc.) that a tech had already recorded on-site — fetched from the database then thrown away before reaching the printout. Fixed + given a regression test. Third (Royce caught this from a fresh export): the run-sheet's tick-boxes and readings were ALSO always blank even when a step showed Complete in the app — first thought to be deliberate (the existing "print empty, complete on site" design), but Royce confirmed he wants recorded results shown, so that's now wired through too. Also fixed printed asset order (was click-order from setup, now alphabetical/numeric).*
- [ ] **Small, low-risk: rename the "Field Run-Sheet" button** — Royce noticed it's not obvious this is the report/export button (reads as a document name, not an action, and sits next to "Print Blank for Onsite" which does read as an action). Recommended "Download Run-Sheet" or "Export Run-Sheet" — label-only change, no rename of the underlying feature/code/tests. Awaiting Royce's go-ahead. _(added 2026-07-15)_

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
- [ ] **`service.assets` vs dashboard off-by-one on `active`:** the assets view has no `active` filter (would show 346 incl. 1 archived asset) while the dashboard tile keeps `active` (345). Cosmetic; noted in case a future "why 345 vs 346" question arises. _(added 2026-07-10)_
- Dashboard slow-load duration canary (from the earlier close) is live — still awaiting its first real event before any optimisation.

---

## ⏩ Session close — 2026-07-07/08 (eq-service) — Shell-embed session bug fully root-caused across 4 shipped PRs; dashboard duration canary added; a live CI-trigger outage found and fixed along the way

*Royce reported the exact "workspace isn't set up" + wrong-chrome screenshot that an earlier same-day session (see the eq-shell chrome-fix entry below) had already partly traced. Ran it to ground across 4 separate deployed fixes, each confirmed live before moving to the next, rather than shipping one guess and declaring victory.*

**Still open (unchanged from the earlier same-day eq-shell session's note, not resolved by this session):**
- [ ] `task_14031bea` — a tenant-logo clip issue is still tracked against `ShellSessionRecovery`'s fallback UI. Correction: the component built in PR #469/#475 renders no logo at all (text + spinner + buttons only) — if a clip is still visible, it's the surrounding Sidebar/Shell chrome rendering around it, not this component itself. _(added 2026-07-08)_
- [ ] **Further dashboard query consolidation** (fold the sequential site-name lookup + maybe upcoming/recent-checks into the counts RPC, one round-trip instead of several) — real DB-migration work, deferred pending real performance data from the new canary. _(added 2026-07-08)_
- [ ] **First-party edge reverse-proxy** (serve `core.eq.solutions/sks/service/*` through a rewrite instead of an iframe) — the architectural endgame if the CHIPS cookie fix (#474) ever fails on another browser; not needed now since CHIPS is confirmed working. _(added 2026-07-08)_

---

## ⏩ Session close — 2026-07-08 (eq-service) — Generic RCD job plan created + Equinix RCD checks seeded live

*Follow-on from the earlier import-audit session, which found Equinix's 4 contracted sites carry RCD scope but zero RCD checks (the RCD-seed feature needs a customer RCD job plan, and only Jemena had one). Royce: "we need to create generic RCD testing... common task" then "seed the RCD checks for Equinix now" — both done live, no code change (data-only, verified via the canonical write path).*

- [ ] **Whether the EQ tenant (zaap) also needs a generic RCD plan** — not asked, not built. _(added 2026-07-08, needs a decision if EQ ever contracts RCD work)_

---

## ⏩ Session close — 2026-07-08 (eq-service) — Contract-import wiring audit + job-plan coverage report shipped

*Full review of the import → asset-list pipeline (job plans, assets, RCD checks, canonical adherence), with an infographic of what's broken/missing. Shipped the one clear code fix (coverage reporting); the reconcile items (site enablement, missing contracts) Royce is handling directly, not delegated.*

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
- [ ] **crows-nest `/loop`** — needs `CLAUDE_PLUGIN_ROOT` (plugin install, or `export CLAUDE_PLUGIN_ROOT=.claude/armada`); don't arm until one clean manual cycle is observed _(added 2026-06-30)_
- [ ] **Add `test: vitest run`** to eq-service `.armada/config.json` once a clean cycle is seen + unit-test green verified _(added 2026-06-30)_

**Notes (load-bearing):**
- eq-service: GitHub repo = `eq-solutions/eq-service`, local folder = `eq-solves-service`; `.claude/` is gitignored, so vendored skills are **local-only** (not committed — correct for a vendored plugin).
- ARMADA drop-in: `charter`/`shipwright`/`muster`/`lighthouse` are path-clean (work without the plugin); `crows-nest`'s pipeline + foghorn/logbook/spyglass need `${CLAUDE_PLUGIN_ROOT}`, which only the plugin installer sets.
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

  **CORRECTED 2026-09-07, re-checked live, not assumed carried-forward:** the schema-consolidation part of the fix above has actually happened since this was written — `app_data.site_credentials` no longer exists at all; only `service.site_credentials` remains (0 rows), and `decrypt_site_credential`/`upsert_site_credential` now both read/write that table, matching the schema-correct recommendation. The original "`authenticated_exec: false`" claim is now **false**: live grant check today shows `authenticated_can_execute = true` on both functions. They do enforce tenant isolation in-body (`auth.jwt()` claim checked against the row's `tenant_id`, raises on mismatch) and `decrypt_site_credential` requires a caller-supplied key it wouldn't otherwise know — so this isn't a cross-tenant leak, and there's nothing live to actually expose (table still empty). But the core open question is unchanged: these RPCs are callable directly by any authenticated tenant member, not gated to admin/manager at the database layer the way the app's own UI presumably intends. Same decision as before, just on more current footing — pick a DB-layer gating approach (or explicitly accept the current one) before this table ever holds real data.

