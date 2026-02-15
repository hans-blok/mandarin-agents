---
agent: mandarin.capability-architect
intent: definieer-agent-boundary
value_stream_fase: aeo.02

bootstrap:
  script: scripts/bootstrap_canon_consult.py

input_files:
  template: artefacten/aeo/aeo.02.capability-architect/templates/agent-boundary.template.md

# Canon URL en grondslagen worden gelezen uit beleid-workspace.md
# Agent-instructies staan in capability-architect.definieer-agent-boundary.agent.md
# Charter wordt automatisch geladen: capability-architect.charter.md (zelfde folder)
# Template wordt automatisch geladen en beschikbaar als [TEMPLATE] placeholder
---
