---
title: EQ — Internal Document Sign-off Register (Design)
owner: Royce Milmlow
last_updated: 2026-08-03
scope: Design for an internal-only document sign-off + reminder register — upload once, push to signers, track who's signed, chase who hasn't. First cut of the safety/quality/commissioning-docs idea explored 2026-08-01.
read_priority: high
status: live
---

# EQ — Internal Document Sign-off Register

**Status:** v1 build-plan steps 1-5 (register view) complete. Schema
(`0233_document_signoff_register.sql`) applied live to both ehow and zaap
2026-08-02 (eq-shell PR #1180). Shell upload+push UI merged and deployed
2026-08-03 (eq-shell PR #1196). Field sign UI merged and deployed 2026-08-03,
pilot-gated to one person (eq-field PR #627). Shell register view merged
2026-08-03 (eq-shell PR #1208) — admins can see who's signed what without
querying the DB. Upload → push → sign → register is a real, working loop for
the pilot user. Reminder cron (the other half of step 5 in the original plan)
was never scoped/discussed and remains not started; step 6 (rollout past the
pilot) also remains — both Royce's call on timing. A signature-pad + evidence-view
upgrade merged 2026-08-03 on top of the above (eq-shell PRs #1212/#1217, eq-field
PR #635): Field signing uses the real signature pad, and the Shell register shows
the drawn signature, timestamps, and a link to the signed document.

## Why

Direct pain, Royce's own words: *"impossible to know who has signed what."*
Picked via `/decide` (2026-08-01) as the low-hanging-fruit start over
AI document generation — cheapest of the two, reuses infrastructure
that's already live, and answers a fact Royce stated, not a guess.
`TODAY.md` GOALS is UNSET, so this isn't weighed against a deadline —
only against effort and stated pain.

## Gap analysis — what exists today vs what this closes

| Area | What exists today | Gap |
|---|---|---|
| Tracking who's signed a document | Nothing — no register, no view, no export. Matches Royce's stated pain exactly | **This is the whole gap.** Every other row below is supporting infrastructure that already exists |
| Identity to sign against | Shell canonical auth — live, already the identity every app trusts | None — directly reusable, no new auth to design |
| Reminder/expiry mechanics | Field's licence-expiry model ("Expiring soon" chip) — live, proven | Pattern exists but has never been pointed at documents |
| Due-date + notify cron | Service's `maintenance_checks` due-dates + the pre-visit brief cron — live | Same shape, wrong target object — needs retargeting, not inventing |
| Admin surface to push something to a targeted audience | Shell/Core already the cross-app admin point | No document-specific upload/audience UI yet |
| Where a document is stored/versioned | ~~Ad hoc~~ **Corrected 2026-08-02:** `app_data.attachments` is a live polymorphic file spine (22 rows on ehow) with live upload/list API routes in Shell | No *document* or *version* record — the spine stores files against quotes/jobs/sites only (`VALID_ENTITY_TYPES` allowlist), with no version or hash concept |
| Signature capture | ~~None~~ **Corrected 2026-08-02:** partial prior art exists — `app_data.swms.signatures` (jsonb, 0 rows) and eq-field's `public.toolbox_talks.attendance` (jsonb, live UI, per-attendee sign-off) | Both store sign-off *denormalised into jsonb*, which cannot answer "who has **not** signed" without a full scan. v1 needs relational rows — see the divergence note below |
| Data location (schema) | ~~Not decided~~ **Resolved 2026-08-02** | **`ehow` / `app_data`**, via the eq-shell `supabase/tenant-migrations/` One Spine. Confirmed live, not inferred — see verification below |
| External (non-EQ-user) signers | None | Deliberately deferred — no real case yet, not designed |
| AI-drafted document content review | Not addressed by this initiative | Separate, already-flagged problem (raised 3× in the 2026-08-01 session) — this system tracks sign-off, it doesn't generate or review content |

**Bottom line:** three of the four supporting mechanisms — identity, reminders, due-date/notify — already exist and are proven live elsewhere in the suite. The only real gap is the register itself. That's why this is the low-lift starting point.

## Live-schema verification — 2026-08-02 (build plan step 1, closed)

Queried live, not read from a doc. Both candidate planes checked.

| Plane | What's actually there | Read |
|---|---|---|
| **`ehow`** (`ehowgjardagevnrluult`) — tenant operational plane | `app_data.swms` (0 rows, has `signatures jsonb` + `version` + status enum incl. `superseded`), `app_data.toolbox_talks` (0 rows), `app_data.attachments` (22 rows, polymorphic spine), `app_data.licences` (115), `public.toolbox_talks` (1 row, eq-field's own) | Every safety/quality document-adjacent table in the suite already lives here, tenant-scoped |
| **`jvkn`** (`jvknxcmbtrfnxfrwfimn`) — canonical control plane | `public.licences` (175), `public.workers` (97), `public.organisations` (3), `worker_credentials`/`worker_inductions` (0 each), all of `shell_control.*` | Holds **cross-tenant person attributes and identity**, not tenant content |

**Decision: `ehow` / `app_data`.** A document is tenant-owned operational
content (an SKS SMP, a switchboard schedule) signed by that tenant's own
staff — not a cross-tenant-identical entity like a licence type. Note
licences exist on *both* planes (175 canonical on jvkn, 115 mirrored on
ehow) precisely because a licence is a person attribute; a document is not.

**Three findings that changed the design:**

1. **`public.acknowledgments` is a trap.** Name suggests document
   attestation; it is actually eq-field **peer recognition** (worker
   praises worker — `given_by_name`, `message`, `tag`). Has its own RLS
   in shell migrations 0138/0139. **Do not overload it.**
2. **Sign-off prior art exists and disagrees with itself.** `app_data.swms.signatures`
   and `public.toolbox_talks.attendance` both store sign-off as jsonb blobs.
   Fine for a point-in-time form record; useless for "who hasn't signed."
   The register diverges deliberately — relational rows, indexed — and the
   migration header says why, so the divergence doesn't read as drift later.
3. **`app_data.attachments` is the wrong shape to reuse for this.** It's the
   many-files-per-entity spine. A document version is exactly *one* file and
   the signature binds to that file's hash — routing through a polymorphic
   many-table makes "exactly one file" unenforceable in the DB. Versions
   carry `storage_path` directly and reuse the same private bucket. Reusing
   the storage, not bending the table.

Nothing named `documents`, `document_versions`, or `sign_off` exists
anywhere in eq-shell, eq-field, or eq-solves-service. Not duplicating work.

## What it reuses — not new infrastructure

| Piece | Existing precedent |
|---|---|
| Identity — who's signing | Shell canonical auth — already the single identity source every app trusts |
| Expiry/reminder pattern | Field's licence-expiry model (the "Expiring soon" filter chip) |
| Due-date + notify pattern | Service's `maintenance_checks` due-dates + the pre-visit brief cron |
| Distribution/admin surface | Shell (Core) — already the cross-app admin point |
| Where people actually work day to day | Field |

## Mechanism — v1 scope, internal signers only

1. Upload a document + set signer(s)/audience from Core (Shell). Audience
   is always targeted — role, crew, site, or specific people. No
   broadcast-to-everyone shortcut in v1.
2. Signers see it in Field, review it, tap to confirm.
3. Signature = authenticated user ID + timestamp + hash of the document
   version. No drawn signature, no vendor — identity is already proven
   by the login, which is arguably stronger evidence than a typical
   e-signature captured via an emailed link.
4. Register view: document → version → assigned signers →
   signed/outstanding → date. Purely informational — an unsigned
   document blocks nothing (no rostering/clock-on gate) in v1.
5. Reminder cron (same shape as the pre-visit brief cron) chases
   outstanding signers on a schedule.
6. Replacing a document (new version) supersedes every signature on the
   prior version — signers must re-sign. The register never shows
   someone as "signed" against content that's since changed underneath
   them.

## Explicitly out of scope for v1

- **External (non-EQ-user) signers** — clients, site owners. Different
  problem, needs either a signing vendor or a link+PIN flow. Not
  designed, not needed until a real external-signing case shows up.
- **AI-drafted or AI-parsed document content.** This is a tracking
  system, not a generation system — deliberately sidesteps the
  AI-touches-safety-content review problem raised three times in the
  2026-08-01 session (photo→hazard suggestions, AI-drafted SWMS text,
  scan-and-reproduce). That problem gets solved once, later, and reused
  — not solved here.

## Decisions — Q&A 2026-08-01

| Question | Decision |
|---|---|
| Broadcast or targeted? | **Targeted only** — role, crew, site, or person. No "everyone" shortcut. |
| Gate or informational? | **Informational only** — register + reminders, nothing blocked. Revisit as a separate, explicitly-scoped decision if a real case demands a gate. |
| Versioning | **Auto-expire on new version** — a new version supersedes every prior signature; signers re-sign. |

## Rough data shape (sketch only, not a migration)

- `documents` — id, title, current_version_id, owner/uploader, tenant
- `document_versions` — id, document_id, version_no, file ref,
  uploaded_at, uploaded_by
- `document_audiences` — document_id, target type (role / crew / site /
  person) — no "all" row, per the targeted-only decision
- `document_signoffs` — version_id, user_id, signed_at, status
  (outstanding / signed / superseded)

Still just a sketch — real column/constraint design happens at migration
time, not here. But the three decisions above are locked, so the shape
won't move on those axes.

## Where it likely lives

Distribution/admin UI in Shell, signing UI in Field, register +
reminder logic as shared logic both read/write rather than owned by
either alone — same shape as Shell already centralizing auth for
apps that don't own identity themselves. Matches the existing
architecture split (asset-scoped work → Service, crew/site-scoped work
→ Field) rather than introducing a new owning app.

## Build plan (v1)

Sequenced so each phase produces something checkable before the next
starts — no big-bang schema-then-UI drop.

1. ~~**Confirm where the data lives.**~~ **DONE 2026-08-02** — `ehow` /
   `app_data`, via the eq-shell `supabase/tenant-migrations/` One Spine.
   Verified against both live planes; see the verification section above.
2. ~~**Schema.**~~ **APPLIED 2026-08-02** — eq-shell
   `supabase/tenant-migrations/0233_document_signoff_register.sql`
   (PR [#1180](https://github.com/eq-solutions/eq-shell/pull/1180)),
   dispatched via `tenant-migrate.yml`, live-confirmed on both ehow
   (sks-canonical) and zaap (eq-canonical-internal) — a real
   insert → publish → supersede round-trip was run on ehow inside a
   rolled-back transaction to prove the trigger, not just check the
   tables exist. Four tables + a `document_register` read view
   (`security_invoker`, per drift CHECK 7), tenant RLS on all four, no
   anon/PUBLIC grant. All three locked decisions are DB constraints
   rather than UI rules: no `'all'` target_kind exists so a broadcast is
   not insertable; nothing gates rostering; `tg_document_version_published`
   repoints the document and supersedes sign-offs on every other version,
   while superseded rows retain `signed_at` + `signed_content_hash` as
   the audit trail.
3. ~~**Shell: upload + push.**~~ **MERGED + DEPLOYED 2026-08-03** — eq-shell
   PR [#1196](https://github.com/eq-solutions/eq-shell/pull/1196)
   (squash `50f202f`, Royce's "merge #1196" go). `upload-document-version.ts`
   (sha256 computed server-side, publishes immediately so the 0233
   trigger handles supersede) + `push-document-audience.ts` +
   `AdminDocumentUpload.tsx` (routed `admin/documents`, tile on
   `AdminHub.tsx`). Three decisions made at this step, all Royce's
   explicit call, not inferred: audience materializes as a **snapshot at
   publish**, not dynamic membership; **crew resolves via the tenant
   canonical tables** (`app_data.teams`/`team_members` — confirmed live
   these exist on ehow but not at all on zaap, handled as an expected
   "no crews here yet" state, not an error); **site targeting is hidden
   entirely** for v1 (`app_data.staff.default_site_id` exists in-schema
   but is 0/99 populated live — no real data to push against yet).
   Permission gate is **interim** — authenticated session only, same
   posture as `list-attachments.ts` — because no permission in
   `@eq-solutions/roles`' real MATRIX cleanly fits "upload/push a
   document" and Royce's call was not to block the build on adding one.
   Netlify auto-deploys eq-shell on merge — live on core.eq.solutions or
   about to be. **Not yet click-tested live.**
4. ~~**Field: sign.**~~ **MERGED + DEPLOYED 2026-08-03** — eq-field PR
   [#627](https://github.com/eq-solutions/eq-field/pull/627) (squash
   `3d41f8f`, v3.5.434, Royce's "merge #627" go). New "Sign Documents"
   nav page reads `app_data.document_register`, shows the current
   version (via a new signed-URL helper against the private
   `attachments` bucket), one tap to sign — no drawn signature, no
   vendor, exactly as designed: identity + timestamp + the version's
   own content hash, copied not recomputed. **Deliberately pilot-gated
   to one person** (`royce.milmlow@sks.com.au` only, allowlist constant
   in `index.html`, two enforcement layers — nav hidden AND a hard
   route-block against direct navigation) rather than a general
   rollout — Field is live SKS production, real tradespeople use it
   daily, and this hadn't been proven end-to-end yet. **Known accepted
   gap, flagged not fixed:** `document_signoffs` RLS
   (`document_signoffs_tenant`) is `cmd: ALL`, tenant-scoped only —
   any authenticated tenant member could currently read OR write any
   signoff row, not just their own. Low real risk while the table
   holds nothing but what's pushed to the pilot user; a real follow-up
   once this moves past one person — needs a signer-scoped policy on
   the eq-shell side (schema owner), not something eq-field can fix
   itself.
5. ~~**Register view.**~~ **MERGED 2026-08-03** — eq-shell PR
   [#1208](https://github.com/eq-solutions/eq-shell/pull/1208) (squash
   `35b204b3`, Royce's "merge #1208" go). Extends `admin/documents`
   with a Register tab — grouped-by-document read of
   `app_data.document_register` via a new `GET ?resource=register`
   action on `push-document-audience.ts`, signer names resolved via
   the same control-plane lookup the push flow uses, outstanding/
   overdue signers surfaced first, resolved documents after.
   Live-reverified independently post-merge, not just trusted from
   the build report: `document_register`'s `due_at`/`is_overdue`/
   `last_reminded_at` columns — laid in with the original migration
   for the reminder cron below, unused until this PR — match live
   schema exactly, and the one real proven row (Environmental
   Management Plan, signed) renders correctly against a live re-run
   of the exact query. Netlify auto-deploys eq-shell on merge — build
   still in flight as of the merge, not yet confirmed live, not
   click-tested. **Reminder cron split out, not built.** This step
   originally bundled a cron (chasing outstanding signers on a
   schedule, shape of the existing pre-visit brief cron) — never
   discussed for this build, stays a real, separate, not-started
   item; the schema already carries the columns for it
   (`due_at`/`last_reminded_at`) whenever it's picked up.
6. **Rollout.** Start with one real document (candidate: an existing
   SMP) end-to-end before onboarding the rest of the switchboard
   schedule / ITC / O&M backlog into the register.

## Post-launch upgrade: real drawn signature + evidence view (2026-08-03)

Royce, after actually using the v1 pilot: *"shouldn't the signature be
actual signing box like the safety docs?"* and *"is the UI built to see
signed paperwork?"* — tap-to-confirm (identity + timestamp + content
hash, no drawing) was a deliberate v1 call, but it didn't match Prestart
Briefings/Toolbox Talks, which already capture a real drawn signature
via a shared, proven component (`createSignatureController`,
`eq-field/scripts/site-reports-shared.js`). Neither Shell nor Field had
any way to view a document or its signing evidence after the fact.
`/decide` run against the two-stage plan below; Royce: recommended
options on both, then "Go".

**Stage A — schema.** `signature_image text` added to
`app_data.document_signoffs`, exposed on `document_register` (eq-shell
migration `0235_document_signoff_signature_image.sql`, PR
[#1212](https://github.com/eq-solutions/eq-shell/pull/1212), squash
`7e7c350`). `CREATE OR REPLACE VIEW` can only append new columns, not
insert mid-list, and resets `security_invoker` on every replace unless
reasserted — both real constraints, caught and handled correctly (the
second one against a bug that's bitten this exact codebase three times
before). Dispatched and confirmed live on both ehow and zaap.

**Stage B — Field capture + Shell evidence view, built in parallel once
schema was live.**
- **eq-field** [PR #635](https://github.com/eq-solutions/eq-field/pull/635)
  (squash `a819715`, v3.5.442): `sign-documents.js` now opens the same
  canvas pad Prestart/Toolbox/Diary/Incidents already use instead of
  writing the PATCH straight off a tap — `signature_image` rides in the
  same request as the original identity/timestamp/hash evidence, not a
  second write. `safety.js`'s file header claiming to be dependency-free
  is stale (its own changelog documents the opposite); confirmed
  `site-reports-shared.js` is the real live source, and that
  `core-bundle-b1.js` is what `index.html` actually serves (the on-disk
  `lazy-loader.js` has no `<script>` tag anywhere) — same class of
  stale-comment/dead-code trap step 4 hit with `auth.js`. Both the real
  file and its bundle twin updated together.
- **eq-shell** [PR #1217](https://github.com/eq-solutions/eq-shell/pull/1217)
  (squash `d498477`): Register tab gains a "View" action per signer —
  identity, exact timestamps, content hash, the drawn signature (or a
  graceful fallback for the many rows that predate this upgrade,
  including the one real EMP signoff), and a link to the actual signed
  file via an on-demand signed-URL endpoint (chosen over eager per-row
  signing specifically to avoid redundant Storage calls on a
  multi-signer document). No new migration — reused `content_hash` and
  `signature_image`, already on the view.

Both confirmed live (core.eq.solutions and field.eq.solutions,
`commit_ref` checked against each merge commit via Netlify MCP, not
assumed). Upload → push → sign (with a real signature) → register →
evidence view is now a complete, working loop for the pilot user.

**Still open, unchanged by this upgrade:** the reminder cron (never
scoped), the known `document_signoffs` RLS gap (tenant-wide, not
signer-scoped — flagged across steps 3, 4, 5, and this upgrade, still
not fixed), and step 6 rollout (widen the Field pilot gate, onboard a
real document past the one EMP test row). All Royce's call on timing,
not a technical blocker.
