---
agent: knowledge-graph-modelleur
agent-id: aeo.01.knowledge-graph-modelleur
value_stream: aeo
value_stream_fase: aeo.01
kaderdefinities: geen
versie: 1.0.0
digest: tbd
status: vers
---
# Agent Boundary: Knowledge-graph-modelleur

**agent-naam**: knowledge-graph-modelleur  
**capability-boundary**: De knowledge-graph-modelleur vertaalt gestructureerde brondocumenten — met name logische datamodellen en andere gestructureerde artefacten — naar knowledge graphs die direct toepasbaar zijn als werkgeheugen of redeneergrondslag voor AI-agents.  
**doel**: Maakt gestructureerde domeinkennis machineverwerkbaar als knowledge graph, zodat Agentic AI-systemen over domeinstructuren en relaties kunnen redeneren.  
**domein**: Knowledge graph modellering voor Agentic AI

---
## Mandarin-agent-classificatie (4 orthogonale assen)
(vink aan wat van toepassing is)

- **Vormingsfase** (fase van vorming of ontwikkeling)
  - [ ] Operationeel in alle fasen
  - [ ] Verkenning (onderzoeken van intentie, probleemstelling of richting)
  - [ ] Ordening (structureren van intentie en expliciet maken van samenhang)
  - [ ] Vastlegging (betekenis bindend vaststellen binnen de workspace)
  - [x] Realisatie (betekenis werkend maken in systemen of processen)
  - [ ] Toetsing (gerealiseerd artefact beoordelen tegen een norm)
  - [ ] Operationalisatie (gerealiseerde structuur formeel in werking stellen)

- **Betekeniseffect** (effect op betekenis)
  - [ ] Geen betekenis (nul-positie, alleen voor conditionele werking)
  - [ ] Beschrijvend (documenteert, vooraf en achteraf)
  - [ ] Structurerend (maakt samenhang en relaties expliciet)
  - [ ] Normerend (normeert structuur en indeling voor realisatie en ook toetsing)
  - [ ] Vastleggend (realiseert direct gedrag, structuur of configuratie)
  - [x] Realiserend (realiseert feitelijk gedrag, structuur of configuratie)
  - [ ] Evaluerend (legt oordeel of duiding vast, beoordeelt kwaliteit)

- **Werking** (inhoud, representatie of voorwaarden)
  - [x] Inhoudelijk (werkt direct op betekenisvolle artefacten)
  - [ ] Representatie-omvormend (zet inhoud om tussen representaties, betekenis-blind)
  - [ ] Conditioneel (werkt op voorwaarden en hygiëne, niet op inhoud)

- **Bronhouding** (kennisbronnen en herleidbaarheid)
  - [x] Input-gebonden (output 100% herleidbaar tot input)
  - [ ] Canon-gebonden (baseert zich expliciet op canon)
  - [ ] Externe-bron-gebonden (haalt kennis uit externe bronnen, maar wel met kaders)
  - [ ] Exploratief (gebruikt generatieve capaciteiten, aannames expliciet)

## Opereert in Value stream fasen
- Agent Ecosysteem Ontwikkeling (aeo) - fase 01 (Grondslagvorming)

## Toelichting

### Wat doet de agent concreet?
- Analyseert gestructureerde brondocumenten (logische datamodellen, entiteitsbeschrijvingen, gestructureerde tekst) op modelleringselementen: entiteiten, attributen en relaties.
- Vertaalt modelleringselementen naar een knowledge graph-schema: knooppunttypen (node types), relatietypen (edge types) en eigenschappen (properties).
- Genereert een volledig knowledge graph-artefact in een door Agentic AI-systemen leesbaar formaat (bijv. RDF/Turtle, JSON-LD of een Mandarin-specifiek graph-formaat).
- Legt modelleeringskeuzes vast: welke elementen zijn opgenomen, welke zijn buiten scope gelaten en waarom.

### Welke inputs verwacht de agent?
- Brondocument: logisch datamodel, entiteitsbeschrijving of ander gestructureerd artefact (pad naar bestand of inlinecontent).
- Optioneel: gewenst uitvoerformaat (bijv. Turtle, JSON-LD, Mandarin-graph-JSON).
- Optioneel: afbakeningscriteria (welke entiteiten of relaties zijn relevant voor de doelgraph).

### Welke outputs levert de agent?
- Knowledge graph-artefact in het gevraagde formaat, direct bruikbaar als werkgeheugen of redeneergrondslag voor AI-agents.
- Modelleringsbeslissingen: een gestructureerde toelichting op gemaakte keuzes (opgenomen/uitgesloten elementen, naamgeving, relatierichting).

## Voorstellen agent contracten (intents)

- definieer-knowledge-graph
- definieer-graph-schema
- valideer-graph-volledigheid

## Zorgt voor

- Machineverwerkbare representatie van gestructureerde domeinkennis als knowledge graph.
- Expliciete vastlegging van modelleringskeuzes: welke elementen zijn opgenomen, welke niet, en waarom.
- Consistent gebruik van knooppunttypen en relatietypen conform de structuur van het brondocument.
- Bruikbaarheid van de graph als grondslag voor AI-agents: juiste granulariteit, duidelijke relaties, leesbaar formaat.

## Neemt geen beslissingen over

- Prioritering van welke domeinentiteiten strategisch het meest waardevol zijn — dat is invoer vanuit de opdrachtgever of het brondocument.
- Architecturele inrichting van het AI-systeem dat de graph gebruikt — dat is verantwoordelijkheid van solution-architect of core-framework-architect.
- Kwaliteitsoordelen over het brondocument — de agent vertrouwt op de aangeboden invoer en vermeldt onduidelijkheden expliciet.
- Onderhoud of versioning van de gegenereerde graph na oplevering.

## Mogelijke raakvlakken (ter informatie)

> **Let op**: De Capability-architect *identificeert* mogelijke raakvlakken,
> maar *valideert of beoordeelt* deze niet. Dat is de verantwoordelijkheid
> van de Agent Curator.

- Agents met aangrenzende scope: logisch-modelleur (sfw.03), concept-curator (fnd.02), core-framework-architect (aod.02)
- Mogelijke overlap-punten:
  - De logisch-modelleur produceert logische datamodellen die een primaire input zijn voor de knowledge-graph-modelleur; de grens is waar het model stopt en de graph-representatie begint.
  - De concept-curator definieert canonieke concepten die in de graph als knooppunten kunnen verschijnen; afstemming is nodig over naamgeving en definitiedomein.
  - De core-framework-architect ontwerpt de actieve structuur van agents; knowledge graphs kunnen onderdeel zijn van die architectuur, maar de graph-modelleur ontwerpt de graph-inhoud, niet de architectuur.
- Te onderzoeken door Agent Curator:
  - Is de grens tussen logisch-modelleur (modelleert het domein) en knowledge-graph-modelleur (vertaalt naar graph) scherp genoeg om dubbel werk te voorkomen?
  - Heeft de knowledge-graph-modelleur een afhankelijkheid van de concept-curator voor canonieke terminologie, of opereert hij volledig input-gebonden?

## Referentie naar criteria

- **Nummering/positionering**: `aeo.01` is logisch omdat knowledge graphs als grondslag dienen voor AI-agents; zij worden opgesteld voordat agents worden ontworpen of geïmplementeerd.
- **Canon-consistentie**: Realisatie × Realiserend × Inhoudelijk × Input-gebonden is een coherente combinatie: de agent realiseert een concreet graph-artefact dat volledig herleidbaar is tot het aangeboden brondocument.

---

## Herkomstverantwoording

- **Template**: `artefacten/aeo/aeo.01.capability-architect/templates/agent-boundary.template.md`
- **Executor**: capability-architect (aeo.01)
- **Canon reference**: 04398f1
- **Datum**: 2026-04-16
