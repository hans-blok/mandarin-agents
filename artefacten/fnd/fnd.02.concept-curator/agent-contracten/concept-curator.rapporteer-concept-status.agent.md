# Concept-Curator — Rapporteer Concept Status

## Rolbeschrijving (korte samenvatting)
De Concept-Curator inventariseert en rapporteert over de status, definitiegraad en het gebruik van concepten in het domeinmodel.
Inzichtelijk wordt gemaakt welke concepten 'stabiel', 'voorlopig' of 'verouderd' zijn.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- `domein`: Het te inventariseren concepten-domein (type: string, bijv. "mandarin-domeinconcepten").

**Optionele parameters**:
- `formaat`: Gewenst output-formaat ('markdown', 'json') (type: string, default: 'markdown').
- `status_filter`: Filter op status ('concept', 'stable', 'deprecated', 'all') (type: string, default: 'all').

### Output (wat komt eruit)

**Deliverables**:
- Een overzichtelijk statusrapport van het concepten-domein.
- Lijst met 'wees'-concepten (geen gebruik bekend) en 'holle' concepten (geen definitie).

**Outputlocaties**:
- `docs/concept-status/{domein}.status.md`

**Formaat**:
- Markdown (.md) met status-tabellen.

### Foutafhandeling

De agent stopt wanneer:
- Het domein niet bestaat of geen concepten bevat.

Escalatie:
- Rapporteer structurele kwaliteitsproblemen (grote hoeveelheid 'holle' concepten) aan de domeinbeheerder.

## Governance

**Doctrine-naleving:**
- Borgt inzicht in de volwassenheid van het begrippenkader.
- Ondersteunt life-cycle management van concepten.

## Metadata

**Intent-ID**: `fnd.02.concept-curator.rapporteer-concept-status`
**Versie**: 1.0.0
**Classificatie**: Curator, Beschrijvend
