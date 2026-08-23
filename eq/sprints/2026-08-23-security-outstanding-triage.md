---
title: Sprint scoping — outstanding items from the 2026-08-23 §C-G security sweep
owner: Royce Milmlow
last_updated: 2026-08-23
scope: Triage of everything left after this session's closures — leads with a tight execution runbook for the 3 items only Royce can close (SEC-57/61/63), full detail for every item kept below. Live-verified, not restated from the register.
read_priority: high
status: live
---

# Sprint scoping — outstanding items from the 2026-08-23 security sweep

Triggered by Royce asking to turn the session-close "needs you" / "deferred" list into
a sprint, then to sprint the 3 remaining Royce-only items specifically. Every item was
re-checked live, not copied from the register's existing writeup.

**Read this section, skip the rest unless you want the reasoning behind it.**

---

## Royce's action list — do these 3, in this order

### 1. SEC-63 — check first, it changes how urgent #2 is (2 minutes)

**Netlify → Team settings → Environment variables → Shared** (or wherever the
team-level "shared" vars live in the current UI — this is the account-scope list,
not a per-site one). Find `SUPABASE_JWT_SECRET`. Check what it's assigned to.

- **If `sks-nsw-labour` is in that list:** this is now P0 — a separate legal
  entity's app is signing sessions with the same secret as the entire EQ suite.
  Tell me and I'll re-prioritise everything else around it.
- **If it's not:** SEC-63 closes as P1, scoped to EQ sites only. Still worth
  fixing (see #2), just not an emergency.

### 2. SEC-61 — the dev-context leak, per site (~5 min/site, 4 sites)

For each of **eq-shell, eq-service, eq-field, eq-cards**: Site settings →
Environment variables. For every variable with the padlock ("contains sensitive
values") icon, open it and check the **dev** context row specifically.

- **If `dev` shows a real value:** delete *only* that row. Leave branch-deploy /
  deploy-preview / production untouched — deleting the whole variable breaks
  those.
- **If `dev` is already empty or the row doesn't exist:** already safe, skip it.

This is the fix the register already worked out (SEC-61/62) — the standard
"delete and recreate with the same value" remediation used for SEC-9/12/18/19
always leaves a fresh `dev` row when it recreates, which is exactly the leak.
Delete-only, don't recreate, and it stays closed this time.

I already have eq-shell's variable list from an accidental pull earlier this
session (checking `ENFORCE_IFRAME_ORIGIN` triggered a bulk read I didn't intend —
see §5 below). I'm deliberately not repeating any of it here, key names included —
that's exactly the kind of exposure this finding is about, and I'd rather you find
it fresh than trust my memory of a live secrets dump. eq-service, eq-field, and
eq-cards I haven't looked at at all.

### 3. SEC-57 — one decision, then optionally a 5-minute config change

Is `grok-by-xai`'s org-wide write/admin access on every repo intentional, or a
default nobody trimmed? (Permissions confirmed live 2026-08-23: `actions:write`,
`administration:write`, `contents:write`, `workflows:write`, all repos.)

- **If intentional:** nothing to do, close the finding with a note why.
- **If not:** GitHub → Organization settings → GitHub Apps → `grok-by-xai` →
  reduce repository access to just the repos it actually needs, or drop the
  `write`-tier permissions it doesn't use. Five minutes once you've decided.

---

## Shipped this sweep, for reference — no action needed on these

| Item | Outcome |
|---|---|
| SEC-44 (P0) | Applied live to jvkn, verified with a production probe |
| SEC-41 / SEC-42 (P1) | Dispatched live to both zaap and ehow, verified with a production probe |
| SEC-50 (P1) | Merged to eq-service main, verified against live source |
| SEC-46 / SEC-47 (P2) | Dispatched live by a concurrent session (detail in §6 below) — SEC-46 confirmed never actually exploitable |
| SEC-45 (P2) | Merged, still blocked applying to jvkn — confirmed classifier-blocked, not an MCP problem |
| SEC-51 (P2) | Resolved as a non-issue (detail in §5 below) |

---

## Detail — the reasoning behind each item, unchanged from the original scoping pass

## 1. SEC-57 — org-wide GitHub App holds write + admin on every repo (P1)

**Not a build task. Genuinely your call — config, not code.**

Re-checked live via `gh api orgs/eq-solutions/installations`, not restated from the
register: the `grok-by-xai` app still holds `actions:write`, `administration:write`,
`contents:write`, `workflows:write`, `repository_selection: all`, last permission
update **2026-08-10** — 13 days ago, not a stale forgotten grant. This is enough to
push to `main` on an auto-deploying repo or dispatch a live-DDL workflow, and it
structurally evades the "only Milmlow can dispatch" reasoning SEC-11/SEC-14 both rest
on (that reasoning checked human collaborators, not app installations).

Two more apps (`figma`, `cloudflare-workers-and-pages`) hold similar scope on
unenumerated repo subsets — not re-checked this pass.

**The actual decision:** is this app's write/admin access intentional (does something
in your workflow depend on it pushing code or dispatching Actions), or is it a default
grant nobody trimmed? If the latter, GitHub's own UI lets you reduce a single
installation's repo scope and permissions without uninstalling it — that's a five-minute
change once you know the answer, not something I can determine for you.

---

## 2. SEC-61 — Netlify `dev`-context secret leak, standard fix doesn't close it (P1)

**Fix pattern is known. Applying it is Royce-hands-only — same classifier block as
SEC-9/12/18/19, confirmed again this session (see the SEC-44/50 closures' own notes).**

The register's own diagnosis (SEC-61/SEC-62) already found the mechanism: Netlify's
"delete + recreate with the same value, all contexts" remediation — the exact recipe
used to close SEC-9/10/12/18/19 historically — always writes a *fresh* `dev`-context
row when it recreates, and a freshly-written row returns unmasked regardless of
`is_secret`. The only vars that don't leak are ones where `dev` was left **empty**, not
recreated.

**Correct fix, not yet applied anywhere:** for each leaking var, delete the `dev`-context
value and leave it unset (don't recreate it at all) — `dev` context isn't used by any
deployed environment, only by `netlify dev` locally, so an empty `dev` value breaks
nothing in production, preview, or branch deploys. 22 vars across eq-shell,
eq-solves-service, eq-field, eq-cards plus one Netlify account-scope var.

**Not attempting this myself.** Netlify env-var writes hit the same "modifying security
settings" classifier block Claude Code has hit on every secret-touching fix this
session (SEC-12, SEC-19, and — new this session — SEC-30/31's own history). This is a
list for you to work through directly in the Netlify dashboard (Site settings →
Environment variables → per var → delete the `dev` row only), not a PR.

---

## 3. SEC-63 — does the account-scope `SUPABASE_JWT_SECRET` reach sks-nsw-labour? (P1, becomes P0 if yes)

**Blocked on your own 2-minute dashboard check. Deliberately not attempted via tooling
this session — explained below.**

A Netlify **account-scope** secret (team `milmlow`), `SUPABASE_JWT_SECRET`, is the same
value that signs every EQ session in the suite. It's real and it's uninventoried
(`ops/secrets-inventory.md` only ever tracked per-site vars). The open question is
whether it's a *shared* variable inherited by every site on the team — including
`sks-nsw-labour`, a separate legal entity — or scoped to specific sites only. If it
reaches sks-nsw-labour, this becomes P0: a different entity's app would be signing
sessions with the same secret as the entire EQ suite.

A concurrent session narrowed this earlier today: confirmed there's exactly one
Netlify team on the account and `sks-nsw-labour` is a member of it — so "it's on a
separate account" isn't the answer. The remaining question — that team-scope var's
actual assigned-projects list — genuinely needs the dashboard, not an API call.

**Why I'm not pulling this myself, and why that's not just caution for its own sake:**
mid-sprint, I tried to check an *unrelated*, genuinely non-secret flag on eq-shell
(`ENFORCE_IFRAME_ORIGIN`, see §5) and the only read path Netlify's tool exposes is
"all vars for a site" — there's no single-variable scope. That one call surfaced
plaintext `dev`-context values for ~20 real secrets on eq-shell into this session's own
tool history. Nothing new was exposed to a new party (this session already held the
Netlify access that made the leak possible — see SEC-61 above), but it's a fresh,
concrete demonstration of exactly why account-scope secret questions shouldn't go
through the same tool path. Check: **Team settings → Environment variables → shared →
`SUPABASE_JWT_SECRET`'s assigned projects.**

---

## 4. SEC-60 — org/repo hardening gaps: 2FA, secret scanning, branch protection (P3)

**Mixed — some of this is buildable now, some is an account-level policy call.**

Four separate gaps bundled under one finding, live-proved 2026-08-20:
- **2FA not required org-wide** — GitHub org setting, your call (Settings → Authentication security).
- **Secret scanning + push protection disabled on all 7 in-scope repos**, including 3
  public ones — this is a free GitHub feature, genuinely buildable: `gh api --method
  PATCH repos/{owner}/{repo} -f security_and_analysis[secret_scanning][status]=enabled`
  per repo. No behavior change to any app, purely additive scanning. **I can do this on
  your go — it's a config flip, not a code change, but "modifying security settings" is
  exactly the classifier's trigger phrase, so worth flagging before I try.**
- **Third-party Actions unpinned org-wide** — a real hygiene gap (unpinned Actions can
  change underneath you), but fixing it means auditing every workflow's `uses:` lines
  across 7 repos and pinning to a SHA — a real piece of work, not a quick flip. Scoping
  this properly is its own follow-up, not done here.
- **Branch protection exists on eq-shell only** — `eq-solves-service`'s `main` (which
  auto-deploys `service.eq.solutions` and gates the ehow migration pipeline) accepts a
  direct push with zero required checks. Given today's SEC-50 fix landed exactly this
  way (direct push, no protection to pass), this is worth closing: add the same required
  checks eq-shell already has (`typecheck · test · lint`, `gitleaks`, migration-hygiene
  equivalents) via `gh api --method PUT repos/eq-solutions/eq-service/branches/main/protection`.

---

## 5. SEC-51 — is `ENFORCE_IFRAME_ORIGIN` actually a live gap? (P2)

**Resolved this session: no, it's not. The flag is already on; the feared breakage
doesn't appear to exist in current code. Recommend closing as a stale comment, not a
security fix.**

Live-checked (this is the check that led to §3's tool-history note above):
`ENFORCE_IFRAME_ORIGIN` is `true` in production on eq-shell, confirming SEC-12's
original claim — it's not a report-only no-op. `checkShellOrigin` (the guard it
controls) is wired into 70+ Netlify functions, and with the flag on, every one of them
hard-403s a disallowed cross-subdomain `Origin`.

The specific fear in `origin-check.ts`'s own comment — that `mint-supabase-jwt` needs a
carve-out because `cards.eq.solutions` legitimately calls it — doesn't hold up against
current code: `mint-supabase-jwt` does call `checkShellOrigin` with no carve-out, but a
repo-wide search of eq-cards found **zero** references to `mint-supabase-jwt` anywhere.
Either Cards never actually called it, or stopped calling it and the comment was never
updated. Either way, nothing observed today suggests this is live-breaking anything.

**Proposed fix:** not a security change — update `origin-check.ts`'s comment to stop
describing a carve-out that doesn't match current callers, and downgrade/close SEC-51
in the register. Low priority, doc hygiene.

---

## 6. SEC-45/46/47 — three P2 findings, same shape as fixes already shipped today

**SEC-46/47 now closed live. SEC-45 merged but still blocked on application — and now
confirmed to be a classifier block specifically, not a Supabase MCP availability
problem.**

- **SEC-45** — `eq_cards_find_or_create_worker_for_invite` (jvkn) had the identical
  zero-caller-check shape SEC-44 had. Merged: eq-cards [PR #291](https://github.com/eq-solutions/eq-cards/pull/291),
  a plain `REVOKE EXECUTE ... FROM authenticated` (no `auth.uid()` guard needed — this
  function takes no user id to bind). **Still not applied to jvkn.** Attempted again
  once Supabase MCP reconnected — blocked by the same Claude Code classifier that's
  blocked every secret/grant write this session, confirming the earlier "MCP is down"
  framing was incomplete: MCP being back didn't change anything. `authenticated`
  confirmed still holding EXECUTE via a fresh live query. Needs Royce's hands via the
  Supabase dashboard SQL editor, same as SEC-19/30/31 before it.
- **SEC-46** — eq-field's CSV-import purge (`_purgeTenantRows()`) had no DB-layer role
  check on `app_data.sites` specifically (its sibling gap, `app_data.staff`, was
  already closed by SEC-33). Merged: eq-shell [PR #1541](https://github.com/eq-solutions/eq-shell/pull/1541),
  migration `0267` — three RESTRICTIVE policies, manager+supervisor tier, mirroring
  SEC-33's own applied pattern. **Dispatched live by a concurrent session**, which
  found the real story: `authenticated` has only ever held `SELECT` on
  `app_data.sites` since migration `0054` (June) — this finding's exploit path never
  actually existed, the RLS gap was real but unreachable without a write grant that
  was never there. The fix shipped as pre-emptive hardening, not an exploit closure.
  Confirmed independently at session close: all 3 policies live on ehow exactly as
  written, `authenticated`'s grants are `{SELECT}` only.
- **SEC-47** — `approve_safety_record` (ehow) didn't check that the approver isn't the
  submitter. Fixed by a concurrent session, migration `0265`, dispatched live —
  correctly used the actor-identity helper (`eq__caller_actor_uid`) rather than the
  older tenant-id-resolving one, a distinction this session's own SEC-46 fix couldn't
  have caught without the same live check. That session also found and closed a new
  same-day sibling bug, **SEC-70**: `eq__guard_timesheet_status`/`eq__guard_leave_status`
  had the identical self-approval identity flaw.

**Remaining:** SEC-45 (jvkn) needs Royce's hands specifically — not a tooling
availability question anymore, a confirmed classifier boundary.

---
## 7. eq-service: duplicate migration version `0192` breaks CI on every PR (unrelated to security)

**Buildable, trivial, found in passing while confirming today's SEC-50 CI failure was
unrelated (it was).**

Two files both claim version `0192`: `0192_backfill_testing_check_frequency_slugs.sql`
and `0192_reconcile_rls_introspection_service_schema.sql`. `supabase_migrations.schema_migrations`
has a primary key on `version`, so local-Supabase bootstrap fails with a duplicate-key
error before any test runs — breaking the `Integration tests (Supabase local)` CI job
on every PR to this repo, not just the ones that happen to touch these files.

**Fix:** rename one of the two to the actual next-free sequential number.
Live-checked: eq-service's highest normal-sequence migration is `0227`
(`0227_service_assets_exclude_it_equipment.sql`) — the next free number is `0228`.
(Two outlier 5-digit files, `00425_recover_stub_tables.sql` and
`00865_scope_gap_check_linkage.sql`, are a different ad-hoc numbering scheme — not part
of the normal sequence, don't renumber against those.)

---


## Summary

| # | Item | Status | Action |
|---|---|---|---|
| 1 | SEC-63 — account-scope secret scope | Narrowed, not resolved | **Your 2-minute dashboard check** — do this first, changes #2's urgency |
| 2 | SEC-61 — Netlify `dev`-context leak | Fix procedure known | **Your hands** — classifier-blocked for Claude Code, ~20 min across 4 sites |
| 3 | SEC-57 — GitHub App permissions | Confirmed live, unchanged | **Your call** — intentional or tighten? |
| 4 | SEC-60 — org/repo hardening (4 sub-items) | Mixed | 2FA = your call · secret scanning = buildable on your go · Actions pinning = needs its own scoping · eq-service branch protection = buildable on your go |
| 5 | SEC-51 — `ENFORCE_IFRAME_ORIGIN` | **Resolved — not a live gap** | Close in register, fix a stale comment |
| 6 | SEC-46/47 (closed) + SEC-45 (blocked) | Mostly done | SEC-46/47 closed live by another session; SEC-45 needs Royce's hands specifically |
| 7 | eq-service migration `0192` collision | Buildable, trivial | Rename one file to `0228` |
