@echo off
setlocal

REM Zet working directory naar de locatie van dit batch-bestand
cd /d "%~dp0"

REM ============================================================================
REM Copy AEO.02 Agents
REM ============================================================================
REM
REM Doel:
REM   Kopieert alle agents uit artefacten/aeo.02.* naar de centrale
REM   workspace-locaties:
REM     - .github/agents   (contracts: *.agent.md)
REM     - .github/prompts  (prompts: *.prompt.md)
REM     - agent-charters   (charters: *.charter.md)
REM     - templates        (agent-specifieke templates: *template*.md)
REM
REM Gebruik:
REM   copy_aeo_02_agents.bat
REM
REM Vereisten:
REM   - Uitvoeren vanuit de workspace root (waar scripts/ bestaat).
REM   - Python 3.9+ in PATH.
REM ============================================================================

echo.
echo ========================================
echo  Copy AEO.02 Agents
echo ========================================
echo.

REM Controleer of Python beschikbaar is
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python niet gevonden. Installeer Python 3.9+ en probeer opnieuw.
    echo.
    pause
    exit /b 1
)

REM Controleer of script bestaat op de verwachte locatie
if not exist "scripts\copy_aeo_02_agents.py" (
    echo [ERROR] Script niet gevonden: scripts\copy_aeo_02_agents.py
    echo.
    echo Dit script moet worden uitgevoerd vanuit de workspace root,
    echo waar scripts\copy_aeo_02_agents.py bestaat.
    echo.
    pause
    exit /b 1
)

echo [INFO] Start kopie van aeo.02 agents naar .github/agents, .github/prompts, agent-charters en templates
echo.

python scripts\copy_aeo_02_agents.py

if errorlevel 1 (
    echo.
    echo [ERROR] Kopieerscript is met fouten gestopt.
    echo.
    pause
    exit /b 1
)

echo.
echo [INFO] Kopie afgerond.
echo.
pause