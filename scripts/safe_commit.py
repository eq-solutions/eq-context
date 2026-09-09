#!/usr/bin/env python3
"""Stable bootstrap for scripts/_safe_commit_impl.py -- fetches origin/main and
execs the CURRENT implementation from there, never this worktree's own
possibly-stale on-disk copy of it.

Why this file exists at all: before it, this script's own guard logic (e.g.
check_upstream_divergence, check_script_currency) only protected a caller
whose local checkout already had the fix -- git fetch refreshes the
origin/main *ref*, not a worktree's own checked-out files, so a worktree
that forked before a fix landed silently ran the old, less-safe version for
as long as it went unsynced (system/failures.md F17, second occurrence: one
shared checkout sat two hours stale relative to a same-day fix and kept
running pre-fix logic for the next 11+ hours, with nothing anywhere warning
that its safety net was out of date).

This file's own job is to almost never need to change: fetch, `git show` the
current implementation, write it to a temp file, exec it with this
invocation's own argv, forward its exit code. Every actual safe_commit
*behavior* now lives in scripts/_safe_commit_impl.py and is re-fetched fresh
on every single call -- so a worktree that never syncs again after reading
THIS file still always runs current logic, because it never actually runs
the on-disk copy of the logic at all. The old single-file design put the
frequently-changing logic and the trust boundary in the same file, so a fix
to one was a fix to the other, and staleness in the file meant staleness in
the guard. Splitting them means only THIS trivial, rarely-touched file needs
to have synced even once -- after that, freshness is no longer something a
caller has to remember to maintain.

Usage (identical to before -- this bootstrap forwards every argument
untouched to the fetched implementation):
    python scripts/safe_commit.py -m "commit message" path/to/file1 path/to/file2
    python scripts/safe_commit.py --dry-run -m "..." path/to/file
    python scripts/safe_commit.py --force -m "..." path/to/file

To test a local, uncommitted edit to scripts/_safe_commit_impl.py before
pushing it, invoke that file directly instead of going through this
bootstrap: `python scripts/_safe_commit_impl.py ...` -- deliberately bypasses
the fetch-fresh behavior below and runs exactly what's on disk.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

IMPL_PATH = "scripts/_safe_commit_impl.py"


def main() -> int:
    caller_cwd = Path.cwd()

    root_result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], cwd=str(caller_cwd), capture_output=True, text=True
    )
    if root_result.returncode != 0:
        print(f"error: not inside a git repo ({root_result.stderr.strip()})", file=sys.stderr)
        return 1
    root = Path(root_result.stdout.strip())

    fetch = subprocess.run(
        ["git", "fetch", "origin", "main", "--quiet"], cwd=str(root), capture_output=True, text=True
    )
    if fetch.returncode != 0:
        print(f"error: git fetch origin main failed:\n{fetch.stderr}", file=sys.stderr)
        return 1

    show = subprocess.run(
        ["git", "show", f"origin/main:{IMPL_PATH}"], cwd=str(root), capture_output=True
    )
    if show.returncode != 0:
        print(
            f"error: origin/main has no {IMPL_PATH} -- cannot fetch the current "
            "implementation. Has it moved or been renamed? (stderr: "
            f"{show.stderr.decode(errors='replace').strip()})",
            file=sys.stderr,
        )
        return 1

    tmp_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(suffix="_safe_commit_impl.py", delete=False) as tmp:
            tmp.write(show.stdout)
            tmp_path = tmp.name

        result = subprocess.run([sys.executable, tmp_path, *sys.argv[1:]], cwd=str(caller_cwd))
        return result.returncode
    finally:
        if tmp_path is not None:
            try:
                Path(tmp_path).unlink()
            except OSError:
                pass


if __name__ == "__main__":
    sys.exit(main())
