#!/usr/bin/env python3
"""
claim-expiry — the F3 guard (rung 3).

F3 (2026-07-11): a goal nobody owned, with no expiry, sat in system/TODAY.md
marked `read_priority: critical` and steered every session for two weeks. Every
CI check passed green because they verify *recency*, not *truth or ownership*.

This check is the guard TODAY.md's GOALS rules promise. It reads the goals YAML
block and FAILS CI on any claim that:
  - is missing a required field (type, owner, asserted_on, expires_on, verify), or
  - has an unparseable `expires_on`, or
  - is past its `expires_on` (expired = dead = "Royce, confirm or kill").

An empty goals section (`claims: []`) PASSES — a blank goals section is honest;
that is the whole lesson of F3. Leaving it blank is never a violation.

SECOND CHECK, ADDED 2026-08-16: any tracked .md file's own frontmatter
`expires_on`, not just TODAY.md's goals. Gap found the same day it was fixed --
system/substrate-a-plus-plan.md claimed outright "It is subject to its own
rules... If it is not reconfirmed, claim-expiry will kill it and tell you", but
this check was scoped only to TODAY.md, so nothing ever checked *that file's
own* expires_on, or system/substrate-plan-v2.md's (3 days past its own
2026-08-12 expiry with no decision recorded and nothing flagging it). Same
shape as F3 -- an unconfirmed claim ages into a lie and nothing notices -- found
in a new corner instead of a new incident.

`status: archived` files are skipped: an archived, superseded planning doc
already tells you not to trust it as current, and flagging its own past-tense
expiry on top would be noise, not signal, on a document that's already
correctly labelled dead.

Ratcheted like review_clock.py's overdue ceiling, not zero-tolerance: starts at
the measured debt on the day this shipped (1 -- substrate-plan-v2.md), so it
doesn't fail the build over a lie this check didn't create. New violations
still fail; lowering the ceiling is the actual review work, same rule as
review_clock.py and prune_ratchet.py.

Exit 0 = all goals owned and unexpired (or none), AND frontmatter expiry within
ceiling. Exit 1 = violation. Exit 2 = the TODAY.md check itself could not run
(fail loud, never silent).
"""
import datetime
import os
import re
import subprocess
import sys

# Windows consoles default to cp1252; these messages contain em-dashes. Without
# this, print() raises UnicodeEncodeError and the guard's output is lost — the
# exact silent-guard failure class this repo exists to kill. Force UTF-8 (no-op
# on Linux CI). Same fix as hooks/session_start.py.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

try:
    import yaml
except ImportError:  # pragma: no cover
    print("claim-expiry: PyYAML not installed (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY_MD = "system/TODAY.md"
REQUIRED = ["type", "owner", "asserted_on", "expires_on", "verify"]

# A status this final means the file already tells you not to trust it as
# current -- its own expiry going past is not a new fact worth surfacing.
ARCHIVED_STATUSES = {"archived"}

# Ratchet, not cliff -- see the module docstring. Measured debt on 2026-08-16
# is 1 file (system/substrate-plan-v2.md). Raising this needs a reason in the
# commit message, same rule as review_clock.py and prune_ratchet.py.
FRONTMATTER_EXPIRY_CEILING = 1

FM_DELIM = re.compile(r"^---\s*$")


def parse_frontmatter(text):
    """Return the frontmatter block as a dict. Empty dict when there is none.

    Deliberately independent of review_clock.py's identical parser -- each
    guard script in this repo is self-contained and single-purpose so one
    script's bug can't silently propagate into another's gate."""
    lines = text.lstrip("﻿").split("\n")
    if not lines or not FM_DELIM.match(lines[0]):
        return {}
    fm = {}
    for line in lines[1:]:
        if FM_DELIM.match(line):
            return fm
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*?)\s*$", line)
        if m:
            fm[m.group(1).lower()] = m.group(2).strip().strip('"').strip("'")
    return {}  # unterminated block -- treat as absent rather than guessing


def as_frontmatter_date(value):
    """Coerce a frontmatter expires_on string to datetime.date, or None."""
    m = re.match(r"^(\d{4}-\d{2}-\d{2})", (value or "").strip())
    if not m:
        return None
    try:
        return datetime.date.fromisoformat(m.group(1))
    except ValueError:
        return None


def check_frontmatter_expiry(files, today):
    """files: iterable of (rel_path, frontmatter_dict). Pure -- no disk I/O.

    Returns a list of violation message strings for every non-archived file
    whose frontmatter expires_on is in the past. A missing or unparseable
    expires_on is not a violation here -- most files never make this claim at
    all, unlike TODAY.md's goals, where expires_on is mandatory."""
    msgs = []
    for rel_path, fm in files:
        if (fm.get("status") or "").strip().lower() in ARCHIVED_STATUSES:
            continue
        exp = fm.get("expires_on")
        if not exp:
            continue
        d = as_frontmatter_date(exp)
        if d is None or d >= today:
            continue
        msgs.append(
            f"::error file={rel_path}::frontmatter expires_on '{exp}' EXPIRED "
            f"{(today - d).days}d ago. An unconfirmed claim past its own "
            f"declared expiry is exactly F3's shape -- Royce, confirm or kill it."
        )
    return msgs


def iter_tracked_md():
    """Tracked .md paths, repo-relative, POSIX separators.

    git ls-files rather than os.walk so __pycache__ and any untracked scratch
    file cannot influence a gate. Mirrors review_clock.py's own helper."""
    try:
        out = subprocess.run(
            ["git", "-C", ROOT, "ls-files", "*.md"],
            capture_output=True, text=True, timeout=30,
        )
        if out.returncode == 0:
            return [p for p in out.stdout.split("\n") if p.strip()]
    except Exception:
        pass
    found = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__", ".pytest_cache")]
        for name in filenames:
            if name.endswith(".md"):
                rel = os.path.relpath(os.path.join(dirpath, name), ROOT)
                found.append(rel.replace(os.sep, "/"))
    return sorted(found)


def collect_frontmatter_violations(today):
    """I/O wrapper: read every tracked .md file's frontmatter and run
    check_frontmatter_expiry against it."""
    files = []
    for rel in iter_tracked_md():
        path = os.path.join(ROOT, rel)
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read(4000)
        except OSError:
            continue
        files.append((rel, parse_frontmatter(text)))
    return check_frontmatter_expiry(files, today)


def extract_goals_block(text):
    """Return the raw YAML string inside the fenced block under the GOALS heading,
    or None if the GOALS section or its ```yaml fence cannot be found."""
    m = re.search(
        r"^##[^\n]*\bGOALS\b[^\n]*$(.*?)(?=^\s*---\s*$|^##\s|\Z)",
        text, re.S | re.M | re.I,
    )
    if not m:
        return None
    fence = re.search(r"```ya?ml\s*\n(.*?)```", m.group(1), re.S)
    return fence.group(1) if fence else None


def as_date(v):
    """Coerce a YAML date or ISO string to datetime.date, or None if not a date."""
    if isinstance(v, datetime.datetime):
        return v.date()
    if isinstance(v, datetime.date):
        return v
    if isinstance(v, str):
        try:
            return datetime.datetime.strptime(v.strip()[:10], "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


def check(text, today):
    """Pure validator. Returns (fatal: bool, messages: list[str]).

    fatal=True means the check could not run (structure changed) — exit 2.
    A non-empty messages list with fatal=False means goal violations — exit 1.
    """
    block = extract_goals_block(text)
    if block is None:
        return True, [
            f"::error file={TODAY_MD}::GOALS section or its ```yaml block not found — "
            f"TODAY.md structure changed; claim-expiry cannot verify goals."
        ]

    try:
        data = yaml.safe_load(block) or {}
    except yaml.YAMLError as e:
        return True, [f"::error file={TODAY_MD}::GOALS yaml block does not parse: {e}"]

    if not isinstance(data, dict) or "claims" not in data:
        return True, [f"::error file={TODAY_MD}::GOALS block has no 'claims:' key."]

    claims = data["claims"] or []
    if not isinstance(claims, list):
        return True, [
            f"::error file={TODAY_MD}::'claims' must be a list "
            f"(got {type(claims).__name__})."
        ]

    msgs = []
    for i, c in enumerate(claims):
        if not isinstance(c, dict):
            msgs.append(f"::error file={TODAY_MD}::claim[{i}] is not a mapping.")
            continue
        label = c.get("text") or c.get("title") or c.get("owner") or f"index {i}"
        for k in REQUIRED:
            if k not in c or c[k] in (None, ""):
                msgs.append(
                    f"::error file={TODAY_MD}::goal '{label}' is missing required field "
                    f"'{k}'. An unowned/undated goal is exactly failure F3."
                )
        exp = c.get("expires_on")
        if exp not in (None, ""):
            d = as_date(exp)
            if d is None:
                msgs.append(
                    f"::error file={TODAY_MD}::goal '{label}' expires_on '{exp}' is not "
                    f"an ISO date (YYYY-MM-DD)."
                )
            elif d < today:
                msgs.append(
                    f"::error file={TODAY_MD}::goal '{label}' EXPIRED on {d} "
                    f"({(today - d).days}d ago). A goal past expires_on is DEAD — "
                    f"Royce, confirm or kill it. It does not silently persist."
                )
    return False, msgs


def main():
    today = datetime.date.today()

    try:
        with open(TODAY_MD, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as e:
        print(f"::error::claim-expiry cannot read {TODAY_MD}: {e}")
        return 2

    fatal, msgs = check(text, today)
    for m in msgs:
        print(m)
    if fatal:
        return 2
    if msgs:
        print(
            f"::error::claim-expiry: {len(msgs)} goal violation(s). Fix the GOALS "
            f"section of {TODAY_MD}, or blank it (claims: []) until a goal is real."
        )
        return 1
    print("claim-expiry: goals owned and unexpired (or UNSET) — OK.")

    fm_msgs = collect_frontmatter_violations(today)
    for m in fm_msgs:
        print(m)
    if len(fm_msgs) > FRONTMATTER_EXPIRY_CEILING:
        print(
            f"::error::claim-expiry: {len(fm_msgs)} file(s) with an expired "
            f"frontmatter expires_on, over the ceiling of {FRONTMATTER_EXPIRY_CEILING}. "
            f"This ceiling is measured debt, not a target -- it can only be lowered "
            f"(confirm-or-kill the file, or bump its expires_on with a real reason)."
        )
        return 1
    print(
        f"claim-expiry: {len(fm_msgs)} file(s) with an expired frontmatter "
        f"expires_on (ceiling {FRONTMATTER_EXPIRY_CEILING}) — OK."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
