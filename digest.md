---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-08-30
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-08-30 02:25 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-08-30 02:20 UTC → 2026-08-30 02:25 UTC)

- Merged: eq-shell [#1673](https://github.com/eq-solutions/eq-shell/pull/1673) feat(documents): edit requires_signoff + reach category mana
- Merged: eq-shell [#1659](https://github.com/eq-solutions/eq-shell/pull/1659) feat(schedule): site_project_id on schedule_entries — write 
- Merged: eq-shell [#1658](https://github.com/eq-solutions/eq-shell/pull/1658) feat(documents): make categories assignable on every documen
- Merged: eq-shell [#1657](https://github.com/eq-solutions/eq-shell/pull/1657) fix(security): revoke stray anon SELECT on 7 field_* views (
- Merged: eq-shell [#1656](https://github.com/eq-solutions/eq-shell/pull/1656) feat(documents): site-scope document pushes and sign-off cer
- Merged: eq-shell [#1653](https://github.com/eq-solutions/eq-shell/pull/1653) feat(nav): unpin Users/Audit log/Security groups/Settings fr
- Merged: eq-shell [#1651](https://github.com/eq-solutions/eq-shell/pull/1651) feat(customers): Field read adapter for site_projects (0288)
- Merged: eq-shell [#1648](https://github.com/eq-solutions/eq-shell/pull/1648) feat(ci): attribute tenant-plane drift violations to eq-fiel

## ⚠ Needs you (9)

- 🔴 **Open security finding** — SEC-1 (P0 — live PII leak) — Public key reads `people`, `timesheets`, `leave_requests`, `audit_log` · [security-register.md](ops/security-register.md)
- 🔴 **Open security finding** — SEC-57 (P1) — An org-wide GitHub App installation (`grok-by-xai`, `repository_selection: all`) · [security-register.md](ops/security-register.md)
- 🔴 **Cron failing** — `index-drift.yml` 3 consecutive scheduled run(s) failed, last success 2026-08-26 · [failures.md](system/failures.md) F11
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-08-23.md](sessions/2026-08-23.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F9: Concurrent-session git races corrupt the shared eq-context checkout · possibly recurred in [2026-08-27.md](sessions/2026-08-27.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F10: core.hooksPath silently resolves to the wrong location — three distinct mechanisms, one sy · possibly recurred in [2026-08-26.md](sessions/2026-08-26.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F12: Side-clone reconciliation blind-overwrote a concurrent session's already-pushed shared-fil · possibly recurred in [2026-08-21.md](sessions/2026-08-21.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-08-27.md](sessions/2026-08-27.md) · [failures.md](system/failures.md)
- 🟠 **PR aging 9d** — eq-solves-service [#791](https://github.com/eq-solutions/eq-service/pull/791) "fix(reports): make reissuing a report possible from the UI"

## 🙋 Waiting on you (260)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **eq-shell** · **SEC-67's env-var half still needs Royce** — 4 confirmed-dead Netlify env vars (`FIELD_SUPABASE_URL`/`_SERVICE_ROLE_KEY`, `NEXT_PUBLIC_SUPABASE_URL`/`_ANON_KEY`), zero code references, ready to delete — blocked by Claude Code's own classifier on unattended env-var writes. Commands in `sessions/2026-08-30.md`. _(added 2026-08-30)_
- **eq-shell** · **SEC-57 — Royce decided "revoke `grok-by-xai`" (2026-08-30), but it can't be done via API.** Confirmed live: `DELETE /orgs/eq-solutions/installations/{id}` doesn't exist (404); `DELETE /app/installations/{id}` needs the app's own JWT auth, not an org member's token (401). Uninstalling a GitHub App from an org is a GitHub-web-UI-only action for a human with org admin rights — Settings → GitHub Apps (or Installed GitHub Apps) → grok-by-xai → Uninstall. Still needs Royce to actually click it. _(added 2026-08-30)_
- **eq-shell** · **Needs Royce's call, security-hardening scope**: SEC-3, SEC-18, SEC-19, SEC-63, SEC-65, SEC-24. Full detail in the sprint doc, not re-listed here. _(added 2026-08-28)_
- **eq-shell** · **Not click-tested live** — same gap as every scope in this arc (site/customer/multi-site all share it): no Shell session/credentials in this environment. Worth one real pass covering all three: push to 2+ sites directly, push to a customer, confirm one signoff + one signature covers the set in both cases, confirm per-site and whole-group certificate exports both render correctly. _(added 2026-08-30)_
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment. Worth a real pass: push the same document to two different sites, confirm two independent Register entries and certificates (each showing only its own site's signers), confirm an existing unscoped push still renders unchanged. _(added 2026-08-28)_
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment. Worth a real pass next time someone's mid-enrollment on a phone: confirm tapping "Open in authenticator app" actually hands off to an installed app on both iOS and Android, confirm the copy button copies the right secret. _(added 2026-08-28)_
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment. Worth a real pass: open the Register tab for a tenant with several signed documents, confirm names now match Staff, open one signer's evidence modal, confirm the signature image still loads (now on demand). _(added 2026-08-28)_
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment. Worth a real pass: push a document to 2+ people via the new checkboxes on both pickers, confirm both get an outstanding sign-off and the combined count is right, confirm a partial failure leaves only the failed name(s) checked. _(added 2026-08-27)_
- **eq-shell** · **Not click-tested live** — no Shell session/credentials in this environment; verified instead via `tsc -b --force`, a full `pnpm run build`, and a direct trace confirming `AdminHub.tsx` already tiles all four removed items. Worth a real pass: sign in as a manager, confirm the Admin section shows only the 5 remaining items and all 4 removed ones are still reachable via All admin tools. _(added 2026-08-28)_
- **eq-shell** · **Not click-tested live by a person** — every verification here was automated (`tsc -b`, `pnpm test`, direct DB queries) or code-level, never an actual live roster-removal on a real multi-tenant worker. Worth a real pass next time one exists: remove a multi-tenant worker from one tenant's roster, confirm their Shell login survives; separately confirm a zaap/EQ-tenant roster removal now actually reaches `org_memberships`/`org_access_requests` end-to-end (only the vault secret's *existence* was confirmed just now, not a live push). _(added 2026-08-27)_
- **eq-shell** · **Not click-tested live** — no login credentials in this environment. Real test is Staff → Aiden Crowley → Add Licence with his actual ID + White Card `.heic` photos, confirming they preview/OCR/save correctly as JPEG. _(added 2026-08-27)_
- **eq-shell** · **Duplicate-code 409 and remove-chip specifically still not confirmed live.** Partially overtaken since 2026-08-27: MOD10 on Telstra SLDC is now a real, actively-used code — Field reads it (chips on Sites/My Schedule), writes against it (roster picker + a typed-code alias resolver), and it's been exercised heavily via direct queries this session — so "does a real code exist and get used for real" is answered. What's specifically NOT confirmed: the add-UI's duplicate-code 409 response and the remove-✕ button, neither exercised this session. _(added 2026-08-27, narrowed 2026-08-30)_
_…and 248 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 1 | 0d |
| eq-solves-service | ✓ success | 4d ago | 6 | 9d |
| eq-field | ✓ success | 0d ago | 1 | 0d |
| eq-cards | ✓ success | 0d ago | 0 | — |
| eq-solves-intake | ✓ success | 11d ago | 0 | — |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: app_data.staff.cards_worker_id pointing at missing jvkn workers: 4](https://eq-solutions.sentry.io/issues/138175643/) | 10 | 2026-08-29 |
| eq-shell | [auth-stall: verify-timeout](https://eq-solutions.sentry.io/issues/134128583/) | 8 | 2026-08-26 |
| eq-shell | [Error: Active org_memberships held by non-members: 15](https://eq-solutions.sentry.io/issues/142429897/) | 7 | 2026-08-29 |
| eq-shell | [Error: Unclaimed worker invites past grace period: 2 still valid, 0 expired](https://eq-solutions.sentry.io/issues/142642035/) | 6 | 2026-08-29 |
| eq-shell | [auth-stall: session-spinner-timeout](https://eq-solutions.sentry.io/issues/134128584/) | 5 | 2026-08-26 |
| eq-field | [TypeError: Failed to fetch](https://eq-solutions.sentry.io/issues/141259049/) | 2 | 2026-08-24 |
| eq-shell | [phone-otp: requested for inactive account](https://eq-solutions.sentry.io/issues/141933696/) | 2 | 2026-08-20 |
| eq-shell | [EQ Field handoff auto-recovery (timeout)](https://eq-solutions.sentry.io/issues/141463602/) | 2 | 2026-08-20 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-08-30 | eq-shell | [#1673](https://github.com/eq-solutions/eq-shell/pull/1673) feat(documents): edit requires_signoff + reach category managemen |
| 2026-08-30 | eq-shell | [#1672](https://github.com/eq-solutions/eq-shell/pull/1672) fix(sites): field_sites.site_lead via contact_site_links (role=si |
| 2026-08-30 | eq-shell | [#1668](https://github.com/eq-solutions/eq-shell/pull/1668) feat(documents): category can override doc_type's signoff routing |
| 2026-08-30 | eq-shell | [#1671](https://github.com/eq-solutions/eq-shell/pull/1671) feat(ci): let other repos apply their own jvkn migrations via thi |
| 2026-08-30 | eq-field | [#832](https://github.com/eq-solutions/eq-field/pull/832) v3.5.604 — SECURITY: apprentice self-assessment — a manager could |
| 2026-08-30 | eq-cards | [#330](https://github.com/eq-solutions/eq-cards/pull/330) feat(ci): apply eq-cards' own jvkn migrations via eq-shell's gove |
| 2026-08-29 | eq-shell | [#1669](https://github.com/eq-solutions/eq-shell/pull/1669) feat(sites): canonical contacts only for site "Ask for" / "Backup |
| 2026-08-29 | eq-shell | [#1670](https://github.com/eq-solutions/eq-shell/pull/1670) feat(documents): ad-hoc multi-site document pushes and sign-off c |
| 2026-08-29 | eq-shell | [#1667](https://github.com/eq-solutions/eq-shell/pull/1667) fix(security): tender-pipeline zaap tables get real authenticated |
| 2026-08-29 | eq-shell | [#1665](https://github.com/eq-solutions/eq-shell/pull/1665) fix(security): add the same-origin check to 15 more cookie-authen |
| 2026-08-29 | eq-shell | [#1662](https://github.com/eq-solutions/eq-shell/pull/1662) fix(security): scope user_invites reads to managers, revoke stray |
| 2026-08-29 | eq-shell | [#1663](https://github.com/eq-solutions/eq-shell/pull/1663) fix(security): drop dead Supabase/Quotes refs from CSP + delete u |
| 2026-08-29 | eq-shell | [#1666](https://github.com/eq-solutions/eq-shell/pull/1666) feat(documents): requires_signoff flag on document_categories (mi |
| 2026-08-29 | eq-shell | [#1664](https://github.com/eq-solutions/eq-shell/pull/1664) fix(documents): lazy-load Register and Reference library tabs |
| 2026-08-29 | eq-shell | [#1654](https://github.com/eq-solutions/eq-shell/pull/1654) fix(data): resolve 4 more divergent staff/shell login names |
_Showing 15 of 95 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-shell** (304 open) · [eq/pending/eq-shell.md](eq/pending/eq-shell.md)
- **eq-cards** (54 open) · [eq/pending/eq-cards.md](eq/pending/eq-cards.md)
- **eq-field** (162 open) · [eq/pending/eq-field.md](eq/pending/eq-field.md)
- **eq-solves-service** (99 open) · [eq/pending/eq-solves-service.md](eq/pending/eq-solves-service.md)
- **eq-solves-intake** (19 open) · [eq/pending/eq-solves-intake.md](eq/pending/eq-solves-intake.md)
- **eq-design-tokens** (1 open) · [eq/pending/eq-design-tokens.md](eq/pending/eq-design-tokens.md)
- **eq-ui** (2 open) · [eq/pending/eq-ui.md](eq/pending/eq-ui.md)
- **eq-receipts** (4 open) · [eq/pending/eq-receipts.md](eq/pending/eq-receipts.md)
- **eq-context** (30 open) · [eq/pending/eq-context.md](eq/pending/eq-context.md)
- **cross-repo** (187 open) · [eq/pending/cross-repo.md](eq/pending/cross-repo.md)
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
| [eq-shell](eq/pending/eq-shell.md) | 2081 | 207 / 101 | 307 | 59 |
| [eq-cards](eq/pending/eq-cards.md) | 509 | 39 / 18 | 115 | 6 |
| [eq-field](eq/pending/eq-field.md) | 1088 | 126 / 46 | 89 | 33 |
| [eq-solves-service](eq/pending/eq-solves-service.md) | 662 | 73 / 26 | 93 | 27 |
| [eq-solves-intake](eq/pending/eq-solves-intake.md) | 152 | 13 / 6 | 5 | 17 |
| [eq-design-tokens](eq/pending/eq-design-tokens.md) | 23 | 1 / 0 | 0 | 1 |
| [eq-ui](eq/pending/eq-ui.md) | 29 | 2 / 0 | 2 | 0 |
| [eq-receipts](eq/pending/eq-receipts.md) | 44 | 3 / 1 | 0 | 0 |
| [eq-context](eq/pending/eq-context.md) | 263 | 25 / 5 | 27 | 5 |
| [cross-repo](eq/pending/cross-repo.md) | 992 | 144 / 43 | 30 | 67 |
| [sks](eq/pending/sks.md) | 53 | 3 / 5 | 0 | 6 |
| [SKS](sks/pending.md) | 469 | 85 / 12 | 0 | 52 |
| [SKS active](sks/active.md) | 119 | 0 / 0 | 0 | 0 |
| [OPS](ops/pending.md) | 516 | 44 / 4 | 0 | 8 |

## Aging open items (45d+, unconfirmed)

_Open items sitting under a section header this old or older — not necessarily wrong, just gone quiet under its own dated write-up. Worth a look before it reads as done-and-forgotten._

- **eq-shell** (2026-07-14) · **Later audit polish** — PDF / branded-report export, and logging who reads the log; then on-request data erasure and anomaly alerts. _(added 2026-07-14; before/after values shipped in #860)_
- **eq-shell** (2026-07-14) · **Crew retry + Sentry watch** — have the crew reopen via a normal browser tab (their home-screen icon may hold stale code from the day's deploys); if anyone still freezes, the fix now self-tags the exact stall in Sentry (`verify-timeout` / `login-timeout` / `session-spinner-timeout` / `chunk-error`). _(added 2026-07-14)_
- **eq-shell** (2026-07-14) · **Material-preset sanity check** — since materials presets now quote at Rate + markup, any entered as already-marked-up sell prices will read higher; worth a glance in the Rate library. _(added 2026-07-14, carried from #820)_
- **eq-shell** (2026-07-14) · **Phone-smoke Comms + Ops mobile on a real device** — both deployed and content-verified, but not exercised through a real authenticated session (auth-gated; not reproducible in the sandbox). _(added 2026-07-14)_
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
_…and 266 more — see each file's Queue health row above._

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
| 2026-08-30 | [SEC-35 merged, deployed, and dispatched live to both tenant planes](sessions/2026-08-30.md) |
| 2026-08-29 | [eq-shell sprint request started, not finished before close](sessions/2026-08-29.md) |
| 2026-08-28 | [Documents to Sign: inline viewer's real bug found and fixed, then mapped audience reach](sessions/2026-08-28.md) |
| 2026-08-27 | [eq-field: Phoenix Khatri "OFF" leave visibility diagnosed; Timesheets Fill Week + Approved column shipped (v3.5.583)](sessions/2026-08-27.md) |
| 2026-08-26 | [Close-out of the 2026-08-25 eq-field/eq-shell session](sessions/2026-08-26.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-08-30 02:25 UTC._
