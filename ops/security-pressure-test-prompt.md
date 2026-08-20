---
title: OPS — EQ Suite Security Pressure-Test Prompt
owner: Royce Milmlow
last_updated: 2026-08-21
scope: Self-contained red-team/pressure-test prompt for the live EQ product suite. Designed to survive being pasted into a context that has none of eq-context loaded — but if eq-context IS available, its live files outrank this document's inlined snapshots. Companion to security-register.md; findings land there, not just in chat.
read_priority: critical
status: live
---

# EQ Suite Security Pressure-Test Prompt

Paste this whole document into a fresh agent session (any tool) to run it standalone,
or run it directly from an eq-context clone. Either way: this is a **findings sweep**,
not a fix-it sweep. Report what you find in the format at §6; don't unilaterally patch
anything auth-adjacent or production-data-adjacent — that's Royce's call, same as every
other EQ session (§1).

**Before you start hunting: read §2's warning.** This document names specific project
IDs, specific finding IDs, and specific "current" facts as of 2026-08-20. That snapshot
will be wrong by the time you run this again. Re-derive, don't trust — that instruction
isn't boilerplate, it's the single most common way this exact suite's own documentation
has gone wrong (`system/failures.md` F14: "a hand-written claim about current state ages
into a lie, and nothing anywhere notices" — three confirmed recurrences, most recently
2026-07-30). Treat this prompt as the same risk class it's asking you to hunt for.

**How hard "hard" means.** Royce's instruction authoring this: *"go as hard as you can
to break things."* That means maximize **technique** — actively attempt auth bypass,
token/claim forgery, tenant-crossing reads, privilege escalation, IDOR — not maximize
**blast radius**. Every real finding this suite's register has ever produced came from
read-only technique; none needed a write. Go all-in on actually defeating a control
wherever you can do that read-only. Where the next step to *prove* something would
require a write, a real OTP/invite exercise against a live account, or touching
sks-labour: stop at that line and report exactly how close you got — that's still a
maximal finding, and closing that last step is explicitly Royce's call, not something
this document authorizes on its own (§7).

---

## 1. Authorization & hard boundaries — read first, non-negotiable

This is Royce Milmlow's own product suite (founder, EQ Solutions). This sweep is
authorized, defensive security testing of systems he owns. That authorization does not
extend past what's written here.

**In scope:** eq-shell, eq-field, eq-solves-service (EQ Service), eq-cards,
eq-solves-intake, and three of the four live Supabase projects behind them (§2).

**OUT OF SCOPE by default:** `nspbmirochztcjijmcrx` (sks-labour) — real live SKS staff
PII, already carries a confirmed open P0 (SEC-1, a public-key PII leak), and is under a
standing decision (Royce, 2026-07-20, reaffirmed after a prior session got as far as
staging a fix): **no engineering changes land on sks-labour, full stop, until EQ Field
replaces it.** That decision covers hardening too, not just breaking changes — a
pressure test that pokes at it, generates load against it, or "helpfully" tightens
something violates a decision that was made deliberately and re-confirmed once already.
"Go as hard as you can" does not reopen this — it's a specific, twice-made call, and
general enthusiasm doesn't override a specific standing decision. If a finding genuinely
requires touching this project to even verify, **stop and ask Royce for explicit "SKS
live" authorization first.**

**Read-only, everywhere in scope — this is the line "as hard as you can" pushes technique
against, not past:**
- SELECT-only queries, GET requests, static config/source inspection, advisor tooling.
- Actively **attempting** to defeat a control (forge a claim, replay a token, cross a
  tenant boundary, escalate a privilege, walk an id space) is in-bounds and encouraged —
  as long as the attempt itself never resolves to an INSERT/UPDATE/DELETE, a schema
  change, or a session/credential you mutate on a real account.
- No exercising OTP/invite/password-reset flows against real accounts.
- **Aggressive ≠ high-volume.** Cap any single technique's request rate low enough that
  it reads as one determined tester, not a script — this is a live system with real
  staff on it today. A self-inflicted lockout, a rate-limiter trip, or a false-alarm page
  to Royce's phone is itself a failure of this sweep, not evidence it worked.
- **Never fetch, print, log, decode, or persist the actual value of a secret or
  credential.** Check *presence* + `is_secret` flag + which deploy contexts it covers —
  never the value. This suite has a long, expensive paper trail of exactly this going
  wrong (SEC-9/10/12/18/24 in the register) and an explicit process fix from it: any
  credential-consumer mapping is scoped to names/presence only. Inherit that fix; don't
  relearn it.
- Findings get **reported**, not unilaterally fixed. Anything auth-adjacent or
  production-data-adjacent needs Royce's explicit review before any change lands —
  identical bar to every other EQ session (`CLAUDE.md` §7 / non-negotiables #8, #9).
- If you find evidence of **current active exploitation** — not just exploitability —
  stop the sweep and surface it immediately. Don't queue it as a normal finding (§7).

---

## 2. Ground truth — re-derive, don't trust this snapshot

### Live systems in scope

| App | Repo | URL | Notes |
|---|---|---|---|
| EQ Shell | eq-shell | core.eq.solutions | Auth hub, canonical data owner. Merging to `main` **is** a production deploy (Netlify's GitHub App, 2-4s, unattended — no separate "deploy" step exists on this repo). |
| EQ Service | eq-solves-service | service.eq.solutions | CMMS, reads canonical via `security_invoker` views |
| EQ Field | eq-field | field.eq.solutions | Resources/dispatch/labour hire. SKS tenant = live prod; `eq` tenant = demo, PIN-gated (see §2 auth model) |
| EQ Cards | eq-cards | (Flutter app + web) | Onboarding intake, real signup traffic |
| EQ Intake | eq-solves-intake | — | Parse/emit engine behind Cards |
| SKS NSW Labour | sks-nsw-labour | sks-nsw-labour.netlify.app | **App/deploy config is fine to check (read-only). Its Supabase project is not — see below.** |

### Supabase projects — this table is the one boundary that matters most

| Project ID | Name | Holds | In scope? |
|---|---|---|---|
| `jvknxcmbtrfnxfrwfimn` | eq-canonical | Control layer — `shell_control.users`, tenant registry, Cards config. Browser-accessible. | Yes |
| `zaapmfdkgedqupfjtchl` | eq-canonical-internal | EQ tenant operational data, server-only | Yes |
| `ehowgjardagevnrluult` | sks-canonical (ehow) | SKS tenant operational data + EQ Service (`service.*`) — **live production data** | Yes, carefully — real customer/site/asset PII lives here, same care as prod anywhere |
| `nspbmirochztcjijmcrx` | sks-labour | SKS **live staff** production data | **NO — §1** |

Re-check `system/infrastructure.md` for the current list before assuming this table is
complete — projects get added, deleted, and re-scoped (urjh was deleted 2026-06-22 after
weeks of stale docs still pointing at it; that's a live F14 example, not hypothetical).

### Auth model, in one page

This suite does **not** use Supabase Auth / `auth.users`. It mints its own JWTs against
`shell_control.users` on eq-canonical, signed with the project's own JWT secret. RLS
reads `app_metadata.tenant_id` / `app_metadata.eq_role` from that JWT — never
`user_metadata`, which is client-editable (SEC-2 was exactly this mistake, since fixed;
confirm it hasn't come back elsewhere — that confirmation is itself a §4.A action item).

- **Shell session:** `eq_shell_session` cookie — HttpOnly, Secure, SameSite=Lax,
  Domain=`.eq.solutions`, 7-day TTL.
- **Supabase JWT** (for modules that talk to Supabase directly): minted by
  `/.netlify/functions/mint-supabase-jwt`, HS256, **15-minute TTL**, refreshed on demand.
  `role: 'authenticated'` is Supabase's fixed Postgres-role slot; the EQ tier lives in
  `app_metadata.eq_role` specifically to avoid colliding with it.
- **Field iframe handoff:** `eq-shell/netlify/functions/token-exchange.ts` mints a
  **60-second** HS256 JWT (`SUPABASE_JWT_SECRET`), `source_app = field:<slug>`, built
  server-side from `session.tenant_id`. SKS token mode (Field hosted off
  `.eq.solutions`) delivers it via URL hash: `...netlify.app/?tenant=<slug>#sh=<jwt>&cid=<uuid>`.
  The old HMAC path (`mint-iframe-token.ts`) is documented as dead code — no caller —
  confirm that's still true rather than trusting the comment (§4.D).
- **Service handoff cookies** (`eq_service_jwt` / `eq_shell_bridge`): SameSite=None;
  Secure; Partitioned (CHIPS), specifically to survive third-party-cookie partitioning
  while embedded.
- **Cards** (Flutter): receives a shell-minted Supabase JWT via the iframe URL hash on
  first load, stores it in `flutter_secure_storage`, refreshes via a `postMessage`
  bridge to the shell.
- **Demo tenant (EQ Field only):** has no Shell/JWT integration — a legacy PIN gate is
  its *only* auth path. Can't be deleted without breaking demo. Worth checking on its
  own terms (§4.D) precisely because it's the one place this suite's modern auth model
  doesn't apply.
- **Shared-secret blast radius:** at least one HMAC secret is known to be reused across
  multiple Netlify deploys for more than one purpose (signing both session cookies and
  the cross-app handoff token on more than one app) — architectural risk flagged in the
  register (SEC-24 as of last read) and not yet resolved. Treat "is this secret used for
  more than one trust boundary, on more than one deploy" as a standing question, not a
  closed one.

---

## 3. What this suite has actually gotten wrong before

Not history for its own sake — these are bug **classes**, not one-off instances, and the
highest-yield move is checking whether each class recurs somewhere *not yet audited*,
not just re-confirming the specific spot it was already found. Full detail and current
status: `ops/security-register.md` (re-read it now — don't rely on this summary for
current state).

1. **RLS scoped by tenant only, when a narrower actor column exists and isn't used.**
   A table has both `tenant_id` and (say) `staff_id`, but every policy only checks
   `tenant_id` — so anyone in the tenant can read/write anyone else's rows. Found once
   already (`app_data.licences` on ehow, same shape a fixed table used to have) —
   the question is which other tenant-scoped table still has this shape.
2. **Anon/public key reads a table directly** because RLS or the grant was never applied,
   or a later migration dropped a grant an earlier one added. Both a from-scratch miss
   (SEC-1) and a regression (six `field_*` views lost their `authenticated` grant to a
   later `DROP`+recreate, 2026-07-19) have happened here.
3. **Secrets marked `is_secret:false`, or `true` but leaking anyway via the `dev` deploy
   context.** Confirmed platform-level root cause: toggling the flag on an
   already-populated var does not purge the plaintext stored before the toggle — only
   delete+recreate does. This one recurred across five separate Netlify sites before it
   was understood, and the register lists it as the single largest finding class here.
4. **SECURITY DEFINER functions default to anon/public EXECUTE** unless explicitly
   revoked. One sweep found ~39 such functions on one tenant project, 12 on another,
   none previously flagged by the advisor tool alone — advisors under-report this one.
   (Live spot-check, 2026-08-20: ehow still shows exactly 12 anon-executable
   `SECURITY DEFINER` functions today, matching the register's count — including one
   named `hard_delete_archived_entity` whose body has not yet been read to confirm it's
   guarded. That's a live, untriaged starting point for §4.B, not a closed question.)
5. **A workflow/runbook/comment claims a safety gate that doesn't actually exist** when
   checked against live config — a "requires human approval" comment on a GitHub Actions
   production environment with zero actual `protection_rules`, found on two separate
   repos. The inverse also happens on this suite: eq-shell's own deploy step is
   *actually* automatic despite historically being described as a separate manual step —
   same failure shape, opposite direction. Trust the live config, never the comment.
6. **Bulk/destructive endpoints check the data shape, not the caller's role.** A
   wipe-and-replace CSV importer (purge tenant rows, then bulk-insert) shipped without
   its intended `isManager` gate — RLS was fine, the app-layer authorization check simply
   wasn't there.
7. **A fix merges but never reaches the live control-plane project**, because
   control-plane migrations (`eq-shell/supabase/migrations/*` against jvkn) have no CI
   apply path — they're hand-applied. "Merged" and "applied" are different facts here;
   a real fix (`provision_tenant` FK) sat merged-but-inert for days because of this.
8. **The register itself says CLOSED or VERIFIED as of some past date.** Treat that as a
   lead, not a fact, same as every other piece of substrate in this repo (`CLAUDE.md`
   Rule 0.5). This is the F14 pattern from the header, applied to the one file this
   sweep leans on most.

---

## 4. The sweep

Do **A–C** first — that's where the real history above clusters, and where "go as hard
as you can" earns the most: don't just read a control, try to beat it. **D–G** are the
broader/standard pass once A–C are clear.

### A. Multi-tenancy & RLS
- Enumerate every table holding tenant-scoped data across `jvkn`/`zaap`/`ehow`
  (Supabase MCP `list_tables`, all three, not `nspbmirochztcjijmcrx`).
- For each: is RLS actually enabled (not just "a policy exists" — check `rowsecurity`,
  or let `get_advisors` flag `rls_disabled`)?
- Read the literal `USING`/`WITH CHECK` expression on every policy, not just its name:
  - `USING (true)` / `WITH CHECK (true)` — an always-true policy is only safe if the
    table also has no reachable grant for the role that would hit it (verify the grant
    side too, don't assume "latent" without checking).
  - Scoped only by `tenant_id` when the same table also has a narrower actor column
    (`staff_id`, `user_id`, `created_by`) that no policy references — pattern #1 above.
  - References `user_metadata` instead of `app_metadata` — pattern from SEC-2, confirm
    it hasn't resurfaced anywhere else.
- Direct anon-key probe (same method `scripts/rls_probe.py` already uses): hit each
  table's PostgREST endpoint with the plain publishable/anon key, confirm it returns
  nothing or 403s for data that isn't the caller's own. **Never run this against
  `nspbmirochztcjijmcrx`** — it already has a confirmed-live version of exactly this
  finding and doesn't need a second demonstration.
- **Don't stop at "the policy looks scoped correctly" — prove it.** Wherever you
  legitimately hold (or can legitimately obtain, e.g. a demo/test tenant session) a
  low-privilege session for one tenant, actually attempt to read or act on another
  tenant's row by substituting its id in the request. This is the same action as the
  IDOR check in §4.E — do it here live wherever a session is already in hand, rather
  than deferring every instance to a later "spot check."
- Grep every in-scope repo for `createPublicAdminClient()` and any direct
  `SUPABASE_SERVICE_ROLE_KEY` usage. For every call site, confirm an explicit tenant
  predicate (`.eq('tenant_id', …)` / `.eq('org_id', …)` or equivalent WHERE) is present,
  and that the id is resolved server-side (session JWT, URL path) — never taken as-is
  from a request body or query string (non-negotiables #11; this is the rule agents
  violate most easily per `rules/agentic-coding.md` §4, so read that section too).

### B. SECURITY DEFINER / RPC surface
- `get_advisors` (security) on all three in-scope projects as a first pass.
- Then go past advisors, which have already under-reported this once: query
  `information_schema.routines` joined to `role_routine_grants`, filter
  `security_type = 'DEFINER'` and grantee in `('anon','public','authenticated')`.
- For every hit, read the actual body (`pg_get_functiondef`) — confirm it internally
  checks `auth.uid()` / the caller's tenant claim before touching data. A function name
  that sounds safe is not evidence; the register's own SEC-4 was only closed after
  someone read the body and confirmed the guard, not from the name alone.
- **Where a function looks guarded, don't stop at reading the guard — try to slip past
  it.** Look specifically for: a guard that checks `auth.uid() IS NOT NULL` but never
  checks *which* tenant that uid belongs to; a guard on the outer function but not on an
  inner one it calls that's independently reachable; an edge-case input (null, empty
  string, an id from a different schema) the guard's author didn't anticipate.
- Confirm `search_path` is pinned (`SET search_path = …`) on every SECURITY DEFINER
  function found — unpinned search_path on a definer function is a known
  schema-shadowing privilege-escalation vector, and it's a known open hygiene item here
  (`function_search_path_mutable`, several projects).

### C. Secrets & credential hygiene — presence and flags only, never values
- Every Netlify site (eq-shell, eq-field, eq-solves-service, eq-cards,
  sks-nsw-labour — its *app config* is fair game even though its Supabase project isn't):
  for every var that's a real credential, check `is_secret` **per deploy context**
  (dev / branch-deploy / deploy-preview / production).
- Specifically re-check `dev` even where `is_secret: true` shows — the confirmed bug is
  that the flag doesn't purge plaintext stored before it was set; only delete+recreate
  does. A var can read `is_secret:true` today and still be leaking on `dev`.
- Map which secrets are **shared across more than one site** (compare var names across
  all five) and flag any shared secret that backs more than one trust boundary (e.g. one
  key signs both session cookies and a cross-app handoff token) as its own finding, even
  if every copy is correctly masked — one leak forges suite-wide, not app-wide.
- GitHub Actions: confirm long-lived secrets (`SUPABASE_ACCESS_TOKEN` etc.) exist only as
  repo/org secrets, and that any workflow step that handles one has masking
  (`::add-mask::`) rather than relying on GitHub's default masking alone.
- **If a tool call returns a value anyway** (wrong tool, unexpected verbosity, whatever) —
  don't reproduce it anywhere, in a finding or otherwise. Note only that it happened and
  which variable. This exact near-miss has already happened here more than once.

### D. Cross-app auth / iframe handoff — attempt forgery, don't just read the code
- Confirm token TTLs are enforced **server-side** on receipt, not just set at mint time —
  a token past its 60-second Field-handoff TTL should be rejected by the receiving app,
  not just carry an `exp` the client-side code happens to respect.
- **Actively attempt cross-tenant replay**, not just a theoretical check: from a
  legitimate low-privilege session, try to construct or replay a token that claims a
  `source_app`/`tenant_id` different from the one your real session holds. If the
  receiving app accepts it, that's a proven finding, not a suspected one.
- URL-hash token delivery (`#sh=<jwt>&cid=<uuid>`): confirm the fragment gets cleared
  from the URL bar/history after consumption. An uncleared fragment is a bearer token
  sitting in browser history.
- `postMessage` origin checks: confirm the receiving side validates `event.origin`
  against an allowlist, not just the message's shape/type — try posting a
  correctly-shaped message from an off-allowlist origin if you can stand one up.
- Confirm `mint-iframe-token.ts` (the legacy HMAC path) genuinely has no live caller —
  grep the actual deployed source, not the comments asserting it's dead. Trusting a
  comment over the live artifact is exactly pattern #5 in §3.
- Cookie flags — `eq_shell_session`, `eq_service_jwt`, `eq_shell_bridge` — verify via
  **live response headers**, not source alone; correct code doesn't guarantee correct
  behavior if a proxy/CDN layer strips or rewrites headers in front of it.
- Demo tenant PIN gate (EQ Field): confirm it's rate-limited, and actively try to use it
  as a pivot toward any real tenant's data — it's the one auth path in this suite that
  predates the JWT model, worth testing on its own terms rather than assuming it
  inherited the same hardening.

### E. Authorization vs authentication — privilege escalation, attempted not just checked
- For every bulk/destructive endpoint (CSV import, "sync", any purge-then-replace
  pattern — grep for `_purge`, bulk `DELETE FROM`, bulk upsert helpers): confirm a
  **role** check gates it, not just a session check, and that the role comes from
  `app_metadata.eq_role` server-side, never a client-supplied field. Pattern #6 in §3
  shipped exactly this gap once already; check the sibling endpoints, not just the one
  already fixed.
- **Where your session holds a specific role, actively try actions that role shouldn't
  have**: call a manager-only RPC from a non-manager session, hit an admin-only route as
  a standard user, submit a bulk-purge/bulk-import endpoint as a caller with no
  relationship to that tenant's data. A 403 is a pass. Success is the finding — and it's
  a stronger finding than "the code path looks reachable," which is all a read-only code
  review can ever prove on its own.
- Confirm role/permission derivation can't be influenced by client-supplied
  `user_metadata` or request-body fields — `app_metadata` only.
- **IDOR — walk it, don't sample it.** Pick at least one representative list/detail
  endpoint per app (sites, customers, assets, or workers are the highest-value targets)
  and substitute a real range of ids you have no relationship to, not just two or three.
  Confirm every single one is denied — a pattern that holds for 9 of 10 tried ids and
  fails on the 10th is exactly the kind of gap a light sample misses and a walk catches.

### F. Standard web/API surface
- **Injection:** grep for hand-built SQL string interpolation vs parameterized
  PostgREST/RPC calls. Rarer here than a hand-rolled backend, but check any raw
  `execute_sql`-style admin paths and report/export generators specifically.
- **SSRF:** anything that fetches a URL from user input (webhook config, PDF/doc
  generation, `pg_net` usage — `pg_net` is confirmed installed in `public` schema on at
  least one project) — confirm no unvalidated user-supplied URL reaches an outbound
  fetch with internal network reachability.
- **XSS:** grep for `dangerouslySetInnerHTML` or equivalent, rendering user-supplied
  free text (site/customer/asset notes, incident descriptions) without sanitization.
- **CSRF:** state-changing routes reachable via bare GET, or POST without
  origin/CSRF-token validation — check the iframe-embedded surfaces first, they're the
  least standard part of this suite's request flow.
- **Headers:** every Netlify/Cloudflare Pages site must ship a `_headers` file
  (non-negotiables #10) — confirm present *and* actually effective in live response
  headers (CSP, X-Frame-Options, etc.) on all five sites, not just that the file exists.
- **Rate limiting / brute force:** this suite mints its own JWTs rather than using
  Supabase Auth, so Supabase's own auth-layer rate limiting does not apply — check the
  custom login/PIN/invite paths specifically for a failed-attempt limit. Confirm the
  limit actually triggers (a handful of deliberate failures, well under lockout-causing
  volume) rather than assuming it from the code — but stay well clear of the volume that
  would actually lock out a real account (§1).
- **Dependencies:** `npm audit` per repo; confirm existing `overrides` (e.g. the
  sharp/uuid pin already in use on eq-service) haven't been silently widened or dropped
  by a later bump.

### G. CI/CD & deploy pipeline integrity
- For every workflow whose header/comments claim a safety gate ("pauses for approval",
  "requires review"): verify against `gh api repos/eq-solutions/<repo>/environments/production`
  (`protection_rules`) directly — don't trust the comment. This exact gap between claim
  and live config has already been found on two repos; check the rest.
- `gh api repos/eq-solutions/<repo>/collaborators` for every in-scope repo — confirm the
  actual dispatch/write access list is who it should be.
- Confirm tenant-migration and service-migration dispatch access hasn't widened since
  last checked.
- Control-plane migrations (`eq-shell/supabase/migrations/*` against `jvkn`): compare
  what's in the repo against what's actually live (`schema_migrations` /
  `pg_get_functiondef`) — "merged" is not "applied" here, and it's already happened once
  that the two silently diverged for days.
- eq-shell specifically: confirm the merge→deploy path is still exactly what's documented
  (Netlify's own GitHub App, no in-repo workflow involved) and hasn't grown an additional,
  less-visible trigger since it was last mapped.

---

## 5. Tooling — use what already exists before improvising

- `scripts/rls_probe.py` — anon-key table probe; maintains a `KNOWN_LEAKS` baseline.
- `scripts/security_audit.py` — wraps `get_advisors`; maintains an `ACCEPTED_ERRORS`
  baseline.
- Supabase MCP — `list_tables`, `get_advisors`, `list_extensions`, `execute_sql`
  (SELECT only, in this context).
- `gh api` — environment protection rules, collaborator lists, workflow config.
- Netlify env-var tooling — presence/`is_secret`/context only, per §C.

Run the existing scripts before hand-rolling new checks. They already encode a baseline;
the point of this sweep is what's **new** beyond that baseline, and whether what the
baseline calls "accepted" or "verified latent" still holds against the live system today.

---

## 6. Reporting a finding

Match `ops/security-register.md`'s existing shape — a priority-list row plus a `### SEC-N`
detail section:

```
| SEC-N | <Severity> | <one-line finding> | <project> | <status> |
```

**Before assigning `SEC-N`: read the current register and use the next free id.** This
document cannot tell you what that is — only the live file can (§2's warning about
snapshot drift applies to numbers too).

Severity, calibrated to this suite's own history rather than a generic CVSS gut-feel:

| Severity | Bar |
|---|---|
| **P0** | Reachable today by an unauthenticated caller, or a caller in the wrong tenant, against real production data or a credential that unlocks real production data. |
| **P1** | Confirmed exploitable, but needs an authenticated and somewhat-privileged starting position, or hasn't been confirmed reachable in practice yet. |
| **P2** | Real gap, but needs an unusual precondition, or already has a partial mitigation (e.g. an always-true policy behind a role that holds no table grant — still worth fixing, not urgent). |
| **P3** | Hygiene/hardening. Latent, no plausible exploitation path today, or moot once a planned retirement lands. |

A finding you *proved* (§4's forgery/escalation/IDOR attempts actually succeeded) and a
finding you only *reasoned your way to* (the code looks like it should be exploitable)
are different strength evidence — say which one you have. Proved beats reasoned at the
same severity; don't let a proved P1 read as weaker than a reasoned P0.

---

## 7. Hard stops — interrupt the sweep for these, don't queue them as a normal finding

- Evidence of **current active exploitation**, not just exploitability — unexpected
  rows, an access pattern that looks like someone else's probe already in progress.
- Anything that would require touching `nspbmirochztcjijmcrx` just to check — stop,
  surface it, get explicit "SKS live" authorization first (§1).
- Anything where the next step to *prove* a finding would require an actual write, a
  real OTP/invite/password-reset exercise against a live account, or generating
  load — stop at the line, report exactly how far you got and what the remaining step
  would be. That last step is Royce's call, not this document's to authorize (see
  "How hard 'hard' means" at the top).
- A secret value returned to you despite the presence-only intent — stop, don't
  reproduce it anywhere, note only that it happened and which variable.
