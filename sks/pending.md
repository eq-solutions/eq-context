---
title: SKS — Pending
owner: Royce Milmlow
last_updated: 2026-07-21
scope: SKS Technologies operational TODO list
read_priority: critical
status: live
---

# SKS Pending

## Real security hole found in SKS's standalone Field system — not fixed, handed off properly (2026-07-20)
*Found while investigating an unrelated EQ Cards issue that turned into a wider cleanup — see `eq/pending.md` for that side. This part is pure SKS, nothing touched, nothing changed.*
- [ ] **SKS's standalone Field app (sks-nsw-labour) currently lets anyone with the app's public web address read or wipe roster/schedule/timesheet data for all ~50 SKS people — no login required.** A 4-stage fix plan already exists: Stage 1 (the identity layer) is built and sitting in an unmerged pull request, ready to activate; Stage 2 (locks data to the right company) is drafted but not run; Stage 3 (removes the open door) is drafted but has 3 known gaps that need closing first (a few tables would go offline instead of getting properly locked down); Stage 4 (final cleanup) isn't drafted yet. Nothing on SKS's live system was touched — this needs Royce's own hands per stage (setting secrets, running SQL, flipping a switch), plus review of the gaps before Stage 3 is safe. Handed off as its own task rather than half-finishing it inside an unrelated session. _(added 2026-07-20)_
  - **Follow-up same day:** all 3 gaps from Stage 3 closed in the Stage-2 draft (the 5 tables now included, the 2 stale-policy tables fixed). Also found a *separate, worse* problem while re-checking live: the app's shared settings table can currently be read by anyone with the public web address too — including what look like internal backend passwords, not just company data. Traced every place that setting is actually used and confirmed removing anon access to the backend-only ones breaks nothing live — drafted, double-checked, ready to run, still **not run** (Royce: "not risking any changes" on a live app with ~50 active users). Also found the same public-access problem on individual staff PIN codes (used to submit timesheets) — but the safe fix there needs an app code change first (the app currently checks PINs in the browser instead of on the server), so that's handed off as its own separate task rather than rushed. A full step-by-step runbook for when Royce is ready exists; nothing requires immediate action. _(added 2026-07-20, same day)_

---

## SKS Field — session 2026-07-21 (mobile My Schedule + home tile: show Sat/Sun when rostered)

**Trigger:** Royce spotted the mobile "My Schedule" day cards only showing Monday-Friday, even though a screenshot showed people rostered to work weekends.

**Completed:**
- [x] **sks-nsw-labour v3.10.99 (PR #68, MERGED, live)** — My Schedule day cards (`roster.js`) and the home tile's shift count / next-shift / schedule subtitle (`home.js`) now build their day list from the existing `getVisibleRosterDays()` helper instead of a hardcoded Mon-Fri array, so Sat/Sun show whenever that week actually has weekend work — same rule the desktop roster grid already uses. Display-logic only, no schema change. Same fix ported to EQ Field the same session (v3.5.338, PR #514, merged) — see `eq/pending.md`.

**Deferred:**
- [ ] Royce to click-through confirm a real weekend-rostered person's mobile schedule + home tile on both apps. _(added 2026-07-21)_

---

## NSW Comms — dashboard, Patrick's demo follow-up, speed fix (2026-07-17/19)
- [ ] **Still needed: who should receive the weekly NSW Comms summary email?** Built, just needs a recipient list before it's switched on. _(added 2026-07-17)_

## Monday meeting prep — Royce + Adam (SKS), adoption + data-security discussion (2026-07-16)
- [x] **Terms/legal review + fixes done, talking points drafted.** Full detail in `eq/pending.md` (EQ-side work: eq-service `/terms` taken down, eq-cards wording softened, eq-field/eq-shell confirmed clean). Positioning locked: personal-tooling framing, no marketing/customer language, Royce recuses from any commercial-terms question. _(done 2026-07-16)_
- [ ] **Not done: live-demo readiness check** (data cleanliness / no visible errors on whatever screen gets shown) — offered, awaiting Royce's go. _(added 2026-07-16)_

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

**Pending (Royce-gated):**
- [x] **Roster data entry on ehow — DECISION 2026-06-15** — start fresh on ehow. Do not migrate from nspb. New entries go direct to ehow from now.
- [ ] **Standalone `sks-nsw-labour` retirement** — NOTE: app is still receiving active feature work as of 2026-06-26 (PRs #32–#54 merged in June). 'Keep warm' understates current investment. Retirement gating question is still open — confirm with Royce whether ehow Field has superseded the standalone app before setting a retirement date. **PIN audit 2026-07-05 (Royce-confirmed):** this repo has its own independent login/PIN system, still actively used — a completely different codebase from eq-field, not affected by eq-field's own PIN-gate retirement (see `eq/changelog/field.md` "SKS = Core-only auth", v3.5.200).
- [ ] **Track 2 RLS STEP 2** — anon SELECT lockdown on ehow. DEFERRED until standalone retired.
- [ ] **SKS anon-remediation (nspb)** — exact policy worklist in `cross-app-linkage-remediation-plan-2026-06-07.md` §7a. Separate from ehow work. SKS-live gated.

**SKS roles / security-groups track (from 2026-06-07):**
- [x] **eq-roles PR #7 — DONE** — merged, v2.3.0 tagged and on main.
- [ ] **eq-shell** — ~~converge `c2-shell-roles` + `sks-field-host` branches~~ — `c2-shell-roles` no longer exists in eq-shell repo (deleted). Re-assess: verify whether the security-groups work from `sks-live-sprint-2026-06-07.md` Prompt A was folded into main or abandoned before reopening this track.
- [ ] **Security groups Phase 2–5** — wire group perms into session, `AdminSecurityGroups` page, first real `user_security_groups` row for a SKS user.

## ⏩ SKS Field — session 2026-07-03 (QA batch: 9 live bug reports)

**Deferred (added 2026-07-03):**
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

**Deferred:**
- [ ] **Anthony Hartley correction**: not actually a violation of the 2026-07-05 "never touch it" plan — re-checked live. His canonical worker id `098e4bff-…` (the one documented as "dead weight, exclude, no hard-archive field") is still there, untouched, exactly as decided — it's referenced from his current live `app_data.staff` row. What got hard-deleted was a *different* duplicate, at the `app_data.staff` (Service/ehow) layer, not the canonical-worker (jvkn) layer the 2026-07-05 decision was about. No action needed.
- [ ] **121 items still pending in `eq_remediation_queue`** (steward-run-001) — unreviewed AI data-quality suggestions for staff/contacts, sitting in EQ Intake's review queue. Breakdown: 54 missing emergency contacts (low confidence — queue's own guidance is dismiss-only, collect via a future Cards prompt), 43 low-confidence trade guesses, 9 more staff duplicates, 11 more email gaps, 8 firmer trade guesses, 1 contact duplicate. Informational, surfaced while auditing the 16 already-committed rows. _(added 2026-07-06)_
- [ ] **eq-shell PR #681 needs review + merge** — fix is already live on ehow (applied directly ahead of the PR); the PR just brings the source-controlled migration back in sync. _(added 2026-07-06)_

## ⏩ SKS Field — session 2026-07-08 (TAFE timesheet prefill — 4 iterative ships)

(full ship history — v3.10.82→87 TAFE prefill + agency filter + Jose Quintanilla fix — recorded in `sks/changelog/labour.md` "2026-07-08"; eq-field ports v3.5.263→269 recorded in `eq/changelog/field.md`)

**Deferred:**
- [ ] `isTafeHolidayCell()` in `scripts/tafe.js` (both apps) is now **dead code** — the timesheet stopped consulting the holiday config at v3.10.84; writers use `tafeIsHolidayForDay` directly. Low-pri cleanup (leave or remove next timesheet touch). _(added 2026-07-08)_
- [ ] Terry Su has no nominated `tafe_day` → won't auto-prefill going forward; Royce to set it in his profile if he attends TAFE regularly (operational data, not a code fix). _(added 2026-07-08)_

## ⏩ SKS Field — session 2026-07-10 (schedule_entries duplicate root-cause + fix)

**Flagged by a concurrent eq-field session** (auditing a roster Revert bug): 6 `(staff_id, date)` duplicate pairs in `app_data.schedule_entries` on ehow, all involving the `nspb-phase3-2026-07-05` import writing a near-blank second row over an existing real one.

**Completed (with Royce's explicit go-ahead — "fix fully now"):**
- [x] **Confirmed exhaustively** — exactly 6 duplicate pairs exist (not a sample; `GROUP BY staff_id, date HAVING count(*) > 1` returns exactly these 6). No unique constraint existed on `(staff_id, date)` (confirmed via `pg_constraint` — only the `schedule_id` PK).
- [x] **Root cause**: the `nspb-phase3-2026-07-05` import (1,006 rows, 63 staff, dates 2026-06-22→2026-10-30) always did a plain INSERT with no existing-row check. **The actual import script was never found in any repo** — ruled out eq-shell's `etl-nspbmir-to-ehow.mjs` specifically (different `imported_from` tag; its deterministic-UUID formula doesn't match the live duplicate rows' actual `schedule_id`s). If anyone knows what actually ran this (manual script, SQL editor, one-off local file), worth checking directly — the root cause here is a well-evidenced inference from data shape, not a confirmed code read.
- [x] **Live-display risk found**: `eq-field/scripts/roster-adapter.js`'s `toWideList` currently shows the correct real data for all 6 people, but only because an *unordered* query happens to return the real row first (heap/physical storage order) — not a guaranteed contract. A VACUUM, new index, or query-plan change could silently flip 6 people's roster cells to blank with zero error anywhere. The function's own inline comment ("last writer wins") is backwards from what the code actually does (first-non-empty wins) — small separate bug, not yet fixed, flagged for whoever's next in that file.
- [x] **Fixed live on ehow**: deleted the 6 stub rows after confirming each was a pure subset of its real-row counterpart (every field null or identical — nothing lost). Added `UNIQUE (staff_id, date)` on `app_data.schedule_entries` (migration `schedule_entries_staff_date_uniq`) so this can't silently recur regardless of what wrote it or whether it runs again. Verified: 0 duplicates remain, all 6 real rows intact, 1000 of the original 1006 import rows untouched.

**Deferred:**
- [ ] `toWideList`'s "first non-empty wins" logic (and its backwards comment) in `eq-field/scripts/roster-adapter.js` — not fixed (another session was already active in this file; avoided a concurrent edit). Worth a defensive tiebreak (prefer non-`imported_from` rows) as belt-and-suspenders now that the constraint prevents new duplicates. _(added 2026-07-10)_
- [x] Source of the `nspb-phase3-2026-07-05` import **identified (Royce, 2026-07-10)**: `nspb` = the standalone **sks-nsw-labour** Supabase project (`nspbmirochztcjijmcrx`, the retiring legacy app). So `nspb-phase3` was a **legacy→canonical roster data migration** pulling roster out of sks-nsw-labour into ehow `app_data.schedule_entries` — not a committed repo script (which is why grepping every repo found nothing), most likely a manual/ad-hoc run. "Phase 3" implies phases 1/2 migrated staff/sites earlier under different tags. **Tension worth noting:** the 2026-06-15 decision was "start fresh on ehow, do NOT migrate from nspb" — yet this migration ran 2026-07-05, three weeks later. Either a deliberate one-off historical backfill that superseded that call, or a run that shouldn't have happened. The `UNIQUE (staff_id, date)` constraint neutralises the duplication risk either way (any future/final nspb backfill now fails loudly, not silently). Optional next step if Royce wants it fully nailed: query nspb directly to confirm the 6 people's TAFE rows exist there as the migration source. _(added 2026-07-10, resolved 2026-07-10)_

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

## Cancelled

- ~~**Workbench customer CSV import**~~ — **CANCELLED** — eq-quotes (Flask) is retired; EQ Ops is the replacement. Re-evaluate if import is still needed against EQ Ops.

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

## ⏩ SKS Field — session 2026-07-10 (roster "Save failed — check connection" — two distinct root causes)

**Reported live:** Collin Toohey hit a "Save failed — check connection" toast on a roster save; Simon Bramall separately reported failures specifically editing roster entries more than a month out. Investigated as one ticket, turned out to be two unrelated bugs sharing the same generic error toast.

**Process note:** hit the same collision twice this session — both `C:\Projects\sks-nsw-labour` and `C:\Projects\eq-field` root checkouts had unrelated uncommitted work from concurrent sessions (`scripts/batch.js` on sks main-adjacent branch; `scripts/audit.js`+`scripts/supabase.js` audit-revert canon patching on eq-field `main`). Used dedicated fresh worktrees off `origin/main` for both instead of touching root, registered in `worktree-registry.md`. Also hit a squash-merge trap: a branch cut locally *after* a PR merged (from the pre-squash local commit, not `origin/main`) diverges from the squashed commit GitHub creates — same content, different SHA, false merge conflict. Fix is `git rebase origin/main <branch>` (git recognizes the duplicate content and skips it), not a manual conflict resolution.

## ⏩ SKS Field / EQ Field — session 2026-07-10 (full pagination sweep)

**Trigger:** picked up the eq-field export truncation flag from the earlier same-day session (`task_69a6ff0f` above). Before building, verified the premise against live git/GitHub state rather than trusting the flag at face value — this caught that the referenced "SKS v3.10.89 fix" was real (PR #56, merged, a genuine live incident — Simon Bramall's far-future roster gap) but only covered the `schedule` table; its sibling `timesheets` load in the exact same function was never touched.

**Deferred:**
- [ ] `audit_log`/`prestarts`/`toolbox_talks` recency caps (both apps) — not a bug, but if older history genuinely needs to be reachable, that's a pagination-UI or date-filter feature to design, not a copy of `sbFetchAll()`. _(added 2026-07-10)_

## ⏩ SKS Field — session 2026-07-12 (loadFromSupabase resilience — one table's failure can't freeze the app)

**Trigger:** follow-up to the pagination sweep. The v3.10.90→.92 outage exposed a deeper fragility — `loadFromSupabase()`'s `Promise.all` over ~8 tables was all-or-nothing: any single 4xx (a future id-less table, an RLS regression, a renamed column, a transient 500) failed the WHOLE sync and silently dropped every user onto their last IndexedDB snapshot, the only symptom being the "Cached …" banner not advancing. The root 400 was fixed in v3.10.92 (#59); the fragility itself was not. Verified base first: my checkout was one commit behind — reset to origin/main (v3.10.92) so the resilience layer sits ON the root fix, not clobbering it. Confirmed live that `team_members`/`timesheet_locks` have no `id` column.

**Completed:**
- [x] **sks-nsw-labour v3.10.93 (PR #60, MERGED, live — `0f68678`)** — split the load into load-critical (people/sites/schedule/managers/timesheets — a failure still aborts the sync and keeps the last-good snapshot) vs optional (teams/team_members/timesheet_locks — wrapped in `.catch(()=>[])` so one table's failure degrades that one feature, not the whole app; same pattern as `apprentices.js` Tier-2). Preserve-on-failure: a failed optional table keeps its last-known value instead of overwriting STATE/the offline snapshot with `[]`. Degraded/failed syncs are now observable — user toast + `sync_degraded` PostHog event (kind partial|failed) + console breadcrumb, transition-guarded so the 30s poll reports once on the healthy→degraded edge, not every tick. Verified end-to-end against the REAL function with forced 400s (optional 400 → app not blanked; critical fail → cached fallback; repeat failure → one toast; failed-optional → data preserved). `index.html` only; `sbFetch`/`sbFetchAll` throw-on-4xx-GET semantics unchanged. Prod serves APP_VERSION 3.10.93.

**Deferred:**
- [x] **EQ Field reconcile — SHIPPED (eq-field #459, v3.5.304, MERGED + live on field.eq.solutions).** EQ Field already solved the freeze via `_loadSafe` (v3.5.201), so it was never exposed. The observability session (`task_8c1fb92e`) closed the two real gaps: (1) **preserve-on-failure** — found a genuine live bug: `_loadSafe` swallowed a failed core fetch to `[]`, then the poll's `STATE.people = people.map(...)` overwrote good on-screen data with empty, blanking Contacts/roster for ~30s on any transient blip (Field has no last-good snapshot). Now each core STATE write skips a failed table, keeping last-known values. (2) **observability** — `_emitSyncHealth()` raises a toast + `sync_degraded` PostHog event (via `analytics.js _events`, house convention), transition-guarded. Client-only, no DB/auth change, not cross-deployed. _(added 2026-07-12, done 2026-07-12)_
- [ ] **Reconcile the two opposite conclusions on EQ Field's id-less `order=id`** — the order=id session (`local_9542b49d`) verified live that Field's `team_members`/`timesheet_locks` load via `app_data.field_*` twin views which HAVE `id`, concluded "not a bug", and Royce said "no change". Yet **eq-field #460 (v3.5.305, merged + live) then added explicit PK ordering to those exact sbFetchAll calls anyway.** Both shipped safely (explicit PK order is harmless even when `id` exists), but the conflicting conclusions mean one session's premise was incomplete — likely a code path that hits the base tables (not the `field_*` view) e.g. a non-SKS/demo tenant. Low-risk, worth a 10-min confirm of which path #460 was guarding. _(added 2026-07-12)_

## ⏩ SKS Field — session 2026-07-12 (outage prevention hardening + EQ Field audit)

**Trigger:** follow-up to the outage post-mortem — "do we know what caused it, and can we stop it recurring." The v3.10.90→.92 outage had three enablers: a silent `order=id` default in `sbFetchAll` (latent trap), no observability (a *handled* 400 → 0 `error_thrown`, invisible ~2 days), and no CI at all. This session built the prevention, then audited whether EQ Field needs the same.

**Completed:**
- [x] **sks-nsw-labour v3.10.95 (PR #63, MERGED, live — `b8cd308`)** — three prevention layers. (1) **Fail-loud `sbFetchAll`** (`scripts/supabase.js`): throws if a caller passes no `orderBy` and the path has no `order=`, instead of silently defaulting to `order=id` — the exact latent trap behind the outage now fails at the call site, loudly, in dev/CI. 7 existing callers given explicit `'id'`. (2) **Degrade email alert** (`index.html` `_alertSyncDegraded`): on a degraded/failed sync, emails `leaveCCList` (ops distribution) via the `send-email` function — throttled 1/device/day (localStorage), SKS-tenant-only, self-guarded so an alert failure can't cascade. Wired off the existing `_emitSyncHealth` edge (v3.10.93), so it fires once per healthy→degraded transition, not every tick. (3) **Bootstrap smoke test** (`scripts/smoke/bootstrap-smoke.mjs` + `.github/workflows/smoke.yml`) — **the repo's first CI.** Hits every table `loadFromSupabase()` reads, the way the app reads it, asserts 2xx; self-configures the sks url/anon-key from `app-state.js` (both public); includes an invariant guard asserting `team_members`/`timesheet_locks` still 400 on `order=id` (so a revert of the fail-loud change is caught here, not as a silent prod outage). Verified GREEN against the live DB. Runs on push to main alongside Netlify's own deploy.
- [x] **Merge parity checklist created (`docs/merge/sks-eqfield-parity-checklist.md`, #62 + #64)** — the cutover gate for when the SKS tenant moves onto the EQ Field codebase. Seeded with the v3.10.94 timesheet UX (hours-flag / weekend auto-show / Sunday rollover) and the two v3.10.95 resilience layers, each with its EQ Field status + the audit verdict.

**Decided (Royce):**
- Build #2 (fail-loud) + #4 (degrade alert) and scaffold #3 (smoke) → shipped all three as v3.10.95.
- Merge #62 + #63 for SKS.
- Before porting anything to EQ Field: "audit then steelman then build — no mistakes."
- Add the fail-loud + degrade-alert items to the merge checklist (#64).

**Audit verdict — neither resilience layer is required for EQ Field now (do NOT port speculatively):**
- **EQ Field structurally can't freeze** — its core boot wraps every fetch in `_loadSafe` (`.catch → []`), so a stray 400 degrades one feature (observably) rather than the whole app. This is *why* SKS froze (unguarded `Promise.all`) and EQ Field never did.
- **Only un-`orderBy`'d id-less caller is `project_targets`** (`scripts/supabase.js`) — and it's `try/catch`-guarded (→ `[]`), Enterprise-tier-only (loader short-circuits below Enterprise), and the table **doesn't exist on eq-canonical OR ehow** (verified live → both `[]`). It would 404, not even hit the `order=id` path. A non-issue.
- **Degrades already observable on EQ Field** via `sync_degraded` (#459); and there are **no live users to email-alert** (field.eq.solutions = deploy-preview traffic only).
- Both belong on the merge-time parity checklist (SKS code carries them across at the codebase-merge phase), not as divergent speculative code with a real regression risk. Logged to #64.

**Deferred:**
- [ ] **Prevention Layer #5 (review/process)** — the outage also had *no human review* (self-merged) as an enabler; a lightweight review gate or required-check on this repo is a process call, Royce's to make. _(added 2026-07-12)_
- [ ] **PR #64 awaiting merge** — the checklist update (fail-loud + degrade-alert as merge parity) is a docs-only PR; auto-mode classifier blocked me self-merging it (ask was "add the items", not "merge without review"). Royce to merge. **NOTE:** the later login fix (#65, merged) also edited `docs/merge/sks-eqfield-parity-checklist.md` (added a "Login / role parity" section), so #64 may now need a rebase before it merges cleanly. _(added 2026-07-12)_

## ⏩ SKS Field — session 2026-07-12 (login: supervisor no longer drops to view-only after a reload)

**Trigger:** Royce reported the SKS login "logs me in as supervisor, logs me out, then logs me back in as view-only — every time." Asked to audit + give options.

**Root cause (audited, not guessed):** supervisor status was held in a *one-shot* sessionStorage flag `eq_auto_admin` that `initApp()` read once and then **deleted** (index.html). The logged-in flag `eq_access_v1` is durable across reloads; the supervisor flag was not. Any same-tab reload — most often the **service-worker auto-reload on deploy** (we shipped four builds that day) — re-ran `initApp()` with the flag already consumed → fell through to `applyStaffMode()` (view-only). `checkAccess()` also early-returned on `eq_access_v1` *before* the durable remember-me restore, so even a remembered supervisor login was bypassed. Staff never noticed (view-only anyway) → looked account-specific. No security hole; a state-persistence bug.

**Completed:**
- [x] **sks-nsw-labour v3.10.96 (PR #65, MERGED + deploying — `6f3eccc`)** — **Option 1 (durable role):** write a durable `eq_role` key at every login path (tenant-code gate, demo, production verify-pin, shell-token SSO, both remember-me restores) and read it in `initApp()` on **every** boot, so supervisor survives a reload. `eq_auto_admin` is kept only to fire the login-moment UX (welcome toast + dashboard jump), never the role. "Switch to view only" + mid-session unlock both update `eq_role` (that choice also survives a reload); logout clears it. Back-compat for sessions open across the upgrade via the legacy flag. **Option 3 (calmer reload):** the SW-activated reload no longer fires instantly — defers to a non-disruptive moment (`_scheduleSwReload`: tab backgrounded, or first safe foreground moment — never mid-edit/type/queued-write; 5-min hard cap). `scripts/auth.js` + `index.html` only; no change to how anyone logs in. Syntax-checked; inline-script parse-error count unchanged vs main.

**Decided (Royce):**
- Fix approach = **Option 1 + 3** (durable role + defer the SW reload), chosen from the audit's four options.
- **Merge** #65 → authorised the production deploy (auth change — explicit approval given).

**Deferred:**
- [ ] **One-time transition after this deploy** — supervisors *currently* logged in have a pre-v3.10.96 session with no `eq_role` (and `eq_auto_admin` already consumed), so their first reload onto v3.10.96 shows view-only once; a single log-out/log-in (or re-unlock) seats the durable role permanently. New logins are correct immediately. Told Royce; no code owed. _(added 2026-07-12)_
- [ ] **EQ Field login-parity check (merge-time)** — EQ Field's login model differs (Shell JWT handoff / canonical, not name+code), so this is **not a verbatim port**. At the codebase-merge phase, verify whether EQ Field re-derives role on every boot or has the same one-shot-consume trap, and fix in its own terms. Logged to the merge parity checklist ("Login / role parity" section). _(added 2026-07-12)_

## ⏩ SKS Field — session 2026-07-12 (DB "not working" outage → root fix + timesheet UX)

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

## ⏩ SKS Field — session 2026-07-11 (Safety offline queue unwedge + Resource Allocation capacity panel + Sentry triage)

**Completed (eq-field, all merged to main + live):**
- [x] **Safety "1 pending offline write" stuck forever (v3.5.298, PR #451).** A prestart saved offline ~25 June (pre-v3.5.220 build) still carried the old `sks_rep` field name; the live `prestarts` column is `site_rep`, so every replay 400'd (`PGRST204`) and re-queued — a poison pill with no exit, re-firing on every Safety open. Fix in `safety.js _qReplay`: (1) normalise queued payloads on replay (`sks_rep`→`site_rep`) so the stuck June prestart actually lands in the DB, not discarded; (2) entries that fail with a permanent 400/404 are parked in a `<queueKey>_dead` localStorage key (payload + error kept, Sentry-captured) and removed from the live queue so the pending pill can't wedge. Transient failures (network/401/403/5xx) still retry. Same dead-letter guard added to `site-reports-shared.js replay()`. No DB change (live `prestarts` schema verified correct first). **Renumbered v3.5.296→298 at merge** — a concurrent session's JSZip perf PR #452 took 296, capacity panel took 297.
- [x] **Resource Allocation capacity panel never rendered for labour-curve jobs (v3.5.297, PR #453).** The Capacity Planning panel stayed on the "Set start dates and worker counts…" empty state for phase-planned jobs (e.g. SKS-16310: start date + 3 phases, flat `peak_workers`/`duration_weeks` empty). The demand builder fully supported phases; only the render GATE checked the flat fields. New `_isAllocated()` gate matches the builder (start date + phases OR peak+duration). Also, per the reviewed "Mock B" design: panel now reads **roster-first** (THIS WEEK strip — N on roster · N free · N jobs live · N needed — above the stat tiles); chart **scales to demand not headcount** (with 90 on the books vs 4–12-crew jobs the old max(HC,demand) scale flattened every job; HC dashed line only draws when demand is within reach, else a legend chip); peak-demand tile names its week; WORKERS/WEEKS/timeline/colour derive from the curve when flat fields empty. **"Save phases" now rebuilds the unpushed labour plan** so "N to assign" tracks the current curve (SKS-16310 showed a stale "66 to assign" from its confirm-time curve while the edited curve implied 114); rows already pushed to the live roster are never touched. SKS-only surface, no DB change.
- [x] **Sentry eq-field queue cleared to zero** — all 5 unresolved issues triaged + resolved, none needed new code: EQ-FIELD-R (`isLeave is not defined`, calendar — fixed by lazy-loader commit d18638f, event predated it); EQ-FIELD-M (null `staff_id` leave POST — fixed by v3.5.221 pre-check, event on v3.5.218); EQ-FIELD-T/S (`LEAVE_DIAG*` — leave-shows-0 diagnostics removed v3.5.292; T's payload actually confirms the fix, 31 rows ok); EQ-FIELD-V (`400: PGRST204` — my own deliberate smoke test of the new dead-letter Sentry capture on the preview).

**Decided (Royce):**
- Capacity panel design = **Mock B** (demand-scaled chart + roster-first strip), reviewed via live-data artifact before build.
- Merge both PRs + fix Sentry errors.

**Deferred — the "bridge pipeline into resources" vision (steelman, Royce liked it; staged so no rewrite):**
- [ ] **Pipeline shadow — demand BEFORE it's won** (highest-leverage next step). Every live tender casts a probability-weighted demand shadow (stage→default win %, or a slider) rendered as a lighter band behind firm demand. Turns the panel from status display into a forward instrument: "if we win 2 of these 4 tenders, do we break?" Small schema touch (probability per tender or per stage); chart gains a second band. Brief was offered but not yet built. _(added 2026-07-11)_
- [ ] **Supply is a curve too, not a flat HC line.** Draw committed-vs-available supply from assignment end-dates: when a job rolls off in week N, those people return to the bench in week N. Two curves (supply stepping down, demand stepping up); the crossover is the hire-or-redeploy trigger. Roster already holds the end dates; nobody reads them forward. Would also dissolve the "which 90 is headcount?" question below. _(added 2026-07-11)_
- [ ] **Demand in roles, not headcount** — "3 electricians + 1 leading hand w/ EWP" vs "4 workers"; match on role + cert, flag "12 free but only 2 licenced". Field already holds roles/licences on people; labour curve needs a role column. Also enables worker-facing "your next 8 weeks" view (recognition angle — visibility forward, not just cost backward). _(added 2026-07-11)_
- [ ] **What-if drag** — drag a start date, watch the curve re-flow ("client wants to push St George 3 weeks — do we still clear the Equinix peak?"). Client-side re-render with a ghost overlay; all inputs already present. _(added 2026-07-11)_
- [ ] **"Which 90 is headcount?" decision** — HC = every unarchived person in People, incl. office/PM staff never rostered to a job, so BENCH and "N free" overstate deployable capacity. Options: keep as-is, filter by role/category, or use "deployed in the last N weeks" as the denominator. (Largely resolved by the supply-curve item above if that ships.) _(added 2026-07-11)_
- [x] **Empty "Pipeline" nav header in employee view** (spawned as background task `task_dcd8df1b`) — the sidebar section wrapper `#nav-section-pipeline` isn't role-gated but all 3 of its items (Pipeline/Resources/Accounts) are `edit-only` (`.nav-item.edit-only` → `display:none` without `body.manager-mode`, base.css:210-211). An employee-view Core login never gets `manager-mode`, so the items hide and only the orphaned "PIPELINE" label shows. **FIXED + LIVE (v3.5.299, PR #455, 2026-07-11):** took the group-level `edit-only` route — marked `#nav-section-pipeline` `.edit-only` + added `.nav-section.edit-only { display:none }` / `.manager-mode .nav-section.edit-only { display:flex }` in base.css, mirroring the existing `.nav-item.edit-only` pattern. Whole group now hides for employees, shows for managers; apprentice-branch inline `display:none` still wins. Other groups verified unaffected (Operations/Manage/Testing keep non-edit-only items; Safety has its own toggle). Prod curl confirmed v3.5.299 serving. _(added 2026-07-11, done 2026-07-11)_

## ⏩ SKS NSW Comms — session 2026-07-11/12 (replace the Excel labour planner)

**The whole NSW Comms module (`core.eq.solutions/sks/comms`) was built out to replace the team's Excel labour planner — all merged to eq-shell main + live.**

(full build history recorded in `eq/changelog/eq-shell.md` "2026-07-16" NSW Comms module entry)

**Deferred:**
- [ ] **Reach the crew — the last mile is off.** Only 6 of 11 comms techs can log in; 0 of 11 get any roster notification (all 11 have a phone). Until this is wired, a booking never reaches the tech automatically. Fix = logins for the 5 + roster SMS. Chip spawned. _(added 2026-07-12)_
- [ ] **NSW Comms per-user toggle** — surface Comms in the invite/user "workspace apps" list so a manager can show it only to people who need it (declutter everyone else's dashboard). Trigger (Royce): once the team is actually using Comms. Chip spawned. _(added 2026-07-12)_
- [ ] **Materials pre-fill — staged, reversible, ready.** The planner has materials status on 84 jobs; the backfill skipped the column (0 filled). Fix dry-run clean: 83 rows, maps cleanly to the dropdown, all targets blank. Blocked at the write (question ≠ consent); run on Royce's go. Chip spawned. _(added 2026-07-12)_
- [ ] **Crew pre-fill — planner knows a lead on 76 jobs, tool shows 1.** Filling means seeding the Field roster from the planner's lead+dates = the first real (stale-date) roster write; do as a curated pass with the real Monday, not an auto-backfill. _(added 2026-07-12)_
- [ ] **Parked planner features** — Gantt (jobs across time) and the Dashboard's hours-by-manager / hours-by-tech analytics not built; NV1-per-person parked (below). Pull back in only if the team asks. _(added 2026-07-12)_
- [ ] **Run one real Monday through it** — book real crews on real jobs, confirm they hit the Field roster. The single step that turns "built" into "used"; it's a trial run, not code. _(added 2026-07-12)_
- [ ] **NV1-as-a-licence PARKED (Royce)** — model NV1 clearance as a Field licence for a real 1-per-3 supervision meter (source: Melbourne MS TECHS sheet). Sound but "polish, not site value yet". _(added 2026-07-12)_
- [ ] **Melbourne import is add-only** — skips any job already in comms, never updates/enriches an existing one. A future "enrich existing" pass if updates from Melbourne should flow. _(added 2026-07-12)_
- [ ] **Cutover** — two parallel Mondays (Excel + core), then the spreadsheet goes read-only; Royce calls it. _(added 2026-07-12)_

**Notes / gotchas:**
- **I caused + fixed a ~15-min comms outage.** During a shared-worktree wipe recovery, `git add`-ing a wiped `comms-jobs.ts` staged its *deletion* → #764 shipped the core comms API function deleted from main; CI passed (a missing Netlify function isn't a compile error) and it deployed. Caught by #765's merge conflict, restored + live-verified (`curl …/comms-jobs` = 401 not 404). Lesson: after any wipe, never `git add <path>` without confirming the file is present + carries your changes.
- Shared eq-shell worktree got wiped (1271 tracked files + node_modules .bin) mid-session by a concurrent process — recovered.

## Untouched substrate items

(Separate from EQ Quotes — preserve)

- [ ] Bring apprentice module from demo to SKS Labour prod
- [ ] Scale EQ Field App for Melbourne office demo
- [ ] R2 backup audit/download from Beelink desktop
- [ ] One-on-one catch-up sessions with 8 key staff — 7 Role Step-Up Charters drafted 2026-07-05 (Collin, Rhys, William, Simon, Matt, David, Luke) as supporting artefacts for these conversations
- [ ] Comms portfolio growth under Royce

## ⏩ SKS NSW Comms — session 2026-07-12 (editable grid + readability)

(recorded in `eq/changelog/eq-shell.md` "2026-07-12" PR #785/#788)

**Notes / gotchas:**
- The first merge was blocked by a **security-gate false alarm** — a safe Field "removed people" view was mis-flagged as an exposed table. Verified it's actually tenant-isolated (a security_invoker view, writes tenant-guarded), cleared the flag; this also unblocked every other eq-shell PR. Folding that view's setup into a proper migration is running as its own background task.
- Shared-checkout race again — the root repo kept getting switched onto other sessions' branches; built in fresh isolated worktrees each time.

**Deferred:**
- [ ] **Excel full-width mode (optional)** — if wrapping isn't enough, switch the table to natural-width columns + sideways scroll like a real spreadsheet. One-flag change; Royce trying the wrap version first. _(added 2026-07-12)_

## ⏩ SKS Plant & Equipment — session 2026-07-13 (calibrated instruments wiped by a manual asset-register wipe → restored + guarded; 2FA grace re-checked)

**Trigger:** Royce reported the plant & equipment items missing — suspected EQ Service had mistaken them for generic assets.

**Root cause (verified live, ehow `app_data.assets` + `app_data.audit_log`):** a MANUAL service-role delete-all+reload of the whole SKS asset register at 2026-07-12 09:53 wiped every row not in the incoming feed — all **16 `plant_equipment` rows** (SKS's own calibrated test instruments: Fluke/Megger/Metrel/Kyoritsu/UNI-T meters, 2 torque wrenches, micro-ohmmeter) plus **817 customer asset rows**. The Plant & Equipment page filters `asset_type='plant_equipment'` server-side, so it went empty. NOT the eq-solves-service importer (which writes its own `service.assets`, never canonical `app_data.assets`) — the delete-all was a manual SQL/service-role run whose service-role JWT sailed past the older 0154 delete guard.

(restore + DB guard recorded in `eq/changelog/eq-shell.md` "2026-07-13" PR #790; 2FA grace re-check found no change needed)

**Decided (Royce):**
- Restore only the 16 instruments; the **817 deleted customer rows = "not required, all good"** — closed, no restore.
- P&E is **separate from EQ Service**; no importer hunt (the runs were manual).
- Approved dispatching 0176 to both tenant planes.
- 2FA enrolment grace stays at 14 days — no change.

**Deferred:**
- [ ] **2FA grace window is a one-line change** (`TOTP_GRACE_MS` in `totp.ts`) if Royce ever wants it shortened or dropped to force enrolment on first sign-in — auth-path change, left until he says go. Not requested now. _(added 2026-07-13)_

## ⏩ SKS Labour hire — session 2026-07-13 (weekly-cost redesign + modal focus fix + 4-provider rate-card audit)

**Trigger:** Royce reviewing `/sks/ops/labour-hire-rates` — wanted the weekly-cost view simpler/grouped, a per-week redundancy charge, the Add-rate modal fixed (kept dropping focus per keystroke), a formula-Excel to check the maths, and a full audit of the labour-hire rate-card PDFs.

(weekly-cost redesign, modal focus fix, and the 4-provider rate-card audit all recorded in `eq/changelog/eq-shell.md` "2026-07-13" PR #804/#805/#807/#808)

**Decided (Royce):**
- Add the redundancy; tidy Cranfield (relabel + delete dupes); retire Core Talent's stale Electrician role — "complete all 3."
- **Ignore Atom's night-shift +25% loading** for now (situational %, not in the standard-week model).
- Excel is the cross-check; the **eq-shell rates page is the ultimate source of truth**.

**Notes / gotchas:**
- The auto-mode classifier **allowed the redundancy INSERT** but **denied the Cranfield UPDATE/DELETE and Electrician retire** until Royce explicitly named/approved the specific `rate_id`s — modifying pre-existing shared rows needs named-specifics, a fresh INSERT doesn't.
- `is_current` (view) = `active AND effective_from<=today AND (effective_to IS NULL OR effective_to>=today)` — retire a current row by setting `effective_to` to a past date.

**Deferred:**
- [ ] **Migration 0177 still un-dispatched** — adds `week` to the rate `unit` CHECK. Until dispatched via the One Pipe: the redundancy sits on `unit='each'` (correct $ value, flat weekly) and the **"week" option in the Add-rate dropdown 400s if picked**. Dispatch when convenient, then flip the redundancy `each`→`week` (cosmetic). _(added 2026-07-13)_
- [ ] **Uploaded rate-card PDFs are not stored** (parse-and-discard) — offered a private file-store + per-rate download link so cards are retained going forward; not built, Royce hasn't taken it up. _(added 2026-07-13)_
- [ ] **Cranfield current rates (eff 2026-07-01) have no July source doc** — amounts verified against the 29-Jan card (identical), but the 1-Jul effective date isn't doc-backed. Cosmetic/low-pri. _(added 2026-07-13)_

## ⏩ SKS Field — session 2026-07-15 (timesheet total double-count + invisible mobile roster header + Pipeline/Resources hidden)

**Trigger:** Royce reported Jack Trusler's Timesheets row total didn't add up (43h against visible 8+10+9 cells), then separately flagged the mobile Weekly Roster header text was invisible, then asked to hide Pipeline/Resources from nav entirely.

(v3.10.97/98 fixes recorded in `sks/changelog/labour.md` "2026-07-15")

**Decided (Royce):**
- Timesheet fix = code fix (leave-aware total) **and** clean the one stale DB row, not just one or the other.
- Pipeline/Resources hide = from **all** managers, not a role-restricted subset.
- Explicitly waived PR review to merge #66 and #67 (each named individually — the auto-mode classifier requires "merge without review" stated fresh per PR, a standing waiver on one PR does not carry to the next).
- Explicitly named the force-push of `claude/jack-trusler-table-math-223dde` to resolve a squash-merge orphaning conflict on PR #67's second commit (classifier requires the branch named, not just "push it").
- **Blocked, unresolved:** the very first push (before any merge ask) was denied by the auto-mode classifier because the commit message + CHANGELOG.md named Jack Trusler alongside his specific leave/hours discrepancy, going into `eq-solutions/sks-nsw-labour` — **classifier-confirmed this repo is PUBLIC**. Offered to anonymize; Royce said push it as-is ("someone's name in a changelog isn't the end of the world") — pushed only after that explicit instruction.

**Deferred:**
- [ ] **EQ Field audit for the same invisible-header CSS pattern** — spawned as background task `task_19ab53ac`, Royce started it as a separate session; running independently, not yet reported back as of this session's close. A scoped grep of eq-field's `styles/mobile.css` during triage found no exact `th.name-col`/`th.center` selector match (EQ Field's mobile Roster likely renders differently, card-based), but EQ Field's `base.css:362` has the identical root-cause `thead tr { color: white }` rule, so any other table page there with a sticky/mobile header override is still at risk under different class names. _(added 2026-07-15)_
- [ ] **`eq-solutions/sks-nsw-labour` is a PUBLIC repo** — worth a decision from Royce on whether that's intended long-term (given it holds live worker names, leave status, and operational data in commit history/CHANGELOG once anyone writes it there) or whether it should be flipped private. Not previously documented in this substrate as a known fact. _(added 2026-07-15)_

## ⏩ EQ Cards — session 2026-07-16 (SKS credential requirements — Photo ID added as soft requirement)

**Trigger:** Royce asked what EQ Cards' minimum tenant requirements are for SKS, then asked whether "form of ID" could be added as a minimum requirement alongside White Card.

(recorded in `eq/changelog/eq-cards.md` "2026-07-16")

**Deferred:**
- [ ] **EQ Solutions' own org (`eq`) has zero credential requirements configured** — worth a call on whether EQ Solutions should require White Card/Photo ID too, or stay requirement-free deliberately (it's the seed-demo org). _(added 2026-07-16)_

## ⏩ SKS Field — session 2026-07-16 (Equinix SY9 duplicate customer — verified already clean)

**Trigger:** Royce flagged a possible duplicate customer for the Equinix SY9 site on ehow and asked which company name was correct.

**Completed:**
- [x] **Confirmed live: "Equinix Hyperscale 2 (SY9) Pty Limited" (`d79ee06f-…`) is the correct/active SY9 customer** (Royce confirmed) — linked to the real SY9 site (499 assets, 10 contract scopes, 2 quotes). The older duplicate "Equinix Hyperscale" (`a57bf144-…`, created 2026-05-23) and its linked site (`95cdc37d-…`) were both already `active=false` with zero dependent rows (quotes/contacts/scopes/jobs) — cleanup had already happened previously. `eq_merge_customers` RPC not needed, no DML required.
- [x] Logged the resolved name + duplicate-customer history to memory (`project_equinix_entity_map.md`) so future Coupa/PO matching doesn't second-guess "Equinix Hyperscale" (no suffix) as live.

(full investigation + fix recorded in `eq/changelog/field.md` "2026-07-19" — DB-only grant restore PR #498, CI guard PR #500)
