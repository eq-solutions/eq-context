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
  1. DIRTY     — eq-context has uncommitted changes sitting in the working tree.
  2. UNPUSHED  — local main is ahead of origin/main (the courier's push half is
                 still manual — see UserPromptSubmit's auto-pull, which only
                 covers the pull side).
  3. LOG GAP   — commits landed in eq-context today but no sessions/<today>.md
                 exists to record what happened.

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
            f"           git -C C:\\Projects\\eq-context push origin main\n"
            f"           (already allow-listed in settings.json — nothing new to approve)"
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

if lines:
    print("=== EQ SESSION END GATE (informational — never blocks) ===")
    print("\n".join(lines))
    print("=== if none of this applies to what you worked on, ignore it ===")

sys.exit(0)
