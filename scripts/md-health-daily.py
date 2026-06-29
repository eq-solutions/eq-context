#!/usr/bin/env python3
"""Daily MD health audit — whitespace-aware, emits JSON for dashboard."""
import hashlib, json, os, re, subprocess, sys
from datetime import datetime, timedelta, date
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
BINARY_EXT = {"zip","tar","gz","7z","docx","doc","xlsx","xls","pptx","ppt","pdf","png","jpg","jpeg","gif","bmp","webp","mov","mp4","mp3","wav"}

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

# ===== 3. binary files in eq-context =====
eqc = ROOT / "eq-context"
if eqc.is_dir():
    for dp, dns, fns in safe_walk(eqc):
        for fn in fns:
            ext = Path(fn).suffix.lstrip(".").lower()
            if ext in BINARY_EXT: add("ERROR","eq-context: binary file",str(dp/fn))

# ===== 6. duplicate / non-canonical sessions =====
sess = eqc / "sessions"
if sess.is_dir():
    s2p = {}
    for p in sess.glob("*.md"):
        try: h = hashlib.sha1(p.read_bytes()).hexdigest()
        except: continue
        if h in s2p: add("ERROR","duplicate session content",str(s2p[h])+" <-> "+str(p))
        else: s2p[h] = p
    # Allow YYYY-MM-DD[-slug].md session logs and the generated INDEX.md
    # (scripts/generate_session_index.py) — mirrors .github/workflows/md-health.yml rule 17.4.
    can = re.compile(r"^(\d{4}-\d{2}-\d{2}(-[a-z0-9-]+)?|INDEX)\.md$")
    for p in sess.glob("*.md"):
        if not can.match(p.name): add("ERROR","non-canonical session filename",str(p))

# ===== 6b. freshness =====
FM_RE = re.compile(r"^---\s*$")
KV_RE = re.compile(r"^([A-Za-z_][\w\-]*)\s*:\s*(.*?)\s*$")
DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
def pfm(text):
    ls = text.splitlines()
    if not ls or not FM_RE.match(ls[0].lstrip("﻿")): return {}
    fm = {}
    for ln in ls[1:]:
        if FM_RE.match(ln): return fm
        m = KV_RE.match(ln)
        if m: fm[m.group(1).lower()] = m.group(2).strip().strip('"').strip("'")
    return {}
def pid(s):
    if not s: return None
    m = DATE_RE.match(s.strip())
    if not m: return None
    try: return date(int(m.group(1)),int(m.group(2)),int(m.group(3)))
    except ValueError: return None

STALE, LCAP, SCAP = 30, 10, 8
td = _today_aest()
fr = ROOT / "eq-context"
if fr.is_dir():
    sh, ph, dh, bl = [], [], [], []
    # Map of repo-relative posix path -> YYYY-MM-DD of last commit touching the file.
    # Used instead of mtime for the last_updated-lag check: mtime advances on every
    # checkout/merge/pull, which is noise; git-log date reflects real edits.
    file_commit_dates = {}
    log_out, _ = run(["git","log","--format=COMMIT %ad","--date=short","--name-only"], cwd=fr)
    current_date = None
    for ln in log_out.splitlines():
        if ln.startswith("COMMIT "):
            current_date = ln[7:].strip()
        elif ln.strip() and current_date:
            if ln not in file_commit_dates:
                file_commit_dates[ln] = current_date
    for dp, dns, fns in safe_walk(fr):
        rr = dp.relative_to(fr)
        if any(part in ("drafts","_archive",".github",".githooks","md-health-reports") for part in rr.parts): continue
        if any(part.startswith("_archive-") or part.startswith("_cleanup-") for part in rr.parts): continue
        for fn in fns:
            if not fn.lower().endswith(".md"): continue
            p = dp / fn
            try: text = p.read_text(encoding="utf-8", errors="replace")
            except (OSError, PermissionError): continue
            fm = pfm(text); rel = p.relative_to(ROOT)
            if fm.get("status","").lower() == "live":
                lu = pid(fm.get("last_updated",""))
                if lu is not None:
                    age = (td - lu).days
                    if age > STALE: sh.append((age, str(rel)))
                else: sh.append((9999, str(rel)+" (no last_updated)"))
            nr = pid(fm.get("next_review",""))
            if nr is not None and nr < td: ph.append(((td-nr).days, str(rel)))
            lu = pid(fm.get("last_updated",""))
            if lu is not None:
                rel_to_fr = str(p.relative_to(fr)).replace("\\", "/")
                gd_str = file_commit_dates.get(rel_to_fr)
                if gd_str:
                    gd = pid(gd_str)
                    if gd is not None:
                        dr = (gd - lu).days
                        if dr > 7: dh.append((dr, str(rel)))
            for m in LINK_RE.finditer(text):
                tgt = m.group(1).split("#",1)[0].strip()
                if not tgt or tgt.startswith(("http://","https://","mailto:","//")): continue
                if not tgt.lower().endswith(".md"): continue
                res = (p.parent / tgt).resolve()
                try: inside = res.is_relative_to(fr)
                except AttributeError: inside = str(res).startswith(str(fr.resolve()))
                if inside and not res.exists():
                    bl.append(str(p.relative_to(ROOT))+" -> "+tgt)
                    if len(bl) >= LCAP: break
            if len(bl) >= LCAP: break
        if len(bl) >= LCAP: break
    sh.sort(reverse=True); ph.sort(reverse=True); dh.sort(reverse=True)
    for a, p in sh[:SCAP]:
        if a == 9999: add("INFO","freshness: status=live no last_updated", p)
        else: add("INFO","freshness: stale (>30d)", str(a)+"d - "+p)
    for d, p in ph[:SCAP]: add("WARN","freshness: next_review past due", str(d)+"d overdue - "+p)
    for d, p in dh[:SCAP]: add("INFO","freshness: last_updated lags mtime", str(d)+"d behind - "+p)
    for b in bl[:LCAP]: add("WARN","freshness: broken internal link", b)

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
