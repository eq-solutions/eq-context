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

# --- F13: false deploy-posture claims about eq-shell -------------------------
# Merging to eq-shell's main starts a production build that is live on
# core.eq.solutions 2-4s later, unattended, via Netlify's own GitHub App
# (installation 121276861). Any active-substrate sentence saying otherwise is
# false. This earns a check rather than another note because it has already been
# wrong twice while PASSING re-verification: its two supporting observations
# (deploy_source: api, cdp_enabled_contexts: [deploy-preview]) are still
# literally true, and only the inference drawn from them was wrong — so anyone
# re-checking the config finds it exactly as described and marks the note
# verified. See system/failures.md F13. Worst case it nearly caused: an
# auth-change PR annotated "manual-deploy-only", which makes merging read as a
# safe intermediate step rather than as deploying auth straight to production.
AUTO_DEPLOY_TOKENS = ("eq-shell", "core.eq.solutions")

# Repos where a manual trigger genuinely IS required. A closed, named set — the
# check allow-lists by name rather than inferring which repo a sentence is
# about, because guessing is what produced F13 in the first place.
MANUAL_DEPLOY_TOKENS = ("eq-cards", "eq-receipts", "eq-website", "sks-nsw-labour",
                        "cloudflare", "eq-intake")

DEPLOY_POSTURE = re.compile(
    r"manual[- ]deploy[- ]only|explicit[- ]only"
    r"|merged but not (?:live|deployed|shipped)"
    r"|not (?:yet )?deployed"
    r"|(?:doesn'?t|does not|never|won'?t) auto.?deploy"
    r"|deploy(?:s|ment)?[^.\n]{0,30}separate explicit step"
    r"|Royce to trigger|needs? (?:an? )?(?:explicit|manual) (?:deploy|trigger)",
    re.IGNORECASE,
)

# Quoting the false claim in order to correct it is not making the claim. Without
# this the correction trips the guard — and a guard that flags its own fix gets
# muted, which is exactly how the original claim survives.
# NOTE the shape here: only POSITIVE assertions count as corrections. An earlier
# draft included a bare `auto.?deploys?\b`, which matches "doesn't auto-deploy"
# — the single most common wording of the false claim — and silently suppressed
# it. The unit tests caught that; without them this guard would have shipped
# catching nothing, which is worse than no guard at all.
DEPLOY_CORRECTION = re.compile(
    r"\bF13\b|\bwrong\b|\bfalse\b|correct(?:ed|ion)|retract|stale claim"
    r"|no longer true|used to say|previously said"
    r"|does auto.?deploy|is auto.?deploy"
    r"|2-4 ?s\b|\bseconds later\b",
    re.IGNORECASE,
)

# failures.md defines this pattern (title, signal regex, note) by design; the
# script and its tests name it to test it.
DEPLOY_SCAN_EXEMPT = ("system/failures.md", "scripts/substrate_honesty.py",
                      "scripts/test_substrate_honesty.py")


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
def _qualified_in_context(repo, path, lineno, window=3, pattern=None):
    """True if `pattern` (default QUALIFIER) matches within +/-window lines."""
    pattern = pattern or QUALIFIER
    try:
        with open(os.path.join(repo, path), encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError:
        return False
    lo = max(0, lineno - 1 - window)
    hi = min(len(lines), lineno + window)
    return bool(pattern.search("".join(lines[lo:hi])))


def classify_deploy_posture(line, path=""):
    """Pure: does this line make a FALSE manual-deploy claim about eq-shell?

    Returns (bool, reason). Kept pure and unit-tested rather than trusted,
    because a noisy guard gets muted and a muted guard is how F13 survived two
    re-verifications. Every suppression below is a real false-positive seen in
    this substrate, not a hypothetical.
    """
    p = path.replace("\\", "/")
    if p in DEPLOY_SCAN_EXEMPT:
        return False, "file defines this pattern by design"
    low = line.lower()
    if not DEPLOY_POSTURE.search(line):
        return False, "no deploy-posture phrasing"
    if not any(t in low for t in AUTO_DEPLOY_TOKENS):
        return False, "not about eq-shell / core.eq.solutions"
    if any(t in low for t in MANUAL_DEPLOY_TOKENS):
        return False, "line also names a genuinely manual-deploy repo"
    if DEPLOY_CORRECTION.search(line):
        return False, "quoted in order to correct it"
    return True, ("claims eq-shell needs a manual deploy — merging to main is "
                  "live on core.eq.solutions 2-4s later, unattended (F13)")


def scan_deploy_posture():
    """git-grep the active tree for false eq-shell deploy-posture claims.

    Returns (findings, suppressed). Suppressed = historical record, or a
    correction sitting within a few lines.
    """
    repo = os.path.join(HERE, "..")
    findings, suppressed, seen = [], 0, set()
    for token in AUTO_DEPLOY_TOKENS:
        try:
            out = subprocess.run(
                ["git", "grep", "-n", "--no-color", "-i", token],
                capture_output=True, timeout=30, cwd=repo,
                encoding="utf-8", errors="replace",
            ).stdout or ""
        except Exception as e:  # not a git checkout, or git missing
            print(f"  (deploy-posture scan skipped for {token}: {e})")
            continue
        for line in out.splitlines():
            parts = line.split(":", 2)
            if len(parts) < 3:
                continue
            path, lineno, content = parts
            path = path.replace("\\", "/")
            key = (path, lineno)
            if key in seen:
                continue
            hit, reason = classify_deploy_posture(content, path)
            if not hit:
                continue
            seen.add(key)
            if is_historical(path) or _qualified_in_context(
                repo, path, int(lineno), pattern=DEPLOY_CORRECTION
            ):
                suppressed += 1
                continue
            findings.append((path, lineno, content.strip()[:110], reason))
    return findings, suppressed


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
            # encoding pinned rather than text=True: text=True decodes with the
            # locale codec, cp1252 on Windows, and this substrate is full of em
            # dashes — a grep whose output includes one raises UnicodeDecodeError
            # and leaves stdout None. LATENT here today, not active: the sole
            # current token (a Supabase project ref) only ever matches ASCII
            # lines, verified 2026-08-15 (53 hits, clean). It bites the moment a
            # token matches prose — which the deploy-posture scan below does, and
            # that is how this was found. Pinned in both places so the next token
            # added to the manifest doesn't silently turn this scan into a no-op.
            out = subprocess.run(
                ["git", "grep", "-n", "--no-color", token],
                capture_output=True, timeout=30, cwd=repo,
                encoding="utf-8", errors="replace",
            ).stdout or ""
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

    print("\n--- Deploy-posture scan (F13: eq-shell claimed manual-deploy) ---")
    posture, posture_suppressed = scan_deploy_posture()
    if posture_suppressed:
        print(f"  ({posture_suppressed} historical or self-correcting mention(s) — exempt.)")
    if posture:
        for path, lineno, content, reason in posture:
            print(f"  FALSE {path}:{lineno}  {content}")
            print(f"        ^ {reason}")
    else:
        print("  ok    no active claim that eq-shell needs a manual deploy")

    print("\n=== summary ===")
    total = len(drift) + len(stale) + len(posture)
    if total == 0:
        print("Substrate is honest: every checked fact matches reality.")
        return 0
    print(f"{total} honesty issue(s) found:")
    for d in drift:
        print(f"  - DRIFT: {d}")
    for path, lineno, content, _ in stale:
        print(f"  - STALE: {path}:{lineno}")
    for path, lineno, content, _ in posture:
        print(f"  - FALSE DEPLOY POSTURE: {path}:{lineno}")
    if strict:
        print("\nSUBSTRATE_HONESTY_STRICT=1 -> failing the build.")
        return 1
    print("\n(report-only — set SUBSTRATE_HONESTY_STRICT=1 to make this a hard gate.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
