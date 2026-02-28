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

echo.
echo ============================================================================
echo Synchronisatie succesvol afgerond
echo ============================================================================
echo.
pause
