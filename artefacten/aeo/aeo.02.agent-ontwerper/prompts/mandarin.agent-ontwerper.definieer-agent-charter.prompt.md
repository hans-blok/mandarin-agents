---
agent: mandarin.agent-ontwerper
intent: definieer-agent-charter
intent-id: aeo.02.agent-ontwerper.01
template: templates/agent-charter.template.md
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
  - name: contracten
    type: agent-contract
    required: false
    lookup:
      strategy: same-agent-folder
      pattern: "agent-contracten/*.agent.md"

---
