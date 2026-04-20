---
agent: ecosysteem-beschrijver
intent: beschrijf-ecosysteem-value-streams-agents
value_stream_fase: alle
scope: alle value streams
timestamp: 2026-04-08 22:15
---

# Ecosysteem: Value Streams & Agents — alle value streams

## Inleiding

Overzicht van alle agents in het mandarin-agents ecosysteem, gegroepeerd per value stream en fase. Per agent is de eerste zin uit de capability-boundary overgenomen, het domein vermeld en het aantal intents geteld op basis van de sectie "Voorstellen agent contracten" in het boundary-document.

Bronbestanden: alle boundary-documenten in de `artefacten/`-map van de workspace.

## Value streams

### AEO — Agent Ecosysteem Ontwikkeling

**Beschrijving**: Omvat het ontwerp, de bouw, het beheer en de overdracht van agents in het Mandarin-ecosysteem.

#### Fase 01 — Grondslagvorming

| Agent | Korte boundary-zin | Domein | Intents |
|-------|-------------------|--------|---------|
| canon-curator | Bewaakt de interne consistentie, traceerbaarheid en terminologische scherpte van alle grondslag-artefacten in de canon-workspace door ze te toetsen aan canonieke normen, geeft inhoudelijk advies voor verbeteringen, en publiceert een machineleesbaar grondslagen-register (JSON) van de complete canon-inhoud. | Canon-governance en grondslag-kwaliteitsbewaking | 4 |
| capability-architect | Definieert de externe verantwoordelijkheid en servicegrens van agents in een scherpe, observeerbare capability-boundary, identificeert aangrenzende raakvlakken en stelt daaruit voortvloeiende boundary-intents voor. | Agent capability-definitie en boundary-architectuur | 1 |

#### Fase 02 — Ecosysteeminrichting

| Agent | Korte boundary-zin | Domein | Intents |
|-------|-------------------|--------|---------|
| agent-curator | Bewaakt de canonieke consistentie van alle agents in het ecosysteem door te toetsen of hun contracts, charters en onderlinge relaties in overeenstemming zijn met constitutie, doctrines en ordeningsconcepten, en maakt overzichten beschikbaar van de agents, inclusief hun prompts, invoerparameters en bijbehorende definities voor human-in-the-loop sturing. | Ecosysteemcontrole en canonieke consistentieborging | 5 |
| agent-engineer | Zet workspace-gebonden agent-specificaties (boundaries, intents, routing) deterministisch om naar aanroepbare en consistente agent-artefacten (prompts, tasks, wiring). | Agent-realisatie | 3 |
| agent-ontwerper | Constitueert de identiteit van een agent door het vastleggen van structuur (template), gedragscontract (agent-contract) en identiteitscharter (agent-charter), zonder technische implementatie of governance-validatie. | Agent-identiteitsconstitutie | 3 |
| ecosysteem-beschrijver | Beschrijft het agent-ecosysteem als samenhangend geheel door agents, hun contracten, hun context en hun onderlinge positionering expliciet en feitelijk vast te leggen, zonder te ontwerpen, te wijzigen of te normeren. | Ecosysteem-documentatie en -positionering | 4 |

#### Fase 03 — Operationele overdracht en ketenbeheer

| Agent | Korte boundary-zin | Domein | Intents |
|-------|-------------------|--------|---------|
| handoff-steward | Creëert handoff-bestanden op basis van een afgerond execution-bestand, kent handoff-identificaties toe vanuit het handoff-register en houdt dit register bij; de ontvangstkant en eventuele kwaliteitsbeoordeling van de overgedragen inhoud vallen buiten scope. | Handoff en overdrachtsbeheer | 3 |

---

### FND — Foundation

**Beschrijving**: Levert infrastructurele en ondersteunende diensten voor alle value streams in het ecosysteem.

#### Fase 01 — Infrastructurele diensten

| Agent | Korte boundary-zin | Domein | Intents |
|-------|-------------------|--------|---------|
| documentatie-omvormer | Transformeert bestaande, betekenisvolle documentatie naar een publiceerbare structuur (bijv. MkDocs) zonder inhoudelijke wijziging, interpretatie of toevoeging van betekenis. | Documentatie-representatie | 3 |
| ecosysteem-coordinator | Orkestreert ecosysteem-brede lifecycle-taken (instructie-generatie, task-aggregatie) die geen individuele agent toebehoort; raakt geen agent-inhoud aan. | Ecosysteem-lifecycle | 2 |

#### Fase 02 — Conceptvorming

| Agent | Korte boundary-zin | Domein | Intents |
|-------|-------------------|--------|---------|
| concept-curator | De concept-curator expliciteert, structureert en beoordeelt conceptuele inhoud op coherentie en traceerbaarheid, zonder normatieve besluiten te nemen of technische implementaties te realiseren. | Conceptbeheer | 4 |
| documentvertaler | Zet een Markdown-document deterministisch om naar een correct en professioneel Word-document (.docx), zonder wijziging van betekenis. | Documentconversie, representatie-omvorming | 1 |

---

### AOD — Architectuur- en Oplossingsontwerp

**Beschrijving**: Omvat architectuurverkenning, domeinmodellering en architectuursynthese voor oplossingsontwerp.

#### Fase 01 — Verkenning

| Agent | Korte boundary-zin | Domein | Intents |
|-------|-------------------|--------|---------|
| architectuur-verkenner | Verkent de probleemruimte en formuleert een eerste architectuurvisie op basis van organisatiecontext en vraagstelling, zonder deze visie uit te werken tot gedetailleerde architectuur. | Architectuurvisie | 2 |
| strategy-framework-architect | (boundary ontbreekt) | — | — |

#### Fase 02 — Architectuurkadering

| Agent | Korte boundary-zin | Domein | Intents |
|-------|-------------------|--------|---------|
| core-framework-architect | Modelleert een coherent landschap over business, applicatie, data en technologie door het instantiëren van het core framework voor een specifiek domein of value stream, waarbij structurele samenhang en traceability tussen lagen centraal staan. | Framework-architectuur en structureel ontwerp | 4 |

#### Fase 05 — Architectuursynthese

| Agent | Korte boundary-zin | Domein | Intents |
|-------|-------------------|--------|---------|
| solution-architect | Synthetiseert alle domeinarchitecturen (business, applicatie, data, technologie) tot één integrale architectuurbeschrijving met expliciete samenhang, oplossingsscenario's en transitierichting, binnen het TOGAF-integratiekader. | Integrale architectuursynthese | 3 |

---

### SFW — Software Product Development

**Beschrijving**: Omvat de softwareontwikkelingsketen van verkenning via werkvoorbereiding tot gedragsspecificatie.

#### Fase 01 — Verkenning

| Agent | Korte boundary-zin | Domein | Intents |
|-------|-------------------|--------|---------|
| hypothese-vormer | Formuleert één expliciete, toetsbare probleem-oplossingshypothese die de huidige situatie contrasteert met een veronderstelde betere toekomst, inclusief maximaal drie aannames als risico's. | Hypothese-formulering en besluitvoorbereiding | 3 |

#### Fase 02 — Werkvoorbereiding

| Agent | Korte boundary-zin | Domein | Intents |
|-------|-------------------|--------|---------|
| thema-verwoorder | Beschrijft op een gestructureerde manier conform Safe epic-statements en doet voorstel voor verbeteringen. | Value stream management / thematische structurering | 3 |

#### Fase 03 — Ontwerp/Specificatie

| Agent | Korte boundary-zin | Domein | Intents |
|-------|-------------------|--------|---------|
| gedragsspecificator | De gedragsspecificator vertaalt functionele behoeften en wijzigingsvragen naar eenduidige, technologie-agnostische en verifieerbare gedragsrequirements in Gherkin-scenario's (Given-When-Then), waarbij oplossingsontwerp en technische implementatie expliciet buiten scope vallen. | Requirements Engineering & BDD | 3 |

---

### MIV — Markt- en Investeringsvorming

**Beschrijving**: Omvat behoeftespecificatie, marktverkenning en strategische leverancierstoetsing.

#### Fase 07 — Behoeftevastlegging voor leveranciersselectie

| Agent | Korte boundary-zin | Domein | Intents |
|-------|-------------------|--------|---------|
| behoefteprofiel-opsteller | Vertaalt functionele en niet-functionele behoeften voor hosting en technisch applicatiebeheer naar een volledig en prioriteerbaar eisenpakket voor leveranciersselectie, zonder leveranciers te beoordelen, te kiezen of contractueel vast te leggen. | Behoeftespecificatie | 3 |
| leveranciers-verkenner | Verkent de markt van relevante hosting-providers en stelt op basis van behoefteprofiel, selectiecriteria en operationele scope een onderbouwde longlist met fit-duiding en expliciete uitsluitingsgronden op, zonder leveranciers te rangschikken, te kiezen of het eisenpakket te wijzigen. | Leveranciersverkenning | 3 |
| positionering-en-monetisatie-toetser | Toetst kandidaat-leveranciers uit een longlist op strategische compatibiliteit met de gekozen marktpositionering en monetisatie-logica van het product, en levert per leverancier een toetsingsuitkomst met onderbouwing; rangschikking, contractuele advisering en het aanpassen van de positioneringsstrategie zelf vallen buiten scope. | Strategische leverancierstoetsing | 3 |

---

## Agents-matrix

Totaaloverzicht van alle agents in scope, gesorteerd op value stream en fase.

| Agent | Value stream | Fase | Output-type | Intents |
|-------|-------------|------|------------|---------|
| canon-curator | aeo | 01 | rapport | 4 |
| capability-architect | aeo | 01 | document | 1 |
| agent-curator | aeo | 02 | rapport | 5 |
| agent-engineer | aeo | 02 | artefact | 3 |
| agent-ontwerper | aeo | 02 | artefact | 3 |
| ecosysteem-beschrijver | aeo | 02 | document | 4 |
| handoff-steward | aeo | 03 | artefact | 3 |
| documentatie-omvormer | fnd | 01 | artefact | 3 |
| ecosysteem-coordinator | fnd | 01 | artefact | 2 |
| concept-curator | fnd | 02 | document | 4 |
| documentvertaler | fnd | 02 | artefact | 1 |
| architectuur-verkenner | aod | 01 | document | 2 |
| strategy-framework-architect | aod | 01 | (boundary ontbreekt) | — |
| core-framework-architect | aod | 02 | document | 4 |
| solution-architect | aod | 05 | document | 3 |
| hypothese-vormer | sfw | 01 | document | 3 |
| thema-verwoorder | sfw | 02 | document | 3 |
| gedragsspecificator | sfw | 03 | artefact | 3 |
| behoefteprofiel-opsteller | miv | 07 | document | 3 |
| leveranciers-verkenner | miv | 07 | document | 3 |
| positionering-en-monetisatie-toetser | miv | 07 | rapport | 3 |

**Totaal agents in scope**: 21
**Totaal value streams in scope**: 5

## Bronbestanden

- `artefacten/aeo/aeo.01.canon-curator/canon-curator.agent-boundary.md`
- `artefacten/aeo/aeo.01.capability-architect/capability-architect.agent-boundary.md`
- `artefacten/aeo/aeo.02.agent-curator/agent-curator.agent-boundary.md`
- `artefacten/aeo/aeo.02.agent-engineer/agent-engineer.agent-boundary.md`
- `artefacten/aeo/aeo.02.agent-ontwerper/agent-ontwerper.agent-boundary.md`
- `artefacten/aeo/aeo.02.ecosysteem-beschrijver/ecosysteem-beschrijver.agent-boundary.md`
- `artefacten/aeo/aeo.03.handoff-steward/handoff-steward.agent-boundary.md`
- `artefacten/fnd/fnd.01.documentatie-omvormer/documentatie-omvormer.agent-boundary.md`
- `artefacten/fnd/fnd.01.ecosysteem-coordinator/ecosysteem-coordinator.agent-boundary.md`
- `artefacten/fnd/fnd.02.concept-curator/concept-curator.agent-boundary.md`
- `artefacten/fnd/fnd.02.documentvertaler/agent-boundary-documentvertaler.md`
- `artefacten/aod/aod.01.architectuur-verkenner/architectuur-verkenner.agent-boundary.md`
- `artefacten/aod/aod.01.strategy-framework-architect/` (lege map — boundary ontbreekt)
- `artefacten/aod/aod.02.core-framework-architect/core-framework-architect.agent-boundary.md`
- `artefacten/aod/aod.05.solution-architect/agent-boundary-solution-architect.md`
- `artefacten/sfw/sfw.01.hypothese-vormer/hypothese-vormer.agent-boundary.md`
- `artefacten/sfw/sfw.02.thema-verwoorder/agent-boundary-thema-verwoorder.md`
- `artefacten/sfw/sfw.03.gedragsspecificator/gedragsspecificator.agent-boundary.md`
- `artefacten/miv/miv.07.behoefteprofiel-opsteller/behoefteprofiel-opsteller.agent-boundary.md`
- `artefacten/miv/miv.07.leveranciers-verkenner/leveranciers-verkenner.agent-boundary.md`
- `artefacten/miv/miv.07.positionering-en-monetisatie-toetser/positionering-en-monetisatie-toetser.agent-boundary.md`
