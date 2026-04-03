---
agent: thema-verwoorder
intent: definieer-thematische-scope
versie: 0.1.0
digest: 5ffa
status: vers
---
# thema-verwoorder — definieer-thematische-scope

## Rolbeschrijving (korte samenvatting)
Deze intent beschrijft het afbakenen en documenteren van de thematische scope binnen de value stream op basis van een hypothese-document. De agent analyseert de hypothese, bedenkt een geschikte titel en identificeert relevante epics.

## Contract
### Input (wat gaat erin)
**Verplichte parameters**:
- hypothese_code: string, de unieke hypothese-code in formaat jjmm.HHHH (bijv. 2603.H9XJ)
- hypothese_bestand: string, bestandsnaam van het hypothese-document (volledige pad of relatieve pad)
- auteur: string, naam van de auteur

**Optionele parameters**:
- toelichting: string, aanvullende tekstuele toelichting

**Opmerking**:
- De hypothese-code komt rechtstreeks uit de hypothese-vormer (bestand `hypothese-<hypothese_code>.md`) en moet onveranderd worden overgenomen in alle vervolgdocumenten waarin deze hypothese wordt gebruikt.
- De agent leest het hypothese-bestand, analyseert de inhoud, en bepaalt zelf:
- Thema-code (korte unieke identificatiecode voor het thema)
- Titel voor het thema
- Relevante epics
- Datum (wordt automatisch gegenereerd)

### Output (wat komt eruit)
**Deliverables**: Markdown document met thematische scope volgens template
**Outputlocaties**: artefacten/sfw/sfw.02.thema-verwoorder/scopes/
**Formaat**: Markdown (.md) volgens template

### Foutafhandeling
- STOP: hypothese_bestand of auteur ontbreekt
- STOP: hypothese_bestand niet gevonden of niet toegankelijk
- STOP: hypothese_bestand bevat onvoldoende informatie voor thematische scope
- STOP: titel niet uniek binnen value stream
- Escaleer naar agent-curator bij overlap of onduidelijke scope

## Governance
- Volgt doctrine-agent-charter-normering.md (Principe 1, 2, 7, 9)
- Transparantie: alle output en beslissingen worden gelogd
- Canon-consultatie verplicht bij boundary-wijzigingen

## Metadata
Intent-ID: sfw.02.thema-verwoorder.definieer-thematische-scope  
Versie: 1.0.0  
Classificatie: Normerend, Ecosysteem, Inhoudelijk, Canon-gebonden
