---
title: eq-shell — full open-work triage and sprint
owner: Royce Milmlow
created: 2026-08-29
last_updated: 2026-08-30
scope: A full triage of every open (`- [ ]`) item in eq/pending/eq-shell.md and eq/pending/cross-repo.md, sorted into what's actually actionable vs. what's noise. No TODAY.md goal exists to prioritise against — this is a menu, not a plan with a deadline.
read_priority: high
status: live
---

# eq-shell — full open-work triage and sprint

## How this was built

Royce asked for "a sprint for this repo, and prompt for any [items] outside this." A full read of `eq/pending/eq-shell.md` (2049 lines) and `eq/pending/cross-repo.md` (992 lines) found **367 open checklist items** — going back to 2026-06-05. That's not a sprint, that's three months of accumulated backlog. Triaged into four buckets before building anything:

| Bucket | Count | What it means |
|---|---|---|
| **A — Real, current, actionable** | 60 | Genuinely open work or decisions. This doc. |
| **B — Verification debt** | 206 | Shipped and working, just never personally click-tested by a signed-in person (structural — this environment has no login credentials for most of the suite). Not a sign anything's broken. |
| **C — Deliberately deferred/parked/declined** | 43 | Royce already made this call. Don't re-raise without new information. |
| **D — Likely stale or superseded** | 56 | Old enough, or explicitly contradicted by later entries, that it's probably a cleanup-candidate rather than live work. |

Full bucket-by-bucket detail (all 367 items, not just the 60 below) is preserved in the extraction transcript, not duplicated into this file — ask if you want the raw B/C/D lists. **Recommend a separate housekeeping pass to archive Buckets C and D out of the live pending.md** per its own archive rule — 99 items (27% of the whole file) are sitting in the "still open" doc when they're actually resolved-as-decided or stale. Not done as part of this sprint; flagged as its own task.

**Staleness caveat**: this is pulled from `pending.md`, and this whole session has shown extremely high concurrent-session write volume (multiple sessions committing to the same substrate within minutes of each other, all week). One item below (PR #1654) was already resolved by the time this doc was written — corrected inline. Treat every item here as "true as of the last pending.md update," not "true right now" — worth a quick live re-check before sinking real effort into any single one, especially before assuming it's still blocking.

**Update 2026-08-30**: 2 items below have since shipped — the eq-cards migration-pipeline decision (Security gaps → "Field writes to the SKS database through its own door") got a direction, got built, and is merged+live ([eq-shell#1671](https://github.com/eq-solutions/eq-shell/pull/1671) + [eq-cards#330](https://github.com/eq-solutions/eq-cards/pull/330)); the pending.md archive cleanup recommended above is done (41 of 43 settled items closed, 13 sections archived — see `sessions/2026-08-30.md`). Both struck through in place below. Royce then asked to prioritize the rest into an actual execution order — that's the new section right after this one.

---

## Execution order

Value-vs-effort, not alphabetical. "Effort" is wall-clock for a focused session, not calendar time — several waves can run in parallel with each other since they don't share files or touch the same systems.

### Wave 1 — ship now (0 new work, 3 decisions)
Already built, just sitting on a merge call. Same shape as #1654/#1671 above — review, or just "merge" if you trust the description.
1. [PR #1637](https://github.com/eq-solutions/eq-shell/pull/1637) — multi-project-code sites. Zero live rows depend on it either way — lowest-stakes of the three.
2. [PR #1381](https://github.com/eq-solutions/eq-shell/pull/1381) — 4 PII/contact-detail leaks fixed. Highest-value of the three (real data exposure, already 6 weeks held for exactly this go-ahead).
3. [PR #1310](https://github.com/eq-solutions/eq-shell/pull/1310) — quote-attachment direct-to-storage. Needs your specific error message before it can move, not just a merge click.

### Wave 2 — quick wins (~1 hour total, high value)
Small, independent, mostly security hygiene. Good candidates to just knock out in one sitting.
1. **Cloudflare 2FA** — 2-minute dashboard click, closes a single-point-of-failure on DNS for the whole suite.
2. **Confirm SEC-63's dev secret is actually deleted** — you said you'd do it via the Netlify dashboard; never confirmed back.
3. **Confirm `ENABLE_PHONE_OTP` is still `true`** — gates a live signup door, blocked from checking via the classifier, needs your dashboard read.
4. **Re-confirm the 3 already-tracked P0 findings' current status** in `ops/security-register.md` — 5-minute read, closes the loop on whether national-scale plans are building on solid ground.

### Wave 3 — this week (bounded, single-session fixes)
**Update 30 Aug**: 3 of 6 fully done this session — struck through below.
1. ~~**2 blank-name worker records**~~ — **done.** Both identified, nothing to backfill (phone-only signups, no name anywhere in the source data).
2. ~~**`eq_revoke_session`'s access-group blind spot**~~ — **done.** [eq-shell#1678](https://github.com/eq-solutions/eq-shell/pull/1678), merged + live.
3. ~~**2 orphaned auth users on jvkn**~~ — turned out bigger than expected, but **done anyway.** Root-caused a real recurring bug (`handle_phone_dedup()` misses phones stored on `shell_control.users` without being the person's actual auth identity) — count had grown to 4 with no code change. Fixed on your go: [eq-shell#1679](https://github.com/eq-solutions/eq-shell/pull/1679), merged + live. The 4 already-orphaned rows themselves left as-is — inert, no live harm.
4. **"Rollback" button** — quick decision (build for real vs. remove), then a small build either way.
5. **Mobile Home's 10-minute cache mismatch** — quick decision (shrink TTL vs. staleness stamp), then a small fix.
6. **6 Equinix sites' contact data** — blocked on you supplying real names/numbers, not a build task.

### Wave 4 — needs a dedicated session (real scope, still single-repo)
Not quick wins — each of these is a proper piece of engineering work on its own.
**Update 30 Aug**: 2 of 6 done. Struck through below.
1. ~~**33 endpoints missing the shared permission-check helper**~~ — **fully closed, and it was never 13 remaining.** 33 → 24 (6 already fixed independently) → a full per-file read of those 24 found only 11 were real gaps. Fixed: 8 platform-admin routes (led by `admin-tenants.ts`'s permanent tenant-delete) + 3 self-scoped credential-set routes (a deactivated user could otherwise still set their own PIN/email/prefs). [eq-shell#1682](https://github.com/eq-solutions/eq-shell/pull/1682), merged + live. The other 13 were always false positives — see Security gaps below for the breakdown. Zero remain.
2. ~~**`quotes.view` server-side check + quote status/notes RPC verification**~~ — **done**, [eq-shell#1681](https://github.com/eq-solutions/eq-shell/pull/1681), merged + live. The "verification" half turned out worse than unverified — see Security gaps below.
3. **`EQ_SECRET_SALT` rotation rehearsal** — the single top production-readiness risk flagged this whole sprint; worth being the first "dedicated session" item picked up.
4. ~~**Function-grant safety net's `app_data` blind spot**~~ — **fully closed: built, merged, dispatched, and verified live.** [eq-shell#1680](https://github.com/eq-solutions/eq-shell/pull/1680), merged. Turned out to be two gaps: zaap/ehow were also running an outdated, more dangerous version of the underlying trigger (the exact failure shape behind the eq-cards #0111 outage) — jvkn had already been quietly upgraded past it, live, undocumented. Ported that fix to the tenant planes, added `app_data`, and dispatched to both zaap and ehow 2026-08-30 (`tenant-migrate.yml` run [33303604383](https://github.com/eq-solutions/eq-shell/actions/runs/33303604383)) — applied clean, 0 errors, 0 checksum drift. Verified post-apply: the 4 quotes RPCs from #1681 that rode the same dispatch (the first functions the new auto-restore logic ever touched in production) kept their `authenticated` grant alongside `service_role`, not just stripped to service-role-only — the exact failure mode this fix exists to prevent, confirmed not to have recurred.
5. **Resend/nudge action for 24 unlinked SKS staff** — needs your human pass over the list first, then the build.
6. **Field's own migrations onto a governed pipeline** — same shape as the eq-cards work just shipped; Field is the other repo writing to a shared database with no governed apply path.

### Wave 5 — needs your decision before anything builds
No code should move until you've picked a direction on these.
1. **S2**: re-point the asset-write permission keys, or document the current CRM-tiering as deliberate?
2. **`ai.use` key**: enforce it, or retire it? Re-flagged across 4+ sessions with no owner.
3. **Security-groups Phase 4**: still wanted, or superseded by the `field.manage_*` work?
4. **No self-service email correction**: worth building, or leave as admin-only?
5. **Nothing alerts on sign-in lockouts**: where should an alert land?

### Wave 6 — bigger initiatives (needs its own scoping pass first, not a slot in this sprint)
Real, but too big to just "pick up" — each of these deserves its own brief before any work starts.
1. Repo-wide lint debt (990+ errors, doubling every few weeks).
2. 24 untriaged security-audit findings (4 P0s among them) — sitting in a Claude.ai artifact, no repo-doc home.
3. 206 Supabase security advisories on ehow.
4. National-scale access-revoke design (instant deactivation, not next-login).
5. Off-platform backup for ehow.
6. Self-serve provisioning's mandatory dry run before it's used on a real prospect.

---

## Ready for your call — PRs sitting on a merge decision

- ~~**PR #1654** — 4 more divergent staff/shell login names resolved~~ — **MERGED AND LIVE as of this session** (`46719f2a`, confirmed via commit-ancestry). Stale in pending.md, corrected here.
- **[PR #1637](https://github.com/eq-solutions/eq-shell/pull/1637)** — multi-project-code sites (add/delete `site_projects` RPCs + UI). Complete, open for review since 2026-08-27. `app_data.site_projects` has zero live rows either way, so nothing's blocked by leaving it — but it's just sitting there.
- **PR #1381** — 4 places showing worker/contact PII to roles that shouldn't see it. Explicitly held pending your go since it touches who-can-see-what. 2026-08-16, six weeks open.
- **PR #1310** — quote-attachment direct-to-storage. You hit real issues testing it; storage CORS and deploy state were both ruled out as the cause, but the actual failure was never pinned down pending a specific error message from you. 2026-08-12.

## Security gaps — real, not yet closed

- **`EQ_SECRET_SALT` rotation readiness never verified.** Flagged as the single top production-readiness risk for the whole suite — it's the fallback signing key for session cookies, tenant JWTs, and the quotes/cards/internal-token families (see this repo's own CLAUDE.md). Nobody has actually rehearsed a rotation. 2026-08-11.
- **46 more actions share the same missing-origin-check gap** a 2026-08-16 fix closed elsewhere — a compromised sibling `*.eq.solutions` site could trigger real admin actions via the shared cookie. Already handed off, in progress in separate sessions — worth confirming status before re-scoping.
- **SEC-63: a dev-context `SUPABASE_JWT_SECRET` plaintext leak** — you chose to delete it yourself via the Netlify dashboard rather than retry past a blocking classifier. Never confirmed done. 2026-08-24.
- **Anon-EXECUTE grant on 2 unallowlisted SECURITY DEFINER functions** on the control plane — spun off as its own task, status unconfirmed. 2026-08-19.
- ~~**`eq_revoke_session`** has the same access-group blind spot as an already-fixed sibling function.~~ **Done** — [eq-shell#1678](https://github.com/eq-solutions/eq-shell/pull/1678), merged + live. 2026-08-16 → 2026-08-30.
- ~~**Orphaned auth users on jvkn**~~ — **done.** Root-caused a real recurring bug (`handle_phone_dedup()` misses phones stored on `shell_control.users` without being the person's actual auth identity — count had grown 2→4 with zero code change) and fixed on your go: [eq-shell#1679](https://github.com/eq-solutions/eq-shell/pull/1679), merged + live. Detail: memory `phone-dedup-misses-shell-only-phone`. 2026-08-23 → 2026-08-30.
- ~~**No server-side `quotes.view` check**~~ — **done**, [eq-shell#1681](https://github.com/eq-solutions/eq-shell/pull/1681) (migration 0296), merged + live. 2026-08-23 → 2026-08-30.
- ~~**Quote status/notes write functions never verified for role checks**~~ — **checked, and it was worse than unverified.** Neither `eq_update_quote_status` nor `eq_add_quote_note` had *any* role check at all, only tenant scoping — a write path, not a read gap (status changes fire real downstream events). Fixed in the same PR (migration 0297), gated on `quotes.create`. 2026-08-23 → 2026-08-30.
- ~~**Database function-grant safety net only covers the `public` schema**~~ — **the real story was bigger, and it's now fully closed.** The live trigger (`eq_enforce_function_privacy`) on zaap/ehow was still running the *original* version — strips a function's grants on every edit with no automatic restoration, the exact shape that caused the eq-cards #0111 outage. jvkn had already been upgraded to a smarter auto-restoring version, live, on 2026-08-25 — but that upgrade was never committed to the repo. [eq-shell#1680](https://github.com/eq-solutions/eq-shell/pull/1680) ports it to the tenant planes and adds `app_data` coverage (61 functions, 14 with real live `authenticated` grants — confirmed the "safe by default" assumption in the original fix's own comment no longer holds). Merged, then dispatched to both zaap and ehow 2026-08-30 — applied clean, and the live grants on the first functions it touched (the #1681 quotes RPCs, riding the same dispatch) were spot-checked and confirmed intact. 2026-08-23 → 2026-08-30.
- ~~**33 data-changing endpoints don't use the shared permission-check helper**~~ — **fully closed, and it was never 13 remaining.** Audit corrected 33 → 24 (6 already fixed independently), then a full per-file read of those 24 — actual auth logic, not just grepping for the helper's name — found only 11 were real gaps: [eq-shell#1682](https://github.com/eq-solutions/eq-shell/pull/1682), merged + live. The other 13 were always false positives: pure reads a crude scan mislabelled, or files already doing an equivalent inline `active` check by hand instead of calling the named helper — spot-verified directly on the 3 highest-stakes ones (`mint-supabase-jwt.ts`, `switch-tenant.ts`, `token-exchange.ts`), confirming the check runs before the sensitive mint/switch, not just present somewhere in the file. One borderline non-issue noted, not fixed: `shell-logout.ts` mechanically matches the pattern, but gating logout on "still active" protects nothing — the mutation is the revocation itself. A first re-audit pass was run against a stale, non-`main` local checkout and wrongly reported 0 gaps *including the 11 already-fixed ones* — caught by cross-checking against a fresh worktree off verified `origin/main` before trusting it. Zero remain. Full detail: `ops/security-register.md` SEC-26. 2026-08-15 → 2026-08-30.
- **Cloudflare account has no 2FA** — `royce@eq.solutions` is the sole Super Administrator over DNS for the entire 4-app suite. 2-minute fix, flagged after last month's DNS outage. 2026-07-22.
- **Field writes to the SKS database through its own door**, outside eq-shell's governed migration pipeline — two known fixes went in by hand because Field has no equivalent approval pipeline. eq-cards had the identical gap; that one's now built and merged ([eq-shell#1671](https://github.com/eq-solutions/eq-shell/pull/1671) + [eq-cards#330](https://github.com/eq-solutions/eq-cards/pull/330), 2026-08-30) — Field's own version of the same fix is now Wave 4 below, same mechanism ready to reuse. 2026-07-21.
- **Several company repos found sitting fully public** (EQ Context, EQ UI, EQ Quotes, EQ Contracts, the old SKS labour app, smaller internal libraries) — given SKS's contractual private-repo requirement, worth a deliberate check whether this is still true. 2026-07-20.
- **No live access-revoke** — role/entitlement changes only take effect on next login. SKS's stated national-rollout requirement is instant. Needs a real design (per-request active-check instead of trusting the session cookie). 2026-07-23.
- **🟠 MFA-bypass posture** — PIN-only Shell→Service auth is single-factor. Flagged, unresolved. 2026-06-05.
- **3 already-tracked P0 findings** (PII leak, leaked service-role key, plaintext API keys) — not new, but flagged again since national-scale plans raise their stakes. Confirm current status in `ops/security-register.md` rather than treat as unstarted.

## Decisions only you can make

- **S2: asset writes are gated on the CRM-tier `entity.edit/delete` permission instead of `equipment.edit/view`.** Re-point the keys, or document it as deliberate? 2026-08-23.
- **`ai.use` permission key still completely unenforced** — re-flagged across 4+ sessions since 2026-08-16 with nobody picking it up. Worth a real decision: enforce it, or retire the key if nothing needs it.
- **Division/state JWT-claim model for national-scale identity** — a recommended direction exists (layer state/region + division into the JWT, add an exec rollup view) but nothing's built. 2026-07-23.
- **Phase 4 of the roles/security-groups rollout has 0 rows, 50+ days after being flagged** — still wanted, or superseded by the `field.manage_*` permission work that's since shipped a different way to the same goal? 2026-06-07.
- **Repo-wide lint sits at 990+ pre-existing errors, up from 438 five weeks ago**, with zero autofix available for the dominant rule. Worth a dedicated session before it doubles again. 2026-08-03 → 2026-08-16.
- **4 P0 / 11 P1 / 9 P2 findings from a full security-vs-industry audit are still almost entirely untriaged** — they live only in a Claude.ai artifact, no repo-doc home. Worth pulling into the security register properly. 2026-07-28.
- **206 Supabase security advisories on ehow** — you asked for a dedicated session to work through these; no evidence it's happened yet. 2026-07-03.

## Data and operational gaps

- ~~**2 more blank-name worker records** sit in `app_data.field_people_removed` on ehow~~ — **resolved 30 Aug.** Both identified: phone-only self-signups with no name captured anywhere in the source data either, nothing to backfill. 2026-08-26.
- **6 of 8 renamed Equinix sites still have no contact data**, and there's no way to derive it — needs real names/numbers from you directly. 2026-08-25.
- **6 workers have no date of birth anywhere**, with nothing in the data to recover one — needs a Cards signup or asking directly, not a code fix. 2026-08-17.
- **Only 117 of 250 SKS canonical sites carry a customer link** — Service's report rollups are blank for the rest. This is a Shell-side backfill, not a Service bug. 2026-07-08.
- **Self-serve tenant provisioning has never had a real dry run** — `provision_tokens` still shows 0 rows, ever. Do this before sending a real prospect a signup link. 2026-07-03.
- **No off-platform backup for ehow** beyond Supabase's native 7-day point-in-time recovery. A target design exists; not built. Conditional on budget appetite. 2026-07-23.

## Smaller feature gaps

- **Resend/nudge action for 24 SKS staff who've never signed into Shell** — needs a human pass over the list first (some shouldn't be re-invited), then the action itself isn't built. 2026-08-20.
- **No self-service way to correct your own email** once set — a worker can set it once, never fix a typo. You raised this; no decision made. 2026-08-18.
- **"Rollback" button on the activity log still doesn't work.** Fails cleanly with a message instead of crashing, but doesn't do anything. Build it for real, or remove it? 2026-08-16.
- **Nothing alerts on sign-in lockouts** — they're recorded now, but recording isn't the same as being told about one. Needs your call on where an alert should land. 2026-08-15.
- **"Today's Actions" and "Outstanding Works" can disagree for up to 10 minutes** on Mobile Home, from a cache-TTL mismatch. Shrink the cache, or add a staleness stamp? 2026-08-14.

## Structural / process debt

- **Recurring shared-checkout git collisions** — concurrent sessions committing on top of each other outside a dedicated worktree. At least 6 confirmed occurrences through early August, never fixed at the root (the fix is "always use a worktree," never enforced).
- **One-login P5**: migrate the last 44 SKS workers off the standalone app and retire it. Confirmed still open against this repo's own memory index. 2026-07-13.
- **Confirm `ENABLE_PHONE_OTP` is actually `true`** on eq-shell's live Netlify env — gates a live Cards signup door, blocked from checking directly by the permission classifier. 2026-07-13.

---

## Outside this repo — needs your call, not built without it

You asked me to prompt you on anything outside eq-shell rather than just build it. 13 items surfaced that aren't eq-shell's alone to fix:

**Squarely another repo's (6):**
- **eq-cards** — delete 3 now-redundant secrets (`SUPABASE_JWT_SECRET`, `SUPABASE_SERVICE_ROLE_KEY`, `EQ_SESSION_SALT`) from its Netlify project once the SSO-broker fix is confirmed live. Otherwise the whole point of that fix — shrinking Cards' blast radius — doesn't land.
- **eq-solves-service** (×3) — the PM Calendar digest stays paused until you review its 20-person recipient list; `RCD_SCHEDULE_PARSE_ENDPOINT_URL` still isn't set (photo-upload button errors without it); 5 Dependabot PRs have never been reviewed.
- **eq-ui** — the shared `Table` component's mobile word-wrap fix only landed on one page; every other page using it (Maintenance, Assets, Job Plans, Contract Scope, Test Records…) still has the gap.
- **eq-solves-intake** — its CSV import path skips the same-worker dedup that direct-upload paths now go through.

**Spans repos, or the boundary itself is undecided (7):**
- **Nav-visibility drift across all 4 apps** — no shared source of truth for "what's in the nav and who can see it," 3+ separate incidents so far. Needs a design call: shared config, or a review checklist.
- **eq-cards' `credentials-canonical-sync`** is deployed but wired to nothing, and hardcodes a stale tenant ID — a licence update in Cards never reaches the old SKS compliance view. Revive it, or retire it in favour of eq-field's live-read pattern?
- **Staff duplicate handling is Archive-only** — a real merge fans into Field-owned operational tables (timesheets, schedule, licences, dispatch), which per this repo's own architecture rule can't be rebuilt Shell-side. Needs eq-field coordination before any build.
- **`EQ_CARDS_HANDOFF_KEY` still isn't generated** — the SSO-broker fix is fully built and verified on both the eq-shell and eq-cards sides, blocked purely on this one manual Netlify step (your go-ahead is already on record from 2026-08-11).
- **One single unified access-control screen**, replacing the two separate systems Field and Shell each run today — your own idea, discussed, needs a design pass before it's buildable.
- **Cards' scope against Upvise isn't designed yet** — what Cards owns vs. what stays in Upvise, and whether they sync.
- **PRs #1190 (eq-shell) and #106 (eq-solves-intake)** — a paired contacts-dedup feature — need review/merge, then a production deploy + migration dispatch needs your explicit go (live Anthropic API calls + a schema change to ehow).

None of this is built. Say the word on any of it and I'll scope it properly rather than guess.
