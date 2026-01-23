@echo off
REM ==============================================================================
REM Fetch Agents - Windows Wrapper
REM ==============================================================================
REM
REM Wrapper script voor fetch_agents.py voor Windows gebruikers.
REM Fetcht agents uit agent-services repository voor opgegeven value stream.
REM
REM Gebruik:
REM   fetch-agents.bat <value-stream>
REM   fetch-agents.bat kennispublicatie
REM   fetch-agents.bat --list
REM
REM ==============================================================================

if "%~1"=="" (
    echo [ERROR] Value stream argument is required
    echo.
    echo Gebruik: fetch-agents.bat ^<value-stream^>
    echo Voorbeeld: fetch-agents.bat kennispublicatie
    echo.
    echo Voor lijst van beschikbare value streams:
    echo   fetch-agents.bat --list
    pause
    exit /b 1
)

python scripts\fetch_agents.py %*
