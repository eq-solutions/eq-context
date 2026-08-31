#!/usr/bin/env python3
"""Live-definition drift check for the shared ehow app_data object registry.

WHY THIS EXISTS (2026-09-01, eq-field session): eq-field and eq-shell edit a
handful of the same app_data objects on ehow through two migration pipelines
that don't read each other's ledger (eq-field: supabase_migrations.schema_
migrations; eq-shell: app_data._eq_migrations). Postgres has no partial
CREATE OR REPLACE, so whichever pipeline applies last always wins the whole
object. Two narrow guards already existed before this script:
  - eq-field's migration-security-invoker-guard.test.js (checks ONE clause
    on the field_people/field_people_removed VIEWS)
  - eq-shell's migrate-tenants.mjs live-fingerprint warning (fires only
    when eq-shell's OWN migration is about to replace 1 of 7 named
    FUNCTIONS; logs a warning nobody outside that CI run ever sees)
Neither would have caught the incident that motivated this script: eq-shell's
0249_field_people_view_parity.sql changed field_people's/field_people_
removed's column list (added a `group` alias, stubbed `employment_type` to
NULL) — a shape neither existing guard was built to look for, on an object
one of them doesn't even cover. See eq-context sessions/2026-09-01.md and
eq/identity/IDENTITY-MODEL.md §3.3.3 for the full incident history.

WHAT THIS DOES DIFFERENTLY: instead of one more shape-specific check, this
diffs the FULL live definition (pg_get_viewdef / pg_get_functiondef) of
every object in eq/identity/shared-db-objects.json against a checked-in
snapshot (eq/identity/shared-db-objects.snapshot.json). Any change to any
registered object — column list, security_invoker, grants, function body,
or the object disappearing entirely — fails this check, regardless of which
repo's pipeline caused it, or whether it was hand-applied outside both.

This is intentionally the ONLY guard that doesn't care about the object's
kind (view vs function) or the specific way it drifted — see the artifact
this session produced for why the pattern-specific guards keep missing new
shapes of the same underlying problem.

Auth: SUPABASE_ACCESS_TOKEN (Management API, same token security-audit.yml
already uses for scripts/security_audit.py — no new secret needed). Without
it this script no-ops cleanly, matching that script's convention exactly.

Usage:
    python3 scripts/check_shared_object_drift.py                 # check (CI mode)
    python3 scripts/check_shared_object_drift.py --update-snapshot  # rebaseline after a reviewed, intentional change
    SUPABASE_ACCESS_TOKEN=sbp_... python3 scripts/check_shared_object_drift.py

Exit codes: 0 = clean (or token unset — no-op), 1 = drift/missing/unbaselined found.
"""
import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTRY_PATH = os.path.join(HERE, "..", "eq", "identity", "shared-db-objects.json")
SNAPSHOT_PATH = os.path.join(HERE, "..", "eq", "identity", "shared-db-objects.snapshot.json")

API = "https://api.supabase.com/v1/projects"
# api.supabase.com sits behind Cloudflare, which 403s the default urllib
# User-Agent ("error code: 1010"). Same fix as scripts/security_audit.py.
USER_AGENT = "eq-context-shared-object-drift (+https://github.com/eq-solutions/eq-context)"

PREVIEW_CHARS = 400


# ── pure logic (unit-tested in test_shared_object_drift.py) ────────────────

def normalize(sql_text):
    """LF-normalise + strip trailing whitespace per line, matching eq-shell's
    migrate-tenants.mjs checksum convention (its 'EOL NOTE') so a Windows
    checkout and a CI run never manufacture phantom drift from line endings.
    """
    if sql_text is None:
        return None
    text = sql_text.replace("\r\n", "\n")
    return "\n".join(line.rstrip() for line in text.split("\n")).strip()


def fingerprint(sql_text):
    norm = normalize(sql_text)
    if norm is None:
        return None
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


def diagnose(live_def, snapshot_entry):
    """Pure decision: given a freshly-fetched live definition (or None if the
    object no longer exists / couldn't be fetched) and this object's stored
    snapshot entry (or None if never baselined), decide what happened.

    Returns (status, detail) where status is one of:
      'clean'        - live matches the snapshot, nothing to do
      'drift'        - live exists but no longer matches the snapshot
      'missing_live' - object is registered but doesn't exist live anymore
      'unbaselined'  - object is registered but has no snapshot entry yet
    """
    live_hash = fingerprint(live_def)

    if live_hash is None:
        return "missing_live", None
    if snapshot_entry is None:
        return "unbaselined", live_hash
    if live_hash == snapshot_entry.get("sha256"):
        return "clean", live_hash
    return "drift", live_hash


# ── I/O ──────────────────────────────────────────────────────────────────

def load_registry():
    with open(REGISTRY_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def load_snapshot():
    if not os.path.exists(SNAPSHOT_PATH):
        return {"objects": {}}
    with open(SNAPSHOT_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def save_snapshot(snapshot):
    snapshot["generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(SNAPSHOT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(snapshot, fh, indent=2, sort_keys=False)
        fh.write("\n")


def object_key(obj):
    return f"{obj['schema']}.{obj['name']}"


def fetch_live_def(project_ref, token, obj):
    """This object's current live definition via the Supabase Management API
    (POST /v1/projects/{ref}/database/query) — the same endpoint eq-shell's
    migrate-tenants.mjs uses. No service-role key, no exec_sql backdoor.
    schema/name come from our own registry file (not user input).
    """
    schema, name, kind = obj["schema"], obj["name"], obj["kind"]
    if kind == "view":
        sql = (
            "select pg_get_viewdef(c.oid, true) as def from pg_class c "
            "join pg_namespace n on n.oid = c.relnamespace "
            f"where n.nspname = '{schema}' and c.relname = '{name}';"
        )
    elif kind == "function":
        sql = (
            "select pg_get_functiondef(p.oid) as def from pg_proc p "
            "join pg_namespace n on n.oid = p.pronamespace "
            f"where n.nspname = '{schema}' and p.proname = '{name}' "
            "order by p.oid limit 1;"
        )
    else:
        raise ValueError(f"unknown object kind {kind!r} for {schema}.{name}")

    req = urllib.request.Request(
        f"{API}/{project_ref}/database/query",
        data=json.dumps({"query": sql}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        rows = json.loads(resp.read())
    if not rows:
        return None
    return rows[0].get("def")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--update-snapshot", action="store_true",
        help="Rebaseline the snapshot from live defs instead of checking. "
             "Use only after reviewing WHY each changed object's definition "
             "moved — this is the 'I looked, this is intentional' step.",
    )
    args = parser.parse_args()

    token = os.environ.get("SUPABASE_ACCESS_TOKEN")
    if not token:
        print("SUPABASE_ACCESS_TOKEN not set — skipping shared-object drift check.")
        print("Set a read-only Supabase personal access token as the CI secret")
        print("SUPABASE_ACCESS_TOKEN to enable this gate (same token security-audit.yml uses).")
        return 0

    registry = load_registry()
    project_ref = registry["project_ref"]
    objects = registry["objects"]
    snapshot = load_snapshot()
    snap_objects = snapshot.setdefault("objects", {})

    results = {"clean": [], "drift": [], "missing_live": [], "unbaselined": [], "fetch_error": []}

    for obj in objects:
        key = object_key(obj)
        try:
            live_def = fetch_live_def(project_ref, token, obj)
        except urllib.error.HTTPError as e:
            detail = e.read().decode()[:300]
            print(f"[{key}] ERROR fetching live definition: {e.code} {detail}")
            results["fetch_error"].append(key)
            continue
        except urllib.error.URLError as e:
            print(f"[{key}] ERROR fetching live definition: {e}")
            results["fetch_error"].append(key)
            continue

        status, live_hash = diagnose(live_def, snap_objects.get(key))
        results[status].append(key)

        if args.update_snapshot:
            if live_hash is None:
                print(f"[{key}] SKIP (object not found live) — not writing a snapshot entry")
                continue
            snap_objects[key] = {
                "schema": obj["schema"],
                "name": obj["name"],
                "kind": obj["kind"],
                "sha256": live_hash,
                "preview": normalize(live_def)[:PREVIEW_CHARS],
            }
            print(f"[{key}] baselined ({live_hash[:12]})")
            continue

        if status == "clean":
            print(f"[{key}] ok  ({live_hash[:12]})")
        elif status == "drift":
            old = snap_objects.get(key, {})
            print(f"[{key}] DRIFT DETECTED")
            print(f"    snapshot hash: {old.get('sha256', '?')[:12]}  ({old.get('preview', '')[:120]}...)")
            print(f"    live hash:     {live_hash[:12]}")
            print(f"    --- full live definition ---\n{live_def}\n    --- end live definition ---")
        elif status == "missing_live":
            print(f"[{key}] MISSING — registered object no longer exists live "
                  f"(dropped, renamed, or a typo in shared-db-objects.json)")
        elif status == "unbaselined":
            print(f"[{key}] UNBASELINED — registered but has no snapshot entry yet "
                  f"(live hash {live_hash[:12]}). Run with --update-snapshot after "
                  f"confirming this is the correct current definition.")

    if args.update_snapshot:
        save_snapshot(snapshot)
        print(f"\nSnapshot written: {SNAPSHOT_PATH}")
        return 0

    problems = results["drift"] + results["missing_live"] + results["unbaselined"] + results["fetch_error"]
    print(f"\n{len(results['clean'])} clean, {len(problems)} needing attention "
          f"({len(results['drift'])} drift, {len(results['missing_live'])} missing, "
          f"{len(results['unbaselined'])} unbaselined, {len(results['fetch_error'])} fetch errors)")

    if problems:
        print(
            "\nA registered object's live definition no longer matches what's "
            "checked in. This means eq-field's or eq-shell's migration pipeline "
            "(or a hand-applied change via the Supabase MCP/dashboard) replaced "
            "something the OTHER side also depends on. Before rebaselining:\n"
            "  1. Find what changed it — check both ledgers' recent entries "
            "(app_data._eq_migrations on ehow, and eq-field's supabase/migrations/).\n"
            "  2. Check both repos' client/query code for anything reading the "
            "old shape (this is exactly what neither pipeline's own guard can see).\n"
            "  3. Only then: python3 scripts/check_shared_object_drift.py --update-snapshot\n"
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
