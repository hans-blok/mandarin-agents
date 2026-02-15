---
agent: capability-architect
intent: definieer-agent-boundary
versie: 1.0.0
---

# Capability-architect — Definieer Agent Boundary

## Rolbeschrijving (korte samenvatting)

De Capability-architect definieert de servicegrens van een agent als duurzame, expliciet aanroepbare capability binnen het ecosysteem. Dit contract beschrijft de externe verantwoordelijkheid van de agent in één scherpe zin, zonder te valideren of te beoordelen.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `capability-architect.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- agent_naam: Naam van de agent waarvoor de boundary wordt gedefinieerd (type: string, kebab-case).
- value_stream_fase: Value stream en fase code (type: string, format: "{vs}.{fase}", bijv. "aeo.02", "fnd.01").
- korte_beschrijving: Korte beschrijving van het doel van de agent (type: string, 1-3 zinnen).


### Output (wat komt eruit)

De Capability-architect levert:
- **Agent-boundary document** met:
  - Externe verantwoordelijkheid in één scherpe zin
  - Expliciete capability boundary (wat wél en níet)
  - Domein en value stream positionering
  - Voorstellen voor intents (prompts)
  - Mogelijke raakvlakken (ter informatie, geen validatie)
- Korte toelichting op gemaakte definitiekeuzes

**Deliverable bestand**: `artefacten/{vs}/{vs}.{fase}.{agent}/agent-boundary-{agent}.md`

**VERPLICHT**: Het bestand MOET worden weggeschreven naar de workspace (niet alleen voorgesteld).

**Bestandsformaat vereisten**:
1. **Moet YAML frontmatter bevatten**: agent, value_stream, value_stream_fase, versie
2. **value_stream en value_stream_fase**: Gebruik de waarden uit de INPUT parameter `value_stream_fase`, NIET van de executor agent
3. **Moet template volgen**: Gebruik `agent-boundary.template.md` (beschikbaar als [TEMPLATE] placeholder)
4. **Classificatie checkboxes**: Gebruik checkbox syntax `- [ ]` en `- [x]` uit template
5. **Intent naming**: Alle voorgestelde intents MOETEN starten met canoniek werkwoord uit `doctrine-intent-naming.md` (meestal "definieer" voor structurerende definitie)

**Outputformaat** (volgens [TEMPLATE] placeholder):
```markdown
---
agent: {agent_naam}
value_stream: {vs}
value_stream_fase: {vs}.{fase}
versie: 1.0.0
---

# Agent Boundary: {Agent-naam}

**agent-naam**: {agent-naam}
**capability-boundary**: {één zin}
**doel**: {één zin}
**domein**: {domein}

---

## Classificatie van de agent
(vink aan wat van toepassing is)

- **Inhoudelijke as**
  - [ ] Ecosysteem-normerend
  - [ ] Structuur-normerend
  - [ ] Structuurrealiserend
  - [ ] Beschrijvend
  - [ ] Curator

[...etc volgens template...]

## Voorstellen agent contracten (intents)

- definieer-{intent-1}
- definieer-{intent-2}
- definieer-{intent-3}

[...rest volgens template...]
```

**Formaat-normering**: 
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek
- Markdown bevat structuur volgens agent-boundary.template.md
- Template wordt automatisch geladen en beschikbaar gemaakt als [TEMPLATE] placeholder

### Foutafhandeling

De Capability-architect:
- stopt wanneer agent_naam, value_stream_fase of korte_beschrijving ontbreekt;
- stopt wanneer agent_naam niet voldoet aan naamgevingsconventies (kebab-case);
- stopt wanneer value_stream_fase niet voldoet aan format "{vs}.{fase}" (bijv. "aeo.02");
- vraagt om verduidelijking wanneer korte_beschrijving te vaag of te breed is (>3 zinnen);
- escaleert naar agent-curator voor ecosysteem-analyse bij onduidelijke positionering;
- escaleert naar agent-smeder NIET (dit is definitie, geen realisatie van artefacten);
- STOP: bij onvoldoende informatie om scherpe boundary te formuleren.

**Let op**: De Capability-architect identificeert mogelijke raakvlakken maar valideert of beoordeelt deze NIET. Validatie is verantwoordelijkheid van Agent Curator.

---

## Werkwijze

### Stappen
1. **Analyseer input**: Begrijp korte_beschrijving en domein, extraheer vs en fase uit value_stream_fase PARAMETER (niet van executor agent)
2. **Laad template**: Gebruik [TEMPLATE] placeholder voor agent-boundary.template.md structuur
3. **Raadpleeg doctrine**: Check doctrine-intent-naming.md voor canonieke werkwoorden (meestal "definieer")
4. **Definieer verantwoordelijkheid**: Formuleer externe verantwoordelijkheid in één zin
5. **Bepaal boundary**: Expliciteer wat wél en níet binnen scope valt (minimaal 3 bullets per sectie)
6. **Classificeer agent**: Vink correcte checkboxes aan volgens template
7. **Identificeer raakvlakken**: Lijst agents met mogelijke overlap (ter informatie, geen validatie)
8. **Positioneer in ecosysteem**: Valideer consistentie van value_stream_fase met classificatie
9. **Stel intents voor**: Voorlopige lijst van 1-3 intents, elk startend met canoniek werkwoord
10. **Schrijf boundary document**: 
    - Gebruik YAML frontmatter met value_stream en value_stream_fase uit INPUT parameter
    - Volg template-structuur volledig (inclusief checkboxes)
    - Schrijf weg naar artefacten/{vs}/{vs}.{fase}.{agent}/agent-boundary-{agent}.md
11. **Valideer compleetheid**: Check template-checklist en kwaliteitsborging

### Kwaliteitsborging
- **YAML frontmatter correct**: agent, value_stream (uit parameter!), value_stream_fase (uit parameter!), versie
- **Capability-boundary** is exact één zin
- **WEL/NIET secties** bevatten minimaal 3 bullets elk
- **Voorgestelde intents** zijn concreet, actionable, en starten met canoniek werkwoord uit doctrine-intent-naming.md
- **Template volledig gevolgd**: Alle secties uit agent-boundary.template.md aanwezig, inclusief checkboxes
- **Classificatie checkboxes** correct aangevinkt met `- [x]` syntax
- **Mogelijke raakvlakken** geïdentificeerd (zonder validatie)
- **Bestand weggeschreven** naar correct pad: artefacten/{vs}/{vs}.{fase}.{agent}/agent-boundary-{agent}.md

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Boundary definieert externe kenmerken
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén capability per agent
  - Principe 7 (Transparante Verantwoording): Definitiekeuzes gedocumenteerd
  - Principe 9 (Output-formaat Normering): Markdown als default
- **doctrine-werkwoorden-intents.md**: Werkwoord "definieer" voor structurerende definitie

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aeo
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: korte_beschrijving (als parameter), referentie_agents (indien opgegeven)
- ✓ Aangemaakte bestanden: agent-boundary-{agent}.md
- ✓ Geen gewijzigde bestanden (boundary is nieuw, of wordt geversioned)
- ✓ Geïdentificeerde raakvlakken (zonder validatie-conclusie)

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → agent-curator: voor ecosysteem-analyse of validatie van overlap
- → constitutioneel-auteur: voor doctrine-interpretatie bij classificatie
- STOP: bij te vage korte_beschrijving die niet te scherpstellen is, bij ontbrekende basale informatie

---

## Metadata

**Intent-ID**: `aeo.02.capability-architect.definieer-agent-boundary`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**: 
- Inhoudelijk: structurerend + ecosysteem-normerend
- Inzet: value-stream-overstijgend
- Vorm: vormvast
- Werking: inhoudelijk
