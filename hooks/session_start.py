#!/usr/bin/env python3
"""
SessionStart gate — RUNG 4 detection.

Replaces the 13-step §1 / §0.6 ritual with something that cannot be skipped and
costs no ceremony. Prints, unprompted, at every session start:

  1. FRESHNESS   — digest.md age. >2 days = the read path may be lying (failure F1).
  2. NEEDS YOU   — the digest's own alert section, which otherwise waits in a file
                   nobody opens (it sat unread for 12 days).
  3. GOALS       — whether TODAY.md has any. If UNSET, no assistant may defer work
                   by appeal to a deadline (failure F3 — the phantom-deadline incident).
  4. RATCHET     — failures whose guard is overdue for promotion (system/failures.md).
  5. CLAIMS      — active incident claims (system/incident-claims.md) that overlap
                   this session's own Needs You list — stops duplicate investigation
                   of the same finding by concurrent sessions.
  6. HOOKS       — core.hooksPath resolves to .githooks at every scope that can set
                   it (--local and, if enabled, --worktree). The identical
                   "pre-commit silently doesn't run" symptom has now recurred via
                   3 distinct mechanisms on 3 different dates (failure F10).

Reads the LOCAL CLONE, never a URL. The URL is what lied on 2026-07-11.
Fails open but loud: a silent guard is the bug we are fixing.
"""
import os, re, subprocess, sys
from datetime import datetime, timezone

# Windows consoles default to cp1252; digest.md's "Needs you" section contains
# emoji (🟠 / ⚠) that the gate echoes back. Without this, print() raises
# UnicodeEncodeError and the ENTIRE gate output is lost — a silent guard, the
# exact failure class this file exists to kill. Force UTF-8; no-op on Linux.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.environ.get("EQ_CONTEXT", r"C:\Projects\eq-context")
if not os.path.isdir(ROOT):
    for alt in ("/sessions/*/mnt/Projects/eq-context", "C:/Projects/eq-context"):
        import glob
        hits = glob.glob(alt)
        if hits:
            ROOT = hits[0]
            break

out = []


def read(rel):
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except Exception:
        return ""


def age_days(datestr):
    try:
        d = datetime.strptime(datestr[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - d).days
    except Exception:
        return None


# --- 0. SYNC (F1, the half the freshness check cannot see) -------------------
# digest.md's stamp is a FILE MTIME, not a sync check. A clone 34 commits behind
# still carries a digest.md stamped today, so FRESHNESS below prints "ok" while
# every file the session reads is stale. That is not hypothetical: on 2026-08-15
# this gate reported "F13 (rung 1, 2x) PROMOTION DUE" off a stale clone when
# origin/main already had F13 at rung 4 with the guard built and merged. The
# session then spent its opening turn acting on a guard that was not overdue.
#
# F1's lesson is "freshness is not truth". A timestamp cannot express staleness
# that arrives as *absence* of commits, so compare refs, not mtimes.
def git(*args, timeout=15):
    try:
        r = subprocess.run(
            ("git", "-C", ROOT) + args, capture_output=True, text=True, timeout=timeout
        )
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


# origin/main is itself only as current as the last fetch. If nothing has
# fetched recently the ref is stale and HEAD == origin/main proves nothing, so
# refresh it first. Same 10-minute cadence the UserPromptSubmit hook uses; fails
# open on a network stall rather than blocking the session.
try:
    fh = os.path.join(ROOT, ".git", "FETCH_HEAD")
    stale = (not os.path.exists(fh)) or (
        (datetime.now(timezone.utc).timestamp() - os.path.getmtime(fh)) > 600
    )
    if stale:
        git("fetch", "origin", "main", timeout=20)
except Exception:
    pass

_local = git("rev-parse", "HEAD")
_remote = git("rev-parse", "origin/main")
if not _local or not _remote:
    out.append(
        "SYNC       ? cannot resolve HEAD or origin/main — verify the clone by hand.\n"
        "           Do not assume the substrate you are reading is current."
    )
elif _local == _remote:
    out.append(f"SYNC       ok — HEAD == origin/main ({_local[:7]})")
else:
    # Only BEHIND is staleness. Being ahead is just local work not pushed yet,
    # which is the normal state of every feature branch — alarming on it would
    # make this line fire in most sessions, and a guard that always fires is
    # one people learn to scroll past. That is how F10's guard reached "rung 4
    # on paper, rung 0 in practice".
    _behind = int(git("rev-list", "--count", f"{_local}..{_remote}") or 0)
    _ahead = int(git("rev-list", "--count", f"{_remote}..{_local}") or 0)
    if _behind:
        out.append(
            f"SYNC       *** STOP *** clone is behind {_behind}"
            + (f" / ahead {_ahead}" if _ahead else "")
            + " vs origin/main.\n"
            "           Every substrate file you read may be stale, and the checks below\n"
            "           (FRESHNESS, NEEDS YOU, GOALS, RATCHET) are computed from those\n"
            "           same stale files — treat all of them as unverified.\n"
            "           A current digest.md stamp does NOT mean the clone is current.\n"
            "           Reconcile against origin/main before trusting substrate content."
        )
    else:
        out.append(
            f"SYNC       ok — {_ahead} local commit(s) ahead of origin/main, none missing"
        )

# --- 1. FRESHNESS (F1) ------------------------------------------------------
digest = read("digest.md")
m = re.search(r"_(\d{4}-\d{2}-\d{2})[^\n]*UTC", digest)
if m:
    a = age_days(m.group(1))
    if a is None:
        out.append("FRESHNESS  ? digest.md stamp unparseable — verify manually.")
    elif a > 2:
        out.append(
            f"FRESHNESS  *** STOP *** digest.md reports {m.group(1)} ({a} days old).\n"
            f"           The substrate read path has served 8-12 day stale content before\n"
            f"           with a 200 OK (failure F1). Verify against the LOCAL CLONE\n"
            f"           before trusting anything you loaded. Do not proceed on this."
        )
    else:
        out.append(f"FRESHNESS  ok — digest.md {m.group(1)} ({a}d)")
else:
    out.append("FRESHNESS  *** digest.md not found or unstamped — you are flying blind. ***")

# --- 1b. REVIEW CLOCK (staleness of the files this gate is about to mandate) --
# FRESHNESS above asks "is the clone current". This asks the other half: "is the
# CONTENT current". A file can be perfectly synced and 62 days out of date, and
# until 2026-08-15 nothing anywhere noticed — 174 files claimed status: live and
# 82 had not been touched in a month.
#
# scripts/review_clock.py gates the whole repo in CI, which is rung 3: it catches
# staleness after the damage. This is the rung-4 half. The action worth
# intercepting is not a file aging — no write to hook — it is a SESSION TRUSTING
# a stale file, and that happens here, at the moment the gate tells you to read
# it. So this checks only CLAUDE.md section 1 step 4's mandated chain, not all 91
# state files. Precision is the point: a gate that lists twenty files nobody is
# about to read is a gate that gets skimmed, which is F10's failure mode.
#
# The rule is IMPORTED, not restated, for the same reason as RATCHET below.
try:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
    from review_clock import (
        cadence_days as _cadence,
        classify as _classify,
        days_overdue as _overdue,
        parse_date as _pdate,
        parse_frontmatter as _pfm,
        review_due as _due,
    )

    # The mandated chain is IMPORTED from session_start_budget.py, which already
    # owns that list and carries the "keep this in step with CLAUDE.md section 1
    # step 4" warning. Retyping it here would create a second copy to drift —
    # and a copy that drifts SHORT goes quiet rather than loud, so nobody would
    # find out. Every tier is checked because the tier question has not been
    # asked yet when this runs.
    from session_start_budget import ALWAYS as _always, TIERS as _tiers

    _today = datetime.now(timezone.utc).date()
    _mandated = list(_always) + [f for files in _tiers.values() for f in files]
    _stale = []
    for _rel in _mandated:
        _text = read(_rel)
        if not _text:
            continue
        _fm = _pfm(_text)
        _kind = _classify(_rel, _fm)
        _n = _overdue(
            _due(_pdate(_fm.get("last_updated", "")),
                 _cadence(_kind, _fm.get("read_priority")),
                 _pdate(_fm.get("review_by", ""))),
            _today,
        )
        if _n:
            _stale.append((_n, _rel, _kind))
    _stale.sort(reverse=True)

    if _stale:
        out.append(f"REVIEW     *** {len(_stale)} mandated file(s) past their review clock ***")
        for _n, _rel, _kind in _stale:
            out.append(f"           {_rel} — {_n}d overdue")
        out.append("           Treat their claims as leads, not facts. This is about TRUST,")
        out.append("           not priority — nothing here is a deadline you owe anyone.")
    else:
        out.append(f"REVIEW     ok — all {len(_mandated)} mandated files within their review clock")
except Exception as exc:  # a broken clock must never silence the rest of the gate
    out.append(f"REVIEW     ? clock unavailable ({exc}) — check by hand.")

# --- 2. NEEDS YOU -----------------------------------------------------------
nm = re.search(r"##\s*⚠?\s*Needs you[^\n]*\n(.*?)(?=\n##\s)", digest, re.S)
items = []
if nm:
    items = [l.strip() for l in nm.group(1).splitlines() if l.strip().startswith("-")]
    if items:
        out.append("NEEDS YOU  " + f"{len(items)} item(s):")
        for it in items[:5]:
            out.append("           " + it[:110])
    else:
        out.append("NEEDS YOU  clear")

# --- 3. GOALS (F3 — the phantom-deadline incident) -----------------------------------
today = read("system/TODAY.md")
if "status: UNSET" in today or "Goals: UNSET" in today or "claims: []" in today:
    out.append(
        "GOALS      *** UNSET *** TODAY.md has no owned goals.\n"
        "           You therefore have NO BASIS to defer, deprioritise, or justify work\n"
        "           by appeal to a deadline or quarterly outcome. Do not borrow one from\n"
        "           an old file. Do not invent one. Say plainly that goals are unset.\n"
        "           (On 2026-07-11 a phantom deadline nobody owned steered two weeks of\n"
        "           sessions. Nobody owned it. Every CI check passed green — failure F3.)"
    )
else:
    ta = age_days((re.search(r"last_updated:\s*(\S+)", today) or [None, ""])[1])
    if ta is not None and ta > 7:
        out.append(f"GOALS      set, but TODAY.md is {ta}d old — treat its numbers as leads, not facts.")
    else:
        out.append("GOALS      set")

# --- 4. RATCHET (promotions due) --------------------------------------------
# The rule lives in hooks/ratchet_rules.py and is IMPORTED, not restated:
# this gate and .github/scripts/guard_ratchet.py used to carry two copies that
# already disagreed (hardcoded `rung < 4` here vs `rung < target` there), which
# is the shape of F13.
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from ratchet_rules import scan as _ratchet_scan

    found = _ratchet_scan(read("system/failures.md"))
except Exception as exc:  # never let a broken classifier silence the gate
    found = None
    out.append(f"RATCHET    ? classifier unavailable ({exc}) — check by hand.")

if found is not None:
    overdue = [f for f in found if f[5] == "OVERDUE"]
    due = [f for f in found if f[5] == "DUE"]
    if overdue:
        out.append("RATCHET    *** PROMOTION DUE *** a guard has failed twice and must climb:")
        for fid, title, rec, rung, target, _ in overdue:
            out.append(f"           {fid} (rung {rung} -> {target}, {rec}x) — {title[:66]}")
        out.append("           A lesson that failed twice IS the thing that failed. Promote it to a hook.")
    if due:
        out.append("RATCHET    below declared target (not yet recurred, guard already owed):")
        for fid, title, rec, rung, target, _ in due:
            out.append(f"           {fid} (rung {rung} -> {target}) — {title[:66]}")
    if not overdue and not due:
        out.append("RATCHET    no promotions due")

# --- 5. CLAIMS (duplicate-investigation guard) ------------------------------
# Cross-references active rows in system/incident-claims.md against this
# session's own "Needs you" items (already parsed above as `items`, if any)
# by ID substring match (SEC-N / F-N / a distinctive slug) — not free-text
# fuzzy matching. Never blocks; loudly flags so a session doesn't start an
# independent investigation of something another live session already claimed.
claims_raw = read("system/incident-claims.md")
claim_rows = re.findall(
    r"^\|\s*([A-Za-z0-9_.\-]+)\s*\|\s*([^|]*?)\s*\|\s*([0-9T:\-]+Z?)\s*\|\s*([^|]*?)\s*\|\s*$",
    claims_raw, re.M
)
STALE_HOURS = 6
active_claims = []
for cid, who, since, notes in claim_rows:
    cid = cid.strip()
    if not cid or re.match(r"^-+$", cid):  # markdown header separator row, not a real claim
        continue
    age_h = None
    try:
        since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
        age_h = (datetime.now(timezone.utc) - since_dt).total_seconds() / 3600
    except Exception:
        pass
    active_claims.append((cid, who.strip(), age_h, notes.strip()))

matches = []
for it in items:
    for cid, who, age_h, notes in active_claims:
        if cid and cid in it:
            if age_h is not None and age_h > STALE_HOURS:
                tag = f"STALE {age_h:.1f}h — claim may be abandoned, but read its notes first"
            elif age_h is not None:
                tag = f"claimed {age_h:.1f}h ago"
            else:
                tag = "claimed"
            label = f"{cid} [{tag}] by {who}" + (f" — {notes}" if notes else "")
            matches.append(label)

if matches:
    out.append("CLAIMS     *** possible duplicate work — check before investigating ***")
    for mtext in matches[:5]:
        out.append("           " + mtext[:140])
    out.append("           system/incident-claims.md")
elif active_claims:
    out.append(f"CLAIMS     {len(active_claims)} active claim(s), none overlap today's Needs You list")
else:
    out.append("CLAIMS     none active")

# --- 6. HOOKS (core.hooksPath resolution — F10) -------------------------------
# The identical "pre-commit silently doesn't run" symptom has recurred through
# three distinct mechanisms: 2026-05-24 hooksPath pointed at a directory missing
# the real hook (prose only, system/lessons.md, no guard); 2026-08-04 hooksPath
# pointed at .git/hooks via an untracked shadow copy of the secret-scanning
# script (failure F8); 2026-08-05 a --worktree-scope override on THIS checkout
# shadowed a correct --local value of .githooks, found only by hand mid-
# investigation (eq/pending.md, "Correction, 2026-08-05"). None of the three had
# a check that runs every session until now. system/failures.md -> F10.
def _git_cfg(*args):
    try:
        p = subprocess.run(["git", "config"] + list(args), cwd=ROOT,
                            capture_output=True, text=True, timeout=5)
        return p.stdout.strip() if p.returncode == 0 else None
    except Exception:
        return None


def _norm_hp(v):
    if v is None:
        return None
    v = v.strip().replace("\\", "/")
    return (v[2:] if v.startswith("./") else v).rstrip("/")


local_hp = _git_cfg("--local", "--get", "core.hooksPath")
worktree_ext = _git_cfg("--get", "extensions.worktreeConfig")
worktree_hp = _git_cfg("--worktree", "--get", "core.hooksPath") if worktree_ext == "true" else None
effective_hp = _git_cfg("--get", "core.hooksPath")
eff_n, local_n, wt_n = _norm_hp(effective_hp), _norm_hp(local_hp), _norm_hp(worktree_hp)

if eff_n != ".githooks":
    out.append(
        f"HOOKS      *** WRONG *** core.hooksPath resolves to {effective_hp!r}, not .githooks\n"
        f"           (local={local_hp!r} worktree={worktree_hp!r}). .githooks/pre-commit\n"
        f"           (secret scanning, frontmatter status enum) is NOT running on this\n"
        f"           checkout. This exact symptom has recurred 3x via 3 mechanisms — wrong\n"
        f"           directory (2026-05-24), a shadow copy at .git/hooks (F8, 2026-08-04),\n"
        f"           a --worktree override silently shadowing --local (2026-08-05). Fix:\n"
        f"           git config --local core.hooksPath .githooks\n"
        f"           and if extensions.worktreeConfig is true, also check --worktree scope —\n"
        f"           it silently wins over --local. system/failures.md -> F10."
    )
elif wt_n is not None and local_n is not None and wt_n != local_n:
    out.append(
        f"HOOKS      *** LATENT SHADOW *** effective core.hooksPath is .githooks (ok for\n"
        f"           now), but --worktree ({worktree_hp!r}) and --local ({local_hp!r}) disagree.\n"
        f"           Worktree scope silently wins over local — this is the exact shape of\n"
        f"           F10's 2026-08-05 recurrence. If this worktree's override is ever cleared\n"
        f"           it reverts to the wrong local value with no warning. system/failures.md -> F10."
    )
else:
    out.append("HOOKS      ok — core.hooksPath resolves to .githooks")

print("=== EQ SESSION GATE (local clone — never the URL) ===")
print("\n".join(out))
print("=== read the above BEFORE the tier question ===")
