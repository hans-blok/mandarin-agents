# CLAUDE.md — mandarin-agents

## Wat is dit?

Dit is de **operationele workspace** van het Mandarin agent-ecosysteem. Agents worden hier ontworpen, gerealiseerd en uitgevoerd. De bijbehorende canonieke grondslagen (constitutie, doctrines) staan in `c:\git\mandarin-canon`.

## Architectuur in één zin

Elke agent heeft een vaste folderstructuur met boundary, charter, contracten, prompts, templates en een runner. De `ecosysteem-coordinator` assembleert bronnen en genereert uitvoeringsklare instructies.

## Folderstructuur

```
artefacten/{vs}/{vs}.{fase}.{agent}/
  {agent}.charter.md
  {agent}.agent-boundary.md
  agent-contracten/{agent}.{intent}.agent.md
  prompts/mandarin.{agent}.{intent}.prompt.md
  templates/{naam}.template.md
  runner/{agent}.runner.py        ← alleen bij fnd agents
executions/
  prompt-instructions/            ← gegenereerde prompt-instructies (LLM-ready)
  execution-ledger.json           ← append-only executielog
audit/
  canon-consult.log.md
  agent-instructions.log.md
```

Value streams: `fnd` (foundation), `aeo` (agent ecosysteem ontwikkeling), `aod`, `sfw`, `miv`.

## Centrale runner

```bash
python artefacten/fnd/fnd.01.ecosysteem-coordinator/runner/ecosysteem-coordinator.runner.py <subcommand>
```

| Subcommand | Wat het doet |
|------------|-------------|
| `genereer-instructies --agent <agent> --intent <intent> -p key=value` | Assembleert bronpakket → schrijft execution file naar `executions/prompt-instructions/` |
| `aggregeer-tasks` | Leest alle `tasks.json` bestanden → schrijft `.vscode/tasks.json` |
| `consulteer-canon --agent <agent> --value-stream <vs> --intent <intent>` | Logt canon SHA naar `audit/canon-consult.log.md` |
| `valideer-agent-structuur` | Valideert agent folder structuur tegen doctrine |
| `list-agents [value_stream_fase]` | Toont beschikbare agents |

**Typische aanroep:**
```bash
cd c:/git/mandarin-agents
python artefacten/fnd/fnd.01.ecosysteem-coordinator/runner/ecosysteem-coordinator.runner.py \
  genereer-instructies \
  --agent agent-ontwerper \
  --intent definieer-agent-charter \
  -p agent_naam=mijn-nieuwe-agent \
  -p value_stream_fase=aeo.01
```

Output verschijnt in `executions/prompt-instructions/`.

## Prompt-frontmatter

Elke prompt heeft YAML frontmatter die de runner instrueert:

```yaml
agent: mandarin.{agent-naam}
intent: {intent-kortschrift}
template: {relatief-pad-of-~}
value_stream_fase: {vs}.{fase}
werkbronnen:                        # bestanden die runner ophaalt voor de LLM
  - name: boundary
    type: agent-boundary
    required: true
    lookup:
      strategy: same-agent-folder   # of: workspace-root, explicit-path
      pattern: "*.agent-boundary.md"
```

**Vuistregel werkbronnen**: Runner-config (werkbronnen) hoort in de **prompt**, niet in het contract. Het contract beschrijft wat een mens moet weten om de agent te gebruiken.

## Governance & canon

- `beleid-workspace.md` — workspace governance (lees dit eerst bij twijfel)
- `c:\git\mandarin-canon\grondslagen\.normatief\.algemeen\constitutie.md` — bron van alle regels
- Agents raadplegen de canon verplicht vóór uitvoering; dit wordt gelogd in `audit/canon-consult.log.md`

## Naamgevingsconventies

| Artefact | Patroon | Voorbeeld |
|----------|---------|-----------|
| Agent ID | `{vs}.{fase}.{agent-naam}` | `aeo.02.agent-ontwerper` |
| Charter | `{agent}.charter.md` | `agent-ontwerper.charter.md` |
| Contract | `{agent}.{intent}.agent.md` | `agent-ontwerper.definieer-agent-charter.agent.md` |
| Prompt | `mandarin.{agent}.{intent}.prompt.md` | `mandarin.agent-ontwerper.definieer-agent-charter.prompt.md` |
| Template | `{naam}.template.md` | `agent-charter.template.md` |
| Execution file | `{yyyymmddNNNN}.{agent}.{intent}.md` | `202604200001.agent-ontwerper.definieer-agent-charter.md` |

Alle agent-namen: lowercase kebab-case. Intents: werkwoord-object in kebab-case.

## YAML header formaat (§5 EXECUTION)

Execution files volgen `yaml-header.template.md`:

```yaml
---
# IDENTIFICATIE
execution-id: {yyyymmddNNNN}
execution-code: exec-{id}

# RELATIES
agent-id: {vs}.{fase}.{agent}
intent-id: {vs}.{fase}.{agent}.{intent}
canon-ref: {sha}
bronhouding: Canon-gebonden
modus: handmatig

# META-DATA
execution-digest: {12-char sha256}
timestamp: {ISO 8601}
status: vers
---
```

## Taal

Alle artefacten, docstrings en output zijn in het **Nederlands**. Code is in Python (runner) of Markdown (artefacten).

## Wat niet te doen

- Wijzig nooit `beleid-workspace.md` of canon-doctrines zonder expliciete opdracht.
- Voeg geen werkbronnen toe aan contract-bestanden (`*.agent.md`) — die horen in de prompt.
- Schrijf geen execution files handmatig — gebruik altijd de runner.
- Commit geen bestanden in `executions/` of `audit/` tenzij expliciet gevraagd.
