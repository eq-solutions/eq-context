#!/usr/bin/env python3
"""Beelink-local cross-repo git audit. NOT CI -- cannot be, by construction.

Walks every git repo directly under C:\\Projects (eq-shell, eq-field,
eq-context, and every sibling) for uncommitted work, unpushed/unpulled
commits, stale lock files, cleanup-patch leftovers, and orphaned worktrees.
A GitHub Actions runner for eq-context checks out ONLY eq-context -- it has
no access to sibling repos on disk, so this half of the script can never
move into CI. It stays exactly where it is, run by hand or by a scheduled
task on the workstation itself.

What this file used to also do, and where that went (2026-08-15). Until
today this file was the ONLY place three checks lived, and NOTHING ran it --
no workflow, no cron, no hook. `git log --diff-filter=A` on this repo's own
history shows it was last touched 2026-07-19 and has been dead weight ever
since. Three of its checks WERE portable (eq-context-only, no sibling-repo
access needed) and have moved to gated, tested scripts:

  binary files in eq-context      already duplicated by md-health.yml's own
                                   inline "17.2 — binary files" step; this
                                   file's copy was just a second, weaker
                                   version of a check that already ran.
  status:live + last_updated>30d  superseded by scripts/review_clock.py,
                                   which does the same job properly --
                                   kind-aware (a record can't go stale, a
                                   generated file gets the tight cron-liveness
                                   clock a flat rule can't express), gated,
                                   ratcheted. This file's version had no
                                   kind-awareness at all: on 2026-08-15 it
                                   would have flagged 82 files, of which 59
                                   were session logs and changelogs -- records,
                                   not stale claims -- which is exactly the
                                   false-signal problem review_clock.py exists
                                   to fix.
  next_review: past due           the frontmatter key this checked for has
                                   ZERO uses across all 328 tracked .md files
                                   (checked 2026-08-15) -- a dead code path
                                   that had never once fired on real data.
                                   review_clock.py's derived cadence replaces
                                   the INTENT (a review clock) without a
                                   hand-typed date, which is the same F3
                                   shape ("a deadline nobody owns") this
                                   check's own design invited.
  broken internal links           superseded by scripts/link_check.py --
                                   exhaustive (this file capped output at 10
                                   and stopped scanning once hit), gated,
                                   tested. This file found 20 real broken
                                   links and reported none of them anywhere
                                   anyone would see, because nothing ran it.
  duplicate session content       genuinely unique, genuinely portable, no
                                   equivalent existed -- extracted whole to
                                   scripts/duplicate_sessions.py, now gated.
  non-canonical session filename  was ALREADY independently covered by
                                   md-health.yml's own rule 17.4 this whole
                                   time; this file's copy was fully redundant
                                   from the start, not just newly superseded.

Emits a Markdown + JSON report to md-health-reports/ either way -- kept for
whoever runs this by hand, not read by anything automated (no dashboard or
workflow consumes the JSON; checked 2026-08-15, see system/machinery.md).
"""
import json, os, re, subprocess, sys
from datetime import datetime, timedelta
from pathlib import Path
try:
    from zoneinfo import ZoneInfo
    AEST = ZoneInfo("Australia/Sydney")
except Exception:
    AEST = None

WIN_ROOT = "C:\\Projects"

def _safe_is_dir(p):
    try: return Path(p).is_dir()
    except (PermissionError, OSError): return False

ROOT = None
if _safe_is_dir(WIN_ROOT):
    ROOT = Path(WIN_ROOT)
else:
    sp = Path("/sessions")
    if _safe_is_dir(sp):
        try:
            cands = [s/"mnt"/"Projects" for s in sp.iterdir() if _safe_is_dir(s/"mnt"/"Projects")]
            if cands:
                cands.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                ROOT = cands[0]
        except (PermissionError, OSError): pass

if ROOT is None:
    print("FATAL: could not find C:\\Projects", file=sys.stderr); sys.exit(2)

REPORTS = ROOT / "md-health-reports"; REPORTS.mkdir(exist_ok=True)

def _today_aest():
    if AEST is not None: return datetime.now(AEST).date()
    return date.today()

TODAY = _today_aest().strftime("%Y-%m-%d")
REPORT_PATH = REPORTS / (TODAY + ".md")
LATEST_PATH = REPORTS / "latest.md"
JSON_PATH = REPORTS / (TODAY + ".json")
LATEST_JSON = REPORTS / "latest.json"

findings = []
repos = []
EXCLUDE_PARTS = {"node_modules", ".git", "dist", "build", ".next"}

def add(sev, cat, msg): findings.append((sev, cat, msg))

def run(cmd, cwd):
    try:
        o = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=15)
        return o.stdout.strip(), o.returncode
    except Exception as e:
        return "ERROR: "+str(e), 1

def safe_walk(root):
    for dp, dns, fns in os.walk(root, onerror=lambda e: None):
        dns[:] = [d for d in dns if d not in EXCLUDE_PARTS
                  and not (Path(dp).name == ".claude" and d == "worktrees")]
        yield Path(dp), dns, fns

# ===== 1. Git repo audit =====
for child in sorted(ROOT.iterdir()):
    if not child.is_dir(): continue
    gd = child / ".git"
    if not (gd.is_dir() or gd.is_file()): continue
    rn = child.name
    br_out, _ = run(["git","rev-parse","--abbrev-ref","HEAD"], cwd=child)
    branch = br_out or "?"
    ab_out, ab_rc = run(["git","rev-list","--left-right","--count",branch+"...@{u}"], cwd=child)
    ahead_behind = ab_out if ab_rc == 0 else "no upstream"
    if ab_rc == 0 and re.match(r"^\d+\s+\d+$", ab_out):
        ahead, behind = (int(x) for x in ab_out.split())
        if ahead > 0: add("WARN", rn+": unpushed", str(ahead)+" local commit(s) not pushed to origin/"+branch)
        if behind > 0: add("WARN", rn+": not pulled", str(behind)+" remote commit(s) not pulled from origin/"+branch)
    porc_out, _ = run(["git","status","--porcelain"], cwd=child)
    pl = [l for l in porc_out.splitlines() if l.strip()]
    real_lines, whitespace_only, untracked = [], 0, 0
    for ln in pl:
        code = ln[:2]
        m = re.match(r"^\s*[MADRCU?!]+\s+(.+)$", ln)
        if not m: real_lines.append(ln); continue
        rel = m.group(1).strip().strip('"')
        if code.strip() == "??": untracked += 1; real_lines.append(ln); continue
        _, rc1 = run(["git","diff","-w","--quiet","--",rel], cwd=child)
        if rc1 == 0:
            _, rc2 = run(["git","diff","-w","--quiet","--cached","--",rel], cwd=child)
            if rc2 == 0: whitespace_only += 1; continue
        real_lines.append(ln)
    uc = len(real_lines)
    if uc > 0:
        oa = None
        for ln in real_lines:
            m = re.match(r"^\s*[MADRCU?!]+\s+(.+)$", ln)
            if not m: continue
            rel = m.group(1).strip().strip('"')
            full = child / rel
            if full.is_file():
                age = datetime.now() - datetime.fromtimestamp(full.stat().st_mtime)
                if oa is None or age > oa: oa = age
        sev = "WARN" if (oa and oa.days > 3) else "INFO"
        msg = str(uc) + " entries uncommitted"
        if oa: msg += " (oldest: " + str(oa.days) + "d old)"
        add(sev, rn+": uncommitted", msg)
    if whitespace_only > 0:
        add("INFO", rn+": whitespace-only diffs",
            str(whitespace_only)+" file(s) — likely missing/incomplete .gitattributes")
    if (child/".git").is_dir():
        try:
            for lf in (child/".git").glob("*.lock"):
                age = datetime.now() - datetime.fromtimestamp(lf.stat().st_mtime)
                if age.total_seconds() > 300:
                    add("WARN", rn+": stale lock", str(lf)+" (age: "+str(int(age.total_seconds()/60))+"m)")
        except Exception: pass
    repos.append({"name": rn, "branch": branch, "uncommitted": uc,
                  "whitespace_only": whitespace_only, "untracked": untracked,
                  "ahead_behind": ahead_behind,
                  "has_gitattributes": (child/".gitattributes").is_file()})

# ===== 2-5 single walk =====
ver_re = re.compile(r"^CHANGELOG-v\d+\.\d+(\.\d+)?\.md$", re.IGNORECASE)
for dp, dns, fns in safe_walk(ROOT):
    for d in list(dns):
        if d.startswith("_cleanup-patch-"): add("WARN","cleanup-patch folder",str(dp/d))
        elif d.startswith("_cleanup-"): add("WARN","cleanup folder",str(dp/d))
        elif d.startswith("_archive-"): add("INFO","archive folder",str(dp/d))
    if dp.name == ".claude":
        wt = dp/"worktrees"
        if wt.is_dir():
            try:
                for c in wt.iterdir():
                    if c.is_dir(): add("WARN","claude worktree leftover",str(c))
            except OSError: pass
    for fn in fns:
        if ver_re.match(fn): add("WARN","per-version changelog",str(dp/fn))

# ===== 7. md count + delta =====
md_count = 0
for dp, dns, fns in safe_walk(ROOT):
    for fn in fns:
        if fn.lower().endswith(".md"): md_count += 1
md_delta = None
yp = REPORTS / ((_today_aest()-timedelta(days=1)).strftime("%Y-%m-%d")+".md")
if yp.is_file():
    try:
        for line in yp.read_text(encoding="utf-8").splitlines():
            if line.startswith("**MD count:**"):
                m = re.search(r"\d+", line)
                if m: md_delta = md_count - int(m.group(0))
                break
    except: pass

# ===== build report =====
ec = sum(1 for f in findings if f[0]=="ERROR")
wc_ = sum(1 for f in findings if f[0]=="WARN")
ic = sum(1 for f in findings if f[0]=="INFO")
status = "RED" if ec > 0 else ("AMBER" if wc_ > 0 else "GREEN")

lines = []
lines.append("---")
lines.append("title: MD Health Report - "+TODAY)
lines.append("owner: Royce Milmlow")
lines.append("last_updated: "+TODAY)
lines.append("scope: Daily audit of C:\\\\Projects MD files and git state")
lines.append("read_priority: reference"); lines.append("status: live")
lines.append("---"); lines.append("")
lines.append("# MD Health Report - "+TODAY); lines.append("")
lines.append("**Status:** "+status)
lines.append("**Errors:** "+str(ec)+"   |   **Warnings:** "+str(wc_)+"   |   **Info:** "+str(ic))
ds = ""
if md_delta is not None:
    sn = "+" if md_delta >= 0 else ""
    ds = " (delta vs yesterday: "+sn+str(md_delta)+")"
lines.append("**MD count:** "+str(md_count)+ds)
lines.append("**Repos audited:** "+str(len(repos))); lines.append("")
if not findings: lines.append("All clean.")
else:
    bc = {}
    for s, c, m in findings: bc.setdefault(c, []).append((s, m))
    for c in sorted(bc):
        lines.append("## "+c); lines.append("")
        for s, m in bc[c]: lines.append("- **"+s+"** - "+m)
        lines.append("")
lines.append("## Repo summary"); lines.append("")
lines.append("| Repo | Branch | Uncommitted | Whitespace | Ahead/Behind | .gitattributes |")
lines.append("|------|--------|-------------|------------|--------------|----------------|")
for r in repos:
    ws = r.get("whitespace_only", 0)
    ha = "yes" if r.get("has_gitattributes") else "MISSING"
    lines.append("| "+r["name"]+" | "+r["branch"]+" | "+str(r["uncommitted"])+" | "+str(ws)+" | "+str(r["ahead_behind"])+" | "+ha+" |")
lines.append(""); lines.append("_Generated by md-health-daily.py_")

content = "\n".join(lines)
REPORT_PATH.write_text(content, encoding="utf-8")
LATEST_PATH.write_text(content, encoding="utf-8")

state = {
    "generated_at": datetime.now().isoformat(timespec="seconds"),
    "date": TODAY, "status": status,
    "counts": {"error": ec, "warn": wc_, "info": ic, "md_total": md_count, "md_delta": md_delta},
    "repos": repos,
    "findings": [{"severity": s, "category": c, "message": m} for s, c, m in findings],
}
JSON_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")
LATEST_JSON.write_text(json.dumps(state, indent=2), encoding="utf-8")

print("Status:   "+status)
print("Errors:   "+str(ec))
print("Warnings: "+str(wc_))
print("Info:     "+str(ic))
print("Report:   "+str(REPORT_PATH))
print("JSON:     "+str(JSON_PATH))
if findings:
    print("\nFindings (top 10):")
    for s, c, m in findings[:10]: print("  ["+s+"] "+c+" - "+m)
sys.exit(0)
