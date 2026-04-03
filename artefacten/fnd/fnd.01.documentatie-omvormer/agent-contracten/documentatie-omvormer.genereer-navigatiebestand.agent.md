---
agent: documentatie-omvormer
intent: genereer-navigatiebestand
versie: 1.0.0
digest: f565
status: vers
---
# Documentatie-omvormer — Genereer Navigatiebestand

## Rolbeschrijving (korte samenvatting)

De documentatie-omvormer genereert de navigatie-sectie (nav) voor mkdocs.yml op basis van de bestaande documentatiestructuur of expliciete ordeningsinput, zonder inhoudelijke interpretatie of prioritering.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `documentatie-omvormer.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- geen

**Optionele parameters**:
- geen

### Output (wat komt eruit)

De documentatie-omvormer levert:
- **Bijgewerkte mkdocs.yml** met complete nav-sectie:
  - Navigatiestructuur die 1:1 overeenkomt met mappenstructuur
  - Titels bepaald volgens titel_bron parameter
  - Volgorde volgens ordening_regels of alfabetisch
- **Nav-sectie fragment** (YAML) voor review

**Deliverable bestand**: `{mkdocs_yml}` (bijgewerkt bestand)

**Outputformaat** (nav-sectie):
```yaml
nav:
  - Home: index.md
  - Sectie 1:
    - Document A: sectie-1/document-a.md
    - Document B: sectie-1/document-b.md
  - Sectie 2:
    - Document C: sectie-2/document-c.md
```

**Formaat-normering**: 
- Output is YAML nav-sectie conform MkDocs specificatie
- Titels worden niet geïnterpreteerd, alleen overgenomen
- Structuur is herleidbaar naar input

### Foutafhandeling

De documentatie-omvormer:
- stopt wanneer docs_folder niet bestaat of leeg is;
- stopt wanneer mkdocs_yml niet bestaat of niet schrijfbaar is;
- stopt wanneer titel_bron="h1" maar bestand geen H1 bevat — gebruikt dan bestandsnaam als fallback;
- vraagt NIET om verduidelijking — agent interpreteert niet;
- escaleert NIET naar andere agents;
- STOP: bij ongeldige YAML-structuur in bestaande mkdocs.yml die niet hersteld kan worden.

**Wat NIET gebeurt:**
- Geen inhoudelijke prioritering of ordening op basis van documentinhoud
- Geen samenvattingen of beschrijvingen toegevoegd aan nav-items
- Geen beslissingen over welke documenten wel/niet in navigatie

---

## Werkwijze

### Stappen
1. **Valideer input**: Controleer of docs_folder en mkdocs_yml bestaan
2. **Scan documentstructuur**: Inventariseer alle markdown-bestanden in docs_folder
3. **Bepaal titels**: Haal titels op volgens titel_bron methode
4. **Pas ordening toe**: Sorteer volgens ordening_regels of alfabetisch
5. **Genereer nav-structuur**: Bouw YAML nav-sectie
6. **Merge met mkdocs.yml**: Vervang of voeg nav-sectie toe aan bestaand bestand
7. **Valideer YAML**: Controleer syntactische correctheid

### Kwaliteitsborging
- Alle bestanden uit docs_folder zijn opgenomen in nav
- Nav-structuur spiegelt mappenstructuur
- Titels zijn herleidbaar naar bron (bestandsnaam of H1)
- YAML is syntactisch correct en MkDocs-compatibel

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar
  - Principe 2 (Eenduidige Verantwoordelijkheid): Navigatie-generatie, geen inhoud
  - Principe 7 (Transparante Verantwoording): Nav-fragment toont resultaat
- **Betekenis-blindheid**: Agent interpreteert geen documentinhoud voor ordening

**Canon-consultatie:**
- Niet van toepassing — agent is input-gebonden, niet canon-gebonden

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Alle gescande bestanden in docs_folder
- ✓ Bepaalde titels per bestand (met bron: filename of h1)
- ✓ Toegepaste ordening_regels
- ✓ Gegenereerde nav-structuur

Logging-formaat: Nav-fragment in output

**Escalatie-paden:**
- Geen escalatie — agent is volledig input-gebonden
- STOP: bij ongeldige YAML of ontbrekende verplichte input

---

## Metadata

**Intent-ID**: `fnd.01.documentatie-omvormer.genereer-navigatiebestand`  
**Versie**: 1.0.0  
**Value Stream**: Fundamental Infrastructure (fnd)  
**Fase**: 01 — Infrastructurele diensten  
**Classificatie**: 
- Vormingsfase: Realisatie
- Betekeniseffect: Geen betekenis
- Werking: Representatie-omvormend
- Bronhouding: Input-gebonden
