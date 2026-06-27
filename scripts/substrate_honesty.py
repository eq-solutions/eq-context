#!/usr/bin/env python3
"""Substrate honesty check — verify load-bearing facts against reality.

The substrate is the source of truth every agent reads. Its danger is that it is
*passive*: a wrong fact does not fail to help, it launders a bad premise into the
whole fleet with authority. On 2026-06-22 the substrate pointed agents at Supabase
project `urjh…` for weeks after it was DELETED. This check makes that class of lie
visible.

It reads system/substrate-facts.yml — the checkable subset of the substrate's
load-bearing claims — and verifies each against reality:

  1. Supabase project liveness  — a 'live' ref must answer (REST returns 401 with
     no key); a 'deleted' ref's host must be gone. Secret-free: no API key, GET
     the unauthenticated REST root only.
  2. Deploy-URL liveness        — a 'live' URL must answer 2xx/3xx. A 4xx root is
     noted (SPA / auth-gate), a 5xx / connection failure is drift.
  3. Stale-reference scan       — a 'forbidden' ref (a deleted project id) must
     not appear as a *live* mention in the active tree (archive/ + sessions/ are
     historical record and exempt; a 'deleted/retired/…'-qualified mention is OK).

Report-only by default: prints a table and exits 0 so it can run on every PR
without blocking while the signal earns trust. Set SUBSTRATE_HONESTY_STRICT=1 to
exit non-zero on any drift (the eventual gate).

SKS-live (nspb…) is intentionally absent from the manifest — SKS-tier, retiring,
and guarded against direct access. EQ is the focus.

Run:  python scripts/substrate_honesty.py
"""
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "..", "system", "substrate-facts.yml")

# Historical-record locations: append-only logs and dated snapshots legitimately
# reference dead systems — an agent reads them as history, not current truth — so
# they are exempt. The scan guards the *active* substrate only. The manifest and
# this script name the forbidden token by design, so they are exempt too.
SCAN_EXEMPT_FILES = ("system/substrate-facts.yml", "scripts/substrate_honesty.py")
DATED_SNAPSHOT = re.compile(r"\d{4}-\d{2}-\d{2}\.md$")
# A mention within a few lines of any of these is a historical/qualified reference
# ("migrated from urjh", "urjh was retired", "old: urjh -> ehow") — not a live claim.
QUALIFIER = re.compile(
    r"delet|retir|\bdead\b|former|\bwas\b|gone|decommiss|legacy|removed|\bRIP\b"
    r"|no longer|migrat|resolved|\bold\b|supersed|replaced|cutover|->|→",
    re.IGNORECASE,
)


def is_historical(path):
    """True if path is append-only history / a dated snapshot (scan-exempt)."""
    p = path.replace("\\", "/")
    if p.startswith(("archive/", "sessions/")):
        return True
    if "/changelog/" in p or p.endswith("changelog.md"):
        return True
    base = p.rsplit("/", 1)[-1]
    if base in ("decisions.md", "lessons.md"):
        return True
    if DATED_SNAPSHOT.search(base):
        return True
    if p in SCAN_EXEMPT_FILES:
        return True
    return False


# --- pure classifiers (unit-tested in test_substrate_honesty.py) -------------
def classify_supabase(http_status, conn_ok):
    """Map a probe result to ('live'|'dead'|'unknown', detail).

    conn_ok is False when the host could not be reached at all (DNS / TCP) — that
    is how a deleted project presents (calibrated against urjh, 2026-06-27).
    A reachable project's REST root answers 401 with no key (calibrated against
    the four live EQ projects).
    """
    if not conn_ok:
        return "dead", "connection failed (host gone)"
    if http_status in (200, 400, 401, 403, 406):
        return "live", f"REST responded {http_status}"
    if http_status and 500 <= http_status < 600:
        return "dead", f"HTTP {http_status} (server error / paused)"
    return "unknown", f"HTTP {http_status}"


def classify_deploy(http_status, conn_ok):
    """Map a probe result to ('live'|'responds'|'dead', detail)."""
    if not conn_ok:
        return "dead", "connection failed"
    if http_status and 200 <= http_status < 400:
        return "live", f"HTTP {http_status}"
    if http_status and 400 <= http_status < 500:
        return "responds", f"HTTP {http_status} (deploy up; root gated / SPA)"
    return "dead", f"HTTP {http_status}"


def verdict(expected, observed):
    """Pure: is an observed liveness consistent with the manifest's claim?

    Returns ('ok'|'info'|'DRIFT', note).
    """
    if expected == "live":
        if observed == "live":
            return "ok", ""
        if observed == "responds":
            return "info", "claimed live; root non-2xx (SPA/auth?) — host up"
        return "DRIFT", "claimed LIVE but reality looks DEAD"
    if expected == "deleted":
        if observed == "dead":
            return "ok", ""
        return "DRIFT", "claimed DELETED but host still ANSWERS"
    return "info", f"unhandled expected={expected!r}"


# --- network probes ----------------------------------------------------------
def _http_status(url, timeout=15):
    """(status:int|None, conn_ok:bool). conn_ok False on DNS/TCP failure."""
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, True
    except urllib.error.HTTPError as e:
        return e.code, True  # server answered with an error status — host is up
    except urllib.error.URLError:
        return None, False   # could not reach host at all
    except Exception:
        return None, False


def probe_supabase(ref):
    status, ok = _http_status(f"https://{ref}.supabase.co/rest/v1/")
    return classify_supabase(status, ok)


def probe_deploy(url):
    status, ok = _http_status(url)
    return classify_deploy(status, ok)


# --- stale-reference scan ----------------------------------------------------
def _qualified_in_context(repo, path, lineno, window=3):
    """True if a QUALIFIER word appears within +/-window lines of lineno."""
    try:
        with open(os.path.join(repo, path), encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError:
        return False
    lo = max(0, lineno - 1 - window)
    hi = min(len(lines), lineno + window)
    return bool(QUALIFIER.search("".join(lines[lo:hi])))


def scan_forbidden(forbidden):
    """git-grep the active tree for deleted refs used as *live* mentions.

    Returns (findings, suppressed). A hit is suppressed when its file is historical
    record or a qualifier word sits within a few lines of it — so only an
    unqualified, current claim (the urjh footgun) survives to be reported.
    """
    repo = os.path.join(HERE, "..")
    findings, suppressed = [], 0
    for entry in forbidden:
        token = entry.get("token", "")
        reason = entry.get("reason", "")
        if not token:
            continue
        try:
            out = subprocess.run(
                ["git", "grep", "-n", "--no-color", token],
                capture_output=True, text=True, timeout=30, cwd=repo,
            ).stdout
        except Exception as e:  # not a git checkout, or git missing
            print(f"  (stale-ref scan skipped for {token}: {e})")
            continue
        for line in out.splitlines():
            parts = line.split(":", 2)
            if len(parts) < 3:
                continue
            path, lineno, content = parts
            path = path.replace("\\", "/")
            if is_historical(path) or _qualified_in_context(repo, path, int(lineno)):
                suppressed += 1
                continue
            findings.append((path, lineno, content.strip()[:100], reason))
    return findings, suppressed


# --- manifest loading --------------------------------------------------------
def load_manifest():
    try:
        import yaml
    except ImportError:
        print("PyYAML not installed — run `pip install pyyaml` to use this check.")
        print("(CI installs it automatically; this is a local-run hint.)")
        sys.exit(0)
    with open(MANIFEST, encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    m = load_manifest()
    strict = os.environ.get("SUBSTRATE_HONESTY_STRICT") == "1"
    drift = []

    print("=== Substrate honesty check ===")
    print("Verifying load-bearing facts in system/substrate-facts.yml against reality.\n")

    print("--- Supabase projects ---")
    for p in m.get("supabase_projects", []):
        observed, detail = probe_supabase(p["ref"])
        status, note = verdict(p["status"], observed)
        mark = {"ok": "ok   ", "info": "info ", "DRIFT": "DRIFT"}.get(status, "?    ")
        line = f"  {mark} {p['label']:<24} claim={p['status']:<8} reality={observed:<8} ({detail})"
        if note:
            line += f"  <- {note}"
        print(line)
        if status == "DRIFT":
            drift.append(f"supabase {p['label']} ({p['ref']}): {note}")

    print("\n--- Deploy URLs ---")
    for d in m.get("deploy_urls", []):
        observed, detail = probe_deploy(d["url"])
        status, note = verdict(d["status"], observed)
        mark = {"ok": "ok   ", "info": "info ", "DRIFT": "DRIFT"}.get(status, "?    ")
        line = f"  {mark} {d['label']:<24} claim={d['status']:<8} reality={observed:<8} ({detail})"
        if note:
            line += f"  <- {note}"
        print(line)
        if status == "DRIFT":
            drift.append(f"deploy {d['label']} ({d['url']}): {note}")

    print("\n--- Stale-reference scan (deleted refs used as live) ---")
    stale, suppressed = scan_forbidden(m.get("forbidden_live_refs", []))
    if suppressed:
        print(f"  ({suppressed} historical/qualified mention(s) in archive, changelogs, "
              "dated snapshots, or beside a 'retired/migrated' note — exempt.)")
    if stale:
        for path, lineno, content, reason in stale:
            print(f"  STALE {path}:{lineno}  {content}")
            print(f"        ^ {reason}")
    else:
        print("  ok    no deleted refs used as live mentions in the active tree")

    print("\n=== summary ===")
    total = len(drift) + len(stale)
    if total == 0:
        print("Substrate is honest: every checked fact matches reality.")
        return 0
    print(f"{total} honesty issue(s) found:")
    for d in drift:
        print(f"  - DRIFT: {d}")
    for path, lineno, content, _ in stale:
        print(f"  - STALE: {path}:{lineno}")
    if strict:
        print("\nSUBSTRATE_HONESTY_STRICT=1 -> failing the build.")
        return 1
    print("\n(report-only — set SUBSTRATE_HONESTY_STRICT=1 to make this a hard gate.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
