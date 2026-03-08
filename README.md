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
├── artefacten/           # Canonieke agent-artefacten per value stream
│   ├── aeo/              # Agent Ecosysteem Ontwikkeling (aeo)
│   ├── aod/              # Architectuur Ontwerp (aod)
│   ├── fnd/              # Fundamenten (fnd)
│   └── sfw/              # Software Fabricage (sfw)
├── docs/                 # Gegenereerde overzichten (MkDocs bron)
│   ├── agents-overzicht.md
│   ├── agents-prompts-overzicht.md
│   └── assets/
├── scripts/              # Ondersteunende scripts
│   └── copy_prompts_mandarin_agents.py
├── prompt-instructions/  # Execution-ready prompts voor runners/LLM
├── audit/                # Logfiles (canon consult, agent-instructions)
├── concepts/             # Conceptuele documentatie (domein- en ordeningsconcepten)
├── mkdocs.yml            # Site-configuratie voor GitHub Pages / MkDocs
├── requirements.txt      # Python dependencies voor runners/tools
└── requirements-docs.txt # Extra dependencies voor documentatie build
```

Binnen `artefacten/` is de structuur verder per value stream en agent
gestandaardiseerd. Voorbeeld voor `aeo.02.agent-curator`:

```text
artefacten/aeo/aeo.02.agent-curator/
├── agent-curator.agent-boundary.md
├── agent-curator.charter.md
├── agent-contracten/
├── prompts/
├── templates/
├── tasks/
└── runner/
		└── agent-curator.runner.py
```

## Kernrunners

### Ecosysteem-coordinator runner

Bestand: `artefacten/aeo/aeo.02.ecosysteem-coordinator/runner/ecosysteem-coordinator.runner.py`

Deze runner is de centrale "One Agent, One Runner"-router voor o.a.:

- `consulteer-canon` – canon-consultatie + logging
- `genereer-instructies` – samengestelde agent-instructies genereren
- `merge-configuraties` – VS Code tasks uit agent-tasks samenvoegen
- `valideer-agent-structuur` – agent folderstructuur toetsen
- `list-agents` – beschikbare agents per value stream tonen
- `fetch-agents` – prompts/agents/tasks naar een consumer-workspace kopiëren

Voorbeeld (lijst agents in aeo.02):

```powershell
python artefacten/aeo/aeo.02.ecosysteem-coordinator/runner/ecosysteem-coordinator.runner.py list-agents aeo.02
```

### Agent-curator runner

Bestand: `artefacten/aeo/aeo.02.agent-curator/runner/agent-curator.runner.py`

Deze runner verzorgt publicatie-overzichten op ecosysteemniveau:

- `publiceer-json` – `agents-publicatie.json` genereren (schema v2.0)
- `publiceer-overzicht` – markdown overzicht van alle agents naar `docs/agents-overzicht.md`
- `rapporteer-prompts-overzicht` – via ecosysteem-coordinator execution-instructies
	genereren voor het prompts-overzicht

Voorbeeld (generate agents-overzicht):

```powershell
python artefacten/aeo/aeo.02.agent-curator/runner/agent-curator.runner.py publiceer-overzicht
```

Na het draaien van deze runner kun je de gegenereerde overzichtsbestanden
vinden in `docs/`.

## Prompt-instructies

Wanneer je `genereer-instructies` (via de ecosysteem-coordinator) of
`rapporteer-prompts-overzicht` (via de agent-curator runner) gebruikt,
worden execution-bestanden aangemaakt in `prompt-instructions/`:

```text
prompt-instructions/
├── <hash>.agent-curator.rapporteer-prompts-overzicht.md
└── history/
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

In `scripts/` staat momenteel één script:

- `copy_prompts_mandarin_agents.py` – ondersteunt het genereren van een
	aggregatie (bijv. `agents.yaml`) uit de canonieke prompts.

Gebruik dit script alleen als je weet hoe het in jouw consumer-workspace
is geïntegreerd; het is primair een hulpscript voor build/publishing.

## Vereisten

- **Python 3.10+** – voor runners en tooling
- **Git** – voor werken met de canon-repository

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
