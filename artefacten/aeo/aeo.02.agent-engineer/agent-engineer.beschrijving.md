---
agent: ecosysteem-beschrijver
intent: beschrijf-agent-positionering
value_stream_fase: aeo.02
scope: agent-engineer
timestamp: 2026-03-22 10:30
execution_id: corr02
canon_ref: f1bc996
---

# Positionering: agent-engineer

## Contextdiagram

```mermaid
flowchart LR
    coordinator["🤖 Ecosysteem-coördinator"]
    ontwerper["🤖 Agent-ontwerper"]
    architect["🤖 Capability-architect"]
    engineer["Agent-engineer"]
    llm["Extern LLM"]
    canon["Canon"]
    templates["Templates"]
    aes["Agent-ecosysteem-ontwikkelsysteem"]

    coordinator -->|initieert realisatieverzoek| engineer
    ontwerper -->|levert charters + contracten| engineer
    architect -->|levert boundary-document| engineer
    canon -->|levert kaderbronnen| engineer
    templates -->|levert prompt-template| engineer
    llm -->|levert inferentie| engineer
    engineer -->|levert prompts / tasks / runner| aes

    classDef agent-zelf fill:#1565c0,stroke:#0d47a1,color:#bbdefb;
    classDef aanroeper  fill:#bbdefb,stroke:#1e88e5,color:#0d47a1;
    classDef ontvanger  fill:#e8f5e9,stroke:#43a047,color:#1b5e20;
    classDef dienst     fill:#fff8e1,stroke:#f9a825,color:#5d4037;

    class engineer agent-zelf;
    class coordinator,ontwerper,architect aanroeper;
    class aes ontvanger;
    class llm,grondslagen,templates dienst;
```

## Uitvoeringsdiagram

```mermaid
sequenceDiagram
    participant EC as 🤖 Ecosysteem-coördinator
    participant AO as 🤖 Agent-ontwerper
    participant AE as Agent-engineer
    participant GL as Grondslagen
    participant LLM as Extern LLM
    participant AES as Agent-ecosysteem-ontwikkelsysteem

    EC->>AE: initieert realisatieverzoek (agent_naam, intent)
    AO->>AE: levert charters + contracten
    AE->>AE: leest contracten + boundary, bepaalt benodigde artefacten
    AE->>GL: raadpleegt doctrines en normen
    GL-->>AE: grondslagen
    AE->>LLM: vraag om generatie van prompts / tasks / runner
    LLM-->>AE: gegenereerde artefacten
    AE->>AE: schrijft prompts, tasks.json, runner.py
    AE->>AE: valideert consistentie (geen half-gerealiseerde intents)
    AE-->>AES: artefacten beschikbaar in ecosysteem
```

## Classificatie

| As | Waarde |
|----|--------|
| Vormingsfase | Realisatie |
| Betekeniseffect | Realiserend |
| Werking | Inhoudelijk |
| Bronhouding | Input-gebonden |

## Intents en output

| Intent | Output bestand |
|--------|---------------|
| `realiseer-agent-prompts` | `artefacten/aeo/aeo.02.{agent_naam}/prompts/{agent_naam}.{intent}.prompt.md` |
| `realiseer-agent-taskconfiguratie` | `artefacten/aeo/aeo.02.{agent_naam}/{agent_naam}.tasks.json` |
| `realiseer-agent-runner` | `artefacten/aeo/aeo.02.{agent_naam}/runner/{agent_naam}.runner.py` |

## Bronbestanden

### Werkbron

- `artefacten/aeo/aeo.02.agent-engineer/agent-engineer.agent-boundary.md` — levert aanroepers, diensten en scope van de agent

### Kaderbron

- `artefacten/aeo/aeo.02.agent-engineer/agent-engineer.charter.md` — levert authoritative classificatie, kerntaken en grenzen
- `artefacten/aeo/aeo.02.agent-engineer/agent-contracten/agent-engineer.realiseer-agent-prompts.agent.md` — levert werkwijze en output-locatie voor intent realiseer-agent-prompts
- `artefacten/aeo/aeo.02.agent-engineer/agent-contracten/agent-engineer.realiseer-agent-taskconfiguratie.agent.md` — levert werkwijze voor intent realiseer-agent-taskconfiguratie
- `artefacten/aeo/aeo.02.agent-engineer/agent-contracten/agent-engineer.realiseer-agent-runner.agent.md` — levert werkwijze voor intent realiseer-agent-runner
