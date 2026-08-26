---
title: EQ Tier — Verify Queue
owner: Royce Milmlow
last_updated: 2026-08-26
scope: Items whose only remaining blocker is your own live sign-in/click-through — the underlying work is already built, merged, and (unless the line itself says otherwise) live. Moved here from eq/pending.md by scripts/rotate_pending.py once a session's real build work is fully done, so a stale "click through to confirm" line no longer pins a whole finished write-up in the live pending doc.
read_priority: high
status: live
---

# EQ Tier — Verify Queue

Nothing left to build on anything below — every line just needs you to
actually open the app and check it. Delete the line once you've confirmed
it. If something's actually broken, that's real signal — flag it back as
a bug rather than just deleting the line.

---

**From:** eq-field: Safety Completeness Checker — Site Audit (2026-08-01)

- [ ] **Royce to click through live**: Site Audits → open/start an audit → mark any item "N" → confirm the yellow banner appears and "Go fix" scrolls/focuses correctly → fill in action + responsible → confirm the banner clears → try Submit with a gap still open → confirm the "Submit anyway?" prompt appears and Cancel keeps it in draft. Verified via an isolated JS harness only (12/12 assertions), not clicked through live — no test login in this sandbox. eq-field [PR #594](https://github.com/eq-solutions/eq-field/pull/594), merged, live v3.5.401. _(added 2026-08-01)_

---

**From:** eq-field: Safety Completeness Checker — Prestart/Toolbox (2026-08-01)

- [ ] **Royce to click through live**: Prestart — tick a High-Risk Construction Work category with no photo/hazards, confirm the banner + Go-fix work, fill both in and confirm it clears. Toolbox — enter a topic with no key safety message, confirm the banner appears and clears once filled. Try Submit on each with a gap still open and confirm the "Submit anyway?" prompt appears. Verified via an isolated JS harness only (21/21 assertions), not clicked through live — no test login in this sandbox. eq-field [PR #597](https://github.com/eq-solutions/eq-field/pull/597), merged, live v3.5.405. _(added 2026-08-01)_

---

**From:** eq-intake: Reconcile silently skipped phone/ABN cleanup for customer and contact imports (2026-07-29)

- [ ] **Royce to reconcile a customer CSV with a messy phone number/ABN and confirm it now gets cleaned up** — verified in code + typecheck, not yet clicked through live. _(added 2026-07-29)_

---

**From:** eq-shell: EQ Ops — view archived quotes without restoring them (2026-07-29)

- [ ] **Royce to click through live**: EQ Ops → "…" → Archived → open a quote via View, confirm it shows a read-only "Archived" badge and only Restore/Download/Delete (no Edit/Mark as Sent/Close/Archive controls), then confirm Restore still works from there. Verified only via the Netlify production deploy record (commit `2b01bf3b` live), not an actual click-through — no production login session in this environment. eq-shell [PR #1093](https://github.com/eq-solutions/eq-shell/pull/1093), merged. _(added 2026-07-29)_

---

**From:** eq-shell: removed a dead, never-linked duplicate import screen (2026-07-29)

- [ ] **Royce to click through the Import screen (`/intake`) on core.eq.solutions once the deploy lands** — confirm it still loads and still commits normally. That screen wasn't touched, but worth a look since it's the app's only working import path now. _(added 2026-07-29)_

---

**From:** eq-service: page-only export bug closed out everywhere, Excel export added to 3 pages (2026-07-29)

- [ ] **Royce to click through Assets/Job Plans/Maintenance Checks once the deploy lands** — confirm the Export button's new dropdown offers CSV and Excel, both download the full list, and the Maintenance Checks "tasks completed" count now shows a real number instead of "/0". Not click-tested live this session — no login credentials available in this environment, verified via type-checking + the full automated test suite + code review only. _(added 2026-07-29)_

---

**From:** eq-shell: licence-review badge never caught a Cards-side edit to an already-reviewed licence — fixed, plus the Field-sync gap it exposed (2026-07-28)

- [ ] **Royce to confirm live**: edit an already-reviewed licence's expiry/number in Cards for an approved worker, confirm the Staff page badge flips to "changed since — re-review needed" without a hard refresh. _(added 2026-07-28)_

---

**From:** eq-cards: Wallet nagged for "Photo ID" even though a Driver Licence was already held (2026-07-28)

- [ ] **Royce to confirm live**: reload the Wallet and confirm the Photo ID nag no longer shows for a worker who holds a Driver Licence or Passport. _(added 2026-07-28)_

---

**From:** eq-shell: TOTP backup codes shipped, closing the authenticator-lockout gap (2026-07-28)

- [ ] **Royce to click through the real flow once the deploy lands**: set up two-step verification, save the codes shown, sign out, sign back in using one of the backup codes instead of the phone app, then generate a fresh set from Settings and confirm the old ones stop working. _(added 2026-07-28)_

---

**From:** eq-cards + eq-shell: blurry licence photo fixed for a worker, admin "replace photo" tool shipped, a duplicate-licence gap closed (2026-07-28)

- [ ] **Royce to confirm live**: open Moahmmed Alsadiq Ahmed Elsayed on the Staff page, check the Photo ID and White Card show the new clearer photos, and that the "Replace photo" button now returns to normal after use. _(added 2026-07-28)_

---

**From:** eq-shell: Google Maps address autocomplete fixed in New Customer wizard (2026-07-28)

- [ ] **Royce to click through a real "New customer" add** once convenient, to confirm the address dropdown now actually appears and fills suburb/state (verified in code + build, not yet eyeballed live). _(added 2026-07-28)_

---

**From:** eq-shell: black-screen-on-load fixed for real, then a follow-up made it actually visible (2026-07-27)

- [ ] **Royce to confirm live** that the loading screen now shows a clearly visible spinner instead of a black or blank pane, next time he opens Service/Field/Cards from Core. _(added 2026-07-27)_

---

**From:** eq-shell/eq-cards: tenant data-plane security sweep + a real login-blocking bug fixed for a live user (2026-07-27)

- [ ] **Royce to click through the new "who gets notified" Settings control** to confirm it reads clearly and saves correctly — code-complete and tested, not yet user-verified. _(added 2026-07-27)_

---

**From:** eq-shell: Customer search now shows what matched (2026-07-23)

- [ ] **Not yet click-tested live** — build-verified only; nobody has actually searched for a site/contact/contract on the real Customers page and confirmed the right label shows. _(added 2026-07-23)_

---

**From:** eq-shell Suppliers: fixed squashed columns + a stale-workspace-switch bug that briefly exposed the wrong tenant's data (2026-07-23)

- [ ] Royce to click through a workspace switch + the Suppliers page once live to confirm the fix. _(added 2026-07-23)_

---

**From:** EQ Field — Pipeline: real manual-remove (archive gated + restorable + permanent delete) + in-browser sample data for demos (2026-07-15, BOTH MERGED + LIVE)

- [ ] **Not click-tested live** — SKS Pipeline is triple-gated to the SKS tenant; this session had no SKS login to verify either feature by hand. Worth a quick real click-through next time you're signed in, especially "Load sample data" before demoing it to anyone. _(added 2026-07-15)_

---

**From:** eq-solves-service: retired a dead planning doc, added a site supervisor field, then caught and fixed a wrong design before it shipped wrong (2026-08-02)

- [ ] **Royce to click through live**: open a site, assign a supervisor from its own contact list, save, reload, confirm it sticks; toggle "Show archived" on the Sites list and confirm it filters/tags correctly. Needs a real sign-in, which is off-limits for Claude to do on your behalf. _(added 2026-08-02)_

---

**From:** eq-solves-service: two small fixes from a screenshot — bigger upload limit, report cover kept its branding (2026-08-02)

- [ ] Royce to spot-check a generated PM Asset Report live for a site that has a photo on file — confirm the band + photo layout looks right. _(added 2026-08-02)_

---

**From:** eq-shell: New Quote form can now attach files before the quote exists (2026-08-01)

- [ ] **Royce to click through live**: open New Quote, attach a couple of files before finishing the form, submit, confirm the files show up on the created quote. _(added 2026-08-01)_

---

**From:** eq-cards: credential-capture screen made photo-first; a leftover production migration reconciled into history (2026-08-01)

- [ ] **Royce to click through live on a real device** — confirm the "take a photo" sheet feels right end to end (camera opens, OCR reads the card, fallback link works). Note: the code merged this morning but wasn't actually live yet when Royce first tried it — this repo's deploy isn't automatic on merge, and nobody had triggered one. Deployed and confirmed live later the same day. _(added 2026-08-01, updated 2026-08-01)_

---

**From:** eq-solves-intake: closed out the rest of the dependency audit findings, both fixes live (2026-08-01)

- [ ] **Royce to click through live**: sign in on core.eq.solutions and confirm Cards/Field/Service each load past "Authorising…" — needs a real login, which Claude can't do on Royce's behalf. _(added 2026-08-01)_

---

**From:** eq-shell: Intake page was crashing for everyone — found the cause, fixed it, confirmed live (2026-08-01)

- [ ] **Royce to click through live**: open Intake as a signed-in user and confirm the page actually renders (not just that the site responds) — needs a real login, which Claude can't do on Royce's behalf. _(added 2026-08-01)_

---

**From:** eq-shell: every permission denial now leaves a trace in the audit log (PR #1154, merged 2026-08-01)

- [ ] **Royce to click through live**: sign in as a non-manager, try a manager-only action, confirm a "denied" row actually lands in the audit log. Needs a real login, which Claude can't do on Royce's behalf. _(added 2026-08-01)_

---

**From:** eq-solves-service: Site photos now show up in the reports that actually need them, plus a real blank-page bug found and fixed (2026-08-01)

- [ ] **Royce to spot-check a live PM Check Report and NSX Test Report from a site with an uploaded photo** — verified via generated samples with a placeholder image, not yet against a real production report. _(added 2026-08-01)_

---

**From:** eq-shell: re-vendored the Intake engine — merge errors now show, duplicate flags can be archived (2026-07-31)

- [ ] **Royce to click through live** — trigger a failed site merge in the Duplicate Sites panel and confirm the error now shows; open the Remediation Queue, find a duplicate flag, click Archive, confirm the record goes inactive and drops off the list. Claude can't do this step itself — it requires signing in, which falls under the hard rule against entering credentials on the user's behalf. _(added 2026-07-31)_

---

**From:** EQ Field screenshot review — cross-tenant fixes (2026-07-30/31)

- [ ] Nobody's confirmed the `eq` tenant's Job Numbers nav placement or mobile Pipeline hiding on a live click-through — same "not yet clicked through production" gap noted in the SKS entry. _(added 2026-07-31)_

---

**From:** eq-shell: dropped redundant mobile top bar on Field/Service; verified Ops-tab gating already live (2026-07-31)

- [ ] **Royce to click through live** on a mobile-width view (~375px or a phone): open Field/Service and confirm the top bar is gone (just the bottom tab bar); open Ops/Comms and confirm nothing changed; from Field/Service, tap Home and confirm Settings/2FA/Sign-out are still reachable there. Note: a related eq-field fix landed 2026-07-31 (v3.5.388) for a home-label clipping issue caught on the same phone-screenshot pass — worth confirming both together. _(added 2026-07-31)_

---

**From:** eq-shell: same archived-staff leak, different dashboard card — Core home's "Compliance & safety" card — fixed + merged (2026-07-30)

- [ ] **Royce to confirm live**: once the deploy lands on core.eq.solutions, reload the dashboard and confirm Huon Henne no longer appears under "Licences expiring" on the Compliance & safety card. _(added 2026-07-30)_

---

**From:** eq-shell + eq-cards: Photo ID compliance-matrix accuracy + full-size licence photo lightbox (2026-07-29 → 2026-07-30)

- [ ] **Moahmmed Elsayed's `photo_id`-typed licence row (number `0140988080`) not yet corrected** — unlike Maylin Ung's case (a driver's-licence-format number, fixed directly), this number doesn't match a recognisable pattern; needs Royce to confirm the actual document type before the DB row is corrected. _(added 2026-07-29)_

---

**From:** eq-shell: Worker sign-in safety net — lost-phone protection, PIN visibility for admins, backup email (2026-07-30)

- [ ] **Royce to click through live, all four features shipped today together** (this section's three plus the compliance-roster-only switch above): invite/adjust a worker with Field access off; correct a test worker's phone number and confirm their old passcode stops working while a fresh sign-in + new passcode works; check the passcode-status view and try "Unlock now" on a locked test account; sign in as a phone-only worker and confirm the backup-email reminder shows, dismisses for that sign-in only, and clears once an email is added. None of this has been clicked through live yet — Claude can't perform this step directly (logging in requires entering a passcode, which falls under a hard rule against entering credentials on the user's behalf, even for the user's own product). _(added 2026-07-30)_

---

**From:** eq-shell: EQ Ops now leads with ex-GST everywhere, Coupa PO-match display fixed (2026-07-30)

- [ ] **Royce to click through live**: open a job's detail view, the create-quote form, the kanban board, and each Reports tab, confirm ex-GST reads as the main figure everywhere it should. Verified via build + typecheck only, not yet clicked through live. _(added 2026-07-30)_

---

**From:** eq-shell: Suppliers page "missing" Login/Password columns — actual root cause fixed (2026-07-28 → 2026-07-30)

- [ ] **Royce to click through live**: Suppliers shows a Columns button, the table scrolls freely past 20 rows instead of paginating, and hovering a masked password shows "Click to reveal". _(added 2026-07-30, PR #1120 merged)_

---

**From:** eq-shell: Audit log was drowning in empty "Automatic" rows — root-caused, fixed, then a live test caught the first fix didn't actually work (2026-07-30)

- [ ] **Royce to click through live**: open Activity log → Suite activity tab, confirm the sentences read sensibly against real SKS data (quotes, shifts, licence reviews), and check the new search/filter on that tab works as expected. New quote events should now show "EQ Ops" natively (not just relabelled) — worth a fresh quote status change to confirm end-to-end. _(added 2026-07-30, PRs #1121/#1123/#1126/#1129/#1132 merged, migrations 0225+0226+0227 dispatched, workers-canonical-sync redeployed v12 — full write-up in `sessions/2026-07-30.md` and `changelog/eq-shell.md`)_

---

**From:** eq-field: dashboard licence-expiry alert

- [ ] **Not click-tested live with real populated canonical data** — needs an authenticated worker session (`canon-read` requires a real session token). Royce to confirm a worker with an expiring Cards licence actually surfaces on the dashboard card. _(added 2026-08-05)_

---

**From:** eq-cards: Wallet declutter + Show mode + OCR dead-session fix (2026-08-03)

- [ ] **Show mode not yet click-tested on a real device with network disabled.** Verified: analyzer clean, full test suite (255 tests) passes, `flutter build web` succeeds and boots with zero console errors via a static preview — but never signed in as a real worker and tapped it (real login is off-limits for me to do on Royce's behalf). Royce to confirm brightness/wakelock/offline behaviour actually work as intended. _(added 2026-08-03)_

---

**From:** eq-receipts: full-width nav + one-click Review from Inbox after a photo import (2026-08-03)

- [ ] **Neither change has been clicked through live** — Supabase OTP auth gated this session out of the real app, no test login available. Same underlying gap as the still-open react-router click-through below — worth doing both in the same real-device pass. _(added 2026-08-03)_

---

**From:** ⏩ EQ Shell — admin licence backfill: back-photo support + OCR-hang diagnosis (2026-08-04)

- [ ] **Live click-through of both the OCR timeout fix (#211/#1235) and the photo-preview backup (#1238) not done** — both PRs' UI paths only render inside an authenticated Shell admin session, off-limits for Claude to sign into. Royce to confirm: a slow/failing OCR read now surfaces a clean timeout instead of hanging; picking a photo shows a working thumbnail that opens full-size; picking a PDF shows a working "View PDF" link. _(added 2026-08-04)_

---

**From:** eq-shell: EQ-SHELL-10/19 "auth-stall: chunk-error" — a second, distinct root cause found and fixed, merged + live (2026-08-05)

- [ ] **Royce to confirm the SKS dashboard loads cleanly** — needs an authenticated session, off-limits for Claude to drive. _(added 2026-08-05)_

---

**From:** eq-field: Birthdays & Anniversaries dashboard widget only showed up sometimes — root-caused and fixed, live (2026-08-05)

- [ ] **Not click-tested live by a real signed-in user** — everything above was verified at the function level and via the deploy preview's boot path, not by an authenticated session actually seeing the widget populate with real people. Royce to confirm on `field.eq.solutions` (or the Shell embed) that Birthdays & Anniversaries now shows up reliably from a fresh Dashboard landing. _(added 2026-08-05)_

---

**From:** eq-shell: Staff can now have a home address, and the compliance-pack export stops showing "Unknown" for names only ever edited in Shell — two PRs merged, live (2026-08-05)

- [ ] **Neither fix has been click-tested live** — Royce to confirm: (1) the address fields save and display correctly on a real staff member, desktop and mobile, (2) re-downloading William's compliance pack now shows "William Hong" instead of "Unknown." _(added 2026-08-05)_

---

**From:** eq-field: new starters no longer sit on the live roster for weeks before they actually start — merged, live (2026-08-05)

- [ ] **Not click-tested live** — Royce to confirm a real future-dated new starter actually disappears from the roster/dispatch/timesheets and shows up correctly in the new Starting Soon widget. _(added 2026-08-05)_

---

**From:** eq-shell: EQ Ops quote-import polish — pricing table layout, PDF drag-and-drop, cost/sell question — three PRs merged, live (2026-08-05)

- [ ] **None of the four PDF-import/pricing-table changes above have been click-tested live yet** — all need an authenticated Shell admin session, off-limits for me to drive. Royce to confirm: (1) Materials save-all + archive behaves correctly on the live setup page, (2) dragging a PDF onto the Jobs page actually fires the import in a real browser, (3) the Cost/Sell toggle on the main "From PDF" button — especially that a real sell-priced supplier PDF now computes cost correctly, and the default Cost path is unchanged, (4) the *same* toggle now also appearing on the second "Import from PDF" button inside the New Quote form when a document has ambiguous pricing. _(added 2026-08-05, updated 2026-08-05)_

---

**From:** eq-shell + eq-field: EQ Field can now trigger a Shell-owned staff/supervisor write via entity-patch — both halves shipped, live (2026-08-05)

- [ ] **Not click-tested live** — no way to drive a real cross-origin Field session from this environment. Royce to confirm: open Field as an SKS admin, click "🏷 Edit category" on a supervisor, change category/role, save, confirm it reflects back on Shell's own Staff page. _(added 2026-08-05)_

---

**From:** eq-field + eq-shell: My Schedule maps link — real root cause found, iframe popups were blocked, merged, live (2026-08-06)

- [ ] **Not yet confirmed on a real device through Core that the maps link now opens.** Three attempts: v3.5.460 (eq-field #655) dropped `target="_blank"` for iOS standalone; v3.5.465 (eq-field #659) switched to Apple's `maps://` scheme — both real, defensible fixes for genuine standalone-PWA use, but Royce's actual test was always through Core (`core.eq.solutions/sks/field`), where neither could work. The real cause: `FieldIframe.tsx`'s iframe `sandbox` attribute never included `allow-popups`, so **any** `target="_blank"` link or `window.open()` inside Field, Service, or Cards was silently blocked whenever accessed through Shell — on any device, not iOS-specific. Fixed for all three apps (eq-shell [#1268](https://github.com/eq-solutions/eq-shell/pull/1268), merged, live on `core.eq.solutions`). Royce to confirm the maps icon now actually opens Maps when accessed through Core. _(added 2026-08-05, updated 2026-08-06)_

---

**From:** eq-service: empty "assign to" member picker on Create Check — root-caused, fixed, merged, live (2026-08-08)

- [ ] **Not click-tested live** — local dev server hung on an unrelated issue during the fix session. Needs a quick manual pass on ACB and NSX Create Check to confirm the dropdown actually populates in the browser. _(added 2026-08-08)_

---

**From:** eq-field: Calendar stopped showing approved leave since the July 10 roster-overlay migration — found + fixed (v3.5.473, PR #674, merged 2026-08-10)

- [ ] **Live click-through not done** — app can't boot in this sandbox (no network to the canonical config service, even for the demo tenant); verified instead via a standalone harness running the actual edited code plus the full existing test suite (26/26) and eslint. Royce to confirm approved leave now shows on the Calendar page on a real tenant. _(added 2026-08-10)_

---

**From:** eq-shell: PR #1287 (Contacts dedup swap) deploy verified clean (2026-08-11)

- [ ] **Still not click-tested live** — deploy health confirms the code reached production, not that the Customers page's duplicate-detection UI still behaves correctly. Needs a real click-through. _(added 2026-08-11)_

---

**From:** eq-field: Calendar stopped showing approved leave since the July 10 roster-overlay migration — found + fixed (v3.5.473, PR #674, merged 2026-08-10)

- [ ] **Live click-through not done** — app can't boot in this sandbox (no network to the canonical config service, even for the demo tenant); verified instead via a standalone harness running the actual edited code plus the full existing test suite (26/26) and eslint. Royce to confirm approved leave now shows on the Calendar page on a real tenant. _(added 2026-08-10)_

---

**From:** eq-shell: EQ Ops archive view gets full search/filter, quotes auto-archive after 7 days invoiced (2026-08-12)

- [ ] **Live click-through not done** — this sandbox has no network path to the tenant-config service, so the Archived-tab search/filter/bulk-select hasn't been visually confirmed in a real browser session. Built against the exact same Table component already proven live elsewhere in the app; build + typecheck clean on both PRs. _(added 2026-08-12)_

---

**From:** eq-shell: EQ Ops archive view gets full search/filter, quotes auto-archive after 7 days invoiced (2026-08-12)

- [ ] **Live click-through not done** — this sandbox has no network path to the tenant-config service, so the Archived-tab search/filter/bulk-select hasn't been visually confirmed in a real browser session. Built against the exact same Table component already proven live elsewhere in the app; build + typecheck clean on both PRs. _(added 2026-08-12)_

---

**From:** eq-field + suite-wide: permission audit (131 rows, Excel), 2 live gaps flagged, next-sprint fix built + shipped as PR #683 (2026-08-12)

- [ ] **Live click-test still not done anywhere across the whole audit thread this section started** (eq-shell, eq-field, eq-solves-service, eq-cards — all fixes merged/applied, `task_fd65aa59`/`task_de667109`/`task_9f6fca23` all resolved. See the 2026-08-13 entry near the top of this file for the full closed-out scope). Every fix across all four apps was verified against live data/CI/direct DB checks, never a real signed-in click-through session. _(added 2026-08-12, updated 2026-08-13)_

---

**From:** eq-roles + eq-field + eq-shell: security-groups export → Field/Shell permission-pipeline fix, 6 PRs merged + live (2026-08-08)

- [ ] **No live click-through yet** on the Shell↔Field permission changes — needs a real signed-in session, off-limits to this environment. `FIELD_PERMS_DRIFT_PAT` was added 2026-08-12 (initially to the wrong repo, eq-field; caught and corrected to eq-shell) and eq-shell [PR #1308](https://github.com/eq-solutions/eq-shell/pull/1308) confirmed the real drift check now passes with it in place — that half is done. Royce has exact test steps: (1) Access Control → revoke/grant a permission → confirm it reaches Field without a fresh login (the actual Phase 0 fix); (2) Custom Groups → new "Field permissions" section → toggle one → confirm it applies in Field. Neither run yet. _(added 2026-08-08, updated 2026-08-12)_

---

**From:** eq-shell: comms job table's JobRow extraction closes out react-hooks/refs — PR #1202 (2026-08-03)

- [ ] **Live click-through not done** — the comms job table's inline editing (click-to-edit, Enter/Tab save-and-move, Esc cancel, cross-row keyboard nav) needs a real click-through on the NSW Comms board before trusting the extraction blind. Content moved verbatim and the shared-state/keyboard-nav logic was reasoned through carefully, but a structural change like this deserves a real look. Needs a real authenticated session, off-limits for me to do myself. _(added 2026-08-03)_

---

**From:** eq-field: Labour Hire archive + "would rehire" rating, ported from SKS (2026-07-28)

- [ ] **No live click-through was possible this session** — the local preview needs credentials this session doesn't have access to. Verified instead via automated tests, a code check, and the exact same checks GitHub runs (all passed), plus a live preview link — but nobody has actually clicked through the real feature yet. Worth a quick real check next time you're in the app. _(added 2026-07-28)_

---

**From:** eq-shell Staff table: reorderable columns + compact Status/Contact cells (2026-07-27)

- [ ] **No live click-through yet** — the blocker ("once merged and live") has been true for 2+ weeks now; still nobody's confirmed the reorderable-columns/compact-cells changes look right live. Worth an actual look. _(added 2026-07-27, unblocked 2026-08-13)_

---

**From:** eq-shell: quick-edit Staff list — Supervisor/Roster toggles + inline fields, no more open-record-to-flip-one-checkbox (2026-07-27)

- [ ] **Live click-through as a lower-permission user (employee/apprentice/labour-hire/subcontractor) still not done** — verified instead by reading the code directly: those roles all lack `field.dispatch`, and without it the new checkboxes render natively `disabled` and the inline text/select cells render as plain unclickable text with no edit affordance at all (not just a disabled button) — confirmed in both `StaffPage.tsx` and the shared roles package. The write endpoint (`entity-patch.ts`) enforces the same permission server-side regardless of what the UI shows. Needs Royce to actually sign in as one of those roles to eyeball it, since Claude doesn't hold a lower-permission test login. _(added 2026-07-27)_

---

**From:** eq-field: who does a supervisor actually see? — built, live, then loosened on your feedback (2026-07-22)

- [ ] **Couldn't get eyes on it working in a real browser this session** — the testing tool kept timing out for reasons unrelated to the change, so it was verified a different way (driving the actual running code directly) instead of a live click-through. Worth a real look next time you're in Timesheets or Roster with supervision unlocked. _(added 2026-07-22)_

---

**From:** ⏩ Session close — 2026-07-06 (eq-field + eq-shell) — canonical link redesigned + shipped, job_title added tenant-wide, root-caused Liam Holmgreen's stuck supervisor status, Batch Fill filters

- [ ] **Live click-through of v3.5.253 (mobile Other bucket) and v3.5.254 (Batch Fill Group/Team filters)** — both deployed and verified via Netlify (commit match, no errors, secret scan clean), but not exercised through a real authenticated SKS session — eq-field's Shell-JWT handoff auth isn't reproducible in a local dev server. _(added 2026-07-06)_

---

**From:** eq-field: Hours overview + Job Numbers panel — mobile decluttered per Royce's screenshots, "Triage-first" fully shipped (2026-08-13)

- [ ] Not click-tested on a real phone — the full "Triage-first" mobile pass is now shipped across 2 PRs ([#687](https://github.com/eq-solutions/eq-field/pull/687): Filters sheet, desktop-only stat grid, tidied Job Numbers rows; [#688](https://github.com/eq-solutions/eq-field/pull/688): group "N pending" pills on collapsed groups, the SHOW-chips/action-row collapsed into its own "Status & tools" sheet), both merged on Royce's explicit go-ahead after CI + deploy-preview went green, but no live click-through has happened on any of it (this sandbox has no live browser access — confirmed again this session via a `file://` preview that boots far enough to hit the same tenant-config network wall every prior mobile PR here has hit). Worth a real look next time Royce is on the app — in particular whether the mobile action row (now 4 buttons: Filters/Status/Job Numbers/Batch Fill) reads as cluttered in its own right. _(updated 2026-08-13)_

---

**From:** Suite-wide permission audit closed out across all 4 apps — 1 real live security hole found + fixed (eq-cards), everything else merged (2026-08-12 → 2026-08-13)

- [ ] **Live click-test still not done anywhere across this whole thread** — every fix above was verified against live data/CI/direct database checks, never a real signed-in click-through session on any of the four apps. _(added 2026-08-13)_

---

**From:** eq-shell: labour-hire invite-path approval was silently dropping flagged licences — found, fixed, merged, live (2026-08-13)

- [ ] **Live click-through not done** — the invite path (existing SimPRO/import staff record, `staff_id`) now records flagged-licence reviews and notifies the worker on approval, matching the self-signup path's existing behaviour. Needs a real signed-in Shell session with `admin.review_cards` to confirm end-to-end — off-limits for this environment. _(added 2026-08-13)_

---

**From:** eq-solves-service: NSX Test Report fixed — dead ACB-only fields left it always printing blank sections (2026-08-14)

- [ ] **Not click-tested against a real generated NSX report** — fix verified via typecheck + code trace only; worth Royce pulling a real NSX Test Report next time one's generated to eyeball the CB Details table looks right. _(added 2026-08-14)_

---

**From:** eq-solves-service: /admin/* pages closed to non-managers (2026-08-14)

- [ ] **Not click-tested by a real non-manager account** — no such login was available in this environment. Worth Royce confirming a technician account gets bounced off `/admin/*` now. _(added 2026-08-14)_

---

**From:** eq-shell: account-enumeration hole closed on the phone+PIN sign-in door (2026-08-15)

- [ ] **Not click-tested in a browser** — both sign-in doors were checked by calling them directly on production (an unknown mobile and an unknown email each return an identical "no" with no extra detail; the unauthed session check still refuses correctly) plus full CI, but nobody signed in through the actual page. Worth Royce trying two things on his phone: a *wrong* PIN, and a number that has *no* PIN set — both should now show the same "That number and PIN didn't match. If you haven't set a PIN yet, use 'Text me a code instead'". Then sign in by text on an account with no PIN and confirm the "Set a PIN" prompt still appears on the Home screen — that prompt is now the only place that guidance is given. _(added 2026-08-15)_

---

**From:** eq-solves-service: NSX Test Report fixed — dead ACB-only fields left it always printing blank sections (2026-08-14)

- [ ] **Not click-tested against a real generated NSX report** — fix verified via typecheck + code trace only; worth Royce pulling a real NSX Test Report next time one's generated to eyeball the CB Details table looks right. _(added 2026-08-14)_

---

**From:** eq-solves-service: /admin/* pages closed to non-managers (2026-08-14)

- [ ] **Not click-tested by a real non-manager account** — no such login was available in this environment. Worth Royce confirming a technician account gets bounced off `/admin/*` now. _(added 2026-08-14)_

---

**From:** eq-shell: a way to hand yourself full admin power through the "custom access groups" screen — found, fixed, and live (2026-08-16)

- [ ] **Not clicked through live** — confirmed by tests and by calling the affected screen's backend directly, not by an actual person building a group in the UI and watching the dangerous options disappear. Worth two minutes on a real admin account. _(added 2026-08-16)_

---

**From:** eq-shell: an AI tool anyone signed in could use to run up costs on the company's AI account — closed, merged, live (2026-08-16)

- [ ] **Not clicked through live yet.** Worth two minutes: try the AI import on a real file, look at the home-page briefing/ask bar as a manager vs. a supervisor, and try opening the licence-scan page as an apprentice (should now say you don't have access). _(added 2026-08-16)_

---

**From:** eq-shell: account-enumeration hole closed on the phone+PIN sign-in door (2026-08-15)

- [ ] **Not click-tested in a browser** — both sign-in doors were checked by calling them directly on production (an unknown mobile and an unknown email each return an identical "no" with no extra detail; the unauthed session check still refuses correctly) plus full CI, but nobody signed in through the actual page. Worth Royce trying two things on his phone: a *wrong* PIN, and a number that has *no* PIN set — both should now show the same "That number and PIN didn't match. If you haven't set a PIN yet, use 'Text me a code instead'". Then sign in by text on an account with no PIN and confirm the "Set a PIN" prompt still appears on the Home screen — that prompt is now the only place that guidance is given. _(added 2026-08-15)_

---

**From:** eq-cards: 3 permission-audit gaps closed — dead JWT minter retired, empty employer credential list fixed, unreachable admin policy fixed (2026-08-16)

- [ ] **Live click-through not done on the credential-list fix specifically.** Verified via live RLS/RPC checks, CI (`flutter analyze` + `flutter test`), and the deploy's ETag change — not by an actual signed-in admin opening a worker's detail screen and seeing their credentials render. _(added 2026-08-16)_

---

**From:** eq-solves-service: any signed-in worker — apprentice, labour hire, subcontractor — could write maintenance checks, defects, test results and assets straight to the database, skipping every in-app permission check. Fixed, shipped, and confirmed live (2026-08-16)

- [ ] **Not clicked through live.** The database change is live on production now — worth two minutes to confirm a low-privilege account (apprentice/labour hire/subcontractor) actually gets blocked from writing, and that an assigned technician can still update their own job. Needs a real signed-in session, not checkable from here. _(added 2026-08-16)_

---

**From:** eq-solves-service: NSX Test Report fixed — dead ACB-only fields left it always printing blank sections (2026-08-14)

- [ ] **Not click-tested against a real generated NSX report** — fix verified via typecheck + code trace only; worth Royce pulling a real NSX Test Report next time one's generated to eyeball the CB Details table looks right. _(added 2026-08-14)_

---

**From:** eq-solves-service: /admin/* pages closed to non-managers (2026-08-14)

- [ ] **Not click-tested by a real non-manager account** — no such login was available in this environment. Worth Royce confirming a technician account gets bounced off `/admin/*` now. _(added 2026-08-14)_

---

**From:** eq-shell: the Shell licence-scanner page has never once saved a licence — found, fixed, merged, live (2026-08-17)

- [ ] **Not clicked through live** — verified by code review, live database checks, and a clean preview build, not by an actual person scanning a licence on the real site and watching it save. Worth two minutes on a real account.

---

**From:** eq-shell: a way to hand yourself full admin power through the "custom access groups" screen — found, fixed, and live (2026-08-16)

- [ ] **Not clicked through live** — confirmed by tests and by calling the affected screen's backend directly, not by an actual person building a group in the UI and watching the dangerous options disappear. Worth two minutes on a real admin account. _(added 2026-08-16)_

---

**From:** eq-shell: an AI tool anyone signed in could use to run up costs on the company's AI account — closed, merged, live (2026-08-16)

- [ ] **Not clicked through live yet.** Worth two minutes: try the AI import on a real file, look at the home-page briefing/ask bar as a manager vs. a supervisor, and try opening the licence-scan page as an apprentice (should now say you don't have access). _(added 2026-08-16)_

---

**From:** eq-shell: account-enumeration hole closed on the phone+PIN sign-in door (2026-08-15)

- [ ] **Not click-tested in a browser** — both sign-in doors were checked by calling them directly on production (an unknown mobile and an unknown email each return an identical "no" with no extra detail; the unauthed session check still refuses correctly) plus full CI, but nobody signed in through the actual page. Worth Royce trying two things on his phone: a *wrong* PIN, and a number that has *no* PIN set — both should now show the same "That number and PIN didn't match. If you haven't set a PIN yet, use 'Text me a code instead'". Then sign in by text on an account with no PIN and confirm the "Set a PIN" prompt still appears on the Home screen — that prompt is now the only place that guidance is given. _(added 2026-08-15)_

---

**From:** eq-cards: 3 permission-audit gaps closed — dead JWT minter retired, empty employer credential list fixed, unreachable admin policy fixed (2026-08-16)

- [ ] **Live click-through not done on the credential-list fix specifically.** Verified via live RLS/RPC checks, CI (`flutter analyze` + `flutter test`), and the deploy's ETag change — not by an actual signed-in admin opening a worker's detail screen and seeing their credentials render. _(added 2026-08-16)_

---

**From:** eq-solves-service: Calendar + every people-list in Service made canonical, 3 database updates shipped to live (2026-08-17)

- [ ] **Not clicked through live by a real signed-in user** — verified via code review, live-database dry-runs, and clean CI, not by actually opening the Calendar page and checking the technician/supervisor dropdowns show the right names. _(added 2026-08-17)_

---

**From:** eq-solves-service: any signed-in worker — apprentice, labour hire, subcontractor — could write maintenance checks, defects, test results and assets straight to the database, skipping every in-app permission check. Fixed, shipped, and confirmed live (2026-08-16)

- [ ] **Not clicked through live.** The database change is live on production now — worth two minutes to confirm a low-privilege account (apprentice/labour hire/subcontractor) actually gets blocked from writing, and that an assigned technician can still update their own job. Needs a real signed-in session, not checkable from here. _(added 2026-08-16)_

---

**From:** eq-solves-service: NSX Test Report fixed — dead ACB-only fields left it always printing blank sections (2026-08-14)

- [ ] **Not click-tested against a real generated NSX report** — fix verified via typecheck + code trace only; worth Royce pulling a real NSX Test Report next time one's generated to eyeball the CB Details table looks right. _(added 2026-08-14)_

---

**From:** eq-solves-service: /admin/* pages closed to non-managers (2026-08-14)

- [ ] **Not click-tested by a real non-manager account** — no such login was available in this environment. Worth Royce confirming a technician account gets bounced off `/admin/*` now. _(added 2026-08-14)_

---

**From:** eq-shell: Cards iframe was blocking the Web Share API, breaking iOS exports through Shell — fixed, live (2026-08-18)

- [ ] **No live click-through yet** — the fix is confirmed genuinely deployed, but nobody has tapped "Save" on an export through `core.eq.solutions/sks/cards` on an actual iOS device since it landed. _(added 2026-08-18)_

---

**From:** eq-shell: "horrendous" screen-to-screen loading — root cause was full page reloads on every sidebar click, fixed, merged, live (2026-08-18)

- [ ] **Not click-tested live by a person** — verified via typecheck, lint, the full test suite, and confirmed production deploys (exact commit match against what's actually serving), not an actual signed-in click-through. Worth two minutes next time Royce is in Shell: click through Staff → Customers → Field → Admin from the sidebar (should feel instant, no white-flash reload), and confirm ctrl/cmd-click still opens a link in a new tab. _(added 2026-08-18)_

---

**From:** eq-shell: Cards-linked worker's DOB guard was blocking unrelated edits (start date, phone, ...) — found, fixed, merged, live (2026-08-18)

- [ ] **Not clicked through live** — verified by code + typecheck/lint, not by an actual admin editing a Cards-linked worker's start date and a DOB and watching each behave correctly. Worth two minutes: edit Mohammed Hussain's start date (should now save), then try typing a different day/month for a Cards-linked worker (should still correctly block). _(added 2026-08-18)_

---

**From:** eq-shell: the Shell licence-scanner page has never once saved a licence — found, fixed, merged, live (2026-08-17)

- [ ] **Not clicked through live** — verified by code review, live database checks, and a clean preview build, not by an actual person scanning a licence on the real site and watching it save. Worth two minutes on a real account.

---

**From:** eq-shell: a way to hand yourself full admin power through the "custom access groups" screen — found, fixed, and live (2026-08-16)

- [ ] **Not clicked through live** — confirmed by tests and by calling the affected screen's backend directly, not by an actual person building a group in the UI and watching the dangerous options disappear. Worth two minutes on a real admin account. _(added 2026-08-16)_

---

**From:** eq-shell: an AI tool anyone signed in could use to run up costs on the company's AI account — closed, merged, live (2026-08-16)

- [ ] **Not clicked through live yet.** Worth two minutes: try the AI import on a real file, look at the home-page briefing/ask bar as a manager vs. a supervisor, and try opening the licence-scan page as an apprentice (should now say you don't have access). _(added 2026-08-16)_

---

**From:** eq-shell: account-enumeration hole closed on the phone+PIN sign-in door (2026-08-15)

- [ ] **Not click-tested in a browser** — both sign-in doors were checked by calling them directly on production (an unknown mobile and an unknown email each return an identical "no" with no extra detail; the unauthed session check still refuses correctly) plus full CI, but nobody signed in through the actual page. Worth Royce trying two things on his phone: a *wrong* PIN, and a number that has *no* PIN set — both should now show the same "That number and PIN didn't match. If you haven't set a PIN yet, use 'Text me a code instead'". Then sign in by text on an account with no PIN and confirm the "Set a PIN" prompt still appears on the Home screen — that prompt is now the only place that guidance is given. _(added 2026-08-15)_

---

**From:** eq-shell: hard-delete for archived user accounts — built, merged, live (2026-08-14)

- [ ] **Not click-tested live** — same sandbox limitation as everything else this session; built against `tsc`/lint/the permission-drift guard only. _(added 2026-08-14)_

---

**From:** eq-cards: export flow finished end-to-end — Export/Download merged into one sheet, auto-provision session race fixed, export-all PDF/Excel added, PDF photo embed shipped then fixed twice, iOS downloads fixed, two nagging reminders removed (2026-08-18)

- [ ] **No live click-through yet on the Web Share "Save" flow specifically through the Shell iframe** since the `allow="web-share"` fix landed — the permission-policy fix is confirmed live (grepped the deployed Shell bundle for `allow:"web-share"`), but nobody has tapped Save through `core.eq.solutions/sks/cards` since. _(added 2026-08-18)_

---

**From:** eq-cards: 3 permission-audit gaps closed — dead JWT minter retired, empty employer credential list fixed, unreachable admin policy fixed (2026-08-16)

- [ ] **Live click-through not done on the credential-list fix specifically.** Verified via live RLS/RPC checks, CI (`flutter analyze` + `flutter test`), and the deploy's ETag change — not by an actual signed-in admin opening a worker's detail screen and seeing their credentials render. _(added 2026-08-16)_

---

**From:** eq-field: apprentices can self-create their initial profile (2026-08-18)

- [ ] **Not click-tested live by a real self-signed-up apprentice** — same SKS Core-only sandbox limitation as PR #722 below. _(added 2026-08-18)_

---

**From:** eq-field: apprentice list fail-open bug + full onboarding/login audit across ehow, jvkn, Sentry (2026-08-18)

- [ ] **Not click-tested live as a non-manager** — same SKS Core-only sandbox limitation as PR #720's own entry below; verified via CI + live DB trace instead. _(added 2026-08-18)_

---

**From:** eq-solves-service: click-to-create on the calendar, a working "reconnect" button on session timeouts, faster warm-up after a deploy, and a safety net for lost in-progress readings (2026-08-18)

- [ ] **Not click-tested live by a real signed-in user.** This session's sandbox has no working login for service.eq.solutions — verified via type-checking and a full production build only. Worth two minutes clicking a calendar day, triggering a session timeout, and filling in part of an ACB/NSX/RCD check then reloading to confirm the draft comes back. _(added 2026-08-18)_

---

**From:** eq-solves-service: Calendar + every people-list in Service made canonical, 3 database updates shipped to live (2026-08-17)

- [ ] **Not clicked through live by a real signed-in user** — verified via code review, live-database dry-runs, and clean CI, not by actually opening the Calendar page and checking the technician/supervisor dropdowns show the right names. _(added 2026-08-17)_

---

**From:** eq-solves-service: any signed-in worker — apprentice, labour hire, subcontractor — could write maintenance checks, defects, test results and assets straight to the database, skipping every in-app permission check. Fixed, shipped, and confirmed live (2026-08-16)

- [ ] **Not clicked through live.** The database change is live on production now — worth two minutes to confirm a low-privilege account (apprentice/labour hire/subcontractor) actually gets blocked from writing, and that an assigned technician can still update their own job. Needs a real signed-in session, not checkable from here. _(added 2026-08-16)_

---

**From:** eq-solves-service: NSX Test Report fixed — dead ACB-only fields left it always printing blank sections (2026-08-14)

- [ ] **Not click-tested against a real generated NSX report** — fix verified via typecheck + code trace only; worth Royce pulling a real NSX Test Report next time one's generated to eyeball the CB Details table looks right. _(added 2026-08-14)_

---

**From:** eq-solves-service: /admin/* pages closed to non-managers (2026-08-14)

- [ ] **Not click-tested by a real non-manager account** — no such login was available in this environment. Worth Royce confirming a technician account gets bounced off `/admin/*` now. _(added 2026-08-14)_

---

**From:** eq-solves-intake + eq-shell: Overview "Fix these" gap cards get a real bulk-fill grid instead of one-row-at-a-time (2026-08-18)

- [ ] **Not click-tested live** — verified via `tsc --noEmit` clean, `vitest run` 50/50, CI green on both PRs, and a Netlify deploy-commit match confirming it's genuinely live — but no authenticated session was available to click through the real UI. Worth 2 minutes: open a "Fix these" card on the Overview tab, fill a few rows in the new grid, Save, confirm the count drops and the score updates. eq-solves-intake [PR #120](https://github.com/eq-solutions/eq-solves-intake/pull/120) + eq-shell [PR #1445](https://github.com/eq-solutions/eq-shell/pull/1445), both merged, live on core.eq.solutions. _(added 2026-08-18)_

---

**From:** eq-shell: Cards iframe was blocking the Web Share API, breaking iOS exports through Shell — fixed, live (2026-08-18)

- [ ] **No live click-through yet** — the fix is confirmed genuinely deployed, but nobody has tapped "Save" on an export through `core.eq.solutions/sks/cards` on an actual iOS device since it landed. _(added 2026-08-18)_

---

**From:** eq-shell: "horrendous" screen-to-screen loading — root cause was full page reloads on every sidebar click, fixed, merged, live (2026-08-18)

- [ ] **Not click-tested live by a person** — verified via typecheck, lint, the full test suite, and confirmed production deploys (exact commit match against what's actually serving), not an actual signed-in click-through. Worth two minutes next time Royce is in Shell: click through Staff → Customers → Field → Admin from the sidebar (should feel instant, no white-flash reload), and confirm ctrl/cmd-click still opens a link in a new tab. _(added 2026-08-18)_

---

**From:** eq-shell: Cards-linked worker's DOB guard was blocking unrelated edits (start date, phone, ...) — found, fixed, merged, live (2026-08-18)

- [ ] **Not clicked through live** — verified by code + typecheck/lint, not by an actual admin editing a Cards-linked worker's start date and a DOB and watching each behave correctly. Worth two minutes: edit Mohammed Hussain's start date (should now save), then try typing a different day/month for a Cards-linked worker (should still correctly block). _(added 2026-08-18)_

---

**From:** eq-shell: the Shell licence-scanner page has never once saved a licence — found, fixed, merged, live (2026-08-17)

- [ ] **Not clicked through live** — verified by code review, live database checks, and a clean preview build, not by an actual person scanning a licence on the real site and watching it save. Worth two minutes on a real account.

---

**From:** eq-shell: a way to hand yourself full admin power through the "custom access groups" screen — found, fixed, and live (2026-08-16)

- [ ] **Not clicked through live** — confirmed by tests and by calling the affected screen's backend directly, not by an actual person building a group in the UI and watching the dangerous options disappear. Worth two minutes on a real admin account. _(added 2026-08-16)_

---

**From:** eq-shell: an AI tool anyone signed in could use to run up costs on the company's AI account — closed, merged, live (2026-08-16)

- [ ] **Not clicked through live yet.** Worth two minutes: try the AI import on a real file, look at the home-page briefing/ask bar as a manager vs. a supervisor, and try opening the licence-scan page as an apprentice (should now say you don't have access). _(added 2026-08-16)_

---

**From:** eq-shell: account-enumeration hole closed on the phone+PIN sign-in door (2026-08-15)

- [ ] **Not click-tested in a browser** — both sign-in doors were checked by calling them directly on production (an unknown mobile and an unknown email each return an identical "no" with no extra detail; the unauthed session check still refuses correctly) plus full CI, but nobody signed in through the actual page. Worth Royce trying two things on his phone: a *wrong* PIN, and a number that has *no* PIN set — both should now show the same "That number and PIN didn't match. If you haven't set a PIN yet, use 'Text me a code instead'". Then sign in by text on an account with no PIN and confirm the "Set a PIN" prompt still appears on the Home screen — that prompt is now the only place that guidance is given. _(added 2026-08-15)_

---

**From:** eq-shell: hard-delete for archived user accounts — built, merged, live (2026-08-14)

- [ ] **Not click-tested live** — same sandbox limitation as everything else this session; built against `tsc`/lint/the permission-drift guard only. _(added 2026-08-14)_

---

**From:** eq-cards: export flow finished end-to-end — Export/Download merged into one sheet, auto-provision session race fixed, export-all PDF/Excel added, PDF photo embed shipped then fixed twice, iOS downloads fixed, two nagging reminders removed (2026-08-18)

- [ ] **No live click-through yet on the Web Share "Save" flow specifically through the Shell iframe** since the `allow="web-share"` fix landed — the permission-policy fix is confirmed live (grepped the deployed Shell bundle for `allow:"web-share"`), but nobody has tapped Save through `core.eq.solutions/sks/cards` since. _(added 2026-08-18)_

---

**From:** eq-cards: 3 permission-audit gaps closed — dead JWT minter retired, empty employer credential list fixed, unreachable admin policy fixed (2026-08-16)

- [ ] **Live click-through not done on the credential-list fix specifically.** Verified via live RLS/RPC checks, CI (`flutter analyze` + `flutter test`), and the deploy's ETag change — not by an actual signed-in admin opening a worker's detail screen and seeing their credentials render. _(added 2026-08-16)_

---

**From:** eq-field: apprentices can self-create their initial profile (2026-08-18)

- [ ] **Not click-tested live by a real self-signed-up apprentice** — same SKS Core-only sandbox limitation as PR #722 below. _(added 2026-08-18)_

---

**From:** eq-field: apprentice list fail-open bug + full onboarding/login audit across ehow, jvkn, Sentry (2026-08-18)

- [ ] **Not click-tested live as a non-manager** — same SKS Core-only sandbox limitation as PR #720's own entry below; verified via CI + live DB trace instead. _(added 2026-08-18)_

---

**From:** eq-solves-service: unchecked-Supabase-query-error bug fully closed out across all 55 `page.tsx` files — dashboard fixed by hand, the remaining 30 swept by 5 parallel isolated-worktree agents, all 6 PRs merged and confirmed live (2026-08-19)

- [ ] **Not click-tested live by a real signed-in user, across all 43 touched files now (dashboard + the 30-file sweep)** — verified via `tsc --noEmit`, CI (only the pre-existing Integration-tests flake failed on every PR), and Netlify commit-ancestry/secret-scan checks, not by actually loading the app and triggering a real query failure. Sentry MCP wasn't authenticated in this session either, so none of the new `route:`-tagged error captures have been watched for live. _(added 2026-08-19)_

---

**From:** eq-solves-service: classification gate built for contract-scope timing — merged, live-verified (2026-08-19)

- [ ] **Not click-tested live** — verified via full type-check + production build, not a real signed-in click-through. Worth a few minutes: open a scope item, try all three timing options, confirm the label looks right, press Generate Calendar once; separately, run an import and confirm the batch timing picker sets the right dates. A working live-session path now exists for this app (`claude-in-chrome` MCP against Royce's own already-authenticated Shell browser session — used 2026-08-20 to click-test the job-plans Global-scope filter fix), so "no working local sign-in" is no longer the real blocker; a bare local dev server still has no session, but that workaround does. _(added 2026-08-19, updated 2026-08-20)_

---

**From:** eq-solves-service: click-to-create on the calendar, a working "reconnect" button on session timeouts, faster warm-up after a deploy, and a safety net for lost in-progress readings (2026-08-18)

- [ ] **Not click-tested live by a real signed-in user.** This session's sandbox has no working login for service.eq.solutions — verified via type-checking and a full production build only. Worth two minutes clicking a calendar day, triggering a session timeout, and filling in part of an ACB/NSX/RCD check then reloading to confirm the draft comes back. _(added 2026-08-18)_

---

**From:** eq-solves-service: Calendar + every people-list in Service made canonical, 3 database updates shipped to live (2026-08-17)

- [ ] **Not clicked through live by a real signed-in user** — verified via code review, live-database dry-runs, and clean CI, not by actually opening the Calendar page and checking the technician/supervisor dropdowns show the right names. _(added 2026-08-17)_

---

**From:** eq-solves-service: any signed-in worker — apprentice, labour hire, subcontractor — could write maintenance checks, defects, test results and assets straight to the database, skipping every in-app permission check. Fixed, shipped, and confirmed live (2026-08-16)

- [ ] **Not clicked through live.** The database change is live on production now — worth two minutes to confirm a low-privilege account (apprentice/labour hire/subcontractor) actually gets blocked from writing, and that an assigned technician can still update their own job. Needs a real signed-in session, not checkable from here. _(added 2026-08-16)_

---

**From:** eq-solves-service: NSX Test Report fixed — dead ACB-only fields left it always printing blank sections (2026-08-14)

- [ ] **Not click-tested against a real generated NSX report** — fix verified via typecheck + code trace only; worth Royce pulling a real NSX Test Report next time one's generated to eyeball the CB Details table looks right. _(added 2026-08-14)_

---

**From:** eq-solves-service: /admin/* pages closed to non-managers (2026-08-14)

- [ ] **Not click-tested by a real non-manager account** — no such login was available in this environment. Worth Royce confirming a technician account gets bounced off `/admin/*` now. _(added 2026-08-14)_

---

**From:** eq-solves-intake + eq-shell: Overview "Fix these" gap cards get a real bulk-fill grid instead of one-row-at-a-time (2026-08-18)

- [ ] **Not click-tested live** — verified via `tsc --noEmit` clean, `vitest run` 50/50, CI green on both PRs, and a Netlify deploy-commit match confirming it's genuinely live — but no authenticated session was available to click through the real UI. Worth 2 minutes: open a "Fix these" card on the Overview tab, fill a few rows in the new grid, Save, confirm the count drops and the score updates. eq-solves-intake [PR #120](https://github.com/eq-solutions/eq-solves-intake/pull/120) + eq-shell [PR #1445](https://github.com/eq-solutions/eq-shell/pull/1445), both merged, live on core.eq.solutions. _(added 2026-08-18)_

---

**From:** eq-shell: Documents "duplicate" rows were phantom onboarding-push sign-offs, not real duplicates — root-caused, fixed, merged, live (2026-08-20)

- [ ] **Not click-tested live** — verified via typecheck/lint/376 tests and confirmed production deploys (exact commit match) for both PRs, not an actual admin session. Worth two minutes: open the Reference library (should show 16 documents, not 44) and try "Push to more people" on an existing Register document. _(added 2026-08-20)_

---

**From:** eq-shell: QR self-join workers showed as never logged in on Admin Users — root-caused, fixed, merged, live (2026-08-20)

- [ ] **Not click-tested live by a person** — verified via typecheck, lint, and exact commit-ancestry against the live production deploy, not by watching a real QR joiner's row actually change on `/sks/admin/users`. Worth a look next time someone joins via a self-join link. _(added 2026-08-20)_

---

**From:** eq-shell: full navigation-by-role audit — 6 gate fixes + 3 dead pages removed, merged, live (2026-08-19)

- [ ] **Not clicked through live** — confirmed by typecheck, the permission-drift guard, and a direct jvkn query proving the Comms fix is a no-op today, not by an actual signed-in click-through. Worth two minutes on NSW Comms, the Ops tile as apprentice/labour_hire/subcontractor, and the mobile Reports row. _(added 2026-08-19)_

---

**From:** eq-shell: Cards iframe was blocking the Web Share API, breaking iOS exports through Shell — fixed, live (2026-08-18)

- [ ] **No live click-through yet** — the fix is confirmed genuinely deployed, but nobody has tapped "Save" on an export through `core.eq.solutions/sks/cards` on an actual iOS device since it landed. _(added 2026-08-18)_

---

**From:** eq-shell: "horrendous" screen-to-screen loading — root cause was full page reloads on every sidebar click, fixed, merged, live (2026-08-18)

- [ ] **Not click-tested live by a person** — verified via typecheck, lint, the full test suite, and confirmed production deploys (exact commit match against what's actually serving), not an actual signed-in click-through. Worth two minutes next time Royce is in Shell: click through Staff → Customers → Field → Admin from the sidebar (should feel instant, no white-flash reload), and confirm ctrl/cmd-click still opens a link in a new tab. _(added 2026-08-18)_

---

**From:** eq-shell: Cards-linked worker's DOB guard was blocking unrelated edits (start date, phone, ...) — found, fixed, merged, live (2026-08-18)

- [ ] **Not clicked through live** — verified by code + typecheck/lint, not by an actual admin editing a Cards-linked worker's start date and a DOB and watching each behave correctly. Worth two minutes: edit Mohammed Hussain's start date (should now save), then try typing a different day/month for a Cards-linked worker (should still correctly block). _(added 2026-08-18)_

---

**From:** eq-shell: the Shell licence-scanner page has never once saved a licence — found, fixed, merged, live (2026-08-17)

- [ ] **Not clicked through live** — verified by code review, live database checks, and a clean preview build, not by an actual person scanning a licence on the real site and watching it save. Worth two minutes on a real account.

---

**From:** eq-shell: a way to hand yourself full admin power through the "custom access groups" screen — found, fixed, and live (2026-08-16)

- [ ] **Not clicked through live** — confirmed by tests and by calling the affected screen's backend directly, not by an actual person building a group in the UI and watching the dangerous options disappear. Worth two minutes on a real admin account. _(added 2026-08-16)_

---

**From:** eq-shell: an AI tool anyone signed in could use to run up costs on the company's AI account — closed, merged, live (2026-08-16)

- [ ] **Not clicked through live yet.** Worth two minutes: try the AI import on a real file, look at the home-page briefing/ask bar as a manager vs. a supervisor, and try opening the licence-scan page as an apprentice (should now say you don't have access). _(added 2026-08-16)_

---

**From:** eq-shell: account-enumeration hole closed on the phone+PIN sign-in door (2026-08-15)

- [ ] **Not click-tested in a browser** — both sign-in doors were checked by calling them directly on production (an unknown mobile and an unknown email each return an identical "no" with no extra detail; the unauthed session check still refuses correctly) plus full CI, but nobody signed in through the actual page. Worth Royce trying two things on his phone: a *wrong* PIN, and a number that has *no* PIN set — both should now show the same "That number and PIN didn't match. If you haven't set a PIN yet, use 'Text me a code instead'". Then sign in by text on an account with no PIN and confirm the "Set a PIN" prompt still appears on the Home screen — that prompt is now the only place that guidance is given. _(added 2026-08-15)_

---

**From:** eq-shell: hard-delete for archived user accounts — built, merged, live (2026-08-14)

- [ ] **Not click-tested live** — same sandbox limitation as everything else this session; built against `tsc`/lint/the permission-drift guard only. _(added 2026-08-14)_

---

**From:** eq-shell: Staff page load time fixed + funnel filters added to Contact, Status, Birthday (2026-08-20)

- [ ] **Live click-through not done** — verified via CI (typecheck/lint/tests) and confirmed production deploy state matching the merge commit, not by an actual signed-in click through Staff. Worth two minutes next time Royce is in Shell: confirm the Contact/Status/Birthday filter icons open a working checkbox list. _(added 2026-08-20)_

---

**From:** eq-cards: export flow finished end-to-end — Export/Download merged into one sheet, auto-provision session race fixed, export-all PDF/Excel added, PDF photo embed shipped then fixed twice, iOS downloads fixed, two nagging reminders removed (2026-08-18)

- [ ] **No live click-through yet on the Web Share "Save" flow specifically through the Shell iframe** since the `allow="web-share"` fix landed — the permission-policy fix is confirmed live (grepped the deployed Shell bundle for `allow:"web-share"`), but nobody has tapped Save through `core.eq.solutions/sks/cards` since. _(added 2026-08-18)_

---

**From:** eq-cards: 3 permission-audit gaps closed — dead JWT minter retired, empty employer credential list fixed, unreachable admin policy fixed (2026-08-16)

- [ ] **Live click-through not done on the credential-list fix specifically.** Verified via live RLS/RPC checks, CI (`flutter analyze` + `flutter test`), and the deploy's ETag change — not by an actual signed-in admin opening a worker's detail screen and seeing their credentials render. _(added 2026-08-16)_

---

**From:** eq-field: apprentices can self-create their initial profile (2026-08-18)

- [ ] **Not click-tested live by a real self-signed-up apprentice** — same SKS Core-only sandbox limitation as PR #722 below. _(added 2026-08-18)_

---

**From:** eq-field: apprentice list fail-open bug + full onboarding/login audit across ehow, jvkn, Sentry (2026-08-18)

- [ ] **Not click-tested live as a non-manager** — same SKS Core-only sandbox limitation as PR #720's own entry below; verified via CI + live DB trace instead. _(added 2026-08-18)_

---

**From:** eq-solves-service: Shell session keepalive found permanently dying on any hiccup — fixed, merged, confirmed live (2026-08-20)

- [ ] **Not click-tested live in an actual embedded Shell session** — verified via 15 targeted automated tests (8 of which fail against the original broken code, proving they're real regression tests, not vacuous ones), a full clean production build, and full lint, not by watching a real technician's session survive a real dropped connection on-site. _(added 2026-08-20)_

---

**From:** eq-solves-service: unchecked-Supabase-query-error bug fully closed out across all 55 `page.tsx` files — dashboard fixed by hand, the remaining 30 swept by 5 parallel isolated-worktree agents, all 6 PRs merged and confirmed live (2026-08-19)

- [ ] **Not click-tested live by a real signed-in user, across all 43 touched files now (dashboard + the 30-file sweep)** — verified via `tsc --noEmit`, CI (only the pre-existing Integration-tests flake failed on every PR), and Netlify commit-ancestry/secret-scan checks, not by actually loading the app and triggering a real query failure. Sentry MCP wasn't authenticated in this session either, so none of the new `route:`-tagged error captures have been watched for live. _(added 2026-08-19)_

---

**From:** eq-solves-service: classification gate built for contract-scope timing — merged, live-verified (2026-08-19)

- [ ] **Not click-tested live** — verified via full type-check + production build, not a real signed-in click-through. Worth a few minutes: open a scope item, try all three timing options, confirm the label looks right, press Generate Calendar once; separately, run an import and confirm the batch timing picker sets the right dates. A working live-session path now exists for this app (`claude-in-chrome` MCP against Royce's own already-authenticated Shell browser session — used 2026-08-20 to click-test the job-plans Global-scope filter fix), so "no working local sign-in" is no longer the real blocker; a bare local dev server still has no session, but that workaround does. _(added 2026-08-19, updated 2026-08-20)_

---

**From:** eq-solves-service: click-to-create on the calendar, a working "reconnect" button on session timeouts, faster warm-up after a deploy, and a safety net for lost in-progress readings (2026-08-18)

- [ ] **Not click-tested live by a real signed-in user.** This session's sandbox has no working login for service.eq.solutions — verified via type-checking and a full production build only. Worth two minutes clicking a calendar day, triggering a session timeout, and filling in part of an ACB/NSX/RCD check then reloading to confirm the draft comes back. _(added 2026-08-18)_

---

**From:** eq-solves-service: Calendar + every people-list in Service made canonical, 3 database updates shipped to live (2026-08-17)

- [ ] **Not clicked through live by a real signed-in user** — verified via code review, live-database dry-runs, and clean CI, not by actually opening the Calendar page and checking the technician/supervisor dropdowns show the right names. _(added 2026-08-17)_

---

**From:** eq-solves-service: any signed-in worker — apprentice, labour hire, subcontractor — could write maintenance checks, defects, test results and assets straight to the database, skipping every in-app permission check. Fixed, shipped, and confirmed live (2026-08-16)

- [ ] **Not clicked through live.** The database change is live on production now — worth two minutes to confirm a low-privilege account (apprentice/labour hire/subcontractor) actually gets blocked from writing, and that an assigned technician can still update their own job. Needs a real signed-in session, not checkable from here. _(added 2026-08-16)_

---

**From:** eq-solves-service: NSX Test Report fixed — dead ACB-only fields left it always printing blank sections (2026-08-14)

- [ ] **Not click-tested against a real generated NSX report** — fix verified via typecheck + code trace only; worth Royce pulling a real NSX Test Report next time one's generated to eyeball the CB Details table looks right. _(added 2026-08-14)_

---

**From:** eq-solves-service: /admin/* pages closed to non-managers (2026-08-14)

- [ ] **Not click-tested by a real non-manager account** — no such login was available in this environment. Worth Royce confirming a technician account gets bounced off `/admin/*` now. _(added 2026-08-14)_

---

**From:** eq-solves-intake + eq-shell: Overview "Fix these" gap cards get a real bulk-fill grid instead of one-row-at-a-time (2026-08-18)

- [ ] **Not click-tested live** — verified via `tsc --noEmit` clean, `vitest run` 50/50, CI green on both PRs, and a Netlify deploy-commit match confirming it's genuinely live — but no authenticated session was available to click through the real UI. Worth 2 minutes: open a "Fix these" card on the Overview tab, fill a few rows in the new grid, Save, confirm the count drops and the score updates. eq-solves-intake [PR #120](https://github.com/eq-solutions/eq-solves-intake/pull/120) + eq-shell [PR #1445](https://github.com/eq-solutions/eq-shell/pull/1445), both merged, live on core.eq.solutions. _(added 2026-08-18)_

---

**From:** eq-shell: Documents "duplicate" rows were phantom onboarding-push sign-offs, not real duplicates — root-caused, fixed, merged, live (2026-08-20)

- [ ] **Not click-tested live** — verified via typecheck/lint/376 tests and confirmed production deploys (exact commit match) for both PRs, not an actual admin session. Worth two minutes: open the Reference library (should show 16 documents, not 44) and try "Push to more people" on an existing Register document. _(added 2026-08-20)_

---

**From:** eq-shell: QR self-join workers showed as never logged in on Admin Users — root-caused, fixed, merged, live (2026-08-20)

- [ ] **Not click-tested live by a person** — verified via typecheck, lint, and exact commit-ancestry against the live production deploy, not by watching a real QR joiner's row actually change on `/sks/admin/users`. Worth a look next time someone joins via a self-join link. _(added 2026-08-20)_

---

**From:** eq-shell: full navigation-by-role audit — 6 gate fixes + 3 dead pages removed, merged, live (2026-08-19)

- [ ] **Not clicked through live** — confirmed by typecheck, the permission-drift guard, and a direct jvkn query proving the Comms fix is a no-op today, not by an actual signed-in click-through. Worth two minutes on NSW Comms, the Ops tile as apprentice/labour_hire/subcontractor, and the mobile Reports row. _(added 2026-08-19)_

---

**From:** eq-shell: nav-by-role audit continued — HUB_APPS consolidated, 2 more real permission-gate bugs found across a full 6-role ground-up sweep (2026-08-21)

- [ ] **Not click-tested live by a person** — every fix this round verified via `tsc -b --force` + production commit-ancestry against the live deploy, not a real signed-in session. Worth two minutes each: confirm a trial-tier tenant no longer sees Service/Ops on the sidebar, and that a Security-Group-scoped user holding `admin.list_users` but not `admin.manage_groups`/`admin.edit_user` no longer sees the now-hidden links. _(added 2026-08-21)_

---

**From:** eq-shell: Cards iframe was blocking the Web Share API, breaking iOS exports through Shell — fixed, live (2026-08-18)

- [ ] **No live click-through yet** — the fix is confirmed genuinely deployed, but nobody has tapped "Save" on an export through `core.eq.solutions/sks/cards` on an actual iOS device since it landed. _(added 2026-08-18)_

---

**From:** eq-shell: "horrendous" screen-to-screen loading — root cause was full page reloads on every sidebar click, fixed, merged, live (2026-08-18)

- [ ] **Not click-tested live by a person** — verified via typecheck, lint, the full test suite, and confirmed production deploys (exact commit match against what's actually serving), not an actual signed-in click-through. Worth two minutes next time Royce is in Shell: click through Staff → Customers → Field → Admin from the sidebar (should feel instant, no white-flash reload), and confirm ctrl/cmd-click still opens a link in a new tab. _(added 2026-08-18)_

---

**From:** eq-shell: Cards-linked worker's DOB guard was blocking unrelated edits (start date, phone, ...) — found, fixed, merged, live (2026-08-18)

- [ ] **Not clicked through live** — verified by code + typecheck/lint, not by an actual admin editing a Cards-linked worker's start date and a DOB and watching each behave correctly. Worth two minutes: edit Mohammed Hussain's start date (should now save), then try typing a different day/month for a Cards-linked worker (should still correctly block). _(added 2026-08-18)_

---

**From:** eq-shell: the Shell licence-scanner page has never once saved a licence — found, fixed, merged, live (2026-08-17)

- [ ] **Not clicked through live** — verified by code review, live database checks, and a clean preview build, not by an actual person scanning a licence on the real site and watching it save. Worth two minutes on a real account.

---

**From:** eq-shell: a way to hand yourself full admin power through the "custom access groups" screen — found, fixed, and live (2026-08-16)

- [ ] **Not clicked through live** — confirmed by tests and by calling the affected screen's backend directly, not by an actual person building a group in the UI and watching the dangerous options disappear. Worth two minutes on a real admin account. _(added 2026-08-16)_

---

**From:** eq-shell: an AI tool anyone signed in could use to run up costs on the company's AI account — closed, merged, live (2026-08-16)

- [ ] **Not clicked through live yet.** Worth two minutes: try the AI import on a real file, look at the home-page briefing/ask bar as a manager vs. a supervisor, and try opening the licence-scan page as an apprentice (should now say you don't have access). _(added 2026-08-16)_

---

**From:** eq-shell: account-enumeration hole closed on the phone+PIN sign-in door (2026-08-15)

- [ ] **Not click-tested in a browser** — both sign-in doors were checked by calling them directly on production (an unknown mobile and an unknown email each return an identical "no" with no extra detail; the unauthed session check still refuses correctly) plus full CI, but nobody signed in through the actual page. Worth Royce trying two things on his phone: a *wrong* PIN, and a number that has *no* PIN set — both should now show the same "That number and PIN didn't match. If you haven't set a PIN yet, use 'Text me a code instead'". Then sign in by text on an account with no PIN and confirm the "Set a PIN" prompt still appears on the Home screen — that prompt is now the only place that guidance is given. _(added 2026-08-15)_

---

**From:** eq-shell: hard-delete for archived user accounts — built, merged, live (2026-08-14)

- [ ] **Not click-tested live** — same sandbox limitation as everything else this session; built against `tsc`/lint/the permission-drift guard only. _(added 2026-08-14)_

---

**From:** eq-shell: Staff page load time fixed + funnel filters added to Contact, Status, Birthday (2026-08-20)

- [ ] **Live click-through not done** — verified via CI (typecheck/lint/tests) and confirmed production deploy state matching the merge commit, not by an actual signed-in click through Staff. Worth two minutes next time Royce is in Shell: confirm the Contact/Status/Birthday filter icons open a working checkbox list. _(added 2026-08-20)_

---

**From:** eq-shell: role-level toggles for Field's 86 fine-grained permissions; deny-support investigated and declined (2026-08-21)

- [ ] **Live click-test not done** — same limitation as every prior PR on this page (#1425, #1429, #1420); needs a real authenticated admin session. Worth two minutes: open a role's Field cell, toggle one of the new checkboxes, confirm it sticks and reaches a live Field session. Full build/decision detail: `sessions/2026-08-23.md`, `eq/changelog/eq-shell.md`, and eq-shell's own memory store (`field-fine-perms-role-matrix.md`). _(added 2026-08-21)_

---

**From:** eq-cards: export flow finished end-to-end — Export/Download merged into one sheet, auto-provision session race fixed, export-all PDF/Excel added, PDF photo embed shipped then fixed twice, iOS downloads fixed, two nagging reminders removed (2026-08-18)

- [ ] **No live click-through yet on the Web Share "Save" flow specifically through the Shell iframe** since the `allow="web-share"` fix landed — the permission-policy fix is confirmed live (grepped the deployed Shell bundle for `allow:"web-share"`), but nobody has tapped Save through `core.eq.solutions/sks/cards` since. _(added 2026-08-18)_

---

**From:** eq-cards: 3 permission-audit gaps closed — dead JWT minter retired, empty employer credential list fixed, unreachable admin policy fixed (2026-08-16)

- [ ] **Live click-through not done on the credential-list fix specifically.** Verified via live RLS/RPC checks, CI (`flutter analyze` + `flutter test`), and the deploy's ETag change — not by an actual signed-in admin opening a worker's detail screen and seeing their credentials render. _(added 2026-08-16)_

---

**From:** eq-field: apprentices can self-create their initial profile (2026-08-18)

- [ ] **Not click-tested live by a real self-signed-up apprentice** — same SKS Core-only sandbox limitation as PR #722 below. _(added 2026-08-18)_

---

**From:** eq-field: apprentice list fail-open bug + full onboarding/login audit across ehow, jvkn, Sentry (2026-08-18)

- [ ] **Not click-tested live as a non-manager** — same SKS Core-only sandbox limitation as PR #720's own entry below; verified via CI + live DB trace instead. _(added 2026-08-18)_

---

**From:** eq-solves-service: Shell session keepalive found permanently dying on any hiccup — fixed, merged, confirmed live (2026-08-20)

- [ ] **Not click-tested live in an actual embedded Shell session** — verified via 15 targeted automated tests (8 of which fail against the original broken code, proving they're real regression tests, not vacuous ones), a full clean production build, and full lint, not by watching a real technician's session survive a real dropped connection on-site. _(added 2026-08-20)_

---

**From:** eq-solves-service: unchecked-Supabase-query-error bug fully closed out across all 55 `page.tsx` files — dashboard fixed by hand, the remaining 30 swept by 5 parallel isolated-worktree agents, all 6 PRs merged and confirmed live (2026-08-19)

- [ ] **Not click-tested live by a real signed-in user, across all 43 touched files now (dashboard + the 30-file sweep)** — verified via `tsc --noEmit`, CI (only the pre-existing Integration-tests flake failed on every PR), and Netlify commit-ancestry/secret-scan checks, not by actually loading the app and triggering a real query failure. Sentry MCP wasn't authenticated in this session either, so none of the new `route:`-tagged error captures have been watched for live. _(added 2026-08-19)_

---

**From:** eq-solves-service: classification gate built for contract-scope timing — merged, live-verified (2026-08-19)

- [ ] **Not click-tested live** — verified via full type-check + production build, not a real signed-in click-through. Worth a few minutes: open a scope item, try all three timing options, confirm the label looks right, press Generate Calendar once; separately, run an import and confirm the batch timing picker sets the right dates. A working live-session path now exists for this app (`claude-in-chrome` MCP against Royce's own already-authenticated Shell browser session — used 2026-08-20 to click-test the job-plans Global-scope filter fix), so "no working local sign-in" is no longer the real blocker; a bare local dev server still has no session, but that workaround does. _(added 2026-08-19, updated 2026-08-20)_

---

**From:** eq-solves-service: click-to-create on the calendar, a working "reconnect" button on session timeouts, faster warm-up after a deploy, and a safety net for lost in-progress readings (2026-08-18)

- [ ] **Not click-tested live by a real signed-in user.** This session's sandbox has no working login for service.eq.solutions — verified via type-checking and a full production build only. Worth two minutes clicking a calendar day, triggering a session timeout, and filling in part of an ACB/NSX/RCD check then reloading to confirm the draft comes back. _(added 2026-08-18)_

---

**From:** eq-solves-service: Calendar + every people-list in Service made canonical, 3 database updates shipped to live (2026-08-17)

- [ ] **Not clicked through live by a real signed-in user** — verified via code review, live-database dry-runs, and clean CI, not by actually opening the Calendar page and checking the technician/supervisor dropdowns show the right names. _(added 2026-08-17)_

---

**From:** eq-solves-service: any signed-in worker — apprentice, labour hire, subcontractor — could write maintenance checks, defects, test results and assets straight to the database, skipping every in-app permission check. Fixed, shipped, and confirmed live (2026-08-16)

- [ ] **Not clicked through live.** The database change is live on production now — worth two minutes to confirm a low-privilege account (apprentice/labour hire/subcontractor) actually gets blocked from writing, and that an assigned technician can still update their own job. Needs a real signed-in session, not checkable from here. _(added 2026-08-16)_

---

**From:** eq-solves-service: NSX Test Report fixed — dead ACB-only fields left it always printing blank sections (2026-08-14)

- [ ] **Not click-tested against a real generated NSX report** — fix verified via typecheck + code trace only; worth Royce pulling a real NSX Test Report next time one's generated to eyeball the CB Details table looks right. _(added 2026-08-14)_

---

**From:** eq-solves-service: /admin/* pages closed to non-managers (2026-08-14)

- [ ] **Not click-tested by a real non-manager account** — no such login was available in this environment. Worth Royce confirming a technician account gets bounced off `/admin/*` now. _(added 2026-08-14)_

---

**From:** eq-solves-intake + eq-shell: Overview "Fix these" gap cards get a real bulk-fill grid instead of one-row-at-a-time (2026-08-18)

- [ ] **Not click-tested live** — verified via `tsc --noEmit` clean, `vitest run` 50/50, CI green on both PRs, and a Netlify deploy-commit match confirming it's genuinely live — but no authenticated session was available to click through the real UI. Worth 2 minutes: open a "Fix these" card on the Overview tab, fill a few rows in the new grid, Save, confirm the count drops and the score updates. eq-solves-intake [PR #120](https://github.com/eq-solutions/eq-solves-intake/pull/120) + eq-shell [PR #1445](https://github.com/eq-solutions/eq-shell/pull/1445), both merged, live on core.eq.solutions. _(added 2026-08-18)_

---

**From:** eq-shell: Documents "duplicate" rows were phantom onboarding-push sign-offs, not real duplicates — root-caused, fixed, merged, live (2026-08-20)

- [ ] **Not click-tested live** — verified via typecheck/lint/376 tests and confirmed production deploys (exact commit match) for both PRs, not an actual admin session. Worth two minutes: open the Reference library (should show 16 documents, not 44) and try "Push to more people" on an existing Register document. _(added 2026-08-20)_

---

**From:** eq-shell: QR self-join workers showed as never logged in on Admin Users — root-caused, fixed, merged, live (2026-08-20)

- [ ] **Not click-tested live by a person** — verified via typecheck, lint, and exact commit-ancestry against the live production deploy, not by watching a real QR joiner's row actually change on `/sks/admin/users`. Worth a look next time someone joins via a self-join link. _(added 2026-08-20)_

---

**From:** eq-shell: full navigation-by-role audit — 6 gate fixes + 3 dead pages removed, merged, live (2026-08-19)

- [ ] **Not clicked through live** — confirmed by typecheck, the permission-drift guard, and a direct jvkn query proving the Comms fix is a no-op today, not by an actual signed-in click-through. Worth two minutes on NSW Comms, the Ops tile as apprentice/labour_hire/subcontractor, and the mobile Reports row. _(added 2026-08-19)_

---

**From:** eq-shell: nav-by-role audit continued — HUB_APPS consolidated, 2 more real permission-gate bugs found across a full 6-role ground-up sweep (2026-08-21)

- [ ] **Not click-tested live by a person** — every fix this round verified via `tsc -b --force` + production commit-ancestry against the live deploy, not a real signed-in session. Worth two minutes each: confirm a trial-tier tenant no longer sees Service/Ops on the sidebar, and that a Security-Group-scoped user holding `admin.list_users` but not `admin.manage_groups`/`admin.edit_user` no longer sees the now-hidden links. _(added 2026-08-21)_

---

**From:** eq-shell: Cards iframe was blocking the Web Share API, breaking iOS exports through Shell — fixed, live (2026-08-18)

- [ ] **No live click-through yet** — the fix is confirmed genuinely deployed, but nobody has tapped "Save" on an export through `core.eq.solutions/sks/cards` on an actual iOS device since it landed. _(added 2026-08-18)_

---

**From:** eq-shell: "horrendous" screen-to-screen loading — root cause was full page reloads on every sidebar click, fixed, merged, live (2026-08-18)

- [ ] **Not click-tested live by a person** — verified via typecheck, lint, the full test suite, and confirmed production deploys (exact commit match against what's actually serving), not an actual signed-in click-through. Worth two minutes next time Royce is in Shell: click through Staff → Customers → Field → Admin from the sidebar (should feel instant, no white-flash reload), and confirm ctrl/cmd-click still opens a link in a new tab. _(added 2026-08-18)_

---

**From:** eq-shell: Cards-linked worker's DOB guard was blocking unrelated edits (start date, phone, ...) — found, fixed, merged, live (2026-08-18)

- [ ] **Not clicked through live** — verified by code + typecheck/lint, not by an actual admin editing a Cards-linked worker's start date and a DOB and watching each behave correctly. Worth two minutes: edit Mohammed Hussain's start date (should now save), then try typing a different day/month for a Cards-linked worker (should still correctly block). _(added 2026-08-18)_

---

**From:** eq-shell: the Shell licence-scanner page has never once saved a licence — found, fixed, merged, live (2026-08-17)

- [ ] **Not clicked through live** — verified by code review, live database checks, and a clean preview build, not by an actual person scanning a licence on the real site and watching it save. Worth two minutes on a real account.

---

**From:** eq-shell: a way to hand yourself full admin power through the "custom access groups" screen — found, fixed, and live (2026-08-16)

- [ ] **Not clicked through live** — confirmed by tests and by calling the affected screen's backend directly, not by an actual person building a group in the UI and watching the dangerous options disappear. Worth two minutes on a real admin account. _(added 2026-08-16)_

---

**From:** eq-shell: an AI tool anyone signed in could use to run up costs on the company's AI account — closed, merged, live (2026-08-16)

- [ ] **Not clicked through live yet.** Worth two minutes: try the AI import on a real file, look at the home-page briefing/ask bar as a manager vs. a supervisor, and try opening the licence-scan page as an apprentice (should now say you don't have access). _(added 2026-08-16)_

---

**From:** eq-shell: account-enumeration hole closed on the phone+PIN sign-in door (2026-08-15)

- [ ] **Not click-tested in a browser** — both sign-in doors were checked by calling them directly on production (an unknown mobile and an unknown email each return an identical "no" with no extra detail; the unauthed session check still refuses correctly) plus full CI, but nobody signed in through the actual page. Worth Royce trying two things on his phone: a *wrong* PIN, and a number that has *no* PIN set — both should now show the same "That number and PIN didn't match. If you haven't set a PIN yet, use 'Text me a code instead'". Then sign in by text on an account with no PIN and confirm the "Set a PIN" prompt still appears on the Home screen — that prompt is now the only place that guidance is given. _(added 2026-08-15)_

---

**From:** eq-shell: hard-delete for archived user accounts — built, merged, live (2026-08-14)

- [ ] **Not click-tested live** — same sandbox limitation as everything else this session; built against `tsc`/lint/the permission-drift guard only. _(added 2026-08-14)_

---

**From:** eq-shell: Staff page load time fixed + funnel filters added to Contact, Status, Birthday (2026-08-20)

- [ ] **Live click-through not done** — verified via CI (typecheck/lint/tests) and confirmed production deploy state matching the merge commit, not by an actual signed-in click through Staff. Worth two minutes next time Royce is in Shell: confirm the Contact/Status/Birthday filter icons open a working checkbox list. _(added 2026-08-20)_

---

**From:** eq-shell: role-level toggles for Field's 86 fine-grained permissions; deny-support investigated and declined (2026-08-21)

- [ ] **Live click-test not done** — same limitation as every prior PR on this page (#1425, #1429, #1420); needs a real authenticated admin session. Worth two minutes: open a role's Field cell, toggle one of the new checkboxes, confirm it sticks and reaches a live Field session. Full build/decision detail: `sessions/2026-08-23.md`, `eq/changelog/eq-shell.md`, and eq-shell's own memory store (`field-fine-perms-role-matrix.md`). _(added 2026-08-21)_

---

**From:** eq-cards: export flow finished end-to-end — Export/Download merged into one sheet, auto-provision session race fixed, export-all PDF/Excel added, PDF photo embed shipped then fixed twice, iOS downloads fixed, two nagging reminders removed (2026-08-18)

- [ ] **No live click-through yet on the Web Share "Save" flow specifically through the Shell iframe** since the `allow="web-share"` fix landed — the permission-policy fix is confirmed live (grepped the deployed Shell bundle for `allow:"web-share"`), but nobody has tapped Save through `core.eq.solutions/sks/cards` since. _(added 2026-08-18)_

---

**From:** eq-cards: 3 permission-audit gaps closed — dead JWT minter retired, empty employer credential list fixed, unreachable admin policy fixed (2026-08-16)

- [ ] **Live click-through not done on the credential-list fix specifically.** Verified via live RLS/RPC checks, CI (`flutter analyze` + `flutter test`), and the deploy's ETag change — not by an actual signed-in admin opening a worker's detail screen and seeing their credentials render. _(added 2026-08-16)_

---

**From:** eq-field: apprentices can self-create their initial profile (2026-08-18)

- [ ] **Not click-tested live by a real self-signed-up apprentice** — same SKS Core-only sandbox limitation as PR #722 below. _(added 2026-08-18)_

---

**From:** eq-field: apprentice list fail-open bug + full onboarding/login audit across ehow, jvkn, Sentry (2026-08-18)

- [ ] **Not click-tested live as a non-manager** — same SKS Core-only sandbox limitation as PR #720's own entry below; verified via CI + live DB trace instead. _(added 2026-08-18)_

---

**From:** eq-solves-service: Shell session keepalive found permanently dying on any hiccup — fixed, merged, confirmed live (2026-08-20)

- [ ] **Not click-tested live in an actual embedded Shell session** — verified via 15 targeted automated tests (8 of which fail against the original broken code, proving they're real regression tests, not vacuous ones), a full clean production build, and full lint, not by watching a real technician's session survive a real dropped connection on-site. _(added 2026-08-20)_

---

**From:** eq-solves-service: unchecked-Supabase-query-error bug fully closed out across all 55 `page.tsx` files — dashboard fixed by hand, the remaining 30 swept by 5 parallel isolated-worktree agents, all 6 PRs merged and confirmed live (2026-08-19)

- [ ] **Not click-tested live by a real signed-in user, across all 43 touched files now (dashboard + the 30-file sweep)** — verified via `tsc --noEmit`, CI (only the pre-existing Integration-tests flake failed on every PR), and Netlify commit-ancestry/secret-scan checks, not by actually loading the app and triggering a real query failure. Sentry MCP wasn't authenticated in this session either, so none of the new `route:`-tagged error captures have been watched for live. _(added 2026-08-19)_

---

**From:** eq-solves-service: classification gate built for contract-scope timing — merged, live-verified (2026-08-19)

- [ ] **Not click-tested live** — verified via full type-check + production build, not a real signed-in click-through. Worth a few minutes: open a scope item, try all three timing options, confirm the label looks right, press Generate Calendar once; separately, run an import and confirm the batch timing picker sets the right dates. A working live-session path now exists for this app (`claude-in-chrome` MCP against Royce's own already-authenticated Shell browser session — used 2026-08-20 to click-test the job-plans Global-scope filter fix), so "no working local sign-in" is no longer the real blocker; a bare local dev server still has no session, but that workaround does. _(added 2026-08-19, updated 2026-08-20)_

---

**From:** eq-solves-service: click-to-create on the calendar, a working "reconnect" button on session timeouts, faster warm-up after a deploy, and a safety net for lost in-progress readings (2026-08-18)

- [ ] **Not click-tested live by a real signed-in user.** This session's sandbox has no working login for service.eq.solutions — verified via type-checking and a full production build only. Worth two minutes clicking a calendar day, triggering a session timeout, and filling in part of an ACB/NSX/RCD check then reloading to confirm the draft comes back. _(added 2026-08-18)_

---

**From:** eq-solves-service: Calendar + every people-list in Service made canonical, 3 database updates shipped to live (2026-08-17)

- [ ] **Not clicked through live by a real signed-in user** — verified via code review, live-database dry-runs, and clean CI, not by actually opening the Calendar page and checking the technician/supervisor dropdowns show the right names. _(added 2026-08-17)_

---

**From:** eq-solves-service: any signed-in worker — apprentice, labour hire, subcontractor — could write maintenance checks, defects, test results and assets straight to the database, skipping every in-app permission check. Fixed, shipped, and confirmed live (2026-08-16)

- [ ] **Not clicked through live.** The database change is live on production now — worth two minutes to confirm a low-privilege account (apprentice/labour hire/subcontractor) actually gets blocked from writing, and that an assigned technician can still update their own job. Needs a real signed-in session, not checkable from here. _(added 2026-08-16)_

---

**From:** eq-solves-service: NSX Test Report fixed — dead ACB-only fields left it always printing blank sections (2026-08-14)

- [ ] **Not click-tested against a real generated NSX report** — fix verified via typecheck + code trace only; worth Royce pulling a real NSX Test Report next time one's generated to eyeball the CB Details table looks right. _(added 2026-08-14)_

---

**From:** eq-solves-service: /admin/* pages closed to non-managers (2026-08-14)

- [ ] **Not click-tested by a real non-manager account** — no such login was available in this environment. Worth Royce confirming a technician account gets bounced off `/admin/*` now. _(added 2026-08-14)_

---

**From:** eq-solves-intake + eq-shell: Overview "Fix these" gap cards get a real bulk-fill grid instead of one-row-at-a-time (2026-08-18)

- [ ] **Not click-tested live** — verified via `tsc --noEmit` clean, `vitest run` 50/50, CI green on both PRs, and a Netlify deploy-commit match confirming it's genuinely live — but no authenticated session was available to click through the real UI. Worth 2 minutes: open a "Fix these" card on the Overview tab, fill a few rows in the new grid, Save, confirm the count drops and the score updates. eq-solves-intake [PR #120](https://github.com/eq-solutions/eq-solves-intake/pull/120) + eq-shell [PR #1445](https://github.com/eq-solutions/eq-shell/pull/1445), both merged, live on core.eq.solutions. _(added 2026-08-18)_

---

**From:** eq-shell: SKS roster editing found broken for 5 days — trigger dropped by migration 0249, fixed + dispatched + merged, live (2026-08-23)

- [ ] **Add and hard-delete still not click-tested live; restore's own bugs are now believed fully fixed but still awaits its first actual successful click.** Edit confirmed 2026-08-23 (Royce's own manager session in the real SKS Field UI, Emergency Contact field on a real person, hard-reload-confirmed both the save and the revert — not just the post-save optimistic UI). Archive confirmed 2026-08-23 (Royce archived a real test person, "Jordan Sample," on the SKS Field Contacts page — verified via direct DB query: `active` flipped to `false` within 25 seconds of the click). Restore itself was live-tested 2026-08-24 and found broken twice more, both now fixed (see the field_people_iud() section below for both). Still unverified by an actual UI session: `savePersonToSB` (add), `restorePersonInSB` (restore — underlying bugs fixed, pending a real click), hard-delete.

---

**From:** eq-shell: Staff page deep-link (`?open=<id>`) tripped react-hooks/set-state-in-effect — fixed (2026-08-23)

- [ ] **Not click-tested live** — verified via eslint/tsc and commit-ancestry against the live deploy, not an actual `?open=<id>` link clicked by a person. Worth confirming next time someone opens a Staff deep-link from the "Ask anything" bar or a Resourcing row click. _(added 2026-08-23)_

---

**From:** eq-shell: compliance-pack "Download ready" click stopped working — fixed via hidden-iframe auto-download (2026-08-23)

- [ ] **Not click-tested live** — verified via `tsc -b --force` and eslint (0 new errors), not an actual file landing in a Downloads folder. Worth confirming next time a pack is built — same ask as the still-open 2026-07-28/07-26 "re-download and eyeball" items further down this file. _(added 2026-08-23)_

---

**From:** eq-shell: Documents "duplicate" rows were phantom onboarding-push sign-offs, not real duplicates — root-caused, fixed, merged, live (2026-08-20)

- [ ] **Not click-tested live** — verified via typecheck/lint/376 tests and confirmed production deploys (exact commit match) for both PRs, not an actual admin session. Worth two minutes: open the Reference library (should show 16 documents, not 44) and try "Push to more people" on an existing Register document. _(added 2026-08-20)_

---

**From:** eq-shell: QR self-join workers showed as never logged in on Admin Users — root-caused, fixed, merged, live (2026-08-20)

- [ ] **Not click-tested live by a person** — verified via typecheck, lint, and exact commit-ancestry against the live production deploy, not by watching a real QR joiner's row actually change on `/sks/admin/users`. Worth a look next time someone joins via a self-join link. _(added 2026-08-20)_

---

**From:** eq-shell: full navigation-by-role audit — 6 gate fixes + 3 dead pages removed, merged, live (2026-08-19)

- [ ] **Not clicked through live** — confirmed by typecheck, the permission-drift guard, and a direct jvkn query proving the Comms fix is a no-op today, not by an actual signed-in click-through. Worth two minutes on NSW Comms, the Ops tile as apprentice/labour_hire/subcontractor, and the mobile Reports row. _(added 2026-08-19)_

---

**From:** eq-shell: nav-by-role audit continued — HUB_APPS consolidated, 2 more real permission-gate bugs found across a full 6-role ground-up sweep (2026-08-21)

- [ ] **Not click-tested live by a person** — every fix this round verified via `tsc -b --force` + production commit-ancestry against the live deploy, not a real signed-in session. Worth two minutes each: confirm a trial-tier tenant no longer sees Service/Ops on the sidebar, and that a Security-Group-scoped user holding `admin.list_users` but not `admin.manage_groups`/`admin.edit_user` no longer sees the now-hidden links. _(added 2026-08-21)_

---

**From:** eq-shell: Cards iframe was blocking the Web Share API, breaking iOS exports through Shell — fixed, live (2026-08-18)

- [ ] **No live click-through yet** — the fix is confirmed genuinely deployed, but nobody has tapped "Save" on an export through `core.eq.solutions/sks/cards` on an actual iOS device since it landed. _(added 2026-08-18)_

---

**From:** eq-shell: "horrendous" screen-to-screen loading — root cause was full page reloads on every sidebar click, fixed, merged, live (2026-08-18)

- [ ] **Not click-tested live by a person** — verified via typecheck, lint, the full test suite, and confirmed production deploys (exact commit match against what's actually serving), not an actual signed-in click-through. Worth two minutes next time Royce is in Shell: click through Staff → Customers → Field → Admin from the sidebar (should feel instant, no white-flash reload), and confirm ctrl/cmd-click still opens a link in a new tab. _(added 2026-08-18)_

---

**From:** eq-shell: Cards-linked worker's DOB guard was blocking unrelated edits (start date, phone, ...) — found, fixed, merged, live (2026-08-18)

- [ ] **Not clicked through live** — verified by code + typecheck/lint, not by an actual admin editing a Cards-linked worker's start date and a DOB and watching each behave correctly. Worth two minutes: edit Mohammed Hussain's start date (should now save), then try typing a different day/month for a Cards-linked worker (should still correctly block). _(added 2026-08-18)_

---

**From:** eq-shell: the Shell licence-scanner page has never once saved a licence — found, fixed, merged, live (2026-08-17)

- [ ] **Not clicked through live** — verified by code review, live database checks, and a clean preview build, not by an actual person scanning a licence on the real site and watching it save. Worth two minutes on a real account.

---

**From:** eq-shell: a way to hand yourself full admin power through the "custom access groups" screen — found, fixed, and live (2026-08-16)

- [ ] **Not clicked through live** — confirmed by tests and by calling the affected screen's backend directly, not by an actual person building a group in the UI and watching the dangerous options disappear. Worth two minutes on a real admin account. _(added 2026-08-16)_

---

**From:** eq-shell: an AI tool anyone signed in could use to run up costs on the company's AI account — closed, merged, live (2026-08-16)

- [ ] **Not clicked through live yet.** Worth two minutes: try the AI import on a real file, look at the home-page briefing/ask bar as a manager vs. a supervisor, and try opening the licence-scan page as an apprentice (should now say you don't have access). _(added 2026-08-16)_

---

**From:** eq-shell: account-enumeration hole closed on the phone+PIN sign-in door (2026-08-15)

- [ ] **Not click-tested in a browser** — both sign-in doors were checked by calling them directly on production (an unknown mobile and an unknown email each return an identical "no" with no extra detail; the unauthed session check still refuses correctly) plus full CI, but nobody signed in through the actual page. Worth Royce trying two things on his phone: a *wrong* PIN, and a number that has *no* PIN set — both should now show the same "That number and PIN didn't match. If you haven't set a PIN yet, use 'Text me a code instead'". Then sign in by text on an account with no PIN and confirm the "Set a PIN" prompt still appears on the Home screen — that prompt is now the only place that guidance is given. _(added 2026-08-15)_

---

**From:** eq-shell: hard-delete for archived user accounts — built, merged, live (2026-08-14)

- [ ] **Not click-tested live** — same sandbox limitation as everything else this session; built against `tsc`/lint/the permission-drift guard only. _(added 2026-08-14)_

---

**From:** eq-shell: Staff page load time fixed + funnel filters added to Contact, Status, Birthday (2026-08-20)

- [ ] **Live click-through not done** — verified via CI (typecheck/lint/tests) and confirmed production deploy state matching the merge commit, not by an actual signed-in click through Staff. Worth two minutes next time Royce is in Shell: confirm the Contact/Status/Birthday filter icons open a working checkbox list. _(added 2026-08-20)_

---

**From:** eq-shell: role-level toggles for Field's 86 fine-grained permissions; deny-support investigated and declined (2026-08-21)

- [ ] **Live click-test not done** — same limitation as every prior PR on this page (#1425, #1429, #1420); needs a real authenticated admin session. Worth two minutes: open a role's Field cell, toggle one of the new checkboxes, confirm it sticks and reaches a live Field session. Full build/decision detail: `sessions/2026-08-23.md`, `eq/changelog/eq-shell.md`, and eq-shell's own memory store (`field-fine-perms-role-matrix.md`). _(added 2026-08-21)_

---

**From:** eq-cards: two admin RPCs silently lost their `authenticated` grant to migration 0131, restored (PR #295 + #296, merged + live 2026-08-23)

- [ ] **Not click-tested live** — nobody has exercised the Cards admin worker-upsert or create-invite flow as a real authenticated org admin since either fix. _(added 2026-08-23)_

---

**From:** eq-cards: export flow finished end-to-end — Export/Download merged into one sheet, auto-provision session race fixed, export-all PDF/Excel added, PDF photo embed shipped then fixed twice, iOS downloads fixed, two nagging reminders removed (2026-08-18)

- [ ] **No live click-through yet on the Web Share "Save" flow specifically through the Shell iframe** since the `allow="web-share"` fix landed — the permission-policy fix is confirmed live (grepped the deployed Shell bundle for `allow:"web-share"`), but nobody has tapped Save through `core.eq.solutions/sks/cards` since. _(added 2026-08-18)_

---

**From:** eq-cards: 3 permission-audit gaps closed — dead JWT minter retired, empty employer credential list fixed, unreachable admin policy fixed (2026-08-16)

- [ ] **Live click-through not done on the credential-list fix specifically.** Verified via live RLS/RPC checks, CI (`flutter analyze` + `flutter test`), and the deploy's ETag change — not by an actual signed-in admin opening a worker's detail screen and seeing their credentials render. _(added 2026-08-16)_

---

**From:** eq-field: apprentices can self-create their initial profile (2026-08-18)

- [ ] **Not click-tested live by a real self-signed-up apprentice** — same SKS Core-only sandbox limitation as PR #722 below. _(added 2026-08-18)_

---

**From:** eq-field: apprentice list fail-open bug + full onboarding/login audit across ehow, jvkn, Sentry (2026-08-18)

- [ ] **Not click-tested live as a non-manager** — same SKS Core-only sandbox limitation as PR #720's own entry below; verified via CI + live DB trace instead. _(added 2026-08-18)_

---

**From:** eq-solves-service: suite-wide grant-drift sweep — 9 functions across jvkn/ehow fixed, zaap confirmed clean (PRs #295/#296/#807/#808/#809, all merged + live 2026-08-23)

- [ ] **Not click-tested live** — none of the 9 fixes have been exercised by a real user/cron run since (beyond the near-miss cron job, which was specifically re-verified). _(added 2026-08-23)_

---

**From:** eq-solves-service: Shell session keepalive found permanently dying on any hiccup — fixed, merged, confirmed live (2026-08-20)

- [ ] **Not click-tested live in an actual embedded Shell session** — verified via 15 targeted automated tests (8 of which fail against the original broken code, proving they're real regression tests, not vacuous ones), a full clean production build, and full lint, not by watching a real technician's session survive a real dropped connection on-site. _(added 2026-08-20)_

---

**From:** eq-solves-service: unchecked-Supabase-query-error bug fully closed out across all 55 `page.tsx` files — dashboard fixed by hand, the remaining 30 swept by 5 parallel isolated-worktree agents, all 6 PRs merged and confirmed live (2026-08-19)

- [ ] **Not click-tested live by a real signed-in user, across all 43 touched files now (dashboard + the 30-file sweep)** — verified via `tsc --noEmit`, CI (only the pre-existing Integration-tests flake failed on every PR), and Netlify commit-ancestry/secret-scan checks, not by actually loading the app and triggering a real query failure. Sentry MCP wasn't authenticated in this session either, so none of the new `route:`-tagged error captures have been watched for live. _(added 2026-08-19)_

---

**From:** eq-solves-service: classification gate built for contract-scope timing — merged, live-verified (2026-08-19)

- [ ] **Not click-tested live** — verified via full type-check + production build, not a real signed-in click-through. Worth a few minutes: open a scope item, try all three timing options, confirm the label looks right, press Generate Calendar once; separately, run an import and confirm the batch timing picker sets the right dates. A working live-session path now exists for this app (`claude-in-chrome` MCP against Royce's own already-authenticated Shell browser session — used 2026-08-20 to click-test the job-plans Global-scope filter fix), so "no working local sign-in" is no longer the real blocker; a bare local dev server still has no session, but that workaround does. _(added 2026-08-19, updated 2026-08-20)_

---

**From:** eq-solves-service: click-to-create on the calendar, a working "reconnect" button on session timeouts, faster warm-up after a deploy, and a safety net for lost in-progress readings (2026-08-18)

- [ ] **Not click-tested live by a real signed-in user.** This session's sandbox has no working login for service.eq.solutions — verified via type-checking and a full production build only. Worth two minutes clicking a calendar day, triggering a session timeout, and filling in part of an ACB/NSX/RCD check then reloading to confirm the draft comes back. _(added 2026-08-18)_

---

**From:** eq-solves-service: Calendar + every people-list in Service made canonical, 3 database updates shipped to live (2026-08-17)

- [ ] **Not clicked through live by a real signed-in user** — verified via code review, live-database dry-runs, and clean CI, not by actually opening the Calendar page and checking the technician/supervisor dropdowns show the right names. _(added 2026-08-17)_

---

**From:** eq-solves-service: any signed-in worker — apprentice, labour hire, subcontractor — could write maintenance checks, defects, test results and assets straight to the database, skipping every in-app permission check. Fixed, shipped, and confirmed live (2026-08-16)

- [ ] **Not clicked through live.** The database change is live on production now — worth two minutes to confirm a low-privilege account (apprentice/labour hire/subcontractor) actually gets blocked from writing, and that an assigned technician can still update their own job. Needs a real signed-in session, not checkable from here. _(added 2026-08-16)_

---

**From:** eq-solves-service: NSX Test Report fixed — dead ACB-only fields left it always printing blank sections (2026-08-14)

- [ ] **Not click-tested against a real generated NSX report** — fix verified via typecheck + code trace only; worth Royce pulling a real NSX Test Report next time one's generated to eyeball the CB Details table looks right. _(added 2026-08-14)_

---

**From:** eq-solves-service: /admin/* pages closed to non-managers (2026-08-14)

- [ ] **Not click-tested by a real non-manager account** — no such login was available in this environment. Worth Royce confirming a technician account gets bounced off `/admin/*` now. _(added 2026-08-14)_

---

**From:** eq-solves-intake + eq-shell: Overview "Fix these" gap cards get a real bulk-fill grid instead of one-row-at-a-time (2026-08-18)

- [ ] **Not click-tested live** — verified via `tsc --noEmit` clean, `vitest run` 50/50, CI green on both PRs, and a Netlify deploy-commit match confirming it's genuinely live — but no authenticated session was available to click through the real UI. Worth 2 minutes: open a "Fix these" card on the Overview tab, fill a few rows in the new grid, Save, confirm the count drops and the score updates. eq-solves-intake [PR #120](https://github.com/eq-solutions/eq-solves-intake/pull/120) + eq-shell [PR #1445](https://github.com/eq-solutions/eq-shell/pull/1445), both merged, live on core.eq.solutions. _(added 2026-08-18)_

---
