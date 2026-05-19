# cleanup-worktrees.ps1
# v3 (2026-05-19) — detect-and-clean, self-maintaining
#
# Policy:
#   - Scans `git worktree list --porcelain` in each known repo
#   - REMOVES a worktree iff ALL of:
#       (a) not the main worktree (which is the repo root itself)
#       (b) not the worktree this script is running from
#       (c) not locked (`git worktree lock` flag absent)
#       (d) working tree is clean — no uncommitted, no untracked
#       (e) branch is fully merged into main/demo (parent of worktree-root branch),
#           OR worktree HEAD is identical to the parent-branch HEAD
#   - SKIPS (with a printed reason) anything that doesn't meet all of the above.
#
# Branches are NEVER deleted — only worktree filesystems + .git/worktrees/<name> metadata.
# Any commits in skipped worktrees remain on their branches for later checkout.
#
# Run from anywhere on the Beelink (absolute paths).
#   .\cleanup-worktrees.ps1                    # full sweep across known repos
#   .\cleanup-worktrees.ps1 -DryRun            # print actions, change nothing
#   .\cleanup-worktrees.ps1 -Force             # ignore the merge-status check (still skips locked/dirty/current)

[CmdletBinding()]
param(
    [switch]$DryRun,
    [switch]$Force
)

$ErrorActionPreference = 'Continue'

$repos = @(
    @{ Path = 'C:\Projects\eq-context';        ParentBranch = 'main' }
    @{ Path = 'C:\Projects\eq-solves-field';   ParentBranch = 'demo' }
    @{ Path = 'C:\Projects\eq-solves-service'; ParentBranch = 'main' }
)

$scriptDir = (Get-Location).Path

function Test-WorktreeRemovable {
    param(
        [string]$WorktreePath,
        [string]$RepoPath,
        [string]$ParentBranch,
        [bool]$IsLocked,
        [bool]$ForceMerge
    )

    if ($WorktreePath -eq $RepoPath) { return @{ Remove = $false; Reason = 'main worktree' } }
    if ($scriptDir -like "$WorktreePath*") { return @{ Remove = $false; Reason = 'this script is running from inside' } }
    if ($IsLocked) { return @{ Remove = $false; Reason = 'locked' } }

    Push-Location $WorktreePath
    try {
        $dirty = (git status --porcelain 2>&1)
        if ($dirty) { return @{ Remove = $false; Reason = "dirty (`n        $($dirty -join "`n        ")`n      )" } }

        if (-not $ForceMerge) {
            $head = (git rev-parse HEAD 2>&1).Trim()
            $parentHead = (git rev-parse "origin/$ParentBranch" 2>&1).Trim()
            if ($LASTEXITCODE -ne 0) { $parentHead = (git rev-parse $ParentBranch 2>&1).Trim() }

            if ($head -eq $parentHead) { return @{ Remove = $true; Reason = 'on parent HEAD' } }

            $merged = git merge-base --is-ancestor HEAD $parentHead 2>&1
            if ($LASTEXITCODE -eq 0) { return @{ Remove = $true; Reason = "fully merged into $ParentBranch" } }
            return @{ Remove = $false; Reason = "has commits not in $ParentBranch (use -Force to override)" }
        }
        return @{ Remove = $true; Reason = '-Force given' }
    } finally {
        Pop-Location
    }
}

function Remove-WorktreeSafe {
    param([string]$WorktreePath, [string]$RepoPath, [string]$WorktreeName)

    if ($DryRun) { Write-Host "    [dry-run] would remove" -ForegroundColor Yellow; return }

    Get-ChildItem -Path $WorktreePath -Recurse -Force -ErrorAction SilentlyContinue |
        ForEach-Object { try { $_.Attributes = 'Normal' } catch {} }
    try { (Get-Item $WorktreePath -Force).Attributes = 'Normal' } catch {}

    try {
        Remove-Item -Recurse -Force $WorktreePath -ErrorAction Stop
        Write-Host "    -> filesystem removed" -ForegroundColor Green
    } catch {
        Write-Warning "    -> filesystem remove failed: $($_.Exception.Message.Split([Environment]::NewLine)[0])"
        Write-Host "    -> probably an open file handle (VS Code / Explorer / terminal). Skipping metadata cleanup." -ForegroundColor Yellow
        return
    }

    $metaPath = Join-Path $RepoPath ".git\worktrees\$WorktreeName"
    if (Test-Path $metaPath) {
        try {
            Remove-Item -Recurse -Force $metaPath -ErrorAction Stop
            Write-Host "    -> metadata removed" -ForegroundColor Green
        } catch {
            Push-Location $RepoPath; git worktree prune 2>&1 | Out-Null; Pop-Location
            Write-Host "    -> metadata pruned via 'git worktree prune'" -ForegroundColor Green
        }
    }
}

foreach ($r in $repos) {
    $repoPath = $r.Path
    $parent   = $r.ParentBranch
    Write-Host ""
    Write-Host "=== $repoPath (parent: $parent) ===" -ForegroundColor Cyan
    if (-not (Test-Path $repoPath)) { Write-Host "  (repo not present, skipping)" -ForegroundColor Gray; continue }

    Push-Location $repoPath
    $porcelain = git worktree list --porcelain 2>&1
    Pop-Location

    $worktrees = @()
    $current = @{}
    foreach ($line in $porcelain) {
        if ($line -match '^worktree (.+)$') {
            if ($current.Count -gt 0) { $worktrees += $current }
            $current = @{ Path = ($matches[1] -replace '/', '\') }
        } elseif ($line -match '^branch (.+)$') {
            $current.Branch = $matches[1]
        } elseif ($line -match '^locked') {
            $current.Locked = $true
        } elseif ($line -match '^HEAD (.+)$') {
            $current.HEAD = $matches[1]
        }
    }
    if ($current.Count -gt 0) { $worktrees += $current }

    foreach ($wt in $worktrees) {
        $name = Split-Path $wt.Path -Leaf
        Write-Host "  $name" -ForegroundColor White
        $verdict = Test-WorktreeRemovable -WorktreePath $wt.Path -RepoPath $repoPath -ParentBranch $parent -IsLocked ([bool]$wt.Locked) -ForceMerge $Force.IsPresent
        if ($verdict.Remove) {
            Write-Host "    decision: REMOVE ($($verdict.Reason))" -ForegroundColor Green
            Remove-WorktreeSafe -WorktreePath $wt.Path -RepoPath $repoPath -WorktreeName $name
        } else {
            Write-Host "    decision: skip ($($verdict.Reason))" -ForegroundColor Gray
        }
    }
}

Write-Host ""
if ($DryRun) { Write-Host "Dry run complete. No changes made." -ForegroundColor Yellow }
else { Write-Host "Cleanup complete." -ForegroundColor Green }
