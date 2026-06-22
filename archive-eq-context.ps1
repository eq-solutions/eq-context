# archive-eq-context.ps1
# Generated 2026-06-15 — eq-context deep clean
# Archives stale May 2026 session files, sprint boards, and backlog docs.
# Run from PowerShell AFTER cleanup-worktrees.ps1 (worktrees must be pruned first).
#   cd C:\Projects\eq-context
#   .\archive-eq-context.ps1
# Add -DryRun to preview without making changes.

[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$repoPath = 'C:\Projects\eq-context'
Push-Location $repoPath

function Git-Mv { param([string]$Src, [string]$Dest)
    $destDir = Split-Path $Dest -Parent
    if (-not (Test-Path $destDir)) {
        if (-not $DryRun) { New-Item -ItemType Directory -Force $destDir | Out-Null }
    }
    if (-not (Test-Path $Src)) { Write-Host "  (skip — not found) $Src" -ForegroundColor Gray; return }
    if ($DryRun) { Write-Host "  [dry-run] git mv $Src -> $Dest" -ForegroundColor Yellow; return }
    git mv $Src $Dest 2>&1
    Write-Host "  MOVED $Src -> $Dest" -ForegroundColor Green
}

function Git-Rm { param([string]$Path)
    if (-not (Test-Path $Path)) { Write-Host "  (skip — not found) $Path" -ForegroundColor Gray; return }
    if ($DryRun) { Write-Host "  [dry-run] git rm $Path" -ForegroundColor Yellow; return }
    git rm $Path 2>&1
    Write-Host "  REMOVED $Path" -ForegroundColor Green
}

# Check for index.lock
if (Test-Path '.git\index.lock') {
    Write-Warning ".git\index.lock exists — another git process is running (VS Code, hook, etc)."
    Write-Warning "Close VS Code / terminals in this repo and re-run."
    Pop-Location; exit 1
}

Write-Host ""
Write-Host "=== 1. Archive May 2026 session files -> archive/sessions-2026-05/ ===" -ForegroundColor Cyan
$maySessions = @(
    'sessions\2026-05-04.md', 'sessions\2026-05-07.md', 'sessions\2026-05-13.md',
    'sessions\2026-05-14.md', 'sessions\2026-05-19.md', 'sessions\2026-05-20.md',
    'sessions\2026-05-20-part-b.md', 'sessions\2026-05-20-part-c.md',
    'sessions\2026-05-20-part-d.md', 'sessions\2026-05-21.md',
    'sessions\2026-05-24.md', 'sessions\2026-05-29.md',
    'sessions\2026-05-30.md', 'sessions\2026-05-31.md'
)
foreach ($s in $maySessions) {
    Git-Mv $s "archive\sessions-2026-05\$(Split-Path $s -Leaf)"
}

Write-Host ""
Write-Host "=== 2. Archive root-level May backlog / sprint / runbook docs ===" -ForegroundColor Cyan
Git-Mv 'field-feature-backlog-2026-05-30.md'        'archive\sprints\field-feature-backlog-2026-05-30.md'
Git-Mv 'quality-polish-backlog-2026-05-30.md'       'archive\sprints\quality-polish-backlog-2026-05-30.md'
Git-Mv 'service-feature-backlog-2026-05-30.md'      'archive\sprints\service-feature-backlog-2026-05-30.md'
Git-Mv 'sprint-2026-05-31-design-system.md'         'archive\sprints\sprint-2026-05-31-design-system.md'
Git-Mv 'security-secret-rotation-runbook-2026-05-31.md' 'archive\security-secret-rotation-runbook-2026-05-31.md'

Write-Host ""
Write-Host "=== 3. Archive eq/sprints/ May files ===" -ForegroundColor Cyan
Git-Mv 'eq\sprints\2026-05-20-S1-canonical-lockin.md' 'archive\sprints\2026-05-20-S1-canonical-lockin.md'
Git-Mv 'eq\sprints\2026-05-20-S3-polish-and-audit.md' 'archive\sprints\2026-05-20-S3-polish-and-audit.md'

Write-Host ""
Write-Host "=== 4. Archive eq/canonical-readiness/ (May planning, superseded by Jun work) ===" -ForegroundColor Cyan
Git-Mv 'eq\canonical-readiness\audit-2026-05-21.md'  'archive\canonical-readiness-2026-05\audit-2026-05-21.md'
Git-Mv 'eq\canonical-readiness\audit-existing-tables.md' 'archive\canonical-readiness-2026-05\audit-existing-tables.md'
Git-Mv 'eq\canonical-readiness\plan.md'             'archive\canonical-readiness-2026-05\plan.md'
Git-Mv 'eq\canonical-readiness\spine.md'            'archive\canonical-readiness-2026-05\spine.md'

Write-Host ""
Write-Host "=== 5. Archive May-31 audit files at root ===" -ForegroundColor Cyan
Git-Mv 'eq-canonical-classification-2026-05-31.md'  'archive\audits-2026-05-31\eq-canonical-classification.md'
Git-Mv 'field-roles-findings-2026-05-31.md'         'archive\audits-2026-05-31\field-roles-findings.md'
Git-Mv 'roles-canonical-audit-2026-05-31.md'        'archive\audits-2026-05-31\roles-canonical-audit.md'
Git-Mv 'sks-anon-exposure-audit-2026-05-31.md'      'archive\audits-2026-05-31\sks-anon-exposure-audit.md'
Git-Mv 'design-system-consolidation-2026-05-31.md'  'archive\audits-2026-05-31\design-system-consolidation.md'

Write-Host ""
Write-Host "=== 6. Archive eq/punch-list-2026-06-02.md (all items done) ===" -ForegroundColor Cyan
Git-Mv 'eq\punch-list-2026-06-02.md' 'archive\punch-list-2026-06-02.md'

Write-Host ""
if ($DryRun) {
    Write-Host "Dry run complete. No changes made." -ForegroundColor Yellow
    Pop-Location; exit 0
}

Write-Host "=== Committing ===" -ForegroundColor Cyan
git add -A
git status --short
git commit -m "archive: May sessions, sprint boards, backlogs, canonical-readiness, May-31 audits (2026-06-15 deep clean)"
Write-Host ""
Write-Host "Done. Auto-push hook will push to origin/main shortly." -ForegroundColor Green

Pop-Location
