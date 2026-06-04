---
title: OPS — Decisions Log
owner: Royce Milmlow
last_updated: 2026-06-03
scope: Append-only log of key decisions across all tiers and the reasoning at the time
read_priority: standard
status: live
---

# OPS — Decisions Log

Append-only log. Key decisions and the reasoning behind them — reasoning
disappears faster than outcomes, which is why this file is the most
important one to maintain.

Format: Status → Decision → Why → Alternatives considered → Implications.
Status values: Accepted | Superseded by [date+title] | On Hold | Deprecated | Proposed.
Append-only — never delete an entry. Supersede or deprecate it instead.
For the current built state of each system, see [system/architecture.md](https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/system/architecture.md).

---

## 2026-06-04 — Low-Friction Onboarding & Portable Worker Identity (Cards-first)

**Status:** Accepted (direction authorised by Royce 2026-06-04). Implementation **phased**; Phases 2–3 trigger a deliberate v2 bump of `eq/identity/IDENTITY-MODEL.md`. Full design: [eq/identity/onboarding-portable-identity-2026-06-04.md](https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/eq/identity/onboarding-portable-identity-2026-06-04.md).

**Decision:** EQ optimises for **lowest friction *above a necessary floor*** (the floor is set by the sensitive payload — licences, right-to-work, PII), not friction-zero. The onboarding model: (1) **Portable identity** — one human = one identity with many tenant memberships; a tradie logs into the *same* EQ Cards across employers (pulls `IDENTITY-MODEL.md` §11.2 multi-tenant-membership forward from v2 backlog; `shell_control.user_tenant_memberships` already exists live). (2) **Decouple authorisation from login convenience** — the admin-issued **claim code** is the high-assurance authorisation event; **phone** is the repeatable convenience credential; **email is an optional recovery channel, not a login requirement**. (3) **Consent per employer** — the worker approves each new employer membership, and the approval scopes what that employer sees. (4) **Force email by *event, not timer*** — never hard-block showing a card; hard-require recovery email only at risk events (phone change, 2nd employer, export); the "14-day wall" is rejected. (5) **Lifecycle policy lives in the control layer** — rules + state in `shell_control`; the **Shell evaluates and projects verdict flags into the JWT via `custom_access_token_hook`**; apps react read-only and never hardcode policy; genuine gates are also server-enforced (RLS/RPC), UI walls are nags.

**Why:** Royce's goal is lowest barrier to entry for tradies (who won't self-serve data entry or remember passwords). Steelman/critique converged on: the friction win is real for *login*, but "lowest possible" ignores recovery, identity-assurance, and SMS-dependency costs that compound at scale. Portability is the right end-state for labour hire (mobility is the point) and resolves *in favour* of phone-as-personal-anchor — while *raising* the assurance floor (a recycled number now exposes cross-employer PII). Putting policy in the control layer is what makes "one portable identity, consistent rules across Cards/Field/Service" true instead of aspirational, and stops each app re-deriving lifecycle logic.

**Alternatives considered:**
- *Per-employer record (window model).* Rejected — same tradie re-onboards every gig, double data entry; structurally wrong for labour hire.
- *Friction-zero (phone-only, no recovery anchor).* Rejected — lost SIM = locked out of sensitive records; phone is a weak uniqueness key for a sensitive, portable identity.
- *Time-based forcing (14-day wall).* Rejected — lands at random/worst moments, manufactures churn; event-based forcing converts on self-evident value.
- *Lifecycle policy per-app (or hardcoded in Cards).* Rejected — drift across the suite; re-litigated per app; the exact failure the control-plane model removes.
- *Build the full model before pilot.* Rejected — out-builds the load; instead: right schema now (Phase 1 thin slice), enforcement engine later (Phases 2–3).

**Implications:**
- **Phased build:** Phase 1 thin slice (phone-OTP + claim + optional recovery-email, state in `shell_control`); Phase 2 enable `custom_access_token_hook` + retire per-method shell-exchange bridges + control-plane policy (= v2 `IDENTITY-MODEL.md` bump); Phase 3 consent-scoping + event-forcing + recovery flow + server-enforced gates.
- **Three open problems to design deliberately, not assume:** (a) identity-resolution / same-human matching beyond the weak phone key; (b) the recovery flow (now a *platform* responsibility under portability); (c) **GoTrue-vs-own-mint reconciliation** — `IDENTITY-MODEL.md` §9 says "not Supabase-Auth-managed", but Cards' phone-OTP uses GoTrue as an OTP transport then swaps for a shell-minted JWT; must be reconciled before Phase 2 because the token hook runs in GoTrue's mint path. Docs lag reality — verify live first.
- **Reachability:** new design doc linked from `IDENTITY-MODEL.md` Related + this entry (per the 2026-05-19 full-link substrate rule).
- **Does not change** the live IDENTITY-MODEL.md yet — that is a deliberate v2 version bump applied when Phase 2 lands, not a silent edit. Related memory: `product_adoption_strategy`, `eq_phone_otp_login_wiring`.

---

## 2026-06-02 — Multi-Tenant Operating Model: Uniform Schema, Per-Tenant Data, Generic Spine

**Status:** Accepted (authorised by Royce 2026-06-02)

**Decision:** Every tenant Supabase gets the SAME full uniform canonical schema (all ~55 `app_data` tables). A tenant simply doesn't *use* the parts that don't apply — carrying unused tables/columns costs effectively nothing (storage, perf, RLS all negligible, and *easier* when uniform). This is what makes the core capability real: build an app once, ship one migration, and every tenant automatically gets the new version pointed at its own data; provisioning a new tenant is "clone the standard." Per-tenant variation is the RARE exception via extension columns/namespaces — never by diverging the standard schema. The one hard discipline: the 6 spine entities (sites, staff, customers, assets, contacts, licences) + 3 structural columns (tenant_id, intake_id, external_id) keep GENERIC semantics — never bake one tenant's meaning into a shared spine field; tenant-specific meaning lives in extensions. See `eq/canonical-readiness/spine.md`.

**Why:** Royce, 2026-06-02 — "building apps together and tenants automatically getting the new version that talks to their own info appeals to me; does it really matter if the tenant Supabase has info the tenant doesn't use?" It doesn't. Uniformity is the enabler of one-codebase-ship-once + trivial provisioning. The earlier "6 align, 49 free to vary" framing was corrected: divergence breaks ship-once, so uniformity is the default and divergence the exception. Drift trends to zero by design.

**Alternatives considered:**
- Per-tenant tailored schemas (rejected — breaks ship-once + auto-upgrade; bespoke provisioning; operational nightmare).
- Minimal per-tenant schema, add tables only when used (rejected — fragments the fleet, reintroduces drift, complicates migrations for marginal storage savings).

**Implications:** Migrations apply identically to all tenants; the drift guard enforces structural identity, not just spine. New-app rollout = one migration + mount the module in Shell. Anti-over-fit guardrail folds in: spine stays general even with one real tenant (SKS). Related: 2026-06-02 gate-kill entry below; memory `project_canonical_spine_map`, `project_eq_north_star_vision`.

---

## 2026-06-02 — GTM Validation Gate Killed (Build For Ourselves)

**Status:** Accepted (authorised by Royce 2026-06-02)

**Decision:** The "5 outside-SKS trade subbies validate Field" GTM validation gate is dead, permanently. EQ is built for ourselves (SKS NSW) because it's a good product. No EQ work — Shell Phase 2, new modules, canonical, anything — is gated on outside-customer validation. Build sequencing is by the **trust ladder** (coherence → surfacing → ask-anything → gating; see memory `project_eq_north_star_vision`) + Royce's go. Stale gate language was purged from the forward docs (`eq/README.md`, `eq/products.md`, `eq/pending.md`); historical records (sessions, archive, changelog, the EXECUTED `canonical-readiness/plan.md`) keep their gate references as point-in-time record.

**Why:** Royce, 2026-06-02: "anything that mentioned 5 outside subbies — this needs to go. We are building for ourselves because it's a good product, end of story." The gate was first removed in direction on 2026-05-30 but never cleaned out of the forward docs, so every audit kept re-surfacing it as live. EQ's value is the integrated per-tenant canonical store + an AI ask-anything layer for SKS itself; gating substrate work behind external validation is a chicken-and-egg trap the canonical-readiness plan already flagged.

**Alternatives considered:**
- Keep the gate (rejected — Royce killed it; building for ourselves is the axiom).
- Soft gate / build-but-don't-cutover (rejected — no outside dependency at all; cutover is Royce's own-merits call).

**Implications:** Roadmap sequences purely on the trust ladder + Royce's go. `STATE.md` already reflects gate-free reality. Supersedes the gate framing in the 2026-05-20 part-d session and any earlier "EQ GTM PRIORITY" entries. Related memory: `project_eq_north_star_vision`, `feedback_royce_is_the_user`.

---

## 2026-06-02 — EQ Tech Bets: PowerSync for Offline, Semantic-Layer/MCP for the Agent, Never Text-to-SQL

**Status:** Accepted (authorised by Royce 2026-06-02)

**Decision:** Lock three standing technology choices for the EQ core platform, validated by adversarially-verified external research (2025–2026 sources; 19 of 25 claims survived 3-vote verification). These ratify existing direction with evidence — they do **not** introduce new build scope.

1. **Offline / local-first → PowerSync** (when EQ Field needs offline). PowerSync mirrors the canonical Supabase Postgres into a per-device SQLite DB (WAL replication down, upload queue up) — true offline reads *and* writes for field workers who lose signal. **ElectricSQL is rejected** for this: it does read-path sync only ("Electric does not do write-path sync") and pushes the write path onto us as a DIY concern.
2. **Agent-over-canonical → semantic layer + typed tools over MCP, with Postgres RLS + column masking enforced at the data layer. Raw / fine-tuned text-to-SQL is banned.** Semantic layers are both more accurate and *fail safe* (explicit error vs silent wrong answer). Fine-tuned text-to-SQL is a security liability (ToxicSQL: 0.44% data poisoning → 79% malicious-SQL rate; 100% evasion of static SQL filters). The agent starts **read + recommend; writes (dispatch, status changes) are human-confirmed** until reliability is proven on SKS's own data.
3. **The moat is the data model + workflow lock-in + compliance depth — not the app code.** Agentic coding has commoditised code (the "Clone Test": if a clone with your team, codebase and frontier models could outcompete you, code is not the moat). For a regulated trade, the defensive moat (licences, certifications, shutdown safety, compliance sign-off) is exactly the hardest-to-clone layer. The cross-customer "data network effect" is contested/over-claimed — **not** banked on while SKS-first.

**Why:** Royce asked for a steelman on direction, best available tech, and where AI is heading, then to document it. The research confirmed the existing strategy rather than redirecting it: the clean canonical Supabase data model already named as the core asset is precisely where 2026 literature says defensibility sits. Recording the three tech choices removes future decision points (which sync engine, how to expose the agent, where the moat lives) and stops them being re-litigated per app.

**Alternatives considered:**
- *ElectricSQL for offline.* Rejected — read-path only; an n=1 practitioner shipped on it for ~2 months then abandoned the push mechanism. Architecture fit for our offline-write case is wrong.
- *Fine-tuned text-to-SQL over canonical.* Rejected — backdoorable, evades static validation, fails silently. Wrong risk profile for a multi-tenant operational DB feeding dispatch/compliance decisions.
- *Treat the apps/features as the moat.* Rejected — commoditised by agentic coding; the durable asset is the spine + workflow embedding + compliance.
- *Build the agent layer now.* Rejected (Royce) — it is documented intent, not active scope. It waits behind the EQ Field B5 cutover; the only thing consuming build hours is getting Field live.

**Implications:**
- Roadmap order unchanged: (1) EQ Field → B5 → daily SKS use; (2) freeze/protect the canonical spine; (3) agent-over-canonical spike (semantic + MCP + RLS, read-only first); (+) PowerSync offline deferred behind Field-live.
- When offline work begins, the open question to resolve first is **conflict resolution on shared operational records** (two techs editing the same dispatch offline) — not the sync transport, which is solved.
- The agent's access model reuses the canonical role registry (`@eq-solutions/roles`) and Supabase RLS — it inherits the user's access, never a broader grant.
- Does not touch auth or SKS live — unaffected by `AUTONOMOUS-SPRINT-RULES.md` §0/§1. No new product surfaces created; Ops/Expenses remain culled per §9.
- Source caveats: sync evidence leans on vendor docs + one practitioner blog (superlative maturity claims were refuted); the semantic-layer accuracy figures are a small vendor benchmark (directional); moat sources are VC thesis pieces (the broad consensus holds, the data-network-effect sub-claim does not). Treat verdicts as well-grounded, exact figures as indicative.

---

## 2026-05-31 — EQ Design System: Tokens Everywhere, Components Per-Stack, Pin Never Vendor

**Status:** Accepted (authorised by Royce 2026-05-31)

**Decision:** Formalise the EQ design-system model the One Spine sprint (2026-05-30) built ad hoc. Three standing rules: (1) **Tokens are the single cross-stack source of truth** — `@eq-solutions/tokens` (one JSON → CSS / TS / Tailwind preset / Dart) is consumed by every surface regardless of stack. (2) **Shared components are per-stack** — `@eq-solutions/ui` (React) for Shell + Service; vanilla (Field) and Flask (Quotes) consume token CSS + a thin local layer; Flutter (Cards) consumes the Dart token output + Flutter widgets. There is deliberately no single cross-stack component set. (3) **Distribution is pin-by-tag, never vendor** (already `AUTONOMOUS-SPRINT-RULES.md` §5) — vendored/hand-copied tokens are the drift mechanism. Claude Design is brought on-brand by attaching the tokens repo + the `design_eq_profile` brief as its "start with context" bundle (`eq/design/claude-design-context.md`).

**Why:** Royce's question — "can we have one UI template for everything?" — resolves to: yes at the token layer (one source already feeds React, vanilla, Flutter, Flask), no at the component layer (a React package can't serve Flask or Flutter). The 2026-05-30 + 2026-05-31 audits showed every drifted surface was a copied-not-pinned one, and the foundation (tokens, theming, first three components) is already strong. Recording the model stops the next app re-deriving it or re-vendoring.

**Alternatives considered:**
- *One cross-stack component library.* Rejected — technically impossible across React / Flutter / Flask; forces a lowest-common-denominator or a maintenance burden. Tokens already deliver the seamlessness that matters.
- *Keep the model implicit in the sprint docs.* Rejected — it was scattered across `design-audit-2026-05-30.md` + Rule §5; a standing decision is the canonical home so it survives the sprint closing.
- *Per-app fonts/colours (status quo before One Spine).* Rejected — that was the drift this consolidation removes.

**Implications:**
- New EQ surface → consume `@eq-solutions/tokens` by tag on day one; never vendor. A React surface also consumes `@eq-solutions/ui`.
- The shared component library grows by promoting best-in-class app components (mostly Service's) into `@eq-solutions/ui`, then adopting in Shell — board rows A7–A12, brief in `component-audit-2026-05-30.md`.
- Plus Jakarta Sans ships self-hosted from the shared layer (one fix for all consumers; supersedes the per-app Google-Fonts loads).
- Claude Design and the Figma connector both point at the same tokens repo + brief; mocks come out on-brand by construction.
- Does not touch auth or SKS live — unaffected by `AUTONOMOUS-SPRINT-RULES.md` §0/§1.

---

## 2026-05-30 — Autonomous Sprint: Full-Auto EQ Deploy, SKS Live Untouchable, Auth Gated

**Status:** Accepted

**Decision:** For the autonomous parallel sprint, agents MAY build, branch, open PRs, gate them green, and **merge + deploy autonomously for EQ-side changes** — superseding, *for the sprint scope only*, the standing "no push/deploy/commit without explicit instruction" and "never deploy to eq-solves-field.netlify.app directly" rules (`CLAUDE.md` §7/§11, `rules/non-negotiables.md`). Two carve-outs remain hard gates:
- **SKS live is untouchable** — no deploy to sks-nsw-labour.netlify.app, no writes to the SKS live DB (`nspbmirochztcjijmcrx`), no Field-merge cutover. Unchanged from the standing rule.
- **Auth-flow changes stay gated** — build + green PR is fine, but deploying any auth / MFA / session / password change still needs Royce's explicit OK. Preserves the standing auth-review non-negotiable.

Full conventions in `SPRINT-BOARD.md`, `AUTONOMOUS-SPRINT-RULES.md`, `STATE.md` (eq-context repo root).

**Why:** 2026-05-30 ran several parallel agent sessions and hit repeated *divergence*: diverged local mains dragging unrelated commits into PRs, duplicate sequential migration numbers breaking Service CI twice (`0097`, then a `0110` near-miss), stale worktrees holding uncommitted work, two sessions colliding in one repo. A source of truth + structural guardrails (branch-from-origin, timestamp migrations, claim-before-start) makes divergence structurally hard; full-auto EQ deploy keeps the sprint moving without a human bottleneck on every change. The carve-outs preserve the only two gates whose blast radius justifies a human: SKS (separate live entity) and auth (suite-wide, hard to unwind).

**Alternatives considered:**
- *Keep all deploys gated.* Rejected — re-introduces the bottleneck the sprint is meant to remove; review load on Royce becomes the constraint.
- *Full-auto including auth + SKS.* Rejected by Royce — auth is highest-blast-radius, SKS is a separate live entity; both keep a human gate.
- *Document the policy only in the root sprint docs.* Rejected — agents load the substrate contract at session start and would get the opposite instruction; the policy must live in the governance log to authoritatively supersede.

**Implications:** Agents on the EQ sprint deploy on green without asking. `rules/non-negotiables.md` and `CLAUDE.md` §7/§11 still carry the old "no direct deploy / auth review" lines — they are superseded by this entry **for the sprint scope only** and should gain a pointer to it (decision-grade edit; Royce to apply, or relax auth too if he chooses). When the sprint ends, mark this Superseded or restore the non-negotiables. The SKS-live and auth carve-outs remain in force permanently regardless of sprint status.

---

## 2026-05-21 — SKS Brand Enforcement: Spec → Artefacts

**Status:** Accepted.

**Decision:** Move SKS brand enforcement from runtime-spec ("Claude reads `rules/brand.md` every output and applies it") to pre-built artefacts (CSS, Word template, preflight checklist). Three artefacts now own enforcement; `rules/brand.md` stays as the source-of-truth spec but is no longer the per-output enforcement surface.

**Why:** Inconsistency in past SKS outputs traced to Claude misremembering or misapplying `brand.md` rules at output time (wrong hex, wrong logo aspect ratio for the Text variant — fixed 2026-05-19, EQ tokens leaking into SKS docs, footer omissions). The cost was paid per-output in tokens (re-fetching and re-reasoning over the full brand spec) AND in defects when the re-reasoning was wrong. Pre-built artefacts pay the cost once at build time, eliminate the failure mode entirely for HTML (CSS link) and Word (template inheritance), and add a six-line final-gate check (`rules/brand-check.md`) for everything else. Expected consistency lift: ~70% → ~98% (estimate from Chat session that designed the kit).

**Artefacts deployed (2026-05-21):**
- `sks-brand.css` → `https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/sks-brand.css` (HTML/web canonical stylesheet; CSS custom properties for colours/fonts; component classes `sks-banner`, `sks-table`, etc.)
- `SKS_Master.docx` → `https://pub-97a4f025d993484e91b8f15a8c73084d.r2.dev/SKS_Master.docx` (Word template with named styles SKSTitle, SKSH1, SKSH2, SKSH3, SKSBody, SKSBodyMuted, SKSCaption, SKSFooter; brand-correct header logo + footer)
- `rules/brand-check.md` in substrate (six-line preflight; linked from `CLAUDE.md` §3 and `rules/brand.md` §7)

**Resolved discrepancies (Royce 2026-05-21):**
- **SKS ABN:** `51 168 906 956`. Three sources had disagreed (`sks/templates.md` footer had `80 006 455 699`; the SKS PDF Style Guide v1.0 footer had `24 004 554 929`; global memories had `51 168 906 956`). Royce confirmed `51 168 906 956`. `sks/templates.md` and the master docx footer string updated to match. Pending follow-up to verify against ASIC / ABN Lookup and to investigate the two stray ABNs.
- **NSW office address:** `27/10 Gladstone Rd, Castle Hill NSW 2154` (matches `rules/brand.md` §7 already; the PDF Style Guide's `Unit 18, 7-9 Percy Street, Auburn NSW 2144` was rejected as the canonical address but flagged for confirmation that Auburn isn't a current second site).
- **Quote body font:** Hybrid Roboto/Calibri policy. Headings in all outputs = Roboto. Body in PDFs we generate = Roboto (fonts embedded). Body in editable `.docx` = **Calibri** (Word default since Office 2007; universally installed on Win/Mac Office; zero install friction; zero layout drift on recipient machines). This supersedes the prior `rules/brand.md` §3 "Muli body with Arial substitution" policy — Muli was never installed in Word by default anyway, Arial was the de-facto rendering, and the new explicit Calibri-for-docx rule replaces the implicit fallback chain. `build-master-docx.js` was refactored to split `SKS.font = "Arial"` into `SKS.headingFont = "Roboto"` and `SKS.bodyFont = "Calibri"`, every named style updated to reference the appropriate token, and the master docx rebuilt + uploaded.

**Alternatives considered:**
- *Keep runtime spec enforcement and just write a better `brand.md`.* Rejected — the failure mode wasn't spec quality, it was recall accuracy at output time. A clearer spec doesn't solve "Claude forgot to fetch it."
- *Roboto everywhere (body + headings).* Rejected by Royce after explaining the recipient-side font fallback risk: editable `.docx` files sent to Equinix / Schneider / Erilyan recipients whose workstations may not have Roboto installed would render in Calibri silently via Word's missing-font substitution, and the layout drift (different metrics → reflow → table breakage) is the exact "looks inconsistent" failure mode this kit is meant to eliminate.
- *Arial everywhere (the previous policy).* Rejected — Arial-only sacrifices the brand visual without solving any problem Roboto-with-Calibri-fallback doesn't already solve.
- *PDF-only deliverables (no editable docx at all).* Rejected — Royce's customers explicitly want the editable docx for variation edits and acceptance signatures. PDF-only would break a real workflow.

**Implications and principle going forward:**

1. **`rules/brand.md` is the SPEC; the artefacts are the ENFORCEMENT.** Future brand updates edit `brand.md` first, then rebuild the artefacts (re-run `node build-master-docx.js`; edit `sks-brand.css` to match). Never edit an artefact without updating the spec.
2. **The R2 bucket holding `sks-brand.css` and `SKS_Master.docx` is in the SKS Cloudflare account, NOT the EQ Solutions Cloudflare account.** Initial upload attempt via `wrangler r2 object put` targeted EQ's `sks-assets` bucket (where wrangler was authed); files were uploaded to the wrong account, then deleted, and Royce did the final upload manually via the SKS Cloudflare dashboard. Future R2 ops on the SKS public bucket need a re-auth (or dashboard upload). Logged as a constraint to remember.
3. **`brand-check.md` is the canary** — if Royce stops seeing the single-line "Brand check: ✓ ..." in outputs, the discipline has lapsed and the next failure is incoming. Three monitoring follow-ups added to `sks/pending.md`.
4. **The 2026-05-21 ABN/address/font discrepancies are surfaced, not yet definitively resolved against external truth** (ASIC for the ABN, internal records for the address). The decision captures Royce's call but `sks/pending.md` carries the verification follow-ups.
5. **Wrangler version 4.x defaults to LOCAL for R2 uploads.** Without `--remote`, `wrangler r2 object put` writes to a local emulator (not actual R2) and reports "Upload complete" with no warning beyond an easily-missed "Resource location: local" line. This is a real footgun that almost caused a silent deployment failure today; all SKS R2 ops from wrangler 4.x must use `--remote`. Logged to `system/lessons.md` is pending.

---

## 2026-05-20 — Split SKS Live Out of eq-field Into Dedicated Repo

**Status:** Accepted; supersedes the 2026-05-13 "eq-field-app Lives at Milmlow Personal Account; One Repo, Two Branches" decision (which itself superseded the original "eq-solutions/eq-field-app" guidance).

**Decision:** The SKS NSW Labour app now lives in its own dedicated GitHub repo `eq-solutions/sks-nsw-labour` (public). The previous arrangement — one repo (`eq-solutions/eq-field`, formerly `Milmlow/eq-field-app`) with `main` = SKS Live and `demo` = EQ Field demo — has been unwound. After the split: `eq-solutions/sks-nsw-labour` serves `sks-nsw-labour.netlify.app` from its `main` branch; `eq-solutions/eq-field` is EQ-Field-only with `main` as the active development branch (the former `demo` renamed in place). The pre-existing local folder split (`C:\Projects\sks-nsw-labour` vs `C:\Projects\eq-solves-field`) now mirrors a real repo boundary instead of two clones of one repo.

Execution sequence (2026-05-20):
1. Created empty `eq-solutions/sks-nsw-labour` via `gh repo create`.
2. From `C:\Projects\sks-nsw-labour` (the local SKS Live clone), pushed `main` (HEAD `aa1eedd`) + the active feature branch `claude/sks-db-hardening-2026-05-20` to the new repo.
3. Manually re-linked the existing `sks-nsw-labour` Netlify project to the new repo via the Netlify dashboard (the API rejects `build_settings.repo_url` PATCH silently — see `system/lessons.md`).
4. Triggered a fresh build via Netlify API; deploy verified ready at commit `aa1eedd` from the new repo (deploy time 6s, no functional change to the live site).
5. Repointed the local clone's `origin` to the new repo (the old eq-field origin retained as `eq-field-archive` for rollback).
6. On `eq-solutions/eq-field`: closed PR #116 (the SKS feature branch's PR against eq-field/main, now obsolete), deleted `claude/sks-db-hardening-2026-05-20`, changed default branch `main` → `demo` as a transient step, deleted the now-orphan `main`, renamed `demo` → `main`. Net result: eq-field has the standard "main is the active development branch" shape.

**Why:** Two-clone-one-repo patterns are an active source of substrate noise and stranded commits. The 2026-05-13 ADR justified the consolidated repo on the grounds that migrating to a separate one "would require redoing Netlify integration, which is not on the priority list" — that estimate proved low (the actual rewire was a dashboard click + ~6s build, totalling under 5 minutes). The cost of not splitting was much higher: the 2026-05-20 md-health audit surfaced the eq-solves-field clone holding a 7-day-stale local-only commit (`db2b5fa Add .gitattributes`) that the sks-nsw-labour clone couldn't see, plus 50 uncommitted entries; the "MISSING .gitattributes" report finding required three separate course corrections before the right action (write a fresh commit on main from the SKS Live clone, since the demo-side commit was never pushed) became clear. Two clones diverging silently is exactly the failure mode that a single-purpose-per-repo structure prevents.

**Alternatives considered:**

- *git worktrees off a single clone* (one `.git`, two working trees `eq-field/main` + `eq-field/demo`). Rejected — solves the local clone-drift problem but doesn't address the underlying conceptual problem (one GitHub repo serving two unrelated products with deliberately divergent codebases). The two branches were 1-ahead-106-behind on `demo` and there was no scenario in which they would converge again. Two products → two repos is the right shape.
- *Single clone, switch branches* on each working session. Rejected — blocks parallel work on EQ Field and SKS Live, makes accidental cross-deploys more likely (push the wrong branch from the wrong context).
- *Cut from a clean HEAD vs subtree-split preserving history.* Adopted the clean-HEAD cut per Royce's 2026-05-20 call ("eq field and sks live are no longer sync — I've gone too far ahead with eq field"). The two codebases share a common ancestor at `948f414` but diverge so heavily afterwards that preserving the intertwined history would have produced a confusing single-product log full of irrelevant EQ Field commits. Cutting from `aa1eedd` gives the new repo a clean baseline; the historical eq-field repo retains the full record if needed.
- *Leave eq-field/main as an archived orphan* (option C in the post-split cleanup question). Rejected — orphan branches in a repo are recurring confusion-generators ("which main is real?"); cheaper to fix once now than answer that question every time someone navigates the repo.

**Implications and principle going forward:**

1. **Update local references** — `C:\Projects\eq-solves-field` (which has 50 uncommitted entries on the local `demo` branch) needs `git fetch --prune && git branch -m demo main && git branch --set-upstream-to=origin/main main` when Royce next opens that folder. Logged in `ops/pending.md`. The OLD origin URL for `C:\Projects\sks-nsw-labour` is retained as `eq-field-archive` remote for rollback for ~30 days.
2. **CLAUDE.md / global rules** — Royce's `C:\Users\EQ\.claude\CLAUDE.md` deployment table lists `sks-nsw-labour.netlify.app` against repo "EQ Field (demo)"; that row needs to become repo `eq-solutions/sks-nsw-labour`. Royce-manual edit (in his personal global rules, not substrate).
3. **The 2026-05-13 ADR is now superseded** but remains in the log as the historical reasoning. Its "migration cost too high" line is the contradicted prediction that motivated this entry's "Why".
4. **Default repo shape going forward** — one product per repo. The next time a dual-purpose pattern is proposed (one repo, two long-lived branches, two products), this ADR is the rebuttal.

---

## 2026-05-20 — Sentry / Observability Project Slug = `eq-<product>`, Not Repo Name

**Status:** Accepted; supersedes the prior "slug = repo name" guidance in `~/.claude/CLAUDE.md` (Observability stack table).

**Decision:** Sentry project slugs (and by extension PostHog project keys, Clarity project IDs, and any other per-app observability slug) follow the **`eq-<product>` convention**: `eq-quotes`, `eq-field`, `eq-expenses`, `eq-ops`. Not the repo name (`eq-quotes-port`), not the deploy slug (`eq-quotes-sks`), not the Netlify site name (`eq-solves-service`). Captured 2026-05-20 in `~/.claude/CLAUDE.md` (Observability stack table). The first project wired under the new rule is `eq-solutions/eq-quotes` on Sentry.

**Why:** Repo names carry implementation history (`-port` for the SQLite→Supabase port, `-react` for a future rewrite, `-v2` for redesigns). Deploy slugs carry deployment history (`-sks` for the SKS pilot tenant). Product slugs are stable across both — they're how a human refers to the system. Tying the observability slug to the product means a repo rename or a tenant addition doesn't break alert routing, DSN environment variables, or the muscle-memory URL pattern `mcp.sentry.dev/mcp/eq-solutions/<product>`.

**Alternatives considered:**
- *Repo-name slug (original rule).* Rejected — couples observability to the repo's implementation history. The eq-solves-service Sentry project already paid this cost; we're not adding more.
- *Deploy-slug slug.* Rejected — couples observability to the deployment tenant. Adding a second tenant of the same product would force a second Sentry project, which is wrong (we want one project per product, not per deploy).
- *Free-form per project.* Rejected — every time the question comes up Royce has to remember "did I call it eq-quotes or quotes-eq or eqq?" Pattern enforcement is cheaper than recall.

**Implications and principle going forward:** When wiring observability for a new EQ app, the slug is mechanical: `eq-` + the product name in `eq/products.md`. The MCP URL, the Fly secret name, the alert email subject pattern all follow. Repo or deploy details stay out of the observability surface. Existing projects (`eq-solves-service`) keep their legacy slug for backwards compat but new ones follow the rule.

---

## 2026-05-19 — Substrate URLs Converted to Full Links for Transitive Fetchability

**Status:** Accepted

**Decision:** All relative paths in `CLAUDE.md` and every `README.md` (eq, sks, ops, system) were converted to full markdown links pointing at the Supabase edge function (base URL `https://urjhmkhbgaxrofurpbgc.supabase.co/functions/v1/context/<path>`). New "substrate map" sections added to `sks/README.md`, `eq/README.md`, `ops/README.md`, and `system/README.md` indexing every canonical file as a fully-qualified clickable URL. The `§8 Where Things Live` table in `CLAUDE.md` was split so each file is its own row with its own clickable link.

**Why:** Claude.ai chat's `web_fetch` tool is allowlist-driven — it only fetches URLs that were user-provided in the prompt or appeared in a prior fetch result. Relative paths like `sks/templates.md` inside an already-fetched `CLAUDE.md` are therefore invisible to it: there's no URL for the allowlist to admit, so sibling files cannot be reached transitively from `/context/claude`. Live confirmation came from a 2026-05-19 chat session that fetched `CLAUDE.md` cleanly but then refused to fetch any of the relative paths inside it because they weren't full URLs. The model could *construct* the URL ("just append the slug to the base") but the fetch tool still wouldn't take it — the constraint is in the tool, not the model.

**Alternatives considered:**
- *Tell Claude to construct URLs from base + relative path.* Rejected — the model can build the string, but `web_fetch` won't fetch URLs it has never observed in the conversation, regardless of provenance.
- *Paste every needed URL into each chat manually.* Rejected — that is precisely the friction this fix removes.
- *Concatenate everything into a single megaprompt.* Rejected — defeats the tier-gating design (§1) and bloats every session beyond the attention budget.

**Implications and principle going forward:** Every new substrate file must be linked as a full markdown URL from at least one already-reachable file — most likely its tier's `README.md` "substrate map" section, or the `§8 Where Things Live` table in `CLAUDE.md` — before it can be considered reachable. Otherwise it is **orphaned**: a fact of life inside the GitHub repo but invisible to any chat that bootstraps from `/context/claude`. Treat un-linked files the way you would treat un-`include`'d source files: from the consumer's perspective they don't exist. When adding a new tier directory or top-level file, the "wire it into a substrate map" step is now on the substrate-structure checklist alongside the `context` edge function update (see `ops/pending.md` → Substrate Discipline).

---

## 2026-05-19 — Dedupe Is Intake's Job, Not Per-App

**Status:** Accepted; companion to the "EQ Quotes Canonical Migration:
Reject Path A, Adopt Parallel-Tracks" entry below.

**Decision:** When a CRM export (SimPRO, AroFlo, Xero, MYOB, etc.)
lands in EQ Intake with structural duplication — the most common
pattern being "one row per (customer, site) where the customer name
repeats across many site rows" — the dedupe + collapse-to-canonical-shape
work happens **inside the intake pipeline**, not inside the app
consuming the data. The skill belongs to the canonical layer. Apps
read clean canonical data; they don't re-implement dedupe themselves.

**Why:**

The pattern is universal. Every CRM with a "site" or "location"
concept produces this shape on export — and every tenant onboarding
into EQ will encounter it. Building dedupe once in intake means
every tenant gets the benefit. Building it per-app means every app
solves the same problem from scratch and the bookkeeper learns N
different dedupe UIs.

It maps to intake's job description per `eq-intake/EQ-INTAKE-ARCHITECTURE.md`:
"AI maps the columns to the canonical schema by reading the column
names and a sample of values, then asks for confirmation. Once
confirmed, the mapping is saved as a template — next time a
similar-shaped file comes in, no AI call needed." Dedupe is exactly
the same shape — AI proposes "47 rows look like one Equinix entity,
collapse to 1 customer + 47 sites?", bookkeeper confirms via the
Confirm-UI, decision is cached so re-importing the same file shape
skips the AI call.

The canonical schema already supports the right answer. `eq-canonical`
has customers + sites + contacts as separate tables with the FKs
pre-wired. SimPRO's flat "customer-with-site per row" splits cleanly:
one customer row + N site rows + contacts attached at the right
level (company-wide vs site-bound).

Confirm-UI is built for low-confidence human review. `CONFIRM-UI-SPEC.md`
already covers AI-proposes + bookkeeper-validates. The dedupe step
adds two confidence tiers ("47 'Equinix' rows = HIGH confidence,
collapse" vs "12 'A.G. Coombs' + 3 'AG Coombs NSW' = MEDIUM, review
each"). Bookkeeper accepts the highs in bulk, eyeballs the mediums.

This is also a sellable feature. "EQ Intake recognizes when your
CRM export has the customer-vs-site pattern wrong and cleans it on
the way in" is a real value prop versus "drop a SimPRO CSV into the
new system, get a mess that doesn't match how you actually work."

**Alternatives considered:**

- **Per-app UI dedupe (e.g. customer list groups by name, contact
  directory dedupes by company+contact)** — rejected. Solves the
  symptom in one app, doesn't transfer to others. EQ Field, EQ
  Service, EQ Cards would all reinvent the same logic. Throwaway
  work given the eq-quotes-port Flask app is being replaced 2-3
  months out anyway.
- **Destructive dedupe during a one-off import script** — rejected.
  Considered earlier same day during the canonical migration reset.
  Bakes legacy assumptions into canonical, skips the audit / rollback
  / schema-version tracking intake provides.
- **`customer_group_id` column linking dupe rows at the data layer** —
  rejected. Adds a concept just to paper over the missing customer↔sites
  FK. If we're adding infrastructure, do it right via the canonical
  customers + sites tables.
- **Fuzzy-match dedupe with no UI review** — rejected. False-positives
  collapse legitimately separate entities ("Smith & Sons" vs "Smith
  Sons Pty Ltd" might be different ABNs). Needs Confirm-UI human
  review for medium-confidence matches.

**Implications:**

- The dedupe step gets added to `eq-intake/CONFIRM-UI-SPEC.md` as a
  new section (companion to column-mapping confirmation).
  Implementation detail lives there; this entry is the "why."
- `eq-quotes-port` Flask app keeps the duplicated customer rows
  visible during the pilot. Estimators learn to search ("Equinix
  SY3" returns the right row, "Equinix Australia" returns ~50). Pain
  level acceptable; if it becomes blocking we revisit with a 2-hour
  UI patch but the goal is no throwaway work.
- When eq-canonical takes over EQ Quotes (~2-3 months out), the data
  arriving there from intake is already deduped. The new React
  module reads clean customers + sites + contacts from canonical
  with no app-side workaround needed.
- Each tenant that onboards via intake benefits. Generic skill, built
  once.

**Risk:** The dedupe AI prompts need real validation against more
than one CRM export shape. SimPRO is the only one we have today.
AroFlo / Xero / MYOB will surface edge cases. Acceptable — the
pattern is sound; per-source quirks land as test fixtures as they
appear.

---

## 2026-05-19 — EQ Quotes Canonical Migration: Reject Path A, Adopt Parallel-Tracks

**Status:** Accepted; reverses an earlier-same-day "Path A — fix in
intake now, delay pilot" stance taken during the canonical migration
review.

**Decision:** EQ Quotes Flask v1 (`https://quotes.eq.solutions`,
hosted Fly.io, backed by `sks-labour` Supabase) ships the SKS pilot
as-is. No data migration, no schema rework, no Supabase repointing.
The `eq-canonical` project (`jvknxcmbtrfnxfrwfimn`) is built as a
**greenfield** multi-tenant canonical layer in parallel. The Flask
app and the canonical layer **do not interact** during the pilot.
When the real EQ Quotes React module is eventually built (Position 4
per the un-defer entry above), it lands as an eq-shell module
against eq-canonical with no inherited coupling.

**Why:** Mid-session, the plan was a 7-phase migration of
sks_quotes_* schema + data from sks-labour to eq-canonical, including
a Customer→Site refactor and a new two-stage typeahead. Phase 1
(bulk SimPRO import: 267 customers / 472 sites / 393 contacts)
landed via a one-off Python script with deterministic UUIDs. Royce
course-corrected three times:

1. "Should we finish eq-shell first?" — i.e., the canonical-data
   work depends on eq-shell being functional, which it isn't yet for
   SKS.
2. "We are not touching SKS — please stop thinking we are, this is a
   fresh start. Nothing to do with SKS." — The canonical layer is
   not "SKS's canonical." It's generic multi-tenant infrastructure.
   Any tenant onboards the same way: via EQ Intake's commit RPC, not
   via direct DB-to-DB migration.
3. "EQ Intake is the only path in." — One-off bulk imports skip the
   audit, rollback, and schema-version tracking that
   `eq_intake_commit_batch` provides. The 1,132 imported rows were
   dropped from eq-canonical and the import scripts retained for
   reference only.

**Alternatives considered:**

- **Path A — migrate EQ Quotes onto eq-canonical now** (rejected
  mid-session — couples a still-evolving canonical layer to a
  pre-pilot Flask app; delays the pilot for an architectural fix
  estimators won't see; bakes SKS-specific assumptions into what
  should be a tenant-agnostic foundation).
- **Path B — dedupe sks_quotes_customers directly without involving
  canonical** (rejected during the earlier-same-day review —
  faster but bakes "Quotes owns customer data" into the system,
  opposite of the conduit thesis).
- **Half-port — Flask app reads from eq-canonical for customer/site,
  writes to sks-labour for quotes** (rejected — cross-project
  reads complicate auth, RLS, and operational debugging; the upside
  is small).

**Implications:**

- `eq-quotes-port` repo's `docs/canonical-migration-plan.md`
  (Phases 1-7) deleted. Replaced by `docs/canonical-plugin-contract.md`
  capturing the operational contract for any future module
  (not just Quotes).
- `eq-canonical` is "ready to receive modules": 12 canonical
  entity tables, intake + export spines, tenants/users/
  module_entitlements all live; one tenant (`core` / EQ Solutions)
  registered; zero canonical entity rows.
- `quotes.eq.solutions` pilot ships unchanged. Estimator feedback
  during the pilot informs whether the eventual React rewrite
  needs to bring forward in the queue (currently Position 4).
- The Flask v1 codebase becomes "the spec" for the eventual React
  rewrite. Business logic, validation, status transitions, money
  math, Word doc tokenization, scope/rate preset structure — all
  documented through working code. Treat as an executable spec.
- No new SKS dependency added to eq-canonical. When SKS is ready to
  move from sks-labour onto canonical (post-pilot, post-rewrite),
  it follows the standard tenant-onboarding flow per the contract
  doc — `INSERT INTO tenants`, provision users with `tenant_id` in
  Raw User Meta, populate entities via EQ Intake.

**Risk:** carrying two implementations of EQ Quotes (Flask v1 +
future React module) during the transition. Acceptable for the
pilot horizon. Becomes problematic if both are maintained
long-term — but the React module replaces the Flask app once it's
proven, no parallel maintenance.

---

## 2026-05-19 — Un-Defer EQ Quotes; Position 4 in EQ Shell Module Queue

**Status:** Accepted; supersedes the 2026-04-29 cull's "EQ Quotes deferred ~6 months" stance.

**Decision:** EQ Quotes is removed from the deferred-products list and reinstated as an active EQ product. Position 4 in the EQ Shell module-mounting sequence after (1) Shell working, (2) Field demo mounted, (3) Service mounted. Current shipped form is Word + Excel templates + SOPs (v2 set finalised 2026-05-18, in live operational use inside SKS quoting motion). The real Quotes product build — React UI under Shell, quote register persisted to canonical Supabase, docx-js Word generation, scope/price/issue/track workflow — does not begin until Shell + Field + Service are mounted under Shell. 10 hrs/week build allocation stays on Shell/Field through validation gate; Quotes work begins when its queue position arrives.

**Why:** Two facts forced the reversal. First, the templates are not deferred in practice — `eq-quotes/` was edited 2026-05-18 with v2 template set finalisation, SKS Implementation Guide, Job Creation Template v7, and Quote Register. The "deferred 6 months" stance contradicted what was actually happening operationally. Second, Royce's 2026-05-19 EQ Shell module-mounting sequence (Shell → Field → Service → Quotes → Intake → Cards) explicitly placed Quotes 4th in the queue. Holding the defer in substrate while the operator is sequencing the product as next-after-Service would manufacture a contradiction the substrate exists to prevent. Better to surface the strategic shift cleanly than carry a stale defer.

**Alternatives considered:**

- **Keep the defer** (rejected — operational reality already invalidates it; templates are live and being used; the strategic queue places Quotes 4th).
- **Un-defer immediately AND start building** (rejected — Shell + Field + Service take priority through the 5/5 validation gate. Quotes waits in queue position 4. The un-defer is a substrate flag flip, not a build-now signal).
- **Un-defer informally without updating products.md / README** (rejected — substrate consistency requires the file matches reality. Half-flipping the defer leaves the contradiction in place for the next audit to flag).
- **Treat Quotes as templates-only forever, never as a real product** (rejected — the EQ Shell sequencing explicitly anticipates a Quotes module, and customer signal during validation-gate engagement may demand the build sooner. Templates are the current shipped form, not the final form).

**Implications:**

- `eq/products.md` gains an EQ Solves — Quotes section (active, templates-only currently, real build deferred to Shell module queue position 4).
- `eq/README.md` removes EQ Quotes from the killed/deferred list with a pointer to this entry.
- `CLAUDE.md` §9 ("Killed / Deferred — NOT Live Products") currently lists EQ Quotes as deferred 6 months. **Follow-up:** Royce to remove that line on next CLAUDE.md edit, or surface as a pending item.
- `archive/changelog-eq-quotes.md` stays in archive for now. When the real product build begins, it moves to `eq/changelog/quotes.md` as the live append-only history. No code-level change to the archive folder today.
- Validation gate stays on Field. Quotes does not introduce a new gate.
- Build allocation: Quotes work does not begin until Shell + Field + Service are all mounted and live. Estimated start: 2-3 months out at current 10 hrs/week pace.
- Strategic risk: real customer signal during Phase A (Shell+Field+Service rollout) may demand Quotes earlier than position 4. If 3 of the first 5 subbies say "quoting is what I actually need", this entry gets superseded and Quotes jumps the queue. Acceptable signal-driven re-rank.

---

## 2026-05-14 — Build vs Adopt: Existing Software Wins by Default

**Status:** Accepted

**Decision:** Add a non-negotiable rule (new "Build vs Adopt" section in `rules/non-negotiables.md`) requiring the assistant to search for and present existing software that solves the same or similar problem before scaffolding anything new — commercial SaaS, open-source, internal SKS/EQ tools, or whatever already runs in the substrate's stack. Building from scratch is permitted only after alternatives are named and rejected with stated reasons. For anything larger than a one-off utility script, the reasoning is logged as an ADR with rejected alternatives under **Alternatives considered**.

**Why:** The substrate has been operating on this principle intermittently for months. The 2026-05-13 decision to absorb Ben Ritchie's `sks-field-reports` MVP into EQ Field rather than rebuild it independently is the principle in action. The 2026-04-29 product cull killed EQ Variations, EQ Compliance, and EQ Ops in part because Procore, Hammertech, and Aconex already do those jobs. The "working before refactoring" rule (CLAUDE.md §4) and the system-prompt guidance to not add features beyond what the task requires both point in the same direction. Formalising the rule prevents the failure mode where the assistant scaffolds something new because the request literally asked for "build me X", even when adopting an existing tool would beat the build on time-to-value, maintenance load, integration, and ecosystem support. Royce's time is the scarcest input. Building software that already exists wastes it.

**Alternatives considered:**

- **Leave the existing soft rule in `rules/stack.md`** (rejected — that rule applies to tech-stack additions (libraries, services) and explicitly says "explain why it beats what's in the stack", but it does not cover whole solutions like SaaS apps, open-source projects, or internal tools. The gap was real).
- **Phrase as SHOULD rather than MUST** (rejected — soft language makes the rule easy to skip silently; the failure mode the rule prevents is exactly "assistant scaffolds without checking", which a SHOULD rule does not catch in practice).
- **Apply to all new code with no exemption** (rejected — would force a search and ADR for trivial utility scripts; the value of the rule is in the bigger builds where adopt-vs-build is consequential. The exemption for one-off utility scripts (~≤100 lines, single-use) keeps the rule from becoming friction theatre).
- **Higher "battle-tested" bar for what counts as existing software** (rejected — a narrower bar would miss small open-source tools and internal-to-SKS solutions that nonetheless solve the problem well. "Production use anywhere — real people, real work" is the right floor).
- **Add to CLAUDE.md §7 critical subset rather than non-negotiables.md** (rejected — §7 is reserved for "MUST NOT" prevention rules guarding against irreversible mistakes (deploys, credentials, cross-deploys). This rule is a positive default about methodology, not a prevention rule; it belongs in non-negotiables.md, which CLAUDE.md §8 already points to).

**Implications:**

- `rules/non-negotiables.md` gains a new "Build vs Adopt" section placed between Substrate and Code & Deployment.
- Future non-trivial build requests should produce an alternatives-considered section in the assistant's response; full-app or full-module builds should also produce an ADR before scaffolding begins.
- `rules/stack.md`'s existing soft version of this rule for tech-stack additions stands as-is — it is now explicitly the narrower stack-specific application of the broader principle.
- The 2026-05-13 sks-field-reports absorption decision is the canonical worked example of the rule. Future ambiguous cases can refer to that ADR for shape (collaboration with existing builder, gradual cutover, no silent retirement of the absorbed tool).
- Failure mode to watch for: rule degenerating into a perfunctory list of alternatives at the top of every build response. The rule's value is in *changing the answer*, not just in *documenting that an answer was reached*. Surface this in a future lessons.md entry if the pattern emerges.

---

## 2026-05-13 — Path C: Absorb sks-field-reports workflows into EQ Field as a Sub-Module

**Status:** Accepted

**Decision:** Workflows from Ben Ritchie's standalone `sks-field-reports.netlify.app` (v29) — Prestart, Toolbox Talk, Daily Site Diary, Weekly Site Report — fold into EQ Field's new "Site Reports" sub-module rather than continuing as a separate SKS internal tool. Treat this as collaboration with Ben, not replacement: his MVP shapes the EQ implementation, and `sks-field-reports.netlify.app` retires only once EQ Field reaches parity on all four workflows AND Ben + Royce sign off on the cutover. Prestart MVP shipped to EQ Field demo as v3.4.69 on 2026-05-13.

**Why:** Two separate apps maintaining the same workflows is the failure mode the substrate audits keep flagging in other places. Folding the workflows into EQ Field (a) gives the commercial product real operational depth (Site Reports becomes a flagship sub-module, not just timesheets), (b) keeps a single canonical data store (`prestarts` table on both Supabases as of 2026-05-13), (c) avoids the dual-source confusion that already required a yellow banner on the EQ Prestart page directing users away from Ben's app, and (d) sets up the commercial unlock — a Friday compliance pack export bundling staff + licences + prestarts + toolbox + weekly into Hammertech/Aconex/Procore format — which only works against one canonical dataset.

**Alternatives considered:**

- **Path A — keep both apps running indefinitely** (rejected — duplicate maintenance, dual-source data, no path to the compliance pack export commercial unlock).
- **Path B — rebuild EQ Field's version independently, ignoring Ben's MVP** (rejected — Ben's app is battle-tested with SKS supervisors; throwing away tacit operational knowledge would re-introduce bugs already squashed in v29).
- **Path D — deprecate sks-field-reports immediately and force migration** (rejected — SKS supervisors currently rely on Ben's tool; pulling the rug before EQ Field parity would break their daily workflow).

**Implications:**

- EQ Field's Site Reports module ships workflows in the order Prestart → Toolbox Talk → Daily Diary → Weekly Report. Toolbox Talk is next (v3.4.74).
- Hub/dashboard restructure deferred until ≥2 workflows ship (no premature abstraction with only Prestart).
- Sub-module lives in "Testing (DO NOT USE)" sidebar section with BETA chips until each workflow soaks on demo.
- Demo → main merge for Site Reports is gated on Ben Ritchie sign-off (not just Royce go) — Ben is a stakeholder, not just an information source.
- Ben Ritchie credit / consulting engagement / role in EQ team to be resolved by Royce + Webb Financial (open coordination item).
- Test prestart rows Ben writes during trial must be cleaned before retirement: `DELETE FROM prestarts WHERE works_scope LIKE 'Test%' OR created_by = '<test name>';`
- Retirement of `sks-field-reports.netlify.app` requires communication window to SKS supervisors — not a silent cutover.
- Compliance pack export (DOCX/PDF generator bundling all 4 workflows for Hammertech/Aconex/Procore) is the demo that closes EQ customer #2 — pre-built only after all 4 workflows exist.

---

## 2026-05-13 — Demo Version Numbers: Second-to-Merge Bumps, Both Shapes Coexist

**Status:** Accepted

**Decision:** When two parallel Claude sessions target the same `demo` branch with the same version number, the second-to-merge bumps to the next number rather than blocking, and both shapes coexist on demo for soak. The branch name keeps its original label (so `claude/v3.4.67-prestart` can ship as v3.4.69 after rebase) — the ship version is what's in the banner/APP_VERSION/sidebar/sw.js tuple, not the branch name.

**Why:** On 2026-05-13 two workstreams collided: Phase B+C role system (`claude/v3.4.68-role-system-clean`) and Site Reports / Prestart MVP (`claude/v3.4.67-prestart`). Both wanted v3.4.68. Role system landed first as v3.4.68 (PR #63); Prestart rebased on top and bumped to v3.4.69 (PR #62). Both ship together because gating either workstream on the other's soak would have delayed customer-visible value by 5-7 days for no defensible reason.

**Alternatives considered:**

- **Serialise via lock file or coordination doc** (rejected — overhead for a 2-3x/year event; Claude sessions are short enough that the rebase cost is small).
- **Pre-allocate version ranges per workstream** (deferred — could revisit if this collision happens twice more; not worth pre-building for an N=1 case).
- **Block second-to-merge until first-to-merge passes soak** (rejected — couples otherwise-independent workstreams; soaks routinely take 5-7 days which would freeze parallel work).

**Implications:**

- Always run `git log origin/demo --oneline -3` before claiming a version number — the brief assumed v3.4.69 was the tip on 2026-05-13 but v3.4.70-73 had already shipped behind it.
- Outstanding brief documents that name a target version (e.g. "Toolbox v3.4.70") become stale fast — confirm the actual next-free number at session start.
- Version bumps are a 4-file tuple per the global feedback memory (banner + APP_VERSION + sidebar span + sw.js CACHE); the rebase-and-bump path must update all four, not just the banner.
- When two parallel worktrees run, confirm worktree paths before multi-step git ops — the working-directory header in a brief can refer to a different worktree than the one the new session is in.

---

## 2026-05-13 — eq-field-app Repo Canonical Org is Milmlow (Personal Account)

**Status:** Accepted

**Decision:** The `eq-field-app` GitHub repo lives at `github.com/Milmlow/eq-field-app` (Royce's personal account). One repo, two long-lived branches: `main` = SKS Labour App (live, deploys to sks-nsw-labour.netlify.app), `demo` = EQ Field demo. References to `eq-solutions/eq-field-app` are stale.

**Why:** A 2026-05-13 substrate audit found `eq/products.md` (Milmlow) and `sks/products.md` (eq-solutions) disagreed about the org prefix on the same repo. Confirmed with Royce 2026-05-13 that the personal account is canonical. Deploy pattern (push to main → Netlify CD to sks-nsw-labour) currently runs from the personal-account repo; migrating to the org would require redoing Netlify integration, which is not on the priority list.

**Alternatives considered:**

- Migrate to `eq-solutions/eq-field-app` (rejected — Netlify integration would need to be redone; no business reason to move it; an SKS live product depends on it deploying cleanly).
- Maintain a fork in eq-solutions and mirror (rejected — duplicate state, the exact failure mode this audit was fixing).

**Implications:**

- `sks/products.md` patched to use Milmlow prefix (2026-05-13).
- Future repo references in any file MUST use `Milmlow/eq-field-app`.
- If the repo ever does migrate to the org, this entry gets superseded — do not silently move references.

---

## 2026-05-13 — EQ Solves Service is Next.js, Documented as Exception to Vite Default

**Status:** Accepted

**Decision:** `rules/stack.md` declares Vite + React as the default frontend for new work. EQ Solves Service is built on **Next.js 16** (App Router, TypeScript strict, Tailwind v4) and is logged as a deliberate exception. Confirmed via direct inspection of `github.com/Milmlow/eq-solves-service` README and `next.config.ts` 2026-05-13.

**Why:** A 2026-05-13 substrate audit found `rules/stack.md` (Vite default) and `eq/products.md` (EQ Solves Service "Next.js + Supabase + Netlify serverless functions") disagreed. Both files were correct in isolation — Vite IS the default, AND EQ Solves Service IS Next.js. The fix was to make the exception explicit in `rules/stack.md`, not to change either underlying fact.

**Alternatives considered:**

- Change `rules/stack.md` default from Vite to Next.js (rejected — most prototypes and the legacy single-HTML apps are vanilla / Vite-shaped; making Next.js the default would mis-direct future small tools).
- Migrate EQ Solves Service to Vite (rejected — production app with 169 commits, 80+ Vitest tests, 22 sprints, first paying customer; Next.js features in use include App Router, server actions, image optimisation, edge middleware — a Vite migration is a multi-week rewrite with no business case).
- Leave the contradiction in `eq/products.md` and `rules/stack.md` (rejected — every audit re-flags it; ambiguity in `rules/` files compounds quietly).

**Implications:**

- `rules/stack.md` now lists EQ Solves Service as the first Exception entry alongside the legacy single-HTML apps.
- Future EQ products should default to Vite unless a Next.js-specific feature (SSR, ISR, server actions) is genuinely required — and if so, document the choice in `ops/decisions.md` before scaffolding.

---

## 2026-05-04 — Decline ChatGPT Structural Expansion Proposal (Operations / Contracts / Modes / START.md)

**Status:** Accepted

**Decision:** Decline ChatGPT's "EQ Context — System Review & Next-Step Plan" proposal in full, with two minor exceptions noted below for possible future revisit. The proposal would have added four new structural elements to the substrate (`/operations/`, `/contracts/`, `/modes/`, `/START.md`) plus rewrites of "loaders into execution contracts" and a JSON schema layer for output standardisation. Rejected as speculative architectural expansion against a substrate that is < 2 hours old in its current form and has not yet been used in a single real-world session. The proposal solves theoretical gaps, not observed ones.

**Why:** The substrate underwent a major refactor on 2026-05-04 specifically to *reduce* structural complexity (state/, knowledge/, drafts/, four root files → tier-separated four-tier model + thin pointers). ChatGPT's review, while correctly diagnosing the system as "behaviourally strong but executionally weak," prescribed re-introducing complexity under different names. Accepting it would have undone the day's consolidation work. The actual remedy for the diagnosed gap is *templates*, not *architecture* — and templates grow organically as operational outputs are produced (one currently exists: SKS Quote v3). Speculative pre-building of operations, contracts, and mode files is the exact failure mode the refactor was designed to escape.

**Alternatives considered:**

- **Accept full ChatGPT proposal** (rejected — restores complexity just deconstructed; introduces 4 new folders and a JSON schema layer; speculative against zero real-world session evidence).
- **Accept "drift correction" rule (item 7) only** (deferred — useful idea but small enough to add organically the first time a real session shows the problem; not worth a commit on its own).
- **Accept "minimum session-close fallback" (item 9) only** (deferred — same reasoning; the existing 5-step §10 has not been used enough to know if a fallback is needed).
- **Accept "structured exploration output pattern" (item 4)** (rejected — risks making exploration formulaic, which defeats its purpose; revisit only if real exploration outputs feel inconsistent in practice).

**Implications:**

- The substrate stays as deployed at session close 2026-05-04: tier-separated repo, single CLAUDE.md behavioural contract, two thin pointer files, no `/operations/`, no `/contracts/`, no `/modes/`, no `/START.md`.
- The original ChatGPT proposal text is logged here for future revisit. Items 7 (drift correction) and 9 (minimum session-close) remain candidates for organic adoption if real-world use surfaces the gaps they predict.
- Re-evaluation trigger: if after ~2 weeks of real-world use across Chat/Cowork/Code, operational outputs are still inconsistent OR sessions are skipping the start protocol, revisit ChatGPT's proposal with felt-need evidence rather than theoretical critique.
- General principle: do not expand substrate structure speculatively. Wait for observed gaps. Theoretical gaps are not gaps.

---

## 2026-05-04 — Real Client Names Permitted in Substrate, Forbidden in Outputs

**Status:** Accepted

**Decision:** Rule #19 ("real client names MUST NOT appear in outputs — use generic placeholders") applies to outputs only. The substrate (`eq-context` repo) MAY contain real client names because operational fidelity is the substrate's whole purpose. The assistant MUST redact to generic placeholders ("Data Centre Client A", "Tier 1 Client") whenever substrate content is carried into outputs.

**Why:** A 2026-05-04 audit found 5 substrate files containing real client names (Equinix, AirTrunk, AWS, DigiCo, Schneider, Telstra, Microsoft) — surfacing the ambiguity in the original rule. Two failure modes were possible: (1) scrub all names from substrate, losing operational fidelity ("Equinix SY6 CUFT" carries protocol/facility/expectation context that "Data Centre Client A SY6" does not); (2) leave the contradiction in place, accepting that every audit re-flags it. Carve-out resolves both: substrate keeps its fidelity, outputs stay clean.

**Alternatives considered:**

- **Strict scrub of substrate** (rejected — loses real operational context that makes the substrate useful; recurring cleanup cost as new names get added; the eq-context repo is private with low leak risk).
- **Leave the contradiction in place** (rejected — every audit will flag this as a violation; ambiguity in non-negotiables compounds quietly).
- **Move client names to a separate encrypted file** (rejected — over-engineered for the actual risk; adds reading-friction to the highest-value tier).

**Implications:**

- Rule #19 in `rules/non-negotiables.md` clarified with substrate carve-out.
- The assistant MUST redact substrate-sourced client names to generic placeholders before any output (document, email, presentation, public artefact).
- "Outputs" defined as: anything sent to, shown to, or seen by parties outside Royce.
- This entry exists so future audits don't re-flag the substrate as a rule violation.

---

## 2026-04-28 — Annual `rules/*` Review Cadence

**Status:** Accepted

**Decision:** All files in `rules/` are reviewed for currency once per year. Mechanism: a recurring calendar event on 28 April each year titled "Review eq-context rules/* for currency". The reviewer (Royce) confirms each rule still applies, amends or supersedes any that don't, and logs the review as a session entry with a "no changes" or "changes applied" outcome.

**Why:** ISO 27001 requires annual review of security policies; the same pattern transfers to any normative ruleset that can drift quietly. `rules/` is the lowest-changing folder by design — without an explicit review cadence, files accumulate stale assumptions invisibly.

**Alternatives considered:**

- `last_reviewed` frontmatter field (rejected 2026-04-28 — duplicates `updated_at` semantics; ritual without signal).
- Quarterly review (rejected — overkill for a folder that changes ~3x/year).
- No formal review (rejected — the gap closes here for ~10 minutes/year of work).

**Implications:**

- Calendar event registered on 2026-04-28; first review fires 2027-04-28.
- The Friday substrate audit (`eq-context-substrate-audit` agent) checks freshness, not currency. This decision adds the currency check at annual cadence.
- Out-of-cycle review is permitted whenever a rule is suspected stale — surface via the relevant tier's `pending.md`.

---

## 2026-04-28 — RFC 2119 Modal Verbs Adopted in `rules/`

**Status:** Accepted

**Decision:** Rules in `rules/non-negotiables.md` use RFC 2119 modal verbs (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) for the bolded rule statements. Narrative prose remains conversational.

**Why:** Rules are normative documents. Without standardised modal verbs, "always X" and "never X" can be read as either absolute or aspirational — fine for two readers who share context, ambiguous for automation or new collaborators.

**Alternatives considered:**

- Apply across all `rules/*` files immediately (deferred — start with non-negotiables; expand as other rules files mature).
- Stay informal (rejected — gap against ISO 80000-1 / RFC 2119 conventions, and the substrate is now mature enough to merit formality).

**Implications:**

- New rules added to `rules/non-negotiables.md` MUST use a modal verb.
- Other `rules/*` files (`brand.md`, `deployment.md`, `stack.md`) MAY adopt the same convention when next edited; not retrofitted unless a real change is being made.
- A meaning-altering rewrite (vs vocabulary sharpening) is a decision-grade change — surfaced via the relevant tier's `pending.md`, not committed inline.

---

## 2026-04-28 — ADR Status Field Adopted on decisions.md

**Status:** Accepted

**Decision:** Every entry in `ops/decisions.md` carries a `Status` field — one of Accepted, Superseded by [date+title], On Hold, Deprecated, or Proposed. Inserted between the entry heading and the `Decision` line.

**Why:** Closes the only real gap against the Nygard ADR standard. Without a Status field, superseded decisions sit alongside current ones with no visual signal — the prose handles supersession but the structure doesn't, which means a fresh reader has to parse every entry to know what's still in force.

**Alternatives considered:**

- Move superseded entries to `decisions-archive.md` immediately (rejected — premature at 13 entries; revisit at 30+).
- Add `last_reviewed` frontmatter (rejected 2026-04-28 — adds ritual without signal once `updated_at` is reliable).

**Implications:**

- All future decision entries MUST start with a `**Status:**` line (codified in `system/md-style.md` ADR section).
- When a decision is superseded, the new decision's title is appended to the old entry's Status line; both entries remain in the file.
- At 30+ entries, split into `decisions-archive.md` for non-Accepted entries.

---

## 2026-04-28 — Supabase Context Store Lives in eq-solves-service-dev, Table is `context_files`

**Status:** Accepted

**Decision:** Confirm the runtime context store as table `context_files` (id, slug UNIQUE, filename, content, updated_at) inside the `eq-solves-service-dev` Supabase project (`urjhmkhbgaxrofurpbgc`) — not a separate dedicated context project, and not the table name `claude_context` that earlier memory carried.

**Why:** Live audit of Supabase 2026-04-28 returned the actual schema. The `context_files` table is the canonical runtime read source for all assistants. Creating a second project just for context would split costs and add an MCP target for no functional benefit while the row count is small (~30).

**Alternatives considered:**

- Dedicated `eq-context-store` Supabase project (rejected — context volume is tiny; multi-project sprawl is worse than co-tenancy with the product DB).
- Move to `claude_context` named table for clarity (rejected — rename would break the live sync action and existing MCP reads; the slug column already gives clarity).

**Implications:**

- All future Supabase MCP queries against the context store target table `context_files`, project `urjhmkhbgaxrofurpbgc`.
- The table is co-located with EQ Solves Service product data; tenant separation is by *table*, not project. This is acceptable because `context_files` has no `tenant_id` and is not part of the multi-tenant data plane.
- Update `system/architecture.md` next session to document this co-tenancy explicitly.

---

## 2026-04-28 — GitHub is the Source of Truth; Direct Supabase Writes are Emergency-Only

**Status:** Accepted

**Decision:** Chat (claude.ai web/mobile) drafts MD deltas; Cowork or Code commits them to GitHub; the sync action propagates to Supabase. Direct chat writes to the `context_files` Supabase table are reserved for emergencies only and must be reconciled to GitHub the same day.

**Why:** Bypassing GitHub destroys the audit trail that is the actual moat of eq-context. The git log is the substrate's value — once Supabase and GitHub drift, every "what did we decide and why" question has two possibly-conflicting answers.

**Alternatives considered:**

- Allow chat to write Supabase routinely (rejected — silently demotes git to a backup).
- Block all chat writes period (rejected — emergencies happen and the runtime store should reflect ground truth).

**Implications:**

- Add a non-negotiable: "GitHub is canonical. Supabase is cache." (see `rules/non-negotiables.md` follow-up — separate task).
- Any direct-Supabase write must append a flag to the relevant tier's `pending.md` titled "RECONCILE: <slug> written direct to Supabase on <date>".

---

## 2026-04-28 — "Done" in eq-context Means a Fresh Supabase updated_at, Nothing Else

**Status:** Accepted

**Decision:** A change is not "done" until the row in `context_files` shows a fresh `updated_at`. Terminal output, commit hashes, and "looks good" visual confirmation do not count.

**Why:** Three claims of completion in one session (2026-04-27/28) all turned out to be false on measurement: a wrong table name in memory, a "brief implemented" that hadn't been pushed, and a "push landed" where two of three files weren't actually edited. Each surface signal looked correct. Only the Supabase row's `updated_at` exposed the gap.

**Alternatives considered:**

- Trust git push output (rejected — push can succeed on the wrong content).
- Trust commit message intent (rejected — commit messages and diffs are routinely mismatched).

**Implications:**

- After every eq-context push, run the verification SQL (see `system/lessons.md` "Substrate Audit Query") and confirm the expected files show today's date.
- Stop using "done" as a status word in this repo unless the SQL has been run.

---

## 2026-04-17 — EQ Design Brief v1.3 Supersedes v1.2

**Status:** Accepted

**Decision:** Move to EQ Design Brief v1.3 as the canonical brand reference.

**Why:** v1.2 allowed three logo variants (Blue, White, Black) and had looser accessibility guidance. v1.3 simplifies to two variants (Blue, White), locks Aptos Display as the print companion to Plus Jakarta Sans web, and mandates WCAG AA minimum. Reducing variants reduces production drift.

**Alternatives considered:** Staying on v1.2 (rejected — Black variant was being misused on busy backgrounds; AA compliance was inconsistent).

**Implications:** All new documents use v1.3 palette and type scale. Old Black logo assets retained but flagged legacy — not for new work.

---

## 2026-04 — Three Supabase Projects, Not One

**Status:** Accepted — supersedes the prior non-negotiable "never spin up a new Supabase project" (which never had a discrete decision entry).

**Decision:** Run three Supabase projects — sks-labour (live), eq-solves-field (demo), eq-solves-service-dev (context store) — instead of the original one-project rule.

**Why:** SKS live production data and EQ demo experiments sharing a project is an unacceptable blast radius. Tenant prefixes (`sks_`, `eq_`) protect tables, but don't protect against a rogue schema migration or a bad DELETE run against the wrong table. Hard project boundaries do.

**Alternatives considered:**

- One project with tighter RLS (rejected — RLS doesn't protect against owner-level mistakes)
- Two projects, SKS vs EQ (rejected — context store belongs in its own paid project with its own access pattern)

**Implications:** Always confirm project ID before connecting. Never touch sks-labour without explicit "SKS live" instruction. The old non-negotiable "never spin up a new Supabase project" is retired — replaced by "never touch SKS live without explicit instruction".

---

## 2026-04-05 — SKS Receipt Tracker: localStorage over Supabase for v1

**Status:** Accepted

**Decision:** Ship with localStorage, migrate to Supabase when multi-user is needed.

**Why:** localStorage removes all backend complexity during battle-testing. Real usage will reveal actual data model needs — designing for Supabase upfront risks building the wrong schema.

**Alternatives considered:** Supabase from day one (rejected — adds auth complexity before value is proven); no persistence (rejected — data loss between sessions kills the use case).

**Implications:** Users must use Export → Backup JSON regularly to protect data until migration. Migration path is clean: data shape stays identical, only read/write functions swap out.

---

## 2026-04-05 — One Shared Cloudflare Worker for All Apps

**Status:** Accepted

**Decision:** Single `anthropic-proxy` worker shared across EQ Expenses, SKS Receipt Tracker, and all future tools needing Anthropic API access.

**Why:** The worker is stateless and generic — it has no app-specific logic. One worker means one API key, one deployment, one place to rotate credentials.

**Alternatives considered:** Per-app workers (rejected — multiplies maintenance for no benefit).

**Implications:** Every new tool that needs AI points at the same URL. Never create a new worker.

---

## 2026-04-05 — eq-context Folder in GitHub (not Supabase)

**Status:** Accepted — reinforced by 2026-04-28 "GitHub is the Source of Truth" decision.

**Decision:** Store the living project context (CLAUDE.md + subfiles) in a GitHub repo, not in Supabase or Claude Project files.

**Why:** GitHub provides version history (every update is a commit), is portable, readable as raw files, and works natively with Claude Code when that enters the workflow. Supabase is better for structured data, not documents. Claude Project files are read-only for Claude — can't be updated programmatically.

**Alternatives considered:**

- Supabase (rejected — no version history, overkill for documents)
- Claude Project files (rejected — read-only, can't be updated in-session)
- Single flat file (rejected — doesn't scale; mixes stable rules with fast-chan