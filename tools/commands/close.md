---
title: "/close command backup — Session End Protocol"
owner: Royce Milmlow
last_updated: 2026-09-08
scope: Durability backup of Royce's user-level Claude Code /close command — source of truth is ~/.claude/commands/close.md, not this file
read_priority: reference
status: live
description: Session-end housekeeping. Updates pending.md, writes session log, pushes substrate. Usage: /close
---

# /close — Session End Protocol (CLAUDE.md §10)

Run every step IN ORDER. Do not skip. This is the last thing that happens in a session.

---

## Step 0 — Isolate first

Never write directly into the shared `C:\Projects\eq-context` root — Steps 2–5 below all
land in a dedicated worktree instead. This closes failure F16 (`system/failures.md`): before
it, every session wrote pending.md/session-log/changelog straight into the bare root, which
is exactly how a ~33-file uncommitted pile and three orphaned worktrees accumulated there.

**Already isolated for this close** (you ran `EnterWorktree` or `git worktree add` earlier
this session, for this repo)? Skip straight to Step 1 — don't create a second one.

**Otherwise, create a scratch worktree off fresh `origin/main`:**
```
git -C C:/Projects/eq-context fetch origin main --quiet
git -C C:/Projects/eq-context worktree add C:/Projects/eq-context-wt-close-<SESSION_ID> -b claude/close-<SESSION_ID> origin/main
```
`<SESSION_ID>` = this session's id (the GUID directory in the scratchpad path — same value
Step 6 already uses for the brief flag) — keeps concurrent sessions' close-worktrees from
colliding on a name. Every path in Steps 2–4 below is `<WORKTREE>\...`, where `<WORKTREE>` =
`C:\Projects\eq-context-wt-close-<SESSION_ID>`.

`EnterWorktree` (harness-native — one call, automatic cwd-switch and exit-time cleanup) works
too and is simpler, **provided this session hasn't already isolated into a worktree for
something else** — that's its own constraint, it refuses to create a second one.

**Already mid-task in a worktree for a DIFFERENT repo's feature work, now closing out
eq-context too?** Verified live 2026-09-08: the harness independently blocks a plain `git -C
<other-repo>` redirect from inside an isolated worktree session ("a worktree-isolated
session's git operations must target its own worktree") — so the manual form above may not
be a working escape hatch either, not just `EnterWorktree`. Not fully resolved this pass —
if you hit this, `ExitWorktree` (`action: "keep"`, preserving the other repo's in-progress
work) back to the session's original directory first, then run Step 0 from there normally.

---

## Step 1 — Inventory what happened

Scan this session's conversation for:
- Tasks completed (any Edit/Write/migration that landed)
- Decisions made (anything Royce confirmed)
- Deferred items (things flagged but not built)
- New information (schema facts, product decisions, constraints)

Hold this list mentally — it drives steps 2–4.

---

## Step 2 — Update the active tier's pending.md

Determine the active tier from the session context. All paths are inside `<WORKTREE>` from
Step 0 — never the bare `C:\Projects\eq-context` root:
- EQ work → `<WORKTREE>\eq\pending\<repo>.md` (e.g. `eq-shell.md`, `eq-field.md`,
  `eq-cards.md`) — **not** `eq\pending.md`. That file was split into one file per repo on
  2026-08-17 and is now just a 28-line index pointing here; at least 6 sessions on
  2026-08-25 alone hit the stale instruction, read the index, and self-corrected. If the
  repo doesn't cleanly match one of the listed files, use `eq\pending\cross-repo.md`.
- SKS work → `<WORKTREE>\sks\pending.md` (not split — still one file)
- OPS work → `<WORKTREE>\ops\pending.md` (not split — still one file)
- If cross-tier, update both.

Read the file. Then:
- Tick (`[x]`) any items completed this session (match by content, not line number)
- Add new deferred items with today's date: `- [ ] <item> _(added YYYY-MM-DD)_`

**Then apply the archive rule** (also stated inline in pending.md — the two must never
diverge again; this contradicted an older "leave ticked items for history" instruction
until 2026-07-27, which is why the file grew to 478 open / 163 unrotated done before
anyone noticed):
- For every section YOU touched this session (don't sweep the whole file — that's a
  separate housekeeping pass, not a per-close step): if it now has **zero open items
  left**, move it wholesale (header + full write-up) to the matching `pending-archive.md`
  for that tier. If it still has **any open item(s)**, trim it down to just the header
  and the remaining `- [ ]` line(s) — drop the italic intro paragraph and every `[x]`
  line; that narrative already lives in the changelog and session log from Steps 3–4,
  it does not need a second home in the live doc.
- Do NOT touch sections you didn't work on this session, and never delete anything —
  archive/trim only moves or drops content that's provably preserved elsewhere
  (changelog + session log). If a section mixes checklist items with free-standing prose
  that isn't part of any bullet (e.g. a standing rule note, a warning block), leave that
  section alone and flag it in the session log instead of guessing at how to trim it.

Write the updated file.

> Brief-gate note: substrate docs (`pending.md`, `sessions/`, `changelog/`) and
> `~/.claude/**` are EXEMPT from the brief-gate (scoped in `guard.js` 2026-06-30), so
> Steps 2–4 write freely without a flag — no more touch-the-flag dance. If you ever
> do hit a block here, the gate over-matched: fix the exemption in `guard.js`, don't
> work around it with `touch`.

---

## Step 3 — Write the session log

Write to `<WORKTREE>\sessions\YYYY-MM-DD.md` where YYYY-MM-DD = today.

If a file for today already exists, append a `---` divider and add below it. Since
`<WORKTREE>` was branched from **fresh** `origin/main` in Step 0, what you see here is
exactly what's already landed — never a mix of landed and another session's still-uncommitted
entries the way reading the bare root's working tree could show.

Format:

```markdown
# Session YYYY-MM-DD — <one-line title of the session's main outcome>

## Built
- <what was actually built/changed, one line per item>

## Decided
- <decisions confirmed by Royce, one line each>

## Deferred
- <items flagged but not built, with reason>

## Notes
<anything that would otherwise be lost — constraints discovered, substrate corrections, gotchas>
```

Keep it tight. Future sessions read this to avoid re-deriving context.

---

## Step 4 — Update changelogs (conditional)

Only run this step if a product file changed this session (eq-shell, eq-service, eq-field, eq-cards, etc.).

Update the relevant changelog at `<WORKTREE>\eq\changelog\<product>.md` (create if missing):

```markdown
## YYYY-MM-DD
- <what changed, one line>
```

---

## Step 5 — Commit and push to GitHub

Land ONLY the files this session actually changed, via `scripts/safe_commit.py` — **never**
a raw `git add`/`commit`/`push` directly against this shared checkout. That raw sequence is
the anti-pattern that produced failure F16 (`system/failures.md`): a bare `git commit -m
"..."` with no `--` pathspec here is exactly what `hooks/pre_tool_use.py`'s own F9(a) guard
blocks, forcing every session to improvise a fix under time pressure at the very end of a
session — and when that final step is skipped, fails, or the session ends before it runs,
the work is left stranded uncommitted in this shared root or in an orphaned worktree (found
live 2026-09-08: a 100+-commit-behind root carrying a ~33-file pile, three abandoned
worktrees in three different naming conventions, two of them holding real unpushed commits).

`safe_commit.py` fetches fresh `origin/main`, commits your named files in a throwaway
scratch worktree, and pushes with fetch+rebase retry on a race — the whole point of this
step, done safely, in one call. Run it FROM `<WORKTREE>` (Step 0) so its relative file
arguments resolve there, not against the bare root:

```
cd C:/Projects/eq-context-wt-close-<SESSION_ID> && python C:/Projects/eq-context/scripts/safe_commit.py -m "chore: session close YYYY-MM-DD [skip ci]" eq/pending/<repo>.md eq/changelog/<product>.md sessions/YYYY-MM-DD.md
```
(scope the session log to **today's file** — not the whole `sessions\` dir, a concurrent
agent may have its own file there — and add `sks/pending.md` / `ops/pending.md` too ONLY if
you changed them; INCLUDE any changelog from Step 4, the file most often forgotten)

**Use forward slashes in the invocation path exactly as shown** — a backslash-separated path
run through the Bash tool (Git Bash/POSIX sh) silently corrupts, since bash treats `\` as its
escape character (confirmed live, recurring 2026-08-16 through 2026-08-31 — see the identical
note in `brief.md` Step 3). List exactly the files this session touched, never a whole
directory or a glob — `safe_commit.py` stages precisely the paths you name, so there's no
`git add -A` equivalent to reach for even under pressure.

On success it prints `Live on origin/main: <sha>` — confirm that line before continuing. On
a repeated non-fast-forward race (rare: `origin/main` moving faster than its 5 built-in
retries) it leaves the commit safe on a local branch inside the scratch worktree it names,
with the exact push command to finish by hand once things settle — read its own output
rather than improvising.

**F16 closed in full by this version of the step**: Steps 2–4 now write into `<WORKTREE>`
from Step 0, never the bare root — so `hooks/pre_tool_use.py`'s F16 guard (blocks Edit/Write
in the bare root, `EnterWorktree` as the escape valve) runs active by default with nothing
in this protocol left for it to conflict with. See `system/failures.md` -> F16.

---

## Step 5.5 — Clean up the worktree

Now that the push succeeded, remove the scratch worktree from Step 0 — leaving it behind is
exactly how F16's three orphans accumulated in the first place:
```
git -C C:/Projects/eq-context worktree remove C:/Projects/eq-context-wt-close-<SESSION_ID> --force
git -C C:/Projects/eq-context branch -D claude/close-<SESSION_ID>
```
Entered via `EnterWorktree` instead? `ExitWorktree` with `action: "remove"` does the same
thing in one call.

---

## Step 6 — Clear the brief flag (LAST — only after the push succeeds)

Now that substrate is committed + pushed, delete THIS SESSION'S flag so it doesn't carry over:
```
Remove-Item "C:\Users\EQ\AppData\Local\Temp\eq-brief-<TODAY>-<SESSION_ID>.flag" -ErrorAction SilentlyContinue
```
(bash: `rm -f "/c/Users/EQ/AppData/Local/Temp/eq-brief-$(date +%Y-%m-%d)-<SESSION_ID>.flag"`)

`<SESSION_ID>` is this session's id (the GUID directory in the scratchpad path). **Never wildcard
this** — `eq-brief-<TODAY>-*.flag` would delete other concurrent sessions' flags and re-block them
mid-work, which is the bug this per-session naming exists to prevent.

Doing this BEFORE the writes (the old ordering) is what blocked Steps 2–4 on repeat closes.

---

## Step 7 — Render the session card (plain English)

End the session on a card Royce can scan in two seconds, not a wall of text. Build it from the Step 1 inventory and render it with `mcp__visualize__show_widget`.

**Plain English is the rule — no jargon on the card.** Translate every technical item into what it means for Royce. Cut migration numbers, PR numbers, table/schema names, "canonical", branch names, version tags. Say what changed and why it matters. (The technical detail already lives in the session log from Step 3 — the log is for the next Claude, the card is for Royce.)

Examples of the translation:
- "Migration 0159 stuck on ehow + zaap (checksum drift)" → "A database update is stuck on two systems — until it lands, Field can't auto-fill the customer on prestart forms."
- "eq-cards PR #127 open" → "An onboarding fix is waiting for your review."
- "Subcontractor role added to eq-roles v2.4.0" → "Added a 'subcontractor' role you can assign to people across the apps."

Fill the card from the inventory:
- **Needs you** — anything needing Royce's decision or action. If there's nothing, show one row: "All clear — nothing waiting on you."
- **Done this session** — what was built or landed.
- **Next** — deferred items and obvious follow-ups. Omit this section only if empty.

Top metrics: **Done** = count built · **Deferred** = new deferred count · **Needs you** = items needing Royce's call.

Call `show_widget` with `title: "eq_session_close_card"`, `favicon` unused, and this HTML. Set the date, the tier badge (EQ / SKS / OPS), the three numbers, and one row per item. Repeat or delete rows as needed. Keep every line plain English.

```html
<h2 class="sr-only">Session close for ‹DATE›: ‹N› done, ‹M› deferred, ‹K› need you.</h2>
<style>
.sc-sec { font-size: 13px; font-weight: 500; color: var(--text-muted); margin: 0 0 8px; }
.sc-row { display: flex; align-items: flex-start; gap: 10px; padding: 10px 12px; border-radius: var(--radius); margin-bottom: 6px; }
.sc-row i { font-size: 18px; line-height: 1.4; flex-shrink: 0; }
.sc-row p { margin: 0; font-size: 14px; line-height: 1.45; color: var(--text-primary); }
.sc-row .sub { color: var(--text-secondary); font-size: 13px; }
</style>
<div style="padding: 0.5rem 0;">
  <div style="display: flex; align-items: baseline; justify-content: space-between; gap: 12px; margin-bottom: 4px;">
    <div style="display: flex; align-items: baseline; gap: 10px;">
      <span style="font-size: 18px; font-weight: 500; color: var(--text-primary);">Session close</span>
      <span style="font-size: 14px; color: var(--text-muted);">‹DATE›</span>
    </div>
    <span style="font-size: 12px; font-weight: 500; padding: 3px 10px; border-radius: 20px; background: var(--bg-accent); color: var(--text-accent);">‹EQ›</span>
  </div>
  <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin: 1rem 0 1.5rem;">
    <div style="background: var(--surface-1); border-radius: var(--radius); padding: 0.85rem 1rem;">
      <div style="font-size: 13px; color: var(--text-muted); margin-bottom: 4px;">Done</div>
      <div style="font-size: 24px; font-weight: 500; color: var(--text-primary);">‹N›</div>
    </div>
    <div style="background: var(--surface-1); border-radius: var(--radius); padding: 0.85rem 1rem;">
      <div style="font-size: 13px; color: var(--text-muted); margin-bottom: 4px;">Deferred</div>
      <div style="font-size: 24px; font-weight: 500; color: var(--text-primary);">‹M›</div>
    </div>
    <div style="background: var(--surface-1); border-radius: var(--radius); padding: 0.85rem 1rem;">
      <div style="font-size: 13px; color: var(--text-muted); margin-bottom: 4px;">Needs you</div>
      <div style="font-size: 24px; font-weight: 500; color: var(--text-warning);">‹K›</div>
    </div>
  </div>
  <p class="sc-sec">Needs you</p>
  <div class="sc-row" style="background: var(--bg-warning);">
    <i class="ti ti-alert-triangle" style="color: var(--text-warning);" aria-hidden="true"></i>
    <p>‹plain-English headline› <span class="sub">— ‹why it matters, plain English›</span></p>
  </div>
  <p class="sc-sec" style="margin-top: 1.25rem;">Done this session</p>
  <div class="sc-row" style="background: var(--surface-1); padding: 8px 12px;">
    <i class="ti ti-check" style="color: var(--text-success);" aria-hidden="true"></i>
    <p>‹what was done› <span class="sub">— ‹plain detail›</span></p>
  </div>
  <p class="sc-sec" style="margin-top: 1.25rem;">Next</p>
  <div class="sc-row" style="background: var(--surface-1); padding: 8px 12px;">
    <i class="ti ti-arrow-right" style="color: var(--text-primary);" aria-hidden="true"></i>
    <p>‹next step› <span class="sub">— ‹why›</span></p>
  </div>
</div>
```

Row swaps: for a "waiting for your review" item use `ti-eye` with `color: var(--text-accent)`; for the all-clear row use `ti-check` with `color: var(--text-success)`. If **Needs you** is 0, set the metric colour to `var(--text-primary)` and show only the all-clear row.

---

## Step 8 — Final confirmation

The card already shows the summary — do NOT restate its contents as text. Print only these two lines below it:

```
Session closed. Pushed to substrate.
Log: sessions/YYYY-MM-DD.md
```

Nothing else. The session is done.
