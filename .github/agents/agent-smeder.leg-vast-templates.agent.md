# Agent Smeder — Leg Templates Vast Voor Agent

## Rolbeschrijving (korte samenvatting)

De Agent Smeder creëert alle benodigde templates (prompt, agent-contract, charter, runner) voor een nieuwe agent op basis van de boundary en voorgestelde intents, zonder de templates zelf al in te vullen.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `{agent-naam}.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- agent_naam: Naam van de nieuwe agent (type: string, kebab-case, bijv. "hypothese-vormer").
- boundary_file: Pad naar het boundary-bestand van de agent (type: string, relatief pad, bijv. "artefacten/sfw/sfw.01.hypothese-vormer/hypothese-vormer.boundary.md").

**Optionele parameters**:
- intents: Komma-gescheiden lijst van intent-namen indien afwijkend van boundary (type: string, bijv. "formuleer,toets,vergelijk").

### Output (wat komt eruit)

De Agent Smeder levert:
- **Template-set per intent**: Voor elke intent in de boundary:
  - Prompt template: `{agent-naam}.{intent}.prompt.md` (YAML frontmatter met placeholders)
  - Agent-contract template: `{agent-naam}.{intent}.agent.md` (contract beschrijving met placeholders)
- **Charter template**: `{agent-naam}.charter.md` (charter structuur met placeholders)
- **Runner skeleton**: `{agent-naam}-{intent}.runner.py` (Python skeleton met placeholders)
- **README**: `README-templates.md` met uitleg over invulling

**Deliverable locatie**: `artefacten/{value_stream}/{value_stream}.{fase}.{agent_naam}/templates/`

**Outputformaat** (folder structuur):
```
artefacten/{vs}/{vs}.{fase}.{agent-naam}/
  templates/
    {agent-naam}.{intent-1}.prompt.md
    {agent-naam}.{intent-1}.agent.md
    {agent-naam}.{intent-1}.runner.py
    {agent-naam}.{intent-2}.prompt.md
    {agent-naam}.{intent-2}.agent.md
    {agent-naam}.{intent-2}.runner.py
    {agent-naam}.charter.md
    README-templates.md
```

**Formaat-normering**: 
- Default formaat: **Markdown** (.md) voor templates, Python (.py) voor runners
- Templates bevatten `{placeholders}` die in volgende stappen worden ingevuld
- Alternatieve formaten alleen op expliciete verzoek
- Conform Principe 9 van doctrine-agent-charter-normering.md

### Foutafhandeling

De Agent Smeder:
- stopt wanneer boundary_file niet bestaat of niet te lezen is;
- stopt wanneer boundary_file geen intents bevat (sectie "Voorstellen agent contracten");
- vraagt om verduidelijking wanneer agent_naam niet voldoet aan naamgevingsconventies (kebab-case);
- escaleert naar agent-curator voor boundary-wijzigingen of onduidelijkheden;
- stopt wanneer de doelfolder al templates bevat (risico op overschrijven zonder versioning).

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Templates forceren contract-first approach
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén template-set per intent
  - Principe 5 (Evolutionaire Integriteit): Templates faciliteren versioning
  - Principe 9 (Output-formaat Normering): Markdown templates als default

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aeo
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: boundary_file
- ✓ Aangemaakte bestanden: alle templates en README per intent
- ✓ Geen gewijzigde bestanden (templates zijn nieuw)

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → agent-curator: voor boundary-onduidelijkheden of wijzigingen
- → engineer-steward: voor Python runner skeleton aanpassingen
- STOP: bij bestaande templates folder (zonder expliciete overschrijf-instructie)

---

## Metadata

**Intent-ID**: `aeo.02.agent-smeder.leg-vast-templates`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**: 
- Inhoudelijk: ecosysteem-normerend, structuurrealiserend
- Inzet: value-stream-specifiek
- Vorm: vormvast
- Werking: inhoudelijk
