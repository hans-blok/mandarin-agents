---
# IDENTIFICATIE
template-id: "001"
template-naam: agent-boundary

# RELATIES
artefact-type-id: "001"
agent-id: aeo.01.capability-architect

# META-DATA
versie: 1.1.0
status: vers
digest: b490
---
# Agent Boundary Document Template

Dit template beschrijft de OUTPUT van de capability-architect.
Het gegenereerde boundary-document krijgt de volgende structuur:

```markdown
---
agent: <agent-naam>
value_stream: <vs-code>
value_stream_fase: <vs-code>.<fase-nummer>
kaderdefinities: <lijst van canonieke paden, of "geen">
versie: 1.0.0
---

# Agent Boundary: <Agent-naam>

agent-naam: <lowercase-hyphens>
capability-boundary: <één zin: wat kan de agent; wat is expliciet uitgesloten>
doel: <één zin: waarom bestaat deze agent>
domein: <één woord of korte frase>
```

---
## Mandarin-agent-classificatie (4 orthogonale assen)
(vink aan wat van toepassing is)

<!--
Richtlijn: Classificeer de agent langs alle vier orthogonale assen.
Raadpleeg mandarin-ecosysteem-ordeningsconcepten.md voor definities en voorbeelden.
-->

- **Vormingsfase** (fase van vorming of ontwikkeling)
  - [ ] Operationeel in alle fasen
  - [ ] Verkenning (onderzoeken van intentie, probleemstelling of richting)
  - [ ] Ordening (structureren van intentie en expliciet maken van samenhang)
  - [ ] Vastlegging (betekenis bindend vaststellen binnen de workspace)
  - [ ] Realisatie (betekenis werkend maken in systemen of processen)
  - [ ] Toetsing (gerealiseerd artefact beoordelen tegen een norm)
  - [ ] Operationalisatie (gerealiseerde structuur formeel in werking stellen)

- **Betekeniseffect** (effect op betekenis)
  - [ ] Geen betekenis (nul-positie, alleen voor conditionele werking)
  - [ ] Beschrijvend (documenteert, vooraf en achteraf)
  - [ ] Structurerend (maakt samenhang en relaties expliciet)
  - [ ] Normerend (normeert structuur en indeling voor realisatie en ook toetsing)
  - [ ] Vastleggend (realiseert direct gedrag, structuur of configuratie)
  - [ ] Realiserend (realiseert feitelijk gedrag, structuur of configuratie)
  - [ ] Evaluerend (legt oordeel of duiding vast, beoordeelt kwaliteit)


- **Werking** (inhoud, representatie of voorwaarden)
  - [ ] Inhoudelijk (werkt direct op betekenisvolle artefacten)
  - [ ] Representatie-omvormend (zet inhoud om tussen representaties, betekenis-blind)
  - [ ] Conditioneel (werkt op voorwaarden en hygiëne, niet op inhoud)
 
- **Bronhouding** (kennisbronnen en herleidbaarheid)
  - [ ] Input-gebonden (output 100% herleidbaar tot input)
  - [ ] Canon-gebonden (baseert zich expliciet op canon)
  - [ ] Externe-bron-gebonden (haalt kennis uit externe bronnen, maar wel met kaders)
  - [ ] Exploratief (gebruikt generatieve capaciteiten, aannames expliciet)


## Opereert in Value stream fasen
- <value stream 1> <value stream fase 1>
- <value stream 2> <value stream fase 2>


## Toelichting

- Wat doet de agent concreet? (2–5 bullets)
- Welke inputs verwacht de agent? (1–3 bullets)
- Welke outputs levert de agent? (1–3 bullets)

## Voorstellen agent contracten (intents)

- <Intent 1 naam>
- <Intent 2 naam>
- <Intent 3 naam>

## Zorgt voor

- <Consistente taal / afspraken / structuur>
- <Heldere afbakening>
- <Hiërarchie en samenhang>

## Neemt geen beslissingen over

- <Prioriteit>
- <Planning>
- <Waarde-afweging>

## Mogelijke raakvlakken (ter informatie)

> **Let op**: De Capability-architect *identificeert* mogelijke raakvlakken,
> maar *valideert of beoordeelt* deze niet. Dat is de verantwoordelijkheid
> van de Agent Curator.

- Agents met aangrenzende scope: <lijst agents>
- Mogelijke overlap-punten: <1–3 bullets>
- Te onderzoeken door Agent Curator: <specifieke aandachtspunten>

## Referentie naar criteria (optioneel)

- Nummering/positionering: <waarom deze naam en plek logisch zijn>
- Canon-consistentie: <korte check>

