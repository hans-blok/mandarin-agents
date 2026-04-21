---
agent: mandarin.agent-ontwerper
intent: definieer-agent-template
intent-id: aeo.02.agent-ontwerper.03
template: ~
bronhouding: Canon-gebonden
versie: 1.2.0
input_parameters:
  - agent_naam
value_stream_fase: aeo.02
werkbronnen:
  - name: boundary
    type: agent-boundary
    required: true
    lookup:
      strategy: same-agent-folder
      pattern: "*.agent-boundary.md"
  - name: inspiratie
    type: artefact
    required: false
    lookup:
      strategy: workspace-root
      pattern: "temp/*"
afnemers:
  - agent: agent-engineer
    intent: realiseer-agent-prompts
    consumes:
      type: agent-template-document
      required: false

---
