---
agent: ecosysteem-coordinator
agent-id: fnd.01.ecosysteem-coordinator
value_stream: fnd
value_stream_fase: fnd.01
bronhouding: Input-gebonden
versie: 1.0.0
digest: 8058
status: vers
---
# Agent Boundary: Ecosysteem-coordinator

**agent-naam**: ecosysteem-coordinator
**capability-boundary**: Orkestreert ecosysteem-brede lifecycle-taken (instructie-generatie, task-aggregatie) die geen individuele agent toebehoort; raakt geen agent-inhoud aan.
**doel**: Waarborgen dat alle agents consistent kunnen opereren door shared infrastructure en cross-cutting concerns centraal te beheren.
**domein**: Ecosysteem-lifecycle

---

## Mandarin-agent-classificatie

| As               | Waarde            |
|------------------|-------------------|
| Vormingsfase     | Operationeel in alle fasen |
| Betekeniseffect  | Geen betekenis    |
| Werking          | Conditioneel      |
| Bronhouding      | Input-gebonden    |

**Validatie**: Operationeel in alle fasen × Geen betekenis × Conditioneel × Input-gebonden — coherente combinatie. Positionering volgt `mandarin-ordeningsconcepten.md`.

## Opereert in Value stream fasen

- fnd.01 — Fundamentele Agents (Infrastructuur)
- Ondersteunt alle value streams

---

## Toelichting

**Wat doet de agent concreet?**
- Assembleert execution-bestanden uit charter + contract + prompt templates
- Aggregeert agent-specifieke task-configuraties naar globale `.vscode/tasks.json`
- Voert `bootstrap:` declaraties uit prompt frontmatter uit

**Welke inputs verwacht de agent?**
- Agent-naam en intent voor instructie-generatie
- Prompt-bestanden met frontmatter metadata

**Welke outputs levert de agent?**
- Execution-bestanden in `executions/` folder
- Geaggregeerde `tasks.json` configuratie

---

## Voorstellen agent contracten (intents)

- `genereer-instructies` — Assembleer execution-bestand uit charter + contract + prompt
- `aggregeer-tasks` — Aggregeer agent-specifieke tasks naar globale tasks.json op basis van beleid-workspace.md

---

## Zorgt voor

- Uniforme instructie-generatie onafhankelijk van welke agent wordt uitgevoerd
- Gecentraliseerd configuratie-beheer zonder duplicatie in agent-runners

---

## Neemt geen beslissingen over

- Inhoud van agent-charters of -contracts (dat doet capability-architect / agent-ontwerper)
- Kwaliteit of correctheid van agents (dat doet agent-curator)
- Agent-specifieke business logic (dat doet de betreffende agent zelf)

---

## Mogelijke raakvlakken (ter informatie)

- **Agents met aangrenzende scope**:
  - `agent-engineer` — scaffoldt runners en prompts; ecosysteem-coordinator assembleert/aggregeert
  - `agent-curator` — valideert agents; ecosysteem-coordinator valideert alleen structuur
  
- **Mogelijke overlap-punten**:
  - `merge-tasks` functionaliteit was in agent-engineer runner, nu geïntegreerd als `aggregeer-tasks`
  - `generate-instructions` functionaliteit was in agent-engineer runner, nu geïntegreerd

- **Te onderzoeken door Agent Curator**:
  - Migratie van `pipeline` van agent-engineer naar ecosysteem-coordinator

---

## Referentie naar criteria

- **Naamgeving**: `ecosysteem-coordinator` drukt uit dat dit een coördinerende rol is, geen creërende of validerende
- **Positionering**: fnd.01 (Fundamentele Agents) omdat dit de infrastructuur betreft waarop alle agents draaien
- **Doctrine-consistentie**: Volgt doctrine-agent-charter-normering Principe 2 (Eenduidige Verantwoordelijkheid) door alleen lifecycle-orchestratie te claimen
