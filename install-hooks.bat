@echo off
REM eq-context: point git at the in-repo hooks/ directory.
REM Run once per clone — no per-file copying, no symlinks.
REM After this, every commit on main auto-pushes to origin.

setlocal
cd /d "%~dp0"

git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
  echo Not inside a git repo. Run this from the eq-context clone root.
  pause
  exit /b 1
)

git config core.hooksPath hooks
if errorlevel 1 (
  echo Failed to set core.hooksPath.
  pause
  exit /b 1
)

echo.
echo Hooks path configured: core.hooksPath = hooks
echo.
echo Verify:
git config --get core.hooksPath
echo.
echo Next commit on main will auto-push to origin.
echo.
echo To disable later:  git config --unset core.hooksPath
echo To bypass once:    set SKIP_AUTOPUSH=1 ^&^& git commit -m "..."
echo.
endlocal
pause
