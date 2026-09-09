#!/usr/bin/env python3
"""Register a new dedicated per-tenant Supabase project for nightly backup.

Automates the two NON-SECRET steps of adding tenant backup coverage (see
.github/workflows/backup-tenants.yml's own header for why a third step --
adding the actual DB URL secret -- can't be automated away: GitHub Actions
can't look up a secret by a name computed at runtime, and Supabase doesn't
expose a project's DB password via the Management API after creation).

This script NEVER touches the secret value itself -- it only writes the
registry entry and the workflow's secret-mapping env line, both git-tracked,
neither containing anything sensitive. Run it, then set the actual secret
yourself (this script prints the exact command at the end).

Usage:
    python scripts/register_tenant_backup.py --slug madagins --project-ref ornndtbdkxfsewspbrwk

Writes two files only -- doesn't commit or push. Land the result with
scripts/safe_commit.py same as any other substrate change (F16 convention).
"""
import argparse
import json
import re
import sys
from datetime import timezone, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY_PATH = HERE.parent / "eq" / "identity" / "tenant-projects.json"
WORKFLOW_PATH = HERE.parent / ".github" / "workflows" / "backup-tenants.yml"

SLUG_RE = re.compile(r"^[a-z][a-z0-9-]{1,40}$")
ENV_LINE_RE = re.compile(r"^(\s+)TENANT_\w+_DB_URL: \$\{\{ secrets\.TENANT_\w+_DB_URL \}\}\s*\n?$")


def secret_name(slug: str) -> str:
    return f"TENANT_{slug.upper().replace('-', '_')}_DB_URL"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--slug", required=True, help="short tenant identifier, e.g. 'madagins' (lowercase, letters/digits/hyphens)")
    parser.add_argument("--project-ref", required=True, help="the tenant's dedicated Supabase project ref")
    args = parser.parse_args()

    slug = args.slug.strip().lower()
    if not SLUG_RE.match(slug):
        print(f"error: --slug {args.slug!r} doesn't look like a slug (lowercase letters/digits/hyphens, starting with a letter)", file=sys.stderr)
        return 1

    secret = secret_name(slug)

    # --- 1. registry (eq/identity/tenant-projects.json) ---
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    if any(t["slug"] == slug for t in registry["tenants"]):
        print(f"error: {slug!r} is already registered in {REGISTRY_PATH}", file=sys.stderr)
        return 1
    registry["tenants"].append({
        "slug": slug,
        "project_ref": args.project_ref,
        "db_url_secret": secret,
        "created": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    })
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"[registry] added {slug!r} -> {REGISTRY_PATH}")

    # --- 2. workflow env line (.github/workflows/backup-tenants.yml) ---
    text = WORKFLOW_PATH.read_text(encoding="utf-8")
    if secret in text:
        print(f"error: {secret!r} already referenced in {WORKFLOW_PATH} -- registry/workflow were out of sync", file=sys.stderr)
        return 1

    lines = text.splitlines(keepends=True)
    last_idx = None
    indent = "      "
    for i, line in enumerate(lines):
        m = ENV_LINE_RE.match(line)
        if m:
            last_idx = i
            indent = m.group(1)
    if last_idx is None:
        print(f"error: couldn't find an existing 'TENANT_*_DB_URL: ${{{{ secrets... }}}}' env line in {WORKFLOW_PATH} to insert after -- add it by hand:", file=sys.stderr)
        print(f"  {indent}{secret}: ${{{{ secrets.{secret} }}}}", file=sys.stderr)
        return 1

    new_line = f"{indent}{secret}: ${{{{ secrets.{secret} }}}}\n"
    lines.insert(last_idx + 1, new_line)
    WORKFLOW_PATH.write_text("".join(lines), encoding="utf-8", newline="\n")
    print(f"[workflow] added env line for {secret!r} -> {WORKFLOW_PATH}")

    print()
    print("Two files changed, both git-tracked, neither contains anything sensitive.")
    print("Land them the normal way, e.g.:")
    print(f'  python scripts/safe_commit.py -m "feat(dr): register tenant {slug} for backup" \\')
    print(f"    eq/identity/tenant-projects.json .github/workflows/backup-tenants.yml")
    print()
    print("Then set the actual secret YOURSELF (never paste a DB URL into an AI session):")
    print(f"  gh secret set {secret} --env production-ops")
    print("  (prompts for the value interactively -- paste it there, not on the command line)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
