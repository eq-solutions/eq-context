#!/usr/bin/env python3
"""
Stop gate — RUNG 4, the missing bookend to session_start.py.

session_start.py enforces freshness/goals/ratchet at rung 4. CLAUDE.md Section 10
(Session End Protocol — update pending.md, log the session, push) has always sat at
rung 1: prose an agent has to remember on the way out. Rung 1 is exactly what F2
proved doesn't hold ("the lesson existed, was read, and still didn't fire" —
system/failures.md). This is that same doctrine applied to the step that produces
the commits everything else in this repo assumes are current and pushed.

Checks only what's mechanically observable — never "was every recommendation
applied" (semantic, unenforceable), only:
  1. DIRTY      — eq-context has uncommitted changes sitting in the working tree.
  2. UNPUSHED   — local main is ahead of origin/main (the courier's push half is
                  still manual — see UserPromptSubmit's auto-pull, which only
                  covers the pull side).
  3. LOG GAP    — commits landed in eq-context today but no sessions/<today>.md
                  exists to record what happened.
  4. WORKTREES  — a linked eq-context worktree (nested .claude/worktrees/* or a
                  sibling eq-context-wt-*) carries uncommitted or unpushed work
                  and this session is about to end without landing or flagging
                  it — the direct mechanism behind failure F16's three orphaned
                  worktrees, two of them holding real never-pushed commits,
                  found live 2026-09-08.

Fires globally (every session, every repo) exactly like session_start.py — and
like it, stays silent unless there is something to say. FAILS OPEN BUT LOUD:
this is informational, never blocks Stop. A Stop hook that traps someone mid-exit
is a new "loop of despair" class (hooks/README.md), and unlike a destructive
Edit/Write, there is no destroyed data at stake here to justify fail-closed.
"""
import os, subprocess, sys
from datetime import date

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.environ.get("EQ_CONTEXT", r"C:\Projects\eq-context")
if not os.path.isdir(ROOT):
    for alt in ("/sessions/*/mnt/Projects/eq-context", "C:/Projects/eq-context"):
        import glob
        hits = glob.glob(alt)
        if hits:
            ROOT = hits[0]
            break

out = []


def git(*args):
    """Run git -C ROOT <args>, return stdout stripped, or None on any failure."""
    try:
        p = subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True, timeout=10)
        return p.stdout.strip() if p.returncode == 0 else None
    except Exception:
        return None


def git_at(path, *args):
    """Same as git() but against an arbitrary worktree path, not ROOT — needed
    to check the state of a linked worktree from outside it."""
    try:
        p = subprocess.run(["git", "-C", path, *args], capture_output=True, text=True, timeout=10)
        return p.stdout.strip() if p.returncode == 0 else None
    except Exception:
        return None


def worktree_paths():
    """F16 — every worktree git already knows about for this repo, via
    --porcelain (blank-line-separated stanzas, each starting with a
    `worktree <path>` line) — far more reliable than parsing the
    human-readable table's column spacing. Excludes ROOT itself (the bare
    checkout DIRTY/UNPUSHED above already cover), and covers BOTH
    conventions currently in use — nested .claude/worktrees/* and a sibling
    C:\\Projects\\eq-context-wt-* — since git tracks either location the
    same way once created via `git worktree add`."""
    raw = git("worktree", "list", "--porcelain") or ""
    root_norm = ROOT.replace("\\", "/").rstrip("/").lower()
    paths = []
    for stanza in raw.split("\n\n"):
        for ln in stanza.splitlines():
            if ln.startswith("worktree "):
                p = ln[len("worktree "):].strip()
                if p.replace("\\", "/").rstrip("/").lower() != root_norm:
                    paths.append(p)
                break
    return paths


if not os.path.isdir(os.path.join(ROOT, ".git")):
    # Not a real checkout (e.g. sandbox with no local clone) — nothing to gate.
    sys.exit(0)

lines = []

# --- 1. DIRTY -----------------------------------------------------------
status = git("status", "--porcelain")
if status:
    files = status.splitlines()
    lines.append(f"DIRTY      {len(files)} uncommitted change(s) in eq-context:")
    for f in files[:6]:
        lines.append("           " + f.strip())
    if len(files) > 6:
        lines.append(f"           ...and {len(files) - 6} more")
    lines.append("           Section 10 isn't done until these are committed (or deliberately left — say so).")

# --- 2. UNPUSHED ----------------------------------------------------------
branch = git("rev-parse", "--abbrev-ref", "HEAD")
if branch == "main":
    ahead = git("rev-list", "--count", "origin/main..HEAD")
    if ahead and ahead.isdigit() and int(ahead) > 0:
        lines.append(
            f"UNPUSHED   {ahead} local commit(s) on main not on origin.\n"
            f"           git -C C:\\Projects\\eq-context fetch origin main\n"
            f"           git -C C:\\Projects\\eq-context rebase origin/main\n"
            f"           git -C C:\\Projects\\eq-context push origin main\n"
            f"           (push already allow-listed in settings.json — nothing new to\n"
            f"           approve; fetch+rebase first in case origin moved since these\n"
            f"           were committed — a bare push here has no divergence check)"
        )
elif branch:
    lines.append(f"BRANCH     on '{branch}', not main — push/PR it yourself if this substrate work should land.")

# --- 3. LOG GAP -----------------------------------------------------------
today = date.today().isoformat()
today_commits = git("log", "--since=midnight", "--oneline")
log_file = os.path.join(ROOT, "sessions", f"{today}.md")
if today_commits and not os.path.isfile(log_file):
    lines.append(
        f"LOG GAP    commits landed in eq-context today but sessions/{today}.md doesn't exist.\n"
        f"           CLAUDE.md Section 10 step 3 — insert it before this substrate goes stale for the next session."
    )

# --- 4. WORKTREES (F16) ----------------------------------------------------
wt_flags = []
for wt in worktree_paths():
    dirty_wt = git_at(wt, "status", "--porcelain")
    ahead_wt = git_at(wt, "rev-list", "--count", "origin/main..HEAD")
    ahead_n = int(ahead_wt) if ahead_wt and ahead_wt.isdigit() else 0
    if dirty_wt or ahead_n:
        bits = []
        if ahead_n:
            bits.append(f"{ahead_n} unpushed commit(s)")
        if dirty_wt:
            bits.append(f"{len(dirty_wt.splitlines())} uncommitted change(s)")
        wt_flags.append(f"           {wt} — {', '.join(bits)}")

if wt_flags:
    lines.append(
        f"WORKTREES  {len(wt_flags)} eq-context worktree(s) carry unlanded work:\n"
        + "\n".join(wt_flags) + "\n"
        "           Land it (scripts/safe_commit.py, or a normal push from inside\n"
        "           that worktree) or clean it up (ExitWorktree / git worktree\n"
        "           remove) — an orphan left behind is exactly how F16's three\n"
        "           abandoned worktrees accumulated. system/failures.md -> F16."
    )

if lines:
    print("=== EQ SESSION END GATE (informational — never blocks) ===")
    print("\n".join(lines))
    print("=== if none of this applies to what you worked on, ignore it ===")

sys.exit(0)
