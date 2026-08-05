---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-05
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-05 12:20 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-05 12:09 UTC → 2026-08-05 12:20 UTC)

- Merged: eq-shell [#1245](https://github.com/eq-solutions/eq-shell/pull/1245) feat(field): Bearer credential so Field can trigger a Shell-
- Merged: eq-shell [#1243](https://github.com/eq-solutions/eq-shell/pull/1243) refactor(workers): simplify invite header to two actions
- Merged: eq-shell [#1240](https://github.com/eq-solutions/eq-shell/pull/1240) feat(staff): "back on file" indicator for licence photos
- Merged: eq-shell [#1237](https://github.com/eq-solutions/eq-shell/pull/1237) fix(staff): hide Company field for Direct, require supervisi
- Merged: eq-shell [#1235](https://github.com/eq-solutions/eq-shell/pull/1235) fix(licences): timeout the OCR auto-read chain instead of ha
- Merged: eq-shell [#1234](https://github.com/eq-solutions/eq-shell/pull/1234) feat(staff): back-photo support in admin licence backfill
- Merged: eq-shell [#1233](https://github.com/eq-solutions/eq-shell/pull/1233) fix(deps): bump fast-uri to 4.1.2 (CVE-2026-18446)
- Merged: eq-shell [#1232](https://github.com/eq-solutions/eq-shell/pull/1232) fix(invites): recover gracefully from a raced duplicate invi

## ⚠ Needs you (9)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Cron failing** — `index-drift.yml` 6 consecutive scheduled run(s) failed, last success 2026-07-29 · [failures.md](system/failures.md) F11
- 🔴 **Cron failing** — `jwt-contract-drift.yml` 10 consecutive scheduled run(s) failed, no success in recent history · [failures.md](system/failures.md) F11
- 🔴 **Cron failing** — `pending-rotate.yml` 4 consecutive scheduled run(s) failed, last success 2026-07-31 · [failures.md](system/failures.md) F11
- 🔴 **Guard bypass? rung 4** — F7: git merge/stash-pop round-trip NUL-fills files on the C:\Projects virtiofs mount · possibly recurred in [2026-08-05.md](sessions/2026-08-05.md) · [failures.md](system/failures.md)
- 🟠 **Sentry new error** — `eq-shell` [Cards handoff request from unexpected origin](https://eq-solutions.sentry.io/issues/138655603/)
- 🟠 **Cron failing** — `adversarial-suite.yml` 1 consecutive scheduled run(s) failed, last success 2026-08-03 · [failures.md](system/failures.md) F11
- 🟠 **Cron failing** — `backup-eq-canonical.yml` 1 consecutive scheduled run(s) failed, last success 2026-08-04 · [failures.md](system/failures.md) F11

## 🙋 Waiting on you (104)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Not click-tested on a real iOS device with Field added to the home screen** — Royce to confirm the maps icon now hands off to the Maps app instead of doing nothing. _(added 2026-08-05)_
- **EQ** · **Royce to confirm the SKS dashboard loads cleanly** — needs an authenticated session, off-limits for Claude to drive. _(added 2026-08-05)_
- **EQ** · **Not click-tested live by a real signed-in user** — everything above was verified at the function level and via the deploy preview's boot path, not by an authenticated session actually seeing the widget populate with real people. Royce to confirm on `field.eq.solutions` (or the Shell embed) that Birthdays & Anniversaries now shows up reliably from a fresh Dashboard landing. _(added 2026-08-05)_
- **EQ** · **Neither fix has been click-tested live** — Royce to confirm: (1) the address fields save and display correctly on a real staff member, desktop and mobile, (2) re-downloading William's compliance pack now shows "William Hong" instead of "Unknown." _(added 2026-08-05)_
- **EQ** · **Not click-tested live** — Royce to confirm a real future-dated new starter actually disappears from the roster/dispatch/timesheets and shows up correctly in the new Starting Soon widget. _(added 2026-08-05)_
- **EQ** · **Not click-tested live with real populated canonical data** — needs an authenticated worker session (`canon-read` requires a real session token); same gap as the Starting Soon item above. Royce to confirm a worker with an expiring Cards licence actually surfaces on the dashboard card. _(added 2026-08-05)_
- **EQ** · **None of the four PDF-import/pricing-table changes above have been click-tested live yet** — all need an authenticated Shell admin session, off-limits for me to drive. Royce to confirm: (1) Materials save-all + archive behaves correctly on the live setup page, (2) dragging a PDF onto the Jobs page actually fires the import in a real browser, (3) the Cost/Sell toggle on the main "From PDF" button — especially that a real sell-priced supplier PDF now computes cost correctly, and the default Cost path is unchanged, (4) the *same* toggle now also appearing on the second "Import from PDF" button inside the New Quote form when a document has ambiguous pricing. _(added 2026-08-05, updated 2026-08-05)_
- **EQ** · **Royce to test on his Samsung/Android Chrome** now that the code and the SMS template are live together for the first time — not yet confirmed working end-to-end. No fix exists for iOS Safari (WebOTP isn't implemented there); manual entry stays as-is on that platform.
- **EQ** · **Not click-tested live** — no way to drive a real cross-origin Field session from this environment. Royce to confirm: open Field as an SKS admin, click "🏷 Edit category" on a supervisor, change category/role, save, confirm it reflects back on Shell's own Staff page. _(added 2026-08-05)_
- **EQ** · **Not confirmed by Royce on the real embedded session** — everything above was verified against a standalone repro (deploy preview + forced `.shell-mode` class), not the actual `core.eq.solutions/sks/field` iframe Royce was looking at (no way to drive that cross-origin session from this environment). Royce to hard-refresh (or bypass the service worker) and confirm the nav bar is back. _(added 2026-08-05)_
- **EQ** · **Sign-off records can be read or overwritten by any signed-in person on the same tenant, not just the person they belong to.** Investigated 2026-08-04 (sprint task T1): the obvious fix (`signer_user_id = auth.uid()`) would break real signing — eq-field's data-plane JWT sets `sub` to the tenant id for every user, not the actor, so `auth.uid()` on the real sign path never equals the signer. Closing this needs an identity-model decision, not a migration. Royce's call: leave deferred, revisit alongside a real second-signer rollout. _(updated 2026-08-04)_
- **EQ** · **Show mode not yet click-tested on a real device with network disabled.** Verified: analyzer clean, full test suite (255 tests) passes, `flutter build web` succeeds and boots with zero console errors via a static preview — but never signed in as a real worker and tapped it (real login is off-limits for me to do on Royce's behalf). Royce to confirm brightness/wakelock/offline behaviour actually work as intended. _(added 2026-08-03)_
_…and 92 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 0 | — |
| eq-solves-service | ✓ success | 1d ago | 5 | 2d |
| eq-field | ✓ success | 0d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: Workers never invited to join, past grace period: 44](https://eq-solutions.sentry.io/issues/135740258/) | 14 | 2026-08-04 |
| eq-solves-service | [UnrecognizedActionError: Server Action "40f8ab2385de590826648056ec7fc02ebdd51eb8](https://eq-solutions.sentry.io/issues/122209933/) | 10 | 2026-08-01 |
| eq-shell | [Cards handoff request from unexpected origin](https://eq-solutions.sentry.io/issues/138655603/) | 9 | 2026-08-05 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 9 | 2026-08-05 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 5 | 2026-08-04 |
| eq-shell | [Error: app_data.staff.cards_worker_id pointing at missing jvkn workers: 7](https://eq-solutions.sentry.io/issues/138175643/) | 4 | 2026-08-04 |
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/137265513/) | 4 | 2026-07-29 |
| eq-shell | [Error: staff-licence-ocr: ocr-licence returned 401](https://eq-solutions.sentry.io/issues/135986280/) | 3 | 2026-08-04 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-05 | eq-shell | [#1256](https://github.com/eq-solutions/eq-shell/pull/1256) fix(observability): stop mislabeling render crashes as chunk-erro |
| 2026-08-05 | eq-shell | [#1255](https://github.com/eq-solutions/eq-shell/pull/1255) fix(briefing): validate submit_briefing tool output before trusti |
| 2026-08-05 | eq-shell | [#1254](https://github.com/eq-solutions/eq-shell/pull/1254) fix(ops): wire the cost/sell question into the other Import from  |
| 2026-08-05 | eq-shell | [#1253](https://github.com/eq-solutions/eq-shell/pull/1253) feat(documents): bulk category assignment for the Templates tab |
| 2026-08-05 | eq-shell | [#1251](https://github.com/eq-solutions/eq-shell/pull/1251) feat(staff): add home address fields to Staff edit (desktop + mob |
| 2026-08-05 | eq-shell | [#1250](https://github.com/eq-solutions/eq-shell/pull/1250) fix(staff): compliance-pack export shows Unknown for names only e |
| 2026-08-05 | eq-shell | [#1252](https://github.com/eq-solutions/eq-shell/pull/1252) feat(ops): ask cost vs. sell when importing a subcontractor PDF |
| 2026-08-05 | eq-shell | [#1249](https://github.com/eq-solutions/eq-shell/pull/1249) feat(ops): drag a subcontractor PDF onto the Jobs home page to st |
| 2026-08-05 | eq-shell | [#1248](https://github.com/eq-solutions/eq-shell/pull/1248) fix(ops): widen Description column and batch-save outlet pricing  |
| 2026-08-05 | eq-shell | [#1247](https://github.com/eq-solutions/eq-shell/pull/1247) feat(field): relay a mint-entity-patch-token credential to the Fi |
| 2026-08-05 | eq-field | [#656](https://github.com/eq-solutions/eq-field/pull/656) v3.5.461 — Dashboard licence-expiry alert is now supervisor-only |
| 2026-08-05 | eq-field | [#655](https://github.com/eq-solutions/eq-field/pull/655) v3.5.459 — My Schedule maps link silently did nothing on iOS home |
| 2026-08-05 | eq-field | [#654](https://github.com/eq-solutions/eq-field/pull/654) v3.5.459 — Dashboard licence alert now reads canonical EQ Cards l |
| 2026-08-05 | eq-field | [#653](https://github.com/eq-solutions/eq-field/pull/653) v3.5.458 — dashboard: fix intermittent blank Birthdays & Annivers |
| 2026-08-05 | eq-field | [#652](https://github.com/eq-solutions/eq-field/pull/652) v3.5.457 — Shell-embedded nav: narrow iframe left with no nav at  |
_Showing 15 of 139 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **Only the last 10 days of signups were checked for the stuck-appMetadata pattern** — the 4 unblocked accounts are the ones caught in that window; any self-join/auto-provision-only account older than that with a never-updated `raw_app_meta_data` would still show the same symptom if they ever come back and retry. No full historical audit run. _(added 2026-08-05)_
- **William's own Cards `public.workers.first_name/last_name` is still blank** (`""`, unchanged since signup) even though his Shell `app_data.staff` record now has his real name — the compliance-pack fix below makes Shell's copy win for that one export, but anything else that reads Cards' own `workers` table directly for display would still show blank for him specifically. Not backfilled. _(added 2026-08-05)_
- **Dashboard tab has no manager-only gate** — every logged-in staff member (not just supervisors) can already see every other staff member's name + licence-expiry status on this card; this session's change widens what flows through that same surface (adds the canonical pool) but doesn't newly expose it. Whether the card itself should be manager-gated is a real open design question, surfaced but not decided or built. _(added 2026-08-05)_
- **Worth a look: `digest.md`'s "Recently built" table shows merge status, not deploy status, for every repo — but eq-cards is the one repo where those two are allowed to diverge for hours by design.** A merged eq-cards PR currently reads identically to a live one on the digest, which is exactly what caused this session's confusion. Might be worth a "manual-deploy pending" flag specific to eq-cards, or a general merged-vs-deployed distinction if other repos ever adopt the same manual-gate pattern.
- **Why the iframe actually went narrow on Royce's real machine is still unconfirmed.** Leading candidate: DevTools was docked open in his screenshots, which alone can shrink the page's available width below 768px. An alternative not ruled out: Shell's own layout being disrupted by the React #418 hydration error below. The v3.5.457 fix doesn't need to know which (it closes the gap for "narrow for any reason"), but if the no-nav symptom recurs on a machine with DevTools closed, the hydration-error angle is the next thing to check. _(added 2026-08-05)_
- **Shell-side `React error #418` (hydration mismatch), `0zzn40uc-_762.js`, thrown at a `$RC`/`$RV` streaming-render boundary — flagged, not investigated.** Found in a console log Royce shared while chasing the nav bug; likely unrelated (a cross-origin Shell hydration failure can't directly manipulate Field's iframe DOM, and the CSS cascade gap above fully explains the symptom on its own) but never independently confirmed as unrelated, and a real Shell-side bug either way. Worth a look on the eq-shell side if it recurs or shows up in Sentry. _(added 2026-08-05)_
- **Environment gotcha hit mid-session, not yet root-caused**: in this worktree, Edit-tool writes to already-tracked files were invisible to Bash/PowerShell/git for 20+ minutes (ruled out simple caching lag), even with sandbox disabled — worked around by reapplying the same edits via a Python script written through Bash so it landed on the real filesystem. Worth investigating if it recurs; logged as memory `worktree-tool-filesystem-desync`. _(added 2026-08-05)_
- **Royce's real 15-file template batch: 12 of 15 are now live**, up from 0 at the previous close — not confirmed whether via the bulk-upload feature or one-by-one, or whether it's actually finished. Corrects the "not run yet" note in the sprint-close section below, which is now stale. _(added 2026-08-05)_
- **`C:\Projects\CLAUDE.md` is still the only home for Rule 0, Rule 0.5 and the load-bearing-facts list.** Rule 0.6 and the effort threshold were moved into governed substrate; the rest wasn't. That file isn't version-controlled, has no CI, and is only read by a session started in that folder. Same shadow-memory class as failure F5. _(added 2026-08-04)_
- **Deleting the shadowed `.git/hooks/pre-commit` is held, not done.** Repointing every worktree's `core.hooksPath` to `.githooks` was tried and reverted for 4 of 5 open worktrees (`agent-af31fd71dc13a91c7`, `silly-noether-ec8a81`, `skills-list-html-908d61`, `eq-context-reflection-protocol-wt`) — their branches predate today's secret-guard delegation, so their own `.githooks/pre-commit` has zero secret-scanning in it. Repointing them would have silently removed their only secret guard, so they're back on `.git/hooks` until their branches merge or rebase past `main` (`1059f85`). Safe to repoint + delete at that point, not before. _(added 2026-08-04)_
_…and 407 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Declined this session, still open if wanted:** widen the Prestart tab past its hardcoded 7-day window, or add a "Show older → Records" link — Royce picked "fix the cap only" via AskUserQuestion; the tab itself is unchanged. _(added 2026-08-04)_
- **Live phone click-through not done** — camera vs. gallery picker, and that "Save changes" actually persists an edit after Submit. _(added 2026-07-31)_
- **Full click-through still not done.** Royce did send real iPhone screenshots (2026-07-31, Home/Roster) — that surfaced two more real bugs, both fixed same day: the loading spinner never animated on iOS (v3.5.387) and, in Shell (`core.eq.solutions`), the "EQ FIELD" home label rendered clipped under Shell's fixed top strip (v3.5.388). Roster Overview's "sites with no one rostered today" panel was also dropped per his direct feedback ("we dont need to show what sites arent being worked at") — v3.5.388. Still unconfirmed on a real phone: the Leave CC list modal (now driven by canonical managers, not free-text email), Job Numbers/Pipeline nav placement. _(added 2026-07-31, updated 2026-07-31)_
- **EQ Wallet — Licences screen critique**: gave direct feedback (add a red/amber dot to the "Expiring soon" filter chip when non-zero so the whole screen doesn't need scanning; no lock-icon legend for a first-time user) but didn't build anything — Royce hasn't said whether he wants it built. _(added 2026-07-31)_
- **Timesheets mobile-entry strategy** — Royce asked "will users actually be doing timesheets on their phone?" No usage data was pulled to answer it responsibly; recommended checking PostHog's `timesheet_saved` event breakdown by device before deciding whether to simplify or cut anything, not done. _(added 2026-07-31)_
- **Build the fix**: `openPinManagement()` does a narrow on-demand `people?select=id,pin&group=in.(Apprentice,Labour Hire)` fetch (same pattern as the staff-timesheet PIN gate in `auth.js`), caches it, `renderPinList()` reads from that cache instead of `p.pin`. Keeps raw PINs out of the general bulk load. Branch fresh off `origin/main`, not the stale `claude/loadfromsupabase-resilient-sync` branch. _(added 2026-07-30)_
- **Separate, lower-priority**: the DB's `has_pin` boolean column is stale/unmaintained (verified live 2026-07-30: 32 of 35 people with a set PIN had `has_pin=false`) — would need an INSERT/UPDATE trigger to sync before it's trustworthy. Not needed for the fix above (on-demand fetch sidesteps it), but worth fixing separately if `has_pin` is ever relied on elsewhere. _(added 2026-07-30)_
- Mirror the roster-grid archive + rating feature (SKS v3.10.104/.105) in EQ Field — flagged as a follow-up task; Royce started it in a separate session, result not yet known. _(added 2026-07-28)_
- **Actual weekly entry hasn't started yet** — the log is ready, first week isn't logged. Per the plan's own proving discipline, needs at least one real supervisor entering their own crew's data (not just one person doing it centrally) to actually test the load the new app has to carry. _(added 2026-07-26)_
- **Needs a real-world check**: have a labour-hire worker (or someone who can log in as one) open the Plant & Equipment list on core.eq.solutions and confirm it loads. Confirmed as far as possible from the data side (production is serving the right code, no other access rule is in the way) but nobody has actually clicked through as that kind of user yet. _(added 2026-07-26)_
_…and 64 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise._

| File | Lines | Open | Done (unrotated) | Aging 45d+ |
|------|------:|-----:|------------------:|------------:|
| [EQ](eq/pending.md) | 3223 | 542 | 87 | 12 |
| [SKS](sks/pending.md) | 404 | 82 | 0 | 16 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 424 | 38 | 2 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-05 | [Tenant-rule audit extended to eq-cards + eq-solves-intake, all 4 PRs merged and live](sessions/2026-08-05.md) |
| 2026-08-05 | [y — My Schedule maps link fixed (iOS home-screen installs)](sessions/2026-08-05-y.md) |
| 2026-08-05 | [x — Sentry confirmed EQ-SHELL-10/19 live, then a /decide pass found F6/F7 were a false alarm and surfaced a genuinely new incident (F12)](sessions/2026-08-05-x.md) |
| 2026-08-05 | [v — Root-caused the pending.md bloat as a 4-day-old broken cron, fixed it, then closed the actual gap as F11](sessions/2026-08-05-v.md) |
| 2026-08-05 | [u — Opened the chunk-error PR and closed out F10 (rung 1 → 4)](sessions/2026-08-05-u.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-05 12:20 UTC._
