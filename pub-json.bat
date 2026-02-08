@echo off
setlocal

REM Zet working directory naar de locatie van dit batch-bestand
cd /d "%~dp0"

REM ==============================================================================
REM Publiceer Agents JSON
REM ==============================================================================
REM
REM Doel:
REM   Voert agent-curator runner uit voor JSON publicatie (externe consumptie).
REM   Genereert agents-publicatie.json conform schema v2.0.
REM
REM Output:
REM   - agents-publicatie.json (root, voor fetch_agents.py en externe tools)
REM
REM Gebruik:
REM   pub-json.bat [volledig|incrementeel|value-stream|fase]
REM
REM Traceability:
REM   - Runner: scripts/agent-curator.runner.py
REM   - Charter: agent-charters/charter.agent-curator.md
REM
REM ==============================================================================

echo.
echo ========================================
echo  Agent Curator - Publiceer JSON
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

REM Bepaal scope (default: volledig)
set "SCOPE=%1"
if "%SCOPE%"=="" set "SCOPE=volledig"

REM Voer agent-curator uit voor JSON publicatie
echo [INFO] Start JSON publicatie (scope: %SCOPE%)...
echo.

python scripts\agent-curator.runner.py publiceer-json --scope %SCOPE%

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
echo [SUCCESS] JSON publicatie voltooid!
echo.
echo Output bestand:
echo   - agents-publicatie.json (schema v2.0)
echo.

pause
exit /b 0