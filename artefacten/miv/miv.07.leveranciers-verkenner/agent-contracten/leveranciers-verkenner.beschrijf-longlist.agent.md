---
agent: leveranciers-verkenner
intent: beschrijf-longlist
versie: 1.0.0
digest: d01e
status: vers
---
# Leveranciers-verkenner — Beschrijf Longlist

## Rolbeschrijving (korte samenvatting)

De leveranciers-verkenner beschrijft een onderbouwde longlist van relevante hosting-providers op basis van behoefteprofiel, selectiecriteria en operationele scope. Deze intent maakt zichtbaar welke leveranciers inhoudelijk in aanmerking komen, zonder ranking, voorkeursadvies of leverancierskeuze.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `leveranciers-verkenner.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- geen.

**Optionele parameters**:
- aanvullende_randvoorwaarden: Aanvullende context of uitsluitingen die niet expliciet in behoefteprofiel of selectiecriteria zijn opgenomen (type: string, default: leeg).

**Afgeleide informatie** (gegenereerd door agent):
- gevonden_behoefteprofiel: Het door de agent gelokaliseerde behoefteprofiel of eisenpakket dat als bronbasis dient voor de marktverkenning.
- kandidaat_leveranciers: Gestructureerde lijst van leveranciers die binnen de opgegeven scope inhoudelijk in aanmerking komen.
- selectiegrondslag: Herleidbare samenvatting van eisen, criteria en scope die de longlist dragen.
- bronoverzicht: Overzicht van geraadpleegde externe bronnen per leverancier.

### Output (wat komt eruit)

De leveranciers-verkenner levert:
- **Longlist-document** (.md) met een onderbouwde lijst van kandidaat-leveranciers:
  - Scope en bronbasis van de verkenning
  - Longlist van leveranciers met korte positionering
  - Toelichting per leverancier waarom deze inhoudelijk in aanmerking komt
  - Herkomstverantwoording van gebruikte bronnen
  - Expliciete afbakening van wat nog niet beoordeeld wordt

**Deliverable bestand**: `artefacten/miv/miv.07.leveranciers-verkenner/output/longlist-{output_naam}.md`

**VERPLICHT**: Het bestand MOET worden weggeschreven naar de workspace (niet alleen voorgesteld).

**Outputformaat**:
```markdown
# Longlist leveranciers: {titel}

## 1. Scope en bronbasis
## 2. Samenvatting van selectiegrondslag
## 3. Longlist kandidaat-leveranciers
## 4. Toelichting per leverancier
## 5. Afbakening
## 6. Herkomstverantwoording
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek
- Output beschrijft welke leveranciers in aanmerking komen, maar bevat geen ranking, score of voorkeursadvies

### Foutafhandeling

De leveranciers-verkenner:
- stopt wanneer geen passend behoefteprofiel kan worden gelokaliseerd, gelezen of afgeleid als bronbasis voor leveranciersverkenning;
- stopt wanneer selectiecriteria_bron ontbreekt, niet leesbaar is of geen bruikbare selectiegrondslag bevat;
- stopt wanneer scope_afbakening ontbreekt of te vaag is om leveranciers buiten of binnen scope te plaatsen;
- stopt wanneer de opdracht vraagt om leveranciers te rangschikken, kiezen of gunnen;
- vraagt om verduidelijking wanneer het gevonden behoefteprofiel, selectiecriteria en scope onderling tegenstrijdig zijn;
- escaleert naar behoefteprofiel-opsteller wanneer bronartefacten onvoldoende scherp of onvolledig blijken;
- escaleert naar capability-architect wanneer onduidelijk is of de vraag nog binnen marktverkenning valt;
- STOP: bij onvoldoende informatie om een herleidbare longlist op te stellen zonder evaluatief eindoordeel.

**Contract is extern observeerbaar**: bevat GEEN implementatie-details, alleen wat agent ontvangt, levert en wanneer stopt.

---

## Werkwijze

### Stappen
1. **Lokaliseer bronartefacten**: Bepaal welk behoefteprofiel of eisenpakket als meest passende bronbasis geldt en verzamel selectiecriteria en scope-afbakening.
2. **Bepaal verkenningskader**: Leg vast welke leverancierscategorieen en contextfactoren relevant zijn.
3. **Verken de markt**: Identificeer leveranciers die inhoudelijk binnen scope lijken te vallen.
4. **Stel de longlist op**: Bundel kandidaat-leveranciers met korte positionering per partij.
5. **Controleer boundary**: Valideer dat de output beschrijvend blijft en geen ranking of voorkeur bevat.
6. **Schrijf output weg**: Leg de longlist vast in de outputmap.
7. **Valideer herleidbaarheid**: Check of elke kandidaat terug te voeren is op bronartefacten en geraadpleegde marktbronnen.

### Kwaliteitsborging
- Het automatisch gevonden behoefteprofiel, selectiecriteria en scope zijn aantoonbaar gebruikt
- Elke leverancier op de longlist heeft een expliciete inhoudelijke grond voor opname
- Output blijft beschrijvend en bevat geen score, ranking of voorkeursadvies
- Afbakening van nog niet beoordeelde aspecten is expliciet opgenomen
- Bestand weggeschreven naar: `artefacten/miv/miv.07.leveranciers-verkenner/output/longlist-{output_naam}.md`

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar, geen implementatie
  - Principe 2 (Eenduidige Verantwoordelijkheid): Intent richt zich uitsluitend op het beschrijven van een longlist
  - Principe 4 (Scheiding van Wat en Hoe): Contract beschrijft leveranciersverkenning, geen beoordelings- of gunningslogica
  - Principe 7 (Transparante Verantwoording): Herleidbaarheid naar bronartefacten en marktbronnen is expliciet
  - Principe 9 (Output-formaat Normering): Markdown als default

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream `miv`
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: automatisch gevonden behoefteprofiel, selectiecriteria_bron en aanvullende randvoorwaarden
- ✓ Aangemaakte bestanden: longlist-output
- ✓ Geraadpleegde marktbronnen: overzicht per leverancier of leveranciersgroep
- ✓ Boundary-check: geen ranking, voorkeursadvies of leverancierskeuze opgenomen

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → behoefteprofiel-opsteller: voor onvoldoende scherpe bronartefacten of selectiegrondslag
- → capability-architect: voor boundary-onduidelijkheid buiten marktverkenning
- STOP: bij ontbrekende bronbasis of verzoek om leveranciers te beoordelen of te kiezen

---

## Metadata

**Intent-ID**: `miv.07.leveranciers-verkenner.beschrijf-longlist`  
**Versie**: 1.0.0  
**Value Stream**: Markt- en Investeringsvorming (miv)  
**Fase**: 07 — Behoeftevastlegging voor leveranciersselectie  
**Classificatie**:
- Vormingsfase: Verkenning
- Betekeniseffect: Beschrijvend
- Werking: Inhoudelijk
- Bronhouding: Externe-bron-gebonden