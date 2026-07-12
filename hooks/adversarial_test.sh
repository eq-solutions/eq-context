#!/usr/bin/env bash
# Adversarial suite — regression tests for the brain.
#
# Plants each failure that has ever escaped the safeguards and asserts it is caught.
# Seeded 2026-07-11 with F1-F5. EVERY future escape gets added here.
# The system's own history becomes its test corpus. This is the part that compounds.
#
# Run before trusting ANY change to hooks/.
set -u
R="$(cd "$(dirname "$0")/.." && pwd)"
pass=0; fail=0

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
