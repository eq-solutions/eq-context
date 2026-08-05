---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-05
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-05 09:01 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-05 08:59 UTC → 2026-08-05 09:01 UTC)

- Merged: eq-shell [#1243](https://github.com/eq-solutions/eq-shell/pull/1243) refactor(workers): simplify invite header to two actions
- Merged: eq-shell [#1240](https://github.com/eq-solutions/eq-shell/pull/1240) feat(staff): "back on file" indicator for licence photos
- Merged: eq-shell [#1237](https://github.com/eq-solutions/eq-shell/pull/1237) fix(staff): hide Company field for Direct, require supervisi
- Merged: eq-shell [#1235](https://github.com/eq-solutions/eq-shell/pull/1235) fix(licences): timeout the OCR auto-read chain instead of ha
- Merged: eq-shell [#1233](https://github.com/eq-solutions/eq-shell/pull/1233) fix(deps): bump fast-uri to 4.1.2 (CVE-2026-18446)
- Merged: eq-shell [#1232](https://github.com/eq-solutions/eq-shell/pull/1232) fix(invites): recover gracefully from a raced duplicate invi
- Merged: eq-shell [#1231](https://github.com/eq-solutions/eq-shell/pull/1231) chore(intake): auto re-vendor eq-intake/eq-platform
- Merged: eq-shell [#1230](https://github.com/eq-solutions/eq-shell/pull/1230) fix(ops): add FK constraint on app_data.jobs.quote_id
- ✅ Needs you: 4 → 3

## ⚠ Needs you (3)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F7: git merge/stash-pop round-trip NUL-fills files on the C:\Projects virtiofs mount · possibly recurred in [2026-08-05.md](sessions/2026-08-05.md) · [failures.md](system/failures.md)

## 🙋 Waiting on you (117)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Neither fix has been click-tested live** — Royce to confirm: (1) the address fields save and display correctly on a real staff member, desktop and mobile, (2) re-downloading William's compliance pack now shows "William Hong" instead of "Unknown." _(added 2026-08-05)_
- **EQ** · **Not click-tested live** — Royce to confirm a real future-dated new starter actually disappears from the roster/dispatch/timesheets and shows up correctly in the new Starting Soon widget. _(added 2026-08-05)_
- **EQ** · **None of the three above have been click-tested live yet** — all need an authenticated Shell admin session, off-limits for me to drive. Royce to confirm: (1) Materials save-all + archive behaves correctly on the live setup page, (2) dragging a PDF onto the Jobs page actually fires the import in a real browser, (3) the Cost/Sell toggle — especially that a real sell-priced supplier PDF now computes cost correctly, and that the default Cost path is unchanged from before. _(added 2026-08-05)_
- **EQ** · **Royce to test on his Samsung/Android Chrome** now that the code and the SMS template are live together for the first time — not yet confirmed working end-to-end. No fix exists for iOS Safari (WebOTP isn't implemented there); manual entry stays as-is on that platform.
- **EQ** · **Not click-tested live** — no way to drive a real cross-origin Field session from this environment. Royce to confirm: open Field as an SKS admin, click "🏷 Edit category" on a supervisor, change category/role, save, confirm it reflects back on Shell's own Staff page. _(added 2026-08-05)_
- **EQ** · **Not confirmed by Royce on the real embedded session** — everything above was verified against a standalone repro (deploy preview + forced `.shell-mode` class), not the actual `core.eq.solutions/sks/field` iframe Royce was looking at (no way to drive that cross-origin session from this environment). Royce to hard-refresh (or bypass the service worker) and confirm the nav bar is back. _(added 2026-08-05)_
- **EQ** · **Sign-off records can be read or overwritten by any signed-in person on the same tenant, not just the person they belong to.** Investigated 2026-08-04 (sprint task T1): the obvious fix (`signer_user_id = auth.uid()`) would break real signing — eq-field's data-plane JWT sets `sub` to the tenant id for every user, not the actor, so `auth.uid()` on the real sign path never equals the signer. Closing this needs an identity-model decision, not a migration. Royce's call: leave deferred, revisit alongside a real second-signer rollout. _(updated 2026-08-04)_
- **EQ** · **Show mode not yet click-tested on a real device with network disabled.** Verified: analyzer clean, full test suite (255 tests) passes, `flutter build web` succeeds and boots with zero console errors via a static preview — but never signed in as a real worker and tapped it (real login is off-limits for me to do on Royce's behalf). Royce to confirm brightness/wakelock/offline behaviour actually work as intended. _(added 2026-08-03)_
- **EQ** · **Sentry MCP connector needs Royce to reconnect** — "user's connection to this connector was invalidated" mid-session; `search_issues`/`search_events` unavailable for the rest of the session, worked around via code + live DB reads instead. _(added 2026-08-04)_
- **EQ** · **`credentials-canonical-sync` is broken and not actually running** — the edge function that's supposed to copy a worker's licence/credential updates from Cards into the SKS compliance/Field-legacy database is deployed but wired to nothing (no database trigger calls it), and even if it were, it hardcodes the wrong SKS tenant ID (the old, corrected-in-2026-06 wrong value). Net effect: a worker updating a licence or White Card in Cards today does not reach the older SKS compliance view at all. Needs Royce's call on reviving it (fix + wire it up) vs retiring it in favour of the newer eq-field app's live-read pattern, which doesn't have this problem by design. Spawned as background task `task_5687d06b`, already started in a separate session. **Checked eq-field's actual "live-read pattern" this session (Royce: "have Field pick it up") — it's narrower than assumed: `eq_get_org_licences` (via `canon-read.js`) only lists licences a worker already holds and flags expiry, with NO org-required-credential gap-checking anywhere in eq-field (no `org_credential_requirements` lookup exists in the repo at all). So retiring the old sync is safe — Field was never depending on it — but "Field picks this up" isn't a real feature swap yet; Field doesn't currently show missing-credential warnings the way the old SKS view did. Retire-vs-revive is still Royce's call; if he wants Field to show compliance gaps going forward, that's new work, not a revival.** _(added 2026-08-03, updated 2026-08-03)_
- **EQ** · **Royce to retry the actual save in the browser** to confirm end-to-end — DB-level fix is verified, only the real click-through confirms the full path. _(added 2026-08-02)_
- **EQ** · **Staff duplicate handling — still Archive-only, needs your call before any build.** A real staff merge fans out into Field-owned operational tables (timesheets, schedule, licences, dispatch) — per the durable architecture rule, that can't be rebuilt Shell-side; it needs Field-repo coordination, which is a scope decision, not something to default on. _(added 2026-08-02)_
_…and 105 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 0 | — |
| eq-solves-service | ✓ success | 0d ago | 5 | 2d |
| eq-field | ✓ success | 0d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-05 | eq-shell | [#1255](https://github.com/eq-solutions/eq-shell/pull/1255) fix(briefing): validate submit_briefing tool output before trusti |
| 2026-08-05 | eq-shell | [#1254](https://github.com/eq-solutions/eq-shell/pull/1254) fix(ops): wire the cost/sell question into the other Import from  |
| 2026-08-05 | eq-shell | [#1253](https://github.com/eq-solutions/eq-shell/pull/1253) feat(documents): bulk category assignment for the Templates tab |
| 2026-08-05 | eq-shell | [#1251](https://github.com/eq-solutions/eq-shell/pull/1251) feat(staff): add home address fields to Staff edit (desktop + mob |
| 2026-08-05 | eq-shell | [#1250](https://github.com/eq-solutions/eq-shell/pull/1250) fix(staff): compliance-pack export shows Unknown for names only e |
| 2026-08-05 | eq-shell | [#1252](https://github.com/eq-solutions/eq-shell/pull/1252) feat(ops): ask cost vs. sell when importing a subcontractor PDF |
| 2026-08-05 | eq-shell | [#1249](https://github.com/eq-solutions/eq-shell/pull/1249) feat(ops): drag a subcontractor PDF onto the Jobs home page to st |
| 2026-08-05 | eq-shell | [#1248](https://github.com/eq-solutions/eq-shell/pull/1248) fix(ops): widen Description column and batch-save outlet pricing  |
| 2026-08-05 | eq-shell | [#1247](https://github.com/eq-solutions/eq-shell/pull/1247) feat(field): relay a mint-entity-patch-token credential to the Fi |
| 2026-08-05 | eq-field | [#653](https://github.com/eq-solutions/eq-field/pull/653) v3.5.458 — dashboard: fix intermittent blank Birthdays & Annivers |
| 2026-08-05 | eq-field | [#652](https://github.com/eq-solutions/eq-field/pull/652) v3.5.457 — Shell-embedded nav: narrow iframe left with no nav at  |
| 2026-08-05 | eq-field | [#651](https://github.com/eq-solutions/eq-field/pull/651) v3.5.456 — Shell-embedded nav: stop giving touchscreen desktops t |
| 2026-08-05 | eq-field | [#650](https://github.com/eq-solutions/eq-field/pull/650) feat(roster): new starters stay off the roster until start date + |
| 2026-08-05 | eq-cards | [#218](https://github.com/eq-solutions/eq-cards/pull/218) fix(auth): read tenant_id/eq_role from JWT, not session.user.appM |
| 2026-08-04 | eq-shell | [#1245](https://github.com/eq-solutions/eq-shell/pull/1245) feat(field): Bearer credential so Field can trigger a Shell-side  |
_Showing 15 of 144 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **PR + deploy decision is Royce's** — fix is ready to review on `claude/fix-chunk-error-mislabeling`; nothing shipped. _(added 2026-08-05)_
- **Confirmed-vs-inferred split of today's 27 events still needs live Sentry data** — specifically what fraction were the mislabeling bug vs. genuine stale-chunk failures, and whether Netlify's edge-purge has a real propagation lag. A fresh set of Sentry-shaped MCP tools appeared in the deferred-tools list right as this session closed, unverified — worth trying first next session before assuming the connector is still broken. _(added 2026-08-05)_
- **Only the last 10 days of signups were checked for the stuck-appMetadata pattern** — the 4 unblocked accounts are the ones caught in that window; any self-join/auto-provision-only account older than that with a never-updated `raw_app_meta_data` would still show the same symptom if they ever come back and retry. No full historical audit run. _(added 2026-08-05)_
- **William's own Cards `public.workers.first_name/last_name` is still blank** (`""`, unchanged since signup) even though his Shell `app_data.staff` record now has his real name — the compliance-pack fix below makes Shell's copy win for that one export, but anything else that reads Cards' own `workers` table directly for display would still show blank for him specifically. Not backfilled. _(added 2026-08-05)_
- **The *other* "Import from PDF" button (client-RFQ parser, `quote-parse-pdf`, on the create-quote form header) deliberately did NOT get the same Cost/Sell toggle** — it already extracts cost and rate as two separate fields from the document, a different data shape than the subcontractor-quote path's single ambiguous `unit_price`. Flagged, not touched. Worth a look only if Royce hits the same cost/sell confusion there too. _(added 2026-08-05)_
- **Worth a look: `digest.md`'s "Recently built" table shows merge status, not deploy status, for every repo — but eq-cards is the one repo where those two are allowed to diverge for hours by design.** A merged eq-cards PR currently reads identically to a live one on the digest, which is exactly what caused this session's confusion. Might be worth a "manual-deploy pending" flag specific to eq-cards, or a general merged-vs-deployed distinction if other repos ever adopt the same manual-gate pattern.
- **Why the iframe actually went narrow on Royce's real machine is still unconfirmed.** Leading candidate: DevTools was docked open in his screenshots, which alone can shrink the page's available width below 768px. An alternative not ruled out: Shell's own layout being disrupted by the React #418 hydration error below. The v3.5.457 fix doesn't need to know which (it closes the gap for "narrow for any reason"), but if the no-nav symptom recurs on a machine with DevTools closed, the hydration-error angle is the next thing to check. _(added 2026-08-05)_
- **Shell-side `React error #418` (hydration mismatch), `0zzn40uc-_762.js`, thrown at a `$RC`/`$RV` streaming-render boundary — flagged, not investigated.** Found in a console log Royce shared while chasing the nav bug; likely unrelated (a cross-origin Shell hydration failure can't directly manipulate Field's iframe DOM, and the CSS cascade gap above fully explains the symptom on its own) but never independently confirmed as unrelated, and a real Shell-side bug either way. Worth a look on the eq-shell side if it recurs or shows up in Sentry. _(added 2026-08-05)_
- **Environment gotcha hit mid-session, not yet root-caused**: in this worktree, Edit-tool writes to already-tracked files were invisible to Bash/PowerShell/git for 20+ minutes (ruled out simple caching lag), even with sandbox disabled — worked around by reapplying the same edits via a Python script written through Bash so it landed on the real filesystem. Worth investigating if it recurs; logged as memory `worktree-tool-filesystem-desync`. _(added 2026-08-05)_
- **Royce's real 15-file template batch: 12 of 15 are now live**, up from 0 at the previous close — not confirmed whether via the bulk-upload feature or one-by-one, or whether it's actually finished. Corrects the "not run yet" note in the sprint-close section below, which is now stale. _(added 2026-08-05)_
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
| [EQ](eq/pending.md) | 3452 | 555 | 196 | 12 |
| [SKS](sks/pending.md) | 428 | 83 | 6 | 16 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 459 | 37 | 8 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-05 | [Tenant-rule audit extended to eq-cards + eq-solves-intake, all 4 PRs merged and live](sessions/2026-08-05.md) |
| 2026-08-05 | [o — Root-caused eq-shell's "auth-stall: chunk-error" Sentry P0, fix ready on its own branch](sessions/2026-08-05-o.md) |
| 2026-08-05 | [i — Templates get real categories; migration dispatched live](sessions/2026-08-05-i.md) |
| 2026-08-05 | [d — F9 wiring-gap follow-up (task_94836df0): answered, fixed, and the shared checkout reconciled](sessions/2026-08-05-d.md) |
| 2026-08-05 | [c — hooks/adversarial_test.sh: deleted, then restored on Royce's direct call; live F9 Cowork-gap found](sessions/2026-08-05-c.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-05 09:01 UTC._
