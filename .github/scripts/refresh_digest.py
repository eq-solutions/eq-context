#!/usr/bin/env python3
"""Generate digest.md — a push-style "what needs your attention" view of the EQ suite.

Companion to refresh_suite_state.py (the full snapshot). suite-state.md answers
"what is the state of everything"; digest.md answers "what, if anything, needs me
right now" — CI failures, aging PRs, stale deploys, substrate drift. If everything
is green it says so in one line. Deterministic; zero LLM inference.

This is the feedback layer of the substrate-coherence model: a solo founder can't
watch 16 dashboards, so the suite reports its own exceptions on a schedule instead
of waiting to be asked. Run nightly via .github/workflows/digest-refresh.yml.
"""
import os
import subprocess
import sys
from datetime import datetime, timezone

import requests

GH_TOKEN = os.environ.get("GH_TOKEN", "")
NETLIFY_TOKEN = os.environ.get("NETLIFY_TOKEN", "")
NOW = datetime.now(timezone.utc)
TODAY = NOW.strftime("%Y-%m-%d")
STAMP = NOW.strftime("%Y-%m-%d %H:%M UTC")

# EQ repos only (SKS is a separate entity). Names are the GitHub repo slugs.
REPOS = ["eq-shell", "eq-solves-service", "eq-field", "eq-cards", "eq-solves-intake"]
PR_AGE_WARN_DAYS = 7

# Netlify sites -> label. Only checked when NETLIFY_TOKEN is set.
NETLIFY_SITES = {
    "core.eq.solutions": "eq-shell",
    "eq-solves-service.netlify.app": "eq-service",
    "eq-solves-field.netlify.app": "eq-field",
}

# CI conclusions that mean "broken" (anything not in the healthy set).
HEALTHY_CI = {"success", "skipped", "neutral"}


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
    """Latest completed CI conclusion on main (success/failure/...), or 'unknown'."""
    data = gh_get(f"repos/eq-solutions/{repo}/actions/runs?branch=main&per_page=5&event=push")
    if not isinstance(data, dict):
        return "unknown"
    for run in data.get("workflow_runs", []):
        if run.get("conclusion"):
            return run["conclusion"]
    return "unknown"


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


# ── assemble ─────────────────────────────────────────────────────────────────
def build():
    attention = []   # (severity_emoji, text)
    pulse = []       # (repo, ci, n_open, oldest)

    for repo in REPOS:
        ci = ci_status(repo)
        prs = open_prs(repo)
        live_prs = [p for p in prs if not p["draft"]]
        ages = [p["age"] for p in live_prs if p["age"] is not None]
        oldest = max(ages) if ages else None
        pulse.append((repo, ci, len(prs), oldest))

        if ci not in HEALTHY_CI and ci != "unknown":
            attention.append(("🔴", f"**CI {ci}** — {repo} `main`"))
        for p in live_prs:
            if p["age"] is not None and p["age"] >= PR_AGE_WARN_DAYS:
                title = p["title"][:70]
                link = f"[#{p['num']}]({p['url']})" if p["url"] else f"#{p['num']}"
                attention.append(("🟠", f"**PR aging {p['age']}d** — {repo} {link} \"{title}\""))

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
    if ok is False:  # only real drift is an attention item; inconclusive is not
        for issue in issues:
            attention.append(("🔴", f"**Substrate drift** — {issue}"))

    # ── render ──
    lines = []
    lines.append("---")
    lines.append("title: EQ Suite — Health Digest")
    lines.append("owner: Royce Milmlow")
    lines.append(f"last_updated: {TODAY}")
    lines.append("scope: Push-style 'what needs your attention' feed across the EQ suite. "
                 "Regenerated nightly by GitHub Action (digest-refresh.yml). Full snapshot in suite-state.md.")
    lines.append("read_priority: high")
    lines.append("status: live")
    lines.append("---")
    lines.append("")
    lines.append("# EQ Suite — Health Digest")
    lines.append(f"_{STAMP} · what needs your attention. Full snapshot: [suite-state.md](suite-state.md)._")
    lines.append("")

    n = len(attention)
    lines.append(f"## ⚠ Needs you ({n})" if n else "## ✓ Needs you (0)")
    lines.append("")
    if attention:
        # 🔴 first, then 🟠
        for emoji, text in sorted(attention, key=lambda a: a[0] != "🔴"):
            lines.append(f"- {emoji} {text}")
    else:
        lines.append("**Nothing flagged — every EQ repo green, no aging PRs, substrate honest.** ✓")
    lines.append("")

    lines.append("## Pulse")
    lines.append("")
    lines.append("| Repo | CI (main) | Open PRs | Oldest |")
    lines.append("|------|-----------|----------|--------|")
    ci_icon = {"success": "✓", "failure": "✗", "cancelled": "⚠", "unknown": "?"}
    for repo, ci, n_open, oldest in pulse:
        icon = ci_icon.get(ci, "?")
        oldest_s = f"{oldest}d" if oldest is not None else "—"
        lines.append(f"| {repo} | {icon} {ci} | {n_open} | {oldest_s} |")
    lines.append("")

    if deploy_rows:
        lines.append("## Deploys")
        lines.append("")
        lines.append("| Site | State | Last deploy |")
        lines.append("|------|-------|-------------|")
        for label, site, state, published in deploy_rows:
            lines.append(f"| {label} | {state} | {published or '?'} |")
        lines.append("")

    lines.append("## Substrate honesty")
    lines.append("")
    if ok is True:
        lines.append("✓ Honest — every load-bearing fact (Supabase project liveness, deploy URLs, "
                     "no deleted refs used as live) matches reality.")
    elif ok is False:
        lines.append("✗ Drift detected — see **Needs you** above. Source: `scripts/substrate_honesty.py`.")
    else:
        lines.append("? Inconclusive — the honesty check did not complete this run.")
    lines.append("")

    lines.append("---")
    lines.append(f"_Generated deterministically (no LLM) by `.github/scripts/refresh_digest.py` · "
                 f"nightly + on demand · {STAMP}._")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    digest = build()
    with open("digest.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(digest)
    print(f"digest.md written for {TODAY}")
    # Echo the 'Needs you' count to the Actions log for at-a-glance run history.
    needs = digest.split("Needs you (")[1].split(")")[0]
    print(f"Needs you: {needs}")
