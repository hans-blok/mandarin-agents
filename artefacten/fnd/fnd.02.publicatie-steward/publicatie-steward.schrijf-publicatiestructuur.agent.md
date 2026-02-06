# Publicatie Steward — Schrijf publicatiestructuur

## Rolbeschrijving

De **publicatie-steward** beheert en bewaakt de publicatiestructuur en -configuratie (inclusief mkdocs.yml) om expliciete content correct, consistent en verantwoord publiek te ontsluiten.

Deze intent genereert een nieuwe `mkdocs.yml` op basis van de bestanden in `docs/` folder en zet deze logisch op in een navigatiestructuur.

**VERPLICHT**: Lees artefacten/fnd/fnd.02.publicatie-steward/publicatie-steward.charter.md voor volledige context, grenzen en werkwijze.

## Contract

### Input (Wat gaat erin)

**Verplichte parameters**:
- workspace-root: Pad naar de root van de workspace (type: string).

**Optionele parameters**:
- include-folders: Folders om te includeren in publicatie (type: lijst van strings, default: ["docs/", "governance/"]).
- exclude-patterns: Patronen van bestanden om uit te sluiten (type: lijst van strings, default: ["**/temp/", "**/.git/"]).
- nav-depth: Maximale diepte van navigatie-hiërarchie (type: integer, default: 3).

### Output (Wat komt eruit)

Bij een geldige opdracht levert de publicatie-steward:

**Primaire output**:
- `mkdocs.yml`: Nieuwe of volledig herschreven mkdocs configuratie met:
  - Site metadata (site_name, site_url, site_description)
  - Theme configuratie (material theme met standaard kleuren/features)
  - Navigatiestructuur gebaseerd op folderstructuur in docs/
  - Plugins (search, git-revision-date)
  
**Secundaire output**:
- `artefacten/publicatie-steward/publicatiestructuur-rapport-<datum>.md`: Rapport met:
  - Overzicht van gescande folders en gevonden bestanden
  - Gegenereerde navigatiestructuur (boom-weergave)
  - Waarschuwingen voor dubbele titels of onduidelijke structuur

**Deliverable eigenschappen:**
- mkdocs.yml is geldig YAML en kan direct door mkdocs worden gebruikt
- Navigatiestructuur volgt logische hiërarchie van folderstructuur
- Alle paden in mkdocs.yml zijn relatief en valide
- Rapport is in Markdown format

### Foutafhandeling

De publicatie-steward:
- Stopt wanneer workspace-root niet bestaat of niet toegankelijk is.
- Waarschuwt wanneer docs/ folder leeg is of niet bestaat.
- Waarschuwt voor broken links maar stopt niet (rapporteert deze).
- Escaleert naar governance wanneer gevoelige content (credentials, secrets) in publicatie-folders wordt gedetecteerd.

## Werkwijze

Voor alle details over werkwijze en kwaliteitsborging zie de charter.

---

Documentatie: [artefacten/fnd/fnd.02.publicatie-steward/publicatie-steward.charter.md](artefacten/fnd/fnd.02.publicatie-steward/publicatie-steward.charter.md)  
Runner: artefacten/fnd/fnd.02.publicatie-steward/publicatie-steward.py
