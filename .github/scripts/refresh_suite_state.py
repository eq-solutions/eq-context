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

def fetch_counts():
    """All suite-state counts via one public RPC (counts only, no rows).

    Replaces the old per-table PostgREST HEAD counts. Those hit service.*/app_data.*
    via Accept-Profile, but PostgREST only serves *exposed* schemas (public) — so every
    request 406'd, fell through to "*/0", and silently reported 0 while ehow held
    thousands of rows. raise_for_status() below makes any future failure loud, not zero.
    """
    resp = requests.post(
        f"{SUPABASE_URL}/rest/v1/rpc/suite_state_counts",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
        },
        json={},
        timeout=15,
    )
    resp.raise_for_status()   # 4xx/5xx now FAILS the job — no more silent "*/0" -> 0
    return resp.json()

def gh_get(path):
    resp = requests.get(
        f"https://api.github.com/{path}",
        headers={"Authorization": f"Bearer {GH_TOKEN}",
                 "Accept": "application/vnd.github.v3+json"},
        timeout=15,
    )
    return resp.json() if resp.ok else []

def main_ci_status(repo):
    """Latest CI run conclusion on main branch."""
    data = gh_get(f"repos/eq-solutions/{repo}/actions/runs?branch=main&per_page=3&event=push")
    if not isinstance(data, dict):
        return "unknown"
    runs = data.get("workflow_runs", [])
    # Find the most recent completed run (skip in_progress)
    for r in runs:
        conclusion = r.get("conclusion")
        if conclusion:
            return conclusion  # "success", "failure", "cancelled", etc.
    return runs[0].get("status", "unknown") if runs else "unknown"

def migration_count(repo="eq-solutions/eq-service"):
    """Count .sql migration files in supabase/migrations/ via GitHub contents API."""
    contents = gh_get(f"repos/{repo}/contents/supabase/migrations")
    if not isinstance(contents, list):
        return "?"
    sqls = [f for f in contents if isinstance(f, dict) and f.get("name", "").endswith(".sql")]
    if not sqls:
        return 0
    latest = sorted(sqls, key=lambda f: f["name"])[-1]["name"]
    return f"{len(sqls)} (latest: {latest.split('_')[0]})"

def netlify_site_info(site_name):
    """Return (state, published_at) for a Netlify site's last deploy."""
    if not NETLIFY_TOKEN:
        return "unknown", None
    try:
        sites = requests.get(
            "https://api.netlify.com/api/v1/sites",
            headers={"Authorization": f"Bearer {NETLIFY_TOKEN}"},
            params={"filter": "all"},
            timeout=10,
        ).json()
        if not isinstance(sites, list):
            return "unknown", None
        match = next(
            (s for s in sites if site_name in (s.get("name", "") + s.get("custom_domain", ""))),
            None,
        )
        if not match:
            return "unknown", None
        deploys = requests.get(
            f"https://api.netlify.com/api/v1/sites/{match['id']}/deploys",
            headers={"Authorization": f"Bearer {NETLIFY_TOKEN}"},
            params={"per_page": 1},
            timeout=10,
        ).json()
        if not isinstance(deploys, list) or not deploys:
            return "unknown", None
        d = deploys[0]
        published = d.get("published_at") or d.get("created_at", "")
        published_short = published[:10] if published else "?"
        return d.get("state", "unknown"), published_short
    except Exception:
        return "unknown", None

# ── 1. live counts ────────────────────────────────────────────────────────────

print("Querying Supabase...")
counts = fetch_counts()
print(f"  counts: {counts}")

# Tripwire: refuse to overwrite real numbers with an all-zero collapse.
with open("suite-state.md", encoding="utf-8") as _f:
    _prev = re.search(r"\| Maintenance checks \| ([\d,]+)", _f.read())
_prev_nonzero = bool(_prev) and _prev.group(1).replace(",", "") != "0"
if all(int(counts.get(k, 0)) == 0 for k in ("sites","customers","assets","users","checks","defects")):
    if _prev_nonzero:
        print("ERROR: all counts zero but file had data — refusing to overwrite.", file=sys.stderr)
        sys.exit(1)
    print("WARNING: all counts are zero.", file=sys.stderr)

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

# ── 4. CI health on main ──────────────────────────────────────────────────────

print("Checking CI health on main branches...")
ci_health = {}
for repo in REPOS:
    ci_health[repo] = main_ci_status(repo)
    print(f"  {repo}: {ci_health[repo]}")

# ── 5. Migration count ────────────────────────────────────────────────────────

print("Counting migrations...")
migrations = migration_count()
print(f"  eq-service migrations: {migrations}")

# ── 6. Netlify deploy status ──────────────────────────────────────────────────

print("Checking Netlify deploys...")
deploy_info = {}
for site_key, label in NETLIFY_SITES.items():
    state, published = netlify_site_info(site_key)
    deploy_info[label] = (state, published)
    print(f"  {label}: {state} ({published})")

# ── 7. Read and patch suite-state.md ─────────────────────────────────────────

with open("suite-state.md", "r", encoding="utf-8") as f:
    content = f.read()

prev_checks = 0
m = re.search(r"\| Maintenance checks \| (\d+)", content)
if m:
    prev_checks = int(m.group(1))

# 7a. Timestamp
content = re.sub(
    r"_Last verified:.*?\n",
    f"_Last verified: {TODAY} (nightly cron)_\n",
    content,
)

# 7a-2. Frontmatter last_updated — was never bumped, only the body line above was,
# so the YAML header silently drifted behind the file's own "Last verified" stamp.
content = re.sub(
    r"(?m)^last_updated: \d{4}-\d{2}-\d{2}$",
    f"last_updated: {TODAY}",
    content,
    count=1,
)

# 7b. Counts table
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

# 7c. First-data flag
if prev_checks == 0 and isinstance(counts["checks"], int) and counts["checks"] > 0:
    content = content.replace(
        "**SKS tenant ID",
        "⚠️ **FIRST OPERATIONAL DATA CREATED** — migration rebuild now matters.\n\n**SKS tenant ID",
    )

# 7d. Open PRs section
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

# 7e. System health section — CI + deploys + migrations
ci_icon = {"success": "✓", "failure": "✗", "cancelled": "⚠", "skipped": "–"}
ci_rows = "\n".join(
    f"| {repo} | {ci_icon.get(status, '?')} {status} |"
    for repo, status in ci_health.items()
)

if NETLIFY_TOKEN:
    deploy_rows = "\n".join(
        f"| {label} | {state} | {published or '?'} |"
        for label, (state, published) in deploy_info.items()
    )
    deploy_block = f"""
| Site | State | Last deploy |
|------|-------|-------------|
{deploy_rows}"""
else:
    deploy_block = "_NETLIFY_TOKEN not set — deploy status unavailable_"

health_block = f"""## System Health (as of {TODAY})

**CI on main:**

| Repo | Status |
|------|--------|
{ci_rows}

**Deploys:**
{deploy_block}

**Migrations:** eq-service has {migrations} applied"""

# Replace existing health section or insert before Architecture
if "## System Health" in content:
    content = re.sub(
        r"## System Health.*?(?=\n---|\n## Architecture)",
        health_block + "\n",
        content,
        flags=re.DOTALL,
    )
else:
    content = content.replace(
        "\n## Architecture: What Owns What",
        f"\n{health_block}\n\n---\n\n## Architecture: What Owns What",
    )

# 7f. ARCH: decisions — append new ones to Key Decisions section
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

# 7g. Field canonical data plane — SKS tenant counts
print("Querying Field canonical data plane (ehow)...")
try:
    field_resp = requests.post(
        f"{SUPABASE_URL}/rest/v1/rpc/field_canonical_health",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
        },
        json={},
        timeout=15,
    )
    field_resp.raise_for_status()
    fc = field_resp.json()
    print(f"  field counts: {fc}")

    def _field_status(n, is_operational=False):
        if n is None:
            return "✗ missing"
        if n == 0:
            return "⚠ empty" if is_operational else "⚠ no data yet"
        return f"✓ {n:,}"

    field_table = f"""| Layer | View / Table | Rows | Status |
|-------|-------------|------|--------|
| Directory | app_data.field_people | {fc.get('people',0):,} | {_field_status(fc.get('people'))} |
| Directory | app_data.field_sites | {fc.get('sites',0):,} | {_field_status(fc.get('sites'))} |
| Directory | app_data.field_managers | {fc.get('managers',0):,} | {_field_status(fc.get('managers'))} |
| Operational | app_data.field_schedule | {fc.get('schedule',0):,} | {_field_status(fc.get('schedule'), True)} |
| Operational | app_data.field_timesheets | {fc.get('timesheets',0):,} | {_field_status(fc.get('timesheets'), True)} |
| Safety | public.prestarts | {fc.get('prestarts',0):,} | {_field_status(fc.get('prestarts'))} |
| Safety | public.toolbox_talks | {fc.get('toolbox_talks',0):,} | {_field_status(fc.get('toolbox_talks'))} |
| Safety | public.site_audits | {fc.get('site_audits',0):,} | {_field_status(fc.get('site_audits'))} |"""

    content = re.sub(
        r"## Field Data Plane.*?(?=\n_Auto-refreshed nightly\..*?\n\n---)",
        field_table,
        content,
        flags=re.DOTALL,
    )
    content = re.sub(
        r"(## Field Data Plane — SKS tenant \(as of )\d{4}-\d{2}-\d{2}(\))",
        rf"\g<1>{TODAY}\g<2>",
        content,
    )
except Exception as e:
    print(f"  WARNING: field canonical health check failed: {e}", file=sys.stderr)

# ── 8. Write back ─────────────────────────────────────────────────────────────

with open("suite-state.md", "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nDone — suite-state.md updated for {TODAY}")
