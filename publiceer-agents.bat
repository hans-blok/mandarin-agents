@echo off
setlocal

REM Zet working directory naar de locatie van dit batch-bestand
cd /d "%~dp0"

REM ==============================================================================
REM Publiceer Agents Overzicht
REM ==============================================================================
REM
REM Doel:
REM   Voert agent-curator runner uit voor volledige agents publicatie.
REM   Genereert agents-publicatie.json en markdown archief met digest.
REM
REM Output:
REM   - agents-publicatie.json (root, voor fetch_agents.py)
REM   - docs/resultaten/agent-publicaties/agents-publicatie-YYYYMMDD-HHMMSS.md
REM
REM Gebruik:
REM   publiceer-agents.bat
REM
REM Traceability:
REM   - Runner: scripts/agent-curator.runner.py
REM   - Charter: agent-charters/charter.agent-curator.md
REM
REM ==============================================================================

echo.
echo ========================================
echo  Agent Curator - Publiceer Overzicht
echo ========================================
echo.

REM Controleer of Python beschikbaar is
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python niet gevonden. Installeer Python 3.9+ en probeer opnieuw.
    pause
    exit /b 1
)

REM Controleer of runner script bestaat
if not exist "scripts\agent-curator.runner.py" (
    echo [ERROR] Runner niet gevonden: scripts\agent-curator.runner.py
    pause
    exit /b 1
)

REM Controleer of artefacten folder bestaat
if not exist "artefacten" (
    echo [ERROR] Folder niet gevonden: artefacten
    echo [DEBUG] Verwachte locatie: %CD%\artefacten
    echo.
    pause
    exit /b 1
)

REM Voer agent-curator uit met volledige scope
echo [INFO] Start volledige agents publicatie...
echo.

python scripts\agent-curator.runner.py --scope volledig

REM Controleer exit code
if errorlevel 1 (
    echo.
    echo [ERROR] Publicatie mislukt. Zie bovenstaande foutmeldingen.
    echo.
    pause
    exit /b 1
)

REM Succes
echo.
echo [SUCCESS] Publicatie voltooid!
echo.
echo Output bestanden:
echo   - agents-publicatie.json
echo   - docs\resultaten\agent-publicaties\agents-publicatie-[timestamp].md
echo.

pause
exit /b 0