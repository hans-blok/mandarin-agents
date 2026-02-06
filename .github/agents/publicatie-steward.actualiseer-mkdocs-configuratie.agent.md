# Publicatie Steward — Actualiseer mkdocs configuratie

## Rolbeschrijving

De **publicatie-steward** beheert en bewaakt de publicatiestructuur en -configuratie (inclusief mkdocs.yml) om expliciete content correct, consistent en verantwoord publiek te ontsluiten.

Deze intent actualiseert een bestaande `mkdocs.yml` met nieuwe content uit de workspace, behoud bestaande structuur waar mogelijk.

**VERPLICHT**: Lees artefacten/fnd/fnd.02.publicatie-steward/publicatie-steward.charter.md voor volledige context, grenzen en werkwijze.

## Contract

### Input (Wat gaat erin)

**Verplichte parameters**:
- mkdocs-yml-path: Pad naar bestaande mkdocs.yml bestand (type: string).

**Optionele parameters**:
- scan-nieuwe-content: Scan workspace voor nieuwe bestanden niet in mkdocs.yml (type: boolean, default: true).
- verwijder-missing-links: Verwijder links naar niet-bestaande bestanden (type: boolean, default: false).
- preserve-custom-order: Behoud handmatige volgorde in navigatie (type: boolean, default: true).

### Output (Wat komt eruit)

Bij een geldige opdracht levert de publicatie-steward:

**Primaire output**:
- `mkdocs.yml`: Geactualiseerde mkdocs configuratie met:
  - Alle bestaande configuratie behouden (theme, plugins, etc.)
  - Navigatie uitgebreid met nieuwe content
  - Broken links verwijderd (indien verwijder-missing-links=true)
  - Bestaande volgorde behouden (indien preserve-custom-order=true)
  
**Secundaire output**:
- `artefacten/publicatie-steward/actualisatie-rapport-<datum>.md`: Rapport met:
  - Overzicht van wijzigingen (toegevoegd, verwijderd, gehandhaafd)
  - Lijst van nieuwe bestanden toegevoegd aan navigatie
  - Lijst van verwijderde links (indien van toepassing)
  - Waarschuwingen voor dubbele titels of structuur-conflicten

**Deliverable eigenschappen:**
- mkdocs.yml behoudt bestaande formatting en commentaar waar mogelijk
- Navigatiestructuur is consistent met bestaande logica
- Alle nieuwe paden zijn relatief en valide
- Rapport toont voor/na vergelijking van navigatie

### Foutafhandeling

De publicatie-steward:
- Stopt wanneer mkdocs.yml niet bestaat of niet leesbaar is.
- Stopt wanneer mkdocs.yml geen valide YAML is (maakt backup voor herstel).
- Waarschuwt wanneer nieuwe content niet logisch in bestaande structuur past.
- Escaleert naar governance wanneer actualisatie zou leiden tot >50 nieuwe items (mogelijk bulk-upload die review nodig heeft).

## Werkwijze

Voor alle details over werkwijze en kwaliteitsborging zie de charter.

---

Documentatie: [artefacten/fnd/fnd.02.publicatie-steward/publicatie-steward.charter.md](artefacten/fnd/fnd.02.publicatie-steward/publicatie-steward.charter.md)  
Runner: artefacten/fnd/fnd.02.publicatie-steward/publicatie-steward.py
