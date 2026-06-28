#!/usr/bin/env python3
"""Generate digest.md — a push-style "what needs your attention" view of the EQ suite.

Companion to refresh_suite_state.py (the full snapshot). suite-state.md answers
"what is the state of everything"; digest.md answers "what, if anything, needs me
right now" — CI failures, aging PRs, stale deploys, substrate drift, and recently
merged work. If everything is green it says so in one line. Deterministic; zero LLM.

This is the feedback layer of the substrate-coherence model: a solo founder can't
watch 16 dashboards, so the suite reports its own exceptions on a schedule instead
of waiting to be asked. Run on every merge to main via repository_dispatch
(suite-state-changed) and nightly as fallback via digest-refresh.yml.
"""
import base64
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

import requests

GH_TOKEN = os.environ.get("GH_TOKEN", "")
NETLIFY_TOKEN = os.environ.get("NETLIFY_TOKEN", "")
NOW = datetime.now(timezone.utc)
TODAY = NOW.strftime("%Y-%m-%d")
STAMP = NOW.strftime("%Y-%m-%d %H:%M UTC")

# EQ repos only (SKS is a separate entity). Names are the GitHub repo slugs.
REPOS = ["eq-shell", "eq-solves-service", "eq-field", "eq-cards", "eq-solves-intake"]
PR_AGE_WARN_DAYS = 7
PR_AGE_CRITICAL_DAYS = 14  # escalates from 🟠 to 🔴
RECENTLY_MERGED_DAYS = 7
RECENT_PR_LIMIT = 15  # max rows shown in "recently built" table

# Netlify sites -> label. Only checked when NETLIFY_TOKEN is set.
NETLIFY_SITES = {
    "core.eq.solutions": "eq-shell",
    "eq-solves-service.netlify.app": "eq-service",
    "eq-solves-field.netlify.app": "eq-field",
}

# CI conclusions that mean "broken" (anything not in the healthy set).
HEALTHY_CI = {"success", "skipped", "neutral"}

# Infra/notification workflows — not build CI. Blocked from ci_status() so they
# don't overwrite the real build signal. Add any new meta-workflows here.
META_WORKFLOW_PATHS = {
    ".github/workflows/notify-substrate.yml",
    ".github/workflows/tenant-migrate.yml",
    ".github/workflows/deploy.yml",
    ".github/workflows/update-goldens.yml",
    ".github/workflows/backup.yml",
    ".github/workflows/integration.yml",       # pre-existing failures; not a build gate
    ".github/workflows/supabase-advisors.yml",
    ".github/workflows/suite-state-refresh.yml",
    ".github/workflows/digest-refresh.yml",
}


# ── fetch helpers ────────────────────────────────────────────────────────────
def gh_get(path):
    try:
        r = requests.get(
            f"https://api.github.com/{path}",
            headers={"Authorization": f"Bearer {GH_TOKEN}",
                     "Accept": "application/vnd.github+json"},
            timeout=15,
        )
        return r.json() if r.ok else None
    except Exception:
        return None


def ci_status(repo):
    """(conclusion, age_days) for the latest completed BUILD CI run on main.

    Skips meta/infra workflows (notify-substrate, deploy, backup, etc.) so the
    result reflects the actual build gate, not the most recent workflow of any kind.
    """
    data = gh_get(f"repos/eq-solutions/{repo}/actions/runs?branch=main&per_page=20&event=push")
    if not isinstance(data, dict):
        return "unknown", None
    for run in data.get("workflow_runs", []):
        if run.get("path") in META_WORKFLOW_PATHS:
            continue
        if run.get("conclusion"):
            age = None
            updated = run.get("updated_at", "")
            if updated:
                try:
                    age = (NOW - datetime.fromisoformat(updated.replace("Z", "+00:00"))).days
                except ValueError:
                    pass
            return run["conclusion"], age
    return "unknown", None


def open_prs(repo):
    """List of {num, title, age_days, draft} for open PRs on a repo."""
    data = gh_get(f"repos/eq-solutions/{repo}/pulls?state=open&per_page=30")
    out = []
    if not isinstance(data, list):
        return out
    for p in data:
        age = None
        created = p.get("created_at", "")
        if created:
            try:
                created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                age = (NOW - created_dt).days
            except ValueError:
                age = None
        out.append({
            "num": p.get("number"),
            "title": (p.get("title") or "").strip(),
            "url": p.get("html_url", ""),
            "age": age,
            "draft": bool(p.get("draft")),
        })
    return out


def recently_merged_prs(repo, days=RECENTLY_MERGED_DAYS):
    """PRs merged in the last N days, newest first."""
    data = gh_get(
        f"repos/eq-solutions/{repo}/pulls?state=closed&per_page=30&sort=updated&direction=desc"
    )
    if not isinstance(data, list):
        return []
    cutoff = NOW - timedelta(days=days)
    out = []
    for p in data:
        merged_at = p.get("merged_at")
        if not merged_at:
            continue
        try:
            merged_dt = datetime.fromisoformat(merged_at.replace("Z", "+00:00"))
        except ValueError:
            continue
        if merged_dt < cutoff:
            continue
        out.append({
            "num": p.get("number"),
            "title": (p.get("title") or "").strip(),
            "url": p.get("html_url", ""),
            "merged": merged_at[:10],
        })
    return out


def pending_open_items(path):
    """Unchecked items from a pending.md file. Returns list of strings."""
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []
    return [
        line.strip()[5:].strip()
        for line in lines
        if line.strip().startswith("- [ ]")
    ]


def worktree_stale_count(registry_path="system/worktree-registry.md"):
    """Count rows in the Stale section of the worktree registry."""
    try:
        with open(registry_path, encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return 0
    in_stale = False
    count = 0
    for line in content.splitlines():
        if "## Stale" in line:
            in_stale = True
            continue
        if in_stale and line.startswith("## "):
            break
        if (in_stale and line.startswith("| ")
                and not line.startswith("| Folder")
                and not line.startswith("|---")
                and "_(none)_" not in line):
            count += 1
    return count


def deploy_state(site):
    """(state, published_date) for a Netlify site's last deploy. Token-gated."""
    if not NETLIFY_TOKEN:
        return None, None
    try:
        sites = requests.get(
            "https://api.netlify.com/api/v1/sites",
            headers={"Authorization": f"Bearer {NETLIFY_TOKEN}"},
            params={"filter": "all"}, timeout=10,
        ).json()
        if not isinstance(sites, list):
            return None, None
        match = next((s for s in sites
                      if site in (s.get("name", "") + s.get("custom_domain", ""))), None)
        if not match:
            return None, None
        deploys = requests.get(
            f"https://api.netlify.com/api/v1/sites/{match['id']}/deploys",
            headers={"Authorization": f"Bearer {NETLIFY_TOKEN}"},
            params={"per_page": 1}, timeout=10,
        ).json()
        if not isinstance(deploys, list) or not deploys:
            return None, None
        d = deploys[0]
        published = (d.get("published_at") or d.get("created_at") or "")[:10]
        return d.get("state", "unknown"), published or None
    except Exception:
        return None, None


def substrate_honesty():
    """Run the L1 honesty check as a subprocess. Returns (ok|None, issue_lines)."""
    here = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(here, "..", "..", "scripts", "substrate_honesty.py")
    if not os.path.exists(script):
        return None, ["substrate_honesty.py not found"]
    try:
        r = subprocess.run([sys.executable, script],
                           capture_output=True, text=True, timeout=120)
        out = r.stdout
    except Exception as e:
        return None, [f"honesty check did not run: {e}"]
    if "Substrate is honest" in out:
        return True, []
    issues = [ln.strip()[2:].strip() for ln in out.splitlines()
              if ln.strip().startswith(("- DRIFT", "- STALE"))]
    return (False, issues) if issues else (None, ["honesty check inconclusive"])


def prev_digest_content():
    """Fetch the currently-committed digest.md from GitHub (before this run overwrites it)."""
    if not GH_TOKEN:
        return None
    data = gh_get("repos/eq-solutions/eq-context/contents/digest.md")
    if not isinstance(data, dict) or "content" not in data:
        return None
    try:
        return base64.b64decode(data["content"]).decode("utf-8")
    except Exception:
        return None


def parse_prev_digest(content):
    """Extract key facts from the previous digest.md for delta comparison."""
    result = {"timestamp": None, "ci": {}, "needs_you": None, "recent_prs": set()}
    if not content:
        return result
    for line in content.splitlines():
        # Timestamp: _2026-06-28 00:36 UTC · ...
        if line.startswith("_") and "UTC" in line:
            m = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC)", line)
            if m:
                result["timestamp"] = m.group(1)
        # CI from Pulse table: | eq-shell | ✓ success | ...
        if line.startswith("| eq-") and line.count("|") >= 3:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                repo = parts[1]
                ci_raw = parts[2]
                if repo in REPOS:
                    if "✓" in ci_raw:
                        result["ci"][repo] = "success"
                    elif "✗" in ci_raw:
                        result["ci"][repo] = "failure"
                    else:
                        result["ci"][repo] = "unknown"
        # Needs you count
        if "Needs you (" in line:
            m = re.search(r"Needs you \((\d+)\)", line)
            if m:
                result["needs_you"] = int(m.group(1))
        # Recent PRs: [#NNN](https://github.com/eq-solutions/REPO/pull/NNN)
        for m in re.finditer(
            r"\[#(\d+)\]\(https://github\.com/eq-solutions/([\w-]+)/pull/\1\)", line
        ):
            result["recent_prs"].add((m.group(2), int(m.group(1))))
    return result


# ── assemble ─────────────────────────────────────────────────────────────────
def build():
    # Fetch previous digest before anything so the delta can compare before/after.
    prev = parse_prev_digest(prev_digest_content())

    attention = []   # (severity_emoji, text)
    pulse = []       # (repo, ci, ci_age, n_open, oldest)
    recent_by_repo = {}  # repo -> [pr, ...]

    for repo in REPOS:
        ci, ci_age = ci_status(repo)
        prs = open_prs(repo)
        live_prs = [p for p in prs if not p["draft"]]
        ages = [p["age"] for p in live_prs if p["age"] is not None]
        oldest = max(ages) if ages else None
        pulse.append((repo, ci, ci_age, len(prs), oldest))
        recent_by_repo[repo] = recently_merged_prs(repo)

        if ci not in HEALTHY_CI and ci != "unknown":
            attention.append(("🔴", f"**CI {ci}** — {repo} `main`"))
        for p in live_prs:
            if p["age"] is not None and p["age"] >= PR_AGE_WARN_DAYS:
                title = p["title"][:70]
                link = f"[#{p['num']}]({p['url']})" if p["url"] else f"#{p['num']}"
                emoji = "🔴" if p["age"] >= PR_AGE_CRITICAL_DAYS else "🟠"
                attention.append((emoji, f"**PR aging {p['age']}d** — {repo} {link} \"{title}\""))

    n_stale_wt = worktree_stale_count()
    if n_stale_wt:
        s = "s" if n_stale_wt > 1 else ""
        attention.append(("🟡", f"**{n_stale_wt} stale worktree{s}** need cleanup — "
                                 f"[worktree-registry.md](system/worktree-registry.md)"))

    # Deploys (only when a Netlify token is wired)
    deploy_rows = []
    for site, label in NETLIFY_SITES.items():
        state, published = deploy_state(site)
        if state is None:
            continue
        deploy_rows.append((label, site, state, published))
        if state != "ready":
            attention.append(("🟠", f"**Deploy {state}** — {label} ({site})"))

    ok, issues = substrate_honesty()
    if ok is False:
        for issue in issues:
            attention.append(("🔴", f"**Substrate drift** — {issue}"))

    # Flatten + sort recently merged; cap for display
    recent_all = [
        (repo, pr)
        for repo, prs in recent_by_repo.items()
        for pr in prs
    ]
    recent_all.sort(key=lambda x: x[1]["merged"], reverse=True)
    total_recent = len(recent_all)
    recent_display = recent_all[:RECENT_PR_LIMIT]

    # Pending open items
    eq_pending = pending_open_items("eq/pending.md")

    # ── render ──
    lines = []
    lines.append("---")
    lines.append("title: EQ Suite — Health Digest")
    lines.append("owner: Royce Milmlow")
    lines.append(f"last_updated: {TODAY}")
    lines.append(
        "scope: Push-style 'what needs your attention' feed across the EQ suite. "
        "Regenerated on merge (repository_dispatch: suite-state-changed) and nightly. "
        "Full snapshot in suite-state.md."
    )
    lines.append("read_priority: high")
    lines.append("status: live")
    lines.append("---")
    lines.append("")
    lines.append("# EQ Suite — Health Digest")
    lines.append(f"_{STAMP} · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._")
    lines.append("")

    # ── delta (since last refresh) ──
    if prev.get("timestamp"):
        delta = []

        # CI changes
        ci_lookup = {repo: ci for repo, ci, _, _, _ in pulse}
        for repo, prev_ci in prev["ci"].items():
            curr_ci = ci_lookup.get(repo, "unknown")
            if prev_ci != curr_ci and curr_ci != "unknown" and prev_ci != "unknown":
                icon = "✅" if curr_ci == "success" else "🔴"
                delta.append(f"{icon} CI {repo}: {prev_ci} → {curr_ci}")

        # New PRs merged
        curr_pr_keys = {(repo, pr["num"]) for repo, pr in recent_all}
        new_prs = sorted(curr_pr_keys - prev["recent_prs"], key=lambda x: x[1], reverse=True)
        for repo, num in new_prs[:8]:
            title = next(
                (pr["title"][:60] for r, pr in recent_all if r == repo and pr["num"] == num), ""
            )
            link = next(
                (f"[#{num}]({pr['url']})" for r, pr in recent_all if r == repo and pr["num"] == num),
                f"#{num}",
            )
            delta.append(f"Merged: {repo} {link} {title}")

        # Needs you delta
        prev_n = prev.get("needs_you")
        curr_n = len(attention)
        if prev_n is not None and prev_n != curr_n:
            if curr_n < prev_n:
                delta.append(f"✅ Needs you: {prev_n} → {curr_n}")
            else:
                delta.append(f"⚠ Needs you: {prev_n} → {curr_n} (new items)")

        if delta:
            lines.append(f"## Since last refresh ({prev['timestamp']} → {STAMP})")
            lines.append("")
            for d in delta:
                lines.append(f"- {d}")
            lines.append("")

    n = len(attention)
    lines.append(f"## ⚠ Needs you ({n})" if n else "## ✓ Needs you (0)")
    lines.append("")
    if attention:
        for emoji, text in sorted(attention, key=lambda a: a[0] != "🔴"):
            lines.append(f"- {emoji} {text}")
    else:
        lines.append("**Nothing flagged — every EQ repo green, no aging PRs, substrate honest.** ✓")
    lines.append("")

    lines.append("## Pulse")
    lines.append("")
    lines.append("| Repo | CI (main) | CI age | Open PRs | Oldest PR |")
    lines.append("|------|-----------|--------|----------|-----------|")
    ci_icon = {"success": "✓", "failure": "✗", "cancelled": "⚠", "unknown": "?"}
    for repo, ci, ci_age, n_open, oldest in pulse:
        icon = ci_icon.get(ci, "?")
        oldest_s = f"{oldest}d" if oldest is not None else "—"
        ci_age_s = f"{ci_age}d ago" if ci_age is not None else "?"
        lines.append(f"| {repo} | {icon} {ci} | {ci_age_s} | {n_open} | {oldest_s} |")
    lines.append("")

    if deploy_rows:
        lines.append("## Deploys")
        lines.append("")
        lines.append("| Site | State | Last deploy |")
        lines.append("|------|-------|-------------|")
        for label, site, state, published in deploy_rows:
            lines.append(f"| {label} | {state} | {published or '?'} |")
        lines.append("")

    # Recently built — replaces the manual PR log in CLAUDE.md
    lines.append(f"## Recently built (last {RECENTLY_MERGED_DAYS} days)")
    lines.append("")
    if recent_display:
        lines.append("| Merged | Repo | PR |")
        lines.append("|--------|------|----|")
        for repo, pr in recent_display:
            title = pr["title"][:65]
            link = f"[#{pr['num']}]({pr['url']})" if pr["url"] else f"#{pr['num']}"
            lines.append(f"| {pr['merged']} | {repo} | {link} {title} |")
        if total_recent > RECENT_PR_LIMIT:
            lines.append(
                f"_Showing {RECENT_PR_LIMIT} of {total_recent} · "
                f"full record in [sessions/](sessions/)_"
            )
        else:
            s = "s" if total_recent != 1 else ""
            lines.append(f"_{total_recent} merge{s} · full record in [sessions/](sessions/)_")
    else:
        lines.append(f"_No merges in the last {RECENTLY_MERGED_DAYS} days._")
    lines.append("")

    # Pending open items (EQ + SKS)
    sks_pending = pending_open_items("sks/pending.md")
    for label, items, path in [("EQ", eq_pending, "eq/pending.md"), ("SKS", sks_pending, "sks/pending.md")]:
        if not items:
            continue
        lines.append(f"## Pending ({label})")
        lines.append("")
        for item in items[:10]:
            lines.append(f"- {item}")
        if len(items) > 10:
            lines.append(f"_…and {len(items) - 10} more · [{path}]({path})_")
        else:
            lines.append(f"_[{path}]({path})_")
        lines.append("")

    lines.append("## Substrate honesty")
    lines.append("")
    if ok is True:
        lines.append(
            "✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, "
            "no deleted refs used as live) matches reality."
        )
    elif ok is False:
        lines.append("✗ Drift detected — see **Needs you** above. Source: `scripts/substrate_honesty.py`.")
    else:
        lines.append("? Inconclusive — the honesty check did not complete this run.")
    lines.append("")

    lines.append("---")
    lines.append(
        f"_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · "
        f"on merge + nightly · {STAMP}._"
    )
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    digest = build()
    with open("digest.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(digest)
    print(f"digest.md written for {TODAY}")
    needs = digest.split("Needs you (")[1].split(")")[0]
    print(f"Needs you: {needs}")
