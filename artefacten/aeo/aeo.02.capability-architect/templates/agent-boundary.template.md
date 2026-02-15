---
agent: capability-architect
intent: definieer-agent-boundary
versie: 1.0.0
# Template voor het definiëren van agent boundaries.
# Definieert de servicegrens: wat de agent wél en níet doet.
# Validatie en beoordeling van overlap/kwaliteit wordt gedaan door Agent Curator.
---


# Agent Boundary Document Template

Dit template beschrijft de OUTPUT van de capability-architect.
Het gegenereerde boundary-document krijgt de volgende structuur:

```markdown
---
agent: <agent-naam>
value_stream: <vs-code>
value_stream_fase: <vs-code>.<fase-nummer>
versie: 1.0.0
---

# Agent Boundary: <Agent-naam>

agent-naam: <lowercase-hyphens>
capability-boundary: <één zin: wat kan de agent; wat is expliciet uitgesloten>
doel: <één zin: waarom bestaat deze agent>
domein: <één woord of korte frase>
```

---
## Classificatie van de agent
(vink aan wat van toepassing is)

<!--
Richtlijn: agents in value stream `agent-enablement` zijn in principe
"Ecosysteem-normerend" op de inhoudelijke as.
-->

- **Inhoudelijke as**
  - [ ] Architectuur-normerend
	- [ ] Architectuur-structurerend
  - [ ] Ecosysteem-normerend
  - [ ] Structuur-normerend
  - [ ] Structuurrealiserend
  - [ ] Beschrijvend
  - [ ] Curator
  - [ ] Geen--nulpunt-

- **Inzet-as**
  - [ ] Value-stream-specifiek
  - [ ] Value-stream-overstijgend

- **Vorm-as**
  - [ ] Vormvast
  - [ ] Representatieomvormend

- **Werkingsas**
  - [ ] Inhoudelijk
  - [ ] Conditioneel


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

