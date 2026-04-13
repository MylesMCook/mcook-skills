@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "ROOT_DIR=%%~fI"
set "DIST_CLI=%ROOT_DIR%\dist\src\claude-cli.js"
set "SOURCE_CLI=%ROOT_DIR%\src\claude-cli.ts"

set "SHOW_HELP="
if /I "%~1"=="help" set "SHOW_HELP=1"
for %%A in (%*) do (
  if /I "%%~A"=="--help" set "SHOW_HELP=1"
  if /I "%%~A"=="-h" set "SHOW_HELP=1"
)

if defined SHOW_HELP (
  if exist "%DIST_CLI%" (
    node "%DIST_CLI%" __brainerd_help__ 2>&1
    exit /b 0
  )

  where npx >nul 2>nul
  if not errorlevel 1 if exist "%SOURCE_CLI%" (
    npx --yes tsx "%SOURCE_CLI%" __brainerd_help__ 2>&1
    exit /b 0
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
