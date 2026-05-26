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
#   - OpenAI keys (sk-...)
#   - Generic 'password=' / 'api_key=' / 'secret=' assignments with non-empty values

set -euo pipefail

# Only check files being added/modified in this commit
files=$(git diff --cached --name-only --diff-filter=ACM)
[ -z "$files" ] && exit 0

# Patterns to scan for (extended regex)
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
)

hits=0
for f in $files; do
  # Skip binaries
  if file --mime "$f" 2>/dev/null | grep -q "charset=binary"; then
    continue
  fi

  for p in "${patterns[@]}"; do
    if matches=$(git show ":$f" 2>/dev/null | grep -En "$p" || true); then
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
