---
title: Sprint — 3 remaining "needs you" items from today's session close
owner: Royce Milmlow
created: 2026-09-09
last_updated: 2026-09-09
scope: Turns this session's close-card "needs you" list into a tight action sprint, per Royce's direct ask. Every item re-checked live at write time, not copied from the card. Explicitly does NOT include SEC-1 (sks-nsw-labour) — that's a separate, already-decided item, not touched by this session and not part of this list.
read_priority: high
status: live
---

# Sprint — 3 remaining items

Not SEC-1. Nothing below touches sks-nsw-labour. This is 3 small, unrelated items left
over from today's eq-field work, re-verified live just now before listing them here — one
originally-flagged 4th item (the `app_data.staff` write/delete RLS gap) turned out to
already be fixed on both tenants on a fresh recheck; see the correction note in
`sessions/2026-09-09.md` for what happened there. It is not on this list because there is
nothing left to do.

---

## 1. Zaap's 2 anon-executable functions (2 minutes)

`eq_get_portal_quote` and `eq_respond_portal_quote` on zaap (`zaapmfdkgedqupfjtchl`) both
grant `EXECUTE` to `anon` — confirmed live again just now, unchanged since the 2026-09-07
review flagged it. Both are also `SECURITY DEFINER`.

This is very likely fine — it reads like a public quote-response flow (a customer clicking
a link in an email, no login) — but nobody has confirmed that by reading what the functions
actually do.

**Ask:** open both function bodies (Supabase dashboard → zaap → Database → Functions, or
ask Claude to pull `pg_get_functiondef` for both) and confirm: (a) this is genuinely meant
to be public, and (b) each function scopes its work to the one quote/tenant the caller's
token proves they own, not an arbitrary ID. If both check out, this closes with no code
change — just a "yes, confirmed intentional" note in the security register.

## 2. Triage 3 stale PRs

All three confirmed still open, untouched since the review flagged them (2026-09-07):

| PR | Title | Last updated | Age |
|---|---|---|---|
| [#930](https://github.com/eq-solutions/eq-field/pull/930) | Dashboard: Headcount tiles show who's working today | 2026-09-05 | 4 days |
| [#895](https://github.com/eq-solutions/eq-field/pull/895) | Apprentices: 6 follow-ups from the full-module audit | 2026-09-02 | 7 days |
| [#890](https://github.com/eq-solutions/eq-field/pull/890) | Copy Last Week could say "saved" when the writes failed | 2026-09-02 | 7 days |

**Ask:** for each, one of: merge it, close it, or say "leave it, I'll get to it" (in which
case it just stays open, no action needed — this isn't forcing a decision, it's surfacing
that nobody's looked in over a week). #930 will need a rebase regardless — `main` has moved
significantly since 2026-09-05.

## 3. Have someone actually log into Madagins as a real user

Nobody has yet. Checked live: both Michelle (`accounts@madagins.com.au`) and Aditi
(`aditi@madagins.com.au`)'s only sign-in timestamp is the automatic one from when their
accounts were created (~30-60 seconds after `created_at`) — not a real return visit — and
`audit_log` on madagins' own database is completely empty.

This was genuinely blocked until today: the schema had real bugs (wrong-tenant RLS
policies, a missing security setting, a missing feature) fixed over the course of this
session. It's not blocked anymore.

**Ask:** have Michelle or Aditi sign in through Core for real and click around — Dashboard,
People, and whichever module they'd actually use day-to-day. This is the only way to
confirm today's database-level fixes actually work end-to-end, not just in isolation.

---

## Not on this list, on purpose

- **SEC-1** (sks-nsw-labour) — separate, already decided, not part of today's work.
- The provisioning-tool hardening items (PR #959's incomplete prerequisite list, the
  recurring `security_invoker` bug class) — these are process/tooling questions, not a
  2-minute action; they're sitting in `eq/pending/eq-field.md`'s madagins section for when
  there's time to actually discuss them, not squeezed into this list.
