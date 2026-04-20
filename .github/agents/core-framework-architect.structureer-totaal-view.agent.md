---
agent: core-framework-architect
intent: structureer-totaal-view
intent-id: aod.02.core-framework-architect.04
versie: 1.0.0
digest: 1920
status: vers
---
# Core-framework-architect — Structureer Totaal View

## Rolbeschrijving (korte samenvatting)

De Core-framework-architect structureert en integreert de actieve structuur, passieve structuur en gedragslaag van een landschap in één coherente ArchiMate totaal view, waarbij alle relaties tussen active, passive en behavior elementen expliciet zijn vastgelegd en traceability van business tot technologie is geborgd.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `core-framework-architect.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- archimate_laag: Te modelleren ArchiMate-laag (type: string, mogelijke waarden: "Business", "Application", "Technology").
- bestand: Pad naar het bronbestand dat als input dient voor modellering (type: string, .md bestand).

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

**Contractuele templatebinding**:

```yaml
template: templates/core-framework-architect.structureer-totaal-view.template.md
```

### Foutafhandeling

De Core-framework-architect:
- stopt wanneer archimate_laag of bestand ontbreekt;
- stopt wanneer archimate_laag ongeldig is (niet Business/Application/Technology);
- stopt wanneer bestand niet bestaat of niet leesbaar is;
- vraagt om verduidelijking wanneer het bronbestand onvoldoende context bevat;
- escaleert naar agent-curator wanneer inconsistenties tussen active structure en behavior worden gedetecteerd;
- escaleert naar constitutioneel-auteur voor interpretatie van strategische kaders bij integratievragen (indien relevant);
- escaleert naar capability-architect voor boundary-vragen wanneer individuele agents in landschap worden gemodelleerd.

Totaal view bevat GEEN implementatie-details, alleen ArchiMate integrale modeling met expliciete cross-layer relaties en traceability.

**Conventie**: Totaal view is leidend voor landschap-overzicht; detail-documenten (active structure, behavior) zijn leidend voor element-specifieke definitie.

## Werkwijze

### Stappen
1. **Valideer input**: Check verplichte parameters en geldigheid van `archimate_laag`
2. **Lees bronbestand**: Lees `bestand` en parse relevante structuur/gedragselementen
3. **Cross-validatie**: Check consistentie van gevonden relaties (geen ontbrekende kernkoppelingen)
4. **Afleiding passive structure**: Bepaal welke data objects, business objects en artifacts nodig zijn
5. **Bouw laagstructuur overzicht**: Hierarchie van lagen met serving-relaties
6. **Bouw integrale relatiematrix**:
   - Active → Behavior → Passive chains (wie doet wat met welke data)
   - Laag-overschrijdende serving relaties (lower → higher layer)
   - Realization & composition hiërarchie
7. **Bouw traceability matrix**: End-to-end traceability van business tot technologie (bijv. Business Process → Application Function → Data Object → Technology Node)
8. **Documenteer ADRs**: Belangrijke beslissingen over integratie-, layering- en traceability-keuzes
9. **Valideer consistentie**: Check compleetheid van relaties en consistentie van de totaal view
10. **Schrijf bestand weg**: Naar afgesproken locatie met versie-metadata

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

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aod
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: bestand
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
| 2026-02-15 | 1.1.0 | Scope aangepast naar landschap-architectuur (business/applicatie/data/technologie i.p.v. agent-ecosysteem). Parameter ecosysteem_naam → landschap_naam + domein. Traceability matrix toegevoegd voor business→technologie traceability. Agent-mapping verwijderd. | agent-smeder |
| 2026-02-15 | 1.0.0 | Initieel contract voor agent-ecosysteem modeling | agent-smeder |
