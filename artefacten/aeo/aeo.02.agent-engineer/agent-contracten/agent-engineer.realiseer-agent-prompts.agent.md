# Agent-engineer — Realiseer Agent Prompts

## Rolbeschrijving (korte samenvatting)

De Agent-engineer genereert en actualiseert promptbestanden voor alle intents van een agent, zodat de agent aanroepbaar is via gestandaardiseerde prompt-artefacten.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `agent-engineer.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)
**Verplichte parameters**:
- agent_naam: Naam van de agent waarvoor prompts worden gerealiseerd (type: string, kebab-case format). Agent-contracten worden automatisch gedetecteerd via workspace-structuur.

**Optionele parameters**:
- intent: Specifieke intent waarvoor prompt wordt gerealiseerd (type: string, kebab-case format). Indien niet opgegeven, worden prompts voor alle intents gegenereerd.

### Output (wat komt eruit)

De Agent-engineer levert:
- **Promptbestanden** (`.prompt.md`): Voor elke intent uit de agent-contracten één prompt-artefact met uitsluitend:
  - YAML frontmatter met metadata (agent, intent, versie, input-parameters)
- **Validatierapport**: Overzicht van gerealiseerde prompts met status (nieuw/geactualiseerd/error)

**Deliverable bestanden**: `artefacten/{vs}/{vs}.{fase}.{agent}/prompts/mandarin.{agent}.{intent}.prompt.md` (Markdown met uitsluitend YAML frontmatter)

**Outputformaat** (standaard structuur per prompt):
```markdown
---
agent: {agent-naam}
intent: {intent-kortschrift}
versie: 1.0.0
input_parameters:
  - {parameter-naam}
  - {parameter-naam}
---
```

**Formaat-normering**: 
- Default formaat: **Markdown** (.md), conform Principe 9
- Promptbestanden zijn altijd Markdown (geen alternatief formaat)
- YAML frontmatter is verplicht onderdeel van elke prompt

### Foutafhandeling

De Agent-engineer:
- stopt wanneer geen agent-contracten gevonden of leesbaar zijn;
- stopt wanneer agent_naam niet afgeleid kan worden uit agent-contracten;
- stopt wanneer value_stream_fase niet afgeleid kan worden uit agent-contracten;
- overschrijft bestaande promptbestanden altijd (deterministisch updategedrag);
- escaleert naar agent-smeder voor contract-verfijning bij onduidelijke intentdefinities;
- rapporteert maar stopt NIET bij ontbrekende agent-contract bestanden (prompts kunnen vóór contracten worden gerealiseerd).

Promptbestanden bevatten GEEN implementatie-logica, alleen metadata en verwijzingen naar contract en charter.

---

## Werkwijze

### Stappen (Batch-uitvoering)
1. **Analyseren (Eénmalig)**:
  - Lokaliseer agent-contracten op basis van workspace-conventie en/of parameter `agent_contracts`
  - Extraheer agent_naam, value_stream_fase, en alle intents uit agent-contracten
   - Bepaal doelfolder voor prompts volgens conventie
   - Controleer of doelfolder bestaat (maak aan indien nodig)
2. **Genereren (Intern)**:
   - Stel voor elke intent een prompt-artefact op in geheugen
   - Zorg voor consistente metadata (versie 1.0.0 voor nieuwe, behoud bestaande versie bij actualisatie)
   - Genereer correcte verwijzingen naar contract en charter
3. **Uitvoeren (Batch output)**:
   - Schrijf alle `.prompt.md` bestanden naar doelfolder
   - Genereer validatierapport met overzicht van gerealiseerde prompts

### Kwaliteitsborging
- Elke intent uit gedetecteerde agent-contracten heeft een prompt-bestand
- YAML frontmatter bevat minimaal: agent, intent, versie, input_parameters (indien aanwezig in contract)
- Verwijzingen naar contract en charter zijn correcte relatieve paden
- Bestandsnaamconventie gevolgd: `mandarin.{agent}.{intent}.prompt.md`
- Geen duplicaties van contract-inhoud in prompt (alleen referenties)

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Prompts verwijzen naar contract, geen duplicatie
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén prompt per intent
  - Principe 5 (Evolutionaire Integriteit): Versioning ingebouwd (start bij 1.0.0)
  - Principe 7 (Transparante Verantwoording): Logging van gerealiseerde prompts
  - Principe 9 (Output-formaat Normering): Markdown met YAML frontmatter

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aeo
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: alle gedetecteerde agent-contract bestanden
- ✓ Aangemaakte bestanden: alle nieuwe `.prompt.md` bestanden
- ✓ Gewijzigde bestanden: geactualiseerde `.prompt.md` bestanden

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → agent-smeder: voor contract-verfijning of onduidelijke intent-beschrijving
- → engineer-steward: NIET (dit is realisatie van aanroep-artefacten, geen runner-implementatie)
- STOP: bij ontbrekende/onleesbare agent-contracten, bij ontbrekende intents-sectie

---

## Metadata

**Intent-ID**: `aeo.02.agent-engineer.realiseer-agent-prompts`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**: 
- Betekeniseffect: Realiserend
- Interventieniveau: Werk
- Werking: Inhoudelijk
- Bron-houding: Input-gebonden
