---
agent: mandarin.agent-engineer
intent: realiseer-agent-runner
versie: 1.0.0
input_parameters:
  # verplicht
  - agent_naam
  # optioneel: expliciete contractfolder; standaard via auto-discovery
  - contract_folder
  # optioneel
  - runner_output_folder
  # optioneel
  - overwrite_existing
value_stream_fase: aeo.02

bootstrap:
  script: scripts/bootstrap_canon_consult.py

# Canon URL en grondslagen worden gelezen uit beleid-workspace.md
# Agent-instructies staan in agent-engineer.realiseer-agent-runner.agent.md
# Charter wordt automatisch geladen: agent-engineer.charter.md (zelfde folder)
# Agent-contracten zijn bron voor intent- en parameterafleiding; boundary_file wordt niet gebruikt
---
