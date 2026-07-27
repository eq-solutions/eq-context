---
title: SKS Tier — Pending Actions Archive
owner: Royce Milmlow
last_updated: 2026-07-27
scope: Done items rotated out of sks/pending.md nightly by scripts/rotate_pending.py to keep the live doc scannable. Nothing here is actionable — pure historical record (also covered in changelogs and sessions/*.md). Append-only, in rotation order.
read_priority: reference
status: archived
---

# SKS Tier — Pending (Archive)

Done items and fully-closed session write-ups rotated out of `sks/pending.md`.
If you're looking for something to action, it's not here — check `sks/pending.md`.
A "(rotated YYYY-MM-DD ...)" note on a section header means only that
section's done items live here; its open items stayed in `sks/pending.md`.

---

## SKS Job Creation spreadsheet — the 3 fields finance/admin always had to fill in by hand can now be pre-set on the customer/job record (2026-07-23) (rotated 2026-07-27)
*Royce sent a real completed Job Creation form (SKS-17359, Equinix) and asked whether the payables invoice email, Market Vertical, and End Client could be nominated somewhere instead of guessed fresh every time.*
- [x] **All 3 are now settable in the app** — Market Vertical and a default payables invoice email live on the customer record (edit any customer in Customers → the dropdown matches the spreadsheet's own 19-industry list exactly); End Client is entered per job when creating/editing a quote in EQ Ops. The downloaded Job Creation spreadsheet now comes out with all 3 already filled in, instead of 2 blank dropdowns and a blank box.
- [x] **Customer search in the Customers screen now also finds sites, contacts, and contract details** — previously only matched the company name.
- [x] **Real click-through done (2026-07-27)** — Royce reported "Job creation stopped working" on a real quote (SKS-17461, Metronode NSW/Equinix). Investigated live in his own session: the export actually succeeded and pulled Market Vertical, Client Type, Market Segment, and the customer-default End Client correctly — not a correctness bug. Royce confirmed after the fact: "it worked after a while — excel took a long time to download." Root cause + fix below.

---

## SKS national scale discovery — "what breaks EQ at ~2,000 employees" (2026-07-23) (rotated 2026-07-27 — open items remain in pending.md)

- [x] **Real scale trajectory confirmed** — 2,000 is a growth target, not current headcount. NSW: ~100 today → 300 in 18 months. VIC: ~700 today → 1,000+ in 12 months (VIC is already bigger than NSW's whole 18-month target). National beyond that grows slower. EQ Field would carry ~80% of the load; Field should reach almost everyone except execs/admin.
- [x] **Sequencing decided by Royce:** fix the known gaps first, prove the software in NSW, then expand — not scale-first-fix-under-load.
- [x] **Org chart read and mapped** — SKS is Region (Eastern/Western) over State, but not cleanly: NSW/QLD/WA/NT each have a proper GM, **VIC does not** — VIC's headcount splits across Major Projects VIC and the VIC Elec/Comms team, both reporting through national functional divisions (Major Projects, Data Centre Solutions + Client Services, AV, HV — HV alone looks like ~90 nationally-mobile trade staff) that cut across every state. **SKS Indigenous Technologies** sits under its own Managing Director, reporting straight to the Group CEO, not into either region — a distinct branded entity, not just a region. Royce's own chain confirmed in the chart: Royce → Mark Brame (GM NSW) → Shane Edmunds (GM Eastern Region) → Matthew Jinks (CEO).
- [x] **Upvise decision: Cards supplements Upvise, does not replace it.** Upvise stays the system of record for employment data; EQ Cards' role is onboarding/qualifications, not the full employment lifecycle. (See `eq/pending.md` for the EQ-side scoping this implies.)

---

## SKS database — three tables had a policy bug that could let a signed-in user see or delete other people's roster/supervisor data (2026-07-22) (rotated 2026-07-27)
*Started as a false alarm: a routine safety check flagged `field_team_supervisors` (added same day by the new "supervisor sees their own crew" feature) as wide open. It wasn't — that flag was itself a false positive, a known blind spot in the checking tool for a safe pattern already used elsewhere. But reading the real table underneath it closely turned up a genuine, separate problem: a leftover, looser rule sitting alongside the correct one, so the correct one didn't actually apply. Found on the brand-new table, then found the same bug on the two older tables the new one had been copied from.*
- [x] **Fixed the false alarm** — added the new table to the checker's existing safe-list (same pattern as several tables already on it), so the automated check stops blocking every other change to the shell app. eq-shell PR [#950](https://github.com/eq-solutions/eq-shell/pull/950), merged.
- [x] **Fixed the real bug on the new crew-supervisor table** — closed the loophole and re-tested live: signed-in SKS users still see everything they should, and a simulated user from a different company now correctly sees nothing (previously would have seen everything). eq-field PR [#533](https://github.com/eq-solutions/eq-field/pull/533), applied live and merged.
- [x] **Found and fixed the identical bug on the two older tables it was copied from** (Teams and Team Members — the everyday "who's on which crew" data), plus a second related issue: the code that creates a new team was trusting a value the app sends it instead of checking it server-side. Systematically checked every table on the SKS database for this same pattern first — confirmed nothing else has it. Live-tested by trying to sneak a bad value through and confirming the system now overrides it. eq-field PR [#536](https://github.com/eq-solutions/eq-field/pull/536), applied live and merged.
- **Not exploited** — SKS is currently the only company on this database, so there was no second company's data to actually leak into; the fix closes the door before that changes. All three fixes verified against the live database before and after, with the actual team/roster counts unchanged throughout.

---

## SKS Field — Safety: Incidents/Near Miss reporting + Prestart copy-from-last (2026-07-22) (rotated 2026-07-27)
*Royce asked for two safety-module improvements: a way to report an incident/near miss, and a faster way to fill in a prestart for a site worked recently.*

**Completed:**
- [x] **Incidents / Near Miss tab shipped** — new 4th tab in Safety (Prestart/Toolbox/Incidents/Records): type (Incident/Near Miss/Hazard Observation), severity, description + voice input, people involved with individual sign-off, photos, draft/submit/delete, Word export, offline queue. New `incidents` table live on Supabase, same RLS/pattern as prestarts/toolbox_talks. Wired into the Records tab (filter + ZIP export) and into the manager-only Safety Report dashboard (stat card, by-person table, site-coverage split). Submitting a High-severity or non-near-miss incident emails every manager with an email on file.
- [x] **Prestart copy-from-last-visit + Duplicate** — picking a site on a new prestart offers to copy scope/hazards/SWMS/HRCW/permits/crew from the most recent *submitted* prestart at that site (within 7 days, any supervisor) — crew signatures reset, everyone still signs fresh. Separate "Duplicate" button on any saved prestart clones it into a new draft for today.
- [x] **Mobile CSS gap fixed** — the Incidents tab was initially missing from the mobile full-screen-modal/anti-zoom/single-column rules that Prestart/Toolbox already had; caught and fixed same session.
- [x] sks-nsw-labour PRs [#69](https://github.com/eq-solutions/sks-nsw-labour/pull/69) — MERGED, v3.10.99 → v3.10.102, deployed via Netlify auto-deploy on push to main.
- [x] **Word doc branding double-checked** — Royce reported the Incident export "isn't branded at all" vs the Prestart doc; generated both from identical data and diffed the file contents byte-for-byte (logo, header, title colour) — identical. **Royce confirmed 2026-07-22: it does look right now** — was a stale service-worker cache, not a real bug. Closed.
- [x] **Found + closed a regression while investigating parity: EQ Field's own "copy from last prestart" feature was accidentally deleted** in a refactor the day before (PR #516 retired the old duplicate prestart form and didn't port the copy-last helpers to the new canonical form). Spun off as a chip session, rebuilt against the new canonical form, Royce approved directly in that session — **eq-field PR [#529](https://github.com/eq-solutions/eq-field/pull/529) MERGED**, live.
- [x] **Royce decided: EQ Field should get its own Incidents/Near-Miss module too** (parity with SKS, not left as the generic Site-Diary field it has today). Spun off as a chip session (`task_bac795b3`), running independently — see `eq/pending.md`.

---

## SKS Field — Leave approval investigation: not a bug, a two-step UX trap (2026-07-22) (rotated 2026-07-27 — open items remain in pending.md)

- [x] **Root-caused, no code fix needed initially.** Checked the live `leave_requests` rows directly: all 3 genuinely still `Pending`, `responded_by`/`responded_at` both null — not a UI/cache issue, the approval never landed server-side. The magic-link flow is deliberately two clicks: the email link opens a confirmation page ("You're about to approve…"), and only a second click on **Confirm — Approve leave** actually applies it (built that way in v3.10.42 specifically so email security scanners like Gmail/Outlook SafeLinks, which auto-follow every link via GET, can't silently auto-approve things). Confirmed the mechanism itself works — May's requests (IDs 44–46) completed cleanly the same way — and ruled out an approver-email/org mismatch (Ian's manager record matches exactly). Most likely explanation: Ian clicked the email link but didn't click the second confirm button.
- [x] **Royce asked to tidy it up — fixed same session.** The email itself was the actual culprit: it said "One-click action" with a plain "✓ Approve" button, directly promising something that wasn't true. Relabelled the email CTA ("Review & Approve" / "Review & Reject", note that it opens a confirmation page) and the confirm page itself (headline "Approve leave" → "Confirm approval", added a loud "⚠ Not yet approved — tap the button below to confirm" banner above the button). Copy/UX only, no change to the token/GET-POST security logic. Verified by rendering the real confirm-page HTML with mocked data before shipping. sks-nsw-labour PR [#70](https://github.com/eq-solutions/sks-nsw-labour/pull/70) MERGED (v3.10.102 → v3.10.103), Netlify auto-deployed.

---

## SKS Ops — Suppliers directory + role-gated credentials (2026-07-21) (rotated 2026-07-27 — open items remain in pending.md)

- [x] **Suppliers directory shipped** — new page under EQ Ops (`core.eq.solutions/sks/ops/suppliers`), searchable, with desktop table + mobile card list (tap-to-call). 47 real suppliers imported from the spreadsheet, explicitly excluding its login/account/password columns (those never touched the database this stage). eq-shell PRs [#927](https://github.com/eq-solutions/eq-shell/pull/927) + [#929](https://github.com/eq-solutions/eq-shell/pull/929), merged, deployed. Migration `0191_suppliers.sql` applied live (SKS only).
- [x] **Column filters added** to the desktop table — category dropdown + text filters on supplier/contact/phone/email/notes. eq-shell PR [#931](https://github.com/eq-solutions/eq-shell/pull/931), merged, deployed.
- [x] **Login/password fields added, gated to managers/supervisors only** — mirrors the same role-gate pattern already used for quote margins and contact PII elsewhere in eq-shell (a database function nulls the fields for anyone else, not just a UI hide). Password renders masked with a click-to-reveal. eq-shell PR [#938](https://github.com/eq-solutions/eq-shell/pull/938), merged, deployed. Migration `0195_supplier_credentials_gate.sql` applied live. **Live-verified end to end** signed in as a manager: saved a test login/password, confirmed it read back correctly, confirmed the reveal toggle works and doesn't open the edit screen by mistake, then removed the test data.

---

## SKS Field — session 2026-07-21 (mobile My Schedule + home tile: show Sat/Sun when rostered) (rotated 2026-07-27 — open items remain in pending.md)

- [x] **sks-nsw-labour v3.10.99 (PR #68, MERGED, live)** — My Schedule day cards (`roster.js`) and the home tile's shift count / next-shift / schedule subtitle (`home.js`) now build their day list from the existing `getVisibleRosterDays()` helper instead of a hardcoded Mon-Fri array, so Sat/Sun show whenever that week actually has weekend work — same rule the desktop roster grid already uses. Display-logic only, no schema change. Same fix ported to EQ Field the same session (v3.5.338, PR #514, merged) — see `eq/pending.md`.

---

## Monday meeting prep — Royce + Adam (SKS), adoption + data-security discussion (2026-07-16) (rotated 2026-07-27 — open items remain in pending.md)

- [x] **Terms/legal review + fixes done, talking points drafted.** Full detail in `eq/pending.md` (EQ-side work: eq-service `/terms` taken down, eq-cards wording softened, eq-field/eq-shell confirmed clean). Positioning locked: personal-tooling framing, no marketing/customer language, Royce recuses from any commercial-terms question. _(done 2026-07-16)_

---

## Done (pruned summary — full history in git log) (rotated 2026-07-27)

- [x] EQ Quotes Supabase port — full Flask rewrite (v50+)
- [x] Fly.io deployment → quotes.eq.solutions
- [x] Cloudflare CNAME (proxy off), custom domain live
- [x] Migrations 001–019 applied to SKS live
- [x] Word doc generator (`app/documents/`) — SKS template + pack/unpack
- [x] Quote register filters — estimator dropdown, customer text, site text
- [x] Inline HTMX status select on quotes list (per-status badge colours)
- [x] Bulk status change
- [x] eq:toast listener — auto-dismissing flash banners
- [x] Customers list — "Job defaults" filter (missing ABN / invoice email / market vertical / end client)
- [x] Customers list — inline contact edit with datalist autocomplete
- [x] Cover page wrap — project name wraps at 24 chars/line
- [x] canonical-vs-alias customer model (v63 Path B)
- [x] Job Creation Template generator (xlsx download)
- [x] Cost-on-line-items, per-line margin chip, budget sheet
- [x] Clickable status journey nodes (v65)
- [x] Static asset cache-busting via content hash (`static_v()` helper)
- [x] Speed pass (v73–v75, 2026-05-23): parallel list queries, TTL-cached lookups, RPC fallback pattern for letter counts / sources / estimator initials
- [x] EQ Field sync (v78, 2026-05-24): migration 022 (`canonical_field_id` + `field_synced_at`), `/integrations/` admin + HTMX sync button, customer list badge, EQ Field `eq-service-sites.js` Netlify Function
- [x] UI collapsible accordions (2026-05-25): clarifications + subcontractors + one-off sections folded by default on quote form; labour and materials always expanded
- [x] OneOffCost Word row (2026-05-25): separate `{{OneOffCost}}` token in template_v3.docx between Subcontractors and Subtotal; row stripped when zero (legacy quotes unaffected); migration 023 (`scope_template_type`)
- [x] Smart-quote corruption fix (2026-05-25): U+201C/U+201D curly quotes in setup/contacts/customers routes.py caused SyntaxError on startup — fixed across all 3 files
- [x] Fly.io redeployment (2026-05-25): confirmed deploy method is `flyctl deploy` (not local Docker); Dockerfile restored after accidental removal; quotes.eq.solutions cert verified issued

---

## ⚠ Time-sensitive — expires 2026-06-15 (rotated 2026-07-27)

- [x] **Worker invites — CLOSED 2026-06-15** — resolved by Royce.
- [x] **8 workers with no email** — CLOSED 2026-06-15.

---

## ⏩ SKS Field — sessions 2026-06-07 through 2026-06-13 (rotated 2026-07-27 — open items remain in pending.md)

- [x] **Roster data entry on ehow — DECISION 2026-06-15** — start fresh on ehow. Do not migrate from nspb. New entries go direct to ehow from now.
- [x] **eq-roles PR #7 — DONE** — merged, v2.3.0 tagged and on main.

---

## ⏩ SKS Field — session 2026-07-03 (QA batch: 9 live bug reports) (rotated 2026-07-27 — open items remain in pending.md)

- [x] At least one SKS person ("Collin ... Toohey") has no record in canonical `app_data.staff`, blocking their leave submissions — data-ops backfill needed, not a code fix _(added 2026-07-03)_ — **RESOLVED, confirmed live 2026-07-06**: `app_data.staff` row exists (`3c9714bd-…`, email `collin.toohey@sks.com.au`, trade `electrical`). Not built this session — found already-fixed during the remediation-queue audit below, likely landed via the 2026-07-02/03 EQ Intake steward-run. Worth confirming his leave submissions actually work end-to-end now that the record exists.

---

## ⏩ SKS Field/Service — session 2026-07-06 (job_plans/defects fixture cleanup + remediation-queue audit) (rotated 2026-07-27 — open items remain in pending.md)

- [x] **job_plans duplicate resolved** — closes the "Duplicate job_plans row, SKS tenant" item from the earlier eq-service contract-scope session today (`sessions/2026-07-06.md`). Turned out to be a batch of 4 hand-seeded fixture rows (`e0000000-…0001-0004`, all same timestamp 2026-04-12, zero FK references anywhere), not just the one E1.25 duplicate. `e0000000-…0002` (E1.30/LVNSX) was a second, worse landmine: a NAME collision (not code) against a real, different job plan (E1.30/PFC) — `previewAssetCountsAction` matches by name, so this would have silently conflated two different asset populations on a future import. All 4 soft-deleted (`is_active=false`).
- [x] **defects fixture batch found + hard-deleted** — 7 more hand-seeded rows (`dd000000-…`/`30000000-…`, two sub-batches, shared fake `raised_by` user id absent from both `auth.users` and `profiles`), zero FK references anywhere (confirmed via `pg_constraint` — no formal FK targets `app_data.defects` at all). `defects`' DELETE trigger is a hard delete (unlike `job_plans`, no soft-delete state exists for this table) — flagged and confirmed with Royce before executing.
- [x] **Swept all 21 other canonical `service.*` tables** for the same fixture-UUID pattern (non-RFC-4122 version nibble, not just prefix-guessing) — zero hits. `job_plans` + `defects` were the only two affected tables.
- [x] **Traced the "who resolved this fixture defect" mystery** — actor `85e30693-…` is Royce's own canonical Shell identity (confirmed against eq-canonical `auth.users` = royce.milmlow@sks.com.au), not a rogue process. Looks orphaned only because Plan B JWT sessions never create a Service-local `auth.users` row — the known, documented Phase-2 identity-convergence gap (migration `0132_current_service_uid.sql`).
- [x] **Audited all 16 `eq_remediation_queue` commits** (EQ Intake's "steward-run-001-2026-07-02" data-quality pass, reviewed by Royce 2026-07-03) against live data:
  - 3 `trade` fixes — clean, untouched since commit.
  - 4 `customer_id` link fixes — clean; the one that later changed (Ben Cheam's Equinix contact, deleted 2026-07-06) was a legitimate, attributed action by Simon Bramall (Equinix account lead) through the app, not a bug.
  - 4 of 8 `email` fixes were silently reverted 2 days later (2026-07-05 07:44:07) as a side effect of that same day's SKS roster-reconciliation session (see below — same 4 people: Ian Marston, Johannes Otto, John McKee, Jonathan Ryan). Traced via `app_data.audit_log`: surgical single-field nulls, `actor_id=null`/`source='system'` (direct-SQL, not through the app). **All 4 emails restored** with Royce's confirmation.
- [x] **Broader activity audit** (all contacts/customers/sites/staff writes, by source) — Royce's own 31-site + 17-contact purge (Erilyan Pty Ltd, DigiCo Infrastructure REIT, 2026-07-03) confirmed legitimate: both customers remain active, nothing duplicated/lost. All 6 "system"-sourced staff hard-deletes (2026-07-05) confirmed safe — every one has a live, current staff record for the same person under a different `staff_id`; stale duplicate stubs, not data loss.

---

## ⏩ SKS Field — session 2026-07-10 (schedule_entries duplicate root-cause + fix) (rotated 2026-07-27 — open items remain in pending.md)

- [x] **Confirmed exhaustively** — exactly 6 duplicate pairs exist (not a sample; `GROUP BY staff_id, date HAVING count(*) > 1` returns exactly these 6). No unique constraint existed on `(staff_id, date)` (confirmed via `pg_constraint` — only the `schedule_id` PK).
- [x] **Root cause**: the `nspb-phase3-2026-07-05` import (1,006 rows, 63 staff, dates 2026-06-22→2026-10-30) always did a plain INSERT with no existing-row check. **The actual import script was never found in any repo** — ruled out eq-shell's `etl-nspbmir-to-ehow.mjs` specifically (different `imported_from` tag; its deterministic-UUID formula doesn't match the live duplicate rows' actual `schedule_id`s). If anyone knows what actually ran this (manual script, SQL editor, one-off local file), worth checking directly — the root cause here is a well-evidenced inference from data shape, not a confirmed code read.
- [x] **Live-display risk found**: `eq-field/scripts/roster-adapter.js`'s `toWideList` currently shows the correct real data for all 6 people, but only because an *unordered* query happens to return the real row first (heap/physical storage order) — not a guaranteed contract. A VACUUM, new index, or query-plan change could silently flip 6 people's roster cells to blank with zero error anywhere. The function's own inline comment ("last writer wins") is backwards from what the code actually does (first-non-empty wins) — small separate bug, not yet fixed, flagged for whoever's next in that file.
- [x] **Fixed live on ehow**: deleted the 6 stub rows after confirming each was a pure subset of its real-row counterpart (every field null or identical — nothing lost). Added `UNIQUE (staff_id, date)` on `app_data.schedule_entries` (migration `schedule_entries_staff_date_uniq`) so this can't silently recur regardless of what wrote it or whether it runs again. Verified: 0 duplicates remain, all 6 real rows intact, 1000 of the original 1006 import rows untouched.
- [x] Source of the `nspb-phase3-2026-07-05` import **identified (Royce, 2026-07-10)**: `nspb` = the standalone **sks-nsw-labour** Supabase project (`nspbmirochztcjijmcrx`, the retiring legacy app). So `nspb-phase3` was a **legacy→canonical roster data migration** pulling roster out of sks-nsw-labour into ehow `app_data.schedule_entries` — not a committed repo script (which is why grepping every repo found nothing), most likely a manual/ad-hoc run. "Phase 3" implies phases 1/2 migrated staff/sites earlier under different tags. **Tension worth noting:** the 2026-06-15 decision was "start fresh on ehow, do NOT migrate from nspb" — yet this migration ran 2026-07-05, three weeks later. Either a deliberate one-off historical backfill that superseded that call, or a run that shouldn't have happened. The `UNIQUE (staff_id, date)` constraint neutralises the duplication risk either way (any future/final nspb backfill now fails loudly, not silently). Optional next step if Royce wants it fully nailed: query nspb directly to confirm the 6 people's TAFE rows exist there as the migration source. _(added 2026-07-10, resolved 2026-07-10)_

---

## Done (this session — 2026-06-01) (rotated 2026-07-27)

- [x] Scott Hotson offer issued and accepted — Operations Lead, Client Services
- [x] Dino Cabal reporting line confirmed — reports to Richo (not Royce)
- [x] Ben Ritchie holiday email sent — pathway conversation booked
- [x] Personal operating system designed and set up:
  - Apple Notes "Brain Dump" note + Siri shortcut (voice capture)
  - iPhone widget for text capture
  - Outlook Tier 1 auto-flag + Read Later rules + Focused Inbox
  - Three Claude sweep prompts saved (standard / quick / end-of-week)
- [x] SKS NSW Delivery board designed — MS Planner, 6 time-buckets, 6 labels, 30 starter tasks seeded (PDF setup guide built)
- [x] NSW interactive org chart built — HTML, 61 people, discipline split (Electrical/Comms), discuss flags, filter strip. Ready for Mark meeting.
- [x] Talent acquisition playbook drafted — relationship-warming, trigger-watching, pace-matching with Dino

---

## Added 2026-07-05 (rotated 2026-07-27 — open items remain in pending.md)

- [x] sks-charters generator — reviewed, built, and committed locally (`59ec109`)

---

## ⏩ SKS Field — session 2026-07-12 (loadFromSupabase resilience — one table's failure can't freeze the app) (rotated 2026-07-27 — open items remain in pending.md)

- [x] **sks-nsw-labour v3.10.93 (PR #60, MERGED, live — `0f68678`)** — split the load into load-critical (people/sites/schedule/managers/timesheets — a failure still aborts the sync and keeps the last-good snapshot) vs optional (teams/team_members/timesheet_locks — wrapped in `.catch(()=>[])` so one table's failure degrades that one feature, not the whole app; same pattern as `apprentices.js` Tier-2). Preserve-on-failure: a failed optional table keeps its last-known value instead of overwriting STATE/the offline snapshot with `[]`. Degraded/failed syncs are now observable — user toast + `sync_degraded` PostHog event (kind partial|failed) + console breadcrumb, transition-guarded so the 30s poll reports once on the healthy→degraded edge, not every tick. Verified end-to-end against the REAL function with forced 400s (optional 400 → app not blanked; critical fail → cached fallback; repeat failure → one toast; failed-optional → data preserved). `index.html` only; `sbFetch`/`sbFetchAll` throw-on-4xx-GET semantics unchanged. Prod serves APP_VERSION 3.10.93.
- [x] **EQ Field reconcile — SHIPPED (eq-field #459, v3.5.304, MERGED + live on field.eq.solutions).** EQ Field already solved the freeze via `_loadSafe` (v3.5.201), so it was never exposed. The observability session (`task_8c1fb92e`) closed the two real gaps: (1) **preserve-on-failure** — found a genuine live bug: `_loadSafe` swallowed a failed core fetch to `[]`, then the poll's `STATE.people = people.map(...)` overwrote good on-screen data with empty, blanking Contacts/roster for ~30s on any transient blip (Field has no last-good snapshot). Now each core STATE write skips a failed table, keeping last-known values. (2) **observability** — `_emitSyncHealth()` raises a toast + `sync_degraded` PostHog event (via `analytics.js _events`, house convention), transition-guarded. Client-only, no DB/auth change, not cross-deployed. _(added 2026-07-12, done 2026-07-12)_

---

## ⏩ SKS Field — session 2026-07-12 (outage prevention hardening + EQ Field audit) (rotated 2026-07-27 — open items remain in pending.md)

- [x] **sks-nsw-labour v3.10.95 (PR #63, MERGED, live — `b8cd308`)** — three prevention layers. (1) **Fail-loud `sbFetchAll`** (`scripts/supabase.js`): throws if a caller passes no `orderBy` and the path has no `order=`, instead of silently defaulting to `order=id` — the exact latent trap behind the outage now fails at the call site, loudly, in dev/CI. 7 existing callers given explicit `'id'`. (2) **Degrade email alert** (`index.html` `_alertSyncDegraded`): on a degraded/failed sync, emails `leaveCCList` (ops distribution) via the `send-email` function — throttled 1/device/day (localStorage), SKS-tenant-only, self-guarded so an alert failure can't cascade. Wired off the existing `_emitSyncHealth` edge (v3.10.93), so it fires once per healthy→degraded transition, not every tick. (3) **Bootstrap smoke test** (`scripts/smoke/bootstrap-smoke.mjs` + `.github/workflows/smoke.yml`) — **the repo's first CI.** Hits every table `loadFromSupabase()` reads, the way the app reads it, asserts 2xx; self-configures the sks url/anon-key from `app-state.js` (both public); includes an invariant guard asserting `team_members`/`timesheet_locks` still 400 on `order=id` (so a revert of the fail-loud change is caught here, not as a silent prod outage). Verified GREEN against the live DB. Runs on push to main alongside Netlify's own deploy.
- [x] **Merge parity checklist created (`docs/merge/sks-eqfield-parity-checklist.md`, #62 + #64)** — the cutover gate for when the SKS tenant moves onto the EQ Field codebase. Seeded with the v3.10.94 timesheet UX (hours-flag / weekend auto-show / Sunday rollover) and the two v3.10.95 resilience layers, each with its EQ Field status + the audit verdict.

---

## ⏩ SKS Field — session 2026-07-12 (login: supervisor no longer drops to view-only after a reload) (rotated 2026-07-27 — open items remain in pending.md)

- [x] **sks-nsw-labour v3.10.96 (PR #65, MERGED + deploying — `6f3eccc`)** — **Option 1 (durable role):** write a durable `eq_role` key at every login path (tenant-code gate, demo, production verify-pin, shell-token SSO, both remember-me restores) and read it in `initApp()` on **every** boot, so supervisor survives a reload. `eq_auto_admin` is kept only to fire the login-moment UX (welcome toast + dashboard jump), never the role. "Switch to view only" + mid-session unlock both update `eq_role` (that choice also survives a reload); logout clears it. Back-compat for sessions open across the upgrade via the legacy flag. **Option 3 (calmer reload):** the SW-activated reload no longer fires instantly — defers to a non-disruptive moment (`_scheduleSwReload`: tab backgrounded, or first safe foreground moment — never mid-edit/type/queued-write; 5-min hard cap). `scripts/auth.js` + `index.html` only; no change to how anyone logs in. Syntax-checked; inline-script parse-error count unchanged vs main.

---

## ⏩ SKS Field — session 2026-07-12 (DB "not working" outage → root fix + timesheet UX) (rotated 2026-07-27)

**Trigger:** Royce reported "the database isn't working" — app stuck on a 4-day-old "Cached" banner. Diagnosed live: DB healthy; every full sync 400'd on two id-less tables and (via the all-or-nothing `Promise.all`) froze the app on its last snapshot. This session shipped the ROOT fix; the resilience layer (v3.10.93 #60) was the follow-up chip.

**Completed:**
- [x] **sks-nsw-labour v3.10.92 (PR #59, MERGED, live — `2e38315`)** — root fix. v3.10.90 paginated `team_members`/`timesheet_locks` via `sbFetchAll()` with no `orderBy`, so both defaulted to `order=id` — neither has an `id` column (PKs `team_id,person_id` / `week_key,org_id`) → 400 on every load. One 400 in the `Promise.all` failed the whole sync → cached-snapshot fallback, silent ~2 days (writes still 200'd so saves looked fine; the 400 was a handled rejection → 0 `error_thrown` in PostHog). Passed each table's PK. Live-verified via API logs (400→200 after deploy). Post-mortem: no review (self-merged), no CI/tests, failure mislabeled "Offline".
- [x] **sks-nsw-labour v3.10.94 (PR #61, MERGED, live — `84abe48`)** — three timesheet UX fixes: (1) **hours-missing red flag** — `placeholder="8"` made an empty cell look filled; a job-with-blank-hours now goes red with a `?` (empty boxes show `hrs`/`h`, not a fake `8`), live-toggled desktop + mobile; nothing auto-writes hours. (2) **weekend auto-show** — any week with Sat/Sun data reveals the weekend columns (`_showWE = tsShowWeekends || hasSat || hasSun`). (3) **Sunday week-rollover fix** — default week used `getDate()-getDay()+1` (JS Sunday=0 → rolled to next week all Sunday); aligned all four week-Monday formulas (index.html ×3 + auth.js) to ISO `-((getDay()+6)%7)`, so the app advances Monday. Rebased onto v3.10.93 first (#60 intact).

**Decided (Royce):**
- Ship the DB fix immediately (live outage); ship all three timesheet fixes as v3.10.94.
- Hours-missing = red flag + kill the "8", NOT auto-fill 8h (auto-fill risks over-billing partial days; invoiced hours stay human-entered).
- Sunday rollover = stay on the current Mon–Sun week through Sunday, advance Monday.

**Deferred:**
- [x] **Prevention — BUILT as v3.10.95 (#63, `b8cd308`, live).** All three layers shipped: (1) **fail-loud `sbFetchAll`** — throws when a caller passes no `orderBy` and the path has no `order=`, instead of silently defaulting to `order=id`; (2) **degrade email alert** — `_alertSyncDegraded` sends a throttled (1/device/day) email to `leaveCCList` via `send-email` on a degraded sync, SKS-tenant-only, self-guarded; (3) **bootstrap smoke test** — `scripts/smoke/bootstrap-smoke.mjs` + `.github/workflows/smoke.yml` (first CI in this repo) hits every bootstrap table on push to main, asserts 2xx, and guards that `team_members`/`timesheet_locks` still 400 on `order=id`. Verified green live. _(added 2026-07-12, done 2026-07-12)_
- [x] **v3.10.94 timesheet UX + the two v3.10.95 resilience layers logged as merge-time parity, not ported now** — checklist created (`docs/merge/sks-eqfield-parity-checklist.md`, #62) seeded with the three timesheet items; the fail-loud `sbFetchAll` + degrade alert added to it (#64). **EQ Field audited (2026-07-12): neither resilience layer is required now** — EQ Field can't freeze (`_loadSafe` wraps every core fetch → `.catch([])`), its only un-`orderBy`'d id-less caller (`project_targets`) is guarded + Enterprise-only + absent from eq-canonical/ehow, and degrades are already observable via #459. Both land at the codebase-merge phase, not as a speculative port. _(added 2026-07-12, done 2026-07-12)_

---

## ⏩ SKS Field — session 2026-07-11 (Safety offline queue unwedge + Resource Allocation capacity panel + Sentry triage) (rotated 2026-07-27 — open items remain in pending.md)

- [x] **Safety "1 pending offline write" stuck forever (v3.5.298, PR #451).** A prestart saved offline ~25 June (pre-v3.5.220 build) still carried the old `sks_rep` field name; the live `prestarts` column is `site_rep`, so every replay 400'd (`PGRST204`) and re-queued — a poison pill with no exit, re-firing on every Safety open. Fix in `safety.js _qReplay`: (1) normalise queued payloads on replay (`sks_rep`→`site_rep`) so the stuck June prestart actually lands in the DB, not discarded; (2) entries that fail with a permanent 400/404 are parked in a `<queueKey>_dead` localStorage key (payload + error kept, Sentry-captured) and removed from the live queue so the pending pill can't wedge. Transient failures (network/401/403/5xx) still retry. Same dead-letter guard added to `site-reports-shared.js replay()`. No DB change (live `prestarts` schema verified correct first). **Renumbered v3.5.296→298 at merge** — a concurrent session's JSZip perf PR #452 took 296, capacity panel took 297.
- [x] **Resource Allocation capacity panel never rendered for labour-curve jobs (v3.5.297, PR #453).** The Capacity Planning panel stayed on the "Set start dates and worker counts…" empty state for phase-planned jobs (e.g. SKS-16310: start date + 3 phases, flat `peak_workers`/`duration_weeks` empty). The demand builder fully supported phases; only the render GATE checked the flat fields. New `_isAllocated()` gate matches the builder (start date + phases OR peak+duration). Also, per the reviewed "Mock B" design: panel now reads **roster-first** (THIS WEEK strip — N on roster · N free · N jobs live · N needed — above the stat tiles); chart **scales to demand not headcount** (with 90 on the books vs 4–12-crew jobs the old max(HC,demand) scale flattened every job; HC dashed line only draws when demand is within reach, else a legend chip); peak-demand tile names its week; WORKERS/WEEKS/timeline/colour derive from the curve when flat fields empty. **"Save phases" now rebuilds the unpushed labour plan** so "N to assign" tracks the current curve (SKS-16310 showed a stale "66 to assign" from its confirm-time curve while the edited curve implied 114); rows already pushed to the live roster are never touched. SKS-only surface, no DB change.
- [x] **Sentry eq-field queue cleared to zero** — all 5 unresolved issues triaged + resolved, none needed new code: EQ-FIELD-R (`isLeave is not defined`, calendar — fixed by lazy-loader commit d18638f, event predated it); EQ-FIELD-M (null `staff_id` leave POST — fixed by v3.5.221 pre-check, event on v3.5.218); EQ-FIELD-T/S (`LEAVE_DIAG*` — leave-shows-0 diagnostics removed v3.5.292; T's payload actually confirms the fix, 31 rows ok); EQ-FIELD-V (`400: PGRST204` — my own deliberate smoke test of the new dead-letter Sentry capture on the preview).
- [x] **Empty "Pipeline" nav header in employee view** (spawned as background task `task_dcd8df1b`) — the sidebar section wrapper `#nav-section-pipeline` isn't role-gated but all 3 of its items (Pipeline/Resources/Accounts) are `edit-only` (`.nav-item.edit-only` → `display:none` without `body.manager-mode`, base.css:210-211). An employee-view Core login never gets `manager-mode`, so the items hide and only the orphaned "PIPELINE" label shows. **FIXED + LIVE (v3.5.299, PR #455, 2026-07-11):** took the group-level `edit-only` route — marked `#nav-section-pipeline` `.edit-only` + added `.nav-section.edit-only { display:none }` / `.manager-mode .nav-section.edit-only { display:flex }` in base.css, mirroring the existing `.nav-item.edit-only` pattern. Whole group now hides for employees, shows for managers; apprentice-branch inline `display:none` still wins. Other groups verified unaffected (Operations/Manage/Testing keep non-edit-only items; Safety has its own toggle). Prod curl confirmed v3.5.299 serving. _(added 2026-07-11, done 2026-07-11)_

---

## ⏩ SKS Field — session 2026-07-16 (Equinix SY9 duplicate customer — verified already clean) (rotated 2026-07-27)

**Trigger:** Royce flagged a possible duplicate customer for the Equinix SY9 site on ehow and asked which company name was correct.

**Completed:**
- [x] **Confirmed live: "Equinix Hyperscale 2 (SY9) Pty Limited" (`d79ee06f-…`) is the correct/active SY9 customer** (Royce confirmed) — linked to the real SY9 site (499 assets, 10 contract scopes, 2 quotes). The older duplicate "Equinix Hyperscale" (`a57bf144-…`, created 2026-05-23) and its linked site (`95cdc37d-…`) were both already `active=false` with zero dependent rows (quotes/contacts/scopes/jobs) — cleanup had already happened previously. `eq_merge_customers` RPC not needed, no DML required.
- [x] Logged the resolved name + duplicate-customer history to memory (`project_equinix_entity_map.md`) so future Coupa/PO matching doesn't second-guess "Equinix Hyperscale" (no suffix) as live.

(full investigation + fix recorded in `eq/changelog/field.md` "2026-07-19" — DB-only grant restore PR #498, CI guard PR #500)

---

## ⏩ SKS Field — sessions 2026-06-07 through 2026-06-13 (rotated 2026-07-27 — open items remain in pending.md)

- [x] **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date. **PIN audit 2026-07-05 (Royce-confirmed):** this repo has its own independent login/PIN system, still actively used — a completely different codebase from eq-field, not affected by eq-field's own PIN-gate retirement (see `eq/changelog/field.md` "SKS = Core-only auth", v3.5.200). **[CLOSED 2026-07-27 — Royce-gated decision now tracked fresher at ops/pending.md's SEC-1 checklist (memory sks-labour-retiring.md)]**
- [x] **eq-shell** — ~~converge `c2-shell-roles` + `sks-field-host` branches~~ — `c2-shell-roles` no longer exists in eq-shell repo (deleted). Re-assess: verify whether the security-groups work from `sks-live-sprint-2026-06-07.md` Prompt A was folded into main or abandoned before reopening this track. **[CLOSED 2026-07-27 — re-checked live: security-groups work was folded into main (not abandoned) — merged PRs #210/#231/#237/#240/#285, still actively extended (PR #1047, 2026-07-27)]**

---

## Added 2026-07-05 (rotated 2026-07-27 — open items remain in pending.md)

- [x] sks-charters has no GitHub remote — decide whether it gets pushed to `eq-solutions` org or stays local-only _(added 2026-07-05)_ **[CLOSED 2026-07-27 — done — pushed to eq-solutions/sks-charters (see the closed item at the top of this file, 2026-07-27)]**

---
