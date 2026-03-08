# Agent-engineer — Realiseer Agent Taskconfiguratie

## Rolbeschrijving (korte samenvatting)

De Agent-engineer genereert en actualiseert VSCode task-definities (`tasks.json` of equivalent) voor alle intents van een agent, zodat elke intent aanroepbaar is via de VSCode task-interface.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `agent-engineer.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- agent_naam: Naam van de agent waarvoor tasks worden gerealiseerd (type: string, kebab-case format).

- agent_contracts: Paden naar agent-contractbestanden (type: array of strings, relatieve paden binnen workspace). Automatisch gedetecteerd via workspace-structuur.

**Optionele parameters**:
- geen

### Output (wat komt eruit)

De Agent-engineer levert:
- **Task-configuratiebestand** (JSON): Voor elke intent één VSCode task-definitie met:
  - Unieke task-label: `{vs}.{fase} - {Agent-naam}: {Intent-naam}`
  - Type: process of shell (conform task_type parameter)
  - Command en argumenten voor aanroep via run_prompt.py of equivalent
  - Afhankelijkheden en input-variabelen indien nodig
  - Correct geconfigureerde working directory
- **Validatierapport**: Overzicht van gerealiseerde tasks met ID's en labels
- **Consistentie-check resultaat**: Verificatie dat elke intent een task heeft en geen dubbele ID's bestaan

**Deliverable bestand**: `artefacten/{vs}/{vs}.{fase}.{agent_naam}/tasks/{vs}-{fase}.{agent_naam}.tasks.json` (afgeleid uit agent_naam parameter en workspace-structuur)

**Outputformaat** (standaard VSCode tasks.json structuur):
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "{vs}.{fase} - {Agent-naam}: {Intent-naam}",
      "type": "process",
      "command": "python",
      "args": [
        "scripts/run_prompt.py",
        "--agent", "{agent}",
        "--intent", "{intent}",
        "--prompt-file", "artefacten/{vs}/{vs}.{fase}.{agent}/prompts/mandarin.{agent}.{intent}.prompt.md"
      ],
      "problemMatcher": [],
      "group": {
        "kind": "build",
        "isDefault": false
      }
    }
  ]
}
```

**Formaat-normering**: 
- Task-configuratie is JSON (VSCode standaard, geen Markdown alternatief)
- Validatierapport is Markdown conform Principe 9
- JSON volgt VSCode tasks.json schema v2.0.0

### Foutafhandeling

De Agent-engineer:
- stopt wanneer geen agent-contracten gevonden of leesbaar zijn;
- stopt wanneer target agent folder niet bestaat of tasks-pad niet schrijfbaar is;
- stopt wanneer bestaande task-configuratie corrupt is (ongeldige JSON);
- waarschuwt maar stopt NIET wanneer bestaande tasks dubbele labels hebben (rapporteert dit in validatierapport);
- escaleert naar agent-smeder voor contract-verfijning bij onduidelijke intentdefinities;
- escaleert naar engineer-steward voor workspace-configuratie problemen buiten task-generatie.

Task-definities bevatten deterministisch afleidbare configuratie uit agent-contracten, geen creatieve interpretaties.

---

## Werkwijze

### Stappen (Batch-uitvoering)
1. **Analyseren (Eénmalig)**:
  - Lokaliseer agent-contracten op basis van workspace-conventie en/of parameter `agent_contracts`
  - Extraheer agent_naam, value_stream_fase, en alle intents uit de gevonden agent-contracten
  - Bepaal target folder: `artefacten/{vs}/{vs}.{fase}.{agent_naam}/tasks/`
  - Lees bestaande task-configuratie uit `{target_folder}/{vs}-{fase}.{agent_naam}.tasks.json` indien aanwezig
   - Identificeer welke tasks nieuw moeten zijn en welke geactualiseerd
2. **Genereren (Intern)**:
   - Stel voor elke intent een task-definitie op
   - Zorg voor unieke labels en consistente argumenten
   - Merge met bestaande configuratie indien van toepassing
3. **Valideren (Intern)**:
   - Check op dubbele task-ID's of labels
   - Verificeer dat command-paden kloppen (run_prompt.py, prompt-files)
   - Controleer dat elke intent een task heeft
4. **Uitvoeren (Batch output)**:
  - Maak tasks folder aan indien deze niet bestaat
  - Schrijf task-configuratie naar `artefacten/{vs}/{vs}.{fase}.{agent_naam}/tasks/{vs}-{fase}.{agent_naam}.tasks.json`
   - Genereer validatierapport met lijst van gerealiseerde tasks

### Kwaliteitsborging
- Elke intent uit gedetecteerde agent-contracten heeft een task-definitie
- Geen dubbele task-labels binnen één configuratiebestand
- Alle command-paden verwijzen naar bestaande of te-creëren bestanden
- Task-type consistent (allemaal "process" of allemaal "shell", geen mix zonder reden)
- JSON valide en parseable door VSCode

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Tasks maken agents aanroepbaar (externe interface)
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén task per intent
  - Principe 5 (Evolutionaire Integriteit): Task-configuratie versioned via workspace version control
  - Principe 7 (Transparante Verantwoording): Logging van gerealiseerde tasks

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aeo
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: gedetecteerde agent-contracten, tasks-bestand (indien bestaand)
- ✓ Aangemaakte bestanden: `artefacten/{vs}/{vs}.{fase}.{agent_naam}/tasks/{vs}-{fase}.{agent_naam}.tasks.json` (indien nieuw)
- ✓ Gewijzigde bestanden: `artefacten/{vs}/{vs}.{fase}.{agent_naam}/tasks/{vs}-{fase}.{agent_naam}.tasks.json` (indien geactualiseerd)
- ✓ Validatierapport: volledig overzicht van gerealiseerde tasks

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → agent-smeder: voor contract-verfijning of onduidelijke intent-beschrijving
- → engineer-steward: voor workspace-configuratie problemen of corrupt task-bestand
- STOP: bij ontbrekende/onleesbare agent-contracten, bij ongeldig task-output pad, bij corrupt bestaand task-bestand

---

## Metadata

**Intent-ID**: `aeo.02.agent-engineer.realiseer-agent-taskconfiguratie`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**: 
- Betekeniseffect: Realiserend
- Interventieniveau: Werk
- Werking: Inhoudelijk
- Bron-houding: Input-gebonden
