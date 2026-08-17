---
title: SKS-tagged (misfiled) — Pending Actions
owner: Royce Milmlow
last_updated: 2026-08-17
scope: Items headed "SKS:" that were sitting in eq/pending.md despite the suite convention that SKS items live in sks/pending.md. Not merged there automatically (a different, more mature tracking system already exists for that file) — flagged here for a human/session to move on purpose.
read_priority: critical
status: live
---

# SKS-tagged (misfiled) — Pending

---

## SKS: QR self-join for 9 named apprentices — cohort verified safe, max-uses cap scoped and held (2026-08-17)
*Follow-up to the 2026-08-16 "QR-code onboarding, apprentices first" decision and the 2026-08-14 duplicate-account-risk entry further down this file. Royce named the actual 9 people (Field roster screenshot, Apprentice filter, minus 2 shown) rather than the full 44-unlinked backlog.*

- [x] **All 9 named apprentices verified individually against both jvkn and ehow before send.** Aiden Crowley and Jessica Robinson are the only two genuinely new identities (no existing Shell login, no Field link). The other 7 (Dylan Lieu, Elliot Gross, Marcus Fuente, Phoenix Khatri, Tara Demamiel, Taya Moody, Terry Su) already have a linked identity end-to-end but have never logged in — safe to send (the existing-user branch signs them in, doesn't duplicate) but doesn't move the 44-unlinked backlog number; only Aiden + Jessica do.
- [x] **`shell-join-tenant.ts` read in full** — confirmed real adopt-before-create phone matching (handles +61/04/bare-9-digit formats, the same class of bug that created the Brett Kilpatrick duplicate on 2026-07-08) and that Field access stays locked behind a licence-presence trigger even for a true self-join — Core access ≠ Field access.
- [x] **Baseline join count recorded** — the Apprentice self-join code sat at 1 prior join before today; should read 10 once all 9 scan. Simple before/after check, no tooling needed.
- [x] **Reconfirmed (Royce's call, unchanged):** the 4 legacy self-join codes with no expiry/no approval (employee/manager/supervisor/apprentice, predating the 2026-08-14 hardening) stay live as-is.

**Deferred:**
- [ ] **Live click-through still not observed** — same caveat as the 2026-08-14 entry further down this file, now scoped to this specific batch. Resolves once Royce sends the link and the first person scans. _(added 2026-08-17)_
- [ ] **Max-uses cap on self-join codes — scoped, not built, Royce's call to hold.** Would need a `max_uses` column (mirrors `expires_at`'s existing shape), an atomic check-and-reject in `shell-join-tenant.ts`, and a field on the Join Links admin page. Estimated under an hour for a working version. Revisit if a link ever actually leaks past its intended recipients, or this becomes a recurring worry. _(added 2026-08-17)_

---

## SKS: self-join link duplicate-account risk checked before a mass send to apprentices (2026-08-14)

- [ ] **Not live-tested today** — this was code-level assurance (plus an old "confirmed live" comment already in the code from an earlier check), not a fresh click-through with a real pre-existing Cards account before the mass send goes out. _(added 2026-08-14)_

---

## ⏩ Session close — 2026-07-02 (strategy + migration recon) — SKS Labour→canonical feasibility (READ-ONLY, no code)

*Advisory session (TRAiDMIN meeting prep + EQ progress read) plus a read-only feasibility recon of the SKS NSW Labour → EQ canonical migration. Nothing written to any DB. Full narrative in `sessions/2026-07-02.md` (search "migration recon").*

**Completed (read-only):**

**Decided (Royce):**
- Focus = **EQ Cards for all of SKS NSW** + **EQ Core/Shell as the daily driver.**
- Migration approach = **shadow/parallel-run**: mirror sks-labour into canonical, reconcile until it matches, cut over crew-by-crew; SKS NSW Labour stays warm as the rollback until the last user is happily migrated.
- Sequence: prove at SKS scale → migrate → grow NSW branch to 200+ → *then* market.
- TRAiDMIN (Sally) meeting: attend to **learn**, abundance out loud, hold the crown jewels (the "why the systems fail" synthesis + canonical/data model), soft referral handshake only — treat as relationship, not a commercial term.

**Deferred (added 2026-07-02):**
- [ ] **Migration runbook** — load order (staff+sites → teams → team_members → schedule_entries → timesheets → leave/locks), crosswalk-completion checklist, the two unpivot specs, two-gate reconciliation. Offered, not built. _(added 2026-07-02)_
- [ ] **Complete the identity crosswalk** — 25 unlinked people + 11 unlinked sites + 9/6/6 unmatched names need a human who knows these people; pay-critical, no automation. _(added 2026-07-02, needs your call)_
- [ ] **Build the canonical reconciliation gate** — name-resolution report (0 red before load) + pay reconciliation (hours/person/week source-vs-canonical identical through one full pay cycle). The `migration_baseline`/`eq_migration_counts` machinery already exists to hang this on. _(added 2026-07-02)_
- [ ] **Verify SKS `tenant_id` live** (`7dee117c-98bd-4d39-af8c-2c81d02a1e85` per suite-state) before any load — must be stamped explicitly on every row (JWT default won't resolve on a service-role insert). _(added 2026-07-02)_
- [ ] **Agenda for tomorrow's meeting with the 7 Claude-using guys** — decide champions vs builders vs testers, guardrails before keys. Offered, not built. _(added 2026-07-02, needs your call)_
- [ ] **Name the EQ↔SKS data-ownership arrangement** before Cards runs all of SKS NSW — whose worker data, under what arrangement, what happens if Royce leaves. Cross-entity governance landmine; name it while it's friendly. _(added 2026-07-02, needs your call)_

**Notes (load-bearing):**
- **Migration tooling is already scaffolded** — `scripts/migrate-tenants.mjs`, `app_data.migration_baseline` (expected = legacy source count, diffed against landed `eq_migration_counts`, read by an admin reconciliation view). The migration is a thing to *run and watch*, not invent.
- **`people.canonical_id` (48/73) and `sites.canonical_id` (24/35) are the intended crosswalk anchors** — match/upsert against the already-populated canonical `staff` (84) / `sites` (272), do NOT blind-insert duplicates. Sites are Shell-owned canonical — write path goes through Shell.
- **Source references workers by TEXT NAME, not id**, in `timesheets.name` / `schedule.name` / `leave_requests.requester_name` — the single biggest data-quality risk, on pay data. Only `leave_balances.person_id` + `team_members.person_id` carry a real integer id.
- **Scope boundary:** sks-labour also holds a full SKS Quotes suite (`sks_quotes_*`, 518 customers, 13,929 contact_links), `tenders` (422), `nominations`, `pending_schedule` — NONE of that migrates into canonical (Quotes retired→Ops; tenders = SKS pipeline). Migrate only the labour/roster subset.
---

