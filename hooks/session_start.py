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

print("=== EQ SESSION GATE (local clone — never the URL) ===")
print("\n".join(out))
print("=== read the above BEFORE the tier question ===")
