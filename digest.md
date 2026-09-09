---
title: EQ Suite — Health Digest
owner: Royce Milmlow
last_updated: 2026-09-09
scope: Push-style 'what needs your attention' feed across the EQ suite. Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. Full snapshot in suite-state.md.
read_priority: high
status: live
---

# EQ Suite — Health Digest
_2026-09-09 07:59 UTC · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._

## Since last refresh (2026-09-09 07:54 UTC → 2026-09-09 07:59 UTC)

- Merged: eq-shell [#1825](https://github.com/eq-solutions/eq-shell/pull/1825) feat(documents): add an outstanding-count badge to My docume
- Merged: eq-shell [#1824](https://github.com/eq-solutions/eq-shell/pull/1824) feat(staff): let a conversation carry a reminder date
- Merged: eq-shell [#1823](https://github.com/eq-solutions/eq-shell/pull/1823) fix(responsive): let iPad join the phone breakpoint instead 
- Merged: eq-shell [#1821](https://github.com/eq-solutions/eq-shell/pull/1821) feat(documents): wire up the Matrix view
- Merged: eq-shell [#1820](https://github.com/eq-solutions/eq-shell/pull/1820) test(documents): add regression coverage for pushDocumentAud
- Merged: eq-shell [#1819](https://github.com/eq-solutions/eq-shell/pull/1819) fix(staff): regenerate Formal headline date on edit, stabili
- Merged: eq-shell [#1817](https://github.com/eq-solutions/eq-shell/pull/1817) feat(staff): backdate conversations, Casual notes attach a s
- Merged: eq-shell [#1812](https://github.com/eq-solutions/eq-shell/pull/1812) chore(intake): re-vendor eq-intake to eq-solves-intake@cfeca

## ⚠ Needs you (9)

- 🔴 **Open security finding** — SEC-71 (P1 — deliberate, review 2026-12-04) — Two-factor authentication is switched off for everyone by two hard-coded constan · [security-register.md](ops/security-register.md)
- 🔴 **Guard bypass? rung 4** — F1: Substrate read path served 8-12 day stale content, 200 OK, no error · possibly recurred in [2026-08-23.md](sessions/2026-08-23.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F9: Concurrent-session git races corrupt the shared eq-context checkout · possibly recurred in [2026-09-08.md](sessions/2026-09-08.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F10: core.hooksPath silently resolves to the wrong location — four distinct mechanisms, one sym · possibly recurred in [2026-09-07.md](sessions/2026-09-07.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F12: Side-clone reconciliation blind-overwrote a concurrent session's already-pushed shared-fil · possibly recurred in [2026-08-30.md](sessions/2026-08-30.md) · [failures.md](system/failures.md)
- 🔴 **Guard bypass? rung 4** — F14: A hand-written claim about current state ages into a lie, and nothing anywhere notices · possibly recurred in [2026-09-09.md](sessions/2026-09-09.md) · [failures.md](system/failures.md)
- 🟠 **Sentry new error** — `eq-shell` [Error: column sites.deleted_at does not exist](https://eq-solutions.sentry.io/issues/145817362/)
- 🟠 **Sentry new error** — `eq-shell` [EQ Field handoff auto-recovery (timeout)](https://eq-solutions.sentry.io/issues/141463602/)
- 🟠 **Deploy uploading** — eq-shell (core.eq.solutions)

## 🙋 Waiting on you (293)

_Items only you can clear — a confirm, a click-through, or a call. Not engineering backlog; the Pending sections below exclude these._

- **eq-shell** · **`madagins`'s ledger needs correcting before any real apply can succeed on it** — the 314 falsely-stamped rows have to be cleared/reset first, or every future apply attempt will keep trusting them and skipping real work. Not done here — Royce's call on timing/ownership, and who ran the original bootstrap (and why) is still unknown. _(added 2026-09-09)_
- **eq-shell** · **EQ-SHELL-23 residual** — re-checked live in Sentry as of this restore: issue still `unresolved`/`new`, exactly 1 occurrence (2026-09-08T21:50 UTC), no re-fire since. Silencing it for good needs the jvkn-side shell account/tenant-membership closed too — Royce's call whether that's worth doing; not requested yet. _(added 2026-09-09, restored 2026-09-09)_
- **eq-shell** · **RLS gap on madagins's `app_data._eq_migrations`** (project `ornndtbdkxfsewspbrwk`) — Supabase advisor flagged RLS disabled on this table (anon-exposed). Same table the "tenant creation..." section above independently found holding 314 falsely-stamped ledger rows from the `--bootstrap` misuse — likely two symptoms of the same under-provisioned tenant, but access-control and ledger-integrity are separate fixes; this one needs its own governed-pipeline dispatch (RLS-enabled-with-no-policy + revoke public/anon/authenticated + grant service_role, added to both repos' `SERVICE_ROLE_ONLY` lists) regardless of how the ledger gets corrected. No evidence of a fix as of this restore, but re-verify live before acting — madagins's schema state has changed hands and shape several times today. Royce's call on timing. _(added 2026-09-09, restored 2026-09-09)_
- **eq-shell** · **Local dev server CSP-vs-Vite-preamble conflict** — `netlify dev` blanks the entire SPA on load; the app's CSP `script-src` header (`netlify.toml`) blocks Vite's dev-mode inline preamble script (`@vitejs/plugin-react can't detect preamble`). Confirmed still present as of this restore: current `netlify.toml`'s `script-src` directive carries no `'unsafe-inline'` and no nonce/hash carve-out for dev. Blocks all local click-testing in this repo, not just this feature. Root cause not yet investigated. _(added 2026-09-09, restored 2026-09-09)_
- **eq-shell** · **"Logged after the fact" indicator, Casual attachment friction, "overall score per person"** — 3 items from the follow-up sprint still waiting on Royce's own decisions, none urgent. Full detail in the sprint doc. _(added 2026-09-09)_
- **eq-shell** · **The structural gap itself is still open** — every future Dependabot PR in this repo will hit the identical `SUPABASE_ACCESS_TOKEN` failure and need the same admin-override, until one of: (a) grant the token to Dependabot secrets (security trade-off, declined for now), or (b) change the workflow to skip this check gracefully when triggered by Dependabot AND the diff touches no schema-relevant files. Neither built — Royce's call which way, if either. _(added 2026-09-09)_
- **eq-shell** · **Not click-tested against the real authenticated page** — no Shell session/credentials in this environment; verified instead via the isolated CSS repro above. _(added 2026-09-09)_
- **eq-shell** · **Not click-tested live by a person** — verified via `tsc -b --force`, eslint, and the full test suite (606/606) only; no Shell session/credentials in this environment. _(added 2026-09-09)_
- **eq-shell** · **Not click-tested live by a person** — verified via a clean `pnpm exec tsc -b` plus an isolated before/after reproduction of the actual CSS cascade at 768px and 1400px, not a real authenticated session on a physical iPad. No Shell/demo credentials in this environment. _(added 2026-09-08)_
- **eq-shell** · **No signal anywhere that an entry was backdated** — once `occurred_at` differs from `created_at`, the UI shows the chosen date as if it were contemporaneous, with nothing like "logged 4d later." Named during the critique as a real product gap, not fixed — Royce's call whether it's worth a small label. _(added 2026-09-08)_
- **eq-shell** · **Not click-tested live by a person** — no Shell credentials in this environment (confirmed again at close: hit the real login wall navigating to `/sks/admin/documents/mine` directly). Worth a real pass, in order of importance: (1) as a Viewer-tier account, confirm `my-signoffs`' Network response never contains another person's name or email — the one check that actually matters; (2) as Assigner, the person/site matrix renders real data and bulk push/remind actually create/notify; (3) as Manager (`documents.manage` without `documents.assign` — not a stock role, needs a custom Access Control group grant to even test), confirm `admin/documents` redirects to the library instead of a dead end, and the Upload tab's "pushing needs assign permission" copy shows instead of a silently missing step.
- **eq-shell** · **`PdfBackfillButton` relocated, not re-verified live** — moved from the Reference-library tab (where it landed by accident, per that component's own dated comment) onto the new `admin/documents` List page, matching Royce's original 2026-09-02 placement call. Not click-tested.
_…and 281 more · [eq/pending.md](eq/pending.md) · [sks/pending.md](sks/pending.md) · [ops/pending.md](ops/pending.md)_

## Pulse

| Repo | CI (main) | CI age | Open PRs | Oldest PR |
|------|-----------|--------|----------|-----------|
| eq-shell | ✓ success | 0d ago | 2 | 0d |
| eq-solves-service | ✓ success | 0d ago | 6 | 4d |
| eq-field | ✓ success | 0d ago | 3 | 6d |
| eq-cards | ✓ success | 0d ago | 2 | 0d |
| eq-solves-intake | ✓ success | 1d ago | 0 | — |

## Deploys

| Site | State | Last deploy |
|------|-------|-------------|
| eq-shell | uploading | 2026-09-09 |

## Live errors (Sentry)

| Project | Error | Events | Last seen |
|---------|-------|--------|-----------|
| eq-shell | [Error: column sites.deleted_at does not exist](https://eq-solutions.sentry.io/issues/145817362/) | 7 | 2026-09-09 |
| eq-shell | [EQ Field handoff stalled at "booted" (10s, no 'accepted' yet)](https://eq-solutions.sentry.io/issues/145052767/) | 3 | 2026-09-09 |
| eq-shell | [EQ Field handoff auto-recovery (timeout)](https://eq-solutions.sentry.io/issues/141463602/) | 2 | 2026-09-09 |
| eq-solves-service | [auth handoff: expired](https://eq-solutions.sentry.io/issues/135281279/) | 2 | 2026-09-09 |
| eq-cards | [minified:B2: AuthRetryableFetchException(message: ClientException: Failed to fet](https://eq-solutions.sentry.io/issues/144338444/) | 2 | 2026-09-08 |
| eq-shell | [Error: Workers missing an active org_membership: 1 (1 already hiding licences)](https://eq-solutions.sentry.io/issues/145797834/) | 1 | 2026-09-08 |
_[sentry.io/eq-solutions](https://eq-solutions.sentry.io/issues/?query=is%3Aunresolved)_

## Recently built (last 7 days)

| Merged | Repo | PR |
|--------|------|----|
| 2026-09-09 | eq-shell | [#1835](https://github.com/eq-solutions/eq-shell/pull/1835) fix(security): enable RLS on app_data._eq_migrations (all tenant  |
| 2026-09-09 | eq-shell | [#1834](https://github.com/eq-solutions/eq-shell/pull/1834) fix(provisioning): enable pg_cron on new tenant projects |
| 2026-09-09 | eq-shell | [#1833](https://github.com/eq-solutions/eq-shell/pull/1833) fix(security): enable RLS on 4 dead wipe_backup tables (ehow) |
| 2026-09-09 | eq-shell | [#1832](https://github.com/eq-solutions/eq-shell/pull/1832) chore(provisioning): audit ehow for objects the tracked pipeline  |
| 2026-09-09 | eq-shell | [#1831](https://github.com/eq-solutions/eq-shell/pull/1831) fix(labour-hire): simplify wordy batch-intake tab copy |
| 2026-09-09 | eq-shell | [#1829](https://github.com/eq-solutions/eq-shell/pull/1829) fix(schema): add app_data.sites.deleted_at, missing on every tena |
| 2026-09-09 | eq-shell | [#1830](https://github.com/eq-solutions/eq-shell/pull/1830) test(staff): add coverage for staff-resourcing's pure rollup logi |
| 2026-09-09 | eq-shell | [#1828](https://github.com/eq-solutions/eq-shell/pull/1828) fix(documents): stop clipping the "..." menu behind the next row |
| 2026-09-09 | eq-field | [#959](https://github.com/eq-solutions/eq-field/pull/959) tool: generate-tenant-provision-sql.mjs — replay eq-field's own m |
| 2026-09-09 | eq-field | [#962](https://github.com/eq-solutions/eq-field/pull/962) docs: fix stale eq-context path refs in CLAUDE.md session-end pro |
| 2026-09-09 | eq-field | [#961](https://github.com/eq-solutions/eq-field/pull/961) v3.5.708 — Role-string literals: wire up eq-roles-canon.js instea |
| 2026-09-09 | eq-field | [#960](https://github.com/eq-solutions/eq-field/pull/960) v3.5.707 — Leave: extract balance/business-day math into leave-ru |
| 2026-09-09 | eq-field | [#958](https://github.com/eq-solutions/eq-field/pull/958) v3.5.706 — sbFetch's core fetch had no timeout, hanging initApp() |
| 2026-09-09 | eq-field | [#956](https://github.com/eq-solutions/eq-field/pull/956) DRAFT (not applied): track app_data.staff write-restriction polic |
| 2026-09-09 | eq-field | [#957](https://github.com/eq-solutions/eq-field/pull/957) v3.5.705 — chore: delete 4 confirmed zero-caller functions |
_Showing 15 of 79 · full record in [sessions/](sessions/)_

## Pending (EQ)

- **eq-shell** (310 open) · [eq/pending/eq-shell.md](eq/pending/eq-shell.md)
- **eq-cards** (64 open) · [eq/pending/eq-cards.md](eq/pending/eq-cards.md)
- **eq-field** (253 open) · [eq/pending/eq-field.md](eq/pending/eq-field.md)
- **eq-solves-service** (68 open) · [eq/pending/eq-solves-service.md](eq/pending/eq-solves-service.md)
- **eq-solves-intake** (19 open) · [eq/pending/eq-solves-intake.md](eq/pending/eq-solves-intake.md)
- **eq-design-tokens** (1 open) · [eq/pending/eq-design-tokens.md](eq/pending/eq-design-tokens.md)
- **eq-ui** (2 open) · [eq/pending/eq-ui.md](eq/pending/eq-ui.md)
- **eq-receipts** (4 open) · [eq/pending/eq-receipts.md](eq/pending/eq-receipts.md)
- **eq-context** (41 open) · [eq/pending/eq-context.md](eq/pending/eq-context.md)
- **cross-repo** (184 open) · [eq/pending/cross-repo.md](eq/pending/cross-repo.md)
- **sks** (8 open) · [eq/pending/sks.md](eq/pending/sks.md)

## Pending (SKS)

- **Rhys Scott + Wayne Rowe may need a `team_supervisors` row too, not just `team_members`** — both now flagged `is_supervisor=true` on `app_data.staff`, matching the "player-coach" pattern already live for David Boyd/Amazon Syd 53, John Angangan/Comms+Vans, Matthew Miller & Simon Bramall/Equinix+Vans. Needs Collin to confirm which team each actually runs. _(added 2026-09-09)_
- **The anon-CRUD/secrets-exposure vulnerability from 2026-07-20 (below) is still fully open — explicitly NOT fixed this session, Royce's deliberate call after being told it doesn't go away on its own.** Confirmed live: `app_config`'s exposed `canonical_api_key_field` is a bearer token for `core.eq.solutions/.netlify/functions/canonical-api` (the ACTIVE Shell/Field system, not the retiring app) and `digest_fn_token` is seeded as a raw Supabase service-role JWT for nspbmir itself — both readable by anyone with the still-public, still-served anon key, regardless of the app's retirement status. The zero-risk, no-soak Step 0 patch (`~/.claude/plans/nspbmir-EMERGENCY-anon-select-narrowing.sql`) remains un-run. Royce was walked through the distinction (token exposure into the *active* system ≠ the retiring app's own roster data) and chose to stop spending time on this repo entirely rather than run even the isolated Step 0 fix. His call to make; flagging plainly so nobody assumes this was closed out. _(added 2026-09-07)_
- **Cross-reference: "Track 2 RLS STEP 2" (anon SELECT lockdown on ehow, further down this file) was deferred "until standalone retired."** Ops has moved off sks-nsw-labour as of today, even though the app/DB itself is still technically live (archived repo, active DB, no hard redirect). Worth whoever picks up ehow RLS work checking whether that's enough to count as "retired" for that gate, rather than assuming either way. _(added 2026-09-07)_
- **Affects 45 of 81 active SKS staff** (everyone Cards-linked with no wizard-entered full date of birth) — fixed going forward, but nobody's birthday has actually been re-entered yet. No action needed unless Royce wants a nudge to re-save. Most should self-resolve as people go through Cards' own licence-scan step, which fills a real date of birth in automatically. _(added 2026-08-24)_
- **Aiden's own birthday (18 Feb) was tested then reverted to blank** — unclear if that's his real date or just what was typed while reproducing the bug; needs a real re-save to confirm either way. Separately, his record still carries the *earlier* session's own trial data (job title, emergency contact, start date) that was meant to be trial-then-undo and never was — untouched by this session, still open. _(added 2026-08-24)_
- **A second, unidentified path also creates blank-name logins** — proven by timing, not guessed: Todd Wilson's and David Boyd's shell logins were created 7 weeks *after* their Cards approval, which rules out the path just patched as their cause. Spawned as background task `task_d904d388`, Royce started it in a separate session; running independently, not yet reported back as of this session's close. _(added 2026-08-23)_
- **Not verified live by a person** — the specific pill-click behavior needs a real Core+SKS session to exercise (Teams is SKS-only, gated behind Core auth, not reachable from a standalone deploy-preview session). Confirmed the fix mirrors an already-shipped, working code pattern (the crew-supervisor picker), not watched working fresh. _(added 2026-08-23)_
- **SKS's own number, for reference: 6 of 32 active SKS members are currently missing White Card** — visible today in Shell's Training Matrix; nothing blocks them from working while missing it (soft-flag by design, not an oversight). Worth a look if Royce wants a harder rule for SKS specifically. _(added 2026-08-19)_
- **A reported roster-grid "alignment" issue (one person's row looked off) couldn't be reproduced from the code** — most likely just placeholder text in blank cells reading like real data at a glance, not an actual bug, but left open rather than guessed at. _(added 2026-08-19)_
- **Still not applied to the live database — checked directly, and Royce turned down the shortcut that would have unblocked it today.** Confirmed merging the PR didn't secretly switch it on. Turning it on for real right now would lock the people who haven't signed in yet out of their own timesheet and leave the moment they do, since the fix depends on their login already being linked to their staff record — 37 of 83 active SKS staff, checked again today. A workaround exists (let just those specific people keep today's wider access until they sign in, instead of holding up everyone else) but Royce said no — waiting for them to actually sign in through the real onboarding process instead, however long that takes. _(added 2026-08-16, decision confirmed 2026-08-16)_
_…and 84 more · [sks/pending.md](sks/pending.md)_

## Queue health

_Hygiene signal, not an alert — a large open count is real backlog; a large done count is unrotated history that belongs in a changelog; a large aging count is open work that's gone 45+ days quiet under its dated section and is worth a look before it becomes the next 478-item surprise. Open splits engineering backlog from Royce's own queue (a confirm, a click-through, a call) — the two used to be counted together here, which made the number look worse than the real engineering backlog actually is; the split matches 'Waiting on you' above._

| File | Lines | Open (eng / you) | Done (unrotated) | Aging 45d+ |
|------|------:|------------------:|------------------:|------------:|
| [eq-shell](eq/pending/eq-shell.md) | 1608 | 215 / 100 | 2 | 78 |
| [eq-cards](eq/pending/eq-cards.md) | 349 | 47 / 17 | 0 | 8 |
| [eq-field](eq/pending/eq-field.md) | 1333 | 188 / 69 | 32 | 48 |
| [eq-solves-service](eq/pending/eq-solves-service.md) | 390 | 50 / 19 | 0 | 20 |
| [eq-solves-intake](eq/pending/eq-solves-intake.md) | 164 | 13 / 6 | 2 | 17 |
| [eq-design-tokens](eq/pending/eq-design-tokens.md) | 25 | 1 / 0 | 0 | 1 |
| [eq-ui](eq/pending/eq-ui.md) | 24 | 2 / 0 | 0 | 0 |
| [eq-receipts](eq/pending/eq-receipts.md) | 46 | 3 / 1 | 0 | 3 |
| [eq-context](eq/pending/eq-context.md) | 227 | 30 / 11 | 0 | 9 |
| [cross-repo](eq/pending/cross-repo.md) | 941 | 136 / 48 | 0 | 77 |
| [sks](eq/pending/sks.md) | 55 | 3 / 5 | 0 | 6 |
| [SKS](sks/pending.md) | 506 | 94 / 15 | 0 | 62 |
| [SKS active](sks/active.md) | 119 | 0 / 0 | 0 | 0 |
| [OPS](ops/pending.md) | 627 | 52 / 4 | 0 | 13 |

## Aging open items (45d+, unconfirmed)

_Open items sitting under a section header this old or older — not necessarily wrong, just gone quiet under its own dated write-up. Worth a look before it reads as done-and-forgotten._

- **eq-shell** (2026-07-24) · **What's the actual remaining pain point for direct employees, now that the Cards→Field pipe is confirmed live end-to-end?** Asked Royce directly — is it that head office doesn't trust/re-checks Field data before their manual Upvise upload, or a different gap not yet found. Not answered yet this session. _(added 2026-07-24)_
- **eq-shell** (2026-07-24) · **An automatic check is scheduled for the morning of 2026-07-25 to confirm the fix actually held overnight** — will look at the 5 originally-reported people directly, check for any suspicious mass-reactivation pattern across staff generally, and report back. Not yet confirmed by Royce himself. _(added 2026-07-24)_
- **eq-shell** (2026-07-24) · **`eq_reconcile_worker_sync()` (the nightly dispatcher itself, jvkn `pg_cron` job id 2) still isn't tracked in any repo migration** — a governance gap independent of the bug above, not touched by this fix. Not urgent now that the harmful write is gone, but worth bringing under the normal migration pipeline at some point. _(added 2026-07-24)_
- **eq-shell** (2026-07-24) · **Not yet click-tested against the newest version** — the tick/cross feedback and the job title column are live, but nobody has run a fresh file through *this* version of the screen yet. _(added 2026-07-24)_
- **eq-shell** (2026-07-24) · **A second, older bookkeeping mismatch of the same kind (two database updates sharing one tracking number, from an earlier session) is still sitting there unresolved** — spotted in passing while fixing the pair above, deliberately left untouched since it wasn't part of what Royce asked for this time. Same fix pattern would apply. _(added 2026-07-24)_
- **eq-shell** (2026-07-23) · **Royce hasn't yet re-pulled a fresh export to eyeball the fixed cells himself** — the fix was confirmed via direct RPC call, not a real export download; he asked for this exact check but got redirected before it happened. _(added 2026-07-26)_ **Checked 2026-09-07 via `/triage`: still genuinely needs Royce's own eyes on a real download — that's the whole point, a second automated check wouldn't satisfy it. No live Shell session in this environment to pull one on his behalf either. Where to do it: open the quote in Job Creation and export — server-side generator is `eq-shell/netlify/functions/job-creation.ts`. Still open.**
- **eq-shell** (2026-07-23) · **The tripwire fix eq-solves-service got today (see that entry below) hasn't been built for eq-shell, and eq-shell needs it too.** This session's assigned private folder had nothing in it — ended up doing all its real work in the one shared master copy instead, same mechanism as eq-solves-service's bug. Confirmed live mid-session: a second, unrelated concurrent session's own work-in-progress (a database list-loading improvement) was sitting there uncommitted where this session could see it, and that session's own folder-switch changed what this session was pointed at partway through, without warning. Nothing was lost either time — caught before anything got mixed up — but it's luck, not a safeguard. _(added 2026-07-23)_
- **eq-shell** (2026-07-21) · **Worth a quick look once deployed:** confirm the Company field shows/saves correctly for Labour Hire and Subcontractor (desktop + mobile), and re-export SKS-17386 to confirm Clarifications now sits left-aligned without needing a manual fix in Word. _(added 2026-07-21)_ **Checked 2026-09-07 via `/triage`: same blocker as the rest of this bucket — no live Shell session in this environment for either the UI click-test or the SKS-17386 doc re-export (`quoteDocGenerator.ts` needs an authed session). Still open; needs a real Shell sign-in to close out.**
- **eq-shell** (2026-07-21) · **The third — a simple "how sure are we this credential is real" label on licences — is deliberately parked**, not forgotten: Royce's 90/10 decision (90% on the SKS career, company-scale Cards parked) puts this on the wrong side of the line, since it's a cross-company trust signal SKS's own onboarding doesn't need. Revisit only if the company-scale question reopens. Full detail in the audit doc (`eq-context/eq/cards/portable-trade-identity-audit-2026-07-20.md`). _(added 2026-07-21)_
- **eq-shell** (2026-07-19) · **Still open, not urgent:** the exact reason EQ Field was slow to load for that one person on 2026-07-19 is unconfirmed — likely just a poor connection, but couldn't fully rule out anything worse. Nothing else has reported it since. _(added 2026-07-19)_
- **eq-shell** (2026-07-17) · **Deferred: who should get the weekly summary email?** Built and ready, just needs a recipient list from Royce before it's switched on. _(added 2026-07-17)_
- **eq-shell** (2026-07-17) · **Declined for now (Royce's call): a personal calendar feed per crew member, and a weather warning near Microsoft dock dates.** Offered as options alongside the above; not built. _(added 2026-07-17)_
- **eq-shell** (2026-07-16) · **Deferred: bigger first-load speedup** — breaking one large file into smaller pieces that only load when needed. Real win, but a bigger change that needs a hands-on check, not just automated tests. _(added 2026-07-19)_
- **eq-shell** (2026-07-16) · **Deferred: extend the "you'll lose this" warning** to other forms — site details, invites, admin settings. Currently only on quotes. _(added 2026-07-19)_
- **eq-shell** (2026-07-16) · **Deferred: make long lists load a page at a time** instead of everything at once (quotes, comms roster, staff, customers). _(added 2026-07-19)_
_…and 327 more — see each file's Queue health row above._

## Possible recurring failures (unconfirmed)

_Session logs mention a pattern matching a known failure below, dated after its last recorded occurrence. Not yet counted — if it's real, bump `recurrences` in [failures.md](system/failures.md) and `guard-ratchet.yml` proposes promotion on its own next run._

- **F5** (rung 0) — An ungoverned shadow memory overrode the canonical contract · 1 session since last recorded, most recent [2026-08-16.md](sessions/2026-08-16.md)

## Recent sessions

| Date | Session |
|------|---------|
| 2026-09-09 | [guard.js worktree-naming gap closed (rules 1/1b/1c/10, `-wt-` infix)](sessions/2026-09-09.md) |
| 2026-09-08 | [Customers/Staff/Equipment gained their own URL; 3 PRs merged + live (work done 2026-09-07, closed after midnight)](sessions/2026-09-08.md) |
| 2026-09-07 | [Labour-hire licence-photo fix re-verified live; full roster audited, no other worker exposed](sessions/2026-09-07.md) |
| 2026-09-06 | [Resumed and shipped the `?tenant=demo` fix, caught two more bugs in the same class before merge](sessions/2026-09-06.md) |
| 2026-09-05 | [SEC-53 verified live, closed in the register, and merged](sessions/2026-09-05.md) |
_[sessions/](sessions/) · 5 shown_

## Substrate honesty

✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, no deleted refs used as live) matches reality.

---
_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · on merge + nightly · 2026-09-09 07:59 UTC._
