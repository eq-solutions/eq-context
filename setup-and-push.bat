@echo off
REM Installs the uploaded .git-credentials into %USERPROFILE%, then runs push-all.bat.
REM Backs up any existing credentials file with a timestamp suffix.

setlocal EnableDelayedExpansion

set SRC=C:\Users\EQ\AppData\Roaming\Claude\local-agent-mode-sessions\805fe7c3-20d4-403b-ba8c-ee1a94a249dd\8cdbef1b-8ad2-4fce-9a03-596ab95a298d\local_2c23f6b5-0a5b-482d-80d1-2d50dca331d6\uploads\.git-credentials
set DEST=%USERPROFILE%\.git-credentials

if not exist "%SRC%" (
  echo SOURCE NOT FOUND: %SRC%
  echo Confirm the uploaded file path is still valid.
  pause
  exit /b 1
)

if exist "%DEST%" (
  for /f "tokens=2 delims==" %%I in ('"wmic os get localdatetime /value"') do set DT=%%I
  set STAMP=!DT:~0,8!-!DT:~8,6!
  echo Backing up existing credentials to %DEST%.bak-!STAMP!
  copy /Y "%DEST%" "%DEST%.bak-!STAMP!" >nul
)

echo Installing credentials to %DEST%
copy /Y "%SRC%" "%DEST%" >nul
if errorlevel 1 (
  echo COPY FAILED.
  pause
  exit /b 1
)

REM Lock perms down (best effort) — only current user readable.
icacls "%DEST%" /inheritance:r >nul 2>&1
icacls "%DEST%" /grant:r "%USERNAME%:F" >nul 2>&1

echo Credentials installed.
echo.

REM Verify git can see store helper. If not configured, set it.
git config --global --get credential.helper >nul 2>&1
if errorlevel 1 (
  echo No global credential.helper set — enabling 'store'.
  git config --global credential.helper store
)

echo.
echo Handing off to push-all.bat...
echo.
call "%~dp0push-all.bat"

endlocal
