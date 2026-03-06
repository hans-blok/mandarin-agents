---
agent: agent-curator
intent: valideer-boundary-overlap
versie: 1.0.0
input_parameters:
  - value_stream_fase
  - agent_namen
  - canon_ref
---

# Agent Prompt: agent-curator — valideer-boundary-overlap

**Raadpleeg**:
- Agent-contract: `artefacten/aeo/aeo.02.agent-curator/agent-contracten/agent-curator.valideer-boundary-overlap.agent.md`
- Agent-charter: `artefacten/aeo/aeo.02.agent-curator/agent-curator.charter.md`

## Instructie

Voer de intent `valideer-boundary-overlap` uit conform het agent-contract.

Analyseer de capability boundaries van alle agents in de opgegeven value stream fase op mogelijke overlap of lacunes. Classificeer elke relatie (GEEN OVERLAP / AANGRENZEND / OVERLAP / CONFLICT) en genereer escalaties naar de capability-architect bij OVERLAP of CONFLICT.

**Aandachtspunten**:
- Minimaal 2 boundary-documenten vereist; stop wanneer minder beschikbaar.
- `agent_namen` is optioneel: geef een subset op als alleen specifieke agents vergeleken moeten worden.
- De agent-curator doet geen aanbevelingen over boundary-herindeling — escaleert uitsluitend naar capability-architect.
