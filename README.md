---
title: eq-context — Repository README
owner: Royce Milmlow
last_updated: 2026-08-30
scope: Human-readable entry point for the eq-context repository
read_priority: reference
status: live
---

# eq-context

Private context repository for EQ Solutions, SKS Technologies, and related entities —
used by any LLM assistant (Claude chat, Cowork, Code; Cursor; Codex; Perplexity;
ChatGPT; Gemini; future tools) to maintain continuity across sessions.

**Tier-separated as of 2026-05-04** — `/eq`, `/sks`, `/sks-team`, `/ops`, `/system`, `/archive`.
Sessions ask "EQ or SKS focus?" at the start so context loads cleanly.

**Entry points:**
- `CLAUDE.md` — master context (Claude Code auto-loads this)
- `AGENTS.md` — equivalent entry point for non-Claude tools
- `COWORK-PROMPT.md` — Cowork session starter (paste at start of each session)
- `system/md-style.md` — style guide for writing or updating any MD in this repo

## How it works

Every assistant conversation that produces new knowledge, decisions, or state changes
ends with "update the MD". The assistant commits only the files that changed, with a
clear commit message describing what was added. Once pushed to `main`, the change is
live: the repo is public, so assistants read these files directly from it via raw URLs
(`https://raw.githubusercontent.com/eq-solutions/eq-context/main/<path>`). A merged
commit is the deliverable — there is no separate cache to sync.

## Structure

```
CLAUDE.md                    ← Master index — assistants read this first, always
AGENTS.md                    ← Tool-neutral equivalent entry point
COWORK-PROMPT.md             ← Cowork session starter
CHAT-PROMPT.md               ← Claude Chat session starter
README.md                    ← This file (human-focused)
digest.md                    ← Push-style health feed — read every session, all tiers
suite-state.md                ← Full nightly-refreshed suite snapshot

rules/
  non-negotiables.md         ← Hard rules that override everything
  brand-eq.md                ← EQ colours, fonts, logo rules (Design Brief v1.3)
  brand-sks.md                ← SKS colours, fonts, logo rules
  brand-check.md              ← Final-gate brand checklist for outputs
  deployment.md              ← Deployment guardrails
  stack.md                   ← Default technology stack

eq/                          ← EQ Solutions tier
  README.md                  ← EQ tier index
  pending.md                 ← EQ-only to-do list
  products.md                ← EQ live products (Field, Service)
  field/
    multi-tenancy/           ← MT plan + explainer (active reference)
    permissions/             ← Role/permission matrix
  changelog/
    eq-field.md              ← EQ Field history
    eq-context.md            ← Substrate self-changelog

sks/                         ← SKS Technologies tier
  README.md                  ← SKS tier index
  pending.md                 ← SKS-only to-do list
  products.md                ← SKS live products (Labour, Receipt Tracker)
  active.md                  ← Rolling active projects
  team.md                    ← NSW team
  templates.md               ← Quote v3 + client context blocks
  changelog/
    labour.md                ← SKS Labour app history

sks-team/                    ← SKS team-facing AI guidance (different audience)
  README.md                  ← SKS-team tier index + rules of the tier
  quoting.md                 ← Canonical router for SKS team quoting

ops/                         ← Operational support
  README.md                  ← OPS tier index
  pending.md                 ← Webb, infra, substrate-discipline items
  entities.md                ← Entity register, accounts, registrations
  decisions.md               ← Append-only decisions (ADR format)
  financial-architecture.md  ← AHD, Delta cliff, CDC PSI

system/                      ← Substrate itself
  README.md                  ← System tier index
  architecture.md            ← Tech architecture (Cloudflare, Supabase)
  infrastructure.md          ← Project IDs, accounts, Beelink
  lessons.md                 ← Tech gotchas (append-only)
  md-style.md                ← MD writing standard (slimmed)
  onboarding.md              ← First-time tutorial

archive/                     ← Parked or deferred — not loaded by default
  README.md                  ← What's in here and why
  changelog-eq-quotes.md     ← EQ Quotes (deferred 6mo)
  changelog-ahd.md           ← AHD (parked to 2027)

sessions/
  YYYY-MM-DD.md              ← Append-only daily logs
  archive/                   ← Older than 30 days

scripts/
  install-hooks.ps1          ← Pre-commit hook installer

.github/workflows/            ← 22 workflows, 20 scheduled (counted 2026-08-15) — no GitHub→Supabase
                                 sync (that path was retired 2026-06-22, see
                                 CLAUDE.md §1). Key ones: digest-refresh.yml +
                                 suite-state-refresh.yml (nightly substrate
                                 regen), claim-expiry.yml + guard-ratchet.yml +
                                 substrate-honesty.yml + index-drift.yml +
                                 frontmatter-check.yml + md-health.yml (CI
                                 gates), backup-*.yml + verify-backup-*.yml
                                 (offsite DR)

hooks/                        ← Session-start/pre-tool-use guards (Python) —
                                 see hooks/README.md
.claude/                      ← Claude Code project config + worktrees
.githooks/                    ← Git-level hooks (installed via scripts/install-hooks.ps1)
supabase/                     ← Local Supabase CLI config, if used
AUTONOMOUS-SPRINT-RULES.md    ← Diverge-proof conventions from the 2026-05-30
                                 sprint — coordination mode retired, conventions
                                 still cited as the origin of the ground-truth-
                                 before-trust rule
```

## Root scratch docs

A number of one-off working docs — sprint plans, audits, runbooks — accumulate
directly at repo root rather than in a tier folder, because they were written
for a single dated piece of work rather than as living substrate. They're not
indexed individually above; this section exists so `scripts/index_drift.py`
has somewhere to point and so they're not simply invisible.

**Archival pass done 2026-07-20** — each of the 22 files previously listed
here was checked individually (read in full, cross-referenced against every
live pointer doc, not just guessed from date) rather than assumed from "most
predate 2026-06-08." 15 were genuinely done and moved into `archive/` (see
`archive/README.md`); the 4 below are still cited as live by something
current and stay at root until whatever cites them is itself resolved.

> **⚠ Re-verified 2026-08-15. This list is NOT a delete list.** The pass that
> wrote it (2026-07-20) was careful and correct on the day; four weeks later
> **four of its nine justifications were false** and five of the nine files
> were archivable. The structural cause: several justifications were anchored
> to `digest.md`, which regenerates nightly, so a hand-written claim about what
> it "still points to" decays silently while continuing to read as verified.
> The count also said "7" over nine entries.
>
> Five were archived 2026-08-15 with per-file evidence in `archive/README.md`:
> `field-feature-backlog-2026-05-30` (zero live citers),
> `access-model-cluster1-build-plan-2026-07-16` and
> `dashboard-signals-build-plan-2026-07-16` (both shipped),
> `eq-secret-salt-rotation-runbook-2026-06-06` and
> `auth-phase4-hmac-retirement-runbook` (both superseded records — note
> `EQ_SECRET_SALT` is still live and Phase 4's salt-retirement half was never
> executed).
>
> **Re-check the citation before acting on any line below.** A justification
> nobody re-derives is worse than none, because it reads as checked.

> **Re-verified 2026-08-30 — all 6 hold, 0 archived this pass.** Different
> result from both prior passes (2026-07-20 archived 15/22, 2026-08-15
> archived 5/9 and found 4 more justifications false) — not because this pass
> was less thorough, but because these particular 6 files' citations turned
> out to be genuinely live, several confirmed against stronger evidence than
> existed before (see per-file notes below). The discipline this section
> exists to enforce only shows up as an archive count when there's something
> to archive; a clean re-check that finds nothing wrong is still the point.
> One process note while re-checking `scripts/prune_ratchet.py`: its
> `root_files` ceiling is still 16 in this checkout (`origin/main`), not 19 —
> the ceiling-raise lives on PR #185 (`claude/substrate-housekeeping-issues-
> 8b9116`), which is open, not merged. Running the script against current
> `main` therefore fails on root_files (19 > 16) regardless of this pass's
> own result; that's pre-existing, resolves whenever #185 merges, and this
> pass doesn't change the root-file count either way (0 archived).

`SKS-CUTOVER-CRITICAL-PATH.md` — cited by `eq/pending.md` as the current
pre-cutover state; Phases A–C not yet started. **Re-verified 2026-08-30,
strongest evidence yet:** `sks/active.md` (last_updated 2026-08-24, 6 days old)
names this file directly as the current SKS Labour retirement plan ("SKS
Labour tracking — being retired, see `SKS-CUTOVER-CRITICAL-PATH.md`"). Phases
A–C still not started in the data — no `field_*` schema exists on the SKS
tenant; confirmed by its own companion log below.
`cross-app-linkage-remediation-plan-2026-06-07.md` — **justification corrected
2026-08-15.** It claimed `digest.md` "still points to its §7a"; `digest.md` has
zero matches for `cross-app-linkage`. The real live dependency is
`sks/pending.md` (an open, SKS-live-gated item). Note the file self-declares
`status: archived` in its own frontmatter while sitting at root — the only root
file in that state. **Re-verified 2026-08-30: citation still holds** —
`sks/pending.md`'s §7a item (SKS anon-remediation on `nspb`) is still an
unchecked `- [ ]`, still SKS-live gated; nothing in `sessions/` since records
it being executed (it would need a live Supabase DDL change under an explicit
"SKS live" instruction — a rare, deliberate, loud action, not something that
happens quietly). The self-declared `status: archived` frontmatter anomaly
also still stands, unresolved — noting it again rather than silently fixing
it, since that's a one-line edit outside this pass's actual scope.
`eq-platform-verified-state-2026-06-03.md` — **justification corrected
2026-08-15.** It claimed the file is "named explicitly in this repo's own
`CLAUDE.md`"; grep returns zero. The real citer is `C:\Projects\CLAUDE.md`, the
umbrella file that is **not in this repo** and self-describes as invisible to
every tool except a session rooted there. Keep the file; the reason was wrong.
**Re-verified 2026-08-30, directly:** the umbrella `C:\Projects\CLAUDE.md` was
read live at this session's own start (Rule 0.5) and still reads "Start from
`eq-context/eq-platform-verified-state-2026-06-03.md` (a DB-verified
snapshot), then re-verify against live." Strongest form of confirmation
available — the citation was observed directly this session, not inferred
from grepping a doc that could itself be stale.
`sks-live-sprint-2026-06-07.md` — **justification corrected 2026-08-15.** It
claimed `digest.md` "still lists its Security Groups Phase 2–5 work as open";
`digest.md` has zero matches for `sks-live-sprint`. `eq/pending.md` does keep
Phase 4 open, but flags it as possibly superseded by the access-model cluster
work, and `shell_control.user_security_groups` has been 0 rows for 50+ days.
Still-wanted-or-superseded is Royce's call, not an archival one. **Re-verified
2026-08-30: citation technically still open, but the decision has now gone
unanswered even longer.** `eq/pending/eq-shell.md`'s Phase 4 line (the item
moved here in the 2026-08-17 pending split) is unchanged since 2026-07-27 — 34
days on the same unresolved either/or. More telling: the fresh 2026-08-28
whole-suite sweep (`sprint-2026-08-28-outstanding-items.md`, 9 agents reading
all 11 `eq/pending/*.md` files live) doesn't mention this item at all, open or
closed — it's fallen out of the active queue without being built or killed. A
live re-check of the row count was attempted this pass and blocked by the
session's own tool-safety classifier; doesn't change the call — the citation
rests on the unresolved decision, not the exact count. Worth Royce settling
explicitly so this stops silently aging.
`SKS-FIELD-PARALLEL-RUN-LOG.md` — the EQ Field parallel-run mismatch log +
clean-week counter the 2026-07-11 cutover plan requires; live, streak at 0.
**Re-verified 2026-08-30: still live and current** — the file's own most
recent entry (2026-08-17) postdates this pass's prior baseline, and
`sks/active.md` (2026-08-24) names it directly as the current tracking file.
Clean-week streak still 0; the file's own honest diagnosis (entry activity
bursts, then stalls — twice now) is unchanged.
`sec9-jvkn-key-rotation-runbook-2026-07-27.md` — ready-to-run SEC-9 rotation
runbook, Royce-gated; stays at root until the key is rotated. **Re-verified
2026-08-30 directly against the register row itself (not a secondary
pointer) — still open, on stronger evidence than before.**
`ops/security-register.md`'s SEC-9 row **Status** column reads **OPEN** as of
its own latest (2026-08-16) entry; that entry closed a related-but-separate
sub-issue (a `dev`-context masking leak across 17 vars), not the underlying
jvkn key rotation — Royce's 2026-08-01 call was to defer the rotation itself
as low-urgency, "whenever convenient." The newer, more specific
`ops/sec9-sec24-netlify-manual-fix-runbook-2026-08-11.md` explicitly names
this exact file as "the real fix for that part, whenever you pick a window."
**Correction to a nearby doc, for the record:** `sprint-2026-08-28-outstanding
-items.md` flagged (correctly hedged, not asserted as fact) that SEC-9
"almost certainly" already closed, reasoning from the register showing no
open P0 entry under that number — that reads the severity column's
strikethrough, not the Status column, which is unambiguous. Direct read this
pass confirms: still open.

The 2 that pass deferred as "too recent to judge" —
`access-model-cluster1-build-plan-2026-07-16.md` and
`dashboard-signals-build-plan-2026-07-16.md` — **were checked 2026-08-15 and
both archived.** Recency was the wrong test: both had already shipped on the
day they were written (PR #885 and PR #886 respectively), so being recent made
them *more* likely to be spent, not less. Deferring on age rather than on
status is what left them at root for a month.

**Added since the 2026-08-15 pass, not yet subject to it** — landed as
`index-drift.yml` orphans (fixed 2026-08-30, itself a substrate-housekeeping
pass) rather than through the archival cadence above:

`sprint-2026-08-28-outstanding-items.md` — whole-suite pending sweep (~180
items across all 11 repo logs + security-register + failures.md), organised
by what each item is blocked on since no `TODAY.md` goal exists to
prioritise against.
`sprint-2026-08-28-security-hardening.md` — the security-shaped slice of the
outstanding-items sweep above, scoped via `/decide`; jvkn/ehow/zaap grant+RLS
cleanup and eq-shell's own app-code security gaps.
`sprint-2026-08-28-worktree-followups.md` — the "needs you" follow-ups left
after the 2026-08-28 eq-field worktree audit (19 of 24 worktrees cleaned up;
full trail in `system/worktree-registry.md`).

## Update frequency

| File / folder | How often |
|---|---|
| `CLAUDE.md`, `AGENTS.md` | Only when structure or rules change |
| `rules/*` | Rarely — annual review (28 April) |
| `*/pending.md` | Every session in the relevant tier |
| `*/products.md` | When product status changes |
| `sks-team/*` | Rarely — only when canonical language or template references change. Single writer (Royce). |
| `ops/entities.md` | When entity/infrastructure changes |
| `system/architecture.md` | When how something is built changes |
| `ops/decisions.md` | Append when a decision is made |
| `system/lessons.md` | Append when a lesson is learned |
| `*/changelog/*.md` | Append when product code is touched |
| `sessions/*` | Every session (new file per ISO date) |
| `archive/*` | Almost never — only on reactivation |

## Never do

- Edit main branch directly for large changes — use a session update workflow
- Delete old session logs — they are the audit trail
- Merge state and rules — they have different update frequencies for a reason
- Cross-pollute tiers — EQ context goes in `/eq`, SKS in `/sks`. Don't mix.
- Reference parked products as live — see `eq/products.md` "Killed / Deferred"
  section (CLAUDE.md §9 is a pointer only, as of 2026-07-19 — don't restate
  facts there, that's the exact bug this rule exists to prevent)
  
