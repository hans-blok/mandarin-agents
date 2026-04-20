---
agent: leveranciers-verkenner
intent: beschrijf-uitsluitingsgronden
intent-id: miv.07.leveranciers-verkenner.01
versie: 1.0.0
digest: 31dc
status: vers
---
# Leveranciers-verkenner — Beschrijf Uitsluitingsgronden

## Rolbeschrijving (korte samenvatting)

De leveranciers-verkenner beschrijft expliciete uitsluitingsgronden voor leveranciers die evident niet passen binnen behoefteprofiel, selectiecriteria of operationele scope. Deze intent maakt zichtbaar waarom een leverancier buiten de longlist valt, zonder negatief eindoordeel, ranking of definitieve afwijzingsbeslissing.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `leveranciers-verkenner.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- selectiecriteria_bron: Pad naar bestaand document met selectiecriteria of harde randvoorwaarden voor leveranciersuitsluiting (type: Path, bestaand markdown-bestand).
- leveranciersbron: Pad naar longlist, bruto leverancierslijst of marktoverzicht waarin mogelijke leveranciers zijn opgenomen (type: Path, bestaand markdown-bestand).

**Optionele parameters**:
- output_naam: Logische naam voor het outputbestand (type: string, default: afgeleid uit leveranciersbron).
- scope_afbakening: Aanvullende scopebeschrijving voor expliciete mismatch-detectie (type: string, default: leeg).
- aanvullende_bronnen: Lijst van externe bronnen die de uitsluitingsgrond onderbouwen (type: list[string], default: leeg).

**Afgeleide informatie** (gegenereerd door agent):
- gevonden_behoefteprofiel: Het door de agent gelokaliseerde behoefteprofiel of eisenpakket dat als basis dient voor uitsluiting op scope-mismatch.
- uitsluitingslijst: Overzicht van leveranciers die evident buiten scope vallen met de bijbehorende grond.
- type_mismatch: Categorisering van uitsluitingsgronden, bijvoorbeeld dienstenpakket, geografie, supportmodel of compliance-context.
- verificatiepunten: Punten die later expliciet gevalideerd moeten worden wanneer een uitsluitingsgrond nog onzeker is.

### Output (wat komt eruit)

De leveranciers-verkenner levert:
- **Uitsluitingsgronden-document** (.md) met expliciete scope-mismatches per leverancier:
  - Scope en bronbasis van de uitsluitingsanalyse
  - Overzicht van leveranciers buiten scope
  - Uitsluitingsgrond per leverancier of leveranciersgroep
  - Eventuele onzekerheden of verificatiepunten
  - Herkomstverantwoording van gebruikte bronnen

**Deliverable bestand**: `artefacten/miv/miv.07.leveranciers-verkenner/output/uitsluitingsgronden-{output_naam}.md`

**VERPLICHT**: Het bestand MOET worden weggeschreven naar de workspace (niet alleen voorgesteld).

**Outputformaat**:
```markdown
# Uitsluitingsgronden leveranciers: {titel}

## 1. Scope en bronbasis
## 2. Gehanteerde uitsluitingscriteria
## 3. Leveranciers buiten scope
## 4. Verificatiepunten en onzekerheden
## 5. Afbakening
## 6. Herkomstverantwoording
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek
- Output beschrijft expliciete uitsluitingsgronden, maar bevat geen ranking, scoring of definitieve gunningsafwijzing

**Contractuele templatebinding**:

```yaml
template: ~
```

### Foutafhandeling

De leveranciers-verkenner:
- stopt wanneer geen passend behoefteprofiel kan worden gelokaliseerd, gelezen of afgeleid als basis voor uitsluitingsanalyse;
- stopt wanneer selectiecriteria_bron ontbreekt, niet leesbaar is of geen bruikbare uitsluitingscriteria bevat;
- stopt wanneer leveranciersbron ontbreekt, niet leesbaar is of geen leveranciers bevat die tegen scope kunnen worden afgezet;
- stopt wanneer de opdracht vraagt om leveranciers formeel af te wijzen, te rangschikken of te selecteren;
- vraagt om verduidelijking wanneer uitsluitingscriteria en scope-afbakening elkaar tegenspreken;
- escaleert naar behoefteprofiel-opsteller wanneer harde randvoorwaarden of selectiecriteria onvoldoende expliciet zijn;
- escaleert naar agent-curator wanneer uitsluitingsgrond dreigt over te gaan in evaluatief leveranciersoordeel;
- STOP: bij onvoldoende informatie om uitsluitingsgronden herleidbaar en beschrijvend vast te leggen.

**Contract is extern observeerbaar**: bevat GEEN implementatie-details, alleen wat agent ontvangt, levert en wanneer stopt.

---

## Werkwijze

### Stappen
1. **Lokaliseer bronartefacten**: Bepaal welk behoefteprofiel als meest passende bron geldt en analyseer dit samen met selectiecriteria, leveranciersbron en aanvullende scope.
2. **Bepaal uitsluitingskader**: Leg vast welke harde randvoorwaarden en scopegrenzen tot uitsluiting kunnen leiden.
3. **Toets leveranciers aan scope**: Bepaal welke leveranciers evident buiten scope vallen.
4. **Beschrijf uitsluitingsgronden**: Leg per leverancier of leveranciersgroep expliciet vast waarom deze niet passend lijkt.
5. **Maak onzekerheden expliciet**: Benoem waar aanvullende verificatie nodig is.
6. **Controleer boundary**: Valideer dat de output beschrijvend blijft en niet verschuift naar formeel afwijzings- of selectieoordeel.
7. **Schrijf output weg**: Leg de uitsluitingsgronden vast in de outputmap.

### Kwaliteitsborging
- Het automatisch gevonden behoefteprofiel, selectiecriteria en leveranciersbron zijn aantoonbaar gebruikt
- Elke uitsluitingsgrond is expliciet terug te voeren op scope, criterium of randvoorwaarde
- Onzekerheden en verificatiepunten zijn apart benoemd
- Output blijft beschrijvend en bevat geen ranking, scoringslogica of gunningsadvies
- Bestand weggeschreven naar: `artefacten/miv/miv.07.leveranciers-verkenner/output/uitsluitingsgronden-{output_naam}.md`

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar, geen implementatie
  - Principe 2 (Eenduidige Verantwoordelijkheid): Intent richt zich uitsluitend op het beschrijven van uitsluitingsgronden
  - Principe 4 (Scheiding van Wat en Hoe): Contract beschrijft scope-mismatch en randvoorwaarden, geen formele afwijzings- of gunningslogica
  - Principe 7 (Transparante Verantwoording): Herleidbaarheid naar bronartefacten en marktbronnen is expliciet
  - Principe 9 (Output-formaat Normering): Markdown als default

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream `miv`
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: automatisch gevonden behoefteprofiel, selectiecriteria_bron, leveranciersbron en aanvullende context
- ✓ Aangemaakte bestanden: uitsluitingsgronden-output
- ✓ Geraadpleegde marktbronnen: aanvullende bronnen die de uitsluitingsgrond ondersteunen
- ✓ Boundary-check: geen formeel afwijzings-, ranking- of selectieoordeel opgenomen

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → behoefteprofiel-opsteller: voor onvoldoende expliciete harde randvoorwaarden of selectiecriteria
- → agent-curator: voor overlap met latere beoordelings- of afwijzingsagents
- STOP: bij ontbrekende bronbasis of verzoek om leveranciers formeel te selecteren of af te wijzen

---

## Metadata

**Intent-ID**: `miv.07.leveranciers-verkenner.beschrijf-uitsluitingsgronden`  
**Versie**: 1.0.0  
**Value Stream**: Markt- en Investeringsvorming (miv)  
**Fase**: 07 — Behoeftevastlegging voor leveranciersselectie  
**Classificatie**:
- Vormingsfase: Verkenning
- Betekeniseffect: Beschrijvend
- Werking: Inhoudelijk
- Bronhouding: Externe-bron-gebonden