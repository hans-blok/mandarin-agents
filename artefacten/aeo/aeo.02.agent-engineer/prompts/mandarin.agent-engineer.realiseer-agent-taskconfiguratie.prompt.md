---
agent: mandarin.agent-engineer
intent: realiseer-agent-taskconfiguratie
intent-id: aeo.02.agent-engineer.02
template: ~
bronhouding: Input-gebonden
versie: 1.0.0
input_parameters:
  - agent_naam
value_stream_fase: aeo.02
afnemers:
  - agent: ecosysteem-coordinator
    intent: aggregeer-tasks
    consumes:
      type: task-configuratie
      required: true

---
