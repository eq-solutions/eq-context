<#
.SYNOPSIS
  Enable the eq-context pre-commit hook for this clone.

.DESCRIPTION
  Tells git to use .githooks/ as the hooks directory so the pre-commit
  hook in this repo is active locally. Run once after cloning the repo.
  Idempotent.

.EXAMPLE
  cd C:\Projects\eq-context
  .\scripts\install-hooks.ps1
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

if (-not (Test-Path .git)) {
    throw "Run this from inside the eq-context repo (no .git directory found here)."
}
if (-not (Test-Path .githooks/pre-commit)) {
    throw ".githooks/pre-commit not found. Pull latest main first."
}
if (-not (Test-Path .githooks/post-commit)) {
    throw ".githooks/post-commit not found. Pull latest main first."
}
if (-not (Test-Path scripts/pre-commit-secrets.sh)) {
    throw "scripts/pre-commit-secrets.sh not found. The pre-commit hook delegates to it and will refuse to run without it."
}

# A hook in .git/hooks/ is SHADOWED once core.hooksPath is set — git uses one
# directory, not both. On 2026-08-04 this clone had an untracked copy of the
# secret guard sitting there, which is why the governed .githooks hook had
# never run. The governed hook now delegates to scripts/pre-commit-secrets.sh
# itself, so the standalone copy is redundant; warn rather than delete it.
$legacyHook = Join-Path (git rev-parse --git-common-dir) 'hooks/pre-commit'
if (Test-Path $legacyHook) {
    Write-Host "NOTE: $legacyHook exists and will be SHADOWED by core.hooksPath." -ForegroundColor Yellow
    Write-Host "      Its secret-scanning is already run by .githooks/pre-commit, so nothing is lost." -ForegroundColor Yellow
    Write-Host "      Safe to delete it once you've confirmed a commit still blocks a planted secret." -ForegroundColor Yellow
    Write-Host ""
}

git config core.hooksPath .githooks
Write-Host ("Configured core.hooksPath = " + (git config core.hooksPath)) -ForegroundColor Green

# On Windows the executable bit isn't tracked the same way, but Git Bash will
# run the hook regardless via bash invocation. Force +x for WSL/macOS sanity.
if (Get-Command bash -ErrorAction SilentlyContinue) {
    bash -c "chmod +x .githooks/pre-commit .githooks/post-commit" 2>$null
}

Write-Host ""
Write-Host "Hooks enabled (pre-commit + post-commit). Pre-commit will block:"
Write-Host "  - committed secrets (GitHub PATs, Supabase JWTs, AWS/Stripe/Anthropic keys)"
Write-Host "  - frontmatter status: outside live|draft|archived|deprecated"
Write-Host "  - per-version CHANGELOG-vX.Y.Z.md files"
Write-Host "  - binary files (.zip, .docx, .pdf, images, etc.)"
Write-Host "  - _cleanup-patch-* folders"
Write-Host "  - non-canonical sessions/ filenames"
Write-Host "  - duplicate-content session files"
Write-Host ""
Write-Host "Bypass (only when truly needed): git commit --no-verify"
