#!/usr/bin/env python3
"""Unit tests for scripts/sync.py pure logic (no network).

Run:  python3 scripts/test_sync.py
These cover the two things that can silently corrupt the live store:
slug derivation (wrong slug = duplicate/lost row) and the orphan-delete
safety cap (the mass-delete guard).
"""
import os
import tempfile
import unittest

import sync


def _touch(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\ntitle: x\n---\n")


class SlugMappingTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        for rel in [
            "CLAUDE.md", "AGENTS.md", "COWORK-PROMPT.md", "README.md",
            "STATE.md", "SPRINT-BOARD.md",
            "eq/pending.md", "eq/field/multi-tenancy/plan.md",
            "sks/active.md", "system/lessons.md", "sessions/2026-06-04.md",
        ]:
            _touch(os.path.join(self.dir, rel))

    def _slugs(self):
        return dict(sync.compute_upserts(self.dir))

    def test_root_files_get_canonical_slugs(self):
        s = self._slugs()
        self.assertEqual(s["claude"], "CLAUDE.md")
        self.assertEqual(s["agents"], "AGENTS.md")
        self.assertEqual(s["cowork"], "COWORK-PROMPT.md")
        self.assertEqual(s["readme"], "README.md")

    def test_other_root_md_lowercased_basename(self):
        s = self._slugs()
        self.assertEqual(s["state"], "STATE.md")
        self.assertEqual(s["sprint-board"], "SPRINT-BOARD.md")

    def test_subdir_slug_is_relative_path_forward_slash(self):
        s = self._slugs()
        self.assertEqual(s["eq/pending.md"], "eq/pending.md")
        self.assertEqual(
            s["eq/field/multi-tenancy/plan.md"], "eq/field/multi-tenancy/plan.md")
        self.assertEqual(s["sessions/2026-06-04.md"], "sessions/2026-06-04.md")

    def test_explicit_root_files_not_double_keyed(self):
        # README.md must only appear as 'readme', never as 'readme' via the
        # generic root sweep producing a second pair.
        slugs = [slug for slug, _ in sync.compute_upserts(self.dir)]
        self.assertEqual(slugs.count("readme"), 1)
        self.assertEqual(slugs.count("claude"), 1)

    def test_current_slugs_matches_upsert_keys(self):
        self.assertEqual(
            sync.compute_current_slugs(self.dir),
            {slug for slug, _ in sync.compute_upserts(self.dir)},
        )


class UncoveredMdTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        _touch(os.path.join(self.dir, "eq/pending.md"))          # covered (tier)
        _touch(os.path.join(self.dir, "STATE.md"))               # covered (root)
        _touch(os.path.join(self.dir, "drafts/wip.md"))          # exempt dir
        _touch(os.path.join(self.dir, ".github/workflows/x.md")) # exempt dir
        _touch(os.path.join(self.dir, "newtier/oops.md"))        # NOT covered

    def test_new_tier_file_is_flagged(self):
        self.assertIn("newtier/oops.md", sync.uncovered_md(self.dir))

    def test_covered_and_exempt_not_flagged(self):
        missed = sync.uncovered_md(self.dir)
        self.assertNotIn("eq/pending.md", missed)
        self.assertNotIn("STATE.md", missed)
        self.assertNotIn("drafts/wip.md", missed)
        self.assertNotIn(".github/workflows/x.md", missed)


class OrphanSafetyTests(unittest.TestCase):
    def test_small_batch_allowed(self):
        blocked, _ = sync.orphan_delete_blocked(["a", "b"], total_existing=100, max_abs=15)
        self.assertFalse(blocked)

    def test_absolute_cap_blocks(self):
        orphans = [str(i) for i in range(20)]
        blocked, reason = sync.orphan_delete_blocked(orphans, total_existing=200, max_abs=15)
        self.assertTrue(blocked)
        self.assertIn("absolute cap", reason)

    def test_fractional_cap_blocks_even_under_abs(self):
        # 10 orphans is under the abs cap of 15, but 10/20 = 50% > 25%.
        orphans = [str(i) for i in range(10)]
        blocked, reason = sync.orphan_delete_blocked(orphans, total_existing=20, max_abs=15)
        self.assertTrue(blocked)
        self.assertIn("%", reason)

    def test_zero_orphans_never_blocks(self):
        blocked, _ = sync.orphan_delete_blocked([], total_existing=0, max_abs=15)
        self.assertFalse(blocked)

    def test_find_orphans(self):
        current = {"a", "b", "c"}
        existing = ["a", "b", "x", "y"]
        self.assertEqual(sync.find_orphans(current, existing), ["x", "y"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
