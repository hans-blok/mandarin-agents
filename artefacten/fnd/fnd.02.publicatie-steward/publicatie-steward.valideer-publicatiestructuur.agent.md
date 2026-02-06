# Publicatie Steward — Valideer publicatiestructuur

## Rolbeschrijving

De **publicatie-steward** beheert en bewaakt de publicatiestructuur en -configuratie (inclusief mkdocs.yml) om expliciete content correct, consistent en verantwoord publiek te ontsluiten.

Deze intent valideert een bestaande `mkdocs.yml` op consistentie, broken links en governance-compliance.

**VERPLICHT**: Lees artefacten/fnd/fnd.02.publicatie-steward/publicatie-steward.charter.md voor volledige context, grenzen en werkwijze.

## Contract

### Input (Wat gaat erin)

**Verplichte parameters**:
- mkdocs-yml-path: Pad naar mkdocs.yml bestand (type: string).

**Optionele parameters**:
- check-broken-links: Controleer of alle paden in nav bestaan (type: boolean, default: true).
- check-governance: Valideer dat geen gevoelige content is opgenomen (type: boolean, default: true).
- strict-mode: Stop bij eerste fout (type: boolean, default: false).

### Output (Wat komt eruit)

Bij een geldige opdracht levert de publicatie-steward:

**Primaire output**:
- `artefacten/publicatie-steward/validatie-rapport-<datum>.md`: Validatierapport met:
  - Status: PASS / WARNINGS / FAIL
  - Lijst van gevonden issues (broken links, missing files, governance violations)
  - Per issue: severity (kritiek/waarschuwing/info), locatie, beschrijving
  - Aanbevelingen voor herstel

**Deliverable eigenschappen:**
- Rapport is in Markdown format met duidelijke status-indicatie
- Issues zijn gesorteerd op severity (kritiek eerst)
- Elk issue heeft actiebare beschrijving en locatie
- Bij PASS status: bevestiging dat alle checks zijn geslaagd

### Foutafhandeling

De publicatie-steward:
- Stopt wanneer mkdocs.yml niet bestaat of niet leesbaar is.
- Stopt wanneer mkdocs.yml geen valide YAML is.
- Waarschuwt voor broken links en missing files (tenzij strict-mode=true).
- Escaleert naar governance wanneer gevoelige content wordt gedetecteerd (credentials, API keys, passwords in tekst).

## Werkwijze

Voor alle details over werkwijze en kwaliteitsborging zie de charter.

---

Documentatie: [artefacten/fnd/fnd.02.publicatie-steward/publicatie-steward.charter.md](artefacten/fnd/fnd.02.publicatie-steward/publicatie-steward.charter.md)  
Runner: artefacten/fnd/fnd.02.publicatie-steward/publicatie-steward.py
