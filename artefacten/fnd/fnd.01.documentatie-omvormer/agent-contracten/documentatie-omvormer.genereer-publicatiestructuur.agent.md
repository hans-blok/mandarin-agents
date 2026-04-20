---
agent: documentatie-omvormer
intent: genereer-publicatiestructuur
intent-id: fnd.01.documentatie-omvormer.03
versie: 1.0.0
digest: e316
status: vers
---
# Documentatie-omvormer — Genereer Publicatiestructuur

## Rolbeschrijving (korte samenvatting)

De documentatie-omvormer transformeert bestaande markdown-documentatie naar een MkDocs-compatibele mappenstructuur zonder inhoudelijke wijziging, interpretatie of toevoeging van betekenis.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `documentatie-omvormer.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- geen (bron is altijd root/docs)

**Optionele parameters**:
- structuur_regels: Expliciete regels voor mappenstructuur of volgorde (type: string of bestandspad, default: geen — structuur wordt 1:1 overgenomen).
- exclude_patterns: Patronen voor bestanden/mappen die moeten worden uitgesloten (type: list[string], default: []).

### Output (wat komt eruit)

De documentatie-omvormer levert:
- **Publiceerbare mappenstructuur** in de doel_folder:
  - Alle bronbestanden getransformeerd naar docs/-compatibele structuur
  - Mappenstructuur herleidbaar naar input of expliciete structuur_regels
  - Geen nieuwe inhoud, samenvattingen of interpretaties toegevoegd
- **`docs/assets/stylesheets/responsive.css`** — altijd aangemaakt als vaste deliverable, inhoud zie hieronder
- **Transformatie-rapport** met overzicht van verplaatste bestanden

**Deliverable bestand**: `{doel_folder}/` (volledige mappenstructuur)

**Outputformaat** (mappenstructuur):
```
docs/
├── index.md
├── assets/
│   └── stylesheets/
│       └── responsive.css
├── {sectie-1}/
│   ├── index.md
│   └── {document-1}.md
└── {sectie-2}/
    └── {document-2}.md
```

**Canonieke inhoud van `responsive.css`** (byte-voor-byte reproduceerbaar, geen inhoudelijke keuze):
```css
/* Responsive overrides — Mandarin publicatie */

/* Tabellen: horizontaal scrollen als te breed voor scherm */
.md-typeset table {
  display: block;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

/* Afbeeldingen nooit breder dan de container */
.md-typeset img {
  max-width: 100%;
  height: auto;
}

/* Mermaid-diagrammen: horizontaal scrollen als te breed */
.md-typeset .mermaid,
.md-typeset [class^="mermaid"] {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
```

**Formaat-normering**: 
- Output is altijd een mappenstructuur met markdown-bestanden
- Bestandsnamen worden niet gewijzigd, alleen locaties
- Inhoud blijft 100% ongewijzigd
- `responsive.css` is een vaste structurele deliverable — geen inhoudelijke beslissing

**Contractuele templatebinding**:

```yaml
template: templates/mkdocs-yml.template.md
```

### Foutafhandeling

De documentatie-omvormer:
- stopt wanneer bron_folder niet bestaat of niet leesbaar is;
- stopt wanneer doel_folder niet schrijfbaar is;
- stopt wanneer structuur_regels naar niet-bestaand bestand verwijst;
- vraagt NIET om verduidelijking — agent is betekenis-blind en interpreteert niet;
- escaleert NIET naar andere agents — transformatie is volledig herleidbaar naar input;
- STOP: bij conflicterende bestandsnamen zonder expliciete resolutie-regel in input.

**Wat NIET gebeurt:**
- Geen inhoudelijke wijzigingen aan documenten
- Geen interpretatie van documentinhoud voor structuurbeslissingen
- Geen toevoeging van nieuwe bestanden of inhoud

---

## Werkwijze

### Stappen
1. **Valideer input**: Controleer of bron_folder bestaat en leesbaar is
2. **Scan bronstructuur**: Inventariseer alle markdown-bestanden en mappenstructuur
3. **Pas structuur_regels toe**: Indien opgegeven, pas expliciete regels toe; anders 1:1 overnemen
4. **Creëer doelstructuur**: Maak mappen aan in doel_folder
5. **Kopieer bestanden**: Verplaats/kopieer bestanden naar doellocaties
6. **Genereer rapport**: Schrijf transformatie-overzicht

### Kwaliteitsborging
- Alle bronbestanden zijn aanwezig in doelstructuur
- Inhoud van bestanden is byte-voor-byte identiek
- Structuur is herleidbaar naar input of expliciete regels
- Geen bestanden "verzonnen" of weggelaten zonder expliciete exclude_pattern

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar
  - Principe 2 (Eenduidige Verantwoordelijkheid): Transformatie van structuur, geen inhoud
  - Principe 7 (Transparante Verantwoording): Transformatie-rapport toont alle acties
- **Betekenis-blindheid**: Agent interpreteert geen inhoud en neemt geen inhoudelijke beslissingen

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Niet van toepassing — agent is input-gebonden, niet canon-gebonden

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Alle gelezen bronbestanden (met pad)
- ✓ Alle aangemaakte doelbestanden (met pad)
- ✓ Toegepaste structuur_regels (indien opgegeven)
- ✓ Uitgesloten bestanden (indien exclude_patterns gebruikt)

Logging-formaat: Transformatie-rapport in output

**Escalatie-paden:**
- Geen escalatie — agent is volledig input-gebonden
- STOP: bij ontbrekende input of onoplosbare conflicten

---

## Metadata

**Intent-ID**: `fnd.01.documentatie-omvormer.genereer-publicatiestructuur`  
**Versie**: 1.0.0  
**Value Stream**: Fundamental Infrastructure (fnd)  
**Fase**: 01 — Infrastructurele diensten  
**Classificatie**: 
- Vormingsfase: Realisatie
- Betekeniseffect: Geen betekenis
- Werking: Representatie-omvormend
- Bronhouding: Input-gebonden
