---
date: 2026-06-15
topic: Worker platform architecture — Cards as home, Core as employer-only, open decisions
status: in-progress
---

# Session prompt — Worker platform architecture

## Context

We had a long session today (eq-cards worktree) that started as a login bug fix for Luke Wheeler and ended with a significant architectural direction being locked. Two ADR entries and a design doc were written into eq-context today. This session is to continue that architectural conversation, challenge the direction, and identify what needs to be built or decided next.

## What was decided today

Read these before responding — they are the ground truth for this session:

- `ops/decisions.md` — two new entries at the top:
  - **2026-06-15 — Phone Identity Deduplication** (hook phone-fallback fix, Proposed, not yet built)
  - **2026-06-15 — Cards is the Worker-Facing EQ Platform; Core is Employer-Only** (Accepted)
- `eq/cards/worker-platform-direction-2026-06-15.md` — full design doc with three UX models and the chosen direction

Short version of what was decided:
- **Cards (`cards.eq.solutions`)** = the worker's mobile home. Wallet-first. Employer affiliations appear as tiles that link out to the employer portal.
- **Core (`core.eq.solutions` / Shell)** = employer-facing only. Admins, schedulers, managers.
- **Cards is never embedded in Shell as an iframe.** The iframe and handoff route are retired.
- **Two auth paths are correct:** employer via Shell HttpOnly cookie; worker via GoTrue phone OTP + `custom_access_token_hook`. Both backed by `shell_control.users`. Not a gap — an accepted model.
- **Long-term:** Field's worker-facing features (timesheets, availability, job assignments) migrate to Cards. Field/Shell retain the employer-admin view.

## What is NOT yet built

### 1. Tenant tile in Cards
The immediate UX bridge between Cards and Core/Field. A "Your workplace" section at the bottom of the wallet screen showing the worker's active employer tenants with a link-out to `shell_control.tenants.portal_url`.

Requires:
- DB: `ALTER TABLE shell_control.tenants ADD COLUMN IF NOT EXISTS portal_url text;` + seed `core.eq.solutions/sks` for SKS
- Cards Flutter UI: read `user_tenant_memberships`, render tile per non-personal tenant, tap opens system browser
- Shell: remove `CardsIframe.tsx`, replace Cards nav tile with external link to `cards.eq.solutions`

### 2. Phone dedup hook fix
`custom_access_token_hook` currently matches `shell_control.users` by UUID only. When a worker's `auth.users` row was pre-created via admin back-fill (different UUID, different phone format), a GoTrue phone OTP creates a duplicate account and the worker lands in the wrong tenant.

Occurred three times in five days: Royce (2026-06-10), SKS health check (2026-06-11), Luke Wheeler (2026-06-15). Each required a manual SQL patch.

The proposed fix is in `ops/decisions.md` (Option A — hook phone-fallback with adopt UPDATE). Not yet decided whether to build A or B (see open questions below).

### 3. IDENTITY-MODEL.md v2
The 2026-06-04 decision flagged this as a Phase 2 trigger. The model currently says "one sign-in at Shell → same identity across all EQ products." The two-auth-path decision (workers via Cards, employers via Shell) needs to be reflected explicitly. The v2 bump is a docs-only change but it unblocks the Phase 2 exchange bridge retirement.

### 4. Dead auth.users row cleanup (Luke Wheeler specifically)
`155ac75c` — the admin-back-filled GoTrue row with phone `+61499645997`. Never signed into. Shell_control row and membership row also exist for it. Should be pruned once the hook fix lands (the adopt UPDATE will make it truly orphaned). Not urgent.

## Open questions to work through in this session

### Q1: Hook fix Option A vs B

**Option A** (hook phone-fallback): Update `custom_access_token_hook` to try UUID lookup first, then phone match as fallback. On phone match with different UUID, run an adopt UPDATE in the hook (`shell_control.users.id` → new GoTrue UUID). Self-healing. One migration. SECURITY DEFINER, existing blast-radius controls apply.

**Option B** (no auth.users in back-fills): Strip `auth.users` creation from all admin import flows. Only `workers` + `shell_control.users` are back-filled. First real GoTrue OTP is the only thing that creates `auth.users`. The `notProvisioned` screen phone-matches against `shell_control.users` before offering personal wallet — if it finds a pre-existing shell row, it adopts it rather than provisioning a new personal wallet.

Which is the right call? A fixes the symptom structurally. B fixes the cause structurally but requires two changes. The 2026-06-04 decision's "avoid out-building the load" heuristic would suggest A first — it's one migration, closes the loop, lets B be a Phase 2 cleanup.

### Q2: Where does the tenant tile live in the Cards nav?

The wallet screen currently shows licences and certs. The design mock showed a "Your workplace" section below the wallet content. Does this belong:
- At the bottom of the existing wallet screen (fastest to build, may feel bolted-on)
- As a second tab or section ("Wallet" / "Work") — cleaner separation but more nav complexity
- Only surfaced when the worker has an active employer affiliation (hide entirely for personal-only workers)

### Q3: Is the Shell nav tile for Cards an external link or removed entirely?

Options:
- **Remove it** — workers don't use Shell, so the Cards tile in Shell nav serves no one
- **Keep it as external link** to `cards.eq.solutions` — useful for admins who want to see the worker-facing app, or for workers who somehow ended up in Shell
- **Repoint it** to the employer's licence-verification view (a Shell-native read of worker credentials) — this is the long-term correct answer but requires building that view

### Q4: Does the personal wallet concept survive the "Cards as home" direction?

Today, a worker with no employer affiliation gets a personal wallet. Under the new direction, Cards IS the worker's home regardless of employer status. The personal wallet is the default state — workers always have their wallet, employers are additive.

This is consistent, but it raises: should the `__personal__` tenant still be surfaced to the worker explicitly, or is it just the technical backing for the "no employer yet" state? Workers probably don't think of themselves as having a "personal tenant" — they just have their wallet.

### Q5: What triggers the tenant tile to appear?

Currently: a worker gets a `user_tenant_memberships` row for SKS when they claim their invite. That's the signal. But what about:
- Workers who were admin-back-filled but haven't claimed yet — do they see the tile?
- Workers who have left an employer — should the tile disappear, or remain greyed out?
- Workers with multiple employers (future state) — multiple tiles?

## Broader architecture questions to steelman

These are bigger than today's build but relevant to where this is heading:

**1. Cards absorbing Field worker features**
The long-term direction is timesheets, availability, and job assignments living in Cards. The data flow would be: Field/Shell writes to the canonical worker-house (`eq-canonical-internal`); Cards reads from it. This requires the canonical migration to be complete (worker data in worker-house, not just in the control plane). How far away is that, and should it inform the tenant tile design?

**2. The Intake layer**
EQ Intake is the parse/emit engine behind Cards. Its role in the "Cards as worker home" model: it should be the path for any employer pushing data TO the worker's canonical record (new job assignment, timesheet approval, licence expiry alert). Has this been designed? The intake flow exists for onboarding (claim, licence import) but not yet for ongoing employer→worker data push.

**3. Worker consent model**
The 2026-06-04 decision said "consent per employer — the worker approves each new employer membership, and the approval scopes what that employer sees." This is Phase 2 (deferred). Under the "Cards as home" model, it becomes more important: if an employer wants to see a worker's wallet, the worker needs to grant that from Cards. Where is that designed? Is there a Phase 2 doc?

**4. The SKS-specific vs platform-generic split**
Right now Cards is being tested with SKS as the one real tenant. Some of what's being built is genuinely platform-generic (personal wallet, tenant tile, two-auth-path). Some is SKS-specific (the manager role, the specific portal_url, the back-fill process). As the platform generalises to other employers, what changes and what stays the same?

## What NOT to relitigate

These are closed:
- Cards embedded in Shell as an iframe — closed, rejected
- Server-side GoTrue session creation from Shell — closed, rejected (ownership inversion)
- Cards' auth migrating to Shell's cookie model — closed, different stacks
- "One sign-in at Shell" applying to workers — closed, workers use Cards auth

## Tone for this session

Challenge everything. The direction is set but the implementation has a lot of open surface. If something in the ADR is wrong or in tension with another decision, say so — that's the point of this session. Refer to live state (Supabase, git, deployed apps) before making claims about what is or isn't built.
