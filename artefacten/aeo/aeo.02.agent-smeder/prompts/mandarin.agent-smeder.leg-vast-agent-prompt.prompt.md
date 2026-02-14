---
agent: mandarin.agent-smeder
intent: leg-vast-agent-prompt
value_stream_fase: aeo.02

input_files:
  boundary_file: "artefacten/{vs}/{vs}.{fase}.{agent}/agent-boundary-{agent}.md"
  templates_folder: "artefacten/{vs}/{vs}.{fase}.{agent}/templates/"
  contracts_folder: "artefacten/{vs}/{vs}.{fase}.{agent}/agent-contracten/"
  template_file: "artefacten/aeo/aeo.02.agent-smeder/templates/agent-prompt.template.md"

bootstrap:
  script: scripts/bootstrap_canon_consult.py

# Canon URL en grondslagen worden gelezen uit beleid-workspace.md
# Agent-instructies staan in agent-smeder.leg-vast-agent-prompt.agent.md
# Charter wordt automatisch geladen: agent-smeder.charter.md (zelfde folder)
---
