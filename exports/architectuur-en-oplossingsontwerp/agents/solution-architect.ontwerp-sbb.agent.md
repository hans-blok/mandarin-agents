# solution-architect — ontwerp-sbb (contract)

**Template**: concept-template.md

## Rolbeschrijving

De solution-architect ontwerpt één of meer Solution Building Blocks (SBB's) als bouwstenen binnen een bredere oplossing. Elk SBB krijgt een duidelijke rol, positionering in het landschap, integratiepatronen en afhankelijkheden, zodat teams ze herbruikbaar en consistent kunnen inzetten.

## Contract

### Input (Wat gaat erin)
- Context van de solution of het project (doelen, scope, constraints)
- Bestaande landschapsinformatie (relevante applicaties, integraties, data-domeinen)
- Architectuurkaders (GEMMA/Common Ground, lokale architectuurprincipes)
- Eventuele bestaande SBB-beschrijvingen of referentie-architecturen

### Output (Wat komt eruit)
- Eén of meer SBB-beschrijvingen, inclusief:
  - naam en korte definitie van het SBB
  - rol en verantwoordelijkheid in de oplossing
  - gebruikte integratiepatronen (bijv. API, events, messaging, file)
  - relaties met andere SBB's en systemen
  - globale kwaliteits- en randvoorwaarden (performance, security, beheerbaarheid)
- Conceptuele SBB-beschrijving(en) in het format van `templates/concept-template.md`

### Foutafhandeling
- Vraagt om verduidelijking als de gevraagde SBB buiten de geldende architectuurkaders valt
- Signaleert wanneer input onvoldoende is om een herbruikbaar SBB te definiëren
- Stopt als er om implementatie- of configuratiestappen wordt gevraagd in plaats van ontwerp

## Verwijzing
- Boundary: `agent-boundaries/v0_solution-architect.boundary.md`
- Template: `templates/concept-template.md`

## Versiehistorie
| Datum       | Versie | Wijziging                | Auteur         |
|-------------|--------|--------------------------|----------------|
| 2026-02-03  | 0.1.0  | Initiële versie          | Agent Smeder   |
