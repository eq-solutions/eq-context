---
title: EQ Suite — outstanding items (whole-suite sweep)
date: 2026-08-28
owner: unassigned — TODAY.md has 0 active goals, so this is a full backlog, not a scoped sprint
scope: all 11 repo pending logs + ops/security-register.md + system/failures.md, swept fresh against origin/main @ 06480b1e
---

# EQ Suite — outstanding items (2026-08-28)

**No goal is currently set.** `system/TODAY.md` shows 0 active goals — you killed the last one 2026-08-12 and the file is deliberately left blank rather than borrow a stale one. That means this document has no basis to tell you what to prioritise; it's organised by **what each item is blocked on** (your call vs. just needs building vs. already decided) so you can cut your own slice.

~180 items below, swept fresh by 9 parallel agents reading the actual current files — not recalled from memory. Two things deliberately left out:

- The "not yet click-tested live by a person" verification note that trails almost every closed item in almost every repo (no live credentials in this sandboxed environment). Repeating it ~150 times would bury the real items — treat everything below as genuinely open, not just unverified.
- **A discrepancy worth one flag rather than three phantom bullets:** `cross-repo.md`'s log still names SEC-9/SEC-10/SEC-12 as open P0 findings, but the current security register — the actual status document, not a log — has no open entry for any of those numbers. Almost certainly already resolved and the log entry simply predates the fix. Not carried below as open; a 30-second confirm would close the loop if you want certainty.

---

## 🔴 Live risk, right now (2)

1. **SEC-1 — sks-nsw-labour's public key still reads real staff PII live** (`people`, `timesheets`, `leave_requests`, `audit_log`). Decision made 2026-06-05, reaffirmed 07-20 and 08-21: fix by decommissioning the app at cutover, not by hardening RLS on something retiring. The decommission's own gate — 3-4 consecutive clean SKS-parallel-run weeks — is still at 0/3-4. The decision stands; it just hasn't executed, and the leak is still live today.
2. **SEC-57 — an org-wide GitHub App holds write access to every repo, including eq-shell.** `grok-by-xai` carries `actions:write` (can dispatch fleet-wide live-DDL tenant migrations), `contents:write` (push to eq-shell `main` = production deploy in 2-4s), plus admin/workflow/PR write. Two more apps (`figma`, `cloudflare-workers-and-pages`) hold similar scope on unenumerated repos. Nobody has reviewed any of this since install (2026-05-19). Needs an org-level GitHub App access review.

---

## Needs your call — security & credentials (6)

- **SEC-3** — ehow's service_role key has never been rotated. No confirmed leak, hygiene-only — just needs a calm window picked.
- **SEC-18** — 7 secrets found stored `is_secret:false` in a 2026-07-30 sweep (`EQ_SERVICE_JWT_SECRET`, `EQ_SERVICE_HANDOFF_KEY`, `EQ_SERVICE_API_KEY`, `EQ_SECRET_SALT`, `EQ_SESSION_SALT`, `EQ_FIELD_HANDOFF_KEY`) beyond the 8 you already re-masked that day. Register's own note: "still not touched."
- **SEC-19** — SEC-1's companion code fix (drop `pin` from sks-nsw-labour's bulk roster `select=*`) is unmerged on branch `claude/sks-nsw-labour-security-30b634` — held by the explicit-deploy rule plus SEC-1's standing freeze on this repo.
- **SEC-24** — `EQ_SECRET_SALT` is one shared HMAC key across 4 live deploys (session cookies + the Shell↔Field iframe handoff on eq-shell/eq-field/sks-nsw-labour/eq-solves-service) — a leak on any one forges sessions suite-wide. Per-consumer key isolation started on eq-field, not finished elsewhere. Needs a cross-repo cutover + rotation-timing call.
- **SEC-63** — a Netlify **account-scope** secret (`SUPABASE_JWT_SECRET`, team `milmlow`) reaches eq-shell/eq-service/eq-field and was never logged in `ops/secrets-inventory.md`; its `dev`-context value is still unmasked. Needs a manual Netlify-dashboard delete — blocked so far by Claude Code's own classifier refusing to do it unattended.
- **SEC-65** — eq-field's `AUDIT_SB_KEY` is the live ehow **service_role** key, not the "publishable" key its own code comment claims. 4 live consumers currently treat it as safe to expose client-side.

---

## Needs your call — access control & identity architecture (cross-cutting)

- **`is_platform_admin` has no step-up/MFA gate on sensitive actions once granted** — unscoped bypass; flagged twice, confirmed it needs its own scoping session, not yet started.
- **`is_platform_admin` bypasses the Conversations UI permission gate** — no exception list or audit trail. RLS closes the real data exposure, but the UI still misleadingly offers the action.
- **No resource-/relationship-level authorization anywhere in the suite** — every permission check is role-based only; nothing checks whether a user actually owns/manages the specific record being acted on. Architectural, wants its own design pass.
- **Shell sign-out doesn't propagate to embedded Field/Service/Cards iframe sessions** — confirmed real for all three (Field: 7-day localStorage token; Service: indefinite auto-refreshing Supabase session; Cards: 4h self-renewing cookie). Cross-app propagation needs a scope/priority call across 4 repos.
- **"One access-control screen" — your own idea, not yet designed** — unifying Field's and Shell's separate permission systems (~86 total switches) into one screen. Needs a proper design pass before any build.
- **Access-Model Phase 2 ("One admin") / Phase 3 (permission guardrails) still fully locked** — deliberately parked pending the SKS parallel-run proving period (see SEC-1's gate above — same 0/3-4 clean weeks). Phase 3 alone would convert 65 real `isManager` call-sites across 11 files; Phase 2 is untouched even after two narrow Phase-3 carve-outs were separately approved.
- **Nav-visibility drift has no shared source of truth** — two options on the table (a shared roles-derived config vs. a lighter review checklist), not decided. Reinforced by a second, more serious incident 2026-08-16 (Service's Sidebar gate found tier-inverted).
- **S2 — `entity-actions.ts`/`entity-patch.ts` gate asset writes on the CRM tier (`entity.edit`/`entity.delete`) instead of `equipment.edit`/`equipment.view`** — aligned by coincidence today, not design. Re-point the keys, or document the CRM-tiering as deliberate.
- **Labour-hire intake front door: merge AdminWorkerInviteForm and LabourHireIntakeTool, or keep both?** — scoped, explicitly not decided.
- **No live access-revoke exists anywhere** — role/entitlement changes only take effect on next login. SKS's national-rollout requirement is instant revoke; needs a real per-request active-flag design.

---

## Needs your call — eq-shell (7)

- **Shell's Internal Document Sign-off Register review flow has no buttons** — approve and reject for staged rows are fully built and network-reachable, but nothing in the UI calls either. Wire it up or retire it.
- **No server-side `quotes.view` check on `eq_list_quotes`/`eq_get_quote_detail`** — any authenticated tenant member can call these RPCs directly regardless of role. You chose to build ownership-scoping first instead of closing this — still open.
- **Email sign-in door only reaches 22 of 73 worker accounts** — 58 admin-typed emails were never verified by the worker and can't safely become logins without a verified add-email flow.
- **Self-serve tenant provisioning still has no real prod dry run** — `shell_control.provision_tokens` was 0 rows as of last check. Your own stated gate: run a real link through Admin → Tenants → Cards before sending one to an actual prospect.
- **credentials-canonical-sync is broken and not running** — Cards licence/credential updates never reach the older SKS compliance view. Revive + fix, or retire in favour of Field's live-read pattern?
- **Site→customer backfill gap** — only 117 of 250 SKS canonical sites carry a `customer_id`, leaving Service's customer-rollup reports blank for the rest. A Shell/canonical-spine data backfill, not a Service bug.
- **eq-cards' own jvkn migrations still have no governed apply path** — 29 of 161 tracked migration files don't match the known ledger-naming convention; 3 shapes scoped, no direction picked.

---

## Needs your call — eq-field / SKS (9)

- **Revert PR #656, or leave v3.5.461 live?** — the licence-expiry supervisor-gate PR was squash-merged (auto-deploys) without your explicit go-ahead. Recommendation was revert; still unanswered.
- **Documents to Sign has no functional fallback for a persistent load failure** — once a document has a PDF twin, "go back and try again" just re-runs the same failing viewer path. You already started a separate session on this (task_445c878c).
- **Sign-in audit-logging fix needs an explicit go-ahead** — rolling repeat sign-in-check writes into one row would shrink the audit log at the source, but touches a live security control. Session ended on an unanswered "scope now or leave parked."
- **"Safety has disappeared now" — your report, never diagnosed** — raised right at a 2026-08-19 session close after an unrelated boot-order fix shipped. Next step: confirm live `APP_VERSION` and whether the whole Safety nav group or just Site Audits is missing.
- **Accessibility pass — status unknown since before the old demo-branch/main split** — never confirmed shipped or dropped. Still a goal, or not?
- **Bus-factor runbook — asked for a 4th consecutive time, still doesn't exist** — "what to do if Royce is out two weeks." Needs scheduling, or an explicit call that it's not a priority.
- **Desktop "cramped" complaint's likely real root cause still unfixed** — `--eq-body-line-height: 1.5` is defined in `tokens.css` but never applied to `body`. The letter-spacing fix that shipped (PR #713) was a different, smaller issue. Desktop polish has been open since the first audit (2026-05-13) — 3+ audits, zero movement.
- **Site internal contacts missing real data for 6 of 7 SKS sites** — only Equinix SY5 has real "Ask for/Backup" contact data. CA1/SY1/SY2/SY3/SY4/SY9 need real names + numbers from you via eq-shell's Edit Site modal.
- **Aiden Crowley's SKS record still carries stale test data from a bug-reproduction thread** — fake job title, emergency contact, start date, cleared birthday. Needs your go on timing to clear it and do a real re-save.

---

## Needs your call — eq-cards (5)

- **3-way visual design picker (Linear / Wallet / Photo-first) needs your own resolve-or-keep call** — triples the maintenance surface of the most-used screens, in tension with "boring beats clever."
- **QR code for on-site sign-in — build or drop** — needs EQ Field to build a scanner too; tap demand is now being tracked to inform the call.
- **Standalone Cards "personal wallet" signup still has zero email capture** — the nudge in PR #1125 only covers the Shell-login path. Deferred on 90/10 SKS-focus reasoning; revisit if standalone signups grow.
- **Cross-session message probe — needs your confirmation it was you** — any Claude Code session on this machine can currently read another session's full transcript and inject messages that render indistinguishably from a normal turn.
- **Doc-freshness / CHANGELOG process proposed, not built or decided** — no guard exists against the ~87-day doc drift a recent sprint found. A checkpoint-based CHANGELOG process is recommended, undecided.

---

## Needs your call — eq-solves-service (7)

- **Suppliers/site-credentials feature provably broken on all 3 layers (list, decrypt, create/update)** — 3 candidate schemas exist, none wired together. Needs a design call on which schema to consolidate onto before any code changes.
- **Calendar digest sending still paused** (`SUPERVISOR_DIGEST_PAUSED=true`) — 21 people currently eligible, including you and a `dev@eq.solutions` account whose manager-role is itself questionable. PM calendar is also empty right now, so un-pausing today would send nothing real yet.
- **Decide whether to turn on scheduled notifications** — groundwork (PR #619) is applied live to ehow but deliberately left switched off. A business decision, unresolved since 2026-07-28.
- **npm audit security-scanner CI check still red** — 16 high-severity findings, all devDependency-only chains unreachable from production code. Options: `npm audit --omit=dev` in CI, or leave red and document why.
- **Mojibake asset-name corruption (47 rows, 3 sites) needs you to run one SQL statement directly** — automated attempts silently failed twice. On ehow: `UPDATE app_data.assets SET name = replace(name, 'Â ', ' ') WHERE name ~ 'Â';`
- **"Approved by" sign-off has no UI to capture it** — the DB columns (`signature_technician_url`/`signature_site_url`/`signature_initials`) have sat unused since migration 0068. Real feature gap; your call on whether to build signature capture.
- **Cold-start infra decision still open** — whether serverless cold start is bad enough to justify an always-on/edge runtime change. Not pursued without your go-ahead.

---

## Needs your call — eq-solves-intake (4)

- **3 site-duplicate groups still need your manual pick** — SYD10, SYD11, M5 Motorway East, plus three 3-way groups have no clear survivor without a human call (a newer usage-check may have already resolved some).
- **Site-resolver "enforcing" phase needs your match-strictness call** — the write-time duplicate resolver only watches today; switching it to redirect writes is a business decision (address-match vs. mandated canonical code).
- **Seed a flagged duplicate pair on ehow for a demo** — the adjudication console has zero flagged rows to click through; inserting a synthetic one needs your explicit go-ahead to write to production SKS data.
- **`ANTHROPIC_API_KEY` still unconfirmed live on sks-canonical** — the Ask tab / gap-suggest / AI-adjudication code is wired correctly but has zero logged invocations. Needs you to type a question into the live Ask tab and confirm.

---

## Needs your call — small repos (4)

- **sks — max-uses cap on self-join codes, scoped and held** — fully scoped (~1 hour of work), but you chose to hold until a link actually leaks or becomes a recurring worry.
- **sks — SKS→canonical migration runbook not built** — load order, crosswalk-completion checklist, two-gate reconciliation spec were offered, never written.
- **sks — identity crosswalk incomplete** — 25 unlinked people, 11 unlinked sites, 9/6/6 unmatched names need a human who knows them. Pay-critical, no automation possible.
- **sks — EQ↔SKS data-ownership arrangement not named** — whose worker data, under what arrangement, what happens if you leave — flagged as worth naming before Cards runs all of SKS NSW.

---

## Open PRs awaiting a merge/dispatch decision

| PR | Repo | What | Status |
|---|---|---|---|
| [#1654](https://github.com/eq-solutions/eq-shell/pull/1654) | eq-shell | 4 more divergent staff/shell login names — audit-trail migration | Data fixes already live; PR just needs a merge call |
| [#1637](https://github.com/eq-solutions/eq-shell/pull/1637) | eq-shell | Multi-project-code sites (MOD10-style) create-UI | Open for review |
| [#1381](https://github.com/eq-solutions/eq-shell/pull/1381) | eq-shell | 4 PII/contact-detail leaks fixed (compliance report, licence badges, join-request notify, customer search) | Held pending your explicit go — touches who-can-see-what |
| [#1590](https://github.com/eq-solutions/eq-shell/pull/1590) | eq-shell | `buildStaffPatch` — Zemi Asri data-clobber companion fix | Not yet merged |
| [#1294](https://github.com/eq-solutions/eq-shell/pull/1294) + [eq-cards#221](https://github.com/eq-solutions/eq-cards/pull/221) | eq-shell + eq-cards | Cards SSO broker fix | Blocked on generating + setting `EQ_CARDS_HANDOFF_KEY` on both Netlify projects before either can deploy |
| [#705](https://github.com/eq-solutions/eq-field/pull/705) | eq-field | Timesheet/leave write-side RLS (any signed-in worker can edit another's content) | Merged but blocked on an unlinked-staff data problem — not eq-field's call to dispatch |
| [#757](https://github.com/eq-solutions/eq-field/pull/757) | eq-field | Same RLS migration, draft form | Dispatch held on 38 of 107 SKS staff still having no linked login |
| [#821](https://github.com/eq-solutions/eq-field/issues/821) / [#822](https://github.com/eq-solutions/eq-field/issues/822) | eq-field | Two PRs collided on the same version number (v3.5.592) | Neither merged; whichever lands next needs renumbering |
| [#791](https://github.com/eq-solutions/eq-solves-service/pull/791) | eq-solves-service | Report-resend flow, revision-reason box | Deliberately held — emails real customers, needs your explicit go |
| [#1190](https://github.com/eq-solutions/eq-solves-intake/pull/1190) / [#106](https://github.com/eq-solutions/eq-solves-intake/pull/106) | eq-solves-intake | 2 PRs awaiting review | Edge-function deploy + migration dispatch need your go once merged (live Anthropic API calls + ehow schema changes) |
| [#300 follow-up](https://github.com/eq-solutions/eq-cards) | eq-cards | 10 `eq_cards_*` functions still carry excess anon/PUBLIC EXECUTE grants | Not exploitable, just unnecessary surface — cleanup in progress in a separate session |
| 2 stale branches | eq-solves-service / eq-solves-intake | `claude/service-canonical-identity-phase3-4` (re-keys shell-auth JWT, remaps 5 SKS users' FK refs, marked "DO NOT DEPLOY without Royce's go") + an eq-intake quality-guardian worktree (engine live, no admin UI) | Ship or shelve — your call |
| 5 Dependabot PRs | eq-solves-service | vitejs/plugin-react, sentry/nextjs, react-dom, eslint-config-next, @eq-solutions packages | Never reviewed |

---

## Ready to build — security register (25, no decision needed)

The register already tags these as straightforward — the fix pattern is known, nothing is waiting on a business call:

SEC-5 (always-true write policies, latent — post-launch cleanup) · SEC-6 (no rate throttle on `context_proposals` anon insert) · SEC-7 (unpin `search_path` on `public.eq_format_au_mobile`, jvkn) · SEC-26 residual (33 data-changing eq-shell endpoints outside the deactivated-account write-gate, need one-by-one review) · SEC-34 (scope `shell_control.user_invites` reads to admins) · SEC-35 (`REVOKE SELECT` on 7 unused-anon-grant `field_*` views, ehow) · SEC-36 (4 zaap tables with stray anon-only policies, no matching `authenticated` policy) · SEC-39 (bind `mint-supabase-jwt`/Field's `verify-shell-token` to a `source_app`/`aud` check) · SEC-40 (tighten Field's CSP `frame-ancestors` off all of `*.netlify.app`) · SEC-43 (role-gate 6 quote-mutation RPCs, same pattern as SEC-41/42/47) · SEC-48 (repoint 4 licence-photos storage policies from `user_metadata` to `app_metadata`) · SEC-49 (add a role check to `service.upsert_site_credential`) · SEC-52 (promote service.eq.solutions CSP off report-only) · SEC-53 (clean CSP allow-lists referencing the deleted `ktmjmdzqrogauaevbktn` project + retired quotes.eq.solutions) · SEC-54 (add an explicit same-origin assertion to eq-service's mutating routes) · SEC-55 (sanitize raw search terms before they hit PostgREST filter strings) · SEC-56 (fix `apply-service-migrations.yml`'s false "pauses for approval" PR comment — posts on 38 of last 100 PRs) · SEC-58 (update `CONTROL-PLANE-LEDGER.md` — tracks only 84 of 131 migration files, one misfiled migration governed by neither pipeline) · SEC-59 (revoke TRUNCATE on 9 `shell_control` tables) · SEC-62 (stop the standard "delete+recreate is_secret:true" secret-remediation recipe from re-leaking a fresh unmasked `dev` row every time it's used) · SEC-64 (fix `ops/secrets-inventory.md` — maps eq-field's `CANONICAL_SERVICE_ROLE_KEY` to the wrong project) · SEC-66 (add 6 missing Tier-1 secret names to eq-field's Sentry scrubber allowlist) · SEC-67 (clean up dead Supabase project refs still stored in eq-shell/sks-nsw-labour env vars) · SEC-68 (low urgency — real secrets as Actions secrets on the public eq-context repo, well-mitigated already) · SEC-69 (add explicit `::add-mask::` where `SENTRY_DSN` gets sliced into `$GITHUB_ENV` across 9 workflows).

## Ready to build — other (6, no decision needed)

- **`field_people_removed_iud` tenant-tautology bug** — fails open on both ehow and zaap; a trigger fires through its attachment regardless of EXECUTE grants, so SEC-13's REVOKE didn't close it.
- **33 data-changing endpoints suite-wide still bypass the deactivated-account guard** — excluded from the original sweep because a crude scan couldn't cleanly tell reads from writes or background jobs. Needs one-by-one triage.
- **46 of 109 same-origin-check gaps still open suite-wide** — any page on another EQ subdomain could trigger these actions using a manager's shared session cookie. Only 5 near-identical twins were fixed; the remaining 46 span account-security, GM Reports, Labour Hire, Intake, uploads, and invites.
- **Type-checking gap in ~17 places in eq-solves-service's DB layer** — a view with custom save-behaviour isn't covered by the auto-generated schema-description file, so writes there go through untyped "trust me" overrides.
- **Shared `@eq-solutions/ui` Table component's mobile word-wrap bug** — unfixed everywhere except one patched page (Maintenance, Assets, Job Plans, Contract Scope, Test Records, etc. all still affected). Scoped as an eq-ui repo change.
- **Unswept: whether ~22 other canonical objects share the "trigger references a column the view doesn't expose" bug class** — only `customers`/`sites`/`assets` were checked after the 2026-07-27 fix that found it.

---

## Substrate / tooling reliability (affects every future session, not product-facing)

**From the failure register:**
- **F4 — nothing watches the product.** The guard is "planned, not yet built." Signals not yet wired into digest.md: prestarts stalled, safety modules at 0, non-Royce write share, `last_login_at` never populated.
- **F5 — an ungoverned shadow memory overrode the canonical contract.** Only 1 of 7 memory layers is governed; the patch meant to prevent drift is what routed a session to a stale URL. Needs `memory-coverage.yml` (CI) + collapsing the other 6 layers to thin pointers.
- **F9 — concurrent-session git races, partially guarded.** The Claude-Code-tool-call path is fully covered; any git command run outside a tool call (a human terminal, a Cowork-emitted script a human runs) has no hook watching it, by construction.
- **F11 — if the digest-refresh watchdog itself ever dies, nothing notices.** It currently catches a failing cron, but only because it runs inside that same cron. Acknowledged as a harder problem, not yet filed as an action.
- **F12 — settings.json vs. settings.template.json drift, hit 3 times now, still no standing check.**
- **F13 — mostly closed.** One live sub-question left: flip `SUBSTRATE_HONESTY_STRICT=1` to make the deploy-posture CI scan itself blocking (it would also block on unrelated network-dependent liveness probes) — undecided.
- **F15 — eq-cards shared-checkout Edit/Write vector is guarded; the git-verb variant (a correctly-scoped commit still landing on whatever branch the shared root happens to be on) is deliberately still open**, smaller and separate.

**From eq-context's own pending log:**
- **`guard.js` is unversioned, untested, and cites a spec file that doesn't exist** — underlies several of the guard bugs below; unlike the governed `hooks/*.py`, it has zero test coverage.
- **`stale-main-gate` blocked 6 commits in a genuinely up-to-date isolated clone** — looks like it checks a hardcoded shared-checkout path instead of the invocation's real repo.
- **`brief-gate` exemption regex doesn't cover the post-split pending files** — still only matches the old flat `eq/pending.md`, so edits to `eq/pending/<repo>.md` get blocked without a `/brief` flag.
- **The safety guard meant to block risky git ops also blocks them in fresh, safe isolated clones** — and once blocked a session-log write that merely *described* the bug.
- **Org-level `EQ_CONTEXT_PAT` has never had a value set** — confirmed via live logs the Authorization header is genuinely empty, breaking merge notifications from all 4 product repos. Needs you to paste a value into the org secret.
- **`index-drift.yml` cron has failed 2 consecutive scheduled runs, never investigated** — last success 2026-08-20.
- **No claim mechanism for digest-surfaced findings** — 5 findings were independently fixed twice by different concurrent sessions in one sitting. `TODAY.md`'s empty `CLAIMS` block could serve this, isn't used that way yet.
- **`C:\Projects\CLAUDE.md` is still the only home for Rule 0/0.5 and the load-bearing-facts list** — not version-controlled, no CI, invisible to any session not rooted in that exact folder. Same shadow-memory class as F5.
- **A substrate-architecture upgrade scoped in a 2026-07-26 Chat conversation has no trace anywhere in this repo** — needs you to pull or re-summarise that original conversation before it's buildable.
- **GitHub MCP's 404s on private EQ repos still unresolved** — one proposed fix ("re-authorize the GitHub App") was already disproved by an earlier investigation, which pointed at Copilot licensing instead.
- **Stale-cull sweep of ~90 open pending items older than 30 days never run** — would close dead items and merge duplicate threads. Flagged as a good standalone session.
- **No restore drill has ever been run against the eq-context-owned ehow backup** — RTO/RPO has never actually been measured.
- **gitleaks pre-commit hook to prevent PAT exposure still not built**, and **`C:\Projects\.git-credentials` still needs updating with the new PAT after rotation** — both logged 2026-06-28, no confirmed follow-up since.

---

## Already decided by you — deliberately deferred, listed for visibility only

- **SEC-11 / SEC-14** — no approval-gate protection on `tenant-migrate.yml` / `apply-service-migrations.yml` production environments. You already accepted this (a required-reviewer plan isn't worth buying when you're the sole collaborator); docs were corrected instead of the posture.
- **SEC-27** — `app_data.licences` RLS is tenant-only (same latent shape timesheets had before their fix), currently harmless only because no grant exists yet. You chose log-only — but the RLS shape should still get fixed *before* anyone adds that grant.
- **SEC-60 residual** — org-wide 2FA requirement, branch protection on the other 5 repos, SHA-pinning third-party Actions. You picked the lowest-disruption subset already (eq-service branch protection + secret scanning on 3 public repos, done 2026-08-24); the rest is a deliberate future pass.
- **SEC-8** — `pg_net` in public schema on sks-labour. Moot the moment SEC-1's decommission actually happens.
- **Access-Model Phase 2/3, SKS's parallel-run gate** — see the access-control section above; this is the same 0/3-4 clean-weeks gate as SEC-1, already decided, just not yet met.

---

*Compiled from a 9-agent parallel sweep of all 11 `eq/pending/*.md` files, `ops/security-register.md`, and `system/failures.md` against eq-context @ `06480b1e`. Items are as current as the substrate itself — a handful may have closed in a session running concurrently with this sweep. If something below looks wrong, the live system wins, not this file.*
