# cleanup-worktrees.ps1
# v4 (2026-05-20) — orphan-aware, covers eq-intake + eq-shell
#
# Two classes of leftover handled:
#
# 1. GIT-KNOWN worktrees (`git worktree list --porcelain`). REMOVE iff ALL of:
#      (a) not the main worktree (the repo root itself)
#      (b) not the worktree this script is running from
#      (c) not locked
#      (d) working tree is clean (no uncommitted, no untracked)
#      (e) branch is fully merged into parent (main/demo), OR worktree HEAD
#          equals parent HEAD
#    Branches are NEVER deleted — only worktree filesystem + .git/worktrees/<name>
#    metadata. Skipped commits remain on their branches.
#
# 2. ORPHAN dirs — `.claude/worktrees/<name>` directories with NO entry in
#    `git worktree list`. Typically left behind by Cowork sessions that ended
#    abnormally. REMOVE iff age > $OrphanAgeDaysDefault OR -Force given.
#    Recent orphans (< threshold) are reported but kept, in case they hold
#    unfinished work.
#
# Run from anywhere on the Beelink (absolute paths).
#   .\cleanup-worktrees.ps1                    # full sweep, 7-day orphan threshold
#   .\cleanup-worktrees.ps1 -DryRun            # print actions, change nothing
#   .\cleanup-worktrees.ps1 -Force             # ignore merge-status check AND
#                                              # remove orphans regardless of age
#   .\cleanup-worktrees.ps1 -OrphanAgeDays 14  # change orphan age threshold

[CmdletBinding()]
param(
    [switch]$DryRun,
    [switch]$Force,
    [int]$OrphanAgeDays = 7
)

$ErrorActionPreference = 'Continue'

$repos = @(
    @{ Path = 'C:\Projects\eq-context';        ParentBranch = 'main' }
    @{ Path = 'C:\Projects\eq-cards';          ParentBranch = 'main' }
    @{ Path = 'C:\Projects\eq-intake';         ParentBranch = 'main' }
    @{ Path = 'C:\Projects\eq-shell';          ParentBranch = 'main' }
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

    # Orphan scan: filesystem dirs under .claude/worktrees/ that git no longer tracks
    $wtBase = Join-Path $repoPath '.claude\worktrees'
    if (Test-Path $wtBase) {
        $knownNames = @($worktrees | ForEach-Object { Split-Path $_.Path -Leaf })
        $orphans = Get-ChildItem $wtBase -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -notin $knownNames }
        foreach ($orph in $orphans) {
            $ageDays = [int]((Get-Date) - $orph.LastWriteTime).TotalDays
            Write-Host "  $($orph.Name) [ORPHAN, ${ageDays}d old]" -ForegroundColor Yellow
            $shouldRemove = $Force.IsPresent -or ($ageDays -gt $OrphanAgeDays)
            if ($shouldRemove) {
                Write-Host "    decision: REMOVE orphan (age ${ageDays}d > ${OrphanAgeDays}d threshold)" -ForegroundColor Green
                if ($DryRun) {
                    Write-Host "    [dry-run] would remove orphan" -ForegroundColor Yellow
                } else {
                    Get-ChildItem -Path $orph.FullName -Recurse -Force -ErrorAction SilentlyContinue |
                        ForEach-Object { try { $_.Attributes = 'Normal' } catch {} }
                    try { (Get-Item $orph.FullName -Force).Attributes = 'Normal' } catch {}
                    try {
                        Remove-Item -Recurse -Force $orph.FullName -ErrorAction Stop
                        Write-Host "    -> orphan removed" -ForegroundColor Green
                    } catch {
                        Write-Warning "    -> orphan remove failed: $($_.Exception.Message.Split([Environment]::NewLine)[0])"
                    }
                }
            } else {
                Write-Host "    decision: skip (age ${ageDays}d <= ${OrphanAgeDays}d threshold, -Force overrides)" -ForegroundColor Gray
            }
        }
    }
}

Write-Host ""
if ($DryRun) { Write-Host "Dry run complete. No changes made." -ForegroundColor Yellow }
else { Write-Host "Cleanup complete." -ForegroundColor Green }
