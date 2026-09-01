#!/usr/bin/env python3
"""
Refresh suite-state.md from live systems.
Run nightly via GitHub Action. Zero LLM inference — deterministic only.

Decision extraction uses ARCH: convention: any PR body line starting with
"ARCH:" is an architectural decision and gets appended automatically.
"""

import os, re, sys, requests
from datetime import datetime, timezone, timedelta

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
GH_TOKEN     = os.environ["GH_TOKEN"]
NETLIFY_TOKEN = os.environ.get("NETLIFY_TOKEN", "")
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

REPOS = ["eq-service", "eq-shell", "eq-field", "eq-cards", "eq-solves-intake"]

NETLIFY_SITES = {
    # Keys are matched as a substring of (Netlify site `name` + `custom_domain`)
    # in netlify_site_info() below. Both eq-service and eq-field entries used to
    # carry their dead pre-rename netlify.app URLs, which are NOT substrings of
    # the live name/domain and would have silently matched nothing — masked
    # until now only because NETLIFY_TOKEN isn't set in CI (see suite-state.md
    # "Deploys" section). Corrected to the live custom domains 2026-08-04,
    # confirmed via the Netlify API: eq-service -> service.eq.solutions,
    # eq-field -> field.eq.solutions.
    "service.eq.solutions": "eq-service",
    "core.eq.solutions":    "eq-shell",
    "field.eq.solutions":   "eq-field",
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

def pulse_flip_marker(prev, cur):
    """'' or '⚠ FLIPPED' for one signal's prev/current value.

    None means "no prior row" (first-ever run, or the row didn't exist yet) --
    that must never itself read as a flip, only a genuine zero<->nonzero
    crossing does. Pure function, no I/O -- see test_pulse_flip_marker.py.
    """
    if prev is None or cur is None:
        return ""
    return "⚠ FLIPPED" if (prev == 0) != (cur == 0) else ""


def render_pulse_rows(pulse_rows_spec, prev_pulse, pulse):
    """[(key, label, value, flip_marker), ...] for every signal in
    pulse_rows_spec, using pulse_flip_marker() for each. Pure function."""
    return [
        (key, label, pulse[key], pulse_flip_marker(prev_pulse.get(key), pulse.get(key)))
        for key, label in pulse_rows_spec
    ]


def fetch_pulse_signal(table, window_days, exclude_system_who=False):
    """Row count in `table` (public schema only -- service.*/app_data.* aren't
    PostgREST-exposed, see fetch_counts()'s docstring) created in the last
    `window_days`. Used for F4's product-pulse signals: public-schema tables
    only, direct REST, no RPC needed."""
    since = (datetime.now(timezone.utc) - timedelta(days=window_days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    params = {"select": "count()", "created_at": f"gte.{since}"}
    if exclude_system_who:
        params["who"] = "neq.system"
    resp = requests.get(
        f"{SUPABASE_URL}/rest/v1/{table}",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Accept": "application/vnd.pgrst.object+json",
        },
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["count"]


def fetch_maintenance_checks_pulse():
    """{'created_7d': N, 'completed_7d': N} via the maintenance_checks_pulse()
    RPC (ehow, applied 2026-09-01, Royce's go per this repo's non-negotiables
    on schema changes). service.maintenance_checks isn't PostgREST-exposed
    (see fetch_counts()'s docstring), so this needs a dedicated RPC rather
    than fetch_pulse_signal()'s direct-table REST call -- same reason
    field_canonical_health() exists for the Field Data Plane section."""
    resp = requests.post(
        f"{SUPABASE_URL}/rest/v1/rpc/maintenance_checks_pulse",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
        },
        json={},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def render_field_block(fc, today):
    """Markdown for the Field Data Plane section from a field_canonical_health()
    payload. Every line flush-left -- 4+ leading spaces reads as an indented code
    block in Markdown, which silently broke this exact table before (see
    splice_field_block()). Pure function, no I/O -- see test_field_block.py."""
    def _field_status(n, is_operational=False):
        if n is None:
            return "✗ missing"
        if n == 0:
            return "⚠ empty" if is_operational else "⚠ no data yet"
        return f"✓ {n:,}"

    # fc.get(key, 0) only defaults when the key is ABSENT -- an RPC response
    # that includes the key with an explicit None still passes None through,
    # which then throws formatting it as `:,}`. _n() treats both cases as 0
    # for the count column; _field_status() still sees the raw value so a
    # real None still renders "✗ missing" rather than a silently-wrong "0".
    def _n(key):
        return fc.get(key) or 0

    return f"""## Field Data Plane — SKS tenant (as of {today})
| Layer | View / Table | Rows | Status |
|-------|-------------|------|--------|
| Directory | app_data.field_people | {_n('people'):,} | {_field_status(fc.get('people'))} |
| Directory | app_data.field_sites | {_n('sites'):,} | {_field_status(fc.get('sites'))} |
| Directory | app_data.field_managers | {_n('managers'):,} | {_field_status(fc.get('managers'))} |
| Operational | app_data.field_schedule | {_n('schedule'):,} | {_field_status(fc.get('schedule'), True)} |
| Operational | app_data.field_timesheets | {_n('timesheets'):,} | {_field_status(fc.get('timesheets'), True)} |
| Safety | public.prestarts | {_n('prestarts'):,} | {_field_status(fc.get('prestarts'))} |
| Safety | public.toolbox_talks | {_n('toolbox_talks'):,} | {_field_status(fc.get('toolbox_talks'))} |
| Safety | public.site_audits | {_n('site_audits'):,} | {_field_status(fc.get('site_audits'))} |
_Auto-refreshed nightly. ✓ = has data · ⚠ = empty (no data yet) · ✗ = table missing_"""


_LEGACY_FIELD_TABLE_RE = (
    r"\| Layer \| View / Table \| Rows \| Status \|.*?"
    r"_Auto-refreshed nightly\. ✓ = has data · ⚠ = empty \(no data yet\) · ✗ = table missing_"
)


def splice_field_block(content, field_block):
    """Insert/refresh field_block in `content` at a self-healing anchor.

    Found 2026-09-01: a 2026-08-15 fix stripped this table's own heading, and
    every nightly run since 2026-08-16 silently no-op'd -- the old regex needed
    literal "## Field Data Plane" text that no longer existed anywhere in the
    file, so re.sub matched nothing, returned content unchanged, and raised
    nothing -- no exception, no log line, nothing to notice. Three cases so this
    can't recur silently: steady state (heading already present, refresh in
    place), a one-time repair of exactly that live shape (heading-less table
    sitting under System Health), and a cold start with neither present. Pure
    function, no I/O -- see test_field_block.py.
    """
    if "## Field Data Plane" in content:
        return re.sub(
            r"## Field Data Plane.*?(?=\n---|\n## Product Pulse|\n## Architecture)",
            field_block,
            content,
            flags=re.DOTALL,
        )
    if re.search(_LEGACY_FIELD_TABLE_RE, content, flags=re.DOTALL):
        return re.sub(_LEGACY_FIELD_TABLE_RE, field_block, content, count=1, flags=re.DOTALL)
    return content.replace(
        "\n## Architecture: What Owns What",
        f"\n{field_block}\n\n---\n\n## Architecture: What Owns What",
    )


def gh_get(path):
    resp = requests.get(
        f"https://api.github.com/{path}",
        headers={"Authorization": f"Bearer {GH_TOKEN}",
                 "Accept": "application/vnd.github.v3+json"},
        timeout=15,
    )
    if not resp.ok:
        # A 13-day silent gap (2026-07-21 through 2026-08-03) taught this: a bad
        # GH_TOKEN made every call here fail, and the caller-side "unknown"/"?"
        # fallbacks swallowed it completely — no error anywhere, in the log or
        # the committed file. Loud stderr means it shows up in the Action's run
        # log instead of requiring a git-blame archaeology dig to notice.
        print(f"  WARNING: GitHub API {resp.status_code} on {path} — {resp.text[:200]}", file=sys.stderr)
        return []
    return resp.json()

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

if __name__ == "__main__":
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

    # Previous Product Pulse values, parsed before this run's content replaces them --
    # needed for zero<->nonzero flip detection (F4: "transitions, not thresholds").
    # None (not 0) means "no prior row" -- e.g. this section's first-ever run --
    # which must never itself read as a flip.
    PULSE_ROWS = [
        ("checks_created_7d", "Maintenance checks created"),
        ("checks_completed_7d", "Maintenance checks completed"),
        ("prestarts_7d", "Prestarts created"),
        ("toolbox_talks_7d", "Toolbox talks created"),
        ("site_audits_7d", "Site audits created"),
        ("nonsystem_writes_7d", "Non-system writes (`audit_log`)"),
    ]
    prev_pulse = {}
    for key, label in PULSE_ROWS:
        m = re.search(rf"\| {re.escape(label)} \| (\d+) \|", content)
        prev_pulse[key] = int(m.group(1)) if m else None

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

    # 7f-ii. ARCH: decisions — EVICT the tail.
    #
    # This section was append-only with no eviction and had reached 67 bullets /
    # 21 KB — 79% of suite-state.md, a file auto-loaded into EVERY session in
    # C:\Projects regardless of tier via the @eq-context/suite-state.md directive.
    # It could only ever grow, and its entries near-verbatim duplicate the
    # per-product changelogs, which are the actual home for this detail.
    #
    # Newest-first is already the insertion order (new decisions are spliced
    # directly under the heading), so keeping the head keeps the recent ones.
    KEEP_DECISIONS = 30

    _dec = re.search(r"(## Key Decisions[^\n]*\n)(.*?)(\n---|\Z)", content, flags=re.DOTALL)
    if _dec:
        head, body, tail = _dec.group(1), _dec.group(2), _dec.group(3)
        # A "bullet" here is a top-level "- " line plus any continuation lines under
        # it; entries in this section are long and often wrap.
        bullets, current = [], []
        for line in body.split("\n"):
            if line.startswith("- "):
                if current:
                    bullets.append("\n".join(current))
                current = [line]
            elif current:
                current.append(line)
        if current:
            bullets.append("\n".join(current))

        if len(bullets) > KEEP_DECISIONS:
            dropped = len(bullets) - KEEP_DECISIONS
            kept = "\n".join(bullets[:KEEP_DECISIONS]).rstrip()
            note = (
                f"\n\n_Older decisions are evicted here, not deleted: the full record lives in "
                f"`eq/changelog/*.md` and `ops/decisions.md`, which is where this detail is "
                f"authored in the first place. Kept: {KEEP_DECISIONS} most recent. "
                f"Evicted this run: {dropped}._\n"
            )
            content = content.replace(head + body + tail, head + kept + note + tail, 1)
            print(f"  Evicted {dropped} decisions past the {KEEP_DECISIONS} most recent")

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
        content = splice_field_block(content, render_field_block(fc, TODAY))
    except Exception as e:
        # Found 2026-08-15: this bare except had been silently swallowing a real
        # failure -- field_canonical_health() threw on every nightly run after a
        # column rename (org_id -> tenant_id on 4 of its 8 tables), and because
        # this except left `content` untouched, the Field Data Plane table stayed
        # frozen at a stale count (field_people showed 66 against a live 83) while
        # the rest of the file, and the file's own last_updated stamp, kept
        # refreshing normally every night. A reader had no way to tell one section
        # was dead -- the file looked current. `::error::` makes this fail loud in
        # the workflow run summary instead of requiring someone to notice a wrong
        # number by hand; the WARNING text is kept for local/manual runs where
        # nothing parses GitHub annotations.
        print(f"::error::field_canonical_health() failed -- Field Data Plane table in suite-state.md was NOT refreshed this run: {e}")
        print(f"  WARNING: field canonical health check failed: {e}", file=sys.stderr)

    # 7h. Product Pulse -- F4 guard: "nothing watches the product," + a real over-read
    # lesson from the same incident (system/failures.md F4) -- the first alarm this
    # gap ever produced was itself wrong, because it read a raw zero as "broken"
    # instead of "young and forward-scheduled." So this section reports transitions
    # (zero<->nonzero), not threshold alarms, and every row is script-computed only
    # -- never hand-editable -- per the one promotion-guard rule kept from the
    # dropped claims-ledger design (ops/pending.md, 2026-07-12): an agent may not
    # mark its own claim verified. md-health.yml's pulse-promotion-guard check
    # enforces that on every PR; direct pushes here are always this same bot.
    #
    # One signal from the original plan (system/substrate-plan-v2.md P3) is
    # deliberately NOT computed: "active users, 7d" needs
    # service.profiles.last_login_at, which is 0-of-5 populated (verified live
    # 2026-09-01, unchanged since the 2026-07-12 design doc already flagged it
    # "unmeasurable"). Reporting a signal with zero real data behind it would
    # be exactly the kind of over-read this guard exists to prevent -- so it's
    # reported as blocked, not as a false 0.
    #
    # "Maintenance checks created/completed" WAS blocked the same way (needed
    # a windowed RPC against service.maintenance_checks, which isn't
    # PostgREST-exposed -- see fetch_counts()'s docstring) until Royce
    # approved the schema change 2026-09-01; see maintenance_checks_pulse()
    # (ehow migration `maintenance_checks_pulse_rpc`, EXECUTE granted to
    # service_role/postgres only, matching suite_state_counts()'s own grants).
    print("Computing product pulse signals (7d)...")
    try:
        checks_pulse = fetch_maintenance_checks_pulse()
        pulse = {
            "checks_created_7d": checks_pulse["created_7d"],
            "checks_completed_7d": checks_pulse["completed_7d"],
            "prestarts_7d": fetch_pulse_signal("prestarts", 7),
            "toolbox_talks_7d": fetch_pulse_signal("toolbox_talks", 7),
            "site_audits_7d": fetch_pulse_signal("site_audits", 7),
            "nonsystem_writes_7d": fetch_pulse_signal("audit_log", 7, exclude_system_who=True),
        }
        print(f"  pulse: {pulse}")

        rendered = render_pulse_rows(PULSE_ROWS, prev_pulse, pulse)
        any_flip = any(flip for _, _, _, flip in rendered)

        pulse_rows = "\n".join(
            f"| {label} | {value} | {flip} |" for _, label, value, flip in rendered
        )
        pulse_block = f"""## Product Pulse (as of {TODAY})
_7-day window. Transition-detection, not thresholds — flags a zero↔nonzero
crossing since the last run, not a raw count. Machine-generated only; see
`system/failures.md` F4._

| Signal | Value (7d) | Flip? |
|--------|-----------:|-------|
{pulse_rows}
| Active users | blocked | `service.profiles.last_login_at` never populated by Shell SSO (0-of-5, verified {TODAY}) — see `ops/pending.md` |

{"⚠️ **At least one signal flipped zero↔nonzero since the last run — see `digest.md`.**" if any_flip else "_No flips this run._"}"""

        if "## Product Pulse" in content:
            content = re.sub(
                r"## Product Pulse.*?(?=\n---|\n## Architecture)",
                pulse_block,
                content,
                flags=re.DOTALL,
            )
        else:
            content = content.replace(
                "\n## Architecture: What Owns What",
                f"\n{pulse_block}\n---\n\n## Architecture: What Owns What",
            )
    except Exception as e:
        print(f"::error::product pulse signal fetch failed -- suite-state.md's Product Pulse section was NOT refreshed this run: {e}", file=sys.stderr)

    # ── 8. Write back ─────────────────────────────────────────────────────────────

    with open("suite-state.md", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nDone — suite-state.md updated for {TODAY}")
