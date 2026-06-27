#!/usr/bin/env python3
"""Unit tests for the security tooling pure logic (no network).

Run:  python3 scripts/test_security.py
Covers the decision functions that decide pass/fail — the bits that, if wrong,
either miss a leak or cry wolf.
"""
import unittest

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
        for ck in security_audit.ACCEPTED_ERRORS:
            self.assertTrue(ck and isinstance(ck, str))


if __name__ == "__main__":
    unittest.main(verbosity=2)
