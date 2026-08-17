#!/usr/bin/env python3
"""
PreToolUse guard — RUNG 4. Prevention, not documentation.

Blocks the failures prose could not stop:
  F2  Edit/Write silently TRUNCATE long files on the C:\\Projects virtiofs mount.
      Recurred twice (2026-05-24, 2026-07-11). Destroyed 31 lines of CLAUDE.md
      while reporting success. Prose was rung 1 and failed twice. This is rung 4.
  F6  Append (>>) NUL-fills long files on the same mount.
  F7  A git merge/stash-pop round-trip NUL-filled scripts/sites.js on 2026-07-28 —
      via a mechanism this file's own blanket git-verb block (below) should already
      have stopped outright. Root cause of THAT gap is still open (unwired hook in
      whatever sandbox ran that session, or a tool name this hook didn't match —
      see system/failures.md -> F7 and ops/pending.md). This file's contribution:
      widen tool matching to also cover PowerShell, not just Bash, and add an
      independent, NOT sandbox-gated pre-git-verb NUL-byte scan of the working
      tree — so corruption from ANY path this guard didn't see still gets caught
      before the next git add/commit/push propagates it further.
  --  git from the Cowork sandbox leaves orphan .git/index.lock (Loop of Despair).
  F9  The SHARED eq-context checkout (C:\\Projects\\eq-context) takes commits from
      several Claude Code sessions plus nightly bots, all against the same working
      directory. Recurred 2026-07-14, 2026-08-03 (x3 in ~10 min), 2026-08-04 (x2),
      2026-08-05 (guard existed but wasn't reachable — see the note below).
      Two distinct DAMAGE mechanisms:
        (a) bare `git commit` (no `--` pathspec) commits the WHOLE index, sweeping
            up anything a concurrent session already staged there — a targeted
            `git add system/worktree-registry.md && git commit` swept up three
            unrelated files another session had staged, 2026-08-04.
        (b) rebase/merge/pull mutate HEAD, the index, and refs across several
            non-atomic steps; two sessions doing this against the same working
            directory at once produced a stuck rebase, conflict markers committed
            straight to `main`, and a ref left pointing at a stale commit.
      Fix: (a) requires an explicit pathspec on every commit in the shared
      checkout; (b) redirects rebase/merge/pull there to an isolated clone.
      Neither check fires outside the ONE shared checkout — a private clone
      (the escape valve both messages recommend) has no concurrent writer, so
      neither risk applies there.
  F12 F9's escape valve (b) ends with `git push origin main` FROM the isolated
      clone — never a manual copy of a resolved file back onto the shared
      checkout's disk. Recurred twice (2026-08-05, 2026-08-17) via exactly
      that anti-pattern: a raw cp/Copy-Item silently overwrote the shared
      checkout's on-disk file with the side-clone's older content, reverting
      a concurrent session's already-pushed edit. Blocks any copy/move whose
      destination path resolves inside the shared checkout while its source
      does not — push from the other checkout instead, so git's own
      fast-forward check can refuse loudly on divergence instead of a
      filesystem copy silently clobbering.

Scope: F2/F6/the git-lock block are Linux sandbox (Cowork) only — on the Beelink
(Windows) Claude Code writes and runs git natively; neither bug applies there, so
those specific checks stay out of the way. F7's corruption *scan* and F9 are
deliberately NOT scoped this way (see in_sandbox() vs the unconditional checks in
main()) — F9 in particular has only ever been observed happening natively on the
Beelink, never in the sandbox, so gating it on in_sandbox() would make it inert
exactly where it's needed.

F9's wiring gap (found + fixed 2026-08-05, one day after shipping): this file
was wired into PreToolUse only at the C:\\Projects umbrella-root settings.json —
the identical "guard that isn't wired" shape session_start.py already hit once
(fixed 2026-07-12 by moving to USER settings, so it fires for every session).
This file never got that same fix, so a session launched inside a repo or
worktree — the common case — never invoked it at all. F9(a) recurred within 24h
of shipping via exactly that gap (commit 2104668, session launched in a
worktree). Fixed by wiring this file at user scope too, alongside guard.js.

Two more independent gaps compounded that same incident, both sharing one root
shape (an intervening `-C <path>` between "git" and what comes next) that
guard.js's own reflection-gate rule already found and fixed for itself,
2026-07-26 — neither fix had been ported here when F9 shipped 2026-08-04:
  1. cwd resolution read data.get("cwd") alone — the session's NOMINAL starting
     directory, never an in-command `cd "<path>" &&` / `git -C <path>`. Fixed by
     effective_cwd(), mirroring guard.js's precedence (-C, then a leading cd,
     then data.cwd).
  2. COMMIT_RE / REBASE_MERGE_PULL_RE required "git" and the verb to be
     separated by whitespace ONLY, so `git -C <path> commit ...` — a real
     invocation shape in this environment — never matched as a commit at all,
     independent of cwd. Found live while writing gap 1's regression test.
     Fixed by widening both to tolerate the same optional `-C <path>` prefix.
Commit 2104668 needed gap 1's fix specifically: its session's nominal cwd was a
real, separate git worktree with its own valid toplevel, so cwd resolution had
to track the command's actual `cd` to see that it had, in fact, landed in the
shared checkout. Wiring alone would not have been enough.

F9(a) also gained a merge-completion exemption (2026-08-05, found live
reconciling a real divergence in this shared checkout): a bare `git commit`
completing an in-progress merge (`.git/MERGE_HEAD` present) is allowed even
with no `--` pathspec — that commit is SUPPOSED to record everything staged,
and can't be meaningfully pathspec-scoped the way a normal commit can. Before
this, the only escape hatch was `--amend`, which doesn't fit a merge commit at
all — this hook had no way to let a legitimate `git commit --no-edit` through
after resolving conflicts.

A same-day earlier version of this note attributed the incident to the commit
running "outside Claude Code's own tool-call hook entirely" — inferred from its
"via Cowork" author string plus the standing Cowork-sandbox git rule below,
never checked against guard.log. guard.log disproves it: gate-outbound fired for
this exact command, timestamped to the second, from an ordinary Claude Code
session — "via Cowork" is this environment's standard git identity, not a
marker of the sandboxed product. Both real mechanisms are the two paragraphs
above, both fixed. Recurrence recorded: system/failures.md -> F9.

FAIL-CLOSED on the truncation guard. If we cannot resolve a path under the mount to
count its lines, we BLOCK. Rationale (learned the hard way, 2026-07-11): the first
version of this hook returned 0 lines for an unresolvable path and let a 308-line
Edit through — it failed OPEN, silently. That is the exact bug class this hook exists
to kill. The cost of a false block is one heredoc. The cost of a false allow is a
destroyed file that reports success.

Contract: exit 2 = BLOCK (stderr shown to the model). exit 0 = allow.
"""
import glob, json, os, platform, re, subprocess, sys

MAX_LINES = 200
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
SHELL_TOOLS = ("Bash", "PowerShell")
GIT_VERBS = (r"\bgit\s+(add|commit|push|pull|rm|mv|checkout|merge|rebase|status|"
             r"stash|reset|fetch|clone|restore|switch|tag|branch|apply|cherry-pick)\b")

# F9 — the ONE shared checkout, never a private/fresh clone (which is the escape
# valve F9's own block messages recommend, and must not itself trip these checks).
# EQ_CONTEXT override matches the convention session_start.py already uses.
SHARED_EQ_CONTEXT = (os.environ.get("EQ_CONTEXT", r"C:\Projects\eq-context")
                      .replace("\\", "/").rstrip("/").lower())
# Both tolerate an optional `-C <path>` between "git" and the verb — without
# it, `git -C <path> commit ...` (a real invocation shape in this environment,
# same fix guard.js's reflection-gate rule already made for itself 2026-07-26)
# never matched as a commit/rebase/merge/pull at all. `[^"]*` (not `[^"]+`) so
# it still matches after _strip_quoted() blanks a quoted path to `""`.
#
# (?!-) after the verb (found 2026-08-05, live, running `git merge-base` for
# this exact investigation): `\b` alone matches the transition between "e" and
# "-", so `merge\b` matches inside "merge-base" too — a real, read-only,
# harmless plumbing command wrongly blocked as if it were `git merge`. Same
# shape for `commit-graph`/`commit-tree` against COMMIT_RE. (?!-) excludes any
# git-verb-shaped subcommand that continues past a hyphen into something else.
COMMIT_RE = re.compile(r'(?<![\w-])git\s+(?:-C\s+(?:"[^"]*"|\S+)\s+)?commit(?!-)\b')
REBASE_MERGE_PULL_RE = re.compile(r'(?<![\w-])git\s+(?:-C\s+(?:"[^"]*"|\S+)\s+)?(rebase|merge|pull)(?!-)\b')

# effective_cwd()'s cd-detection (2026-08-15) — `cd` recognised at true string
# start, at the start of a literal line (re.MULTILINE), OR immediately after a
# command separator (`&&`/`;`/`|`), so `git worktree add X && cd X && git
# rebase ...` — this hook's own escape-valve advice, followed literally, on
# ONE line — resolves correctly instead of falling through to the session's
# nominal cwd. See effective_cwd()'s own docstring for the live incident this
# closes. finditer() returns matches left-to-right; effective_cwd() takes the
# LAST one, since a later cd in a chain overrides an earlier one.
_CD_CHAIN_RE = re.compile(r'(?:^|&&|;|\|)\s*cd\s+(?:"([^"]*)"|(\S+))', re.MULTILINE)

# F10 — matches a `git config` SET of core.hooksPath: an optional --local/
# --worktree/--global scope, then the key, then a value (quoted or bare).
# Deliberately does NOT match a bare read (`git config core.hooksPath`, no
# value — nothing follows the key so the trailing \s+(value) group can't
# match) or `--get`, and the (?!--unset\b) lookahead keeps a real `--unset`
# invocation (flag comes BEFORE the key in git's own grammar: `git config
# --unset core.hooksPath`) from ever reaching this regex as if `--unset`
# were the value — moot given where git actually puts the flag, kept as a
# defensive belt-and-braces read of this regex's own intent. --unset itself
# is deliberately NOT blocked: none of F10's 3 real recurrences were caused
# by one, and `--worktree --unset core.hooksPath` specifically can be the
# legitimate FIX (removing a bad worktree-scope override so a correct
# --local value takes effect again) — blocking every --unset shape would
# risk blocking the correction itself, a worse outcome than the narrower
# gap this leaves. See the F10 block below for the full recurrence history.
HOOKSPATH_SET_RE = re.compile(
    r'(?<![\w-])git\s+(?:-C\s+(?:"[^"]*"|\S+)\s+)?config\s+'
    r'(?:--(local|worktree|global)\s+)?'
    r'core\.hooksPath\s+(?!--unset\b)(?:"([^"]*)"|(\S+))'
)

# Extensions that are legitimately binary — skip these in the F7 NUL scan so a
# real image/font doesn't false-positive. Everything else (source, docs, config)
# is expected to be text; a NUL byte in one of those is always corruption.
NUL_SCAN_SKIP_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".bmp",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".pdf", ".zip", ".gz", ".tar", ".7z",
    ".mp3", ".mp4", ".wav", ".mov",
    ".sqlite", ".db", ".bin", ".exe", ".dll", ".so", ".pyc",
}


def in_sandbox():
    # The virtiofs truncation + NUL-fill + git-lock bugs are Linux-sandbox-only.
    # On the Beelink (Windows) Claude Code writes natively and none of them apply,
    # so the guard deliberately no-ops there. EQ_FORCE_GUARD=1 turns it on anyway
    # (and =0 forces it off), which is how the adversarial suite tests both sides
    # of this from a single machine regardless of what platform it actually runs on.
    v = os.environ.get("EQ_FORCE_GUARD")
    if v == "1":
        return True
    if v == "0":
        return False
    return platform.system() != "Windows"


def effective_cwd(cmd, data):
    """The directory a shell command ACTUALLY runs a git verb in — not just the
    session's nominal starting cwd. data.get("cwd") stays pinned to wherever the
    session started and does not follow an in-command `cd` or `git -C` — the
    identical blind spot guard.js's own reflection-gate rule hit and fixed for
    itself 2026-07-26 (confirmed live there: `cd "<path>" && git commit ...` and
    `git -C "<path>" commit ...` are the actual shapes this environment's Bash
    tool produces, since it discourages a separate `cd`). Missing this let F9(a)
    recur 2026-08-05 even after the wiring fix alone: a session's nominal cwd was
    a real, separate git worktree, so data.cwd resolved to the worktree's own
    toplevel even though the command had already `cd`ed into the shared checkout.
    Mirrors guard.js's exact precedence: -C first, then a leading cd.

    re.MULTILINE on the cd fallback (found 2026-08-05, live, false-blocking a
    rebase genuinely run inside an isolated clone — the F9 escape valve this
    hook itself recommends): bare `^` anchors to the start of the WHOLE command
    string, not the start of a line. A `cd "<path>" && git ...` preceded by an
    earlier line — e.g. `CLONE="<path>"\ncd "$CLONE" && git rebase ...`, an
    ordinary way to spell a long path once and reuse it — put `cd` second, so
    `^` never matched, the function fell through to data.get("cwd"), and a
    command genuinely `cd`-ed into a private clone got attributed to whatever
    directory the session nominally started in. Same failure shape as the two
    gaps above (an effective-directory regex too narrow for a real invocation
    shape this environment's Bash tool produces), a different specific cause
    (line-anchoring, not a missing `-C` prefix). guard.js's own equivalent
    check is regex-per-call on a single flattened cwd string, not re.search
    against the raw multi-line command, so it was never exposed to this
    particular gap. system/failures.md -> F9 — a guard false-positive, not a
    new corruption recurrence, so it isn't counted as one there (same
    treatment as F9(a)'s merge-completion exemption above).

    2026-08-15: the cd-detection above only recognised `cd` at the true start
    of the command string or of a literal line (bare `^` / re.MULTILINE) — it
    did not recognise `cd` chained onto an EARLIER command on the SAME line
    via `&&`/`;`/`|`, e.g. `git worktree add X origin/main && cd X && git
    rebase origin/main`. That shape is not exotic — it is this hook's OWN
    escape-valve advice, followed literally (`git clone ... && cd <dir> &&
    git rebase ...`), and this environment's Bash tool genuinely produces it
    as one line. Found live: a rebase run inside a real, separate `git
    worktree add` AND inside a fresh `git clone` was both wrongly blocked —
    the exact two escape valves this hook recommends. Root cause distinct
    from the 2026-08-05 fix above: that one handles `cd` on a later LINE;
    this handles `cd` later on the SAME line, which has no literal newline
    for `^`/MULTILINE to anchor to. Fixed by also matching `cd` immediately
    after a command separator, and by taking the LAST such match — a later
    `cd` in a chain overrides an earlier one for where the trailing git verb
    actually runs, same reasoning `-C` already gets.

    Deliberately NOT quote-stripped: a first pass ran this whole function
    against _strip_quoted(cmd), reasoning that a commit message merely
    containing the text "cd <path>" shouldn't be misread as a real shell cd.
    That broke 6 of this suite's own existing tests — _strip_quoted() blanks
    quoted CONTENTS to "" (an empty quoted string), and every real -C/cd
    value in actual use here IS quoted (`cd "<path>"`, `git -C "<path>"`), so
    stripping first destroys the exact value this function exists to read.
    The false-negative that pass was guarding against is real in principle
    but was already equally present in the ORIGINAL code (an embedded
    newline inside a quoted multi-line argument could already misplace a
    line-start cd) — a distinct, pre-existing, narrower risk, not something
    this fix introduces or is scoped to close. Left as-is rather than solved
    partially and unsafely; a genuine fix needs position-aware quote
    tracking (know which & / cd / ^ occurrences are real shell syntax vs.
    inside a string literal), which is adversarial-test-grade work in its
    own right, not a same-pass addition to a narrower, already-confirmed bug."""
    m = re.search(r'git\s+-C\s+"([^"]+)"', cmd) or re.search(r'git\s+-C\s+(\S+)', cmd)
    if not m:
        cd_matches = list(_CD_CHAIN_RE.finditer(cmd))
        if cd_matches:
            last = cd_matches[-1]
            return last.group(1) if last.group(1) is not None else last.group(2)
    if m:
        return m.group(1)
    return data.get("cwd") or os.getcwd()


def repo_root_for(cwd):
    """git's own idea of the repo root for `cwd` — None if not inside one."""
    try:
        p = subprocess.run(["git", "-C", cwd or ".", "rev-parse", "--show-toplevel"],
                            capture_output=True, text=True, timeout=5)
    except Exception:
        return None
    if p.returncode != 0:
        return None
    return p.stdout.strip().replace("\\", "/")


def nul_corrupted_files(repo_root):
    """F7 — scan the working tree's modified/untracked files for NUL bytes, the
    shared F6/F7 signature. Scoped to `git status --porcelain` output (what a git
    verb is actually about to touch), not every tracked file, so it stays cheap.
    Returns a list of (relpath, nul_count); None if the check itself couldn't run
    (caller treats that as 'nothing to report', not as a block — a broken scan
    should not itself become a new way to get stuck)."""
    try:
        p = subprocess.run(["git", "-C", repo_root, "status", "--porcelain"],
                            capture_output=True, text=True, timeout=10)
    except Exception:
        return None
    if p.returncode != 0:
        return None
    hits = []
    for line in p.stdout.splitlines():
        if len(line) < 4:
            continue
        rel = line[3:].strip().strip('"')
        if " -> " in rel:          # rename entries: "old -> new"
            rel = rel.split(" -> ", 1)[1]
        _, ext = os.path.splitext(rel)
        if ext.lower() in NUL_SCAN_SKIP_EXT:
            continue
        full = os.path.join(repo_root, rel)
        if not os.path.isfile(full):
            continue
        try:
            with open(full, "rb") as fh:
                data = fh.read()
        except Exception:
            continue
        if b"\x00" in data:
            hits.append((rel, data.count(b"\x00")))
    return hits


def mount_roots():
    """Every plausible root for the C:\\Projects tree, in this filesystem."""
    roots = []
    for pat in ("/sessions/*/mnt/Projects", "/mnt/Projects", "C:/Projects"):
        roots.extend(glob.glob(pat))
    return [r for r in roots if os.path.isdir(r)]


# Test-only escape valve — mirrors the EQ_CONTEXT override above for F9.
# targets_mount() gates on a literal "/projects/" path segment, true for the
# real C:\Projects mount but NOT true when the adversarial suite itself is run
# from a clone checked out somewhere else (e.g. a throwaway clone for
# clean-room verification). Without this, F2/F7's own ROOT-derived fixtures
# (CLAUDE_MD, LESSONS, the F7 NUL-scan repo) silently read as "not the mount"
# and every case expecting BLOCK instead ALLOWS — a location artifact, not a
# guard regression (confirmed 2026-08-05: the SAME 3 cases fail identically
# against an old, pre-F9 commit run from a non-/projects/ location, and origin/
# main passes 0/75 clean from a /projects/-pathed one — see system/failures.md).
# Unset in every real session; only the test suite sets it, pointed at ROOT.
EQ_MOUNT_ROOT = (os.environ.get("EQ_MOUNT_ROOT", "")
                 .replace("\\", "/").rstrip("/").lower())


def targets_mount(path):
    p = (path or "").replace("\\", "/").lower()
    if "/projects/" in p or p.endswith("/projects") or "c:/projects" in p:
        return True
    return bool(EQ_MOUNT_ROOT) and (p == EQ_MOUNT_ROOT or p.startswith(EQ_MOUNT_ROOT + "/"))


def resolve(path):
    """Map a Windows-or-Linux path onto a real file here. None = unresolvable."""
    if not path:
        return None
    if os.path.isfile(path):
        return path
    if EQ_MOUNT_ROOT:
        pl = path.replace("\\", "/").lower()
        if pl == EQ_MOUNT_ROOT or pl.startswith(EQ_MOUNT_ROOT + "/"):
            # EQ_MOUNT_ROOT paths are already real, correctly-rooted paths on
            # THIS filesystem (the test suite's own fixtures) — unlike the
            # real-mount case below, there's no cross-environment (Windows-
            # path-seen-from-a-Linux-sandbox) translation to do. Parent exists
            # ⇒ genuinely a new file, same rule the real-mount loop uses.
            return path if os.path.isdir(os.path.dirname(path)) else None
    p = path.replace("\\", "/")
    m = re.search(r"(?i)(?:^[a-z]:/Projects|/mnt/Projects|.*?/mnt/Projects)/(.*)$", p)
    tail = m.group(1) if m else None
    if not tail:
        m2 = re.search(r"(?i)/Projects/(.*)$", p)
        tail = m2.group(1) if m2 else None
    if not tail:
        return None
    for root in mount_roots():
        cand = os.path.join(root, tail)
        if os.path.isfile(cand):
            return cand
        if os.path.isdir(os.path.dirname(cand)):
            return cand          # parent exists ⇒ genuinely a new file
    return None


def is_shared_eq_context(root):
    """F9 — True ONLY for the one shared checkout, by exact path. A private/fresh
    clone has a different root and correctly returns False here even though
    `git rev-parse --show-toplevel` still calls it a perfectly good repo."""
    return bool(root) and root.rstrip("/").lower() == SHARED_EQ_CONTEXT


def _strip_quoted(s):
    """F9 — blank out single/double-quoted string content before scanning a
    command for flags. Without this, a commit message that happens to contain
    ' -- ' (e.g. -m "fixes tests -- see PR") would look like a real pathspec
    separator and the bare-commit check below would wrongly allow it through."""
    return re.sub(r"'[^']*'|\"[^\"]*\"", '""', s or "")


def _norm_hookspath(v):
    """F10 — identical normalization to session_start.py's own _norm_hp(), kept
    in lockstep deliberately: this hook decides whether to BLOCK a hooksPath
    SET, session_start.py's HOOKS check decides whether to WARN about the
    result — both must agree on what ".githooks" means (backslashes, a
    leading "./", a trailing "/") or a value one considers fine and the other
    considers wrong would be needlessly confusing."""
    if v is None:
        return None
    v = v.strip().replace("\\", "/")
    return (v[2:] if v.startswith("./") else v).rstrip("/")


# F12 — a raw file copy/move whose DESTINATION lands inside the shared
# eq-context checkout. Deliberately scoped on the PATH STRINGS in the command
# text, never on cwd/repo-root the way F9/F10 are: the incident shape is an
# absolute-path copy that can be issued from anywhere (a side-clone, a linked
# worktree, a scratch dir), not only from a command run FROM inside the shared
# checkout. See the F12 block below (in main()) for the full rationale.
COPY_VERB_RE = re.compile(r'(?<![\w.-])(cp|mv|copy|xcopy|robocopy|Copy-Item|Move-Item)(?=\s)',
                           re.IGNORECASE)


def _norm_path_for_compare(p):
    """Normalize a Windows-or-Git-Bash path to a lowercase, forward-slash form
    for a simple prefix comparison against SHARED_EQ_CONTEXT. Not resolve() —
    this never touches the filesystem, it only asks 'is this path SPELLED as
    inside the shared checkout'. Mirrors guard.js's normalizeMsysPath() for the
    /c/ drive-letter case; the /tmp MSYS-mount case doesn't apply here (F12's
    risk is a copy INTO C:\\Projects\\eq-context specifically, never a copy
    whose destination is under /tmp)."""
    if not p:
        return ""
    p = p.strip().strip('"').strip("'").replace("\\", "/")
    m = re.match(r'^/([A-Za-z])(/.*|$)', p)
    if m:
        p = f"{m.group(1).lower()}:{m.group(2) or '/'}"
    return p.rstrip("/").lower()


def _is_under_shared(p):
    norm = _norm_path_for_compare(p)
    return norm == SHARED_EQ_CONTEXT or norm.startswith(SHARED_EQ_CONTEXT + "/")


def _looks_like_flag(token):
    """True for a Windows/robocopy-style flag (-Force, /E, /MIR, /R:3) that
    _copy_targets_shared should skip when hunting for the src/dest positional
    args. A leading '-' is always a flag. A leading '/' is ambiguous on
    Windows — it's ALSO how a genuine Git-Bash MSYS absolute path spells a
    drive letter (/c/Projects/eq-context/...) — so it's only treated as a
    flag when there's no FURTHER slash after the first segment; a real path
    always has one (found live building this: an earlier version filtered
    '/c/Projects/...' out entirely as if it were a bare '/E'-style flag,
    silently defeating the msys-path BLOCK case one line down from PASS)."""
    body = token.lstrip('\'"')
    if body.startswith('-'):
        return True
    if body.startswith('/'):
        return '/' not in body[1:]
    return False


def _copy_targets_shared(cmd):
    """dest string if `cmd` looks like a copy/move whose DESTINATION resolves
    inside the shared eq-context checkout while the SOURCE does not — the
    exact F12 incident shape (a cross-checkout copy-back). None otherwise,
    including a same-checkout copy (source already under the shared root too
    — an ordinary, safe operation) and a copy whose destination is elsewhere.

    Deliberately tolerant of flags (skips anything _looks_like_flag() calls)
    and takes the LAST TWO remaining positional tokens as src/dest — covers
    the common cp/Copy-Item/xcopy 2-path shape (including `Copy-Item -Path X
    -Destination Y`, since the flag names themselves get filtered and X/Y
    remain the last two positional tokens) and robocopy's dir-then-dir shape.
    Known, accepted narrowing: this does NOT parse robocopy's trailing file
    list or wildcard globs — a guard built to catch the incident shape that
    actually happened (a single-file cp/Copy-Item), not to parse every copy
    invocation grammar exhaustively. Same tradeoff this file already makes
    for F9(a)'s pathspec detection."""
    m = COPY_VERB_RE.search(cmd)
    if not m:
        return None
    tokens = re.findall(r'"[^"]*"|\'[^\']*\'|\S+', cmd[m.end():])
    positional = [t for t in tokens if not _looks_like_flag(t)]
    if len(positional) < 2:
        return None
    src, dest = positional[-2], positional[-1]
    if _is_under_shared(dest) and not _is_under_shared(src):
        return dest
    return None


def block(msg):
    sys.stderr.write(msg)
    sys.exit(2)


# --- F13: false eq-shell deploy-posture claim (rung 4) -----------------------
# scripts/substrate_honesty.py already catches this claim once it is on disk
# (rung 3, per-PR + nightly). That is detection AFTER the damage: by then the
# sentence has been read by whoever the substrate auto-loads into. This layer
# stops it landing at all.
#
# Every PATTERN lives in that scanner and is IMPORTED here, never restated. Two
# copies of this definition drifting apart is precisely the shape of F13, so a
# guard built by copy-paste would reproduce the failure it exists to prevent.
# Only the SCOPING is local: the scanner classifies a line at a time, which is
# right for a file it can re-read around, while a Write payload arrives as one
# blob, so this splits it into bullets first.
F13_HISTORICAL = re.compile(
    r"(^|/)(sessions|archive)/|-archive\.md$|changelog|failures\.md$", re.IGNORECASE
)
_F13_BULLET = re.compile(r"\s*(?:[-*+]\s|#{1,6}\s|\d+\.\s|\|)")


def _f13_classifier():
    """substrate_honesty.classify_deploy_posture, or None if it can't load.

    Degrades to "no opinion" rather than blocking every write — an import error
    here must not become an outage on the Write tool.
    """
    try:
        scripts = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
        if scripts not in sys.path:
            sys.path.insert(0, scripts)
        from substrate_honesty import classify_deploy_posture
        return classify_deploy_posture
    except Exception:
        return None


def f13_verdict(tool, ti):
    """(reason) if this edit writes the false claim, else None."""
    if tool not in EDIT_TOOLS:
        return None
    path = (ti.get("file_path") or ti.get("notebook_path") or "").replace("\\", "/")
    if not path.lower().endswith(".md") or F13_HISTORICAL.search(path):
        return None
    classify = _f13_classifier()
    if classify is None:
        return None

    chunks = [ti.get("content") or "", ti.get("new_string") or ""]
    for e in ti.get("edits") or []:
        if isinstance(e, dict):
            chunks.append(e.get("new_string") or "")

    for chunk in chunks:
        lines = chunk.splitlines()
        # Bullet-scoped, not line-scoped: the repo name and the posture phrase
        # routinely land on different wrapped lines of one item, and F13's own
        # guard spec is written per-bullet for exactly that reason.
        start = 0
        for i in range(len(lines) + 1):
            if i == len(lines) or (i > start and _F13_BULLET.match(lines[i])):
                scope = " ".join(lines[start:i]).strip()
                if scope:
                    try:
                        bad, reason = classify(scope, path)
                    except Exception:
                        bad, reason = False, ""
                    if bad:
                        return reason
                start = i
    return None


def main():
    raw = sys.stdin.read()
    if not raw.strip():
        sys.exit(0)
    data = json.loads(raw)
    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}

    # --- F7: pre-existing NUL corruption, checked ahead of ANY git verb -----
    # Deliberately NOT gated on in_sandbox() — see the module docstring. Runs
    # on every platform, every session, whenever a Bash/PowerShell command is
    # about to touch git, regardless of whether this hook thinks it's in the
    # sandbox. If the working tree is already NUL-corrupted (from a path this
    # guard never saw), block before it can be added/committed/pushed further.
    if tool in SHELL_TOOLS and re.search(GIT_VERBS, ti.get("command", "") or ""):
        cwd = effective_cwd(ti.get("command", "") or "", data)
        root = repo_root_for(cwd)
        if root and targets_mount(root):
            hits = nul_corrupted_files(root)
            if hits:
                detail = "\n".join(f"    {rel} — {n} NUL bytes" for rel, n in hits)
                block(
                    f"BLOCKED by pre_tool_use (F7, rung 4).\n\n"
                    f"  The working tree already has NUL-corrupted file(s), before this\n"
                    f"  {tool} command even runs:\n{detail}\n\n"
                    f"  Do NOT git add/commit/push this state — that would land the\n"
                    f"  corruption in history. Recover first:\n"
                    f"    git checkout -- <file>   (discard the corrupted copy), or\n"
                    f"    read the file, confirm the intended content, then\n"
                    f"    cat > <file> << 'EOF'   (full rewrite — never >>, see F6)\n\n"
                    f"  This didn't come from this hook's own >> check (F6) or its\n"
                    f"  Edit/Write check (F2) — something else corrupted this file.\n"
                    f"  system/failures.md -> F6, F7.\n"
                )

    # --- F9: shared eq-context checkout — concurrent-session git races ------
    # Deliberately NOT gated on in_sandbox() — every occurrence so far (2026-07-14,
    # 2026-08-03 x3, 2026-08-04 x2) happened natively on the Beelink (Windows), not
    # in the Cowork sandbox. Scoped to the ONE shared checkout by exact path — see
    # is_shared_eq_context() — so the fresh clone this hook recommends as the fix
    # is never itself blocked by it.
    if tool in SHELL_TOOLS:
        cmd9 = ti.get("command", "") or ""
        cwd9 = effective_cwd(cmd9, data)
        root9 = repo_root_for(cwd9)
        if is_shared_eq_context(root9):
            stripped9 = _strip_quoted(cmd9)

            # (a) bare `git commit` — no `--` pathspec, no --amend, no in-progress
            # merge. A bare commit records EVERYTHING currently staged, not just
            # what this command just `git add`ed — see module docstring, F9(a).
            # Completing an in-progress merge (.git/MERGE_HEAD exists) is the one
            # case where that's not a risk: the whole point of that commit IS to
            # record everything staged, and a merge commit can't be meaningfully
            # pathspec-scoped the way a normal commit can. Found live 2026-08-05
            # reconciling a real divergence in this shared checkout — this hook
            # had no way to allow a legitimate `git commit --no-edit` after
            # resolving conflicts, only --amend as an escape hatch that didn't fit.
            in_merge9 = os.path.isfile(os.path.join(root9, ".git", "MERGE_HEAD"))
            if (COMMIT_RE.search(stripped9) and "--amend" not in stripped9
                    and not in_merge9
                    and not re.search(r"(^|\s)--(\s+\S)", stripped9)):
                block(
                    "BLOCKED by pre_tool_use (F9, rung 4).\n\n"
                    "  Bare `git commit` in the SHARED eq-context checkout, with no\n"
                    "  `--` pathspec. `git commit` with no pathspec commits EVERYTHING\n"
                    "  currently staged, not just what you just `git add`ed. If a\n"
                    "  concurrent session (or a leftover from one) has anything staged\n"
                    "  in this same working directory, it rides into your commit.\n\n"
                    "  This is exactly what happened on 2026-08-04: a targeted\n"
                    "  `git add system/worktree-registry.md && git commit` swept up\n"
                    "  three unrelated files another session had already staged.\n\n"
                    "  Scope the commit explicitly:\n"
                    "    git commit -m \"...\" -- path/one.md path/two.md\n\n"
                    "  This commits only the named paths' current content and leaves\n"
                    "  everything else in the index untouched, no matter what else is\n"
                    "  staged. If you genuinely mean to commit everything currently\n"
                    "  staged: run `git status --short` first, then name every path\n"
                    "  you saw after `--`.\n\n"
                    "  system/failures.md -> F9.\n"
                )

            # (b) rebase/merge/pull — multi-step, non-atomic ref/HEAD/index
            # mutation. --abort/--continue/--skip recover an ALREADY-in-flight
            # operation and must stay allowed, or this hook would trap a session
            # inside the exact stuck state it exists to prevent.
            m9 = REBASE_MERGE_PULL_RE.search(stripped9)
            if m9 and not re.search(r"--(abort|continue|skip)\b",
                                     stripped9[m9.end():m9.end() + 40]):
                verb9 = m9.group(1)
                block(
                    f"BLOCKED by pre_tool_use (F9, rung 4).\n\n"
                    f"  `git {verb9}` in the SHARED eq-context checkout\n"
                    f"  ({SHARED_EQ_CONTEXT}). This repo takes commits from multiple\n"
                    f"  Claude Code sessions and nightly bots all day. {verb9} mutates\n"
                    f"  HEAD, the index, and refs across several non-atomic steps — if\n"
                    f"  another session touches this same working directory\n"
                    f"  mid-operation, you get what's already happened here more than\n"
                    f"  once: a stuck rebase, conflict markers committed straight to\n"
                    f"  main, or a ref left pointing at a stale commit (2026-07-14,\n"
                    f"  2026-08-03).\n\n"
                    f"  Do this in an ISOLATED clone instead:\n"
                    f"    git clone https://github.com/eq-solutions/eq-context.git <dir>\n"
                    f"    cd <dir> && git {verb9} ...   (safe — nobody else writes here)\n"
                    f"    git push origin main\n\n"
                    f"  Already mid-{verb9}, trying to get OUT of a stuck state?\n"
                    f"  --abort / --continue / --skip are allowed through.\n\n"
                    f"  system/failures.md -> F9. rules/agentic-coding.md.\n"
                )

            # (c) F10 — core.hooksPath set to anything but .githooks. Run against
            # the RAW command, not stripped9: _strip_quoted() would blank out the
            # very value this needs to read. The false-positive cost (an unrelated
            # command whose quoted text happens to contain a full, real
            # `git config core.hooksPath <bad-value>` invocation) is vanishingly
            # unlikely next to the false-negative cost this exists to close — see
            # module docstring's F2 FAIL-CLOSED rationale for the same tradeoff
            # made the same way elsewhere in this file. Ratchet promotion
            # 2026-08-05: rung 1 (system/lessons.md prose) -> rung 4. This is the
            # ONE thing all 3 real recurrences share — an explicit SET landing a
            # wrong value — so it's the one this closes; see HOOKSPATH_SET_RE's
            # own comment for why --unset is deliberately left alone.
            m10 = HOOKSPATH_SET_RE.search(cmd9)
            if m10:
                val10 = m10.group(2) if m10.group(2) is not None else m10.group(3)
                if _norm_hookspath(val10) != ".githooks":
                    scope10 = m10.group(1)
                    flag10 = f"--{scope10} " if scope10 else ""
                    block(
                        f"BLOCKED by pre_tool_use (F10, rung 4).\n\n"
                        f"  Setting core.hooksPath ({scope10 or 'default/--local'} scope) to\n"
                        f"  {val10!r} in the SHARED eq-context checkout — not .githooks.\n\n"
                        f"  This exact symptom has recurred 3 times via 3 different\n"
                        f"  mechanisms (wrong directory 2026-05-24, a shadow copy at\n"
                        f"  .git/hooks 2026-08-04, a --worktree override silently shadowing\n"
                        f"  --local 2026-08-05) — every time, .githooks/pre-commit (secret\n"
                        f"  scanning, frontmatter status-enum) silently stopped running.\n\n"
                        f"  If .githooks is genuinely wrong for what you're doing, that's a\n"
                        f"  decision this hook shouldn't make silently either — stop and ask.\n"
                        f"  Otherwise, the governed value is .githooks:\n"
                        f"    git config {flag10}core.hooksPath .githooks\n\n"
                        f"  system/failures.md -> F10.\n"
                    )

    # --- F12: raw file copy blind-overwrites the SHARED checkout ------------
    # The F9 escape valve (isolated clone/worktree for rebase/merge/pull) ends
    # with `git push origin main` FROM that clone — never a manual copy of a
    # resolved file back onto the shared checkout's disk. Two real incidents
    # did exactly that instead (2026-08-05, 2026-08-17): a raw cp/Copy-Item
    # overwrote the shared checkout's on-disk copy of a file with the
    # side-clone's version, silently reverting whatever a concurrent session
    # had already pushed there in the meantime. A `git push` merges/
    # fast-forwards through git's own machinery and fails loudly on
    # divergence; a filesystem copy has no such check — it just clobbers.
    #
    # Scoped on the DESTINATION path STRING alone (see _copy_targets_shared),
    # not on cwd/repo-root the way F9/F10 are, and deliberately NOT gated on
    # in_sandbox() — same reasoning as F9/F10/F13: both real incidents
    # happened natively on Windows. Rung raised 2 -> 4, closing the general
    # gap the ledger entry named as still open after the narrower
    # substrate_sync.py dirty-checkout fix shipped 2026-08-17.
    if tool in SHELL_TOOLS:
        dest12 = _copy_targets_shared(ti.get("command", "") or "")
        if dest12:
            block(
                f"BLOCKED by pre_tool_use (F12, rung 4).\n\n"
                f"  This copies into the SHARED eq-context checkout\n"
                f"  ({SHARED_EQ_CONTEXT}) from somewhere else — a side-clone, a\n"
                f"  linked worktree, or another checkout entirely.\n\n"
                f"  A raw file copy has no merge/divergence check. If a\n"
                f"  concurrent session pushed to this same file in the\n"
                f"  meantime, the copy silently overwrites it — no error, no\n"
                f"  conflict marker, nothing to catch before it's gone. This is\n"
                f"  exactly what happened twice (2026-08-05, 2026-08-17): an\n"
                f"  older local copy landed on top of a concurrent session's\n"
                f"  already-pushed edit.\n\n"
                f"  Push from the OTHER checkout instead — git's own\n"
                f"  fast-forward check refuses loudly on divergence instead of\n"
                f"  clobbering:\n"
                f"    git -C <other-checkout> push origin main\n\n"
                f"  Then bring the shared checkout up to date the normal way\n"
                f"  (only safe when it has nothing uncommitted — see F9):\n"
                f"    git -C \"{SHARED_EQ_CONTEXT}\" pull --ff-only origin main\n\n"
                f"  Deliberately placing a brand-new, unrelated file here (not\n"
                f"  reconciling a divergent copy of something already tracked)?\n"
                f"  Use the Write tool instead of a shell copy — this guard only\n"
                f"  exists to stop a copy-back from silently clobbering someone\n"
                f"  else's already-pushed edit.\n\n"
                f"  system/failures.md -> F12.\n"
            )

    # --- F13: false eq-shell deploy-posture claim entering substrate --------
    # Deliberately ABOVE the in_sandbox() gate, same reasoning as F7/F9/F10:
    # both recorded recurrences were written from a normal Windows session, not
    # the sandbox. Gated below, this would be dormant in the exact environment
    # where the failure actually happens.
    _f13 = f13_verdict(tool, ti)
    if _f13:
        block(
            f"BLOCKED by pre_tool_use (F13, rung 4).\n\n"
            f"  This {tool} writes a deploy-posture claim about eq-shell /\n"
            f"  core.eq.solutions that is never true on that repo:\n"
            f"    {_f13}\n\n"
            f"  Merging a PR to eq-shell main IS the deploy — Netlify's GitHub App\n"
            f"  (installation 121276861) builds production, live 2-4s later,\n"
            f"  unattended. There is no gap between 'merge it' and 'ship it'.\n\n"
            f"  This bites hardest on AUTH changes: the claim makes a merge read as\n"
            f"  a safe intermediate step when it IS the production deploy.\n\n"
            f"  Do NOT re-derive the posture from deploy_source or\n"
            f"  cdp_enabled_contexts — both look exactly as the false claim\n"
            f"  describes, which is how it survived two re-verifications. Check\n"
            f"  liveness by commit ancestry against the newest ready production\n"
            f"  deploy instead.\n\n"
            f"  Quoting the claim in order to CORRECT it is fine — say so in the\n"
            f"  same bullet (wrong / corrected / no longer / F13) and this passes.\n\n"
            f"  system/failures.md -> F13 · rules/deployment.md\n"
        )

    if not in_sandbox():
        sys.exit(0)

    # --- F2: silent truncation ---------------------------------------------
    if tool in EDIT_TOOLS:
        path = ti.get("file_path") or ti.get("notebook_path") or ""
        if targets_mount(path):
            real = resolve(path)
            if real is None:
                block(
                    f"BLOCKED by pre_tool_use (F2, rung 4) — FAIL-CLOSED.\n\n"
                    f"  Cannot resolve '{path}' to count its lines, so I cannot prove\n"
                    f"  this {tool} is safe. Edit/Write TRUNCATE SILENTLY on this mount.\n\n"
                    f"  Use bash heredoc, then verify:\n"
                    f"    cat > <file> << 'EOF' ... EOF\n"
                    f"    wc -l <file> && tail -2 <file>\n"
                )
            if os.path.isfile(real):
                try:
                    with open(real, encoding="utf-8", errors="replace") as fh:
                        n = sum(1 for _ in fh)
                except Exception as e:
                    block(f"BLOCKED by pre_tool_use (F2) — cannot read '{real}' to verify length ({e}). "
                          f"Use bash heredoc + wc -l.\n")
                if n > MAX_LINES:
                    block(
                        f"BLOCKED by pre_tool_use (F2, rung 4).\n\n"
                        f"  {tool} on a {n}-line file under the C:\\Projects mount.\n"
                        f"  Edit/Write TRUNCATE SILENTLY against virtiofs and report SUCCESS.\n"
                        f"  This destroyed 31 lines of CLAUDE.md on 2026-07-11 (§12, §13, End).\n\n"
                        f"  Use bash heredoc instead, then VERIFY:\n"
                        f"    cat > <file> << 'EOF'   (FULL REWRITE — the ONLY safe method.\n"
                        f"                             Do NOT use >> to append: it NUL-fills\n"
                        f"                             on this mount. See F6.)\n"
                        f"    wc -l <file> && tail -2 <file>\n\n"
                        f"  system/failures.md → F2. Do not retry this tool on this file.\n"
                    )

    # --- F6: append (>>) NUL-fills long files on this mount ------------------
    if tool in SHELL_TOOLS:
        cmd = ti.get("command", "") or ""
        for tgt in re.findall(r">>\s*([^\s;&|)]+)", cmd):
            t = tgt.strip("\"'")
            if t.startswith(("/tmp", "/dev", "/var", "$", "&")):
                continue                       # scratch + shell vars are fine
            block(
                f"BLOCKED by pre_tool_use (F6, rung 4).\n\n"
                f"  Append (>>) to '{t}'. On the C:\\Projects virtiofs mount, append does not\n"
                f"  truncate — it NUL-FILLS. On 2026-07-11 'cat >> system/lessons.md' wrote\n"
                f"  3,955 NUL bytes instead of the content. The file became binary. It\n"
                f"  reported SUCCESS.\n\n"
                f"  FULL REWRITE ONLY:\n"
                f"    cat > {t} << 'EOF'   (read the file first, re-emit it whole)\n\n"
                f"  Then verify ALL THREE — wc -l alone will NOT catch a NUL-fill:\n"
                f"    wc -l {t} && tail -2 {t}\n"
                f"    python3 -c \"d=open('{t}','rb').read(); print('NULs:', d.count(b'\\x00'))\"\n\n"
                f"  system/failures.md -> F6.\n"
            )

    # --- git from sandbox ---------------------------------------------------
    if tool in SHELL_TOOLS and re.search(GIT_VERBS, ti.get("command", "") or ""):
        block(
            "BLOCKED by pre_tool_use hook.\n\n"
            "  git from the Cowork sandbox against C:\\Projects leaves an orphan\n"
            "  .git/index.lock the sandbox cannot unlink (virtiofs EPERM). It then blocks\n"
            "  every later git command — including yours, from PowerShell.\n\n"
            "  Emit a .bat / .ps1 for Royce to run instead.\n"
            "  Read-only inspection is fine: cat .git/HEAD, cat .git/refs/heads/*\n\n"
            "  system/lessons.md → 'Loop of Despair'.\n"
        )

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        # Fail open ONLY for unexpected internal errors — and never silently.
        sys.stderr.write(f"[pre_tool_use ERROR — GUARD DID NOT RUN: {e}] treat writes as unguarded.\n")
        sys.exit(0)
