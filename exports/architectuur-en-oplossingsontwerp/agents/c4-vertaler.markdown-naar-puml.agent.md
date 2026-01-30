# c4-vertaler — markdown-naar-puml (contract)

**Template**: puml-diagram.template.puml

## Rolbeschrijving

De c4-vertaler zet een Markdown-beschrijving van een architectuurmodel om naar een PlantUML (PUML) representatie. Dit contract beschrijft de interface voor deze vertaling.

## Contract

### Input (Wat gaat erin)
- markdown_beschrijving (type: string; Markdown-tekst van het model)
- context (type: string; optioneel, extra toelichting of scope)

### Output (Wat komt eruit)
- puml_code (type: string; geldige PlantUML-code die het model weergeeft)
- waarschuwingen (type: lijst van string; optioneel, bij niet-ondersteunde constructies)

### Foutafhandeling
- Stopt en geeft een duidelijke foutmelding als de Markdown niet valide of niet te parsen is.
- Vraagt om verduidelijking als de input te vaag of onvolledig is.

## Verwijzing
- Charter: `exports/architectuur-en-oplossingsontwerp/charters-agents/c4-vertaler.charter.md`
- Template: `templates/puml-diagram.template.puml`