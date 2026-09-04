#!/usr/bin/env python3
"""Cross-project Supabase security-advisor audit.

Pulls the security advisors for every EQ/SKS Supabase project via the Supabase
Management API and fails if any ERROR-level security finding exists (and prints
a WARN/INFO summary). Designed to run in CI on a schedule so a new missing-RLS
or insecure-policy finding can't sit unnoticed.

Auth: needs a Supabase personal access token (read-only is fine) in
SUPABASE_ACCESS_TOKEN. Create at https://supabase.com/dashboard/account/tokens
and store it as the CI secret SUPABASE_ACCESS_TOKEN. Without it the script
prints how to set it and exits 0 (so it no-ops cleanly until wired).

Known ERROR findings can be baselined (ACCEPTED) so CI fails only on NEW ones —
mirror of rls_probe's KNOWN_LEAKS. Keep the baseline empty unless a finding is
genuinely accepted-with-a-ticket.

Run:  SUPABASE_ACCESS_TOKEN=sbp_… python3 scripts/security_audit.py
"""
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://api.supabase.com/v1/projects"
# api.supabase.com sits behind Cloudflare, which 403s the default urllib
# User-Agent with "error code: 1010" (a browser-signature block). Sending any
# explicit UA clears it (verified 2026-06-27: no-UA -> 1010; with-UA -> reaches
# Supabase). Without this, the advisor audit silently errors once the token is set.
USER_AGENT = "eq-context-security-audit (+https://github.com/eq-solutions/eq-context)"

PROJECTS = {
    "eq-canonical": "jvknxcmbtrfnxfrwfimn",
    "eq-canonical-internal": "zaapmfdkgedqupfjtchl",
    "sks-canonical": "ehowgjardagevnrluult",
    "eq-receipts": "bgrhqvmvzgotxzjneskv",
}

# Accepted ERROR findings (cache_key -> "ticket — review_by"). Baseline so CI
# fails only on NEW errors. Keep tight; every entry is a tracked risk.
ACCEPTED_ERRORS = {
    # SEC-2 closed 2026-07-21 — live-verified fixed via eq-shell tenant-migrations
    # 0023/0178 on both planes, entry removed. See ops/security-register.md.
    #
    # SEC-73 — app_data.field_people_directory + app_data.field_managers are
    # deliberate definer-rights views (security_invoker=false; eq-field PRs
    # #813/#814/#817, 2026-08-27). Tenant isolation is the view's own
    # `tenant_id = (auth.jwt()->'app_metadata'->>'tenant_id')::uuid` predicate,
    # which eq-shell's drift gate (scripts/check-tenant-drift.mjs CHECK 7,
    # VIEW_INVOKER_REVIEWED_DEFINER) re-verifies live on both planes every run,
    # together with the no-anon grant. Accepted as a governed exception by
    # Royce 2026-09-04 (option (a) in the register row); review_by 2026-12-04.
    # The advisor cache_key carries NO project ref, so one key covers the same
    # finding on every project in PROJECTS — today that is 2 views x ehow/zaap
    # = the 4 findings that have failed this gate since 2026-08-30. A same-named
    # definer view appearing on jvkn or eq-receipts would be accepted by these
    # keys too; see the SEC-73 row in ops/security-register.md.
    "security_definer_view_app_data_field_people_directory": "SEC-73 — review_by 2026-12-04",
    "security_definer_view_app_data_field_managers": "SEC-73 — review_by 2026-12-04",
}


def triage(lints):
    """Pure: split advisor lints by level. Unit-tested.

    Returns dict with 'error'/'warn'/'info' lists of (lint_name, detail, cache_key).
    """
    out = {"error": [], "warn": [], "info": []}
    for l in lints or []:
        lvl = (l.get("level") or "").upper()
        bucket = {"ERROR": "error", "WARN": "warn", "INFO": "info"}.get(lvl)
        if not bucket:
            continue
        out[bucket].append((l.get("name", "?"), l.get("detail", ""), l.get("cache_key", "")))
    return out


def fetch(ref, token):
    req = urllib.request.Request(
        f"{API}/{ref}/advisors/security",
        headers={"Authorization": f"Bearer {token}", "User-Agent": USER_AGENT},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    # API returns {"lints":[...]} (shape matches the MCP get_advisors output).
    return data.get("lints", data if isinstance(data, list) else [])


def main():
    token = os.environ.get("SUPABASE_ACCESS_TOKEN")
    if not token:
        print("SUPABASE_ACCESS_TOKEN not set — skipping advisor audit.")
        print("Set a read-only token (https://supabase.com/dashboard/account/tokens)")
        print("as the CI secret SUPABASE_ACCESS_TOKEN to enable this gate.")
        return 0

    new_errors = []
    fetch_failures = []
    for name, ref in PROJECTS.items():
        try:
            lints = fetch(ref, token)
        except urllib.error.HTTPError as e:
            detail = e.read().decode()[:200]
            print(f"[{name}] ERROR fetching advisors: {e.code} {detail}")
            fetch_failures.append(f"{name}: HTTP {e.code} — {detail}")
            continue
        except urllib.error.URLError as e:
            print(f"[{name}] ERROR fetching advisors: network — {e.reason}")
            fetch_failures.append(f"{name}: network — {e.reason}")
            continue
        t = triage(lints)
        print(f"[{name}] ERROR {len(t['error'])} · WARN {len(t['warn'])} · INFO {len(t['info'])}")
        for nm, detail, ck in t["error"]:
            if ck in ACCEPTED_ERRORS:
                print(f"  ACCEPTED {nm}: {detail[:120]}  [{ACCEPTED_ERRORS[ck]}]")
            else:
                print(f"  NEW-ERROR {nm}: {detail[:160]}")
                new_errors.append(f"{name}: {nm} — {detail[:120]}")

    print("\n=== summary ===")
    # A fetch failure on one project must not hide the results already
    # gathered for every other project (the eq-solves-field incident:
    # SEC-17 — one dead ref aborted the whole run's summary for a month).
    if fetch_failures:
        print(f"{len(fetch_failures)} project(s) could not be reached:")
        for f in fetch_failures:
            print(f"  - {f}")
    if new_errors:
        print(f"{len(new_errors)} NEW ERROR-level security finding(s):")
        for e in new_errors:
            print(f"  - {e}")
        return 1
    if fetch_failures:
        return 2
    print("No new ERROR-level security findings. (Accepted baseline still open — see register.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
