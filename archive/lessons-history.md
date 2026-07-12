---
title: Lessons — Historical Narratives (ARCHIVED)
owner: Royce Milmlow
last_updated: 2026-07-12
scope: Full narrative write-ups moved out of system/lessons.md — either fully dead (pre-GitHub-substrate Supabase mechanisms, deleted 2026-06-22) or superseded by a shorter rule that now lives in one canonical place (system/failures.md, system/TODAY.md, hooks/README.md) per the "one fact, one home" rule (AUTONOMOUS-SPRINT-RULES.md §7). Kept for git history and full context — read only when tracing how a rule came to be.
read_priority: reference
status: archived
---

# Lessons — Historical Narratives

`system/lessons.md` keeps a short rule + a pointer here for each of these. Read this file when you want the full story behind a rule, not just the rule.

---

## Memory Drift on Substrate Names — Always Verify Before Describing

**Problem:** In a chat session diagramming the eq-context architecture, the assistant confidently described the Supabase context table as `claude_context` on a dedicated project. A live Supabase query revealed the table is actually `context_files` and lives co-tenant in `eq-solves-service-dev` (`urjhmkhbgaxrofurpbgc`).
**Fix:** Before describing any substrate (table names, project IDs, file paths, schema), run a live verification query through the relevant MCP. Memory is a draft, not a source.
**Why it matters:** The whole point of eq-context is to be ground truth. If the assistant's description of ground truth is itself wrong, every diagram, brief, and decision built on it inherits the error. Cheap to verify, expensive to undo.

**Retroactive note (added 2026-06-22):** The `context_files` table and the `eq-solves-service-dev` project (`urjhmkhbgaxrofurpbgc`) were deleted 2026-06-22. The substrate is now served directly from the public GitHub repo (github.com/eq-solutions/eq-context) via raw CDN URLs — no Supabase store. The principle still holds (verify before describing), but the verification target is now the GitHub raw URL, not a Supabase MCP query.

---

## Update Discipline Lapsed — 17 of 30 Files Stale by 15+ Days at 2026-04-27 Audit

**Problem:** Live audit of `context_files` on 2026-04-27 found that despite the README's "every session ends with update the MD" rule, 17 of 30 rows were last synced more than 15 days ago — including `knowledge/decisions.md`, `knowledge/architecture.md`, `knowledge/lessons.md`, and all seven `changelog/*` files. Sessions logs were appending fine; the substrate files that compound value across sessions were not.
**Root cause:** The discipline of "update the MD" became "update the session log" — the cheapest action got done, the higher-value ones did not. The sync action was never broken; the human-side habit was.
**Fix:**
1. End every chat session that produces a decision, lesson, or status change with an explicit Cowork or Code update directive.
2. Add a weekly Friday review: query `context_files` for any row older than 14 days, surface as a checklist.
3. The session log alone is not "updating the MD" — at minimum it pairs with one of decisions / lessons / pending / products / architecture.
**Why it matters:** The substrate's compounding value is the difference between a one-session AI tool and a portable operating system. Stale knowledge files quietly hollow that out without any visible failure.
**Retroactive note (added 2026-04-28):** The "17 of 30" count was partially inflated by an `updated_at` freshness bug fixed 2026-04-28. The GitHub Action's PostgREST upsert sent only `slug/filename/content`, and the column's `DEFAULT now()` only fires on INSERT — so for every row edited after its first sync, `updated_at` stayed frozen at the row's original creation time. Several of the "stale" files had genuinely been edited recently (frontmatter dates proved it). The discipline lapse was real, but the audit metric overstated it. With the new `context_files_set_updated_at` trigger (`BEFORE UPDATE FOR EACH ROW SET updated_at = NOW()`), the audit query now gives a clean signal. See "False-Implementation Pattern" below and `decisions.md` 2026-04-28 for the fix details.

---

## Substrate Audit Query — Use This to Spot Staleness Fast

**Pattern:** Run this Supabase query end-of-week to find files that have drifted past the cadence promised by the README's update-frequency table:

```sql
-- Updated 2026-05-04 for tier-separated structure (eq/sks/ops/system).
SELECT slug, updated_at, NOW() - updated_at AS age
FROM context_files
WHERE
  (slug LIKE '%/pending.md' AND updated_at < NOW() - INTERVAL '7 days')
  OR (slug LIKE 'system/%' AND updated_at < NOW() - INTERVAL '14 days')
  OR (slug LIKE 'ops/%' AND updated_at < NOW() - INTERVAL '14 days')
  OR (slug LIKE '%/changelog/%' AND updated_at < NOW() - INTERVAL '30 days')
  OR (slug LIKE 'archive/%' AND updated_at < NOW() - INTERVAL '180 days')
ORDER BY updated_at ASC;
```

Treat each result row as a "needs update or explicit no-change confirmation".

**Retroactive note (added 2026-06-22):** The `context_files` table and its host project (`urjhmkhbgaxrofurpbgc`) were deleted 2026-06-22. This SQL query is no longer executable. Staleness detection for the GitHub-based substrate can be done via: `gh api repos/eq-solutions/eq-context/commits?path=<file>&per_page=1` to get the last commit date per file, or by reading the `last_updated` frontmatter field in each markdown file directly.

---

## False-Implementation Pattern — Surface Signals Lie, Measurement Doesn't

**Problem:** On 2026-04-27/28, three "implementation complete" claims in one session all turned out to be wrong on measurement: (1) memory said wrong Supabase table name, (2) "brief was implemented" but nothing had been pushed, (3) "push landed" but the diff showed only one of three files changed and the content didn't match the brief.
**Fix:** After any change to eq-context, run this exact verification before claiming done:

```sql
SELECT slug, updated_at, LENGTH(content) AS chars,
  CASE WHEN content LIKE '%<expected-marker>%' THEN 'present' ELSE 'MISSING' END AS marker_check
FROM context_files
WHERE slug IN ('<file-1>', '<file-2>', '<file-3>');
```

Replace `<expected-marker>` with a unique string that should be in the new content (a date, a heading, a phrase). Replace the slugs with the files that should have changed.
**Why it matters:** Terminal output and commit hashes are success-shaped artefacts, not success itself. Only the row in Supabase containing the expected content counts as done.

**Retroactive note (added 2026-06-22):** The `context_files` Supabase table was deleted with its host project 2026-06-22. The substrate is now GitHub. The verification pattern is: fetch `https://raw.githubusercontent.com/eq-solutions/eq-context/main/<path>` and check the expected marker is present. "Done" = expected content at the raw GitHub URL, not a Supabase row.

---

## Sync Workflow Has Two Path Lists That Must Stay in Sync (2026-05-07)

**Problem:** `.github/workflows/sync-context.yml` has duplicate state for which folders count as substrate: a YAML `paths:` filter at the top that decides **whether** the workflow triggers on a push, and a Python `SUBDIR_PATTERNS` glob list inside the script that decides **what files** the script actually reads and upserts. When `sks-team/` was added as a new tier, only the YAML `paths:` filter was updated. The glob list was missed.

**Symptoms:**
- Push of `sks-team/quoting.md` to `main` triggers the workflow (path filter matches)
- Workflow runs green — exit code 0
- Verification job inside the workflow passes (it only checks slugs the script *tried* to sync)
- But `context_files` table has zero rows for `sks-team/*`
- Public edge function returns 404 for those paths
- Substrate looks healthy from every signal except direct DB query

**Root cause:** Path filter and glob list are duplicate state. They have to be kept in sync manually. There is no test or check that catches drift between them.

**Fix applied (2026-05-07):** Added `"sks-team/**/*.md"` to the `SUBDIR_PATTERNS` list. Verified end-to-end with a test commit — `sks-team/*` rows now sync within ~30 seconds of any push.

**Rule going forward:** When adding a new tier folder to `eq-context`, update **both** locations in `sync-context.yml`:
1. The `on.push.paths:` YAML list (top of file, ~line 11)
2. The Python `SUBDIR_PATTERNS` array (inside the inline script, ~line 53)

Future hardening worth considering: collapse the two into a single source — e.g. derive the YAML paths list from the Python list at workflow render time, or vice versa. Until then, treat them as a known footgun.

**Why it matters:** Workflow-green-but-rows-absent is a uniquely bad failure mode. It violates the "done = fresh updated_at" rule from the substrate non-negotiable and the False-Implementation Pattern lesson — but indirectly: the *expected* slugs were never queued for verification at all, so the verification job has nothing to fail on. The only signal that catches it is direct query against `context_files` for the slug you expected. Worth re-running that as a separate check after any workflow change touching path lists.

**Retroactive note (added 2026-06-22):** The Supabase cache (`context_files`, urjhmkhbgaxrofurpbgc) was deleted 2026-06-22. The `sync-context.yml` workflow now syncs to GitHub only. The diagnostic for a missed-path failure is: check the workflow run logs to confirm the file appeared in the triggered path list, then fetch the raw GitHub URL to verify content is present. The Supabase-query verification step is obsolete.

---

## Edge Function `/context/<slug>` Only Served Single-Segment Paths Until 2026-05-07

**Problem:** The Supabase edge function at `https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/<slug>` was written for the original flat 5-slug substrate (`eq`, `sks`, `cowork`, `rules`, `agents`). When the substrate was refactored on 2026-05-04 to tier-separated paths and the workflow started syncing slugs like `sks/team.md` and `sks-team/quoting.md`, the edge function was never updated. It used `pathParts[pathParts.length - 1]` to extract the slug — meaning `/context/sks-team/quoting.md` resolved to slug `quoting.md` and 404'd because no such row exists.

**Symptoms:** Top-level slugs (`/context/claude`, `/context/eq`) appeared to work. Anything tier-deep returned `# Not Found` even though the row was present in `context_files`. Easy to miss because the Cowork session-start protocol fetches `/context/claude` (works) and rarely fetches a tier-deep file from chat.

**Fix applied (2026-05-07):** Two-line change — slug now constructed by joining all path segments after `context/`, plus a fallback that tries `<slug>/README.md` when a single-segment slug doesn't resolve directly. So:
- `/context/eq` → tries `eq` → not found → tries `eq/README.md` → serves tier index
- `/context/sks-team/quoting.md` → tries `sks-team/quoting.md` → serves directly
- `/context/claude` → tries `claude` → serves directly (top-level slug exists)

**Why it matters:** Most of the substrate has been silently unreachable via public URL for ~3 days. Anyone fetching tier files from a non-Cowork tool got 404s. The edge function is the public face of the substrate — it has to keep up with substrate structure changes, same as the sync workflow does.

**Rule going forward:** When the substrate structure changes (new tier folder, renamed slug, etc.), the edge function is on the checklist of things to update — not just the workflow.

**Retroactive note (added 2026-06-22):** The Supabase project hosting this edge function (`urjhmkhbgaxrofurpbgc`, eq-solves-service-dev) was deleted 2026-06-22. The edge function no longer exists. The substrate is now served directly from the public GitHub repo via raw CDN URLs (https://raw.githubusercontent.com/eq-solutions/eq-context/main/<path>). The "update the edge function" checklist item is obsolete — the GitHub raw URL structure matches the file path directly and requires no function update.

---

## The Substrate Read Path Lied — `raw.githubusercontent.com/.../main/` Served 8–12 Day Stale Content (2026-07-11)

Full narrative moved here 2026-07-12; `system/lessons.md` keeps the short rule + this pointer. Canonical record: `system/failures.md` → **F1**.

**Problem:** A Cowork session ran the §1 start sequence and fetched the substrate via the canonical raw URLs. It was served:
- `CLAUDE.md` stamped **2026-06-04** — full of dead Supabase `urjh` URLs. Reality on `main`: the **2026-07-03** rewrite, GitHub-only, correct. **8 days stale.**
- `digest.md` stamped **2026-06-29**. Reality on `main`: **2026-07-11 08:14 UTC**, generated that morning. **12 days stale.**

Every fetch returned **200 OK**. No error. No warning. The repo was correct the entire time.

**Proof:** fetching the *same file at a pinned commit SHA* returned the **correct** content. The `/main/` branch alias and the SHA-pinned URL disagreed about the contents of the same commit. The branch alias is CDN-cached; the SHA path is not.

**What it cost:** the assistant concluded the master contract was broken, produced a confident critique of ~40 "dead URLs", and was authorised to rewrite the file. **Executing that would have reverted the 2026-07-03 work and reintroduced the dead Supabase URLs — while logging a session note saying it had fixed them.** Caught only because a `git` reflog read showed local `main` == `origin/main`, which contradicted the fetched file.

**Compounding cause:** Royce's Cowork *preferences* block contained a hand-written patch — "the substrate is GitHub only, fetch from raw.githubusercontent…" — written earlier to correct the then-stale contract. That patch **overrode `CLAUDE.md` §1's own instruction** (Cowork reads the *local clone*, not URLs) and routed the assistant to the cached URL. **The patch written to prevent substrate drift is what caused the assistant to read drifted substrate.**

**Fix (applied 2026-07-11):** `CLAUDE.md` §1 freshness gate; local clone **mandatory** for Code/Cowork; cache warning; delete the preferences patch. Enforced at rung 4 by `hooks/session_start.py`.

**Why it matters:** §1's "Fallback if substrate fetch fails" **cannot catch this** — it triggers on *errors*, and a stale cache hit is not an error. This is the precise failure the fallback exists to prevent (silent substitution), arriving through the one door the fallback doesn't watch. **An assistant reading silently-stale substrate is more dangerous than one with no substrate at all: it is confidently wrong, and it will "fix" work that was already done.**

**Rule:** treat a substrate read as *evidence*, not *truth*, until its `last_updated` is checked against the calendar. **If you have a clone, the clone wins. Always.**

---

## Writes to the `C:\Projects` Mount Are Not Safe — Neither Edit/Write NOR Append (2026-07-11)

Full narrative moved here 2026-07-12; `system/lessons.md` keeps the rule + the reference table + this pointer. Canonical record: `system/failures.md` → **F2**, **F6**. Enforced at rung 4 by `hooks/pre_tool_use.py`.

**This lesson cost us three times before it was enforced by a hook. Do not re-learn it by hand.**

Three distinct corruption modes on the `C:\Projects` virtiofs mount from the Cowork sandbox:

| Method | Behaviour | Safe? |
|---|---|---|
| `Edit` / `Write` tool on a long file | **Silently TRUNCATES.** Reports success. `CLAUDE.md` 308 → 277 lines; §12, §13 and End destroyed. | **NO** |
| `cat >> file << EOF` (append) | **NUL-FILLS.** Wrote **3,955 NUL bytes** instead of the content. The append is gone; the file becomes binary. Reports success. | **NO** |
| `cat > file << EOF` (full rewrite) | Correct. Verified on `CLAUDE.md` (308 lines), `TODAY.md`, `failures.md`, all hooks. | **YES** |

**The trap:** an earlier version of this lesson said *"For appends, prefer bash `cat >>` over Edit on long files."* **That advice was wrong and it destroyed a file.** Append is not a safe fallback. It is a different corruption with the same silent-success signature.

**Rule — no exceptions:**
1. **Full rewrite only.** `cat > file << 'EOF'`. Never `>>`. Never `Edit`/`Write` on anything long.
2. **Verify every single write:** `wc -l`, `tail -2`, and **`grep -c $'\x00'` — a NUL byte means the write corrupted.** A byte count that looks plausible is not proof; the NUL-fill produced a *larger* file.
3. **`wc -l` alone will not save you.** The NUL-filled `lessons.md` reported a *sane* line count. Only a NUL scan caught it.

**Why it matters:** every corruption mode on this mount **reports success**. The filesystem lies, the tools lie, and the line count lies. The only thing that does not lie is reading the bytes back. **Verify, or you did not write it.**

---

## The Substrate Contained a Goal Nobody Owned (2026-07-11)

Full narrative moved here 2026-07-12; `system/lessons.md` keeps the short rule + this pointer. Canonical record: `system/failures.md` → **F3**; `system/TODAY.md` carries its own "read this before using this file" telling of the same incident (kept there because it's the file most likely to be read by an agent about to repeat the mistake).

**Problem:** `system/TODAY.md` — `read_priority: critical`, the first file loaded by every assistant in every session, the stated filter for *every* build decision — contained:

> **A hard deadline nobody set.**
> *"Default question for every build/feature decision: does this move outcome 1, 2, or 3 before [the deadline]?"*

An assistant loaded it, believed it, and spent a session repeatedly telling Royce to **defer work** against that deadline. It shaped the priority of every recommendation made.

Then Royce said: **"what's that deadline? why are you mentioning it?"**

He did not recognise it. It had governed session prioritisation for two weeks.

**Nothing detected this. Nothing could.** Sixteen CI workflows. A nightly digest. A drift detector. `frontmatter-check`. And `auto-bump-frontmatter`, which was **faithfully keeping the phantom's `last_updated` looking fresh.** Every check passed green — because **every check verifies recency, not truth or ownership.**

**This is a different bug from substrate drift.** Drift is when the substrate *falls behind* reality. This is when the substrate contains something that was **never true, or stopped being true, and no mechanism exists to notice** — because no mechanism ever asked *"who says so, and is it still so?"*

`last_updated` records when someone **touched** a file. It says nothing about whether anything in it is **real**. A confident, well-formatted, freshly-dated, critically-prioritised assertion that no human currently owns will propagate through every agent you run, forever, and every check you have will report success. **Freshness is not truth. A fresh lie is still a lie — it is just a lie with better hygiene.**

**Fix (applied 2026-07-11, guard built 2026-07-12):**
1. **`TODAY.md` GOALS section is now explicitly `UNSET`** and blank. **A blank goals section is honest. A stale one is a phantom that steers every agent you run.** Never fill a slot in a critical file because it looks empty.
2. **Goals are typed, owned, and expiring.** `type: goal` · `owner` · `asserted_on` · `expires_on`. A goal nobody reconfirms **dies** and surfaces as *"confirm or kill."*
3. **No assistant may write a goal.** Assistants propose; only Royce owns. This is the specific safeguard that would have prevented it.
4. **`hooks/session_start.py`** announces `GOALS UNSET` at every session start.
5. **`claim-expiry.yml`** (built 2026-07-12) — a goal in `TODAY.md` that is undated, unowned, or past `expires_on` now fails CI, on change + nightly.

**The deeper rule — the one that generalises:** an agent quoting the substrate must **inherit its confidence type**. Say *"5 users (asserted 2026-06-28, unverified)"* — never *"5 users."* The assistant quoted `TODAY.md`'s guesses with exactly the same confidence as numbers pulled from live SQL, **because the substrate gave it no way to tell the difference.** That is the bug. Everything else is a symptom.

---

## The First Guard I Wrote Failed Open, Silently (2026-07-11)

Full narrative moved here 2026-07-12; `system/lessons.md` keeps the short rule + this pointer. `hooks/README.md`'s "Why fail-closed" section carries the same story, kept there because it's read by whoever next edits the hook.

**Problem:** `hooks/pre_tool_use.py` was written to block long-file `Edit`s (failure F2). Its first adversarial test — Edit a 308-line `CLAUDE.md` — **passed straight through.** The hook could not resolve the path, `line_count()` returned `0`, `0 > 200` was false, and it **allowed the write while reporting nothing.**

**The guard built to stop silent failures failed silently.** Caught only because the adversarial suite tested it instead of trusting it.

**Fix:** **fail-closed.** If the hook cannot resolve a path under the mount to count its lines, it **blocks**. Cost of a false block: one heredoc. Cost of a false allow: a destroyed file that reports success.

**Rule:** **a guard that fails open without announcing it is worse than no guard at all** — it manufactures the feeling of safety and delivers none of it. Every guard must answer: *what do I do when I don't know?* If the answer is "allow, quietly", it is not a guard, it is decoration. And: **never trust a guard you have not attacked.**
