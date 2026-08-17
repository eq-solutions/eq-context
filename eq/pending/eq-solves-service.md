---
title: EQ Service — Pending Actions
owner: Royce Milmlow
last_updated: 2026-08-17
scope: EQ Service engineering backlog, split out of eq/pending.md (2026-08-17) so a session working in this repo isn't wading through the other 8 repos' items too. Same conventions as before: "- [ ]" open, "- [x]" done (rotated out nightly by scripts/rotate_pending.py), "- [~]" in progress.
read_priority: critical
status: live
---

# EQ Service — Pending

Split out of `eq/pending.md` (2026-08-17) — see `eq/pending.md` for why. SKS items live in `sks/pending.md`. OPS items (entities, tax, infra) in `ops/pending.md`.

---

## eq-service: ACB/NSX cover masthead + blank page 2 fixed; live Secondary Injection load bug found and fixed (2026-08-17)
*Royce reviewed a generated ACB Test Report (St George Private Hospital) and flagged four formatting issues plus one live-app discrepancy. Two formatting issues were confirmed bugs already fixed once elsewhere and never propagated to ACB/NSX — same recurring pattern as the 2026-08-14 NSX dead-fields fix below. The live-app discrepancy turned out to be a real, tenant-wide bug, not a stale report.*

- [x] `buildMasthead()` (shared by ACB, NSX, Work Order Details, and the Run-Sheet) rebuilt as a percentage-width table so the tenant logo pins hard-right on every cover — the old tab-stop layout never reliably reached the margin.
- [x] Removed a leading `PageBreak` before the ACB/NSX table of contents that produced a genuinely blank page 2 on every report — same defect already fixed in `pm-check-report.ts` on 2026-08-01, never propagated to ACB/NSX.
- [x] Dropped the redundant "ACB Test Report" masthead caption on ACB (Royce's call) — it repeated both the cover title and the running page header.
- [x] ACB/NSX sign-off "Prepared by" + a completion-status line now populate from real per-breaker `tested_by` / `overallResult` data instead of always rendering blank underscores.
- [x] **Found and fixed a live production bug**: `SecondaryInjectionTable`'s `loadSiFunction()` matched saved reading labels without the `Electrical: ` category prefix the save action actually stores them with (every other field on the same tab got this right). Result: the Long Time / Short Time / Instantaneous fields always loaded blank on reopen, for every ACB and NSX test, tenant-wide, regardless of what was saved — confirmed live against a real SKS check with saved readings that were rendering correctly in the generated report but blank in the app itself.
- [x] eq-service PR [#745](https://github.com/eq-solutions/eq-service/pull/745) merged to `main` (commit `2aa779c`), auto-deploys to service.eq.solutions.

**Deferred:**
- [ ] **"Approved by" has no real data source to wire to.** The DB carries unused `signature_technician_url` / `signature_site_url` / `signature_initials` columns from migration 0068 (2026-04), explicitly intended for exactly this, but no UI anywhere has ever captured them. Real feature gap, not a wiring fix — needs Royce's call on whether to build signature capture. _(added 2026-08-17)_
- [ ] **Masthead caption redundancy also exists on NSX, Work Order Details, and the Run-Sheet** — only dropped for ACB per Royce's explicit scoping this session. Revisit if he wants it dropped everywhere. _(added 2026-08-17)_
- [ ] **Secondary Injection load fix not click-tested live post-deploy** — verified via code trace (label-prefix mismatch confirmed against live DB data) plus a regenerated sample report, not by an actual technician reopening a check with saved SI data and watching the fields populate. Worth Royce doing that once. _(added 2026-08-17)_
- [ ] **One CI check failed on the merge (Integration tests), confirmed pre-existing and unrelated** — CI's local Supabase bootstrap is missing the `app_data` schema (migration 0152 fails: `schema "app_data" does not exist`), same class of gap PR #737 (merged earlier the same day) was meant to close. Worth checking whether #737's fixture guard actually covers this migration. _(added 2026-08-17)_

---

## eq-solves-service: any signed-in worker — apprentice, labour hire, subcontractor — could write maintenance checks, defects, test results and assets straight to the database, skipping every in-app permission check. Fixed, shipped, and confirmed live (2026-08-16)

**Deferred:**
- [ ] **Not clicked through live.** The database change is live on production now — worth two minutes to confirm a low-privilege account (apprentice/labour hire/subcontractor) actually gets blocked from writing, and that an assigned technician can still update their own job. Needs a real signed-in session, not checkable from here. _(added 2026-08-16)_

---

## eq-solves-service: Settings page showed broken account controls to Shell-embedded users — fixed, merged, live (2026-08-16)
*Started from Royce spotting UI on `core.eq.solutions/sks/service/settings` that "shouldn't be there" — a broken "Member Since: Invalid Date" caught the eye. Traced live against both databases: Service's own old sign-in record for the account and Shell's real one are two different IDs, so the settings page was looking up the wrong record every time someone reached it through Shell.*

- [x] Confirmed live (not guessed): the "Update Profile" button was quietly doing nothing — it looked like it saved, but matched zero records — and "Change Password" would have failed outright, since it was pointed at a sign-in record that doesn't exist for anyone using it through Shell.
- [x] Fixed: for anyone using Service through Shell, that section now just points them to Shell to manage their name, email and password — the same way the branding settings already do. Nothing changed for people who sign in to Service directly.
- [x] Merged and confirmed live on service.eq.solutions ([PR #733](https://github.com/eq-solutions/eq-service/pull/733)).

**Deferred:**
- [ ] **Not clicked through live in either state.** No safe way to produce a working Shell login locally to test the fixed version, and the standalone side has no working test account — the practice/demo login has been broken since a database move in June and was never reconnected. Worth Royce opening `core.eq.solutions/sks/service/settings` once to eyeball it for real. _(added 2026-08-16)_
- [ ] **The practice/demo account is still broken** — unrelated to this fix, but found while trying to test it. Sign-in intentionally hides the "try the demo" option because it fails every time; worth reseeding if the demo link is still wanted. _(added 2026-08-16)_
- [ ] **The original question — what Shell's access-control screen looks like for Service permissions — wasn't followed up.** This session only got as far as the settings-page bug that jumped out first; the permissions-matrix screenshot Royce shared is still unreviewed. _(added 2026-08-16)_

---

## eq-solves-service: NSX Test Report fixed — dead ACB-only fields left it always printing blank sections (2026-08-14)
*Simon Bramall reported an ACB check's report came out empty in some sections. ACB's report wiring traced clean end-to-end (every field has a real collection path). The NSX Test Report, though, still carried template rows copy-pasted from ACB that the NSX workflow never actually collects.*

- [x] Removed Performance Level, Protection Unit Fitted, and Earth-Leakage Tripping Delay from the NSX report's breaker-details table — NSX has no data for any of them (no earth-leakage column even exists on the table).
- [x] Removed the Main Contact Resistance table — Royce deliberately stopped NSX from collecting that reading back in May, but the report kept showing an empty table for it on every single NSX report since.
- [x] eq-service PR [#731](https://github.com/eq-solutions/eq-service/pull/731) merged, deployed live on service.eq.solutions (confirmed via Netlify — deploy `6a7ef65d`, production, matches the merge commit).

**Deferred:**
- [ ] **Not click-tested against a real generated NSX report** — fix verified via typecheck + code trace only; worth Royce pulling a real NSX Test Report next time one's generated to eyeball the CB Details table looks right. _(added 2026-08-14)_

---

## eq-solves-service: /admin/* pages closed to non-managers (2026-08-14)
*Royce: gate the remaining Admin pages that were reachable by any signed-in technician who typed the URL directly — the sidebar hid the link, but that's not access control. A prior sweep (PRs #707-#727) had already closed 3 of 9 admin pages; this closed the rest.*

- [x] **Gated the last 6 ungated `/admin/*` pages (hub, users, settings, media, reports, backup) to managers only.** Before this, any signed-in technician who typed the URL directly could see the full team roster (names, emails, phones), branding settings, and download a full workspace backup. eq-service [PR #728](https://github.com/eq-solutions/eq-service/pull/728), merged (Royce's "merge the PR once CI passes" go) and confirmed live on service.eq.solutions (Netlify deploy `commit_ref` matches the merge commit exactly, secret scan clean).
- [x] Deliberately left `admin/imports` and `admin/activity` on their existing, slightly wider permission (manager **or** supervisor, from PR #709) instead of tightening everyone to manager-only — a blanket gate would have silently undone that earlier, confirmed decision.
- [ ] **Not click-tested by a real non-manager account** — no such login was available in this environment. Worth Royce confirming a technician account gets bounced off `/admin/*` now. _(added 2026-08-14)_

---

## eq-solves-service: session-expiry Server Action crash (EQ-SOLVES-SERVICE-D) — root-caused, fixed suite-wide across ~120 call sites, merged (2026-08-14)

- [ ] **No manual browser smoke test yet** — need to actually expire a session mid-form-submit on a few touched pages and confirm the friendly "sign in again" message renders, rather than just type/unit verification. _(added 2026-08-14)_
- [ ] **Old branch `fix/session-expiry-server-action-errors` left with a redundant commit** (`df74500`, content-identical to the now-merged #725) — harmless, but worth deleting next time someone's in eq-service. _(added 2026-08-14)_

---

## eq-service: migrations dispatched live; mobile check-detail header overflow found+fixed+deployed; eq-context accidental-checkout scare investigated (2026-08-13)

- [ ] **Not click-tested on a real phone** — same sandbox limitation as other recent mobile fixes (no path to complete the Shell-iframe auth handoff here). Verified instead via `tsc --noEmit` (clean) and a static Tailwind-class repro at 375px sent directly to Royce, plus confirming the live Netlify production deploy matches the merge commit. _(added 2026-08-13)_
- [ ] **No independent confirmation yet from the other session.** Messaged it directly via `send_message` with the full incident writeup, asking for its own explicit confirmation that nothing is missing — no reply received before this session closed. _(added 2026-08-13)_

---

## eq-service: RCD circuit pass/fail computed + auto-defect on fail — built, shipped, dispatched live (2026-08-10)

- [ ] **Remaining RCD improvements scoped but not built**: restructure the flat single-page circuit grid into the same 3-step wizard ACB/NSX use, and generalize the schema off Jemena's specific shape (hardcoded section labels, per-circuit ID field, calendar-month-driven test cycle) before a second customer needs RCD. _(added 2026-08-10)_

---

## eq-service: app_data CI fixture — manifest fixed + merged (#737), DDL bootstrap snapshot still blocked (2026-08-16)

- [ ] **DDL bootstrap snapshot (`0000_app_data_tenant_plane_fixture.sql`) still stale — needs `supabase db dump --linked` from a machine with working IPv4/DB connectivity.** The JSON shape-manifest half is fixed and live (regenerated straight from ehow via the Management API, merged in [eq-service#737](https://github.com/eq-solutions/eq-service/pull/737)) — enough to make the new weekly drift-check pass. The SQL DDL fixture itself wasn't refreshed: this environment's `supabase db dump --linked` fails on an IPv6-only network with no cached DB password — a different, more specific blocker than the earlier Docker one (not hit this session; the manifest route queries live ehow directly and bypasses Docker/local `supabase start` entirely). Possibly the root cause of the pre-existing `Integration tests (Supabase local)` CI failure (`schema "app_data" does not exist` at migration 0061) — not confirmed. _(added 2026-08-16)_

---

## eq-solves-service: maintenance_checks is_active/deleted_at sync gap (2026-08-10)
*Surfaced while chasing down a "68-day overdue" check flagged in `TODAY.md`'s FACTS refresh — that check turned out to be soft-deleted, which led to finding and fixing 3 unfiltered by-ID read/write paths ([eq-service PR #693](https://github.com/eq-solutions/eq-service/pull/693), merged). This is the one real gap found but not fixed that session.*

- [ ] **`archiveTestingCheckAction` (`app/(app)/testing/check-actions.ts`) soft-deletes via `is_active: false` only — never stamps `deleted_at`.** The auto-stamping `set_deleted_at` trigger (migration `0035`) was only ever created on `public.maintenance_checks`; production reads/writes `app_data.maintenance_checks`, which has no such trigger. `service.maintenance_checks`'s `INSTEAD OF UPDATE` trigger (migration `0147`) just echoes back whatever `deleted_at` already was — it doesn't stamp `now()` either.
- **Verified live impact, 2026-08-10: currently benign.** Of 35 total rows, 2 have `is_active=false` with `deleted_at` still null (the sync gap is real, not theoretical) — but 0 rows have `is_active=true` with `deleted_at` set, so nothing is leaking through the app's `is_active`-based filters today. Latent, not active.
- **Why it's still worth fixing:** the Archive page's grace-period/auto-purge countdown (migrations `0035`, `0193`) reads `deleted_at`. For those 2 rows, that countdown either never started or is silently wrong.
- **Fix options, neither built:** (a) have `archiveTestingCheckAction` stamp `deleted_at: new Date().toISOString()` explicitly alongside `is_active: false` — smaller, safer, one call site; (b) create the missing `set_deleted_at` trigger on `app_data.maintenance_checks` to match `public.maintenance_checks` — more durable, catches every future archive path, not just this one action.

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
- [ ] Add `WHERE a.active = true` to `service.assets` view so soft-delete works correctly _(added 2026-06-29)_
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

