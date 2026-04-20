---
agent: knowledge-graph-modelleur
intent: definieer-graph-schema
intent-id: aeo.01.knowledge-graph-modelleur.02
versie: 1.0.0
status: vers
---
# Knowledge-graph-modelleur — Definieer Graph Schema

## Rolbeschrijving (korte samenvatting)

De knowledge-graph-modelleur definieert het graph-schema voor een domein door knooppunttypen, relatietypen en eigenschapsspecificaties expliciet vast te leggen op basis van een gestructureerd brondocument — los van de instantie-data — als herbruikbaar structuurkader voor knowledge graph-generatie.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `knowledge-graph-modelleur.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- brondocument: Pad naar het gestructureerde brondocument waaruit het schema wordt afgeleid (type: string, pad relatief ten opzichte van de workspace root).
- schema-naam: Naam van het te genereren graph-schema, gebruikt in bestandsnaam en identificatie (type: string, kebab-case).

**Optionele parameters**:
- domeinafbakening: Beschrijving of selectie van het domeingebied waarvoor het schema geldt; wanneer afwezig wordt het volledige brondocument als domein beschouwd (type: string, 1-3 zinnen).
- versie: Gewenste startversie van het schema (type: string, semver-formaat, default: "1.0.0").

**Afgeleide informatie** (geëxtraheerd uit brondocument):
- entiteittypen: Alle entiteittypes gevonden in het brondocument
- relatietypen: Alle relatietypes gevonden in het brondocument
- domeinterminologie: Gebruikte naamgeving in het brondocument

### Output (wat komt eruit)

De knowledge-graph-modelleur levert:
- **Graph-schema document** met:
  - Schema-identificatie: naam, versie, domein, brondocument
  - Knooppunttype-definities: per type de naam, label, verplichte en optionele eigenschappen met datatype
  - Relatietypen-definities: naam, brontype, doeltype, kardinaliteit, richting, label
  - Beperkingen (constraints): integriteitsregels die gelden voor het schema
  - Toelichting op schema-keuzes

**Deliverable bestand**: `artefacten/aeo/aeo.01.knowledge-graph-modelleur/schemas/{schema-naam}.graph-schema.md`

**Contractuele templatebinding**:
```yaml
output:
  - type: graph-schema
    herkomstpositie: initiërend
    template: ~
```

**Outputformaat** (standaard structuur):
```markdown
# Graph Schema: {schema-naam}

**Versie**: {versie}
**Domein**: {domein}
**Brondocument**: {pad}
**Datum**: {yyyy-mm-dd}

---

## Knooppunttype-definities

### {NodeType}
- **Label**: "{Nederlandse naam}"
- **Verplichte eigenschappen**:
  - `{eigenschap}` ({datatype}) — {toelichting}
- **Optionele eigenschappen**:
  - `{eigenschap}` ({datatype}) — {toelichting}

## Relatietype-definities

### {RELATIE_TYPE}
- **Van**: {NodeType}
- **Naar**: {NodeType}
- **Kardinaliteit**: {1:1 | 1:N | N:N}
- **Richting**: {enkelvoudig | bidirectioneel}
- **Label**: "{Nederlandse naam van relatie}"

## Beperkingen

- {constraint 1}
- {constraint 2}

## Schema-keuzes

- {toelichting op naamgeving}
- {toelichting op kardinaliteitskeuzes}
```

**Formaat-normering**: 
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek

### Foutafhandeling

De knowledge-graph-modelleur:
- stopt wanneer `brondocument` niet bestaat of niet leesbaar is;
- stopt wanneer `brondocument` geen identificeerbare entiteitstructuur bevat om een schema van af te leiden;
- stopt wanneer `schema-naam` leeg is of niet voldoet aan kebab-case naamgeving;
- vraagt om verduidelijking wanneer `domeinafbakening` verwijst naar entiteiten die niet in het brondocument voorkomen.

De knowledge-graph-modelleur definieert uitsluitend de schemastructuur; vult geen instantie-data in en wijzigt het brondocument niet.

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract beschrijft extern observeerbaar gedrag
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén taak — schema-definitie, geen instantie-generatie
  - Principe 4 (Scheiding van Wat en Hoe): Contract specificeert input/output, niet implementatie
  - Principe 7 (Transparante Verantwoording): Schema-keuzes vastgelegd in output
  - Principe 9 (Output-formaat Normering): Markdown als default

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen (`template: ~`)

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aeo
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door runner)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: brondocument
- ✓ Aangemaakte bestanden: {schema-naam}.graph-schema.md
- ✓ Geen gewijzigde bestanden
- ✓ Aantal gedefinieerde knooppunttypen en relatietypen

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → logisch-modelleur: wanneer het brondocument modelleerkundige ambiguïteiten bevat die schema-keuzes blokkeren
- → capability-architect: wanneer het schema een scope beslaat die buiten de boundary van de agent valt
- STOP: bij onleesbaar brondocument, bij brondocument zonder herkenbare structuur

---

## Metadata

**Intent-ID**: `aeo.01.knowledge-graph-modelleur.definieer-graph-schema`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 01 — Grondslagvorming  
**Classificatie**:
- Vormingsfase: Realisatie
- Betekeniseffect: Realiserend
- Werking: Inhoudelijk
- Bronhouding: Input-gebonden
