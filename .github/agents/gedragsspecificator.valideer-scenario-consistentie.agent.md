---
agent: gedragsspecificator
intent: valideer-scenario-consistentie
intent-id: sfw.03.gedragsspecificator.02
versie: 0.1.0
digest: 9b15
status: vers
---
# Gedragsspecificator — Valideer Scenario Consistentie

## Rolbeschrijving (korte samenvatting)
Valideert Gherkin-scenario's tegen functionele specificaties en ubiquitous language. Rapporteert logische inconsequenties, ontbrekende definities en gaten in de scenario-dekking.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- `feature_files`: Een of meerdere feature files (.feature) die moeten worden gevalideerd (type: string of bestandspaden).
- `specificatie_document`: Het functionele specificatiedocument waartegen wordt gevalideerd (referentie).

**Optionele parameters**:
- `validation_rules`: Aanvullende specifieke validatieregels (bijv. stijl, naming conventions).

### Output (wat komt eruit)

**Deliverables**:
- Een validatierapport met bevindingen en aanbevelingen, volgens `gedragsspecificator.valideer-scenario-consistentie.template.md`.

**Outputlocaties**:
- `artefacten/sfw/sfw.03.gedragsspecificator/validatie-rapporten/rapport-{feature-naam}.md`

**Formaat**:
- Markdown (.md)

**Contractuele templatebinding**:

```yaml
template: templates/gedragsspecificator.valideer-scenario-consistentie.template.md
```

### Foutafhandeling

De agent stopt wanneer:
- De input features of specificaties niet kunnen worden gelezen.
- Er geen relatie is gevonden tussen de specificatie en de features, waardoor validatie zinloos is.

Escalatie:
- Rapporteer ernstige inconsequenties of definitieconflicten terug naar de specificatie-auteur.

## Governance

**Doctrine-naleving:**
- Controleert of terminologie in features consistent is met de specificatie.
- Controleert op ambiguïteit en interpreteerbaarheid.

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

## Metadata

**Intent-ID**: `sfw.03.gedragsspecificator.valideer-scenario-consistentie`
**Versie**: 1.0.0
**Classificatie**: Structuurrealiserend (validatie), Curator (controleert kwaliteit)
