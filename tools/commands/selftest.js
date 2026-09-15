#!/usr/bin/env node
'use strict';

// Self-test for guard.js. Run: node .claude/hooks/selftest.js
// Sensitive literals are built from parts so this file can be written/scanned
// without the guard's own scan-secrets / block-sks-live rules tripping on it.

const { execFileSync, spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');
const GUARD = path.join(__dirname, 'guard.js');

// Real worktree fixtures (own + a sibling), each with an actual .git gitlink
// file, so rule 1 (block-worktree-write, pure string comparison) can be tested
// in isolation from rule 1b (detect-fake-worktree, force:true, fs.existsSync-
// based) -- any /worktrees/<name>/ or -wt path with no real .git makes 1b
// force-block unconditionally, which would swallow whatever rule 1 itself
// decided and make its cases pass/fail for the wrong reason. Created fresh
// under the OS temp dir and torn down after the run.
// NOT "...-wt-<pid>" -- that shape would itself match rules 1b/1c's own
// per-segment -wt(-.*)?$ check (widened 2026-09-08) on this root segment,
// which sits ahead of every real nested-worktree segment in the path and
// wins the loop's break-on-first-match, since it has no .git of its own.
// Confirmed live: broke 9 previously-passing cases the moment the infix
// widening landed, all of them paths nested under this root.
const fixtureRoot = path.join(os.tmpdir(), 'eq-guard-selftest-' + process.pid);
const mineDir = path.join(fixtureRoot, 'worktrees', 'myworktree');
const otherDir = path.join(fixtureRoot, 'worktrees', 'otherworktree');
// No .git written here -- deliberately the "looks like a worktree, isn't
// one" fixture for the detect-fake-worktree regression cases below.
const fakeDir = path.join(fixtureRoot, 'worktrees', 'fakeworktree');
fs.mkdirSync(mineDir, { recursive: true });
fs.mkdirSync(otherDir, { recursive: true });
fs.mkdirSync(fakeDir, { recursive: true });
fs.writeFileSync(path.join(mineDir, '.git'), 'gitdir: ../../../.git/worktrees/myworktree\n');
fs.writeFileSync(path.join(otherDir, '.git'), 'gitdir: ../../../.git/worktrees/otherworktree\n');
const toWin = p => p.replace(/\\/g, '/');
const toGitBash = p => toWin(p).replace(/^([A-Za-z]):/, (_, d) => '/' + d.toLowerCase());
const mineWin = toWin(mineDir), mineGitBash = toGitBash(mineDir);
const otherWin = toWin(otherDir), otherGitBash = toGitBash(otherDir);

// Infix-named (<repo>-wt-<topic>, NOT nested under worktrees/) counterparts
// of the fixtures above -- added alongside widening rules 1 (block-worktree-
// write), 1b and 1c (detect-fake-worktree, isFile/shell) to also recognize
// this shape, same audit finding cited at rule 10's fix (system/failures.md
// F16): infix is the dominant live worktree-naming convention, not just a
// trailing -wt suffix. realInfixDir has a genuine .git (isolates rule 1's
// own cross-worktree comparison from 1b's fake-worktree force-block, same
// reason mineDir/otherDir do above); fakeInfixDir deliberately has none --
// the infix-named twin of fakeDir, for 1b/1c's own regression cases.
const realInfixDir = path.join(fixtureRoot, 'eq-context-wt-f9-mine');
const fakeInfixDir = path.join(fixtureRoot, 'eq-context-wt-f9-fake');
fs.mkdirSync(realInfixDir, { recursive: true });
fs.mkdirSync(fakeInfixDir, { recursive: true });
fs.writeFileSync(path.join(realInfixDir, '.git'), 'gitdir: ../../.git/worktrees/infixmine\n');

// Fixtures for rule 11 (warn-untracked-migrations): real git repos (git
// status is what the rule actually shells out to) named to exercise the
// eq-field-only scoping. migEqFieldDir has an UNTRACKED supabase/migrations
// .sql -> must warn. migEqFieldCleanDir has the SAME file already committed
// -> must not warn (proves it's untracked-specific, not presence-specific).
// migOtherRepoDir has the untracked file but is named eq-service, not
// eq-field -> must not warn (proves the scoping the task explicitly
// requires -- this rule must never fire outside eq-field).
const migEqFieldDir = path.join(fixtureRoot, 'eq-field');
const migEqFieldCleanDir = path.join(fixtureRoot, 'eq-field-clean');
const migOtherRepoDir = path.join(fixtureRoot, 'eq-service');
function initMigFixture(dir, { tracked }) {
  fs.mkdirSync(path.join(dir, 'supabase', 'migrations'), { recursive: true });
  execFileSync('git', ['init', '--quiet'], { cwd: dir });
  execFileSync('git', ['config', 'user.email', 'test@test.com'], { cwd: dir });
  execFileSync('git', ['config', 'user.name', 'test'], { cwd: dir });
  fs.writeFileSync(path.join(dir, '.gitkeep'), '');
  execFileSync('git', ['add', '.gitkeep'], { cwd: dir });
  execFileSync('git', ['commit', '-m', 'init', '--quiet'], { cwd: dir });
  fs.writeFileSync(path.join(dir, 'supabase', 'migrations', '20260101_test.sql'), '-- test\n');
  if (tracked) {
    execFileSync('git', ['add', 'supabase/migrations/20260101_test.sql'], { cwd: dir });
    execFileSync('git', ['commit', '-m', 'add migration', '--quiet'], { cwd: dir });
  }
}
initMigFixture(migEqFieldDir, { tracked: false });
initMigFixture(migEqFieldCleanDir, { tracked: true });
initMigFixture(migOtherRepoDir, { tracked: false });

// Fixtures for rule 10's inWorktree10 naming fast-path (stale-main-gate).
// A real bare "remote" plus two plain `git clone`s (not `git worktree add`,
// so both get their own real .git directory -- git-dir === git-common-dir
// for either one, meaning the git-dir/git-common-dir fallback a few lines
// below the fast-path correctly says "not a worktree" regardless of name.
// Only the naming fast-path itself can make inWorktree10 true here, which
// is exactly what these two cases isolate). Both clones are exactly 1
// commit behind origin/main once the seed pushes a second commit below, so
// `git commit` on either is a genuine stale-main-gate trigger unless the
// naming heuristic exempts it first: staleControlDir (no special name) is
// the negative control that proves the fixture really is behind and really
// blocks; staleInfixDir uses the <repo>-wt-<topic> infix shape eq-context's
// own worktree-registry audit found is the dominant live convention
// (system/failures.md F16, 2026-09-08) -- the fast-path regex only ever
// recognized a trailing -wt suffix before this fix, so this case denied
// (wrongly) pre-fix. Deliberately a SEPARATE temp root from fixtureRoot
// above, not nested under it: fixtureRoot's own basename already contains
// "-wt-" (eq-guard-selftest-wt-<pid>), which would confound staleControlDir
// as a negative control the moment the fast-path regex learns to match the
// infix shape.
const staleFixtureRoot = path.join(os.tmpdir(), 'eq-guard-selftest-stale-' + process.pid);
const staleRemoteDir = path.join(staleFixtureRoot, 'stale-remote.git');
const staleSeedDir = path.join(staleFixtureRoot, 'stale-seed');
const staleControlDir = path.join(staleFixtureRoot, 'plain-clone');
const staleInfixDir = path.join(staleFixtureRoot, 'eq-context-wt-f9-worktree-isolation');

execFileSync('git', ['init', '--bare', '--quiet', staleRemoteDir]);
// A fresh bare repo's HEAD points at whatever init.defaultBranch resolves
// to, which may not be "main" and doesn't exist yet either way -- cloning a
// repo with a dangling HEAD checks out nothing. Repointing it before the
// first push guarantees both clones below actually check out main.
execFileSync('git', ['symbolic-ref', 'HEAD', 'refs/heads/main'], { cwd: staleRemoteDir });

execFileSync('git', ['init', '--quiet', staleSeedDir]);
execFileSync('git', ['config', 'user.email', 'test@test.com'], { cwd: staleSeedDir });
execFileSync('git', ['config', 'user.name', 'test'], { cwd: staleSeedDir });
fs.writeFileSync(path.join(staleSeedDir, 'a.txt'), '1\n');
execFileSync('git', ['add', 'a.txt'], { cwd: staleSeedDir });
execFileSync('git', ['commit', '-m', 'c1', '--quiet'], { cwd: staleSeedDir });
// Rename whatever init.defaultBranch produced to "main" regardless -- safe
// here (unlike before the first commit) since the branch ref concretely
// exists by now.
execFileSync('git', ['branch', '-m', 'main'], { cwd: staleSeedDir });
execFileSync('git', ['remote', 'add', 'origin', staleRemoteDir], { cwd: staleSeedDir });
execFileSync('git', ['push', '--quiet', 'origin', 'main'], { cwd: staleSeedDir });

// Both taken while the remote is still at c1 -- each becomes exactly 1
// commit behind origin/main the instant the seed pushes c2 below.
execFileSync('git', ['clone', '--quiet', staleRemoteDir, staleControlDir]);
execFileSync('git', ['clone', '--quiet', staleRemoteDir, staleInfixDir]);

fs.writeFileSync(path.join(staleSeedDir, 'a.txt'), '2\n');
execFileSync('git', ['commit', '-am', 'c2', '--quiet'], { cwd: staleSeedDir });
execFileSync('git', ['push', '--quiet', 'origin', 'main'], { cwd: staleSeedDir });

// Fixtures for rule 8 (brief-gate) -- previously UNTESTED entirely (this
// file's own decision() helper defaults EQ_SKIP_BRIEF: '1' specifically so
// no other case accidentally exercises it -- see that function's own
// comment). Written to the SAME hardcoded path guard.js itself checks
// (C:/Users/EQ/AppData/Local/Temp, not os.tmpdir() -- unlike every other
// fixture in this file, rule 8 never resolves that path dynamically), so
// this suite only produces a meaningful result run on the one machine
// guard.js is itself hardcoded for -- true of the rest of this file too
// (every fixture assumes a real git.exe, a real Windows temp dir).
//
// briefFlagFresh: the CURRENT (post-2026-09-15) dateless shape for one
// specific session id -- proves a same-session flag satisfies the gate.
// briefFlagOldFormatOtherSession: the OLD, pre-2026-09-15 dated shape, for
// a DIFFERENT session id than the one under test -- a leftover a session
// running old brief.md against new guard.js (or vice versa, mid-rollout)
// could plausibly produce. Proves it does NOT satisfy the gate for an
// unrelated session id, i.e. the fix didn't accidentally start matching
// "any eq-brief-* file" instead of the exact per-session name.
const BRIEF_TEMP = 'C:/Users/EQ/AppData/Local/Temp';
const briefSidFresh = 'selftest-brief-fresh-' + process.pid;
const briefSidNone = 'selftest-brief-none-' + process.pid;
const briefSidOtherSession = 'selftest-brief-other-' + process.pid;
const briefFlagFresh = `${BRIEF_TEMP}/eq-brief-${briefSidFresh}.flag`;
const briefFlagOldFormatOtherSession = `${BRIEF_TEMP}/eq-brief-2026-01-01-${briefSidOtherSession}.flag`;
fs.writeFileSync(briefFlagFresh, '');
fs.writeFileSync(briefFlagOldFormatOtherSession, '');

const SKS_ID = 'nspb' + 'mirochztcjijmcrx';
const KEY = 'sk-' + 'ABCD1234EFGH5678IJKL9012';
const PW = 'password = ' + '"changeme123456"';

function decision(payload, env) {
  let out = '';
  try {
    // EQ_SKIP_BRIEF: '1' by default so brief-gate (rule 8, force:true, fires on
    // any non-exempt file write with no session brief flag) doesn't piggyback
    // on cases exercising a different rule. None of the cases below test
    // brief-gate itself; pass { EQ_SKIP_BRIEF: '0' } to re-engage it if one is added.
    out = execFileSync('node', [GUARD], { input: JSON.stringify(payload), env: { ...process.env, EQ_SKIP_BRIEF: '1', ...env }, encoding: 'utf8' });
  } catch (e) { out = (e.stdout || '').toString(); }
  out = out.trim();
  if (!out) return 'allow';
  try { return JSON.parse(out).hookSpecificOutput.permissionDecision || 'allow'; }
  catch (_) { return 'malformed'; }
}

// For warn-only-always rules (blockable: false, e.g. warn-untracked-migrations):
// decision() can't tell "fired as a warning" from "never fired" -- both leave
// permissionDecision unset (empty stdout -> 'allow'). guard.js always exits 0
// (allow() and deny() both process.exit(0)), so execFileSync never throws and
// its return value is stdout-only -- stderr from a successful run is silently
// dropped, not "just not returned". spawnSync gives {stdout, stderr} regardless
// of exit code, which is what the WARN line (process.stderr.write) needs.
function warnedRule(payload, env, ruleName) {
  const res = spawnSync('node', [GUARD], { input: JSON.stringify(payload), env: { ...process.env, EQ_SKIP_BRIEF: '1', ...env }, encoding: 'utf8' });
  return (res.stderr || '').includes(ruleName);
}

const bash = c => ({ tool_name: 'Bash', tool_input: { command: c }, cwd: '/x' });
const write = (p, c) => ({ tool_name: 'Write', tool_input: { file_path: p, content: c }, cwd: '/c/app' });
const sql = q => ({ tool_name: 'mcp__svc__execute_sql', tool_input: { query: q }, cwd: '/x' });
// Rule 8 (brief-gate) cases need a session_id on the payload -- write() has
// none, and adding one there would be a no-op for every existing case
// (EQ_SKIP_BRIEF defaults to '1' in decision(), see below) but an
// unnecessary risk to every passing case for a field only this rule reads.
const writeSid = (p, c, sid) => ({ tool_name: 'Write', tool_input: { file_path: p, content: c }, cwd: '/c/app', session_id: sid });

const cases = [
  ['sks-live in Bash, warn mode → forced deny',        bash('psql ' + SKS_ID), {}, 'deny'],
  ['sks-live unlocked → unlock beats force',           bash('psql ' + SKS_ID), { EQ_ALLOW_SKS_LIVE: '1' }, 'allow'],
  ['sk- key write, warn mode → forced deny',           write('/c/app/x.js', KEY), {}, 'deny'],
  ['inline password write, warn → tunable (allow)',    write('/c/app/x.js', PW), {}, 'allow'],
  ['git push, warn → tunable (allow)',                 bash('git push'), {}, 'allow'],
  ['git push, block mode → deny',                      bash('git push'), { EQ_GUARD_MODE: 'block' }, 'deny'],
  ['DROP via MCP, block mode → deny',                  sql('DROP TABLE workers'), { EQ_GUARD_MODE: 'block' }, 'deny'],
  ['worktree write, block mode → deny',                { tool_name: 'Write', tool_input: { file_path: '/c/Projects/eq-shell-wt/a.ts', content: 'x' }, cwd: '/c/Projects/eq-context' }, { EQ_GUARD_MODE: 'block' }, 'deny'],
  // Same REAL worktree (both fixture dirs carry an actual .git, so 1b's
  // fake-worktree check can't confound the result), but file_path and cwd
  // reported in DIFFERENT path styles (one Git-Bash /c/..., one Windows C:/...)
  // -- both refer to the identical location, so this must allow. Regression
  // check for the mixed-style false-positive class fixed in 1b/1c on
  // 2026-08-05: rule 1's fp.startsWith(c) never accounted for Git-Bash's fake
  // drive-letter root either. Not observed live (guard.log shows file_path/cwd
  // are always Windows-style together in every real session logged) but
  // nothing in the code guaranteed that. (added 2026-08-05)
  ['worktree write, same dir mixed styles (gitbash path/win cwd), block → allow', { tool_name: 'Write', tool_input: { file_path: mineGitBash + '/a.ts', content: 'x' }, cwd: mineWin }, { EQ_GUARD_MODE: 'block' }, 'allow'],
  ['worktree write, same dir mixed styles (win path/gitbash cwd), block → allow', { tool_name: 'Write', tool_input: { file_path: mineWin + '/a.ts', content: 'x' }, cwd: mineGitBash }, { EQ_GUARD_MODE: 'block' }, 'allow'],
  // Cross worktree (file_path in the SIBLING real fixture, cwd in mine), mixed
  // styles -- must still deny. Both dirs have a real .git so this isolates rule
  // 1's own comparison rather than riding on 1b's unconditional force-block.
  ['worktree write, cross dir mixed styles (gitbash path/win cwd), block → deny', { tool_name: 'Write', tool_input: { file_path: otherGitBash + '/a.ts', content: 'x' }, cwd: mineWin }, { EQ_GUARD_MODE: 'block' }, 'deny'],
  ['git push via PowerShell, block → deny',            { tool_name: 'PowerShell', tool_input: { command: 'git push' }, cwd: '/x' }, { EQ_GUARD_MODE: 'block' }, 'deny'],
  ['benign ls, block mode → allow',                    bash('ls -la'), { EQ_GUARD_MODE: 'block' }, 'allow'],
  ['guard off → allow everything',                     bash('psql ' + SKS_ID), { EQ_GUARD_OFF: '1' }, 'allow'],
  // rule 1c (detect-fake-worktree, shell case) via resolveEffCwd() -- had NO
  // coverage before this pair; every worktree case above goes through the
  // Write-tool path (rules 1/1b) instead. warn mode (no EQ_GUARD_MODE
  // override) is deliberate: it isolates 1c (force:true, blocks regardless
  // of mode) from rule 4 gate-outbound, which also matches any `git commit`
  // and would otherwise block/allow on its own MODE-dependent logic and
  // confound the result either way.
  //
  // Regression for the relative-cd bug fixed 2026-08-20: resolveEffCwd()
  // used to return a `cd`/`-C` target as-is, so a RELATIVE target (as opposed
  // to an already-absolute one) got resolved by fs.existsSync() against the
  // guard PROCESS's own cwd instead of the tool call's -- false-positiving
  // this exact case (a real worktree, entered via a relative cd) as fake.
  // Confirmed this case fails ('deny' instead of 'allow') against the
  // pre-fix code.
  ['shell git-commit, relative cd into a REAL worktree, warn → allow (regression: resolveEffCwd must resolve a relative cd target against the reported cwd, not return it raw)',
    { tool_name: 'Bash', tool_input: { command: 'cd worktrees/myworktree && git commit -m "x"' }, cwd: fixtureRoot }, {}, 'allow'],
  // Same relative-cd resolution path, but into a fixture with no .git at
  // all -- confirms the fix above didn't loosen real detect-fake-worktree
  // (a genuinely fake worktree must still block).
  ['shell git-commit, relative cd into a GENUINELY fake worktree (no .git), warn → still deny',
    { tool_name: 'Bash', tool_input: { command: 'cd worktrees/fakeworktree && git commit -m "x"' }, cwd: fixtureRoot }, {}, 'deny'],
  // Regression for the worktree-add-then-cd bug fixed 2026-08-21: creating a
  // worktree with `git worktree add` and then `cd`-ing into it to keep
  // working is a normal, recommended pattern (this file's own stale-main-gate
  // rule 10 suggests exactly this) -- but resolveEffCwd() picks the LAST cd
  // in the whole string with no regard for whether it comes before or after
  // the worktree-add that creates the target, so it was checking a path's
  // .git existence before the add that creates it had even run. Confirmed
  // this case fails ('deny' instead of 'allow') against the pre-fix code.
  ['shell git worktree add + cd into the just-created worktree, warn → allow (regression: creating-this-worktree exemption)',
    { tool_name: 'Bash', tool_input: { command: 'git worktree add --detach worktrees/newworktree origin/main && cd worktrees/newworktree && git status' }, cwd: fixtureRoot }, {}, 'allow'],
  // Same shape, but the `git worktree add` targets a DIFFERENT worktree than
  // the one being cd'd into -- proves the exemption is scoped to the actual
  // target, not "any worktree add anywhere in the command", so an unrelated
  // genuinely-fake worktree still blocks.
  ['shell git worktree add (different target) + cd into an UNRELATED fake worktree, warn → still deny',
    { tool_name: 'Bash', tool_input: { command: 'git worktree add --detach worktrees/newworktree origin/main && cd worktrees/fakeworktree && git status' }, cwd: fixtureRoot }, {}, 'deny'],
  // Infix-named (<repo>-wt-<topic>) counterparts of the worktree-write /
  // fake-worktree cases above, added alongside widening rules 1/1b/1c to
  // recognize this shape (same finding as rule 10's fix above).
  // cwd is a synthetic unrelated path, NOT fixtureRoot -- realInfixDir is a
  // CHILD of fixtureRoot, so fp.startsWith(c) would be trivially true against
  // fixtureRoot regardless of inWt, never actually exercising rule 1's own
  // comparison (caught live: this case still failed after the guard.js fix,
  // for that reason, until the cwd here was corrected).
  ['worktree write, infix-named REAL worktree, foreign cwd, block mode → deny (regression: rule 1 inWt must recognize the infix -wt- shape, not just a trailing -wt suffix)',
    { tool_name: 'Write', tool_input: { file_path: path.join(realInfixDir, 'a.ts'), content: 'x' }, cwd: '/c/Projects/unrelated' }, { EQ_GUARD_MODE: 'block' }, 'deny'],
  ['worktree write, infix-named REAL worktree, editing from within it, block mode → allow (no false-positive: same worktree, not foreign)',
    { tool_name: 'Write', tool_input: { file_path: path.join(realInfixDir, 'a.ts'), content: 'x' }, cwd: realInfixDir }, { EQ_GUARD_MODE: 'block' }, 'allow'],
  ['detect-fake-worktree (isFile), infix-named FAKE worktree (no .git), warn → deny (regression: rule 1b per-segment -wt$ check must recognize the infix shape too)',
    { tool_name: 'Write', tool_input: { file_path: path.join(fakeInfixDir, 'a.ts'), content: 'x' }, cwd: fakeInfixDir }, {}, 'deny'],
  ['detect-fake-worktree (shell), infix-named FAKE worktree (no .git), warn → deny (regression: rule 1c per-segment -wt$ check must recognize the infix shape too)',
    { tool_name: 'Bash', tool_input: { command: 'git commit -m "x"' }, cwd: fakeInfixDir }, {}, 'deny'],
  // Rule 10 (stale-main-gate) naming fast-path -- both clones above are
  // genuinely 1 commit behind origin/main. The control proves the fixture
  // really blocks without a naming exemption; the infix case is the actual
  // regression check (see fixture comment above for why -- fails pre-fix).
  ['stale-main-gate: plain-named clone, 1 behind origin/main, warn → deny (fixture control)',
    { tool_name: 'Bash', tool_input: { command: 'git commit -m "x" --allow-empty' }, cwd: staleControlDir }, {}, 'deny'],
  ['stale-main-gate: <repo>-wt-<topic> infix-named clone, 1 behind origin/main, warn → allow (regression: fast-path must recognize the infix -wt- shape, not just a trailing -wt suffix or nested /worktrees/)',
    { tool_name: 'Bash', tool_input: { command: 'git commit -m "x" --allow-empty' }, cwd: staleInfixDir }, {}, 'allow'],
  // brief-gate (rule 8) -- force:true, so WARN mode (no EQ_GUARD_MODE
  // override) still denies when it fires; this also doubles as the
  // regression check that force:true isn't accidentally MODE-dependent.
  ['brief-gate: no flag for this session id, non-exempt write, warn mode → forced deny (never briefed)',
    writeSid('/c/app/brief-none.js', 'x', briefSidNone), { EQ_SKIP_BRIEF: '0' }, 'deny'],
  // The actual fix (2026-09-15): a same-session flag with NO date in its
  // name satisfies the gate. Nothing about this case depends on what today
  // actually is -- that's the point of removing the date entirely rather
  // than special-casing "yesterday or today" (the fixture flag was written
  // once, at suite-startup time, and stays valid regardless of when the
  // suite itself happens to run or how long it runs for).
  ['brief-gate: session flag present (current dateless format), non-exempt write, warn mode → allow (the 2026-09-15 fix)',
    writeSid('/c/app/brief-fresh.js', 'x', briefSidFresh), { EQ_SKIP_BRIEF: '0' }, 'allow'],
  // Regression: an OLD-format DATED flag exists, but for a DIFFERENT
  // session id than the one under test here (briefSidOtherSession, not
  // briefSidNone) -- must still deny. Proves the fix didn't loosen matching
  // to "any eq-brief-* file exists", only to "this exact session id's
  // dateless flag exists".
  ['brief-gate: old-format dated flag exists for a DIFFERENT session id, warn mode → still forced deny (no cross-session or old-format false-positive)',
    writeSid('/c/app/brief-cross.js', 'x', briefSidNone), { EQ_SKIP_BRIEF: '0' }, 'deny']
];

// warn-untracked-migrations (rule 11) -- fires on git commit, eq-field only,
// only when supabase/migrations has an untracked .sql. Never blocks (checked
// separately below via decision(), which must stay 'allow' in every case --
// this rule is blockable: false, so it must be a no-op for the permission
// decision regardless of what it logs).
const warnCases = [
  ['untracked migration in eq-field, git commit -> warn-untracked-migrations fires',
    { tool_name: 'Bash', tool_input: { command: 'git commit -m "x"' }, cwd: migEqFieldDir }, {}, true],
  ['same file already committed (tracked) in eq-field -> does not fire (untracked-specific, not presence-specific)',
    { tool_name: 'Bash', tool_input: { command: 'git commit -m "x"' }, cwd: migEqFieldCleanDir }, {}, false],
  ['same untracked file, but repo is eq-service not eq-field -> does not fire (eq-field-only scoping)',
    { tool_name: 'Bash', tool_input: { command: 'git commit -m "x"' }, cwd: migOtherRepoDir }, {}, false],
];

let pass = 0;
const total = cases.length + warnCases.length * 2;
try {
  for (const [name, payload, env, want] of cases) {
    const got = decision(payload, env);
    const ok = got === want;
    if (ok) pass++;
    console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}  (want ${want}, got ${got})`);
  }
  for (const [name, payload, env, want] of warnCases) {
    const got = warnedRule(payload, env, 'warn-untracked-migrations');
    const ok = got === want;
    if (ok) pass++;
    console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}  (want ${want}, got ${got})`);
    // blockable: false must hold regardless of mode -- confirm it never denies,
    // even under EQ_GUARD_MODE=block. EQ_ALLOW_DEPLOY unlocks gate-outbound,
    // which also matches any git commit and would otherwise confound this
    // check with ITS OWN block decision -- same isolation problem this file
    // already documents for the rule-1c relative-cd cases above.
    const permGot = decision(payload, { ...env, EQ_GUARD_MODE: 'block', EQ_ALLOW_DEPLOY: '1' });
    const permOk = permGot === 'allow';
    if (permOk) pass++;
    console.log(`${permOk ? 'PASS' : 'FAIL'}  ${name} (never blocks, even in block mode)  (want allow, got ${permGot})`);
  }
} finally {
  try { fs.rmSync(fixtureRoot, { recursive: true, force: true }); } catch (_) { /* best-effort */ }
  try { fs.rmSync(staleFixtureRoot, { recursive: true, force: true }); } catch (_) { /* best-effort */ }
  try { fs.rmSync(briefFlagFresh, { force: true }); } catch (_) { /* best-effort */ }
  try { fs.rmSync(briefFlagOldFormatOtherSession, { force: true }); } catch (_) { /* best-effort */ }
}
console.log(`\n${pass}/${total} passed`);
process.exit(pass === total ? 0 : 1);

// === DURABILITY BACKUP META ===
// This is a durability backup, not the live file — it is never loaded or
// executed from this path. Source of truth: ~/.claude/hooks/selftest.js
// (Royce's machine, user-level, not version-controlled). Last synced:
// 2026-09-15. Checked for drift every session by hooks/session_start.py's
// CMDSYNC step (system/failures.md -> F19), which truncates the file at
// the "DURABILITY BACKUP META" marker above before hashing, so keep that
// marker line byte-exact if you touch this comment. To restore: copy
// everything ABOVE this block back to ~/.claude/hooks/selftest.js unchanged.
// === END META ===
