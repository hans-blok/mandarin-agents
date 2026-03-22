---
agent: ecosysteem-beschrijver
intent: beschrijf-agent-positionering
value_stream_fase: sfw.01
scope: hypothese-vormer
timestamp: 2026-03-22 21:26
execution_id: 58fe
canon_ref: adef1f5
---

# Positionering: hypothese-vormer

## Contextdiagram

```mermaid
flowchart LR
    initiator["👤 Initiator"]
    hypothese["Hypothese-vormer"]
    thema["🤖 Thema-verwoorder"]
    llm["Extern LLM"]
    human["👤 Human-in-the-loop"]

    initiator -->|levert probleembeschrijving en idee| hypothese
    llm -->|levert inferentie| hypothese
    hypothese -->|levert hypothese-document| thema
    hypothese -->|levert hypothese ter controle| human

    classDef agent-zelf fill:#1565c0,stroke:#0d47a1,color:#bbdefb;
    classDef aanroeper  fill:#bbdefb,stroke:#1e88e5,color:#0d47a1;
    classDef ontvanger  fill:#e8f5e9,stroke:#43a047,color:#1b5e20;
    classDef dienst     fill:#fff8e1,stroke:#f9a825,color:#5d4037;

    class hypothese agent-zelf;
    class initiator aanroeper;
    class thema,human ontvanger;
    class llm dienst;
```

## Uitvoeringsdiagram

```mermaid
sequenceDiagram
    participant IN as 👤 Initiator
    participant HV as Hypothese-vormer
    participant LLM as Extern LLM
    actor HiL as Human-in-the-loop

    IN->>HV: levert probleembeschrijving, idee en context
    HV->>HV: leest boundary, charter en contracten
    HV->>LLM: vraag om tekst te genereren (synthese)
    LLM-->>HV: gegenereerde tekst (synthese)
    HV->>HV: schrijft hypothese-{code}.md
    HV-->>HiL: output beschikbaar ter controle
```

## Classificatie

| As | Waarde |
|----|--------|
| Vormingsfase | Verkenning |
| Betekeniseffect | Beschrijvend |
| Werking | Inhoudelijk |
| Bronhouding | Exploratief |

## Intents en output

| Intent | Output bestand |
|--------|---------------|
| `beschrijf-hypothese` | `artefacten/sfw/sfw.01.hypothese-vormer/output/hypothese-{hypothese_code}.md` |
| `beschrijf-aannames` | `artefacten/sfw/sfw.01.hypothese-vormer/output/hypothese-{hypothese_code}.md` |
| `beschrijf-toetsbaarheid` | `artefacten/sfw/sfw.01.hypothese-vormer/output/hypothese-{hypothese_code}.md` |

## Bronbestanden

### Werkbron

- `artefacten/sfw/sfw.01.hypothese-vormer/hypothese-vormer.agent-boundary.md` — levert aanroepers, diensten en scope van de agent

### Kaderbron

- `artefacten/sfw/sfw.01.hypothese-vormer/hypothese-vormer.charter.md` — levert authoritative classificatie, kerntaken en grenzen
- `artefacten/sfw/sfw.01.hypothese-vormer/agent-contracten/hypothese-vormer.beschrijf-hypothese.agent.md` — levert werkwijze en output-locatie voor intent beschrijf-hypothese
- `artefacten/sfw/sfw.01.hypothese-vormer/agent-contracten/hypothese-vormer.beschrijf-aannames.agent.md` — levert werkwijze voor intent beschrijf-aannames
- `artefacten/sfw/sfw.01.hypothese-vormer/agent-contracten/hypothese-vormer.beschrijf-toetsbaarheid.agent.md` — levert werkwijze voor intent beschrijf-toetsbaarheid
