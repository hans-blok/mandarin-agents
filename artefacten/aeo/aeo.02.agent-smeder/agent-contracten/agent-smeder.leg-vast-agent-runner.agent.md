# Agent Smeder — Schrijf Runner

## Rolbeschrijving (korte samenvatting)

De Agent Smeder creëert een Python runner-script op basis van het agent-contract en charter, door het runner skeleton in te vullen met agent-specifieke parameters, validaties en run_prompt.py aanroep-logica.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `{agent-naam}.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- boundary_file: Pad naar boundary-bestand (type: string, relatief pad).
- agent_contract_file: Pad naar agent-contract bestand (type: string, relatief pad, .agent.md).
- skeleton_file: Template bestandsnaam voor runner skeleton (type: string, bijv. "agent-runner.skeleton.py"). Locatie wordt afgeleid via conventie.

**Afgeleide informatie** (geëxtraheerd uit boundary en contract):
- agent_naam: Afgeleid uit boundary-bestandsnaam of contract metadata
- intent: Afgeleid uit agent_contract_file bestandsnaam of metadata
- value_stream_fase: Afgeleid uit boundary header (format: "{vs}.{fase}")

**Optionele parameters**:
- charter_file: Pad naar charter bestand voor extra context (type: string, optioneel).

### Output (wat komt eruit)

De Agent Smeder levert:
- **Python runner script** (`.runner.py`) met:
  - Configuration: Agent/intent/prompt-pad constanten ingevuld
  - CLI arguments: Agent-specifieke parameters uit agent-contract (verplicht vs optioneel)
  - Input validatie: Validaties afgeleid uit contract (formaat, constraints, business rules)
  - Parameter mapping: CLI args → run_prompt.py `-p` parameters
  - Run execution: Correct aangeroepen run_prompt.py met juiste paden
  - Audit logging: Logging naar audit/{runner-naam}.log.md
  - Error handling: Exit codes (0/1/2/3)
  - Docstring: Volledig gedocumenteerd met usage voorbeelden
- **README-runner.md**: Korte usage guide voor de runner

**Deliverable bestanden**: 
- `scripts/{agent-naam}-{intent}.runner.py`
- `scripts/README-{agent-naam}-{intent}.runner.md`

**Outputformaat** (Python script structuur):
```python
#!/usr/bin/env python3
"""
{agent-naam}-{intent}.runner.py - {Beschrijving uit contract}

Runner voor agent {agent-naam}, intent {intent}.
Voert run_prompt.py aan met voorgedefinieerde parameters.

Usage:
    python {runner}.py --{param1} VALUE [OPTIONS]
"""

# Configuration (INGEVULD)
RUNNER_NAME = "{agent}-{intent}"
AGENT_NAME = "{agent}"
INTENT_NAME = "{intent}"
VALUE_STREAM_FASE = "{vs}.{fase}"
PROMPT_FILE = "artefacten/{vs}/{vs}.{fase}.{agent}/mandarin.{agent}.{intent}.prompt.md"

# ... [parse_arguments met agent-specifieke params]
# ... [validate_inputs met contract-validaties]
# ... [build_run_prompt_params met parameter mapping]
# ... [run_agent, log_execution, main]
```

**Formaat-normering**: 
- Python (.py) met PEP 8 formatting
- Type hints volgens PEP 484
- Docstrings volgens PEP 257
- Shebang `#!/usr/bin/env python3`

### Foutafhandeling

De Agent Smeder:
- stopt wanneer agent_contract_file niet bestaat of niet te lezen is;
- stopt wanneer agent_contract geen Input sectie bevat (geen parameters → geen runner nodig?);
- vraagt om verduidelijking wanneer parameter-types onduidelijk zijn (agent-contract moet expliciet zijn);
- escaleert naar engineer-steward voor complexe validatie-logica die buiten runner-scope valt;
- stopt wanneer scripts/ folder niet bestaat (moet eerst worden aangemaakt);
- vraagt bevestiging wanneer een runner al bestaat zonder versioning-instructie.

Runner is een VOORBEREIDER, niet de agent zelf. LLM voert instructies uit, runner bereidt voor.

## Werkwijze

### Stappen
1. **Lees boundary**: Extraheer agent_naam, value_stream_fase uit header
2. **Lees agent-contract**: Extraheer intent uit metadata of bestandsnaam, plus Input sectie (verplichte + optionele parameters)
3. **Lees skeleton**: Gebruik agent-runner.skeleton.py als basis
4. **Vul Configuration** (regel 33-45):
   - RUNNER_NAME = "{agent}-{intent}"
   - AGENT_NAME = "{agent}"
   - INTENT_NAME = "{intent}"
   - VALUE_STREAM_FASE = "{vs}.{fase}"
   - PROMPT_FILE = "artefacten/{vs}/{vs}.{fase}.{agent}/prompts/mandarin.{agent}.{intent}.prompt.md"
5. **Vul parse_arguments** (regel 56-122):
   - Voor elke verplichte parameter: `parser.add_argument('--{param}', type={type}, required=True, help="{help}")`
   - Voor elke optionele parameter: `parser.add_argument('--{param}', type={type}, required=False, help="{help}")`
6. **Vul validate_inputs** (regel 128-175):
   - Voor elke verplichte parameter: `if not args.{param}: errors.append("...")`
   - Voor formaat-validaties uit contract: `if not validate_{format}(args.{param}): errors.append("...")`
   - Voor business rules uit contract: custom validatie-code
7. **Vul build_run_prompt_params** (regel 181-218):
   - Voor elke parameter: `params.extend(['-p', '{key}={args.param}'])`
8. **Update docstring**: Vul runner-beschrijving, usage voorbeelden
9. **Schrijf README**: Korte usage guide met voorbeelden
10. **Valideer syntax**: Run `python -m py_compile {runner}.py`
11. **Test run**: `python {runner}.py --help` moet werken

### Kwaliteitsborging
- Python syntax valide (py_compile check)
- Alle parameters uit contract gemapt naar CLI arguments
- Validaties aanwezig voor verplichte parameters
- Docstring compleet met usage voorbeelden
- Type hints overal aanwezig
- Exit codes correct toegepast (0/1/2/3)
- README-runner.md met concrete voorbeelden

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 4 (Scheiding van Wat en Hoe): Runner is HOE (uitvoering), agent-contract is WAT
  - Principe 7 (Transparante Verantwoording): Audit logging ingebouwd
  
**Code kwaliteit** (engineer-steward standaard):
- PEP 8 style guide
- PEP 484 type hints
- PEP 257 docstrings
- Expliciete foutafhandeling
- Input Quality Gate pattern

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aeo
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: agent_contract_file, skeleton_file, charter_file (indien van toepassing)
- ✓ Aangemaakte bestanden: {agent}-{intent}.runner.py, README-{agent}-{intent}.runner.md
- ✓ Geen gewijzigde bestanden (runner is nieuw, of wordt geversioned)

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → engineer-steward: voor complexe validatie-logica, Python-specifieke vragen, code review
- → agent-curator: NIET (runner is technisch, geen boundary-kwestie)
- STOP: bij ontbrekende agent_contract, bij onduidelijke parameter-types, bij ontbrekende scripts/ folder

---

## Metadata

**Intent-ID**: `aeo.02.agent-smeder.leg-vast-agent-runner`  
**Versie**: 1.0.0  
**Value Stream**: Agent Enablement Orchestration (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**: 
- Inhoudelijk: ecosysteem-normerend, structuurrealiserend
- Inzet: value-stream-specifiek
- Vorm: vormvast
- Werking: inhoudelijk
