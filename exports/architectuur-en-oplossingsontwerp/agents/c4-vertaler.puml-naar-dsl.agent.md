# c4-vertaler — puml-naar-dsl (contract)

**Template**: -

## Rolbeschrijving

De c4-vertaler zet een PlantUML (PUML) architectuurdiagram om naar een C4 DSL-bestand. Dit contract beschrijft de interface voor deze vertaling.

## Contract

### Input (Wat gaat erin)
- puml_code (type: string; geldige PlantUML-code van het model)
- context (type: string; optioneel, extra toelichting of scope)

### Output (Wat komt eruit)
- dsl_bestand (type: string; geldige C4 DSL-code die het model weergeeft)
- waarschuwingen (type: lijst van string; optioneel, bij niet-ondersteunde constructies)

### Foutafhandeling
- Stopt en geeft een duidelijke foutmelding als de PUML niet valide of niet te parsen is.
- Vraagt om verduidelijking als de input te vaag of onvolledig is.

## Verwijzing
- Charter: `exports/architectuur-en-oplossingsontwerp/charters-agents/c4-vertaler.charter.md`
- Template: `templates/c4-dsl.template.dsl`
