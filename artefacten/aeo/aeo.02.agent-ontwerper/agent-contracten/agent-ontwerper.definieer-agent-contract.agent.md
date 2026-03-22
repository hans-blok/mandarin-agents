---
agent: agent-ontwerper
intent: definieer-agent-contract
versie: 1.0.0
---

# Agent-ontwerper — Definieer Agent Contract

## Rolbeschrijving (korte samenvatting)

De Agent-ontwerper creëert agent-contract documenten voor elke intent uit de boundary, waarbij het externe contract van de agent functioneel wordt beschreven met input, output, foutafhandeling en governance.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `agent-ontwerper.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- agent_naam: Naam van de agent waarvoor contracten worden gedefinieerd (type: string, kebab-case).

**Optionele parameters**:
- intent_naam: Naam van de specifieke intent waarvoor contract wordt gedefinieerd (type: string, kebab-case, bijv. "definieer-charter", "analyseer-hypothese").
Standaard is dat voor alle intents in "Voorstellen agent contracten" sectie in boundary een template wordt aangemaakt. Wanneer deze parameter is opgegeven, wordt alleen voor deze intent een contract gegenereerd.

- template_file: Override voor agent-contract template locatie (type: string, default: "artefacten/aeo/aeo.02.agent-smeder/templates/agent-contract-intent.template.md").
- referenties: Lijst van referentie-documenten of bestaande contracten als voorbeeld (type: list[string]).

**Afgeleide informatie** (geëxtraheerd uit boundary):
- capability_boundary: Context voor contract-scope
- classificatie: Voor metadata-sectie in contract
- intent_beschrijving: Uit "Voorstellen agent contracten" sectie in boundary
- template_file: vaak is een template aanwezig. dit template wordt gelezen voor het maken van het contract.

### Output (wat komt eruit)

De Agent-ontwerper levert:
- **Agent-contract document** (.agent.md) met volledige contract-beschrijving:
  - YAML frontmatter: agent, intent, versie
  - Rolbeschrijving: Wat doet agent bij deze specifieke intent (1-2 zinnen)
  - Contract sectie:
    - Input (wat gaat erin): Verplichte en optionele parameters met types en constraints
    - Output (wat komt eruit): Deliverables, bestandsformaten, outputlocaties, formaat-normering
    - Foutafhandeling: Stop-condities, escalatiepaden, wat NIET gebeurt
  - Werkwijze (optioneel): Stappen en kwaliteitsborging bij multi-step processes
  - Governance:
    - Doctrine-naleving: Verwijzingen naar relevante principes
    - Canon-consultatie: Bootstrap en logging specificatie
    - Transparantie-verplichtingen: Wat wordt gelogd
    - Escalatie-paden: Naar welke agents bij welke situaties
  - Metadata: Intent-ID, versie, value stream, fase, classificatie
- Korte toelichting op ontwerpkeuzes en parameter-selectie

**Deliverable bestand**: `artefacten/{vs}/{vs}.{fase}.{agent}/agent-contracten/{agent}.{intent}.agent.md`

**VERPLICHT**: Het bestand MOET worden weggeschreven naar de workspace (niet alleen voorgesteld).

**Outputformaat** (volgens agent-contract-intent.template.md):
```markdown
---
agent: {agent-naam}
intent: {intent-naam}
versie: 1.0.0
---

# {Agent-naam} — {Intent Titel}

## Rolbeschrijving (korte samenvatting)
{1-2 zinnen wat agent doet bij deze intent}

**VERPLICHT**: Raadpleeg de agent charter voor volledige context.

## Contract

### Input (wat gaat erin)
**Verplichte parameters**: ...
**Optionele parameters**: ...

### Output (wat komt eruit)
**Deliverable bestand**: ...
**Outputformaat**: ...
**Formaat-normering**: ...

### Foutafhandeling
{Stop-condities en escalaties}

## Werkwijze (optioneel)
### Stappen
### Kwaliteitsborging

## Governance
**Doctrine-naleving**: ...
**Canon-consultatie**: ...
**Transparantie-verplichtingen**: ...
**Escalatie-paden**: ...

## Metadata
**Intent-ID**: {vs}.{fase}.{agent}.{intent}
**Versie**: 1.0.0
**Classificatie**: [uit boundary]
```

**Formaat-normering**: 
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek
- Contract volgt strikte template-structuur uit agent-contract-intent.template.md

### Foutafhandeling

De Agent-ontwerper:
- stopt wanneer boundary_file niet bestaat of niet te lezen is;
- stopt wanneer intent_naam niet voorkomt in "Voorstellen agent contracten" sectie van boundary;
- stopt wanneer agent_naam, intent_naam of value_stream_fase ontbreekt of incorrect format heeft;
- vraagt om verduidelijking wanneer intent-beschrijving in boundary te vaag is om contract te formuleren;
- escaleert naar capability-architect voor boundary-verfijning bij ontbrekende intent-definitie;
- escaleert naar agent-curator voor ecosysteem-analyse als intent overlap heeft met andere agents;
- STOP: bij onvoldoende informatie om volledig contract te genereren met minimaal 2 verplichte parameters en concrete output-specificatie.

**Contract is extern observeerbaar**: bevat GEEN implementatie-details, alleen wat agent ontvangt, levert en wanneer stopt.

---

## Werkwijze

### Stappen
1. **Analyseer boundary**: Lees boundary_file en zoek intent_naam in "Voorstellen agent contracten" sectie.
2. **Raadpleeg template**: Lees agent-contract-intent.template.md voor volledige structuur.
3. **Bepaal parameters**: Afleiden welke input-parameters nodig zijn op basis van intent-beschrijving en domein.
4. **Specificeer output**: Bepaal deliverable bestandslocatie, formaat en structuur.
5. **Formuleer rolbeschrijving**: Schrijf 1-2 zinnen wat agent doet specifiek bij deze intent.
6. **Detail input-contract**: Lijst minimaal 2 verplichte parameters met type, constraints en format.
7. **Detail output-contract**: Specificeer deliverable pad, formaat, structuur (met voorbeeld indien gestructureerd).
8. **Expliciteer foutafhandeling**: Minimaal 3 stop-condities en escalatiepaden naar andere agents.
9. **Bepaal werkwijze**: Alleen toevoegen als proces >3 stappen heeft; anders weglaten.
10. **Documenteer governance**: Doctrine-principes, canon-consultatie, transparantie, escalaties.
11. **Stel metadata samen**: Intent-ID format {vs}.{fase}.{agent}.{intent}, classificatie uit boundary.
12. **Schrijf contract**: Genereer volledig contract-bestand en schrijf weg naar correct pad.
13. **Valideer compleetheid**: Check minimale vereisten (2+ params, concrete output, 3+ stop-condities, doctrine-refs).

### Kwaliteitsborging
- Contract heeft YAML frontmatter met agent, intent, versie
- Rolbeschrijving is 1-2 zinnen, specifiek voor deze intent
- Input heeft minimaal 2 verplichte parameters met type en constraints
- Output specificeert concrete bestandspad volgens workspace-structuur
- Foutafhandeling heeft minimaal 3 stop-condities en duidelijke escalatiepaden
- Governance-sectie verwijst naar relevante doctrine-principes
- Metadata heeft correcte Intent-ID format: {vs}.{fase}.{agent}.{intent}
- Classificatie komt uit boundary en wordt niet gewijzigd
- Bestand weggeschreven naar: artefacten/{vs}/{vs}.{fase}.{agent}/agent-contracten/{agent}.{intent}.agent.md

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar, geen implementatie
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén contract per intent, één verantwoordelijkheid
  - Principe 4 (Scheiding van Wat en Hoe): Contract = wat wordt ontvangen/geleverd, niet hoe geïmplementeerd
  - Principe 5 (Evolutionaire Integriteit): Versioning ingebouwd (start 1.0.0)
  - Principe 7 (Transparante Verantwoording): Transparantie-verplichtingen expliciet in contract
  - Principe 9 (Output-formaat Normering): Markdown als default

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aeo
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: boundary_file, template_file (agent-contract-intent.template.md), referenties (indien opgegeven)
- ✓ Aangemaakte bestanden: {agent}.{intent}.agent.md
- ✓ Geen gewijzigde bestanden (contract is nieuw, of wordt geversioned bij update)
- ✓ Intent-analyse: intent gevonden in boundary, parameters afgeleid, output-locatie bepaald

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → capability-architect: voor boundary-verfijning of onduidelijke intent-definitie
- → agent-curator: voor ecosysteem-validatie als intent overlap heeft met andere agents
- → constitutioneel-auteur: voor doctrine-interpretatie bij contract-design vragen
- STOP: bij ontbrekende intent in boundary, bij te vage intent-omschrijving die niet te vertalen is naar contract

---

## Metadata

**Intent-ID**: `aeo.02.agent-ontwerper.definieer-agent-contract`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**: 
- Betekeniseffect: Normerend
- Interventieniveau: Werk
- Werking: Inhoudelijk
- Bron-houding: Canon-gebonden
