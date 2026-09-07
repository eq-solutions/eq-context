#!/usr/bin/env python3
"""Unit tests for check_budgets.py's pure parsing logic. No git, no fixtures on disk."""
import unittest

from check_budgets import extract_budget, is_budget_marker_exempt


class ExtractBudgetTests(unittest.TestCase):
    def test_no_marker_returns_none(self):
        self.assertIsNone(extract_budget("# Just a regular file\n\nNothing budget-related here.\n"))

    def test_simple_currently_form(self):
        text = "**Budget:** ~500 lines (currently 405). Past that, evict the oldest.\n"
        self.assertEqual(extract_budget(text), 500)

    def test_prose_form_wrapped_across_lines(self):
        text = (
            "**Full pruning history:** `x`. **Budget:** this file should stay under\n"
            "~150 lines -- if it's bigger, history is leaking back in; check the\n"
            "protocol above is being followed.\n"
        )
        self.assertEqual(extract_budget(text), 150)

    def test_stops_at_blank_line_not_a_later_number(self):
        text = (
            "**Budget:** ~400 lines (currently 257).\n"
            "\n"
            "## Some unrelated section mentioning 9999 lines of something else\n"
        )
        self.assertEqual(extract_budget(text), 400)

    def test_marker_with_no_number_raises(self):
        with self.assertRaises(ValueError):
            extract_budget("**Budget:** we should really set one of these at some point.\n")

    def test_the_three_real_notes_added_2026_09_07(self):
        # Regression guard: a future rewording of any of these three shouldn't
        # silently stop being enforced.
        worktree_registry = (
            "**Full pruning history:** `system/worktree-registry-archive.md`. **Budget:**\n"
            "this file should stay under ~150 lines -- if it's bigger, history is leaking\n"
            "back in; check Protocol step 3 above is being followed.\n"
        )
        lessons = (
            "**Budget:** ~500 lines (currently 405). Past that, evict the oldest resolved\n"
            "entries to `archive/lessons-history.md` using the same trim-not-delete pattern\n"
            "as the 2026-07-12 precedent above -- rule + pointer stays here, full narrative\n"
            "moves. (`rules/tidy-protocol.md` Step 5, 2026-09-07.)\n"
        )
        failures = (
            "**Budget:** ~400 lines (currently 257). Past that, evict entries whose guard\n"
            "has held for 90+ days with zero recurrences to a new `system/failures-archive.md`\n"
            "(same split pattern as `system/worktree-registry-archive.md`) -- keep the F-number\n"
            "and rung here as a one-line pointer, move the full incident narrative.\n"
        )
        self.assertEqual(extract_budget(worktree_registry), 150)
        self.assertEqual(extract_budget(lessons), 500)
        self.assertEqual(extract_budget(failures), 400)


class BudgetMarkerExemptTests(unittest.TestCase):
    def test_session_logs_exempt_wholesale(self):
        self.assertTrue(is_budget_marker_exempt("sessions/2026-09-07.md"))
        self.assertTrue(is_budget_marker_exempt("sessions/2026-01-01.md"))

    def test_machinery_doc_exempt(self):
        # Describes what check_budgets.py does; never declares its own budget.
        self.assertTrue(is_budget_marker_exempt("system/machinery.md"))

    def test_real_budgeted_files_not_exempt(self):
        self.assertFalse(is_budget_marker_exempt("system/failures.md"))
        self.assertFalse(is_budget_marker_exempt("system/lessons.md"))
        self.assertFalse(is_budget_marker_exempt("system/worktree-registry.md"))
        self.assertFalse(is_budget_marker_exempt("eq/pending/eq-shell.md"))


if __name__ == "__main__":
    unittest.main()
