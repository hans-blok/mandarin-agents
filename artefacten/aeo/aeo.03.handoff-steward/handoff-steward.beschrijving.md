---
agent: ecosysteem-beschrijver
intent: beschrijf-agent-positionering
value_stream_fase: aeo.02
scope: handoff-steward
timestamp: 2026-04-08 19:52
execution_id: 8221
execution_digest: df1552aac773
---

# Positionering: handoff-steward

## Contextdiagram

```mermaid
flowchart LR
    coordinator["🤖 Ecosysteem-coordinator"]
    curator["🤖 Agent-curator"]
    ontvanger["🤖 Ontvangende agent"]
    steward["🤖 Handoff-steward"]
    human["👤 Human-in-the-loop"]

    coordinator -->|levert execution-bestand voor initiële handoff| steward
    curator -->|vraagt registerinspectie of valideert afwijkingen| steward
    steward -->|levert handoff-bestand| ontvanger
    ontvanger -->|bevestigt ontvangst voor handoff-sluiting| steward
    steward -->|levert output ter controle| human

    classDef agent-zelf fill:#1565c0,stroke:#0d47a1,color:#bbdefb;
    classDef aanroeper  fill:#bbdefb,stroke:#1e88e5,color:#0d47a1;
    classDef ontvanger  fill:#e8f5e9,stroke:#43a047,color:#1b5e20;

    class steward agent-zelf;
    class coordinator,curator aanroeper;
    class ontvanger,human ontvanger;
```

## Uitvoeringsdiagram

```mermaid
sequenceDiagram
    participant EC as 🤖 Ecosysteem-coordinator
    participant HS as 🤖 Handoff-steward
    participant EX as Execution-bestand
    participant HR as Handoff-register
    participant OA as 🤖 Ontvangende agent
    actor HiL as Human-in-the-loop

    EC->>HS: initieert realiseer-initiele-handoff
    HS->>EX: leest execution-bestand
    EX-->>HS: execution-identiteit en overdrachtscontext
    HS->>HR: leest handoff-register
    HR-->>HS: huidig volgnummer en registerstatus
    HS->>HR: schrijft nieuwe registerentry
    HS->>HS: genereert handoff-bestand conform template
    HS-->>OA: levert handoff-bestand
    OA->>HS: bevestigt ontvangst voor sluiting
    HS->>HR: markeert handoff als gesloten
    HS-->>HiL: output en log beschikbaar ter controle
```

## Classificatie

| As | Waarde |
|----|--------|
| Vormingsfase | Realisatie |
| Betekeniseffect | Vastleggend |
| Werking | Inhoudelijk |
| Bronhouding | Canon-gebonden |

## Intents en output

| Intent | Output bestand |
|--------|---------------|
| `realiseer-initiele-handoff` | `handoffs/{handoff_id}.handoff.md` |
| `realiseer-handoff-sluiting` | `{handoff_register_pad}` |
| `realiseer-overzicht-inspectie-handoffs` | `{output_bestand}` (optioneel) |

## Bronbestanden

### Werkbron

- `artefacten/aeo/aeo.03.handoff-steward/handoff-steward.agent-boundary.md` — levert capability-boundary, classificatie, directe raakvlakken, inputs en outputs

### Kaderbron

- `artefacten/aeo/aeo.03.handoff-steward/handoff-steward.charter.md` — levert authoritative classificatie, kerntaken, grenzen en output-locaties
- `artefacten/aeo/aeo.03.handoff-steward/agent-contracten/handoff-steward.realiseer-initiele-handoff.agent.md` — levert input, output en werkwijze voor het aanmaken van nieuwe handoffs
- `artefacten/aeo/aeo.03.handoff-steward/agent-contracten/handoff-steward.realiseer-handoff-sluiting.agent.md` — levert input, output en werkwijze voor het sluiten van bestaande handoffs
- `artefacten/aeo/aeo.03.handoff-steward/agent-contracten/handoff-steward.realiseer-overzicht-inspectie-handoffs.agent.md` — levert input, output en werkwijze voor registerinspectie