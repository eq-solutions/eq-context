---
title: EQ Field — Changelog
owner: Royce Milmlow
last_updated: 2026-08-21
scope: UNRECONCILED PAIR with eq/changelog/eq-field.md, the repo-slug-convention canonical file. This file was archived 2026-08-17 as a dead twin (superseded_by: eq-field.md — see archive/changelog-field-dead-twin.md), then recreated from scratch 2026-08-19 by a session that didn't check it had been retired. It has since collected 5 real entries (PR #729/#730/#735/#736/#738, 2026-08-19/20) that exist nowhere in eq-field.md. Not marked superseded_by because that would falsely claim eq-field.md already holds this content — it doesn't yet. Which record survives is Royce's call, same posture as the 2026-08-17 merge; until then both files stay flagged rather than silently diverging again (third time this pair has drifted — see archive/changelog-eq-field-dead-twin.md and archive/changelog-field-dead-twin.md for the first two).
read_priority: reference
status: live
---

# EQ Field Changelog

> **UNRECONCILED PAIR** — this file was archived 2026-08-17, then recreated
> 2026-08-19 and has since collected entries not present in
> `eq/changelog/eq-field.md` (the canonical, repo-slug-named file — read that
> one first). See frontmatter `scope` for detail.

## 2026-08-20
- v3.5.529 (PR #738): non-manager workers could see every other worker's hours on Timesheets, not just their own — `_getTsFilteredPeople()` had no identity scoping at all, only editing was ever gated. Now filters non-managers to their own row (agency logins exempted). Also fixed mobile Timesheets card rows rendering ~2x oversized — a bare `.empty` class collided with an unrelated generic empty-state placeholder rule.

## 2026-08-19
- v3.5.528 (PR #735): Documents to Sign pilot widened to a second real signer, after eq-shell's onboarding auto-push fired 12 real document sign-offs at an existing SKS electrician (a start_date correction misread as a new-starter event) with no screen anywhere for him to act on them.
- v3.5.527 (PR #736): fixed the apprentice list showing every apprentice instead of just the caller's own card — root cause was a boot-order race (lazy-loaded apprentices.js meant the boot-time data fetch silently never ran on a direct deep-link visit), not the scoping logic itself. Also: Timesheets nav hidden from apprentice/employee/labour_hire on desktop (mobile already had this), Prestarts/Toolboxes made visible to every role (permission matrix already granted it, nav never reflected it), Site Audits restored to manager-only.
- v3.5.526 (PR #730): Edit Roster row-action icons no longer overflow their column on Labour Hire rows; Sites page customer groups are now collapsible (large groups default collapsed, search force-expands matches).
- v3.5.525 (PR #729): Job Numbers mobile drawer item moved out of a stale "Beta" section into Manage. Digest settings (recipient list + section toggles) restricted to manager/supervisor roles — was viewable/editable by every role including apprentices. Digest recipient list collapses on mobile.
- PR #728 (applied live): RLS on prestarts/toolbox_talks/incidents/site_diaries/site_audits/site_audit_items now requires manager/supervisor role for writes — was tenant-scoped only, any authenticated user could bypass the app's own access rule via the API.
