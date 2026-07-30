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

Scope: F2/F6/the git-lock block are Linux sandbox (Cowork) only — on the Beelink
(Windows) Claude Code writes and runs git natively; neither bug applies there, so
those specific checks stay out of the way. F7's corruption *scan* is deliberately
NOT scoped this way (see in_sandbox() vs the unconditional check in main()) — it
is defense-in-depth against the sandbox-scoping assumption itself being wrong, or
being bypassed by a wiring gap this file can't see from inside its own process.

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


def targets_mount(path):
    p = (path or "").replace("\\", "/").lower()
    return "/projects/" in p or p.endswith("/projects") or "c:/projects" in p


def resolve(path):
    """Map a Windows-or-Linux path onto a real file here. None = unresolvable."""
    if not path:
        return None
    if os.path.isfile(path):
        return path
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


def block(msg):
    sys.stderr.write(msg)
    sys.exit(2)


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
        cwd = data.get("cwd") or os.getcwd()
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
