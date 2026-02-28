# Concept-Curator — Definieer Concept

## Rolbeschrijving (korte samenvatting)
De Concept-Curator definieert en structureert concepten op basis van aangeleverde terminologie, zodat deze coherent en traceerbaar worden vastgelegd binnen de domeinconcepten. Hij toetst of de definitie voldoet aan de eisen voor eenduidigheid en consistentie.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `concept-curator.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- `term`: De naam van het te definiëren concept (type: string).
- `definitie`: De voorgestelde definitie van het concept (type: string).
- `domein`: Het domein waarbinnen het concept wordt gedefinieerd (type: string, bijv. "mandarin-domeinconcepten").

**Optionele parameters**:
- `synoniemen`: Lijst van alternatieve termen (type: string, komma-gescheiden).
- `relaties`: Lijst van gerelateerde concepten (type: string, structuur: "relatie:concept").
- `bron`: Bronvermelding van de definitie (type: string).

### Output (wat komt eruit)

**Deliverables**:
- Een gestructureerd concept-bestand (`.md`) dat voldoet aan de geldende taxonomie.
- Logging van eventuele inconsistenties indien de definitie strijdig is met bestaande concepten.

**Outputlocaties**:
- `concepts/{domein}/{term}.md`

**Formaat**:
- Markdown (.md) volgens `concept.template.md`.

### Foutafhandeling

De agent stopt wanneer:
- De verplichte parameters (`term`, `definitie`, `domein`) ontbreken.
- Het domein niet bestaat of niet toegankelijk is.
- De definitie te vaag of circulair is (bijv. "Een agent is een agent").

Escalatie:
- Bij fundamentele begripsverwarring wordt geëscaleerd naar de domein-eigenaar of architect.

## Governance

**Doctrine-naleving:**
- Volgt de principes van eenduidige begripsvorming.
- Markeert concepten als 'concept', 'vastgesteld' of 'vervallen'.

## Metadata

**Intent-ID**: `fnd.02.concept-curator.definieer-concept`
**Versie**: 1.0.0
**Classificatie**: Curator, Inhoudelijk
