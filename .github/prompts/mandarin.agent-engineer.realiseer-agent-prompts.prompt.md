---
agent: mandarin.agent-engineer
intent: realiseer-agent-prompts
versie: 1.0.0
input_parameters:
  # verplichte runtime-parameters: geen
  # optioneel: expliciete contractbestanden; standaard via auto-discovery
  - agent_contracts
  # optioneel: indien leeg worden prompts voor alle intents gerealiseerd
  - intent
value_stream_fase: aeo.02

bootstrap:
  script: scripts/bootstrap_canon_consult.py

# Canon URL en grondslagen worden gelezen uit beleid-workspace.md
# Agent-instructies staan in agent-engineer.realiseer-agent-prompts.agent.md
# Charter wordt automatisch geladen: agent-engineer.charter.md (zelfde folder)
# Agent-contracten worden automatisch gedetecteerd via workspace-conventie (geen boundary_file)
---
