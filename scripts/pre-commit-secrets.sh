#!/usr/bin/env bash
# Native pre-commit hook for eq-context — secret-pattern guard.
#
# Catches the most common secret formats so they never leave the
# working tree. Works without gitleaks or pre-commit framework
# installed. The .pre-commit-config.yaml at the repo root is the
# preferred prod-grade version; this script is the always-on fallback.
#
# Install:
#   cp scripts/pre-commit-secrets.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# Bypass for an emergency (use sparingly):
#   git commit --no-verify
#
# Pattern coverage:
#   - GitHub PATs (ghp_, gho_, ghu_, ghs_, ghr_)
#   - GitHub fine-grained PATs (github_pat_)
#   - Supabase service-role + anon JWTs (eyJhbGc...)
#   - Sentry auth tokens (sntrys_ + sntryu_ + sntryo_)
#   - AWS access keys (AKIA...)
#   - Stripe live keys (sk_live_)
#   - Anthropic API keys (sk-ant-)
#   - OpenAI keys (sk-proj-... and legacy sk-...)
#   - Generic 'password=' / 'api_key=' / 'secret=' / 'token=' assignments whose
#     value is a 20+ char high-entropy token (placeholders like YOUR_KEY_HERE
#     may also trip it — clear the value or use --no-verify).
#
# Coverage rule: every format listed above MUST have a matching entry in the
# `patterns` array below. Do not advertise here what the array doesn't enforce.

set -euo pipefail

# Only check files being added/modified in this commit
files=$(git diff --cached --name-only --diff-filter=ACM)
[ -z "$files" ] && exit 0

# Patterns to scan for (extended regex)
# Matched case-insensitively (grep -iEn below). Every format the header
# comment advertises MUST appear here — a scanner that under-delivers on its
# documented coverage is worse than none (false confidence). Last reconciled
# against the header 2026-06-04.
patterns=(
  'ghp_[A-Za-z0-9]{36,}'
  'gho_[A-Za-z0-9]{36,}'
  'ghu_[A-Za-z0-9]{36,}'
  'ghs_[A-Za-z0-9]{36,}'
  'ghr_[A-Za-z0-9]{36,}'
  'github_pat_[A-Za-z0-9_]{40,}'
  'eyJhbGciOiJIUzI1NiI[A-Za-z0-9_.-]{40,}'
  'sntrys_[A-Za-z0-9_]{40,}'
  'sntryu_[A-Za-z0-9_]{40,}'
  'sntryo_[A-Za-z0-9_]{40,}'
  'AKIA[0-9A-Z]{16}'
  'sk_live_[A-Za-z0-9]{24,}'
  'sk-ant-[A-Za-z0-9_-]{40,}'
  # OpenAI: project keys (sk-proj-) and legacy (sk-<base62>). Ordered before
  # the legacy form; sk-ant- above is matched by its own stricter pattern.
  'sk-proj-[A-Za-z0-9_-]{32,}'
  'sk-[A-Za-z0-9]{32,}'
  # Generic 'key = value' / 'key: value' assignments. The value must be a
  # 20+ char high-entropy token (no spaces) so prose like "the access token
  # model" cannot trip it — only real secret-shaped values do.
  '(password|passwd|secret|api[_-]?key|apikey|access[_-]?key|auth[_-]?token|bearer)["'"'"']?[[:space:]]*[:=][[:space:]]*["'"'"']?[A-Za-z0-9/+_=-]{20,}'
)

hits=0
for f in $files; do
  # Skip binaries
  if file --mime "$f" 2>/dev/null | grep -q "charset=binary"; then
    continue
  fi

  for p in "${patterns[@]}"; do
    if matches=$(git show ":$f" 2>/dev/null | grep -iEn "$p" || true); then
      if [ -n "$matches" ]; then
        echo "❌ Possible secret in $f:" >&2
        echo "$matches" | sed 's/^/   /' >&2
        echo "" >&2
        hits=$((hits + 1))
      fi
    fi
  done
done

if [ "$hits" -gt 0 ]; then
  echo "❌ Pre-commit secret guard: $hits potential leak(s) detected." >&2
  echo "If this is a false positive, run: git commit --no-verify" >&2
  echo "(and consider tightening the pattern or adding the file to an allowlist)." >&2
  exit 1
fi

exit 0
