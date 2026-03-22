---
agent: mandarin.ecosysteem-beschrijver
intent: beschrijf-agent-positionering
bronhouding: Input-gebonden
versie: 1.0.0
input_parameters:
  - agent_naam
value_stream_fase: aeo.02

---

## Output

Schrijf het resultaat weg naar:

```
artefacten/[vs]/[vs].[fase].[agent_naam]/[agent_naam].beschrijving.md
```

Waarbij `[vs]` en `[fase]` worden afgeleid uit `value_stream_fase` (bijv. `aeo.02` → `vs=aeo`, `fase=02`).

Voorbeeld voor `agent_naam=agent-ontwerper`, `value_stream_fase=aeo.02`:
```
artefacten/aeo/aeo.02.agent-ontwerper/agent-ontwerper.beschrijving.md
```
