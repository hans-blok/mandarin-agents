---
agent: mandarin.agent-smeder
intent: leg-vast-agent-runner
value_stream_fase: aeo.02

input_files:
  boundary_file: "artefacten/{vs}/{vs}.{fase}.{agent}/agent-boundary-{agent}.md"
  templates_folder: "artefacten/{vs}/{vs}.{fase}.{agent}/templates/"
  charter_file: "artefacten/{vs}/{vs}.{fase}.{agent}/{agent}.charter.md"
  contracts_folder: "artefacten/{vs}/{vs}.{fase}.{agent}/agent-contracten/"
  prompts_folder: "artefacten/{vs}/{vs}.{fase}.{agent}/prompts/"
  template_file: "artefacten/aeo/aeo.02.agent-smeder/templates/agent-runner.skeleton.py"

bootstrap:
  script: scripts/bootstrap_canon_consult.py

# Canon URL en grondslagen worden gelezen uit beleid-workspace.md
# Agent-instructies staan in agent-smeder.leg-vast-agent-runner.agent.md
# Charter wordt automatisch geladen: agent-smeder.charter.md (zelfde folder)
---
