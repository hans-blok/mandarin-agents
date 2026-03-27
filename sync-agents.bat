@echo off
REM ============================================================================
REM Sync Agents
REM 
REM Synchroniseert agent assets naar .github/ en .vscode/:
REM - Prompts naar .github/prompts/
REM - Agent-contracten naar .github/agents/
REM - Genereert .github/copilot/agents.yaml
REM - Aggregeert tasks naar .vscode/tasks.json
REM 
REM Verwerkt: aeo.02.* en fnd.01.* agents
REM ============================================================================

echo.
echo ============================================================================
echo Sync Agents
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
if not exist "scripts\sync_agents.py" (
    echo [ERROR] Script niet gevonden: scripts\sync_agents.py
    pause
    exit /b 1
)

REM Run het synchronisatie script (inclusief task aggregatie)
echo [Info] Start synchronisatie...
echo.
python scripts\sync_agents.py

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
