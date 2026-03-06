@echo off
REM ============================================================================
REM Agent-Engineer Pipeline Runner
REM
REM Voert voor een specifieke agent de volgende intents uit:
REM 1. realiseer-agent-prompts
REM 2. realiseer-agent-taskconfiguratie
REM
REM Gebruik:
REM   run-agent-engineer-pipeline.bat agent-naam [opties]
REM
REM Voorbeelden:
REM   run-agent-engineer-pipeline.bat capability-architect
REM   run-agent-engineer-pipeline.bat agent-curator --skip-bootstrap
REM   run-agent-engineer-pipeline.bat --all                (alle agents)
REM ============================================================================

setlocal

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is niet beschikbaar in PATH.
    exit /b 1
)

REM Voer pipeline uit
python scripts\agent_engineer_pipeline.py %*

exit /b %ERRORLEVEL%
