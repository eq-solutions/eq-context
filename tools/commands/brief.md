---
title: "/brief command backup — Session Gate (Rule 0.6)"
owner: Royce Milmlow
last_updated: 2026-09-08
scope: Durability backup of Royce's user-level Claude Code /brief command — source of truth is ~/.claude/commands/brief.md, not this file
read_priority: reference
status: live
description: Run the Rule 0.6 session gate and produce a structured task brief. Usage: /brief <repo-name>
---

# /brief — Session Gate (Rule 0.6)

**Trigger:** `/brief <repo>` where `<repo>` is the target repo name (e.g. `eq-shell`, `eq-solves-service`, `eq-field`).

When this skill is invoked, run the following steps IN ORDER. Do not skip any step. Do not start building until Royce confirms the brief.

---

## Step 1 — Read the health digest

Read `C:\Projects\eq-context\digest.md`.

**Check its currency before trusting it — a fresh-looking stamp is not the same as
current content (this is failure F1: the substrate has served stale content with no
error before).** Run `git -C C:/Projects/eq-context log HEAD..origin/main --oneline -- digest.md`.
If that returns anything, say so plainly in the brief's Health section ("digest.md is
N commits behind origin/main as of this read — treat below as a lower bound, not
current truth") instead of presenting its contents as unconditionally current. One
extra git call — it's what would have caught a stale brief going out unflagged on
2026-09-07.

Extract and display:
- **Needs you** section — if non-empty, list each item with its emoji prefix
- **Pulse** section — CI status per repo, any stale worktrees, aging PRs
- **Live errors (Sentry)** — if present, list the top errors

If digest.md is missing or unreadable, state that explicitly and continue.

---

## Step 2 — Check worktree registry

Run `git -C C:/Projects/$ARGUMENTS worktree list` — this is the authoritative, live
source. **Do not rely on `system/worktree-registry.md` for current state** (per root
`CLAUDE.md`'s own "Active locked worktrees" line) — as of 2026-09-07 it's also grown to
368.5KB / 647 lines, past what a normal file-read can load in one call, so treating it
as this step's primary mechanism silently fails rather than just being stale. Read it
only for historical narrative the live command won't show (why a worktree exists, who
owns it).

List any active worktrees for the target repo (`$ARGUMENTS`). If one exists, surface it — working from a second worktree on the same repo creates conflicts.

**If `$ARGUMENTS` is `eq-context` itself:** isolate before writing anything — `EnterWorktree`
(one call, no clone/setup), and land any substrate change via `python
C:/Projects/eq-context/scripts/safe_commit.py -m "..." <files>`, never a raw commit/push
against this shared checkout. See `system/failures.md` -> F16 and the SessionStart gate's own
ISOLATE line, which repeats this on every session regardless of target repo.

---

## Step 3 — Git state on the target repo

Run these commands on `C:/Projects/$ARGUMENTS`:

```
git -C C:/Projects/$ARGUMENTS fetch origin main --quiet
git -C C:/Projects/$ARGUMENTS branch -a
git -C C:/Projects/$ARGUMENTS status
git -C C:/Projects/$ARGUMENTS log --oneline -5
git -C C:/Projects/$ARGUMENTS log HEAD..origin/main --oneline
```

**Use forward slashes exactly as shown, even though `$ARGUMENTS` substitutes to a plain repo name.** If these commands run through the Bash tool (Git Bash/POSIX sh), a backslash-separated path like `C:\Projects\eq-field` gets silently corrupted — bash treats `\` as its escape character, so `\P` and `\e` collapse to `P`/`e`, turning the path into `C:Projectseq-field` with no error until git fails with a confusing "No such file or directory". Confirmed recurring across multiple live sessions 2026-08-16 through 2026-08-31. Forward slashes sidestep this entirely and work identically in PowerShell.

Extract:
- Current branch
- Uncommitted changes (list files)
- Recent commits (last 5, one line each)
- Remote branches that look relevant (open feature branches)
- **Staleness** — the `HEAD..origin/main` output. If non-empty, the branch is missing real history from `main`. Skim the commit titles for anything touching the same files or feature area as today's task — if something looks related, read it (`git show <sha> --stat`) before writing new code. This is what would have caught the 2026-07-28 duplicate-work incident (a stale `eq-solves-service` branch shipped a fix already merged days earlier via #589/#590) before any work was done on it, instead of discovering it mid-session.

---

## Step 3.5 — Untracked migration check (eq-field only)

**Only run this step if `$ARGUMENTS` is `eq-field`.** Skip entirely for every other repo (eq-shell, eq-solves-service, eq-cards, eq-context, etc.) — this step must not fire outside eq-field.

eq-field hand-applies Supabase migrations via the Supabase MCP — there is no CI path that applies `supabase/migrations/*.sql` (no workflow in `.github/workflows/` touches that directory). This has twice left an applied migration sitting uncommitted in the shared checkout for an extended period — once for a full day, only found by chance ([eq-field PR #764](https://github.com/eq-solutions/eq-field/pull/764); one file's own "DRAFT — NOT APPLIED" header comment was still there a full day after it had actually gone live). Buried inside Step 3's generic "Uncommitted: `<files>`" line, that fact doesn't register as urgent. This step gives it a specific, named callout instead.

1. Run:
   ```
   git -C C:/Projects/eq-field status --porcelain --untracked-files=all -- supabase/migrations
   ```
   Keep lines starting `?? ` and ending `.sql` — these are the untracked migration files.

2. None found → state "No untracked migrations" in Step 5's output and move on to Step 4.

3. For each untracked file, classify it against the live ledger:
   - Read the file. Derive its **short name**: strip the leading date prefix (`YYYYMMDD` or the full `YYYYMMDDHHMMSS`, optionally followed by a single letter, then `_`) and the `.sql` extension.
   - Pick which tenant DB to check. Default to **ehow** (`ehowgjardagevnrluult`, the live SKS tenant) first — that's where the real incident happened and where a missed migration matters most. Also check **zaap** (`zaapmfdkgedqupfjtchl`, the eq sandbox tenant) if the filename/content points at the `eq` tenant, or if ehow shows no match.
   - Call the Supabase MCP `list_migrations` tool for the relevant project ID(s).
   - Match carefully — the ledger's `name` field does **not** always equal the file's short name. Verified live 2026-08-24 against ehow's own ledger, all three shapes occur: usually it's the short name (`ehow_second_wave_jwt_tenant_gate`); sometimes it's the full filename stem with the date still attached (`20260819_timesheets_leave_actor_identity_fix`); sometimes it's a near-miss, e.g. an applied `_v2` revision against a file that has no `_v2` in its own name. Check both the short name and the full stem for a match, exact or clear substring.

4. Classify each file:
   - **APPLIED-BUT-UNCOMMITTED** — a clear ledger match on a checked project. This is the failure mode that already happened twice — call it out as urgent, name the file and the matching ledger entry (`version` + `name`), and say it should be committed this session.
   - **DRAFT (not yet applied)** — no match on any project checked. Ordinary in-progress work — say so plainly, don't manufacture urgency.
   - **UNKNOWN** — the match is ambiguous (e.g. a near-miss name, or the MCP call failed) — say what's unclear rather than guessing either way.

This is a WARNING surface only — never a reason to block or refuse to continue. A genuinely in-progress draft migration is normal and fine. Carry the result into Step 5.

---

## Step 4 — Supabase recon (conditional)

**Only run this step** if Royce's task description mentions any of: schema, migration, database, table, RLS, function, edge function, Supabase, DB, query, data.

Query ehow (`ehowgjardagevnrluult`) via Supabase MCP:
- `list_tables` on the relevant schema (`service`, `app_data`, or `public`)
- One targeted `execute_sql` if the task implies a specific table

State what exists vs. what the task assumes — flag any divergence.

---

## Step 5 — Output the structured brief

Emit this exact format:

```
## Session Brief — <repo> — <date>

### Health
<digest Needs you items, or "All clear">

### Worktrees
<active worktrees for this repo, or "None — clear to proceed">

### Git state
Branch: <current branch>
Uncommitted: <files or "clean">
Recent commits:
- <commit>
- <commit>
...
Staleness: <"Up to date with main" or "N commits behind main — <one-line skim result>">

### Migration check (eq-field only — omit this whole section for other repos)
<"No untracked migrations", or one line per untracked file:>
⚠️ <filename> — APPLIED-BUT-UNCOMMITTED (ledger match: <project> "<name>", version <version>) — commit this now, it's already live
⚠️ <filename> — DRAFT, not yet applied (no match on <project(s) checked>)
⚠️ <filename> — UNKNOWN — <why it's ambiguous>

### DB state (if checked)
<what exists vs. what the task assumes, or "Not checked — not a DB task">

### What exists
<verified against live state above>

### What's broken / missing
<the specific gap>

### What changes
<file / function / table scope>

### Constraints
<what not to touch, auth rules, deploy rules>

---
Confirm this brief before I write anything.
```

After emitting the brief, write the flag file so the brief gate in guard.js is satisfied for this session.

The flag is **per-session, not per-day** — several agents run on this machine at once, and a
shared daily flag meant one session's `/close` re-blocked every other live session while one
session's `/brief` waived the gate for sessions that never ran one. Substitute `<SESSION_ID>`
below with this session's id: it is the GUID directory in the scratchpad path, and guard.js
echoes it in any brief-gate block message (`[session <id>]`).

```powershell
$today = Get-Date -Format 'yyyy-MM-dd'
$sid   = '<SESSION_ID>'
# ${today} braces are load-bearing: "$today.flag" parses as a property access and
# yields eq-brief-.flag, which the guard.js brief-gate never matches.
New-Item -Path "C:\Users\EQ\AppData\Local\Temp\eq-brief-${today}-${sid}.flag" -ItemType File -Force | Out-Null
```

Do not write code, edit files, or make tool calls beyond the reads above until Royce replies to confirm the brief.

---

## Defaults when no repo is given

If no repo is given, ask:

> Which repo is this session targeting?
> 1. eq-shell (core.eq.solutions)
> 2. eq-solves-service (EQ Service)
> 3. eq-field (field.eq.solutions)
> 4. eq-cards
> 5. eq-context (substrate only)
> 6. Other — type the repo name

Then proceed with the chosen repo.
