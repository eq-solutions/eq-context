---
title: Substrate-coherence sprint — honesty CI + security gate + digest + Node 24 bump
date: 2026-06-27
owner: Royce Milmlow + Claude Code
scope: eq-context repo — substrate observability layer
session_id: 9d0edb59-5c97-4110-91de-31c1e33be786
---

# 2026-06-27 — Substrate-coherence sprint

## What shipped

### PR #38 — EQ-only security gate (`97d0e35`)
- `scripts/rls_probe.py` — public-key zero-rows probe on 4 EQ Supabase projects (eq-canonical, eq-canonical-internal, sks-canonical/ehow, eq-solves-field). No secrets needed.
- `scripts/security_audit.py` — Supabase management API advisor audit (needs `SUPABASE_ACCESS_TOKEN`); EQ-only scope (sks-labour dropped); accepted-baseline dict.
- `scripts/test_security.py` — unit tests for triage logic.
- `.github/workflows/security-audit.yml` — weekly Sunday + on-push to scripts + on-demand. Advisory mode (`continue-on-error: true`).
- Scope decisions: urjh (deleted) and sks-labour (retiring) removed from PROJECTS.

### PR #39 — Substrate-honesty CI (`094d104`)
- `system/substrate-facts.yml` — machine-readable manifest: 5 Supabase projects (4 live, 1 deleted/urjh), 3 deploy URLs, 1 forbidden live ref (urjh).
- `scripts/substrate_honesty.py` — probes manifest vs reality; classifiers `classify_supabase`, `classify_deploy`, `verdict`; `scan_forbidden` with historical-file exemption and ±3-line context check; 42 urjh mentions correctly suppressed.
- `scripts/test_substrate_honesty.py` — 15 classifier unit tests; key regression: `deleted+live → DRIFT`.
- `.github/workflows/substrate-honesty.yml` — nightly 11:00 UTC + on-PR + dispatch. No secrets.

### PR #40 — Suite-health digest (`0a072d4`)
- `.github/scripts/refresh_digest.py` — generates `digest.md`: CI status, PRs aging ≥7d, deploy state (Netlify token-gated), substrate honesty section.
- `.github/workflows/digest-refresh.yml` — nightly 12:00 UTC (after suite-state + honesty). Commits `digest.md [skip ci]`.
- `digest.md` — seed snapshot committed; regenerated nightly.
- `CLAUDE.md` §1 — added digest read instruction as the session-start "push" delivery mechanism.

### PR #41 — Cloudflare 1010 UA fix (`a7f79c2`)
- Root cause: urllib default (empty) User-Agent is blocked by Cloudflare in front of `api.supabase.com` with HTTP 403 / error code 1010.
- Fix: `USER_AGENT` constant in `scripts/security_audit.py`; passed in every `fetch()` request.
- `SUPABASE_ACCESS_TOKEN` wired by Royce in GitHub repository secrets (`sbp_…`).
- Post-fix: advisor audit reaches Supabase — all 4 EQ projects return ERROR 0.

### PR #42 — Node 24 actions bump (`7268589`)
- `actions/checkout@v4` → `@v7` (released 2026-06-18)
- `actions/setup-python@v5` → `@v6` (released 2026-06-24)
- 12 occurrences across 7 workflow files. Clears GitHub deprecation annotation.

### eq-cards AGENTS.md (direct push, separate Cowork session)
- `commit 7fd2094` — added `AGENTS.md` to eq-cards root. Self-contained: stack, commands, guardrails, substrate pointer.

## Decisions

- **Advisory-first gate** — `continue-on-error: true` on finding steps; flip to blocking by removing those lines once signal is trusted.
- **Lean finish** — mid-sprint Royce selected lean cut: drop #20 (drift-guard promotion already done everywhere via recon), fill eq-cards only (the one real AGENTS.md gap), wire the session-start hook. Not the full "all 5" he'd greenlighted.
- **EQ-only scope** — sks-labour excluded from all probing (retiring + separate entity). A green gate no longer implies SKS-labour's SEC-1 finding is closed (tracked in `ops/security-register.md`).
- **Stale-ref suppression** — historical files (archive/, sessions/, changelog/, decisions.md, lessons.md, dated snapshots) and qualified mentions (deleted/retired/former/→) are exempt from forbidden-ref scan. Prevents 42 legitimate urjh mentions from false-triggering.

## Bugs found and fixed

- **Stale-ref false positives (16→0)**: first scan version used single-line qualifier check; widened to `is_historical()` + ±3-line context window.
- **CI didn't fire on PR open**: GitHub silently dropped `pull_request: opened` trigger; nudged with empty commit (`synchronize` event).
- **Cloudflare 1010**: urllib no-UA → 403/1010; with-UA → reaches Supabase. Fixed by `USER_AGENT` constant.

## Repo state

eq-context `main` @ `d0ff247` (includes session log commit). All PRs merged, no open PRs, CI green.
