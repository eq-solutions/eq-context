#!/usr/bin/env python3
"""Unit tests for the security tooling pure logic (no network).

Run:  python3 scripts/test_security.py
Covers the decision functions that decide pass/fail — the bits that, if wrong,
either miss a leak or cry wolf.
"""
import contextlib
import datetime
import io
import os
import unittest
from unittest import mock

import rls_probe
import security_audit


class ClassifyTests(unittest.TestCase):
    def test_rows_is_leak(self):
        self.assertEqual(rls_probe.classify(200, '[{"id":1}]')[0], "LEAK")

    def test_empty_array_is_pass(self):
        self.assertEqual(rls_probe.classify(200, "[]")[0], "empty")

    def test_401_is_blocked(self):
        self.assertEqual(rls_probe.classify(401, "")[0], "blocked")

    def test_404_is_blocked(self):
        self.assertEqual(rls_probe.classify(404, "")[0], "blocked")

    def test_200_nonjson_not_leak(self):
        self.assertEqual(rls_probe.classify(200, "not json")[0], "blocked")

    def test_known_leak_baseline_is_tracked(self):
        # Every KNOWN_LEAKS key must look like project.public.table — guards typos
        for k in rls_probe.KNOWN_LEAKS:
            self.assertRegex(k, r"^[a-z0-9-]+\.public\.[a-z0-9_]+$")


class TriageTests(unittest.TestCase):
    def test_splits_by_level(self):
        lints = [
            {"level": "ERROR", "name": "a", "detail": "x", "cache_key": "k1"},
            {"level": "WARN", "name": "b", "detail": "y", "cache_key": "k2"},
            {"level": "INFO", "name": "c", "detail": "z", "cache_key": "k3"},
            {"level": "WARN", "name": "d", "detail": "w", "cache_key": "k4"},
        ]
        t = security_audit.triage(lints)
        self.assertEqual(len(t["error"]), 1)
        self.assertEqual(len(t["warn"]), 2)
        self.assertEqual(len(t["info"]), 1)

    def test_handles_empty_and_unknown_level(self):
        t = security_audit.triage([{"level": "BOGUS"}, {}])
        self.assertEqual((len(t["error"]), len(t["warn"]), len(t["info"])), (0, 0, 0))

    def test_accepted_errors_baseline_shape(self):
        # Every entry is advisor cache_key -> "SEC-n — review_by YYYY-MM-DD" (the
        # register's mechanism for a tracked, accepted risk). Guards a typo'd key,
        # a missing ticket, and an entry with no review date.
        for ck, why in security_audit.ACCEPTED_ERRORS.items():
            self.assertTrue(ck and isinstance(ck, str))
            self.assertRegex(ck, r"^[a-z0-9_]+$")
            self.assertRegex(why, r"^SEC-\d+ — review_by \d{4}-\d{2}-\d{2}$")

    def test_accepted_errors_review_dates_not_past(self):
        # The review_by date is enforced HERE and nowhere else. The day after
        # it passes, this fails the weekly workflow's unit-test step until the
        # finding is re-reviewed in ops/security-register.md and the entry's
        # review_by extended (or the entry removed). Deliberate: an accepted
        # risk nobody re-reviews is not accepted, it is forgotten.
        overdue = security_audit.overdue_reviews()
        self.assertEqual(overdue, [], "review_by has passed for: " + ", ".join(
            f"{ck} ({d})" for ck, d in overdue
        ) + " — re-review in ops/security-register.md, then extend review_by or remove the entry")

    def test_overdue_reviews_fires_after_the_date(self):
        # Prove the guard bites: the day after review_by every entry is overdue,
        # and an entry with no parseable date is overdue on any day (fail closed).
        keys = sorted(security_audit.ACCEPTED_ERRORS)
        self.assertEqual(
            sorted(ck for ck, _ in security_audit.overdue_reviews(today=datetime.date(2099, 1, 1))), keys)
        for ck, why in security_audit.ACCEPTED_ERRORS.items():
            due = datetime.date.fromisoformat(why.rsplit(" ", 1)[1])
            # on the review date itself: still fine; the day after: overdue
            self.assertNotIn(ck, [k for k, _ in security_audit.overdue_reviews(today=due)])
            self.assertIn(ck, [k for k, _ in security_audit.overdue_reviews(today=due + datetime.timedelta(days=1))])
        with mock.patch.dict(security_audit.ACCEPTED_ERRORS, {"x_no_date": "SEC-0 — no date"}, clear=True):
            self.assertEqual(security_audit.overdue_reviews(today=datetime.date(2020, 1, 1)), [("x_no_date", None)])


class AcceptedBaselineRunTests(unittest.TestCase):
    """main() end-to-end with fetch() stubbed — still no network. Proves the
    baseline keys match what the advisor actually returns (cache_key), and that
    an ERROR finding NOT in the baseline still fails the run."""

    # Exact lint shape from get_advisors on ehow + zaap, 2026-09-04 (SEC-73).
    SEC73_LINTS = [
        {"level": "ERROR", "name": "security_definer_view",
         "detail": "View `app_data.field_people_directory` is defined with the SECURITY DEFINER property",
         "cache_key": "security_definer_view_app_data_field_people_directory"},
        {"level": "ERROR", "name": "security_definer_view",
         "detail": "View `app_data.field_managers` is defined with the SECURITY DEFINER property",
         "cache_key": "security_definer_view_app_data_field_managers"},
    ]

    def _run(self, lints_by_ref):
        def fake_fetch(ref, token):
            return lints_by_ref.get(ref, [])

        buf = io.StringIO()
        with (
            mock.patch.object(security_audit, "fetch", fake_fetch),
            mock.patch.dict(os.environ, {"SUPABASE_ACCESS_TOKEN": "sbp_test"}),
            contextlib.redirect_stdout(buf),
        ):
            rc = security_audit.main()
        return rc, buf.getvalue()

    def test_sec73_definer_views_accepted_on_both_planes(self):
        rc, out = self._run({
            security_audit.PROJECTS["sks-canonical"]: self.SEC73_LINTS,
            security_audit.PROJECTS["eq-canonical-internal"]: self.SEC73_LINTS,
        })
        self.assertEqual(rc, 0, out)
        self.assertEqual(out.count("ACCEPTED security_definer_view"), 4, out)
        self.assertNotIn("NEW-ERROR", out)

    def test_unlisted_error_still_fails(self):
        novel = [{"level": "ERROR", "name": "rls_disabled_in_public",
                  "detail": "Table `public.x` has RLS disabled",
                  "cache_key": "rls_disabled_in_public_public_x"}]
        rc, out = self._run({security_audit.PROJECTS["sks-canonical"]: novel})
        self.assertEqual(rc, 1, out)
        self.assertIn("NEW-ERROR rls_disabled_in_public", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
