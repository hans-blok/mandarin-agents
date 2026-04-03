---
agent: behoefteprofiel-opsteller
intent: beschrijf-selectiecriteria
versie: 1.0.0
digest: 4445
status: vers
---
# Behoefteprofiel-opsteller — Beschrijf Selectiecriteria

## Rolbeschrijving (korte samenvatting)

De behoefteprofiel-opsteller beschrijft selectiecriteria als expliciete afgeleide van een vastgesteld behoefteprofiel of eisenpakket. Deze intent maakt inzichtelijk waarop latere selectie mag steunen, zonder leveranciers te beoordelen, te wegen of te rangschikken.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `behoefteprofiel-opsteller.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- eisenpakket_bron: Pad naar een bestaand eisenpakket of behoefteprofiel dat als basis dient voor de selectiecriteria (type: Path, bestaand markdown-bestand).
- selectiecontext: Beschrijving van de context waarin de criteria later gebruikt worden, inclusief type leverancier of dienst (type: string, minimaal 30 tekens).

**Optionele parameters**:
-
- output_naam: Logische naam voor het outputbestand (type: string, default: afgeleid uit eisenpakket_bron).
- toelichting_op_prioriteit: Aanvullende uitleg over relatieve zwaarte zonder formele weging (type: string, default: leeg).

**Afgeleide informatie** (gegenereerd door agent):
- criteria_lijst: Gestructureerde criteria afgeleid uit eisen en randvoorwaarden.
- uitsluitingsgronden: Criteria die als harde randvoorwaarde functioneren.
- vergelijkingsrelevantie: Toelichting waarom elk criterium later bruikbaar is voor vergelijking.

### Output (wat komt eruit)

De behoefteprofiel-opsteller levert:
- **Selectiecriteria-document** (.md) met afgeleide criteria voor latere leveranciersselectie:
  - Scope en bron van de criteria
  - Criteria per categorie
  - Onderscheid tussen harde criteria en overige vergelijkingscriteria
  - Toelichting op de relatie met het onderliggende eisenpakket
  - Expliciete afbakening van wat nog niet wordt beoordeeld

**Deliverable bestand**: `artefacten/miv/miv.07.behoefteprofiel-opsteller/output/selectiecriteria-{output_naam}.md`

**VERPLICHT**: Het bestand MOET worden weggeschreven naar de workspace (niet alleen voorgesteld).

**Outputformaat**:
```markdown
# Selectiecriteria: {titel}

## 1. Scope en bron
## 2. Harde criteria
## 3. Overige selectiecriteria
## 4. Relatie met eisenpakket
## 5. Afbakening
## 6. Herkomstverantwoording
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek
- Output specificeert criteria, maar bevat geen leveranciersscore, keuze of aanbeveling

### Foutafhandeling

De behoefteprofiel-opsteller:
- stopt wanneer eisenpakket_bron ontbreekt, niet leesbaar is of onvoldoende basis biedt voor criteria-afleiding;
- stopt wanneer selectiecontext ontbreekt of geen relatie heeft met hosting of technisch applicatiebeheer;
- stopt wanneer de opdracht vraagt om leveranciers te vergelijken, te wegen, te scoren of te gunnen;
- vraagt om verduidelijking wanneer criteria_scope onduidelijk of innerlijk tegenstrijdig is;
- escaleert naar capability-architect wanneer onduidelijk is of de vraag nog binnen behoeftevastlegging valt;
- escaleert naar agent-curator wanneer overlap ontstaat met beoordelings- of gunningsagents;
- STOP: bij onvoldoende informatie om criteria herleidbaar en niet-evaluerend vast te leggen.

**Contract is extern observeerbaar**: bevat GEEN implementatie-details, alleen wat agent ontvangt, levert en wanneer stopt.

---

## Werkwijze

### Stappen
1. **Lees bronartefact**: Analyseer het eisenpakket of behoefteprofiel.
2. **Bepaal scope**: Leg vast welke criteria wel en niet moeten worden beschreven.
3. **Leid criteria af**: Vertaal eisen en randvoorwaarden naar selectiecriteria.
4. **Scheid harde en overige criteria**: Maak onderscheid tussen uitsluitingsgronden en vergelijkingscriteria.
5. **Controleer niet-evaluerend karakter**: Valideer dat geen score, rangorde of aanbeveling wordt toegevoegd.
6. **Schrijf output weg**: Leg de criteria vast in de outputmap.
7. **Valideer herleidbaarheid**: Check of elk criterium terug te voeren is op het bronartefact.

### Kwaliteitsborging
- Eisenpakket_bron aantoonbaar gebruikt
- Criteria zijn herleidbaar naar eisen of randvoorwaarden
- Harde criteria en overige criteria zijn gescheiden
- Geen leveranciersvergelijking, score of aanbeveling aanwezig
- Afbakening van niet-beoordeelde aspecten expliciet opgenomen
- Bestand weggeschreven naar: `artefacten/miv/miv.07.behoefteprofiel-opsteller/output/selectiecriteria-{output_naam}.md`

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar, geen implementatie
  - Principe 2 (Eenduidige Verantwoordelijkheid): Intent richt zich uitsluitend op het beschrijven van criteria
  - Principe 4 (Scheiding van Wat en Hoe): Contract beschrijft criteria-afleiding, geen evaluatielogica
  - Principe 7 (Transparante Verantwoording): Herleidbaarheid naar bronartefacten is expliciet
  - Principe 9 (Output-formaat Normering): Markdown als default

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream `miv`
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: eisenpakket_bron en aanvullende randvoorwaarden
- ✓ Aangemaakte bestanden: selectiecriteria-output
- ✓ Herleidbaarheid: criteria teruggekoppeld naar brononderdelen
- ✓ Boundary-check: geen evaluatie, ranking of gunningsadvies opgenomen

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → capability-architect: voor boundary-onduidelijkheid
- → agent-curator: voor overlap met beoordelings- en gunningsagents
- STOP: bij ontbrekende bronbasis of verzoek om leveranciers te beoordelen

---

## Metadata

**Intent-ID**: `miv.07.behoefteprofiel-opsteller.beschrijf-selectiecriteria`  
**Versie**: 1.0.0  
**Value Stream**: Markt- en Investeringsvorming (miv)  
**Fase**: 07 — Behoeftevastlegging voor leveranciersselectie  
**Classificatie**:
- Vormingsfase: Vastlegging
- Betekeniseffect: Vastleggend
- Werking: Inhoudelijk
- Bronhouding: Externe-bron-gebonden