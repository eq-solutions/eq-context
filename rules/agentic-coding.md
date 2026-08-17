---
title: Rules — Agentic Coding
owner: Royce Milmlow
last_updated: 2026-08-17
scope: How assistants write and verify EQ/SKS product code — plan gate, verification standard, maintainability guards
read_priority: critical
status: live
---

# Rules — Agentic Coding

Writing code is no longer the constraint. **Verifying it, and not accumulating
regression debt across many agent-driven iterations, is.** These rules govern how
code gets planned, proven, and kept maintainable. They sit alongside
`rules/non-negotiables.md` (which overrides everything) and `rules/stack.md`
(what to build with).

---

## 1. Session Gate — plan before execute

Before any build task (any Edit, Write, migration, or PR), run in this order:

1. **Suite state** — read `suite-state.md` first. Check System Health for CI failures and stale deploys.
2. **Live recon** — query the live system, don't infer it. `list_tables` / a targeted `select` on the relevant Supabase project beats an assumption. Same for a deployed version or an applied migration. (`rules/non-negotiables.md` — substrate claims about live state are leads, not facts.)
3. **Branch check** — `git branch -a` + `git status` on the target repo, **plus `git fetch origin main --quiet && git log HEAD..origin/main --oneline`**. Non-empty output means real history from `main` is missing. Skim the titles for anything touching the same files or feature before writing new code — a stale branch once shipped a fix that had already merged days earlier via another session, discovered mid-build instead of before it (2026-07-28).
4. **Worktree check** — read `system/worktree-registry.md` before creating any worktree. **Default to a fresh worktree for any commit-producing work** in a repo with concurrent-session traffic (eq-shell, eq-field, eq-context itself) — not just app code. eq-context's own root checkout forked from `origin/main` multiple times on 2026-08-08 from concurrent sessions committing directly on its shared `main`; recovered without loss, but only after real content-level forensics (see `sessions/2026-08-08.md`). `git worktree add <path> origin/<branch>`, commit and push from there, remove the worktree after. This is a *documented* rule, not a self-enforcing one — per §3, it's backed by a structural guard: `eq-guard`'s `stale-main-gate` rule (added 2026-08-09) blocks a `git commit` directly on a shared checkout's `main`/`master` when local HEAD is behind its upstream (`EQ_SKIP_STALE_MAIN=1` to override for a deliberate one-off). eq-field's identical rule (its own `CLAUDE.md`, PR #673) was violated same-day by concurrent sessions before this guard existed — the prose alone doesn't hold; the guard is what actually closes the gap.
5. **State the brief** — what exists (verified), what's broken, what changes, what not to touch. Royce confirms. Then build.

**Step 5 is not optional.** Template: `system/task-brief-template.md`. On the Beelink
it is mechanically gated — a commit-time hook blocks writes until the brief has run
this session, so a forgotten brief fails loudly rather than silently. Other tools are
on their honour; the gate's absence is not permission to skip.

If live state contradicts the task's assumptions, **stop and surface the gap** before
writing anything.

---

## 2. Verification beats inspection

**A change is done when it has been exercised, not when it has been read.**
Static analysis, a green typecheck, and a passing review all confirm the code is
*shaped* right. None of them confirm it *works*.

Three real cases, all where inspection had already passed:

| What passed | What still shipped broken | Caught by |
|---|---|---|
| `flutter analyze` clean | four crashing wallet cards (2026-07-21) | the widget-test suite |
| Code review on the original PR | three stacked bugs; self-serve provisioning had **never once worked** in production | re-running the live flow after each fix |
| A green terminal + a commit hash | substrate content that never landed | fetching the committed file and checking for an expected marker |

Rules that follow:

- The assistant MUST run the repo's own behavioural gate before calling a change done — widget tests for Flutter (`rules/stack.md`), `tsc + next build` for EQ Service, the test suite where one exists.
- Where a change alters a user-visible flow, the assistant SHOULD exercise that flow end to end, or state plainly that it could not and what remains unproven. **"Analyzer clean, tests green, not click-tested" is an honest and acceptable outcome. "Done" when it means only the first two is not.**
- A fix for a bug that inspection missed once MUST be verified by re-running the thing that failed, not by re-reading the patch.
- Anything only Royce can prove (a real sign-in, a device, a customer-facing send) goes to the relevant repo's `eq/pending/<repo>.md` with a date — never left implied. `eq/pending.md` is split by repo since 2026-08-17 (its own index lists the files); use `cross-repo.md` for work genuinely spanning 2+ repos.

---

## 3. Maintainability under iterative agent edits

The failure mode is code that is individually correct and collectively incoherent.

- **Working before refactoring.** Never restructure while a bug is being fixed.
- **Match the change to the task.** A bug fix does not need surrounding cleanup; a one-shot operation does not need a helper. Three similar lines beat a premature abstraction.
- **No half-finished implementations**, and no backwards-compatibility shims for a state that never shipped.
- **Prefer a structural guard over a documented rule.** A rule an agent must remember is the weakest form of safety the substrate has — `system/failures.md` records prose failing twice on a lesson that was read the same session. Where a mistake can be made impossible (a helper that injects the filter, a check that fails the build), build that instead of writing the reminder.
- **One fact, one home.** Duplicating a fact into a second file creates two answers to the same question and no way to tell which drifted.

---

## 4. Multi-tenancy — the constraint agents violate most easily

Tenant isolation is the failure with the worst blast radius in this suite and the
least visible symptom: a missing filter returns *more* data, not an error.

- **`rules/non-negotiables.md` #11 is the hard rule** — every service-role or admin-client query carries an explicit tenant filter. RLS is not a backstop for these connections; it is bypassed entirely.
- The tenant id is resolved **server-side** — from the session JWT, the URL path, or an orchestration loop. Never from client-supplied JSON.
- Which project holds what, and why one-per-tenant: `system/architecture.md` (Control Layer + per-tenant model). Which project is live vs deleted: `rules/deployment.md`.
- The full defence-in-depth design — explicit filter, injecting wrapper, short-lived tenant-impersonation JWT so RLS still catches a bypass — is in `eq/field/multi-tenancy/plan.md` Step 2.5. Read it before writing a new edge function that touches tenant data.

---

## 5. Effort threshold

Match the machinery to the task. Parallelism is for preventing compounding errors,
not for looking thorough.

| Condition | Approach |
|---|---|
| 3+ repos touched, schema migration, or auth flow change | Multi-agent workflow (parallel) |
| Multi-file within one repo, or uncertain scope | Written plan → single agent |
| Single-file, clear scope | Direct execution |

Never reach for multi-agent orchestration on scale alone. Token budget is real.

---

## 6. Search hygiene

Do not search a whole workspace root — it sweeps archives, vendored code, and
`node_modules` across every repo. Scope to a named repo, or delegate to a
search-specialised agent.
