---
agent: core-framework-architect
intent: structureer-gedrag
versie: 1.0.0
digest: 976b
status: vers
---
# Core-framework-architect — Structureer Gedrag

## Rolbeschrijving (korte samenvatting)

De Core-framework-architect structureert de gedragslaag (behavior layer) van een landschap door ArchiMate behavior-elementen (business processen, applicatie functies, technology processen) per laag vast te leggen met hun flow-, trigger- en serving-relaties voor een specifiek domein of value stream.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `core-framework-architect.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- archimate_laag: Te modelleren ArchiMate-laag (type: string, mogelijke waarden: "Business", "Application", "Technology").
- bestand: Pad naar het bronbestand dat als input dient voor modellering (type: string, .md bestand).

### Output (wat komt eruit)

De Core-framework-architect levert:
- **ArchiMate Gedragslaag Document** (`.md`): Volledige behavior layer definitie met:
  - **Business Layer Behavior**: Business Processes, Functions, Interactions, Events
  - **Application Layer Behavior**: Application Processes, Functions, Interactions, Events
  - **Technology Layer Behavior**: Technology Processes, Functions (indien van toepassing)
  - **Flow-relaties** tussen behavior elementen (welk gedrag vloeit naar welk gedrag)
  - **Triggering-relaties** (welke events of processen triggeren ander gedrag)
  - **Serving-relaties** (welk gedrag ondersteunt welke active elementen)
  - **Koppeling naar Active Structuur** (assignment relations: welke actors/components realiseren welk gedrag)
  - **Koppeling naar Passive Structuur** (access relations: welk gedrag gebruikt/produceert welke data)
  - **Architectuurbeslissingen (ADRs)** over gedragskeuzes en flows
  - **Validatie checklist**
- Korte toelichting op gedragspatronen, flows en rationale

**Deliverable bestand**: `artefacten/{vs}/{vs}.{fase}.core-framework-architect/landschappen/{domein}/core-framework-architect.structureer-gedrag.md`

**Outputformaat** (standaard structuur per template):
```markdown
# {landschap_naam} — Gedragslaag Definitie

## ArchiMate Behavior Elementen

### Business Layer Behavior
| Element ID | Type | Naam | Beschrijving | Getriggerd door |

### Application Layer Behavior
| Element ID | Type | Naam | Beschrijving | Gebruikt door |

### Technology Layer Behavior (indien van toepassing)
| Element ID | Type | Naam | Beschrijving | Ondersteunt |

## Relaties tussen Behavior Elementen
### Flow Relaties
### Triggering Relaties
### Serving Relaties

## Koppeling naar Active Structuur
## Koppeling naar Passive Structuur
## Architectuurbeslissingen (ADRs)
## Validatie Checklist
```

**Formaat-normering**: 
- Default formaat: **Markdown** (.md), conform Principe 9
- ArchiMate elementen in tabelformaat voor leesbaarheid
- Element IDs volgen conventie: {laag_prefix}.{type_prefix}.{volgnummer} (bijv. "BUS.PROC.001")

### Foutafhandeling

De Core-framework-architect:
- stopt wanneer archimate_laag of bestand ontbreekt;
- stopt wanneer archimate_laag ongeldig is (niet Business/Application/Technology);
- stopt wanneer bestand niet bestaat of niet leesbaar is;
- vraagt om verduidelijking wanneer het bronbestand onvoldoende context bevat;
- escaleert naar constitutioneel-auteur voor interpretatie van strategische kaders (indien relevant);
- escaleert naar capability-architect voor boundary-vragen van individuele agents (indien agents in landschap);
- escaleert naar agent-curator wanneer inconsistenties in landschapstructuur worden gedetecteerd.

Gedragsdefinitie bevat GEEN implementatie-details (code, technische configuratie), alleen ArchiMate behavior modeling.

**Conventie**: Elk behavior element heeft een unieke ID binnen het document voor traceerbaarheid.

## Werkwijze

### Stappen
1. **Valideer input**: Check verplichte parameters en geldigheid van `archimate_laag`
2. **Lees bronbestand**: Lees `bestand` en bepaal relevante context voor gedragsmodellering
3. **Per laag - structureer behavior elementen**: 
   - Business layer: Processen, functies, events relevant voor domein/landschap
   - Application layer: Application processes en functions
   - Technology layer: Indien van toepassing, technology processes
4. **Structureer flow-relaties**: Welk gedrag vloeit naar welk ander gedrag (sequencing)
5. **Structureer triggering-relaties**: Welke events of processen triggeren ander gedrag
6. **Structureer serving-relaties**: Welk gedrag ondersteunt welke active elementen
7. **Koppel naar active structuur**: Assignment relaties (welke actor/component realiseert welk gedrag)
8. **Koppel naar passive structuur**: Access relaties (welk gedrag gebruikt welke data/objecten)
9. **Documenteer ADRs**: Belangrijke beslissingen over gedragspatronen, flows en interacties
10. **Vul validatie checklist**: Controleer compleetheid van relaties en flows
11. **Schrijf bestand weg**: Naar afgesproken locatie met versie-metadata

### Kwaliteitsborging
- Elk behavior element heeft minimaal één relatie (flow, triggering, serving of assignment)
- Alle behavior elementen hebben een assignment naar een active element (gerealiseerd door actor/component)
- ADRs zijn aanwezig voor niet-triviale gedragskeuzes (complexe flows, trigger-patronen)
- Element IDs zijn uniek en volgen naamgevingsconventie
- Validatie checklist is volledig ingevuld
- Business processen reflecteren domeinspecifieke werkwijzen, niet generieke patronen

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Gedragsdefinitie is extern observeerbaar (ArchiMate modeling)
  - Principe 2 (Eenduidige Verantwoordelijkheid): Focus op behavior layer, niet op active/passive structuur
  - Principe 5 (Evolutionaire Integriteit): Versioning ingebouwd via metadata header
  - Principe 7 (Transparante Verantwoording): ADRs documenteren gedragsbeslissingen
  - Principe 9 (Output-formaat Normering): Markdown als default
- **ArchiMate 3.1 Specification**: Volgt ArchiMate behavior metamodel voor layering en relaties

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aod
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: bestand
- ✓ Aangemaakte bestanden: core-framework-architect.structureer-gedrag.md
- ✓ Geen gewijzigde bestanden (gedragsdefinitie is nieuw, of wordt geversioned)

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → constitutioneel-auteur: voor interpretatie van strategische kaders (indien relevant, maar niet leidend voor structuur)
- → capability-architect: voor boundary-vragen van individuele agents binnen behavior context
- → agent-curator: voor landschap-inconsistenties of overlap-detectie
- STOP: bij ontbrekende verplichte parameters, bij ongeldige laagnamen

---

## Metadata

**Intent-ID**: `aod.02.core-framework-architect.structureer-gedrag`  
**Versie**: 1.3.0  
**Value Stream**: Agent Ontwerp & Doorontwikkeling (aod)  
**Fase**: 02 — Architectuurkadering  
**Classificatie**: 
- Betekeniseffect: Realiserend
- Interventieniveau: Werk
- Werking: Inhoudelijk
- Bron-houding: Canon-gebonden

## Change Log

| Datum | Versie | Wijziging | Auteur |
|-------|--------|-----------|--------|
| 2026-02-21 | 1.3.0 | Inputcontract vereenvoudigd naar exact twee verplichte parameters: `archimate_laag` en `bestand`. | agent-smeder |
| 2026-02-15 | 1.2.0 | Intent-werkwoord gewijzigd van 'definieer' naar 'structureer' (beter passend bij structuurrealiserend). | agent-smeder |
| 2026-02-15 | 1.1.0 | Scope aangepast naar landschap-architectuur (business/applicatie/data/technologie i.p.v. agent-ecosysteem). Parameter ecosysteem_naam → landschap_naam + domein. | agent-smeder |
| 2026-02-15 | 1.0.0 | Initieel contract voor agent-ecosysteem modeling | agent-smeder |
