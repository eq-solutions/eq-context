#!/usr/bin/env python3
"""No two session logs may hold byte-identical content.

Why (2026-08-15). This check has existed since at least 2026-06 in
scripts/md-health-daily.py -- a Beelink-only script nothing has ever run in
CI. It found none of the 34 checks that script performs were exempt from
that gap; two were superseded by better versions built today
(review_clock.py, link_check.py) and one -- session filename shape -- was
already independently covered by md-health.yml's own rule 17.4. This is the
one real, portable gap left: nothing anywhere checks that two session logs
don't hold the exact same content, which is the specific failure a bad
copy-paste or a botched merge produces (write today's log, accidentally
save yesterday's content into it, or duplicate a file during a branch
reconciliation).

Content, not filename -- two files can legitimately share a filename
pattern (both matching YYYY-MM-DD[-slug].md, rule 17.4's job) while one is
a byte-for-byte accidental copy of the other. That's what this catches:
identical content under two different paths, which rule 17.4 has no way to
see.

Run:   python scripts/duplicate_sessions.py
Gate:  exit 1 if any two session files are byte-identical.
       DUPLICATE_SESSIONS_REPORT=1 reports without gating.
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SESSIONS_DIR = os.path.join(ROOT, "sessions")


def find_duplicates(paths_and_bytes):
    """paths_and_bytes: [(relative_path, content_bytes)]. Returns pairs of
    (first_path, later_path) for every later file whose content exactly
    matches an earlier one. Pure -- no filesystem, so directly testable.

    Order matters only for which path is reported as "first" (the one
    already indexed) vs "later" (the duplicate) -- callers should pass a
    stable order (e.g. sorted by path) so results are deterministic.
    """
    seen = {}
    duplicates = []
    for path, content in paths_and_bytes:
        digest = hashlib.sha1(content).hexdigest()
        if digest in seen:
            duplicates.append((seen[digest], path))
        else:
            seen[digest] = path
    return duplicates


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if not os.path.isdir(SESSIONS_DIR):
        print(f"--- Duplicate session content scan ---\n\n  {SESSIONS_DIR} not found, skipped")
        return 0

    files = sorted(f for f in os.listdir(SESSIONS_DIR) if f.endswith(".md"))
    paths_and_bytes = []
    for f in files:
        with open(os.path.join(SESSIONS_DIR, f), "rb") as fh:
            paths_and_bytes.append((f, fh.read()))

    duplicates = find_duplicates(paths_and_bytes)

    print("--- Duplicate session content scan ---\n")
    print(f"  {len(files)} session file(s) checked, {len(duplicates)} duplicate pair(s)\n")
    for first, later in duplicates:
        print(f"  DUPLICATE  {later}  is byte-identical to  {first}")

    print()
    if duplicates:
        print(f"FAIL: {len(duplicates)} duplicate session file(s) found")
        print(
            "\n  Two session logs with identical content is almost always a copy-paste\n"
            "  or merge accident, not two genuinely identical days -- check which one\n"
            "  is real and delete or rewrite the other."
        )
        if os.environ.get("DUPLICATE_SESSIONS_REPORT") == "1":
            print("\n  (DUPLICATE_SESSIONS_REPORT=1 — reporting only, not gating)")
            return 0
        return 1

    print("ok: no two session files share identical content")
    return 0


if __name__ == "__main__":
    sys.exit(main())
