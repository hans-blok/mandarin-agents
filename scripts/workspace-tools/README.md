# Workspace Tools

Deze folder bevat hulpmiddelen voor het inrichten en onderhouden van workspaces.

## Overzicht Bestanden

### Workspace Initialisatie
- **init-workspace.bat** - Initialiseert een nieuwe workspace met folder structuur
- **fetch-agents.bat** - Haalt agents op voor een value stream
- **fetch_agents.py** - Python implementatie voor agent fetching

### Repository Management
- **pull.bat** - Clone of update een GitHub repository
- **pull-repo.ps1** - PowerShell implementatie van repository pull/clone

## Gebruik

### 1. Nieuwe Workspace Initialiseren

**Doel**: Een lege workspace inrichten met de juiste folder structuur.

**Stappen**:
1. Kopieer deze bestanden naar de workspace root:
   ```
   init-workspace.bat  →  <workspace-root>/init-workspace.bat
   fetch-agents.bat    →  <workspace-root>/fetch-agents.bat
   fetch_agents.py     →  <workspace-root>/scripts/fetch_agents.py
   ```

2. Voer uit in command prompt:
   ```cmd
   init-workspace.bat
   # of met value stream:
   init-workspace.bat kennispublicatie
   ```

**Resultaat**: Workspace structuur aangemaakt
```
<workspace-root>/
  ├── .github/prompts/      # Agent prompts
  ├── charters-agents/      # Agent charters
  ├── scripts/runners/      # Agent runner scripts
  ├── docs/resultaten/      # Output van agents
  ├── logs/                 # Log bestanden (ignored)
  ├── temp/                 # Tijdelijke bestanden (ignored)
  ├── .gitignore            # Git ignore configuratie
   └── beleid-mandarin-agents.md   # Workspace beleid
```

### 2. Repository Clonen/Updaten

**Doel**: Clone een GitHub repository of update een bestaande.

**Gebruik**:
```cmd
pull.bat <repository-naam>

# Voorbeelden:
pull.bat mandarin-canon
pull.bat mandarin-agents
```

**Gedrag**:
- Als repository **niet bestaat**: clone vanuit `https://github.com/hans-blok/<repo>.git`
- Als repository **wel bestaat**: voer `git pull` uit om te updaten

**Vereisten**:
- Git geïnstalleerd en in PATH
- Internet connectie
- Toegang tot GitHub repository (publiek of met credentials)

### 3. Agents Fetchen

**Doel**: Haal agents op voor een specifieke value stream.

**Gebruik**:
```cmd
fetch-agents.bat <value-stream>

# Voorbeelden:
fetch-agents.bat kennispublicatie
fetch-agents.bat --list
```

**Vereisten**:
- Python 3.9+ geïnstalleerd
- `agents-publicatie.json` manifest in workspace root of mandarin-agents

## Vereisten per Tool

| Tool | Python | Git | Internet |
|------|--------|-----|----------|
| init-workspace.bat | ✓ | - | - |
| pull.bat | - | ✓ | ✓ |
| fetch-agents.bat | ✓ | - | Optioneel* |

*fetch-agents werkt met lokale mandarin-agents of haalt deze op indien nodig.

## Installatie van Vereisten

**Python 3.9+**:
- Download: https://www.python.org/downloads/
- Verificatie: `python --version`

**Git**:
- Download: https://git-scm.com/downloads
- Verificatie: `git --version`

## Troubleshooting

**"Python niet gevonden"**:
- Installeer Python 3.9+ en voeg toe aan PATH
- Herstart command prompt na installatie

**"Git niet gevonden"**:
- Installeer Git en voeg toe aan PATH
- Herstart command prompt na installatie

**"Permission denied"**:
- Controleer schrijfrechten in de directory
- Run command prompt als administrator

**"Repository niet gevonden"**:
- Controleer of repository bestaat op GitHub
- Controleer internet connectie
- Bij private repos: configureer Git credentials

## Typisch Workflow

**Nieuwe workspace opzetten**:
1. Kopieer workspace tools naar nieuwe folder
2. Run `init-workspace.bat <value-stream>`
3. Run `pull.bat canon` (optioneel, voor governance)
4. Run `pull.bat mandarin-agents` (optioneel, voor agents)
5. Run `fetch-agents.bat <value-stream>` (als mandarin-agents lokaal)
6. Begin met werken in de workspace

## Over deze Folder

Deze folder (`scripts/workspace-tools/`) is een **toolkit** voor workspace beheer.

**Belangrijk**: Deze bestanden zijn bedoeld om te kopiëren naar workspaces waar je ze nodig hebt.
