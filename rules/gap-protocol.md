---
title: Gap / Centering Protocol
owner: Royce Milmlow
last_updated: 2026-08-02
scope: On-demand "where do I actually stand" pass — light mode is the default; full HTML/gap-table mode is parked for later
read_priority: high
status: live
---

# Gap / Centering Protocol

**Purpose:** remove the friction of not knowing where a piece of work actually stands — for Royce, mid-sprint, when a project has enough moving parts that gut feel and doc memory have drifted apart. It replaces "let me re-read everything" with one grounded pass that ends in a single next move.

**Trigger phrases:** `/gap <project>`, "run the (light) centering process", "I feel lost in the progress of this work", "where do we actually stand on X". Any tool that has read this file can run it from the phrases alone; `/gap` (`~/.claude/commands/gap.md`) is a Claude-Code-only convenience, not a requirement.

**Distinct from the other on-demand passes:**
- `/decide` (`rules/decision-protocol.md`) — choosing between options, before a choice is made.
- `/reflect` (`rules/reflection-protocol.md`) — auditing a finished output before it ships.
- `/gap` — neither. It's a **status reset**: what's actually true right now, what the smallest meaningful win looks like for the real person who feels the pain, the biggest gaps between them, and the one thing worth doing next.

**Default mode is Light** (below) — chat output, four questions, under a page. The heavier HTML/artifact version with the full Desired-State/Gap-table/Appetite structure is **parked**, not deleted — see "Full mode (parked)" at the bottom. Expand into it later if light mode proves too thin for a given project; don't reach for it by default.

---

## Light mode (default)

### Step 0 — cheap live check, before writing anything

Run one `git log --oneline -20` on the relevant repo before answering "Current Reality." This is the single cheapest thing that catches a stale doc claim — it's what caught both errors the one time this process skipped grounding (EQ Intake gap analysis, 2026-08-02: a "Parked" feature that had actually merged and deployed, and a "3 profiles" count that was actually 12). If a specific claim hinges on a DB row count or deploy state, check that one thing too — but don't run a full audit for a light pass. If live and memory/docs disagree, live wins, and say so in one clause ("actually shipped — git log shows PR #X merged \<date\>").

### The four questions

**1. Core problem** — one plain sentence: what real friction am I trying to remove, and for whom?

**2. Current Reality** — what actually exists and works today. Be blunt. No "almost," no "mostly."

**3. Desired Outcome** — what does the smallest meaningful win look like for the real person who feels the pain? One concrete moment, not a feature list.

**4. Gaps** — the 3 biggest things still missing between current reality and that win.

**5. Next Move** — the single smallest thing shippable or provable in the next time box that moves closest to that win. State the time box explicitly (ask if Royce didn't give one).

### Rules

- Whole response under one page.
- No fluff, no feature lists, no optimistic language.
- End with the exact next action and the time box, nothing appended after it.

### Defaults when `$ARGUMENTS` is empty

If no project is given, ask:

> Which project needs centering?
> 1. Name a repo or initiative directly
> 2. "This session" — the thing already being discussed
> 3. Free text — describe it

---

## Revise mode (light)

If Royce comes back with a short correction instead of a new run — a wording tweak, "that's expected, not a bug," "I'll handle that one," "let's just fix it now," or "explain that" — treat it the same way the full mode does: infer the intent (correct wording / reframe status / delegate ownership / act now / explain further) from phrasing rather than asking for a tag, and only touch the line referenced. Don't re-run Step 0 unless the correction implies a fact needs re-checking (e.g. "I think that one already shipped").

---

## Full mode (parked — not the default, build out further when actually needed)

The original heavier spec, kept here so expanding later is editing, not rebuilding from scratch. Do not run this unless Royce explicitly asks for the fuller version (e.g. "give me the full centering doc" / "I want the artifact version").

### CRITICAL — ground every claim in the live system, not docs or memory

Same rule as Step 0 above, but exhaustive: before any status claim, check (1) git log on the relevant repo(s), (2) a live DB query if the domain has one (Supabase MCP `list_tables` / `execute_sql`), (3) current deploy state (Netlify MCP). Live wins over docs, and the output says so explicitly when they disagree.

### Output: one self-contained HTML document

Filename: `[project]-centering.html`. Single HTML file, inline CSS, delivered via the Artifact tool (load `artifact-design` first). EQ-brand-consistent per `rules/brand-eq.md`: Plus Jakarta Sans, `#3DA8D8` / `#2986B4` / `#EAF5FB` / `#1A1A2E`, no gradients, no shadows on static cards, flat Linear/Notion aesthetic, theme-aware, calm operator tone.

**Sections:** Hero (project, date, one-line purpose) → **1. Current Reality** (status labels only: Live / Partial / In Progress / Parked / Not started — no optimistic language) → **2. Desired State (100/100)** (4-6 concrete friction-disappeared moments for named real people, not a feature list) → **3. Gap Analysis** (P1/P2/P3 table, every gap mapped to a named 100/100 moment, columns: Priority / Gap / Blocks / Current status / Smallest next verifiable outcome) → **4. Appetite & Kill Criteria** (time/energy budget for the next move only, plus specific evidence that would kill/redirect it) → **Centering Action** (single highest-leverage next move + smallest shippable proof within the appetite).

### Non-negotiable rules

Operator voice. Truth over optimism. Flag incomplete/parked work in its own row, never inside a summary sentence. Short and ruthless — clarity over completeness.

### Revise mode (full, section-keyed)

Royce may annotate a delivered doc section-by-section instead of writing a new prompt, e.g.:

```
Desired state
C - For SKS its workbench, can we use "payroll" - generic terms

Gaps
P1 - Getting closer to onboarding the whole team, doing it in tranches
P1 - I'll investigate if you can upload timesheets into workbench
P2 - Lets work on a solution now
P2 - explain this further
```

Infer intent from phrasing, no rigid tag syntax:

| Phrasing pattern | Intent | Action |
|---|---|---|
| "use X instead", wording correction | **Correct wording** | Edit that row/line only, re-render |
| "getting closer to X", "this is expected" | **Reframe status** | Update status + one-line context; not a newly-discovered bug |
| "I'll investigate", "leave this with me" | **Delegate ownership** | Mark owned by Royce, don't queue as a Centering Action |
| "let's work on a solution now", "fix this" | **Act now** | Stop revising the doc — do the work this session |
| "explain this further", "why" | **Explain, don't edit** | Answer in chat; only change the doc if the explanation reveals the original claim was wrong |

Regenerate only the referenced sections/rows. Don't re-run the full live-verification pass unless the annotation implies a new fact needs checking. If intent is genuinely ambiguous, ask — one line, two readings — rather than guess.
