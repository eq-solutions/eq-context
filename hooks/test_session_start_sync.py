#!/usr/bin/env python3
"""Pins the SYNC check in session_start.py.

Why this test exists (2026-08-15): the gate's FRESHNESS check reads digest.md's
timestamp and reports "ok" when it is recent. A clone can be 34 commits behind
origin/main and still carry a digest.md stamped today — mtime cannot express
staleness that arrives as the *absence* of commits. On 2026-08-15 that gap made
the gate announce "F13 (rung 1, 2x) PROMOTION DUE" when origin/main already had
F13 at rung 4, guard built and merged. The session acted on it before catching
the error by hand.

The regression this pins is specific and narrow: **the gate must never report a
clean sync state for a clone whose HEAD differs from origin/main.** Asserting
only "STOP appears when behind" would pass against a gate that printed STOP
unconditionally, so the clean case is asserted too.

Real git repos in a temp dir — no network, no fixtures on disk, cross-platform.
"""
import os
import subprocess
import sys
import tempfile
import unittest

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "session_start.py")


def git(cwd, *args):
    return subprocess.run(
        ("git",) + args, cwd=cwd, capture_output=True, text=True, timeout=30
    )


def commit(repo, name, body):
    with open(os.path.join(repo, name), "w", encoding="utf-8") as fh:
        fh.write(body)
    git(repo, "add", "-A")
    git(repo, "commit", "-m", f"add {name}", "--no-gpg-sign")


def build_pair(tmp):
    """An 'origin' repo and a clone of it, both with a fresh-stamped digest.md.

    The fresh stamp is the point: it is what makes FRESHNESS report ok, so any
    staleness the gate detects has to come from the ref comparison.
    """
    from datetime import datetime, timezone

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    digest = f"# digest\n\n_{stamp} 02:00 UTC_\n\n## Needs you\n\n## Next\n"

    origin = os.path.join(tmp, "origin")
    os.makedirs(origin)
    git(origin, "init", "-b", "main")
    git(origin, "config", "user.email", "t@t")
    git(origin, "config", "user.name", "t")
    commit(origin, "digest.md", digest)

    clone = os.path.join(tmp, "clone")
    git(tmp, "clone", origin, clone)
    git(clone, "config", "user.email", "t@t")
    git(clone, "config", "user.name", "t")
    return origin, clone, digest


def run_gate(root):
    env = dict(os.environ, EQ_CONTEXT=root, PYTHONIOENCODING="utf-8")
    r = subprocess.run(
        (sys.executable, HOOK), capture_output=True, text=True, timeout=60, env=env
    )
    return r.stdout + r.stderr


class SyncCheck(unittest.TestCase):
    def test_in_sync_clone_reports_ok(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, clone, _ = build_pair(tmp)
            out = run_gate(clone)
            self.assertIn("SYNC", out, "gate emitted no SYNC line at all")
            self.assertNotIn(
                "*** STOP ***",
                out,
                "gate cried STOP on a clone that is level with origin/main",
            )

    def test_behind_clone_is_never_reported_clean(self):
        """The 2026-08-15 failure, reproduced: fresh digest.md, stale commits."""
        with tempfile.TemporaryDirectory() as tmp:
            origin, clone, digest = build_pair(tmp)
            commit(origin, "later.md", "landed after the clone was taken\n")
            git(clone, "fetch", "origin", "main")

            out = run_gate(clone)

            self.assertIn(
                "*** STOP ***",
                out,
                "clone is behind origin/main and the gate did not say so",
            )
            self.assertNotIn(
                "SYNC       ok",
                out,
                "gate reported SYNC ok while HEAD != origin/main — the exact "
                "blind spot this check exists to close",
            )
            # The whole point: FRESHNESS is happy, and that must not be enough.
            self.assertIn(
                "FRESHNESS  ok",
                out,
                "test is not exercising the real failure — FRESHNESS should be "
                "reporting ok here, since digest.md carries today's stamp",
            )

    def test_diverged_clone_is_never_reported_clean(self):
        """Ahead-and-behind, which is how the real checkout actually drifted."""
        with tempfile.TemporaryDirectory() as tmp:
            origin, clone, _ = build_pair(tmp)
            commit(origin, "theirs.md", "remote work\n")
            commit(clone, "mine.md", "local work\n")
            git(clone, "fetch", "origin", "main")

            out = run_gate(clone)
            self.assertIn("*** STOP ***", out, "diverged clone reported as clean")
            self.assertNotIn("SYNC       ok", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
