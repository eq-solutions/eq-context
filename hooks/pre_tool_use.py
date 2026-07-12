#!/usr/bin/env python3
"""
PreToolUse guard — RUNG 4. Prevention, not documentation.

Blocks the two failures prose could not stop:
  F2  Edit/Write silently TRUNCATE long files on the C:\\Projects virtiofs mount.
      Recurred twice (2026-05-24, 2026-07-11). Destroyed 31 lines of CLAUDE.md
      while reporting success. Prose was rung 1 and failed twice. This is rung 4.
  --  git from the Cowork sandbox leaves orphan .git/index.lock (Loop of Despair).

Scope: Linux sandbox (Cowork) only. On the Beelink (Windows) Claude Code writes and
runs git natively; neither bug applies, so the guard stays out of the way.

FAIL-CLOSED on the truncation guard. If we cannot resolve a path under the mount to
count its lines, we BLOCK. Rationale (learned the hard way, 2026-07-11): the first
version of this hook returned 0 lines for an unresolvable path and let a 308-line
Edit through — it failed OPEN, silently. That is the exact bug class this hook exists
to kill. The cost of a false block is one heredoc. The cost of a false allow is a
destroyed file that reports success.

Contract: exit 2 = BLOCK (stderr shown to the model). exit 0 = allow.
"""
import glob, json, os, platform, re, sys

MAX_LINES = 200
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
GIT_VERBS = (r"\bgit\s+(add|commit|push|pull|rm|mv|checkout|merge|rebase|status|"
             r"stash|reset|fetch|clone|restore|switch|tag|branch|apply|cherry-pick)\b")


def in_sandbox():
    # The virtiofs truncation + NUL-fill + git-lock bugs are Linux-sandbox-only.
    # On the Beelink (Windows) Claude Code writes natively and none of them apply,
    # so the guard deliberately no-ops there. EQ_FORCE_GUARD=1 turns it on anyway,
    # which is how the adversarial suite tests the guard from Windows.
    if os.environ.get("EQ_FORCE_GUARD") == "1":
        return True
    return platform.system() != "Windows"


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
                        f"    cat > <file> << 'EOF'   (full rewrite)\n"
                        f"    cat >> <file> << 'EOF'  (append)\n"
                        f"    wc -l <file> && tail -2 <file>\n\n"
                        f"  system/failures.md → F2. Do not retry this tool on this file.\n"
                    )

    # --- F6: append (>>) NUL-fills long files on this mount ------------------
    if tool == "Bash":
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
    if tool == "Bash" and re.search(GIT_VERBS, ti.get("command", "") or ""):
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
