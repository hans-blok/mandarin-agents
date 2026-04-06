# Mandarin Agents

Deze repository bevat de **canonieke definitie van Mandarin agents**:
charters, contracts, prompts, templates, runners en ondersteunende tooling
voor het Mandarin workspace-ecosysteem.

De inhoud van deze repo wordt geconsumeerd door andere workspaces (bijv.
architectuur- of delivery-workspaces), maar is zelf het "bron-boek" van
alle agents.

## Globale structuur

De relevante top-level mappen zijn:

```text
mandarin-agents/
â”œâ”€â”€ artefacten/           # Canonieke agent-artefacten per value stream
â”‚   â”œâ”€â”€ aeo/              # Agent Ecosysteem Ontwikkeling (aeo)
â”‚   â”œâ”€â”€ aod/              # Architectuur Ontwerp (aod)
â”‚   â”œâ”€â”€ fnd/              # Fundamenten (fnd)
â”‚   â””â”€â”€ sfw/              # Software Fabricage (sfw)
â”œâ”€â”€ docs/                 # Gegenereerde overzichten (MkDocs bron)
â”‚   â”œâ”€â”€ agents-overzicht.md
â”‚   â”œâ”€â”€ agents-prompts-overzicht.md
â”‚   â””â”€â”€ assets/
â”œâ”€â”€ scripts/              # Ondersteunende scripts
â”‚   â””â”€â”€ copy_prompts_mandarin_agents.py
â”œâ”€â”€ executions/           # Execution-bestanden (bronpakketten) voor runners/LLM
â”œâ”€â”€ audit/                # Logfiles (canon consult, agent-instructions)
â”œâ”€â”€ concepts/             # Conceptuele documentatie (domein- en ordeningsconcepten)
â”œâ”€â”€ mkdocs.yml            # Site-configuratie voor GitHub Pages / MkDocs
â”œâ”€â”€ requirements.txt      # Python dependencies voor runners/tools
â””â”€â”€ requirements-docs.txt # Extra dependencies voor documentatie build
```

Binnen `artefacten/` is de structuur verder per value stream en agent
gestandaardiseerd. Voorbeeld voor `aeo.02.agent-curator`:

```text
artefacten/aeo/aeo.02.agent-curator/
â”œâ”€â”€ agent-curator.agent-boundary.md
â”œâ”€â”€ agent-curator.charter.md
â”œâ”€â”€ agent-contracten/
â”œâ”€â”€ prompts/
â”œâ”€â”€ templates/
â”œâ”€â”€ tasks/
â””â”€â”€ runner/
		â””â”€â”€ agent-curator.runner.py
```

## Kernrunners

### Ecosysteem-coordinator runner

Bestand: `artefacten/fnd/fnd.01.ecosysteem-coordinator/runner/ecosysteem-coordinator.runner.py`

Deze runner is de centrale "One Agent, One Runner"-router voor o.a.:

- `consulteer-canon` â€“ canon-consultatie + logging
- `genereer-instructies` â€“ samengestelde agent-instructies genereren
- `merge-configuraties` â€“ VS Code tasks uit agent-tasks samenvoegen
- `valideer-agent-structuur` â€“ agent folderstructuur toetsen
- `list-agents` â€“ beschikbare agents per value stream tonen
- `fetch-agents` â€“ prompts/agents/tasks naar een consumer-workspace kopiÃ«ren

Voorbeeld (lijst agents in aeo.02):

```powershell
python artefacten/fnd/fnd.01.ecosysteem-coordinator/runner/ecosysteem-coordinator.runner.py list-agents aeo.02
```

### Agent-curator runner

Bestand: `artefacten/aeo/aeo.02.agent-curator/runner/agent-curator.runner.py`

Deze runner verzorgt publicatie-overzichten op ecosysteemniveau:

- `publiceer-json` â€“ `agents-publicatie.json` genereren (schema v2.0)
- `publiceer-overzicht` â€“ markdown overzicht van alle agents naar `docs/agents-overzicht.md`
- `rapporteer-prompts-overzicht` â€“ via ecosysteem-coordinator execution-instructies
	genereren voor het prompts-overzicht

Voorbeeld (generate agents-overzicht):

```powershell
python artefacten/aeo/aeo.02.agent-curator/runner/agent-curator.runner.py publiceer-overzicht
```

Na het draaien van deze runner kun je de gegenereerde overzichtsbestanden
vinden in `docs/`.

## Execution-bestanden

Wanneer je `genereer-instructies` (via de ecosysteem-coordinator) of
`rapporteer-prompts-overzicht` (via de agent-curator runner) gebruikt,
worden execution-bestanden aangemaakt in `executions/`:

```text
executions/
â”œâ”€â”€ <hash>.agent-curator.rapporteer-prompts-overzicht.md
â””â”€â”€ history/
```

Deze bestanden bevatten:

- YAML-frontmatter met execution-metadata (agent, intent, execution_id, canon_ref, ...)
- De volledige samengestelde instructies (charter + contract + prompt + context)

Ze zijn bedoeld om 1-op-1 in een LLM of agent-runtime te plakken.

## Documentatie (MkDocs / GitHub Pages)

De repo bevat een minimale MkDocs-config om overzichten als site te
publiceren (bijv. via GitHub Pages):

- Config: `mkdocs.yml`
- Brondocs: `docs/agents-overzicht.md`, `docs/agents-prompts-overzicht.md`

Lokale build:

```powershell
pip install -r requirements-docs.txt
mkdocs serve
```

Daarna is de site beschikbaar op `http://127.0.0.1:8000` (of het adres
dat MkDocs toont).

## Scripts

In `scripts/` staat momenteel Ã©Ã©n script:

- `copy_prompts_mandarin_agents.py` â€“ ondersteunt het genereren van een
	aggregatie (bijv. `agents.yaml`) uit de canonieke prompts.

Gebruik dit script alleen als je weet hoe het in jouw consumer-workspace
is geÃ¯ntegreerd; het is primair een hulpscript voor build/publishing.

## Vereisten

- **Python 3.10+** â€“ voor runners en tooling
- **Git** â€“ voor werken met de canon-repository

Installeer dependencies voor deze repo:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Voor documentatie-builds gebruik je aanvullend `requirements-docs.txt`.

## Beleid & governance

- Workspace-beleid en canon-koppeling: `beleid-workspace.md`
- Canon en doctrines (externe repo): mandarin-canon (gebruikt door
	`consulteer-canon` in de ecosysteem-coordinator runner)

Voor agent-specifieke governance (boundaries, charters, contracts) zie de
respectieve bestanden onder `artefacten/<vs>/<vs>.<fase>.<agent>/`.

## Licentie

Zie de licentie- en herkomstinformatie in de individuele agent- en
templatebestanden.
