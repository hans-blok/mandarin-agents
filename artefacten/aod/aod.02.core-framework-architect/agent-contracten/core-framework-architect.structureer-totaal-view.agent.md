# Core-framework-architect — Structureer Totaal View

## Rolbeschrijving (korte samenvatting)

De Core-framework-architect structureert en integreert de actieve structuur, passieve structuur en gedragslaag van een landschap in één coherente ArchiMate totaal view, waarbij alle relaties tussen active, passive en behavior elementen expliciet zijn vastgelegd en traceability van business tot technologie is geborgd.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `core-framework-architect.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- landschap_naam: Naam van het te modelleren landschap (type: string, 2-50 karakters, bijv. "Transport Logistiek", "Financiële Administratie").
- domein: Domein of value stream waarvoor het landschap wordt gemodelleerd (type: string, bijv. "transport", "finance", "hr").
- value_stream_fase: Value stream en fase-aanduiding (type: string, format: "{vs}.{fase}", bijv. "aod.02").
- lagen: Lijst van ArchiMate lagen die geïntegreerd moeten worden (type: list[string], mogelijke waarden: "Business", "Application", "Technology").
- active_structuur_file: Pad naar de actieve structuur definitie (type: string, .md bestand, verplicht want basis voor integratie).
- gedrag_file: Pad naar de gedragslaag definitie (type: string, .md bestand, verplicht want basis voor integratie).

**Optionele parameters**:
- bestaande_totaal_view_file: Pad naar eerder gedefinieerde totaal view voor evolutie (type: string, .md bestand).
- layering_principes: Lijst van expliciete layering principes voor het landschap (type: list[string], bijv. ["Lower layers serve higher layers", "No cross-layer dependencies"]).

### Output (wat komt eruit)

De Core-framework-architect levert:
- **ArchiMate Totaal View Document** (`.md`): Integrale landschap-architectuur view met:
  - **Laagstructuur Overzicht** (hiërarchie van Business/Application/Technology layers)
  - **Active Structure per laag** (samenvatting met verwijzing naar detail-document)
  - **Passive Structure per laag** (data objects, business objects, artifacts) - afgeleid uit behavior access-relaties
  - **Behavior per laag** (samenvatting met verwijzing naar detail-document)
  - **Integrale Relatiematrix**:
    - Active → Behavior → Passive (kernpatroon: wie doet wat met welke data)
    - Laag-overschrijdende Serving Relaties (bijv. Application serveert Business)
    - Realization & Composition Hiërarchie
  - **Traceability Matrix**: Business → Application → Data → Technology
  - **Architectuurbeslissingen (ADRs)** over integratiekeuzes, layering, traceability
  - **Consistentie Validatie rapport** (zijn alle relaties compleet en consistent?)
- Korte toelichting op integratiepatronen, cross-layer relaties en traceability

**Deliverable bestand**: `artefacten/{vs}/{vs}.{fase}.core-framework-architect/landschappen/{domein}/core-framework-architect.structureer-totaal-view.md`

**Outputformaat** (standaard structuur per template):
```markdown
# {landschap_naam} — Totaal Architectuur View

## Laagstructuur Overzicht
### Laag Hiërarchie
| Laag Niveau | Laag Naam | Primaire Functie | Serving relaties |

**Layering Principes**: ...

## Active Structure (per laag)
### {Laag_naam} — Active Elementen
*Zie core-framework-architect.structureer-actieve-structuur.md voor details*

## Passive Structure (per laag)
### {Laag_naam} — Passive Elementen
| Element ID | Type | Naam | Inhoud | Gebruikt door (Behavior) |

## Behavior (per laag)
### {Laag_naam} — Behavior Elementen
*Zie core-framework-architect.structureer-gedrag.md voor details*

## Integrale Relatiematrix
### Active → Behavior → Passive (Kernpatroon)
### Laag-overschrijdende Serving Relaties
### Realization & Composition Hiërarchie

## Traceability Matrix
### Business → Application → Data → Technology

## Architectuurbeslissingen (ADRs)
## Consistentie Validatie
```

**Formaat-normering**: 
- Default formaat: **Markdown** (.md), conform Principe 9
- ArchiMate relaties in matrix-formaat voor overzicht
- Element IDs consistent met active_structuur_file en gedrag_file
- Verwijzingen naar detail-documenten voor complete definitie
- Traceability matrix toont end-to-end relaties business tot technologie

### Foutafhandeling

De Core-framework-architect:
- stopt wanneer landschap_naam, domein, value_stream_fase, active_structuur_file of gedrag_file ontbreken;
- stopt wanneer active_structuur_file of gedrag_file niet bestaan of niet leesbaar zijn;
- stopt wanneer lagen leeg zijn of ongeldige laagnamen bevatten (niet Business/Application/Technology);
- stopt wanneer active_structuur_file en gedrag_file inconsistente landschap_naam of lagen bevatten;
- vraagt om verduidelijking wanneer layering_principes tegenstrijdig zijn met bestaande structuur;
- escaleert naar agent-curator wanneer inconsistenties tussen active structure en behavior worden gedetecteerd;
- escaleert naar constitutioneel-auteur voor interpretatie van strategische kaders bij integratievragen (indien relevant);
- escaleert naar capability-architect voor boundary-vragen wanneer individuele agents in landschap worden gemodelleerd.

Totaal view bevat GEEN implementatie-details, alleen ArchiMate integrale modeling met expliciete cross-layer relaties en traceability.

**Conventie**: Totaal view is leidend voor landschap-overzicht; detail-documenten (active structure, behavior) zijn leidend voor element-specifieke definitie.

## Werkwijze

### Stappen
1. **Valideer input**: Check verplichte parameters en bestaan van active_structuur_file en gedrag_file
2. **Lees active structure**: Parse active elementen per laag uit active_structuur_file
3. **Lees behavior**: Parse behavior elementen per laag uit gedrag_file
4. **Cross-validatie**: Check consistentie tussen active en behavior (alle assignments kloppen, geen ontbrekende relaties)
5. **Afleiding passive structure**: Bepaal welke data objects, business objects en artifacts nodig zijn (afgeleid uit behavior access relations)
6. **Bouw laagstructuur overzicht**: Hierarchie van lagen met serving-relaties
7. **Formuleer layering principes**: Expliciete regels over laag-interacties (indien niet opgegeven, afleiden uit structuur)
8. **Bouw integrale relatiematrix**:
   - Active → Behavior → Passive chains (wie doet wat met welke data)
   - Laag-overschrijdende serving relaties (lower → higher layer)
   - Realization & composition hiërarchie
9. **Bouw traceability matrix**: End-to-end traceability van business tot technologie (bijv. Business Process → Application Function → Data Object → Technology Node)
10. **Documenteer ADRs**: Belangrijke beslissingen over integratie-, layering- en traceability-keuzes
11. **Valideer consistentie**: Check compleetheid van relaties en consistentie tussen detail-documenten en totaal view
12. **Schrijf bestand weg**: Naar afgesproken locatie met versie-metadata

### Kwaliteitsborging
- Alle active elementen uit active_structuur_file zijn opgenomen in totaal view
- Alle behavior elementen uit gedrag_file zijn opgenomen in totaal view
- Integrale relatiematrix is compleet (elke active-behavior assignment heeft passende passive access, indien relevant)
- Traceability matrix toont volledige chains van business tot technologie
- Layering principes zijn expliciet en worden nageleefd in serving-relaties
- ADRs zijn aanwezig voor alle niet-triviale integratiekeuzes
- Consistentie validatie rapport toont geen blokkerende issues
- Passive structure is volledig afgeleid uit behavior (geen losstaande data objecten zonder access-relatie)

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Totaal view is extern observeerbaar (ArchiMate integrale view)
  - Principe 2 (Eenduidige Verantwoordelijkheid): Focus op integratie van active/passive/behavior, niet op detail-definitie
  - Principe 5 (Evolutionaire Integriteit): Versioning ingebouwd via metadata header
  - Principe 7 (Transparante Verantwoording): ADRs documenteren integratiekeuzes, traceability traceerbaar
  - Principe 9 (Output-formaat Normering): Markdown als default
- **ArchiMate 3.1 Specification**: Volgt ArchiMate layered view metamodel voor integrale modeling

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aod
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: active_structuur_file, gedrag_file, bestaande_totaal_view_file (indien evolutie)
- ✓ Aangemaakte bestanden: core-framework-architect.structureer-totaal-view.md
- ✓ Geen gewijzigde bestanden (totaal view is nieuw, of wordt geversioned)

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → agent-curator: voor inconsistenties tussen active structure en behavior, of landschap-structuur issues
- → constitutioneel-auteur: voor interpretatie van strategische kaders bij integratievragen (indien relevant)
- → capability-architect: voor boundary-verificatie wanneer individuele agents in landschap worden gemodelleerd
- STOP: bij ontbrekende verplichte parameters, bij niet-bestaande input-files, bij inconsistente landschap_naam tussen input-files

---

## Metadata

**Intent-ID**: `aod.02.core-framework-architect.structureer-totaal-view`  
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
| 2026-02-15 | 1.1.0 | Scope aangepast naar landschap-architectuur (business/applicatie/data/technologie i.p.v. agent-ecosysteem). Parameter ecosysteem_naam → landschap_naam + domein. Traceability matrix toegevoegd voor business→technologie traceability. Agent-mapping verwijderd. | agent-smeder |
| 2026-02-15 | 1.0.0 | Initieel contract voor agent-ecosysteem modeling | agent-smeder |
