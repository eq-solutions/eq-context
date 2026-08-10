---
title: Simultaneous users across the EQ Suite
owner: Royce Milmlow
last_updated: 2026-08-11
scope: How session/auth concurrency actually works today, per app — verified against live code and git history, not assumed. system/punch-list.md item 12.
read_priority: standard
status: live
---

# Simultaneous users across the EQ Suite

**Verdict up front:** multi-device-same-person is architecturally sound by
design — stateless, independently-revocable sessions everywhere, no seat
caps anywhere in the platform. There's exactly one real bug in that scenario,
already fixed and live (Cards' multi-tab session collision). The
multi-person-same-tenant-at-volume question — 20+ technicians logging in at
once during a shift change — has never been empirically tested. Say that
plainly rather than extrapolating from the one number that does exist.

---

## Why Cards had a bug and the others don't (yet)

The four apps use three different session mechanisms. That difference is
the whole story:

| App | Session lives in | Rotating GoTrue refresh token? |
|---|---|---|
| **Shell** | HttpOnly cookie, custom HMAC-signed, own mint | No |
| **Field** | `sessionStorage` (tab-scoped) + `localStorage` for "remember me" | No — custom JWTs, no GoTrue session ever created |
| **Service** (Shell-embedded) | httpOnly cookie, custom-minted, 4h TTL | No — same pattern as Field/Shell |
| **Service** ("EQ entity" direct-login) | Supabase session via `@supabase/ssr` | **Yes** — real GoTrue session |
| **Cards** | Browser storage shared per-origin across every tab/iframe | **Yes** — real, persistent, auto-rotating, even via the Shell handoff |

Shell, Field, and Service's Shell-embedded path all deliberately avoid a
persistent, auto-rotating GoTrue session — a documented design choice
(`eq/identity/IDENTITY-MODEL.md` §9). Cards is the one app that both
persists a real rotating session in shared browser storage *and* is
routinely opened in multiple tabs at once (every Shell tenant tile opens a
fresh Cards iframe). That combination is what produced the bug — and why
it's structurally specific to Cards, not a platform-wide risk.

---

## Per-app mechanics

**Shell** — 7-day HMAC-signed cookie, unique `jti` per session, each
individually revocable without touching a user's other sessions. **No
concurrent-session cap anywhere** — confirmed directly in code, multiple
devices/tabs per person is expected and normal. Role/entitlement changes
reach an already-open tab within 5 minutes (a live poll, not aspirational).
`verify-shell-session` fails **closed** on a lookup error — a Supabase hiccup
401s every session, not just the one that should die.

**Field** — three separate auth surfaces (Shell/JWT handoff for SKS; a
legacy PIN gate still live for the demo tenant only; `sks-nsw-labour` as a
fully separate codebase). Login state lives in `sessionStorage`
(tab-scoped — each tab independently re-runs its own handoff, can't inherit
another tab's stale state). No GoTrue session is ever created, so Field
structurally cannot reproduce Cards' rotation race.

**Service** — two paths: SKS/ehow via a custom-minted 4h cookie with a
proactive self-healing refresh (`ShellTokenRefresh.tsx`, refreshes 5 min
before expiry) and a full recovery flow for total cookie loss
(`ShellSessionRecovery.tsx`, one-attempt-per-tab guard, manual fallback
button); the standalone "EQ entity" tenant via a real Supabase/GoTrue
session. Handoff failures are actively monitored in Sentry with severity
tiers, not handled blind.

**Cards** — real GoTrue session, rotating refresh tokens, shared per-origin
storage. The Shell handoff itself becomes a full session (`verifyOTP`
exchange into a real `auth.sessions` row) — this is the one bridge that
converts a short-lived handoff token into a long-lived, auto-rotating
session, and the root of its unique exposure. Native mobile uses
keychain-backed secure storage with no "tabs" concept — the bug is a
web/iframe-embedding failure mode only.

---

## The Cards bug, precisely (fixed, live since 2026-08-05)

Every `cards.eq.solutions` iframe across every open Shell tab shares the
same origin's storage. A refresh-token rotation triggered by one tab
invalidated the cached session another tab still held — reproduced live
2026-08-04, GoTrue rejected the stale token with 403 "missing sub claim,"
and the app silently fell through to the email sign-in screen instead of
running the working Shell handoff.

- **PR #212** — validate any cached session with a live `getUser()` call
  before trusting it.
- **PR #212 introduced a second bug**, caught same day, fixed by **#216** —
  it skipped the handoff whenever *any* session validated, even a valid
  session for a *different* identity. Final shape: `?shell=1` always asks
  Shell first; a validated local session is only a fallback when Shell
  itself can't produce a token.
- **A related bug, same window (PR #215):** two screens each independently
  retried `refreshSession()` up to 3× waiting for `tenant_id` — a real
  signup triggered 12+ concurrent refresh calls in 90 seconds, racing
  GoTrue's single-use rotation and forcing a mid-signup sign-out. Same
  underlying rotation-race class, fixed same window.

No open follow-up tied to the collision mechanism itself.

---

## Proven safe vs. genuinely untested

**Proven, with evidence:**
- Cards' specific multi-tab collision — fixed, no reproducing code path left.
- No concurrent-session cap anywhere in the platform (code-verified negative).
- Role/entitlement propagation to open tabs within 5 minutes (verified against the actual poll code).
- Service's Shell-embedded session has a shipped, monitored self-healing path for both routine expiry and total cookie loss.
- Field's tab-scoped storage structurally avoids the Cards-style collision.

**Genuinely untested — do not treat these as settled:**
- **A synchronised login-burst load test has never been run.** Flagged open 2026-08-06, still open. Two live-fire attempts at an adjacent question (can Field scale to 300–1,200 people with a shift-start burst) were both abandoned — one failed on infra, one was correctly blocked by the safety classifier as DoS-shaped. The fallback answer was a **calculation**, not a fired test: sks-labour's DB allows 60 simultaneous connections, ~25 in normal use, so headcount is fine under real login behaviour. **That figure is scoped to sks-labour specifically** (the older standalone DB) — no equivalent connection-pool figure exists for the newer per-tenant projects (ehow/eq-canonical/eq-canonical-internal) that Shell/Field/Service actually run against day to day.
- **Service's standalone "EQ entity" direct-login path** uses the same risk *class* as Cards (rotating refresh token, shared per-origin storage) — cookie-based rather than localStorage, not typically iframe-embedded, no incident reported, but also never tested. Worth a deliberate check, not a known defect.
- **Netlify Function concurrency has no configured ceiling and no measured one** — confirmed only negatively (no provisioned-concurrency knob exists), the actual account-level ceiling has never been measured.

---

## Real limits that do exist

1. **Shell login rate limit — 5 attempts per IP per 15 minutes**, keyed by IP, cleared on success. Mostly a brute-force guard, but because the increment happens before the clear, a genuinely simultaneous burst of 6+ *correct* logins from one IP (a shift-change crew on shared site WiFi, all logging in the same second) could produce spurious 429s — a real edge case distinct from what the limit was designed to catch.
2. **Field's PIN lockout is also per-IP**, but only triggers on wrong codes — doesn't threaten a burst of correct simultaneous logins.
3. **sks-labour: 60 simultaneous DB connections** (documented, not load-tested against; scope-limited to that one legacy project — see above).
4. **No seat/license/concurrent-user cap anywhere** — confirmed twice, independently.

---

## Multi-device-same-person vs. multi-person-same-tenant

These are different scenarios with different answers — conflating them is
the easiest way to overclaim safety:

| Finding | Which scenario |
|---|---|
| No session cap; independent, revocable sessions per device | Multi-device same-person — safe by design |
| Cards' fixed collision bug | Multi-device same-person specifically — only manifests with multiple tabs/tiles open at once |
| Shell's login rate-limit edge case | Multi-person same-tenant, same location/NAT |
| sks-labour's 60-connection figure | Multi-person same-tenant at scale — calculated, not tested, and scoped to one legacy DB |
| Netlify Function concurrency (unmeasured) | Multi-person same-tenant at volume — genuinely unknown |

**Bottom line:** the platform is sound for how people actually use it today
(one person, multiple devices). The real open question — many people, same
moment, same tenant — has a plausible answer for one legacy database and no
answer at all for the databases the platform actually runs on now. That gap
is real and worth closing with an actual test before it matters, not before
it's asked about again.
