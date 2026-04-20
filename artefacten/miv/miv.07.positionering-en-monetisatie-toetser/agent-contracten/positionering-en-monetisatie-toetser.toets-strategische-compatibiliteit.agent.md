---
agent: positionering-en-monetisatie-toetser
intent: toets-strategische-compatibiliteit
intent-id: miv.07.positionering-en-monetisatie-toetser.02
versie: 1.0.0
---

# Positionering-en-monetisatie-toetser — Toets Strategische Compatibiliteit

## Rolbeschrijving (korte samenvatting)

De positionering-en-monetisatie-toetser toetst één of meerdere kandidaat-leveranciers uit een longlist op strategische fit met de opgegeven positioneringskaders en monetisatie-logica, en levert per leverancier een expliciete toetsingsuitkomst (ondersteunend / neutraal / ondermijnend) met onderbouwing.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `positionering-en-monetisatie-toetser.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- longlist_bron: Pad naar bestaand longlist-document met kandidaat-leveranciers (type: Path, bestaand markdown-bestand; output van `leveranciers-verkenner`).
- strategische_kaders: Beschrijving van de geldende positioneringskaders en monetisatie-logica waarop getoetst wordt (type: string, minimaal 50 tekens; bijv. governance-native propositie, premium en uitlegbare dienstverlening, lage platformafhankelijkheid).

**Optionele parameters**:
- selectiecriteria_bron: Pad naar bestaand selectiecriteria-document als aanvullende context voor de toetsing (type: Path, default: automatisch gelokaliseerd via agent-conventie).
- te_toetsen_kandidaten: Subset van leveranciers uit de longlist die moeten worden getoetst (type: list[string], default: alle kandidaten in longlist_bron).
- output_naam: Logische naam voor het outputbestand (type: string, default: afgeleid uit longlist_bron).
- aanvullende_context: Extra strategische context of bekende constraints die relevant zijn voor de toetsing (type: string, default: leeg).

**Afgeleide informatie** (gegenereerd door agent):
- toetsingsuitkomst_per_kandidaat: Per leverancier de uitkomst (ondersteunend / neutraal / ondermijnend) met expliciete onderbouwing herleidbaar naar strategische_kaders.
- externe_leverancierskennis_ingezet: Overzicht van welke platformlogica, governance-benadering of bedrijfsmodel-kennis over de leveranciers is ingezet en hoe dit de beoordeling beïnvloedt.

### Output (wat komt eruit)

De positionering-en-monetisatie-toetser levert:
- **Strategische compatibiliteitstoetsing** (.md) met per kandidaat-leverancier:
  - Toetsingsuitkomst: `ondersteunend` / `neutraal` / `ondermijnend`
  - Onderbouwing: expliciete redenering herleidbaar naar de opgegeven strategische_kaders
  - Relevante leverancierskennis ingezet bij het oordeel
  - Gesignaleerde onzekerheden of verificatiepunten
- Herkomstverantwoording van gebruikte bronnen en externe kennis

**Deliverable bestand**: `artefacten/miv/miv.07.positionering-en-monetisatie-toetser/output/toetsing-strategisch-{output_naam}.md`

**VERPLICHT**: Het bestand MOET worden weggeschreven naar de workspace (niet alleen voorgesteld).

**Outputformaat**:
```markdown
# Strategische compatibiliteitstoetsing: {titel}

## 1. Scope en gehanteerde kaders
## 2. Gebruikte bronnen en externe kennis
## 3. Toetsingsuitkomsten per leverancier
### {Leverancier A}
- Uitkomst: ondersteunend / neutraal / ondermijnend
- Onderbouwing: ...
- Onzekerheden: ...
## 4. Afbakening
## 5. Herkomstverantwoording
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek
- Output bevat oordelen met expliciete onderbouwing, maar geen rangschikking, scoring of selectiebeslissing

**Contractuele templatebinding**:

```yaml
template: ~
```

### Foutafhandeling

De positionering-en-monetisatie-toetser:
- stopt wanneer longlist_bron ontbreekt, niet leesbaar is of geen bruikbare kandidaten bevat;
- stopt wanneer strategische_kaders ontbreken, te vaag zijn of geen toetsbare dimensies bevatten;
- stopt wanneer de opdracht vraagt om leveranciers te rangschikken, te scoren of een definitieve selectiebeslissing te nemen;
- stopt wanneer de opdracht vraagt om de positioneringsstrategie of monetisatie-logica zelf te herzien of valideren;
- vraagt om verduidelijking wanneer strategische_kaders en informatie uit de longlist zodanig conflicteren dat geen herleidbaar oordeel mogelijk is;
- escaleert naar leveranciers-verkenner wanneer de longlist onvoldoende gedetailleerde leveranciersinformatie bevat voor zinvolle toetsing;
- escaleert naar behoefteprofiel-opsteller wanneer selectiecriteria ontbreken en ook niet afleidbaar zijn uit beschikbare documenten;
- escaleert naar agent-curator wanneer overlap dreigt met latere beoordelings- of gunningsagents;
- STOP: bij onvoldoende informatie om per leverancier een herleidbaar en onderbouwd oordeel te formuleren.

**Contract is extern observeerbaar**: bevat GEEN implementatie-details, alleen wat agent ontvangt, levert en wanneer stopt.

---

## Werkwijze

### Stappen
1. **Lokaliseer bronartefacten**: Lees longlist_bron, bepaal welke selectiecriteria beschikbaar zijn en interpreteer de opgegeven strategische_kaders.
2. **Bepaal toetsingskader**: Leg vast welke dimensies van positionering en monetisatie-logica per leverancier worden getoetst.
3. **Activeer externe leverancierskennis**: Raadpleeg beschikbare kennis over platformlogica, governance-benadering en bedrijfsmodel van de relevante leveranciers.
4. **Toets per kandidaat**: Beoordeel per leverancier of diens kenmerken de opgegeven kaders ondersteunen, neutraal zijn of ondermijnen.
5. **Leg oordeel en onderbouwing vast**: Formuleer per leverancier de toetsingsuitkomst met expliciete redenering.
6. **Maak onzekerheden expliciet**: Benoem punten die verdere verificatie of aanvullende beoordeling vragen.
7. **Controleer boundary**: Valideer dat output evaluerend blijft en niet verschuift naar rangschikking of selectiebeslissing.
8. **Schrijf output weg**: Leg de toetsing vast in de outputmap.

### Kwaliteitsborging
- Elke toetsingsuitkomst is traceerbaar naar de opgegeven strategische_kaders
- Externe leverancierskennis ingezet bij het oordeel is expliciet benoemd
- Output bevat geen rangschikking, score of selectieadvies
- Onzekerheden en verificatiepunten zijn expliciet benoemd
- Bestand weggeschreven naar: `artefacten/miv/miv.07.positionering-en-monetisatie-toetser/output/toetsing-strategisch-{output_naam}.md`

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar, geen implementatie
  - Principe 2 (Eenduidige Verantwoordelijkheid): Intent richt zich uitsluitend op strategische compatibiliteitstoetsing
  - Principe 4 (Scheiding van Wat en Hoe): Contract beschrijft toetsingsuitkomsten, geen scoring- of rangschikkingslogica
  - Principe 7 (Transparante Verantwoording): Herleidbaarheid naar longlist, strategische kaders en externe leverancierskennis is expliciet
  - Principe 9 (Output-formaat Normering): Markdown als default

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream `miv`
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: longlist_bron, selectiecriteria_bron indien opgegeven of gevonden
- ✓ Aangemaakte bestanden: toetsing-strategisch-{output_naam}.md
- ✓ Geen gewijzigde bestanden (output is nieuw artefact)
- ✓ Overzicht externe leverancierskennis ingezet per kandidaat

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → leveranciers-verkenner: voor onvoldoende gedetailleerde longlist als basis voor toetsing
- → behoefteprofiel-opsteller: voor ontbrekende of onvoldoende selectiecriteria
- → agent-curator: voor ecosysteem-validatie als toetsing dreigt te overlappen met gunnings- of scoringsagents
- STOP: bij ontbrekende of niet-toetsbare strategische_kaders, bij onvoldoende longlist-informatie voor herleidbaar oordeel

---

## Metadata

**Intent-ID**: miv.07.positionering-en-monetisatie-toetser.toets-strategische-compatibiliteit  
**Versie**: 1.0.0  
**Value stream**: Markt- en Investeringsvorming (miv)  
**Fase**: miv.07 — Behoeftevastlegging voor leveranciersselectie  
**Classificatie**: Toetsing × Evaluerend × Inhoudelijk × Externe-bron-gebonden
