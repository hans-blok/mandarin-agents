---
agent: ecosysteem-coordinator
value_stream: aeo
value_stream_fase: aeo.02
versie: 1.0.0
---

# Agent Boundary: Ecosysteem-coordinator

**agent-naam**: ecosysteem-coordinator
**capability-boundary**: Orkestreert ecosysteem-brede lifecycle-taken (canon-synchronisatie, instructie-generatie, configuratie-aggregatie) die geen individuele agent toebehoort; raakt geen agent-inhoud aan en wijzigt geen canon.
**doel**: Waarborgen dat alle agents consistent kunnen opereren door shared infrastructure en cross-cutting concerns centraal te beheren.
**domein**: Ecosysteem-lifecycle

---

## Mandarin-agent-classificatie (4 orthogonale assen)

- **Vormingsfase** (fase van vorming of ontwikkeling)
  - [x] Operationeel in alle fasen
  - [ ] Verkenning (onderzoeken van intentie, probleemstelling of richting)
  - [ ] Ordening (structureren van intentie en expliciet maken van samenhang)
  - [ ] Vastlegging (betekenis bindend vaststellen binnen de workspace)
  - [ ] Realisatie (betekenis werkend maken in systemen of processen)
  - [ ] Toetsing (gerealiseerd artefact beoordelen tegen een norm)
  - [ ] Operationalisatie (gerealiseerde structuur formeel in werking stellen)

- **Betekeniseffect** (effect op betekenis)
  - [x] Geen betekenis (nul-positie, alleen voor conditionele werking)
  - [ ] Beschrijvend (documenteert, vooraf en achteraf)
  - [ ] Structurerend (maakt samenhang en relaties expliciet)
  - [ ] Normerend (normeert structuur en indeling voor realisatie en ook toetsing)
  - [x] Vastleggend (realiseert direct gedrag, structuur of configuratie)
  - [ ] Realiserend (realiseert feitelijk gedrag, structuur of configuratie)
  - [ ] Evaluerend (legt oordeel of duiding vast, beoordeelt kwaliteit)

- **Werking** (inhoud, representatie of voorwaarden)
  - [ ] Inhoudelijk (werkt direct op betekenisvolle artefacten)
  - [ ] Representatie-omvormend (zet inhoud om tussen representaties, betekenis-blind)
  - [x] Conditioneel (werkt op voorwaarden en hygiëne, niet op inhoud)

- **Bronhouding** (kennisbronnen en herleidbaarheid)
  - [x] Input-gebonden (output 100% herleidbaar tot input)
  - [ ] Canon-gebonden (baseert zich expliciet op canon)
  - [ ] Externe-bron-gebonden (haalt kennis uit externe bronnen, maar wel met kaders)
  - [ ] Exploratief (gebruikt generatieve capaciteiten, aannames expliciet)

---

## Opereert in Value stream fasen

- aeo.02 — Agent Ecosysteem Ontwikkeling (Ecosysteeminrichting)

---

## Toelichting

**Wat doet de agent concreet?**
- Raadpleegt mandarin-canon en registreert commit SHA voor traceerbaarheid
- Assembleert execution-bestanden uit charter + contract + prompt templates
- Merget agent-specifieke task-configuraties naar globale `.vscode/tasks.json`
- Voert `bootstrap:` declaraties uit prompt frontmatter uit
- Valideert of agent-folders voldoen aan doctrine-structuur

**Welke inputs verwacht de agent?**
- Workspace-beleid dat het pad naar mandarin-canon repository specificeert (lokaal of GitHub URL)
- Agent-naam en intent voor instructie-generatie
- Prompt-bestanden met frontmatter metadata
- Agent-naam en intent voor instructie-generatie
- Prompt-bestanden met frontmatter metadata

**Welke outputs levert de agent?**
- Execution-bestanden in `prompt-instructions/` folder
- Samengevoegde `tasks.json` configuratie
- Audit-logs in `audit/canon-consult.log.md`

---

## Voorstellen agent contracten (intents)

- `consulteer-canon` — Raadpleeg mandarin-canon, log commit SHA, retourneer grondslagen
- `genereer-instructies` — Assembleer execution-bestand uit canon + charter + contract + prompt
- `merge-configuraties` — Voeg agent-specifieke tasks samen naar globale tasks.json
- `valideer-agent-structuur` — Controleer doctrine-compliance van agent-folders

---

## Zorgt voor

- Consistente canon-raadpleging met verifieerbare audit trail
- Uniforme instructie-generatie onafhankelijk van welke agent wordt uitgevoerd
- Gecentraliseerd configuratie-beheer zonder duplicatie in agent-runners
- Structuur-validatie als kwaliteitspoort voor nieuwe agents

---

## Neemt geen beslissingen over

- Inhoud van agent-charters of -contracts (dat doet capability-architect / agent-ontwerper)
- Kwaliteit of correctheid van agents (dat doet agent-curator)
- Canon-inhoud of doctrine-wijzigingen (dat doet constitutioneel-auteur)
- Agent-specifieke business logic (dat doet de betreffende agent zelf)

---

## Mogelijke raakvlakken (ter informatie)

- **Agents met aangrenzende scope**:
  - `agent-engineer` — scaffoldt runners en prompts; ecosysteem-coordinator assembleert/aggregeert
  - `agent-curator` — valideert agents; ecosysteem-coordinator valideert alleen structuur
  
- **Mogelijke overlap-punten**:
  - `merge-tasks` functionaliteit zit nu in agent-engineer runner
  - `generate-instructions` functionaliteit zit nu in agent-engineer runner
  - Canon consultatie is geïntegreerd in de ecosysteem-coordinator runner

- **Te onderzoeken door Agent Curator**:
  - Migratie van `generate-instructions`, `merge-tasks`, `pipeline` van agent-engineer naar ecosysteem-coordinator
  - ~~Integratie van `bootstrap_canon_consult.py` als intent van deze agent~~ ✓ Voltooid

---

## Referentie naar criteria

- **Naamgeving**: `ecosysteem-coordinator` drukt uit dat dit een coördinerende rol is, geen creërende of validerende
- **Positionering**: aeo.02 (Ecosysteeminrichting) omdat dit de infrastructuur betreft waarop agents draaien
- **Canon-consistentie**: Volgt doctrine-agent-charter-normering Principe 2 (Eenduidige Verantwoordelijkheid) door alleen lifecycle-orchestratie te claimen; volgt ook doctrine-agent-runner-architectuur uit de canon
