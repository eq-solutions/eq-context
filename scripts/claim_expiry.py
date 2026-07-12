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

Exit 0 = all goals owned and unexpired (or none). Exit 1 = violation. Exit 2 =
the check itself could not run (fail loud, never silent).
"""
import datetime
import re
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

TODAY_MD = "system/TODAY.md"
REQUIRED = ["type", "owner", "asserted_on", "expires_on", "verify"]


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
    try:
        with open(TODAY_MD, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as e:
        print(f"::error::claim-expiry cannot read {TODAY_MD}: {e}")
        return 2

    fatal, msgs = check(text, datetime.date.today())
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
