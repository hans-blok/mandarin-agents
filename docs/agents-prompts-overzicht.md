# Ecosysteem Agent Prompt Contracten Overzicht

**Gegenereerd op**: 2026-03-08  
**Execution ID**: c81c  
**Canon Reference**: 2aa7464  
**Aantal agents**: 11  
**Aantal intents**: 33

---

## Overzicht per Value Stream

| Value Stream | Beschrijving | Agents | Intents |
|-------------|--------------|--------|---------|
| **AEO** | Agent Ecosysteem Ontwikkeling | 5 | 15 |
| **AOD** | Architectuur Ontwerp | 1 | 4 |
| **FND** | Fundamenten | 2 | 5 |
| **SFW** | Software Fabricage | 3 | 9 |

---

# AEO — Agent Ecosysteem Ontwikkeling

## agent-curator

**Domein**: Ecosysteemcontrole en canonieke consistentieborging  
**Value Stream Fase**: aeo.02

### rapporteer-ecosysteem-overzicht

**Beschrijving**  
Genereert tabellarisch overzicht van alle agents in een value stream fase, met status van artefacten en canonieke consistentie.

#### Input (parameters)

*Geen verplichte parameters*

#### Output

- **type:** Markdown  
- **bestand:** `docs/agents-overzicht.md`

---

### rapporteer-prompts-overzicht

**Beschrijving**  
Genereert gestructureerd overzicht per agent uit alle prompt-contracten, inclusief invoerparameters en beschrijvingen.

#### Input (parameters)

*Geen verplichte parameters*

#### Output

- **type:** Markdown  
- **bestand:** `docs/agents-prompts-overzicht.md`

---

### valideer-agent-consistentie

**Beschrijving**  
Toetst per agent of artefacten canoniek consistent zijn met constitutie, doctrines en ordeningsconcepten.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `agent_naam` | string | Naam van de agent om te valideren |
| `value_stream_fase` | string | Value stream fase (format: {vs}.{fase}) |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `scope` | string | Validatiescope (charter/contracten/prompts/tasks/alles) |

#### Output

- **type:** Markdown  
- **bestand:** `artefacten/{vs}/{vs}.{fase}.{agent_naam}/agent-curator.valideer-agent-consistentie.rapport.md`

---

### valideer-boundary-overlap

**Beschrijving**  
Analyseert capability boundaries van alle agents op overlap of lacunes.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `value_stream_fase` | string | Value stream fase (format: {vs}.{fase}) |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `agent_namen` | list[string] | Specifieke agents om te analyseren |
| `canon_ref` | string | Canon commit referentie |

#### Output

- **type:** Markdown  
- **bestand:** `artefacten/{vs}/{vs}.{fase}/agent-curator.valideer-boundary-overlap.rapport.md`

---

## agent-engineer

**Domein**: Agent-lifecycle realisatie en code-generatie  
**Value Stream Fase**: aeo.02

### realiseer-agent-prompts

**Beschrijving**  
Genereert en actualiseert promptbestanden voor alle intents van een agent.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `agent_naam` | string | Naam van de agent |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `intent` | string | Specifieke intent om te genereren |

#### Output

- **type:** Markdown met YAML frontmatter  
- **bestand:** `artefacten/{vs}/{vs}.{fase}.{agent}/prompts/mandarin.{agent}.{intent}.prompt.md`

---

### realiseer-agent-runner

**Beschrijving**  
Genereert Python runner-scripts voor alle intents van een agent met parameter-handling en logging.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `agent_naam` | string | Naam van de agent |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `contract_folder` | string | Folder met agent-contracten |
| `runner_output_folder` | string | Output folder voor runners |
| `overwrite_existing` | boolean | Overschrijf bestaande runners |

#### Output

- **type:** Python  
- **bestand:** `{runner_output_folder}/{agent}-{intent}.runner.py`

---

### realiseer-agent-taskconfiguratie

**Beschrijving**  
Genereert VSCode task-definities voor alle intents van een agent.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `agent_naam` | string | Naam van de agent |
| `agent_contracts` | array[string] | Lijst van agent-contract paden |

#### Output

- **type:** JSON  
- **bestand:** `artefacten/{vs}/{vs}.{fase}.{agent_naam}/tasks/{vs}-{fase}.{agent_naam}.tasks.json`

---

## agent-ontwerper

**Domein**: Agent-identiteit en artefact-ontwerp  
**Value Stream Fase**: aeo.02

### definieer-agent-charter

**Beschrijving**  
Creëert het agent-charter document met identiteit, rol, grenzen, kerntaken en werkwijze.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `agent_naam` | string | Naam van de agent (kebab-case) |
| `boundary_file` | string | Pad naar agent-boundary document |
| `value_stream_fase` | string | Value stream fase (format: {vs}.{fase}) |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `template_file` | string | Override voor charter template locatie |
| `referenties` | list[string] | Referentie-documenten voor charter-definitie |

#### Output

- **type:** Markdown  
- **bestand:** `artefacten/{vs}/{vs}.{fase}.{agent}/{agent}.charter.md`

---

### definieer-agent-contract

**Beschrijving**  
Creëert agent-contract documenten voor elke intent uit de boundary met input, output en governance.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `agent_naam` | string | Naam van de agent (kebab-case) |
| `boundary_file` | string | Pad naar agent-boundary document |
| `intent_naam` | string | Naam van de intent |
| `value_stream_fase` | string | Value stream fase (format: {vs}.{fase}) |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `template_file` | string | Override voor contract template locatie |
| `referenties` | list[string] | Referentie-documenten |

#### Output

- **type:** Markdown  
- **bestand:** `artefacten/{vs}/{vs}.{fase}.{agent}/agent-contracten/{agent}.{intent}.agent.md`

---

### definieer-agent-template

**Beschrijving**  
Creëert context-specifieke output templates voor een agent.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `agent_naam` | string | Naam van de agent (kebab-case) |
| `boundary_file` | string | Pad naar agent-boundary document |
| `template_naam` | string | Naam van de template |
| `output_type` | string | Type output (document/rapport/validatie) |
| `value_stream_fase` | string | Value stream fase (format: {vs}.{fase}) |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `voorbeeldstructuur` | string | Voorbeeldstructuur voor template |
| `referentie_templates` | list[string] | Referentie-templates |

#### Output

- **type:** Markdown  
- **bestand:** `artefacten/{vs}/{vs}.{fase}.{agent}/templates/{template-naam}.template.md`

---

## capability-architect

**Domein**: Agent-capability definiëring en boundary-vaststelling  
**Value Stream Fase**: aeo.02

### definieer-agent-boundary

**Beschrijving**  
Definieert de servicegrens van een agent als duurzame, expliciet aanroepbare capability.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `agent_naam` | string | Naam van de agent (kebab-case) |
| `value_stream_fase` | string | Value stream fase (format: {vs}.{fase}) |
| `korte_beschrijving` | string | Korte beschrijving van agent doel (1-3 zinnen) |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `template_file` | string | Override voor template locatie |

#### Output

- **type:** Markdown  
- **bestand:** `artefacten/{vs}/{vs}.{fase}.{agent}/{agent}.agent-boundary.md`

---

## ecosysteem-coordinator

**Domein**: Cross-cutting ecosysteem lifecycle management  
**Value Stream Fase**: aeo.02

### consulteer-canon

**Beschrijving**  
Raadpleegt mandarin-canon repository, extraheert grondslagen voor value stream en logt met commit SHA.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `agent` | string | Naam van de agent |
| `value_stream` | string | Value stream code (aeo/aod/fnd/sfw) |
| `intent` | string | Intent naam |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `canon_path` | string | Lokaal pad naar canon repository |
| `canon_github_url` | string | GitHub URL voor canon repository |
| `grondslagen` | string | Komma-gescheiden lijst van grondslagen |
| `workspace_file` | string | Workspace bestand dat canon raadpleegt |

#### Output

- **type:** Markdown (append)  
- **bestand:** `audit/canon-consult.log.md`

---

### genereer-instructies

**Beschrijving**  
Assembleert execution-ready instructiebestanden door canon-context, charter, contract en prompt samen te voegen.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `agent` | string | Naam van de agent |
| `intent` | string | Intent naam |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `execution_file` | string | Output bestandspad |
| `params` | list[string] | Extra parameters (key=value) |
| `skip_bootstrap` | boolean | Skip canon bootstrap |
| `method` | string | Initialisatie methode (manual/runner/pipeline) |

#### Output

- **type:** Markdown  
- **bestand:** `executions/{hash}.{agent}.{intent}.md`

---

### merge-configuraties

**Beschrijving**  
Aggregeert agent-specifieke task-configuraties naar één globale `.vscode/tasks.json`.

#### Input (parameters)

*Geen verplichte parameters*

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `filter_fase` | string | Filter op value stream fase |
| `tasks_folder` | string | Root folder voor tasks |
| `output_file` | string | Output bestand |
| `dry_run` | boolean | Toon wat gedaan zou worden |

#### Output

- **type:** JSON  
- **bestand:** `.vscode/tasks.json`

---

### valideer-agent-structuur

**Beschrijving**  
Controleert of agent-folders voldoen aan doctrine-voorgeschreven structuur.

#### Input (parameters)

*Geen verplichte parameters*

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `agent_naam` | string | Specifieke agent om te valideren |
| `value_stream_fase` | string | Value stream fase |
| `strict` | boolean | Stricte validatie modus |
| `output_format` | string | Output formaat (markdown/json) |

#### Output

- **type:** Console of Markdown  
- **bestand:** `audit/agent-structuur-validatie-{timestamp}.md`

---

# AOD — Architectuur Ontwerp

## core-framework-architect

**Domein**: ArchiMate-gebaseerde architectuur structurering  
**Value Stream Fase**: aod.02

### structureer-actieve-structuur

**Beschrijving**  
Structureert de actieve structuur (ArchiMate active elements) per laag met hiërarchie, dependencies en relaties.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `archimate_laag` | string | ArchiMate laag (Business/Application/Technology) |
| `bestand` | string | Bronbestand met structuur informatie |

#### Output

- **type:** Markdown  
- **bestand:** `artefacten/{vs}/{vs}.{fase}.core-framework-architect/landschappen/{domein}/core-framework-architect.structureer-actieve-structuur.md`

---

### structureer-gedrag

**Beschrijving**  
Structureert de gedragslaag (ArchiMate behavior elements) per laag met flow-, trigger- en serving-relaties.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `archimate_laag` | string | ArchiMate laag (Business/Application/Technology) |
| `bestand` | string | Bronbestand met gedragsinformatie |

#### Output

- **type:** Markdown  
- **bestand:** `artefacten/{vs}/{vs}.{fase}.core-framework-architect/landschappen/{domein}/core-framework-architect.structureer-gedrag.md`

---

### structureer-passieve-structuur

**Beschrijving**  
Structureert de passieve structuur (ArchiMate passive elements) per laag met inhoud, eigenaarschap en access-relaties.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `archimate_laag` | string | ArchiMate laag (Business/Application/Technology) |
| `bestand` | string | Bronbestand met structuur informatie |

#### Output

- **type:** Markdown  
- **bestand:** `artefacten/{vs}/{vs}.{fase}.core-framework-architect/landschappen/{domein}/core-framework-architect.structureer-passieve-structuur.md`

---

### structureer-totaal-view

**Beschrijving**  
Integreert actieve structuur, passieve structuur en gedragslaag in één coherente ArchiMate totaal view.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `archimate_laag` | string | ArchiMate laag (Business/Application/Technology) |
| `bestand` | string | Bronbestand met totaalstructuur |

#### Output

- **type:** Markdown  
- **bestand:** `artefacten/{vs}/{vs}.{fase}.core-framework-architect/landschappen/{domein}/core-framework-architect.structureer-totaal-view.md`

---

# FND — Fundamenten

## concept-curator

**Domein**: Conceptuele definitie en coherentie  
**Value Stream Fase**: fnd.02

### definieer-concept

**Beschrijving**  
Definieert en structureert concepten op basis van aangeleverde terminologie, toetst op eenduidigheid en consistentie.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `term` | string | Naam van het te definiëren concept |
| `definitie` | string | Voorgestelde definitie van het concept |
| `domein` | string | Domein waarbinnen concept wordt gedefinieerd |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `synoniemen` | string | Alternatieve termen (komma-gescheiden) |
| `relaties` | string | Gerelateerde concepten (format: relatie:concept) |
| `bron` | string | Bronvermelding van de definitie |

#### Output

- **type:** Markdown  
- **bestand:** `concepts/{domein}/{term}.md`

---

### rapporteer-concept-status

**Beschrijving**  
Inventariseert en rapporteert over status, definitiegraad en gebruik van concepten in het domeinmodel.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `domein` | string | Domein om te rapporteren |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `formaat` | string | Output formaat (markdown/json) |
| `status_filter` | string | Filter op concept status |

#### Output

- **type:** Markdown  
- **bestand:** `docs/concept-status/{domein}.status.md`

---

### valideer-concept-coherentie

**Beschrijving**  
Valideert of gebruikte concepten consistent en coherent zijn met geldende definitiekaders.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `artefact_bestand` | bestandspad | Te valideren artefact |
| `domein` | string | Domein voor conceptvalidatie |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `striktheid` | string | Validatie niveau (strict/normal/lenient) |

#### Output

- **type:** Markdown  
- **bestand:** `audit/concept-validatie/{artefact-naam}.validatie.md`

---

### verweef-concepten

**Beschrijving**  
Verbindt concepten met elkaar door expliciete relaties te leggen, borgt samenhang en traceerbaarheid.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `concept_bestand` | string | Pad naar concept bestand |

#### Output

- **type:** Markdown (update-in-place)  
- **bestand:** `{concept_bestand}`

---

## documentvertaler

**Domein**: Representatie-omvorming zonder betekeniswijziging  
**Value Stream Fase**: fnd.02

### zet-om-naar-docx

**Beschrijving**  
Zet een Markdown-document deterministisch om naar Word-document zonder wijziging van betekenis.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `markdown_file` | string | Pad naar Markdown bronbestand |
| `output_path` | string | Pad voor Word output |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `conversie_opties` | object | Conversie-instellingen |

#### Output

- **type:** Word document  
- **bestand:** `{output_path}` (.docx)

---

# SFW — Software Fabricage

## hypothese-vormer

**Domein**: Hypothese-formulering en toetsbaar maken  
**Value Stream Fase**: sfw.01

### beschrijf-hypothese

**Beschrijving**  
Beschrijft één expliciete, toetsbare probleem-oplossingshypothese met max 3 aannames als risico's.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `probleem` | string | Beschrijving huidige situatie (min 30 tekens) |
| `idee_voor_de_oplossing` | string | Het idee voor verbetering (min 30 tekens) |
| `auteur` | string | Naam van de bedenker |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `bronnen` | string | Documenten of mensen die informatie leverden |
| `context` | string | Situatie of omgeving waarin probleem speelt |
| `betrokkenen` | string | Wie zijn betrokken (gebruikers, teams, klanten) |

#### Output

- **type:** Markdown  
- **bestand:** `artefacten/sfw/sfw.01.hypothese-vormer/output/hypothese-{hypothese_code}.md`

---

### beschrijf-aannames

**Beschrijving**  
Expliciteert maximaal drie kritieke aannames als risico's die een hypothese dragen.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `hypothese_titel` | string | Titel van de hypothese |

#### Output

- **type:** Markdown (update Sectie 3)  
- **bestand:** Update van hypothese-document

---

### beschrijf-toetsbaarheid

**Beschrijving**  
Expliciteert toetsbaarheid van hypothese met criteria voor klopt/klopt-niet en eerste toetsstap.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `hypothese_statement` | string | Hypothese statement (min 30 tekens) |
| `auteur` | string | Naam van auteur |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `hypothese_bestand` | string | Pad naar hypothese document |
| `toetsingscontext` | string | Context voor toetsing |
| `beschikbare_metrics` | list[string] | Beschikbare meetwaarden |
| `acceptatie_drempel` | string | Drempelwaarden voor acceptatie |

#### Output

- **type:** Markdown  
- **bestand:** Standalone `toetsbaarheid-{datum}.md` of update Sectie 5

---

## thema-verwoorder

**Domein**: Thematische scope en epic structurering  
**Value Stream Fase**: sfw.02

### definieer-thematische-scope

**Beschrijving**  
Bakent thematische scope af binnen value stream op basis van hypothese-document.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `hypothese_bestand` | string | Pad naar hypothese document |
| `auteur` | string | Naam van auteur |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `toelichting` | string | Aanvullende toelichting |

#### Output

- **type:** Markdown  
- **bestand:** `artefacten/sfw/sfw.02.thema-verwoorder/scopes/`

---

### definieer-epic-structuur

**Beschrijving**  
Legt epic gestructureerd vast volgens SAFe-conventies binnen thematische context.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `thema_code` | string | Code van het thema |
| `auteur` | string | Naam van auteur |

#### Output

- **type:** Markdown  
- **bestand:** `artefacten/sfw/sfw.02.thema-verwoorder/epics/`

---

### definieer-verbeter-voorstel

**Beschrijving**  
Genereert meerdere verbetervoorstellen voor een thema op basis van scope en epic structuur.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `thema_code` | string | Code van het thema |
| `auteur` | string | Naam van auteur |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `toelichting` | string | Aanvullende toelichting |

#### Output

- **type:** Markdown  
- **bestand:** `artefacten/sfw/sfw.02.thema-verwoorder/verbeteringen/`

---

## gedragsspecificator

**Domein**: Gedragsspecificatie en Gherkin-vertaling  
**Value Stream Fase**: sfw.03

### specificeer-gedrag

**Beschrijving**  
Vertaalt informele business wensen naar gestructureerde gedragsspecificatie als tussenstap vóór Gherkin.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `context_bestand` | bestandspad | Bestand met context informatie |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `data_beschrijving_bestand` | bestandspad | Bestand met data beschrijving |
| `proces_beschrijving_bestand` | bestandspad | Bestand met proces beschrijving |

#### Output

- **type:** Markdown  
- **bestand:** `artefacten/sfw/sfw.03.gedragsspecificator/specificaties/{feature-naam}.md`

---

### valideer-scenario-consistentie

**Beschrijving**  
Valideert Gherkin-scenario's tegen functionele specificaties en ubiquitous language.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `feature_files` | string/bestandspaden | Gherkin feature files om te valideren |
| `specificatie_document` | referentie | Functionele specificatie als referentie |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `validation_rules` | string | Aanvullende validatieregels |

#### Output

- **type:** Markdown  
- **bestand:** `artefacten/sfw/sfw.03.gedragsspecificator/validatie-rapporten/rapport-{feature-naam}.md`

---

### vertaal-naar-gherkin

**Beschrijving**  
Vertaalt functionele requirement-specificaties naar formele, uitvoerbare Gherkin-scenario's.

#### Input (parameters)

**Verplicht:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `specificatie_document` | string | Pad naar specificatie document |
| `context` | string | Context voor vertaling |

**Optioneel:**

| Parameter | Type | Beschrijving |
|-----------|------|--------------|
| `extra_regels` | string | Aanvullende vertaalregels |
| `bestaande_feature_files` | paden | Bestaande feature files voor referentie |

#### Output

- **type:** Gherkin  
- **bestand:** `artefacten/sfw/sfw.03.gedragsspecificator/features/{feature-naam}.feature`

---

## Versiebeheer

| Versie | Datum | Wijziging |
|--------|-------|-----------|
| 1.0.0 | 2026-03-08 | Initieel overzicht gegenereerd door agent-curator |

---

**Gegenereerd door**: agent-curator  
**Intent**: rapporteer-prompts-overzicht  
**Conform template**: ecosysteem-agent-prompt-contracten.template.md
