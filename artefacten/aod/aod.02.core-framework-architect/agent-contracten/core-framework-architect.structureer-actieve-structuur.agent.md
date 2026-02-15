# Core-framework-architect — Structureer Actieve Structuur

## Rolbeschrijving (korte samenvatting)

De Core-framework-architect structureert de actieve structuur (active structure) van een landschap door ArchiMate active elementen (business actors/roles, applicatie components, technology nodes) per laag vast te leggen met hun hiërarchie, dependencies en relaties voor een specifiek domein of value stream.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `core-framework-architect.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- landschap_naam: Naam van het te modelleren landschap (type: string, 2-50 karakters, bijv. "Transport Logistiek", "Financiële Administratie").
- domein: Domein of value stream waarvoor het landschap wordt gemodelleerd (type: string, bijv. "transport", "finance", "hr").
- value_stream_fase: Value stream en fase-aanduiding (type: string, format: "{vs}.{fase}", bijv. "aod.02").
- lagen: Lijst van ArchiMate lagen die gemodelleerd moeten worden (type: list[string], mogelijke waarden: "Business", "Application", "Technology").

**Optionele parameters**:
- bestaande_structuur_file: Pad naar eerder gedefinieerde structuur voor evolutie (type: string, .md bestand).
- scope_constraints: Specifieke beperkingen op scope (type: string, max 200 karakters).
- domein_specifieke_actors: Lijst van bekende actors/componenten in het domein (type: list[string], voor context).

### Output (wat komt eruit)

De Core-framework-architect levert:
- **ArchiMate Actieve Structuur Document** (`.md`): Volledige active structure definitie met:
  - **Business Layer Active Structure**: Business Actors, Roles, Collaborations
  - **Application Layer Active Structure**: Application Components, Collaborations
  - **Technology Layer Active Structure**: Nodes, Devices, System Software (indien van toepassing)
  - **Hiërarchische relaties** (Composition & Aggregation binnen en tussen lagen)
  - **Lagen-overschrijdende relaties** (Assignment, Realization, Serving)
  - **Dependencies & Communicatiepatronen** (welke componenten zijn afhankelijk van elkaar)
  - **Architectuurbeslissingen (ADRs)** over structuurkeuzes, componentengrenzen
  - **Validatie checklist**
- Korte toelichting op structuurpatronen, componentengrenzen en rationale

**Deliverable bestand**: `artefacten/{vs}/{vs}.{fase}.core-framework-architect/landschappen/{domein}/core-framework-architect.structureer-actieve-structuur.md`

**Outputformaat** (standaard structuur per template):
```markdown
# {landschap_naam} — Actieve Structuur Definitie

## ArchiMate Active Structure Elementen

### Business Layer Active Structure
| Element ID | Type | Naam | Rol/Verantwoordelijkheid | Boundary |

### Application Layer Active Structure
| Element ID | Type | Naam | Capability | Interfaces |

### Technology Layer Active Structure (indien van toepassing)
| Element ID | Type | Naam | Hosting Capability | Communicatie |

## Hiërarchische Relaties (Composition & Aggregation)
## Lagen-overschrijdende Relaties
## Dependencies & Communicatie
## Architectuurbeslissingen (ADRs)
## Validatie Checklist
```

**Formaat-normering**: 
- Default formaat: **Markdown** (.md), conform Principe 9
- ArchiMate elementen in tabelformaat voor leesbaarheid
- Element IDs volgen conventie: {laag_prefix}.{type_prefix}.{volgnummer} (bijv. "APP.COMP.001")
- Domein-specifieke namen voor actors/componenten (bijv. "Chauffeur", "Planning Systeem")

### Foutafhandeling

De Core-framework-architect:
- stopt wanneer landschap_naam, domein, value_stream_fase of lagen ontbreken;
- stopt wanneer lagen leeg zijn of ongeldige laagnamen bevatten (niet Business/Application/Technology);
- stopt wanneer bestaande_structuur_file is opgegeven maar bestand niet bestaat;
- vraagt om verduidelijking wanneer scope_constraints te vaag of tegenstrijdig zijn;
- escaleert naar capability-architect voor boundary-verificatie wanneer individuele agents worden gemodelleerd;
- escaleert naar agent-curator wanneer inconsistenties in landschapstructuur worden gedetecteerd;
- escaleert naar constitutioneel-auteur voor interpretatie van strategische kaders bij structuurvragen (indien relevant).

Actieve structuur bevat GEEN implementatie-details (code, deployment scripts), alleen ArchiMate active structure modeling.

**Conventie**: Elk active element heeft een unieke ID binnen het document voor traceerbaarheid. Domein-specifieke naamgeving is verplicht.

## Werkwijze

### Stappen
1. **Valideer input**: Check verplichte parameters, lagenlijst en domein
2. **Lees bestaande structuur**: Indien evolutie, lees bestaande active structure definitie
3. **Analyseer domein**: Bepaal welke actors, componenten en nodes relevant zijn voor dit specifieke domein
4. **Per laag - structureer active elementen**:
   - Business layer: Actors (bijv. Chauffeur, Planner), roles, collaborations
   - Application layer: Components met domein-specifieke namen (bijv. Planning Systeem, Transport Management)
   - Technology layer: Indien van toepassing, nodes en devices
5. **Structureer compositie-relaties**: Welke elementen zijn samengesteld uit andere elementen (hiërarchie)
6. **Structureer aggregatie-relaties**: Welke elementen worden gegroepeerd (logische sets)
7. **Structureer assignment-relaties**: Welke active elementen realiseren welk gedrag (cross-reference naar behavior)
8. **Structureer realization-relaties**: Welke components realiseren welke services
9. **Structureer serving-relaties**: Welke lower layer elementen serven higher layer elementen (bijv. Application serveert Business)
10. **Structureer dependencies**: Welke componenten zijn afhankelijk van andere componenten (koppeling, integratie)
11. **Documenteer ADRs**: Belangrijke beslissingen over componentengrenzen, layering, dependencies
12. **Vul validatie checklist**: Controleer compleetheid van relaties en domein-specifieke naamgeving
13. **Schrijf bestand weg**: Naar afgesproken locatie met versie-metadata

### Kwaliteitsborging
- Elk active element heeft minimaal één relatie (composition, serving, assignment of dependency)
- ADRs zijn aanwezig voor niet-triviale structuurkeuzes (componentengrenzen, layering-beslissingen)
- Element IDs zijn uniek en volgen naamgevingsconventie
- Validatie checklist is volledig ingevuld
- Domein-specifieke naamgeving is consistent toegepast (geen generieke namen zoals "Component 1")
- Business actors reflecteren domeinspecifieke rollen (bijv. Chauffeur, Planner, niet "Gebruiker A")

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Structuurdefinitie is extern observeerbaar (ArchiMate modeling)
  - Principe 2 (Eenduidige Verantwoordelijkheid): Focus op active structure, niet op behavior/passive
  - Principe 5 (Evolutionaire Integriteit): Versioning ingebouwd via metadata header
  - Principe 7 (Transparante Verantwoording): ADRs documenteren structuurbeslissingen
  - Principe 9 (Output-formaat Normering): Markdown als default
- **ArchiMate 3.1 Specification**: Volgt ArchiMate active structure metamodel voor layering en relaties

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aod
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: bestaande_structuur_file (indien evolutie)
- ✓ Aangemaakte bestanden: core-framework-architect.structureer-actieve-structuur.md
- ✓ Geen gewijzigde bestanden (structuurdefinitie is nieuw, of wordt geversioned)

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → capability-architect: voor boundary-verificatie wanneer individuele agents worden gemodelleerd
- → agent-curator: voor inconsistenties in landschapstructuur of overlap-detectie
- → constitutioneel-auteur: voor interpretatie van strategische kaders bij structuurvragen (indien relevant)
- STOP: bij ontbrekende verplichte parameters, bij ongeldige laagnamen

---

## Metadata

**Intent-ID**: `aod.02.core-framework-architect.structureer-actieve-structuur`  
**Versie**: 1.2.0  
**Value Stream**: Agent Ontwerp & Doorontwikkeling (aod)  
**Fase**: 02 — Architectuurkadering  
**Classificatie**: 
- Inhoudelijk: structuurrealiserend
- Inzet: value-stream-specifiek
- Vorm: vormvast
- Werking: inhoudelijk

## Change Log

| Datum | Versie | Wijziging | Auteur |
|-------|--------|-----------|--------|
| 2026-02-15 | 1.2.0 | Intent-werkwoord gewijzigd van 'definieer' naar 'structureer' (beter passend bij structuurrealiserend). | agent-smeder |
| 2026-02-15 | 1.1.0 | Scope aangepast naar landschap-architectuur (business/applicatie/data/technologie i.p.v. agent-ecosysteem). Parameter ecosysteem_naam → landschap_naam + domein. Agent-mapping verwijderd, focus op domein-specifieke actors/componenten. | agent-smeder |
| 2026-02-15 | 1.0.0 | Initieel contract voor agent-ecosysteem modeling | agent-smeder |
