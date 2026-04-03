---
agent: gedragsspecificator
intent: specificeer-gedrag
versie: 0.1.0
digest: ebcd
status: vers
---
# Gedragsspecificator — Specificeer Gedrag

## Rolbeschrijving (korte samenvatting)
De gedragsspecificator vertaalt informele business wensen, user stories en randvoorwaarden naar een gestructureerde gedragsspecificatie. Dit dient als tussenstap om ambiguïteit te verwijderen voordat formele Gherkin-scenario's worden geschreven.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- `context_bestand`: Pad of bestandsnaam naar het document met de contextbeschrijving (type: bestandspad).

**Optionele parameters**:
- `data_beschrijving_bestand`: Pad of bestandsnaam naar de beschrijving van de data (type: bestandspad).
- `proces_beschrijving_bestand`: Pad of bestandsnaam naar de beschrijving van het proces (type: bestandspad).

### Output (wat komt eruit)

**Deliverables**:
- Een ingevuld specificatiedocument op basis van `gedragsspecificator.specificeer-gedrag.template.md`.

**Outputlocaties**:
- `artefacten/sfw/sfw.03.gedragsspecificator/specificaties/{feature-naam}.md`

**Formaat**:
- Markdown (.md)

### Foutafhandeling

De agent stopt wanneer:
- De input te vaag of tegenstrijdig is om een eenduidige specificatie van af te leiden.
- Er essentiële context ontbreekt (bijv. "wie is de gebruiker?").

Escalatie:
- Bij onduidelijke requirements: vraag verduidelijking aan de aanvrager (Product Owner rol).

## Governance

**Doctrine-naleving:**
- Volgt de template-structuur strikt.
- Markeert aannames expliciet als 'Openstaande Vragen' (geen impliciete aannames).

## Metadata

**Intent-ID**: `sfw.03.gedragsspecificator.specificeer-gedrag`
**Versie**: 1.0.0
**Classificatie**: Structuurrealiserend, Inhoudelijk
