---
agent: ecosysteem-beschrijver
intent: beschrijf-agent-positionering
value_stream_fase: aeo.02
scope: agent-ontwerper
timestamp: 2026-03-22 10:30
execution_id: corr01
canon_ref: f1bc996
---

# Positionering: agent-ontwerper

## Contextdiagram

```mermaid
flowchart LR
    coordinator["🤖 Ecosysteem-coördinator"]
    architect["🤖 Capability-architect"]
    ontwerper["Agent-ontwerper"]
    llm["Extern LLM"]
    canon["Canon"]
    engineer["🤖 Agent-engineer"]
    aes["Agent-ecosysteem-ontwikkelsysteem"]

    coordinator -->|initieert ontwerpverzoek| ontwerper
    architect -->|levert boundary-document| ontwerper
    canon -->|levert templates en doctrine| ontwerper
    llm -->|levert inferentie| ontwerper
    ontwerper -->|levert charter / contract / template| engineer
    ontwerper -->|levert charter / contract / template| aes

    classDef agent-zelf fill:#1565c0,stroke:#0d47a1,color:#bbdefb;
    classDef aanroeper  fill:#bbdefb,stroke:#1e88e5,color:#0d47a1;
    classDef ontvanger  fill:#e8f5e9,stroke:#43a047,color:#1b5e20;
    classDef dienst     fill:#fff8e1,stroke:#f9a825,color:#5d4037;

    class ontwerper agent-zelf;
    class coordinator,architect aanroeper;
    class engineer,aes ontvanger;
    class llm,canon dienst;
```

## Uitvoeringsdiagram

```mermaid
sequenceDiagram
    participant EC as 🤖 Ecosysteem-coördinator
    participant CA as 🤖 Capability-architect
    participant AO as Agent-ontwerper
    participant Canon as Canon
    participant LLM as Extern LLM
    participant AES as Agent-ecosysteem-ontwikkelsysteem
    participant AE as 🤖 Agent-engineer

    EC->>AO: initieert ontwerpverzoek (agent_naam, intent)
    CA->>AO: levert boundary-document
    AO->>Canon: raadpleegt charter/contract template + doctrine
    Canon-->>AO: templates en grondslagen
    AO->>LLM: vraag om tekst te genereren (synthese) op basis van boundary + templates
    LLM-->>AO: gegenereerde artefacten (synthese)
    AO->>AO: schrijft charter / contract / template
    AO-->>AES: artefacten beschikbaar in ecosysteem
    AO-->>AE: artefacten beschikbaar voor implementatie
```

## Classificatie

| As | Waarde |
|----|--------|
| Vormingsfase | Vastlegging |
| Betekeniseffect | Normerend |
| Werking | Inhoudelijk |
| Bronhouding | Canon-gebonden |

## Intents en output

| Intent | Output bestand |
|--------|---------------|
| `definieer-agent-charter` | `artefacten/aeo/aeo.02.{agent_naam}/{agent_naam}.charter.md` |
| `definieer-agent-contract` | `artefacten/aeo/aeo.02.{agent_naam}/agent-contracten/{agent_naam}.{intent}.agent.md` |
| `definieer-agent-template` | `artefacten/aeo/aeo.02.{agent_naam}/templates/{template-naam}.template.md` |

## Bronbestanden

### Werkbron

- `artefacten/aeo/aeo.02.agent-ontwerper/agent-ontwerper.agent-boundary.md` — levert aanroepers, diensten en scope van de agent

### Kaderbron

- `artefacten/aeo/aeo.02.agent-ontwerper/agent-ontwerper.charter.md` — levert authoritative classificatie, kerntaken en grenzen
- `artefacten/aeo/aeo.02.agent-ontwerper/agent-contracten/agent-ontwerper.definieer-agent-charter.agent.md` — levert werkwijze en output-locatie voor intent definieer-agent-charter
- `artefacten/aeo/aeo.02.agent-ontwerper/agent-contracten/agent-ontwerper.definieer-agent-contract.agent.md` — levert werkwijze voor intent definieer-agent-contract
- `artefacten/aeo/aeo.02.agent-ontwerper/agent-contracten/agent-ontwerper.definieer-agent-template.agent.md` — levert werkwijze voor intent definieer-agent-template
