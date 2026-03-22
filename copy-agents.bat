@echo off
REM ============================================================================
REM Copy Mandarin Agents Assets
REM 
REM Synchroniseert agent assets naar .github/ en genereert agents.yaml:
REM - Leegmaakt .github/prompts en .github/agents
REM - Kopieert alle prompts naar .github/prompts
REM - Kopieert alle agent-contracten naar .github/agents
REM - Verwijdert en regenereert .github/copilot/agents.yaml
REM 
REM Versie: 1.0.0
REM Auteur: agent-smeder
REM ============================================================================

echo.
echo ============================================================================
echo Copy Mandarin Agents Assets
echo ============================================================================
echo.

REM Ga naar workspace root
cd /d "%~dp0"

REM Check of Python beschikbaar is
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is niet beschikbaar in PATH
    echo        Installeer Python of activeer virtual environment
    pause
    exit /b 1
)

REM Check of script bestaat
if not exist "scripts\copy_prompts_mandarin_agents.py" (
    echo [ERROR] Script niet gevonden: scripts\copy_prompts_mandarin_agents.py
    pause
    exit /b 1
)

REM Verwijder .vscode\tasks.json
if exist ".vscode\tasks.json" (
    echo [Info] Verwijder .vscode\tasks.json...
    del /f ".vscode\tasks.json"
)

REM Run het synchronisatie script
echo [Info] Start synchronisatie...
echo.
python scripts\copy_prompts_mandarin_agents.py

if errorlevel 1 (
    echo.
    echo [ERROR] Synchronisatie mislukt
    pause
    exit /b 1
)

REM Activeer workspace configuratie (tasks.json)
echo [Info] Activeer workspace configuratie...
echo.
python artefacten/aeo/aeo.02.ecosysteem-coordinator/runner/ecosysteem-coordinator.runner.py activeer-workspace-configuratie

if errorlevel 1 (
    echo.
    echo [ERROR] Activeer workspace configuratie mislukt
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo Synchronisatie en workspace configuratie succesvol afgerond
echo ============================================================================
echo.
pause
