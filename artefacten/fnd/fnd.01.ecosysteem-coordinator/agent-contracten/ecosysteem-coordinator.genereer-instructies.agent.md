---
agent: ecosysteem-coordinator
intent: genereer-instructies
versie: 1.0.0
---

# Ecosysteem-coordinator — Genereer Instructies

## Rolbeschrijving (korte samenvatting)

Assembleert execution-ready instructiebestanden door canon-context, agent charter, contract en prompt templates samen te voegen tot een volledig uitvoerbaar bestand voor LLM-executie.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `ecosysteem-coordinator.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- agent: Naam van de agent waarvoor instructies worden gegenereerd (type: string, kebab-case).
- intent: Intent naam voor instructie-generatie (type: string, kebab-case).

**Optionele parameters**:
- execution_file: Pad waar execution-bestand wordt geschreven (type: string, default: auto-generated in prompt-instructions/).
- params: Key=value parameters voor placeholder substitutie (type: list[string], format: "key=value").
- skip_bootstrap: Sla canon-consultatie over (type: boolean, default: false, alleen voor development).
- method: Execution method voor audit (type: string, choices: manual|runner|pipeline, default: manual).

### Output (wat komt eruit)

De ecosysteem-coordinator levert:
- **Execution bestand**: Volledig samengesteld instructiebestand met metadata header
  - YAML frontmatter met execution_id, timestamp, agent, intent, canon_ref
  - Canon-context (geraadpleegde grondslagen indien niet skipped)
  - Agent charter content
  - Agent contract content
  - Prompt-specifieke instructies
- **Console output**: Samenvatting en pad naar gegenereerd bestand

**Deliverable bestand**: `prompt-instructions/{timestamp}-{agent}.{intent}.md`

**Outputformaat** (execution bestand):
```markdown
---
execution_id: {4-char-hash}
timestamp: {ISO-8601}
agent: {agent}
intent: {intent}
value_stream_fase: {vs.fase}
canon_ref: {commit-sha}
---

**Voer de volgende instructie uit:**

# Agent Execution: {agent} — {intent}

## Parameters
- {key}: {value}

## Instructies

{charter content}

---

{contract content}

---

{prompt content}
```

**Formaat-normering**: 
- Markdown met YAML frontmatter
- UTF-8 encoding zonder BOM

### Foutafhandeling

De ecosysteem-coordinator:
- stopt wanneer agent niet gevonden wordt in artefacten/ structuur;
- stopt wanneer intent niet gevonden wordt (geen matching prompt of contract);
- stopt wanneer charter ontbreekt voor opgegeven agent;
- vraagt NIET om verduidelijking (auto-discovery based);
- escaleert naar agent-engineer indien prompt-bestand ontbreekt (scaffolding nodig);
- logt warning wanneer contract ontbreekt maar gaat door met alleen charter + prompt.

---

## Werkwijze

### Stappen
1. **Consulteer canon**: Roep `consulteer-canon` intent aan (tenzij skip_bootstrap)
2. **Locate agent artefacten**: Zoek agent folder in artefacten/{vs}/{vs}.{fase}.{agent}/
3. **Load charter**: Lees {agent}.charter.md
4. **Load contract**: Zoek {agent}.{intent}.agent.md in agent-contracten/
5. **Load prompt**: Zoek mandarin.{agent}.{intent}.prompt.md in prompts/
6. **Substitute parameters**: Vervang placeholders met opgegeven params
7. **Assemble execution file**: Combineer alle componenten met metadata header
8. **Write output**: Schrijf naar execution_file pad
9. **Log to audit**: Append naar audit/agent-instructions.log.md

### Kwaliteitsborging
- Execution ID is uniek (timestamp + agent hash)
- Canon reference is altijd aanwezig (of expliciet "skipped")
- Alle gelezen bestanden worden gelogd voor traceerbaarheid

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Assembleert bestaande definities
  - Principe 7 (Transparante Verantwoording): Volledige logging van samenstellingsproces
  - Principe 9 (Output-formaat Normering): Markdown default

**Canon-consultatie:**
- Roept `ecosysteem-coordinator.consulteer-canon` aan als eerste stap
- Canon-context wordt opgenomen in execution bestand

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Alle gelezen bestanden (charter, contract, prompt)
- ✓ Gegenereerd execution bestand (pad en execution_id)
- ✓ Parameters die zijn gesubstitueerd
- ✓ Canon commit reference

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → agent-engineer: indien prompt-bestand ontbreekt (scaffolding vereist)
- → capability-architect: indien charter ontbreekt (boundary niet gedefinieerd)
- STOP: bij agent folder niet gevonden

---

## Metadata

**Intent-ID**: `aeo.02.ecosysteem-coordinator.genereer-instructies`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**: Conditioneel / Input-gebonden
