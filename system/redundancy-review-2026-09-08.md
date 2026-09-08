---
title: Redundancy review — EQ suite, scored across four layers
owner: Royce Milmlow
last_updated: 2026-09-08
scope: Cross-cutting score across the four redundancy layers spanning the EQ suite — data/platform DR, infra SPOFs, human/bus-factor, and substrate/knowledge consistency. Synthesis + net-new live findings only; each layer's full detail stays in its own doc.
read_priority: high
status: live
---

# Redundancy review — EQ suite, scored across four layers

Asked 2026-09-08 — no existing doc scored across all four redundancy layers
together. Each layer already had its own doc (`dr-backups.md`,
`infra-redundancy-scoping-2026-08-11.md`, `../ops/bus-factor-runbook.md`) but
nothing connected them or compared them. This doc is that index plus the
findings this pass added live — it does not restate any layer's own detail.

**Out of scope:** SKS-owned DR — per `dr-backups.md`'s own scope line, SKS
databases are never covered from the EQ side of the entity boundary.

**This is a dated snapshot, same convention as
`infra-redundancy-scoping-2026-08-11.md`.** Re-score via a new dated file next
time rather than editing these numbers in place.

---

## 1. Data / platform DR — 9/10

Full detail: [`system/dr-backups.md`](dr-backups.md),
[`system/runbooks/supabase-restore-drill.md`](runbooks/supabase-restore-drill.md).

Two-tier (Supabase managed daily + offsite R2 daily) across all three
platform planes (ehow, eq-canonical, eq-canonical-internal), auth data
explicitly captured, silent-empty guards, Sentry-monitored with missed-run
detection, and — the part almost nobody actually does — **proven by drill**:
quarterly automated restores into an ephemeral container, RTOs of 4-6
seconds, live-verified row counts.

**Gaps (already on file, not new):** PITR off on all three planes, inherited
from an SKS-scale cost decision and never independently re-confirmed at
current scale. Auth-data restore into a *real* Supabase target (not the
drill's bare container) plus the app-repoint smoke test is still a rare
manual game-day, not automated.

## 2. Infrastructure SPOFs — 5/10

Full detail: [`system/infra-redundancy-scoping-2026-08-11.md`](infra-redundancy-scoping-2026-08-11.md).

| SPOF | 2026-08-11 finding | This pass (2026-09-08) |
|---|---|---|
| Netlify (all 4 EQ prod sites, one account) | 1 member, Royce sole Owner, no recovery path | **Re-confirmed live** via `netlify-team-services-reader` → `get-teams`: still 1 member. **New finding:** `enforce_mfa: "not_enforced"` — not caught in the original pass. |
| Supabase (3 DBs, one org, one region) | No multi-AZ, no read replica | Not re-checked this pass. |
| DNS / domain (one Cloudflare zone, one GoDaddy registrar) | Registrar-lock/auto-renew never independently verified live | Still unverified — 4 weeks on. |
| Auth hub (eq-shell + jvkn) | Confirmed cascading in code (`token-exchange.ts`) — Shell/jvkn down means no new sessions suite-wide | Unchanged. Still an implicit tradeoff, not a signed-off decision. |
| Crons | Genuinely split across GitHub Actions + Netlify Scheduled Functions | Unchanged — fine as-is. |
| GitHub (source control, CI/CD trigger, all DR/security automation) | Not assessed — outside the original 5-vector scope | **New vector, found 2026-09-08** (surfaced by a direct "what if GitHub is down" question, not a scheduled sweep). Not in the live runtime path — deployed apps, auth, and data don't call GitHub, so an outage doesn't take the product down: Netlify keeps serving already-built apps, Supabase keeps serving data, existing sessions are unaffected. What stops: shipping anything new (Netlify's GitHub App can't trigger a build without it), and every DR/security automation job — backups, restore-verify, restore-drills, digest/suite-state refresh, the whole guard-ratchet system are all GitHub Actions. Substrate reads via `raw.githubusercontent.com` fail; local clones (Beelink/Cowork/Code) are unaffected, they're just files on disk. Compounding risk, not a direct one: an outage long enough to skip a backup window widens RPO past the normal 24h *if* it overlaps a real DB incident in the same window. |

**Six vectors now, not five** — GitHub wasn't in the original 2026-08-11 scope. `infra-redundancy-scoping-2026-08-11.md` itself is left as the historical record of what was checked then; the sixth row lives only here.

**New this pass:** attempted to verify GitHub org-admin membership via
`list_repository_collaborators` (owner `eq-solutions`, repo `eq-shell`) — the
connected GitHub App returned `404`. That check is **not currently possible**
from an AI session; needs Royce's own confirmation via
`github.com/orgs/eq-solutions/people`, not another retry.

Neither of the two decisions the 2026-08-11 pass flagged as worth a real call
(Netlify recovery path, auth-hub accept-or-fix) has been acted on a month
later.

## 3. Human / bus-factor redundancy — 3/10

Full detail: [`ops/bus-factor-runbook.md`](../ops/bus-factor-runbook.md).

The runbook's own §1 ("Who to contact") is still unfilled — the doc says so
itself: *"only Royce can complete this section... if the honest answer is
'nobody but Royce,' that's the single highest-priority gap."* Combined with
§2's live Netlify finding above, that's not hypothetical today: there is
currently no confirmed second human with Netlify access, and GitHub/Supabase
org admin lists aren't independently checkable from this session at all.
Never game-dayed against anyone but Royce.

## 4. Substrate / knowledge redundancy — 6/10

Full detail: [`system/failures.md`](failures.md) (the guard-ratchet ledger),
[`system/machinery.md`](machinery.md) (the guard inventory).

Not traditionally scored as "redundancy," but keeping many concurrent AI
sessions and tools from silently diverging or corrupting the one shared
checkout is exactly that problem. The ledger tracks it with real rigor — 15
failure classes, a 4-rung enforcement ladder, adversarial regression tests —
more mature than most teams' actual product tooling.

The two most-recurring entries both sit at rung 4 with **stated, still-open
gaps**, quoted from their own notes:
- **F9** (concurrent-session git races, 5 recurrences): *"no guard currently
  protects a session's own staged-but-uncommitted work FROM a concurrent
  session's git operation."*
- **F14** (hand-written claims silently going stale, 5 recurrences): doesn't
  cover hand-maintained prose inside nominally `generated` files — caused a
  real 6-day live bug in eq-field before being caught.

**Live evidence this pass, not a new failure class:** this session opened
with the local clone 90 commits behind `origin/main`, carrying ~30
uncommitted files that overlap almost exactly with work already pushed by a
concurrent session (F9's exact shape); `core.hooksPath` resolving in a way
`hooks/session_start.py`'s own HOOKS check flagged wrong; and
`shared-object-drift.yml` at 6 consecutive failures sitting in `digest.md`'s
Needs You. By the time this doc was actually written, the same checkout had
drifted from 90 to 93 to **101** commits behind — three re-checks in one
session, each one further behind, while multiple other session-close
worktrees (`eq-context-wt-close`, `eq-context-wt-close-b6eaba92`) were active
on the same repo concurrently. All of this is existing, tracked, rung-4-guarded
failure classes — this is their known gaps still being live, not a new bypass.

---

## Overall: 6/10 — strong foundations, unclosed loops

Unweighted average of the four scores above. The one thing almost every team
gets wrong — data DR — is the one thing this suite has actually drilled and
proven. The weakest link isn't infrastructure, it's that redundancy for the
person running it all is close to zero, and two of the substrate's own
most-recurring failures are known-open rather than closed.

## Top 5 (cross-layer, ordered by leverage)

1. **Fix the human SPOF.** Add a second Netlify team member, turn on
   `enforce_mfa`, fill `../ops/bus-factor-runbook.md` §1. Cheapest,
   highest-exposure gap in the review — an afternoon of work.
2. **Reconcile this checkout and make `scripts/safe_commit.py` the default
   write path for eq-context.** It already fixes F9's open gap in practice
   (throwaway-worktree commit+push, rebase-and-retry on race) — it's just
   sitting unused. Sort out the current 100+-behind/uncommitted-pile state
   before it becomes F9's 6th recurrence — it was actively getting worse
   (90 → 93 → 101 commits behind) over the course of writing this one doc.
3. **Make the auth-hub cascade a conscious decision, not an implicit one.**
   Either formally accept "Shell/jvkn down = no new sessions suite-wide" in
   writing with alerting on `token-exchange.ts` failure rate, or scope a
   degraded-mode fallback. The most consequential SPOF in the suite currently
   has nobody's signature on it.
4. ~~**Close the code-repo backup gap**~~ **BUILT 2026-09-08, not yet armed** —
   [`backup-code.yml`](../.github/workflows/backup-code.yml) takes a nightly
   `git bundle --all` of every active EQ repo to the same R2 bucket used by
   the DB jobs, `code/` prefix — no new infrastructure. Needs `CODE_BACKUP_PAT`
   added (see the workflow's own header) before its first real run; every
   attempt fails loudly, not silently, until then.
5. ~~**Re-arm `shared-object-drift.yml`**~~ **FIXED 2026-09-08, verified green.**
   Not a broken cron — the guard was correctly detecting a real drift on
   `app_data.field_people_iud`, unreconciled since migrations 0273/0274
   (eq-shell PR #1567/#1572, 2026-08-24) shipped the upward Cards-identity-push
   feature and nobody ran `--update-snapshot` afterward. Traced to the exact
   PRs, confirmed both sides' code already matches (eq-cards PR #325,
   2026-08-27), re-verified all 12 registered objects live against ehow before
   rebaselining, pushed via `scripts/safe_commit.py`, re-dispatched —
   confirmed green (run `34210284442`). **DNS re-verified**: `eq.solutions`
   still authoritative on Cloudflare (`robin`/`clark.ns.cloudflare.com`),
   matching the original finding. **Not re-verified**: registrar-lock status
   and Cloudflare account MFA (dashboard-only, no tool access) and whether
   `token-exchange.ts` has a live alert rule (Sentry's alert-rules API
   returned 410 Gone — a dead endpoint, not a permissions block; not chased
   further).

---

## Follow-ups

- GitHub org-admin membership still needs Royce's own direct confirmation —
  the MCP-based check is a `404`, not just unfilled.
- The two live checks this pass (Netlify team state, GitHub collaborator
  attempt) cost two tool calls and turned up a finding the original scoping
  missed. Worth repeating on every future re-score, not just this once.
- This file's own creation deliberately did not touch git — no add, commit,
  or push. The working tree was already 90+ commits behind `origin/main`
  (worsening to 101 while this doc was being written) with a large
  uncommitted pile when this pass started. Reconciling that is item #2
  above, not attempted here.
