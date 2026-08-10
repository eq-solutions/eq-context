---
title: Infra redundancy — suite-wide single points of failure (scoping)
owner: Royce Milmlow
last_updated: 2026-08-11
scope: What can take the whole EQ suite down at once, outside the database-backup picture (dr-backups.md covers that separately). Scoping only — no fixes built here.
read_priority: high
status: live
---

# Infra redundancy — suite-wide single points of failure

Answers "what can go wrong, beyond DB loss, and can we build in contingencies" — asked
2026-08-11 after the redundancy-review parked item was found to only ever have covered
eq-cards' storage/worker-sync layer, never the suite as a whole. **Database/storage backup
is already solid and out of scope here** — see [`dr-backups.md`](dr-backups.md): 3 platform
DBs, daily offsite, verified nightly, restore-drilled quarterly (now on all three planes,
see [`restore-drill-eq-canonical.yml`](../.github/workflows/restore-drill-eq-canonical.yml)).
This doc is everything else that could take a live app down.

Live-verified 2026-08-11 (Netlify + Supabase MCP + code reads), not assumed. Five areas
checked; findings and honest gaps below.

---

## 1. Netlify — one account holds every app

**Confirmed:** all 10 sites — eq-shell, eq-service, eq-field, eq-cards, plus sks-nsw-labour,
eq-receipts, sks-comms, eq-core-design, life-tracking, knx-job-folder — sit under one
Netlify team (`Milmlow's team`, Pro plan, **1 member**, Royce as sole Owner). No secondary
owner exists.

**Real, confirmed SPOF.** Losing access to this one account (lockout, suspension, lost
2FA/recovery) takes down hosting **and every scheduled function** for all four production
apps at once. Each site is a single deploy target — Netlify's CDN is globally distributed
for already-built assets, but there's no second hosting provider standing by.

**Contingency options, not built:**
- Add a second team member (even read-only/billing-only) as an account-recovery path — cheapest, no engineering.
- Document a manual re-deploy path (static export → any other static host) as a break-glass procedure, not a live secondary.
- Accepted-risk option: Netlify's own account-recovery support process is the fallback, same as most small teams run.

## 2. Supabase — one org, one region, three single-instance projects

**Confirmed:** ehow/jvkn/zaap are all `ap-southeast-2`, Pro plan, one org
(`sqjyblkiqonyrdobaucn`), `ACTIVE_HEALTHY`. No read replica, no multi-AZ. PITR is off on
all three — already flagged in `dr-backups.md`'s own Follow-ups as inherited cost logic,
never independently re-confirmed at current scale.

**Real, confirmed SPOF**, same shape as Netlify: one org means an org-level incident or
account lockout affects all three platform DBs simultaneously. A region-level Supabase
outage in ap-southeast-2 would take Service, Field, Shell, and Cards' backend down together
— there's no multi-region failover on this tier.

**Contingency options, not built:**
- The PITR re-confirm already on file — cheapest lever, tightens Tier-1 RPO without an architecture change.
- Multi-AZ/HA add-on exists on Supabase's Team/Enterprise tier — real cost, not scoped here.
- Accepted-risk option: this is a small-team-scale tradeoff most orgs this size accept; the offsite R2 backup is the actual mitigation already built, not a live failover.

## 3. DNS / domain — one zone, one registrar, both unverified live

**Documented in `infrastructure.md`, not independently re-checked this pass** (no login
attempted): registrar = GoDaddy, DNS = Cloudflare (zone `eq.solutions`, proxied). Netlify's
own custom-domain config confirms `core./service./field./cards.eq.solutions` all resolve
through this path today.

**Real SPOF as documented, two layers:** a Cloudflare account issue takes every subdomain
offline at once (no secondary DNS host); a GoDaddy registrar issue (expiry, transfer,
suspension) is a second, independent SPOF underneath that.

**Not verified this pass:** current NS records, registrar-lock status, Cloudflare account
recovery/MFA posture. Worth an honest re-check rather than trusting `infrastructure.md`'s
age.

**Contingency options, not built:**
- Confirm registrar auto-renew + registrar-lock are both on — cheapest, prevents the single most common domain-loss cause (accidental expiry).
- Secondary DNS is a real architecture change (split-horizon or a second authoritative host) — not proportionate at this scale unless Cloudflare account hygiene is already tight.

## 4. Auth/identity — eq-shell + jvkn is a real cascading SPOF, confirmed in code

**Confirmed via `token-exchange.ts` + `IDENTITY-MODEL.md`:** every Field/Service session
mint goes through this one Netlify function querying `shell_control.users`/`tenants` on
jvkn. No fallback path — a DB query failure returns a hard 401/500. The one standalone
fallback that exists (Field's legacy PIN gate) is explicitly code-blocked for the SKS/core
tenant and only still live on the non-production demo tenant.

**This is the most consequential SPOF found.** If eq-shell (Netlify) or jvkn (Supabase) is
down, Field and Service both lose the ability to authenticate **new** sessions — by design,
not an oversight (the identity model deliberately centralizes on Shell). Already-minted
60-second JWTs simply expire and aren't renewable until Shell's back.

**Contingency options, not built — this is the one worth a real decision, not just hygiene:**
- Accept it as an explicit architectural tradeoff (single auth hub is also *why* the suite is coherent — the alternative is N separate auth systems, which is its own redundancy nightmare). Document it as accepted, not silently assumed.
- A genuine degraded-mode fallback (e.g. extend already-minted JWT lifetime automatically if token-exchange is unreachable) is real engineering, not a config change — would need its own scoping pass and touches the live auth path, so it's excluded under the current goal anyway.
- Cheapest real improvement: alerting. Is there a live monitor that pages if `token-exchange.ts` starts failing broadly? Not checked this pass — worth confirming before anything architectural.

## 5. Cron/background jobs — genuinely split across two providers already

**Confirmed, better than assumed:** not one scheduler. GitHub Actions runs the DB
backups/drills/digest refresh (eq-context); Netlify Scheduled Functions run
eq-solves-service's own crons (pre-visit briefs, supervisor digest, the canonical-outbox
drain, keep-warm). A GitHub Actions outage doesn't touch Service's crons and vice versa.

**Not a suite-wide SPOF** — each provider is only a SPOF for its own job set, which is
already the reasonable design. No action needed here; included for completeness since it
was one of the five things asked about.

---

## Bottom line

Two real, confirmed single points of failure worth a decision (not silent acceptance):
**#1 Netlify account has no recovery path** (cheap to fix — add a second team member) and
**#4 the auth hub cascades** (expensive to change, and arguably the right tradeoff — needs
a conscious "yes, accept this" not a shrug). #2 and #3 are standard small-team-scale
tradeoffs already partially mitigated by the backup work in `dr-backups.md`. #5 turned out
fine on inspection.

None of the fixes above are built. This is the scoping pass Royce asked for — the actual
build (if any) is a separate decision, and #4 in particular is a live/auth-adjacent change
that falls inside the current goal's exclusion while he's overseas.
