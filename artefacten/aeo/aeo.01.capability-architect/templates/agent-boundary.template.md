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
bronhouding: <Input-gebonden | Canon-gebonden | Externe-bron-gebonden | Exploratief>
versie: 1.0.0
---

# Agent Boundary: <Agent-naam>

agent-naam: <lowercase-hyphens>
capability-boundary: <één zin: wat kan de agent; wat is expliciet uitgesloten>
doel: <één zin: waarom bestaat deze agent>
domein: <één woord of korte frase>
```

---
## Mandarin-agent-classificatie

| As               | Waarde                  |
|------------------|-------------------------|
| Vormingsfase     | <kies één waarde>       |
| Betekeniseffect  | <kies één waarde>       |
| Werking          | <kies één waarde>       |
| Bronhouding      | <kies één waarde>       |

**Validatie**: <Vormingsfase> × <Betekeniseffect> × <Werking> × <Bronhouding> — <beschrijving>. Positionering volgt `mandarin-ordeningsconcepten.md`.

<!--
Geldige waarden per as (raadpleeg mandarin-ordeningsconcepten.md voor definities):
Vormingsfase:    Operationeel in alle fasen | Verkenning | Ordening | Vastlegging | Realisatie | Toetsing | Operationalisatie
Betekeniseffect: Geen | Beschrijvend | Structurerend | Normerend | Vastleggend | Realiserend | Evaluerend
Werking:         Inhoudelijk | Representatie-omvormend | Conditioneel
Bronhouding:     Input-gebonden | Canon-gebonden | Externe-bron-gebonden | Exploratief
-->


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

