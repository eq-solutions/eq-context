# Access-model parity harness

Snapshot every user's **effective permissions** (role ∪ group perms ∪ tenant
overrides − denials, via `@eq-solutions/roles`'s `resolveEffectivePermissions()`)
so a change to the canonical matrix, a tenant override, or a security group can
be diffed before/after. "No diff" is a single hash comparison, not a manual read.

Part of the [Access-Model Plan](../ACCESS-MODEL-PLAN.md) — the gate for every
phase after Phase 0.

## Files
- `raw-grants-<date>.json` — one row per active (user, tenant) membership, pulled
  from jvkn (`shell_control.user_tenant_memberships` join `security_group_perms`
  join `tenant_role_overrides`). See the SQL in the plan doc / session log for
  the exact query — re-run it fresh before each snapshot.
- `compute-snapshot.mjs` — pure function: raw grants in, sorted effective-perms
  + a SHA-256 hash out.
- `snapshot-<date>-{before,after}.json` — committed outputs. Diff the `hash`
  field first; only read `results` if it changed.

## Running it
`compute-snapshot.mjs` imports `@eq-solutions/roles` by package name, so Node's
module resolution needs to find it — which means the script must be run from
*inside* a tree where that package resolves (Node resolves relative to the
**importing file's** location, not the shell's cwd).

```
cp compute-snapshot.mjs /c/Projects/eq-roles/_tmp-compute-snapshot.mjs
cd /c/Projects/eq-roles
node _tmp-compute-snapshot.mjs /path/to/raw-grants-<date>.json > /path/to/snapshot-<date>.json
rm _tmp-compute-snapshot.mjs
```

(If eq-roles ever gains a proper workspace/npm link setup, this step-around
stops being necessary — swap for a plain `node compute-snapshot.mjs`.)

## Baseline
`snapshot-2026-07-08-before.json` — hash `37300a13c30ca0598bbad675dbf4eedc5245edcd5e87cecae2c833065f77eee0`,
49 rows across 4 tenants (SKS, EQ, Favour Perfect, + a 4th all-`employee`
no-signal tenant — almost certainly the `__personal__`/default tenant Cards
workers land on, not a real Shell-facing business tenant).

Every phase from here re-pulls raw grants, re-runs the harness, and the diff
against the previous snapshot IS the safety check — not a promise, a number.

## Incident note (2026-07-08)
This whole folder + `ACCESS-MODEL-PLAN.md` were written, confirmed successfully,
then found **missing from disk** later the same session — a concurrent Claude
Code session's activity in this same non-worktree `eq-context` checkout (a
`/close` run that landed commit `8199f19`) most likely ran a destructive
operation (`git clean`/`checkout --`) that wiped untracked files in between.
Recreated faithfully from the authoring session's own transcript — the
regenerated snapshot hash matches the originally reported value exactly.
**Lesson: commit substrate writes immediately, don't batch them for later.**
