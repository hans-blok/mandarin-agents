---
agent: ecosysteem-coordinator
intent: valideer-agent-structuur
versie: 1.0.0
---

# Ecosysteem-coordinator — Valideer Agent Structuur

## Rolbeschrijving (korte samenvatting)

Controleert of agent-folders in de workspace voldoen aan de doctrine-voorgeschreven structuur (naamgeving, verplichte bestanden, folder-indeling), zonder inhoudelijke beoordeling van de agents zelf.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `ecosysteem-coordinator.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- Geen verplichte parameters; valideert alle agents in workspace

**Optionele parameters**:
- agent_naam: Valideer alleen specifieke agent (type: string, kebab-case).
- value_stream_fase: Filter op value stream fase (type: string, bijv. "aeo.02").
- strict: Faal bij elke warning (type: boolean, default: false).
- output_format: Rapportage formaat (type: string, choices: console|markdown|json, default: console).

### Output (wat komt eruit)

De ecosysteem-coordinator levert:
- **Validatierapport**: Overzicht van alle agents met compliance status
  - Per agent: folder-locatie, gevonden bestanden, ontbrekende bestanden
  - Samenvatting: totaal, passed, failed, warnings
- **Exit code**: 0 bij succes, 1 bij failures (in strict mode ook bij warnings)

**Deliverable bestand**: 
- Console output (default)
- Of: `audit/agent-structuur-validatie-{timestamp}.md` (bij markdown format)

**Outputformaat** (console):
```
Agent Structuur Validatie
=========================

[✓] aeo.02.agent-curator
    ├── agent-curator.charter.md
    ├── agent-curator.agent-boundary.md
    ├── agent-contracten/ (4 contracts)
    ├── prompts/ (4 prompts)
    ├── runners/ (1 runner)
    └── tasks/ (1 task file)

[✗] aeo.02.hypothese-vormer
    ├── hypothese-vormer.charter.md
    ├── [MISSING] hypothese-vormer.agent-boundary.md
    └── runners/ (1 runner)

Samenvatting: 10 agents, 9 passed, 1 failed
```

**Formaat-normering**: 
- Markdown of console text
- Emoji indicators voor status

### Foutafhandeling

De ecosysteem-coordinator:
- rapporteert missing maar stopt niet (tenzij strict mode);
- stopt wanneer artefacten/ folder niet bestaat;
- waarschuwt bij onbekende folder-structuur (niet-standaard indeling);
- escaleert NIET (alleen rapportage, geen correctie).

---

## Werkwijze

### Stappen
1. **Scan artefacten/**: Vind alle agent folders (pattern: {vs}.{fase}.{agent})
2. **Filter indien opgegeven**: Pas agent_naam of value_stream_fase filter toe
3. **Check verplichte bestanden**: 
   - {agent}.charter.md
   - {agent}.agent-boundary.md
4. **Check standaard folders**:
   - agent-contracten/ (min 1 .agent.md)
   - prompts/ (min 1 .prompt.md)
   - runners/ (exact 1 .runner.py)
   - tasks/ (min 1 .tasks.json)
5. **Check naamgeving**: Kebab-case, geen spaties, lowercase
6. **Aggregeer resultaten**: Bouw rapport met status per agent
7. **Output rapport**: Console, markdown of JSON
8. **Bepaal exit code**: 0 als alle checks passed (of warnings in non-strict)

### Kwaliteitsborging
- Alle agents worden gerapporteerd, ook volledig compliant
- Missing items worden expliciet benoemd met verwacht pad
- Rapport is machine-parseable in JSON mode

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 3 (Decentrale en Strict Gescheiden Bestandslocatie): Valideert folder-structuur
  - Principe 7 (Transparante Verantwoording): Rapporteert volledig en transparant

**Canon-consultatie:**
- Raadpleegt doctrine voor verwachte folder-structuur
- Valideert tegen `doctrine-agent-runner-architectuur.md` (Principe 3: locatie-conventie)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Aantal gescande agent folders
- ✓ Per agent: compliance status en details
- ✓ Totaal passed/failed/warnings

Logging-formaat: Console of markdown rapport

**Escalatie-paden:**
- → agent-engineer: voor scaffolding van ontbrekende bestanden (optioneel advies)
- → capability-architect: voor ontbrekende boundary-definities (optioneel advies)
- Geen automatische escalatie; alleen rapportage

---

## Metadata

**Intent-ID**: `aeo.02.ecosysteem-coordinator.valideer-agent-structuur`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**: Conditioneel / Input-gebonden
