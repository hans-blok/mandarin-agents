---
agent: mandarin.ecosysteem-beschrijver
intent: beschrijf-agent-positionering
intent-id: aeo.02.ecosysteem-beschrijver.01
bronhouding: Input-gebonden
versie: 1.0.0
input_parameters:
  - agent_naam
value_stream_fase: aeo.02
template: templates/beschrijf-agent-positionering.template.md

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
