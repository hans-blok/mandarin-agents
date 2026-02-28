# thema-verwoorder — definieer-verbeter-voorstel

## Rolbeschrijving (korte samenvatting)
Deze intent beschrijft het voorstellen van verbeteringen aan bestaande epics of thematische structuren binnen de value stream.

## Contract
### Input (wat gaat erin)
**Verplichte parameters**:
- onderwerp: string, onderwerp van de verbetering
- huidige_situatie: string, beschrijving van de huidige situatie
- gewenste_situatie: string, beschrijving van de gewenste situatie

**Optionele parameters**:
- voorgestelde_verbetering: string
- impact: string
- randvoorwaarden: string
- auteur: string
- datum: datum

### Output (wat komt eruit)
**Deliverables**: Markdown document met verbeter-voorstel volgens template
**Outputlocaties**: artefacten/sfw/sfw.02.thema-verwoorder/verbeteringen/
**Formaat**: Markdown (.md) volgens template

### Foutafhandeling
- STOP: onderwerp, huidige_situatie of gewenste_situatie ontbreekt
- STOP: voorgestelde_verbetering te vaag of niet onderbouwd
- STOP: impact niet beschreven bij majeure wijziging
- Escaleer naar agent-curator bij onduidelijke verbetering of overlap

## Governance
- Volgt doctrine-agent-charter-normering.md (Principe 1, 2, 7, 9)
- Transparantie: alle output en beslissingen worden gelogd
- Canon-consultatie verplicht bij boundary-wijzigingen

## Metadata
Intent-ID: sfw.02.thema-verwoorder.definieer-verbeter-voorstel  
Versie: 1.0.0  
Classificatie: Normerend, Ecosysteem, Inhoudelijk, Canon-gebonden
