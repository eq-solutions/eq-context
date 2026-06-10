---
title: "Sprint 8 Board — Close the Loop"
owner: Royce Milmlow
last_updated: 2026-06-10
scope: Sprint 8 task board
read_priority: critical
status: live
---

# Sprint 8 Board — Close the Loop

**Started:** 2026-06-10
**Theme:** Four things started, not finished. One hard deadline. Sprint 8 is not a new build — it is the work that eliminates four active risks that compound every day they stay open.

---

## Steelman

Sprint 7 shipped a technically complete migration. The smoke test hasn't run.

That sounds minor. It isn't. Until PR #257 merges and the domain cutover executes:

- **urjh is still live** — two sources of truth for the same data, one of which is the old one. A session that writes to urjh after cutover (e.g. Sentry cron hitting the old URL) creates silent divergence. The migration cost was significant; the window for it to matter is open until urjh's keys are revoked.
- **`service.eq.solutions` is still up** — that's a second auth surface with direct-urjh email+MFA, not Shell OTP. The cutover removes it; until then it's a live bypass of the Shell auth model.
- **urjh service-role keys are still valid** — they exist in Netlify env vars and aren't rotated. Every day they're live is a day a leak of those vars matters.

Meanwhile:

- **25 workers have invites expiring 2026-06-15.** That's 5 days from now. If those expire, Royce manually re-invites 25 people. The fix is a 30-minute Supabase query to populate missing emails and a reminder to staff. The cost of missing this deadline is ~2 hours of admin pain.
- **Three GitHub PATs are compromised** (were tracked in plaintext in `system/infrastructure.md`). They've been on the CRITICAL list for weeks. The PATs gate push access to `eq-solutions/*`. Every day is exposure.
- **EQ_SECRET_SALT parity between Shell and Service has never been verified.** If they differ, Shell-minted sessions silently fail validation in Service — you get "login works but Service doesn't load", diagnosed as auth, hours of debugging in production. A 5-minute environment variable check now.
- **SKS roles Prompt A** (merge eq-roles PR #7 + converge eq-shell branches) is Royce's action, not an agent's. Every day it waits, the SKS roles sprint (Prompts B-E) waits. That sprint gates the first real SKS user assignment in `user_security_groups`, which gates the SKS Field go-live smoke, which gates retiring the standalone (`sks-nsw-labour v3.10.59`). Prompt A is 20 minutes of Royce's time. The dependency chain is long.

**The steelman:** Sprint 8 is not glamorous. It is the sprint where things that are 90% done become 100% done, and three security obligations that have been deferred too long get closed. Sprint 9 can be the roles sprint (B-E), the design system, EQ Field features. Sprint 8 just closes the loop.

---

## Definition of Done

Sprint 8 is complete when:

- [ ] `service.eq.solutions` redirects to `core.eq.solutions` or is decommissioned
- [ ] urjh service-role keys are revoked in Netlify
- [ ] urjh is paused in Supabase
- [ ] All 25 worker invites are resent or expiry date extended; email gaps on 8 workers filled
- [ ] All 3 GitHub PATs rotated (old ones revoked, new fine-grained PAT issued)
- [ ] `EQ_SECRET_SALT` confirmed identical between Shell and Service prod env vars
- [x] eq-roles PR #7 merged, v2.3.0 tagged *(already on main)*
- [x] eq-shell dep at v2.3.0 *(already on main)*
- [ ] Stale branches `c2-shell-roles` + `sks-field-host` closed on GitHub

---

## Stream A — Sprint 7 landing (unblocked, ~2h)

**Dependency:** none. Royce has access to service.eq.solutions, Supabase, and Netlify now.

**Why this stream first:** every other stream is independent of it, but the risk window for urjh divergence closes only when these 4 steps are done. It is the oldest open item.

### A1 — Smoke test (Royce, 15 min)

1. Open `core.eq.solutions` in incognito.
2. Sign in via Shell OTP.
3. Navigate to Service module.
4. Confirm maintenance checks, tests, defects visible (should show SKS data on ehow tenant `7dee117c`).
5. Create a test maintenance check — confirm it saves without error.
6. Record: passed or failed.

**If pass → proceed A2. If fail → open a session in eq-service, describe the symptom.**

### A2 — Merge PR #257 (Royce, 5 min)

GitHub → eq-solutions/eq-service → Pull Requests → #257 → Merge.
Netlify auto-deploys from main. Wait for deploy to complete (~3 min).

### A3 — Service domain cutover (Royce, 20 min, requires Netlify + Cloudflare access)

1. **Netlify:** Go to `eq-solves-service` site → Domain settings → Remove `service.eq.solutions`.
2. **Cloudflare:** Add a redirect rule: `service.eq.solutions` → `core.eq.solutions/sks/service` (301).
3. Confirm redirect fires in browser.
4. Update `NEXT_PUBLIC_SITE_URL` in Netlify env vars for the shell site if it's pointing anywhere stale.
5. Update Supabase Auth URL allowlist on ehow: remove `service.eq.solutions`, confirm `core.eq.solutions` is present.

### A4 — Revoke urjh keys + pause (Royce, 15 min)

1. Netlify → `eq-solves-service` site → Environment variables → delete or blank `SUPABASE_SERVICE_ROLE_KEY` (the urjh one).
2. Supabase → `urjhmkhbgaxrofurpbgc` → Settings → API → Regenerate service role key (invalidates the old one).
3. Supabase → `urjhmkhbgaxrofurpbgc` → Settings → Pause project.

> **Caution:** confirm the scheduler/cron routes (`supervisor-digest`, `pre-visit-brief`) are not still pointing at urjh before pausing. Run a quick grep on eq-service for `urjhm` before step 2. If hits: flag, defer A4 until routes are moved.

---

## Stream B — Worker invite deadline (unblocked, ~30 min)

**Hard deadline: 2026-06-15.** Invites expire. Miss this, ~2h of re-invite admin.

### B1 — Fill email gaps on 8 workers (agent session, 15 min)

8 workers in `eq-canonical.public.workers` have null email. Run:

```sql
SELECT id, full_name, email, created_at
FROM public.workers
WHERE email IS NULL OR email = ''
ORDER BY created_at;
```

Cross-reference with EQ Field staff records. Update email via:

```sql
UPDATE public.workers SET email = '<correct_email>' WHERE id = '<uuid>';
```

**Owner:** agent session in eq-shell, targeting `jvknxcmbtrfnxfrwfimn`. Requires Royce to confirm correct emails (cross-ref from Field or HR records).

### B2 — Extend or resend invites for 25 workers (Royce, 10 min)

In eq-canonical `public.worker_invites`, check expiry:

```sql
SELECT w.full_name, wi.email, wi.expires_at, wi.status
FROM public.worker_invites wi
JOIN public.workers w ON w.id = wi.worker_id
WHERE wi.status = 'pending'
  AND wi.expires_at < now() + interval '7 days'
ORDER BY wi.expires_at;
```

Options:
- **Extend:** `UPDATE public.worker_invites SET expires_at = now() + interval '14 days' WHERE status = 'pending';`
- **Resend:** trigger the invite email via Shell admin UI if available, or via a Supabase Edge Function call.

**Owner:** Royce (SQL above can be run via Supabase Studio SQL editor — no code change needed). Confirm with Royce which option.

### B3 — Remind staff (Royce, 5 min)

Send a Slack/WhatsApp/SMS to field staff: "Check your email for an EQ Shell invite — expires [date]. Click Accept, then set your PIN."

---

## Stream C — Security obligations (unblocked, ~30 min total)

These are overdue. No technical prerequisite.

### C1 — EQ_SECRET_SALT parity check (Royce, 5 min)

1. Netlify → `core.eq.solutions` (eq-shell site) → Environment variables → find `EQ_SECRET_SALT`. Copy the value (last 4 chars sufficient for comparison).
2. Netlify → `eq-solves-service` site → Environment variables → find `EQ_SECRET_SALT`. Compare last 4 chars.
3. **If identical:** record confirmed in `eq-context/sessions/2026-06-10.md` and tick this item.
4. **If different:** do not deploy anything until fixed. Open a session — the fix is setting the Service env var to match Shell, then redeploying.

> This is the 🔴 item. It is 5 minutes. Do it before the stream A cutover work — if they differ, the smoke test (A1) will silently fail authentication.

### ~~C2 — Rotate GitHub PATs~~ ✓ Done 2026-06-10

All 3 PATs revoked, new fine-grained PAT issued, Beelink credentials updated.

### C3 — Add gitleaks pre-commit hook to eq-context (agent session, 10 min)

Prevents a recurrence of C2.

```bash
cd C:\Projects\eq-context
npx --yes gitleaks protect --staged --redact --config .gitleaks.toml
```

Or add a simpler hook that greps for `ghp_|gho_|supabase.co.*service_role` before commit. One small file:

```
.git/hooks/pre-commit (or .husky/pre-commit)
```

**Owner:** short agent session in eq-context. Done when the hook fires on a test commit containing a fake `ghp_` string.

---

## Stream D — SKS roles entry ✓ Already done (verified 2026-06-10)

Live inspection found all three D items complete on main:

| Item | Finding |
|---|---|
| D1 — merge eq-roles PR #7 + tag v2.3.0 | ✅ PR #7 commit `e017cc0` is on main; `v2.3.0` tag exists |
| D2 — branch convergence | ✅ Both branches stale — content already on main; close without merging |
| D3 — dep bump in eq-shell | ✅ main already has `@eq-solutions/roles: github:eq-solutions/eq-roles#v2.3.0` |

**Stale branches to close (do not merge):**
- `claude/c2-shell-roles` — roles wiring already on main. Branch still on `#main` dep + older tokens version (v1.0.0 vs v1.3.2 on main). Merging would be a downgrade.
- `claude/sks-field-host` — fieldTenants.ts URL change irrelevant (SKS Field routes via Shell `/sks/field`, not an external URL). 64KB behind main.

**Unblocked:** Sprint 9 roles sprint (Prompts B-E) can start now. Prompts are in `sks-live-sprint-2026-06-07.md`.

---

## Order of operations

```
C1 (salt check)  →  A1 (smoke)  →  A2 (PR #257 merge)
                                 →  A3 (domain cutover)
                                 →  A4 (urjh pause)

B1 + B2 + B3  ←  run any time, MUST be done before 2026-06-15

C2 ✓ DONE     C3 (gitleaks hook)  ←  any time

D1/D2/D3 ✓ DONE  ←  Sprint 9 roles (B-E) is unblocked
```

**Do C1 first, always.** Everything else in Streams A and D is a push to production. If the salt is wrong, diagnose it before any prod deployment.

---

## What is NOT in Sprint 8

Explicitly excluded — these belong in Sprint 9 or later:

| Item | Why excluded |
|---|---|
| SKS roles Prompts B-E | Gate on D2/D3. Will be Sprint 9 (full agent sprint, detailed prompts already in `sks-live-sprint-2026-06-07.md`). |
| SKS Field smoke + soak + retire standalone | Gate on roles sprint completion. |
| P2 customer convergence (481 ambiguous) | Needs Royce dedup decisions — not a sprint task, a working session. |
| EQ Design System A7-A11 | No deadline, no block. Sprint 9 or 10. |
| EQ Field tender pipeline SKS promotion | Gate on SKS live being further along. |
| Scheduler/route migration (4.4) | Needs route-hosting decision first. Separate session. |
| EQ Service delta WO import dry-run | Valuable but not time-critical. |
| P7a SKS anon-remediation | Requires "SKS live" explicit instruction. |
| P7d EQ Service advisor audit | May be moot if Sprint 7 cutover completes + urjh decommissioned — confirm first (A4). |

---

## Sprint 9 preview (plan now, run then)

Once Sprint 8 closes the loop:

- **SKS roles Prompts B-E** (agent sprint, prompts in `sks-live-sprint-2026-06-07.md`) — wire `extra_perms` into session, build `AdminSecurityGroups` page, walk first real SKS user E2E, apply `WITH CHECK` hardening.
- **SKS Field smoke + soak** (Royce) — functional click-through on `core.eq.solutions/sks/field`, 24-48h soak, retire standalone.
- **Design system A7-A10** — Modal, FormInput, StatusBadge, Card/Toast/Tabs.

Sprint 9 is executable as soon as `user_security_groups` has its first real row.
