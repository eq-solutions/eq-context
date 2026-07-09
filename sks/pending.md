---
title: SKS — Pending
owner: Royce Milmlow
last_updated: 2026-07-06 (eq_update_staff fix)
scope: SKS Technologies operational TODO list
read_priority: critical
status: live
---

# SKS Pending

## Done (pruned summary — full history in git log)

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

## Apply when ready (no code change needed)

_Nothing pending — migrations 001–023 all applied._

## ⚠ Time-sensitive — expires 2026-06-15

- [x] **Worker invites — CLOSED 2026-06-15** — resolved by Royce.
- [x] **8 workers with no email** — CLOSED 2026-06-15.

---

## ⏩ SKS Field — sessions 2026-06-07 through 2026-06-13

**Completed:**
- [x] **ehow SKS canonical DB** — 58 staff + 591 sites synced to ehow (`ehowgjardagevnrluult`). All 11 `app_data.field_*` views created. Full JWT coverage (v3.5.125, PR #267, 2026-06-11). SKS Field (`core.eq.solutions/sks/field`) loads correctly.
- [x] **Audit_log clean slate** — 109 legacy nspb-UUID rows deleted; RLS policies corrected to SKS org_id.

**Pending (Royce-gated):**
- [x] **Roster data entry on ehow — DECISION 2026-06-15** — start fresh on ehow. Do not migrate from nspb. New entries go direct to ehow from now.
- [ ] **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date. **PIN audit 2026-07-05 (Royce-confirmed):** this repo has its own independent login/PIN system, still actively used — a completely different codebase from eq-field, not affected by eq-field's own PIN-gate retirement below.
- [x] **eq-field's standalone PIN gate — retired in practice for SKS (confirmed 2026-07-05).** Three legacy pieces (~1,271 lines): tenant-wide STAFF_CODE/MANAGER_CODE gate, per-worker 4-digit staff-timesheet PIN, supervisor PIN-management UI. All explicitly code-blocked for SKS (`_lockGateForCoreOnly()` + matching guards) — SKS authenticates exclusively via the Shell JWT/cookie handoff. **Cannot be physically deleted yet** — the `eq` demo tenant has no Shell/JWT integration and depends on this gate as its only way in. Full detail: IDENTITY-MODEL.md §7.1.
- [ ] **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
- [ ] **SKS anon-remediation (nspb)** — exact policy worklist in `cross-app-linkage-remediation-plan-2026-06-07.md` §7a. Separate from ehow work. SKS-live gated.

**SKS roles / security-groups track (from 2026-06-07):**
- [x] **eq-roles PR #7 — DONE** — merged, v2.3.0 tagged and on main.
- [ ] **eq-shell** — ~~converge `c2-shell-roles` + `sks-field-host` branches~~ — `c2-shell-roles` no longer exists in eq-shell repo (deleted). Re-assess: verify whether the security-groups work from `sks-live-sprint-2026-06-07.md` Prompt A was folded into main or abandoned before reopening this track.
- [ ] **Security groups Phase 2–5** — wire group perms into session, `AdminSecurityGroups` page, first real `user_security_groups` row for a SKS user.

## ⏩ SKS Field — session 2026-07-03 (QA batch: 9 live bug reports)

**Completed (eq-field v3.5.218–222 + eq-shell PR #619, all merged and live):**
- [x] Leave submit — real error now logged (console + Sentry) instead of generic "check connection"; adapter's specific "no matching staff record" toast no longer gets overwritten
- [x] Timesheets — duplicate "Pre-fill from Roster" button removed
- [x] Timesheets — "Weekends" toggle actually shows Sat/Sun columns now (was wired to a dead renderer)
- [x] Roster — "(unknown)" staff names on cold boot fixed (staff-map load-order race)
- [x] Middle names — display-only strip everywhere (roster/editor/mobile/batch-fill); Editor name-column misalignment fixed alongside it
- [x] Prestarts not saving — `sks_rep`/`site_rep` column typo fixed
- [x] Toolbox Talks not saving — migration applied to ehow adding 4 missing form columns
- [x] `?tab=person-wizard` deep link — Shell-side tab-forwarding race fixed (PR #619); URL correctly holds now
- [x] Site Audits — audited, already correct, no bug
- [x] Document branding — confirmed already shipped v3.5.191, no action needed
- [x] Acknowledgments — confirmed live and working, no action needed

**Deferred (added 2026-07-03):**
- [ ] Person-wizard renders blank content specifically on a cold `?tab=person-wizard` deep-link boot (normal in-app "Add Person" nav works fine) — root cause not found despite exhaustive code trace + live Sentry/entitlement checks; needs Royce's own DevTools session with the Field-iframe console context selected _(added 2026-07-03)_
- [x] At least one SKS person ("Collin ... Toohey") has no record in canonical `app_data.staff`, blocking their leave submissions — data-ops backfill needed, not a code fix _(added 2026-07-03)_ — **RESOLVED, confirmed live 2026-07-06**: `app_data.staff` row exists (`3c9714bd-…`, email `collin.toohey@sks.com.au`, trade `electrical`). Not built this session — found already-fixed during the remediation-queue audit below, likely landed via the 2026-07-02/03 EQ Intake steward-run. Worth confirming his leave submissions actually work end-to-end now that the record exists.
- [ ] Royce to independently click-through-confirm the Weekends toggle, roster names, and both safety forms live (smoke-tested remotely, not yet confirmed by Royce beyond the original repros) _(added 2026-07-03)_

## ⏩ SKS Field — session 2026-07-05 (3-way reconciliation: legacy roster vs canonical vs Cards)

**Verified live** (eq-canonical `jvknxcmbtrfnxfrwfimn` vs sks-labour `nspbmirochztcjijmcrx` legacy live-prod roster, matched by phone):
- 10 real people active in the legacy roster had NO canonical worker record — **created as stubs 2026-07-05** (unclaimed, `+61` phone, role mapped from legacy `group`): Ali Alsalman, Bob Sheather, Carl Waru, Charlie Eyiam-Rowe, Dean Francis, Glen Dwyer, Isaac Hussein, Matthew Dang, Richard Brooks, Walid Hijazi. Ready for the invite batch (Task #1).
- 10 more legacy rows (Kyle Peters, Liam Foster, Mia Thompson, Noah Evans, Oscar Wright, Patrick Hall, Quinn Murphy, Ryan Brooks, Sam Taylor, Tyler James) carry obviously sequential fake phones (`4112000xx`/`4113000xx`) — flagged as legacy seed/demo data, NOT onboarded. Confirm with Royce if in doubt before ever creating stubs for these.
- John Angangan phone mismatch RESOLVED: his real auth account (created 2026-07-01, active login) uses `447444250`, matching the legacy roster — canonical `workers.phone` had the wrong number (`439842416`, likely a data-entry error). **Corrected to `+61447444250`.**
- **Andrew Murphy + Thomas Cavanough — EXCLUDE from the SKS invite batch and any future roster work.** Legacy roster marks both `archived=true` (left the company); canonical `workers` has no equivalent status field (structural gap — worth a future `active`/`left_at` column). Their canonical stubs stay as historical record only.
- **Anthony Hartley duplicate — resolved by exclusion, not deletion.** Keep stub `48a884e9-…` (role=supervisor, has the live invite, stamped 2026-07-04). Stub `098e4bff-…` (role=employee, different phone, no invite) is dead weight — exclude it from the batch; no schema field exists to hard-archive it, so it's just never touched/never invited.
- 10 people exist in canonical/Cards with NO match in the legacy roster — **RESOLVED by Royce 2026-07-05:**
  - **Daniel Bower, Jack Fitzpatrick, Ross Davidson — no longer work at SKS.** Same treatment as Andrew Murphy/Thomas Cavanough above: exclude from the invite batch and any future roster work; canonical stubs stay as historical record only.
  - **Ian Marston, Johannes Otto, John McKee, Jonathan Ryan — all managers.** Role corrected `employee` → `manager` (Leif Lundberg + Mark Brame were already `manager`, no change needed).
  - **Mitchell Forsyrh — subcontractor.** Role left NULL: `'subcontractor'` is **not a valid `eq_role` enum value** (only manager/supervisor/employee/apprentice/labour_hire exist), even though `cards-approve-staff.ts`'s `WORKER_ROLES` JS Set includes it — same class of app-vs-DB vocabulary drift the 2026-07-04 role audit found elsewhere. **Needs a decision: add `subcontractor` to the enum, or map him to an existing role** (`labour_hire` is the closest semantic fit but isn't accurate — a subcontractor runs their own business, unlike agency labour hire).
- Sharon Maroni's canonical phone (`296599199`) looks like a landline (02-prefix), not a mobile — worth a data check before she's included in any phone-OTP invite.
- [ ] **Reverse-angle gap (independent read-only pass 2026-07-05):** 9 legacy `people` rows have a canonical twin already but `people.canonical_id` is still NULL — matched live by phone+email vs jvkn `workers`: Louisa Cardinale, Matthew Khreich, Andre de Biasi, Damon Francis, Timothy Chapman, Bruno Pedrosa, Eric Nguyen (phone-only), Liam Holmgreen, Sam Powell. Back-link write not yet run; handed to the concurrent console actioning this batch (Royce copy-pasted the id list). Low-risk `UPDATE people SET canonical_id=… WHERE id=…` on nspb _(added 2026-07-05)_

## ⏩ SKS Field/Service — session 2026-07-06 (job_plans/defects fixture cleanup + remediation-queue audit)

**Completed (ehow live, SKS tenant, all via direct SQL with Royce's go-ahead at each destructive step):**
- [x] **job_plans duplicate resolved** — closes the "Duplicate job_plans row, SKS tenant" item from the earlier eq-service contract-scope session today (`sessions/2026-07-06.md`). Turned out to be a batch of 4 hand-seeded fixture rows (`e0000000-…0001-0004`, all same timestamp 2026-04-12, zero FK references anywhere), not just the one E1.25 duplicate. `e0000000-…0002` (E1.30/LVNSX) was a second, worse landmine: a NAME collision (not code) against a real, different job plan (E1.30/PFC) — `previewAssetCountsAction` matches by name, so this would have silently conflated two different asset populations on a future import. All 4 soft-deleted (`is_active=false`).
- [x] **defects fixture batch found + hard-deleted** — 7 more hand-seeded rows (`dd000000-…`/`30000000-…`, two sub-batches, shared fake `raised_by` user id absent from both `auth.users` and `profiles`), zero FK references anywhere (confirmed via `pg_constraint` — no formal FK targets `app_data.defects` at all). `defects`' DELETE trigger is a hard delete (unlike `job_plans`, no soft-delete state exists for this table) — flagged and confirmed with Royce before executing.
- [x] **Swept all 21 other canonical `service.*` tables** for the same fixture-UUID pattern (non-RFC-4122 version nibble, not just prefix-guessing) — zero hits. `job_plans` + `defects` were the only two affected tables.
- [x] **Traced the "who resolved this fixture defect" mystery** — actor `85e30693-…` is Royce's own canonical Shell identity (confirmed against eq-canonical `auth.users` = royce.milmlow@sks.com.au), not a rogue process. Looks orphaned only because Plan B JWT sessions never create a Service-local `auth.users` row — the known, documented Phase-2 identity-convergence gap (migration `0132_current_service_uid.sql`).
- [x] **Audited all 16 `eq_remediation_queue` commits** (EQ Intake's "steward-run-001-2026-07-02" data-quality pass, reviewed by Royce 2026-07-03) against live data:
  - 3 `trade` fixes — clean, untouched since commit.
  - 4 `customer_id` link fixes — clean; the one that later changed (Ben Cheam's Equinix contact, deleted 2026-07-06) was a legitimate, attributed action by Simon Bramall (Equinix account lead) through the app, not a bug.
  - 4 of 8 `email` fixes were silently reverted 2 days later (2026-07-05 07:44:07) as a side effect of that same day's SKS roster-reconciliation session (see below — same 4 people: Ian Marston, Johannes Otto, John McKee, Jonathan Ryan). Traced via `app_data.audit_log`: surgical single-field nulls, `actor_id=null`/`source='system'` (direct-SQL, not through the app). **All 4 emails restored** with Royce's confirmation.
- [x] **Broader activity audit** (all contacts/customers/sites/staff writes, by source) — Royce's own 31-site + 17-contact purge (Erilyan Pty Ltd, DigiCo Infrastructure REIT, 2026-07-03) confirmed legitimate: both customers remain active, nothing duplicated/lost. All 6 "system"-sourced staff hard-deletes (2026-07-05) confirmed safe — every one has a live, current staff record for the same person under a different `staff_id`; stale duplicate stubs, not data loss.
- [x] **Root-caused + fixed the unattributed "system" staff-write pattern — `eq_update_staff` (public RPC, eq-shell) had a real bug**: every optional param defaulted to `NULL`, and `NULLIF(trim(NULL), '')` also evaluates to `NULL`, so "field not sent" and "field explicitly cleared" were indistinguishable — any partial-payload call (e.g. only correcting `employment_type`) silently wiped every other field it didn't mean to touch. `first_name`/`last_name` were already correctly `COALESCE`-protected; `email`/`phone`/`trade`/`level`/`employment_type` were not. Confirmed via full `audit_log` history: this fired **3 times, hit 6 people** — Eric (Hoang Minh) Nguyen (2026-06-30, twice same day), Mohammed Nabeel Hussain (2026-07-02), plus the 4 already found (Ryan/Otto/Marston/McKee, 2026-07-05). All 6 emails now restored. `staff-update.ts` (the only wrapper) has zero live callers in eq-shell or eq-field — every hit came from a direct RPC call, which is also why it's unattributed (no PostgREST session, no `x-eq-actor` header to read). Fixed in both the live ehow function and source: eq-shell PR **#681** (`0165_fix_eq_update_staff_field_clobber.sql`, COALESCE added to match the name-field pattern), branched fresh off `origin/main` after an earlier commit accidentally landed on a concurrent session's branch (`claude/staff-job-title-column`) in the shared eq-shell checkout — caught before push, no harm done, but a reminder to branch explicitly off `origin/main` when editing a repo mid-session rather than trusting whatever's currently checked out.

**Deferred:**
- [ ] **Anthony Hartley correction**: not actually a violation of the 2026-07-05 "never touch it" plan — re-checked live. His canonical worker id `098e4bff-…` (the one documented as "dead weight, exclude, no hard-archive field") is still there, untouched, exactly as decided — it's referenced from his current live `app_data.staff` row. What got hard-deleted was a *different* duplicate, at the `app_data.staff` (Service/ehow) layer, not the canonical-worker (jvkn) layer the 2026-07-05 decision was about. No action needed.
- [ ] **121 items still pending in `eq_remediation_queue`** (steward-run-001) — unreviewed AI data-quality suggestions for staff/contacts, sitting in EQ Intake's review queue. Breakdown: 54 missing emergency contacts (low confidence — queue's own guidance is dismiss-only, collect via a future Cards prompt), 43 low-confidence trade guesses, 9 more staff duplicates, 11 more email gaps, 8 firmer trade guesses, 1 contact duplicate. Informational, surfaced while auditing the 16 already-committed rows. _(added 2026-07-06)_
- [ ] **eq-shell PR #681 needs review + merge** — fix is already live on ehow (applied directly ahead of the PR); the PR just brings the source-controlled migration back in sync. _(added 2026-07-06)_

## ⏩ SKS Field — session 2026-07-08 (TAFE timesheet prefill — 4 iterative ships)

**Completed (sks-nsw-labour v3.10.82→85, all merged to main + deployed; ported to eq-field v3.5.263→267):**
- [x] **v3.10.82** — TAFE days no longer mute the timesheet during a configured TAFE holiday (payroll could not enter real hours on the break week). `_tsDayStatus` made holiday-aware via a shared `isTafeHolidayCell()` helper in `tafe.js`.
- [x] **v3.10.83** — soft "🎓 TAFE break" hint on the (now editable) holiday-week TAFE cell so it didn't look like the prefill vanished.
- [x] **v3.10.84** — superseded both: EVERY apprentice TAFE day renders as an editable cell pre-filled with `TAFE`/8h you type a real job over. Stays `workable:false` (completion/40h unchanged); 8h counted via `_tafeHrs`, made **entry-aware (job OR hours)** so overwriting never double-counts. Verified 6/6.
- [x] **v3.10.85 (final, Royce-approved)** — the prefill is driven by each apprentice's **nominated `people.tafe_day`**, not just roster-typed TAFE — so their TAFE day prepopulates EVERY week incl. future weeks. Roster content still wins (site keeps day workable; leave mutes); nominated-day default only fills an empty cell. Verified 8/8.

**Verified live (nspb `nspbmirochztcjijmcrx`):** `app_config.tafe_holidays` correct (winter break 06→17 Jul, anon-readable); **NO `tafe-weekly-fill` cron on the nspb project** (the PR #399 cron enablement was on ehow/canonical — the eq-field data plane — a separate lane). Apprentice nominated `tafe_day`s captured; Terry Su has none (had TAFE hand-typed on 3 roster days); Aiden Crowley nominated=tue but rostered SYD55 that Tue.

**Also completed (same day, after the TAFE work — sks-nsw-labour v3.10.86 / eq-field v3.5.268, merged + deployed):**
- [x] **Labour-hire agency filter on Timesheets** — new Agency dropdown next to Group; pick a business → list narrows to that agency's people so their sheet can be printed/exported and sent. Built from the `people.agency` tag on active LH workers (case-folded); selection persists. `↓ Export CSV` / `↓ Payroll Report` now honour the on-screen filters (were dumping everyone) and the filename carries an agency suffix. eq-field exports unified onto `_getTsFilteredPeople()` (now also include Direct, matching the on-screen view + SKS).
- [x] **Agency data tidy (nspb, 2 rows)** — merged look-alike tags: `Madigans`→`Madagins` (Ali Alsalman) and `core`→`Core` (Zemi Asri). Now 7 clean agencies (Atom×7, Core×2, Cranfield×2, DL Electrical×2, Carter & Osbourne×1, IVI×1, Madagins×3). Royce confirmed spelling = "Madagins".
- [x] **Jose Quintanilla "still labour hire" — fixed (nspb) + guard shipped (v3.10.87 / eq-field v3.5.269).** Root cause: he was moved LH→Direct (`group='SKS Direct'`) but kept `agency='Madagins'`; the app doesn't infer LH from agency, but the stale tag showed against him + leaked him into the new agency filter. **EQ/canonical (ehow `app_data.staff`) was already correct** (Direct, no agency). Cleared his nspb agency manually, then shipped the guard: SKS `savePerson()` forces agency empty for non-LH + hides the field; **eq-field guarded at `savePersonToSB()`** (covers BOTH the add modal and the person wizard) + hides/clears the field on both forms. Was chip `task_354e9f49`. Non-LH people can no longer carry an agency.

**Deferred:**
- [ ] `isTafeHolidayCell()` in `scripts/tafe.js` (both apps) is now **dead code** — the timesheet stopped consulting the holiday config at v3.10.84; writers use `tafeIsHolidayForDay` directly. Low-pri cleanup (leave or remove next timesheet touch). _(added 2026-07-08)_
- [ ] Terry Su has no nominated `tafe_day` → won't auto-prefill going forward; Royce to set it in his profile if he attends TAFE regularly (operational data, not a code fix). _(added 2026-07-08)_

## ⏩ SKS Field — session 2026-07-08 (schedule_entries duplicate root-cause + fix)

**Flagged by a concurrent eq-field session** (auditing a roster Revert bug): 6 `(staff_id, date)` duplicate pairs in `app_data.schedule_entries` on ehow, all involving the `nspb-phase3-2026-07-05` import writing a near-blank second row over an existing real one.

**Completed (with Royce's explicit go-ahead — "fix fully now"):**
- [x] **Confirmed exhaustively** — exactly 6 duplicate pairs exist (not a sample; `GROUP BY staff_id, date HAVING count(*) > 1` returns exactly these 6). No unique constraint existed on `(staff_id, date)` (confirmed via `pg_constraint` — only the `schedule_id` PK).
- [x] **Root cause**: the `nspb-phase3-2026-07-05` import (1,006 rows, 63 staff, dates 2026-06-22→2026-10-30) always did a plain INSERT with no existing-row check. **The actual import script was never found in any repo** — ruled out eq-shell's `etl-nspbmir-to-ehow.mjs` specifically (different `imported_from` tag; its deterministic-UUID formula doesn't match the live duplicate rows' actual `schedule_id`s). If anyone knows what actually ran this (manual script, SQL editor, one-off local file), worth checking directly — the root cause here is a well-evidenced inference from data shape, not a confirmed code read.
- [x] **Live-display risk found**: `eq-field/scripts/roster-adapter.js`'s `toWideList` currently shows the correct real data for all 6 people, but only because an *unordered* query happens to return the real row first (heap/physical storage order) — not a guaranteed contract. A VACUUM, new index, or query-plan change could silently flip 6 people's roster cells to blank with zero error anywhere. The function's own inline comment ("last writer wins") is backwards from what the code actually does (first-non-empty wins) — small separate bug, not yet fixed, flagged for whoever's next in that file.
- [x] **Fixed live on ehow**: deleted the 6 stub rows after confirming each was a pure subset of its real-row counterpart (every field null or identical — nothing lost). Added `UNIQUE (staff_id, date)` on `app_data.schedule_entries` (migration `schedule_entries_staff_date_uniq`) so this can't silently recur regardless of what wrote it or whether it runs again. Verified: 0 duplicates remain, all 6 real rows intact, 1000 of the original 1006 import rows untouched.

**Deferred:**
- [ ] `toWideList`'s "first non-empty wins" logic (and its backwards comment) in `eq-field/scripts/roster-adapter.js` — not fixed (another session was already active in this file; avoided a concurrent edit). Worth a defensive tiebreak (prefer non-`imported_from` rows) as belt-and-suspenders now that the constraint prevents new duplicates. _(added 2026-07-08)_
- [ ] Source of the `nspb-phase3-2026-07-05` import itself is still unknown — no `nspb-phase1`/`nspb-phase2` tag exists anywhere either, so it's unclear if this was a manual one-off or part of a larger unlogged migration effort. _(added 2026-07-08)_

## ⏩ SKS Field — session 2026-07-04 (Cards→Field migration path verified, read-only)

**Verified live (eq-canonical `jvknxcmbtrfnxfrwfimn` + eq-field repo) — no code changed:**
- New **eq-field reads eq-canonical directly** (app-state.js:27-28). Write-through: editing a Field person looks up canonical `workers` by email, creates a stub if absent, stores `worker_id` back (people.js:1032-1050). Licences **live-read** from canonical via RPC `eq_get_org_licences(p_org_id)` (canon-read.js:142). This validates Royce's migration model: set up in canonical → Field reads it → licences flow through, no re-keying.
- **No-dup dedup** = `eq_cards_link_or_create_worker` adopts an unlinked stub by **normalised phone OR email** (phone = last-9 AU digits; prefers most-credentialed stub; single stub). Mobile is the load-bearing key (Cards = phone-OTP, email often blank).
- **Apply-to-SKS** = `eq_cards_submit_access_request` → `org_access_requests`; SKS org (`00000000-…-0002`, tenant `7dee117c`) has **accepts_applications=true**.
- **Licence review** = admin approval writes `shell_control.cards_field_approvals` (`licence_verifications` jsonb + `licences_verified_at`). Credential enum has NO review state — review lives on the approval row.

**Deferred / next:**
- [ ] First **Cards→Field approval for SKS never run** — `cards_field_approvals` has 79 rows across other tenants, **0 for SKS**. When the first SKS worker signs up to Cards + applies, exercise the admin approve + licence-verify path end-to-end (machinery proven elsewhere, unproven for this tenant) _(added 2026-07-04)_
- [ ] **SKS staff data-entry rule** — enter each person **once** with an accurate mobile (+ email where held); no DB uniqueness on `workers.phone`, so two stubs sharing a number = only the best-credentialed one gets adopted, the other dangles. 0 phones on multiple worker rows today — keep it that way _(added 2026-07-04)_

---

## Done (this session — 2026-06-01)

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

## Pending (added 2026-06-01)

- [ ] Book monthly check-in cadence with Richo (Michael Richardson)
- [ ] Tell Mark about catch-up conversations before starting (casual, no fanfare)
- [ ] Confirm Scott Hotson start date + written offer
- [ ] Schedule Simon Bramall catch-up — Equinix Account Lead conversation
- [ ] Hold Ben Ritchie coffee — first/second week back
- [ ] Schedule Simon + Matt three-way (Equinix rhythm + scope clarity)
- [ ] Koos Otto role redesign conversation — HV Technical Lead framing
- [ ] Pair Huon Henne with Leif as comms shadow — frame as deployment
- [ ] Launch weekly construction PM standup (Royce chairs initially, Ben presents LOTO)
- [ ] Set up MS Planner board (setup PDF at `SKS_NSW_Delivery_Planner_Setup.pdf`)
- [ ] Leif → Senior Comms Advisor reframe — demand-driven framing
- [ ] Wayne Rowe exit conversation — Mark to own
- [ ] Charlotte White → Project Coordinator scope definition

## Tools built (2026-06-01) — reference

| Deliverable | File | Format |
|---|---|---|
| NSW Operating Plan v2 | `SKS_NSW_Operating_Plan_v2.html` | HTML |
| Interactive org chart | `SKS_NSW_Org_Chart_Interactive.html` | HTML |
| Personal operating system setup | `Royce_Operating_System_Setup.pdf` | PDF |
| MS Planner delivery system setup | `SKS_NSW_Delivery_Planner_Setup.pdf` | PDF |
| Scott Hotson JD | `Scott_Hotson_Operations_Lead_SKS.docx` | Word |

## Active (in progress or blocked)

- [ ] ~~**Workbench customer CSV import**~~ — **CANCELLED** — eq-quotes (Flask) is retired; EQ Ops is the replacement. Re-evaluate if import is still needed against EQ Ops.

## Test suite — EQ Quotes (RETIRED — do not work on these)

The following tests belong to eq-quotes-port (Flask), which is retired as of 2026. EQ Ops replaces it. These items are closed with no action required.

- ~~Rewrite test_calc.py~~
- ~~Rewrite test_quotes_service.py~~
- ~~Rewrite test_schema.py~~
- ~~Update test_validation.py~~

## Open conversations (deferred from handoff-2026-05-22)

| # | Topic | Notes |
|---|---|---|
| 1c | **Smarter contact dedup** | Manual merge of any two contacts, phone-aware auto-detection |
| 2 | **Stop SimPRO mirroring at source** | Change next SimPRO sync to stop the customer × site denormalisation |
| 3 | **Per-customer cost-split ratio (Budget)** | Equinix ÷1.1, Ramsay ×0.4, etc. Add 5th customer column |
| 4 | **Auto-email Job Creation Template + status flip on download** | Verbal Win → Won-Awaiting Job No on send |
| 5 | **ABR API integration for ABN auto-fill** | abr.business.gov.au free lookup, "Look up ABN" button per customer |
| 6 | **Smart AI enrichment for customer fields** | Claude API: market_vertical + end_client from name; alias propagation |
| 7 | **Backfill missing invoice emails + ABNs** | After #5+#6 land |
| 8 | **Phase 3: drop legacy contact columns after soak** | **Phase 1 done 2026-05-23** (migration 021): `primary_contact_id` live, 323/518 FKs set. **Phase 2 done 2026-05-23** (v77): app reads via FK with legacy fallback, inline picker writes `contact_id`, dual-write soak started. **Phase 3 (v79):** migration 023 (was "022" — renumbered after EQ Field sync consumed 022) `DROP COLUMN contact, email, phone`; remove fallback branches. Safe after ≥24h soak. |
| E | **Group-level pagination on /customers** | 2-step query: DISTINCT names → fetch rows per page. PERF TODO in `customers.py:list_for_admin_grouped`. Trigger: >5k customers OR p95 >800ms after speed pass |

## Known gaps the team will hit

1. **ABN blank on every generated Job Creation Template** — paste once per customer via `/customers/<id>` → "Job creation defaults" → "ABN" inline edit
2. **Invoice email blank for Ramsay, Schneider, Metronode, 3/9 Equinix** — same path
3. **Cost data NULL on quotes before v62** — estimators should re-enter Cost values when editing older quotes

## Added 2026-07-05

- [ ] David Boyd charter — confirm qualification path (electrical licence / Cert IV / Diploma PM / senior-title move) and sharpen the "Where you're growing" section
- [x] sks-charters generator — reviewed, built, and committed locally (`59ec109`)
- [ ] sks-charters has no GitHub remote — decide whether it gets pushed to `eq-solutions` org or stays local-only _(added 2026-07-05)_
- [ ] `npm run check` (blank-trailing-page regression check) needs LibreOffice (`soffice`) + poppler (`pdftoppm`) installed on the Beelink — currently neither is on PATH, script degrades gracefully but doesn't actually validate _(added 2026-07-05)_

## Untouched substrate items

(Separate from EQ Quotes — preserve)

- [ ] Bring apprentice module from demo to SKS Labour prod
- [ ] Scale EQ Field App for Melbourne office demo
- [ ] R2 backup audit/download from Beelink desktop
- [ ] Scott Hotson hire finalisation
- [ ] One-on-one catch-up sessions with 8 key staff — 7 Role Step-Up Charters drafted 2026-07-05 (Collin, Rhys, William, Simon, Matt, David, Luke) as supporting artefacts for these conversations
- [ ] Comms portfolio growth under Royce
