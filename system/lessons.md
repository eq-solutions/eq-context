---
title: SYSTEM — Lessons Learned
owner: Royce Milmlow
last_updated: 2026-07-12
scope: Hard-won technical gotchas; append-only. Full narratives for the entries marked "moved to archive" live in archive/lessons-history.md.
read_priority: reference
status: live
---

# SYSTEM — Lessons Learned

Hard-won technical knowledge. Append — never overwrite.
Format: what went wrong → what the fix is → why it matters.

**Trimmed 2026-07-12** — several entries here were the full narrative of an
incident that's also told, more canonically, in `system/failures.md` (the
ledger), `system/TODAY.md` (the specific goal-nobody-owned incident), or
`hooks/README.md` (the guard-construction stories). Per the repo's own
"one fact, one home" rule (`AUTONOMOUS-SPRINT-RULES.md` §7), those entries now
carry just the rule + a pointer; the full narrative moved to
`archive/lessons-history.md`, not deleted.

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

**Bonus 2:** Edit/Write file tools may TRUNCATE writes silently against this mount when the file is large — see "Writes to the C:\Projects Mount Are Not Safe" below. Full rewrite (`cat >`) is the only safe method; append (`cat >>`) also corrupts.

---

## Memory Drift on Substrate Names — Always Verify Before Describing

**Rule:** Before describing any substrate fact (table names, project IDs, file paths, schema), verify it live — through the relevant MCP or a fresh read — rather than trust memory. Memory is a draft, not a source.

Full incident (an assistant confidently misnamed a since-deleted Supabase table) → `archive/lessons-history.md`.

---

## Update Discipline Lapsed (2026-04-27)

**Rule:** A session log alone is not "updating the substrate." Every session that produces a decision, lesson, or status change needs an explicit update to the relevant pending/decisions/lessons file, not just its own log entry.

Full incident (17 of 30 files found stale by 15+ days on a since-retired Supabase-backed substrate) → `archive/lessons-history.md`.

---

## False-Implementation Pattern — Surface Signals Lie, Measurement Doesn't

**Rule:** After any change to eq-context, verify the actual committed content at its canonical location (today: fetch the raw GitHub URL and check for an expected marker) before claiming "done." A green terminal, a commit hash, or "I pushed it" are success-*shaped*, not success.

Full incident (three "implementation complete" claims in one session, all wrong on measurement) → `archive/lessons-history.md`.

---

## The Substrate Read Path Lied (2026-07-11) — F1

**Rule:** A substrate read from a cached URL (e.g. `raw.githubusercontent.com/.../main/`) can return **200 OK with 8–12-day-stale content** — no error, indistinguishable from a live read except by checking `last_updated` against the calendar. **If you have a local clone, the clone wins. Always.**

Canonical record + fix: `system/failures.md` → **F1**. Enforced at rung 4 by `hooks/session_start.py`. Full narrative → `archive/lessons-history.md`.

---

## Writes to the `C:\Projects` Mount Are Not Safe — Neither Edit/Write NOR Append (2026-07-11) — F2, F6

**This lesson cost us three times before it was enforced by a hook. Do not re-learn it by hand.**

| Method | Behaviour | Safe? |
|---|---|---|
| `Edit` / `Write` tool on a long file | **Silently TRUNCATES.** Reports success. | **NO** |
| `cat >> file << EOF` (append) | **NUL-FILLS.** File becomes binary. Reports success. | **NO** |
| `cat > file << EOF` (full rewrite) | Correct. | **YES** |

**Rule:** full rewrite only. Verify every write with `wc -l`, `tail -2`, **and a NUL scan** (`grep -c $'\x00'`) — a NUL-fill produces a *larger*, sane-looking line count; `wc -l` alone will not catch it.

Canonical record: `system/failures.md` → **F2**, **F6**. Enforced at rung 4 by `hooks/pre_tool_use.py`. Full narrative → `archive/lessons-history.md`.

---

## The Substrate Contained a Goal Nobody Owned (2026-07-11) — F3

**Rule:** treat **facts** and **goals** as different substances with different half-lives. A fact is machine-verifiable and re-checked by SQL. A goal is verifiable *only by the human who owns it*, has an expiry, and must never be inferred or written by an assistant. An unowned, undated goal in a critical file will steer every agent that reads it — and every recency-based check will report it as fine, because recency isn't truth.

Canonical record: `system/failures.md` → **F3**. `system/TODAY.md` carries its own telling of this incident (the file most likely to be read by an agent about to repeat it). Guard: `claim-expiry.yml` (rung 3, built 2026-07-12). Full narrative → `archive/lessons-history.md`.

---

## The First Guard I Wrote Failed Open, Silently (2026-07-11)

**Rule:** a guard that fails open without announcing it is worse than no guard at all — it manufactures the feeling of safety and delivers none of it. Every guard must answer *what do I do when I don't know?* — if the answer is "allow, quietly," it's decoration, not a guard. Never trust a guard you have not adversarially attacked.

Full incident (the first version of `pre_tool_use.py` silently let a 308-line edit through) → `hooks/README.md` "Why fail-closed", and `archive/lessons-history.md`.

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

**Note (2026-07-12):** `auto-bump-frontmatter.yml` — the bot referenced above — was itself retired 2026-07-12 (it was manufacturing false freshness; see `system/failures.md` F3). This entry is kept for the `core.hooksPath` gotcha, which remains true independent of that bot's removal. **Practical effect:** dates across the substrate are honest again post-retirement, so expect more files to show real, unmasked staleness at once than you'd have seen while the bot was faking freshness — that's the system working correctly, not new drift.

---

## Verify the Live System Before Building (2026-06-22)

**Rule:** Before writing any code, migration, or PR — query the actual live system. Do not trust docs, suite-state.md, session logs, or substrate files as a substitute for live verification. The failure mode (documented 2026-06-03) is: assume something is not built, build a parallel version, discover it already existed — wasted work and reverts.

**Checklist before any build task:**
1. `list_tables` on the relevant Supabase project (ehow: ehowgjardagevnrluult or eq-canonical: jvknxcmbtrfnxfrwfimn)
2. `git branch -a` + `git status` on the target repo
3. Check worktree-registry.md for in-flight work on a branch
4. Read suite-state.md for CI/deploy status

**Why it matters:** Substrate files lag reality. A 10-second Supabase query beats a wrong-premise build that takes two hours to undo.

---

## Substrate Lags Reality — and urjh Is Deleted (2026-06-22)

**Rule:** Substrate files (CLAUDE.md, suite-state.md, session logs, pending.md) always lag the live system. Treat substrate claims about DB schema, applied migrations, deployed versions, and key/secret status as leads to verify — not facts.

**Critical dead reference:** Supabase project `urjhmkhbgaxrofurpbgc` (urjh / eq-solves-service-dev) was DELETED 2026-06-22. Any reference to it as a live project in substrate files is stale. Do not query it, do not reference it as a data store, do not deploy edge functions to it. The sole live DB for EQ Service and EQ Field is ehow (`ehowgjardagevnrluult`).

**The substrate itself is on GitHub:** The eq-context substrate is served via GitHub raw CDN (https://raw.githubusercontent.com/eq-solutions/eq-context/main/<path>). There is no Supabase cache, no edge function, no context_files table. These were all retired when urjh was deleted.
