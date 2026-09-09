---
title: eq-shell Sentry follow-ups — sprint
owner: Royce Milmlow
created: 2026-09-09
last_updated: 2026-09-09
scope: Everything left open from today's two eq-shell Sentry sweeps, cross-checked live against Sentry and git immediately before writing this — not copied from an earlier chat summary. Excludes Madagins/tenant-architecture work, which has its own more authoritative sprint (see the cross-reference below) rather than being duplicated here.
read_priority: high
status: live
---

# eq-shell Sentry follow-ups — sprint (2026-09-09)

## Read this first — a possible collision with in-flight work

`eq-shell-wt-pgcron` (branch `fix/tenant-provisioning-pg-cron`, uncommitted as of this
write) reconstructs ~37 legacy `public.*` objects onto Madagins' own dedicated Supabase
project (`ornndtbdkxfsewspbrwk`) plus fixes a missing `pg_cron` extension there — a lot of
careful, real work.

**`eq/sprints/2026-09-09-tenant-onboarding-sprint.md`** (written the same day, via a full
`/decide` pass) reaches a different, decided conclusion: **shared ehow is the default data
plane for every new tenant; a dedicated project is an explicit opt-in escape hatch, not
the default** — and its item #5 is "archive the orphaned `eq-tenant-madagins` Supabase
project." If that decision holds, the dedicated-project migration work in
`eq-shell-wt-pgcron` may be solving a problem about to be deleted rather than fixed.

Not resolved here — didn't want to guess at which one is current without asking. **Whoever
picks up `eq-shell-wt-pgcron` next should read the tenant-onboarding sprint's Decision #1
first**, and confirm with Royce whether that work still applies before finishing it.

---

## Still genuinely open (verified live just before writing this)

### 1. EQ-SHELL-1R — EQ Field doesn't finish loading after a successful handoff
**Status: unresolved, regressed. Real and growing** — 3+ users hit this today across
different roles/devices (supervisor on Android, apprentice on iPhone), most recently
within the last hour. Every occurrence shows the same shape: shell-side token mint
completes in under 2 seconds every time — the stall is entirely downstream, inside EQ
Field's own load path, between "handoff accepted" and first render.

**Not eq-shell's to fix** — needs a session rooted in eq-field. The brief is ready:

> Sentry issues EQ-SHELL-1R and EQ-SHELL-21 (eq-shell org, both culprit `/sks/field`) show
> the shell-side handoff — token mint, iframe boot, handoff-accept — completing cleanly in
> under 5 seconds every time. The failure is specifically post-accept, pre-render: EQ Field
> knows who the user is but sometimes takes 12s to multiple minutes to actually paint
> content. Profile what's slow between "handoff accepted" and first meaningful render —
> likely a slow query or asset load on mount for at least the supervisor/apprentice roles.
> Live-verify against real logs, don't just read source.

### 2. EQ-SHELL-23 — test-account cleanup is deliberately partial
Jordan A. Sample's `app_data.staff` row is deactivated and both licences are gone (done
this session, on your go-ahead). The Sentry check will very likely still fire once more —
downgraded from `invisible_licences` to the milder `at_risk`, since nothing is actually
hidden anymore. Fully silencing it needs the jvkn-side shell account + tenant membership
closed too, which is a bigger action than what you scoped.

**Needs your call:** close it out fully, or leave it as a quiet `at_risk`?

### 3. Netlify auto-deploy silently didn't fire on a real merge today
PR #1826 (the Firefox chunk-crash fix) merged cleanly — CI, secret scan, and the
tenant-drift checks all passed, the repo's own `notify` and release-tag automation both
ran — but Netlify itself never created a deployment record for that commit. No status
check, no queued build, nothing. Worked around with a one-off manual deploy via the
Netlify MCP; the underlying webhook/git-integration issue is still unexplained.

**Needs your call:** check the site's GitHub integration status directly in the Netlify
dashboard when convenient. This isn't blocking anything today, but the "merge = deploy"
assumption this repo runs on doesn't hold if it recurs.

---

## Watching, not acting — deliberately

### 4. EQ-SHELL-T / EQ-SHELL-V — the intermittent sign-in stall
Quiet since 2026-09-06 (no new occurrences across either today's sweeps). Correctly set to
`ignored, archived_until_escalating` — the right call given the quiet trend, not a fix.
Root cause was never actually found despite two sessions' worth of investigation (client
code doesn't explain the multi-fetch pattern seen in two separate replays) — if it
escalates again, start from `eq/pending/eq-shell.md`'s existing write-up rather than
re-deriving from scratch, and go straight to watching replay `ee5ceacc486f425fb42efb3115a3e219`
directly rather than more automated digging.

---

## Summary

| # | Item | Status | Next |
|---|---|---|---|
| — | Madagins dedicated-project work may collide with a decided architecture change | **Flagged, not resolved** | Read the tenant-onboarding sprint's Decision #1 before finishing `eq-shell-wt-pgcron` |
| 1 | EQ-SHELL-1R (EQ Field slow to render post-handoff) | Open, growing | Needs an eq-field-rooted session — brief above |
| 2 | EQ-SHELL-23 residual | Partial by design | Your call: close fully or leave at `at_risk` |
| 3 | Netlify auto-deploy didn't fire on a real merge | Unexplained | Check the Netlify dashboard's GitHub integration |
| 4 | EQ-SHELL-T/V | Quiet, ignored-until-escalating | Watch only — replay link above if it returns |
