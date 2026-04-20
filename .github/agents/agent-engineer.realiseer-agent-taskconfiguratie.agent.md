---
agent: agent-engineer
intent: realiseer-agent-taskconfiguratie
intent-id: aeo.02.agent-engineer.02
versie: 1.1.0
digest: 0e61
status: vers
---
# Agent-engineer — Realiseer Agent Taskconfiguratie

## Rolbeschrijving (korte samenvatting)

De agent-engineer genereert en actualiseert VSCode task-definities voor alle intents van een agent, zodat elke intent aanroepbaar is via de VSCode task-interface en de bestaande doelagent-runner.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `agent-engineer.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- agent_naam: Naam van de agent waarvoor tasks worden gerealiseerd (type: string, kebab-case format).

**Optionele parameters**:
- geen

**Afgeleide informatie**:
- agent-contracten: automatisch gedetecteerd via de workspace-structuur
- value_stream_fase, `vs` en `fase`: afgeleid uit de agentfolder
- runner-pad: afgeleid als `artefacten/{vs}/{vs}.{fase}.{agent_naam}/runner/{agent_naam}.runner.py`

### Output (wat komt eruit)

De agent-engineer levert één task-configuratiebestand:

`artefacten/{vs}/{vs}.{fase}.{agent_naam}/tasks/{vs}-{fase}.{agent_naam}.tasks.json`

**Contractuele templatebinding**:
```yaml
output:
  - type: tasks-configuratie
    herkomstpositie: initiërend
    template: ~
```

Dit bestand bevat:
- `version: 2.0.0`
- een `tasks`-array met per intent precies één `process`-task
- een `inputs`-array met één `promptString`-invoer per contractparameter

**Outputformaat** (representatieve VSCode tasks.json structuur):
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "{vs}.{fase} - {Agent-naam}: {Intent-naam}",
      "type": "process",
      "command": "python",
      "args": [
        "artefacten/{vs}/{vs}.{fase}.{agent}/runner/{agent}.runner.py",
        "{intent}",
        "--{contract-parameter-kebab-case}",
        "${input:in_{agent}_{intent}_{parameter}}"
      ],
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "shared"
      }
    }
  ],
  "inputs": [
    {
      "id": "in_{agent}_{intent}_{parameter}",
      "type": "promptString",
      "description": "{parameter-beschrijving}"
    }
  ]
}
```

**Formaat-normering**: 
- Task-configuratie is JSON (VSCode standaard, geen Markdown alternatief)
- JSON volgt VSCode tasks.json schema v2.0.0
- `template: ~` is expliciet omdat de volledige vorm in dit contract en het JSON-schema al voldoende is gespecificeerd

### Foutafhandeling

De Agent-engineer:
- stopt wanneer de doelagent niet via contract-discovery kan worden gevonden;
- stopt wanneer geen leesbare agent-contracten of geldige intents worden gevonden;
- stopt wanneer het tasks-pad niet kan worden aangemaakt of beschreven;
- overschrijft het bestaande task-configuratiebestand deterministisch;
- vereist contract-verfijning door agent-ontwerper wanneer intent- of parameterinformatie onvoldoende expliciet is.

Task-definities bevatten uitsluitend deterministisch afleidbare configuratie uit agent-contracten en folderstructuur.

---

## Werkwijze

### Stappen (Batch-uitvoering)
1. **Analyseren**:
  - lokaliseer de agentfolder en contracten via workspace-conventie;
  - leid `vs`, `fase`, `value_stream_fase` en het runner-pad af;
  - extraheer per contract de intent plus verplichte en optionele parameters.
2. **Genereren**:
  - stel voor elke intent een `process`-task op;
  - vertaal contractparameters naar CLI-argumenten in kebab-case;
  - maak per unieke parameterprompt een `inputs`-item aan.
3. **Uitvoeren**:
  - maak de tasks-folder aan indien nodig;
  - schrijf het volledige JSON-bestand deterministisch weg;
  - rapporteer via console-output het aantal tasks en inputs.

### Kwaliteitsborging
- Elke intent uit gedetecteerde agent-contracten heeft één task-definitie.
- Elke task heeft `type: process`, `command: python` en `presentation.reveal/panel`.
- Elke contractparameter resulteert in een CLI-argument en een input-definitie.
- JSON is valide en parseable door VSCode.

---

## Governance

**Doctrine-naleving:**
- **doctrine-bronhouding-en-exploratie.md**:
  - Input-gebonden bronhouding: alleen expliciete input en afleidbare workspace-context gebruiken
  - Geen aanvullende kennis of exploratieve invulling buiten de meegeleverde context
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Tasks maken bestaande agent-runners aanroepbaar (externe interface)
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén task per intent
  - Principe 5 (Evolutionaire Integriteit): Task-configuratie versioned via workspace version control
  - Principe 7 (Transparante Verantwoording): Console-output maakt gerealiseerde aantallen zichtbaar
- **doctrine-runner-discipline-en-runner-kernel.md**:
  - Task-configuraties verwijzen consistent naar de doelagent-runner
  - Geen creatieve of agent-specifieke afwijkingen in aanroepstructuur zonder expliciete reden
- **doctrine-templategebruik.md** (v1.0.0):
  - ook voor configuratie-output moet expliciet worden vastgelegd dat geen afzonderlijk template geldt (`template: ~`)

**Canon-consultatie:**
- de directe subcommand `realiseer-agent-taskconfiguratie` voert zelf geen canon-consultatie uit;
- wanneer deze intent via de ecosysteem-coordinator wordt gestart, wordt governance-context daar vooraf samengesteld en vastgelegd.

**Transparantie-verplichtingen:**

Bij uitvoering rapporteert de runner via console-output ten minste:
- het pad van het geschreven task-configuratiebestand;
- het aantal gerealiseerde tasks;
- het aantal gerealiseerde inputs.

**Escalatie-paden:**
- contract-verfijning verloopt via agent-ontwerper;
- STOP: bij ontbrekende/onleesbare agent-contracten, ontbrekende agentcontext of onschrijfbaar task-outputpad.

---
