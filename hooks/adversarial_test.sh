#!/usr/bin/env bash
# Adversarial suite — regression tests for the brain.
#
# Plants each failure that has ever escaped the safeguards and asserts it is caught.
# Seeded 2026-07-11 with F1-F5, grew to cover F6-F9 since. NOT kept in lockstep with
# every case in adversarial_test.py (the CI-authoritative suite, hooks/README.md) —
# session_end.py and auto_pr_guard.py's fixtures don't translate cleanly to bash, so
# those stay Python-only. This file's job is bash-native coverage of pre_tool_use.py
# itself: every failure class it blocks, tested here too.
# The system's own history becomes its test corpus. This is the part that compounds.
#
# Run before trusting ANY change to hooks/. (Was accidentally deleted 2026-08-05 —
# swept into a concurrent Claude Code session's bare `git commit` in the shared
# checkout; pre_tool_use.py's F9 guard existed but wasn't reachably wired for
# that session (fixed 2026-08-05 — system/failures.md -> F9, recurrence 4).
# Restored same day.)
set -u
R="$(cd "$(dirname "$0")/.." && pwd)"
pass=0; fail=0

# F2/F6-main/git-sandbox-block are Linux-sandbox-scoped (in_sandbox() checks
# platform.system() != "Windows"). Without this, every run on native Windows
# silently no-ops those checks and reports them as failures below — not because
# anything regressed, but because the guard correctly doesn't apply there. That
# makes the file misleading for ANY change, not just this one: 9 "failures" on
# every single run trains you to stop reading them. Force sandbox mode so this
# suite actually exercises what it claims to, on every platform it runs on.
export EQ_FORCE_GUARD=1

t() {  # name | json | expected_exit
  printf "  %-56s" "$1"
  echo "$2" | python3 "$R/hooks/pre_tool_use.py" >/dev/null 2>&1
  e=$?
  if [ "$e" = "$3" ]; then echo "PASS"; pass=$((pass+1))
  else echo "*** FAIL *** (exit $e, expected $3)"; fail=$((fail+1)); fi
}

echo "=== F2 — silent truncation on the virtiofs mount (must BLOCK) ==="
t "Edit 308-line CLAUDE.md (linux path)"      "{\"tool_name\":\"Edit\",\"tool_input\":{\"file_path\":\"$R/CLAUDE.md\"}}" 2
t "Edit CLAUDE.md (windows path)"             '{"tool_name":"Edit","tool_input":{"file_path":"C:\\Projects\\eq-context\\CLAUDE.md"}}' 2
t "Edit unresolvable path (FAIL-CLOSED)"      '{"tool_name":"Edit","tool_input":{"file_path":"C:\\Projects\\ghost\\x.md"}}' 2
t "Write over a long file"                    "{\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"$R/system/lessons.md\"}}" 2

echo "=== git from the sandbox (must BLOCK) ==="
t "git commit"                                '{"tool_name":"Bash","tool_input":{"command":"git commit -m x"}}' 2
t "git push"                                  '{"tool_name":"Bash","tool_input":{"command":"cd /x && git push origin main"}}' 2
t "git status"                                '{"tool_name":"Bash","tool_input":{"command":"git status"}}' 2

echo "=== F6 — append (>>) NUL-fills on the mount (must BLOCK) ==="
t "cat >> lessons.md"                         '{"tool_name":"Bash","tool_input":{"command":"cat >> system/lessons.md << EOF"}}' 2
t "echo >> a mount path"                      '{"tool_name":"Bash","tool_input":{"command":"echo x >> C:/Projects/f.md"}}' 2
t "CONTROL: >> /tmp (scratch is fine)"        '{"tool_name":"Bash","tool_input":{"command":"echo x >> /tmp/s.log"}}' 0
t "CONTROL: >> a shell var (CI output)"                '{"tool_name":"Bash","tool_input":{"command":"echo due= >> $GITHUB_OUTPUT"}}' 0

echo "=== F7 — pre-existing NUL corruption caught ahead of a git verb, INDEPENDENT of sandbox status ==="
F7DIR="$R/.tmp_f7_fixture_sh"
rm -rf "$F7DIR"
mkdir -p "$F7DIR"
git -C "$F7DIR" init -q -b main
git -C "$F7DIR" config user.email test@example.com
git -C "$F7DIR" config user.name test
printf 'hello\n' > "$F7DIR/clean.md"
git -C "$F7DIR" add -A
git -C "$F7DIR" commit -q -m seed

tf7() {  # name | force_guard_env | expected_exit  (fixture already has a NUL-corrupted uncommitted file)
  printf "  %-56s" "$1"
  (cd "$F7DIR" && echo '{"tool_name":"Bash","tool_input":{"command":"git commit -am x"}}' | EQ_FORCE_GUARD="$2" python3 "$R/hooks/pre_tool_use.py" >/dev/null 2>&1)
  e=$?
  if [ "$e" = "$3" ]; then echo "PASS"; pass=$((pass+1))
  else echo "*** FAIL *** (exit $e, expected $3)"; fail=$((fail+1)); fi
}
printf 'hello\x00\x00\x00 world\n' > "$F7DIR/clean.md"
tf7 "BLOCKS with sandbox guard explicitly OFF (not sandbox-scoped)" 0 2
tf7 "BLOCKS with sandbox guard ON too"                               1 2
printf 'hello\nmore text, no corruption\n' > "$F7DIR/clean.md"
tf7 "CONTROL: clean modified tree + guard OFF -> not blocked"        0 0
rm -rf "$F7DIR"

echo "=== F9 — shared eq-context checkout: concurrent-session git races (must BLOCK) ==="
# Only bash+git-command coverage here — two cases stay Python-only rather than
# fighting bash-in-bash-in-JSON quoting to duplicate: the message-containing-a-
# literal-'--' false-negative check, and the cwd-tracking regression added
# 2026-08-05 (commit 2104668 — a session's NOMINAL cwd differs from where its
# command actually `cd`ed). adversarial_test.py already covers both robustly.
F9DIR="$R/.tmp_f9_fixture_sh"
rm -rf "$F9DIR"
mkdir -p "$F9DIR"
git -C "$F9DIR" init -q -b main
git -C "$F9DIR" config user.email test@example.com
git -C "$F9DIR" config user.name test
printf 'hello\n' > "$F9DIR/seed.md"
git -C "$F9DIR" add -A
git -C "$F9DIR" commit -q -m seed

# EQ_FORCE_GUARD pinned to 0 here, overriding the global export=1 above: F9 isn't
# sandbox-gated, but the LATER, pre-existing "any git verb blocks in the sandbox"
# rule fires unconditionally once in_sandbox() is true — so with the global force
# left on, an F9-allowed case (e.g. a pathspec-scoped commit) would still get
# blocked by that unrelated rule and misread as a regression. Caught live 2026-08-05.
tf9() {  # name | git-command | expected_exit  (fixture IS "the shared checkout")
  printf "  %-56s" "$1"
  (cd "$F9DIR" && echo "{\"tool_name\":\"Bash\",\"tool_input\":{\"command\":\"$2\"}}" | EQ_CONTEXT="$F9DIR" EQ_FORCE_GUARD=0 python3 "$R/hooks/pre_tool_use.py" >/dev/null 2>&1)
  e=$?
  if [ "$e" = "$3" ]; then echo "PASS"; pass=$((pass+1))
  else echo "*** FAIL *** (exit $e, expected $3)"; fail=$((fail+1)); fi
}
tf9 "bare git commit in the SHARED checkout -> BLOCK"  "git commit -m x" 2
tf9 "pathspec-scoped commit -- <path> -> allowed"       "git commit -m x -- seed.md" 0
tf9 "--amend -> allowed"                                "git commit --amend -m x" 0
tf9 "git rebase <ref> -> BLOCK"                         "git rebase origin/main" 2
tf9 "git merge <ref> -> BLOCK"                          "git merge origin/main" 2
tf9 "git pull -> BLOCK"                                 "git pull" 2
tf9 "git rebase --continue -> allowed (escape a stuck state)" "git rebase --continue" 0
tf9 "git rebase --abort -> allowed"                     "git rebase --abort" 0
tf9 "git merge-base (read-only plumbing, not a merge) -> NOT blocked" "git merge-base main origin/main" 0
tf9 "git commit-graph write (not a commit) -> NOT blocked"            "git commit-graph write" 0

# Real in-progress merge fixture (own dir, not F9DIR) -- proves F9(a)'s merge
# exemption against genuine .git/MERGE_HEAD state, not a hand-rolled file.
MDIR="$R/.tmp_f9_merge_fixture_sh"
rm -rf "$MDIR"
mkdir -p "$MDIR"
git -C "$MDIR" init -q -b main
git -C "$MDIR" config user.email test@example.com
git -C "$MDIR" config user.name test
printf 'base\n' > "$MDIR/shared.md"
git -C "$MDIR" add -A
git -C "$MDIR" commit -q -m base
git -C "$MDIR" checkout -q -b side
printf 'side change\n' > "$MDIR/shared.md"
git -C "$MDIR" commit -q -am "side change"
git -C "$MDIR" checkout -q main
printf 'main change\n' > "$MDIR/shared.md"
git -C "$MDIR" commit -q -am "main change"
git -C "$MDIR" merge side -q >/dev/null 2>&1   # real conflict -> leaves MERGE_HEAD
printf 'resolved\n' > "$MDIR/shared.md"
git -C "$MDIR" add -A

printf "  %-56s" "bare commit COMPLETING an in-progress merge -> allowed"
(cd "$MDIR" && echo '{"tool_name":"Bash","tool_input":{"command":"git commit --no-edit"}}' | EQ_CONTEXT="$MDIR" EQ_FORCE_GUARD=0 python3 "$R/hooks/pre_tool_use.py" >/dev/null 2>&1)
e=$?
if [ "$e" = "0" ]; then echo "PASS"; pass=$((pass+1)); else echo "*** FAIL *** (exit $e, expected 0)"; fail=$((fail+1)); fi

rm -f "$MDIR/.git/MERGE_HEAD"
printf "  %-56s" "CONTROL: same staged state w/o MERGE_HEAD -> still BLOCKED"
(cd "$MDIR" && echo '{"tool_name":"Bash","tool_input":{"command":"git commit --no-edit"}}' | EQ_CONTEXT="$MDIR" EQ_FORCE_GUARD=0 python3 "$R/hooks/pre_tool_use.py" >/dev/null 2>&1)
e=$?
if [ "$e" = "2" ]; then echo "PASS"; pass=$((pass+1)); else echo "*** FAIL *** (exit $e, expected 2)"; fail=$((fail+1)); fi
rm -rf "$MDIR"

echo "=== F9 controls — same ops OUTSIDE the shared checkout must NOT be blocked ==="
tf9o() {  # name | git-command | expected_exit  (fixture is NOT "the shared checkout")
  printf "  %-56s" "$1"
  (cd "$F9DIR" && echo "{\"tool_name\":\"Bash\",\"tool_input\":{\"command\":\"$2\"}}" | EQ_CONTEXT="${F9DIR}-not-the-shared-one" EQ_FORCE_GUARD=0 python3 "$R/hooks/pre_tool_use.py" >/dev/null 2>&1)
  e=$?
  if [ "$e" = "$3" ]; then echo "PASS"; pass=$((pass+1))
  else echo "*** FAIL *** (exit $e, expected $3)"; fail=$((fail+1)); fi
}
tf9o "bare commit in a private clone -> allowed (F9's own escape valve)" "git commit -m x" 0
tf9o "rebase in a private clone -> allowed"                              "git rebase origin/main" 0
rm -rf "$F9DIR"

echo "=== CONTROLS — legitimate work must NOT be blocked ==="
t "Edit a short file"                         "{\"tool_name\":\"Edit\",\"tool_input\":{\"file_path\":\"$R/hooks/README.md\"}}" 0
t "Write a NEW file (parent exists)"          "{\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"$R/system/new.md\"}}" 0
t "heredoc write (the sanctioned path)"       '{"tool_name":"Bash","tool_input":{"command":"cat > x.md << EOF"}}' 0
t "cat .git/HEAD (read-only inspection)"      '{"tool_name":"Bash","tool_input":{"command":"cat .git/HEAD"}}' 0
t "file outside the mount"                    '{"tool_name":"Edit","tool_input":{"file_path":"/tmp/scratch.md"}}' 0

echo "=== F1 / F3 — SessionStart gate must SPEAK ==="
out="$(EQ_CONTEXT="$R" python3 "$R/hooks/session_start.py" 2>/dev/null)"
printf "  %-56s" "gate reports freshness"
echo "$out" | grep -q "FRESHNESS" && { echo "PASS"; pass=$((pass+1)); } || { echo "*** FAIL ***"; fail=$((fail+1)); }
printf "  %-56s" "gate reports goals status (F3)"
echo "$out" | grep -q "GOALS" && { echo "PASS"; pass=$((pass+1)); } || { echo "*** FAIL ***"; fail=$((fail+1)); }
printf "  %-56s" "gate reports ratchet state"
echo "$out" | grep -q "RATCHET" && { echo "PASS"; pass=$((pass+1)); } || { echo "*** FAIL ***"; fail=$((fail+1)); }

echo
echo "  $pass passed, $fail failed"
[ "$fail" -eq 0 ] || exit 1
