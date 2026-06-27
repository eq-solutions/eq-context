#!/usr/bin/env python3
"""RLS zero-rows probe — the public-key data-leak test.

For each sensitive table, issue a REST read using the project's PUBLIC
publishable key (the exact key that ships to browsers) and assert anon cannot
read rows. This is the truest test of "can a stranger pull our data": if a
`GET` with the public key returns rows, that's a live leak.

Safety: GET-only, never writes. The publishable keys here are public by design
(they're served to every browser client) — committing them is fine and they do
NOT match the secret-scanner's JWT pattern. SECURITY DEFINER *RPCs* are NOT
probed here because calling unknown functions could mutate data — those are a
manual/review check (see ops/security-register.md).

Scope: EQ projects only. SKS NSW Labour (the retiring app) is deliberately not
probed — it's SKS-tier, on its way out, and guarded against direct access. EQ is
the focus.

Interpretation per target:
  HTTP 200 + non-empty array  -> LEAK   (anon read data — FAIL)
  HTTP 200 + empty array      -> pass   (RLS returns no rows)
  HTTP 4xx (401/403/404/406)  -> pass   (table/schema not exposed to anon)
Exit 1 if any LEAK.

Run:  python3 scripts/rls_probe.py
"""
import json
import os
import sys
import urllib.error
import urllib.request

# Public publishable keys (sb_publishable_…) — safe to commit; served to browsers.
PROJECTS = {
    "eq-canonical": {
        "url": "https://jvknxcmbtrfnxfrwfimn.supabase.co",
        "key": "sb_publishable_Is2HjKJeBaGOjBSKXp8m7A_GyZpeqSr",
        "targets": ["workers", "worker_credentials", "worker_invites", "profiles", "licences", "tenants"],
    },
    "eq-canonical-internal": {
        "url": "https://zaapmfdkgedqupfjtchl.supabase.co",
        "key": "sb_publishable_W6mSlBaw3z9VuCGb_AVNKw_uhLaZsHS",
        "targets": ["people", "timesheets", "leave_requests", "projects", "sites", "workers", "worker_credentials"],
    },
    "sks-canonical": {
        "url": "https://ehowgjardagevnrluult.supabase.co",
        "key": "sb_publishable_hxFkxp_oA4NPvYoDINoFXw__0Z4Oqj2",
        "targets": ["sks_customers", "sks_staff", "sks_quotes", "sks_quotes_customers", "sks_quotes_contacts"],
    },
    "eq-solves-field": {
        "url": "https://ktmjmdzqrogauaevbktn.supabase.co",
        "key": "sb_publishable_rLY8fFG52GPjzZrrhoqATA_bOrRyfXL",
        "targets": ["people", "timesheets", "leave_requests", "nominations", "audit_log", "tenders"],
    },
}


# Known, tracked, time-boxed exposures. A leak listed here is reported LOUDLY
# every run but does NOT fail the build — so CI fails on NEW regressions while
# this stays visible with an owner + deadline (not silently green, not
# permanently red). See ops/security-register.md. Remove an entry the moment
# it's fixed. Format: "project.public.table": "ticket — review_by".
# (Empty — the only entries were SKS-Labour, removed when SKS-Labour was dropped
#  from the EQ gate. Add EQ exposures here if a tracked one is ever accepted.)
KNOWN_LEAKS = {}


def classify(status, body_text):
    """Pure decision: ('LEAK'|'empty'|'blocked', detail). Unit-tested."""
    if status == 200:
        try:
            rows = json.loads(body_text)
        except (ValueError, TypeError):
            return "blocked", "200 non-JSON"
        if isinstance(rows, list) and len(rows) > 0:
            return "LEAK", f"200 returned {len(rows)} row(s)"
        return "empty", "200 empty"
    return "blocked", f"{status}"


def probe(url, key, table):
    req = urllib.request.Request(
        f"{url}/rest/v1/{table}?select=*&limit=1",
        headers={"apikey": key, "Authorization": f"Bearer {key}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return classify(resp.status, resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return classify(e.code, "")
    except urllib.error.URLError as e:
        return "error", f"network: {e.reason}"


def main():
    only = os.environ.get("RLS_PROBE_PROJECT")  # optional single-project filter
    new_leaks, known = [], []
    print("=== RLS zero-rows probe (public key must read 0 rows) ===")
    for name, cfg in PROJECTS.items():
        if only and name != only:
            continue
        print(f"\n[{name}] {cfg['url']}")
        for table in cfg["targets"]:
            verdict, detail = probe(cfg["url"], cfg["key"], table)
            key = f"{name}.public.{table}"
            if verdict == "LEAK":
                if key in KNOWN_LEAKS:
                    print(f"  KNOWN-LEAK public.{table}: {detail}  [{KNOWN_LEAKS[key]}]")
                    known.append(key)
                else:
                    print(f"  LEAK   public.{table}: {detail}")
                    new_leaks.append(f"{key} ({detail})")
            else:
                mark = {"empty": "ok    ", "blocked": "ok    ", "error": "ERR   "}.get(verdict, "?     ")
                print(f"  {mark} public.{table}: {detail}")
    print("\n=== summary ===")
    if known:
        print(f"KNOWN/tracked leaks still open ({len(known)}) — see ops/security-register.md:")
        for k in known:
            print(f"  ! {k}")
    if new_leaks:
        print(f"\nNEW LEAK: {len(new_leaks)} untracked table(s) readable by the public key:")
        for l in new_leaks:
            print(f"  - {l}")
        return 1
    print("\nNo NEW anon-readable rows.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
