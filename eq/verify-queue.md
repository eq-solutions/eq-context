---
title: EQ Tier — Verify Queue
owner: Royce Milmlow
last_updated: 2026-08-11
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
