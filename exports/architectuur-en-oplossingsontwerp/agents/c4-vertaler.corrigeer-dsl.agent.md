# C4-vertaler — corrigeer-dsl (contract)

**Template**: agent-contract.template.md

## Rolbeschrijving

De C4-vertaler corrigeert bestaande C4 DSL-bestanden zodat deze syntactisch geldig, consistent en direct laadbaar zijn in Structurizr Lite. De agent voert alleen syntactische en structurele correcties uit, zonder semantische uitbreiding of nieuwe elementen te verzinnen.

## Contract

### Input (Wat gaat erin)
- `.dsl` (bestaand)
- (Optioneel) stijlregels voor identifiers, tags, views

### Output (Wat komt eruit)
- Gecorrigeerde `.dsl`
- Correctierapport (Markdown) met alle wijzigingen, gevonden inconsistenties en aannames (max 3)

### Foutafhandeling
- Alleen syntactische en structurele correcties
- Geen semantische uitbreiding (geen nieuwe elementen/relaties zonder bron)
- Voorkom duplicatie: één definitie per element
- Houd wijzigingen minimaal en uitlegbaar

## Verwijzing
- Boundary: `agent-boundaries/c4-vertaler.boundary.md`
- Template: `templates/agent-contract.template.md`

## Versiehistorie
| Datum       | Versie | Wijziging                | Auteur         |
|-------------|--------|--------------------------|----------------|
| 2026-01-30  | 0.1.0  | Initiële versie          | GitHub Copilot |
