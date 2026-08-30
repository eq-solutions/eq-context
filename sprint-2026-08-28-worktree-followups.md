---
title: eq-field worktree cleanup — follow-up sprint
date: 2026-08-28
last_updated: 2026-08-30
owner: Royce Milmlow
scope: the 3 "needs you" items left after the 2026-08-28 eq-field worktree audit (19 of 24 worktrees cleaned up; full audit trail in eq-context/system/worktree-registry.md's "round 2" entry and its Active table)
read_priority: standard
status: live
---

# eq-field worktree cleanup — follow-up sprint (2026-08-28)

No goal is set in `TODAY.md` — this doesn't claim strategic priority, just a bounded 2-item cleanup with a clear finish line: each one either gets removed or gets an explicit "leave it" reason.

**Re-verified live immediately before writing this** (this repo moves fast — 2 of the original 3 flagged items had already changed underneath the session-close card that prompted this sprint, within minutes):

---

## Moved on since the summary — nothing to action

- **`eq-field/.claude/worktrees/documents-to-sign-feature-3035a3`** — no longer the detached-HEAD/unpushed-commit concern the original audit flagged. Another session has since claimed this folder for unrelated work on branch `claude/apprentices-tab-security-603749`. Dropped from this sprint; whoever is on that branch owns it now.

---

## Shipped

- [x] **`eq-field-apprentice-scope-race-wt`** — removed via `git worktree remove`. Royce's explicit go (asked directly in-session, no PR existed to verify merge status against — this was a stale `main`-only snapshot, 87 behind/0 ahead, nothing unique lost).
- [x] **`C:\Users\EQ\AppData\Local\Temp\ci-repro`** — removed via `git worktree remove --force` (its working tree was already emptied out on disk, so git flagged it as "modified/untracked" rather than clean — the force was clearing a husk, not discarding real content). Royce's explicit go, same as above.

Both closed in the same session that opened this sprint — see `system/worktree-registry.md` for the audit-trail entry.

---

## Watching — other sessions' active work, no action needed

- **`site-contact-mapping-fix`** / [PR #821](https://github.com/eq-solutions/eq-field/pull/821) — still open, branch has moved (new commit since the audit). Someone's actively finishing "site contact info silently dead since v3.5.551."
- **`supervisor-list-population-9e6715`** — now on branch `claude/roster-project-code-picker` (was `claude/multi-project-site-display-1483e9` / PR #822 at audit time). Still active, still reads as live work closing the `site_projects`-not-wired-to-Field gap already on record.

Neither needs a decision — just don't clean up their worktrees out from under them.

---

*Compiled from the 2026-08-28 eq-field worktree audit (see `system/worktree-registry.md`), re-verified live against `git worktree list --porcelain` immediately before writing. If something above looks wrong, the live system wins, not this file.*
