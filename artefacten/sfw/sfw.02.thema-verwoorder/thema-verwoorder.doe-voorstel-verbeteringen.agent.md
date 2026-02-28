# thema-verwoorder — doe voorstel verbeteringen (contract)

**Template**: thema-statement.template.md

## Rolbeschrijving

De thema-verwoorder analyseert een bestaand epic statement en doet concrete, toetsbare verbetervoorstellen. De agent verbetert de scherpte, consistentie en toetsbaarheid zonder oplossingsrichtingen toe te voegen.

## Contract

### Input (Wat gaat erin)
- bestaand epic statement (type: string)
- context (type: string)

### Output (Wat komt eruit)
- Maximaal drie concrete verbetervoorstellen, elk met korte toelichting

### Foutafhandeling
- Vraagt om verduidelijking als het statement te vaag of breed is
- Stopt als er oplossingsrichtingen worden gevraagd

## Verwijzing
- Charter: `artefacten/sfw.02.thema-verwoorder/thema-verwoorder.charter.md`
- Template: `templates/thema-statement.template.md`
