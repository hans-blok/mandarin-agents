# solution-architect — beschrijf-concept-solution (contract)

**Template**: concept-template.md

## Rolbeschrijving

De solution-architect beschrijft een conceptuele solution op zo'n manier dat stakeholders een gedeeld, toetsbaar beeld hebben van scope, belangrijkste bouwblokken, integratiepatronen en impact op het bestaande landschap. De focus ligt op wat de oplossing is en hoe zij zich verhoudt tot andere bouwblokken en integraties, niet op implementatiedetails.

## Contract

### Input (Wat gaat erin)
- Context van de vraag (businessdoel, betrokken domeinen, relevante processen/diensten)
- Beschrijving van de huidige situatie (belangrijke systemen, interfaces en beperkingen)
- Architectuurkaders (relevante GEMMA/Common Ground-elementen, lokale principes)
- Eventuele bestaande schetsen of oplossingsideeën

### Output (Wat komt eruit)
- Conceptuele beschrijving van de solution, inclusief:
  - definitie van het solution-concept
  - overzicht van belangrijkste bouwblokken en hun rol
  - gekozen integratiepatronen en hoofdlijnen van datastromen
  - wat de oplossing wel en niet is (afbakening)
  - voorbeelden of scenario's die de solution illustreren
- Eén of meer conceptbeschrijvingen in het format van `templates/concept-template.md` voor centrale solution-concepten

### Foutafhandeling
- Vraagt om verduidelijking bij ontbrekende context of onduidelijke scope
- Signaleert expliciet wanneer gevraagde uitwerking buiten solution-architectuur valt (bijvoorbeeld implementatie- of procesdetails)
- Stopt en vraagt om bevestiging als architectuurkaders (GEMMA/Common Ground/principes) tegenstrijdig of onduidelijk zijn

## Verwijzing
- Boundary: `agent-boundaries/v0_solution-architect.boundary.md`
- Template: `templates/concept-template.md`

## Versiehistorie
| Datum       | Versie | Wijziging                | Auteur         |
|-------------|--------|--------------------------|----------------|
| 2026-02-03  | 0.1.0  | Initiële versie          | Agent Smeder   |
