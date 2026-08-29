---
title: eq-field worktree cleanup — follow-up sprint
date: 2026-08-28
owner: Royce Milmlow
scope: the 3 "needs you" items left after the 2026-08-28 eq-field worktree audit (19 of 24 worktrees cleaned up; full audit trail in eq-context/system/worktree-registry.md's "round 2" entry and its Active table)
---

# eq-field worktree cleanup — follow-up sprint (2026-08-28)

No goal is set in `TODAY.md` — this doesn't claim strategic priority, just a bounded 2-item cleanup with a clear finish line: each one either gets removed or gets an explicit "leave it" reason.

**Re-verified live immediately before writing this** (this repo moves fast — 2 of the original 3 flagged items had already changed underneath the session-close card that prompted this sprint, within minutes):

---

## Moved on since the summary — nothing to action

- **`eq-field/.claude/worktrees/documents-to-sign-feature-3035a3`** — no longer the detached-HEAD/unpushed-commit concern the original audit flagged. Another session has since claimed this folder for unrelated work on branch `claude/apprentices-tab-security-603749`. Dropped from this sprint; whoever is on that branch owns it now.

---

## Needs your call

- [ ] **`eq-field-apprentice-scope-race-wt`** — checked out on `main` itself, 87 commits behind `origin/main`, 0 ahead. Confirmed unchanged since the original audit. Objectively nothing would be lost removing it (no unique commits), but it isn't a feature branch with a PR to verify against, so it's a decision, not an assumption. **Recommended: remove it.**
- [ ] **`C:\Users\EQ\AppData\Local\Temp\ci-repro`** — outside `C:\Projects` entirely, detached HEAD, 2-week-stale commit (v3.5.491), working tree already shows ~280 files deleted from disk (not staged — genuinely gone). Confirmed unchanged since the original audit. Reads as a spent CI-repro checkout, but this session doesn't own that lifecycle. **Recommended: remove it, unless it's wired into an active CI/repro workflow.**

Both asked directly in-session; this row updates to Shipped the moment either lands.

---

## Watching — other sessions' active work, no action needed

- **`site-contact-mapping-fix`** / [PR #821](https://github.com/eq-solutions/eq-field/pull/821) — still open, branch has moved (new commit since the audit). Someone's actively finishing "site contact info silently dead since v3.5.551."
- **`supervisor-list-population-9e6715`** — now on branch `claude/roster-project-code-picker` (was `claude/multi-project-site-display-1483e9` / PR #822 at audit time). Still active, still reads as live work closing the `site_projects`-not-wired-to-Field gap already on record.

Neither needs a decision — just don't clean up their worktrees out from under them.

---

*Compiled from the 2026-08-28 eq-field worktree audit (see `system/worktree-registry.md`), re-verified live against `git worktree list --porcelain` immediately before writing. If something above looks wrong, the live system wins, not this file.*
