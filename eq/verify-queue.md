---
title: EQ Tier — Verify Queue
owner: Royce Milmlow
last_updated: 2026-08-01
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
