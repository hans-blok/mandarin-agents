# Concept-Curator — Valideer Concept Coherentie

## Rolbeschrijving (korte samenvatting)
De Concept-Curator valideert of gebruikte concepten consistent en coherent zijn met de geldende definitiekaders en signaleert afwijkingen of tegenstrijdigheden. Hij stuurt niet bij op beleid, maar markeert waar begrippen afwijken van hun canonieke betekenis.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- `artefact_bestand`: Het te valideren document of bestand (type: bestandspad).
- `domein`: Het referentiekader waartegen gevalideerd wordt (type: string, bijv. "mandarin-domeinconcepten").

**Optionele parameters**:
- `striktheid`: Niveau van validatie ('strict', 'normal', 'lenient') (type: string, default: 'normal').

### Output (wat komt eruit)

**Deliverables**:
- Een validatierapport met bevindingen (inconsistenties, onbekende termen, dubbelzinnigheden).

**Outputlocaties**:
- `audit/concept-validatie/{artefact-naam}.validatie.md`

**Formaat**:
- Markdown (.md) met tabellen van bevindingen.

### Foutafhandeling

De agent stopt wanneer:
- Het te valideren artefact niet leesbaar is.
- Het referentiedomein niet beschikbaar is.

Escalatie:
- Rapporteer ernstige begripsverwarring aan de auteur van het artefact.

## Governance

**Doctrine-naleving:**
- Controleert op consistent gebruik van de Ubiquitous Language.
- Signaleert 'drift' in betekenis van concepten.

## Metadata

**Intent-ID**: `fnd.02.concept-curator.valideer-concept-coherentie`
**Versie**: 1.0.0
**Classificatie**: Curator, Inhoudelijk, Kwaliteitsborging
