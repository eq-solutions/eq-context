---
title: EQ — Internal Document Sign-off Register (Sprint — Harden Before Rollout)
owner: Royce Milmlow
last_updated: 2026-08-04
scope: Close the gaps between the current pilot and a genuinely working version, before widening past a one-person test. Companion to internal-signoff-register-design-2026-08-01.md.
read_priority: reference
status: live
---

# Sprint — Document Sign-off Register: Harden Before Rollout

## Where this starts (2026-08-04)

Live on core.eq.solutions: upload (PDF/Word/Excel/image) → push to a role/crew/person → real drawn-signature sign-off → register + evidence view (signature, content hash, file link) → sign-off certificate PDF, generated live → template documents (no sign-off required). One real document has gone through it end to end, signed by one real person — Royce.

## Priority call (Royce, 2026-08-04)

Proving this works with a real second person is explicitly **lower priority right now** — this sprint hardens the feature itself first. Rollout is the last task, not the first.

---

## T1 — Scope `document_signoffs` so a signer can only touch their own row (~30 min)

**Repo:** eq-shell (tenant-migration, both ehow + zaap)

**Problem:** the live RLS policy (`document_signoffs_tenant`, migration 0233) is a single `FOR ALL` policy scoped only to tenant — any signed-in tenant member can read *and overwrite* any other signer's row, not just their own. Harmless with one real row in the whole table today; becomes a real integrity gap the moment a second signer exists — the entire point of this feature is an authentic per-person record.

**Fix:** split into per-operation policies:
- SELECT — stays tenant-wide (the register and certificate both need to show every signer's status to an admin).
- INSERT — stays tenant-wide, interim (the push flow has no `documents.*` permission yet — that's T4 below, not this task).
- UPDATE — scoped to the signer's own row only, so nobody else can write someone else's status, timestamp, or signature image.

**Acceptance:** a second tenant member's session cannot UPDATE a row where they aren't the signer; the existing self-sign flow is unaffected; register/certificate reads unaffected.

**Attempted 2026-08-04 — blocked, not a migration.** Verification (required before writing the fix, per this task's own brief) found `signer_user_id = auth.uid()` would break real signing, not scope it: eq-field's data-plane JWT hardcodes `sub` to the tenant id for every user (`verify-pin.js:654`, comment: *"cast-safe in RLS... NOT the actor"*), so `auth.uid()` on the real sign path never equals `signer_user_id`. Closing this gap for real is an identity-model change to how that JWT carries identity — auth-adjacent, needs Royce's explicit direction on which of several real tradeoffs to take, not something to pick unilaterally. No migration written, nothing committed. Revisit alongside T5 (rollout) rather than as a standalone schema task.

**Royce's call (2026-08-04): leave deferred.** Consistent with T5 also being lower priority right now — no urgency to pick an identity-model direction while there's no second real signer.

---

## T2 — Reminder/chase mechanism — DONE (2026-08-04)

**Repo:** eq-shell

**Problem:** an outstanding sign-off is invisible unless someone opens the Register tab and looks — no nudge, no chase. Flagged repeatedly across this build; never scoped.

**Shipped:** daily scheduled function (Netlify `config.schedule`, 22:00 UTC / ~8am AEST), loops every active tenant, emails anyone with a `document_signoffs` row outstanding past the cadence, using the existing `reminder_count`/`last_reminded_at` columns for dedup. PR [#1226](https://github.com/eq-solutions/eq-shell/pull/1226) shipped it at 3-days-first / 4-days-repeat; Royce asked for a uniform weekly cadence same day, PR [#1228](https://github.com/eq-solutions/eq-shell/pull/1228) changed both constants to 7 days. Both merged, CI green, live.

**Not yet proven live:** the mechanism has never actually fired. The one real signoff (Environmental Management Plan, ehow) was assigned 08:56:58 and signed 08:57:14 UTC on 2026-08-03 — 16 seconds later — so no row has ever sat outstanding long enough to trigger it, on the old cadence or the new one. Code-reviewed sound, functionally unexercised.

---

## T3 — Templates: bulk upload (optional — only if one-at-a-time is actually annoying)

**Repo:** eq-shell

**Status today:** the Templates tab is live (shipped 2026-08-03, PR #1222). Nothing engineering-side blocks saving the 15 SKS DB Schedule files right now — one at a time, through the existing upload form, Type = Template. That upload has to be Royce; it needs a live login, same as every other click-through item already on his plate.

**If worth building:** a multi-file picker that loops the existing `upload-document-version` call per file (title defaulting to the filename), so 15 files is one action instead of 15. Small — similar shape/effort to the certificate + templates work just shipped.

**Not included unless asked for** — flag back if the one-by-one flow turns out to be genuinely annoying enough to be worth it.

---

## T4 — Interim permission gate (`documents.*` in `@eq-solutions/roles`) — later

**Repo:** eq-roles, eq-shell

**Status:** any authenticated tenant member can currently upload, push, and see everything — an explicit, accepted interim decision made throughout this whole build, not an oversight. Matters once this is used by more than Royce; per the priority call above, that's later.

**Not scheduled this sprint** — listed so it isn't forgotten, not because anything today is blocking on it.

---

## T5 — Roll out past the one-person pilot — last

**Repo:** n/a — usage, not code.

**What:** push one real document to one real second person; get them to sign it on their own phone.

**Depends on:** ideally T1 landed first — a second signer's row should be protected before it exists.

This is the "proving it works" step Royce explicitly said should be lower on the list — parked here on purpose, not dropped.

---

## Dependency order

```
T1 (RLS)               — independent, do first (integrity precondition for T5)
T2 (reminder scoping)  — independent
T3 (bulk template upload) — independent, optional
T4 (permission gate)   — independent, deferred
T5 (real rollout)      — last; ideally after T1
```

## Done definition

"Working version" = T1 shipped, and T2 either built or consciously deferred with a real reason — not forgotten. T3 / T4 / T5 are judgement calls, not blockers.
