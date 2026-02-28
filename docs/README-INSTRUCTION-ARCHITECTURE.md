# Mandarin Agent Instruction Generation Architectuur

Dit document beschrijft de werkwijze en architectuurprincipes achter het Mandarin agent instruction generation systeem.

## Overzicht

Het Mandarin agent systeem gebruikt een **gedistribueerde architectuur** waarbij:
- **Regels** centraal worden beheerd in de canon (governance, doctrine, grondslagen)
- **Processen** decentraal worden uitgevoerd in workspaces (agents, scripts, runners)
- **Configuratie** per workspace wordt beheerd in `beleid-workspace.md`

Deze splitsing zorgt voor schaalbaarheid, consistentie en traceerbaarheid.

## Architectuur Principes

### 1. SOLID: Interface Segregation Principle

**Principe**: Interfaces bevatten alleen wat nodig is, niets meer.

**Toepassing**:
- Prompt bestanden (`.prompt.md`) bevatten **minimale metadata**
- Alleen wat `generate_instructions.py` nodig heeft: `agent`, `intent`, `value_stream`, `bootstrap`
- Geen redundante velden zoals `charter_ref`, `charter-acknowledgement`, `canon-resolved-ref`
- Agent-instructies staan in aparte `.agent.md` bestanden

**Voorbeeld minimale prompt**:
```yaml
---
agent: mandarin.agent-curator
intent: bepaal-agent-boundary
value_stream: aeo

bootstrap:
  script: scripts/bootstrap_canon_consult.py
---
```

### 2. Single Source of Truth

**Principe**: Elke informatie heeft precies één authoritative bron.

**Toepassing**:
- **Canon URL**: `beleid-workspace.md` → `canon_github_url`
- **Grondslagen-patronen**: `beleid-workspace.md` → `grondslagen` map
- **Governance regels**: mandarin-canon repository
- **Canon consultatie logging**: `audit/canon-consult.log.md` (centraal append-only log)

**Voordelen**:
- Geen inconsistenties tussen prompt bestanden
- Eén plek om configuratie aan te passen
- Makkelijk auditeerbaar

### 3. Separation of Concerns: Proces vs. Regels

**Principe**: Scheiding tussen "hoe we werken" (proces) en "waaraan we moeten voldoen" (regels).

**Toepassing**:

| Concern | Locatie | Eigenaar | Frequentie wijziging |
|---------|---------|----------|---------------------|
| **Regels** | mandarin-canon repo | Governance | Laag (wekelijks/maandelijks) |
| **Proces** | workspace scripts | Engineers | Hoog (dagelijks) |
| **Config** | beleid-workspace.md | Workspace team | Medium (per workspace setup) |

**Voordeel**: Procesverbeteringen (zoals generate_instructions.py optimaliseren) vereisen geen wijzigingen in governance documenten.

### 4. Convention over Configuration

**Principe**: Verstandige defaults, minimale configuratie.

**Conventies**:
- Workspace configuratie: **altijd** `beleid-workspace.md` in root (hardcoded in `generate_instructions.py`)
- Canon logging: **altijd** `audit/canon-consult.log.md`
- Prompt bestanden: altijd `mandarin.<agent>.<intent>.prompt.md` naamgeving
- Agent contracten: altijd `<agent>.<intent>.agent.md` in agent folder

## VS Code Task Integratie

Het systeem biedt naadloze integratie met VS Code via tasks:

### Task: "Agent: Execute (Generate + Save)"

```json
{
  "label": "Agent: Execute (Generate + Save)",
  "type": "process",
  "command": "powershell",
  "args": [
    "-Command",
    "python scripts/generate_instructions.py --agent ${input:agentName} --intent ${input:intentName} --execution-file agent-execution/<hash>.<agent>.<intent>.md; if ($LASTEXITCODE -eq 0) { code <file> }"
  ]
}
```

**Gebruik**:
1. Druk op `Ctrl+Shift+P`
2. Typ "Tasks: Run Task"
3. Selecteer "Agent: Execute (Generate + Save)"
4. Voer agent naam en intent in
5. Execution file wordt gegenereerd en geopend

**Voordelen**:
- Geen command-line kennis nodig
- Automatische naamgeving met hash
- Direct reviewen in editor
- Traceerbaar in agent-execution/ folder

## Workflow: Agent Uitvoeren

### Stap 0: Canon Consultatie (Verplicht)

Voordat een agent werkt, moet deze de governance-regels raadplegen:

```
┌───────────────────────────────────────────────────────────────────┐
│ 1. generate_instructions.py leest beleid-workspace.md            │
│    ↓                                                              │
│ 2. Haalt canon_github_url en grondslagen-patroon                 │
│    ↓                                                              │
│ 3. Voert bootstrap_canon_consult.py uit                          │
│    ↓                                                              │
│ 4. Bootstrap kloont/update canon repo                            │
│    ↓                                                              │
│ 5. Leest grondslagen (constitutie, doctrine, etc.)               │
│    ↓                                                              │
│ 6. Logt consultatie naar audit/canon-consult.log.md              │
│    ↓                                                              │
│ 7. generate_instructions.py vervangt placeholders                │
│    ↓                                                              │
│ 8. Genereert execution-ready instructies en schrijft naar file   │
│    ↓                                                              │
│ 9. Agent ontvangt volledige context en kan werken                │
└───────────────────────────────────────────────────────────────────┘
```

### Commando

```bash
# Modern (auto-discovery)
python scripts/generate_instructions.py \
  --agent capability-architect \
  --intent definieer-agent-boundary \
  --execution-file agent-execution/xxxx.capability-architect.definieer-agent-boundary.md

# Klassiek (backward compatible)
python scripts/generate_instructions.py \
  .github/prompts/mandarin.agent-curator.bepaal-agent-boundary.prompt.md \
  -p agent_naam=nieuwe-agent \
  -p value_stream_fase=aeo.02 \
  --input-file input/beschrijving.md
```

### Wat gebeurt er?

1. **Workspace config laden**: `beleid-workspace.md` wordt gelezen
2. **Prompt metadata laden**: YAML frontmatter uit `.prompt.md`
3. **Bootstrap uitvoeren**: 
   - Canon URL uit `beleid-workspace.md`
   - Grondslagen-patroon uit `beleid-workspace.md` op basis van `value_stream`
   - Consultatie gelogd naar `audit/canon-consult.log.md`
4. **Placeholders vervangen**: `[agent_naam]`, `[INPUT_CONTENT]`, etc.
5. **Agent instructies tonen**: Volledige, samengestelde prompt

## Bestandsstructuur

### beleid-workspace.md (Workspace Root)

Centrale configuratie per workspace:

```yaml
---
workspace: mandarin-agents
value_stream: aeo
canon_github_url: https://github.com/hans-blok/mandarin-canon.git

# Grondslagen-patronen per value stream
grondslagen:
  aeo: "grondslagen/.algemeen/*,grondslagen/aeo/*"
  sfw: "grondslagen/.algemeen/*,grondslagen/sfw/*"
  aod: "grondslagen/.algemeen/*,grondslagen/aod/*"
  kvl: "grondslagen/.algemeen/*,grondslagen/kvl/*"
  miv: "grondslagen/.algemeen/*,grondslagen/miv/*"
  fnd: "grondslagen/.algemeen/*,grondslagen/fnd/*"
---

# Beleid voor de MANDARIN-AGENTS workspace
...
```

### Prompt Bestand (.prompt.md)

Minimale metadata (SOLID Interface Segregation):

```yaml
---
agent: mandarin.agent-curator
intent: bepaal-agent-boundary
value_stream: aeo

bootstrap:
  script: scripts/bootstrap_canon_consult.py
  
# Canon URL en grondslagen komen uit beleid-workspace.md
# Agent-instructies staan in .agent.md bestand
---
```

### Agent Contract (.agent.md)

Volledige agent-instructies en outputspecificatie:

```markdown
# Agent Contract: bepaal-agent-boundary

## Input
- [agent_naam]: Naam van de nieuwe agent
- [INPUT_CONTENT]: Beschrijving capability boundary

## Taak
Bepaal de agent boundary en maak folder structuur aan.

## Output
- `artefacten/[value_stream_fase].[agent_naam]/[agent_naam].boundary.md`
```

### Canon Consult Log (audit/canon-consult.log.md)

Append-only audit log van alle canon consultaties:

```markdown
---
Agent: agent-curator
Value Stream: aeo
Intent: bepaal-agent-boundary
Method: manual
Canon Path: c:\git\mandarin-canon
Branch: main
SHA: a3f5b2c
Timestamp: 2026-02-13T14:30:00+01:00

Consulted Files:
| Folder | Bestand |
|--------|---------|
| grondslagen/.algemeen | constitutie.md |
| grondslagen/aeo | doctrine-agent-charter.md |
---
```

## Voordelen van deze Architectuur

### 1. Schaalbaarheid
- Nieuwe value streams: voeg toe aan `beleid-workspace.md`
- Nieuwe agents: maak minimale `.prompt.md`
- Geen redundantie in 100+ prompt bestanden

### 2. Traceerbaarheid
- Centraal log van canon consultaties
- Elke agent-uitvoering gedocumenteerd
- SHA commit hash van gebruikte canon versie

### 3. Governance Compliance
- Verplichte canon consultatie (kan niet worden overgeslagen)
- Grondslagen altijd via beleid-workspace.md (single source of truth)
- Auditeerbaar via logs

### 4. Onderhoudbaarheid
- Wijzig canon URL op één plek
- Wijzig grondslagen-patroon op één plek
- Scripts onafhankelijk te verbeteren

### 5. Developer Experience
- Minimale boilerplate in prompts
- Duidelijke conventies
- Self-documenting via docstrings
- **VS Code integratie**: Direct uitvoeren via tasks (Ctrl+Shift+P > Tasks: Run Task)
- **Auto-discovery**: Agent boundary files worden automatisch gevonden
- **Execution files**: Ready-to-execute instructies met metadata

## Anti-Patterns (Vermijd Dit)

### ❌ Canon URL in elk prompt bestand
```yaml
# NIET DOEN
bootstrap:
  canon-github-url: https://github.com/hans-blok/mandarin-canon.git  # ← Redundant!
```

**Probleem**: Bij URL wijziging moet je 100+ bestanden aanpassen.

### ❌ Grondslagen-patronen in prompts
```yaml
# NIET DOEN  
bootstrap:
  grondslagen: "grondslagen/.algemeen/*,grondslagen/aeo/*"  # ← Hardcoded!
```

**Probleem**: Bij wijziging folder-structuur in canon moet je alle prompts aanpassen.

### ❌ Charter metadata in prompts
```yaml
# NIET DOEN
charter-acknowledgement:
  charter-id: agent-curator
  charter-versie: 1.0.0
  canon-resolved-ref: a3f5b2c  # ← Wordt runtime bepaald!
```

**Probleem**: Runtime informatie hoort niet in static files. Gebruik logs.

### ❌ Agent-instructies in .prompt.md
```markdown
# NIET DOEN
---
agent: agent-curator
---

# Lange agent instructies hier...
(Dit hoort in .agent.md bestand)
```

**Probleem**: Prompt bestanden worden groot en onoverzichtelijk. Gebruik `.agent.md` voor instructies.

## Migratie van Oude Prompts

Als je oude prompts hebt met redundante metadata:

```bash
# Script om prompts te minimaliseren
# (Verwijder grondslagen, canon-github-url, charter-acknowledgement)
```

Of handmatig per prompt:
1. Verwijder `charter-acknowledgement` sectie
2. Verwijder `grondslagen` uit `bootstrap`
3. Verwijder `canon-github-url` uit `bootstrap`
4. Voeg comment toe: `# Canon URL en grondslagen komen uit beleid-workspace.md`

## Veelgestelde Vragen

### Kan ik de canon URL per prompt overschrijven?

Ja, maar **not recommended**. De fallback-mechanisme in `generate_instructions.py` ondersteunt dit:
```yaml
bootstrap:
  canon-github-url: https://github.com/other/canon  # Override (discouraged)
```

Maar je verliest dan **Single Source of Truth** principe.

### Waar worden agent-instructies opgeslagen?

In `.agent.md` bestanden naast de `.prompt.md`:
- `mandarin.agent-curator.bepaal-agent-boundary.prompt.md` (metadata)
- `agent-curator.bepaal-agent-boundary.agent.md` (instructies)

### Hoe voeg ik een nieuwe value stream toe?

Voeg toe aan `beleid-workspace.md`:
```yaml
grondslagen:
  nieuwe: "grondslagen/.algemeen/*,grondslagen/nieuwe/*"
```

Alle prompts met `value_stream: nieuwe` gebruiken dit automatisch.

### Moet elke workspace een beleid-workspace.md hebben?

**Ja**. Dit is de conventie (hardcoded). Zonder dit bestand:
- Geen canon URL beschikbaar
- Geen grondslagen-patronen
- Fallback naar hardcoded defaults

## Zie Ook

- [beleid-workspace.md](../beleid-workspace.md) - Workspace configuratie template
- [scripts/generate_instructions.py](../scripts/generate_instructions.py) - Instruction generator implementatie
- [.vscode/tasks.json](../.vscode/tasks.json) - VS Code task integratie
- [templates/agent-charter.template.md](../templates/agent-charter.template.md) - Charter template

---

*Laatste update: 2026-02-15*  
*Architectuur versie: 2.1 (Instruction generation + VS Code integratie)*
