@echo off
REM ==============================================================================
REM Fetch Agents - Windows Wrapper
REM ==============================================================================
REM
REM Wrapper voor fetch_mandarin_agents.py die agents ophaalt uit mandarin-agents
REM repository op basis van value-stream.fase patroon.
REM
REM Gebruik:
REM   fetch-agents.bat <value-stream.fase>  - Fetch agents voor value stream fase
REM
REM Voorbeelden:
REM   fetch-agents.bat miv.01   - Fetch MIV fase 01 agents
REM   fetch-agents.bat aeo.02   - Fetch AEO fase 02 agents
REM   fetch-agents.bat fnd.01   - Fetch FND fase 01 agents
REM   fetch-agents.bat sfw.01   - Fetch SFW fase 01 agents
REM
REM Output:
REM   - Console: Directe feedback over fetch proces
REM   - Terminal log: logs\fetch-agents-YYYYMMDD-HHMMSS.log
REM
REM ==============================================================================

REM Check if argument provided
if "%~1"=="" (
    echo [ERROR] Value stream.fase pattern is required
    echo.
    echo Gebruik: fetch-agents.bat ^<value-stream.fase^>
    echo.
    echo Voorbeelden:
    echo   fetch-agents.bat miv.01
    echo   fetch-agents.bat aeo.02
    echo   fetch-agents.bat fnd.01
    echo   fetch-agents.bat sfw.01
    echo.
    pause
    exit /b 1
)

REM Create logs directory if needed
if not exist "logs" mkdir logs

REM Generate timestamp for wrapper log
for /f "delims=" %%i in ('powershell -Command "Get-Date -Format 'yyyyMMdd-HHmmss'"') do set timestamp=%%i
set logfile=logs\fetch-agents-%timestamp%.log

echo [INFO] Fetch agents wrapper gestart om %time%
echo [INFO] Pattern: %1
echo [INFO] Output log: %logfile%
echo.

REM Run script with pattern argument, log to file and console
python scripts\workspace-tools\fetch_mandarin_agents.py %1 > %logfile% 2>&1
set exit_code=%ERRORLEVEL%

REM Show log content
type %logfile%

REM Report result
echo.
if %exit_code% equ 0 (
    echo [WRAPPER] Fetch completed successfully
    echo [WRAPPER] Log: %logfile%
) else (
    echo [WRAPPER] Fetch failed with exit code %exit_code%
    echo [WRAPPER] Check log for details: %logfile%
)

exit /b %exit_code%
