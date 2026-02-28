# Templates voor core-framework-architect

Deze folder bevat **context-specifieke output templates** voor alle artefacten van de **core-framework-architect** agent.

## Overzicht

De templates zijn gegenereerd door de **agent-smeder** (intent: `leg-vast-templates`) conform het "Prompt First" principe en zijn **inhoudelijk afgestemd** op de boundary van de core-framework-architect.
De templates beschrijven de **output-structuur** die de agent moet opleveren: ArchiMate-gebaseerde architectuurdocumenten.

## Template structuur

### Per intent (output templates):
- `core-framework-architect.{intent}.template.md` - Structuur van het ArchiMate document dat de agent oplevert

**Geen charter of runner templates**: Deze zijn eigendom van agent-smeder en worden gebruikt bij andere intents (`leg-vast-agent-charter`, `leg-vast-agent-runner`).

## Intents

De volgende intents zijn gedefinieerd in de boundary en vertaald naar output templates:

1. **structureer-gedrag**  
   Template: `core-framework-architect.structureer-gedrag.template.md`  
   Output: ArchiMate Behavior Layer definitie met processen, functies en relaties

2. **structureer-actieve-structuur**  
   Template: `core-framework-architect.structureer-actieve-structuur.template.md`  
   Output: ArchiMate Active Structure met agents, componenten en hun mapping

3. **structureer-totaal-view**  
   Template: `core-framework-architect.structureer-totaal-view.template.md`  
   Output: Integrale ArchiMate view met cross-layer relaties

## Volgende stappen

Deze templates dienen als basis voor de output van de core-framework-architect.
Tijdens de executie van de agent zal de LLM deze structuur gebruiken om specifieke architectuur-beslissingen vast te leggen.

**Vervolg in agent-smeder workflow**:
1. Agent-contracten vastleggen (intent: `leg-vast-agent-contract`)
2. Prompts vastleggen (intent: `leg-vast-agent-prompt`)
3. Charter vastleggen (intent: `leg-vast-agent-charter`)
4. Runners vastleggen (intent: `leg-vast-agent-runner`)

## Metadata

**Agent**: core-framework-architect  
**Value Stream**: Agent Ontwerp & Doorontwikkeling (aod)  
**Fase**: 02 - Ecosysteeminrichting  
**Gegenereerd door**: agent-smeder.leg-vast-templates (Execution ID: df0f)  
**Datum**: 2026-02-15  
**Canon Referentie**: e00a176  
