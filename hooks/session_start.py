#!/usr/bin/env python3
"""
SessionStart gate — RUNG 4 detection.

Replaces the 13-step §1 / §0.6 ritual with something that cannot be skipped and
costs no ceremony. Prints, unprompted, at every session start:

  1. FRESHNESS   — digest.md age. >2 days = the read path may be lying (failure F1).
  2. NEEDS YOU   — the digest's own alert section, which otherwise waits in a file
                   nobody opens (it sat unread for 12 days).
  3. GOALS       — whether TODAY.md has any. If UNSET, no assistant may defer work
                   by appeal to a deadline (failure F3 — the 1 August phantom).
  4. RATCHET     — failures whose guard is overdue for promotion (system/failures.md).

Reads the LOCAL CLONE, never a URL. The URL is what lied on 2026-07-11.
Fails open but loud: a silent guard is the bug we are fixing.
"""
import os, re, sys
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

# --- 2. NEEDS YOU -----------------------------------------------------------
nm = re.search(r"##\s*⚠?\s*Needs you[^\n]*\n(.*?)(?=\n##\s)", digest, re.S)
if nm:
    items = [l.strip() for l in nm.group(1).splitlines() if l.strip().startswith("-")]
    if items:
        out.append("NEEDS YOU  " + f"{len(items)} item(s):")
        for it in items[:5]:
            out.append("           " + it[:110])
    else:
        out.append("NEEDS YOU  clear")

# --- 3. GOALS (F3 — the 1 August phantom) -----------------------------------
today = read("system/TODAY.md")
if "status: UNSET" in today or "Goals: UNSET" in today or "claims: []" in today:
    out.append(
        "GOALS      *** UNSET *** TODAY.md has no owned goals.\n"
        "           You therefore have NO BASIS to defer, deprioritise, or justify work\n"
        "           by appeal to a deadline or quarterly outcome. Do not borrow one from\n"
        "           an old file. Do not invent one. Say plainly that goals are unset.\n"
        "           (On 2026-07-11 a phantom '1 August' deadline steered two weeks of\n"
        "           sessions. Nobody owned it. Every CI check passed green — failure F3.)"
    )
else:
    ta = age_days((re.search(r"last_updated:\s*(\S+)", today) or [None, ""])[1])
    if ta is not None and ta > 7:
        out.append(f"GOALS      set, but TODAY.md is {ta}d old — treat its numbers as leads, not facts.")
    else:
        out.append("GOALS      set")

# --- 4. RATCHET (promotions due) --------------------------------------------
fails = read("system/failures.md")
due = []
for blk in re.split(r"\n\s*-\s+id:\s*", fails)[1:]:
    fid = blk.split("\n", 1)[0].strip()
    rec = re.search(r"recurrences:\s*(\d+)", blk)
    rung = re.search(r"rung:\s*(\d+)", blk)
    title = re.search(r"title:\s*(.+)", blk)
    if rec and rung and int(rec.group(1)) >= 2 and int(rung.group(1)) < 4:
        due.append(f"{fid} (rung {rung.group(1)}, {rec.group(1)}x) — {title.group(1)[:70] if title else ''}")
if due:
    out.append("RATCHET    *** PROMOTION DUE *** a guard has failed twice and must climb:")
    for d in due:
        out.append("           " + d)
    out.append("           A lesson that failed twice IS the thing that failed. Promote it to a hook.")
else:
    out.append("RATCHET    no promotions due")

print("=== EQ SESSION GATE (local clone — never the URL) ===")
print("\n".join(out))
print("=== read the above BEFORE the tier question ===")
