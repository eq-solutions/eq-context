#!/usr/bin/env python3
"""
PreToolUse guard — RUNG 4. The leash for an auto-PR-finding agent.

From the 2026-07-20 "self-improving substrate" conversation (sessions/2026-07-20.md,
session 9): the steelman for automation that finds and fixes its own drift was
real. The counter-argument was also real — if the same model deciding what to
fix also decides whether the fix is safe to land, that's the model grading its
own homework on exactly the judgment most likely to be wrong. So the boundary
lives here, outside the acting model, enforced at the point of action, not in
a prompt the model could misread or a self-assessment it could get wrong.

Only active when EQ_AUTO_PR_MODE=1 is set. Normal interactive Claude Code
sessions never see this guard — it exists for a scoped, automated agent run,
not for you at the keyboard.

Scope is read from system/auto-pr-scope.md's fenced ALLOW/DENY block — one
source of truth, not duplicated into this file (the same "one fact, one home"
rule the rest of this repo already holds itself to). If that file is missing
or unparseable, FAIL CLOSED: block everything. A guard that can't find its own
leash does not get to decide it's off the leash.

Enforces, unconditionally, regardless of scope file content:
  - No push to main. No merge. No force-push. No branch/tag deletion.
  - No edit to system/auto-pr-scope.md itself, even if ALLOW somehow named it —
    the leash cannot lengthen itself from inside.

Contract: exit 2 = BLOCK (stderr shown to the model). exit 0 = allow.
"""
import json
import os
import re
import sys

EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
SCOPE_FILE = "system/auto-pr-scope.md"
NEVER_EDITABLE = {SCOPE_FILE}  # cannot lengthen its own leash, no matter what ALLOW says

DANGEROUS_GIT = re.compile(
    r"\bgit\s+push\b.*\b(main|master)\b"
    r"|\bgh\s+pr\s+merge\b"
    r"|\bgit\s+push\b.*--force"
    r"|\bgit\s+push\b.*-f\b"
    r"|\bgit\s+branch\s+-D\b"
    r"|\bgit\s+push\b.*--delete\b",
    re.I,
)


def active():
    return os.environ.get("EQ_AUTO_PR_MODE") == "1"


def block(msg):
    sys.stderr.write(msg)
    sys.exit(2)


def repo_root():
    return os.environ.get("EQ_CONTEXT", r"C:\Projects\eq-context")


def parse_scope(root):
    """Read ALLOW/DENY globs from auto-pr-scope.md. None on any parse failure
    (caller must treat None as fail-closed, not as an empty-but-valid scope)."""
    path = os.path.join(root, SCOPE_FILE)
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return None
    m = re.search(r"```\s*\nALLOW:\s*\n(.*?)\nDENY:\s*\n(.*?)\n```", content, re.S)
    if not m:
        return None
    allow = [ln.strip() for ln in m.group(1).splitlines() if ln.strip()]
    deny = [ln.strip() for ln in m.group(2).splitlines() if ln.strip()]
    if not allow:
        return None
    return allow, deny


def normalize(path):
    return (path or "").replace("\\", "/").lstrip("/")


def relpath(path, root):
    p = normalize(path)
    r = normalize(root)
    if p.lower().startswith(r.lower() + "/"):
        return p[len(r) + 1:]
    return p  # already relative, or unresolvable — matched as-is (fail-closed via ALLOW miss)


def _glob_to_regex(pattern):
    """Translate our two supported constructs to regex — deliberately not
    fnmatch, which requires a literal '/' between '**' and what follows and so
    silently excludes DIRECT children of a '**/' directory (a real bug this
    caught: '.github/scripts/**/*.py' would have blocked editing
    '.github/scripts/refresh_digest.py' itself — zero path segments deep,
    not one).
      **/  -> zero or more full path segments
      **   -> anything, including '/' (only meaningful at pattern end)
      *    -> anything except '/'
    """
    out = []
    i, n = 0, len(pattern)
    while i < n:
        if pattern[i:i + 3] == "**/":
            out.append(r"(?:.*/)?")
            i += 3
        elif pattern[i:i + 2] == "**":
            out.append(r".*")
            i += 2
        elif pattern[i] == "*":
            out.append(r"[^/]*")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return "^" + "".join(out) + "$"


def path_matches(path, patterns):
    return any(re.match(_glob_to_regex(pat), path) for pat in patterns)


def main():
    if not active():
        sys.exit(0)

    raw = sys.stdin.read()
    if not raw.strip():
        sys.exit(0)
    data = json.loads(raw)
    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}
    root = repo_root()

    # --- unconditional: no landing the work itself, regardless of scope ------
    if tool in {"Bash", "PowerShell"}:
        cmd = ti.get("command", "") or ""
        if DANGEROUS_GIT.search(cmd):
            block(
                "BLOCKED by auto_pr_guard (rung 4) — FAIL-CLOSED.\n\n"
                "  An auto-PR-mode agent may open a PR and stop. It may never push to\n"
                "  main/master, merge a PR, force-push, or delete a branch. A human makes\n"
                "  every landing decision — this is not a prompt-level rule, it's enforced\n"
                "  here regardless of what the agent believes it's authorized to do.\n\n"
                "  system/auto-pr-scope.md — 'The three rules, unconditionally'.\n"
            )

    # --- scoped: edits must land inside ALLOW, never in DENY or the leash file
    if tool in EDIT_TOOLS:
        path = ti.get("file_path") or ti.get("notebook_path") or ""
        rel = relpath(path, root)

        if rel in NEVER_EDITABLE:
            block(
                f"BLOCKED by auto_pr_guard (rung 4) — FAIL-CLOSED.\n\n"
                f"  '{rel}' is the scope file itself. It cannot expand its own leash from\n"
                f"  inside an automated run, even if ALLOW somehow named it. Scope changes\n"
                f"  require a normal human-reviewed PR.\n"
            )

        scope = parse_scope(root)
        if scope is None:
            block(
                f"BLOCKED by auto_pr_guard (rung 4) — FAIL-CLOSED.\n\n"
                f"  Could not read/parse {SCOPE_FILE} to determine what's in scope.\n"
                f"  A guard that can't find its own leash does not get to decide it's off\n"
                f"  the leash. Fix the scope file (as a normal, human-reviewed change) —\n"
                f"  do not retry this edit until it parses.\n"
            )
        allow, deny = scope

        if path_matches(rel, deny):
            block(
                f"BLOCKED by auto_pr_guard (rung 4) — FAIL-CLOSED.\n\n"
                f"  '{rel}' matches system/auto-pr-scope.md's DENY list.\n"
                f"  Out of scope for an automated fix, unconditionally.\n"
            )

        if not path_matches(rel, allow):
            block(
                f"BLOCKED by auto_pr_guard (rung 4) — FAIL-CLOSED.\n\n"
                f"  '{rel}' does not match any pattern in system/auto-pr-scope.md's ALLOW\n"
                f"  list. Default is deny — only explicitly listed paths are in scope.\n"
            )

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        # Fail CLOSED here, unlike pre_tool_use.py's outer handler — this guard
        # exists specifically for unsupervised runs. An unattended agent hitting
        # a swallowed internal error and proceeding unguarded is worse than one
        # that stops and waits for a human to look at the traceback.
        sys.stderr.write(f"[auto_pr_guard ERROR — BLOCKING, fail-closed: {e}]\n")
        sys.exit(2)
