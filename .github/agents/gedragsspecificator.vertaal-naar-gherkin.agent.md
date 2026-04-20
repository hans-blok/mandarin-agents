---
agent: gedragsspecificator
intent: vertaal-naar-gherkin
intent-id: sfw.03.gedragsspecificator.03
versie: 0.1.0
digest: d9ff
status: vers
---
# Gedragsspecificator — Vertaal naar Gherkin

## Rolbeschrijving (korte samenvatting)
Vertaalt functionele requirement-specificaties en acceptatiecriteria naar formele, uitvoerbare Gherkin-scenario's (Given/When/Then).

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- `specificatie_document`: Het gestructureerde requirement-document (output van 'specificeer-gedrag') of een vergelijkbare functionele beschrijving.
- `context`: Beschrijft de feature of capability waarvoor scenario's moeten worden opgesteld.

**Optionele parameters**:
- `extra_regels`: Specifieke bedrijfsregels of constraints die in acht moeten worden genomen.
- `bestaande_feature_files`: Paden naar bestaande `.feature` bestanden om consistentie in taalgebruik te borgen.

### Output (wat komt eruit)

**Deliverables**:
- Een of meerdere `.feature` bestanden met Gherkin-scenario's.

**Outputlocaties**:
- `artefacten/sfw/sfw.03.gedragsspecificator/features/{feature-naam}.feature`

**Formaat**:
- Gherkin (Feature file format: `.feature`).

**Contractuele templatebinding**:

```yaml
template: templates/gedragsspecificator.vertaal-naar-gherkin.template.md
```

### Foutafhandeling

De agent stopt wanneer:
- De specificatie onduidelijk is of ontbrekende informatie bevat waardoor scenario's niet eenduidig kunnen worden opgesteld.
- Er inconsistenties worden ontdekt in de input (bijv. tegenstrijdige acceptatiecriteria).

Escalatie:
- Rapporteer ambiguïteit terug naar de bron (specificatie-eigenaar).

## Governance

**Doctrine-naleving:**
- Gebruikt consistent de Ubiquitous Language zoals gedefinieerd in de specificatie.
- Scenario's zijn onafhankelijk en atomair.
- Gebruikt declaratieve stijl (beschrijf *wat*, niet *hoe* - vermijd UI-details tenzij relevant).

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

## Metadata

**Intent-ID**: `sfw.03.gedragsspecificator.vertaal-naar-gherkin`
**Versie**: 1.0.0
**Classificatie**: Representatieomvormend, Inhoudelijk
