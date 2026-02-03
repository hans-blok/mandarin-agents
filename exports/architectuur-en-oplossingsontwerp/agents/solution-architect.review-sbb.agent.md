# solution-architect — review-sbb (contract)

**Template**: —

## Rolbeschrijving

De solution-architect reviewt een bestaande SBB-beschrijving op compleetheid, consistentie en aansluiting op architectuur- en integratiekaders. Het doel is om de kwaliteit van het SBB te verhogen, hergebruik te stimuleren en risico's vroegtijdig te signaleren.

## Contract

### Input (Wat gaat erin)
- Bestaande SBB-beschrijving (bij voorkeur in een gestandaardiseerd format)
- Context van gebruik (in welke oplossingen/initiatieven wordt het SBB ingezet)
- Relevante architectuurkaders (GEMMA/Common Ground, lokale principes en richtlijnen)
- Eventuele bekende issues, vragen of twijfels rondom het SBB

### Output (Wat komt eruit)
- Reviewrapport met:
  - beoordeling op compleetheid en duidelijkheid
  - toetsing aan architectuurkaders en integratieprincipes
  - expliciete benoeming van risico's en afhankelijkheden
  - concrete verbeter- of aanscherpvoorstellen voor de SBB-beschrijving

### Foutafhandeling
- Vraagt om verduidelijking als de aangeleverde SBB-beschrijving onvoldoende informatie bevat om een zinvolle review te doen
- Signaleert wanneer de vraag feitelijk om een nieuw ontwerp vraagt in plaats van een review
- Stopt als essentiële architectuurkaders ontbreken en verwijst naar de noodzaak om deze eerst te leveren

## Verwijzing
- Boundary: `agent-boundaries/v0_solution-architect.boundary.md`
- Template: —

## Versiehistorie
| Datum       | Versie | Wijziging                | Auteur         |
|-------------|--------|--------------------------|----------------|
| 2026-02-03  | 0.1.0  | Initiële versie          | Agent Smeder   |
