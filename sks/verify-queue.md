---
title: SKS Tier — Verify Queue
owner: Royce Milmlow
last_updated: 2026-09-05
scope: Items whose only remaining blocker is your own live sign-in/click-through — the underlying work is already built, merged, and (unless the line itself says otherwise) live. Moved here from sks/pending.md by scripts/rotate_pending.py once a session's real build work is fully done, so a stale "click through to confirm" line no longer pins a whole finished write-up in the live pending doc.
read_priority: high
status: live
---

# SKS Tier — Verify Queue

Nothing left to build on anything below — every line just needs you to
actually open the app and check it. Delete the line once you've confirmed
it. If something's actually broken, that's real signal — flag it back as
a bug rather than just deleting the line.

---

**From:** SKS Field — session 2026-07-21 (mobile My Schedule + home tile: show Sat/Sun when rostered)

- [ ] Royce to click-through confirm a real weekend-rostered person's mobile schedule + home tile on both apps. _(added 2026-07-21)_

---

**From:** Weekly digest opt-in panel silently stopped appearing — fixed (v3.5.390, PR #583, merged 2026-07-31)

- [ ] **Royce to click through live on `core.eq.solutions/sks/field?tab=managers`**: confirm the panel appears with real SKS supervisors listed (not just demo-tenant data), and that toggling a supervisor's opt-in checkbox still saves. Not yet confirmed with real tenant data — only demo-tenant + isolated-harness verified. _(added 2026-07-31)_

---

**From:** Leave — delete an approved request, including its roster entry — shipped (v3.10.111, PR #78, merged 2026-08-10)

- [ ] **Live click-through not done** — verified via a full standalone test in the demo sandbox (stubbed the two network calls since this environment can't reach the real Supabase project) rather than a real production click-through. Royce to confirm on a real approved leave record. _(added 2026-08-10)_

---

**From:** Roster-notification login popup removed (v3.10.110, PR #77, sks-nsw-labour)

- [ ] **Royce to confirm live**: log in for real post-deploy and confirm no popup appears. Superseded by v3.10.111 (PR #78) landing cleanly on top with no reported regression, but that's not the same as an actual click-through. _(added 2026-08-04, recovered from an unpopped stash 2026-08-20 — never made it into this file at the time)_

---

**From:** SKS roster editing was silently broken for 5 days — trigger dropped by migration 0249, fixed + dispatched, live (2026-08-23)

- [ ] **Edit and archive now click-tested live (2026-08-23, Royce's own manager session) — add, restore, and hard-delete still aren't.** Full detail in `eq/pending/eq-shell.md`. _(added 2026-08-23)_

---

**From:** ehow RLS gap — 26 SKS tables were readable/writable cross-tenant, now closed (2026-08-23)

- [ ] **Needs a real SKS login to confirm nothing broke** — apprentice competencies, supervisor/people notes, audit log, tenders, site audits, nominations, pending schedule. Same "not click-tested live by a person" gap as everything else in this queue. _(added 2026-08-23)_

---

**From:** SKS Uniform Order Template added to `sks/templates.md` (2026-09-01)

- [ ] **Division→kit mapping is Title-only, not confirmed** — the Stay Safe catalogue has no per-division SKU split, so the template's 9 roles pick kit by Title (Site/Management/Office) only; Division (Electrical/Comms/AV) currently only drives a suggested embroidery tag. Needs Sharon/Royce to confirm whether Division should actually change colour/garment/embroidery before wider rollout. _(added 2026-09-01)_

---

**From:** SKS login + Timesheets: "click OK to continue" gate on the retirement notices, merged live (2026-09-02)

- [ ] **Not click-tested with real Supabase data** — this environment has no network access to the SKS database, so verification (z-index stacking, backdrop-click protection, OK-button dismissal) ran with the login name picker and timesheet list empty. The logic doesn't depend on data volume, but worth a real click-through when convenient. _(added 2026-09-02)_

---
