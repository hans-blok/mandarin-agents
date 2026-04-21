---
agent: mandarin.agent-ontwerper
intent: definieer-agent-contract
intent-id: aeo.02.agent-ontwerper.02
template: templates/agent-contract-intent.template.md
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
  - name: charter
    type: agent-charter
    required: false
    lookup:
      strategy: same-agent-folder
      pattern: "*.charter.md"
afnemers:
  - agent: agent-engineer
    intent: realiseer-agent-prompts
    consumes:
      type: agent-contract
      required: true
  - agent: agent-engineer
    intent: realiseer-agent-runner
    consumes:
      type: agent-contract
      required: true
  - agent: agent-curator
    intent: valideer-runner-contract-consistentie
    consumes:
      type: agent-contract
      required: true

---
