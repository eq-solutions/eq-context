# Session 2026-07-30 — guard.js selftest fixed; ~/.claude brought under version control

## Built
- Root-caused `selftest.js` 10/11 failure: rule 8 (`brief-gate`, force:true) was
  piggybacking on the test harness's `write()` cases and forcing a deny the
  "inline password write" case didn't expect — not a bug in rule 2 (scan-secrets)
  or the `decide()` blockers filter, both of which were already correct.
- Fixed `selftest.js` to default every invocation to `EQ_SKIP_BRIEF=1`, isolating
  each case to the rule it targets. `guard.js` itself needed no change.
  11/11 now passes.
- `git init`'d `C:\Users\EQ\.claude` (had no git history, no parent repo either).
- Added `.gitignore` excluding `.credentials.json`, session/cache/telemetry/
  chrome/shell-snapshot data, `hooks/guard.log`, and the `plugins/marketplaces/`
  third-party clone.
- Committed the selftest fix (`59cacf2`), then the rest of the directory's
  config on request — CLAUDE.md, hooks, settings.json, commands/, plans/,
  plugins metadata, reference docs, misc SQL (`e5b9a14`).

## Decided
- `~/.claude` config is worth version-controlling; sensitive/regenerable
  content (credentials, session data, third-party clones, churn logs) stays
  out via `.gitignore` rather than blanket-excluded from git entirely.

## Deferred
- **Remote + push for `~/.claude`** — asked where to push (new private repo
  vs. existing repo vs. hold off) given `plans/` contains SKS live-Supabase
  (`nspbmirochztcjijmcrx`) lockdown/remediation SQL that must never be public.
  Not yet answered — repo is local-only, 2 commits on `master`, no remote.

## Notes
- Checked `guard.log` for evidence of scan-secrets or brief-gate ever falsely
  blocking a legitimate real-session write — none found; every logged
  instance was `MODE=warn` and brief-gate's force-block behaviour matches its
  documented design.
- `notif_1.sql` / `notif_2.sql` / `notifications_insert.sql` (now committed in
  the second `~/.claude` commit) contain UUID-keyed notification rows, no
  plaintext PII spotted in spot-checks — flagged to Royce as worth a second
  look given the repo has no remote yet, easy to scrub from history if needed.
