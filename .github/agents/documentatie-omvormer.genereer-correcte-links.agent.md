---
agent: documentatie-omvormer
intent: genereer-correcte-links
intent-id: fnd.01.documentatie-omvormer.01
versie: 1.0.0
digest: a6bd
status: vers
---
# Documentatie-omvormer — Genereer Correcte Links

## Rolbeschrijving (korte samenvatting)

De documentatie-omvormer controleert en herstelt interne links in markdown-documentatie zodat deze correct werken na publicatie op GitHub en GitLab, zonder inhoudelijke wijziging van de documenten.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `documentatie-omvormer.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- docs_folder: Pad naar de docs-map met te controleren documentatie (type: string).
- platform: Doelplatform voor linkvalidatie: "github", "gitlab", of "mkdocs" (type: string).

**Optionele parameters**:
- base_url: Basis-URL voor absolute links (type: string, default: relatieve links).
- exclude_patterns: Patronen voor bestanden die moeten worden overgeslagen (type: list[string], default: []).

### Output (wat komt eruit)

De documentatie-omvormer levert in de chat:
- **Link-validatierapport** met:
  - Lijst van alle gevonden interne links
  - Status per link: geldig of ongeldig
  - Voor ongeldige links: gecorrigeerde pad-suggestie

**Outputformaat** (chat):
```markdown
# Link Validatie Rapport

**Platform**: {platform}
**Docs folder**: {docs_folder}

## Samenvatting
- Totaal bestanden gescand: {n}
- Totaal links gevonden: {n}
- Geldige links: {n}
- Ongeldige links: {n}

## Details

| Bestand | Link | Status | Correctie |
|---------|------|--------|-----------|
| docs/index.md | [tekst](pad) | ✓ geldig | - |
| docs/intro.md | [tekst](oud-pad) | ✗ ongeldig | → nieuw-pad |
```

**Formaat-normering**: 
- Rapport wordt getoond in chat
- Correcties zijn suggesties, geen automatische wijzigingen
- Linktekst blijft ongewijzigd

**Contractuele templatebinding**:

```yaml
template: ~
```

### Foutafhandeling

De documentatie-omvormer:
- stopt wanneer docs_folder niet bestaat of leeg is;
- stopt wanneer platform geen geldige waarde heeft;
- rapporteert ongeldige links in chat maar stopt NIET bij onoplosbare links;
- vraagt NIET om verduidelijking — agent interpreteert niet.

**Wat NIET gebeurt:**
- Geen automatische wijziging van bestanden
- Geen interpretatie van linkdoel of -context

---

## Werkwijze

### Stappen
1. **Valideer input**: Controleer docs_folder en platform parameter
2. **Scan bestanden**: Inventariseer alle markdown-bestanden
3. **Extraheer links**: Vind alle markdown-links [tekst](pad) en referenties
4. **Valideer links**: Controleer of doelbestand bestaat
5. **Bepaal correcties**: Voor ongeldige links, bepaal correct pad
6. **Toon rapport**: Output validatierapport in chat

### Kwaliteitsborging
- Alle markdown-bestanden in docs_folder zijn gescand
- Alle interne links zijn gevalideerd
- Rapport bevat complete status per link
- Correctiesuggesties zijn bruikbaar voor handmatige aanpassing

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar
  - Principe 2 (Eenduidige Verantwoordelijkheid): Linkvalidatie, geen automatische correctie
  - Principe 7 (Transparante Verantwoording): Volledig rapport van alle bevindingen
- **Betekenis-blindheid**: Agent interpreteert geen linkcontext of documentinhoud

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Niet van toepassing — agent is input-gebonden, niet canon-gebonden

**Transparantie-verplichtingen:**

Bij uitvoering toont de agent in chat:
- ✓ Alle gescande bestanden
- ✓ Alle gevonden links met validatiestatus
- ✓ Correctiesuggesties voor ongeldige links

Logging-formaat: Link-validatierapport in chat

**Escalatie-paden:**
- Geen escalatie — agent is volledig input-gebonden
- STOP: bij ongeldige input

---

## Metadata

**Intent-ID**: `fnd.01.documentatie-omvormer.genereer-correcte-links`  
**Versie**: 1.0.0  
**Value Stream**: Fundamental Infrastructure (fnd)  
**Fase**: 01 — Infrastructurele diensten  
**Classificatie**: 
- Vormingsfase: Realisatie
- Betekeniseffect: Geen betekenis
- Werking: Representatie-omvormend
- Bronhouding: Input-gebonden
