---
title: SYSTEM — Lessons Learned
owner: Royce Milmlow
last_updated: 2026-05-24
scope: Hard-won technical gotchas; append-only
read_priority: reference
status: live
---

# SYSTEM — Lessons Learned

Hard-won technical knowledge. Append — never overwrite.
Format: what went wrong → what the fix is → why it matters.

---

## Netlify — `build_settings.repo_url` Cannot Be PATCHed Via API

**Problem:** When migrating a Netlify project to a new source GitHub repo, the obvious move is `PATCH /api/v1/sites/{id}` with `{"build_settings":{"repo_url":"https://github.com/<new>","repo_path":"<new>","provider":"github","repo_branch":"main",...}}`. The API returns 200 OK with a refreshed `updated_at` — but `repo_url` and `repo_path` in the response are unchanged. The patch is **silently rejected**. Confirmed 2026-05-20 attempting to rewire `sks-nsw-labour.netlify.app` from `eq-solutions/eq-field` to `eq-solutions/sks-nsw-labour`.

**Fix:** The repo source on a Netlify project is OAuth-protected (it requires the GitHub App webhook + deploy key to be set up on the new repo). It can only be changed through:

1. **Netlify dashboard** — Project → Configuration → Build & deploy → Continuous deployment → Repository → Manage repository → Link to a different repository. The standard supported path. Takes ~60s, preserves all env vars, build settings, custom domains, deploy hooks. Recommended.
2. **Netlify CLI** — `netlify link` operates on local folders, not at remote project config level. No CLI command exposes the relink-to-different-repo operation.
3. **Recreate the project** — `POST /sites` with the new repo, migrate env vars, swap the custom domain. Heavy.

After the dashboard relink, the new repo is wired but Netlify does **not** auto-trigger a deploy from it (Netlify only auto-deploys on git push webhooks). Trigger a first build manually via `POST /api/v1/sites/{id}/builds` with `{}` body, then poll `/sites/{id}/deploys/{deploy_id}` until `state=ready`.

**Also note:** branch-only changes (`build_settings.repo_branch`) on the same site are subject to the same silent rejection. Same dashboard path: change "Branch to deploy" in Build settings. Discovered while migrating `eq-solves-field.netlify.app` from `demo` → `main` after the 2026-05-20 demo→main rename.

**Why it matters:** The "I'll script the Netlify rewire" assumption costs the most time when discovered mid-migration — the new repo is already created, code is already pushed, and you're staring at an API that lied with a 200. Better to know up front that the rewire is a dashboard step (or a manual user action) and plan the migration with that in the critical path. Affects any migration that splits one repo into two, consolidates two into one, or moves a repo between orgs.

---

## Supabase Function Migrations — Search Path + Privilege Hygiene

**Problem:** Supabase Security Advisor flags every function lacking an explicit `SET search_path` in its definition (category: "Function Search Path Mutable"), and every `SECURITY DEFINER` function callable by `public` or `authenticated` (categories: "Public Can Execute SECURITY DEFINER" and "Signed-In Users Can Execute SECURITY DEFINER"). Discovered 2026-05-19 on `eq-demo-canonical` — 17 warnings on 7 functions across the 4 advisor categories, all originating from `eq-intake/sql/001-003_*.sql`. The migrations used a session-level `set search_path = public` at the top of the file (which only affects the migration session), but didn't bake `SET search_path` into each function definition.

**Fix:** Two parts.

1. **Per-function (in the migration):** Every `CREATE FUNCTION` (or `CREATE OR REPLACE FUNCTION`) MUST include `SET search_path = public, pg_temp` (or whatever schema list the function actually needs) inside the function declaration — not just at file top. Example: `CREATE FUNCTION foo() RETURNS void LANGUAGE plpgsql SET search_path = public, pg_temp AS $$ ... $$;`
2. **Per-`SECURITY DEFINER` function:** Always pair the `CREATE FUNCTION ... SECURITY DEFINER` with explicit grants: `REVOKE EXECUTE ... FROM PUBLIC; REVOKE EXECUTE ... FROM authenticated; GRANT EXECUTE ... TO service_role` (or whichever specific role legitimately calls it). The default privilege on functions is `EXECUTE TO PUBLIC` which is wrong for server-side machinery.
3. **For existing functions that already shipped without these:** apply a follow-up migration using `ALTER FUNCTION ... SET search_path` and `REVOKE/GRANT` statements. Use `pg_catalog.pg_proc` iteration to catch every overload defensively — see `eq-intake/sql/004_security_advisor_fix.sql` for the pattern.

**Why it matters:** Mutable `search_path` enables function hijack — an attacker creates a same-named function in a schema earlier in the search path (e.g. `pg_temp` in a session they control) and your `SECURITY DEFINER` function calls *theirs* with elevated privileges. Public-callable `SECURITY DEFINER` lets unauthenticated requests (anon key) run with the function owner's privileges. Both are low *real* risk in default hosted Supabase environments — public schema writes are restricted, `pg_temp` is per-session — but trivial to prevent at write time, and the advisor reflags every new function as you build. Cleaning at definition time costs zero; cleaning retroactively costs a migration per project.

---

## GitHub API

**Problem:** Inline `-d` flag fails for large JSON payloads in GitHub API PUT requests.
**Fix:** Write full JSON payload (base64-encoded content) to a temp file, use `--data @/tmp/payload.json`.
**Also:** Always include `branch` parameter explicitly. Include existing file's blob SHA in PUT requests or the API rejects the update.

---

## GitHub API — Pushing Multiple Files

**Problem:** GitHub Contents API requires one HTTP request per file — no bulk push endpoint.
**Fix:** Use a Python script to loop through files, fetching SHAs first then PUTting each file.
**Pattern:** Get tree with `?recursive=1` to retrieve all SHAs in one call, then push files individually.

---

## GitHub MCP — Session Activation

**Problem:** GitHub MCP tools don't always load in a session that was open before the connector was authorised.
**Fix:** Start a fresh chat session after connecting GitHub MCP. Tools load correctly from session start.
**Fallback:** Use GitHub API with a temporary PAT if MCP tools unavailable. Revoke PAT after use.

---

## SVG Uploads to Claude Project

**Problem:** Claude.ai blocks SVG file uploads for security reasons.
**Fix:** Rename SVG files to .txt before uploading. Rename back after downloading.

---

## ASIC Connect

**Problem:** ASIC Connect doesn't work in modern browsers.
**Fix:** Use Edge in Internet Explorer compatibility mode.
**Also:** Leave the Building/Property name field blank for standard residential addresses.

---

## pptxgenjs — PowerPoint Compatibility

**Problem:** Files generated by pptxgenjs open fine in LibreOffice but PowerPoint throws corrupt file error.
**Root cause:** Empty directory entries in the ZIP that LibreOffice ignores but PowerPoint rejects.
**Fix:** Strip empty directory entries after generation — skip entries ending in `/`.

---

## docx Library — Page Numbers

**Problem:** `PageNumber` is not a direct named export from the `docx` npm library.
**Fix:** Use `SimpleField("PAGE")` instead.

---

## ReportLab — Subscripts/Superscripts

**Problem:** Unicode subscript/superscript characters render as solid black boxes in ReportLab PDFs.
**Fix:** Use ReportLab XML markup tags: `<sub>2</sub>` and `<super>2</super>` in Paragraph objects.

---

## Email Security — ZIP Files with Executables

**Problem:** ZIP files containing .bat, .exe, or Python scripts are flagged by corporate email security.
**Fix:** Remove all executables from distributions. Use single-file HTML + Cloudflare Worker instead.

---

## ThreatLocker on Corporate PCs

**Problem:** ThreatLocker blocks Python, .bat files, and unapproved executables on SKS corporate laptops.
**Fix:** Single-file HTML approach — opens in any browser, zero install, nothing for ThreatLocker to block.
**Escalation:** If HTML file itself is blocked, host on Cloudflare Pages and share a URL.

---

## SheetJS for Client-Side Excel

**Lesson:** SheetJS (xlsx.full.min.js from cdnjs) generates valid .xlsx files entirely in the browser.
No server, no Python, no openpyxl needed for single-file tool distribution.
CDN: `https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js`
**Limitation:** Complex formatting requires openpyxl server-side for pixel-perfect templates.

---

## localStorage Data Design

**Lesson:** Design localStorage data structures as if going into Supabase from day one.
Use UUIDs (`crypto.randomUUID()`), ISO date strings, consistent field names.
Migration to Supabase then only requires replacing read/write functions — no reshaping.

---

## Cloudflare Worker CORS

**Lesson:** Always include CORS headers in worker response AND handle OPTIONS preflight.
Without OPTIONS handling, browsers block the first request before it reaches the worker.

---

## HHT Crypto — CGT Investor Classification

**Lesson:** Hexican Holdings Trust is CGT investor across ALL crypto — not trading stock.
Capital losses in HHT are quarantined within the trust — cannot flow to personal or CDC.
Do not suggest strategies that assume these losses are available elsewhere.

---

## eq-context GitHub Upload — Browser Drag and Drop Flattens Folders

**Problem:** Dragging a zip or folder into GitHub's browser upload flattens the folder structure —
all files land in root, subfolders are lost.
**Fix:** Either push via git CLI, or use GitHub API (Python script with base64 encoding per file).

---

## Cowork Sandbox + Git — Orphan `.git/index.lock` (the Loop of Despair)

**Problem:** When Claude runs `git` from the Cowork Linux sandbox against a Windows-mounted repo (`C:\Projects\*`), every git command leaves a `.git/index.lock` behind that the sandbox **cannot unlink** — the virtiofs mount allows create/overwrite but blocks `unlink()` on files that pre-existed the session. The lock then blocks every subsequent git command, including the user's own commands from PowerShell/cmd. Cleaning it from Windows usually works, but if Claude keeps running git from the sandbox, a fresh orphan lock appears within seconds and the user is stuck in a loop.

**Symptoms:** `fatal: Unable to create '.git/index.lock': File exists. Another git process seems to be running...` repeating across many commands, even after deleting the lock.

**Root cause:** Each Linux-side git op opens `index.lock`, then tries to `unlink()` it on exit. virtiofs returns `EPERM` for unlink-of-pre-existing-file. The lock survives. Next git op sees it, errors out. Repeat.

**Recovery (Windows side):**
- cmd: `del /f /q .git\index.lock`
- PowerShell: `Remove-Item .git\index.lock -Force`
- If both fail (rare): rename first — `ren .git\index.lock index.lock.dead && del .git\index.lock.dead`

**Rule for Claude:** Do NOT run `git` (status, add, commit, rm, pull, push, anything) from the Cowork sandbox against `C:\Projects\*` repos. Use Read/Write/Edit for file content; emit a `.bat` (cmd) or `.ps1` (PowerShell) script for the user to run. Read-only inspection via `cat .git/HEAD`, `cat .git/refs/heads/*` is fine — those don't take a lock.

**Bonus:** If user's terminal title says "Command Prompt", they're in cmd.exe — `Remove-Item` won't work. Match the script type to the shell.

**Bonus 2:** Edit/Write file tools may TRUNCATE writes silently against this mount when the file is large. For appends, prefer bash `cat >> file << EOF` over Edit on long files.

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
**Retroactive note (added 2026-04-28):** The "17 of 30" count was partially inflated by an `updated_at` freshness bug fixed 2026-04-28. The GitHub Action's PostgREST upsert sent only `slug/filename/content`, and the column's `DEFAULT now()` only fires on INSERT — so for every row edited after its first sync, `updated_at` stayed frozen at the row's original creation time. Several of the "stale" files had genuinely been edited recently (frontmatter dates proved it). The discipline lapse was real, but the audit metric overstated it. With the new `context_files_set_updated_at` trigger (`BEFORE UPDATE FOR EACH ROW SET updated_at = NOW()`), the audit query now gives a clean signal. See "False-Implementation Pattern" lesson and `decisions.md` 2026-04-28 for the fix details.

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
- `/context/eq` → tries `eq` → not found → tries `eq/README.md` → ✅ serves tier index
- `/context/sks-team/quoting.md` → tries `sks-team/quoting.md` → ✅ serves directly
- `/context/claude` → tries `claude` → ✅ serves directly (top-level slug exists)

**Why it matters:** Most of the substrate has been silently unreachable via public URL for ~3 days. Anyone fetching tier files from a non-Cowork tool got 404s. The edge function is the public face of the substrate — it has to keep up with substrate structure changes, same as the sync workflow does.

**Rule going forward:** When the substrate structure changes (new tier folder, renamed slug, etc.), the edge function is on the checklist of things to update — not just the workflow.

**Retroactive note (added 2026-06-22):** The Supabase project hosting this edge function (`urjhmkhbgaxrofurpbgc`, eq-solves-service-dev) was deleted 2026-06-22. The edge function no longer exists. The substrate is now served directly from the public GitHub repo via raw CDN URLs (https://raw.githubusercontent.com/eq-solutions/eq-context/main/<path>). The "update the edge function" checklist item is obsolete — the GitHub raw URL structure matches the file path directly and requires no function update.

---

## PowerShell Won't Run Scripts from CWD Without `.\` Prefix (2026-05-14)

**Problem:** Royce typed `setup-and-push.bat` at a PowerShell prompt in
`C:\Projects\eq-context`. The file existed, but PowerShell threw
`CommandNotFoundException` with `setup-and-push.bat : The term ... is
not recognized`. cmd.exe runs current-directory scripts directly;
PowerShell does not, by default, for safety.

**Fix:** `.\setup-and-push.bat` — or invoke via cmd: `cmd /c setup-and-push.bat`.

**Why it matters:** When emitting `.bat` files for Royce to run, default
to telling him `.\name.bat` rather than `name.bat`. Costs nothing if
he's in cmd, saves a round-trip if he's in PowerShell (which is the
default modern terminal).

---

## `Repository not found` from GitHub is Ambiguous (2026-05-14)

**Problem:** `git push` returned `remote: Repository not found / fatal:
repository '...' not found` for `Milmlow/eq-solves-assets`. Easy to
mis-diagnose as a credential failure — but GitHub returns this same
404 for both genuinely-missing repos AND access-denied private repos
(deliberate, to avoid leaking private repo names).

**Fix:** Before assuming a credential problem, browser-verify the
remote URL exists. If the repo is listed under the user/org page but
the push still 404s, then it's a PAT scope issue. If the repo isn't
listed at all, the local clone's remote URL is wrong (renamed?
typo?).

**Why it matters:** Auth diagnostics waste a lot of time when the real
problem is a missing remote. One browser tab beats ten rounds of
credential helper debugging.

---

## `demo` Branch Protection Caught Us — But For the Wrong Reason (2026-05-14)

**Problem:** A multi-repo push script (`push-all.bat`) blindly ran
`git push origin HEAD` against four repos. For eq-solves-field, local
HEAD was on `demo` branch and the push was rejected as non-fast-forward
(remote had unmerged commits). The reject was correct, but the rule
that *should* have caught it — CLAUDE.md §11 "never push to `demo`
without instruction" — wasn't enforced anywhere. The reject was a happy
accident, not a designed safety net.

**Fix:** Push automation needs to be branch-aware. The post-commit hook
for eq-context only pushes when on `main` — same pattern should apply
to per-repo hooks for the apps. For `push-all.bat`, the safer default
is `git push origin main` (explicit branch), not `git push origin HEAD`
(whatever-you're-checked-out-on).

**Why it matters:** The hard rules in §11 only help if they're encoded
into the automation. "Never push to demo" as prose protects you in
manual workflow; the same rule has to be a `branch != demo` check
in any script that pushes.

---

## `.git-credentials` Should Never Travel Through Chat (2026-05-14)

**Problem:** Mid-session, the credentials file was uploaded into chat
as a `.git-credentials` file to wire up a push. Even though it wasn't
read by Claude, the file sat in plaintext in
`%APPDATA%\Claude\local-agent-mode-sessions\...\uploads\` and in
chat history. Anyone with access to either could exfiltrate PATs.

**Fix:** For credential installation, generate a `.bat`/`.ps1` that
reads the credentials from a path the user already controls (their own
file, not an upload) and writes to `%USERPROFILE%\.git-credentials`.
If a file must move, it moves on the user's machine — never through
the chat boundary.

**Recovery if it already happened:** delete the uploaded file from
`%APPDATA%\Claude\local-agent-mode-sessions\...\uploads\` and rotate
the PATs. Treat any credentials that touched chat as compromised.

**Why it matters:** The substrate has a hard rule against hardcoded
credentials. The same posture has to extend to credentials in flight
— not just credentials at rest in code.

---

## `core.hooksPath` Pointing at Wrong Directory — Pre-Commit Hook Silently Skipped (2026-05-24)

**Problem:** `git config core.hooksPath` was set to `hooks/` which only contained `post-commit` (the auto-push script). The pre-commit hook that bumps `last_updated` on staged files lived in `.githooks/pre-commit`. Because `core.hooksPath` didn't point at `.githooks/`, the pre-commit hook never ran — silently. Symptoms: `last_updated` dates were never bumping before commits, the GitHub `auto-bump-frontmatter.yml` bot kept detecting stale dates and pushing its own bump commits, and every `git push` required a `git pull --rebase` first because the bot had already pushed.

**Fix:** Three steps.
1. Copy `hooks/post-commit` → `.githooks/post-commit` so both hooks live in the same directory.
2. Change `core.hooksPath` from `hooks` to `.githooks` (local git config: `git config core.hooksPath .githooks`).
3. Update `scripts/install-hooks.ps1` to check for `post-commit` in `.githooks/` and `chmod +x` both hooks.

After the fix: pre-commit bumps dates before each commit, the bot finds nothing to change, pushes land clean on the first try.

**Re-clone setup:** Run `.\scripts\install-hooks.ps1` after cloning to wire `core.hooksPath` correctly. Without this step the hooks directory defaults to `.git/hooks/` which is empty.

**Why it matters:** A pre-commit hook that silently doesn't run is worse than no hook at all — you think the guard is in place and it isn't. The tell was the bot's auto-bump commits appearing on every push. Any time you see the bot fighting your pushes, check `git config core.hooksPath` before diagnosing the bot itself.

---

## Verify the Live System Before Building (added 2026-06-22)

**Rule:** Before writing any code, migration, or PR — query the actual live system. Do not trust docs, suite-state.md, session logs, or substrate files as a substitute for live verification. The failure mode (documented 2026-06-03) is: assume something is not built, build a parallel version, discover it already existed — wasted work and reverts.

**Checklist before any build task:**
1. `list_tables` on the relevant Supabase project (ehow: ehowgjardagevnrluult or eq-canonical: jvknxcmbtrfnxfrwfimn)
2. `git branch -a` + `git status` on the target repo
3. Check worktree-registry.md for in-flight work on a branch
4. Read suite-state.md for CI/deploy status

**Why it matters:** Substrate files lag reality. A 10-second Supabase query beats a wrong-premise build that takes two hours to undo.

---

## Substrate Lags Reality — and urjh Is Deleted (added 2026-06-22)

**Rule:** Substrate files (CLAUDE.md, suite-state.md, session logs, pending.md) always lag the live system. Treat substrate claims about DB schema, applied migrations, deployed versions, and key/secret status as leads to verify — not facts.

**Critical dead reference:** Supabase project `urjhmkhbgaxrofurpbgc` (urjh / eq-solves-service-dev) was DELETED 2026-06-22. Any reference to it as a live project in substrate files is stale. Do not query it, do not reference it as a data store, do not deploy edge functions to it. The sole live DB for EQ Service and EQ Field is ehow (`ehowgjardagevnrluult`).

**The substrate itself is on GitHub:** The eq-context substrate is served via GitHub raw CDN (https://raw.githubusercontent.com/eq-solutions/eq-context/main/<path>). There is no Supabase cache, no edge function, no context_files table. These were all retired when urjh was deleted.

---

## The Substrate Read Path Lied — `raw.githubusercontent.com/.../main/` Served 8–12 Day Stale Content (2026-07-11)

**Problem:** A Cowork session ran the §1 start sequence and fetched the substrate via the canonical raw URLs. It was served:
- `CLAUDE.md` stamped **2026-06-04** — full of dead Supabase `urjh` URLs. Reality on `main`: the **2026-07-03** rewrite, GitHub-only, correct. **8 days stale.**
- `digest.md` stamped **2026-06-29**. Reality on `main`: **2026-07-11 08:14 UTC**, generated that morning. **12 days stale.**

Every fetch returned **200 OK**. No error. No warning. The repo was correct the entire time.

**Proof:** fetching the *same file at a pinned commit SHA* returned the **correct** content. The `/main/` branch alias and the SHA-pinned URL disagreed about the contents of the same commit. The branch alias is CDN-cached; the SHA path is not.

**What it cost:** the assistant concluded the master contract was broken, produced a confident critique of ~40 "dead URLs", and was authorised to rewrite the file. **Executing that would have reverted the 2026-07-03 work and reintroduced the dead Supabase URLs — while logging a session note saying it had fixed them.** Caught only because a `git` reflog read showed local `main` == `origin/main`, which contradicted the fetched file.

**Compounding cause:** Royce's Cowork *preferences* block contained a hand-written patch — "the substrate is GitHub only, fetch from raw.githubusercontent…" — written earlier to correct the then-stale contract. That patch **overrode `CLAUDE.md` §1's own instruction** (Cowork reads the *local clone*, not URLs) and routed the assistant to the cached URL. **The patch written to prevent substrate drift is what caused the assistant to read drifted substrate.**

**Fix (applied 2026-07-11):** `CLAUDE.md` §1 freshness gate; local clone **mandatory** for Code/Cowork; cache warning; delete the preferences patch. Enforced at rung 4 by `hooks/session_start.py`. Logged as **F1** in `system/failures.md`.

**Why it matters:** §1's "Fallback if substrate fetch fails" **cannot catch this** — it triggers on *errors*, and a stale cache hit is not an error. This is the precise failure the fallback exists to prevent (silent substitution), arriving through the one door the fallback doesn't watch. **An assistant reading silently-stale substrate is more dangerous than one with no substrate at all: it is confidently wrong, and it will "fix" work that was already done.**

**Rule:** treat a substrate read as *evidence*, not *truth*, until its `last_updated` is checked against the calendar. **If you have a clone, the clone wins. Always.**

---

## Writes to the `C:\Projects` Mount Are Not Safe — Neither Edit/Write NOR Append (2026-07-11)

**This lesson has now cost us three times. It is enforced at rung 4 (`hooks/pre_tool_use.py`). Do not re-learn it.**

Three distinct corruption modes on the `C:\Projects` virtiofs mount from the Cowork sandbox:

| Method | Behaviour | Safe? |
|---|---|---|
| `Edit` / `Write` tool on a long file | **Silently TRUNCATES.** Reports success. `CLAUDE.md` 308 → 277 lines; §12, §13 and End destroyed. | **NO** |
| `cat >> file << EOF` (append) | **NUL-FILLS.** Wrote **3,955 NUL bytes** instead of the content. The append is gone; the file becomes binary. Reports success. | **NO** |
| `cat > file << EOF` (full rewrite) | Correct. Verified on `CLAUDE.md` (308 lines), `TODAY.md`, `failures.md`, all hooks. | **YES** |

**The trap:** the earlier version of this lesson said *"For appends, prefer bash `cat >>` over Edit on long files."* **That advice was wrong and it destroyed this file.** Append is not a safe fallback. It is a different corruption with the same silent-success signature.

**Rule — no exceptions:**
1. **Full rewrite only.** `cat > file << 'EOF'`. Never `>>`. Never `Edit`/`Write` on anything long.
2. **Verify every single write:** `wc -l`, `tail -2`, and **`grep -c $'\x00'` — a NUL byte means the write corrupted.** A byte count that looks plausible is not proof; the NUL-fill produced a *larger* file.
3. **`wc -l` alone will not save you.** The NUL-filled `lessons.md` reported a *sane* line count. Only a NUL scan caught it.

**Why it matters:** every corruption mode on this mount **reports success**. The filesystem lies, the tools lie, and the line count lies. The only thing that does not lie is reading the bytes back. **Verify, or you did not write it.**

---

## The Substrate Contained a Goal Nobody Owned (2026-07-11)

**Problem:** `system/TODAY.md` — `read_priority: critical`, the first file loaded by every assistant in every session, the stated filter for *every* build decision — contained:

> **34 days to 1 August 2026.**
> *"Default question for every build/feature decision: does this move outcome 1, 2, or 3 before 1 August?"*

An assistant loaded it, believed it, and spent a session repeatedly telling Royce to **defer work** against that deadline. It shaped the priority of every recommendation made.

Then Royce said: **"what's august 1? why are you mentioning that?"**

He did not recognise it. It had governed session prioritisation for two weeks.

**Nothing detected this. Nothing could.** Sixteen CI workflows. A nightly digest. A drift detector. `frontmatter-check`. And `auto-bump-frontmatter`, which was **faithfully keeping the phantom's `last_updated` looking fresh.** Every check passed green — because **every check verifies recency, not truth or ownership.**

**This is a different bug from substrate drift.** Drift is when the substrate *falls behind* reality. This is when the substrate contains something that was **never true, or stopped being true, and no mechanism exists to notice** — because no mechanism ever asked *"who says so, and is it still so?"*

`last_updated` records when someone **touched** a file. It says nothing about whether anything in it is **real**. A confident, well-formatted, freshly-dated, critically-prioritised assertion that no human currently owns will propagate through every agent you run, forever, and every check you have will report success. **Freshness is not truth. A fresh lie is still a lie — it is just a lie with better hygiene.**

**Fix (applied 2026-07-11):**
1. **`TODAY.md` GOALS section is now explicitly `UNSET`** and blank. **A blank goals section is honest. A stale one is a phantom that steers every agent you run.** Never fill a slot in a critical file because it looks empty.
2. **Goals are typed, owned, and expiring.** `type: goal` · `owner` · `asserted_on` · `expires_on`. A goal nobody reconfirms **dies** and surfaces as *"confirm or kill."*
3. **No assistant may write a goal.** Assistants propose; only Royce owns. This is the specific safeguard that would have prevented it.
4. **`hooks/session_start.py`** announces `GOALS UNSET` at every session start: *"you have NO BASIS to defer or deprioritise anything."*
5. Logged as **F3** in `system/failures.md`. Target rung 3 (`claim-expiry.yml`) — **not yet built.**

**Rule:** treat **facts** and **goals** as different substances with different half-lives. A fact ("ehow is the live DB") is machine-verifiable and should be re-checked by SQL. A goal ("NSW live by August") is verifiable *only by the human who owns it*, and must expire fast. Storing both in the same file under the same freshness rules is precisely how a lapsed intention becomes a governing constraint.

**The deeper rule — the one that generalises:** an agent quoting the substrate must **inherit its confidence type**. Say *"5 users (asserted 2026-06-28, unverified)"* — never *"5 users."* On 2026-07-11 the assistant quoted `TODAY.md`'s guesses with exactly the same confidence as numbers it had pulled from live SQL, **because the substrate gave it no way to tell the difference.** That is the bug. Everything else is a symptom.

---

## The First Guard I Wrote Failed Open, Silently (2026-07-11)

**Problem:** `hooks/pre_tool_use.py` was written to block long-file `Edit`s (failure F2). Its first adversarial test — Edit a 308-line `CLAUDE.md` — **passed straight through.** The hook could not resolve the path, `line_count()` returned `0`, `0 > 200` was false, and it **allowed the write while reporting nothing.**

**The guard built to stop silent failures failed silently.** Caught only because the adversarial suite tested it instead of trusting it.

**Fix:** **fail-closed.** If the hook cannot resolve a path under the mount to count its lines, it **blocks**. Cost of a false block: one heredoc. Cost of a false allow: a destroyed file that reports success.

**Rule:** **a guard that fails open without announcing it is worse than no guard at all** — it manufactures the feeling of safety and delivers none of it. Every guard must answer: *what do I do when I don't know?* If the answer is "allow, quietly", it is not a guard, it is decoration. And: **never trust a guard you have not attacked.** `hooks/adversarial_test.sh` — 15 tests, seeded from every failure that has ever escaped. Every future escape gets added.
