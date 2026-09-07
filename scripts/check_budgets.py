#!/usr/bin/env python3
"""Check every tracked markdown file with a stated **Budget:** line against its
current size, and report which are over.

Written 2026-09-07 (rules/tidy-protocol.md Step 5, Pass Log row (c)) to close the
exact gap rules/agentic-coding.md Section 3 warns about: "prefer a structural
guard over a documented rule ... where a mistake can be made impossible, build
that instead of writing the reminder." A `**Budget: ~N lines**` sentence a file
carries on its own is a reminder nothing enforces -- this is the enforcement.

Discovers budgeted files automatically (scans every tracked *.md for the literal
string "**Budget:**") rather than hardcoding a file list, so a future /tidy pass
that adds a budget to a new file is picked up here for free, with nothing to
maintain in this script.

Usage:
    python scripts/check_budgets.py       # human-readable report
    python scripts/check_budgets.py --ci  # same, but quiet on a clean pass (exit code only)

Exit code 0 if every budgeted file is within budget, 1 if any is over -- or if a
file declares a Budget: line this script couldn't parse a number out of, which is
treated as a failure so a malformed budget note doesn't silently stop being
checked.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

BUDGET_PARAGRAPH_RE = re.compile(r"\*\*Budget:\*\*(.*?)(?:\n\s*\n|\Z)", re.DOTALL)
BUDGET_NUMBER_RE = re.compile(r"~?(\d+)\s*lines")


def repo_root(start: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], cwd=str(start),
        capture_output=True, text=True, check=True,
    )
    return Path(result.stdout.strip())


def tracked_markdown_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "*.md"], cwd=str(root),
        capture_output=True, text=True, check=True,
    )
    return [root / line for line in result.stdout.splitlines() if line.strip()]


def extract_budget(text: str) -> int | None:
    """Return the stated line-count budget, or None if the file has no
    **Budget:** marker. Raises ValueError if it has one but no parseable number
    nearby -- that's a malformed note, not an absent one, and should fail loud
    rather than silently stop being checked."""
    para_match = BUDGET_PARAGRAPH_RE.search(text)
    if not para_match:
        return None
    num_match = BUDGET_NUMBER_RE.search(para_match.group(1))
    if not num_match:
        raise ValueError(
            "found a **Budget:** marker but no parseable '<number> lines' near it: "
            f"{para_match.group(1)[:120]!r}"
        )
    return int(num_match.group(1))


def check_all(
    root: Path,
) -> tuple[list[tuple[str, int, int]], list[tuple[str, int, int]], list[tuple[str, str]]]:
    """Returns (ok, over, errors) -- ok/over are (path, budget, actual) triples,
    errors are (path, message) pairs for files with an unparseable budget."""
    ok: list[tuple[str, int, int]] = []
    over: list[tuple[str, int, int]] = []
    errors: list[tuple[str, str]] = []

    for path in tracked_markdown_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue  # not every tracked .md is guaranteed readable as utf-8; skip rather than crash

        try:
            budget = extract_budget(text)
        except ValueError as exc:
            errors.append((str(path.relative_to(root)).replace("\\", "/"), str(exc)))
            continue
        if budget is None:
            continue

        actual = len(text.splitlines())
        rel = str(path.relative_to(root)).replace("\\", "/")
        (over if actual > budget else ok).append((rel, budget, actual))

    return ok, over, errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--ci", action="store_true", help="quiet on a clean pass; only print failures")
    args = parser.parse_args()

    root = repo_root(Path.cwd())
    ok, over, errors = check_all(root)

    if not args.ci or over or errors:
        if ok:
            print(f"Within budget ({len(ok)}):")
            for rel, budget, actual in sorted(ok):
                print(f"  OK    {rel}  {actual}/{budget} lines")

    if over:
        print(f"\nOVER BUDGET ({len(over)}):")
        for rel, budget, actual in sorted(over):
            print(f"  OVER  {rel}  {actual}/{budget} lines (+{actual - budget})")

    if errors:
        print(f"\nUNPARSEABLE Budget: marker ({len(errors)}):")
        for rel, msg in sorted(errors):
            print(f"  ERR   {rel}  {msg}")

    if not ok and not over and not errors:
        print("No file in the repo declares a **Budget:** marker.")

    return 1 if (over or errors) else 0


if __name__ == "__main__":
    sys.exit(main())
