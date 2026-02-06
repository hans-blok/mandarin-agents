# Publicatie Steward — Rapporteer publicatiestatus

## Rolbeschrijving

De **publicatie-steward** beheert en bewaakt de publicatiestructuur en -configuratie (inclusief mkdocs.yml) om expliciete content correct, consistent en verantwoord publiek te ontsluiten.

Deze intent genereert een overzicht van gepubliceerde versus niet-gepubliceerde content in de workspace.

**VERPLICHT**: Lees artefacten/fnd/fnd.02.publicatie-steward/publicatie-steward.charter.md voor volledige context, grenzen en werkwijze.

## Contract

### Input (Wat gaat erin)

**Verplichte parameters**:
- workspace-root: Pad naar de root van de workspace (type: string).

**Optionele parameters**:
- mkdocs-yml-path: Pad naar mkdocs.yml bestand (type: string, default: "mkdocs.yml").
- scan-folders: Folders om te scannen voor content (type: lijst van strings, default: ["docs/", "governance/", "artefacten/"]).
- include-stats: Voeg statistieken toe aan rapport (type: boolean, default: true).

### Output (Wat komt eruit)

Bij een geldige opdracht levert de publicatie-steward:

**Primaire output**:
- `artefacten/publicatie-steward/publicatiestatus-rapport-<datum>.md`: Statusrapport met:
  - Samenvatting: totaal aantal bestanden, gepubliceerd, niet-gepubliceerd
  - Tabel: gepubliceerde content (pad, titel, sectie in mkdocs.yml)
  - Tabel: niet-gepubliceerde content (pad, reden niet gepubliceerd)
  - Statistieken per folder (indien include-stats=true)
  - Aanbevelingen: content die mogelijk gepubliceerd zou moeten worden

**Deliverable eigenschappen:**
- Rapport is in Markdown format met duidelijke tabellen
- Alle paden zijn relatief ten opzichte van workspace-root
- Status is objectief (geen interpretatie waarom content niet gepubliceerd is)
- Aanbevelingen zijn gefilterd (geen temp/, .git/, of expliciet uitgesloten folders)

### Foutafhandeling

De publicatie-steward:
- Stopt wanneer workspace-root niet bestaat of niet toegankelijk is.
- Waarschuwt wanneer mkdocs.yml niet bestaat (rapporteert dan alleen niet-gepubliceerde content).
- Waarschuwt wanneer scan-folders niet bestaan of leeg zijn.
- Escaleert NIET (dit is alleen een rapportage-intent zonder wijzigingen).

## Werkwijze

Voor alle details over werkwijze en kwaliteitsborging zie de charter.

---

Documentatie: [artefacten/fnd/fnd.02.publicatie-steward/publicatie-steward.charter.md](artefacten/fnd/fnd.02.publicatie-steward/publicatie-steward.charter.md)  
Runner: artefacten/fnd/fnd.02.publicatie-steward/publicatie-steward.py
