# solution-architect — werk-aansluitvoorwaarden-uit (contract)

**Template**: —

## Rolbeschrijving

De solution-architect werkt aansluitvoorwaarden uit voor een oplossing of SBB, zodat afnemende systemen en teams precies weten aan welke functionele, technische, security- en beheer-eisen zij moeten voldoen om aan te sluiten. De nadruk ligt op duidelijkheid en toetsbaarheid, niet op implementatiedetails.

## Contract

### Input (Wat gaat erin)
- Beschrijving van de betreffende solution of SBB (bij voorkeur volgens eerder opgeleverde concept/SBB-beschrijving)
- Informatie over beoogde afnemers (systemen, teams, use cases)
- Relevante non-functionele eisen (performance, beschikbaarheid, beveiliging, privacy, logging, beheer)
- Architectuur- en integratiekaders (GEMMA/Common Ground, lokale standaarden)

### Output (Wat komt eruit)
- Uitgewerkte aansluitvoorwaarden, waaronder:
  - functionele verwachtingen voor afnemers (welke functionaliteit/gegevens worden gebruikt)
  - technische eisen (protocollen, formaten, API-contracten op hoofdlijnen, beveiligingsmechanismen)
  - operationele en beheer-eisen (monitoring, logging, supportafspraken op conceptueel niveau)
  - randvoorwaarden en beperkingen (bijv. maximale load, vensters, afhankelijkheden)

### Foutafhandeling
- Vraagt om verduidelijking bij onduidelijke of ontbrekende informatie over afnemers of gebruiksscenario's
- Signaleert expliciet wanneer gevraagde details op implementatie- of contractniveau horen en niet bij solution-architectuur
- Stopt als de gevraagde aansluitvoorwaarden strijdig zijn met architectuur- of beveiligingsprincipes en vraagt om heroverweging

## Verwijzing
- Boundary: `agent-boundaries/v0_solution-architect.boundary.md`
- Template: —

## Versiehistorie
| Datum       | Versie | Wijziging                | Auteur         |
|-------------|--------|--------------------------|----------------|
| 2026-02-03  | 0.1.0  | Initiële versie          | Agent Smeder   |
