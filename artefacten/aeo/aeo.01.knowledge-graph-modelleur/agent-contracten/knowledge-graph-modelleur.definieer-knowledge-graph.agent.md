---
agent: knowledge-graph-modelleur
intent: definieer-knowledge-graph
intent-id: aeo.01.knowledge-graph-modelleur.01
versie: 1.0.0
status: vers
---
# Knowledge-graph-modelleur — Definieer Knowledge Graph

## Rolbeschrijving (korte samenvatting)

De knowledge-graph-modelleur transformeert een gestructureerd brondocument — zoals een logisch datamodel of entiteitsbeschrijving — naar een volledig knowledge graph-artefact dat direct toepasbaar is als werkgeheugen of redeneergrondslag voor AI-agents.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `knowledge-graph-modelleur.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- brondocument: Pad naar het gestructureerde brondocument dat als basis dient voor de graph (type: string, pad relatief ten opzichte van de workspace root; ondersteunde typen: logisch datamodel, entiteitsbeschrijving, gestructureerde markdown).
- graph-naam: Naam van de te genereren knowledge graph, gebruikt in bestandsnaam en kopregel (type: string, kebab-case).

**Optionele parameters**:
- uitvoerformaat: Gewenst formaat van de knowledge graph-output (type: string, waarden: "markdown-yaml", "turtle", "json-ld", default: "markdown-yaml").
- afbakeningscriteria: Selectie van entiteiten of relaties die relevant zijn voor de doelgraph; wanneer afwezig worden alle elementen uit het brondocument opgenomen (type: list[string], default: volledig brondocument).
- schema-bestand: Pad naar een eerder gedefinieerd graph-schema dat als structuurkader geldt; wanneer afwezig wordt het schema afgeleid uit het brondocument (type: string, optioneel).

**Afgeleide informatie** (geëxtraheerd uit brondocument):
- entiteiten: Lijst van entiteittypen gevonden in het brondocument
- relaties: Lijst van relatietypen gevonden in het brondocument
- attributen: Eigenschappen per entiteittype

### Output (wat komt eruit)

De knowledge-graph-modelleur levert:
- **Knowledge graph-artefact** in het gevraagde uitvoerformaat met:
  - Knooppunttypen (node types): gestructureerde definitie van alle entiteittypen
  - Relatietypen (edge types): gestructureerde definitie van alle relatietypen met richting en kardinaliteit
  - Eigenschappen (properties): per knooppunttype de relevante attributen met datatype
  - Instanties (optioneel): concrete knooppunten en relaties wanneer brondocument concrete data bevat
- **Modelleringsbeslissingen**: toelichting op gemaakte keuzes — opgenomen en uitgesloten elementen, naamgeving, relatierichting, granulariteit

**Deliverable bestand**: `artefacten/aeo/aeo.01.knowledge-graph-modelleur/knowledge-graphs/{graph-naam}.knowledge-graph.md`

**Contractuele templatebinding**:
```yaml
output:
  - type: knowledge-graph
    herkomstpositie: initiërend
    template: ~
```

**Outputformaat** (standaard structuur bij uitvoerformaat "markdown-yaml"):
```markdown
# Knowledge Graph: {graph-naam}

**Brondocument**: {pad-naar-brondocument}
**Uitvoerformaat**: markdown-yaml
**Datum**: {yyyy-mm-dd}

---

## Knooppunttypen

```yaml
node_types:
  - naam: {EntityType}
    label: "{Nederlandse naam}"
    eigenschappen:
      - naam: {attribuut}
        type: {string|integer|boolean|date}
        verplicht: {true|false}
```

## Relatietypen

```yaml
edge_types:
  - naam: {RELATIE_TYPE}
    van: {EntityType}
    naar: {EntityType}
    kardinaliteit: {1:1|1:N|N:N}
    richting: {enkelvoudig|bidirectioneel}
```

## Modelleringsbeslissingen

- **Opgenomen**: {welke elementen en waarom}
- **Uitgesloten**: {welke elementen en waarom}
- **Naamgeving**: {gehanteerde naamgevingsconventies}
```

**Formaat-normering**: 
- Default formaat: **Markdown met embedded YAML** (.md), conform Principe 9
- Alternatieve formaten (Turtle, JSON-LD) alleen op expliciete verzoek via parameter `uitvoerformaat`

### Foutafhandeling

De knowledge-graph-modelleur:
- stopt wanneer `brondocument` niet bestaat of niet leesbaar is op het opgegeven pad;
- stopt wanneer `brondocument` geen herkenbare structuur bevat (geen entiteiten, attributen of relaties identificeerbaar);
- stopt wanneer `schema-bestand` is opgegeven maar niet bestaat of onleesbaar is;
- vraagt om verduidelijking wanneer `afbakeningscriteria` verwijzen naar entiteiten die niet in het brondocument voorkomen;
- meldt onduidelijkheden expliciet in de modelleringsbeslissingen wanneer het brondocument tegenstrijdige of onvolledige structuurinformatie bevat — de agent stopt niet, maar documenteert de aanname.

De knowledge-graph-modelleur wijzigt het brondocument niet; rapporteert uitsluitend de graph en de modelleringsbeslissingen.

---

## Werkwijze

### Stappen
1. **Lees brondocument**: Analyseer het opgegeven brondocument op aanwezige entiteiten, attributen en relaties.
2. **Extraheer structuurinformatie**: Identificeer knooppunttypen, relatietypen en eigenschappen conform het brondocument; pas `afbakeningscriteria` toe indien opgegeven.
3. **Raadpleeg schema-bestand** (indien opgegeven): Gebruik het schema als structuurkader voor naamgeving en typering.
4. **Modelleer knooppunttypen**: Vertaal entiteiten naar knooppunttype-definities met eigenschappen en datatypes.
5. **Modelleer relatietypen**: Vertaal relaties naar relatietypen met richting en kardinaliteit.
6. **Documenteer modelleringsbeslissingen**: Leg vast welke elementen zijn opgenomen, welke zijn uitgesloten en waarom; documenteer naamgevingskeuzes.
7. **Genereer graph-artefact**: Schrijf het knowledge graph-artefact in het gevraagde uitvoerformaat.
8. **Valideer volledigheid**: Controleer of alle entiteiten en relaties uit het brondocument (binnen de afbakening) zijn verwerkt.

### Kwaliteitsborging
- Alle entiteiten uit het brondocument (binnen afbakening) zijn verwerkt als knooppunttype
- Alle relaties zijn voorzien van richting en kardinaliteit
- Modelleringsbeslissingen documenteren ten minste de opgenomen én uitgesloten elementen
- Uitvoerformaat is correct toegepast conform de `uitvoerformaat`-parameter
- Bestand weggeschreven naar het correcte pad

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract beschrijft extern observeerbaar gedrag
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén taak — graph genereren vanuit brondocument
  - Principe 4 (Scheiding van Wat en Hoe): Contract specificeert input/output, niet implementatie
  - Principe 7 (Transparante Verantwoording): Modelleringsbeslissingen expliciet vastgelegd in output
  - Principe 9 (Output-formaat Normering): Markdown als default

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen (`template: ~`)

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aeo
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door runner)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: brondocument, schema-bestand (indien opgegeven)
- ✓ Aangemaakte bestanden: {graph-naam}.knowledge-graph.md
- ✓ Geen gewijzigde bestanden
- ✓ Aantal verwerkte knooppunttypen en relatietypen

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → logisch-modelleur: wanneer brondocument inconsistenties bevat die vragen om modelleerkundige interpretatie
- → capability-architect: wanneer het toepassingsbereik van de graph de boundary van de agent overschrijdt
- STOP: bij onleesbaar of ongestructureerd brondocument, bij onvindbaar schema-bestand

---

## Metadata

**Intent-ID**: `aeo.01.knowledge-graph-modelleur.definieer-knowledge-graph`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 01 — Grondslagvorming  
**Classificatie**:
- Vormingsfase: Realisatie
- Betekeniseffect: Realiserend
- Werking: Inhoudelijk
- Bronhouding: Input-gebonden
