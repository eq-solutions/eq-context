---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-28
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-28 05:24 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-28 04:20 UTC → 2026-08-28 05:24 UTC)

- Merged: eq-shell [#1655](https://github.com/eq-solutions/eq-shell/pull/1655) fix(auth): add same-device path for mobile TOTP enrollment
- Merged: eq-shell [#1637](https://github.com/eq-solutions/eq-shell/pull/1637) feat(customers): add/remove project codes on a site
- Merged: eq-shell [#1633](https://github.com/eq-solutions/eq-shell/pull/1633) feat(drift-guard): CHECK 14 — tenant/self/org isolation inva
- Merged: eq-shell [#1632](https://github.com/eq-solutions/eq-shell/pull/1632) docs(drift): confirm eq_cards_admin_sync_tenant_access live-
- Merged: eq-shell [#1630](https://github.com/eq-solutions/eq-shell/pull/1630) feat(customers): let one Site carry multiple project/module 
- Merged: eq-shell [#1629](https://github.com/eq-solutions/eq-shell/pull/1629) chore(drift): allowlist eq_cards_admin_sync_tenant_access — 
- Merged: eq-shell [#1622](https://github.com/eq-solutions/eq-shell/pull/1622) docs(security): correct stale organisations_anon_bootstrap_r
- Merged: eq-shell [#1621](https://github.com/eq-solutions/eq-shell/pull/1621) feat(identity): sync EQ Field roster removal/re-add to Shell

## ⚠ Needs you (9)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-57 (P1) — An org-wide GitHub App installation (`grok-by-xai`, `repository_selection: all`) · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-08-23.md](sessions/2026-08-23.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F9: Concurrent-session git races corrupt the shared eq-context checkout · possibly recurred in [2026-08-27.md](sessions/2026-08-27.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F10: core.hooksPath silently resolves to the wrong location — three distinct mechanisms, one sy · possibly recurred in [2026-08-26.md](sessions/2026-08-26.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F12: Side-clone reconciliation blind-overwrote a concurrent session's already-pushed shared-fil · possibly recurred in [2026-08-21.md](sessions/2026-08-21.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-08-27.md](sessions/2026-08-27.md) · [failures.md](system/failures.md)
- 🟠 **PR aging 7d** — eq-solves-service [#791](https://github.com/eq-solutions/eq-service/pull/791) "fix(reports): make reissuing a report possible from the UI"
- 🟠 **Cron failing** — `index-drift.yml` 1 consecutive scheduled run(s) failed, last success 2026-08-26 · [failures.md](system/failures.md) F11

## 🙋 Waiting on you (251)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment. Worth a real pass: open the Register tab for a tenant with several signed documents, confirm names now match Staff, open one signer's evidence modal, confirm the signature image still loads (now on demand). _(added 2026-08-28)_
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment. Worth a real pass: push a document to 2+ people via the new checkboxes on both pickers, confirm both get an outstanding sign-off and the combined count is right, confirm a partial failure leaves only the failed name(s) checked. _(added 2026-08-27)_
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment; verified instead via `tsc -b --force`, a full `pnpm run build`, and a direct trace confirming `AdminHub.tsx` already tiles all four removed items. Worth a real pass: sign in as a manager, confirm the Admin section shows only the 5 remaining items and all 4 removed ones are still reachable via All admin tools. _(added 2026-08-28)_
- **eq-shell** · **Not click-tested live by a person** — every verification here was automated (`tsc -b`, `pnpm test`, direct DB queries) or code-level, never an actual live roster-removal on a real multi-tenant worker. Worth a real pass next time one exists: remove a multi-tenant worker from one tenant's roster, confirm their Shell login survives; separately confirm a zaap/EQ-tenant roster removal now actually reaches `org_memberships`/`org_access_requests` end-to-end (only the vault secret's *existence* was confirmed just now, not a live push). _(added 2026-08-27)_
- **eq-shell** · **Not click-tested live** — no login credentials in this environment. Real test is Staff → Aiden Crowley → Add Licence with his actual ID + White Card `.heic` photos, confirming they preview/OCR/save correctly as JPEG. _(added 2026-08-27)_
- **eq-shell** · **Not click-tested live** — verified via `tsc -b --force`, live DB queries (jvkn/ehow), and production commit-ancestry, not a real signed-in session creating a fresh Labour Hire/Apprentice/Subcontractor invite end-to-end. Worth a real click-through next time someone invites a non-Employee worker: confirm the Staff record shows the correct employment_type immediately, before the invite is ever claimed. _(added 2026-08-26)_
- **eq-shell** · **Not click-tested live by a person** — verified via `tsc -b`, the access-control preview panel, production deploy-ancestry, and (as of this close) Sharon Maroni's own live `nav_scope` row confirmed correct by direct query (`["customer","site","contact","staff","licence","equipment","field","suppliers"]` — Royce confirmed keep Suppliers) — but nobody has actually signed in as a Simple-mode user and watched the sidebar itself narrow. Worth two minutes next time there's a way to see her session or a test account. _(added 2026-08-26)_
- **eq-shell** · **Not click-tested live by a person** — no live Shell session/credentials in this environment. Worth a pass: on the join-links page, confirm a used deactivated link shows "Can't delete — already used" with no button, confirm the "Show deactivated & expired (N)" toggle expands/collapses correctly and the count matches. _(added 2026-08-26)_
- **eq-shell** · **Not click-tested live by a person** — verified via `tsc -b --force`, eslint, live Supabase tracing of the exact chain, and a production commit-ancestry check, not a real join-flow click-through as a brand-new user. _(added 2026-08-26)_
- **eq-shell** · **Not click-tested live** — no live Shell session/credentials in this environment. Worth a real pass: change a test user's role, confirm a `user.role_changed` row lands in `audit_log`, and (harder to stage) confirm a simulated membership-write failure now returns a real error instead of a false "saved." _(added 2026-08-26)_
- **eq-shell** · **Mobile Commercials-layout fix not click-tested live** — verified via `tsc -b --force` only; no live session/credentials in this environment, and this repo's local dev tooling is broken under Node 24 (existing memory). Worth a real look next time someone's on `/ops` → New Quote on a phone. _(added 2026-08-26)_
- **eq-shell** · **S6 — not code.** Neither of the 2026-08-23 sweep's own live fixes (`staff_conversations` write gate, GM Reports direct-API bypass) has been click-tested by a person yet. Whenever convenient, on you or whoever's got a live session. **Click-test steps written and delivered to Royce in chat 2026-08-26** — Fix A (`staff_conversations`): sign in without `staff.manage_conversations`, confirm no write path via the UI *and* via a direct browser-console insert (RLS, not just a hidden button). Fix B (GM Reports): sign in as manager, confirm periods/jobs/invoice-run/forecast screens still load, confirm archive/delete on a report period still works. Still needs an actual person to run it. _(added 2026-08-25)_
_…and 239 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 2 | 0d |
| eq-solves-service | ✓ success | 2d ago | 6 | 7d |
| eq-field | ✓ success | 0d ago | 1 | 0d |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 9d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: app_data.staff.cards_worker_id pointing at missing jvkn workers: 4](https://eq-solutions.sentry.io/issues/138175643/) | 8 | 2026-08-27 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 8 | 2026-08-26 |
| eq-shell | [Error: Active org_memberships held by non-members: 15](https://eq-solutions.sentry.io/issues/142429897/) | 5 | 2026-08-27 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 5 | 2026-08-26 |
| eq-shell | [Error: Unclaimed worker invites past grace period: 1 still valid, 0 expired](https://eq-solutions.sentry.io/issues/142642035/) | 4 | 2026-08-27 |
| eq-field | [TypeError: Failed to fetch](https://eq-solutions.sentry.io/issues/141259049/) | 2 | 2026-08-24 |
| eq-shell | [phone-otp: requested for inactive account](https://eq-solutions.sentry.io/issues/141933696/) | 2 | 2026-08-20 |
| eq-shell | [EQ Field handoff auto-recovery (timeout)](https://eq-solutions.sentry.io/issues/141463602/) | 2 | 2026-08-20 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-28 | eq-shell | [#1655](https://github.com/eq-solutions/eq-shell/pull/1655) fix(auth): add same-device path for mobile TOTP enrollment |
| 2026-08-28 | eq-field | [#821](https://github.com/eq-solutions/eq-field/pull/821) v3.5.592 — FIX: site contact info silently dead since v3.5.551 |
| 2026-08-28 | eq-field | [#825](https://github.com/eq-solutions/eq-field/pull/825) v3.5.595 — Documents to Sign: report a failed PDF load to Sentry |
| 2026-08-28 | eq-field | [#824](https://github.com/eq-solutions/eq-field/pull/824) v3.5.594 — Documents to Sign: raw-file fallback for a failed PDF  |
| 2026-08-27 | eq-shell | [#1653](https://github.com/eq-solutions/eq-shell/pull/1653) feat(nav): unpin Users/Audit log/Security groups/Settings from th |
| 2026-08-27 | eq-shell | [#1652](https://github.com/eq-solutions/eq-shell/pull/1652) fix(documents): staff-preferred signer names + lazy signature ima |
| 2026-08-27 | eq-shell | [#1645](https://github.com/eq-solutions/eq-shell/pull/1645) feat(documents): multi-select checkboxes for the person push pick |
| 2026-08-27 | eq-shell | [#1648](https://github.com/eq-solutions/eq-shell/pull/1648) feat(ci): attribute tenant-plane drift violations to eq-field, be |
| 2026-08-27 | eq-shell | [#1646](https://github.com/eq-solutions/eq-shell/pull/1646) feat(drift-guard): CHECK 11 — migration identity for jvkn control |
| 2026-08-27 | eq-shell | [#1641](https://github.com/eq-solutions/eq-shell/pull/1641) feat(ci): governed apply path for jvkn control-plane migrations |
| 2026-08-27 | eq-shell | [#1644](https://github.com/eq-solutions/eq-shell/pull/1644) fix(documents): refresh the Register after a successful upload or |
| 2026-08-27 | eq-shell | [#1635](https://github.com/eq-solutions/eq-shell/pull/1635) feat(documents): convert uploads to PDF at commit time (migration |
| 2026-08-27 | eq-shell | [#1642](https://github.com/eq-solutions/eq-shell/pull/1642) fix(drift-guard): CHECK 7 content-verified exception for app_data |
| 2026-08-27 | eq-shell | [#1639](https://github.com/eq-solutions/eq-shell/pull/1639) fix(ci): wire CHECK 6/7/8/9/12/13/14 into the drift-check securit |
| 2026-08-27 | eq-shell | [#1638](https://github.com/eq-solutions/eq-shell/pull/1638) feat(ci): jvkn control-plane checks as a reusable workflow |
_Showing 15 of 90 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-shell** (294 open) · [eq/pending/eq-shell.md](eq/pending/eq-shell.md)
- **eq-cards** (53 open) · [eq/pending/eq-cards.md](eq/pending/eq-cards.md)
- **eq-field** (160 open) · [eq/pending/eq-field.md](eq/pending/eq-field.md)
- **eq-solves-service** (98 open) · [eq/pending/eq-solves-service.md](eq/pending/eq-solves-service.md)
- **eq-solves-intake** (19 open) · [eq/pending/eq-solves-intake.md](eq/pending/eq-solves-intake.md)
- **eq-design-tokens** (1 open) · [eq/pending/eq-design-tokens.md](eq/pending/eq-design-tokens.md)
- **eq-ui** (2 open) · [eq/pending/eq-ui.md](eq/pending/eq-ui.md)
- **eq-receipts** (4 open) · [eq/pending/eq-receipts.md](eq/pending/eq-receipts.md)
- **eq-context** (30 open) · [eq/pending/eq-context.md](eq/pending/eq-context.md)
- **cross-repo** (186 open) · [eq/pending/cross-repo.md](eq/pending/cross-repo.md)
- **sks** (8 open) · [eq/pending/sks.md](eq/pending/sks.md)

## Pending (SKS)

- **Affects 45 of 81 active SKS staff** (everyone Cards-linked with no wizard-entered full date of birth) — fixed going forward, but nobody's birthday has actually been re-entered yet. No action needed unless Royce wants a nudge to re-save. Most should self-resolve as people go through Cards' own licence-scan step, which fills a real date of birth in automatically. _(added 2026-08-24)_
- **Aiden's own birthday (18 Feb) was tested then reverted to blank** — unclear if that's his real date or just what was typed while reproducing the bug; needs a real re-save to confirm either way. Separately, his record still carries the *earlier* session's own trial data (job title, emergency contact, start date) that was meant to be trial-then-undo and never was — untouched by this session, still open. _(added 2026-08-24)_
- **A second, unidentified path also creates blank-name logins** — proven by timing, not guessed: Todd Wilson's and David Boyd's shell logins were created 7 weeks *after* their Cards approval, which rules out the path just patched as their cause. Spawned as background task `task_d904d388`, Royce started it in a separate session; running independently, not yet reported back as of this session's close. _(added 2026-08-23)_
- **Not verified live by a person** — the specific pill-click behavior needs a real Core+SKS session to exercise (Teams is SKS-only, gated behind Core auth, not reachable from a standalone deploy-preview session). Confirmed the fix mirrors an already-shipped, working code pattern (the crew-supervisor picker), not watched working fresh. _(added 2026-08-23)_
- **SKS's own number, for reference: 6 of 32 active SKS members are currently missing White Card** — visible today in Shell's Training Matrix; nothing blocks them from working while missing it (soft-flag by design, not an oversight). Worth a look if Royce wants a harder rule for SKS specifically. _(added 2026-08-19)_
- **A reported roster-grid "alignment" issue (one person's row looked off) couldn't be reproduced from the code** — most likely just placeholder text in blank cells reading like real data at a glance, not an actual bug, but left open rather than guessed at. _(added 2026-08-19)_
- **Still not applied to the live database — checked directly, and Royce turned down the shortcut that would have unblocked it today.** Confirmed merging the PR didn't secretly switch it on. Turning it on for real right now would lock the people who haven't signed in yet out of their own timesheet and leave the moment they do, since the fix depends on their login already being linked to their staff record — 37 of 83 active SKS staff, checked again today. A workaround exists (let just those specific people keep today's wider access until they sign in, instead of holding up everyone else) but Royce said no — waiting for them to actually sign in through the real onboarding process instead, however long that takes. _(added 2026-08-16, decision confirmed 2026-08-16)_
- **The disposable EQ-side tenant doesn't have this fix** — lower priority, since that tenant holds no real data, but the identical gap exists there too and needs some prerequisite pieces built first before it can be ported. _(added 2026-08-16)_
- **Run the first real weekly export/import test** — SKS NSW Labour → Export Schedule CSV → EQ Field (logged in as the SKS org) → Import Schedule CSV. Discussed and confirmed safe; not actually run this session. _(added 2026-08-14)_
- **~7 SKS staff missing from EQ Field's staff table** (hired since the 5 Jul snapshot): Ahmed Masaud, Amir Farid, Callum Treharne, Jhon Jairo Velasquez Meneses, ~~Nabeel Hussain~~, Paul Bolger, Timothy Sue — plus a handful of name-string mismatches (e.g. "Bruno Pedrosa" vs "Bruno Vita Pedrosa", "Jose Quintanilla" vs "Jose Luis Quintanilla Rodriguez"). Royce said he'll manage this himself via EQ Field's People admin. **Correction 2026-08-25: "Nabeel Hussain" was never missing** — he's already in `app_data.staff`, just filed under his legal first name "Mohammed Hussain" (confirmed via matching personal email `nabzhussain95@…` and phone). Likely a name-string-match false positive against whatever hire list this cross-check ran against — same class of gap as the "Bruno Pedrosa" mismatch example earlier in this same bullet. Not investigated further (fixing the matching heuristic wasn't this session's scope); the other 6 names + mismatches remain unverified. _(added 2026-08-14, corrected 2026-08-25)_
_…and 75 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise. Open splits engineering backlog from Royce's own queue (a confirm, a click-through, a call) — the two used to be counted together here, which made the number look worse than the real engineering backlog actually is; the split matches 'Waiting on you' above._

| File | Lines | Open (eng / you) | Done (unrotated) | Aging 45d+ |
|------|------:|------------------:|------------------:|------------:|
| [eq-shell](eq/pending/eq-shell.md) | 2022 | 203 / 95 | 291 | 55 |
| [eq-cards](eq/pending/eq-cards.md) | 491 | 39 / 17 | 109 | 6 |
| [eq-field](eq/pending/eq-field.md) | 1079 | 123 / 44 | 90 | 33 |
| [eq-solves-service](eq/pending/eq-solves-service.md) | 662 | 73 / 26 | 93 | 24 |
| [eq-solves-intake](eq/pending/eq-solves-intake.md) | 152 | 13 / 6 | 5 | 16 |
| [eq-design-tokens](eq/pending/eq-design-tokens.md) | 23 | 1 / 0 | 0 | 1 |
| [eq-ui](eq/pending/eq-ui.md) | 29 | 2 / 0 | 2 | 0 |
| [eq-receipts](eq/pending/eq-receipts.md) | 44 | 3 / 1 | 0 | 0 |
| [eq-context](eq/pending/eq-context.md) | 263 | 25 / 5 | 27 | 5 |
| [cross-repo](eq/pending/cross-repo.md) | 992 | 144 / 43 | 30 | 66 |
| [sks](eq/pending/sks.md) | 53 | 3 / 5 | 0 | 6 |
| [SKS](sks/pending.md) | 469 | 85 / 12 | 0 | 50 |
| [SKS active](sks/active.md) | 119 | 0 / 0 | 0 | 0 |
| [OPS](ops/pending.md) | 516 | 44 / 4 | 0 | 8 |

## Aging open items (45d+, unconfirmed)

_Open items sitting under a section header this old or older — not necessarily wrong, just gone quiet under its own dated write-up. Worth a look before it reads as done-and-forgotten._

- **eq-shell** (2026-07-13) · **8 lower-value lighthouse findings left unfiled (queued)** — TOTP replay window, canonical-api warm-Lambda scope cache, dashboard-counts missing the issues entity, README migration-range drift, check-perm-sync error message, unused vendored `eq-format-ui`, a Unicode-glyph success icon on the public quote page. Pick up in a future recon if worth it. _(added 2026-07-13)_
- **eq-shell** (2026-07-13) · **Leif still needs to accept** — his invite is valid/unused (token regenerated 2026-07-13, expires 07-20). Royce sending him the link + the how-to page (`scratchpad/leif-signin-howto.html`, artifact `de35bebb`). _(added 2026-07-13)_
- **eq-shell** (2026-07-13) · **Root cause: the resend branch of `invite-user.ts` (added `3a4c724`) hardcodes `email_delivered: false` — it calls sendEmail but throws the result away. The first-time-invite branch reports it correctly.** Fix made (capture `resendResult.delivered`) + typechecks clean, but UNCOMMITTED in the worktree — awaiting Royce's ship decision. _(added 2026-07-13)_
- **eq-shell** (2026-07-13) · **M365 deliverability unverified** — Resend accepted the invite email, but `sks.com.au` is Microsoft 365 and may quarantine/junk it. Check messageId `3d0e29d5` status in Resend + Leif's junk. Separate from the reporting bug. _(added 2026-07-13)_
- **eq-shell** (2026-07-13) · **Durable, only if it starts hitting many devices: submit `eq.solutions` for categorization to FortiGuard/Palo Alto/Zscaler (stops default inspection everywhere over time) + publish a "Network Requirements / allowlist" page as a standard enterprise-onboarding step.** eq.solutions is NOT on the HSTS preload list ("unknown") — the `preload` token is inert; optional hygiene to drop it. Not needed for a one-off. _(added 2026-07-13)_
- **eq-shell** (2026-07-12) · **No sourcemaps uploaded for eq-shell** (`@sentry/vite-plugin`/`sentry-cli` absent from the build) — Sentry events are exactly as minified as the console, so it isn't a shortcut here. Optional follow-up if prod JS errors keep needing manual decode: wire up sourcemap upload in its own PR. _(added 2026-07-12)_
- **eq-shell** (2026-07-12) · **Post-merge cleanup:** drop the `eq_set_workbench_job_no` wrapper once no caller remains — the last trace of the word. _(added 2026-07-12)_
- **eq-shell** (2026-07-12) · **Optional (declined for now):** rename GM `job_code` → `job_number` across the 3 GM tables (+ unique constraints, parser, UI) for strict one-name-in-the-schema. _(added 2026-07-12)_
- **eq-shell** (2026-07-11) · **Arm/build the queued fleet bugs** — #736 (invite-users-batch entitlements), #737 (zero-row 404) armed, not yet built. #734 (quote-job-consumer) + #735 (RLS `(select)` wrapping) filed UNARMED — Royce's call to arm. #705 (eq-intake xlsx) DONE this session — see below. _(added 2026-07-11)_
- **eq-shell** (2026-07-11) · **zaap tender tables are now service_role-only** (no `authenticated` tenant policies — the create migration's `field_authed_all_*` never reached zaap). Fine if the EQ app reads them via service_role; add the authenticated tenant policy if Field ever needs authed access there. _(added 2026-07-11)_
- **eq-shell** (2026-07-10) · eq-shell: fix focus-triggered refetch/hydration crash on Field iframe wrapper so spinner doesn't get stuck on tab return _(added 2026-07-10, in progress in separate eq-shell session — task_b2cf81ea)_
- **eq-shell** (2026-07-08) · **EQ Service "session expired, please reconnect" stuck screen — root cause still genuinely unknown.** Two chased theories were investigated and explicitly REFUTED with hard evidence: React error #418 (hydration mismatch) is a dated, known, confirmed-non-blocking noise pattern (2026-07-05 team note, 705 events/14d, essentially every active user) — NOT the cause. A suspected hanging `token-exchange` call was also refuted — real Netlify function logs showed every invocation completing in under 4s with zero errors; the "pending forever" read came from a flaky automated browser tab (same tab independently threw an unrelated CDP "renderer frozen" error). Two chips built on these now-retracted theories (`task_2911c80d`, `task_abbb7fd0`) were already started by Royce before the retraction landed — worth redirecting or discarding. The actual cause of the stuck-reconnect screen is still open. _(added 2026-07-08)_
- **eq-shell** (2026-07-08) · **EQ Service sidebar-header tenant logo clipped** (in `ShellSessionRecovery`'s fallback UI specifically, not the top bar — top bar renders fine live) — chip `task_14031bea` was already started by Royce before this correction landed; built on a stale "top-bar alignment" framing. _(added 2026-07-08)_
- **eq-shell** (2026-07-08) · Core Talent now shows both an `"Electrician"` role (older invoice, 21 Jun) and a `"NSW Licensed Electrician"` role (newer rate card, 1 Jul) — may be the same job under two labels, inflating the weekly-cost table with a stale row. Left for Royce's own sanity-check pass before the Atom agency upload. _(added 2026-07-08)_
- **eq-shell** (2026-07-06) · **No live browser click-through of PR #686's changes** — bulk "All on/off" buttons and the collapsible customer/site grouping have only been typecheck/lint-verified, never clicked in a real browser session. _(added 2026-07-06, needs your call — or hand it to a session with live credentials)_
_…and 255 more — see each file's Queue health row above._

## Possible duplicate pending items (unconfirmed)

_Two open items worded similarly enough that they might be the same thing logged twice. Not auto-merged — check both, close or fold one into the other by hand if they really are the same._

- **eq-context** · **gitleaks pre-commit hook** — prevent PAT exposure in substrate history
  **cross-repo** · **gitleaks pre-commit hook** — prevent PAT exposure in substrate history _(added 2026-06-28)_

- **eq-cards** · **Send Huon** the connection-email reply + before/after graphic. _(needs your call)_
  **cross-repo** · **Send Huon** the connection-email reply + before/after graphic. _(added 2026-07-02)_

## Possible recurring failures (unconfirmed)

_Session logs mention a pattern matching a known failure below, dated after its last recorded occurrence. Not yet counted — if it's real, bump `recurrences` in [failures.md](system/failures.md) and `guard-ratchet.yml` proposes promotion on its own next run._

- **F5** (rung 0) — An ungoverned shadow memory overrode the canonical contract · 1 session since last recorded, most recent [2026-08-16.md](sessions/2026-08-16.md)

## Recent sessions

| Date | Session |
|------|---------|
| 2026-08-28 | [Documents to Sign: inline viewer's real bug found and fixed, then mapped audience reach](sessions/2026-08-28.md) |
| 2026-08-27 | [eq-field: Phoenix Khatri "OFF" leave visibility diagnosed; Timesheets Fill Week + Approved column shipped (v3.5.583)](sessions/2026-08-27.md) |
| 2026-08-26 | [Close-out of the 2026-08-25 eq-field/eq-shell session](sessions/2026-08-26.md) |
| 2026-08-25 | [Canonical wiring map: jvkn/Shell/Field read-write capabilities, verified live end-to-end](sessions/2026-08-25.md) |
| 2026-08-24 | [SEC-58 (control-plane ledger) and SEC-65 (AUDIT_SB_KEY label) closed](sessions/2026-08-24.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-28 05:24 UTC._
