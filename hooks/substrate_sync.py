#!/usr/bin/env python3
"""UserPromptSubmit hook — keep the substrate clone current, and say so when it isn't.

Why this file exists (2026-08-15). The wiring used to carry its own logic inline
in C:/Users/EQ/.claude/settings.json:

    git -C <repo> pull --ff-only origin main *>$null

Three faults, all of which cost a session:

1. `*>$null` swallowed the failure. Once branches diverge git refuses to
   fast-forward, so the pull stopped working and nothing said so.
2. Nothing compared HEAD against origin/main afterwards, so a clone could sit
   34 commits behind while every gate reported green.
3. The logic lived only in settings.json — a file in a local-only git repo with
   no remote, edited concurrently by other sessions, and covered by no test.
   settings.template.json (the governed copy) did not carry this hook at all,
   so there was nothing to drift *from*.

The cost, observed 2026-08-15: the session-start gate announced
"F13 (rung 1, 2x) PROMOTION DUE" off the stale clone when origin/main already
had F13 at rung 4 with the guard built and merged.

Per the template's own rule — logic in the governed repo, wiring only in
settings.json — that inline blob is now this file, which is versioned, tested
(hooks/test_substrate_sync.py) and shared by every machine that clones eq-context.

Fails open, always exit 0: a broken sync check must never block a prompt.
"""
import os
import subprocess
import sys
import time

REPO = os.environ.get("EQ_CONTEXT", r"C:\Projects\eq-context")
FETCH_MAX_AGE_SECONDS = 600


def git(*args, timeout=20):
    """Return stdout on success, empty string on any failure. Never raises."""
    try:
        r = subprocess.run(
            ("git", "-C", REPO) + args, capture_output=True, text=True, timeout=timeout
        )
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def refresh_remote_ref():
    """Fetch if the last one is stale, so origin/main is worth comparing against.

    A pull that cannot fast-forward still needs to leave origin/main current --
    otherwise the divergence it just refused to resolve is also invisible to the
    comparison below. That fallback is the whole point.
    """
    try:
        fetch_head = os.path.join(REPO, ".git", "FETCH_HEAD")
        age = time.time() - os.path.getmtime(fetch_head)
        if age <= FETCH_MAX_AGE_SECONDS:
            return
    except Exception:
        pass  # missing or unreadable FETCH_HEAD -> treat as stale, fetch below

    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if branch == "main":
        before = git("rev-parse", "HEAD")
        git("pull", "--ff-only", "origin", "main", timeout=30)
        after = git("rev-parse", "HEAD")
        if before and after and before == after:
            # Pull was a no-op or was refused. Either way make sure the remote
            # ref is current so the comparison below is meaningful.
            git("fetch", "origin", "main", timeout=30)
    else:
        git("fetch", "origin", "main", timeout=30)


def main():
    if not os.path.isdir(os.path.join(REPO, ".git")):
        return

    refresh_remote_ref()

    local = git("rev-parse", "HEAD")
    remote = git("rev-parse", "origin/main")
    if not local or not remote or local == remote:
        return

    # Only BEHIND is staleness -- ahead is unpushed local work, the normal state
    # of any feature branch. Warning on that would fire this hook on nearly
    # every prompt, and a warning that always fires is one nobody reads.
    behind = int(git("rev-list", "--count", f"{local}..{remote}") or 0)
    if not behind:
        return

    ahead = int(git("rev-list", "--count", f"{remote}..{local}") or 0)
    print(
        f"*** SUBSTRATE OUT OF SYNC *** {REPO} is behind {behind}"
        + (f" / ahead {ahead}" if ahead else "")
        + f" vs origin/main. Files you read from it may be stale, and a current "
        f"digest.md stamp does NOT mean the clone is current (failure F1). "
        f"Reconcile before trusting substrate content."
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
