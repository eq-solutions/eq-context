#!/usr/bin/env node
'use strict';

// eq-guard — PreToolUse guardrails for the agent runtime.
// One dispatcher, all rules. Reads the hook JSON on stdin, inspects the
// pending tool call, and either lets it through, records a warning, or
// (in block mode) denies it. Spec: system/operating-model-roadmap.md.
//
// Modes & unlocks (environment variables):
//   EQ_GUARD_MODE   warn | block        default: warn  (warn = record only, never block)
//   EQ_GUARD_OFF    1                   disable every rule
//   EQ_ALLOW_DEPLOY 1                   bypass gate-outbound (push/deploy/commit)
//   EQ_ALLOW_SQL    1                   bypass gate-sql (write/DDL SQL)
//   EQ_ALLOW_SKS_LIVE 1                 bypass block-sks-live
//   EQ_COWORK       1                   engage block-cowork-git (set in the Cowork sandbox only)
//
// Fail-open by design: any internal error logs and allows. A broken guard
// must never brick a session. Decisions are appended to guard.log beside
// this script.

const fs = require('fs');
const path = require('path');
const os = require('os');

const LOG = path.join(__dirname, 'guard.log');
const MODE = ((process.env.EQ_GUARD_MODE || 'warn').toLowerCase() === 'block') ? 'block' : 'warn';
const truthy = v => /^(1|true|yes|on)$/i.test(v || '');

// Git-Bash (MSYS) paths aren't real Windows paths -- Node's fs calls run
// natively on Windows and know nothing about MSYS mounts. Two styles seen
// live: a drive-letter path (/c/Projects/... -> C:/Projects/..., handled
// since 2026-08-05) and the /tmp mount, which MSYS maps to the Windows TEMP
// directory -- the same place os.tmpdir() resolves to. Confirmed live
// 2026-08-17: a real `git worktree add <path> origin/main` under /tmp
// produced a genuine .git gitdir-pointer file, but detect-fake-worktree
// (1b/1c below) still reported no .git, because fs.existsSync('/tmp/x/.git')
// resolves against Windows' own filesystem root, not MSYS's /tmp -- an
// ENOENT on a path that was never real to Node to begin with, not a signal
// the worktree is fake. One shared helper so a third mount style only needs
// fixing here, not at every callsite.
function normalizeMsysPath(p) {
  const norm = p.replace(/\\/g, '/');
  const driveM = norm.match(/^\/([A-Za-z])(\/.*|$)/);
  if (driveM) return `${driveM[1].toUpperCase()}:${driveM[2] || '/'}`;
  if (norm === '/tmp' || norm.startsWith('/tmp/')) {
    return path.join(os.tmpdir(), norm.slice(4)).replace(/\\/g, '/');
  }
  return norm;
}

function log(line) { try { fs.appendFileSync(LOG, line + '\n'); } catch (_) { /* ignore */ } }
function firstLine(s) { return String(s || '').split('\n')[0].slice(0, 160); }

function allow() { process.exit(0); }                 // empty stdout -> normal permission flow
function deny(reason) {
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      permissionDecision: 'deny',
      permissionDecisionReason: reason
    }
  }));
  process.exit(0);
}

function fileContent(input) {
  const parts = [];
  if (typeof input.content === 'string') parts.push(input.content);
  if (typeof input.new_string === 'string') parts.push(input.new_string);
  if (typeof input.new_source === 'string') parts.push(input.new_source);
  if (Array.isArray(input.edits)) for (const e of input.edits) if (e && typeof e.new_string === 'string') parts.push(e.new_string);
  return parts.join('\n');
}

function evaluate(data) {
  const tool = data.tool_name || '';
  const input = data.tool_input || {};
  const cwd = data.cwd || process.cwd() || '';
  const fileTools = ['Edit', 'Write', 'NotebookEdit', 'MultiEdit'];
  const isFile = fileTools.includes(tool);
  const isShell = tool === 'Bash' || tool === 'PowerShell';
  const isMcpSql = /__(execute_sql|execute-sql|apply_migration)$/.test(tool);
  const filePath = input.file_path || input.notebook_path || '';
  const cmd = isShell ? String(input.command || '') : '';
  const v = [];

  // 1. block-worktree-write — editing a worktree you're not working in
  if (isFile && filePath) {
    // Normalize a Git-Bash-style absolute path's fake drive segment (/c/... ->
    // c:/...) before comparing -- same class of bug fixed in 1b/1c below: without
    // it, a legitimate same-worktree edit reported in one path style against a
    // cwd reported in the other never satisfies fp.startsWith(c) even though
    // they're the identical location, and a legitimate edit gets flagged as a
    // foreign worktree write. Not observed live (guard.log shows filePath/cwd
    // are always Windows-style together in every real session logged) but
    // nothing guaranteed that stays true. (fixed 2026-08-05, see 1b/1c)
    const toDriveForm = s => { const m = s.match(/^\/([a-z])(\/.*|$)/); return m ? `${m[1]}:${m[2] || '/'}` : s; };
    const fp = toDriveForm(filePath.replace(/\\/g, '/').toLowerCase());
    const c = toDriveForm(cwd.replace(/\\/g, '/').toLowerCase());
    // Second alternative widened 2026-09-08 -- see rule 10's stale-main-gate
    // fix below for the audit finding (system/failures.md F16): <repo>-wt-
    // <topic> infix is the dominant live worktree-naming convention, not
    // just a trailing -wt suffix. Unlike rule 10, this rule has no git-dir
    // fallback -- a naming miss here isn't a performance nit, it's a real
    // foreign-worktree write sailing through completely undetected.
    const inWt = /\/worktrees\/[^/]+/.test(fp) || /[^/]*-wt(-[^/]*)?(\/|$)/.test(fp);
    if (inWt && c && !fp.startsWith(c)) {
      v.push({ rule: 'block-worktree-write', blockable: true, unlocked: false,
        reason: `write into a worktree you are not in: ${filePath}` });
    }
  }

  // 1b. detect-fake-worktree — editing inside a path that LOOKS like an
  // isolated git worktree (matches /worktrees/<name>/ or <name>-wt/) but has
  // no .git of its own. Root cause of repeated eq-solves-service session
  // collisions (2026-07-22/23): a real linked worktree has its own .git FILE
  // (a gitdir pointer, ~70 bytes) at its root — e.g. eqsvc-loadtime-ux. Some
  // session-assigned "worktree" folders were never actually created via
  // `git worktree add` and are just plain nested subdirectories (confirmed:
  // asset-import-export-1fe110, unruffled-noyce-657c65 — zero .git of their
  // own). Any git command run from inside one of these walks up to the
  // PARENT repo's .git and mutates ITS shared branch/working tree. Two
  // sessions each believing they're isolated then collide on the same
  // checkout: one sees the other's uncommitted edits appear, or the checked-
  // out branch changes under them mid-task. This does not fire on the Bash
  // tool, so running `git worktree add <path> <branch>` to fix a path is
  // never blocked — only direct file edits into an unfixed fake worktree are.
  if (isFile && filePath) {
    // Normalize before splitting -- see normalizeMsysPath() above. file_path is
    // conventionally Windows-style in this environment so the drive-letter case
    // was latent rather than observed live, but nothing guarantees a caller
    // won't pass a Unix-style one. (fixed 2026-08-05, /tmp case fixed 2026-08-17)
    const normPath = normalizeMsysPath(filePath);
    const isAbs = normPath.startsWith('/');
    const segs = normPath.split('/').filter(Boolean);
    let wtRoot = null;
    for (let i = 0; i < segs.length; i++) {
      if (segs[i].toLowerCase() === 'worktrees' && segs[i + 1]) { wtRoot = (isAbs ? '/' : '') + segs.slice(0, i + 2).join('/'); break; }
      // Widened 2026-09-08 to also match the <repo>-wt-<topic> infix shape
      // (segs[i] has no '/', so the whole-segment intent is the same as
      // rule 1's `-wt(-[^/]*)?` above -- see that comment for why).
      if (/-wt(-.*)?$/i.test(segs[i])) { wtRoot = (isAbs ? '/' : '') + segs.slice(0, i + 1).join('/'); break; }
    }
    if (wtRoot) {
      let hasGit = true; // fail open: an fs error should never block
      try { hasGit = fs.existsSync(wtRoot + '/.git'); } catch (_) { hasGit = true; }
      if (!hasGit) {
        v.push({ rule: 'detect-fake-worktree', blockable: true, unlocked: false, force: true,
          reason: `"${wtRoot}" looks like an isolated worktree but has no .git of its own — it's a plain folder silently sharing the PARENT repo's working tree and branch, which is exactly how concurrent sessions collide. Run "git worktree add <path> <branch>" to give it a real, isolated .git before editing here, or work from a path that already has one.` });
      }
    }
  }

  // 1c. detect-fake-worktree (shell case, added 2026-08-05) — same shape as 1b
  // above, but for git commands run via Bash/PowerShell. 1b only ever fires on
  // isFile, so `git commit`/`git rebase`/etc. run from inside an unfixed fake
  // worktree sailed through unchecked even though this file already knows how
  // to detect the exact shape. Reuses rule 9's own cwd-resolution precedent
  // below (data.cwd stays pinned to session start, doesn't follow an
  // in-command cd/-C) rather than trusting cwd alone.
  //
  // Originally had its own inline cd/-C regex here instead of calling
  // resolveEffCwd() (defined below, but hoisted -- same function scope).
  // Two bugs from that duplication, found in the 2026-08-17 sweep that fixed
  // resolveEffCwd() itself: (a) cmd.match() with no /g on `-C` took the FIRST
  // occurrence, not the last, same "first not last" bug as rule 9/10 had; (b)
  // the cd regex was anchored `^\s*cd` with no chain-boundary alternation at
  // all, so it only matched a cd at the TRUE START of the whole command --
  // strictly narrower than even resolveEffCwd()'s pre-fix version, meaning any
  // cd chained after an earlier command (`cd "<repo>" && cd "<scratch>" && git
  // ...`, this hook's own recommended worktree-clone pattern) was invisible to
  // it and silently fell back to the stale session-start cwd. Now delegates to
  // the one shared, already-correct implementation instead of a second
  // hand-rolled copy that can drift out of sync with it again.
  if (isShell && /\bgit\b/.test(cmd)) {
    const effCwd1c = resolveEffCwd(cmd, cwd);
    // Normalize before splitting -- see normalizeMsysPath() above.
    // Confirmed live 2026-08-05: a Git-Bash-style cd target (/c/Projects/...,
    // exactly what the Bash tool's own system prompt tells callers to use)
    // false-positived on every legitimate worktree, because .filter(Boolean)
    // silently dropped the leading empty segment from the leading /, and the
    // resulting relative-looking path ("c/Projects/...") got checked against
    // the hook process's own cwd instead of the real worktree location.
    // Confirmed live again 2026-08-17, same shape, different mount: a /tmp
    // cwd (the Bash tool's own pwd for a worktree created under the OS temp
    // dir) resolved against Windows' real filesystem instead of MSYS's /tmp.
    const normCwd1c = normalizeMsysPath(effCwd1c);
    const isAbs1c = normCwd1c.startsWith('/');
    const segs1c = normCwd1c.split('/').filter(Boolean);
    let wtRoot1c = null;
    for (let i = 0; i < segs1c.length; i++) {
      if (segs1c[i].toLowerCase() === 'worktrees' && segs1c[i + 1]) { wtRoot1c = (isAbs1c ? '/' : '') + segs1c.slice(0, i + 2).join('/'); break; }
      // Same infix widening as rule 1b above.
      if (/-wt(-.*)?$/i.test(segs1c[i])) { wtRoot1c = (isAbs1c ? '/' : '') + segs1c.slice(0, i + 1).join('/'); break; }
    }
    if (wtRoot1c) {
      // If THIS SAME command is itself creating this worktree via `git
      // worktree add ... <target>`, checking for its .git now is premature,
      // not evidence of a fake worktree -- the add hasn't run yet at
      // evaluation time (this hook runs before any of the chain executes).
      // Confirmed live 2026-08-21: `cd A && git worktree add --detach
      // ../foo-wt <ref> && ... && cd ../foo-wt && git status` -- the LAST-cd
      // fix above correctly finds the `cd ../foo-wt` at the END of the chain
      // (added so the caller can keep working inside the just-created
      // worktree), but that's the SAME target the earlier `git worktree add`
      // in the same string is still in the middle of creating. resolveEffCwd
      // then resolved that relative target against data.cwd (session-start
      // cwd, not the clone dir the chain actually `cd`'d into first) and
      // landed on a path that was never real -- compounding, but the fix
      // below closes the case regardless of which base it lands on: it
      // doesn't matter WHERE the check thinks the target is, only whether
      // this command is provably the one creating it.
      //
      // Narrow fix: exempt only when a `git worktree add` invocation in this
      // exact command targets the same basename -- derived from wtRoot1c
      // itself (not segs1c's tail), since cwd can legitimately have more
      // segments after the worktree root (a subdirectory inside it). An
      // unrelated pre-existing fake worktree mentioned nowhere near a
      // `worktree add` still blocks (see selftest.js).
      const wtBase1c = wtRoot1c.split('/').filter(Boolean).pop() || '';
      const escBase1c = wtBase1c.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const addingThisWt = escBase1c && new RegExp('git\\s+worktree\\s+add\\b[^&|;\\n]*\\b' + escBase1c + '\\b').test(cmd);
      let hasGit1c = true; // fail open: an fs error should never block
      if (!addingThisWt) {
        try { hasGit1c = fs.existsSync(wtRoot1c + '/.git'); } catch (_) { hasGit1c = true; }
      }
      if (!hasGit1c) {
        v.push({ rule: 'detect-fake-worktree', blockable: true, unlocked: false, force: true,
          reason: `"${wtRoot1c}" looks like an isolated worktree but has no .git of its own — running git here walks up to the PARENT repo's .git and mutates ITS shared branch/working tree, exactly how concurrent sessions collide. Run "git worktree add <path> <branch>" to give it a real, isolated .git first, or run this from a path that already has one.` });
      }
    }
  }

  // 2. scan-secrets — hardcoded credentials in written content
  if (isFile) {
    const content = fileContent(input);
    const pats = [
      [/\bsk-[A-Za-z0-9]{20,}\b/, 'API key (sk-…)', true],
      [/\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]+/, 'JWT', true],
      [/\bAKIA[0-9A-Z]{16}\b/, 'AWS access key', true],
      [/(api[_-]?key|secret|token|password|passwd)\s*[:=]\s*['"][^'"\s]{12,}['"]/i, 'inline credential assignment', false]
    ];
    for (const [re, label, force] of pats) {
      if (re.test(content)) {
        v.push({ rule: 'scan-secrets', blockable: true, unlocked: false, force,
          reason: `possible hardcoded secret (${label}) in ${filePath || 'content'}` });
        break;
      }
    }
  }

  // 3. lint-client-names — real client names in non-substrate outputs (warn-only always)
  if (isFile) {
    const isSubstrate = /eq-context/i.test(filePath) || /eq-context/i.test(cwd);
    if (!isSubstrate) {
      const content = fileContent(input);
      const hits = ['Equinix', 'AirTrunk'].filter(n => new RegExp('\\b' + n + '\\b', 'i').test(content));
      if (hits.length) {
        v.push({ rule: 'lint-client-names', blockable: false, unlocked: false,
          reason: `real client name(s) in output: ${hits.join(', ')} — use "Data Centre Client A"` });
      }
    }
  }

  // 4. gate-outbound — push / deploy / commit without an explicit unlock
  if (isShell) {
    const re = /\bgit\s+push\b|\bgit\s+commit\b|\bnetlify\s+deploy\b|\bnpx\s+netlify\s+deploy\b|\bsupabase\s+(db\s+push|deploy|link)\b/i;
    if (re.test(cmd)) {
      v.push({ rule: 'gate-outbound', blockable: true, unlocked: truthy(process.env.EQ_ALLOW_DEPLOY),
        reason: `outbound/publish command: ${firstLine(cmd)}` });
    }
  }

  // 5. block-sks-live — anything referencing the SKS live Supabase project
  if (isShell || isMcpSql) {
    const blob = isShell ? cmd : JSON.stringify(input);
    if (/nspbmirochztcjijmcrx/i.test(blob)) {
      v.push({ rule: 'block-sks-live', blockable: true, unlocked: truthy(process.env.EQ_ALLOW_SKS_LIVE), force: true,
        reason: 'references SKS live Supabase project (nspbmirochztcjijmcrx)' });
    }
  }

  // 6. gate-sql — write / DDL SQL without an explicit unlock
  const ddl = /\b(insert|update|delete|drop|alter|truncate|grant|revoke)\b/i;
  if (isMcpSql) {
    const sqlText = String(input.query || input.sql || JSON.stringify(input));
    if (ddl.test(sqlText) || /\bcreate\s+(table|schema|policy|function|index)\b/i.test(sqlText)) {
      v.push({ rule: 'gate-sql', blockable: true, unlocked: truthy(process.env.EQ_ALLOW_SQL),
        reason: `write/DDL SQL: ${firstLine(sqlText)}` });
    }
  } else if (isShell && /\bpsql\b|execute_sql/.test(cmd) && ddl.test(cmd)) {
    v.push({ rule: 'gate-sql', blockable: true, unlocked: truthy(process.env.EQ_ALLOW_SQL),
      reason: `write SQL via shell: ${firstLine(cmd)}` });
  }

  // 7. block-cowork-git — git from the Cowork sandbox against C:\Projects
  if (isShell && truthy(process.env.EQ_COWORK)) {
    if (/^\s*git\b/.test(cmd) && /projects/i.test(cwd)) {
      v.push({ rule: 'block-cowork-git', blockable: true, unlocked: false,
        reason: 'git from the Cowork sandbox against C:\\Projects — emit a .bat/.ps1 for the host to run instead' });
    }
  }

  // 8. brief-gate — require /brief to have run today before the first file edit.
  // Unlock with EQ_SKIP_BRIEF=1 for quick one-off sessions.
  //
  // Scope: the gate exists to force the Session Gate (Rule 0.6) before BUILDING —
  // editing product code / schema where wrong-premise work is costly. It must NOT
  // fire on edits that aren't building, or it just trains the touch-the-flag bypass
  // (which then erodes the gate where it matters). Exempt three classes:
  //   • ~/.claude/**            — user skills, hooks, settings, memory (config, not building)
  //   • eq-context recording    — pending.md / pending-archive.md / pending/<repo>.md /
  //                               sessions/ / changelog/ (housekeeping; /close writes
  //                               these at session END, when no brief is owed)
  //   • scratchpad / temp       — throwaway working files
  // Everything else under a project repo (incl. eq-context *code*: scripts, workflows,
  // migrations) stays gated.
  if (isFile && filePath) {
    const fp = filePath.replace(/\\/g, '/').toLowerCase();
    // Broadened 2026-08-06 — .includes('/eq-context/') requires an exact bounded
    // path segment, so it never matched any eq-context WORKTREE (every one of
    // this repo's own worktrees is named eq-context-<slug>-wt, per convention) —
    // the substrate-doc exemption below silently never applied inside a worktree,
    // guaranteeing a brief-gate false-block on the very "/close via isolated
    // worktree" pattern this repo's own memory/practice recommends for safety.
    // Confirmed live: only masked by an already-set brief flag from an earlier
    // /brief in the same session; broke as soon as that flag was cleared.
    // Applied 2026-08-06 with Royce's explicit go, after the classifier
    // correctly blocked an earlier unprompted attempt at this same edit.
    const inEqContext = /\/eq-context(-[^/]*)?\//.test(fp);
    const exempt =
      fp.includes('/users/eq/.claude/') ||
      // pending.md and pending-archive.md are the same housekeeping class — the archive
      // rule (pending.md's own instructions + /close Step 2) moves fully-closed sections
      // from one into the other as part of the SAME close pass, so gating one and not the
      // other just reproduces the touch-the-flag bypass this exemption exists to avoid.
      // (fixed 2026-07-28 — pending-archive.md was missed when this exemption was scoped)
      //
      // fp.includes('/pending/') added 2026-08-17: eq/pending.md was split into
      // eq/pending/<repo>.md (one file per repo, mirroring eq/changelog/<repo>.md —
      // see that commit's own scope note in eq/pending.md). The exact-suffix regex
      // above only ever matched the flat pending.md/pending-archive.md filenames, so
      // every per-repo file under the new eq/pending/ subdirectory started blocking
      // the moment this shipped — confirmed live same-session: an edit to
      // eq/pending/eq-solves-intake.md was blocked with "brief not run this
      // session" while the same-session eq/changelog/eq-intake.md edit sailed
      // through ungated, and the pending/ edit only succeeded while an unrelated
      // /close-run brief flag was still active — it re-blocked the instant that
      // flag cleared. Matched by substring, same as /sessions/ and /changelog/
      // above, not by a narrower exact-suffix regex, so it doesn't need a fourth
      // fix if the per-repo files ever get their own further split.
      (inEqContext && (/\/pending(-archive)?\.md$/.test(fp) || /\/suite-state\.md$/.test(fp) || fp.includes('/sessions/') || fp.includes('/changelog/') || fp.includes('/pending/'))) ||
      fp.includes('/appdata/local/temp/') ||
      fp.includes('/scratchpad/');
    if (!exempt) {
      // Per-SESSION flag, not per-day-global. The global file was shared state across
      // every concurrent session on this machine: one session's /close deleted it and
      // silently re-blocked every other live session mid-work, while one session's
      // /brief waived the gate for sessions that never ran one. Both directions were
      // wrong, and the observed workaround was inline `touch`ing the flag — the exact
      // bypass the scope comment above warns erodes the gate. (fixed 2026-07-21)
      const sid = String(data.session_id || '').replace(/[^A-Za-z0-9-]/g, '');
      let flagFile;
      if (sid) {
        // No date component (fixed 2026-09-15, system/failures.md). Used to be
        // eq-brief-<LOCAL-DATE>-<sid>.flag, with <LOCAL-DATE> recomputed via `new
        // Date()` fresh on EVERY call, not pinned to session start. A session that
        // ran /brief before local midnight and made its first edit after it wrote a
        // flag dated yesterday while this check looked for today's -- blocked again,
        // mid-session, despite having genuinely briefed. Confirmed live 2026-09-15
        // (session aa21d298-ed51-4e00-a5d4-adad5cf8fcca): flag written 2026-09-14
        // 21:09 local, a Write blocked 2026-09-15 04:20 local with this exact reason,
        // forcing a manual re-write under the new date to unblock. sid (a GUID)
        // already scopes the flag to exactly one session -- that's what the
        // 2026-07-21 fix above secured -- so the date bought nothing a session id
        // doesn't already give, and nothing here or in brief.md/close.md relies on
        // it for cleanup or any other purpose (Temp still holds undated- AND
        // dated-format flags going back weeks; nothing has ever swept either).
        // Dropping it removes the whole bug class instead of special-casing
        // "yesterday or today". brief.md's own flag-write and close.md's own
        // flag-clear must both match this exactly -- see those files.
        flagFile = `C:/Users/EQ/AppData/Local/Temp/eq-brief-${sid}.flag`;
      } else {
        // No session_id (older harness / direct invocation) => fall back to the
        // legacy global, date-keyed flag rather than hard-blocking on a name that
        // nothing can write -- this path has no session id to scope to, so LOCAL
        // date (not UTC) is the only scoping available. Must match how /brief
        // writes it (PowerShell `Get-Date -Format yyyy-MM-dd`, local) -- UTC here
        // spuriously blocked every edit for the first hours after local midnight in
        // ahead-of-UTC zones (AEST): the flag landed under the local date while the
        // gate looked for the UTC one. (fixed 2026-07-12). Deliberately NOT
        // de-dated the way the sid branch above was: with no session id, a date is
        // the only isolation this path has at all, and removing it would silently
        // reintroduce the exact cross-session leak the 2026-07-21 fix closed --
        // narrower, session-id-less problem, not in scope for the 2026-09-15 fix.
        const now = new Date();
        const today = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
        flagFile = `C:/Users/EQ/AppData/Local/Temp/eq-brief-${today}.flag`;
      }
      const briefRan = fs.existsSync(flagFile);
      if (!briefRan) {
        v.push({ rule: 'brief-gate', blockable: true, unlocked: truthy(process.env.EQ_SKIP_BRIEF), force: true,
          reason: `brief not run this session — type /brief <repo> first (or set EQ_SKIP_BRIEF=1 to skip) [session ${sid || 'unknown'}]` });
      }
    }
  }

  // Shared by rule 9 (reflection-gate) and rule 10 (stale-main-gate): resolve
  // the directory a git-commit command actually targets. `git -C <path>` is
  // matched unanchored (safe -- `-C` is git's own flag, can appear anywhere).
  // `cd <path>` is only trustworthy right at a command boundary -- start of
  // string, or just after a line break / `;` / `&&` / `||` / `&` / `|` --
  // because a bare `^` with no `m` flag matches ONLY the start of the entire
  // string, not the start of each line. That silently broke on a real
  // multi-line invocation:
  //   CLOSE="C:/some/path"
  //   cd "$CLOSE" && git commit -m "..."
  // (string doesn't start with "cd", so the old anchored regex never matched
  // at all) and fell through to data.cwd, which is documented below as NOT
  // following an in-command cd -- confirmed live 2026-08-14 as a false
  // stale-main-gate block on a fully isolated clone that was 0 commits behind.
  // Falls back to the tool-reported cwd only when neither pattern is found.
  //
  // Second occurrence of the same bug class, confirmed live 2026-08-17: a
  // chain can legitimately `cd` MORE THAN ONCE before the trailing git
  // command -- e.g. `cd "<repo>" && SCRATCH="<scratch-clone-path>" && cd
  // "$SCRATCH" && git commit ...`, a real shape this environment produces
  // when a session cd's into a named repo for context, then into an isolated
  // scratch clone before actually committing. `cmd.match()` with no `/g` flag
  // only ever returns the FIRST occurrence in the string, so the later, real
  // cd into the isolated clone was silently ignored in favour of the earlier,
  // unrelated one -- guard.log shows 6 consecutive stale-main-gate blocks all
  // reporting the SAME "1 commit(s) behind", matching the first-cd'd repo's
  // own genuinely-behind state, not the isolated (and current) scratch clone
  // the commit actually ran in. Fixed by scanning every cd in the chain and
  // taking the LAST one -- the same fix pre_tool_use.py's _CD_CHAIN_RE already
  // applies for the identical shape (a later cd overrides an earlier one).
  //
  // Third occurrence of the same bug class, confirmed live 2026-08-20: the
  // captured cd/-C target can be RELATIVE (`cd .claude/worktrees/foo && git
  // commit ...`) and was being returned as-is. Every downstream consumer
  // then resolved that relative string against the GUARD PROCESS's own cwd
  // instead of the tool call's -- fs.existsSync in 1c false-positived
  // detect-fake-worktree on a real, properly `git worktree add`-created
  // worktree (confirmed via `git worktree list` + a direct .git gitdir-
  // pointer read); the same relative string handed to rules 9/10's execSync
  // `cwd` option would have silently failed open instead (ENOENT -> caught
  // -> gate skipped), the opposite failure mode but the same root cause.
  // Same fix shape as normalizeMsysPath() above for the other two non-native
  // path forms this function's return value flows into: resolve against the
  // caller-supplied cwd before returning, and only when the target isn't
  // already absolute (an MSYS-style /c/... target already has a root as far
  // as path.isAbsolute() is concerned -- normalizeMsysPath() downstream is
  // still what turns that into a real Windows path; this fix only closes the
  // truly-relative case).
  function resolveEffCwd(cmd, cwd) {
    let m = cmd.match(/git\s+-C\s+"([^"]+)"/) || cmd.match(/git\s+-C\s+(\S+)/);
    if (!m) {
      const cdRe = /(?:^|[\r\n;&|])\s*cd\s+(?:"([^"]+)"|(\S+))/g;
      let match, last = null;
      while ((match = cdRe.exec(cmd)) !== null) last = match;
      if (last) m = [null, last[1] !== undefined ? last[1] : last[2]];
    }
    if (!m) return cwd;
    const target = m[1];
    return path.isAbsolute(target) ? target : path.resolve(cwd, target);
  }

  // 9. reflection-gate -- require a paired docs/reflection-log.md entry before
  // committing in eq-field. Spec: eq-context rules/reflection-protocol.md.
  // Fires at COMMIT (not every Edit) so it lands once per shipped change, at
  // the last checkpoint before the decision is final, not on every WIP edit.
  //
  // Does NOT trust data.cwd alone -- confirmed live 2026-07-26 that this
  // session's reported cwd stays pinned to wherever the session started and
  // does not follow an in-command cd, so cwd-only detection silently missed
  // a real eq-field commit run as: cd "<path>" && git commit ...
  // (the actual pattern every git command in this environment uses, per
  // guard.log). Parses the command string for cd "<path>" / git -C <path>
  // first and only falls back to data.cwd if neither is present.
  //
  // Unlock with EQ_SKIP_REFLECT=1.
  // Trigger tolerates an intervening -C <path> between "git" and "commit" --
  // confirmed live 2026-07-26 that `git -C "<path>" commit ...` (the actual
  // most-used invocation here, since the Bash tool discourages cd) slipped
  // through entirely unblocked: the old /\bgit\s+commit\b/ trigger requires
  // "git" and "commit" separated by whitespace ONLY, so anything between them
  // (like -C "<path>") skipped evaluation before the cwd-parsing code below
  // ever ran.
  const gitCommitRe = /\bgit\s+(?:-C\s+(?:"[^"]+"|\S+)\s+)?commit\b/;
  if (isShell && gitCommitRe.test(cmd)) {
    let effCwd = resolveEffCwd(cmd, cwd);
    const cwdNorm = effCwd.replace(/\\/g, '/').toLowerCase();
    const inEqField = /\/eq-field(\/|-[a-z0-9-]*)?(\/|$)/.test(cwdNorm);
    if (inEqField) {
      let staged = null;
      try {
        const { execSync } = require('child_process');
        staged = execSync('git diff --cached --name-only', { cwd: effCwd, encoding: 'utf8' })
          .split('\n').map(s => s.trim().replace(/\\/g, '/').toLowerCase()).filter(Boolean);
      } catch (_) { staged = null; }
      if (staged && staged.length && !staged.includes('docs/reflection-log.md')) {
        v.push({ rule: 'reflection-gate', blockable: true, unlocked: truthy(process.env.EQ_SKIP_REFLECT), force: true,
          reason: 'committing in eq-field without a paired docs/reflection-log.md entry in the same commit -- run /reflect first (or set EQ_SKIP_REFLECT=1 to skip)' });
      }
    }
  }
  // 10. stale-main-gate — block a commit directly on a shared checkout's
  // `main`/`master` when local HEAD is behind its upstream. Root cause of the
  // eq-context / eq-shell "concurrent sessions fork main" collisions confirmed
  // live 2026-08-08/09 (independent sessions committing directly on the same
  // non-worktree root checkout without syncing first; one recovery found a
  // silent rebase-abort had already dropped a session's own uncommitted work).
  // Structural guard per rules/agentic-coding.md §3 ("prefer a structural
  // guard over a documented rule") backing the worktree-isolation guidance
  // added there the same day.
  //
  // Does a real `git fetch` (not just the last-known remote-tracking ref) --
  // tested against a throwaway local+remote pair before wiring this in: a
  // second session's push is invisible to `git rev-list HEAD..@{upstream}`
  // until fetched, so skipping the fetch would silently defeat the one case
  // this rule exists for. Scoped narrowly (only direct git-commit on
  // main/master, outside any worktree) specifically so this network cost is
  // paid only by the risky pattern being discouraged, not by every commit
  // everywhere -- worktree-based commits (the common case) never reach this
  // branch. 5s fetch timeout; any failure (offline, slow remote, no upstream)
  // fails open per this file's own design principle -- a flaky network check
  // must never brick a session.
  //
  // Unlock with EQ_SKIP_STALE_MAIN=1 for a deliberate one-off.
  if (isShell && gitCommitRe.test(cmd)) {
    let effCwd10 = resolveEffCwd(cmd, cwd);
    const cwdNorm10 = effCwd10.replace(/\\/g, '/').toLowerCase();
    // Fast path: known naming conventions (no subprocess). Falls through to a
    // real git check below for a worktree created somewhere else (e.g. a
    // session's scratchpad dir) that this naming heuristic can't see.
    //
    // Second alternative widened 2026-09-08 to also match the <repo>-wt-<topic>
    // INFIX shape (e.g. eq-context-wt-f9-worktree-isolation), not just a
    // trailing -wt suffix -- eq-context's own worktree-registry audit found
    // infix is the DOMINANT live naming convention across the suite (7 folders
    // vs 1-2 suffix-style; system/failures.md F16), so the old suffix-only
    // pattern silently missed most real worktrees on this fast path. Mirrors
    // the broader `/eq-context(-[^/]*)?\//` shape already used for the same
    // purpose elsewhere in this file (brief-gate, above). Does not change
    // correctness for a miss -- the git-dir/git-common-dir fallback right
    // below already catches any real worktree this heuristic doesn't name-
    // match -- but it does matter when that fallback itself can't run (git
    // missing, timeout, any other execSync failure), where the heuristic's
    // result is all that's left.
    let inWorktree10 = /\/worktrees\/[^/]+/.test(cwdNorm10) || /[^/]*-wt(-[^/]*)?(\/|$)/.test(cwdNorm10);
    if (!inWorktree10) {
      try {
        const { execSync: execSyncWt } = require('child_process');
        // --git-dir and --git-common-dir diverge in a linked worktree
        // (git-dir -> .git/worktrees/<name>, git-common-dir -> the main
        // repo's real .git) and are identical everywhere else -- true
        // regardless of where the worktree lives or what it's named.
        const out10 = execSyncWt('git rev-parse --git-dir --git-common-dir',
          { cwd: effCwd10, encoding: 'utf8', timeout: 5000, stdio: ['pipe', 'pipe', 'ignore'] }).trim().split('\n');
        if (out10.length >= 2) {
          const path10 = require('path');
          inWorktree10 = path10.resolve(effCwd10, out10[0].trim()) !== path10.resolve(effCwd10, out10[1].trim());
        }
      } catch (_) { /* not a git repo, git missing, etc -- keep the path-heuristic result */ }
    }
    if (!inWorktree10) {
      try {
        const { execSync } = require('child_process');
        const opts = { cwd: effCwd10, encoding: 'utf8', timeout: 5000, stdio: ['pipe', 'pipe', 'ignore'] };
        const branch = execSync('git rev-parse --abbrev-ref HEAD', opts).trim();
        if (branch === 'main' || branch === 'master') {
          const upstream = execSync('git rev-parse --abbrev-ref --symbolic-full-name @{upstream}', opts).trim();
          if (upstream) {
            const remote = upstream.split('/')[0];
            execSync(`git fetch ${remote} ${branch} --quiet`, opts);
            const behind = parseInt(execSync(`git rev-list --count HEAD..${upstream}`, opts).trim(), 10);
            if (behind > 0) {
              v.push({ rule: 'stale-main-gate', blockable: true, unlocked: truthy(process.env.EQ_SKIP_STALE_MAIN), force: true,
                reason: `committing directly on "${branch}" while ${behind} commit(s) behind ${upstream} -- fetch + rebase first, or isolate in a worktree ("git worktree add <path> ${upstream}") and commit/push from there instead. This is the exact shared-root-checkout fork pattern that already cost real recovery time this week (EQ_SKIP_STALE_MAIN=1 to override deliberately).` });
            }
          }
        }
      } catch (_) { /* no upstream, offline, not a git repo, or git error -- fail open */ }
    }
  }

  // 11. warn-untracked-migrations -- eq-field hand-applies Supabase migrations via
  // the Supabase MCP; this repo has no CI path that applies supabase/migrations/*.sql
  // (confirmed: no workflow in .github/workflows touches that directory). Twice now a
  // migration got applied live and then sat as an untracked file in the shared
  // checkout for a full day before anyone noticed and committed it -- one file's own
  // "DRAFT -- NOT APPLIED" header comment was still there a day after it had actually
  // gone live, because nothing revisited the file after the hand-apply (eq-context
  // memory migrations-applied-uncommitted; eq-field PR #764).
  //
  // Always warn-only (blockable: false -- never enters the blockers filter regardless
  // of MODE, stronger than force:false since MODE=block can't flip it either). This
  // hook cannot call the Supabase MCP's list_migrations tool to tell
  // applied-but-uncommitted apart from genuinely-still-draft -- MCP tools are called
  // by the agent loop, not by a detached hook subprocess -- and an untracked migration
  // file is not inherently wrong; normal mid-draft work looks identical from here.
  // That classification is /brief's job (Step 3.5, eq-field only, ~/.claude/commands/
  // brief.md). This rule exists only so the raw fact surfaces even when a session
  // skips /brief (EQ_SKIP_BRIEF=1) or hand-applies a migration mid-session, after
  // brief already ran clean earlier in the same session.
  //
  // Fires at commit time (same resolveEffCwd + inEqField pattern as rule 9) rather
  // than on every edit -- that's the natural checkpoint where a forgotten file is
  // cheapest to fold into the same commit, and matches this file's existing
  // convention of paying a git-subprocess cost only at commit time, not on the isFile
  // hot path (rule 8 deliberately stays fs.existsSync-only for exactly that reason).
  if (isShell && gitCommitRe.test(cmd)) {
    let effCwd11 = resolveEffCwd(cmd, cwd);
    const cwdNorm11 = effCwd11.replace(/\\/g, '/').toLowerCase();
    const inEqField11 = /\/eq-field(\/|-[a-z0-9-]*)?(\/|$)/.test(cwdNorm11);
    if (inEqField11) {
      try {
        const { execSync: execSyncMig } = require('child_process');
        // --untracked-files=all, not the default normal: normal collapses a
        // wholly-untracked directory to one line ("?? supabase/migrations/"),
        // which would never end in .sql and silently match nothing. Doesn't
        // reproduce against the real repo today (supabase/migrations/ already
        // has hundreds of tracked files, so git never collapses it) but it's
        // a one-line fix for a real latent gap -- caught by selftest.js's own
        // fixture, which starts that directory wholly untracked.
        const out11 = execSyncMig('git status --porcelain --untracked-files=all -- supabase/migrations',
          { cwd: effCwd11, encoding: 'utf8', timeout: 5000, stdio: ['pipe', 'pipe', 'ignore'] });
        const untracked11 = out11.split('\n')
          .filter(l => l.startsWith('?? ') && l.trim().toLowerCase().endsWith('.sql'))
          .map(l => l.slice(3).trim());
        if (untracked11.length) {
          v.push({ rule: 'warn-untracked-migrations', blockable: false, unlocked: false,
            reason: `${untracked11.length} untracked supabase/migrations/*.sql file(s): ${untracked11.join(', ')} -- if any are already live (hand-applied via Supabase MCP), commit them now; verify against the live ledger with the Supabase MCP's list_migrations before assuming it's safe to leave uncommitted.` });
        }
      } catch (_) { /* not a git repo, git missing, path error -- fail open */ }
    }
  }

  return { tool, violations: v };
}

function decide(raw) {
  if (truthy(process.env.EQ_GUARD_OFF)) return allow();
  let data;
  try { data = JSON.parse(raw || '{}'); } catch (_) { return allow(); } // fail-open on bad input
  let tool = '', violations = [];
  try { ({ tool, violations } = evaluate(data)); }
  catch (err) { log(`${new Date().toISOString()}\tERROR\tguard-internal\t-\t-\t${err && err.message}`); return allow(); }

  if (!violations.length) return allow();

  const ts = new Date().toISOString();
  // session_id + cwd appended as trailing tab fields (additive — existing 6-field
  // readers are unaffected). Lets a session-scoped consumer (ddl_migration_gate.py)
  // attribute a gate-sql/apply_migration event to the session and repo it came
  // from; historical lines without these fields are simply not session-attributable.
  const sessId = data.session_id || '';
  const evtCwd = (data.cwd || process.cwd() || '').replace(/\\/g, '/');
  for (const x of violations) {
    log(`${ts}\t${MODE}\t${x.rule}\t${x.unlocked ? 'unlocked' : 'fired'}\t${tool}\t${x.reason}\t${sessId}\t${evtCwd}`);
  }

  // A rule blocks when it is blockable, not unlocked, and either forced
  // (always-block — near-zero false positives) or the session is in block mode.
  const blockers = violations.filter(x => x.blockable && !x.unlocked && (x.force || MODE === 'block'));
  if (blockers.length) {
    return deny('eq-guard blocked: ' + blockers.map(x => `${x.rule} — ${x.reason}`).join(' ; '));
  }

  process.stderr.write(`eq-guard WARN [${MODE}]: ${violations.map(x => x.rule).join(', ')}\n`);
  return allow();
}

let raw = '';
try {
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', d => { raw += d; });
  process.stdin.on('end', () => decide(raw));
  process.stdin.on('error', () => decide(raw));
} catch (_) { decide(raw); }

// === DURABILITY BACKUP META ===
// This is a durability backup, not the live file — it is never loaded or
// executed from this path. Source of truth: ~/.claude/hooks/guard.js
// (Royce's machine, user-level, not version-controlled). Last synced:
// 2026-09-15. Checked for drift every session by hooks/session_start.py's
// CMDSYNC step (system/failures.md -> F19), which truncates the file at
// the "DURABILITY BACKUP META" marker above before hashing, so keep that
// marker line byte-exact if you touch this comment. To restore: copy
// everything ABOVE this block back to ~/.claude/hooks/guard.js unchanged.
// === END META ===
