#!/usr/bin/env python3
"""Unit tests for the pure classifiers in substrate_honesty.py.

No network. Thresholds are calibrated against real probes (2026-06-27):
live EQ projects answer 401; the deleted urjh host refuses connection.

Run:  python scripts/test_substrate_honesty.py
"""
import sys

from substrate_honesty import classify_supabase, classify_deploy, verdict


def check(name, got, want):
    if got != want:
        print(f"FAIL {name}: got {got!r}, want {want!r}")
        return 1
    print(f"ok   {name}")
    return 0


def main():
    f = 0

    # Supabase: 401 with no key == live (calibrated against jvkn/zaap/ehow/ktmj).
    f += check("supabase 401 -> live", classify_supabase(401, True)[0], "live")
    f += check("supabase 200 -> live", classify_supabase(200, True)[0], "live")
    # Deleted project: host unreachable (calibrated against urjh).
    f += check("supabase connfail -> dead", classify_supabase(None, False)[0], "dead")
    f += check("supabase 503 -> dead", classify_supabase(503, True)[0], "dead")
    f += check("supabase 418 -> unknown", classify_supabase(418, True)[0], "unknown")

    # Deploy URLs.
    f += check("deploy 200 -> live", classify_deploy(200, True)[0], "live")
    f += check("deploy 301 -> live", classify_deploy(301, True)[0], "live")
    f += check("deploy 404 -> responds", classify_deploy(404, True)[0], "responds")
    f += check("deploy connfail -> dead", classify_deploy(None, False)[0], "dead")
    f += check("deploy 500 -> dead", classify_deploy(500, True)[0], "dead")

    # verdict() — the manifest-claim vs reality decision.
    f += check("live+live -> ok", verdict("live", "live")[0], "ok")
    f += check("live+responds -> info", verdict("live", "responds")[0], "info")
    f += check("live+dead -> DRIFT", verdict("live", "dead")[0], "DRIFT")
    f += check("deleted+dead -> ok", verdict("deleted", "dead")[0], "ok")
    # The headline regression: a deleted project that has come back to life.
    f += check("deleted+live -> DRIFT", verdict("deleted", "live")[0], "DRIFT")

    print()
    if f:
        print(f"{f} test(s) FAILED")
        return 1
    print("all substrate-honesty classifier tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
