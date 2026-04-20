---
agent: behoefteprofiel-opsteller
intent: structureer-eisenpakket
intent-id: miv.07.behoefteprofiel-opsteller.03
versie: 1.0.0
digest: 0408
status: vers
---
# Behoefteprofiel-opsteller — Structureer Eisenpakket

## Rolbeschrijving (korte samenvatting)

De behoefteprofiel-opsteller structureert een behoefteprofiel tot een vergelijkbaar en prioriteerbaar eisenpakket voor latere leveranciersselectie. Deze intent ordent eisen, wensen en randvoorwaarden, zonder al een beoordelingsmodel of leveranciersoordeel te produceren.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `behoefteprofiel-opsteller.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- behoefteprofiel_bron: Pad naar een bestaand behoefteprofiel of gelijkwaardig bronartefact dat als basis dient voor structurering (type: Path, bestaand markdown-bestand).
- ordeningskader: Beschrijving van de gewenste indeling van eisen, wensen en randvoorwaarden (type: string, minimaal 30 tekens).
- prioriteringsgrondslag: Uitleg op basis waarvan prioriteiten worden toegekend of overgenomen (type: string, minimaal 20 tekens).

**Optionele parameters**:
- aanvullende_toelichting: Extra uitleg van de opdrachtgever over structuur of nadrukpunten (type: string, default: leeg).

**Afgeleide informatie** (gegenereerd door agent):
- eisenindeling: Gestructureerde indeling in eisen, wensen en randvoorwaarden.
- prioriteitsniveaus: Expliciet vastgelegde prioriteitsklassen per onderdeel.
- vergelijkingsbasis: De onderdelen die latere vergelijking van aanbiedingen mogelijk maken.

### Output (wat komt eruit)

De behoefteprofiel-opsteller levert:
- **Eisenpakket** (.md) met geordende en prioriteerbare eisen:
  - Samenvatting van scope
  - Geordende eisen per categorie
  - Scheiding tussen harde eisen, wensen en randvoorwaarden
  - Prioriteringsuitleg per categorie of onderdeel
  - Toelichting op vergelijkingsrelevantie

**Deliverable bestand**: `artefacten/miv/miv.07.behoefteprofiel-opsteller/output/eisenpakket-{output_naam}.md`

**VERPLICHT**: Het bestand MOET worden weggeschreven naar de workspace (niet alleen voorgesteld).

**Outputformaat**:
```markdown
# Eisenpakket: {titel}

## 1. Scope en bron
## 2. Harde eisen
## 3. Wensen
## 4. Randvoorwaarden
## 5. Prioritering
## 6. Toelichting voor latere vergelijking
## 7. Herkomstverantwoording
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek
- Output legt structuur vast, maar kent geen score of leveranciersoordeel toe

**Contractuele templatebinding**:

```yaml
template: ~
```

### Foutafhandeling

De behoefteprofiel-opsteller:
- stopt wanneer behoefteprofiel_bron ontbreekt, niet leesbaar is of geen bruikbare behoefte-inhoud bevat;
- stopt wanneer ordeningskader ontbreekt en niet uit de bron afleidbaar is;
- stopt wanneer de opdracht vraagt om leveranciers te scoren, te vergelijken of te rangschikken;
- vraagt om verduidelijking wanneer prioriteringsgrondslag innerlijk tegenstrijdig of onvoldoende expliciet is;
- escaleert naar capability-architect wanneer onduidelijk is of de gevraagde structurering nog binnen deze boundary valt;
- escaleert naar agent-curator wanneer overlap ontstaat met latere beoordelings- of sourcingrollen;
- STOP: bij onvoldoende basis om een herleidbaar en vergelijkbaar eisenpakket vast te leggen.

**Contract is extern observeerbaar**: bevat GEEN implementatie-details, alleen wat agent ontvangt, levert en wanneer stopt.

---

## Werkwijze

### Stappen
1. **Lees bronartefact**: Analyseer het behoefteprofiel en relevante toelichting.
2. **Bepaal ordening**: Pas het ordeningskader toe op de verzamelde behoeften.
3. **Scheid categorieen**: Maak expliciet onderscheid tussen eisen, wensen en randvoorwaarden.
4. **Leg prioriteiten vast**: Koppel prioriteitsniveaus op basis van de opgegeven grondslag.
5. **Controleer vergelijkingsgeschiktheid**: Valideer dat de structuur latere vergelijking ondersteunt.
6. **Schrijf output weg**: Leg het eisenpakket vast in de outputmap.
7. **Valideer boundary**: Controleer dat geen leveranciersoordeel of gunningslogica is toegevoegd.

### Kwaliteitsborging
- Behoefteprofiel_bron is aantoonbaar gebruikt
- Harde eisen, wensen en randvoorwaarden zijn gescheiden opgenomen
- Prioritering is navolgbaar onderbouwd
- Structuur ondersteunt latere vergelijking van aanbiedingen
- Geen scoremodel, leveranciersoordeel of gunningsadvies aanwezig
- Bestand weggeschreven naar: `artefacten/miv/miv.07.behoefteprofiel-opsteller/output/eisenpakket-{output_naam}.md`

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar, geen implementatie
  - Principe 2 (Eenduidige Verantwoordelijkheid): Intent richt zich uitsluitend op structurering van het eisenpakket
  - Principe 4 (Scheiding van Wat en Hoe): Contract beschrijft structuur, output en grenzen
  - Principe 7 (Transparante Verantwoording): Bron en prioriteringsgrondslag zijn traceerbaar
  - Principe 9 (Output-formaat Normering): Markdown als default

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream `miv`
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: behoefteprofiel_bron en aanvullende context
- ✓ Aangemaakte bestanden: eisenpakket-output
- ✓ Toegepaste ordenings- en prioriteringsgrondslag
- ✓ Boundary-check: geen leveranciersvergelijking of gunningsadvies opgenomen

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → capability-architect: voor scope- of boundary-vragen
- → agent-curator: voor overlap met selectie- en beoordelingsagents
- STOP: bij ontbrekend bronprofiel of verzoek om leveranciers te scoren

---

## Metadata

**Intent-ID**: `miv.07.behoefteprofiel-opsteller.structureer-eisenpakket`  
**Versie**: 1.0.0  
**Value Stream**: Markt- en Investeringsvorming (miv)  
**Fase**: 07 — Behoeftevastlegging voor leveranciersselectie  
**Classificatie**:
- Vormingsfase: Vastlegging
- Betekeniseffect: Vastleggend
- Werking: Inhoudelijk
- Bronhouding: Externe-bron-gebonden