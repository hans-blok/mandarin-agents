---
agent: mandarin.capability-architect
intent: definieer-agent-boundary
value_stream_fase: aeo.02

input_files:
  # Verplichte input bestanden voor deze intent
  template_file: "artefacten/aeo/aeo.02.capability-architect/templates/agent-boundary.template.md"
  # Optioneel:
  # referentie_boundaries: "artefacten/{vs}/{vs}.{fase}.{vergelijkbare-agent}/{vergelijkbare-agent}.agent-boundary.md"

bootstrap:
  script: scripts/bootstrap_canon_consult.py

# Canon URL en grondslagen worden gelezen uit beleid-workspace.md
# Agent-instructies staan in capability-architect.definieer-agent-boundary.agent.md
# Charter wordt automatisch geladen: capability-architect.charter.md (zelfde folder)
---
