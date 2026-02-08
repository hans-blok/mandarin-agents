@echo off
setlocal

REM Zet working directory naar de locatie van dit batch-bestand
cd /d "%~dp0"

REM ==============================================================================
REM Publiceer Agents Overzicht
REM ==============================================================================
REM
REM Doel:
REM   Voert agent-curator runner uit voor markdown overzichten (interne documentatie).
REM   Genereert markdown rapporten in artefacten/agent-curator/.
REM
REM Output:
REM   - artefacten/agent-curator/agents-overzicht-[timestamp].md
REM   - artefacten/agent-curator/value-streams-overzicht-[timestamp].md
REM
REM Gebruik:
REM   pub-overzicht.bat [scope] [detail-niveau]
REM   
REM Parameters:
REM   scope: volledig|incrementeel|value-stream|fase (default: volledig)
REM   detail-niveau: basis|uitgebreid (default: uitgebreid)
REM
REM Voorbeelden:
REM   pub-overzicht.bat
REM   pub-overzicht.bat volledig basis
REM   pub-overzicht.bat value-stream uitgebreid
REM
REM Traceability:
REM   - Runner: scripts/agent-curator.runner.py
REM   - Charter: agent-charters/agent-curator.charter.md
REM
REM ==============================================================================

echo.
echo ==================================================
echo  Agent Curator - Publiceer Markdown Overzicht
echo ==================================================
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

REM Bepaal parameters (defaults: volledig, uitgebreid)
set "SCOPE=%1"
if "%SCOPE%"=="" set "SCOPE=volledig"

set "DETAIL_NIVEAU=%2"
if "%DETAIL_NIVEAU%"=="" set "DETAIL_NIVEAU=uitgebreid"

REM Voer agent-curator uit voor overzicht publicatie
echo [INFO] Start overzicht publicatie...
echo [INFO] Scope: %SCOPE%
echo [INFO] Detail niveau: %DETAIL_NIVEAU%
echo.

python scripts\agent-curator.runner.py publiceer-overzicht --scope %SCOPE% --detail-niveau %DETAIL_NIVEAU%

REM Controleer exit code
if errorlevel 1 (
    echo.
    echo [ERROR] Overzicht publicatie mislukt. Zie bovenstaande foutmeldingen.
    echo.
    pause
    exit /b 1
)

REM Succes
echo.
echo [SUCCESS] Overzicht publicatie voltooid!
echo.
echo Output locatie:
echo   - artefacten\agent-curator\*.md (markdown rapporten)
echo.

pause
exit /b 0