---
agent: ecosysteem-coordinator
intent: merge-configuraties
versie: 1.0.0
---

# Ecosysteem-coordinator — Merge Configuraties

## Rolbeschrijving (korte samenvatting)

Aggregeert agent-specifieke task-configuraties uit de hele workspace naar één globale `.vscode/tasks.json`, zodat alle agent-intents via VS Code Tasks aanroepbaar zijn zonder handmatige configuratie.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `ecosysteem-coordinator.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- Geen verplichte parameters; werkt op workspace-conventie

**Optionele parameters**:
- filter_fase: Filter op specifieke value stream fase (type: string, bijv. "aeo.02", "sfw.01").
- tasks_folder: Pad naar .vscode/tasks/ folder (type: string, default: ".vscode/tasks/").
- output_file: Pad naar output tasks.json (type: string, default: ".vscode/tasks.json").
- dry_run: Toon wat zou worden samengevoegd zonder te schrijven (type: boolean, default: false).

### Output (wat komt eruit)

De ecosysteem-coordinator levert:
- **Samengevoegde tasks.json**: Volledig JSON-bestand met alle agent tasks
  - version: "2.0.0"
  - tasks: Alle tasks uit agent-specifieke bestanden
  - inputs: Gecombineerde input-definities voor VS Code prompts
- **Console rapport**: Overzicht van verwerkte bestanden en task-counts

**Deliverable bestand**: `.vscode/tasks.json`

**Outputformaat** (tasks.json):
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "{vs}.{fase} - {agent}: {intent}",
      "type": "process",
      "command": "python",
      "args": [
        "artefacten/{vs}/{vs}.{fase}.{agent}/runners/{agent}.runner.py",
        "{intent}",
        "--param-1", "${input:paramName}"
      ]
    }
  ],
  "inputs": [
    {
      "id": "paramName",
      "type": "promptString",
      "description": "Parameter beschrijving"
    }
  ]
}
```

**Formaat-normering**: 
- JSON conform VS Code tasks schema v2.0.0
- UTF-8 encoding
- 2-space indentation

### Foutafhandeling

De ecosysteem-coordinator:
- stopt wanneer geen task-bestanden gevonden worden;
- stopt wanneer een task-bestand ongeldige JSON bevat (parseert niet);
- waarschuwt bij duplicate task labels (neemt laatste waarde);
- waarschuwt bij duplicate input IDs (neemt laatste waarde);
- vraagt NIET om verduidelijking (deterministic aggregation).

---

## Werkwijze

### Stappen
1. **Scan .vscode/tasks/**: Verzamel alle *.json bestanden
2. **Scan artefacten/**: Zoek alle **/tasks/*.tasks.json bestanden
3. **Filter indien opgegeven**: Pas filter_fase toe op bestandsnamen
4. **Parse JSON**: Laad elk bestand en valideer structuur
5. **Merge tasks**: Combineer alle tasks arrays met deduplicatie
6. **Merge inputs**: Combineer alle inputs arrays met deduplicatie
7. **Write output**: Schrijf samengevoegde tasks.json
8. **Report**: Print overzicht van bronbestanden en task-counts

### Kwaliteitsborging
- Output JSON is syntactisch correct (valideer voor schrijven)
- Alle bronbestanden worden gelogd
- Task labels zijn uniek (warning bij duplicaten)

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 4 (Scheiding van Wat en Hoe): Aggregeert alleen, wijzigt geen task-definities
  - Principe 7 (Transparante Verantwoording): Logt alle bronbestanden

**Canon-consultatie:**
- Geen canon-consultatie vereist (pure aggregatie-operatie)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Alle gelezen task-bestanden (paden)
- ✓ Aantal tasks per bronbestand
- ✓ Totaal aantal samengevoegde tasks
- ✓ Eventuele duplicaat-warnings

Logging-formaat: Console output (geen audit log append voor deze operatie)

**Escalatie-paden:**
- → agent-engineer: indien task-bestanden ontbreken voor bekende agents
- STOP: bij geen task-bestanden gevonden
- STOP: bij JSON parse errors

---

## Metadata

**Intent-ID**: `aeo.02.ecosysteem-coordinator.merge-configuraties`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**: Conditioneel / Input-gebonden
