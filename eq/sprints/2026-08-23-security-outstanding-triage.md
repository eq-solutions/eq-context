---
title: Sprint scoping — outstanding items from the 2026-08-23 §C-G security sweep
owner: Royce Milmlow
last_updated: 2026-08-23
scope: Triage of everything still open after this session's SEC-44/41/42/50 closures — what's genuinely buildable now vs. genuinely Royce's call, with a concrete proposal for each buildable item. Live-verified, not just restated from the register.
read_priority: high
status: live
---

# Sprint scoping — outstanding items from the 2026-08-23 security sweep

Triggered by Royce asking to turn the session-close "needs you" / "deferred" list into
a sprint. Every item below was re-checked live this session, not copied from the
register's existing writeup — three of the eight resolved or changed shape in the
process.

**Correction while writing this:** the prior session-close pending.md entry bundled
"SEC-60/61" as one Netlify dev-context item. That was wrong — SEC-61 is the Netlify
leak; **SEC-60 is a separate, unrelated P3 finding** (org/repo hardening gaps: 2FA,
secret scanning, branch protection). Split correctly below.

---

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

**Genuinely buildable, same pattern as this session's SEC-44/41/42 work. Not started —
these are P2, below today's priority cut, not blocked on anything.**

- **SEC-45** — `eq_cards_find_or_create_worker_for_invite` (jvkn) has the identical
  zero-caller-check shape SEC-44 had, on the sibling resolver. Its only legitimate
  caller is server-role, so unlike SEC-44 this doesn't need an `auth.uid()` guard —
  a plain `REVOKE EXECUTE ... FROM authenticated` closes it, same control-plane apply
  path as SEC-44.
- **SEC-46** — eq-field's CSV-import purge (`_purgeTenantRows()`) has no DB-layer role
  check on the Sites/Supervision tables specifically (every other importer's table
  does). Needs an `entity.delete`-equivalent RLS policy addition on ehow — same shape
  as today's SEC-41/42 fix, dispatched via the tenant-migrate.yml One Pipe.
- **SEC-47** — `approve_safety_record` (ehow) doesn't check that the approver isn't the
  submitter. Needs a same-function guard (`submitted_by <> auth.uid()` or equivalent)
  added as a first statement, same shape as SEC-44's fix. 35 prestarts + 1 toolbox talk
  live behind it today.

None of these need a product decision first — permission tiers are either already
established (SEC-45 mirrors SEC-44 exactly) or self-evident (SEC-47's fix is "don't
let someone approve their own submission"). Ready to build on your go.

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
| 1 | SEC-57 — GitHub App permissions | Confirmed live, unchanged | **Your call** — intentional or tighten? |
| 2 | SEC-61 — Netlify `dev`-context leak | Fix pattern known | **Your hands** — classifier-blocked for Claude Code, exact var list ready |
| 3 | SEC-63 — account-scope secret scope | Narrowed, not resolved | **Your 2-minute dashboard check** — genuinely can't be read via tooling safely |
| 4 | SEC-60 — org/repo hardening (4 sub-items) | Mixed | 2FA = your call · secret scanning = buildable on your go · Actions pinning = needs its own scoping · eq-service branch protection = buildable on your go |
| 5 | SEC-51 — `ENFORCE_IFRAME_ORIGIN` | **Resolved — not a live gap** | Close in register, fix a stale comment |
| 6 | SEC-45/46/47 — three P2 code fixes | Buildable, not started | **Ready to build on your go** — same patterns as today's fixes |
| 7 | eq-service migration `0192` collision | Buildable, trivial | Rename one file to `0228` |
