---
agent: leveranciers-verkenner
intent: beschrijf-leveranciersfit
versie: 1.0.0
---

# Leveranciers-verkenner — Beschrijf Leveranciersfit

## Rolbeschrijving (korte samenvatting)

De leveranciers-verkenner beschrijft per kandidaat-leverancier de inhoudelijke fit met behoefteprofiel, selectiecriteria en operationele context. Deze intent maakt per leverancier zichtbaar waar vermoedelijke aansluiting of mismatch zit, zonder formele scoring, ranking of selectie-oordeel.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `leveranciers-verkenner.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- longlist_bron: Pad naar bestaand longlist-document of gelijkwaardige lijst van kandidaat-leveranciers die inhoudelijk in aanmerking komen (type: Path, bestaand markdown-bestand).
- fit_aspecten: Beschrijving van de fit-aspecten, gebaseerd op het door de agent gelokaliseerde behoefteprofiel, die per leverancier moeten worden geduid, zoals managed services, compliance, GitLab-beheer, supportmodel en schaalbaarheid (type: string, minimaal 30 tekens).

**Optionele parameters**:
- output_naam: Logische naam voor het outputbestand (type: string, default: afgeleid uit longlist_bron).
- selectiecriteria_bron: Pad naar bestaand document met selectiecriteria voor aanvullende duiding (type: Path, default: leeg).
- aanvullende_context: Extra operationele context of bekende beperkingen voor de fit-duiding (type: string, default: leeg).

**Afgeleide informatie** (gegenereerd door agent):
- gevonden_behoefteprofiel: Het door de agent gelokaliseerde behoefteprofiel of eisenpakket dat als basis dient voor de fit-duiding.
- fit_notities: Korte beschrijvende notities per leverancier over vermoedelijke aansluiting op de opgegeven fit-aspecten.
- aandachtspunten: Punten per leverancier die verdere verificatie of latere beoordeling vragen.
- herkomstoverzicht: Overzicht van bronnen en criteria waarop de fit-duiding is gebaseerd.

### Output (wat komt eruit)

De leveranciers-verkenner levert:
- **Leveranciersfit-document** (.md) met korte fit-notitie per kandidaat-leverancier:
  - Scope en gebruikte fit-aspecten
  - Leveranciersoverzicht met fit-duiding per partij
  - Aandachtspunten of onzekerheden per leverancier
  - Expliciete afbakening van wat nog niet wordt beoordeeld
  - Herkomstverantwoording van gebruikte bronnen

**Deliverable bestand**: `artefacten/miv/miv.07.leveranciers-verkenner/output/leveranciersfit-{output_naam}.md`

**VERPLICHT**: Het bestand MOET worden weggeschreven naar de workspace (niet alleen voorgesteld).

**Outputformaat**:
```markdown
# Leveranciersfit: {titel}

## 1. Scope en fit-aspecten
## 2. Gebruikte bronnen
## 3. Fit-duiding per leverancier
## 4. Aandachtspunten en onzekerheden
## 5. Afbakening
## 6. Herkomstverantwoording
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek
- Output bevat beschrijvende fit-duiding per leverancier, maar geen score, ranking of selectieadvies

### Foutafhandeling

De leveranciers-verkenner:
- stopt wanneer longlist_bron ontbreekt, niet leesbaar is of geen bruikbare kandidaten bevat;
- stopt wanneer geen passend behoefteprofiel kan worden gelokaliseerd, gelezen of afgeleid als basis voor fit-duiding;
- stopt wanneer fit_aspecten ontbreken of te vaag zijn om per leverancier inhoudelijke aansluiting te beschrijven;
- stopt wanneer de opdracht vraagt om leveranciers formeel te beoordelen, te rangschikken of te selecteren;
- vraagt om verduidelijking wanneer longlist, het gevonden behoefteprofiel en fit-aspecten onderling conflicteren;
- escaleert naar behoefteprofiel-opsteller wanneer de bronartefacten onvoldoende scherp zijn voor zinvolle fit-duiding;
- escaleert naar agent-curator wanneer overlap dreigt met latere beoordelings- of scoringsagents;
- STOP: bij onvoldoende informatie om fit-notities beschrijvend en herleidbaar op te stellen.

**Contract is extern observeerbaar**: bevat GEEN implementatie-details, alleen wat agent ontvangt, levert en wanneer stopt.

---

## Werkwijze

### Stappen
1. **Lokaliseer bronartefacten**: Analyseer de longlist, bepaal welk behoefteprofiel als meest passende bron geldt en verzamel relevante selectiecriteria.
2. **Bepaal fit-kader**: Leg vast welke fit-aspecten per leverancier moeten worden beschreven.
3. **Duid leveranciersfit**: Beschrijf per kandidaat waar vermoedelijke aansluiting of mismatch zit.
4. **Maak onzekerheden expliciet**: Benoem punten die verdere verificatie of latere beoordeling vragen.
5. **Controleer boundary**: Valideer dat de output beschrijvend blijft en niet verschuift naar scoring of voorkeur.
6. **Schrijf output weg**: Leg de fit-notities vast in de outputmap.
7. **Valideer herleidbaarheid**: Check of elke fit-duiding terug te voeren is op bronartefacten en externe bronnen.

### Kwaliteitsborging
- Longlist en het automatisch gevonden behoefteprofiel zijn aantoonbaar gebruikt
- Elke leverancier heeft een korte, inhoudelijke fit-notitie op de opgegeven aspecten
- Onzekerheden en verificatiepunten zijn expliciet benoemd
- Output blijft beschrijvend en bevat geen ranking, score of voorkeursadvies
- Bestand weggeschreven naar: `artefacten/miv/miv.07.leveranciers-verkenner/output/leveranciersfit-{output_naam}.md`

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar, geen implementatie
  - Principe 2 (Eenduidige Verantwoordelijkheid): Intent richt zich uitsluitend op het beschrijven van leveranciersfit
  - Principe 4 (Scheiding van Wat en Hoe): Contract beschrijft fit-duiding, geen formele beoordelings- of scoringslogica
  - Principe 7 (Transparante Verantwoording): Herleidbaarheid naar longlist, behoefteprofiel en marktbronnen is expliciet
  - Principe 9 (Output-formaat Normering): Markdown als default

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream `miv`
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: longlist_bron, automatisch gevonden behoefteprofiel en selectiecriteria_bron indien opgegeven
- ✓ Aangemaakte bestanden: leveranciersfit-output
- ✓ Geraadpleegde marktbronnen: overzicht van bronnen die de fit-duiding ondersteunen
- ✓ Boundary-check: geen score, ranking of selectieoordeel opgenomen

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → behoefteprofiel-opsteller: voor onvoldoende scherpe bronartefacten of onduidelijke criteria
- → agent-curator: voor overlap met beoordelings-, scorings- of gunningsagents
- STOP: bij ontbrekende bronbasis of verzoek om formele leveranciersbeoordeling

---

## Metadata

**Intent-ID**: `miv.07.leveranciers-verkenner.beschrijf-leveranciersfit`  
**Versie**: 1.0.0  
**Value Stream**: Markt- en Investeringsvorming (miv)  
**Fase**: 07 — Behoeftevastlegging voor leveranciersselectie  
**Classificatie**:
- Vormingsfase: Verkenning
- Betekeniseffect: Beschrijvend
- Werking: Inhoudelijk
- Bronhouding: Externe-bron-gebonden