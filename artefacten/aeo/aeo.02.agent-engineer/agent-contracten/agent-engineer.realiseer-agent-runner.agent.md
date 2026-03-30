---
agent: agent-engineer
intent: realiseer-agent-runner
versie: 1.2.0
---

# Agent-engineer — Realiseer Agent Runner

## Rolbeschrijving (korte samenvatting)

De agent-engineer genereert centrale Python runners voor doelagents, zodat elke intent van die agent via één vaste voordeur aanroepbaar is en execution-file generatie gedelegeerd kan worden aan de ecosysteem-coordinator.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `agent-engineer.charter.md` in de parent folder van dit contract.

**Status**: Operationeel realisatiepad.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- agent_naam: Naam van de agent waarvoor runners worden gerealiseerd (type: string, kebab-case format).

**Optionele parameters**:
- contract_folder: Pad naar de folder met agent-contracten (type: string, relatief pad, format: `artefacten/{vs}/{vs}.{fase}.{agent}/agent-contracten/`). Indien niet opgegeven, automatisch afgeleid via workspace-conventie.
- runner_output_folder: Folder voor gegenereerde runners (type: string, default: `scripts/`).
- overwrite_existing: Of bestaande runner-scripts overschreven mogen worden (type: boolean, default: false).

### Output (wat komt eruit)

De agent-engineer levert één centraal runnerbestand per doelagent:

`artefacten/{vs}/{vs}.{fase}.{agent}/runner/{agent}.runner.py`

Of, wanneer `runner_output_folder` expliciet is opgegeven:

`{runner_output_folder}/{agent}.runner.py`

De runner bevat:
- één argparse-subcommand per gedetecteerde intent;
- per intent CLI-parameters afgeleid uit verplichte en optionele contractparameters;
- een gedeelde delegatiefunctie die `ecosysteem-coordinator.runner.py genereer-instructies` aanroept;
- een vaste `TARGET_AGENT`-constante voor de doelagent.

**Outputformaat** (operationele doelstructuur):
```python
#!/usr/bin/env python3
"""
Runner voor agent: {agent}
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


TARGET_AGENT = "{agent}"


def run_intent(intent: str, params: dict[str, str]) -> int:
    ...


def main() -> int:
    parser = argparse.ArgumentParser(description=f"Runner voor agent: {TARGET_AGENT}")
    subparsers = parser.add_subparsers(dest="intent", required=True)
    # intent-parsers afgeleid uit contracten

    args = parser.parse_args()
    return run_intent(args.intent, params)


if __name__ == "__main__":
    sys.exit(main())
```

**Formaat-normering**: 
- runners zijn Python-scripts (geen Markdown alternatief);
- de gegenereerde runner bevat alleen deterministisch afleidbare parser- en delegatielogica;
- de runner bevat geen domein-specifieke business logic.

### Foutafhandeling

De Agent-engineer:
- stopt wanneer de doelagent niet via contract-discovery kan worden gevonden;
- stopt wanneer de opgegeven `contract_folder` niet bestaat of geen `.agent.md` bestanden bevat;
- stopt wanneer geen intents uit de contractset kunnen worden afgeleid;
- stopt wanneer het doelrunnerbestand al bestaat en `overwrite_existing` niet expliciet `true` is;
- vereist contractverfijning door agent-ontwerper wanneer parameter- of intentinformatie onvoldoende expliciet is.

---

## Werkwijze

### Stappen (Batch-uitvoering)
1. **Context ontdekken**:
    - lokaliseer de doelagent via contract-discovery of expliciete contractfolder;
    - bepaal `vs`, `fase`, `value_stream_fase` en het outputpad.
2. **Contracten analyseren**:
    - lees alle doelcontracten;
    - extraheer intents en hun verplichte en optionele parameters.
3. **Runner genereren**:
    - genereer één centrale runner met subcommands voor alle intents;
    - genereer CLI-argumenten in kebab-case op basis van contractparameters;
    - voeg een delegatiefunctie toe richting de ecosysteem-coordinator.
4. **Schrijven en rapporteren**:
    - schrijf het runnerbestand weg;
    - rapporteer via console-output het doelpad en het aantal verwerkte contracten.

### Kwaliteitsborging
- Elke gedetecteerde intent heeft een subcommand in de gegenereerde runner.
- Elke contractparameter resulteert in een CLI-argument.
- De runner is syntactisch valide Python.
- Delegatie verloopt consequent via `ecosysteem-coordinator.runner.py genereer-instructies`.

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
    - Principe 1 (Identiteit vóór Implementatie): één centrale runner vormt de vaste voordeur van de agent
    - Principe 2 (Eenduidige Verantwoordelijkheid): de runner beperkt zich tot parser- en delegatielogica
    - Principe 5 (Evolutionaire Integriteit): runner-generatie is versioned via workspace version control

**Canon-consultatie:**
- de generator zelf voert geen canon-consultatie uit;
- governance-opbouw voor execution-files blijft bij de ecosysteem-coordinator, die door de gegenereerde runner wordt aangeroepen.

**Transparantie-verplichtingen:**

Bij uitvoering rapporteert de runner-generator via console-output:
- het pad van het gegenereerde runnerbestand;
- het aantal verwerkte contracten.

**Escalatie-paden:**
- contractverfijning verloopt via agent-ontwerper;
- engineer-steward is alleen nodig voor aanvullende domeinspecifieke runnerlogica buiten het delegatiepatroon;
- STOP: bij ontbrekende agentcontext, ongeldige contractfolder of bestaand runnerbestand zonder expliciete overwrite-toestemming.
