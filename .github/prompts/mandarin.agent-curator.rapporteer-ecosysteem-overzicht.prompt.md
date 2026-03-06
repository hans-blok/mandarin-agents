---
agent: agent-curator
intent: rapporteer-ecosysteem-overzicht
versie: 1.0.0
input_parameters:
  - value_stream_fase
  - canon_ref
  - detail_niveau
---

# Agent Prompt: agent-curator — rapporteer-ecosysteem-overzicht

**Raadpleeg**:
- Agent-contract: `artefacten/aeo/aeo.02.agent-curator/agent-contracten/agent-curator.rapporteer-ecosysteem-overzicht.agent.md`
- Agent-charter: `artefacten/aeo/aeo.02.agent-curator/agent-curator.charter.md`

## Instructie

Voer de intent `rapporteer-ecosysteem-overzicht` uit conform het agent-contract.

Genereer een tabellarisch overzicht van alle agents in de opgegeven value stream fase, met status van aanwezige artefacten (charter, contracten, prompts, tasks) en canonieke consistentie per agent. Schrijf het resultaat weg naar `docs/agents-overzicht.md`.

**Aandachtspunten**:
- `value_stream_fase` kan ook `alles` zijn om alle value stream fasen te rapporteren.
- `detail_niveau` default is `samenvatting`; bij `volledig` ook bevindingen per agent opnemen.
- Het bestand `docs/agents-overzicht.md` wordt bij elke run overschreven.
