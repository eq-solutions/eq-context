---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-11
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-11 01:44 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-10 23:55 UTC → 2026-08-11 01:44 UTC)

- Merged: eq-shell [#1285](https://github.com/eq-solutions/eq-shell/pull/1285) fix(ci): field-perms-drift skips cleanly until FIELD_PERMS_D
- Merged: eq-shell [#1281](https://github.com/eq-solutions/eq-shell/pull/1281) feat(access-control): expose eq-field's 74 fine-grained perm
- Merged: eq-solves-service [#698](https://github.com/eq-solutions/eq-service/pull/698) fix(migrations): pin search_path on 6 functions flagged by a
- Merged: eq-solves-service [#696](https://github.com/eq-solutions/eq-service/pull/696) feat(migrations): extend --verify to catch function signatur
- Merged: eq-solves-service [#695](https://github.com/eq-solutions/eq-service/pull/695) docs(ci): fix stale approval-gate comment on apply-service-m
- Merged: eq-solves-service [#694](https://github.com/eq-solutions/eq-service/pull/694) feat(testing): compute RCD circuit pass/fail, auto-create de
- Merged: eq-solves-service [#693](https://github.com/eq-solutions/eq-service/pull/693) fix(maintenance): archived checks still reachable by direct 
- Merged: eq-solves-service [#692](https://github.com/eq-solutions/eq-service/pull/692) fix(testing): assignee picker empty on ACB/NSX Create Check

## ⚠ Needs you (5)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-9 (P0 — confirmed exposure, same window as SEC-3, possible second exposure 2026-07-27) — A different service_role key (`jvkn`/eq-canonical) was pasted directly into a ch · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-24 (P1 — OPEN, found 2026-08-08) — `QUOTES_CRON_SECRET` on eq-shell stored `is_secret: false` — full plaintext retu · [security-register.md](ops/security-register.md)
- 🟠 **Sentry new error** — `eq-cards` [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/139929381/)
- 🟠 **Sentry new error** — `eq-cards` [minified:C4: Exception: Could not load Blob from its URL. Ha](https://eq-solutions.sentry.io/issues/131122766/)

## 🙋 Waiting on you (105)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **EQ** · **Needs Royce, not more building:** merge/deploy waits until he's back (2026-08-22) or explicitly comfortable being reachable if it needs a fast revert — same standing hold as any auth-path change per CLAUDE.md, made explicit here because of the overseas goal specifically. Also still needed regardless of timing: generate + set `EQ_CARDS_HANDOFF_KEY` on both Netlify projects (nothing works until it exists) — manual-hands-only, Claude Code is blocked from writing Netlify secrets by design. _(added 2026-08-10)_
- **EQ** · **Not built.** Royce to decide whether this graduates back onto `system/punch-list.md` for the actual simplification work, given the goal's current exclusion on live UI changes affecting real users while overseas. _(added 2026-08-10)_
- **EQ** · **Work sits uncommitted, not lost** — on branch `fix/integration-ci-app-data-bootstrap` in the shared root checkout at `C:\Projects\eq-solves-service`. Needs Royce to get Docker running (or hand over a `supabase db dump` directly, or greenlight a pure-SQL fallback) to resume. _(added 2026-08-10)_
- **EQ** · **Live click-through not done** — app can't boot in this sandbox (no network to the canonical config service, even for the demo tenant); verified instead via a standalone harness running the actual edited code plus the full existing test suite (26/26) and eslint. Royce to confirm approved leave now shows on the Calendar page on a real tenant. _(added 2026-08-10)_
- **EQ** · **2 items need Royce's call, not a code fix** — `claude/service-canonical-identity-phase3-4` (eq-service): re-keys shell-auth JWT + remaps 5 SKS users' FK refs, explicitly marked "DO NOT DEPLOY without Royce's go" in its own commit, never landed — still wanted or shelved? `worktree-wf_79f7a4de-c56-4` (eq-intake): the quality-guardian engine is live but no admin UI in eq-service ever surfaced its output — still wanted? _(added 2026-08-08)_
- **EQ** · **Not click-tested live** — EQ Field's CSV import was rewired from destructive (purge+reinsert) to additive (match existing person by phone/email before insert) ([eq-field PR #660](https://github.com/eq-solutions/eq-field/pull/660), merged, live). Needs Royce to re-upload a real SKS person's CSV row and confirm their linked records (timesheets, leave, licences — 6 tables carry a soft `person_id` reference) and id survive the round trip. _(added 2026-08-07)_
- **EQ** · **Royce to test on his Samsung/Android Chrome** now that the code and the SMS template are live together for the first time — not yet confirmed working end-to-end. No fix exists for iOS Safari (WebOTP isn't implemented there); manual entry stays as-is on that platform.
- **EQ** · **Not confirmed by Royce on the real embedded session** — everything above was verified against a standalone repro (deploy preview + forced `.shell-mode` class), not the actual `core.eq.solutions/sks/field` iframe Royce was looking at (no way to drive that cross-origin session from this environment). Royce to hard-refresh (or bypass the service worker) and confirm the nav bar is back. _(added 2026-08-05)_
- **EQ** · Auto-login from Shell's tenant tile into Cards was silently skipping the handoff and bouncing to the sign-in screen instead — reported live by Royce, root-caused same session. `cards.eq.solutions` iframes across every open Shell tab share one browser's local storage, and a refresh-token rotation triggered by one tab invalidates the session another tab still has cached. The splash screen only checked whether *a* session object existed in storage, not whether it was still valid, so a stale cached session silently pre-empted the working handoff. Root-caused live against Royce's own SKS account: PostHog showed `shell_handoff_started` never fired on the failing attempt, and eq-canonical's auth logs showed `403 bad_jwt: invalid claim: missing sub claim` at the same second. Fixed in eq-cards [PR #212](https://github.com/eq-solutions/eq-cards/pull/212) (squash-merged `36a23cd`) — `_handleShellEntry()` now validates any cached session with a live `getUser()` call before trusting it, signing out and falling through to the existing handoff on any failure. Merged and deployed (explicit `Build & Deploy` workflow dispatch — Netlify + Sentry source-map upload both succeeded). **Needs Royce's click-through**: his own browser has a bad session already stuck in local storage from before the fix — clearing site data for `cards.eq.solutions` once (or a private window) and reloading the tenant tile is a device-side action only he can do; confirming the clean auto-login after that is the last open step. _(added 2026-08-04)_
- **EQ** · **Sign-off records can be read or overwritten by any signed-in person on the same tenant, not just the person they belong to.** Investigated 2026-08-04 (sprint task T1): the obvious fix (`signer_user_id = auth.uid()`) would break real signing — eq-field's data-plane JWT sets `sub` to the tenant id for every user, not the actor, so `auth.uid()` on the real sign path never equals the signer. Closing this needs an identity-model decision, not a migration. Royce's call: leave deferred, revisit alongside a real second-signer rollout. _(updated 2026-08-04)_
- **EQ** · **Sentry MCP connector needs Royce to reconnect** — "user's connection to this connector was invalidated" mid-session; `search_issues`/`search_events` unavailable for the rest of the session, worked around via code + live DB reads instead. _(added 2026-08-04)_
- **EQ** · **`credentials-canonical-sync` is broken and not actually running** — the edge function that's supposed to copy a worker's licence/credential updates from Cards into the SKS compliance/Field-legacy database is deployed but wired to nothing (no database trigger calls it), and even if it were, it hardcodes the wrong SKS tenant ID (the old, corrected-in-2026-06 wrong value). Net effect: a worker updating a licence or White Card in Cards today does not reach the older SKS compliance view at all. Needs Royce's call on reviving it (fix + wire it up) vs retiring it in favour of the newer eq-field app's live-read pattern, which doesn't have this problem by design. Spawned as background task `task_5687d06b`, already started in a separate session. **Checked eq-field's actual "live-read pattern" this session (Royce: "have Field pick it up") — it's narrower than assumed: `eq_get_org_licences` (via `canon-read.js`) only lists licences a worker already holds and flags expiry, with NO org-required-credential gap-checking anywhere in eq-field (no `org_credential_requirements` lookup exists in the repo at all). So retiring the old sync is safe — Field was never depending on it — but "Field picks this up" isn't a real feature swap yet; Field doesn't currently show missing-credential warnings the way the old SKS view did. Retire-vs-revive is still Royce's call; if he wants Field to show compliance gaps going forward, that's new work, not a revival.** _(added 2026-08-03, updated 2026-08-03)_
_…and 93 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 2 | 0d |
| eq-solves-service | ✓ success | 0d ago | 1 | 0d |
| eq-field | ✓ success | 0d ago | 0 | — |
| eq-cards | ✓ success | 0d ago | 1 | — |
| eq-solves-intake | ✓ success | 2d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-cards | [<unknown>](https://eq-solutions.sentry.io/issues/137265513/) | 5 | 2026-08-09 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/139929381/) | 4 | 2026-08-10 |
| eq-cards | [minified:C4: Exception: Could not load Blob from its URL. Has it been revoked?](https://eq-solutions.sentry.io/issues/131122766/) | 4 | 2026-08-10 |
| eq-cards | [LateInitializationError: Field '' has not been initialized.](https://eq-solutions.sentry.io/issues/136695941/) | 4 | 2026-08-04 |
| eq-cards | [minified:a3W: FunctionException(status: 401, details: {error: unauthorized}, rea](https://eq-solutions.sentry.io/issues/138367603/) | 3 | 2026-08-02 |
| eq-shell | [Error: events GET 500: Error - Request ID: 01KZPVXME1ZW9F7NMD4TDF2CDF](https://eq-solutions.sentry.io/issues/139586029/) | 2 | 2026-08-10 |
| eq-cards | [TimeoutException: TimeoutException after 0:00:14.000000: Future not completed](https://eq-solutions.sentry.io/issues/129414832/) | 2 | 2026-08-07 |
| eq-shell | [TimeoutError: The operation was aborted due to timeout](https://eq-solutions.sentry.io/issues/138753891/) | 2 | 2026-08-04 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-11 | eq-solves-service | [#698](https://github.com/eq-solutions/eq-service/pull/698) fix(migrations): pin search_path on 6 functions flagged by adviso |
| 2026-08-10 | eq-shell | [#1293](https://github.com/eq-solutions/eq-shell/pull/1293) feat(staff): multi-file OCR intake, shared between admin invite a |
| 2026-08-10 | eq-shell | [#1292](https://github.com/eq-solutions/eq-shell/pull/1292) fix(canonical-sync): let a duplicate worker adopt a dangling-link |
| 2026-08-10 | eq-shell | [#1279](https://github.com/eq-solutions/eq-shell/pull/1279) feat(staff): labour-hire candidate review + ops intake tool |
| 2026-08-10 | eq-shell | [#1291](https://github.com/eq-solutions/eq-shell/pull/1291) fix(quotes): surface errors on Word-doc download instead of swall |
| 2026-08-10 | eq-solves-service | [#687](https://github.com/eq-solutions/eq-service/pull/687) chore(deps-dev): bump eslint-config-next from 16.2.2 to 16.3.0 |
| 2026-08-10 | eq-solves-service | [#688](https://github.com/eq-solutions/eq-service/pull/688) chore(deps): bump @sentry/nextjs from 10.68.0 to 10.69.0 |
| 2026-08-10 | eq-solves-service | [#696](https://github.com/eq-solutions/eq-service/pull/696) feat(migrations): extend --verify to catch function signature dri |
| 2026-08-10 | eq-solves-service | [#695](https://github.com/eq-solutions/eq-service/pull/695) docs(ci): fix stale approval-gate comment on apply-service-migrat |
| 2026-08-10 | eq-solves-service | [#684](https://github.com/eq-solutions/eq-service/pull/684) chore(deps): bump the eq-design-system group across 1 directory w |
| 2026-08-10 | eq-solves-service | [#686](https://github.com/eq-solutions/eq-service/pull/686) chore(deps-dev): bump @vitejs/plugin-react from 6.0.4 to 6.0.5 |
| 2026-08-10 | eq-solves-service | [#694](https://github.com/eq-solutions/eq-service/pull/694) feat(testing): compute RCD circuit pass/fail, auto-create defects |
| 2026-08-10 | eq-solves-service | [#693](https://github.com/eq-solutions/eq-service/pull/693) fix(maintenance): archived checks still reachable by direct ID |
| 2026-08-10 | eq-field | [#676](https://github.com/eq-solutions/eq-field/pull/676) chore(lint): tighten file-size ratchet after decomposition (#675) |
| 2026-08-10 | eq-field | [#675](https://github.com/eq-solutions/eq-field/pull/675) v3.5.474-477 — docx-export fix + file-size decomposition (timeshe |
_Showing 15 of 45 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **The actual blocker to Field being prod-ready is still open: why did real usage never start.** SKS NSW Labour is what real workers use today; Field's own parallel-run proving period sits at 0 consecutive clean weeks (per `ops/security-register.md`). Recommended pulling PostHog/`audit_log` data to find the real adoption friction (login flow, missing feature parity, mobile gaps) rather than waiting for it to self-resolve — not started this session, got sidetracked into the file-size work instead. Real next step if "prod ready" is the goal.
- Decided **against** an ES-modules + event-delegation rewrite of the script architecture for now (would kill the `window.foo` exposure boilerplate and `onclick=""`-global pattern this session hit repeatedly) — real value, but delivers nothing user-visible and competes with the adoption question above. Revisit once Field has real daily use and there's slack for invisible cleanup.
- **EQ_SECRET_SALT rotation readiness never actually verified.** Flagged as the top production-readiness risk (single point of failure for suite-wide SSO — session cookie, tenant JWTs, Cards, quotes handoff, internal tokens all fall back to it per `token.ts`), but never checked this session. Real next step once Royce is back on his main setup. _(added 2026-08-11)_
- **Shift-start concurrency unverified.** 65-70 people logging in around the same time against a 60s iframe-token TTL has never been load-tested. No evidence of a problem, no evidence against one either. _(added 2026-08-11)_
- **O&M manual upload is mislabeled, not missing.** `AdminDocumentUpload.tsx`'s doc-type dropdown already has an "O&M manual" option (`value: 'om'`) — but only `doc_type === 'template'` gets the no-signoff/reusable-library treatment (skips audience-push, shows in Templates tab, gets a category). Selecting "O&M manual" today forces it through the normal sign-off/push flow, which makes no sense for a reference manual nobody needs to sign. Fix is a small conditional change (give `'om'` the same treatment as `'template'`), no schema change. Separately: there's no asset/equipment association anywhere in the data model (`documents`/`document_categories` have no `asset_id`) — fine if browse-by-category is enough, genuinely new work if "show me the manual for this switchboard" is wanted.
- **Compliance-doc SKS-website linking is independent of the pilot-gated signing feature — confirmed, safe to build separately.** The pilot gate (`PILOT_SIGN_ALLOWLIST`, eq-field) only restricts Field's "Sign Documents" page; the Shell-side Templates/Register admin surface has no permission gate at all today. A link field would live on the ungated side — add a URL column/reuse `reference` on `app_data.documents`, render as a link in the Register/Templates table (`AdminDocumentUpload.tsx:2006` currently renders `reference` as plain text). The *signing* half of that same original brain-dump line ("finalise how people sign these including environmental and SWMS") is not independent — that's the existing pilot-gated feature, blocked on the same T5 rollout-past-pilot decision already tracked in `eq/documents/internal-signoff-register-sprint-2026-08-04.md`.
- **Deploy order matters, spelled out:** eq-cards' new `shell-verify.js` has no fallback to the old local-signing path — if it deploys before eq-shell's endpoint is live and keyed on both sides, Cards login breaks for real users immediately (Cards is taking live self-signup traffic today). Sequence: (1) generate `EQ_CARDS_HANDOFF_KEY`, set on both projects, (2) merge+deploy eq-shell #1294, confirm the endpoint responds, (3) merge+deploy eq-cards #221. Royce's stated plan: do this from the Beelink, not ad hoc. _(added 2026-08-11)_
- **After the deploy confirms working:** delete `SUPABASE_JWT_SECRET` / `SUPABASE_SERVICE_ROLE_KEY` (jvkn) / `EQ_SESSION_SALT` from eq-cards' Netlify project — otherwise the whole point of this fix (cutting Cards' blast radius) doesn't actually land, they just sit there unused but still exposed to SEC-9's dev-context leak. _(added 2026-08-11)_
- **Threshold values not independently verified against primary standard text** — 300ms trip time at rated current / 100ms at 5× rated current for 30mA RCDs, sourced from AS/NZS 3000 Table J1 via web search, flagged explicitly in the PR. Worth Royce's direct confirmation these are the right numbers before they're the sole gate on a real compliance defect. _(added 2026-08-10)_
- **Not click-tested live** — verified end-to-end via a rolled-back transaction against live ehow (untested/pass/fail/nuisance-trip/unverified-rating cases, create-on-fail, auto-resolve-on-refix) and by inspecting the generated docx's actual XML for the expected shading, but never through the real browser UI. _(added 2026-08-10)_
_…and 459 more · [eq/pending.md](eq/pending.md)_

## Pending (SKS)

- **Declined this session, still open if wanted:** widen the Prestart tab past its hardcoded 7-day window, or add a "Show older → Records" link — Royce picked "fix the cap only" via AskUserQuestion; the tab itself is unchanged. _(added 2026-08-04)_
- **Live phone click-through not done** — camera vs. gallery picker, and that "Save changes" actually persists an edit after Submit. _(added 2026-07-31)_
- **Stale SKS brand color found in the incident-alert email** (`#1F335C` vs. the corrected `#203060`) — spun off as a background task, ran in a separate session; outcome not visible from this session. _(added 2026-07-31)_
- **Full click-through still not done.** Royce did send real iPhone screenshots (2026-07-31, Home/Roster) — that surfaced two more real bugs, both fixed same day: the loading spinner never animated on iOS (v3.5.387) and, in Shell (`core.eq.solutions`), the "EQ FIELD" home label rendered clipped under Shell's fixed top strip (v3.5.388). Roster Overview's "sites with no one rostered today" panel was also dropped per his direct feedback ("we dont need to show what sites arent being worked at") — v3.5.388. Still unconfirmed on a real phone: the Leave CC list modal (now driven by canonical managers, not free-text email), Job Numbers/Pipeline nav placement. _(added 2026-07-31, updated 2026-07-31)_
- **EQ Wallet — Licences screen critique**: gave direct feedback (add a red/amber dot to the "Expiring soon" filter chip when non-zero so the whole screen doesn't need scanning; no lock-icon legend for a first-time user) but didn't build anything — Royce hasn't said whether he wants it built. _(added 2026-07-31)_
- **Timesheets mobile-entry strategy** — Royce asked "will users actually be doing timesheets on their phone?" No usage data was pulled to answer it responsibly; recommended checking PostHog's `timesheet_saved` event breakdown by device before deciding whether to simplify or cut anything, not done. _(added 2026-07-31)_
- **Build the fix**: `openPinManagement()` does a narrow on-demand `people?select=id,pin&group=in.(Apprentice,Labour Hire)` fetch (same pattern as the staff-timesheet PIN gate in `auth.js`), caches it, `renderPinList()` reads from that cache instead of `p.pin`. Keeps raw PINs out of the general bulk load. Branch fresh off `origin/main`, not the stale `claude/loadfromsupabase-resilient-sync` branch. _(added 2026-07-30)_
- **Separate, lower-priority**: the DB's `has_pin` boolean column is stale/unmaintained (verified live 2026-07-30: 32 of 35 people with a set PIN had `has_pin=false`) — would need an INSERT/UPDATE trigger to sync before it's trustworthy. Not needed for the fix above (on-demand fetch sidesteps it), but worth fixing separately if `has_pin` is ever relied on elsewhere. _(added 2026-07-30)_
- Mirror the roster-grid archive + rating feature (SKS v3.10.104/.105) in EQ Field — flagged as a follow-up task; Royce started it in a separate session, result not yet known. _(added 2026-07-28)_
- **Actual weekly entry hasn't started yet** — the log is ready, first week isn't logged. Per the plan's own proving discipline, needs at least one real supervisor entering their own crew's data (not just one person doing it centrally) to actually test the load the new app has to carry. _(added 2026-07-26)_
_…and 66 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise._

| File | Lines | Open | Done (unrotated) | Aging 45d+ |
|------|------:|-----:|------------------:|------------:|
| [EQ](eq/pending.md) | 3256 | 568 | 35 | 12 |
| [SKS](sks/pending.md) | 409 | 83 | 0 | 16 |
| [SKS active](sks/active.md) | 109 | 0 | 0 | 0 |
| [OPS](ops/pending.md) | 402 | 37 | 0 | 1 |

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-11 | [EQ Cards: removed dead CardScreen (710 lines), merged live](sessions/2026-08-11.md) |
| 2026-08-10 | [Delete an approved leave request (SKS), then found + fixed a live Calendar regression in EQ Field](sessions/2026-08-10.md) |
| 2026-08-08 | [eq-field CSV import permission gap: found, fixed, merged, deployed](sessions/2026-08-08.md) |
| 2026-08-07 | [My Schedule maps link: the real root cause was Shell's iframe sandbox, not iOS](sessions/2026-08-07.md) |
| 2026-08-06 | [Document sign-off register: real vision from Royce, two trust gaps fixed](sessions/2026-08-06.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-11 01:44 UTC._
