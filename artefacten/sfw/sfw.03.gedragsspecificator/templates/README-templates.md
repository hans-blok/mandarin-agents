# Templates voor agent-gedragsspecificator

Dit document beschrijft de beschikbare output templates voor de `gedragsspecificator` agent. Deze templates borgen eenduidige outputstructureren van requirements en tests.

## 1. Doel en Gebruik

De agent `gedragsspecificator` genereert verschillende soorten output tijdens het vertalen van business requirements naar Gherkin. Elk template ondersteunt een specifieke stap in dit proces.

### 1. `gedragsspecificator.specificeer-gedrag.template.md`
**Doel**: Het vastleggen van de functionele requirements voorafgaand aan de formele vertaling naar Gherkin.
**Wanneer Gebruiken**: Tijdens de initiële requirement analyse en refinement sessies. Legt de basis voor Gherkin.
**Inhoud**: Context, User Story, Acceptatiecriteria (niet-Gherkin), Business Rules, Voorbeelden.

### 2. `gedragsspecificator.vertaal-naar-gherkin.template.md`
**Doel**: Het leveren van een uitvoerbaar, gestructureerd testscenario in Gherkin-formaat.
**Wanneer Gebruiken**: Als output van de `vertaal-naar-gherkin` intent.
**Inhoud**: Feature, Background, Scenario (Given/When/Then), Scenario Outline.

### 3. `gedragsspecificator.valideer-scenario-consistentie.template.md`
**Doel**: Het rapporteren over de consistentie en volledigheid van de scenario's.
**Wanneer Gebruiken**: Als validatiestap na het opstellen van gedragsspecificaties of Gherkin scenario's.
**Inhoud**: Audit findings, terminologie checks, ontbrekende edge cases, traceerbaarheid, conclusie.

## 2. Best Practices

- Gebruik altijd de template als startpunt.
- Vul placeholders `{...}` in met specifieke context.
- Behoud de sectiestructuur om consistentie over projecten heen te waarborgen.
- Verwijder niet-relevante secties alleen in overleg met stakeholders (of markeer als N/A).
