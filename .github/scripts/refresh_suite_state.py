#!/usr/bin/env python3
"""
Refresh suite-state.md from live systems.
Run nightly via GitHub Action. Zero LLM inference — deterministic only.

Decision extraction uses ARCH: convention: any PR body line starting with
"ARCH:" is an architectural decision and gets appended automatically.
"""

import os, re, sys, requests
from datetime import datetime, timezone

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
GH_TOKEN     = os.environ["GH_TOKEN"]
NETLIFY_TOKEN = os.environ.get("NETLIFY_TOKEN", "")
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

REPOS = ["eq-service", "eq-shell", "eq-field", "eq-cards", "eq-solves-intake"]

NETLIFY_SITES = {
    "eq-solves-service.netlify.app": "eq-service",
    "core.eq.solutions":             "eq-shell",
    "eq-solves-field.netlify.app":   "eq-field",
}

# ── helpers ──────────────────────────────────────────────────────────────────

def pg_count(table, schema="service", q=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?select=count{('&' + q) if q else ''}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Prefer": "count=exact",
        "Accept-Profile": schema,
    }
    resp = requests.head(url, headers=headers, timeout=10)
    cr = resp.headers.get("content-range", "*/0")
    return int(cr.split("/")[-1]) if "/" in cr else 0

def gh_get(path):
    resp = requests.get(
        f"https://api.github.com/{path}",
        headers={"Authorization": f"Bearer {GH_TOKEN}",
                 "Accept": "application/vnd.github.v3+json"},
        timeout=15,
    )
    return resp.json() if resp.ok else []

def netlify_deploy_status(site_name):
    if not NETLIFY_TOKEN:
        return "unknown"
    sites = requests.get(
        "https://api.netlify.com/api/v1/sites",
        headers={"Authorization": f"Bearer {NETLIFY_TOKEN}"},
        params={"filter": "all"},
        timeout=10,
    ).json()
    if not isinstance(sites, list):
        return "unknown"
    match = next((s for s in sites if site_name in (s.get("name","") + s.get("custom_domain",""))), None)
    if not match:
        return "unknown"
    deploys = requests.get(
        f"https://api.netlify.com/api/v1/sites/{match['id']}/deploys",
        headers={"Authorization": f"Bearer {NETLIFY_TOKEN}"},
        params={"per_page": 1},
        timeout=10,
    ).json()
    if not isinstance(deploys, list) or not deploys:
        return "unknown"
    d = deploys[0]
    return d.get("state", "unknown")

# ── 1. live counts ────────────────────────────────────────────────────────────

print("Querying Supabase...")
counts = {}
try:
    counts = {
        "checks":    pg_count("maintenance_checks"),
        "acb":       pg_count("acb_tests"),
        "rcd":       pg_count("rcd_tests"),
        "defects":   pg_count("defects"),
        "sites":     pg_count("sites",     "app_data", "active=eq.true"),
        "customers": pg_count("customers", "app_data", "active=eq.true"),
        "assets":    pg_count("assets",    "app_data", "active=eq.true"),
        "users":     pg_count("tenant_members"),
    }
    print(f"  counts: {counts}")
except Exception as e:
    print(f"  Supabase error: {e}", file=sys.stderr)
    counts = {k: "(err)" for k in ["checks","acb","rcd","defects","sites","customers","assets","users"]}

# ── 2. open PRs ──────────────────────────────────────────────────────────────

print("Querying GitHub open PRs...")
open_prs: dict[str, list] = {}
for repo in REPOS:
    prs = gh_get(f"repos/eq-solutions/{repo}/pulls?state=open&per_page=20")
    if isinstance(prs, list) and prs:
        open_prs[repo] = [(p["number"], p["title"]) for p in prs]

# ── 3. ARCH: decisions from merged PRs ───────────────────────────────────────

print("Scanning merged PRs for ARCH: decisions...")
arch_decisions: list[tuple[int, str, str]] = []  # (pr_num, repo, decision_text)
for repo in REPOS:
    prs = gh_get(f"repos/eq-solutions/{repo}/pulls?state=closed&per_page=50&sort=updated&direction=desc")
    if not isinstance(prs, list):
        continue
    for p in prs:
        if not p.get("merged_at"):
            continue
        body = p.get("body") or ""
        for line in body.splitlines():
            line = line.strip()
            if line.upper().startswith("ARCH:"):
                text = line[5:].strip()
                arch_decisions.append((p["number"], p["merged_at"][:10], text))

# ── 4. Netlify deploy status ──────────────────────────────────────────────────

print("Checking Netlify deploys...")
deploy_status = {}
for site_key, label in NETLIFY_SITES.items():
    deploy_status[label] = netlify_deploy_status(site_key)

# ── 5. Read and patch suite-state.md ─────────────────────────────────────────

with open("suite-state.md", "r", encoding="utf-8") as f:
    content = f.read()

prev_checks = 0
m = re.search(r"\| Maintenance checks \| (\d+)", content)
if m:
    prev_checks = int(m.group(1))

# 5a. Timestamp
content = re.sub(
    r"_Last verified:.*?\n",
    f"_Last verified: {TODAY} (nightly cron)_\n",
    content,
)

# 5b. Counts table
def fmt(v):
    return f"{v:,}" if isinstance(v, int) else str(v)

counts_table = f"""| Entity | Count | Schema |
|--------|-------|--------|
| Sites | {fmt(counts['sites'])} | app_data.sites |
| Customers | {fmt(counts['customers'])} | app_data.customers |
| Assets | {fmt(counts['assets'])} | app_data.assets |
| Tenants | 1 (SKS Technologies) | service.tenants |
| Users | {fmt(counts['users'])} | service.tenant_members |
| Maintenance checks | {fmt(counts['checks'])} | service.maintenance_checks |
| Defects | {fmt(counts['defects'])} | service.defects |"""

content = re.sub(
    r"\| Entity \| Count \| Schema \|.*?(?=\n\n\*\*SKS tenant)",
    counts_table,
    content,
    flags=re.DOTALL,
)

# 5c. First-data flag
if prev_checks == 0 and isinstance(counts["checks"], int) and counts["checks"] > 0:
    content = content.replace(
        "**SKS tenant ID",
        "⚠️ **FIRST OPERATIONAL DATA CREATED** — migration rebuild now matters.\n\n**SKS tenant ID",
    )

# 5d. Open PRs section
pr_lines = [f"## Open PRs (as of {TODAY})\n"]
if open_prs:
    for repo, prs in sorted(open_prs.items()):
        pr_lines.append(f"**{repo}:**")
        for num, title in prs:
            pr_lines.append(f"- #{num} {title}")
        pr_lines.append("")
else:
    pr_lines.append("_No open PRs_\n")

pr_block = "\n".join(pr_lines)
content = re.sub(
    r"## Open PRs.*?(?=\n---)",
    pr_block,
    content,
    flags=re.DOTALL,
)

# 5e. Netlify deploy status — append to Crons section if status != "ready"
degraded = {k: v for k, v in deploy_status.items() if v not in ("ready", "unknown", "")}
if degraded:
    deploy_note = "⚠️ **Deploy issues:** " + ", ".join(f"{k}={v}" for k, v in degraded.items())
    content = content.replace("## Architecture: What Owns What", deploy_note + "\n\n## Architecture: What Owns What")

# 5f. ARCH: decisions — append new ones to Key Decisions section
existing_pr_nums = set(re.findall(r"PR #(\d+)", content))
new_decisions = []
for pr_num, date, text in arch_decisions:
    if str(pr_num) not in existing_pr_nums:
        new_decisions.append(f"- {text} (PR #{pr_num}, {date})")

if new_decisions:
    decisions_block = "\n".join(new_decisions)
    content = re.sub(
        r"(## Key Decisions.*?\n)",
        r"\1" + decisions_block + "\n",
        content,
        count=1,
        flags=re.DOTALL,
    )
    print(f"  Added {len(new_decisions)} new ARCH decisions")

# ── 6. Write back ─────────────────────────────────────────────────────────────

with open("suite-state.md", "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nDone — suite-state.md updated for {TODAY}")
