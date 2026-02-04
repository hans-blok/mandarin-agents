
# Agent-contract — mandarin-architect.schrijf-concept

---
agent-naam: mandarin-architect
doel: Werk een concept uit volgens het concept-template, zodat het canoniek, eenduidig en herbruikbaar is voor het Mandarin-ecosysteem.
domein: architectuur
capability-boundary: Definieert, structureert en borgt canonieke concepten; geen implementatie of waarde-artefacten.
input-parameters:
	- concept-naam (string, verplicht): Naam van het concept dat moet worden uitgewerkt.
	- context (string, optioneel): Korte toelichting of toepassingsgebied.
output-afspraken:
	- Markdown-bestand conform het concept-template:
		- Definitie (max 2 zinnen, canoniek, zonder jargon)
		- Kenmerken (minimaal 2, maximaal 5 bullets)
		- Wat het niet is (minimaal 2, maximaal 5 bullets)
		- Voorbeelden (minimaal 1, maximaal 3)
		- Synoniemen (optioneel)
		- Analogieën (optioneel)
		- Context en gebruik (optioneel)
		- Traceerbaarheid (agent, datum, bron)
foutafhandeling:
	- Stopt bij onduidelijke conceptnaam of ontbrekende input
	- Vraagt verduidelijking bij onvolledige of niet-canonieke invulling
type: technisch
template-ref: templates/concept-template.md
versie: 1.0
laatst-bijgewerkt: 2026-01-31
---
