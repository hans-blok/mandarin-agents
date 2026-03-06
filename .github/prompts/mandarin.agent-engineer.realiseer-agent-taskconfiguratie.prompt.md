---
agent: mandarin.agent-engineer
intent: realiseer-agent-taskconfiguratie
versie: 1.0.0
input_parameters:
  # verplicht
  - agent_naam
 
value_stream_fase: aeo.02

bootstrap:
  script: scripts/bootstrap_canon_consult.py

# Canon URL en grondslagen worden gelezen uit beleid-workspace.md
# Agent-instructies staan in agent-engineer.realiseer-agent-taskconfiguratie.agent.md
# Charter wordt automatisch geladen: agent-engineer.charter.md (zelfde folder)
# Agent-contracten worden gebruikt voor intent-discovery; boundary_file wordt niet gebruikt
# Task-output vast: artefacten/aeo/aeo.02.agent-engineer/tasks/aeo-02.agent-engineer.tasks.json
---
