# cleanup-worktrees.ps1
# Generated: 2026-05-18 (v2 — handles unregistered worktrees + permission-denied)
# Removes orphan Claude worktrees from eq-context, eq-solves-field, eq-solves-service
# Run from anywhere on the Beelink — paths are absolute.
# Safe: only removes worktree directories, does not touch branches or commits.

$ErrorActionPreference = "Continue"

function Remove-Worktree {
    param(
        [string]$RepoPath,
        [string]$WorktreeName
    )
    $worktreePath = Join-Path $RepoPath ".claude\worktrees\$WorktreeName"
    Write-Host "[$RepoPath] $WorktreeName" -ForegroundColor Cyan

    if (-not (Test-Path $worktreePath)) {
        Write-Host "  -> Already gone" -ForegroundColor Gray
        return
    }

    # Strip read-only / hidden / system flags on all files inside (fixes Permission denied)
    Get-ChildItem -Path $worktreePath -Recurse -Force -ErrorAction SilentlyContinue |
        ForEach-Object { $_.Attributes = 'Normal' }

    # Also clear the directory itself
    (Get-Item $worktreePath -Force).Attributes = 'Normal'

    try {
        Remove-Item -Recurse -Force $worktreePath -ErrorAction Stop
        Write-Host "  -> Deleted" -ForegroundColor Green
    } catch {
        Write-Warning "  -> Still failed: $_"
        Write-Host "     Try: takeown /f `"$worktreePath`" /r /d y && icacls `"$worktreePath`" /grant `"$env:USERNAME`:F` /t" -ForegroundColor Yellow
    }
}

# --- eq-context ---
$repo = "C:\Projects\eq-context"
Remove-Worktree $repo "practical-bhabha-e28313"

# --- eq-solves-field ---
$repo = "C:\Projects\eq-solves-field"
Remove-Worktree $repo "dreamy-bhabha-006b91"
Remove-Worktree $repo "epic-noether-984c57"
Remove-Worktree $repo "festive-roentgen-60761d"
Remove-Worktree $repo "loving-dubinsky-128a63"
Remove-Worktree $repo "upbeat-varahamihira-797063"
Remove-Worktree $repo "zen-golick-a9e7e1"

# --- eq-solves-service ---
$repo = "C:\Projects\eq-solves-service"
Remove-Worktree $repo "crazy-swanson-cb5a62"
Remove-Worktree $repo "relaxed-hopper-e45f17"
Remove-Worktree $repo "sharp-germain-af2e3f"
Remove-Worktree $repo "xenodochial-clarke-fe01e2"

Write-Host ""
Write-Host "Worktree cleanup complete." -ForegroundColor Green
Write-Host "Run 'git worktree list' in each repo to verify." -ForegroundColor Gray
