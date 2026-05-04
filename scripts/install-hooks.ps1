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

git config core.hooksPath .githooks
Write-Host ("Configured core.hooksPath = " + (git config core.hooksPath)) -ForegroundColor Green

# On Windows the executable bit isn't tracked the same way, but Git Bash will
# run the hook regardless via bash invocation. Force +x for WSL/macOS sanity.
if (Get-Command bash -ErrorAction SilentlyContinue) {
    bash -c "chmod +x .githooks/pre-commit" 2>$null
}

Write-Host ""
Write-Host "Pre-commit hook enabled. It will block:"
Write-Host "  - per-version CHANGELOG-vX.Y.Z.md files"
Write-Host "  - binary files (.zip, .docx, .pdf, images, etc.)"
Write-Host "  - _cleanup-patch-* folders"
Write-Host "  - non-canonical sessions/ filenames"
Write-Host "  - duplicate-content session files"
Write-Host ""
Write-Host "Bypass (only when truly needed): git commit --no-verify"
