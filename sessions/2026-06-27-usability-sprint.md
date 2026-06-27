---
title: 2026-06-27 — Usability sprint + security gate promotion
repos: eq-field, eq-context, eq-solves-service
---

## What was done

### eq-field PR #349 — MERGED `fd13677`
`fix(people): on_roster filter + toolbox logo dead path`

- `index.html`: exposed `on_roster` from `field_people` view in people filter bar; added "On Roster" checkbox
- `scripts/people.js` `renderContacts()`: applies `on_roster===true` filter when checkbox checked
- `scripts/toolbox.js:567`: fixed dead logo path — `dx.fetchLogoBase64('/images/eq-logo.png')` → `dx.fetchTenantLogo()` (pattern matches `safety.js`/`audits.js`)

### eq-context PR #43 — MERGED `100e78f`
`chore(security): promote gate from advisory to blocking`

- Removed two `continue-on-error: true` lines from `.github/workflows/security-audit.yml`
- Pre-condition: ERROR 0 confirmed across all 4 EQ projects before flip
- Gate now blocks on new ERROR-level Supabase advisories and RLS zero-row probe failures

### eq-service PR #292 — CLOSED
Stale parked docs PR (13 days aging); decisions already captured in CLAUDE.md.

### Worktree cleanup
- **eq-context:** Removed orphaned `relaxed-babbage-8b1983` and `unruffled-ellis-de2f31` (no PRs)
- **eq-field:** Removed `ts-spans` (on main, no PR) and ran `sad-black-76cc32` cleanup script (worktree already gone, script self-deleted)

### CLAUDE.md
- Added PR #349, #43, #292 closed
- Added eq-shell PR #487 and eq-field PR #348 as current open PRs
- Documented cleaned-up worktrees

## Sprint context
This was the "usability first" sprint selected to move toward Q3 goal:
> *EQ Field/Service used by NSW office for REAL operational work by 1 August 2026*

The `on_roster` filter directly addresses the Q3 test: "Is this being used at SKS?" — SKS staff list is now filterable to current roster members without wading through all historical workers.

## Decisions
- Advisory security gate → blocking: signal was clean, timing right. Gate promotes on this commit.
- Sites curation (`sites.field_enabled` — 591 all enabled): SQL-ready to identify sites with no recent jobs, but requires Royce to execute against ehow (SKS live). Deferred — Royce-gated.

### CI gate unblock — eq-shell PR #489 — OPEN `6acd3b8`
`fix(ci): allow-list eq_cards_find_invites_by_phone in drift CHECK 6`

- `eq_cards_find_invites_by_phone()` added to jvkn in eq-cards PR #99 (codeless company finder)
- Anon has EXECUTE privilege; self-guards via `auth.uid()` (returns empty for unauthenticated)
- Fix: added to `FUNC_EXEC_ANON_ALLOW['eq-canonical (control plane)']` in `check-tenant-drift.mjs:503`
- No DB change, no auth behaviour change. Safe to merge on CI green.

### Migration identity divergence — informational, not a blocker
4 migrations (0142-0145) show as "missing" in drift check because they were applied via Supabase MCP (not the tenant-migrate runner). Live query confirmed all objects exist on ehow:
- `app_data.gm_invoice_run` ✓ (0144+0145)
- `public.eq_update_staff()` ✓ (0142)
- `public.eq_create_quote()` ✓ (0143)
Backfilling `_eq_migrations` records would clear the noise but is optional; not urgent.

### Adoption gap — organizational (Royce-gated)
From live Supabase query: pm_calendar 0 rows, last defect 3 weeks ago, 5 of 56 staff with accounts.
SKS is not yet using Field/Service for daily work. Technical blockers cleared; adoption is SKS process, not code.

## Open PRs entering next session
- **eq-shell PR #489** (`fix(ci): allow-list eq_cards_find_invites_by_phone in CHECK 6`) — OPEN. Merge on CI green.
- **eq-field PR #348** (`feat(canon-read): server-side proxy for jvkn worker PII reads`) — OPEN. Review separately.
- **eq-solves-service PR #345** (`draft(identity): Phase 3 re-key + reference migration`) — DRAFT. Review-only.
- **eq-shell PRs #487 + #488** — both MERGED (licence scroll fix + intake spinner).
