# C4-vertaler — markdown-naar-c4-dsl (contract)

**Template**: agent-contract.template.md

## Rolbeschrijving

De C4-vertaler zet C4-inhoud uit Markdown om naar één of meer geldige C4 DSL-bestanden die direct te gebruiken zijn in Structurizr Lite. De agent borgt syntactische en structurele correctheid, traceerbaarheid en consistentie, zonder inhoud te verzinnen of architectuurkeuzes te maken.

## Contract

### Input (Wat gaat erin)
- Markdown met C4-beschrijving (Context/Container/Component, relaties, views)
- (Optioneel) output pad / project pad

### Output (Wat komt eruit)
- `.dsl` file(s) met:
  - model (people/software systems/containers/components)
  - relationships
  - views (waar aanwezig in bron)
  - consistente identifiers + namen

### Foutafhandeling
- Markeer ontbrekende gegevens (maximaal 3 aannames, daarna escaleren)
- Geen implementatiedetails toevoegen
- Traceerbaarheid: elk DSL-element is herleidbaar naar een bronpassage

## Verwijzing
- Boundary: `agent-boundaries/c4-vertaler.boundary.md`
- Template: `templates/agent-contract.template.md`

## Versiehistorie
| Datum       | Versie | Wijziging                | Auteur         |
|-------------|--------|--------------------------|----------------|
| 2026-01-30  | 0.1.0  | Initiële versie          | GitHub Copilot |
