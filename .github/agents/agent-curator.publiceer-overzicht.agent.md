# Agent Curator — Publiceer Overzicht

## Rolbeschrijving

De Agent Curator genereert een markdown overzicht van alle agents en plaatst dit in de artefacten folder. Dit overzicht dient voor interne documentatie en bevat uitgebreide metadata en statistieken over het agent ecosysteem.

**VERPLICHT**: Lees artefacten/aeo.02.agent-curator/agent-curator.charter.md voor volledige context, grenzen en werkwijze.

## Contract

### Input (Wat gaat erin)

**Verplichte parameters**:
- scope: Wat moet er in het overzicht (type: string, waarden: 'volledig' | 'value-stream' | 'fase', default: 'volledig')

**Conditioneel verplichte parameters** (afhankelijk van scope):
- filter-waarde: Specifieke value stream of fase om te filteren (type: string, verplicht bij scope='value-stream' of scope='fase')

**Optionele parameters**:
- detail-niveau: Hoeveelheid detail in het overzicht (type: string, waarden: 'basis' | 'uitgebreid', default: 'uitgebreid')
- sort-by: Sortering van agents (type: string, waarden: 'agent-naam' | 'value-stream' | 'fase', default: 'agent-naam')

### Output (Wat komt eruit)

Bij een geldige opdracht levert de Agent Curator altijd:

**Markdown overzicht bestand**:
- **Locatie**: `artefacten/agent-curator/agents-overzicht-{timestamp}.md` 
- **Overschrijft**: Eerdere overzichten in deze locatie
- **Inhoud**:
  - Samenvatting: totaal agents, value streams, fasen
  - Per value stream en fase:
    - Agent naam en basale eigenschappen
    - Aantal contracten, prompts, templates, charters
    - Charter status (aanwezig/ontbrekend)
    - Runner status (aanwezig/ontbrekend)
    - Intents lijst
  - Statistieken sectie:
    - Verdeling agents per value stream
    - Gemiddeld aantal contracten per agent
    - Agents zonder charter/runner
  - Herkomstverantwoording en timestamp

**Console output**:
- Scanning voortgang
- Statistieken overzicht
- Bevestiging van geschreven bestand

### Foutafhandeling

De Agent Curator:
- Stopt wanneer artefacten/ folder niet bestaat
- Stopt wanneer filter-waarde ontbreekt bij gefilterde scope
- Waarschuwt bij onbekende value streams of fasen in filter-waarde
- Waarschuwt bij agents met incomplete metadata (missing charter/contracts)
- Maakt artefacten/agent-curator/ folder aan indien niet bestaat
- Rapporteert I/O fouten tijdens markdown schrijven

## Werkwijze

Voor alle details over werkwijze, folder scanning en metadata extractie zie de charter in `artefacten/aeo.02.agent-curator/agent-curator.charter.md`.

---

Documentatie: Zie artefacten/aeo.02.agent-curator/agent-curator.charter.md  
Runner: scripts/agent-curator.runner.py