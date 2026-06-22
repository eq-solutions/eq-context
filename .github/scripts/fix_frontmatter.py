#!/usr/bin/env python3
"""One-shot: add missing frontmatter keys to all violating files."""

import re, sys
from pathlib import Path

ROOT = Path(".")

FIXES = {
    "SPRINT-BOARD.md": {
        "_move_comment": True,  # HTML comment is before ---
    },
    "_ws1-customer-dedup-2026-06-07.md": {
        "owner": "Royce Milmlow", "last_updated": "2026-06-07",
        "read_priority": "reference", "status_override": "archived",
    },
    "_ws2-site-customer-backfill-2026-06-07.md": {
        "owner": "Royce Milmlow", "last_updated": "2026-06-07",
        "read_priority": "reference", "status_override": "archived",
    },
    "canonical-wiring-activation-status-2026-06-07.md": {
        "owner": "Royce Milmlow", "last_updated": "2026-06-07",
        "scope": "Canonical wiring activation log — what shipped 2026-06-07 and what remained gated",
        "read_priority": "reference", "status_override": "archived",
    },
    "canonical-wiring-deploy-runbook-2026-06-07.md": {
        "owner": "Royce Milmlow", "last_updated": "2026-06-07",
        "scope": "6-step canonical wiring deploy runbook built 2026-06-07 — superseded by live system",
        "read_priority": "reference", "status_override": "archived",
    },
    "cross-app-linkage-audit-2026-06-07.md": {
        "owner": "Royce Milmlow", "last_updated": "2026-06-07",
        "scope": "Cross-app linkage audit across 4 Supabase projects and 5 repos — 2026-06-07 snapshot",
        "read_priority": "reference", "status_override": "archived",
    },
    "cross-app-linkage-remediation-plan-2026-06-07.md": {
        "last_updated": "2026-06-07",
        "scope": "Remediation plan for cross-app linkage gaps found 2026-06-07 — superseded by live wiring",
        "read_priority": "reference", "status_override": "archived",
    },
    "cross-app-linkage-sprint-2026-06-07.md": {
        "last_updated": "2026-06-07",
        "scope": "Sprint plan for cross-app linkage convergence — 2026-06-07, now complete",
        "read_priority": "reference", "status_override": "archived",
    },
    "platform-architecture-audit-2026-06-02.md": {
        "owner": "Royce Milmlow", "read_priority": "reference",
    },
    "sprint-2026-06-08-ui-consistency.md": {
        "read_priority": "reference",
    },
    "system/worktree-registry.md": {
        "_no_fm": True,
        "title": "Worktree Registry",
        "owner": "Royce Milmlow", "last_updated": "2026-06-22",
        "scope": "Active and stale git worktrees — check before creating a new one",
        "read_priority": "critical", "status": "live",
    },
    "worker-identity-linker-spec-2026-06-07.md": {
        "_no_fm": True,
        "title": "Worker Identity Linker — Spec",
        "owner": "Royce Milmlow", "last_updated": "2026-06-07",
        "scope": "Spec for linking canonical workers to auth.users — 2026-06-07",
        "read_priority": "reference", "status": "archived",
    },
    "eq/canonical-readiness/service-consumes-canonical-spine-2026-06-16.md": {
        "_no_fm": True,
        "title": "EQ Service → Canonical Spine — Decision + Design",
        "owner": "Royce Milmlow", "last_updated": "2026-06-16",
        "scope": "Decision record: EQ Service reads customers/sites from canonical spine (app_data.*) on ehow",
        "read_priority": "reference", "status": "live",
    },
}

def inject_fm(path, keys):
    """Add frontmatter block to a file that has none."""
    text = path.read_text(encoding="utf-8")
    fm = "---\n"
    for k, v in keys.items():
        fm += f"{k}: {v}\n"
    fm += "---\n\n"
    path.write_text(fm + text, encoding="utf-8")
    print(f"  + created frontmatter: {path}")

def add_keys(path, keys):
    """Add missing keys to existing frontmatter."""
    text = path.read_text(encoding="utf-8")
    # Find end of frontmatter
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        print(f"  ! could not parse frontmatter in {path}", file=sys.stderr)
        return
    fm_body = m.group(1)
    end_pos = m.end()
    new_lines = []
    for k, v in keys.items():
        if k.startswith("_"):
            continue
        if k == "status_override":
            # Replace or add status
            if re.search(r"^status:", fm_body, re.MULTILINE):
                fm_body = re.sub(r"^status:.*$", f"status: {v}", fm_body, flags=re.MULTILINE)
            else:
                new_lines.append(f"status: {v}")
            continue
        if not re.search(rf"^{k}:", fm_body, re.MULTILINE):
            new_lines.append(f"{k}: {v}")
    if new_lines:
        fm_body = fm_body.rstrip() + "\n" + "\n".join(new_lines)
    new_text = "---\n" + fm_body + "\n---\n" + text[end_pos:]
    path.write_text(new_text, encoding="utf-8")
    print(f"  + added keys {[k for k in keys if not k.startswith('_') and k != 'status_override']} to {path}")

def fix_sprint_board(path):
    """Move HTML comment to after frontmatter."""
    text = path.read_text(encoding="utf-8")
    # Comment is on line 1, frontmatter starts on line 2
    lines = text.split("\n")
    if lines[0].startswith("<!--") and lines[1] == "---":
        comment = lines[0]
        rest = "\n".join(lines[1:])  # everything from --- onwards
        # Find end of frontmatter in rest
        m = re.match(r"^---\n(.*?)\n---\n", rest, re.DOTALL)
        if m:
            new_text = rest[:m.end()] + comment + "\n" + rest[m.end():]
            path.write_text(new_text, encoding="utf-8")
            print(f"  + moved comment inside frontmatter block: {path}")
        return
    print(f"  ! SPRINT-BOARD.md unexpected structure", file=sys.stderr)

for rel, spec in FIXES.items():
    path = ROOT / rel
    if not path.exists():
        print(f"SKIP (not found): {rel}")
        continue
    if spec.get("_move_comment"):
        fix_sprint_board(path)
    elif spec.get("_no_fm"):
        keys = {k: v for k, v in spec.items() if not k.startswith("_")}
        inject_fm(path, keys)
    else:
        add_keys(path, spec)

print("\nDone.")
