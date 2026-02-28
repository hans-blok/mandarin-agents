# Tasks per Value Stream Fase

Deze folder bevat task definities georganiseerd per value stream fase.

## Structuur

- `global.json` - Algemene tasks (Canon sync, generic agent execute)
- `aeo-02.json` - Agent Ecosysteem Ontwikkeling fase 02 (Capability Architect, Agent Smeder)
- `aod-02.json` - Architectuur Ontwikkeling fase 02 (Core Framework Architect)

## Usage

**Tasks toevoegen:**
1. Voeg tasks toe in de juiste fase-specifieke JSON file
2. Gebruik prefix `{VS}.{FASE} - {Agent}: {Intent}` voor labels (bijv. "AOD.02 - Core Framework: Structureer Gedrag")
3. Run merge script om naar hoofdfile te schrijven

**Merge naar tasks.json:**
```powershell
python scripts/merge_tasks.py
```

Dit merged alle files in deze folder naar `.vscode/tasks.json`.

## Conventies

- Label format: `{VS}.{FASE} - {Agent}: {Intent}` (hoofdletters voor VS/FASE)
- Sorteer tasks alfabetisch binnen elke file
- Gebruik descriptive intent namen in labels
- Alle tasks gebruiken dezelfde input definitions (gedefinieerd in merge script)
- Tasks gebruiken VS Code input variables zoals `${input:landschapNaam}`, `${input:domeinNaam}`, etc.

## Beschikbare Inputs

Gedefinieerd in `scripts/merge_tasks.py` (automatisch toegevoegd bij merge):

- `agentName` - Agent naam (voor generic execution)
- `intentName` - Intent naam (voor generic execution)
- `targetAgentName` - Naam van target agent (voor smeder/curator)
- `valueStreamFase` - Value stream fase (bijv. aeo.02, fnd.01)
- `korteBeschrijving` - Korte beschrijving agent capability
- `landschapNaam` - Naam van het landschap (voor core-framework-architect)
- `domeinNaam` - Domein of value stream (voor core-framework-architect)
- `archimateLagen` - ArchiMate lagen (voor core-framework-architect)
- `activeStructuurFile` - Pad naar actieve structuur bestand (voor totaal view)
- `gedragFile` - Pad naar gedrag bestand (voor totaal view)

## Voordelen

- ✅ Centraal beheer per value stream fase
- ✅ Schaalbaar voor nieuwe agents
- ✅ Overzichtelijk per domein
- ✅ Geen merge conflicts bij parallelle ontwikkeling
- ✅ Eenvoudig nieuwe fase toevoegen = nieuw file aanmaken
