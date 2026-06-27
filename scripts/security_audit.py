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

PROJECTS = {
    "eq-canonical": "jvknxcmbtrfnxfrwfimn",
    "eq-canonical-internal": "zaapmfdkgedqupfjtchl",
    "sks-canonical": "ehowgjardagevnrluult",
    "eq-solves-field": "ktmjmdzqrogauaevbktn",
    "sks-labour": "nspbmirochztcjijmcrx",
    "eq-substrate": "urjhmkhbgaxrofurpbgc",
}

# Accepted ERROR findings (cache_key -> "ticket — review_by"). Baseline so CI
# fails only on NEW errors. Keep tight; every entry is a tracked risk.
ACCEPTED_ERRORS = {
    # eq-canonical-internal: rate-limit table RLS trusts user_metadata.
    "rls_references_user_metadata_app_data_eq_intake_rate_limits_tenant_isolation":
        "SEC-2 user_metadata in RLS — review_by 2026-06-12",
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
        headers={"Authorization": f"Bearer {token}"},
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
    for name, ref in PROJECTS.items():
        try:
            lints = fetch(ref, token)
        except urllib.error.HTTPError as e:
            print(f"[{name}] ERROR fetching advisors: {e.code} {e.read().decode()[:200]}")
            return 2
        t = triage(lints)
        print(f"[{name}] ERROR {len(t['error'])} · WARN {len(t['warn'])} · INFO {len(t['info'])}")
        for nm, detail, ck in t["error"]:
            if ck in ACCEPTED_ERRORS:
                print(f"  ACCEPTED {nm}: {detail[:120]}  [{ACCEPTED_ERRORS[ck]}]")
            else:
                print(f"  NEW-ERROR {nm}: {detail[:160]}")
                new_errors.append(f"{name}: {nm} — {detail[:120]}")

    print("\n=== summary ===")
    if new_errors:
        print(f"{len(new_errors)} NEW ERROR-level security finding(s):")
        for e in new_errors:
            print(f"  - {e}")
        return 1
    print("No new ERROR-level security findings. (Accepted baseline still open — see register.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
