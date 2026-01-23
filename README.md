# Mandarin Agents

Deze repository bevat agent definities, scripts en tools voor het Mandarin workspace ecosysteem.

## 📚 Workspace Tools

**Voor het opzetten van een nieuwe workspace**, zie:

➡️ **[scripts/workspace-tools/README.md](scripts/workspace-tools/README.md)**

Deze folder bevat alle hulpmiddelen voor:
- Workspace initialisatie (folder structuur creëren)
- Agent fetching (agents ophalen voor value streams)
- Repository management (clone/update repositories)

## Structuur

```
mandarin-agents/
├── scripts/
│   └── workspace-tools/         # 🔧 Tools voor workspace setup
│       ├── README.md            # ← Start hier voor nieuwe workspaces
│       ├── init-workspace.bat
│       ├── fetch-agents.bat
│       ├── fetch_agents.py
│       ├── pull.bat
│       └── pull-repo.ps1
├── exports/                     # Gepubliceerde agents per value stream
│   ├── utility/                 # Utility agents (alle workspaces)
│   ├── kennispublicatie/
│   ├── architectuur-en-oplossingsontwerp/
│   └── ...
├── .github/
│   └── prompts/                 # Agent prompts
├── charters-agents/             # Agent charters
├── agents-publicatie.json       # Agent manifest
└── init-workspace.py            # Python implementatie workspace init
```

## Quick Start

### Nieuwe Workspace Maken

```cmd
# 1. Kopieer workspace tools naar je nieuwe workspace
copy scripts\workspace-tools\init-workspace.bat <nieuwe-workspace>\
copy scripts\workspace-tools\fetch-agents.bat <nieuwe-workspace>\
copy scripts\workspace-tools\fetch_agents.py <nieuwe-workspace>\scripts\

# 2. Initialiseer workspace
cd <nieuwe-workspace>
init-workspace.bat kennispublicatie

# 3. Workspace is klaar!
```

Zie [scripts/workspace-tools/README.md](scripts/workspace-tools/README.md) voor uitgebreide instructies.

## Agents

Alle agent definities zijn beschikbaar via `agents-publicatie.json` manifest en georganiseerd per value stream in `exports/`.

### Utility Agents
Agents in `exports/utility/` zijn beschikbaar voor alle workspaces.

### Value Stream Agents
Agents in `exports/<value-stream>/` zijn specifiek voor die waardestroom.

## Voor Ontwikkelaars

### Publicatie Proces

```cmd
# Agent definities publiceren vanuit development repository
publiceer-agents.bat
```

### Repository Synchronisatie

```cmd
# Wijzigingen naar remote pushen
push.bat
```

## Vereisten

- **Python 3.9+** - Voor Python scripts
- **Git** - Voor repository operaties
- **Internet connectie** - Voor clone/pull operaties

## Beleid

Zie [beleid-mandarin-agents.md](beleid-mandarin-agents.md) voor workspace-specifiek beleid en governance.

## Licentie

Zie licentie informatie in individuele agent definities.
