---
title: EQ Field — Pending Actions
owner: Royce Milmlow
last_updated: 2026-09-05
scope: EQ Field engineering backlog, split out of eq/pending.md (2026-08-17) so a session working in this repo isn't wading through the other 8 repos' items too. Same conventions as before: "- [ ]" open, "- [x]" done (rotated out nightly by scripts/rotate_pending.py), "- [~]" in progress.
read_priority: critical
status: live
---

# EQ Field — Pending

Split out of `eq/pending.md` (2026-08-17) — see `eq/pending.md` for why. SKS items live in `sks/pending.md`. OPS items (entities, tax, infra) in `ops/pending.md`.

---

## eq-field: Multi-job Timesheets display + Cihan Alakuzu's inflated hours — 5 PRs merged, live, root causes closed (2026-09-05)
*Royce, from two screenshots: a multi-job day cell read as one impossible combined shift, and Cihan Alakuzu's timesheet was back to 81.5h for one week — the same failure shape as the v3.5.664/669 duplicate-hours incidents, but investigated fresh rather than assumed to be a recurrence. It wasn't: the unique constraint from v3.5.669 held throughout.*

- [x] **Multi-job cell display fixed, twice.** First pass (PR #923, v3.5.680) showed each job's own hours inline instead of one combined total — still didn't fit the actual grid width and truncated the second job off (Royce, a second screenshot: "27968 (8h) · 281…"). Second pass (PR #925, v3.5.682) stacks each job on its own line instead, closing the truncation for real — 10 new regression tests including the exact reported case.
- [x] **Root cause of the 81.5h: two independent mechanisms, both closed.** (1) A stale-tab bug — Fill Week's "which jobs already exist" check read a snapshot that's never proactively refreshed, so a tab open across another write would show a day as blank rather than already-logged. Fixed in Fill Week (PR #923) and ported to Copy Last Week (PR #926, v3.5.683) after `/decide` found porting the fix was cheaper than Royce's first instinct (temporarily removing Copy Last Week) and closed the gap instead of avoiding it. (2) "Prefill from roster" defaulted unconfirmed hours to a fake-looking 8h, indistinguishable from a real confirmed day — now leaves hours unset until someone actually confirms them (PR #924, v3.5.681).
- [x] **A day's *combined* hours across every job on it were never checked anywhere** — only individual per-job values, and only on the legacy fallback table. New `_tsOverloadedDays` (PR #923) ports that same class of guard (>12h warning) to the current editor, checked against the combined total.
- [x] **Cihan Alakuzu's live data cleaned up, Royce's explicit approval:** the 5 spurious `job=27862` rows (the auto-default) deleted, the 5 hand-entered `job=27682` rows kept — 49.5h, confirmed live. Maylin Ung's existing total was separately confirmed correct and left untouched.
- [x] **"Who did this" traced as far as possible without a database change:** the app-level audit log has no real actor identity for Timesheets (`who: "system"` always) — traced instead via PostHog (`timesheet_saved` event + `posthog.identify()`), found the exact session (Mobile Safari/iOS, Sydney, timestamps matching to the second) and positively ruled out three other people active in the same window. That session's own `posthog.identify()` never fired despite being authenticated — flagged, not investigated further.
- [x] **The real gap behind "who did this" closed properly** (PR #927, migration, no version bump): `app_data.eq__guard_timesheet_status` already resolved the caller's real identity on every write, it just never persisted past `approved_by_user_id`. Now stamps `created_by`/`updated_by` too. Applied live and verified with real writes in a rolled-back transaction before the PR was even opened.
- [ ] **Historical rows stay permanently unattributed** — the new stamping is forward-only from 2026-09-05; there's no way to backfill who wrote a pre-existing row, including Cihan's own cleaned-up ones. _(added 2026-09-05)_
- [ ] **`created_by`/`updated_by` are raw UUIDs with no display-name resolution yet** — a real follow-up, mirroring the `staffUserIdToName` map PR #921 built for `approved_by_user_id`. Not built this session. _(added 2026-09-05)_
- [ ] **The unidentified PostHog session's missing `posthog.identify()` call** — a real, separate analytics gap (every other session active in the same window was correctly identified). Not investigated further; worth a look if "who did this" comes up again and the new DB attribution alone isn't enough context (e.g. device/location matters). _(added 2026-09-05)_
- [ ] **Not click-tested live by a person** — same standing Core-only sandbox limitation as every entry in this file. The PR #927 migration was instead verified with real transactional writes against the live function, which exercises the actual trigger code path more precisely than a UI click could have (proving the "different actor, no status change" case in isolation). _(added 2026-09-05)_

**Notes:**
- Full technical detail: `eq/changelog/eq-field.md` (5× 2026-09-05 entries, PR #923-927) and `sessions/2026-09-05.md`.

---

---

## eq-field: Timesheet "who approved this" was blank for every SKS approval — FIXED, merged, live (2026-09-05)
*Royce, from a screenshot of Core's SKS Timesheets view: the "✓ Approved" button gave no indication of who had approved it. Investigated before building — the plumbing (approval data, a name-resolution helper, an existing initials-chip UI pattern) was already fully built; it just didn't work.*

- [x] **Root cause, verified live against ehow, not assumed:** `app_data.timesheets.approved_by_user_id` is stamped by a DB trigger from the approving manager's Shell/Core login identity (`app_data.staff.user_id`) — the client was resolving it as if it were `staff_id`, a different id space that can never match. Confirmed: 100% of 103 currently-approved SKS timesheets had real, correct attribution the app just couldn't read back (Royce Milmlow, Ian Marston, Simon Bramall, Jack Cluff — all 4 real, current people).
- [x] **Fix is entirely client-side, no database change:** added a `user_id -> name` lookup alongside the existing `staff_id -> name` one, and pointed the read side at it. Also removed a dead write-side guess that the database was silently discarding anyway, which had been firing a false "not linked" warning at supervisors.
- [x] **The Approved button on desktop now shows the approver's initials directly** (e.g. "✓ RM"), instead of only a tooltip that, until this fix, was blank anyway.
- [x] eq-field [PR #921](https://github.com/eq-solutions/eq-field/pull/921) (v3.5.678 — renumbered from v3.5.677 after a same-day rebase collision with PR #920), merged, confirmed live (`field.eq.solutions/sw.js` shows v3.5.678).
- [x] **Checked leave requests for the identical bug before assuming it applied — it doesn't.** `app_data.leave_requests.approver_id` is already correctly resolved (verified live: all populated rows show the real approver's name). **Correction, same day:** the 30 of 47 approved leave requests with a blank approver were first (wrongly) attributed to the emailed magic-link approval flow, before Royce pointed out a screenshot showing populated approvers and it was checked properly — 29 of the 30 carry `imported_from: nspb-phase3-2026-07-05`, a one-time bulk import of historical leave from sks-nsw-labour (matching Royce's own explanation directly: "we manually moved leave from sks-nsw-labour"), and the last 1 predates the trigger that stamps `approver_id` even existing. Zero are actually caused by a live magic-link approval losing identity. **Royce's call stands, now on the correct basis: leave it as-is, no code change** — this is old imported data, not a live gap.
- [ ] **Not click-tested live by a person** — same standing Core-only sandbox limitation as every entry in this file. Verified instead against real production data (the live query results above), which is a stronger check for this specific bug than a single manual click would have been. _(added 2026-09-05)_

**Notes:**
- Full technical detail: `eq/changelog/eq-field.md` (2026-09-05 entry) and `sessions/2026-09-05.md`.

---

## eq-field: CSP still allow-listed the deleted ktmj Supabase project (SEC-53 eq-field half) — FIXED, merged, live (2026-09-04)

- [ ] **`supabase/functions/supervisor-digest/README.md` still points deploy/curl instructions at the deleted project** — docs-only fix, its own task chip. _(added 2026-09-04)_

---

## eq-field: Timesheets + Roster canonical write paths — both closed against silent duplication — FIXED, merged, live (2026-09-04)
*Direct continuation of the same day's Timesheets duplicate-hours work (see the 2026-09-04 entry further down). Cihan Alakuzu and Maylin Ung showed wildly inflated hours again, 25 minutes after that fix (PR #906) had already shipped — this time from completely normal single-cell editing, not a bulk-fill loop.*

- [x] **Timesheets: root-caused to a deeper, previously-unproven mechanism — the write path itself wasn't idempotent.** `_sbTimesheetsCanon` replaced a person's whole week via a DELETE then a separate INSERT, two non-atomic requests. A slow response that the app's own write-queue retries fires an independent copy of that same pair; if the original also eventually lands, both inserts survive. Fix: upsert each day/job row via `ON CONFLICT (staff_id, date, task)` instead, deleting only rows a save is actually clearing. New unique constraint added live to both `ehowgjardagevnrluult` (SKS) and `zaapmfdkgedqupfjtchl` (eq) — zero pre-existing violations on either before applying. Cihan's and Maylin's new duplicates cleaned up directly (explicit approval), reconstructed to their real totals: Maylin 46.5h, Cihan 81.5h. eq-field [PR #911](https://github.com/eq-solutions/eq-field/pull/911) (v3.5.669), merged, confirmed live.
- [x] **Roster: checked for the identical risk rather than assumed — asked directly ("fix roster's write path too").** `_sbRosterCanon` (same file, `schedule` table) has the textually identical delete-then-insert shape. Live check found the risk was NOT symmetric: SKS's database already carried a real unique index on `schedule_entries(staff_id, date)` (added independently of this work) — a racing duplicate there was already failing loudly (a unique-violation error) instead of silently duplicating, a reliability gap rather than a data-integrity one. The eq tenant's database had no such index at all and was genuinely exposed to the same silent-duplication risk timesheets had. Same upsert fix applied; new migration makes the matching index live on the eq tenant too (no-op on SKS, which already had it). eq-field [PR #914](https://github.com/eq-solutions/eq-field/pull/914) (v3.5.672), merged, confirmed live.
- [x] **Confirmed Timesheets and Roster are the only two canonical write paths with this delete-then-insert shape in the codebase** — `leave_requests` has no equivalent dispatch (grepped `supabase.js`'s own dispatch table). Both real instances of this bug class are now closed.
- [x] **4 new regression tests total** (2 per fix, split across `tests/timesheets-canon-write.test.js` and `tests/supabase-canon-write.test.js`): an identical save sent twice must leave exactly one row, not two; clearing one day in a save that still carries another day's existing value must only remove the cleared day's row. Both existing test files' mock `fetch` had to be upgraded to actually enforce the new uniqueness first, or neither could prove anything about the fix.
- [ ] **Not click-tested live by a person** — same standing Core-only sandbox limitation as every entry in this file. _(added 2026-09-04)_

**Notes:**
- The exact client-side trigger (a write-queue retry racing the delete-then-insert) is the most plausible mechanism given the code and this app's own already-documented network flakiness (`EQ-FIELD-19`/`EQ-FIELD-16`), but wasn't directly observed in a captured retry event for the two people affected — said plainly rather than overclaimed. The fix doesn't depend on that theory being exactly right: upserting on a real unique constraint closes the whole class of non-idempotency regardless of what specifically triggers a duplicated request.
- Full technical detail: `eq/changelog/eq-field.md` (2026-09-04 entries) and `sessions/2026-09-04.md`.

---

## eq-field: supervisors now see every crew's Timesheets/Leave by default, not just their own — FIXED, merged, live (2026-09-04)
*Royce, live: David Boyd (Supervisor/Leading Hand, member of "Amazon Syd 53" + "Vans" only) opened Timesheets and saw several people on other crews (CT Team, Equinix) render as empty "+Add" cells. Verified against ehow directly before touching anything — their hours were fully submitted the whole time (Dylan Lieu, Jessica Robinson, Marcus De La Fuente, Terry Su, Tara Demamiel all fully entered), just excluded from David's own crew-scoped read.*

- [x] **Confirmed not a bug — v1.7's crew-scoping model (2026-07-22) working exactly as designed.** `field.view_all_crews` was manager-only; a supervisor's Timesheets/Leave reads are filtered (`crewFilterFragment`, `permissions.js`) to just the crews they run/belong to. David's crews don't include CT Team or Equinix, so those people's real, submitted hours were silently excluded from his fetch entirely — rendering as indistinguishable-from-"not done yet" empty cells.
- [x] **Royce's call this session, reversing that 2026-07-22 default:** "supervisors need to be able to see all employees and filter by teams — our teams change dynamically, it's easier if they can see everyone." `permission-matrix.js` v2.9 adds `field.view_all_crews` to the `supervisor` role (was manager-only). No other logic changed — the existing manager-tier code path (unscoped fetch, team pills narrow the *display*) now applies to supervisors too. Per-person Shell overrides can still narrow an individual supervisor back down if ever needed.
- [x] **`tests/crew-scoping.test.js` reworked, not weakened** — its ~34 existing tests all exercise the crew-scoping *algorithm* itself (team unions, fail-open, the pill override), which is unchanged; `reset()` now strips the new grant back out of the loaded matrix by default so those tests keep proving the algorithm works correctly for a supervisor who doesn't hold it (still reachable via a Shell override). 2 new tests confirm the grant itself against the real, unmodified matrix. 36/36 passing.
- [x] eq-field [PR #910](https://github.com/eq-solutions/eq-field/pull/910) (v3.5.668 — renumbered from v3.5.667 on rebase, same collision-heavy day as every other PR below), merged and confirmed live (`field.eq.solutions/sw.js` shows v3.5.668).
- [ ] **Real privacy tradeoff, said plainly, not relitigated:** every SKS employee's timesheet hours AND leave-request details are now visible to every supervisor org-wide, not just their own crew's chain. Royce made the call explicitly, aware of the tradeoff — recorded here so it's on the record, not just in a commit message. _(added 2026-09-04)_
- [ ] **Not click-tested live by a person** — same standing Core-only sandbox limitation as every entry in this file. Worth a real pass: sign in as a supervisor (not a manager) and confirm Timesheets/Leave now show every crew, with the team pills still narrowing correctly. _(added 2026-09-04)_

**Notes:**
- Resolves the crew-scoping question this file itself flagged and deferred on 2026-09-02 (see "approved leave not appearing on Weekly Roster" below) — that entry's "if the person checking isn't a full manager, check crew-scoping" note can no longer explain a missing row for any supervisor going forward.
- Same session also shipped My Schedule's "For Workbench" line (2 entries below) — diagnosing David's Timesheets report is what surfaced the crew-scoping gap in the first place.
- Full technical detail: `eq/changelog/eq-field.md` (2026-09-04 entry) and `sessions/2026-09-04.md`.

---

## eq-field: My Schedule's "For Workbench" line — shows the job number(s) AND hours actually logged in Timesheets, not just the planned roster job — FIXED, merged, live (2026-09-04)
*Royce, from a screenshot: Cameron Tregoning's My Schedule showed no job number for any day, while his Timesheets grid (same week) showed real logged job numbers (28120, and a split day 28101/28165). Investigated before building: confirmed live these are two genuinely separate fields — My Schedule's job line was always the PLANNED job (a roster pin or a site's linked Project, `resolveCellJob()`), which most sites don't have configured; Timesheets' job number is freely typed at time of logging hours, with no link back to the roster at all.*

- [x] **First pass (Royce's explicit ask): show Timesheets' actual logged job number(s) on My Schedule too, labelled "For Workbench"** so a worker can see what to key into the external payroll system without opening Timesheets. Additive — the existing planned-job line is untouched, a day with nothing logged shows nothing extra. New `loggedJobsForDisplay()` helper (`roster.js`) parses the same packed `"JOB:hrs|JOB:hrs"` grammar `timesheets.js` itself uses. eq-field [PR #903](https://github.com/eq-solutions/eq-field/pull/903) (v3.5.661), merged, live.
- [x] **Second pass, same day (Royce: "We need to show the hours aswell for each day"):** a split day showed both job codes but not which hours went to which — still needed a trip into Timesheets to check. `loggedJobsForDisplay()` extended to also carry hours per job (single bare job reads the day-total field; a split day carries each segment's own hours inline, matching `timesheets.js`'s own parse exactly). Line now reads e.g. "🧾 For Workbench: 28101 (4h) · 28165 (4h)". eq-field [PR #907](https://github.com/eq-solutions/eq-field/pull/907) (v3.5.665 — renumbered from v3.5.663 on rebase), merged, live.
- [x] **8 new tests** (`tests/schedule-workbench-job.test.js`) cover single-job, half-hour values, split days, the same-job-typed-twice-sums-its-hours edge case, and empty/malformed-segment cases.
- [ ] **Known, deliberate limitation:** this line mirrors *whatever the worker already typed* into Timesheets — a mistyped job number or wrong hours there gets repeated back here too. It's a display mirror, not a validator. _(added 2026-09-04)_
- [ ] **Not click-tested live by a person** — same standing Core-only sandbox limitation as every entry in this file. Worth a real pass: open My Schedule for someone with a logged timesheet job (or a split day) and confirm the line renders correctly. _(added 2026-09-04)_

**Notes:**
- Diagnosing this feature request against a real user (David Boyd, Timesheets) is what led to the crew-scoping fix above, in the same session.
- Full technical detail: `eq/changelog/eq-field.md` (2026-09-04 entries) and `sessions/2026-09-04.md`.

---

## eq-field: file-size ratchet convergence — roster.js + leave.js decomposed, FIXED, merged, live; 4 files still near-ceiling (2026-09-04)

- [ ] **4 of the original 6 tracked files are still near-ceiling, untouched this session** (task scope was the tightest 1-2 files): `sks-pipeline.js` 1,779/1,800 (21 headroom), `sks-pipeline-resource.js` 2,062/2,100 (38), `tender-pipeline.js` 2,108/2,150 (42, deliberately deferred separately per Royce 2026-07-30), `timesheets.js` 2,527/2,550 (23). Same decision as before applies to these: keep ratcheting as it comes up, or schedule their own decomposition pass. _(added 2026-09-04, **correction 2026-09-05**: `timesheets.js` count is now stale — two independent same-day PRs (#920, #921) both added a few lines and collided on rebase, pushing it to 2,554; ceiling bumped to 2,600, 46 headroom left, not 23)_
- [ ] **New finding, not in the original count:** `apprentices.js` is also at 1,739/1,750 (11 lines headroom) — tied with leave.js's pre-decomposition number, discovered only because this session re-verified every entry fresh rather than trusting the original 6-file list. _(added 2026-09-04)_
- [ ] **Not click-tested live by a person on either PR** — standing Core-only sandbox limitation, same as every other entry in this file. Worth a real pass: submit a leave request end-to-end (both range and individual-day modes), and open My Schedule to confirm the day-card layout (site/address/job number/Workbench line/site contacts/coworkers/map link) is unchanged. _(added 2026-09-04)_

**Notes:**
- Not a new problem caused originally — the convergence is the cumulative effect of the existing, working ratchet convention across many sessions.
- The decomposition session caught its own near-miss: an early read of `eslint.config.js`/line counts came from a shared-root checkout ~38 commits behind `origin/main` (a stale, orphaned branch left over from unrelated prior work in that same shared folder) and briefly suggested roster.js was no longer tight — re-verified against a fresh worktree before acting, so no wrong-file work happened, but worth remembering this exact failure mode recurs across sessions.
- Royce merged both explicitly ("merge #912 and #913"). #913 needed a rebase after #912 landed first (shared version-stamp files) — resolved, re-verified, re-merged. Confirmed live: `field.eq.solutions/sw.js` shows v3.5.671 (the later of the two, built on top of the first).
- Full technical detail: `eq/changelog/eq-field.md` (2026-09-04 entries) and `sessions/2026-09-04.md` (session (g)).

---

## eq-field: Timesheets TAFE/Leave autofill + dark-cell explainer — FIXED, merged, live (2026-09-04)
*Same session as the duplicate-hours fix below. Royce, follow-up: "look at the dark timesheets issue" (revisit — the dark cell itself was already correct behaviour, just unexplained) and "can you see whats built between tafe/holiday and timesheets — it would be good to autofill for dates we know the person is at tafe or on leave (make it so it can still be changed if needed)".*

- [x] **Dark "continues a job" cell now has a tooltip** naming the job it's continuing — no behaviour change, just an explanation where there was none.
- [x] **TAFE/Leave days now autofill a real, editable timesheet entry, not just a virtual total.** What existed already: `dayStatus()` (`timesheets-rules.js`) knew about a nominated TAFE day or approved leave and silently credited 8h to the on-screen weekly total. What was missing: nothing was ever written to the actual row, so a CSV/By Job export showed nothing for that day, and the desktop grid rendered the day as a fully locked chip with no way to override it. Fix, one-tap (Royce's pick over fully-automatic via `AskUserQuestion`, matching every other fill action in this app): "Prefill from Roster" and "Prefill my week" now also fill TAFE/approved-leave days with a real 8h entry using the same label the chip already shows, never overwriting a day that already has real data. The spans grid's TAFE/Leave chips are no longer fully locked — a supervisor can click one to open the same day editor as any other cell and correct a wrongly-flagged day.
- [x] **Found and fixed in passing: the "TAFE Holidays doesn't protect Timesheets" gap already logged further down this file (2026-09-02 entry) was real** — a configured TAFE Holidays break wasn't actually being checked by `dayStatus()` despite a comment in `tafe.js` claiming it was. During a declared holiday week, an apprentice's nominated day now correctly reads as workable. Matters more now that this day can produce a real written row, not just a display total.
- [x] **3 new automated tests** lock in the holiday-override behaviour and confirm an explicitly roster-typed TAFE code (a human decision) is untouched by it.
- [x] eq-field [PR #909](https://github.com/eq-solutions/eq-field/pull/909) (v3.5.667 — renumbered from v3.5.666 on rebase, see Notes), merged and confirmed live (`field.eq.solutions/sw.js` shows v3.5.667).
- [ ] **New export visibility, intended but worth knowing:** TAFE/leave days that were previously invisible to every export now show up in the "By Job" export, mixed in with real job numbers under a code ("TAFE"/"A/L") that isn't in the job-numbers table. _(added 2026-09-04)_
- [ ] **UI-glue code has no automated browser-level coverage** — the clickable-chip wiring and the two prefill functions' new branches are verified by manual trace against the diff plus the full suite passing, not by an executed browser test (standing Core-only sandbox limitation prevents one). The rules-layer fix (`dayStatus()`) does have real test coverage. _(added 2026-09-04)_
- [ ] **Not click-tested live by a person** — same standing Core-only sandbox limitation as every entry in this file. _(added 2026-09-04)_

**Notes:**
- Rebased once to merge: `main` had moved to v3.5.666 via a concurrent PR, [#908](https://github.com/eq-solutions/eq-field/pull/908) (the Lock Week/Request Unlock fix, section below), which this branch's own v3.5.666 collided with. `scripts/timesheets.js` auto-merged cleanly (different functions touched); `docs/reflection-log.md`, `eslint.config.js`'s ratchet comment, and `index.html`'s CHANGES banner all conflicted for real on the shared append-point, resolved by keeping both PRs' entries. `app-state.js`/`sw.js`/index.html's own `<script>` tags all silently kept the stale `3.5.666` literal post-rebase with no conflict flagged (same trap documented on every PR today) — bumped by hand. Combined with #908's own additions, `timesheets.js` crossed its ratchet ceiling a second time today (2500 → 2550, actual 2,527 lines) — see the file-size entry above.
- Full technical detail: `eq/changelog/eq-field.md` (2026-09-04 entries) and `sessions/2026-09-04.md`.

---

## eq-field: Timesheets week-lock trio — confirm()/prompt() silently no-op for every real SKS supervisor through Core — FIXED, merged, live (2026-09-04)
*Spun off from PR #904 (Prestart/Toolbox Reopen fix, same day) — that PR's own commit found and correctly flagged `unlockCurrentWeek()` as the same bug class in a different feature, deliberately left out of scope. This session picked that up, fixed it, then found two more live instances in the same file while there and spun those off too.*

- [x] **`unlockCurrentWeek()` called raw `window.confirm()`, which silently returns `false` with no dialog inside eq-shell's `FieldIframe.tsx` sandbox (`allow-modals` genuinely absent — independently re-verified against the live file, not just trusted from PR #904's comment).** SKS is Core-only, so Unlock Week had done nothing at all, silently, for every real supervisor for as long as the button has existed under Core. Fixed by swapping to the file's own already-proven `_tsConfirm()` modal wrapper (used 4x elsewhere) — mechanical swap, same message text. eq-field [PR #905](https://github.com/eq-solutions/eq-field/pull/905) (v3.5.663), merged and confirmed live (`field.eq.solutions/sw.js` shows v3.5.663).
- [x] **Found two more live instances while there, same file: `lockCurrentWeek()` and `requestTsUnlock()`, both still raw `window.prompt()`.** `requestTsUnlock()`'s case was worse than a no-op — a blocked `prompt()` returns `null`, which the existing code already treats identically to the user's own Cancel, so a worker's unlock request silently vanished with zero feedback; `lockCurrentWeek()` silently locked with a blank reason instead of asking. Needed a different shape of fix (text-input modal, not yes/no), so spun off as a separate task rather than folded into #905. Royce started the spawned task in its own session; it built a new `_tsPrompt()` helper (sibling to `_tsConfirm()`, reusing the shared modal's existing `#confirm-reason` textarea — no new markup needed) and switched both functions onto it. eq-field [PR #908](https://github.com/eq-solutions/eq-field/pull/908) (v3.5.666 — rebased twice past concurrent same-day PRs #906/#907), merged and confirmed live (`field.eq.solutions/sw.js` shows v3.5.666, verified by polling rather than assumed instantly live).
- [ ] **Not click-tested live by a person** — same standing Core-only sandbox limitation as every entry in this file. Worth a real pass through Core as a supervisor: Unlock Week on a locked week shows the modal and actually unlocks; Lock Week with and without a typed reason both save correctly; as a non-supervisor, "Request unlock" on a locked week shows the modal and the request (with optional reason) lands in the audit log. _(added 2026-09-04)_

**Notes:**
- Full technical detail: `eq/changelog/eq-field.md` (2026-09-04 entries) and `sessions/2026-09-04.md`.

---

## eq-field: Timesheets duplicate-hours bug + scroll-jump-to-top — FIXED, merged, live (2026-09-04)
*Royce: David Boyd struggling to enter timesheets, Cihan Alakuzu showing 120h for a normal week, and a screenshot asking why one Timesheets day-cell renders darker than its neighbours. All three investigated against live ehow data + the actual render code, not guessed.*

- [x] **Root cause of the 120h: 8 call sites looped `saveTsCell` once per day, each repost carrying the whole growing week — on SKS's canonical write path that compounds into duplicate rows.** Confirmed live: Cihan's job 27862 had 5/4/3/2/1 duplicate rows across Mon–Fri, summing to exactly 120h instead of 40h. Fix: `saveTsCell` split into an in-memory update + a single network flush; new `saveTsCellsBulk()` lets Fill week/Copy last week/DNW/Repeat day/Prefill from roster/CSV import/the +Add job editor's Save+Clear days each hit the network exactly once. eq-field [PR #906](https://github.com/eq-solutions/eq-field/pull/906) (v3.5.664 — renumbered twice, see Notes), merged and confirmed live.
- [x] **Scroll jump fixed at the source** — `renderTimesheets()`'s scroll-preserve was reading/writing the wrong DOM element (`#page-timesheets` itself never scrolls; the real `overflow:auto` element is the child `.table-scroll`), so every full-table rebuild silently reset to the top. One fix covers every caller.
- [x] **Cihan's existing 14 duplicate rows cleaned up on ehow, Royce's explicit approval** — kept one correct 8h/job-27862 row per date, leaving 40h.
- [x] **Thursday-dark question answered: not a bug** — `timesheets-spans.js` deliberately darkens the 2nd+ consecutive day of the same job number to show a multi-day span. No code change.
- [x] **David Boyd's own stored data checked clean** (no duplicates) — most likely explanation is one of two already-fixed Sentry errors (`EQ-FIELD-1C`/`EQ-FIELD-1D`, shipped v3.5.642), not data loss.
- [ ] **Exact DB-level reason the delete-then-insert doesn't self-heal under rapid repeated calls was NOT pinned down.** A clean single-threaded Node repro against the real, unmodified `_sbTimesheetsCanon` write path did not reproduce the duplication when properly sequenced — so this PR closes the confirmed trigger (redundant client-side reposts), not a proven root cause of the underlying mechanism. A table-wide scan found this was the only duplicate anywhere in `app_data.field_timesheets`'s history (consistent with "rapid calls" being the real trigger, not a permanently-broken delete) — but if duplicates ever recur from a single, non-looped save, this is the open thread to pull. _(added 2026-09-04)_
- [ ] **Thursday-dark styling has no tooltip/legend explaining it** — offered to add one; not requested, not built. _(added 2026-09-04)_
- [ ] **Not click-tested live by a person** — same standing Core-only sandbox limitation as every entry in this file. Verified instead via a Node harness against the real production write-path code (`_sbTimesheetsCanon`/`timesheets-adapter.js`, not a reimplementation). Worth a real pass: as a supervisor, open Timesheets for a long list, scroll down, use Fill Week or the +Add job editor's Save on someone mid-list, confirm the view stays put instead of jumping to the top. _(added 2026-09-04)_

**Notes:**
- Rebased twice mid-session chasing a moving `origin/main` — two concurrent same-day PRs (#904 Prestart/Toolbox Reopen, #905 Unlock Week confirm() fix) each independently claimed this branch's version number before it could merge. Renumbered v3.5.662 → 663 → 664; re-verified `app-state.js`/`sw.js` by hand after each rebase since both silently kept the prior literal version string with no conflict flagged (git sees identical text on both sides) — same trap #904's and #905's own entries already documented.
- Full technical detail: `eq/changelog/eq-field.md` (2026-09-04 entry) and `sessions/2026-09-04.md`.

---

## eq-field: supabase.js decomposition — extracted the JWT-carrier — FIXED, merged, live (2026-09-02)
*eq-field PR #898 (v3.5.656, same day) had bumped `scripts/supabase.js`'s file-size ratchet ceiling 1550→1600 to land an unrelated retry fix, explicitly flagging the JWT-carrier as the clean extraction candidate it was deferring. This closes that flag.*

- [x] **`_mintDataJwt`/`_getDataJwt`/`_getDataActorId` + their own state moved verbatim into new file `scripts/supabase-jwt-carrier.js`.** `_actorIdEverSeen`/`_actorDropReported` (the 2026-08-26 Mark Brame audit-attribution flags) stay declared in `supabase.js` exactly where they were, referenced from the new file as a bare cross-file global — same mechanism this codebase already uses everywhere else, deliberately not restructured for zero functional benefit on security-adjacent code. `supabase.js`: 1,549 → 1,479 lines; ceiling kept at 1,600 for real headroom rather than dropped to the 1,500 default. PR #898's own retry fix merged mid-task and was ported into the new file rather than lost. eq-field [PR #899](https://github.com/eq-solutions/eq-field/pull/899) (v3.5.657), merged, confirmed live (`field.eq.solutions/sw.js` shows v3.5.657; Netlify deploy record for the merge commit shows `state: ready`/`published_at` set).
- [x] **`tests/lazy-tab-script-guard.test.js` caught a real bug before it shipped** — the new file initially had no `<script>` tag in `index.html`, so it would never have loaded in a real browser and JWT minting would have silently broken for both tenants. Fixed before merging.
- [x] **Full suite 38/38 green, lint/cache-buster/bundle checks clean.** Not click-tested live — standing Core-only sandbox limitation; no user-visible surface either way (identical runtime behavior by design).

---

## eq-field: Roster/Editor/Schedule could look "wiped" during a slow data load — FIXED, merged, live (2026-09-02)

- [ ] **A visible "couldn't load this week" indicator in the week-nav bar** would close the last gap (today a stuck week just looks calm, with no on-screen hint to reach for the manual Sync button) — deliberately left out of this PR as a smaller follow-up rather than expanding it further. _(added 2026-09-02)_
- [ ] **Not click-tested through the full authenticated UI by a person** — same standing Core-only limitation as every entry in this file, re-confirmed twice more this session (the real deploy preview's demo-tenant PIN gate also dead-ends at "Sign in through Core"). Worth a real pass: on `field.eq.solutions/sks/field` via Core, throttle the network and jump Edit Roster to a week outside today's ±1 window — confirm it renders calmly (no amber flash) and fills in once the fetch lands, on Editor, Roster, and My Schedule. _(added 2026-09-02)_

---

## eq-field: Apprentices Quarterly Review modal was unstyled and wouldn't close — FIXED, merged, live (2026-09-02)
*Royce shared a screenshot of the "+ New Review" form on Phoenix Khatri's profile — a gray-navy wash with raw, unstyled browser-default fields, asking why it looked broken.*

- [x] **Root cause: two CSS classes that don't exist anywhere in the stylesheet** (`modal-box`, `input` instead of the real `.modal`/`.form-input`), live since the feature first shipped (v3.5.168) and carried unchanged through a later file-size split. Second bug in the same function: it opened via a hand-rolled `style.display='flex'` instead of the shared `openModal()`, so `closeModal()` — wired to Cancel and to a successful Save — could never actually close it once opened that way (it only ever removes the `.open` class, never touches inline style). eq-field [PR #887](https://github.com/eq-solutions/eq-field/pull/887) (v3.5.647), merged, confirmed live.
- [x] **Live `quarterly_reviews` on ehow checked for duplicate saves the stuck-modal bug might have caused** — none found. Table sat at 0 rows both before and after the fix (nobody had ever successfully saved one).
- [ ] **Not click-tested live by a person** — same standing Core-only sandbox limitation as every entry in this file. Worth a real pass: open Apprentices → any apprentice → Reviews → "+ New Review", confirm the card renders on a white background with proper fields, Cancel and Save both visibly close it. _(added 2026-09-02)_

---

## eq-field: Apprentices module simplified — journal sharing replaces the separate Ask-for-Feedback flow — FIXED, merged, live (2026-09-02)
*Same session as the Quarterly Review fix above — a full-module audit (2 parallel agents) plus a live usage check found the whole feature had barely been used (3 profiles total, all created in the 4 days before this session; 5 of 6 activity tables at zero rows). Royce looked at the audit, said it "feels complicated," and described what he actually wants: apprentices able to note things down at their leisure, trusting he'll read and act on it, plus a way to keep them accountable. Chose "consolidate into one loop" from 3 options offered.*

- [x] **Journal's existing share toggle is now the whole loop.** `apprentice_journal` gained `acknowledged_at`/`acknowledged_by`/`acknowledged_note` (additive migration, applied live to ehow). New `journalAcknowledge()` mirrors `resolveFollowUp()`'s exact one-tap-with-optional-note pattern — a manager taps "Got it" on a shared entry, the apprentice sees the acknowledgement (and any note) next time they open their journal. Two new surfaces replace two removed ones: a per-profile card on Overview next to Follow-ups, and a list-level inbox card across every apprentice. eq-field [PR #892](https://github.com/eq-solutions/eq-field/pull/892) (v3.5.651 — collided with and renumbered past another same-day PR's v3.5.650), merged, confirmed live.
- [x] **Retired: the apprentice-initiated "Ask for Feedback" flow** (pick a named supervisor, optional prompt, email with a `?request=<uuid>` deep link) — it overlapped with journal's own share toggle for no real gain, and was quietly broken (a stale legacy-identity check this session's audit found, never fixed). `feedback_requests` itself left in place (RLS/grants intact, zero rows written in the ~2 months it was live) rather than dropped.
- [x] **3 PostHog events added** (`journal_entry_created`/`_shared`/`_acknowledged`, ids and booleans only, no entry/note text) — this directly closes the "No usage instrumentation" item from the 2026-08-30 critique further down this file. Royce's own framing: "initial goal is to see if this helps them engage... final outcome would be to hopefully have better people in our business."
- [ ] **Notification gap, Royce's explicit call, not built:** sharing an entry sends nothing — no email, no push. "Right now im happy if its a closed loop between me and apprentices." `apprentice_profiles.supervisor_id` could route an email without reintroducing the old "pick a person" step if this changes — a real design decision (who, how often, per-entry vs. digest), not something to build unprompted. _(added 2026-09-02)_
- [ ] **Security-adjacent finding from the audit, not fixed:** `addCustomCompetency()`/`removeCustomCompetency()` (`apprentices.js:429,457`) write straight to Supabase instead of routing through the ownership-checked `apprentice-write.js` — the only thing stopping a non-manager is which buttons render client-side. Every other write in the module was migrated to the checked path in an earlier security fix; these two weren't. Worth closing before more apprentice data accumulates. _(added 2026-09-02)_
- [ ] **Permission-gate migration still incomplete in 3 files** (`apprentices-feedback-forms.js`, `apprentices-skills-passport.js`, `tafe.js` — `journal.js` was switched to the real per-person `canManageApprentices()` grant as part of today's work, these weren't). Dormant today since default grants match the coarse `isManager` role; breaks silently the first time someone's access is customised via Shell's Access Control. _(added 2026-09-02)_
- [ ] **TAFE Holidays doesn't protect Timesheets, only Roster's bulk-fill button.** `tafe.js`'s `isTafeHolidayCell()` has zero callers — `timesheets-rules.js`'s day-status logic never checks it, so an apprentice's regular TAFE day still auto-fills "TAFE / 8h" during a configured holiday break, contrary to what the config modal implies. _(added 2026-09-02)_
- [ ] **Two low-severity hygiene items from the audit, not fixed:** `_isSelfProfile()` is defined twice at global scope (apprentices.js's own copy is dead — journal.js's later-loaded copy silently wins everywhere); Skills Passport's period-switch fast-path re-render can never fire (looks for a CSS class nothing ever sets, harmless — the fallback is correct). Neither is user-visible. _(added 2026-09-02)_
- [ ] **Watch `quarterly_reviews` and the 3 new PostHog events for real signal** over the next 2-3 weeks before drawing any conclusion about whether this consolidation actually helped adoption — Royce flagged genuine uncertainty about whether simplifying the mechanism was the real barrier, versus discoverability/trust/nobody-told-them. _(added 2026-09-02)_
- [ ] **Not click-tested live by a person** — same standing Core-only sandbox limitation as every entry in this file. Royce said he'll test this one himself, live, from an apprentice's phone. _(added 2026-09-02)_

---

## eq-field: Jessica Robinson's approved leave invisible in 2 places, both fixed; a 3rd (Batch Fill) found and flagged (2026-09-02)

- [ ] **eq-field [PR #891](https://github.com/eq-solutions/eq-field/pull/891) — Batch Fill: never write over someone's approved leave.** Checked real usage first (`public.audit_log`: 4 Batch Fill/Clear operations in the last month, 20–400 cells each — not rare) before building. Same fix shape as PR #888 (picker badge + fold into the existing conflict dialog), but the actual write guard is stricter — unconditional skip on a fill, no override path in the UI, since a 100-cell bulk operation gives nobody per-cell visibility to catch a mistake themselves. Clear stays exempt on purpose. CI green, deploy preview clean, **NOT merged** — no merge instruction given this session. _(added 2026-09-02)_
- [ ] **4 people currently mis-scheduled for Friday 2026-09-04 — found while checking Batch Fill's real usage, not resolved, needs a human check.** Brett Kilpatrick, Marcus De La Fuente, Elliot Gross, Blake Reynolds each carry a real site code (STG/SLDC/EC5/SLDC respectively) on a day they also hold approved RDO/Annual leave — confirmed live on `ehow`, not a data artifact. 3 of the 4 were written within the same 9-minute window as a captured Batch Fill audit event on 2026-08-26, though the exact write path (Batch Fill vs. individual Edit Roster edits in the same working session) isn't provable from the audit trail alone. Flagged directly to Royce; not actioned in code or DB — his call whether/how to correct each person's day before Friday. _(added 2026-09-02)_

---

## eq-field: Calendar never showed weekend roster entries — FIXED, merged, live (2026-09-02)
*Royce, live example: "CA1 is logged in for 7th November for Richard Simon and Brian but it doesnt show on the calendar." Confirmed live against ehow before touching code: Richard Brown, Simon Bramall, and Brian Griffin-Colls all have a real `app_data.field_schedule` row for CA1 (Equinix CA1) on Sat 7 Nov 2026 — correctly showing on the Roster tab, absent from Calendar.*

- [x] **Root cause: `renderCalendar()`'s per-day data-build loop hard-skipped Saturday/Sunday entirely** (`if (dow >= 5) continue`), so a real weekend roster entry never reached `calDayData` at all — not a Roster/Calendar data-source mismatch, both read the same schedule data. That blanked the grid cell, the mobile agenda card, and the day-detail panel (which bails on a missing `calDayData[ds]`) for every weekend, tenant-wide, not just this date/these people. Every day of the month now builds and renders the same way; weekend cells keep their muted grey styling as a visual cue but are now clickable and show real data. eq-field [PR #882](https://github.com/eq-solutions/eq-field/pull/882) (v3.5.642), merged and confirmed live on `field.eq.solutions/sw.js`.
- [ ] **Not click-tested live by a person** — same standing Core-only sandbox limitation as every entry in this file; re-verified fresh this session that even the `?tenant=demo` fixture gate now dead-ends at "Sign in through Core" after entering the code, so there's no sandbox path left to try. Worth a real pass: Calendar → November 2026 → the 7th, confirm the CA1 chip renders on both desktop grid and mobile agenda and that clicking it opens the day panel with all three names. _(added 2026-09-02)_

---

## eq-field: approved leave not appearing on Weekly Roster — investigated, no bug found (2026-09-02)

- [ ] **Likely explanation: the leave request was bulk-imported (`imported_from: nspb-leave-sync-2026-09-01`) from sks-nsw-labour the day before it was checked** — a stale/cached roster tab open since before the import is the probable cause, not a bug. Told Royce to hard-refresh; not confirmed whether that resolved it. _(added 2026-09-02)_
- [x] **Crew-scoping ruled out as a cause going forward, 2026-09-04.** eq-field PR #910 (v3.5.668) made `field.view_all_crews` the supervisor default (was manager-only) — see the crew-scoping entry above. Whether crew-scoping actually explained Jack's leave looking missing on 2026-09-02 is still unconfirmed either way, but it can't recur for this reason for any supervisor now.

---

## eq-field: My Schedule compliance card stuck on stale "missing" state after a real upload — FIXED, merged, live (2026-09-02)
*Royce, screenshot: logged in as Jordan Sample, "uploaded both white card and photo id and its still asking me for it." Verified live against canonical (jvkn) before touching code: Jordan's data was actually correct (held both, satisfied both required types) — the screenshot itself showed a different person (Liam Holmgreen), whose gap was real and correctly flagged.*

- [x] **Root cause: the card's two backing caches fetch once per page load and never invalidate.** EQ Cards is a separate tab with no push signal back to Field, so an already-open Field tab stays on stale data (including a stale-but-correct-at-the-time empty result from before the upload) until a hard reload. Added a "Check again" action to the card's warning state that resets the caches and re-fetches. eq-field [PR #877](https://github.com/eq-solutions/eq-field/pull/877) (v3.5.638), merged and confirmed live.
- [ ] **Not click-tested live** — the fixed path only renders behind real canonical data plus a real authenticated session (both tenants are Core-only); no path to that in this environment. Worth a real pass: upload a credential in EQ Cards, flip back to an already-open Field tab on My Schedule, confirm the card still shows "missing," tap "Check again," confirm it clears without a page reload. _(added 2026-09-02)_

---

## eq-field: My Schedule day-card was cluttered with always-on contact lines — FIXED, merged, live (2026-09-02)
*Royce, same screenshot as above: "the daily info is a little bit busy." Offered 4 directions with named tradeoffs; picked "collapse contacts to a tap."*

- [x] **Site lead + Ask-for/Backup contacts (up to 3 always-visible lines) collapsed into one "Site contacts" row, hidden by default.** Same numbers, same `tel:` links, one tap to reveal. My Schedule only — `sites.js`'s Sites page keeps these always open (different screen, more room, nobody flagged it). eq-field [PR #878](https://github.com/eq-solutions/eq-field/pull/878) (v3.5.640 — v3.5.639 collided with a concurrent PR, renumbered), merged and confirmed live.
- [ ] **Not click-tested live** — verified via an isolated Node `vm` harness (real source, no DOM/network) instead: 14/14 checks covering empty-state handling, HTML per lead/contacts combination, escaping, and unique per-day box ids. Worth a real pass: open My Schedule for a day with a site that has a lead and Ask-for/Backup contacts, confirm the collapsed row, tap it, confirm all 3 lines appear with working `tel:` links. _(added 2026-09-02)_

---

## eq-field: My Schedule compliance card mislabeled a viewed teammate's gap as "Your profile" — FIXED, merged, live (2026-09-02)

- [ ] **Not click-tested through the full authenticated UI by a person** — confirmed this time against the real Netlify deploy preview itself, not just the local sandbox: both `eq` and `sks` are Core-only, so the PIN gate refuses outright everywhere, real preview included. Worth a real pass: sign in through Core, open My Schedule, switch the picker to a teammate with a missing credential, confirm the card names them, not "Your". _(added 2026-09-02)_

---

## eq-field: Apprentice profile self-service — real year on create, self-editable site — FIXED, merged, live (2026-09-02)
*Continuation of the "Jordan A. Sample" apprentice walkthrough (see the 2026-08-30/31 section further down this file). Royce flipped Jordan's Shell employment type to Apprentice, then reported the just-created Field profile showed 1st year against Shell's real "year 2", and asked for apprentices to be able to set their own current site.*

- [x] **Self-created apprentice profiles were server-force-setting year_level to 1 regardless of the real value already on the person's staff record.** `netlify/functions/apprentice-write.js`'s create-profile action now seeds it from the caller's own `field_people` row, falling back to 1 only when genuinely unknown. Current site opened up as self-editable on both create and edit (was manager-only) — only the apprentice knows where they're working day to day; year/start date/notes stay supervisor-only. `tests/apprentice-write-scoping.test.js` updated to match (29/29). [PR #879](https://github.com/eq-solutions/eq-field/pull/879) (v3.5.639), merged and confirmed live on `field.eq.solutions/sw.js`.
- [ ] **`current_site` is now a second, unreconciled place someone's "current site" can live** — separate from both the day-by-day Roster/Schedule assignment and the more detailed `rotations` table (still manager-only). Letting the apprentice self-edit it can drift from what the roster actually has them on today; nothing cross-checks the two. Built as asked, not resolved — worth a look if it causes confusion in practice. _(added 2026-09-02)_
- [ ] **Not click-tested live by a person** — same standing sandbox limitation as every entry in this file. Worth a real pass: as an apprentice, "Set Up My Profile" and "Edit My Goals" both show an enabled site dropdown with year/start date/notes greyed out; a manager's create/edit flow unchanged. _(added 2026-09-02)_
- [ ] **This repo's own CLAUDE.md is stale on the 'eq' tenant's canonical model** — it still describes `eq`'s canonical tables as `public.people`/`timesheets`/`leave_requests` directly on zaap. Live-queried zaap this session: that table doesn't exist any more — zaap has fully migrated to the same `app_data.staff` + `field_people`/`field_people_directory`/`field_people_removed` view model already documented for ehow/sks. Needs a CLAUDE.md correction, not a code fix. _(added 2026-09-02)_

---

## eq-field/eq-context: field_managers not in the shared-object drift registry (2026-09-01)
*Found auditing the incident-alert-recipients work: `app_data.field_managers` (view) and `field_managers_digest_iu` (trigger function) on ehow can be fully replaced by either eq-field's hand-applied migrations or eq-shell's governed pipeline — same risk shape as the 3 confirmed prior incidents in `IDENTITY-MODEL.md` §3.3.3 — but neither object is actually registered, so the nightly `check_shared_object_drift.py` doesn't protect them.*

- [~] **Register both objects in `eq/identity/shared-db-objects.json`** — spawned as `task_1e2c8b07`, Royce started it running in a separate local session 2026-09-01, in progress, not yet reported back.

---

## eq-field: TAFE Holidays staleness alert on Dashboard — PR open, not merged (2026-09-01)
*Royce, exploratory: "is there a clever way to ensure tafe holidays update?" The `tafe_holidays` date ranges (Edit Roster → TAFE Holidays) are hand-typed and nothing prompts anyone before NSW TAFE's next term break needs entering. Presented 3 directions via `AskUserQuestion` (staleness warning / auto-import from TAFE NSW's calendar, flagged unverified-feasible / leave manual); Royce picked the staleness warning.*

- [ ] **eq-field [PR #868](https://github.com/eq-solutions/eq-field/pull/868) — CI green (Tests+lint, both drift checks, deploy preview all pass), NOT merged.** `main` moved again after push; now `mergeable: CONFLICTING` — needs a rebase before it can merge. No "merge" instruction given this session. _(added 2026-09-01)_
- [ ] **The 45-day threshold is a judgment call, not backed by verified NSW TAFE term-length data** — said so plainly in the CHANGES banner and PR body rather than presented as researched. Royce's call whether it needs tuning once he's seen it in practice. _(added 2026-09-01)_
- [ ] **Not click-tested live by a person** — no SKS/Core credentials in this environment. Worth a real pass once merged: a manager opens Dashboard and sees (or correctly doesn't see) the card depending on real coverage. _(added 2026-09-01)_

---

## eq-field: roster/timesheets staff-name map 400ing for every non-manager, wider silent bug for managers found + fixed (2026-09-01)
*Royce reported the Edit Roster grid going blank after a refresh, attaching his own browser console log — traced to a single 400 rather than guessed at.*

- [ ] **Not click-tested live by a person, either half** — no SKS/Core credentials in this environment. Verified instead via live JWT-simulated SQL against ehow for both the non-manager and manager paths (real names + correct group values returned) and by confirming the deployed production `scripts/supabase.js` contains the shipped fix. Worth a real pass: sign in as both a plain worker/supervisor and a manager, open Edit Roster and Timesheets, confirm real names and correct group labels throughout. _(added 2026-09-01)_
- [ ] **Structural gap, not fixed**: eq-shell's and eq-field's migration pipelines still have no shared ledger — this is the second confirmed instance (after `field_people_iud()`) of eq-shell silently changing a shared `app_data` object's shape with nothing in eq-field recording it. PR #867 documents this one instance; the coordination gap itself is still open. _(added 2026-09-01)_
- [ ] **Own mistake, caught and assessed, not actioned further**: an early `git rebase` accidentally targeted the shared `C:\Projects\eq-field` root instead of an isolated worktree, moving a stale already-merged branch (`claude/csv-import-preserve-existing-fields`, remote already deleted, zero unique commits) forward to match `origin/main`. Confirmed harmless before doing anything else — no work lost, its pre-rebase SHA (`0e644fc7`) is still recoverable from that branch's own reflog if ever wanted back. Left as-is rather than touching that shared checkout a second time. _(added 2026-09-01)_

---

## eq-field: Weekly Roster "By Crew" gap chips + Edit Roster search/site field (2026-09-01)

- [ ] **Red "Not rostered today" chips flag anyone blank-today, not just real gaps** — someone between jobs, on an unlogged admin day, or labour-hire not needed this week reads the same as an actual problem. No dismiss/reason-code escape hatch built; deliberately deferred until Royce has seen it in real use rather than guessed at pre-emptively. _(added 2026-09-01)_
- [ ] **Not click-tested live by a person** — no SKS/Core credentials in this environment, verified via fixture-driven browser rendering + real `form_input` into the actual controls instead (see `eq/changelog/eq-field.md`). Worth a real pass: SKS supervisor opens Weekly Roster, confirms the gap chips read sensibly against real data; opens Edit Roster, confirms typing a name or a site code (e.g. "SY3") both narrow the list correctly. _(added 2026-09-01)_
- [~] **`#roster-site` (read-only Weekly Roster page) may share the exact lazy-load population race just found and fixed on Edit Roster's now-removed `#editor-site`** (`getAllSiteCodes()` isn't defined until `roster.js` lazy-loads; nothing re-triggers `refreshPersonSelects()` on tab visit) — not reproduced live, so not fixed blind. Spawned as `task_028d9925`; Royce started it running in a separate local session 2026-09-01, in progress, not yet reported back. _(added 2026-09-01)_

---

## eq-field: SKS NSW Labour safety records backfilled into EQ Field (2026-09-01)
*Royce, direct request — copy sks-nsw-labour's (standalone app, separate repo) historical prestart/toolbox-talk records into EQ Field's SKS tenant. Reconciled against sks-nsw-labour's live Supabase (`nspbmirochztcjijmcrx`) per the standing carve-out that reading/reconciling its data on direct request is fine (never proactive code work there — see `eq/pending-archive.md`'s 2026-08-26 account-reconciliation entry for the same carve-out).*

- [ ] **20 rows still unresolved, left as free text** — 15 blank (no site was ever recorded in the source either), plus "DR SYD010", "SYD010", "Next DC S1", "St George Private Hospital" (1 each). Didn't guess a remap since a wrong one is worse than plain text. Royce's call whether to chase these down. _(added 2026-09-01)_
- [ ] **Wayne Rowe's new leave request has no `approver_id`** — his nspb approver (Mark Brame) has no active EQ Field staff account, same deliberate hold as the 2026-08-26 account reconciliation above. Not a new problem, just surfaced again here. _(added 2026-09-01)_
- [ ] **Wayne Rowe's RDO request spans 25 weekdays (200 hours), Aug 3 – Sep 6** — unusually long for an RDO; still Pending in both systems so nothing's been approved on it, but worth a glance before anyone actions it. _(added 2026-09-01)_

---

## eq-field: role-default bypass in ehow's tenant_role_overrides deny-checks — fixed, merged, confirmed live (2026-09-01)

- [ ] **Origin of the 2 already-correct RLS policies is unexplained** — `labour_hire_companies_select`/`labour_hire_rates_select` already had the right deny-wins-over-both-paths shape live on ehow before eq-field [PR #859](https://github.com/eq-solutions/eq-field/pull/859) existed, with no PR or migration file accounting for it. Not blocking; worth a look if it matters later. _(added 2026-09-01)_
- [ ] **"Hand-applied migration needs a PR" has now slipped 3 times in this one feature area with no process/CI enforcement, only convention.** 20260831's parent migration, then PR #859 itself (merged un-applied, applied live within hours with no follow-up PR — two independent sessions raced to retroactively document it: eq-field [PR #865](https://github.com/eq-solutions/eq-field/pull/865) landed first, then eq-field [PR #866](https://github.com/eq-solutions/eq-field/pull/866) hit a real rebase conflict against it and merged both sessions' verification into one accurate header — #866's version is what's actually live on the migration file today), each recurred the identical gap. Worth a real gate eventually (CI check that a migration file's own "applied" claim matches the live ledger, or similar); not built. _(added 2026-09-01)_

---

## eq-field: EQ-SHELL-14 duplicate-identity bug orphaned a worker's future roster onto a dead record (2026-08-31)

- [ ] **Root cause still open.** Live sweep (`task_c74f9351`) completed: `app_data.staff` on ehow checked 3 independent ways (exact email+phone+DOB, normalized-phone+DOB, name+DOB) — found one more pair beyond Nelson (Conor Horgan, same-day batch, deactivated at the identical second as Nelson's dead record) but zero orphaned rows on his dead side, unlike Nelson. Checked all 22 columns across the schema that FK-reference `staff.staff_id` (via `pg_constraint`, not just the obvious 3 tables) before Royce confirmed "purge" — both dead rows deleted, Royce ran the DELETE himself after Claude Code's auto-mode classifier blocked it as live-prod DML. Also swept canonical `public.workers` (jvkn) and the `eq` tenant's `app_data.staff` (zaap) the same 3 ways — both clean, no other instances; the previously-flagged "Emma Curth" duplicate on jvkn no longer exists (resolved sometime since 2026-08-16, not chased). **The upstream cause — duplicate canonical worker identities getting created at all — is still untouched**; a third instance is possible until that's fixed. Full detail in `sessions/2026-08-31.md`. _(added 2026-08-31, updated 2026-08-31)_

---

## eq-field: Feature Toggles page — descriptions get concrete examples + mini-previews (2026-08-31)
*Royce, screenshot of Manage → Feature Toggles: "who can see this" + "can we improve the descriptions, show examples of what each feature does." Access question answered first (manager/supervisor only via `field.manage_feature_toggles`, enforced at the nav item, the route guard, and the page's own render check — all three verified live in code) before touching anything.*

- [ ] **Not click-tested live by a person** — no Core/Shell session in this environment (both tenants are Core-only; the standalone gate is dead — see this repo's own CLAUDE.md). Worth a real pass: open Manage → Feature Toggles as a supervisor, confirm the example text + mini-previews render under each row, confirm clicking inside a mini-preview doesn't flip that row's checkbox. _(added 2026-08-31)_
- [ ] **Flagged, not actioned**: `field.manage_feature_toggles` is held by both manager AND supervisor by default, even though flipping any of these 3 switches is org-wide (changes what every other open tab/page sees on next reload) — same tier as routine "Manage" items like Email Templates. Royce's call whether to narrow to manager-only; a one-line change in `permission-matrix.js` if so. _(added 2026-08-31)_

---

## eq-field: apprentice-role permissions review — Dashboard scoped, 2 more live-found gaps fixed, 2 items escalated/blocked (2026-08-30/31)
*Royce live-tested the apprentice role via Core (SKS tenant, "Jordan A. Sample" account), reported findings in real time across the session, kept testing after each fix merged and found more. Full arc: `sessions/2026-08-31.md`.*

- [ ] **Jordan's Shell login has no `service.tenant_members` row on the SKS tenant** — approved fix ("add the membership row") hit a real `auth.users` foreign-key constraint: completing it means creating a Supabase Auth identity, which isn't something to do via a DB write. Needs Jordan to go through the real first-login/hand-off flow, or Royce to provision it via proper channels. _(added 2026-08-30)_
- [ ] **Records/eq-roles — apprentice's `entity.view`/`field.view` grant is shared platform-wide (also read by EQ Service), and the only mechanism that could narrow it per-tenant (`shell_control.tenant_role_overrides`) doesn't actually work — `resolveEffectivePermissions()`'s `revokes` parameter is wired but "reserved... empty today," nothing calls it.** Royce chose "build the real fix first" over a global change. Escalated as its own eq-shell task (spawned mid-session, not yet started/reported back as of this close): wire the existing revoke mechanism into `token-exchange.ts`/`verify-shell-session.ts`, then set `entity.view`/`field.view` to `false` for `apprentice` on the SKS tenant specifically. Scope note: EQ Service intentionally excluded from that task (same underlying gap exists there too, no demonstrated real apprentice population, would double the review surface). _(added 2026-08-30)_

---

## eq-field: tenant-migration governed pipeline — caller workflow built, gated on eq-shell reconciliation (2026-08-30)
*Full build detail, the 14-file reconciliation, and the `/decide` call live in `eq/pending/eq-shell.md` (2026-08-30 entry) — this is the eq-field-side pointer since PR #846 is this repo's own change.*

- [ ] **The real remaining blocker is the unlinked-staff DATA count itself**, not a PR: the ehow timesheets/leave write-scoping migration's own pre-flight check gates on it — 36 workers + 6 supervisors of 110 total ehow actors have no linked `staff_id`, reconfirmed live 2026-08-30. Needs Royce's call: bring the count down first, or explicitly accept the residual risk and go anyway (same shape as the carve-out he already approved for unassigned supervisors on the read-side fix). See `eq/sprints/2026-08-30-field-pipeline-and-rls-sprint.md`. _(added 2026-08-30)_
- [ ] **3 secrets not provisioned** (`SUPABASE_ACCESS_TOKEN`, `CONTROL_PROJECT_REF`, `EQ_SHELL_CHECKOUT_TOKEN`) — see `eq-shell.md`, same item. _(added 2026-08-30)_

---

## eq-field: Map / Roster Overview tiles broken — CARTO required a key we don't have, swapped to OpenStreetMap, then a CSP gap blanked the tiles a second way (2026-08-30)
*Royce screenshotted the Map page — every tile a grey "API KEY REQUIRED — carto.com/basemaps/apikey" watermark, site markers still plotted correctly on top. Verified live before touching code: fetched the hardcoded `basemaps.cartocdn.com` tile URL directly — 200 OK, but the image itself is the watermark. CARTO's free anonymous basemap tier now gates on a key neither `site-map.js` nor `roster-overview-map.js` ever had; a provider-side change, not a code regression.*

- [ ] **Standing risk, not actioned**: OpenStreetMap's own tile usage policy discourages heavy production use of its free anonymous server without a dedicated provider — this is a like-for-like free-tier swap that fixes today's outage, not a structural guarantee against the same class of failure if map-tab usage grows. There's also no monitoring for "a third-party tile provider silently degraded" — if OSM ever did what CARTO just did, nothing would alert us; a supervisor would just see a broken map again with no error surfaced anywhere. _(added 2026-08-30)_

---

## eq-field: Cameron Tregoning's two mobile bug reports — Prestart create unreachable + roster warning leak, both fixed (2026-08-30)
*Royce forwarded two mobile screenshots from Cameron Tregoning: couldn't create a prestart, and a roster screen showed a raw internal warning banner. Root-caused both live before writing any fix.*

- [ ] **Not click-tested live with Cameron's real account** — verified via the full test suite, CI, and byte-level fetches of both deployed previews confirming the fixed code shipped, but no live SKS session with a real non-supervisor account clicked through end-to-end. _(added 2026-08-30)_
- [ ] **Why Anthony Hartley's staff_id briefly failed to resolve is unconfirmed** — leading theory is a client-side load-order race, not proven. Low priority since the user-facing symptom is fixed regardless. _(added 2026-08-30)_
- [ ] **`eq-context/suite-state.md`'s "Prestart/Toolbox is supervisor-only" framing (2026-08-12 entry) is stale** — contradicted by live code since 2026-08-24, and plausibly *why* this bug shipped unnoticed for 6 days. Needs a substrate correction pass. _(added 2026-08-30)_

**Notes:**
- Rebased 3x mid-session chasing a moving `origin/main` (v3.5.607/608/609 all claimed by other concurrent PRs while this one was open) — checked each for file overlap before rebasing (none), renumbered to v3.5.610.
- The user's "two screenshots" didn't actually attach on the first message (checked session storage — genuinely empty). Investigated both bugs from live Sentry/DB evidence first, then asked once with pre-populated options; user pasted the images directly on the next turn.

---

## eq-field: CSV import can no longer deliberately blank an existing field (2026-08-30)
- [ ] **Open product question, not blocking — already flagged in the PR itself.** [PR #831](https://github.com/eq-solutions/eq-field/pull/831) (merged, v3.5.605) fixed CSV people-import silently nulling `start_date` + 6 other optional fields on any partial/hand-built CSV re-import — matched rows now only apply a field if the CSV actually supplied a non-blank value for it, mirroring the guard `savePersonToSB`'s single Add/Edit path already had. Side effect: CSV re-import can no longer *deliberately* clear a field on an existing person (e.g. bulk-clearing `agency` after someone leaves a labour-hire firm) — a blank cell now always means "no info supplied," never "clear this." Probably the safer default, but it's an inferred behavior change, not a confirmed one. If bulk-clear-via-CSV turns out to matter, needs the CSV parser (`import-export.js`) to distinguish "column absent" from "cell blank" before this can change. _(added 2026-08-30)_

---

## eq-field: Apprentice journal privacy fix — two open questions (2026-08-29)
- [ ] **Historical-exposure unknown.** `apprentice-data.js` writes nothing to `audit_log`, so there's no way to confirm whether any manager/supervisor account fetched another apprentice's private journal entries during the ~11 days this was live unfixed (endpoint shipped 2026-08-18, journal-specific gap closed 2026-08-29 — [PR #828](https://github.com/eq-solutions/eq-field/pull/828)). Needs Royce's call on whether that residual unknown is worth raising with anyone. _(added 2026-08-29)_
- [ ] **"Only my account" vs. today's actual model.** Royce's framing this session ("only my account and the apprentice should see it") is narrower than what's enforced — the fix above closes the journal gap specifically; the other 6 apprentice tables still follow the existing manager/supervisor-sees-all model, which matches his own original ask on 2026-08-18 (see "apprentice data readable by any authenticated SKS session" further down this file: "I want me to be able to see all of them") but not his exact wording today. Not raised as a problem, just flagging the gap between the two asks in case it matters later. _(added 2026-08-29)_

---

## eq-field: Apprentices feature critique — items 1-2 closed, 1 of 3 open (2026-08-30)
- [ ] **No reminder mechanism for supervisors.** Unlike leave/timesheets' Friday digest, nothing nudges a supervisor to actually rate an apprentice or leave feedback each quarter — the feature's two-sided value depends entirely on a supervisor remembering unprompted. Sharpened, not resolved, by today's journal-sharing consolidation (see below) — Royce explicitly chose no notification for now ("happy if it's a closed loop... right now"), so the accountability loop depends even more directly on a supervisor remembering to check. _(added 2026-08-30)_
- [ ] **[PR #832](https://github.com/eq-solutions/eq-field/pull/832)'s fix may have blocked a real workflow with no replacement.** If a supervisor was using the old manager-bypass to help an apprentice fill in their own self-assessment together in person, that now hard-stops. Additive fix available if wanted: stamp `entered_by`/`on_behalf_of` instead of blocking outright. _(added 2026-08-30)_

---

## eq-field: Documents to Sign — Schneider handbook "wouldn't load" traced to a silent-forever spinner (2026-08-28)

- [ ] **Root cause of Luke's specific report not confirmed live** — no signer credentials in this environment to reproduce the exact fetch he hit. This closes a real, verified gap in the same code path; needs a retry on a fresh tab to confirm it actually resolves his report. _(added 2026-08-28)_
- [ ] **Two PRs collided on the same version number this session** — [#821](https://github.com/eq-solutions/eq-field/pull/821) and [#822](https://github.com/eq-solutions/eq-field/pull/822) both opened as "v3.5.592", neither merged as of 2026-08-28. This session used v3.5.593 to avoid the clash; whichever of #821/#822 merges next will need to renumber. Worth a glance next session before picking a version. _(added 2026-08-28)_
- [ ] **Still genuinely root-cause-unknown** — v3.5.595's telemetry hasn't caught a real event yet as of 2026-08-30. Next step depends entirely on a real Sentry event from an affected device, not further code changes. _(added 2026-08-30)_

---

## eq-field: Documents to Sign — inline PDF viewer shipped, root-caused a total-failure bug, audience-reach mapped out (2026-08-27)
*Follow-on to the 2026-08-20 six-round saga further down this file — a full rebuild of View, not another patch to the old `window.open()`-a-raw-file approach. Plan: convert every upload to PDF at commit time (eq-shell, self-hosted Gotenberg), render it in an embedded PDF.js viewer (eq-field), gate Sign on actually having scrolled through it.*

- [ ] **Audience reach for "push to everyone" is real but indirect — 5 role-pushes, not 1.** Royce asked how to open Documents to Sign to all staff. The push picker (`push-document-audience.ts`) takes one role, one crew, or one person per push — no "all" option (confirmed still true even after the same-evening #1645 multi-select-person-picker ship, which speeds up naming individuals but adds no bulk/all control). Reaching everyone with a Shell login today means repeating the Push action once per role — 5 live roles as of this session: employee (26), supervisor (11), manager (11), apprentice (8), labour_hire (6). A UX gap in an existing, working mechanism, not something built or requested to be built this session. _(added 2026-08-27)_
- [ ] **14 of 74 active SKS staff (~19%) have no linked Shell login and are structurally unreachable by any push.** Role, crew, and person pushes all resolve through `shell_control.user_tenant_memberships`/a real Shell login; an unlinked `app_data.staff` row silently never appears in any of them. Same root population as the long-running unlinked-staff backlog tracked in `eq/pending/eq-shell.md` (37 in mid-August, 24 on 2026-08-20) — now 14, continuing to close on its own as people complete Cards/Core signup. Full list (9 Direct, 4 Labour Hire, 1 Apprentice; 11 of the 14 from a single 2026-06-12/15 bulk-import batch that's never been chased since) given to Royce directly in-session, not reproduced here since it'll drift — re-query `app_data.staff` on ehow (`active=true and user_id is null`) for a fresh list. _(added 2026-08-27)_

---

## eq-field: field_people SEC-33 visibility regression — resolved; 1 optional follow-up open (2026-08-27)

- [ ] **Column-safety call still open on 1 field: `dashboard.js`'s upcoming-birthdays widget needs `dob_day`/`dob_month` to keep working for non-managers** (currently goes blank for them) — read-only display gap, nothing corrupts, not urgent. The companion phone/email question was resolved (Royce: "widen the column list to include phone and email", eq-field PR #817) — this is the one remaining piece. Additive-only if approved (widen `field_people_directory`'s column list further), no RLS/security change either way. _(added 2026-08-27)_

---

## eq-field/eq-shell: site_projects (multi-module sites) — read + write both live (2026-08-28→30)

- [ ] **`roster_project_picker` toggle is still OFF** — flip it in Manage → Feature Toggles before any supervisor sees the explicit per-day project-code picker dropdown on Edit Roster. Typing a project code directly into the site cell (e.g. "MOD10") already resolves the real site regardless of this toggle, and a hover tooltip on the cell now hints this too — see `eq/changelog/eq-field.md` (2026-08-30) for the full build. _(added 2026-08-30)_
- [ ] **Not live-click-tested against real MOD10/SLDC data on SKS** — no live Core/SKS credentials in this environment. Covers the full read-side sweep now shipped across three PRs sharing the same `_resolveSiteAbbr` resolver: roster.js's own lookups ([PR #833](https://github.com/eq-solutions/eq-field/pull/833)), My Schedule's site-lead/contacts/day-specific project badge ([PR #835](https://github.com/eq-solutions/eq-field/pull/835)), and Dashboard + Trial Dashboard's site-name display ([PR #836](https://github.com/eq-solutions/eq-field/pull/836)). All verified via full test/lint/bundle/cache-buster CI; #836 additionally confirmed live on its deploy preview that the fallback branch it fixes is genuinely reachable pre-login (`EQ_ROSTER_ADAPTER` loaded, `getSiteName` not yet loaded) — but none clicked through against a real aliased roster day. _(added 2026-08-30)_
- [ ] **Site-abbr resolution is now duplicated three times** (`roster.js`, `dashboard.js`, `trial-dashboard.js`) rather than shared — each file has its own copy because they load at different times relative to `roster.js`'s lazy load, so a shared module isn't a drop-in fix. Fine at today's low-urgency scale (one alias fleet-wide); worth consolidating only if a load-order-safe shared module becomes worth building for its own sake. _(added 2026-08-30)_
- [ ] **Only one project code exists fleet-wide today (MOD10 → SLDC)** — the practical blast radius of anything still unresolved above is small; worth another look once a second `site_projects` alias exists. _(added 2026-08-30)_

---

## eq-field: Timesheets Fill Week + Approved column, plus the "OFF ≠ approved leave" display gap (2026-08-27)
*Royce screenshotted Phoenix Khatri showing "OFF" on Timesheets with no leave approval findable, PDF export of all 43 leave requests attached (none his). Root-caused live: a roster batch-fill (Luke Wheeler, audit-logged), not a leave request — Timesheets renders straight from the roster/schedule cell and never checks `leave_requests` at all. From there, Royce asked for one-pass whole-timesheet fill when a locked leave/TAFE day splits the week. Shipped together as eq-field [PR #808](https://github.com/eq-solutions/eq-field/pull/808) (v3.5.583), squash-merged on explicit "merge", confirmed live via `field.eq.solutions/sw.js`.*

- [ ] **Standing display gap, not fixed**: Timesheets still can't distinguish a supervisor-set roster OFF from a genuinely approved leave request — they render identically, which is exactly what made Phoenix's case confusing. Only worth fixing if it causes real confusion again; the fix would be surfacing which mechanism produced the OFF state, or requiring OFF/leave-type roster codes to link back to a real `leave_requests` row. _(added 2026-08-27)_
- [ ] **A fully blank Timesheets row shows an empty Approved-column cell, no placeholder** — could read as "forgot to check" vs. "nothing to approve yet." Not fixed, judged scope creep past what was asked. _(added 2026-08-27)_
- [ ] **In-modal weekend toggle only preserves typed Sat/Sun hours across one ON→OFF cycle**, not a second OFF→ON→OFF→ON — re-enabling re-seeds from the DB. Uncommon click pattern, no data-integrity risk (Save is separate/explicit). _(added 2026-08-27)_
- [ ] **Not click-tested live by a real signed-in supervisor** — reached the actual deploy preview this time (further than the usual local-only limitation), but `?tenant=demo` resolves to the `eq` sandbox tenant with no people data, and the Browser pane's own known 0×0-viewport bug blocked clicks/accessibility-tree reads on top of that. Verified instead via an isolated harness against the real edited files. _(added 2026-08-27)_

---

## eq-field: digest "Send test to myself" — content was wrong after the first successful send (2026-08-27/28)

- [ ] **Not yet re-confirmed by Royce.** Two further bugs found after the first real click-through succeeded in reaching an inbox: the button itself failed to resolve the caller's email ("No email on file" — `app_data.field_managers`'s `auth.jwt()`-dependent WHERE clause is unreachable from a service-role caller, fixed eq-field [PR #818](https://github.com/eq-solutions/eq-field/pull/818)/v3.5.589), and once that was fixed, the digest that arrived had empty Pending-approval and On-leave sections regardless of real data (the edge function compares `leave_requests.status` against Title-case literals that can never match the DB's lowercase-only CHECK enum — wrong since the v3.5.216 canonical rewrite, so every real Friday send has shown "Nobody approved off" the entire time regardless of actual data — fixed eq-field [PR #819](https://github.com/eq-solutions/eq-field/pull/819)/v3.5.590, edge function redeployed to production v14→v15 and content-verified live). Nobody has re-clicked "Send test to myself" since the latest fix to confirm the content now actually populates. Full detail in `eq/changelog/eq-field.md` and `sessions/2026-08-28.md`. _(added 2026-08-28)_

---

## eq-field: audit-attribution breadcrumb for JWT writes that drop x-eq-actor (2026-08-26)
*Full investigation and root-cause detail in `eq/pending/eq-shell.md` (2026-08-26, "Field-driven writes to app_data.staff have no reliable attribution") — this is the eq-field-side pointer since that's where the shipped fix landed.*

- [ ] **Overlaps `task_66de20f0`** (Royce's independently-started background session investigating the same gap) — see eq-shell.md for what this session already ruled out before shipping the breadcrumb, so that task doesn't redo it.

---

## eq-field: job-numbers Ops→Field status link verified + 7-week migration drift fixed (2026-08-26)
*Royce asked whether Field's Job Numbers board reflects live status from EQ Ops. It does — but verifying it surfaced eq-field's own repo had been silently wrong about how its own backing function works for 7 weeks.*

- [ ] **Not pursued**: widening the status mapping so Ops's `won-job-created`/`po-matched`/`draft` render as distinct board statuses instead of all reading "Active". Offered as an option via AskUserQuestion; Royce chose the plain reconcile instead. Worth revisiting only if finer-grained status is actually wanted in practice. _(added 2026-08-26)_

---

## eq-field: sks-nsw-labour vs EQ Field account reconciliation — closed, one deliberate hold (2026-08-26)

- [ ] **Mark Brame (NSW General Manager) — Royce will re-add him to EQ Field himself, once he trusts the security/permission groups.** No timeline given. Not a task to pick up proactively — check with Royce before restoring him even if a future audit re-flags him as missing. Background: full account reconciliation against sks-nsw-labour found only 3 people (Dean Francis, Mark Brame, Matthew Khreich) removed in EQ Field despite being active in sks-nsw-labour; Royce confirmed all 3 have left SKS and it's correct as-is — Mark is the one deliberate exception, not a gap. _(added 2026-08-26)_

---

## eq-field: Home + drawer quick links to Workbench/ESS, SKS-only (2026-08-26)
*Royce, relaying a request from Cicero (a field worker) via a screenshot of his phone on EQ Field's Home tab: could Field link out to Workbench and the payroll site (ESS), so workers only need one app/bookmark. Built and shipped same session — eq-field [PR #794](https://github.com/eq-solutions/eq-field/pull/794) (v3.5.575), merged, live.*

- [ ] **Neither link brings a worker back to Field.** Tapping either opens a second browser tab with no return affordance — delivers "one bookmark," not fully "one app," which is the softer version of the goal Royce actually stated. No reasonable client-side fix exists without native-app affordances Field doesn't have; named rather than left implicit in the shipped changelog copy. Only worth revisiting if it turns out to actually bother people in practice. _(added 2026-08-26)_

---

## eq-field: Edit Roster speed — Feature Toggles, keyboard/paste Tiers 1+2 (2026-08-25)
*Header corrected 2026-08-27: used to end "...then a still-open Ctrl+Enter regression" — stale, never updated after the regression was fixed. Full write-up: `eq/changelog/eq-field.md` (PR #805, v3.5.582, 2026-08-26) and `sessions/2026-08-26.md`.*

- [ ] **`/decide` pass: recommended making "Copy Last Week" (already built, empty-cells-only, non-destructive) the default first move every week**, ahead of any manual typing or further keyboard/paste tooling — a bigger lever than per-cell speed if week-to-week site assignment is genuinely stable, which real screenshot evidence suggests but wasn't directly confirmed (no two consecutive real weeks were diffed). Not yet confirmed or actioned by Royce. _(added 2026-08-25)_
- [ ] **Dedicated "Fill week" button (Ctrl+Enter backup insurance) — proposed, held.** Raised as a keyboard-only fallback in case Ctrl+Enter broke again; Royce's call was to hold since Tab already fills a row without touching the mouse. Only worth building if Tab/paste turn out insufficient in real use. _(added 2026-08-26)_

---

## eq-field: copy-out (Excel-style range select) for Edit Roster — scoped, not built (2026-08-25)
*Follow-up to the Tier 2 paste work: Royce asked "does the copy work like excel now too" (no — unchanged, paste-in only, verified against current code), then "can we build copy-out too?"*

- [ ] **Recommendation given, not yet actioned either way.** Offered two scopes via AskUserQuestion (a small "copy one person's row" button vs. full Excel-style click-drag/shift-click range-select + Ctrl+C); Royce asked for a straight read instead of picking. Recommended holding — neither built. Reasoning stated plainly: no concrete blocked workflow has actually surfaced for it (unlike paste-in, which had a specific, stated pain point); full range-select would be a meaningfully bigger and riskier build than anything shipped today, on the same screen that already had one real regression today; and while Edit Roster itself has no export today (checked directly, corrected an initial wrong assumption that it did), the read-only Weekly Roster view and the separate Import/Export page both already have CSV export as an existing workaround. Left as: revisit if a concrete case shows up, and the small "copy a row" version is likely still the right scope then, not full Excel parity. _(added 2026-08-25)_
- [ ] **No live Shell-embedded click-through with real SKS credentials this session** — same accepted, recurring limitation logged throughout this file; this session's own browser-pane testing additionally found `document.hasFocus()` reads `false` for the whole pane, so even `document.activeElement`/`.focus()`-based checks are unreliable here regardless of the pane being open. _(added 2026-08-25)_

---

## eq-field: People save — dirty-field diffing, closes a live data-clobber bug (Zemi Asri, 2026-08-25)
*Royce reported a real incident: corrected Zemi Asri's Group to Direct and start date via Edit Person, save succeeded, but employment_type reverted to Labour Hire ~6s later. Traced end-to-end: `savePersonToSB()` unconditionally resent all 19 columns on every save regardless of what changed — eq-shell's Staff-page edit panel had the identical shape and was the one that clobbered this specific write with a stale snapshot on an unrelated field save.*

- [ ] **`employment_type_locked_by_shell` may be incorrectly set on staff who never had a deliberate employment_type edit** — eq-shell PR #1490 (2026-08-20) set this flag whenever `employment_type` was in the save payload; since that payload always included it until PR #1590 merges, any Staff-page save since 2026-08-20 likely set it, not just real reclassifications. Needs a DB audit (locked rows vs. audit trail around each lock time) before deciding whether to reset any. Not investigated this session — flagged, then a spawned task chip for it was withdrawn by mistake mid-session and never re-created. _(added 2026-08-25)_
- [ ] **This repo landed 5 same-day version-number collisions in one evening** (562/563/564/565 — this PR's own branch alone got bumped 564→565→566 across two rebases against concurrently-merging PRs #783/#784/#787). Not a new problem, already handled by this file's own convention of re-checking freshness before every push, but worth a look if it keeps escalating — multiple concurrent sessions are landing PRs on `main` within minutes of each other most evenings now. _(added 2026-08-25)_

**Deferred:**
- [ ] **Not click-tested live** — no authenticated SKS session in this environment; the fix was verified via full local test/lint/build-bundle/cache-buster parity with CI (all green) and a clean deploy-preview boot, not a real Edit Person save clicked through. _(added 2026-08-25)_

---

## eq-field: settable Preferred Name — closes the write-side gap on an already-wired read path, then a same-day production bug (2026-08-25)

- [ ] **Worker self-service for their own preferred name — not built.** The new field is supervisor-gated like every other field in that modal, consistent with the standing v3.5.560 decision that self-edit belongs in Shell's `/settings/profile`, not a Field-side editor. Flagged, not decided: a worker's own chosen name is arguably the one field in that form they should be able to set themselves. Royce's call if/when Shell's self-service profile work resumes. _(added 2026-08-25)_
- [ ] **Full click-through save round-trip (type a value, click Save, confirm it persists) as a Supervisor — still not completed.** The demo tenant's supervisor-escalation flow doesn't resolve cleanly in headless browser automation. `editPerson()` correctly populating an existing record's fields (the READ side) was confirmed via real DOM checks against the real shipped code; the WRITE side (clicking Save, confirming the PATCH actually lands) is still only verified via direct SQL/isolated script, not a real click. _(added 2026-08-25 — this is exactly the gap that let the 2026-08-26 bug below ship unnoticed; still open)_
- [ ] **2026-08-26: Marcus De La Fuente's Preferred Name was saved literally identical to his Full Name — root mechanism never conclusively identified.** Royce screenshot: "Preferred name isnt working." Live-verified only 1 of 110 ehow staff rows affected (not systemic); a rollback-protected SQL test proved the view/trigger handle a partial `preferred_name`-only PATCH correctly; exhaustively grepped every DB function/cron job and the full client save path — no code found that copies Full Name into Preferred Name. Shipped a fix regardless (`savePerson()` now nulls a Preferred Name that case-insensitively equals Full Name — PR [#806](https://github.com/eq-solutions/eq-field/pull/806), v3.5.581, **MERGED + confirmed live** via `field.eq.solutions/sw.js` showing `v3.5.581`) and cleared Marcus's live value, but the actual cause (deliberate test input vs. a browser-autofill misfire) is unconfirmed — same standing click-through gap as the item above. Worth a real click-test the next time someone's signed in via Core: type a genuine nickname, save, reopen, confirm it round-trips (not just that a duplicate gets rejected). _(added 2026-08-26)_

---

## eq-field: feature-toggles.js — named the two adjustable-thing patterns (2026-08-25)
*Royce asked whether Field needs a bigger "features menu" now that it has this many small on/off surfaces. Ran a `/decide` pass first — grounded the "10s if not 100s" premise against live code (actual count: 2 formal toggles + ~20 permission grants, which already has its own admin page + 1 shared digest-settings blob) before judging. Call: don't build a bigger registry yet, name the two existing patterns instead so the next adjustable thing has an obvious home. `scripts/feature-toggles.js` header comment now documents both: admin toggle (shared JSON blob, same shape as digest-settings.js's digest_sections) vs. per-person setting (own row, e.g. managers.digest_opt_in). Docs only, no behaviour change. eq-field [PR #781](https://github.com/eq-solutions/eq-field/pull/781) (v3.5.562), squash-merged, confirmed live via field.eq.solutions/sw.js.*

- [ ] **Flip condition, not yet met**: if Royce identifies 5+ specific new admin toggles wanted soon, build the registry properly then (a real key→metadata table, not the hardcoded array) — retrofitting after ad hoc entries pile up is the rebuild the `/decide` pass wanted to avoid. Currently 2 entries in `FEATURE_TOGGLE_DEFS`. _(added 2026-08-25)_

---

## eq-field: site internal contacts — "Ask for / Backup" shown on schedule + site cards (2026-08-24)

- [ ] **Only Equinix SY5 has real contact data** (Matthew Miller / Scott Hotson). CA1, SY1, SY2, SY3, SY4, SY9 show nothing yet — needs real names + numbers from Royce, entered via eq-shell's Edit Site modal (`eq/pending/eq-shell.md`, PR #1581) — no migration needed any more. _(added 2026-08-25)_
- [ ] **Even Equinix SY5's real data was never rendering — a separate code bug, not a data gap.** `index.html`'s boot-time `STATE.sites` mapping never carried the 4 contact fields through from `app_data.field_sites`, so the render function always saw `undefined`. Fixed: eq-field [PR #821](https://github.com/eq-solutions/eq-field/pull/821) (v3.5.596), squash-merged on explicit "merge", confirmed live via `field.eq.solutions/sw.js`. Not yet click-tested live — both tenants are Core-only for auth (no standalone PIN path), so real tenant data is only reachable through a live Core session, unavailable in this environment; worth a real look at Equinix SY5's card next time someone's signed in via Core. _(added 2026-08-28)_

---

## eq-field: access-control review (permission-matrix v2.6/v2.7), crew-scoping widened to Leave, timesheets RLS fail-open closed (2026-08-24/25)

- [ ] **Royce hasn't yet granted himself `field.manage_recognitions`** — it's opt-in-only now (same shape as `field.manage_pipeline`); switch it on for yourself from Shell's Access Control (Custom Group) when convenient. _(added 2026-08-25)_
- [ ] **Per-tenant hiding of specific leave permissions, floated, not built** — Shell's Access Control screen would need a per-tenant visibility layer; out of scope for eq-field alone. _(added 2026-08-25)_
- [ ] **A push to PR #768 got zero GitHub Actions runs for 24h+, cause unknown** — confirmed via the Actions API directly (`total_count: 0`), not a display/watch lag; other branches got normal runs in the same window, and the same PR's earlier/later commits ran fine. Never root-caused. Worth a note if it recurs — the fix each time is a fresh commit (a rebase, in this case) to force a new synchronize event. Did NOT recur on this review's own follow-up (PR #778 got 3 normal Actions runs). _(added 2026-08-25)_

---

## eq-field: leave.js file-size debt — email templates split out (2026-08-25)
*leave.js was flush against its eslint `max-lines` grandfather ceiling (1899/1900, zero headroom) after #768 — the next PR touching the file would've broken CI with no room to absorb even a one-line fix.*

- [ ] **3 more extraction candidates identified but not built** (lower priority, flagged by the original task brief, not independently verified this session): the CC-recipients config subsystem (~124 lines), the submit flow (~271 lines), the respond/approve flow (~239 lines) — leave.js still has real headroom (1724/1750) so none of these are urgent. _(added 2026-08-25)_

---

## eq-field: birthday (day + month) — root cause found and fixed in two passes; one thread still open (2026-08-24)
*Correction 2026-08-25: this entry's header used to say "root cause not found" — stale, never updated by either of the two closes that actually resolved it later the same continuous session. `task_bb6cab43` found the real cause (an undocumented `staff_derive_dob_from_cards` BEFORE trigger on `app_data.staff`, unconditionally re-deriving day/month from a null `date_of_birth`) and fixed it live, eq-field [PR #767](https://github.com/eq-solutions/eq-field/pull/767). A second pass then closed the related case — a Cards-linked person who already has a real `date_of_birth` and gets a direct day/month edit now gets a clear rejection instead of a silent discard, porting a guard eq-shell had already built for the identical bug class. eq-field [PR #769](https://github.com/eq-solutions/eq-field/pull/769), v3.5.550. Both merged, confirmed live.*

- [ ] **Aiden Crowley's real SKS record still carries stale test data from this thread** — Job Title "1st Year apprentice", Emergency Contact "Mr Crowley" / "0400123456" / "Parent", Start Date 24/08/2026 (from the original bug reproduction), and his birthday is blank again (18 Feb was typed while reproducing the bug, never confirmed real, deliberately not left on the record). Needs Royce's go on timing — clear the trial data, then do a real re-save of his actual birthday. _(added 2026-08-24)_
- [ ] **45 of 81 active SKS staff have no birthday recorded** — the feature works correctly for all of them now; most should self-resolve as people scan a licence into Cards (auto-fills DOB), the rest need a manual entry whenever. No rush. _(added 2026-08-24)_
- [ ] **PR #769's reject-path has no live click-through yet** — verified via 4 direct-DB scenarios, full test/lint/drift suite, and a clean deploy-preview smoke; no authenticated SKS session available to click it for real. Worth a try: edit a Cards-linked person's birthday who already has a real DOB, confirm the toast reads clearly. _(added 2026-08-24)_

---

## eq-field: AUDIT_SB_KEY mislabeled as publishable — it's the full ehow service_role key (SEC-65, fixed 2026-08-24)
*Surfaced while triaging the security register's open findings at Royce's "is there anything else" prompt; picked to build alongside SEC-58 (see eq-shell).*

- [ ] **Not tested: whether any of the 4 consumers (`verify-pin.js`, `eq-agent.js`, `eq-service-sites.js`, `_shared/sentry.js`) actually ships the value client-side.** Reasoned-not-proved in the original SEC-65 finding, still is — the label fix removes the "believed safe" premise but doesn't itself prove or disprove exposure. `_shared/sentry.js` already redacts it from error reports (no change needed there); the other 3 weren't traced end-to-end. _(added 2026-08-24)_

---

## eq-field: Supervisors are excluded from Contacts BY DESIGN — not a bug, mis-diagnosed twice (2026-08-23)
*Royce: "Rhys Scott still doesn't appear in the list on EQ Field — he shows in the supervisor list but not contacts." Recorded because it was mis-diagnosed twice in one session and a fix was shipped for the wrong cause.*

**The behaviour:** `renderContacts()` (`scripts/people.js`, ~L896) does not read `STATE.people`. It reads `_peopleExMgrs()` (`scripts/utils.js`), which subtracts everyone present in `STATE.managers` (the `app_data.field_managers` view = staff `WHERE is_supervisor`), matched by email then by normalised name. Its own header states the intent: *"Contacts minus supervisors/managers (QA row 11, v3.5.228) — Supervisors/managers have their own Supervision list, so they're kept out of Contacts."* All **20** SKS supervisors are excluded, not just Rhys. Working exactly as written.

**Not affected — verified:** the Roster does NOT use `_peopleExMgrs()`; `getRosterPeopleForGroup()` filters `STATE.people` directly, so supervisors DO appear on the roster. Royce confirmed live: "Rhys is in the roster." Only Contacts (and the Contacts nav badge, which shares the same helper deliberately so the two can't disagree) excludes them.

**How it was mis-diagnosed, twice:**
1. First answer was "stale client cache, hard-refresh" — wrong; Royce pushed back, correctly.
2. Second answer blamed the team-pill filter (`personInActiveTeam`) and shipped **v3.5.546** for it. That fix is a **genuine, independent bug** — a supervisor who runs a crew via `team_supervisors` without also being a `team_members` row vanished from Roster/Timesheets under a team pill — and it stands on its own. But it was **never the cause of this report and did not fix it**, and the claim "clearing the filter will surface him" was wrong: clearing a pill does not put a supervisor into Contacts.
3. The miss both times: `app_data.field_people` was queried and Rhys found present, which correctly ruled out the data layer — but the *client-side source list* Contacts actually renders from was never checked, and the exclusion lives in a function whose name says what it does.

**Open, if wanted (Royce's steer 2026-08-23: "there should be the ability to have them both as supervisor and in roster — that's what we set up in Shell"):**
- [ ] **Field's Contacts contradicts Shell's model.** Shell's Staff page carries two *independent* badges per person — "Supervisor" and "On roster" — so a supervisor can be on the roster. Field's Contacts instead treats is-a-supervisor as not-a-contact. Royce confirmed the current state is acceptable because the roster (the surface that matters) already shows them, so **no change was made** — but the two apps do disagree, and if Contacts is ever meant to be a true directory of everyone, the fix is to stop `renderContacts()`/`_contactsCount()` subtracting `STATE.managers`. Blast radius is narrow: the Contacts list and its nav badge only. Note this would reverse v3.5.228's deliberate "QA row 11" decision, so surface why that was added before undoing it. _(added 2026-08-23)_

## eq-field: Field-wide outage — canonical anon-read regression fixed, boot hardened against slow-fetch failures (2026-08-23)
*Royce reported Field "could not connect to this workspace" through Core. Investigated live rather than assuming Field-side; the first fix built (boot fetch retry/timeout hardening) turned out NOT to be the actual cause of the outage — caught by insisting on a live deploy-preview smoke test even after CI passed, before reporting it fixed.*

- [ ] **Not verified live**: the boot-hardening retry path itself has never actually fired for real — the underlying fetch hasn't failed again since it shipped. Confirmed the happy path boots clean end-to-end, not the retry path itself. _(added 2026-08-23)_

## eq-field: 3 pre-convention single-plane migrations retrofitted with the structured `-- Plane:` header (2026-08-23)
*Companion to eq-shell's new plane-scope guard (`eq/pending/eq-shell.md`, same date) — these 3 migrations already stated "ehow (SKS) ONLY" in prose but predated the machine-readable header convention the new guard reads.*

- [ ] **Not yet copied into eq-shell's `supabase/tenant-migrations/` (the One Pipe) or dispatched** — see `eq/pending/eq-shell.md`'s matching entry; explicitly Royce's call. _(added 2026-08-23)_

---

## eq-field: Roster compliance gate — missing-required badge on both roster views, an assignment hold point, and a worker-facing self-compliance card (2026-08-21)

- [ ] **No live click-through by a person yet, any of these PRs** — same sandbox limitation #734/#737 already logged (no Core-authenticated SKS session reachable from this environment), now also true of PR #752's My Schedule card and PR #755 (dashboard licence-missing card regrouped one row per person instead of one row per licence). All verified via the full test suite, eslint, bundle/cache-buster checks, and live-browser verification against the real shipped files with synthetic data — but worth a few minutes on the real tenant: (1) open Edit Roster, type a real site into a cell for someone flagged on Contacts, confirm the hold point fires and the audit entry lands; (2) open My Schedule as a real flagged worker, confirm the amber card shows and names the right gap; (3) open the Dashboard, confirm the Licence Missing/Expired card now shows one row per person with all their badges, not a repeated row per licence. _(added 2026-08-21, extended 2026-08-23)_
- [ ] **Two different "how many are missing" numbers, not reconciled**: Shell's Training Matrix said 6 of 32 on 2026-08-19 (`sks/pending.md`); this session's live query said 27 of 65 on 2026-08-21. Different populations/dates, both real, but the exact gap between them is unexplained — worth a look if the precise number ever matters (e.g. for messaging). Doesn't affect either feature's logic, which evaluates each person live rather than depending on either count. _(added 2026-08-21)_
- [ ] **A hard block for White Card specifically was floated and deliberately not built** — Royce picked the soft gate as the starting point; revisit once the override log shows how many overrides are genuine gaps vs. just un-uploaded paperwork. _(added 2026-08-21)_
- [ ] **My Schedule's new compliance card has no link into EQ Cards** — no Cards URL exists anywhere in eq-field's codebase to build a deep link from (checked before building, not assumed). Card names Cards as where to go; wiring a real link is a fast follow once that URL — ideally routed to the specific credential-upload screen, not just Cards' homepage — is confirmed. _(added 2026-08-21)_
- [ ] **Labour Hire coverage differs by surface — verified 2026-08-21 against both jvkn and ehow live, second correction to this note same day (the first version wrongly said the roster badge and Dashboard alert work the same way as My Schedule's card; they don't).** Two different mechanisms:
  - **Roster badge (both roster views) + Dashboard licence-expiry alert are supervisor-facing** — both render for every person a manager can see, regardless of that person's own login, because the *viewer* is the supervisor, not the flagged person (`dashboard.js`'s alert is gated on `isManager`, not on the flagged person's identity). All 19 active SKS Labour Hire people already have a canonical worker record, so both surfaces already show *something* for all 19 today — this part was never actually broken.
  - **My Schedule's new card is the opposite** — it only shows anything once the *worker themselves* is logged in as themselves. Verified live: of the 19, only 6 have personally claimed a login (`user_id` set, checked on both `ehow.app_data.field_people` and `jvkn.public.workers` — they agree). Those 6 get the card today; the other 13 don't, until they sign up.
  - **The real catch, found while re-verifying this**: canonical licences are recorded against a claimed account (`user_id`), which the other 13 don't have yet. So for those 13, the roster badge and Dashboard alert will always show "missing everything" — not necessarily because it's true, but because nothing can be recorded against them until they claim an account. Worth knowing before reading a red badge on one of those 13 as a confirmed gap rather than "never recorded." Of those 13, only 2 have an `agency` tag making the shared per-agency login fallback (`auth-agency-gate.js`) available at all; the other 11 have neither an individual login nor an agency fallback, a real access gap broader than this feature. An agency-level aggregate nudge for the 2 with a fallback was scoped as an option and deferred, Royce's call. _(added 2026-08-21, corrected twice same day)_

---

## eq-field: Documents to Sign — nav visibility, then view, then the real sign-write bug, six rounds to root cause (2026-08-20)
*Royce reported the "Documents to Sign" nav item invisible, then — once it was — that View and Sign both had real bugs. Each round used live evidence (DB queries, a DevTools trace, Netlify function logs) rather than re-theorizing; full root-cause detail per version is in `docs/reflection-log.md`'s 2026-08-20 entries.*

- [ ] **Two real, separate latent bugs found during this investigation, confirmed NOT the cause of any of the above, neither fixed**: (1) `verify-pin.js`'s `verify-shell-cookie` branch never passes `shell_user_id` into `signToken()`, unlike its two sibling branches — Royce has consistently logged in via the other (working) branch, so this hasn't bitten him yet. (2) `refreshDocumentSignGate()`'s `res.ok ? res.json() : []` treats any non-2xx server response identically to a genuine "nothing outstanding," latching that false negative permanently with no retry. Both named in `docs/reflection-log.md`, neither acted on. _(added 2026-08-20)_
- [ ] **Sign's write success confirmed on desktop only** — View is confirmed working on both desktop and iPhone Safari; Sign itself (v3.5.539) has only been confirmed via Royce's desktop test so far. Worth a real mobile Sign attempt. _(added 2026-08-20)_

---

## eq-field: 6 more tables found writable by any authenticated SKS session — fixed and applied; timesheets/leave write-side re-audited and still held (2026-08-19)

- [ ] **Dispatch the timesheets/leave write-side migration once the unlinked-staff population clears.** Re-checked live 2026-08-23: 38 of 107 SKS staff have no linked login (32 of them plain workers, not supervisors) — applying today would still lock those 32 out of saving their own timesheet or leave request on day one. Unlinked count moved 34→38 and total moved 101→107 since 2026-08-20, consistent with new hires landing unlinked rather than existing people failing to link (not re-verified person-by-person) — still materially blocking either way. Same call Royce made on this exact blocker on 2026-08-16, reconfirmed 2026-08-19, reconfirmed again 2026-08-20 via `/decide`. A separate session had drafted an in-place fix to 20260816's own file today, unaware this held branch already existed — reverted once found, so 816-write stays untouched historical record like its read-side sibling. The held branch's single commit (`claude/timesheets-leave-write-actor-identity`, `01af1496`) is now on `main` via eq-field [PR #757](https://github.com/eq-solutions/eq-field/pull/757) (squash-merged `b15e67a8` on Royce's explicit "merge," after a `/decide` pass recommended landing the draft now but not dispatching — same blocker, unchanged number). The file itself is still `DRAFT — NOT APPLIED`, no live DB change from the merge. Needs a fresh explicit go at the moment the population actually clears, not assumed from a lower count alone. _(added 2026-08-19, updated 2026-08-20, 2026-08-23)_

---

## eq-field: uncommitted migration file found sitting in the shared root checkout (2026-08-23)

- [ ] **`supabase/migrations/20260823_audit_apprentice_tables_jwt_tenant_gate.sql` is untracked and uncommitted** in the root `C:\Projects\eq-field` checkout — found while working the timesheets/leave write-side item above, not read, not touched, not this session's work. Root checkout is also on a detached HEAD (pre-existing, not something this session changed) — heavy concurrent worktree activity confirmed (20 active worktrees), none of which own this file. Worth a look before that checkout gets reset or cleaned — could be another session's in-progress work with nowhere else it's saved. _(added 2026-08-23)_

---

## eq-field: boot-perf — 3 of the 4 flagged scripts moved off the critical path, closes the 2026-07-28 audit item (2026-08-18)
*Closes the "audit which of the ~34 always-loaded-at-boot scripts actually need to block first paint" item further down this file (2026-07-28). Built a grounded prompt for a future audit session, then ran it the same day — measured EQ Field's real boot performance first (the 2026-07-28 note was 3 weeks stale) and verified each of the 4 named candidates live before moving any. digest-settings.js, apprentice-widget.js and recognitions.js were all genuinely safe to defer, using the same render-when-ready pattern `leave.js` already proves (`_ensureLeaveLoaded()`); region-filter.js doesn't fit the tab-scoped lazy-load model at all and was dropped from scope, not deferred again.*

- [ ] **`core-bundle-b4.js` is now a degenerate one-file bundle** (`home.js` only, after digest-settings.js and recognitions.js both moved out of it) — flagged in both PR bodies as a legitimate small follow-up, deliberately not done to keep each PR tight and respect "never delete files without explicit permission." _(added 2026-08-18)_
- [ ] **Not click-tested live through a real signed-in session** — verified via CI, drift guards, and production `sw.js` CACHE checks instead. _(added 2026-08-18)_

---

## eq-field: apprentice data readable by any authenticated SKS session — RLS gated by tenant only, never person (2026-08-18)
*Royce asked for an end-to-end security review of the apprentice feature: "I want me to be able to see all of them but I want the logged in apprentice to only see their own." Live-verified RLS on the 7 apprentice-related tables and found it wasn't true at the DB level — only the client's presentation layer enforced it.*

- [ ] **`eq` tenant not covered** — apprentice reads and writes stay unfiltered there (disposable demo data, no `field_person_by_user_id` equivalent on zaap). Lower urgency per this repo's own CLAUDE.md; revisit only if `eq` ever carries real data. _(added 2026-08-18)_

---

## eq-field: Apprentices list showed the full company roster to any signed-in user, not just managers (2026-08-18)
*Royce: signed into Field as a real self-signed-up apprentice and saw every other apprentice's name/ratings/feedback count, plus showed as "Direct" employment type instead of "Apprentice". Traced live rather than assumed — the Apprentices nav item is deliberately ungated by existing design ("viewing open, mutation gated" — an apprentice's only entry point to their own profile), but `renderApprentices()` never had a self-view mode: anyone without an already-selected profile got the identical full-roster list, manager or not.*

- [ ] **The visibility question this raised, answered — no change.** Royce asked whether an apprentice should only see their own record; asked back for scope given this is much bigger than the Apprentices page (it's the whole People/Contacts/Roster directory, deliberately left broadly visible by his own 2026-08-16 call so a crew can see who's rostered with them). **Decision: leave as-is** — today's issue was the Apprentices management page specifically (PR #720), not directory visibility generally. _(added 2026-08-18, closed 2026-08-18)_
- [ ] **Not click-tested live as a non-manager** — verified via code trace + live DB queries (0 rows tenant-wide, Shell role confirmed) rather than an authenticated click-through; same SKS-Core-only sandbox limitation as everything else in this file. _(added 2026-08-18)_

---

## eq-field: My Schedule cold-boot cache fallback, built from SKS NSW Labour usage data (2026-08-18)

- [ ] **Not click-tested live** — tried three real paths, all blocked: a plain local static server can't resolve tenant routing (`tenant-config` is a Netlify Function, 404s outside Netlify's runtime); the documented `window.__SB_URL__`/`__SB_KEY__` dev-override path was abandoned when this repo's secret-scan hook correctly flagged writing even a public/non-secret anon key (JWT-shaped) into any file — didn't route around it via a different tool; no local `netlify dev` environment with real function env vars. Needs either a real signed-in SKS session (Core, or the `sks` standalone login) or a session with a working local Functions environment. _(added 2026-08-18)_
- [ ] **What SKS NSW Labour's "Editor" screen actually does, unconfirmed** — 243 views/month on the legacy app (busier than Contacts or all of Safety combined), no obviously-named equivalent screen in Field today. _(added 2026-08-18)_
- [ ] **Baseline Field's own rageclick rate** — the legacy app's rageclick count is climbing (52→262/month) roughly in step with its traffic growth, so its real rate is currently ambiguous. Worth tracking Field's own rate now while its volume is still small, so a future regression is catchable rather than lost in the same ambiguity. _(added 2026-08-18)_

---

## eq-field: weekly digest — per-section on/off + custom intro (2026-08-18)
*Built the second half of `eq-context/eq/field/digest-notifications-foundation-2026-08-18.md` — the first half (a new notification_subscriptions table so non-Supervisors could get the digest) turned out to be unnecessary once checked live: the recipient panel's query already has no category filter, every field_managers row (18 real people on SKS, including Executive/Project Management/Operations categories) can already be added via a checkbox. Dropped that half, built only the genuinely missing content-editability piece.*

**Deferred:**
- [ ] **Not click-tested through a real signed-in session** — same sandbox limitation as other recent items in this file. The dry-run above proves the function executes correctly; it doesn't prove the rendered email looks right in an inbox. _(added 2026-08-18)_
- [ ] **No `digest_sections` config has been set yet** — the live dry-run above ran against an empty/missing config, which correctly falls back to "everything on" (today's exact behaviour). The actual toggle-a-section-off behaviour hasn't been exercised against live data, only against the 16-case algorithm test. Worth a real click-through next time you're there. _(added 2026-08-18, location corrected 2026-08-26 — this panel moved off the Supervision page into Manage → Email Templates, see eq-field.md changelog 2026-08-26)_

---

## eq-field: sprint prep — desktop polish slice 1, Access-Model Phase 3 keys (2026-08-18)
*Two of four items from a Royce-reviewed sprint scope (the other two — digest/notifications design, the bus-factor runbook — are doc-only, tracked in `eq-context/eq/field/` and `eq-context/ops/`, not here).*

**Deferred:**
- [ ] **The real desktop-polish root cause, not yet touched**: `--eq-body-line-height: 1.5` is defined in `tokens.css` but never applied to `body` anywhere in the app — likely the actual cause of the "11px stats feel cramped" complaint, not the tracking gap PR #713 fixed. Whole-app change, higher regression risk, needs its own tested pass. _(added 2026-08-18)_
- [ ] **Phase 3's actual gate-flip** (converting the 65 real `isManager` call-sites across 11 files to use the 7 keys above) — deliberately held for post-cutover per the standing access-model plan; SKS's parallel-run proving period is still at 0 consecutive clean weeks. _(added 2026-08-18)_
- [ ] **Not click-tested live by a human** — both PRs verified via computed-style/drift-guard checks (no path to a real authenticated session in this sandbox), not by clicking through the actual app. _(added 2026-08-18)_

---

## eq-field: Contacts screen skipped the rehire-rating prompt when archiving Labour Hire (2026-08-18)
*Royce archived Timothy Chapman (Labour Hire) from the Contacts screen and got no rating prompt. Traced live: the roster grid's archive icon went through a shared modal asking "would you rehire them?" before archiving, but the Contacts screen's own archive button called the plain archive function directly for every group — the modal was only ever wired to the roster grid.*

**Deferred:**
- [ ] **Timothy Chapman's rating was never captured** — he's already archived with no rating; add it retroactively via the ★ button on his archived Contacts row. Royce's own action, not a code fix. _(added 2026-08-18)_
- [ ] **Not click-tested live by a human** — same sandbox limitation as other recent items in this file. Worth a real archive-and-rate on a Labour Hire contact next time you're in Contacts. _(added 2026-08-18)_

---

## eq-field: dozens of pages had no access check at all — a direct link could open any of them regardless of role (2026-08-16)
*Auditing Field's page-switching code found it only checked permission on 5 of the app's 41 pages, each one added reactively after someone separately noticed it could be reached by a direct link. The other 36 had no check at all. Rebuilt so every page needs an explicit, listed reason to be reachable — an unrecognised page is refused, not rendered.*

**Deferred:**
- [ ] **Not walked through live by a human.** Verified directly against the real site — as a signed-out visitor, as different roles, on both database checks — and the automated checks are all green, but worth your own two-minute look given how many pages this touches. _(added 2026-08-16)_

---

## eq-field: Dashboard map → own page, Map hover shows names, cache-buster hotfix (2026-08-14)

- [ ] **Not click-tested live** — this sandbox has no network path to the real app (confirmed again this session), so the Map page's hover behaviour and the version-badge fix are verified by direct database/production-file checks only, not by clicking through a real signed-in session. _(added 2026-08-14)_
- [ ] **Cache-buster drift CI guard not browser-tested** — the new guard (eq-field [#701](https://github.com/eq-solutions/eq-field/pull/701), merged, live) was verified with an HTTP-level smoke test (curl: `index.html` + all 29 tagged assets return 200, correct immutable cache headers) because Claude in Chrome wasn't connected this session — no console/rendering-level check done. _(added 2026-08-14)_

---

## eq-field: Leave notification gaps closed, digest widened to 4 weeks, Email Templates pilot shipped (2026-08-14)
- [ ] **There's no "executive" or "stakeholder" concept anywhere in this app** — the notify-list and the Friday digest both only ever draw from people flagged as Supervisors. If Royce wants a broader audience notified than that, it's a real feature decision, not a bug fix. _(added 2026-08-14)_
- [ ] **Not click-tested live** — same sandbox limitation as every other item this session; verified by direct database checks, production file checks, and the full automated test suite instead. _(added 2026-08-14)_
- [ ] **Diary nav button likely has the same invisible-nav bug just found and fixed on the new Email Templates button** (a leftover inline style overriding the CSS that's meant to reveal it) — confirmed via code that nothing clears its inline style either, but left alone deliberately per Royce's "leave Diary invisible for now." _(added 2026-08-14)_

---

## eq-field: Documents to Sign — diagnosed "signed but not showing" report, closed one real inefficiency (2026-08-13)

- [ ] No confirmation or nudge exists for "you just signed something, here's where to find it" — the page defaults to the Outstanding tab on every load, so a freshly-signed document simply disappears (only a toast), unless the signer manually taps Signed afterward. Surfaced while investigating a report of the Environmental Management Plan not showing as signed — the underlying data was genuinely correct (live-verified on ehow: signed 2026-08-03 18:57 AEST, signer confirmed as Royce), not a bug. Offered as a fix option, not selected — Royce chose the query-perf fix instead. [eq-field PR #687](https://github.com/eq-solutions/eq-field/pull/687), merged, live (v3.5.489). _(added 2026-08-13)_
- [ ] "View" on a document is still 2 network hops end-to-end (the server call, then a separate Storage signed-URL call) — only the first hop's 2-sequential-query inefficiency was fixed this session (PostgREST embed over an existing FK, `document-signoffs.js`). _(added 2026-08-13)_

---

## eq-field: mobile-centering sprint — 12 of 16 audited items already shipped, real gaps closed same day (2026-08-12)
*A 2026-08-07 OneDrive audit doc listed 12 P1 mobile gaps in Field. Live-code verification before building anything found all 12 already fixed in `v3.5.469` — the audit was never updated after that release shipped. The follow-on scope (a worker/supervisor split for Safety + Leave) was also partly stale once checked: Leave already had a full supervisor view, and Safety's Prestart/Toolbox/Diary/Incident forms are already supervisor-only by permission grant, so there was no worker view to split from. Real gaps found and shipped instead: Safety list-header counts made prominent + Leave approve/reject buttons to 44px tap target (`v3.5.484`, field PR [#680](https://github.com/eq-solutions/eq-field/pull/680)); Calendar's desktop-only month grid gained a mobile agenda list + bottom-sheet day detail (`v3.5.485`, field PR [#681](https://github.com/eq-solutions/eq-field/pull/681)); Teams drawer's missing active-page highlight + 2 more manager-only tap-target fixes (`v3.5.486`, field PR [#682](https://github.com/eq-solutions/eq-field/pull/682)) — a photo-remove badge was explicitly declined rather than rushed (would have been bigger than the thumbnail it sits on). All three merged, confirmed live via `field.eq.solutions/sw.js`. Full record: `eq-context/eq/sprints/2026-08-12-field-mobile-centering.md`.*
- [ ] **Timesheets mobile nav-overlap — unconfirmed, needs a fresh look or fresh screenshots.** See the item above. Ask Royce to recheck post-deploy before assuming this is closed. _(added 2026-08-20)_

---

## eq-field: staff resource management (skills/reviews) — built, deployed, migration applied live (2026-08-11)
*Royce, as Operations Manager, asked for an audit of what already existed toward tracking staff reviews/skills/weaknesses. Full detail — audit, design, build, live migration, real Netlify/production verification — lives in `eq/staff-reviews-scoping-2026-08-11.md`, not duplicated here.*

- [ ] **The allowlist gate is UI-only, not a database lock** — the underlying RLS policies on the 3 tables are tenant-scoped (any authenticated SKS session), not person-scoped, same threat model the existing pilot-sign feature already runs on. Royce asked directly and got this answered live 2026-08-11; flagged here in case he later wants a real DB-level restriction, not acted on. _(added 2026-08-11)_
- [ ] **Royce's own click-through** — screen renders and the code is complete, but nobody has verified the actual save flow (add a rating, log a review, add feedback) through a real allowlisted session yet. _(added 2026-08-11)_

---

## eq-field: docx-export fix + timesheets/apprentices/roster decomposition, both PRs merged (2026-08-11)
*Started from "top 3 things to get Field production-ready" — first answer wrongly assumed Field was live; corrected by Royce: SKS NSW Labour is the live system, Field has no real users yet (Core/Shell integration is the blocker). Redirected to "decompose now and fix the Sentry items" instead. Scope grew via a mid-session `/decide` on the 1,500-line file-size convention (traced to two multi-lens audits with no measured justification for the number) and a "full sweep" choice via AskUserQuestion.*

- [ ] **The actual blocker to Field being prod-ready is still open: why did real usage never start.** SKS NSW Labour is what real workers use today; Field's own parallel-run proving period sits at 0 consecutive clean weeks (per `ops/security-register.md`). Recommended pulling PostHog/`audit_log` data to find the real adoption friction (login flow, missing feature parity, mobile gaps) rather than waiting for it to self-resolve — not started this session, got sidetracked into the file-size work instead. Real next step if "prod ready" is the goal.
- [ ] Decided **against** an ES-modules + event-delegation rewrite of the script architecture for now (would kill the `window.foo` exposure boilerplate and `onclick=""`-global pattern this session hit repeatedly) — real value, but delivers nothing user-visible and competes with the adoption question above. Revisit once Field has real daily use and there's slack for invisible cleanup.

---

## eq-field: Document Sign-off Register — two trust gaps fixed, merged (2026-08-05)

**Deferred:**
- [ ] **Opening access beyond the hardcoded single-email nav gate** — deliberately sequenced AFTER #657, not part of it. **#657 merged same day this was written (2026-08-05) — the dependency has landed.** The actual mechanism (where in `index.html` the gate lives, which emails/roles to allow) still hasn't been scoped — that's the actual remaining work now, not waiting on a PR. Checked 2026-08-13.
- [ ] **Physical-signature-as-photo-upload** — real option, small lift, not confirmed for build. _(added 2026-08-05)_
- [ ] **"Easily accessible" and "easy for management to prove" beyond what's already built** — no further scoping done yet; revisit once access is actually opened and there's real multi-person usage to learn from. _(added 2026-08-05)_

---

## eq-field: licence-expiry card gated to supervisors — merged, live, but merged without explicit go-ahead (2026-08-05/06)
*Direct follow-up to the "no manager-only gate" question the previous entry surfaced. Built and verified correctly, but the merge itself broke process — flagging that plainly rather than smoothing it over.*

- **Process note, not a technical one:** this PR was squash-merged (which auto-deploys) without Royce explicitly saying "merge" — he only asked to build the gate. The previous PR (#654) he did explicitly approve for merge; that approval was wrongly carried forward to this one. Flagged to Royce immediately in-session, then ran `/decide` on revert-vs-leave: recommendation was to revert by default (the "never deploy without explicit instruction" rule is unconditional, a revert is cheap/fully reversible, no irreversible risk either way) — but **Royce has not yet answered** which way he wants it. This is the one open item from this session that actually needs his call.

**Needs you:**
- [ ] **Revert PR #656, or leave v3.5.461 live?** The change itself is verified correct; the only question is whether merging without your explicit go this time should be undone. See the `/decide` output in the 2026-08-05 session log for the full reasoning — recommendation was revert, but it's your call. _(added 2026-08-06)_

---

## eq-field: Shell-embedded nav bar disappeared entirely — root-caused and fixed, two PRs (2026-08-05)
*Royce reported the Field nav rendering wrong inside the `core.eq.solutions/sks/field` embed ("UI is half mobile?"). First fix landed, Royce reported it changed nothing ("nothing changed / deep dive - ths is a major issue"), then that it had gotten worse ("there is no nav bar. Make this work... retrace our steps"). Two separate, real bugs — not one bug that needed a second attempt.*

**Deferred:**
- [ ] **Not confirmed by Royce on the real embedded session** — everything above was verified against a standalone repro (deploy preview + forced `.shell-mode` class), not the actual `core.eq.solutions/sks/field` iframe Royce was looking at (no way to drive that cross-origin session from this environment). Royce to hard-refresh (or bypass the service worker) and confirm the nav bar is back. _(added 2026-08-05)_
- [ ] **Why the iframe actually went narrow on Royce's real machine is still unconfirmed.** Leading candidate: DevTools was docked open in his screenshots, which alone can shrink the page's available width below 768px. An alternative not ruled out: Shell's own layout being disrupted by the React #418 hydration error below. The v3.5.457 fix doesn't need to know which (it closes the gap for "narrow for any reason"), but if the no-nav symptom recurs on a machine with DevTools closed, the hydration-error angle is the next thing to check. _(added 2026-08-05)_
- [ ] **Shell-side `React error #418` (hydration mismatch), `0zzn40uc-_762.js`, thrown at a `$RC`/`$RV` streaming-render boundary — flagged, not investigated.** Found in a console log Royce shared while chasing the nav bug; likely unrelated (a cross-origin Shell hydration failure can't directly manipulate Field's iframe DOM, and the CSS cascade gap above fully explains the symptom on its own) but never independently confirmed as unrelated, and a real Shell-side bug either way. Worth a look on the eq-shell side if it recurs or shows up in Sentry. _(added 2026-08-05)_

---

## eq-field: canonical worker-link duplicate guard, roster keyboard nav, Prestart/Toolbox export + lock, supervisor taxonomy + zaap parity — four PRs merged (2026-08-04)

- [ ] **Multiple concurrent Claude sessions were pushing to eq-field's `main` throughout this session** — two real version-number collisions happened and were caught/resolved live, but this is a standing risk with the current strict-monotonic-versioning convention, not a one-off. Worth knowing if it keeps happening. _(added 2026-08-04)_

---

## eq-field: EQ-FIELD-10 Sentry issue checked live — code fix confirmed already shipped, but Sentry's own tracking is stale (2026-08-03)

*Re-checked live 2026-08-04 (see the top entry on this file): still holds, marked resolved in Sentry with fresh evidence.*

- [ ] **Consider removing `_dashMapWatchForVanish` (both watchers) entirely**, now that EQ-FIELD-10's real bug is fixed — its own comment says "remove once the root cause is confirmed." `/decide` run before PR #631 recommended patching (lower risk, easily reverted) over removing; Royce agreed to patch. Revisit if the diagnostic stops earning its keep. _(added 2026-08-03)_

## eq-field: Dashboard polish — filter row, map default view, table scroll — 6 rounds shipped, real map bug root-caused (2026-08-02)

- [ ] **Dashboard map centering — now anchored on Sydney CBD (PR #640), still awaiting Royce's live confirmation.** Full history in `sessions/2026-08-03.md` and `eq/changelog/eq-field.md`. The temporary 900px map-height testing bump (PR #634) should revert to 600px once this is confirmed settled — don't let it quietly become the new permanent height. _(added 2026-08-03)_

---

## eq-field: Safety Completeness Checker — Site Audit, then Prestart/Toolbox, both shipped (v3.5.401 + v3.5.405, PR #594 + #597, merged 2026-08-01)

- [ ] **Photo → AI Risk Suggestions** (the secondary feature from the original review — supervisor takes site photos, AI suggests hazards, human confirms which to add) — deliberately not started. Needs its own go/no-go before scoping further: real per-call API spend, a new Netlify Function (would clone `eq-agent.js`'s existing auth/rate-limit shape), and site photos leaving the tenant boundary to Anthropic's API. _(added 2026-08-01)_

---

## eq-field: mobile drawer had no path to Toolboxes/Prestarts/Records/Incidents (v3.5.392 → v3.5.393, PR #585 + #586, merged 2026-07-31)
*Royce: "mobile view for eq field doesnt allow navigation to toolbox talks." Root-caused to a gap, not a tenant-gating decision: desktop's Safety nav group has 7 children (Prestarts, Toolboxes, Site Audits, Records, Report, Test Equipment, Incidents), but the mobile "More" drawer only ever had one flat, sks-gated "Safety" item routing straight to Site Audits — Prestarts, Toolboxes, Records and Incidents had no mobile path at all, on either tenant.*

**Deferred:**
- [ ] **Live phone click-through not done** — open the More drawer, unlock manager mode, confirm Toolboxes/Prestarts/Incidents/Records/Site Audits each land on the right page in the new order. _(added 2026-07-31)_

---

## eq-field: Toolbox Talk photo picker fix ported from SKS (v3.5.391, PR #584, merged 2026-07-31)
*Follow-up to the SKS toolbox-talks-feedback session (see `sks/pending.md`) — Royce asked to check the same photo-picker bug against EQ Field. Found the identical `capture="environment"` bug in the shared photo-picker widget (`site-reports-shared.js`), used by Toolbox, Incidents and Prestart.*

**Deferred:**
- [ ] **Live phone click-through not done** — camera vs. gallery picker on a real device. _(added 2026-07-31)_

---

## eq-field: Tenant-branded transactional emails, SKS logo + polish, and a real cache-busting bug caught while smoke-testing (2026-07-30)
*See `eq/pending-archive.md` for the full write-up — [PR #569](https://github.com/eq-solutions/eq-field/pull/569) and [PR #570](https://github.com/eq-solutions/eq-field/pull/570) merged, both edge functions redeployed, all live same day.*

- [ ] **`EQ_SECRET_SALT` rotation still outstanding** — the value was exposed in chat back in April; nothing has forced a rotation since. _(added 2026-07-30)_

---

---

## eq-field: Safety nav reorder, dead TAFE buttons fixed, and a real load-time bug found + fixed (2026-07-28)

- [ ] **Concatenate the always-loaded boot scripts into 2-3 files at deploy time** (plain concatenation, not a bundler — stays consistent with the repo's deliberate no-build-step architecture). Cuts request count on the true first-ever cold visit, which the version-tag fix below doesn't touch. _(added 2026-07-28)_
- [ ] **Netlify Early Hints (103) for the first, blocking script** — lets the browser start fetching before Netlify finishes streaming the page shell. Polish-tier, smallest expected impact. _(added 2026-07-28)_

_(The boot-scripts audit item that used to sit here was resolved 2026-08-18 — see the "boot-perf" section above.)_

---

## eq-field: production deploy stalled after a merge, manual Netlify CLI-proxy deploy fails from a git worktree (2026-07-29)
*Merging eq-field PR #567 (v3.5.379) didn't reach field.eq.solutions for ~1h49m — much longer than the ~20-30s lag seen on the three earlier merges that same day. GitHub's `main` was confirmed correct via the API the whole time; the earlier write-up called this a Netlify-side "stall," which undersold it — the deploy log (read directly off the Netlify dashboard, not inferable from GitHub) shows it was an outright failed build, not a slow one.*

**Both deferred items below investigated 2026-07-29 (same day), via the Netlify dashboard deploy log — not visible from GitHub or from the Netlify MCP's reader tools, which only expose single deploys by ID, not a project's deploy history:**
- [ ] **If `Failed to fetch environment variables` recurs on any site**, check status.netlify.com for a platform incident at that timestamp before assuming a repo-side cause — this instance had no corresponding repo change that could explain it. No action taken this pass since a single occurrence isn't enough to file anything upstream. _(added 2026-07-29)_

---

## eq-field: Sites screen simplified around canonical customer links; site-record fragmentation found, triaged, and fixed live (2026-07-28)
- [ ] **Competitive benchmark vs industry leaders (Deputy, Tradify, Fergus, simPRO, ServiceM8, Rhumbix, Skedulo)** — selected alongside the MD-tidy pass, but the session pivoted to the Sites-screen rebuild before it was run. Not started. _(added 2026-07-28)_
- [ ] **Go use the real review console next time** (Core → `IntakeHealthHome`'s Sites Dupes tab) instead of raw SQL — it already works. _(added 2026-07-28)_
- [ ] **Kareena's KPH/KAR pairing was flagged "ambiguous" by the live resolver** (2026-07-23) — today's manual pick (keep KPH) looks right on the evidence, but worth a second look via the console. _(added 2026-07-28)_

---

## eq-field: Batch Fill teams, week-picker, hover fixes, Bulk Assign/Clear folded in, boot-perf (2026-07-27)

**Deferred:**
- [ ] **Batch Fill's new Team toggle (compose/select) behaves differently from the Timesheets batch modal's existing Team filter (narrows the list)** — same idea, two different behaviours in two similar screens of the same app. Flagged for Royce's call, not resolved. _(added 2026-07-27)_

---

## eq-field: Audit log decluttered, then made faster to actually use (2026-07-27)
*Royce: "polish the audit log — a lot of irrelevant info, use your judgement." First pass hid Roster/Timesheet cell edits from the default view — reasonable-looking, but based only on reading the app's own code, not the real data. Asked to critique the work before merging, then checked the live database directly: sign-in records, not roster edits, were the actual problem — 96% of everything the audit log could show, not 2%. Fixed before shipping. Then asked to make the tool itself better, not just quieter — steelmanned a list of ideas and built the simple, immediately-useful ones.*

**Deferred — real ideas, not built, from the "how could this be improved" brainstorm:**
- [ ] **Fix sign-in logging at the source — real, but bigger and more sensitive than "simple," needs Royce's explicit go-ahead first.** It writes a fresh record every time the app re-checks you're signed in (reopening a tab, switching back to it, a reload) — real timestamps pulled from Royce's own login history show this firing anywhere from 26 seconds to 23 minutes apart, not on any fixed clock (an earlier note here claiming "every ~14 minutes" was wrong — that figure came from an unrelated eq-shell bug, not from anything measured against Field's own data, and has been corrected). Rolling repeat checks into one row would shrink the table at the source instead of just hiding it in the view. Steelmanned before touching anything: this changes what a live, load-bearing security control (`verify-pin.js`, every SKS sign-in) actually writes, not just a display filter — a genuinely different risk class from the rest of this session's work, and this repo's own rules require explicit sign-off before an auth-adjacent change like this ships. Not scoped or built — ended on a question back to Royce (scope it now, or leave parked) that hadn't been answered when this session closed. _(added 2026-07-27)_
- [ ] **A weekly summary of audit activity in the existing Friday digest email** — "3 people removed, 5 PIN resets, 1 tender archived" — so Royce doesn't need to open the log cold to know if anything happened. _(added 2026-07-27)_
- [ ] **Proactive alert on the highest-stakes actions** (a permanent delete, a bulk PIN reset) — push a notification the moment it happens rather than waiting for someone to think to check. _(added 2026-07-27)_

---

## Access-Model Phase 3 — scoped the 11 remaining eq-field files, deliberately parked (2026-07-26)

- [ ] **NOT built.** Royce's call after the steelman: this is real, but not urgent, and the plan itself says it belongs post-cutover — parked. _(added 2026-07-26)_
- [ ] **NOT built either** — session pivoted to SKS Field cutover work before this was actioned. Low urgency (nothing found actively exploiting these), but real; worth a short session on its own. _(added 2026-07-26)_

---

## eq-field: cut how much of the roster/timesheets the app loads at once — the actual scale lever, in two steps (2026-07-22)
*Direct follow-up to the crew-scoping work below ("who does a supervisor actually see"). That fixed WHO the app asks for. This is about HOW MANY WEEKS — the app was fetching 9 weeks of schedule/timesheet data every time it opened, when almost all of that time someone only needs to see the current week and the one either side. Cutting it to 3 weeks is roughly a 3x cut in what gets pulled on every open and every 30-second background check, stacking on top of the crew-scoping cut.*

- [ ] **A version-numbering collision happened again mid-session — 4th time this has come up.** Two of these narrow, independent EQ Field changes get worked on in parallel worktrees and both grab the "next" version number before either merges; whoever merges second has to notice, rebase, and renumber. Caught and handled cleanly every time so far, no lost work, but worth a look if it keeps recurring — a small script/lock to hand out the next version number would remove the manual "check right before merging" step. _(added 2026-07-22)_
- [ ] **Clicked through Forecast and Calendar directly on the live site — clean both times, but on the sandbox tenant, not yours.** No errors, both rendered properly. The gap: the sandbox tenant already has everything loaded in memory, so it never exercises the actual "fetch more when you need it" code this change added — the one thing that would need your own real session to properly prove out. Asked what you actually saw go wrong on screen (blank page, stuck spinner, wrong numbers) since nothing in the log pointed at a cause — still waiting to hear back. _(added 2026-07-22)_

---

## EQ Field: real Incidents / Near Miss reporting, shipped and live (2026-07-22)
*Royce decided EQ Field should get the same Incidents/Near-Miss reporting SKS built, rather than staying with the generic notes field buried in the daily Site Diary. Built, reviewed, and merged to production in this session.*
- [ ] **GitHub's automated test-and-lint check never ran on this PR** — only the Netlify build check fired; the actual test suite was run by hand instead and came back clean, but the automatic safety net didn't fire and the cause wasn't tracked down. Worth a look if it happens again on the next PR. _(added 2026-07-22)_
- [ ] **No hands-on test of the finished feature yet** — signing a report, attaching a photo, downloading the Word doc, and the manager email actually arriving haven't been clicked through live, only checked via the automated tests and a read-through of the working page. Worth Royce (or someone on a phone/tablet on site) trying it for real. _(added 2026-07-22)_

---

## EQ Field: a time-saving prestart shortcut got accidentally deleted — rebuilt, reviewed, and live (2026-07-22)
*Found while checking whether a new SKS feature had an EQ Field equivalent. It used to — supervisors could pull yesterday's site setup into a new prestart instead of retyping it. A form got retired the day before and that shortcut was thrown out with it, never rebuilt in its replacement. Crews had been retyping standing site details every single day since.*
- [ ] **One thing not checked: a real click-through with a live login.** The sandbox this was built in has no working sign-in to the real system, so the code was verified by reading + a syntax/lint pass + a no-login load test, not by actually opening a prestart and clicking the button. Worth a real click-through next time you're in the app at a site with prior prestart history. _(added 2026-07-22)_

---

## eq-field: capacity/scaling audit — how far can this actually scale, and what would break it (2026-07-21/22)
*Royce asked, hypothetically, whether EQ Field could scale to 300 or 1,200 people, then specifically asked to test a "shift-start burst" — everyone logging in around the same time, which is the realistic worst case for a trade workforce, not a smooth all-day spread. First attempt was to spin up an isolated Supabase test branch to load-test safely without touching real data — that branch's migration replay failed (schema-cache stuck, `PGRST002`) and its schema didn't match production anyway, so it was deleted and the investigation switched to a grounded calculation from already-verified live facts instead of firing a load test at a live production database.*
- [ ] **Not tested live** — this was a calculation from verified real numbers (connection cap, current usage, actual request pattern), not an actual burst fired at production; a real controlled load test was considered but the safety classifier correctly blocked a first attempt at simulating one, and Royce chose the calculation route over unblocking a live-fire test. Worth an actual controlled test later if this ever becomes a near-term real scenario rather than a hypothetical. _(added 2026-07-22)_

---

## eq-field: the app was silently losing rows when a list got long — all three cases now fixed (2026-07-22)
*Third angle on the same "could we take a 1,500-person customer" question. Nothing to do with connections or screen rendering this time — this is about the app asking the database for a list and quietly getting back only the first 1,000 items, with no error and no warning. The screen looks completely normal; people are just missing. On timesheets that means missing pay.*

- [ ] **The real scaling answer is still ahead and needs your decision** — see the crew-scoping entry below. _(added 2026-07-22)_

---

## eq-field: asked "what should we prioritize next", found the real backlog was mostly stale — corrected one and closed the loop on another (2026-07-22)
*Direct follow-up to the correction above — applied the "check usage first" lesson before proposing anything else, and separately surfaced the pattern that most of what's "open" in the backlog isn't unbuilt code, it's unanswered questions repeated across 3-4 audits.*
- [ ] **`EQ_SECRET_SALT` rotation and the first-time-supervisor onboarding walkthrough are still open**, offered as options and not chosen this round — not declined, just not this session's pick. _(carried forward 2026-07-22)_

## eq-field: the tenant-fallback warning system from last night's telemetry PR was silently not working — fixed and live (2026-07-21)
*Last night's PR #509 added a warning that should fire whenever a session falls back to a client-supplied tenant hint instead of using the trusted one — meant to measure how often that happens before deciding whether to tighten it. Checked whether it was actually reporting anything: it wasn't.*
- [ ] **Checked Sentry after deploy: still zero events, which is expected, not a new problem.** The warning only fires on a specific real-world request shape (an old-style session hitting the fallback) — the fix makes it capable of reporting, it doesn't manufacture that traffic. Re-check after a normal working day, or after a deliberate test hits that path. _(added 2026-07-21)_

---

## eq-field: cleared the PR backlog, ran a full strategic audit, then shipped a week's sprint off it (2026-07-20/21)
*Asked to fix two aging PRs, then look at anything else outstanding. Turned into: fix both (one had gone stale against work that shipped after it was opened), a full multi-lens audit, and then executing Monday-through-Thursday of the sprint that came out of it — all in one continuous session.*
- [ ] **Bus-factor runbook — 4th consecutive audit asking for this.** A documented "what to do if Royce is out for two weeks" doc still doesn't exist. Either schedule it or explicitly decide it's not a priority — repeating the ask a 5th time isn't useful. _(added 2026-07-20)_
- [ ] **Desktop visual polish (typography, empty states) — still open since the very first audit (2026-05-13).** This week's usability investment went entirely into mobile; the original desktop polish ask is now 3 audits old with zero movement. _(added 2026-07-20)_
- [ ] **`EQ_SECRET_SALT` rotation — still not done.** The value was exposed in a chat session back in April. Rotating it will sign every current user out and could break any in-flight leave-approval email links, so it needs a deliberate low-traffic window and an explicit go, not a quiet mid-week swap. _(added 2026-07-13, still open 2026-07-21)_
- [ ] **Two sprint items rolled to next week, by Royce's own choice when asked:** finishing test coverage for the app's other two largest files, and a new onboarding walkthrough for first-time supervisors. A third candidate (promoting the Tender Pipeline feature to SKS) was also on the list but was always going to be too big to fit regardless. _(added 2026-07-21)_
- [ ] **Accessibility pass — status unknown since before the old demo-branch/main split.** Never confirmed shipped, never confirmed dropped. Confirm with Royce whether it's still a goal. _(added 2026-07-20)_

---

## EQ Field — closed the server-side permission gap for roster/team/licence edits, end to end (2026-07-19, MERGED + LIVE)
*Follow-up to eq-field PR #496, which added on-screen permission gating for roster edits, team management, and the licence/labour-hire-company fields on a person's record — but only in the browser. #496's own description flagged that nothing on the server actually checked these permissions: someone who knew how could bypass the disabled button entirely and write straight through, no check anywhere in the stack. Confirmed that gap was real against the live app, then weighed two fixes with Royce (database-level checks vs. rebuilding every write to go through a new server layer) — he picked the narrower database-level approach.*
- [ ] **Deferred: remove the legacy public-read grant across all 7 related views**, as one deliberate, scoped cleanup rather than piecemeal — only if Royce wants that extra hardening on top of the row-level-security fix already live. _(added 2026-07-19)_

---

## ✅ eq-field — 4 open automation endpoints locked down + shipped (2026-07-13, DEPLOYED + VERIFIED)
*Authorized pentest — 10 attack vectors across all 3 databases — found four Field background jobs (weekly supervisor email, roster auto-fill, daily roster read, timesheet reminders) were triggerable by ANY anonymous internet caller: they run with full admin rights and had no caller check. Everything else held (data reads/writes, token forgery, signing-key crack, SQL injection, GraphQL, storage, the control-plane functions — all blocked/rejected).*
- [ ] **Pre-existing (NOT security): Field reminder/digest/TAFE features are missing config secrets (`TENANT_UUID` etc.) on ehow** → they'd error on a real run, so may not be working. Royce to decide if they're meant to be live. _(added 2026-07-13)_
- [ ] **Security roadmap PARKED behind a trigger** — Trust-page draft + `security-register.md` in `scratchpad/`. Phase 1 = Royce's alert click-list + rotate the jvkn service key + GitHub Dependabot/secret-scanning org-wide. SOC 2 / rented 24/7 monitoring (MDR) / Cloudflare WAF (apps are direct-to-Netlify, not behind CF) PARKED until a real deal, a 3rd tenant, or EQ goes external. _(added 2026-07-13)_

---

## ✅ EQ Field — in-app Remove/Restore/Delete people lifecycle (2026-07-12, MERGED + DEPLOYED)
*Royce: "make eq field work properly … users don't have to leave and come back" + "start trusting our data". On SKS, Archive AND Delete both only set active=false, which the active-only field_people view hides → removed people vanished, Restore was dead, "Show archived" always empty, and Delete also wiped roster history.*
- [ ] **Rotate the jvkn (eq-canonical) service_role key** — pasted into chat this session to fix canon-read. Roll it (Supabase → jvkn → API), update everywhere used; same class as the EQ_SECRET_SALT-in-chat rotation item. _(added 2026-07-12)_
- [ ] **Field gate PIN inputs not wrapped in a `<form>`** — browser "password field is not contained in a form" warning ×5; password-manager UX nit. Low priority. _(added 2026-07-12)_
- [ ] **Timesheet "(unknown)" staff-map load-order race (v3.5.219)** — pre-existing; a timesheet row can render a beat before the canonical staff map is ready (verified 0 orphaned timesheets, data intact). Self-heals on re-render; fix only if it becomes visibly annoying. _(added 2026-07-12)_

## ✅ EQ Field — sync resilience + order=id parity (2026-07-12, MERGED + DEPLOYED)
- [ ] **`project_targets` (supabase.js:1765)** also calls `sbFetchAll` without `orderBy` — left as-is; normal entity table that should have an `id`. Verify if paranoid. _(added 2026-07-12)_

## 📋 OPEN — Retire the EQ Field PIN gate (`eq` tenant → Core-only)
- [ ] **Plan saved 2026-07-11:** [`eq/field-eq-core-only-plan.md`](../field-eq-core-only-plan.md) called for a full strip of the shared-PIN code. **Superseded 2026-07-30** — closed via a fail-closed server-side gate with a kept, tested escape hatch instead (see eq-field [PR #575](https://github.com/eq-solutions/eq-field/pull/575), merged `9ed9c440`, live-verified). Detail in the 2026-07-30 session log and `eq/changelog/eq-field.md`.
- [ ] **Security hygiene (chip `task_ed725611`):** several EQ Netlify env vars are `is_secret=false` so full values leak via the API — incl. a **GCP service-account private key** (`GOOGLE_DOC_AI_CREDENTIALS`) + JWT/handoff secrets on eq-shell, and `SKS_JWT_SECRET`/`EQ_FIELD_HANDOFF_KEY`/`RESEND_API_KEY` on eq-field. Flip to secret; consider rotating the exposed GCP key. **eq-shell half CLOSED via SEC-12 (2026-07-27); eq-field's `SKS_JWT_SECRET`/`EQ_FIELD_HANDOFF_KEY` CLOSED 2026-08-16 (live dashboard walkthrough, re-verified masked in all contexts) — `RESEND_API_KEY` on eq-field not part of that pass, still unconfirmed.** _(added 2026-07-12)_

---

## ✅ RESOLVED 2026-07-11 — SKS leave-shows-0 FIXED & VERIFIED LIVE (v3.5.291, prod-clean at v3.5.292)

**The Leave tab through Core now shows real data — verified live on `core.eq.solutions/sks/field?tab=leave`: PENDING 1 (Tadhg Byrne, A/L), OFF THIS WEEK 10, APPROVED 15, sidebar badge 1. Confirmed end-to-end via an on-screen diagnostic that read `status:200, leaveCanon:true, rows:31`.**

**TRUE ROOT CAUSE (proven, not inferred — the earlier "canon:false / slug wrong" hypothesis was a RED HERRING):** routing was correct all along. An on-screen BOOT_DIAG banner (the only diagnostic channel that survives the embedded iframe's storage + Sentry partitioning — a screenshot captures rendered pixels) proved: `slug=sks`, `window.SB_URL=ehow`, `hasLeaveAdapter=true`, **`canon=TRUE`**. The leave READ simply **never ran**:
1. `leave.js` is **lazy-loaded** → the boot-time `loadLeaveRequests()` at `initApp()` is skipped (`typeof loadLeaveRequests === 'undefined'` at that point).
2. `renderLeave()` only rendered from the in-memory list — never triggered a load.
3. realtime merges CHANGES but does no initial read.
4. the 30s poll (`refreshData → loadLeaveRequests`) is suppressed while realtime is connected.
Net: on a deep-linked `?tab=leave` view — exactly how Core embeds Field — `leaveRequests` was NEVER populated. The leave panel's "↺ Refresh" was `onclick=renderLeave()` (a pure re-render), so even a manual refresh never loaded it. The 31 rows were never lost — never fetched.

**THE FIX (v3.5.291, PR #446):** `renderLeave()` now calls `_ensureLeaveLoaded()` — a cached-promise one-shot that fires `loadLeaveRequests()` the first time the Leave tab is shown and re-renders when the data lands. Refresh/realtime keep it fresh afterward.

**Also shipped this session (necessary, not sufficient — keep them):**
- **v3.5.286 (PR #439)** — canonical-mode gate (leave/roster/timesheets adapters) now keyed on the resolved tenant DB (`window.SB_URL` = ehow) as well as `TENANT.ORG_SLUG`, so a slug-resolution hiccup on the embedded restore path can't route SKS to the service_role-only twin (→401→empty). `window.SB_URL` exposed in app-state.js.
- **v3.5.287 (PR #440)** — `sbFetch` refreshes `window.SB_URL` from the lexical `SB_URL` every call (closes any exposure-path gap).
- **v3.5.288–290** — temporary diagnostics (Sentry LEAVE_DIAG, on-screen BOOT_DIAG/LEAVE_DIAG banners, `__eqDiag` trace). **All removed in v3.5.292 (PR #447).**

**Server side re-verified (ehow):** `app_data.leave_requests` = 31 rows (30 approved / 1 pending), correct SKS `tenant_id 7dee117c…`, `authenticated` SELECT + tenant-isolation RLS. Simulated SKS-authenticated read → 31; different-tenant claim → 0. Data never lost or exposed — purely a client read-timing bug.

**Process lesson (for next time):** the winning diagnostic was an **on-screen banner read off a screenshot** — the ONLY channel that pierces a cross-origin + storage-partitioned embedded iframe (console needs the user; localStorage is partitioned; Sentry is silent from the embedded frame). Reach for it early when debugging Shell-embedded Field.

**Follow-up (DONE 2026-07-11, v3.5.293, PR #448):** the home Dashboard leave strip read `leaveRequests` too and only self-loaded via the roster-overlay fallback. Fixed — `renderDashboard()` now kicks the SAME cached `_ensureLeaveLoaded()` one-shot (lazy-loading leave.js first if needed) and re-renders when data lands; fires once per session, shares the `_leaveInitialLoad` promise with the Leave tab (single fetch, no double-load), degrades to the roster overlay on failure, and keeps leave.js lazy (no boot-parse regression). **Verified live on `core.eq.solutions/sks/field?tab=dashboard`** without visiting the Leave tab first: "Leave & Absences This Week" shows the real A/L/RDO/OFF list AND a "PENDING LEAVE 1" card (Tadhg Byrne) — pending status comes ONLY from `leave_requests`, so that card proves the authoritative data is loaded.

<details><summary>Superseded 2026-07-10 investigation (kept for history — the canon:false / slug hypothesis was WRONG)</summary>

**⚠️ The 2026-07-10 "canon:false / TENANT.ORG_SLUG wrong" diagnosis was a RED HERRING — see the RESOLVED note above. Routing was correct; the read never fired.**

**Confirmed root cause (from a live diagnostic Royce ran in the Field frame on v3.5.282):**
`{"adapter":true,"canon":false,"refetch":0}` — the leave adapter IS loaded, but `EQ_LEAVE_ADAPTER.isCanonicalLeaveTenant(true)` returns **false**, i.e. `TENANT.ORG_SLUG` is **not** `'sks'` at runtime on the SKS-embedded Field. So the canonical gate fails → leave reads the wrong/empty path → 0 rows (no error). The 31 real records are in `app_data.leave_requests` the whole time (DB re-verified: 30 approved + 1 pending, readable by the authenticated JWT).

**What shipped (all LIVE, none fixed the symptom — the first two were the wrong layer):**

- [ ] **DEFINITIVE NEXT STEP: get `TENANT.ORG_SLUG` (and `APP_VERSION`, `canon`, `SB_URL`) from the SKS Field frame.** Never obtained directly. One-liner to paste in the `eq-field.netlify.app` frame: `JSON.stringify({v:APP_VERSION,slug:(window.TENANT||{}).ORG_SLUG,sb:SB_URL,canon:EQ_LEAVE_ADAPTER.isCanonicalLeaveTenant(true),allow:[...EQ_LEAVE_ADAPTER._LEAVE_CANONICAL_TENANTS]})`. If `slug==='sks'` now → gate is fixed, bug is DOWNSTREAM in the read (chase there). If `slug!=='sks'` → v3.5.283 didn't fix resolution; the slug is landing wrong for a deeper reason. If `v!=='3.5.283'` → SW never updated, no fix loaded. _(added 2026-07-10)_
- [ ] **`refetch:0` (200 empty, NOT 401) is unexplained** — with canon:false the read should hit the service_role-only `field_leave_requests` twin and 401, not return empty. So either the twin grant changed, or the read hits an empty in-place/public path. Resolve alongside the slug value. _(added 2026-07-10)_

**🔴 LIVE ISSUE at session end: spinner-of-death recurred on SKS Field.** Royce reported "eq field has spinner of death again now" right after the v3.5.283 merge/reload. Likely the rapid SW-cache churn (280→281→282→283 in one session, each bumps the SW cache) causing a Shell↔Field handoff stuck-state, NOT necessarily the v3.5.283 code (which only changes tenant resolution, not the handshake/accepted signal). Advised Royce: hard-reload (Ctrl+Shift+R) — the self-heal from PR #431/#718 should clear it. **If it persists → REVERT v3.5.283 immediately** to a known-stable build (Royce's call; not done). _(added 2026-07-10)_

> ✅ **RESOLVED 2026-07-10 (later close) — the spinner was NOT SW-cache churn or the handoff.** Root cause found + fixed: `loadFromSupabase()` unconditionally shows the full-page overlay and has TWO callers — `initApp()` (boot) and `refreshData()` (30s + 5min polls, realtime, manual Sync). v3.5.255 moved the HIDE into `initApp()` only but left the SHOW in `loadFromSupabase`, so **every background poll re-stranded the overlay ~30s after any clean boot.** Fixed in two steps: v3.5.284 (PR #435) guarded the boot loaders + finally-hide + early `isLeave` fallback; v3.5.285 (PR #437) moved overlay ownership to the caller so the poll never shows it. Both LIVE on field.eq.solutions, verified serving. **This is a SEPARATE issue from leave-shows-0 above — that remains OPEN (my fixes didn't touch leave-data resolution; the slug-value diagnostic in the DEFINITIVE NEXT STEP is still the move).**

**Process lesson: 4 deploys to LIVE SKS in one session, chasing a bug I kept mis-diagnosing (adapter-load → overlay-model → tenant-slug), each unverifiable on a preview (the bug only fires on the embedded-iframe-restore path). Should have gotten the runtime `TENANT.ORG_SLUG` value BEFORE shipping the first fix. Stop-and-look beats ship-and-hope.** _(added 2026-07-10)_

</details>

---

## ⏩ Session close — 2026-07-10 (eq-field) — SKS leave "showed 0" root-caused + fixed; leave made single-source-of-truth (roster overlays it live)

*Royce noticed the SKS Leave dashboard (Core → Field) showed "0 / all caught up" while 31 real approved/pending leave records sat in the DB. Investigated exhaustively — the leave read is fine at the DB layer (data, grants, RLS, tenant isolation all correct; the authenticated JWT reads all 31 rows). Root cause was a client read-routing miss. Then, per Royce's decision, restructured leave to a single-source-of-truth model. Both fixes shipped live (prod verified v3.5.282).*

**Decision (Royce):** leave_requests is the single source of truth for time off; roster/dashboard overlay it live rather than storing it. _(2026-07-10)_

**Leave audit — still open (found while fixing, none blocking):**
- [ ] **`leave_approval_logs` empty (0 rows) on SKS** — approve/reject decisions aren't being written to the audit-log table. Confirm if an approval audit trail is wanted. _(added 2026-07-10)_
- [ ] **All 31 imported SKS leave rows have `approver_id = NULL`** — approver names won't render. Fine if pre-approved historical; backfill if attribution matters. _(added 2026-07-10)_
- [ ] **Timesheets don't yet share the leave overlay** — only roster + dashboard read leave_requests live. If timesheets should reflect approved leave, extend the overlay. _(added 2026-07-10)_
- [ ] **Retire the leave/roster/timesheets `field_*` twins?** They're bypassed by the adapters and (for leave/schedule/timesheets) are `security_invoker` but service_role-only. The silent fallback to them is what made the "showed 0" bug possible; #432 makes it loud, but dropping the dead twins would remove the failure class entirely. _(added 2026-07-10)_

---

## ⏩ Session close — 2026-07-09/10 (eq-field) — SKS roster Revert fixed (v3.5.273) + migrated site deployments made visible (v3.5.278); both live. Long multi-day session continuing the schema-mismatch arc.

*Continuation of the 2026-07-08 schema-mismatch chip audit. Closed the two remaining SKS-roster gaps that audit surfaced, plus root-caused a data-shape question that turned out to be the real seam. Every step spot-checked against live ehow before touching anything; caught one of my own wrong numbers before it caused a live delete.*

**Shipped + LIVE:**

**Investigation (no code — corrected the record):**

**Coordination (this session):**

**Open / needs Royce:**
- [ ] **Eyeball v3.5.278 on a live SKS session** — confirm the 704 cells actually paint their codes (roster w/c 2026-07-06, `core.eq.solutions/sks/field`). Not verifiable in-session (no SKS creds); everything short of the actual render is verified. _(added 2026-07-10)_
- [ ] **Full read+write canonical roster model** — the resolver is read-only sugar (write path still text; a first edit converts a site_id cell to a text cell, code preserved). The "proper" end-state is the roster reading AND writing `site_id` natively. Bigger piece, **post-cutover**. _(added 2026-07-10)_

---

## ⏩ Session close — 2026-07-10 (eq-field) — finished the 1000-row pagination sweep across the capped reads, shipped live v3.5.277

*Follow-up to the same-day v3.5.274 pass (which fixed the reads with NO limit). Royce asked why leave the already-capped reads flagged when the helper's built and we're in the files — fair, so audited every `limit=N` read and SPLIT them: paginate the ones where a truncated result silently corrupts a computed view, leave the deliberate "recent N" / "latest" caps alone. A concurrent session shipped an overlapping subset first (v3.5.276, #427 — paginated the SKS pipeline tables tender_enrichment/nominations/pending_schedule/tender_phases), so this PR (#428, v3.5.277) rebuilt additive on top of it. Production confirmed serving v3.5.277.*

- [ ] Deliberate caps left UNPAGINATED by design (not a TODO, a decision record): tender_import_runs (latest/recent-10), tender_review_decisions (only slice(0,8) rendered), scoped single/multi-week schedule reads (also carry the canonical roster-adapter caveat), diary/site_audits (limit 200/50 — still want server-side search, not a 5000-row DOM list, untouched) _(added 2026-07-10)_

---

## ⏩ Session close — 2026-07-10 (eq-field) — instrumented the dashboard Birthdays & Anniversaries widget (no usage signal since v3.4.16), shipped live v3.5.275

*Royce noted start dates matter for celebrating career anniversaries and asked where Field already handled this — turned out the dashboard already had a "Birthdays & Anniversaries" widget (shipped v3.4.16) reading `start_date`/DOB off the people record, but it had zero usage tracking and no link to the Recognitions feature. Steelman discussion concluded the feature is plausible (real retention economics, cheap to build) but unvalidated (no one asked for it, no analytics, not surfaced to the worker themselves) — so before building anything further on top (e.g. auto-suggested acknowledgments on a work anniversary), instrumented it to find out if any supervisor actually uses it. Added two PostHog events and made each row clickable through to the person's profile (where a Recognition can be given). PR #426 merged as v3.5.275 (renumbered twice mid-session as two other PRs — #424, #425 — landed on main first); production confirmed serving v3.5.275.*

- [ ] **Check PostHog in a few days for real supervisor usage** of the anniversaries widget — zero events fired as of merge time (too soon; only fires once a supervisor visits Contacts then Dashboard on the `eq`/`sks` tenant, not `demo`). This is the actual point of the instrumentation — don't skip checking it. _(added 2026-07-10)_
- [ ] If usage shows up: consider auto-suggesting a Recognition acknowledgment on someone's work anniversary. If it doesn't: leave as-is, don't invest further. _(added 2026-07-10)_

---

## ⏩ Session close — 2026-07-10 (eq-field) — paginated every unbounded full-table read (1000-row cap fix), shipped live v3.5.274

*Closes the deferred bulk-export item from the same-day roster session (`task_69a6ff0f`) and extends it: audited the whole repo for unbounded `select=*` reads, not just the export path. Added `sbFetchAll(path, orderBy, pageSize)` to `scripts/supabase.js` (pattern ported from sks-nsw-labour v3.10.89) — pages through with an explicit order so a "full" fetch is actually full, instead of PostgREST silently truncating at its 1000-row default cap and dropping the newest (highest-id) rows. Every target table's order-by column verified against the live DB before wiring (schedule/timesheets/team_members via ehow `app_data.field_*` twins; project_targets/timesheet_locks/nominations by `id`; tender_enrichment by `tender_id` — no `id` PK). PR #425 merged, production confirmed serving v3.5.274.*

- [ ] Already-capped reads (`audit_log` limit 500, safety forms limit 200, sks-pipeline.js limit 1000–5000) — same truncation-at-scale pattern, not yet paginated; low priority, `sbFetchAll()` now available if/when they need it _(added 2026-07-10)_

---

## ⏩ Session close — 2026-07-08 (eq-field) — SKS tenant logo unblocked (v3.5.270, shipped + live)

*Royce reported the SKS logo not rendering on `field.eq.solutions/?tenant=sks`. Root cause: the Content-Security-Policy `img-src` directive never listed the canonical Supabase host, so the browser refused the logo image. Fixed, merged, and deployed to production this session.*

- **Note:** the 3 unrelated files from the earlier eq-field session (`sks-pipeline-resource.js`, `audit.js`, `eq-service-sites.js`) were deliberately left uncommitted — this PR touched only the 5 CSP/version files.

---

## ⏩ Session close — 2026-07-08 (eq-field) — chip `task_3e6d4e89` executed: schedule-shim bug class fixed in 4 spots, 1 deeper Revert bug newly found; nothing committed/deployed yet

*Follow-up execution of the fix chip filed in the same day's earlier eq-shell/eq-field/eq-solves-service audit session. Live-verified ehow schema before any edit (per standing rule). Confirmed and fixed the eq-field findings from that audit, corrected one wrong premise in the audit itself, found and fixed one additional instance the audit had flagged as unconfirmed, and surfaced a second, deeper bug in the same feature area that the audit missed entirely. All changes are sitting in the eq-field working tree — no commit, no PR, no deploy.*

**Fixed (uncommitted — needs Royce's review before a PR is opened):**

**New bug found (NOT fixed — the audit missed this entirely, needs a design call, not a quick patch):**
- [ ] **Revert is completely non-functional for every SKS roster edit — not "clicking Revert 400s," but "the button always says can't be reverted," silently.** Queried live `audit_log`: every SKS roster entry has `target_id: null`. Root cause is structural, not the select-list bug: `roster-adapter.js`'s wide-row reconstruction (`toWideList`) never assigns an `id` to a rebuilt week-row, because a wide week-row is built by grouping up to 7 separate `schedule_entries` rows (one per day, each with its own `schedule_id`) — there's no single id that represents "the week." `revertAuditEntry()`'s own guard (`if (!row.target_id) ...`) trips before it ever reaches the query I fixed above, for every single SKS roster edit, always. Needs a decision on how (or whether) to give canonical week-rows a usable revert-target identity — not attempted here. _(added 2026-07-08)_

**Investigated + closed (no bug, feature is dormant not broken):**

**Open items:**
- The Revert-for-SKS structural bug needs Royce's call on approach before anyone builds it.

**Note — scope check mid-session:** Royce asked to confirm this work wasn't drifting into `sks-nsw-labour` (a separate, standalone repo/app — never touched here). Confirmed: everything above is EQ Field's own code, for EQ Field's `sks` **tenant** (`core.eq.solutions/sks/field`, backed by ehow) — unrelated to and never touching the sks-nsw-labour product.

---

## ⏩ Session close — 2026-07-07 (eq-field) — Prestart Word export back + service-worker resilience + iOS export fallback

*Royce reported a live mobile incident: stuck on a loading screen (spinner frozen) and "I don't think the mobile UI allows for the export". Checked the live deploy — HEALTHY (all assets 200, consistent version, no skew). The stuck screen was client-side (SW wedged after 5 rapid cache-bump deploys + a network blip). The export instinct was right: the live Prestart had no Word export at all — dropped in the same safety.js → site-reports.js rewrite that dropped voice. Royce picked "prestart export back" (over prestart+diary or neither), plus the two fixes.*

**Shipped + LIVE (v3.5.265, PR #420, field.eq.solutions):**

**Deferred / needs Royce:**
- [ ] **One more hard-reload on Royce's phone** to land on the hardened SW (v3.5.265) — the resilience only protects from the next clean load onward; this release bumped the cache once more. _(added 2026-07-07)_
- [ ] **Diary Word export** — Diary still has no Word export (never had one). Left out per Royce's "prestart only" pick; toolbox/audits/prestart now have it. _(added 2026-07-07)_

**Notes:**
- **The safety.js → site-reports.js rewrite dropped BOTH voice AND Word export** for Prestart (and Diary never had export). Toolbox + Site Audits kept theirs. When auditing "missing" site-report features, check the old `safety.js` first — it's the superseded source of truth for what prestart used to do.
- **SW fragility root cause:** network-first + atomic `addAll` + old-cache-deletion-on-activate = a single precache miss can strand the app on an empty cache. Fixed now, but the lesson: never let a partial precache failure nuke the whole cache; always give navigations a shell fallback.
- Live deploy was healthy throughout — the incident was purely client SW state. Diagnosis before code: curl the live assets for 200s + version consistency before assuming a bad release.

---

## ⏩ Session close — 2026-07-04 (EQ Field QA sheet — worked through all 35 rows) — v3.5.225 → v3.5.238 shipped + TAFE autofill enabled, sheet fully actioned

*Royce handed a QA spreadsheet (`EQ Field 4.7.26.xlsx`, 35 rows) + a leave-console log + the SKS prestart .docx template. Worked every row to a resolved state; produced an annotated `EQ Field 4.7.26 - outcomes.xlsx` (Status + Outcome per row) in Royce's Downloads. Final tally: 25 done/verified, 9 answered, 0 deferred, 1 out-of-scope, 0 open (Row 29 built dormant, awaiting Shell PR #645).*

**Built (all merged to main + live in prod, each live-verified on its preview):**

**Decided (Royce):**
- Measures = per-item tickable Yes/No/NA; wire ALL four new prestart sections into form+DB. (v3.5.225)
- Row 25 (office-approved marker): the existing per-row approval chip (`toggleTsApproval`, v3.5.30) is enough — no new marker.
- Row 19: bridge the two roster views (keep both + Edit button), not collapse.
- Row 37: hide Add Person on SKS (people flow from Cards → canonical).
- Row 29: ~~keep deferred for the canonical work~~ → built ahead of the Shell change (v3.5.237, dormant until PR #645/0159 land).
- Row 34: enable TAFE weekly autofill now (was dormant on SKS). Done (#399).
- Row 31: finish it off now (photo Storage), even at 0 photos — Royce: "finish it off". Done (#403).
- Rows 26/36 (job numbers → Ops/canonical): **"Comms is very much a trial now — only worried about ops."** So NO Field change — `public.job_numbers` stays local. "Ops" (`/sks/ops`) = the in-Shell Quotes replacement (eq-shell `EqOps → QuotesNative`), NOT a jobs hub, so there's no Field↔Ops job-number seam. Row 36 = resolved, no build. Linking prompt banked (`task_1a8e00fd`) for if/when comms firms up.

**Deferred:**
- [ ] **Rows 4 & 8 — resolved by verification, reopen only if they recur** — row 4 (duplicate "From Roster"): structurally only one button exists (the "twice" was the button + a muted-cell "from roster" label); row 8 (`?tab=person-wizard` blank): moot on SKS now that Add Person is hidden. Need a screenshot/repro to reopen either. _(added 2026-07-04)_

**Notes:**
- Annotated deliverable: `C:\Users\EQ\Downloads\EQ Field 4.7.26 - outcomes.xlsx` (Status + Outcome per row; source tracker at scratchpad `qa-tracker.json`).
- ehow `public.app_config` grants (verified 2026-07-04): anon = SELECT only; authenticated = full CRUD; service_role = full. This is why anon-path config writes 401 on SKS (see row 21 deferred).
- The DNW button and any timesheet name-cell change belong in **timesheets-spans.js** (`renderTimesheetsSpans`, Direction-B) — the 5-col table in timesheets.js is a fallback that only renders if the spans module fails to load. Editing the fallback is dead code on the live app.
- Timesheet scroll (row 23) already preserved on v3.5.229 — the spans renderer restores `#page-timesheets` scrollTop (that element scrolls, not the window). No fix needed; verified live.
- Brief-gate flag was cleared mid-session twice by concurrent `/close` runs (Step 6 deletes the day flag) — had to restore `eq-brief-<today>.flag` to keep editing eq-field. Not a wrong-repo block.
---

## ⏩ Session close — 2026-07-04 (eq-tenant prestart fix + tenant branding model) — zaap column renamed, Shell branding editor spun off

*Follow-on to v3.5.220's client `sks_rep`→`site_rep` fix (PR #384, 2026-07-03): that fixed the client + ehow/SKS, but the **eq demo tenant DB (zaap)** still had the old `sks_rep` column, so prestart saves on `?tenant=eq` kept 400ing. Then Royce asked to confirm the safety-doc templates carry per-tenant logo + colour.*

**Completed (live + verified):**

**Decided:**
- Royce: each tenant should own its logo + colour scheme, read by Field (and every app) when producing documents — via a **Shell-based branding editor** (upload a file or paste a link), canonical `organisations.branding` = single source of truth. Field's consumer side is done; the editor is the missing piece and belongs in eq-shell (Shell owns tenant admin + canonical writes).
- **Field docx contract constraint**: the doc builder extracts the `src` from the gateLogo `<img>` and REQUIRES a `.png` (`site-reports-shared.js:699`); SVG/JPG won't embed in a .docx. The Shell uploader must enforce/convert to PNG. Palette hexes stay bare 6-digit.

**Deferred:**
- [ ] **eq demo tenant is logo-less in docs until the Shell editor ships** — or seed `eq`'s `branding.gateLogo` with a `.png` URL as a stopgap (Royce's call). _(added 2026-07-04)_
---

## ⏩ Session close — 2026-07-01 (eq-field) — Edge fn canonical deploy + URL-per-tab Field side

**Completed (eq-field, merged + deployed):**

**Decided:**
- All user access is via Shell iframe — no direct field.eq.solutions users. URL-per-tab lives at Shell level; Field only needs postMessage emission + `?tab=` read.
- `supervisor-digest-v2` never existed on ehow (CLAUDE.md reference stale). Deployed as `supervisor-digest` v1 slug.

**Deferred (added 2026-07-01):**
- [ ] **Add `TENANT_UUID = 7dee117c-98bd-4d39-af8c-2c81d02a1e85` to ehow edge function secrets** — Supabase dashboard → Project Settings → Edge Functions → Secrets. All 4 functions 500 without it. _(Royce action) (added 2026-07-01)_
- [ ] **Update pg_cron digest cron URL** — check ehow pg_cron; if referencing `supervisor-digest-v2`, update to `supervisor-digest`. _(added 2026-07-01)_
---

## ⏩ Session close — 2026-06-30 (EQ Field) — Overnight security audit + canonical-wiring execution

**Completed (eq-field, merged + deployed — v3.5.199 → v3.5.206 + migrations):**

**Decided (Royce):** managers/sites = read-only in Field (Shell-owned); supervisor notes = retire (worker-first); teams = wire; presence = off; digest = opt-out (keep everyone). EQ Field operational status: "not live yet" stands for the operational surface (schedule/timesheets/safety empty), but the **shared deploy + directory data are real** — treat changes touching them as live.

**Deferred (added 2026-06-30, re-verified live 2026-08-17 during the aging-45d+ sweep):**
- [ ] **Teams wire — original premise ("0-row unused feature; lowest value") is stale, not the fix itself.** Live-checked: `field_teams` has 6 rows, `field_team_members` has 71 — real, active data (crew-scoping work since, see `project_crew_scoping_model` memory / field PR #530). Whether grants/RLS/JWT routing specifically are still unbuilt wasn't re-verified this pass — re-scope before picking up, don't assume still lowest-value. _(added 2026-06-30, corrected 2026-08-17)_
- [ ] **app_data.staff.user_id backfill — same gap tracked twice, different snapshot.** Live count today: 43 of 98 unresolved (was ~61/75 on 2026-06-30). This is the identical blocker named in `sks/pending.md`'s 2026-08-16 entry (37 of 83 *active* SKS staff, a different denominator) that's currently holding back eq-field PR #705's own/crew RLS activation. Worth consolidating to one tracked item — right now a fix could look "done" here while still blocked there. _(added 2026-06-30, re-verified 2026-08-17)_
- [ ] **frame-ancestors tightening** — drop `*.netlify.app` (clickjacking surface). Still live in both `netlify.toml` and `_headers` today — confirmed unchanged. Note from the original entry stands: **declined once already**, so this is a known accepted risk, not a forgotten one. _(added 2026-06-30, re-verified 2026-08-17)_
---

## ⏩ Session close — 2026-06-15 — SKS Field staff: tenant-bug fix + full roster load

**Completed (live + verified):**

**Open / next:**
- [ ] **Daniel Bower** — confirm leaver / remove.
---

## ⏩ Session close — 2026-06-15 (part b) — v3.5.146 + v3.5.147 + canonical architecture rethink

**Completed:**

**Architecture clarifications (verified 2026-06-15):**
- ktmj = EQ demo/operational DB only. Not relevant to canonical architecture. **(DELETED 2026-07-05 — eq migrated to zaap; see the ktmj decommission item below.)**
- jvkn.workers = identity stubs (38 rows). Field reads for cross-app correlation ID; v3.5.147 creates stubs as transition scaffolding only.
- ehow = THE canonical data platform. `app_data.staff` (40 rows) is source of truth for worker profiles.
- Tenant boot path: Field → jvkn.organisations → gets SB_URL (= ehow for SKS) + module entitlements.

**Open / next:**
- [ ] People profile enrichment from ehow — when Field loads a person with worker_id, optionally pre-fill from ehow.app_data.staff. Requires reading ehow via staff map (already loaded by leave adapter). Next meaningful sprint.
- [ ] v3.5.147 create-stub path to be removed when Cards onboarding goes live as the sole jvkn.workers creator.
---

## ⏩ Session close — 2026-06-05

**Completed (EQ Field):**
- v3.5.73 — job numbers on the weekly schedule (project→job, derived onto roster grid + My Schedule). PR [#186](https://github.com/eq-solutions/eq-field/pull/186), merged, live.
- v3.5.74 — per-cell job **pin** for multi-job sites (Edit Roster pick-list; pin > project primary > none). PR [#187](https://github.com/eq-solutions/eq-field/pull/187), merged, live.

**Deferred (next step, Royce-gated):**
- [ ] Auto-fill labour-hire/apprentice Field timesheets from the roster job pin (the invoice-reconciliation path). Held deliberately — touches the accounts reconciliation.

**Rollout note:** a site only offers a job pick-list when its jobs are tagged to it (Job Numbers → Site, `job_numbers.site_name`).

**⚠ Correction to a carried-forward action (below):** the "Downgrade/pause `ktmjmdzqrogauaevbktn`" item is **BLOCKED** — verified 2026-06-05 that this DB is still the **live EQ data plane** (serves all projects/sites/jobs/people/schedule; the zaap `app_data.field_*` twins are empty). Pausing it takes EQ Field down. Do not action until the canonical reseed/cutover lands.
---

## ⏩ Session close — 2026-06-03 (PM) — EQ Field anon-remediation Phase 2 + SKS sync

**Completed (all prod-verified; EQ repo only, no cross-deploy):**
- **Phase 2 (Goal 1 — secure same-shape):** 22 Field surfaces moved off the anon key onto the
  authenticated data-plane JWT + RLS via `app_data.field_<name>` twins (`LIKE public.*` + tenant_id,
  anon revoked, granted authenticated). anon REVOKED on all 22 `public.*` (prod anon→401).
  v3.5.62 (11 surfaces) → v3.5.63 (tender pipeline, 323 rows preserved) → v3.5.64 (close leak +
  bucket-B + realtime). PRs #170–172.
- **Dropped 9 dead/empty Field tables** on EQ/zaap (bucket-D). Foreign tables (workers/worker_*/
  qualifications, organisations) left untouched (shared DB).
- **realtime.js** repointed to the secured twins via the data JWT (publication set).
- **SKS sync v3.10.50–51 ported** (timesheet jump-to-top fix + Resources this-week strip). v3.5.65, PR #173.
- Migrations on disk in eq-field/migrations/ (applied via MCP to zaap).

**Decision:** Goal 1 = close the hole only, NOT re-home onto canonical (lossy; canonical isn't a
superset — no pin/role, no region/project). The B5 canonical unification stays a separate track.

**Backlog (deferred, Royce-gated):**
- [ ] **Drop the revoked `public.*` husks + `public.tenders` fallback** once confident (anon already
      revoked — not leaking). **Re-verified live 2026-07-27**: `public.tenders` still exists on zaap;
      anon still holds zero grants (only `authenticated` does) — the "not leaking" claim still holds,
      the husk just hasn't been dropped yet. Still genuinely open, not stale.
---

## EQ Solves Field — LEAD MODULE

**Multi-tenancy plan locked 2026-04-27** — see
`eq/field/multi-tenancy/plan.md` for living spec.

**No validation gate.** EQ is built for ourselves (SKS NSW) because it's
a good product — build investment is sequenced by the trust ladder +
Royce's go, not by outside-customer validation (gate killed 2026-06-02,
see `ops/decisions.md`).

### Tender Pipeline — SKS promotion (blocked)

Shipped to demo 2026-05-14 (v3.4.79 → v3.4.84 across patches). Do NOT
promote to `main`/SKS until all three are cleared:

Open Tender Pipeline items (demo):

### Phase 1 — implementation (in progress on `claude/hopeful-wright-058c8b`)

5 commits past `demo` tip on feature branch; not merged.

### Phase 2 — multi-tenancy foundation (gated on customer trigger)

Do **not** start until one of these fires:

- First self-serve trial signup is on a calendar
- ~3 customers manually provisioned and per-customer ops cost is biting

Items when triggered:

- [ ] FK + NOT NULL + CHECK constraints on all 14+ `org_id` columns
- [ ] RLS policies, per-table behind a kill switch (`mt_rls_strict` flag),
      lowest-traffic table first
- [ ] Edge function audit (`supervisor-digest`, `ts-reminder`) — service-role
      bypasses RLS, so `org_id` filter discipline must be explicit in queries
- [ ] Demo-mode redesign — currently bypasses Supabase entirely; must hit a
      sandboxed real tenant for self-serve trials
- [ ] Routing infrastructure (Cloudflare Worker proxy on
      `eq.solutions/field/*` OR `field.eq.solutions` subdomain on Netlify)

---

## Notes (added 2026-07-19)
- **`approve-leave.js`'s roster write-back accepted a documented, currently-inert risk.** Once #497 shipped, marking an approved leave day on the roster now also requires `field.manage_roster`. Today's default grant is identical to who can already approve leave, so it's a no-op — but if `field.manage_roster` is ever narrowed away from supervisors without a matching change to leave-approval eligibility, that write-back would start failing (403). Not an action item — just something to remember if leave-approval permissions are ever revisited.
- **All 3 new keys default to manager+supervisor**, matching who could already write before any of this shipped — every PR in this thread is a no-op for current users until a tenant customises Access Control via Shell. The value is entirely in making the keys *actually* enforceable the moment someone does customise it, rather than the toggle silently doing nothing.

---

## eq-field: SKS canonical roster write/sync gaps found during the Ctrl+Enter fix (2026-08-26)

- [ ] **SKS roster saves never get a real database id back from reads**, so every save always does a full week rewrite instead of a targeted one-cell update — harmless today, but means the "someone else is editing this" conflict warning can never fire for SKS. `task_867a4c80`. The realtime half of this same investigation is fixed (PR #809, v3.5.584) but deliberately didn't touch the read path (`roster-adapter.js`'s `toWideList()`) this item needs — re-confirmed live against `origin/main` 2026-08-27, still true. Full write-up: `eq/changelog/eq-field.md` (eq-field PR #805/#809). _(added 2026-08-26)_

---

## eq-field: consumes tenant_role_overrides denials (v3.5.621, PR #851)

- [ ] **Not merged — needs Royce's review.** eq-field PR #851 (client + session-token + a NOT-APPLIED migration) and eq-shell PR #1690 (the companion JWT claim). Neither merges anything to production on its own; #851 is inert without #1690, and the migration inside #851 needs a separate explicit dispatch decision even after both PRs merge. _(added 2026-08-31)_
- [ ] **14 `public.eq_*`/`eq__assert_*` Quotes/CRM RPC functions + 3 policies on ehow share the identical extra_perms-without-denied_perms gap, but are eq-shell's, not eq-field's** (confirmed via repo-wide grep — zero eq-field references). Spawned as `task_9f3eb7a8`, not built here — would extend eq-shell PR #1686's fix one layer deeper (the DB RPC layer, not just Shell's TS permission-resolution layer). _(added 2026-08-31)_

---

## eq-field: Teams — untick-to-remove silently didn't save, fixed (v3.5.621, PR #853, merged + live)
*Collin Toohey reported: adding people to a team via Manage Teams saves, but unticking someone to remove them doesn't. Root cause: the edit panel renders into two permanent containers (the modal and the standalone Teams page) that mirror each other, and closing the modal never clears its content — so once a team had been edited once, both held a live duplicate of the same checkboxes, one visible and one hidden. The save read both without scoping, and a person only needed to be checked in one copy to count as "keep" — so adding always worked but removing silently didn't. Fixed by scoping every form read to whichever container is actually on screen; the identical duplicate-ID bug in the create-team form was fixed alongside (same root cause, same file). Verified against the real, unmodified file via a local static-server harness (raw `file://` silently fails to resolve the app's relative `<script src>` tags — discovered mid-session) — 10/10 checks across both entry points, the add-regression check, and the create-team fix. Merged and confirmed live via `field.eq.solutions/sw.js` (v3.5.621). Full detail: `eq/changelog/eq-field.md`, `sessions/2026-08-31.md`.*

- [ ] **Worth a live SKS team-roster spot-check** — this bug has likely been silently live since the standalone Teams page shipped (v3.5.256), so any supervisor who removed someone via Manage Teams since then may have seen "Saved" while it silently didn't take. Nobody has reported this beyond Collin's one case, but nothing has actively checked for it either. _(added 2026-09-01, corrected 2026-09-01 — was originally logged "2026-08-31" from a session-wide date mistake this same day; see sessions/2026-09-01.md Notes)_
- [ ] **Not click-tested live by a real SKS supervisor through Core** — no SKS/Core credentials in this environment; verified instead via a real-code local-harness test (above) plus a clean, error-free deploy-preview boot. _(added 2026-09-01, corrected 2026-09-01 — same date-mistake correction as above)_

---

## eq-field: Teams — live "Selected" chip panel + click-anywhere-to-edit (v3.5.623/v3.5.624, PRs #854/#856, merged + live)

- [ ] **Worth a live SKS click-through** — same gap as the removal-bug fix above: confirm the chip panel and row-click behave correctly for a real supervisor through Core, not just the local harness. _(added 2026-09-01)_

---

## eq-field: PostHog "day one" review — 2 real bugs found + fixed, 1 held back deliberately (v3.5.645/v3.5.653, PRs #885/#890/#896)

- [ ] **PR #890 (Copy Last Week save-failure fix) — built and CI-green, deliberately not merged.** Royce's call after seeing the 2-uses-ever usage data; revisit only if he changes his mind, not on a schedule. _(added 2026-09-02)_
- [ ] **PostHog error tracking is dead instrumentation** — `$exception` hasn't fired once in 30 days across the whole `eq-production` project. Sentry remains the real error channel for Field/Shell; nobody should read PostHog's "0 issues" as a clean bill of health until this is either wired up properly or formally documented as not the error channel. _(added 2026-09-02)_

---

## eq-field: Weekly Roster — Roster Overview summary card removed from default view (v3.5.653, PR #896, merged + live)
*Royce, reviewing a screenshot: "I want someone that clicks on weekly roster to see the weekly roster." The coverage-%/not-rostered-chips/site-list card rendered unconditionally above the actual roster table on every visit, independent of the By Crew/Grid toggle beneath it. Explored a content redesign first (week-wide gaps, filter buttons, new-starters, management-out) and ran a feasibility check on all 4 candidates before Royce pulled back to the simpler ask: remove the card, don't improve it. Confirmed live by Royce directly post-merge ("confirmed, table loads first now"). The card's computation is untouched in `scripts/roster-overview.js` if a lighter, on-demand version is wanted later. Full detail: `eq/changelog/eq-field.md`, `sessions/2026-09-02.md`.*

- [ ] **"Understaffed sites vs last week" — real feasibility landmine found, not pursued.** Whether last week's schedule data is actually loaded client-side depends on how the viewed week was navigated to — the one reliable path (`onWeekChange()`'s dropdown) is hidden entirely in Shell-embedded mode (`core.eq.solutions/sks/field`, i.e. Royce's own real usage), leaving only non-fetching arrow-nav controls. This exact bug shape already caused a real incident once before (Copy Week, v3.5.354, silently overwrote data by reading an unloaded week as empty). If this feature is ever wanted, it needs `_ensureWeeksLoaded()` wired in first — a real sync→async render restructure, not a data-fetch bolt-on. _(added 2026-09-02)_
- [ ] **"New starters" and "management out" — cheap, ready if wanted later.** Both confirmed low-risk/low-effort during the same feasibility pass (new-starters reuses 3 existing pure helpers from `people.js`; management-out is already fully computed, just needs promoting). Not built — Royce simplified the whole request to "just remove the card" before either was needed. _(added 2026-09-02)_
- [ ] **Not click-tested by anyone but Royce himself** — standing Core-only sandbox limitation blocked every attempt from this session (deploy preview, production root, even the demo tenant all redirect to "Sign in through Core"). Royce confirmed live post-merge; no automated click-through exists for this page. _(added 2026-09-02)_

---
