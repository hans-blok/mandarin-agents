# Agent: thema-verwoorder

De agent **thema-verwoorder** vertaalt een geselecteerde veranderhypothese naar een thematische beschrijving, epics en concrete verbeter-voorstellen. De agent vormt de schakel tussen de **hypothese-vormer** (input) en o.a. de **gedragsspecificator** en de toekomstige **verbeteringen-analist (feature-analyst)** (output).

## Overzicht van intents en volgorde

De belangrijkste intents van de thema-verwoorder zijn:

1. `definieer-thematische-scope`
2. `definieer-epic-structuur`
3. `definieer-verbeter-voorstel` (of reeksen voorstellen)

Een typische uitvoeringsvolgorde ziet er zo uit:

1. **definieer-thematische-scope**  
   - **Context / input**  
     - Gekozen hypothese uit de agent **hypothese-vormer** (bijv. outputdocument `hypothese-HYP-YYYYMMDD-XX.md`).  
     - Eventuele aanvullende context van de gebruiker: veranderinitiatief, scope-afbakening, betrokken domeinen, constraints.  
   - **Doel**  
     - Een thematische beschrijving formuleren rond de gekozen hypothese: welk thema staat centraal, welke probleemruimte en welke waardegebieden.  
   - **Output**  
     - Een thematische-scope-beschrijving (markdown) die als bron dient voor de volgende intents.

2. **definieer-epic-structuur**  
   - **Context / input**  
     - De thematische-scope-beschrijving uit de vorige intent.  
     - De oorspronkelijke hypothese(s) uit de hypothese-vormer (voor traceerbaarheid).  
     - Gebruiker kan hier accenten leggen: prioriteiten, volgorde, afhankelijkheden tussen epics.  
   - **Doel**  
     - Het thema opdelen in een logische set van epics (thematische veranderlijnen) met een korte beschrijving, rationale en globale scope per epic.  
   - **Output**  
     - Een epic-structuurdocument (markdown) dat per epic de kern, scope en rationale vastlegt.  
     - Dit document vormt input voor zowel:
       - de **gedragsspecificator** (die epics verder uitwerkt naar gewenst gedrag, scenario’s en specificaties);  
       - de toekomstige **verbeteringen-analist / feature-analyst** (die epics vertaalt naar feature‑kandidaten en backlog-items).

3. **definieer-verbeter-voorstel**  
   - **Context / input**  
     - De epic-structuur uit stap 2.  
     - Eventuele aanvullende richtlijnen van de gebruiker: gewenste mate van detaillering, constraints (budget, tijd), afhankelijkheden met andere initiatieven.  
   - **Doel**  
     - Per epic één of meerdere concrete verbeter‑voorstellen formuleren: wat gaan we precies veranderen, waarom, voor wie en welk effect verwachten we.  
   - **Output**  
     - Een set verbeter‑voorstel-documenten (markdown), conform de template `thema-verwoorder.definieer-verbeter-voorstellen.template.md`.  
     - Deze voorstellen zijn direct herbruikbaar als:
       - input voor de **gedragsspecificator** (om gewenst gedrag en specificaties verder te verfijnen);  
       - input voor de toekomstige **verbeteringen-analist / feature-analyst** (om features, user stories of requirements af te leiden).

## Relatie met andere agents

- **Hypothese-vormer**  
  - Levert de initiële veranderhypothese(n) die in de thema-verwoorder worden omgezet naar een thematische scope, epics en verbeter-voorstellen.

- **Gedragsspecificator**  
  - Ontvangt de thematische epics en/of verbeter-voorstellen als input.  
  - Werkt deze verder uit naar concreet gewenst gedrag, scenario’s en specificaties.

- **Verbeteringen-analist (feature-analyst)**  
  - Deze agent moet nog worden gerealiseerd.  
  - Zal de thematische epics en verbeter‑voorstellen gebruiken om features, backlog‑items en requirements-structuren te definiëren.

## Gebruik in de workspace

De exacte uitvoering (tasks, prompts en runners) wordt gegenereerd en beheerd via de **agent-engineer** en **ecosysteem-coordinator**. In de praktijk volg je per thema het patroon:

1. Kies een hypothese met de **hypothese-vormer**.  
2. Start de thema-verwoorder met `definieer-thematische-scope` voor dit thema.  
3. Werk de thematische scope uit naar epics via `definieer-epic-structuur`.  
4. Werk (per epic) de epics uit naar concrete verbeter‑voorstellen via `definieer-verbeter-voorstel`.  
5. Gebruik de resulterende documenten als input voor de gedragsspecificator en later de verbeteringen-analist.
