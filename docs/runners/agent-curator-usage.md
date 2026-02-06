# Agent Curator — Publiceer Agents Overzicht

## Overzicht

De Agent Curator runner scant alle agent-folders in `artefacten/` en genereert een overzicht van alle agents gestructureerd per value stream en fase.

## Output

### JSON (agents-publicatie.json)

Een machine-leesbaar overzicht volgens het schema in `schemas/agents-publicatie-schema.json` met:
- Value streams met hun naam en 3-letter code
- Fases binnen elke value stream met naam en 2-cijferig volgnummer
- Agents per fase met:
  - Naam
  - Aantal contracts (*.agent.md bestanden)
  - Aantal templates (uit Template veld in charter)
  - Aantal runners (in scripts/runners/)
  - Optioneel: domein

### Markdown (docs/resultaten/agent-publicaties/)

Een overzichtelijk gearchiveerd rapport met tabellen per value stream en fase, inclusief metadata over de scan.

## Gebruik

```bash
# Genereer volledig overzicht
python scripts/runners/agent-curator.py
```

Het script scant automatisch:
- `artefacten/<vs-code>.<fase-nr>.<agent-naam>/` (flat structuur)
- `artefacten/<vs-code>/<vs-code>.<fase-nr>.<agent-naam>/` (nested structuur)

## Folder Naming Conventie

Agents moeten volgens het patroon benoemd zijn:
```
<vs-code>.<fase-nr>.<agent-naam>
```

Waarbij:
- `vs-code`: 3-letter value stream code (aeo, sfw, aod, kvl, miv, fnd)
- `fase-nr`: 2-cijferig fasenummer (01, 02, 03, ...)
- `agent-naam`: agent identifier (lowercase met hyphens)

Voorbeelden:
- `aeo.02.agent-curator`
- `sfw.01.hypothese-vormer`
- `fnd.01.workspace-steward`

## Counted Artifacts

1. **Contracts**: `<agent-naam>.*.agent.md` bestanden in de agent folder
2. **Templates**: Template veld in charter (niet "-" of "—"), bestand moet bestaan in `templates/`
3. **Runners**: 
   - Script: `scripts/runners/<agent-naam>.py`
   - Module: `scripts/runners/<agent-naam>/__init__.py`

## Value Streams & Fases

De mappings van codes naar namen zijn gedefinieerd in de runner op basis van:
- `temp/mandarin-value-streams-en-fasen.md`

Ondersteunde value streams:
- **AEO** (00): Agent Ecosysteem Ontwikkeling
- **SFW** (01): Softwareontwikkeling  
- **AOD** (02): Architectuur- en Oplossingsontwerp
- **KVL** (03): Kennisvastlegging
- **MIV** (04): Markt- en Investeringsvorming
- **FND**: Foundational (value-stream-overstijgend)

## Schema

Het JSON-formaat volgt het schema: `schemas/agents-publicatie-schema.json`

Versie 3.0 introduceert de nieuwe structuur met nested value streams en fases.

## Traceability

- Charter: `artefacten/aeo.02.agent-curator/agent-curator.charter.md`
- Contract: `artefacten/aeo.02.agent-curator/agent-curator.publiceer-agents.overzicht.agent.md`
- Prompt: `.github/prompts/mandarin.agent-curator.publiceer-agents.overzicht.prompt.md`
- Schema: `schemas/agents-publicatie-schema.json`
- Runner: `scripts/runners/agent-curator.py`
