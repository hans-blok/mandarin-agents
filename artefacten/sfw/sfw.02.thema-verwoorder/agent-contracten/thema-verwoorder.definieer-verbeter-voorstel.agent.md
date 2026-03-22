# thema-verwoorder — definieer-verbeter-voorstellen

## Rolbeschrijving (korte samenvatting)
Deze intent beschrijft het genereren van meerdere verbetervoorstellen voor een thema op basis van de thematische scope en gedefinieerde epic structuur. De agent analyseert de bestaande context en bedenkt zelf concrete verbetervoorstellen.

## Contract
### Input (wat gaat erin)
**Verplichte parameters**:
- hypothese_code: string, de unieke hypothese-code in formaat jjmm.HHHH (bijv. 2603.H9XJ)
- thema_code: string, unieke identificatiecode van het thema
- auteur: string, naam van de auteur

**Optionele parameters**:
- toelichting: string, vrije tekst met aanvullende context of richting

**Opmerking**:
- De hypothese-code wordt als vaste referentie gebruikt in alle verbetervoorstellen, zodat duidelijk blijft op welke oorspronkelijke hypothese de voorgestelde verbeteringen terug te voeren zijn.
- De agent:
1. Zoekt de thematische scope op basis van de thema_code (artefacten/sfw/sfw.02.thema-verwoorder/scopes/)
2. Zoekt gerelateerde epic structuren (artefacten/sfw/sfw.02.thema-verwoorder/epics/)
3. Analyseert de context en bedenkt zelf meerdere verbetervoorstellen
4. Genereert per voorstel: probleem, oplossing, impact, randvoorwaarden, features
5. Datum wordt automatisch gegenereerd

### Output (wat komt eruit)
**Deliverables**: Markdown document met meerdere verbetervoorstellen volgens template
**Outputlocaties**: artefacten/sfw/sfw.02.thema-verwoorder/verbeteringen/
**Formaat**: Markdown (.md) volgens template

### Foutafhandeling
- STOP: thema_code of auteur ontbreekt
- STOP: thematische scope voor thema_code niet gevonden
- STOP: onvoldoende context om verbetervoorstellen te genereren
- Escaleer naar agent-curator bij onduidelijke scope of overlap

## Governance
- Volgt doctrine-agent-charter-normering.md (Principe 1, 2, 7, 9)
- Transparantie: alle output en beslissingen worden gelogd
- Canon-consultatie verplicht bij boundary-wijzigingen

## Metadata
Intent-ID: sfw.02.thema-verwoorder.definieer-verbeter-voorstellen  
Versie: 1.0.0  
Classificatie: Normerend, Ecosysteem, Inhoudelijk, Canon-gebonden
