#!/usr/bin/env python3
"""Sync eq-context markdown files to the Supabase context store.

Extracted from .github/workflows/sync-context.yml (2026-06-04) so the
slug-mapping and orphan-deletion logic can be unit-tested and run locally.
The GitHub Action invokes `python3 scripts/sync.py`.

Slug semantics are IDENTICAL to the previous inline script — do not change
them casually; every slug here is a live key in the context_files table and
in CLAUDE.md fetch URLs.

  - ROOT_FILES        → canonical short slug (claude, agents, cowork, readme)
  - other root *.md   → lowercased basename without extension (STATE.md → state)
  - subdirectory *.md → the repo-relative path itself (eq/pending.md → eq/pending.md)

Env:
  SUPABASE_URL                 (required)
  SUPABASE_SERVICE_ROLE_KEY    (required)
  MAX_ORPHAN_DELETE            (optional, default 15) — abort guard, see below
"""
import datetime
import glob
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

# Root entry-point files: slug → filename. Tier-separated structure (2026-05-04).
ROOT_FILES = {
    "claude": "CLAUDE.md",
    "agents": "AGENTS.md",
    "cowork": "COWORK-PROMPT.md",
    "readme": "README.md",
}

# Subdirectory glob patterns. Recursive (**) covers nested folders.
SUBDIR_PATTERNS = [
    "rules/**/*.md",
    "eq/**/*.md",
    "sks/**/*.md",
    "sks-team/**/*.md",
    "ops/**/*.md",
    "system/**/*.md",
    "archive/**/*.md",
    "sessions/**/*.md",
]

ROOT_MD_PATTERN = "*.md"
ROOT_EXPLICIT_FILES = set(ROOT_FILES.values())

# Orphan-delete safety cap. A bad edit to SUBDIR_PATTERNS (e.g. dropping
# 'eq/**') would make every slug under it look orphaned. Refuse implausibly
# large delete batches — that signals a pattern change, not real deletions.
DEFAULT_MAX_ORPHAN_ABS = 15
MAX_ORPHAN_FRAC = 0.25


# ----------------------------------------------------------------------
# Pure logic (unit-tested in test_sync.py — no network, no env)
# ----------------------------------------------------------------------
def compute_upserts(root="."):
    """Return an ordered list of (slug, filepath) pairs to upsert.

    filepath is repo-relative with forward slashes, matching the slug used
    for subdirectory files. `root` is prepended only for filesystem access.
    """
    pairs = []

    # Explicit root files (canonical slugs)
    for slug, filename in ROOT_FILES.items():
        pairs.append((slug, filename))

    # Other root-level *.md → lowercased basename without extension
    for filepath in sorted(glob.glob(os.path.join(root, ROOT_MD_PATTERN))):
        base = os.path.basename(filepath)
        if base in ROOT_EXPLICIT_FILES:
            continue
        slug = os.path.splitext(base)[0].lower()
        pairs.append((slug, base))

    # Subdirectory *.md → repo-relative path as slug
    for pattern in SUBDIR_PATTERNS:
        for filepath in sorted(glob.glob(os.path.join(root, pattern), recursive=True)):
            rel = os.path.relpath(filepath, root).replace(os.sep, "/")
            pairs.append((rel, rel))

    return pairs


def compute_current_slugs(root="."):
    """The full set of slugs that SHOULD exist, mirroring compute_upserts."""
    return {slug for slug, _ in compute_upserts(root)}


def find_orphans(current_slugs, existing_slugs):
    """Slugs present in the store but no longer produced by the file tree."""
    return sorted(s for s in existing_slugs if s not in current_slugs)


def orphan_delete_blocked(orphans, total_existing, max_abs):
    """True if the orphan batch is too large to delete safely.

    Returns (blocked: bool, reason: str|None).
    """
    n = len(orphans)
    frac = (n / total_existing) if total_existing else 0
    if n > max_abs:
        return True, f"{n} orphans exceeds absolute cap {max_abs}"
    if frac > MAX_ORPHAN_FRAC:
        return True, f"{n}/{total_existing} = {frac:.0%} exceeds {MAX_ORPHAN_FRAC:.0%}"
    return False, None


# ----------------------------------------------------------------------
# Network side-effects (not unit-tested; exercised in CI against live store)
# ----------------------------------------------------------------------
def _headers(service_key, extra=None):
    h = {"apikey": service_key, "Authorization": f"Bearer {service_key}"}
    if extra:
        h.update(extra)
    return h


def upsert(base_url, service_key, slug, filepath, synced):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"  {slug}: {filepath} not found — skipping")
        return

    payload = json.dumps({
        "slug": slug,
        "filename": filepath,
        "content": content,
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{base_url}/rest/v1/context_files?on_conflict=slug",
        data=payload,
        headers=_headers(service_key, {
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates,return=minimal",
        }),
        method="POST",
    )
    try:
        with urllib.request.urlopen(req):
            print(f"  {slug}: synced ({len(content)} chars)")
            synced.add(slug)
    except urllib.error.HTTPError as e:
        print(f"  {slug}: ERROR {e.code} - {e.read().decode()}")
        raise


def fetch_existing_slugs(base_url, service_key):
    url = f"{base_url}/rest/v1/context_files?select=slug&limit=10000"
    req = urllib.request.Request(url, headers=_headers(service_key), method="GET")
    with urllib.request.urlopen(req) as resp:
        return [row["slug"] for row in json.loads(resp.read())]


def verify_freshness(base_url, service_key, synced):
    if not synced:
        print("  (no slugs synced - nothing to verify)")
        return
    slugs_param = ",".join(urllib.parse.quote(s, safe="") for s in sorted(synced))
    url = (f"{base_url}/rest/v1/context_files"
           f"?slug=in.({slugs_param})&select=slug,updated_at")
    req = urllib.request.Request(url, headers=_headers(service_key), method="GET")
    with urllib.request.urlopen(req) as resp:
        rows = json.loads(resp.read())

    by_slug = {row["slug"]: row["updated_at"] for row in rows}
    now = datetime.datetime.now(datetime.timezone.utc)
    threshold = datetime.timedelta(seconds=60)
    failures = []
    for slug in sorted(synced):
        ts = by_slug.get(slug)
        if ts is None:
            failures.append(f"{slug}: NOT FOUND post-upsert")
            continue
        age = now - datetime.datetime.fromisoformat(ts)
        if age > threshold:
            failures.append(f"{slug}: STALE ({int(age.total_seconds())}s old)")
        else:
            print(f"  {slug}: fresh ({int(age.total_seconds())}s)")

    if failures:
        print("=== VERIFICATION FAILED ===")
        for f in failures:
            print(f"  {f}")
        raise SystemExit(1)
    print("=== Verification passed ===")


def delete_orphans(base_url, service_key, orphans):
    for slug in orphans:
        encoded = urllib.parse.quote(slug, safe="")
        req = urllib.request.Request(
            f"{base_url}/rest/v1/context_files?slug=eq.{encoded}",
            headers=_headers(service_key, {"Prefer": "return=minimal"}),
            method="DELETE",
        )
        try:
            with urllib.request.urlopen(req):
                print(f"  Deleted orphan: {slug}")
        except urllib.error.HTTPError as e:
            print(f"  ERROR deleting {slug}: {e.code} - {e.read().decode()}")
            raise


def main():
    base_url = os.environ["SUPABASE_URL"]
    service_key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    max_abs = int(os.environ.get("MAX_ORPHAN_DELETE", DEFAULT_MAX_ORPHAN_ABS))

    synced = set()
    print("=== Syncing context files ===")
    for slug, filepath in compute_upserts("."):
        upsert(base_url, service_key, slug, filepath, synced)

    print("=== Verifying freshness ===")
    verify_freshness(base_url, service_key, synced)

    print("=== Checking for orphaned rows ===")
    existing = fetch_existing_slugs(base_url, service_key)
    current = compute_current_slugs(".")
    orphans = find_orphans(current, existing)

    if not orphans:
        print("  No orphaned rows found.")
        print("Done.")
        return

    blocked, reason = orphan_delete_blocked(orphans, len(existing), max_abs)
    if blocked:
        print("=== ORPHAN DELETE ABORTED (safety cap) ===")
        print(f"  {reason}. This usually means a glob pattern changed, not that "
              f"{len(orphans)} files were deleted.")
        print("  Slugs that WOULD have been removed:")
        for slug in orphans:
            print(f"    - {slug}")
        print("  If intentional, re-run with MAX_ORPHAN_DELETE above the count.")
        raise SystemExit(1)

    print(f"  Found {len(orphans)} orphaned slug(s) — removing.")
    delete_orphans(base_url, service_key, orphans)
    print(f"  Removed {len(orphans)} orphaned row(s).")
    print("Done.")


if __name__ == "__main__":
    sys.exit(main())
