#!/usr/bin/env python3
"""Unit tests for check_shared_object_drift's pure logic (normalize/
fingerprint/diagnose). No network — the I/O half (fetch_live_def, the
Management API call) is the same untested boundary every other
Supabase-touching script in this repo has (security_audit.py's fetch(),
refresh_digest.py's gh_get()).

Run: python3 scripts/test_shared_object_drift.py
"""
from check_shared_object_drift import normalize, fingerprint, diagnose

passed = failed = 0


def check(name, got, expected):
    global passed, failed
    ok = got == expected
    print(("PASS" if ok else "FAIL") + f" {name}")
    if ok:
        passed += 1
    else:
        failed += 1
        print(f"     got {got!r} expected {expected!r}")


# ── normalize ────────────────────────────────────────────────────────────
check("normalize: CRLF -> LF", normalize("select 1;\r\nselect 2;\r\n"), "select 1;\nselect 2;")
check("normalize: strips trailing whitespace per line",
      normalize("select 1;   \nselect 2;\t\n"), "select 1;\nselect 2;")
check("normalize: strips leading/trailing blank lines",
      normalize("\n\nselect 1;\n\n"), "select 1;")
check("normalize: None passes through", normalize(None), None)
check("normalize: CRLF + trailing whitespace together",
      normalize("a  \r\nb\t\r\n  \r\nc\r\n"), "a\nb\n\nc")

# ── fingerprint ──────────────────────────────────────────────────────────
check("fingerprint: same content, different line endings -> same hash",
      fingerprint("select 1;\r\nselect 2;"), fingerprint("select 1;\nselect 2;"))
check("fingerprint: different content -> different hash",
      fingerprint("select 1;") == fingerprint("select 2;"), False)
check("fingerprint: None -> None", fingerprint(None), None)
check("fingerprint: is a 64-char hex sha256", len(fingerprint("x")), 64)

# ── diagnose ─────────────────────────────────────────────────────────────
h_a = fingerprint("CREATE VIEW x AS SELECT 1;")
h_b = fingerprint("CREATE VIEW x AS SELECT 2;")

status, _ = diagnose("CREATE VIEW x AS SELECT 1;", {"sha256": h_a})
check("diagnose: matching hash -> clean", status, "clean")

status, live_hash = diagnose("CREATE VIEW x AS SELECT 2;", {"sha256": h_a})
check("diagnose: mismatched hash -> drift", status, "drift")
check("diagnose: drift still returns the live hash", live_hash, h_b)

status, _ = diagnose(None, {"sha256": h_a})
check("diagnose: object gone live -> missing_live", status, "missing_live")

status, live_hash = diagnose("CREATE VIEW x AS SELECT 1;", None)
check("diagnose: no snapshot entry yet -> unbaselined", status, "unbaselined")
check("diagnose: unbaselined still returns the live hash", live_hash, h_a)

status, _ = diagnose(None, None)
check("diagnose: never seen live AND never baselined -> missing_live wins", status, "missing_live")

print(f"\n{passed} passed, {failed} failed")
if failed:
    raise SystemExit(1)
