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


def bash(cmd):
    return {"tool_name": "Bash", "tool_input": {"command": cmd}}


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

print()
print("  {} passed, {} failed".format(passed, failed))
sys.exit(1 if failed else 0)
