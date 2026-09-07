---
title: Triage Protocol
owner: Royce Milmlow
last_updated: 2026-09-07
scope: On-demand fast pass through digest.md's curated pending buckets (Needs you / Waiting on you / Aging 45d+), rendered as clickable HTML cards via mcp__visualize — one small decision per item, batched
read_priority: high
status: live
---

# Triage Protocol

**Purpose:** work through a large number of small, independent pending decisions fast, without reading a wall of markdown or holding the whole backlog in your head. Every item already sits in `digest.md`'s curated buckets — this protocol's only job is to render them as clickable cards and route each click back into a real action, batched so 268 items doesn't mean 268 lines of chat.

**Trigger phrases:** `/triage [scope]`, "help me work through the pending list", "there's a lot of pending stuff, let's triage it", "clear the backlog", "rate our pending items". Any tool that has read this file can run it from the phrases alone; `/triage` (`~/.claude/commands/triage.md`) is a Claude-Code-only convenience, not a requirement.

**Distinct from the other on-demand passes:**
- `/gap` (`rules/gap-protocol.md`) — one project, deep status reset, chat output only.
- `/decide` (`rules/decision-protocol.md`) — one decision, weighed with a six-step pass, before a choice is made.
- `/triage` — neither. Many small decisions, one click each, wide not deep. If an item turns out to need real thought, drop out of the loop and run `/decide` on it instead of forcing a button click.

---

## Scope — what this pulls, and what it deliberately doesn't

Three buckets, all already curated by `.github/scripts/refresh_digest.py` — this protocol adds no new pending-item detection, it only renders what already exists:

| Bucket | Source in `digest.md` | Typical size |
|---|---|---|
| `needs-you` | "⚠ Needs you" section | Single digits — P0/P1 security, failing crons, guard-bypass flags |
| `waiting-on-you` | "🙋 Waiting on you" section | Hundreds — confirms, click-throughs, calls only Royce can clear |
| `aging` | "Aging open items (45d+, unconfirmed)" section | Hundreds — open items gone quiet under their own dated write-up |

**Deliberately out of scope:** the raw per-repo engineering backlog (`eq/pending/<repo>.md`, `sks/pending.md`, `ops/pending.md` — roughly 1,300 items suite-wide). That's normal work queue, not a "only you can decide this" list — triaging it here would just be re-reading the backlog with extra clicks. If a specific backlog item needs a decision, reference it directly rather than routing all of pending.md through this tool.

**Never load a `pending.md` file whole.** The master `CLAUDE.md` §1 step 4 retired that pattern for a reason (491KB, ~125K tokens, 2026-08-17) — `digest.md` already gives you what's needed for the three buckets above. If a click-through needs more context than `digest.md`'s one-line summary, read only the linked file's specific section (grep for the item's own text or dated header), never the whole file.

**`digest.md` itself is machine-generated — never hand-edit it.** It's regenerated deterministically by `refresh_digest.py` on merge and nightly; a hand edit gets silently overwritten. Every action below writes to the *source* file `digest.md` links to (`ops/security-register.md`, `system/failures.md`, the relevant `eq/pending/<repo>.md`, `sks/pending.md`, `ops/pending.md`), never to `digest.md` itself.

**Check `digest.md`'s own currency before trusting its counts.** Same freshness gate `/brief` runs: `git -C C:/Projects/eq-context log HEAD..origin/main --oneline -- digest.md`. If that returns anything, say so before quoting a bucket size as current — treat it as a lower bound, same as any other stale-substrate read.

---

## Running a pass

### 1. Pick the scope

`$ARGUMENTS` is a bucket name (`needs-you` / `waiting-on-you` / `aging`), a repo name (filters `waiting-on-you`/`aging` to that repo), or `all` (walks all three in severity order: needs-you, then waiting-on-you, then aging). Empty → ask, per `triage.md`'s default block.

### 2. Pull the batch

Read `digest.md`'s relevant section fresh — don't trust a stale copy from earlier in a long session, `digest.md` changes on every merge. Take the next 6-8 items in the section's existing order. Give each a short session-scoped id: `NY1`, `NY2`… for needs-you, `WY1`, `WY2`… for waiting-on-you, `AG1`, `AG2`… for aging — numbered continuously across the whole bucket, not reset per batch, so "batch 2" starts at `WY7`, not `WY1` again. These ids are ephemeral: recomputed fresh each `/triage` run, never a stable cross-session identifier, and not the same thing as a PR number or a `failures.md` F-number.

### 3. Write the legend, then the widget

Per the visualize tool's own design rule, detail goes in your response text, not the widget box — so before calling `show_widget`, write a short plain list in chat: id, a compact paraphrase (one line — `digest.md`'s own text is often 2-3 sentences, cut it down), and the source file. This is also what lets you resolve the id when the click comes back, since the widget itself only shows a ~5-word label.

Then call `show_widget` (call `mcp__visualize__read_me` with `modules: ["interactive"]` first if this session hasn't already) with one card per item:

- Leading icon in a role-tinted circle: `ti-alert-triangle` / `--bg-danger` for needs-you, `ti-user-check` / `--bg-accent` for waiting-on-you, `ti-clock` / `--bg-warning` for aging. No emoji — the visualize system doesn't load them as icons, Tabler outline only.
- Title line: `<id> · <≤6-word label>`, sentence case, no bold beyond the pre-set weight.
- Subtitle line (`--text-secondary`, 13px): repo/source + age if known.
- One bare `<input type="text">` per card, `id="note-<id>"`, placeholder `Add context (optional)`, sitting between the subtitle and the buttons. Lets Royce attach a reason before clicking so a later read of wherever the click lands (an archived line, a spawned task, the fix itself) says *why*, not just *what*. Empty is the common case and costs nothing extra — this exists to prevent "why did I do this" confusion later, not to slow down the default path.
- Four bare `<button>` tags per card: `Act now ↗`, `Spawn task ↗`, `Defer ↗`, `Dismiss ↗` — each `onclick="triageAction('<id>','<verb>')"` using exactly those four verb strings. One shared `<script>` block at the end of the whole widget (after every card, per the visualize system's own streaming order — style, content, script last) reads the matching input at click time:
  ```js
  function triageAction(id, verb) {
    var el = document.getElementById('note-' + id);
    var note = el ? el.value.trim() : '';
    sendPrompt(note ? 'Triage ' + id + ': ' + verb + ' — ' + note : 'Triage ' + id + ': ' + verb);
  }
  ```
  Read the note from the input rather than hand-concatenating it into the `onclick` attribute — free text can contain a quote or apostrophe that would break a string literal built that way.
- Cards stacked vertically (`display:flex; flex-direction:column; gap:12px`), each a `--surface-2` box, `0.5px solid var(--border)`, `12px` radius, `1rem 1.25rem` padding. No left-border accent — it conflicts with rounded corners (single-sided border needs `border-radius:0`); the icon circle carries the color instead.
- One `<h2 class="sr-only">` first, summarizing the batch for screen readers.
- After the last card, one more bare row with two controls: `Next batch ↗` (`sendPrompt('Triage: next batch')`) if more remain in this bucket/scope, `Stop here ↗` (`sendPrompt('Triage: stop')`) always.

Keep this mechanical — the template is fixed, don't redesign it each run. If a batch is genuinely complex enough to need real design thought, that's a sign it doesn't belong in this tool (drop to `/decide`, or a normal Artifact, per the visualize system's own "consider an Artifact instead" escape hatch for anything past simple).

**One worked card plus the shared script**, so future runs have a literal pattern to copy rather than reconstructing these rules into markup from scratch:

```html
<div style="background:var(--surface-2); border:0.5px solid var(--border); border-radius:12px; padding:1rem 1.25rem;">
  <div style="display:flex; align-items:flex-start; gap:10px; margin-bottom:12px;">
    <div style="width:28px; height:28px; border-radius:50%; background:var(--bg-danger); display:flex; align-items:center; justify-content:center; flex-shrink:0;">
      <i class="ti ti-alert-triangle" style="font-size:16px; color:var(--text-danger);" aria-hidden="true"></i>
    </div>
    <div style="flex:1; min-width:0;">
      <p style="font-size:15px; font-weight:500; margin:0;">NY1 · SEC-1 live PII leak</p>
      <p style="font-size:13px; color:var(--text-secondary); margin:2px 0 0;">Public key reads people, timesheets, leave_requests, audit_log</p>
    </div>
  </div>
  <input type="text" id="note-NY1" placeholder="Add context (optional)" style="width:100%; margin:0 0 10px;" />
  <div style="display:flex; gap:8px; flex-wrap:wrap;">
    <button onclick="triageAction('NY1','act now')">Act now ↗</button>
    <button onclick="triageAction('NY1','spawn task')">Spawn task ↗</button>
    <button onclick="triageAction('NY1','defer')">Defer ↗</button>
    <button onclick="triageAction('NY1','dismiss')">Dismiss ↗</button>
  </div>
</div>
```

```html
<script>
function triageAction(id, verb) {
  var el = document.getElementById('note-' + id);
  var note = el ? el.value.trim() : '';
  sendPrompt(note ? 'Triage ' + id + ': ' + verb + ' — ' + note : 'Triage ' + id + ': ' + verb);
}
</script>
```

### 4. Handle the click

The reply lands as an ordinary next message: `Triage <id>: <verb>`, or `Triage <id>: <verb> — <comment>` if Royce typed something in that card's note field. Resolve `<id>` against the legend you wrote in step 3 (same conversation, a few lines up). The verb is always one of the four fixed strings, so anything after it following ` — ` is the comment, verbatim — don't paraphrase it away. Then:

- **Act now** — do the fix this turn, same as any normal request. Read the item's linked source file for full context first if the one-line digest summary isn't enough. A comment here is Royce steering the fix (a constraint, a preferred approach, a "but not X") — treat it as an instruction, not just a note to log.
- **Spawn task** — call `spawn_task` with a title/tldr/prompt built from the item's full text (not just the card's short label) and its source file path, so the spawned session doesn't need this conversation's context. Fold any comment into that prompt too — it's exactly the context a spawned session would otherwise be missing.
- **Defer** — bump the item's dated note in its *source* file. For a `waiting-on-you`/`aging` item sourced from a `pending.md`/`eq/pending/<repo>.md` entry, this means editing that line/section in place (new date, the comment as the one-line reason if given) — same dated-entry convention those files already use throughout. For a `needs-you` item sourced from `ops/security-register.md` or `system/failures.md`, read that file's own tracking convention first (status field, recurrence counter, whatever it already uses) rather than assuming the pending.md pattern transfers — these two files aren't structured like pending.md and haven't been audited as part of writing this protocol.
- **Dismiss** — for a `pending.md`-sourced item, move the line to the tier's `pending-archive.md` (the same split already used for completed items — see `eq/pending-archive.md`, `sks/pending-archive.md`, `ops/pending-archive.md`), carrying the comment across as the recorded reason. An archived line with no reason is exactly the "confusion later" the note field exists to prevent — if Royce didn't give one, archive it plainly rather than inventing one. For a `security-register.md`/`failures.md`-sourced item, same structural caveat as Defer above: check the file's own convention before writing anything.
- No comment given → proceed exactly as already specified above, nothing extra to log.
- Anything other than a clean `Triage <id>: <verb>` reply (a question about the item, a correction, "wait, explain NY3 first") — drop out of the button loop and just answer normally. Infer intent from phrasing, same as `/gap`'s revise mode; don't force it back into a card.

### 5. Don't commit per click

Accumulate edits across the whole run. Do not `git add`/`commit`/`push` after each item — `system/failures.md` F9 is concurrent-session git races corrupting this exact shared checkout, and a triage pass clicking through dozens of items in a row is the highest-risk shape for that failure. Commit once, at the natural end of the pass (Royce clicks "Stop here", the bucket runs out, or the session is closing anyway) — or just leave it for `/close`, which already does this as step 5 of its own sequence.

### 6. Close out

When the pass ends (bucket exhausted or "Stop here" clicked), give one short plain-text tally — counts by verb, e.g. "4 acted on, 2 spawned, 6 deferred, 1 dismissed" — and say plainly that nothing's pushed yet. No widget for this part; it's a summary sentence, not a new decision.

---

## Why this exists

Royce said he feels like there's a lot of pending stuff and wants a fast, clickable way to move through it — most of what "a lot" means already lives in `digest.md`'s Needs-you / Waiting-on-you / Aging sections (2026-09-07 snapshot: 7 / 261 / 344+, read from a clone that was 7-8 commits behind origin at the time — a lower bound, not exact), already curated, just never rendered as anything other than a markdown list read top to bottom. This protocol adds the interaction layer, not a new data source. (2026-09-07)
