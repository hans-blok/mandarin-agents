---
agent: ecosysteem-beschrijver
intent: beschrijf-agent-positionering
value_stream_fase: aeo.02
scope: ecosysteem-beschrijver
timestamp: 2026-03-22 10:00
execution_id: 1d61
canon_ref: f1bc996
---

# Positionering: ecosysteem-beschrijver

## Contextdiagram

```mermaid
flowchart LR
    coordinator["Ecosysteem-coördinator"]
    ontwerper["Agent-ontwerper"]
    ecosysteem["Ecosysteem-beschrijver"]
    llm["Extern LLM"]
    human["👤 Human-in-the-loop"]

    coordinator -->|initieert beschrijvingsverzoek| ecosysteem
    ontwerper -->|levert charters en contracten| ecosysteem
    llm -->|levert inferentie| ecosysteem
    ecosysteem -->|levert beschrijving ter controle| human

    classDef agent-zelf fill:#1565c0,stroke:#0d47a1,color:#bbdefb;
    classDef aanroeper  fill:#bbdefb,stroke:#1e88e5,color:#0d47a1;
    classDef ontvanger  fill:#e8f5e9,stroke:#43a047,color:#1b5e20;
    classDef dienst     fill:#fff8e1,stroke:#f9a825,color:#5d4037;

    class ecosysteem agent-zelf;
    class coordinator,ontwerper aanroeper;
    class human ontvanger;
    class llm dienst;
```

## Uitvoeringsdiagram

```mermaid
sequenceDiagram
    participant EC as Ecosysteem-coördinator
    participant AO as Agent-ontwerper
    participant EB as Ecosysteem-beschrijver
    participant LLM as Extern LLM
    actor HiL as Human-in-the-loop

    EC->>EB: initieert beschrijvingsverzoek (agent_naam)
    AO->>EB: levert charters en contracten
    EB->>EB: leest boundary, charter en contracten
    EB->>LLM: vraag om tekst te genereren (synthese)
    LLM-->>EB: gegenereerde tekst (synthese)
    EB->>EB: schrijft ecosysteem-beschrijver.beschrijving.md
    EB-->>HiL: output beschikbaar ter controle
```

## Classificatie

| As | Waarde |
|----|--------|
| Vormingsfase | Verantwoording |
| Betekeniseffect | Beschrijvend |
| Werking | Inhoudelijk |
| Bronhouding | Input-gebonden |

## Intents en output

| Intent | Output bestand |
|--------|---------------|
| `beschrijf-agent-positionering` | `artefacten/aeo/aeo.02.ecosysteem-beschrijver/ecosysteem-beschrijver.beschrijving.md` |
| `beschrijf-ecosysteem-artefacten` | `artefacten/aeo/aeo.02.ecosysteem-beschrijver/ecosysteem-beschrijver.beschrijf-ecosysteem-artefacten.md` |
| `beschrijf-ecosysteem-contracten` | `artefacten/aeo/aeo.02.ecosysteem-beschrijver/ecosysteem-beschrijver.beschrijf-ecosysteem-contracten.md` |
| `beschrijf-ecosysteem-value-streams-agents` | `artefacten/aeo/aeo.02.ecosysteem-beschrijver/ecosysteem-beschrijver.beschrijf-ecosysteem-value-streams-agents.md` |

## Bronbestanden

- `artefacten/aeo/aeo.02.ecosysteem-beschrijver/ecosysteem-beschrijver.agent-boundary.md`
- `artefacten/aeo/aeo.02.ecosysteem-beschrijver/ecosysteem-beschrijver.charter.md`
- `artefacten/aeo/aeo.02.ecosysteem-beschrijver/agent-contracten/ecosysteem-beschrijver.beschrijf-agent-positionering.agent.md`
- `artefacten/aeo/aeo.02.ecosysteem-beschrijver/agent-contracten/ecosysteem-beschrijver.beschrijf-ecosysteem-artefacten.agent.md`
- `artefacten/aeo/aeo.02.ecosysteem-beschrijver/agent-contracten/ecosysteem-beschrijver.beschrijf-ecosysteem-contracten.agent.md`
- `artefacten/aeo/aeo.02.ecosysteem-beschrijver/agent-contracten/ecosysteem-beschrijver.beschrijf-ecosysteem-value-streams-agents.agent.md`
