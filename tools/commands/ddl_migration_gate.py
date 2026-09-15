#!/usr/bin/env python3
"""
Stop gate — DDL-without-migration.

Chat's finding (2026-07-30): the same security_invoker bug recurred three
separate times because a live DDL change gets applied via MCP (apply_migration
/ execute_sql) under time pressure and the corresponding migration file just
never makes it back into git that session. guard.js's gate-sql rule already
observes every one of these calls (PreToolUse, logged to guard.log) but never
correlates "a live write/DDL happened" against "did a migration file for it
land in git" — that correlation is this hook.

Mechanism: guard.js now tags every guard.log line with session_id + cwd. This
hook, at Stop, re-reads guard.log for THIS session's gate-sql lines whose tool
is apply_migration/execute_sql, groups them by git repo (resolved from cwd),
and for each repo checks whether a migrations-path file was committed (or is
at least sitting uncommitted) since the earliest such event this session.

Three states per repo:
  MISSING     — DDL went out live, no migration file touched at all (staged,
                committed, or working-tree) — the actual recurring bug.
  UNCOMMITTED — a migration file exists in the working tree but isn't
                committed yet — softer, same class as session_end.py's DIRTY.
  (silent)    — a migration-path commit landed since the DDL event — covered.

Fails open, never blocks Stop (informational only) — same doctrine as
session_end.py: a Stop hook that traps someone mid-exit is a new "loop of
despair" class, and there is no destroyed data at stake here to justify
fail-closed.

Added 2026-08-24: an UNCONDITIONAL eq-field sweep (check_eq_field_untracked_
migrations), independent of session_id/guard.log/this-session's-own-events
entirely. The MISSING/UNCOMMITTED logic above is session-scoped by
construction (it only ever looks at gate-sql lines tagged with THIS
session's id) — which structurally cannot catch the actual incident that
motivated it: a migration hand-applied via the Supabase MCP in an EARLIER
session, still sitting untracked when a LATER session starts and never
itself touches SQL (confirmed live 2026-08-23/24 — eq-context memory
migrations-applied-uncommitted, eq-field PR #764 — applied 2026-08-23,
discovered and committed a full day later, in a different session than the
one that applied it). The new check has no such requirement: it looks at
live git state in the eq-field working tree every time this hook runs,
regardless of what this session itself did.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HOOKS_DIR = os.path.dirname(os.path.abspath(__file__))
# EQ_GUARD_LOG_TEST lets selftest exercise this against a throwaway log/repo
# instead of the real guard.log — never set in normal operation.
GUARD_LOG = os.environ.get("EQ_GUARD_LOG_TEST") or os.path.join(HOOKS_DIR, "guard.log")
MIGRATION_PATHSPECS = ["**/migrations/**", "**/tenant-migrations/**"]


def read_stdin_meta():
    """Returns (session_id, cwd). Reads stdin exactly once -- callers needing
    both fields must go through this, not the old single-field reader, since
    the stream can't be re-read."""
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        return str(data.get("session_id") or ""), str(data.get("cwd") or "")
    except Exception:
        return "", ""


def git(repo, *args, timeout=10):
    try:
        p = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, timeout=timeout)
        return p.stdout.strip() if p.returncode == 0 else None
    except Exception:
        return None


def repo_root(cwd):
    top = git(cwd, "rev-parse", "--show-toplevel")
    return top or None


def parse_ts(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def _is_eq_field_repo(root):
    """Same path-segment semantics as guard.js's own inEqField regex
    (/\\/eq-field(\\/|-[a-z0-9-]*)?(\\/|$)/) -- a segment named exactly
    eq-field, or eq-field-<topic>-wt per this repo's documented worktree
    convention. Kept in sync by hand; the two can't literally share source
    across a JS hook and a Python hook."""
    norm = root.replace("\\", "/").lower()
    return re.search(r'/eq-field(/|-[a-z0-9-]*)?(/|$)', norm) is not None


def check_eq_field_untracked_migrations(session_cwd):
    """Unconditional sweep, independent of this session's own DDL activity --
    closes the exact gap the session-scoped MISSING/UNCOMMITTED check below
    cannot: a migration hand-applied via the Supabase MCP in an EARLIER
    session, still untracked when THIS session starts and never itself
    touches SQL. See the module docstring's 2026-08-24 note.

    Repo identity comes only from this session's own reported cwd (pinned at
    session start and does not follow an in-command cd -- same limitation
    guard.js documents at length for its own cwd handling). Good enough for
    the dominant case -- an eq-field session is rooted in an eq-field
    checkout or worktree, same as this repo's own convention -- without the
    complexity of reconstructing full cwd history from a log that doesn't
    carry it for non-violation tool calls.
    """
    if not session_cwd:
        return []
    root = repo_root(session_cwd)
    if not root or not _is_eq_field_repo(root):
        return []
    # --untracked-files=all, not the default normal: normal collapses a wholly-
    # untracked directory to one line ("?? supabase/migrations/", no .sql
    # suffix), which the filter below would silently miss entirely. Doesn't
    # reproduce against the real repo today (that directory already has
    # hundreds of tracked files, so git never collapses it) but it's a
    # one-line fix for a real latent gap -- confirmed live against a fresh
    # fixture repo where the directory starts wholly untracked.
    out = git(root, "status", "--porcelain", "--untracked-files=all", "--", "supabase/migrations")
    if not out:
        return []
    files = [line[3:].strip() for line in out.splitlines()
             if line.startswith("?? ") and line.strip().lower().endswith(".sql")]
    if not files:
        return []
    return [
        f"UNTRACKED-MIGRATION  eq-field: {len(files)} untracked supabase/migrations/*.sql file(s) present "
        f"({', '.join(files)}) — independent of this session's own DDL activity, may have been applied in "
        f"an earlier session. If any are already live, verify against the Supabase MCP's list_migrations "
        f"ledger and commit before this session ends."
    ]


def main():
    session_id, session_cwd = read_stdin_meta()
    lines = check_eq_field_untracked_migrations(session_cwd)

    if not session_id or not os.path.isfile(GUARD_LOG):
        if lines:
            print("=== DDL-WITHOUT-MIGRATION GATE (informational — never blocks) ===")
            print("\n".join(lines))
            print("=== if this DDL was read-only or already reconciled another way, ignore it ===")
        sys.exit(0)

    events = []  # (ts, cwd)
    try:
        with open(GUARD_LOG, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 8:
                    continue  # pre-tagging line, not session-attributable
                ts, mode, rule, status, tool, reason, sid, cwd = parts[:8]
                if rule != "gate-sql" or sid != session_id:
                    continue
                if not (tool.endswith("apply_migration") or tool.endswith("execute_sql") or tool.endswith("execute-sql")):
                    continue
                events.append((ts, cwd))
    except Exception:
        events = []  # fail open

    # Group by resolved repo root.
    by_repo = {}
    for ts, cwd in events:
        if not cwd:
            continue
        root = repo_root(cwd)
        if not root:
            continue
        by_repo.setdefault(root, []).append(ts)

    for root, ts_list in sorted(by_repo.items()):
        parsed = [t for t in (parse_ts(x) for x in ts_list) if t]
        if not parsed:
            continue
        since = min(parsed) - timedelta(seconds=60)
        since_str = since.strftime("%Y-%m-%dT%H:%M:%SZ")

        committed = git(root, "log", f"--since={since_str}", "--oneline", "--", *MIGRATION_PATHSPECS)
        if committed:
            continue  # covered

        uncommitted = git(root, "status", "--porcelain", "--", *MIGRATION_PATHSPECS)
        repo_name = os.path.basename(root)
        if uncommitted:
            lines.append(
                f"UNCOMMITTED  {repo_name}: live DDL applied this session ({len(ts_list)} call(s)) — "
                f"a migration file is sitting uncommitted. Commit it before this session ends."
            )
        else:
            lines.append(
                f"MISSING      {repo_name}: live DDL applied this session ({len(ts_list)} call(s)) via "
                f"apply_migration/execute_sql — no migration file (committed or uncommitted) found under "
                f"supabase/migrations or tenant-migrations since. This is the recurring security_invoker-class "
                f"gap — the live change and the repo are now out of sync."
            )

    if lines:
        print("=== DDL-WITHOUT-MIGRATION GATE (informational — never blocks) ===")
        print("\n".join(lines))
        print("=== if this DDL was read-only or already reconciled another way, ignore it ===")

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)  # fail open, always

# === DURABILITY BACKUP META ===
# This is a durability backup, not the live file — it is never loaded or
# executed from this path. Source of truth: ~/.claude/hooks/ddl_migration_gate.py
# (Royce's machine, user-level, not version-controlled). Last synced: 2026-09-15.
# Checked for drift every session by hooks/session_start.py's CMDSYNC step
# (system/failures.md -> F19), which truncates the file at the "DURABILITY
# BACKUP META" marker above before hashing, so keep that marker line byte-exact
# if you touch this comment. To restore: copy everything ABOVE this block back
# to ~/.claude/hooks/ddl_migration_gate.py unchanged.
# === END META ===
