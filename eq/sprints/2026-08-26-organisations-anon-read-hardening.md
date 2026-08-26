---
title: Sprint — hardening after the 3rd organisations_anon_bootstrap_read regression
owner: Royce Milmlow
last_updated: 2026-08-26
scope: What's left after the 3rd organisations anon-read regression (eq-shell) — sequences 2 in-flight PRs from a concurrent session against what's genuinely still unbuilt, so nothing gets duplicated. Every item live-verified (gh pr view, git ls-remote, ListAgents) immediately before writing, not restated from pending.md.
read_priority: high
status: live
---

# Sprint — hardening after the 3rd organisations_anon_bootstrap_read regression

Triggered by Royce asking to turn this incident's outstanding items into a sprint, with
an explicit instruction to check what a concurrent session is already building first so
nothing gets duplicated.

**The short version: every item from this incident except one is now fixed and live.
The last one — a cross-repo consumer check — is unscoped and unbuilt, and that's the
only thing in here still actually worth calling "the sprint."**

---

## Already fixed — no action needed

| Item | Outcome |
|---|---|
| `organisations_anon_bootstrap_read` dropped a 3rd time (10:34 UTC, out-of-band via eq-cards PR #324) | Restored live, paper-trailed — [PR #1618](https://github.com/eq-solutions/eq-shell/pull/1618), merged |
| `CONTROL-PLANE-LEDGER.md`'s stale "confirmed live" claim on the 08-23 fix | Corrected — [PR #1622](https://github.com/eq-solutions/eq-shell/pull/1622), merged |
| CHECK 10 (`intentional_anon_reads`) wasn't wired to the auto-filed security issue — a schedule-caught drop never surfaced anywhere | Fixed — [PR #1623](https://github.com/eq-solutions/eq-shell/pull/1623), merged |
| CHECK 10's own verbose printer crashed on a real violation (bad `array_agg` handling) | Fixed, same PR — [#1623](https://github.com/eq-solutions/eq-shell/pull/1623), merged |
| Unrelated `eq_cards_admin_sync_tenant_access` drift blocking every merge repo-wide | Fixed — [PR #1629](https://github.com/eq-solutions/eq-shell/pull/1629), merged |
| Duplicate CHECK 10 fix sitting on branch `claude/check10-drift-printer-fix` | Resolved — branch no longer existed on origin |
| `0162`/`0163`/`0164` mis-attributed to an unidentified out-of-band actor | Corrected in the ledger — they're eq-cards' own tracked migrations (PR eq-cards#323/#324), not drift. The paper-trail files this PR originally added to *this* repo were removed as redundant once that was found — two repos independently claiming the same migration would have been actively wrong. [PR #1627](https://github.com/eq-solutions/eq-shell/pull/1627), merged (`02a9b405`) |
| `CHECK 12`/`13` — stacked-permissive-policy + RLS invariants ported to jvkn, directly motivated by this incident | Built and merged — [PR #1628](https://github.com/eq-solutions/eq-shell/pull/1628), merged (`ea3d649a`), stacked cleanly on #1627 once it landed (the migration files dropped out of #1628's own diff automatically — no rebase needed) |

`scripts/check-tenant-drift.mjs` is no longer being actively edited by anyone as of
these merges — the earlier "don't touch it" coordination note is stood down.

---

## The actual sprint — not started by anyone yet

### CHECK 11 — jvkn migration-identity (deferred by #1628 itself, not forgotten)

#1628's own PR body explicitly scopes this out: a `CHECK 11` mirroring `CHECK 3`
(tenant-plane migration-identity, which derives its expected-object list from
`tenant-migrations/*.sql`) needs a cutoff-date/strictness design call jvkn doesn't have
yet — jvkn's migrations tree has its own grandfather-cutoff precedent (2026-07-03, per
`check-tenant-drift.mjs`'s existing comments) that a jvkn-scoped version would need to
either reuse or deliberately diverge from. Whoever picks this up should read #1628's
reasoning first and coordinate rather than re-deriving the cutoff question from
scratch — it's the same file, same author's already-stated open question.

### The real gap: nothing stops another repo from re-breaking this

**This is the one item in this whole incident that isn't closed and isn't in flight.**
`CHECK 10`/`12`/`13` (once #1628 lands) all run inside eq-shell's own CI, against
eq-shell's own migration files. Nothing makes an **eq-cards** migration — the actual
source of all 3 regressions so far — check any of them before merging. Eq-cards' own
consumer-trace before PR #324 was thorough within eq-cards, and still missed EQ Field's
cross-repo dependency, because nothing in that process could see it. That's a structural
gap, not a diligence failure, and CHECK 12/13 don't touch it — they hard­en jvkn's
*state*, not who's allowed to *change* it from outside this repo.

Three shapes this could take, none built, none obviously right — **Royce's call, not
decided here:**

1. **Cross-repo CI call.** eq-cards' own migration-touching PRs call out to eq-shell's
   `check-tenant-drift.mjs` (or just CHECK 10/12/13) before merge. Catches it
   pre-merge, which is strictly better than catching it post-merge. Needs eq-cards' CI
   to reach eq-shell's script and jvkn credentials it may not currently have wired —
   real cross-repo CI coupling, not a small change.
2. **Shared package or reusable workflow.** Extract the positive-assertion checks into
   something every jvkn-touching repo (eq-shell, eq-cards, and whichever others end up
   writing to the control plane) pulls in as a required check of their own — a
   `workflow_call` reusable Action, or a small versioned npm package. Each repo already
   needs `SUPABASE_ACCESS_TOKEN`/`CONTROL_PROJECT_REF`-equivalent access to touch jvkn
   at all, so this doesn't add a new credential-sharing problem, just a shared-code
   one. Leans the same direction #1628 already leans (porting checks so the same
   reasoning travels with the code) — **the option this doc would lean toward if asked
   to pick**, but genuinely Royce's call given the setup cost.
3. **Don't prevent it — make it recoverable in minutes, not hours.** Trust the
   already-fixed 3-hourly schedule + auto-filed issue (#1623) as the safety net, and
   spend the effort on mean-time-to-recovery instead: a one-command restore runbook,
   maybe a Slack/PagerDuty ping on that filed issue rather than relying on someone
   noticing it in the GitHub Issues tab. Cheapest option, zero cross-repo engineering —
   but guarantees a 4th occurrence will still happen someday, just caught fast instead
   of slow.

Not attempting any of these unprompted — this is a real architecture decision with
cross-repo implications, not a mechanical fix.

---

## Summary

| # | Item | Status | Action |
|---|---|---|---|
| 1 | 3rd regression, ledger, CHECK 10's 2 bugs, unrelated drift block, duplicate branch | **All fixed** | Nothing |
| 2 | PR #1627 — ledger correction (0162/0163/0164 mis-attribution) | **Merged** (`02a9b405`) | Nothing |
| 3 | PR #1628 — CHECK 12/13 | **Merged** (`ea3d649a`) | Nothing |
| 4 | CHECK 11 — jvkn migration-identity | Scoped, not started | Needs the cutoff/strictness call #1628 already flagged — coordinate with its original author |
| 5 | Cross-repo consumer-check gap | Unscoped, not started | **Royce's call** — 3 options above, none built |

**What's actually left after this pass: exactly #4 and #5.** Everything else this
sprint originally scoped is closed.
