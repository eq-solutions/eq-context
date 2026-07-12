#!/usr/bin/env python3
"""
Adversarial suite - regression tests for the brain. Cross-platform (no bash/WSL).

Plants every failure that has ever escaped the safeguards and asserts it is caught.
Seeded 2026-07-11 with F1-F6. EVERY future escape gets added here.
The system's own history becomes its test corpus. This is the part that compounds.

Run:  python hooks/adversarial_test.py
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = os.path.join(ROOT, "hooks", "pre_tool_use.py")
GATE = os.path.join(ROOT, "hooks", "session_start.py")
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
t("Write over 508-line lessons.md", {"tool_name": "Write", "tool_input": {"file_path": LESSONS}}, 2)

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

print()
print("  {} passed, {} failed".format(passed, failed))
sys.exit(1 if failed else 0)
