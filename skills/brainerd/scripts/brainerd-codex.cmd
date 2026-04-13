@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "ROOT_DIR=%%~fI"
set "DIST_CLI=%ROOT_DIR%\dist\src\codex-cli.js"
set "SOURCE_CLI=%ROOT_DIR%\src\codex-cli.ts"

set "SHOW_HELP="
if /I "%~1"=="help" set "SHOW_HELP=1"
for %%A in (%*) do (
  if /I "%%~A"=="--help" set "SHOW_HELP=1"
  if /I "%%~A"=="-h" set "SHOW_HELP=1"
)

if defined SHOW_HELP (
  if exist "%DIST_CLI%" (
    call :run_help node "%DIST_CLI%" __brainerd_help__
    exit /b %ERRORLEVEL%
  )

  where npx >nul 2>nul
  if not errorlevel 1 if exist "%SOURCE_CLI%" (
    call :run_help npx --yes tsx "%SOURCE_CLI%" __brainerd_help__
    exit /b %ERRORLEVEL%
  )
)

if exist "%DIST_CLI%" (
  node "%DIST_CLI%" %*
  exit /b %ERRORLEVEL%
)

where npx >nul 2>nul
if %ERRORLEVEL% EQU 0 if exist "%SOURCE_CLI%" (
  npx --yes tsx "%SOURCE_CLI%" %*
  exit /b %ERRORLEVEL%
)

echo Brainerd runtime is missing. Rebuild the skill or reinstall the packaged copy. 1>&2
exit /b 1

:run_help
set "HELP_OUTPUT=%TEMP%\brainerd-help-%RANDOM%-%RANDOM%.txt"
%* > "%HELP_OUTPUT%" 2>&1
set "HELP_STATUS=%ERRORLEVEL%"
type "%HELP_OUTPUT%"
if "%HELP_STATUS%"=="0" (
  del "%HELP_OUTPUT%" >nul 2>nul
  exit /b 0
)
findstr /B /C:"Usage:" "%HELP_OUTPUT%" >nul 2>nul
if not errorlevel 1 (
  del "%HELP_OUTPUT%" >nul 2>nul
  exit /b 0
)
del "%HELP_OUTPUT%" >nul 2>nul
exit /b %HELP_STATUS%
