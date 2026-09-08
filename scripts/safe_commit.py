#!/usr/bin/env python3
"""Commit + push specific files to origin/main via a throwaway isolated worktree.

Why: this shared checkout regularly carries another live session's uncommitted
work (see system/failures.md F9). A direct `git add <file> && git commit` in the
main checkout risks sweeping that up (a targeted `git add` swept up three
unrelated staged files on 2026-08-04 -- see hooks/pre_tool_use.py), and a direct
`git commit` is blocked outright when the checkout is behind origin/main
(eq-guard's stale-main-gate). This script does the safe version instead: fetch,
branch off a fresh origin/main in a scratch worktree, copy in exactly the given
files from the caller's working tree, commit, push (rebasing and retrying on a
non-fast-forward race), then tear the worktree down. It never reads or writes
any *other* file's state in the caller's own working tree or index -- the only
thing it touches there, on a successful push, is unstaging the files just
pushed (see --no-unstage), so `git status` doesn't misleadingly show
already-shipped work as still pending.

Before touching anything, it also checks each requested file for upstream
divergence: if origin/main's current copy differs from what the caller's own
HEAD had for that path, someone else has pushed a change to it since the
caller last synced. Copying the caller's (now-stale) bytes over a scratch
worktree branched fresh off that same origin/main would silently discard the
other push, so this refuses and prints a diff instead, unless --force. This is
the same failure shape as system/failures.md F12 (a blind overwrite of a
concurrent session's already-pushed edits), reached here through a mechanism
F12's own cp/mv/xcopy guard can't see: this script's copy step is a Python
`write_bytes` call into a scratch worktree, never a shell copy command against
the bare checkout.

Usage:
    python scripts/safe_commit.py -m "commit message" path/to/file1 path/to/file2

    python scripts/safe_commit.py --dry-run -m "..." path/to/file
        Do everything up to (not including) the push; leaves the scratch
        worktree in place for inspection instead of tearing it down.

    python scripts/safe_commit.py --force -m "..." path/to/file
        Skip the upstream-divergence check below and overwrite origin/main's
        current copy of the requested file(s) with the caller's bytes
        regardless. For a deliberate wholesale replace -- not the default,
        because the default is what turns the other failure mode loud
        instead of silent.

This does NOT resolve content conflicts. When origin/main has moved since the
caller's own HEAD for a requested file, the script refuses to proceed and
prints what changed (`git log HEAD..origin/main -- <file>` shows the full
history) -- reconciling the content is still the caller's call to make. The
divergence check only looks at paths requested on this invocation, and only
against the caller's own HEAD as the baseline, not a full three-way merge --
it catches "the file moved upstream since I last read it," not every possible
conflict shape.
"""
from __future__ import annotations

import argparse
import difflib
import secrets
import subprocess
import sys
import time
from pathlib import Path


def run(args: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(args, cwd=str(cwd), capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(
            f"command failed: {' '.join(args)}\n"
            f"cwd: {cwd}\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )
    return result


def repo_root(start: Path) -> Path:
    return Path(run(["git", "rev-parse", "--show-toplevel"], cwd=start).stdout.strip())


def show_at_ref(root: Path, ref: str, rel: str) -> bytes | None:
    """Raw bytes of `rel` at `ref` in `root`, or None if it doesn't exist there."""
    result = subprocess.run(["git", "show", f"{ref}:{rel}"], cwd=str(root), capture_output=True)
    return result.stdout if result.returncode == 0 else None


def resolve_files(files: list[str], caller_cwd: Path, root: Path) -> dict[str, bytes]:
    """Validate every requested path exists and read its current bytes now,
    before anything else (a fetch, a rebase) can change under us."""
    out: dict[str, bytes] = {}
    for f in files:
        candidate = Path(f)
        src = candidate if candidate.is_absolute() else (caller_cwd / f)
        if not src.is_file():
            src = root / f  # caller may have passed a repo-relative path from elsewhere in the tree
        if not src.is_file():
            raise SystemExit(
                f"error: {f!r} is not a file (checked {caller_cwd / f} and {root / f})"
            )
        rel = src.resolve().relative_to(root.resolve())
        out[str(rel).replace("\\", "/")] = src.read_bytes()
    return out


def check_upstream_divergence(root: Path, file_contents: dict[str, bytes], force: bool) -> bool:
    """Compare origin/main's current copy of each requested file against what
    the caller's own HEAD had for that path -- a proxy for the base the caller
    last read/edited from. If they differ, origin/main moved since then;
    blindly copying the caller's bytes over a scratch worktree branched fresh
    off that same origin/main would silently discard whatever changed there.
    Returns False (having already printed why) if the caller should stop,
    unless --force."""
    conflicts: list[tuple[str, bytes | None, bytes | None]] = []
    for rel in sorted(file_contents):
        base = show_at_ref(root, "HEAD", rel)
        upstream = show_at_ref(root, "origin/main", rel)
        if base == upstream:
            continue  # origin/main hasn't moved past the caller's own HEAD for this file
        if file_contents[rel] == upstream:
            continue  # caller's bytes already match origin/main -- nothing would be lost
        conflicts.append((rel, base, upstream))

    if not conflicts:
        return True

    print(
        f"SAFETY CHECK FAILED: origin/main has moved since your HEAD for "
        f"{len(conflicts)} requested file(s) -- committing now would silently "
        "overwrite whatever changed there. Re-merge first (`git log HEAD..origin/main "
        "-- <file>` shows the history), or rerun with --force to overwrite anyway.",
        file=sys.stderr,
    )
    for rel, base, upstream in conflicts:
        print(f"\n--- {rel} (your HEAD -> origin/main) ---", file=sys.stderr)
        before = (base or b"").decode("utf-8", errors="replace").splitlines(keepends=True)
        after = (upstream or b"").decode("utf-8", errors="replace").splitlines(keepends=True)
        sys.stderr.writelines(
            difflib.unified_diff(before, after, fromfile="your HEAD", tofile="origin/main")
        )

    if force:
        print("\n--force given -- overwriting origin/main's changes anyway.", file=sys.stderr)
        return True

    return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-m", "--message", required=True, help="commit message")
    parser.add_argument(
        "files", nargs="+", help="repo-relative paths to commit, as they currently exist on disk"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="stop before pushing; leave the scratch worktree for inspection",
    )
    parser.add_argument(
        "--no-unstage", action="store_true",
        help="don't unstage the pushed files in the caller's own checkout afterward",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="skip the upstream-divergence check and overwrite origin/main's current "
        "copy of the requested file(s) regardless",
    )
    parser.add_argument(
        "--max-retries", type=int, default=5,
        help="max fetch+rebase+push retries on a non-fast-forward race (default 5)",
    )
    args = parser.parse_args()

    caller_cwd = Path.cwd()
    root = repo_root(caller_cwd)
    file_contents = resolve_files(args.files, caller_cwd, root)

    print(f"Repo root: {root}")
    print(f"Files ({len(file_contents)}): {', '.join(sorted(file_contents))}")

    print("Fetching origin/main...")
    run(["git", "fetch", "origin", "main", "--quiet"], cwd=root)

    if not check_upstream_divergence(root, file_contents, args.force):
        return 1

    stamp = time.strftime("%Y%m%d-%H%M%S")
    wt_name = f"safe-commit-{stamp}-{secrets.token_hex(3)}"
    wt_path = root / ".claude" / "worktrees" / wt_name
    branch = f"chore/{wt_name}"

    print(f"Creating scratch worktree {wt_path} off origin/main on branch {branch}...")
    run(["git", "worktree", "add", "-b", branch, str(wt_path), "origin/main"], cwd=root)

    def cleanup() -> None:
        print(f"Cleaning up scratch worktree {wt_path}...")
        run(["git", "worktree", "remove", str(wt_path), "--force"], cwd=root, check=False)
        run(["git", "branch", "-D", branch], cwd=root, check=False)

    try:
        for rel, content in file_contents.items():
            dest = wt_path / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content)

        rel_paths = sorted(file_contents.keys())
        run(["git", "add", "--", *rel_paths], cwd=wt_path)

        status = run(["git", "status", "--porcelain"], cwd=wt_path)
        staged_paths = {line[3:].strip() for line in status.stdout.splitlines()}
        expected = set(rel_paths)
        unexpected = staged_paths - expected
        missing = expected - staged_paths  # requested file byte-identical to origin/main already

        if unexpected:
            print(
                f"SAFETY CHECK FAILED: unexpected files staged that weren't requested: {unexpected}\n"
                "This should be impossible (only requested paths were `git add`ed) -- aborting "
                f"without committing. Scratch worktree preserved at {wt_path} for inspection.",
                file=sys.stderr,
            )
            return 1

        if missing:
            print(f"Note: already matches origin/main exactly, nothing to stage: {sorted(missing)}")

        if not staged_paths:
            print("Nothing to commit -- every requested file already matches origin/main.")
            return 0

        print(f"Staged {len(staged_paths)} file(s): {sorted(staged_paths)}")

        run(["git", "commit", "-m", args.message], cwd=wt_path)
        commit_sha = run(["git", "rev-parse", "HEAD"], cwd=wt_path).stdout.strip()
        print(f"Committed locally: {commit_sha}")

        if args.dry_run:
            print(
                f"--dry-run: stopping before push. Scratch worktree left at {wt_path}.\n"
                f"  To finish by hand:  git -C \"{wt_path}\" push origin HEAD:main\n"
                f"  To discard instead: git worktree remove \"{wt_path}\" --force "
                f"&& git branch -D {branch}"
            )
            return 0

        pushed = False
        for attempt in range(1, args.max_retries + 1):
            run(["git", "fetch", "origin", "main", "--quiet"], cwd=wt_path)
            push = run(["git", "push", "origin", "HEAD:main"], cwd=wt_path, check=False)
            if push.returncode == 0:
                print(f"Pushed to origin/main (attempt {attempt}).")
                pushed = True
                break
            race = any(s in push.stderr for s in ("non-fast-forward", "fetch first", "stale info"))
            if not race:
                print(push.stderr, file=sys.stderr)
                print(
                    f"Push failed for a reason other than a race. Scratch worktree "
                    f"preserved at {wt_path}.", file=sys.stderr,
                )
                return 1
            print(f"Push rejected (attempt {attempt}/{args.max_retries}) -- origin/main moved. "
                  "Rebasing and retrying...")
            run(["git", "rebase", "origin/main"], cwd=wt_path)

        if not pushed:
            print(
                f"Gave up after {args.max_retries} push attempts -- origin/main is moving faster "
                f"than this script can keep up. The commit is safe on local branch {branch!r} in "
                f"{wt_path} -- push it by hand once things settle: "
                f"git -C \"{wt_path}\" push origin HEAD:main",
                file=sys.stderr,
            )
            return 1

        final_sha = run(["git", "rev-parse", "HEAD"], cwd=wt_path).stdout.strip()
        print(f"Live on origin/main: {final_sha}")

        if not args.no_unstage:
            run(["git", "restore", "--staged", "--", *sorted(staged_paths)], cwd=root, check=False)

    except Exception as exc:  # noqa: BLE001 - deliberately broad: any failure must preserve evidence
        print(f"error: {exc}", file=sys.stderr)
        print(
            f"Scratch worktree preserved at {wt_path} for inspection -- not auto-cleaned on error.",
            file=sys.stderr,
        )
        return 1

    cleanup()
    return 0


if __name__ == "__main__":
    sys.exit(main())
