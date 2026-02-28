# thema-verwoorder — definieer-thematische-scope

## Rolbeschrijving (korte samenvatting)
Deze intent beschrijft het afbakenen en documenteren van de thematische scope binnen de value stream.

## Contract
### Input (wat gaat erin)
**Verplichte parameters**:
- thema: string, naam van het thema
- beschrijving: string, korte beschrijving van het thema

**Optionele parameters**:
- onderwerpen: lijst van afgebakende onderwerpen
- uitsluitingen: lijst van uitgesloten onderwerpen
- relevante_epics: lijst van relevante epics
- auteur: string
- datum: datum

### Output (wat komt eruit)
**Deliverables**: Markdown document met thematische scope volgens template
**Outputlocaties**: artefacten/sfw/sfw.02.thema-verwoorder/scopes/
**Formaat**: Markdown (.md) volgens template

### Foutafhandeling
- STOP: thema of beschrijving ontbreekt
- STOP: thema niet uniek binnen value stream
- STOP: beschrijving te vaag of te lang (>10 zinnen)
- Escaleer naar agent-curator bij overlap of onduidelijke scope

## Governance
- Volgt doctrine-agent-charter-normering.md (Principe 1, 2, 7, 9)
- Transparantie: alle output en beslissingen worden gelogd
- Canon-consultatie verplicht bij boundary-wijzigingen

## Metadata
Intent-ID: sfw.02.thema-verwoorder.definieer-thematische-scope  
Versie: 1.0.0  
Classificatie: Normerend, Ecosysteem, Inhoudelijk, Canon-gebonden
