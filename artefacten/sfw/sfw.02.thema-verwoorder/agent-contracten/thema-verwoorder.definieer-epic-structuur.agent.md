# thema-verwoorder — definieer-epic-structuur

## Rolbeschrijving (korte samenvatting)
Deze intent beschrijft het gestructureerd vastleggen van een epic volgens SAFe-conventies binnen de thematische context. De agent leest een eerder gedefinieerde thematische scope en structureert een epic binnen die context.

## Contract
### Input (wat gaat erin)
**Verplichte parameters**:
- thema_code: string, unieke identificatiecode van het thema
- auteur: string, naam van de auteur

**Opmerking**: De agent zoekt de thematische scope op basis van de thema_code in artefacten/sfw/sfw.02.thema-verwoorder/scopes/, analyseert de context, en bepaalt zelf:
- Epic titel
- Epic beschrijving
- Epic doelstelling (epic_doel)
- Epic scope
- Relevante stakeholders
- Kritieke succesfactoren
- SAFe Epic Statement elementen
- Datum (wordt automatisch gegenereerd)

### Output (wat komt eruit)
**Deliverables**: Markdown document met gestructureerde epic volgens template (inclusief SAFe Epic Statement)
**Outputlocaties**: artefacten/sfw/sfw.02.thema-verwoorder/epics/
**Formaat**: Markdown (.md) volgens template

### Foutafhandeling
- STOP: thema_code of auteur ontbreekt
- STOP: thematische scope bestand voor thema_code niet gevonden of niet toegankelijk
- STOP: thematische scope bevat onvoldoende informatie voor epic structuur
- STOP: epic_titel niet uniek binnen value stream
- Escaleer naar agent-curator bij onduidelijke scope of overlap

## Governance
- Volgt doctrine-agent-charter-normering.md (Principe 1, 2, 7, 9)
- Transparantie: alle output en beslissingen worden gelogd
- Canon-consultatie verplicht bij boundary-wijzigingen

## Metadata
Intent-ID: sfw.02.thema-verwoorder.definieer-epic-structuur  
Versie: 1.0.0  
Classificatie: Normerend, Ecosysteem, Inhoudelijk, Canon-gebonden
