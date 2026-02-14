---
agent: mandarin.agent-smeder
intent: leg-vast-templates
value_stream_fase: aeo.02

input_files:
  boundary_file: "artefacten/{vs}/{vs}.{fase}.{agent}/agent-boundary-{agent}.md"

bootstrap:
  script: scripts/bootstrap_canon_consult.py

# Canon URL en grondslagen worden gelezen uit beleid-workspace.md
# Agent-instructies staan in agent-smeder.leg-vast-templates.agent.md
# Charter wordt automatisch geladen: agent-smeder.charter.md (zelfde folder)
---
