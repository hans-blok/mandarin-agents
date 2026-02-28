# Agent Curator — Publiceer JSON

## Rolbeschrijving

De Agent Curator genereert de agents-publicatie.json conform schema v2.0 voor externe consumptie. Dit JSON-bestand bevat een hiërarchische structuur van value streams, fasen en agents met alleen de essentiële counts (aantal bestanden per type).

**VERPLICHT**: Lees artefacten/aeo.02.agent-curator/agent-curator.charter.md voor volledige context, grenzen en werkwijze.

## Contract

### Input (Wat gaat erin)

**Verplichte parameters**:
- scope: Wat moet er gepubliceerd worden (type: string, waarden: 'volledig' | 'incrementeel', default: 'volledig')

**Optionele parameters**:
- output-pad: Alternatieve locatie voor JSON bestand (type: string, default: workspace root)

### Output (Wat komt eruit)

Bij een geldige opdracht levert de Agent Curator altijd:

**JSON Schema v2.0 bestand**:
- **Locatie**: `agents-publicatie.json` (workspace root)
- **Schema**: Conform `schemas/agents-publicatie-schema.json` v2.0
- **Structuur**: 
  ```json
  {
    "metadata": {
      "gegenereerd_op": "ISO 8601 timestamp",
      "versie": "2.0",
      "aantal_value_streams": N,
      "aantal_agents": M
    },
    "value_streams": [
      {
        "code": "aeo",
        "fasen": [
          {
            "volgnummer": "01",
            "agents": [
              {
                "naam": "agent-naam",
                "aantal_agent_files": N,
                "aantal_prompts": N,
                "aantal_templates": N,
                "aantal_charters": N
              }
            ]
          }
        ]
      }
    ]
  }
  ```

**Console output**:
- Scanning progress per value stream
- Statistics: totaal agents, value streams, fasen
- Success confirmatie met pad naar JSON bestand

### Foutafhandeling

De Agent Curator:
- Stopt wanneer artefacten/ folder niet bestaat
- Waarschuwt bij ongeldige folder namen (niet conform {vs}.{fase}.{agent} pattern)
- Waarschuwt bij lege value streams of fasen
- Stopt bij I/O fouten tijdens JSON schrijven
- Rapporteert schema validatie fouten (indien validatie enabled)

## Werkwijze

Voor alle details over werkwijze, folder scanning algoritme en schema conformiteit zie de charter in `artefacten/aeo.02.agent-curator/agent-curator.charter.md`.

---

Documentatie: Zie artefacten/aeo.02.agent-curator/agent-curator.charter.md  
Runner: scripts/agent-curator.runner.py
