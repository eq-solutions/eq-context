#!/usr/bin/env python3
"""
Adversarial suite - regression tests for the brain. Cross-platform (no bash/WSL).

Plants every failure that has ever escaped the safeguards and asserts it is caught.
Seeded 2026-07-11 with F1-F6. EVERY future escape gets added here.
The system's own history becomes its test corpus. This is the part that compounds.

Run:  python hooks/adversarial_test.py
"""
import json, os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = os.path.join(ROOT, "hooks", "pre_tool_use.py")
GATE = os.path.join(ROOT, "hooks", "session_start.py")
END_GATE = os.path.join(ROOT, "hooks", "session_end.py")
AUTO_PR_GUARD = os.path.join(ROOT, "hooks", "auto_pr_guard.py")
CLAUDE_MD = os.path.join(ROOT, "CLAUDE.md")
LESSONS = os.path.join(ROOT, "system", "lessons.md")
SHORT = os.path.join(ROOT, "hooks", "README.md")
NEWF = os.path.join(ROOT, "system", "brand-new-file.md")

env = dict(os.environ, EQ_FORCE_GUARD="1")
passed = failed = 0


def run_hook(payload):
    p = subprocess.run([sys.executable, HOOK], input=json.dumps(payload),
                       capture_output=True, text=True, env=env)
    return p.returncode


def t(name, payload, expect):
    global passed, failed
    got = run_hook(payload)
    ok = got == expect
    print("  {:<52}{}".format(name, "PASS" if ok else "*** FAIL *** (got {}, want {})".format(got, expect)))
    passed += ok
    failed += (not ok)


def edit(path):
    return {"tool_name": "Edit", "tool_input": {"file_path": path}}


# Every existing bash() test predates F7's pre-git-verb NUL scan, which resolves
# a repo root from the payload's "cwd" (falling back to os.getcwd()) and scans
# ITS actual working tree. Pointing plain bash() calls at a real git repo would
# make those tests' outcomes depend on whatever happens to be modified in that
# repo's working tree at the moment the suite runs — exactly the kind of ambient-
# state coupling a regression test must not have. NOGIT_CWD is a bare, repo-less
# tempdir: repo_root_for() returns None there, so F7 cleanly no-ops and every
# pre-existing test keeps its original, fully deterministic behavior.
NOGIT_CWD = tempfile.mkdtemp(prefix="eq_nogit_")


def bash(cmd, cwd=NOGIT_CWD):
    return {"tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": cwd}


def powershell(cmd, cwd=NOGIT_CWD):
    return {"tool_name": "PowerShell", "tool_input": {"command": cmd}, "cwd": cwd}


print("=== F2 - silent truncation on the mount (must BLOCK) ===")
t("Edit 296-line CLAUDE.md", edit(CLAUDE_MD), 2)
t("Edit CLAUDE.md via windows path", edit(r"C:\Projects\eq-context\CLAUDE.md"), 2)
t("Edit unresolvable path (FAIL-CLOSED)", edit(r"C:\Projects\ghost\x.md"), 2)
t("Write over 200-line lessons.md", {"tool_name": "Write", "tool_input": {"file_path": LESSONS}}, 2)

print("=== F6 - append (>>) NUL-fills on the mount (must BLOCK) ===")
t("cat >> lessons.md", bash("cat >> system/lessons.md << EOF"), 2)
t("echo >> a mount path", bash("echo x >> C:/Projects/f.md"), 2)

print("=== git from the sandbox (must BLOCK) ===")
t("git commit", bash("git commit -m x"), 2)
t("git push", bash("cd /x && git push origin main"), 2)
t("git status", bash("git status"), 2)
t("git merge via PowerShell (widened tool matching)", powershell("git merge origin/main"), 2)
t("git stash pop via PowerShell (widened tool matching)", powershell("git stash pop"), 2)


def _clear_readonly_and_retry(func, path, exc_info):
    """shutil.rmtree onerror hook — git marks some .git/objects files read-only
    on Windows, and shutil.rmtree(ignore_errors=True) silently leaves those (and
    therefore the whole directory) behind rather than raising. That then makes
    the NEXT fixture's os.makedirs() hit FileExistsError against a half-deleted
    leftover. Clear the attribute and retry the specific failing op instead of
    swallowing it blind."""
    import stat
    os.chmod(path, stat.S_IWRITE)
    func(path)


def _rmtree_retry(path, attempts=5, delay=0.2):
    """Bounded local retry for the rare case even the onerror clear loses a race
    against a just-exited git subprocess still releasing its handle — not a
    wait-on-external-system poll, same tolerance every fixture here already needs."""
    import time
    for _ in range(attempts):
        if not os.path.exists(path):
            return
        shutil.rmtree(path, onerror=_clear_readonly_and_retry)
        if not os.path.exists(path):
            return
        time.sleep(delay)


def f7_fixture_repo(corrupt):
    """A throwaway repo NESTED under ROOT (not a random tempdir) — targets_mount()
    matches on a '/projects/' path segment, and ROOT already sits under that on
    both the local Windows checkout and the CI runner's relocated /mnt/Projects
    checkout (see adversarial-suite.yml's relocation step). A plain tempdir
    would silently skip the F7 check, the same "quiet pass for the wrong reason"
    trap this suite's own CI comment already warns about for the F2 fixtures."""
    d = os.path.join(ROOT, ".tmp_f7_fixture")
    _rmtree_retry(d)
    os.makedirs(d)
    run = lambda *a: subprocess.run(["git", *a], cwd=d, capture_output=True, text=True)
    run("init", "-q", "-b", "main")
    run("config", "user.email", "test@example.com")
    run("config", "user.name", "test")
    target = os.path.join(d, "clean.md")
    with open(target, "w") as fh:
        fh.write("hello\n")
    run("add", "-A")
    run("commit", "-q", "-m", "seed")
    if corrupt:
        with open(target, "wb") as fh:
            fh.write(b"hello\x00\x00\x00 world\n")   # F6/F7's shared signature
    else:
        with open(target, "a") as fh:
            fh.write("more text, no corruption\n")
    return d


def bash_at(cmd, cwd):
    return {"tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": cwd}


def te(name, payload, expect, extra_env):
    global passed, failed
    env2 = dict(os.environ)
    env2.update(extra_env)
    got = subprocess.run([sys.executable, HOOK], input=json.dumps(payload),
                          capture_output=True, text=True, env=env2).returncode
    ok = got == expect
    print("  {:<52}{}".format(name, "PASS" if ok else "*** FAIL *** (got {}, want {})".format(got, expect)))
    passed += ok
    failed += (not ok)


print("=== F7 - pre-existing NUL corruption caught ahead of a git verb, INDEPENDENT of sandbox status ===")
corrupt_repo = f7_fixture_repo(corrupt=True)
te("BLOCKS with sandbox guard explicitly OFF (proves F7 isn't sandbox-scoped)",
   bash_at("git commit -am x", corrupt_repo), 2, {"EQ_FORCE_GUARD": "0"})
te("BLOCKS with sandbox guard ON too (F7 fires ahead of the pre-existing blanket block either way)",
   bash_at("git commit -am x", corrupt_repo), 2, {"EQ_FORCE_GUARD": "1"})
_rmtree_retry(corrupt_repo)

clean_repo = f7_fixture_repo(corrupt=False)
te("clean modified tree + sandbox guard OFF -> NOT blocked (F7 finds nothing, F2/F6/git-blanket correctly dormant)",
   bash_at("git commit -am x", clean_repo), 0, {"EQ_FORCE_GUARD": "0"})
te("clean modified tree + sandbox guard ON -> still blocked, but by the PRE-EXISTING git-blanket rule, not F7",
   bash_at("git commit -am x", clean_repo), 2, {"EQ_FORCE_GUARD": "1"})
_rmtree_retry(clean_repo)


def f9_fixture_repo():
    """A throwaway repo for F9's shared-checkout tests — real git repo, one
    committed file, so `git commit -- <path>` / `git rebase --continue` etc.
    have real state to operate against without touching the live ROOT. F9 is
    identified by EXACT PATH (is_shared_eq_context), not by repo content, so
    "is this the shared checkout" is entirely controlled per-call via the
    EQ_CONTEXT env var — same mechanism the GATE tests below already use."""
    d = os.path.join(ROOT, ".tmp_f9_fixture")
    _rmtree_retry(d)
    os.makedirs(d)
    run = lambda *a: subprocess.run(["git", *a], cwd=d, capture_output=True, text=True)
    run("init", "-q", "-b", "main")
    run("config", "user.email", "test@example.com")
    run("config", "user.name", "test")
    with open(os.path.join(d, "seed.md"), "w") as fh:
        fh.write("hello\n")
    run("add", "-A")
    run("commit", "-q", "-m", "seed")
    return d


print("=== F9 - shared eq-context checkout: concurrent-session git races (must BLOCK) ===")
f9_repo = f9_fixture_repo()
# EQ_FORCE_GUARD pinned to "0" on both: F9 is deliberately NOT sandbox-gated (see
# module docstring), but the LATER, pre-existing "any git verb blocks in the
# sandbox" rule still runs unconditionally once in_sandbox() is true — so on a
# Linux CI runner (where in_sandbox() is TRUE by default, no forcing needed) an
# F9-allowed case like a pathspec-scoped commit would still get blocked by that
# unrelated rule, and this test would wrongly read as a regression. Pinning "0"
# tests F9's OWN verdict in isolation, on every platform, matching how the F7
# tests above already pin EQ_FORCE_GUARD per-case rather than trust the ambient
# platform. Caught live 2026-08-05 by simulating EQ_FORCE_GUARD=1 by hand.
SAME = {"EQ_CONTEXT": f9_repo, "EQ_FORCE_GUARD": "0"}                       # this fixture IS "the shared checkout"
OTHER = {"EQ_CONTEXT": f9_repo + "-not-the-shared-one", "EQ_FORCE_GUARD": "0"}  # a different one — F9 must stay dormant

te("bare `git commit` in the SHARED checkout -> BLOCK",
   bash_at("git commit -m x", f9_repo), 2, SAME)
te("`git commit -m x -- <path>` (pathspec-scoped) -> allowed",
   bash_at("git commit -m x -- seed.md", f9_repo), 0, SAME)
te("`git commit --amend` -> allowed (different, already-governed risk)",
   bash_at("git commit --amend -m x", f9_repo), 0, SAME)
te("commit message containing a literal ' -- ' does not false-negative",
   bash_at('git commit -m "fixes tests -- see PR"', f9_repo), 2, SAME)
te("`git rebase <ref>` in the SHARED checkout -> BLOCK",
   bash_at("git rebase origin/main", f9_repo), 2, SAME)
te("`git merge <ref>` in the SHARED checkout -> BLOCK",
   bash_at("git merge origin/main", f9_repo), 2, SAME)
te("`git pull` in the SHARED checkout -> BLOCK (fetch+merge/rebase, same risk)",
   bash_at("git pull", f9_repo), 2, SAME)
te("`git rebase --continue` (escaping an already-stuck state) -> allowed",
   bash_at("git rebase --continue", f9_repo), 0, SAME)
te("`git rebase --abort` -> allowed",
   bash_at("git rebase --abort", f9_repo), 0, SAME)
te("`git merge --abort` -> allowed",
   bash_at("git merge --abort", f9_repo), 0, SAME)
te("PowerShell bare commit in the SHARED checkout -> BLOCK (tool matching)",
   {"tool_name": "PowerShell", "tool_input": {"command": "git commit -m x"}, "cwd": f9_repo}, 2, SAME)

print("=== F9 controls - same operations OUTSIDE the shared checkout must NOT be blocked ===")
te("bare `git commit` in a private/fresh clone -> allowed (F9's own escape valve)",
   bash_at("git commit -m x", f9_repo), 0, OTHER)
te("`git rebase <ref>` in a private/fresh clone -> allowed",
   bash_at("git rebase origin/main", f9_repo), 0, OTHER)
te("`git status` / `git push` untouched by F9 even INSIDE the shared checkout",
   bash_at("git push origin main", f9_repo), 0, SAME)
_rmtree_retry(f9_repo)

print("=== CONTROLS - legitimate work must NOT be blocked ===")
t("Edit a short file", edit(SHORT), 0)
t("Write a NEW file (parent exists)", {"tool_name": "Write", "tool_input": {"file_path": NEWF}}, 0)
t("cat > full rewrite (sanctioned)", bash("cat > system/x.md << EOF"), 0)
t("cat .git/HEAD (read-only)", bash("cat .git/HEAD"), 0)
t(">> /tmp scratch is fine", bash("echo x >> /tmp/s.log"), 0)
t("file outside the mount", edit("/tmp/scratch.md"), 0)

print("=== F1 / F3 - SessionStart gate must SPEAK ===")
g = subprocess.run([sys.executable, GATE], capture_output=True, text=True,
                   env=dict(env, EQ_CONTEXT=ROOT))
out = g.stdout
for label, key in [("gate reports freshness", "FRESHNESS"),
                   ("gate reports goals status (F3)", "GOALS"),
                   ("gate reports ratchet state", "RATCHET")]:
    ok = key in out
    print("  {:<52}{}".format(label, "PASS" if ok else "*** FAIL ***"))
    passed += ok
    failed += (not ok)

print("=== SESSION END GATE — Stop hook must speak on dirty state, stay quiet clean, never block ===")


def fixture_repo(dirty):
    """A throwaway git repo so the Stop-hook test doesn't depend on live ROOT state.

    'Clean' means genuinely closed out per Section 10 — main branch, today's
    session log committed — not just "has no changes", so the quiet-path
    assertion actually exercises all three checks landing negative.
    """
    import datetime
    d = tempfile.mkdtemp(prefix="eq_end_gate_")
    run = lambda *a: subprocess.run(["git", *a], cwd=d, capture_output=True, text=True)
    run("init", "-q", "-b", "main")
    run("config", "user.email", "test@example.com")
    run("config", "user.name", "test")
    os.makedirs(os.path.join(d, "sessions"), exist_ok=True)
    today = datetime.date.today().isoformat()
    with open(os.path.join(d, "sessions", f"{today}.md"), "w") as fh:
        fh.write("seed session log\n")
    run("add", "-A")
    run("commit", "-q", "-m", "seed")
    if dirty:
        with open(os.path.join(d, "f.md"), "w") as fh:
            fh.write("uncommitted change\n")
    return d


def run_end_gate(root):
    p = subprocess.run([sys.executable, END_GATE], capture_output=True, text=True,
                       env=dict(os.environ, EQ_CONTEXT=root))
    return p.returncode, p.stdout


for label, dirty_flag, want_marker in [
    ("dirty fixture reports DIRTY", True, "DIRTY"),
    ("clean fixture stays quiet", False, None),
]:
    d = fixture_repo(dirty_flag)
    try:
        code, out = run_end_gate(d)
        ok = code == 0 and ((want_marker in out) if want_marker else out.strip() == "")
        print("  {:<52}{}".format(label, "PASS" if ok else "*** FAIL *** (exit {}, out: {!r})".format(code, out[:200])))
        passed += ok
        failed += (not ok)
    finally:
        shutil.rmtree(d, ignore_errors=True)

# Never blocks, even against the live repo (whatever state it's in right now).
code, _ = run_end_gate(ROOT)
ok = code == 0
print("  {:<52}{}".format("end gate never blocks Stop (exit 0)", "PASS" if ok else "*** FAIL *** (exit {})".format(code)))
passed += ok
failed += (not ok)

print("=== AUTO-PR GUARD — the leash from the 2026-07-20 self-improving-substrate call ===")


def run_guard(payload, auto_pr_mode=True, root=ROOT):
    # root always pinned explicitly (default: this repo's real ROOT), matching
    # the GATE test's existing convention below — the hook's own EQ_CONTEXT
    # fallback is a hardcoded Windows path and silently resolves to nothing on
    # Linux CI, which is exactly the bug an unpinned root would have hidden.
    env = dict(os.environ)
    if auto_pr_mode:
        env["EQ_AUTO_PR_MODE"] = "1"
    else:
        env.pop("EQ_AUTO_PR_MODE", None)
    env["EQ_CONTEXT"] = root
    p = subprocess.run([sys.executable, AUTO_PR_GUARD], input=json.dumps(payload),
                       capture_output=True, text=True, env=env)
    return p.returncode


def guard_edit(path):
    return {"tool_name": "Edit", "tool_input": {"file_path": path}}


def guard_bash(cmd):
    return {"tool_name": "Bash", "tool_input": {"command": cmd}}


def tg(name, payload, expect, **kw):
    global passed, failed
    got = run_guard(payload, **kw)
    ok = got == expect
    print("  {:<52}{}".format(name, "PASS" if ok else "*** FAIL *** (got {}, want {})".format(got, expect)))
    passed += ok
    failed += (not ok)


tg("dormant without EQ_AUTO_PR_MODE (even for main push)", guard_bash("git push origin main"), 0, auto_pr_mode=False)
tg("in-scope edit (.github/scripts/x.py) allowed", guard_edit(os.path.join(ROOT, ".github", "scripts", "x.py")), 0)
tg("in-scope edit (archive/x.md) allowed", guard_edit(os.path.join(ROOT, "archive", "x.md")), 0)
tg("out-of-scope edit (eq/pending.md) blocked", guard_edit(os.path.join(ROOT, "eq", "pending.md")), 2)
tg("unlisted path blocked (default-deny)", guard_edit(os.path.join(ROOT, "README.md")), 2)
tg("the leash file itself blocked, unconditionally", guard_edit(os.path.join(ROOT, "system", "auto-pr-scope.md")), 2)
tg("explicit DENY wins (CLAUDE.md)", guard_edit(CLAUDE_MD), 2)
tg("git push to main blocked", guard_bash("git push origin main"), 2)
tg("git push --force blocked", guard_bash("git push --force origin claude/foo"), 2)
tg("gh pr merge blocked", guard_bash("gh pr merge 42 --merge"), 2)
tg("git push to a feature branch allowed", guard_bash("git push origin claude/some-fix-branch"), 0)
tg("gh pr create allowed", guard_bash('gh pr create --title "x" --body "y"'), 0)

d = tempfile.mkdtemp(prefix="eq_no_scope_")
tg("missing scope file fails CLOSED (blocks, not allows)",
   guard_edit(os.path.join(d, ".github", "scripts", "x.py")), 2, root=d)
shutil.rmtree(d, ignore_errors=True)

# A move/delete's SOURCE never goes through Edit/Write — caught live while
# actually trying to dogfood an archive/** cleanup: `git mv <root file>
# archive/x.md` sailed through with exit 0 because only the destination
# looked in-scope; the source (a root-level file) was never checked at all.
tg("git mv: out-of-scope SOURCE blocked even though dest is archive/**",
   guard_bash("git mv deploy.sh archive/deploy.sh"), 2)
tg("rm: out-of-scope path blocked", guard_bash("rm deploy.sh"), 2)
tg("rm: in-scope path (archive/**) allowed", guard_bash("rm archive/old-thing.md"), 0)
tg("git mv: both sides in-scope allowed", guard_bash("git mv archive/a.md archive/b.md"), 0)
tg("chained command: benign && out-of-scope rm still blocked",
   guard_bash("echo hi && rm deploy.sh"), 2)
tg("git commit message containing the word 'rm' is not a real rm (control)",
   guard_bash('git commit -m "rm stale reference"'), 0)
tg("npm script name containing 'cp' is not a real cp (control)",
   guard_bash("npm run cp-assets"), 0)

# Scope widened same day (2026-07-20) after the dogfood attempt above showed
# the original ALLOW never covered a root .md's SOURCE deletion.
tg("git mv: root .md source now allowed (scope widened)",
   guard_bash("git mv WEEKEND-MERGE-RUNBOOK.md archive/WEEKEND-MERGE-RUNBOOK.md"), 0)
tg("root .sh (non-.md) still out of scope — *.md widening isn't a blanket root exemption",
   guard_bash("git mv deploy.sh archive/deploy.sh"), 2)
tg("root README.md still explicitly protected despite *.md widening",
   guard_edit(os.path.join(ROOT, "README.md")), 2)
tg("*.md does not reach into subdirectories (eq/pending.md still blocked)",
   guard_edit(os.path.join(ROOT, "eq", "pending.md")), 2)

print()
print("  {} passed, {} failed".format(passed, failed))
sys.exit(1 if failed else 0)
