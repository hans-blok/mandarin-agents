---
agent: ecosysteem-beschrijver
template_naam: beschrijf-ecosysteem-value-streams-agents
versie: 1.0.0
output_type: document
doel: Geeft een gestructureerd overzicht van alle value streams en hun agents in het ecosysteem â€” welke agents per value stream en fase, inclusief hun boundary-classificatie, domein en intentaantal.
---

# Template: Ecosysteem Value Streams & Agents Overzicht

## Doel en gebruik

Dit template structureert de output van de intent `beschrijf-ecosysteem-value-streams-agents`. Het produceert een leesbaar overzicht van alle value streams, hun fasen, en de agents die daarbinnen actief zijn. Per agent wordt de boundary-classificatie en het intentaantal opgenomen. Het document is beschrijvend â€” geen evaluatie, geen normering.

Gebruikt door: `beschrijf-ecosysteem-value-streams-agents`

## Structuur

```markdown
---
agent: ecosysteem-beschrijver
intent: beschrijf-ecosysteem-value-streams-agents
value_stream_fase: <value_stream_fase>
scope: <scope-omschrijving>
timestamp: <yyyy-mm-dd HH:MM>
---

# Ecosysteem: Value Streams & Agents â€” <scope>

## Inleiding

<Korte beschrijving van de scope: welke value streams in scope, basis-bronbestanden, hoe agents zijn geÃ¯dentificeerd.>

## Value streams

### <value-stream-code> â€” <value-stream-naam>

**Beschrijving**: <Ã©Ã©n zin over wat deze value stream voortbrengt of regisseert>

#### Fase <fase-code> â€” <fase-naam>

| Agent | Korte boundary-zin | Domein | Intents |
|-------|-------------------|--------|---------|
| <agent-naam> | <eerste zin uit boundary "doelstelling" sectie> | <domein uit charter/boundary> | <n> |
| <agent-naam> | ... | ... | ... |

---

### <value-stream-code-2> â€” <value-stream-naam-2>

[herhaal structuur]

---

## Agents-matrix

Totaaloverzicht van alle agents in scope, gesorteerd op value stream en fase.

| Agent | Value stream | Fase | Output-type | Intents |
|-------|-------------|------|------------|---------|
| <agent-naam> | <vs-code> | <fase> | <classificatie: document / artefact / ...> | <n> |
| ... | ... | ... | ... | ... |

**Totaal agents in scope**: <n>  
**Totaal value streams in scope**: <n>

## Bronbestanden

- `artefacten/<vs>/<vs>.<fase>.<agent>/<agent-naam>.agent-boundary.md`
- `artefacten/<vs>/<vs>.<fase>.<agent>/<agent-naam>.charter.md` (indien aanwezig)
```

## Placeholders

| Placeholder | Type | Beschrijving | Verplicht |
|-------------|------|--------------|-----------|
| `<value_stream_fase>` | string | bijv. "aeo.02" | Ja |
| `<scope-omschrijving>` | string | bijv. "alle value streams" of "aeo.02" | Ja |
| `<timestamp>` | string | ISO 8601 datetime | Ja |
| `<value-stream-code>` | string | bijv. "aeo", "fnd", "sfw" | Ja |
| `<value-stream-naam>` | string | volledige naam van de value stream | Ja |
| `<fase-code>` | string | bijv. "02" | Ja |
| `<agent-naam>` | string | kebab-case agent naam | Ja |
| `<boundary-zin>` | string | eerste zin uit doelstelling in boundary | Ja |
| `<domein>` | string | domein of context uit charter/boundary | Ja |
| `<n> (intents)` | integer | aantal intents in de agent-boundary | Ja |
| `<output-type>` | string | bijv. document, artefact, rapport | Ja |

## Validatie-criteria

- âœ“ Elke bekende value stream heeft een eigen sectie
- âœ“ Alle agents in scope staan in de agents-matrix
- âœ“ De boundary-zin is de eerste zin uit de "doelstelling"- of "korte-beschrijving"-sectie in het boundary-document
- âœ“ Intents-teller klopt met het aantal intents in het boundary-document
- âœ“ Document bevat geen evaluatie of oordeel over agents
- âœ“ Bronbestanden zijn expliciet vermeld

## Voorbeeld-output

```markdown
---
agent: ecosysteem-beschrijver
intent: beschrijf-ecosysteem-value-streams-agents
value_stream_fase: aeo.02
scope: alle value streams
timestamp: 2026-03-21 10:00
---

# Ecosysteem: Value Streams & Agents â€” alle value streams

## Inleiding

Overzicht van alle agents in het mandarin-agents ecosysteem, gegroepeerd per value stream en fase.
Bronbestanden: alle boundary- en charter-documenten in de artefacten/-map.

## Value streams

### aeo â€” Agent Engineering & Orchestration

**Beschrijving**: Omvat het ontwerp, de implementatie en het beheer van agents in het ecosysteem.

#### Fase 02 â€” Implementatie

| Agent | Korte boundary-zin | Domein | Intents |
|-------|-------------------|--------|---------|
| agent-curator | Beheert de kwaliteit en consistentie van het agent-ecosysteem. | Kwaliteitsbeheer | 6 |
| agent-engineer | Implementeert agents op basis van contracten en templates. | Implementatie | 4 |
| agent-ontwerper | Ontwerpt agent-structuren op basis van boundaries en intents. | Ontwerp | 3 |
| capability-architect | Definieert de capability-grenzen van agents. | Architectuur | 2 |
| ecosysteem-coordinator | CoÃ¶rdineert het gehele agent-ecosysteem. | CoÃ¶rdinatie | 5 |

## Agents-matrix

| Agent | Value stream | Fase | Output-type | Intents |
|-------|-------------|------|------------|---------|
| agent-curator | aeo | 02 | rapport | 6 |
| agent-engineer | aeo | 02 | artefact | 4 |
| agent-ontwerper | aeo | 02 | artefact | 3 |
| capability-architect | aeo | 02 | document | 2 |
| ecosysteem-coordinator | aeo | 02 | document | 5 |

**Totaal agents in scope**: 5  
**Totaal value streams in scope**: 1

## Bronbestanden

- artefacten/aeo/aeo.02.agent-curator/agent-curator.agent-boundary.md
- artefacten/aeo/aeo.02.agent-engineer/agent-engineer.agent-boundary.md
- artefacten/aeo/aeo.02.agent-ontwerper/agent-ontwerper.agent-boundary.md
- artefacten/aeo/aeo.02.capability-architect/capability-architect.agent-boundary.md
- artefacten/fnd/fnd.01.ecosysteem-coordinator/ecosysteem-coordinator.agent-boundary.md
```

## Gebruiksinstructies

1. Bepaal de scope (Ã©Ã©n fase, meerdere fasen, of alle value streams).
2. Lees per agent het boundary-document om de boundary-zin, het domein en het intentaantal te extraheren.
3. Groepeer agents per value stream en per fase.
4. Vul de agents-matrix met alle agents in scope.
5. Schrijf de inleiding op basis van de scope.
6. Schrijf het document weg conform de output-locatie-afspraak.

## Versiebeheer

| Versie | Datum | Wijziging |
|--------|-------|-----------|
| 1.0.0 | 2026-03-21 | InitiÃ«le template voor ecosysteem-beschrijver |

---

**Template-categorie**: Agent-specifiek  
**Gebruikt door intents**: beschrijf-ecosysteem-value-streams-agents
