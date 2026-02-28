@echo off
REM ============================================================================
REM Generate agents-publicatie.json v2.0
REM 
REM Scant alle value_stream folders in artefacten/ en genereert een
REM vereenvoudigd JSON-bestand met counts van agent artifacts.
REM 
REM Versie: 2.0.0
REM Auteur: engineer-steward
REM ============================================================================

echo.
echo ============================================================================
echo Generate agents-publicatie.json v2.0
echo ============================================================================
echo.

REM Ga naar workspace root
cd /d "%~dp0"

REM Roep Python script aan
python scripts\generate_agents_publicatie.py

REM Check exit code
if %ERRORLEVEL% neq 0 (
    echo.
    echo [FOUT] Script gefaald met exit code %ERRORLEVEL%
    echo.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [OK] agents-publicatie.json succesvol gegenereerd
echo.
pause
