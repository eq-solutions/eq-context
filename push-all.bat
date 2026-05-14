@echo off
REM Push order: eq-context first (priority), then the rest.
REM Per-URL credential helpers (eq-solutions + Milmlow) must be wired in git config.

setlocal EnableDelayedExpansion
set FAILED=

echo ============================================================
echo [1/3] eq-context (priority)
echo ============================================================
pushd C:\Projects\eq-context
git status -sb
git push origin HEAD
if errorlevel 1 set FAILED=!FAILED! eq-context
popd

echo.
echo ============================================================
echo [2/3] eq-cards
echo ============================================================
pushd C:\Projects\eq-cards
git status -sb
git push origin HEAD
if errorlevel 1 set FAILED=!FAILED! eq-cards
popd

echo.
echo ============================================================
echo [3/3] eq-solves-field
echo ============================================================
pushd C:\Projects\eq-solves-field
git status -sb
git push origin HEAD
if errorlevel 1 set FAILED=!FAILED! eq-solves-field
popd

echo.
echo ============================================================
if "!FAILED!"=="" (
  echo All pushes succeeded.
) else (
  echo FAILED:!FAILED!
  echo Re-run individually or paste the error back to me.
)
echo ============================================================
endlocal
pause
