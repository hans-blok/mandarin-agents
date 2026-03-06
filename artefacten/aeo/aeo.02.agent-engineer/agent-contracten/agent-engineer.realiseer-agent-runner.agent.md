# Agent-engineer — Realiseer Agent Runner

## Rolbeschrijving (korte samenvatting)

De Agent-engineer genereert Python runner-scripts voor alle intents van een agent, zodat elke intent programmatisch aanroepbaar is met correcte parameter-handling, logging en foutafhandeling.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `agent-engineer.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- agent_naam: Naam van de agent waarvoor runners worden gerealiseerd (type: string, kebab-case format).

**Optionele parameters**:
- contract_folder: Pad naar de folder met agent-contracten (type: string, relatief pad, format: `artefacten/{vs}/{vs}.{fase}.{agent}/agent-contracten/`). Indien niet opgegeven, automatisch afgeleid via workspace-conventie.
- runner_output_folder: Folder voor gegenereerde runners (type: string, default: `scripts/`).
- overwrite_existing: Of bestaande runner-scripts overschreven mogen worden (type: boolean, default: false).

### Output (wat komt eruit)

De Agent-engineer levert:
- **Runner-scripts** (`.py`): Voor elke intent één Python script met:
  - Correcte imports (argparse, run_prompt.py, logging)
  - Parameter-parsing gebaseerd op agent-contract input-specificatie
  - Aanroep van run_prompt.py met juiste argumenten
  - Foutafhandeling conform agent-contract escalatiepaden
  - Logging naar audit/agent-instructions.log.md
  - Docstring met korte beschrijving van intent
- **Validatierapport**: Overzicht van gerealiseerde runners met bestandsnamen en status

**Deliverable bestanden**: `{runner_output_folder}/{agent}-{intent}.runner.py`

**Outputformaat** (standaard Python runner structuur):
```python
#!/usr/bin/env python3
"""
Runner voor agent-engineer intent: {intent-naam}

Gegenereerd door agent-engineer op basis van:
- Contract-discovery: artefacten/{vs}/{vs}.{fase}.{agent}/agent-contracten/
- Contract: artefacten/{vs}/{vs}.{fase}.{agent}/agent-contracten/{agent}.{intent}.agent.md
"""

import argparse
import sys
from pathlib import Path

# Imports voor run_prompt.py (workspace-specifiek)
sys.path.insert(0, str(Path(__file__).parent))
from run_prompt import run_agent_intent


def main():
    parser = argparse.ArgumentParser(
        description="{Intent-naam} - {Korte rolbeschrijving uit contract}"
    )
    
    # Parameters gebaseerd op agent-contract input-specificatie
    parser.add_argument("--{param1}", required=True, help="{param1-beschrijving}")
    parser.add_argument("--{param2}", required=False, default={default}, help="{param2-beschrijving}")
    
    args = parser.parse_args()
    
    # Aanroep van run_prompt.py
    result = run_agent_intent(
        agent="{agent}",
        intent="{intent}",
        prompt_file="artefacten/{vs}/{vs}.{fase}.{agent}/prompts/mandarin.{agent}.{intent}.prompt.md",
        parameters=vars(args)
    )
    
    if not result.success:
        print(f"Error: {result.error_message}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Output: {result.output_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**Formaat-normering**: 
- Runners zijn Python-scripts (geen Markdown alternatief, dit is uitvoerbare code)
- Validatierapport is Markdown conform Principe 9
- Python code volgt PEP 8 en bevat type hints waar relevant

### Foutafhandeling

De Agent-engineer:
- stopt wanneer contract_folder (indien opgegeven) niet bestaat of leeg is;
- stopt wanneer geen agent-contracten gevonden of leesbaar zijn;
- stopt wanneer agent-contracten niet leesbaar zijn of geen input-sectie bevatten;
- stopt wanneer runner_output_folder niet bestaat en niet aangemaakt kan worden;
- vraagt om verduidelijking wanneer bestaande runners aanwezig zijn en overwrite_existing=false;
- escaleert naar agent-smeder voor contract-verfijning bij ontbrekende of onduidelijke input-specificaties;
- escaleert naar engineer-steward voor complexe runner-implementaties buiten standaard-patroon.

Runner-scripts bevatten ALLEEN deterministisch afleidbare logica uit contract (parameter-parsing, run_prompt aanroep), geen domein-specifieke business logic.

---

## Werkwijze

### Stappen (Batch-uitvoering)
1. **Analyseren (Eénmalig)**:
    - Lokaliseer agent-contracten via workspace-conventie en/of `contract_folder`
    - Extraheer agent_naam, value_stream_fase, en alle intents uit agent-contracten
   - Extraheer per contract de input-parameters (verplicht en optioneel)
    - Bepaal runner-bestandsnamen volgens conventie
2. **Genereren (Intern)**:
   - Stel voor elke intent een runner-script op in geheugen
   - Genereer argparse-configuratie gebaseerd op contract input-sectie
   - Zorg voor correcte run_prompt.py aanroep met juiste paden
   - Voeg foutafhandeling toe conform contract escalatiepaden
3. **Uitvoeren (Batch output)**:
   - Schrijf alle `.runner.py` bestanden naar runner_output_folder
   - Maak bestanden executable (chmod +x op Unix-systemen)
   - Genereer validatierapport met overzicht van gerealiseerde runners

### Kwaliteitsborging
- Elke intent uit gedetecteerde agent-contracten heeft een runner-script
- Alle verplichte parameters uit contract zijn required arguments in runner
- Alle optionele parameters uit contract hebben default values in runner
- Runner-scripts zijn syntactisch valide Python (parseable zonder errors)
- Paden naar prompt-files in runners zijn correct en relatief tot workspace root
- Bestandsnaamconventie gevolgd: `{agent}-{intent}.runner.py`

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Runners maken contract programmatisch aanroepbaar
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén runner per intent
  - Principe 5 (Evolutionaire Integriteit): Runners versioned via workspace version control
  - Principe 7 (Transparante Verantwoording): Logging ingebouwd in runners

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aeo
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: alle gedetecteerde agent-contract bestanden
- ✓ Aangemaakte bestanden: alle nieuwe `.runner.py` bestanden
- ✓ Gewijzigde bestanden: geactualiseerde `.runner.py` bestanden (indien overwrite_existing=true)
- ✓ Validatierapport: volledig overzicht van gerealiseerde runners

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → agent-smeder: voor contract-verfijning of ontbrekende input-specificaties
- → engineer-steward: voor complexe runner-implementaties of custom business logic
- STOP: bij ontbrekende/onleesbare agent-contracten, bij lege contract_folder (indien opgegeven)

---

## Metadata

**Intent-ID**: `aeo.02.agent-engineer.realiseer-agent-runner`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**: 
- Betekeniseffect: Realiserend
- Interventieniveau: Werk
- Werking: Inhoudelijk
- Bron-houding: Input-gebonden
