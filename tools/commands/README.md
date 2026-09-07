---
title: Claude Code Command Backups — Index
owner: Royce Milmlow
last_updated: 2026-09-07
scope: Explains why brief/close/housekeep are mirrored here and decide/deploy-topology-verify/entity-boundary-guard/gap/reflect/tidy aren't
read_priority: reference
status: live
---

# Claude Code custom commands — durability backup

These are copies of Royce's user-level Claude Code slash commands, normally
kept at `~/.claude/commands/` (currently `C:\Users\EQ\.claude\commands\` on
his Windows machine). Added 2026-09-06 after a PC migration, when checking
which custom commands survived surfaced that these three have no backup
anywhere except that one machine's user profile.

**This is a backup, not a synced mirror.** Editing the live file at
`~/.claude/commands/<name>.md` does **not** update the copy here, and vice
versa. If one of these commands changes, re-copy it into this folder in the
same session (or note the drift) — otherwise this backup silently goes stale,
which is exactly the failure mode the rest of this repo works hard to avoid
(see `system/failures.md`).

## Why only these four

Claude Code auto-discovers commands from `~/.claude/commands/*.md`. Nine exist
today: `brief`, `close`, `decide`, `deploy-topology-verify`, `entity-boundary-guard`,
`gap`, `housekeep`, `reflect`, `tidy`.

Six of them (`decide.md`, `deploy-topology-verify.md`, `entity-boundary-guard.md`,
`gap.md`, `reflect.md`, `tidy.md`) are already safe without being copied here — each
is a short trigger whose real logic lives in a tracked rule file:

| Command | Backed by |
|---|---|
| `/decide` | `rules/decision-protocol.md` |
| `/deploy-topology-verify` | `rules/deploy-topology-protocol.md` |
| `/entity-boundary-guard` | `rules/entity-boundary-protocol.md` |
| `/gap` | `rules/gap-protocol.md` |
| `/reflect` | `rules/reflection-protocol.md` |
| `/tidy` | `rules/tidy-protocol.md` |

The three copied into this folder (`brief.md`, `close.md`, `housekeep.md`)
have no such split — the entire protocol, including incident-specific detail
(exact git commands, path-escaping gotchas, the session-close HTML card
template), lives only in the command file itself. `CLAUDE.md` §10 documents
a 5-bullet summary of `/close`, not the full 8-step version that's actually
in use — this folder is the only full copy outside the local machine.

## Restoring onto a new machine

Copy these three files into `~/.claude/commands/` on the new machine
(`decide.md`, `gap.md`, `reflect.md`, `tidy.md` are short enough to recreate from
scratch by hand from the table above, or copy them from the working machine
the same way if convenient).
