---
agent: mandarin.agent-smeder
intent: leg-vast-agent-prompt-versie
value_stream_fase: aeo.02

input_files:
  boundary_file: "artefacten/{vs}/{vs}.{fase}.{agent}/agent-boundary-{agent}.md"
  existing_prompt_file: "artefacten/{vs}/{vs}.{fase}.{agent}/prompts/{agent}.{intent}.prompt.md"

bootstrap:
  script: scripts/bootstrap_canon_consult.py

# Canon URL en grondslagen worden gelezen uit beleid-workspace.md
# Agent-instructies staan in agent-smeder.leg-vast-agent-prompt-versie.agent.md
# Charter wordt automatisch geladen: agent-smeder.charter.md (zelfde folder)
---
