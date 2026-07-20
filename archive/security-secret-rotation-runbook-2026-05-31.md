---
title: SECURITY — EQ_SECRET_SALT rotation & backup runbook
owner: Royce Milmlow
last_updated: 2026-05-31
scope: EQ SSO shared HMAC key — backup, coordinated rotation across the Netlify deploys, cadence, per-app split
read_priority: reference
status: live
---

# SECURITY — EQ_SECRET_SALT rotation & backup runbook

## What this secret is

`EQ_SECRET_SALT` is the HMAC-SHA256 key behind every signed token EQ Shell
issues. All token code lives in eq-shell `netlify/functions/_shared/token.ts` —
a single `SECRET_SALT = process.env.EQ_SECRET_SALT`; `sign()` throws if unset.

It signs:

- the `eq_shell_session` cookie (login → all of Shell) — `signSessionToken` / `verifySessionToken`
- the **Field** iframe handoff token (`mint-iframe-token` → `ShellTokenPayload`),
  verified by EQ Field's `verify-pin` (`action=verify-shell-token`)
- the **Service** iframe handoff token (`mint-service-iframe-token` → `ServiceTokenPayload`),
  verified by EQ Service's `/.netlify/functions/shell-auth`
- the **Quotes** handoff token (`mint-quotes-iframe-token` → `QuotesTokenPayload`) —
  Phase 3, not yet a live consumer

**Cards is the exception.** `mint-cards-iframe-token` mints a **Supabase JWT**
(signed with `SUPABASE_JWT_SECRET`, 15-min TTL), NOT an `EQ_SECRET_SALT` token.
The eq-cards deploy still holds `EQ_SECRET_SALT` because its own shell-session
verification (`eq-cards/.../shell-verify.js`) reads the salt-signed Shell cookie.
So a salt mismatch on the Cards deploy breaks Cards' *cookie* path, not the JWT
hash handoff. Confirm exact behaviour against eq-cards functions before rotating.

Background: eq-shell `README.md` → "Required environment variables (Netlify)"
and eq-shell `CLAUDE.md` → "Don't touch without checking downstream".

## Where it lives today

| Location | Context | Role |
|---|---|---|
| Netlify env — **eq-shell** | Production (+ Deploy Previews) | Minter for all handoffs + session cookie |
| Netlify env — **eq-solves-field** | Production | Verifies Field handoff |
| Netlify env — **eq-solves-service** | Production | Verifies Service handoff |
| Netlify env — **eq-cards** | Production | Verifies Shell session cookie (see Cards note) |
| Dev `.env` files (gitignored) | local | Each dev running `netlify dev` |
| **(gap) no vault backup** | — | If all Netlify copies are wiped, value is unrecoverable → must rotate everywhere |

## Who can access it

- Anyone with a Netlify team role that can view env vars on those sites.
- Anyone holding a local `.env`.

Keep Netlify team membership tight. The vault entry below is the canonical
backup, not a second live source.

## Secure backup — do this once, now

Create ONE entry in the team password manager (1Password / Bitwarden — whichever
EQ standardises on). **Not** in any git repo, **not** in eq-context as plaintext.

Entry contents:

- name: `EQ_SECRET_SALT (EQ SSO HMAC key)`
- the value — paste directly from Netlify; never echo to a terminal, log, or commit
- consuming sites: eq-shell, eq-solves-field, eq-cards, eq-solves-service (+ Quotes when live)
- last-rotated date, who rotated, link to this runbook
- access restricted to the owner + whoever can deploy these sites

To back up without exposing the value: copy from the Netlify UI (eq-shell → Site
config → Env vars → reveal) straight into the vault field. Never via chat, a
file, a shell command, or a commit. **This doc must never contain the value.**

## Rotation procedure

### The constraint

`token.ts` is **single-key** — it verifies with exactly one salt, no grace path.
The moment a site's functions pick up a new salt:

1. **Session cookies:** every live `eq_shell_session` signed with the old salt
   fails → all Shell users must log in again. Expected, not a bug.
2. **Iframe handoffs (60s TTL):** the handshake only validates while minter
   (Shell) and verifier (Field/Service) hold the SAME salt. With one key, no
   ordering avoids a brief window where the two disagree.

### Netlify behaviour that matters

A function reads `process.env.EQ_SECRET_SALT` at runtime, but the value is
snapshotted into the deploy. **Changing the env var only takes effect after that
site redeploys.** "Redeploy goes live" = the cutover instant. Four redeploys
cannot go live at the same millisecond.

### Option A — proper fix (recommended): dual-key grace window *(small code change, separate PR)*

Add `EQ_SECRET_SALT_NEXT`. Make every `verify*Token` (and the session-cookie
verify) try `EQ_SECRET_SALT` then `EQ_SECRET_SALT_NEXT`; keep `sign()` on the
primary. Rotation then has **zero** handshake gap and no forced re-login:

1. Set `EQ_SECRET_SALT_NEXT = <new>` on all sites; redeploy. Everyone now *accepts* old or new.
2. Promote: set `EQ_SECRET_SALT = <new>`, clear `_NEXT`, on all sites; redeploy. Everyone signs+accepts new; old is dead.

The ~5s host clock skew is irrelevant here — both keys are valid throughout.
This is the only way to truly rotate without breaking the 60s handoff. Track as
a security-backlog item.

### Option B — no-code rotation available today *(accept a short maintenance window)*

1. Pick a low-traffic window; warn users SSO will blip and they'll re-login once.
2. Generate a new high-entropy value (≥32 bytes, e.g. `openssl rand -hex 32`).
   Don't keep it in shell history beyond pasting into Netlify + vault.
3. Set the env var on ALL of eq-shell, eq-solves-field, eq-cards,
   eq-solves-service (Production; mirror to Deploy Previews per
   eq-shell `docs/runbooks/deploy-preview-env.md`). Value set, not yet redeployed.
4. Trigger redeploys on all four **back-to-back** (same minute). They go live
   within ~1–3 min of each other; that span is the gap window.
5. During the gap, new iframe handoffs may fail at "Authorising…". Because tokens
   are 60s and re-minted on mount, a retry once both sides are live succeeds.
   No data risk — only transient handshake failures.
6. Verify (below), then update the vault entry's value + last-rotated date.
7. Update each dev's local `.env`.

### Verify after rotation

- `curl -i https://core.eq.solutions/.netlify/functions/verify-shell-session`
  → `401 {"valid":false}` (function healthy, salt loaded).
- Browser smoke: sign in at core.eq.solutions, click into /field, /service,
  /cards — each iframe must load past "Authorising…".
- Preview: `./scripts/smoke-preview.sh https://deploy-preview-<N>--eq-shell.netlify.app`.
- No `Server misconfigured — missing EQ_SECRET_SALT` 500s in Netlify logs / Sentry (`eq-shell`).

### Do NOT during rotation

- Don't shorten the 60s TTL to "speed up" expiry — with ~5s skew the usable
  window is already ~55s; tightening risks rejecting valid tokens.
- Don't rotate one site and leave others — partial rotation = permanent SSO break.
- Don't store the new value anywhere except Netlify + the vault.

## Cadence recommendation

**Default: rotate on compromise / personnel change, not on a calendar.** With the
single-key design, every scheduled rotation forces a suite-wide re-login + a
handshake blip — real friction for a key that never leaves the server (it is not
exposed to browsers). Calendar rotation only becomes worthwhile once Option A lands.

Mandatory triggers regardless of cadence:

- Netlify account compromise
- a departing person who had env or deploy access
- the value leaking into a log / commit / screenshot
- contractor offboarding

Once dual-key (Option A) exists, an **annual** rotation is cheap — adopt it then.
Either way, keep the vault entry's last-rotated date current so staleness shows.

## Per-app keys later?

**Yes — move to per-consumer keys once handshakes are stable, but as a deliberate
later step.** Today one key signs the cookie + Field + Service (+ Quotes), so a
leak's blast radius is the whole suite, and Field's trust cannot be re-established
without logging everyone out.

Target: a distinct signing key per relationship — e.g. `EQ_FIELD_HANDOFF_KEY`,
`EQ_SERVICE_HANDOFF_KEY`, and a separate `EQ_SESSION_SALT` for the cookie. Then a
Field-side incident rotates only Field's key; cookie + Service stay untouched.

Sequencing: land Option A (dual-key verify) first — it is the mechanism that makes
*any* rotation break-free, and per-app keys are just "more keys to rotate." Do
per-app keys as a follow-on.
