---
title: SKS Tier — Verify Queue
owner: Royce Milmlow
last_updated: 2026-08-13
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
