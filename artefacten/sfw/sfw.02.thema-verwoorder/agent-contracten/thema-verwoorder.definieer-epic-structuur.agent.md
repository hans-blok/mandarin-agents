# thema-verwoorder — definieer-epic-structuur

## Rolbeschrijving (korte samenvatting)
Deze intent beschrijft het gestructureerd vastleggen van een epic volgens Safe-conventies binnen de thematische context van de value stream.

## Contract
### Input (wat gaat erin)
**Verplichte parameters**:
- epic_titel: string, titel van de epic
- epic_beschrijving: string, korte beschrijving van de epic

**Optionele parameters**:
- epic_scope: string, scope van de epic
- epic_stakeholders: lijst van betrokkenen
- epic_ksf: lijst van kritieke succesfactoren
- auteur: string
- datum: datum

### Output (wat komt eruit)
**Deliverables**: Markdown document met gestructureerde epic volgens template
**Outputlocaties**: artefacten/sfw/sfw.02.thema-verwoorder/epics/
**Formaat**: Markdown (.md) volgens template

### Foutafhandeling
- STOP: epic_titel of epic_beschrijving ontbreekt
- STOP: epic_titel niet uniek binnen value stream
- STOP: epic_beschrijving te vaag of te lang (>10 zinnen)
- Escaleer naar agent-curator bij onduidelijke scope of overlap

## Governance
- Volgt doctrine-agent-charter-normering.md (Principe 1, 2, 7, 9)
- Transparantie: alle output en beslissingen worden gelogd
- Canon-consultatie verplicht bij boundary-wijzigingen

## Metadata
Intent-ID: sfw.02.thema-verwoorder.definieer-epic-structuur  
Versie: 1.0.0  
Classificatie: Normerend, Ecosysteem, Inhoudelijk, Canon-gebonden
