# Task-drafter — Realiseer VSCode Tasks JSON

## Rolbeschrijving (korte samenvatting)

De task-drafter realiseert en onderhoudt `.vscode/tasks.json` zodat agent-intents eenduidig en direct startbaar zijn via VS Code tasks. Binnen deze intent vertaalt de agent boundary- en intentinformatie naar concrete task-definities zonder de intent-inhoud zelf uit te voeren.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `task-drafter.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- `agent_naam`: Naam van de doelagent waarvoor tasks worden opgenomen (type: string, kebab-case).

**Optionele parameters**:
- `intent`: Intentnaam die als task startbaar moet worden gemaakt (type: string, kebab-case).
- `agent_contract`: Pad naar specifiek agent-contractbestand (type: string, relatief pad naar `.agent.md`).
- `task_label`: Overschrijft standaard taaklabel (type: string, default: afgeleid van intent).
- `command`: Overschrijft standaard commandostructuur (type: string, default: powershell-oproep generate_instructions.py).
- `inputs`: Extra VS Code task inputs (type: list, default: lege lijst).

**Selectieregel intent-scope**:
- Als `intent` of `agent_contract` is meegegeven: maak of update alleen de task(s) voor die specifieke intent.
- Als beide niet zijn meegegeven: maak of update tasks voor alle intents op basis van alle agent-contracten van `agent_naam`.

### Output (wat komt eruit)

De task-drafter levert:
- **Bijgewerkt taskbestand**: `.vscode/tasks.json`
  - nieuwe of geüpdatete task entry met label, command, args en presentation
  - consistente naamgeving en parameterisatie voor intent-start
  - behoud van valide JSONC-structuur van het bestand
- **Traceerinformatie**: intent en herkomst opgenomen in task-detail of aanvullende velden

**Deliverable bestand**: `.vscode/tasks.json`

**Outputformaat** (standaard structuur):
```jsonc
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "AEO.02 - <Agent>: <Intent>",
      "type": "process",
      "command": "powershell",
      "args": [
        "-Command",
        "... generate_instructions.py ..."
      ],
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "shared"
      }
    }
  ]
}
```

**Formaat-normering**:
- Default formaat: **JSONC** binnen `.vscode/tasks.json` (workspace-taskstandaard)
- Structuur volgt VS Code tasks schema `version: 2.0.0`
- Wijzigingen blijven beperkt tot task-definities en bijbehorende inputs

### Foutafhandeling

De task-drafter:
- stopt wanneer `.vscode/tasks.json` niet leesbaar is of niet parsebaar naar geldige tasks-structuur;
- stopt wanneer `agent_naam` ontbreekt of ongeldig geformatteerd is;
- stopt wanneer `agent_contract` is opgegeven maar niet bestaat of niet eindigt op `.agent.md`;
- stopt wanneer de gevraagde wijziging buiten task-orchestratie valt (bijv. inhoudelijke prompt- of contractgeneratie);
- vraagt om verduidelijking wanneer label-conventie of commandostructuur ambigu is;
- escaleert naar `agent-smeder` wanneer de intent/contractcontext onvolledig is;
- escaleert naar `capability-architect` wanneer boundary-afbakening onduidelijk of conflicterend is.

Deze intent realiseert alleen task-registratie en voert geen agent-intentinhoud uit.

---

## Werkwijze

### Stappen (Batch-uitvoering)
1. Bepaal scope op basis van parameters: specifieke intent (`intent`/`agent_contract`) of alle intents van `agent_naam`.
2. Lees boundary en relevante agent-contracten voor de te realiseren intent(s).
3. Lees bestaande `.vscode/tasks.json` en inventariseer bestaande labels/inputs.
4. Genereer nieuwe of bijgewerkte task-entry conform naamgevingsconventie.
5. Pas tasks en benodigde inputs consistent toe in één wijzigingsset.
6. Valideer syntactische geldigheid van het bestand en controleer op dubbele labels.

### Kwaliteitsborging
- Elke gerealiseerde intent heeft exact één eenduidig task-label.
- Bij meegegeven `intent`/`agent_contract` worden geen taken buiten die scope aangemaakt of aangepast.
- Zonder `intent`/`agent_contract` worden voor alle gevonden agent-contracten van `agent_naam` tasks gerealiseerd.
- Task entry bevat command, args, problemMatcher en presentation.
- Bestandsstructuur blijft valide JSONC met `version: "2.0.0"`.
- Geen inhoudelijke runtime-acties buiten task-registratie.

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): contract beschrijft extern observeerbaar gedrag
  - Principe 2 (Eenduidige Verantwoordelijkheid): intent beperkt tot tasks-json realisatie
  - Principe 7 (Transparante Verantwoording): wijzigingen en herkomst traceerbaar
- **doctrine-mandarin-agents-output-structuur.md**: output en paden consistent met workspace-conventies

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream `aeo`
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: boundary, bestaande `.vscode/tasks.json`, relevante templates
- ✓ Aangemaakte bestanden: niet van toepassing tenzij tasks-bestand initieel ontbreekt
- ✓ Gewijzigde bestanden: `.vscode/tasks.json` met wijzigingsdoel per task-entry

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → `agent-smeder`: voor onduidelijke intent- of contractdefinitie
- → `capability-architect`: voor boundary-conflicten of scope-ambiguïteit
- STOP: bij ongeldige taskstructuur of ontbrekende minimale input

---

## Metadata

**Intent-ID**: `aeo.02.task-drafter.realiseer-vscode-tasks-json`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**: 
- Betekeniseffect: Realiserend
- Interventieniveau: Werk
- Werking: Inhoudelijk
- Bron-houding: Canon-gebonden