---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-05
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-05 07:32 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-05 07:13 UTC → 2026-08-05 07:32 UTC)

- Merged: eq-shell [#1240](https://github.com/eq-solutions/eq-shell/pull/1240) feat(staff): "back on file" indicator for licence photos
- Merged: eq-shell [#1237](https://github.com/eq-solutions/eq-shell/pull/1237) fix(staff): hide Company field for Direct, require supervisi
- Merged: eq-shell [#1235](https://github.com/eq-solutions/eq-shell/pull/1235) fix(licences): timeout the OCR auto-read chain instead of ha
- Merged: eq-shell [#1233](https://github.com/eq-solutions/eq-shell/pull/1233) fix(deps): bump fast-uri to 4.1.2 (CVE-2026-18446)
- Merged: eq-shell [#1232](https://github.com/eq-solutions/eq-shell/pull/1232) fix(invites): recover gracefully from a raced duplicate invi
- Merged: eq-shell [#1228](https://github.com/eq-solutions/eq-shell/pull/1228) fix(documents): sign-off reminder cadence to a uniform 7 day
- Merged: eq-shell [#1227](https://github.com/eq-solutions/eq-shell/pull/1227) fix(ops): collapsed group header count/total hidden for long
- Merged: eq-shell [#1226](https://github.com/eq-solutions/eq-shell/pull/1226) feat(documents): daily reminder email for outstanding sign-o

## ⚠ Needs you (3)

- 🔴 **Sentry 27 events today** — `eq-shell` [auth-stall: chunk-error](https://eq-solutions.sentry.io/issues/137294044/)
- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)

## 🙋 Waiting on you (113)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **None of the three above have been click-tested live yet** — all need an authenticated Shell admin session, off-limits for me to drive. Royce to confirm: (1) Materials save-all + archive behaves correctly on the live setup page, (2) dragging a PDF onto the Jobs page actually fires the import in a real browser, (3) the Cost/Sell toggle — especially that a real sell-priced supplier PDF now computes cost correctly, and that the default Cost path is unchanged from before. _(added 2026-08-05)_
- **EQ** · **Royce to test on his Samsung/Android Chrome** now that the code and the SMS template are live together for the first time — not yet confirmed working end-to-end. No fix exists for iOS Safari (WebOTP isn't implemented there); manual entry stays as-is on that platform.
- **EQ** · **Not click-tested live** — no way to drive a real cross-origin Field session from this environment. Royce to confirm: open Field as an SKS admin, click "🏷 Edit category" on a supervisor, change category/role, save, confirm it reflects back on Shell's own Staff page. _(added 2026-08-05)_
- **EQ** · **Sign-off records can be read or overwritten by any signed-in person on the same tenant, not just the person they belong to.** Investigated 2026-08-04 (sprint task T1): the obvious fix (`signer_user_id = auth.uid()`) would break real signing — eq-field's data-plane JWT sets `sub` to the tenant id for every user, not the actor, so `auth.uid()` on the real sign path never equals the signer. Closing this needs an identity-model decision, not a migration. Royce's call: leave deferred, revisit alongside a real second-signer rollout. _(updated 2026-08-04)_
- **EQ** · **Show mode not yet click-tested on a real device with network disabled.** Verified: analyzer clean, full test suite (255 tests) passes, `flutter build web` succeeds and boots with zero console errors via a static preview — but never signed in as a real worker and tapped it (real login is off-limits for me to do on Royce's behalf). Royce to confirm brightness/wakelock/offline behaviour actually work as intended. _(added 2026-08-03)_
- **EQ** · **Sentry MCP connector needs Royce to reconnect** — "user's connection to this connector was invalidated" mid-session; `search_issues`/`search_events` unavailable for the rest of the session, worked around via code + live DB reads instead. _(added 2026-08-04)_
- **EQ** · **`credentials-canonical-sync` is broken and not actually running** — the edge function that's supposed to copy a worker's licence/credential updates from Cards into the SKS compliance/Field-legacy database is deployed but wired to nothing (no database trigger calls it), and even if it were, it hardcodes the wrong SKS tenant ID (the old, corrected-in-2026-06 wrong value). Net effect: a worker updating a licence or White Card in Cards today does not reach the older SKS compliance view at all. Needs Royce's call on reviving it (fix + wire it up) vs retiring it in favour of the newer eq-field app's live-read pattern, which doesn't have this problem by design. Spawned as background task `task_5687d06b`, already started in a separate session. **Checked eq-field's actual "live-read pattern" this session (Royce: "have Field pick it up") — it's narrower than assumed: `eq_get_org_licences` (via `canon-read.js`) only lists licences a worker already holds and flags expiry, with NO org-required-credential gap-checking anywhere in eq-field (no `org_credential_requirements` lookup exists in the repo at all). So retiring the old sync is safe — Field was never depending on it — but "Field picks this up" isn't a real feature swap yet; Field doesn't currently show missing-credential warnings the way the old SKS view did. Retire-vs-revive is still Royce's call; if he wants Field to show compliance gaps going forward, that's new work, not a revival.** _(added 2026-08-03, updated 2026-08-03)_
- **EQ** · **Royce to retry the actual save in the browser** to confirm end-to-end — DB-level fix is verified, only the real click-through confirms the full path. _(added 2026-08-02)_
- **EQ** · **Staff duplicate handling — still Archive-only, needs your call before any build.** A real staff merge fans out into Field-owned operational tables (timesheets, schedule, licences, dispatch) — per the durable architecture rule, that can't be rebuilt Shell-side; it needs Field-repo coordination, which is a scope decision, not something to default on. _(added 2026-08-02)_
- **EQ** · **Royce to click through live**: open a site, assign a supervisor from its own contact list, save, reload, confirm it sticks; toggle "Show archived" on the Sites list and confirm it filters/tags correctly. Needs a real sign-in, which is off-limits for Claude to do on your behalf. _(added 2026-08-02)_
- **EQ** · **Royce to check `admin/users/migrate` for SKS against the 44-workers number above** — the invite screen and the 44 are counted two different ways (one by tenant employee record, one by Cards worker record), so they may not match exactly. Worth confirming they're the same gap before assuming the invite screen alone closes it. _(added 2026-08-02)_
- **EQ** · Royce to spot-check a generated PM Asset Report live for a site that has a photo on file — confirm the band + photo layout looks right. _(added 2026-08-02)_
_…and 101 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 0 | — |
| eq-solves-service | ✓ success | 0d ago | 5 | 1d |
| eq-field | ✓ success | 0d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 0d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [auth-stall: chunk-error](https://eq-solutions.sentry.io/issues/137294044/) | 27 | 2026-08-05 |
| eq-shell | [Error: Workers never invited to join, past grace period: 44](https://eq-solutions.sentry.io/issues/135740258/) | 15 | 2026-08-04 |
| eq-solves-service | [UnrecognizedActionError: Server Action "40f8ab2385de590826648056ec7fc02ebdd51eb8](https://eq-solutions.sentry.io/issues/122209933/) | 10 | 2026-08-01 |
| eq-shell | [Cards handoff request from unexpected origin](https://eq-solutions.sentry.io/issues/138655603/) | 9 | 2026-08-05 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 9 | 2026-08-05 |
| eq-shell | [TypeError: l.brief.map is not a function](https://eq-solutions.sentry.io/issues/138902984/) | 8 | 2026-08-05 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 5 | 2026-08-04 |
| eq-shell | [Error: app_data.staff.cards_worker_id pointing at missing jvkn workers: 7](https://eq-solutions.sentry.io/issues/138175643/) | 4 | 2026-08-04 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-05 | eq-shell | [#1253](https://github.com/eq-solutions/eq-shell/pull/1253) feat(documents): bulk category assignment for the Templates tab |
| 2026-08-05 | eq-shell | [#1251](https://github.com/eq-solutions/eq-shell/pull/1251) feat(staff): add home address fields to Staff edit (desktop + mob |
| 2026-08-05 | eq-shell | [#1250](https://github.com/eq-solutions/eq-shell/pull/1250) fix(staff): compliance-pack export shows Unknown for names only e |
| 2026-08-05 | eq-shell | [#1252](https://github.com/eq-solutions/eq-shell/pull/1252) feat(ops): ask cost vs. sell when importing a subcontractor PDF |
| 2026-08-05 | eq-shell | [#1249](https://github.com/eq-solutions/eq-shell/pull/1249) feat(ops): drag a subcontractor PDF onto the Jobs home page to st |
| 2026-08-05 | eq-shell | [#1248](https://github.com/eq-solutions/eq-shell/pull/1248) fix(ops): widen Description column and batch-save outlet pricing  |
| 2026-08-05 | eq-shell | [#1247](https://github.com/eq-solutions/eq-shell/pull/1247) feat(field): relay a mint-entity-patch-token credential to the Fi |
| 2026-08-05 | eq-field | [#651](https://github.com/eq-solutions/eq-field/pull/651) v3.5.456 — Shell-embedded nav: stop giving touchscreen desktops t |
| 2026-08-05 | eq-field | [#650](https://github.com/eq-solutions/eq-field/pull/650) feat(roster): new starters stay off the roster until start date + |
| 2026-08-05 | eq-cards | [#218](https://github.com/eq-solutions/eq-cards/pull/218) fix(auth): read tenant_id/eq_role from JWT, not session.user.appM |
| 2026-08-04 | eq-shell | [#1245](https://github.com/eq-solutions/eq-shell/pull/1245) feat(field): Bearer credential so Field can trigger a Shell-side  |
| 2026-08-04 | eq-shell | [#1246](https://github.com/eq-solutions/eq-shell/pull/1246) feat(documents): categories for the Templates tab |
| 2026-08-04 | eq-shell | [#1231](https://github.com/eq-solutions/eq-shell/pull/1231) chore(intake): auto re-vendor eq-intake/eq-platform |
| 2026-08-04 | eq-shell | [#1244](https://github.com/eq-solutions/eq-shell/pull/1244) fix(security): guard entity-patch against same-site confused-depu |
| 2026-08-04 | eq-shell | [#1243](https://github.com/eq-solutions/eq-shell/pull/1243) refactor(workers): simplify invite header to two actions |
_Showing 15 of 145 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **The *other* "Import from PDF" button (client-RFQ parser, `quote-parse-pdf`, on the create-quote form header) deliberately did NOT get the same Cost/Sell toggle** — it already extracts cost and rate as two separate fields from the document, a different data shape than the subcontractor-quote path's single ambiguous `unit_price`. Flagged, not touched. Worth a look only if Royce hits the same cost/sell confusion there too. _(added 2026-08-05)_
- **Worth a look: `digest.md`'s "Recently built" table shows merge status, not deploy status, for every repo — but eq-cards is the one repo where those two are allowed to diverge for hours by design.** A merged eq-cards PR currently reads identically to a live one on the digest, which is exactly what caused this session's confusion. Might be worth a "manual-deploy pending" flag specific to eq-cards, or a general merged-vs-deployed distinction if other repos ever adopt the same manual-gate pattern.
- **Environment gotcha hit mid-session, not yet root-caused**: in this worktree, Edit-tool writes to already-tracked files were invisible to Bash/PowerShell/git for 20+ minutes (ruled out simple caching lag), even with sandbox disabled — worked around by reapplying the same edits via a Python script written through Bash so it landed on the real filesystem. Worth investigating if it recurs; logged as memory `worktree-tool-filesystem-desync`. _(added 2026-08-05)_
- **Bulk-assigning a category to the 12 templates that predate this feature** (today it's one row at a time) — flagged as background task `task_8de01dba`; Royce started it in a separate session, still running as of this close. _(added 2026-08-05)_
- **Royce's real 15-file template batch: 12 of 15 are now live**, up from 0 at the previous close — not confirmed whether via the bulk-upload feature or one-by-one, or whether it's actually finished. Corrects the "not run yet" note in the sprint-close section below, which is now stale. _(added 2026-08-05)_
- **`C:\Projects\CLAUDE.md` is still the only home for Rule 0, Rule 0.5 and the load-bearing-facts list.** Rule 0.6 and the effort threshold were moved into governed substrate; the rest wasn't. That file isn't version-controlled, has no CI, and is only read by a session started in that folder. Same shadow-memory class as failure F5. _(added 2026-08-04)_
- **Deleting the shadowed `.git/hooks/pre-commit` is held, not done.** Repointing every worktree's `core.hooksPath` to `.githooks` was tried and reverted for 4 of 5 open worktrees (`agent-af31fd71dc13a91c7`, `silly-noether-ec8a81`, `skills-list-html-908d61`, `eq-context-reflection-protocol-wt`) — their branches predate today's secret-guard delegation, so their own `.githooks/pre-commit` has zero secret-scanning in it. Repointing them would have silently removed their only secret guard, so they're back on `.git/hooks` until their branches merge or rebase past `main` (`1059f85`). Safe to repoint + delete at that point, not before. _(added 2026-08-04)_
- **Multiple concurrent Claude sessions were pushing to eq-field's `main` throughout this session** — two real version-number collisions happened and were caught/resolved live, but this is a standing risk with the current strict-monotonic-versioning convention, not a one-off. Worth knowing if it keeps happening. _(added 2026-08-04)_
- **Roll out past the one-person pilot** — push a real document to a real second person, get them to sign on their own phone. Royce reaffirmed this is lower priority than hardening the feature itself first. _(updated 2026-08-04)_
- **eq-field's `sw.js` `CACHE_FIRST_PATHS` only lists `/icons/` (SKS) and `/manifest.json`, not `/icons-eq/` or the new `/manifest-eq.json`** — a pre-existing asymmetry noticed while fixing the item above (SKS assets get faster but staler cache-first serving; EQ assets are always network-first/fresh). Left alone deliberately — fixing it means deciding a caching tradeoff, not just correcting a stale value. _(added 2026-08-04)_
_…and 402 more · [eq/pending.md](eq/pending.md)_

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
| [EQ](eq/pending.md) | 3392 | 544 | 185 | 12 |
| [SKS](sks/pending.md) | 428 | 83 | 6 | 16 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 463 | 38 | 6 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-05 | [Tenant-rule audit extended to eq-cards + eq-solves-intake, all 4 PRs merged and live](sessions/2026-08-05.md) |
| 2026-08-05 | [i — Templates get real categories; migration dispatched live](sessions/2026-08-05-i.md) |
| 2026-08-05 | [d — F9 wiring-gap follow-up (task_94836df0): answered, fixed, and the shared checkout reconciled](sessions/2026-08-05-d.md) |
| 2026-08-05 | [c — hooks/adversarial_test.sh: deleted, then restored on Royce's direct call; live F9 Cowork-gap found](sessions/2026-08-05-c.md) |
| 2026-08-05 | [b — Back-photo follow-through: confirmed live, then made it actually visible](sessions/2026-08-05-b.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-05 07:32 UTC._
