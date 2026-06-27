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

## Open PRs entering next session
- **eq-shell PR #487** (`fix(staff): licence image scroll + archive 500 on patch`) — OPEN. Review + merge.
- **eq-field PR #348** (`feat(canon-read): server-side proxy for jvkn worker PII reads`) — OPEN. Review separately.
- **eq-solves-service PR #345** (`draft(identity): Phase 3 re-key + reference migration`) — DRAFT. Review-only.
