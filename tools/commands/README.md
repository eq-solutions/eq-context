---
title: Claude Code Command + Hook Backups — Index
owner: Royce Milmlow
last_updated: 2026-09-15
scope: Explains why brief/close/housekeep + guard.js are mirrored here, why decide/deploy-topology-verify/entity-boundary-guard/gap/reflect/tidy/triage aren't, and how drift against the live files is now checked
read_priority: reference
status: live
---

# Claude Code custom commands + hooks — durability backup

These are copies of Royce's user-level Claude Code slash commands and one
hook, normally kept at `~/.claude/commands/` and `~/.claude/hooks/`
(currently `C:\Users\EQ\.claude\commands\` / `...\hooks\` on his Windows
machine). Added 2026-09-06 after a PC migration, when checking which custom
commands survived surfaced that these had no backup anywhere except that one
machine's user profile. `guard.js` joined 2026-09-15 (see Hooks below).

**This is a backup, not a synced mirror — copying still has to happen by
hand.** Editing a live file does **not** update its copy here, and vice
versa. What changed 2026-09-15: every Claude Code session now checks these
files for drift (`hooks/session_start.py`'s CMDSYNC step, warn-only, fires
every session) and says so loudly if they've diverged — so a stale copy no
longer goes unnoticed indefinitely. It still doesn't fix itself: when CMDSYNC
fires, re-copy the changed file's body into this folder in the same session
(keep this file's own frontmatter/meta block) — otherwise the backup stays
stale even though you've now been told. This is exactly the failure mode the
rest of this repo works hard to avoid (`system/failures.md` -> F19, the
incident that motivated CMDSYNC in the first place).

## Why only these three commands (+ one hook)

Claude Code auto-discovers commands from `~/.claude/commands/*.md`. Ten exist
today: `brief`, `close`, `decide`, `deploy-topology-verify`, `entity-boundary-guard`,
`gap`, `housekeep`, `reflect`, `tidy`, `triage` (`triage.md` was missing from
this list until 2026-09-15 — present live the whole time, just never added
here).

Seven of them (`decide.md`, `deploy-topology-verify.md`, `entity-boundary-guard.md`,
`gap.md`, `reflect.md`, `tidy.md`, `triage.md`) are already safe without being copied
here — each is a short trigger whose real logic lives in a tracked rule file:

| Command | Backed by |
|---|---|
| `/decide` | `rules/decision-protocol.md` |
| `/deploy-topology-verify` | `rules/deploy-topology-protocol.md` |
| `/entity-boundary-guard` | `rules/entity-boundary-protocol.md` |
| `/gap` | `rules/gap-protocol.md` |
| `/reflect` | `rules/reflection-protocol.md` |
| `/tidy` | `rules/tidy-protocol.md` |
| `/triage` | `rules/triage-protocol.md` |

The three copied into this folder (`brief.md`, `close.md`, `housekeep.md`)
have no such split — the entire protocol, including incident-specific detail
(exact git commands, path-escaping gotchas, the session-close HTML card
template), lives only in the command file itself. `CLAUDE.md` §10 documents
a 5-bullet summary of `/close`, not the full 8-step version that's actually
in use — this folder is the only full copy outside the local machine.

## Hooks

`guard.js` (`~/.claude/hooks/guard.js`) is the PreToolUse enforcement engine
behind brief-gate, reflection-gate, stale-main-gate, and everything else this
substrate relies on a live Claude Code session to actually stop — 42KB, no
tracked-elsewhere split the way the six commands above have. It had **no
backup anywhere** until 2026-09-15, found while investigating why
`brief.md`/`close.md`'s backups had gone stale (above) — a materially bigger
gap than the two files that prompted the check, since guard.js is the
enforcement itself, not just instructions a session reads. The copy here
carries a `// === DURABILITY BACKUP META ===` … `// === END META ===` comment
block instead of YAML frontmatter (staying valid JS); CMDSYNC strips it
before comparing, the same way it strips the commands' YAML frontmatter.

## Restoring onto a new machine

Copy `brief.md`, `close.md`, `housekeep.md` into `~/.claude/commands/` and
`guard.js` into `~/.claude/hooks/` on the new machine (`decide.md`, `gap.md`,
`reflect.md`, `tidy.md`, `triage.md` are short enough to recreate from scratch
by hand from the table above, or copy them from the working machine the same
way if convenient). Strip each file's backup-only header first — the YAML
frontmatter on the three `.md` files, the `DURABILITY BACKUP META` comment
block on `guard.js` — before dropping it into place; a stray frontmatter
block would break `guard.js` as valid JS.
