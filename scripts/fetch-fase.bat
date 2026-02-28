@echo off
setlocal

REM ============================================================================
REM Fetch fase (prompts + tasks)
REM
REM Gebruik:
REM   fetch-fase.bat fnd.02
REM
REM Dit script verwacht exact 1 parameter: value_stream_fase.
REM Het haalt in de CURRENT working directory op:
REM   - prompts via scripts/fetch_prompts.py
REM   - tasks via scripts/fetch_tasks.py
REM ============================================================================

if "%~1"=="" (
    echo [ERROR] Ontbrekende parameter value_stream_fase.
    echo Gebruik: fetch-fase.bat fnd.02
    exit /b 1
)

set "VALUE_STREAM_FASE=%~1"
set "SCRIPT_DIR=%~dp0"
set "SOURCE_ROOT=%SCRIPT_DIR%.."
set "TARGET_ROOT=%CD%"

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is niet beschikbaar in PATH.
    exit /b 1
)

echo.
echo ============================================================================
echo Fetch fase: %VALUE_STREAM_FASE%
echo Source: %SOURCE_ROOT%
echo Target: %TARGET_ROOT%
echo ============================================================================
echo.

python "%SCRIPT_DIR%fetch_prompts.py" %VALUE_STREAM_FASE% --source "%SOURCE_ROOT%" --target "%TARGET_ROOT%"
if errorlevel 1 (
    echo [ERROR] fetch_prompts.py mislukt.
    exit /b 1
)

python "%SCRIPT_DIR%fetch_tasks.py" %VALUE_STREAM_FASE% --source "%SOURCE_ROOT%" --target "%TARGET_ROOT%"
if errorlevel 1 (
    echo [ERROR] fetch_tasks.py mislukt.
    exit /b 1
)

echo.
echo [OK] Fase %VALUE_STREAM_FASE% succesvol opgehaald.
echo.

endlocal
exit /b 0
