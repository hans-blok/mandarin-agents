---
agent: positionering-en-monetisatie-toetser
intent: stel-toetsingsrapport-op
intent-id: miv.07.positionering-en-monetisatie-toetser.03
versie: 1.0.0
---

# Positionering-en-monetisatie-toetser — Stel Toetsingsrapport Op

## Rolbeschrijving (korte samenvatting)

De positionering-en-monetisatie-toetser stelt het volledige strategische toetsingsrapport samen op basis van de individuele toetsingsuitkomsten en spanningsveldanalyse, en levert een samenvattend overzicht van strategisch meest compatibele en meest risicovolle kandidaten als onderbouwde basis voor menselijke besluitvorming.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `positionering-en-monetisatie-toetser.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- toetsing_bron: Pad naar bestaand strategische-compatibiliteitstoetsing-document (type: Path, bestaand markdown-bestand; output van `toets-strategische-compatibiliteit`).
- spanningsvelden_bron: Pad naar bestaand spanningsvelden-overzicht (type: Path, bestaand markdown-bestand; output van `signaleer-spanningsvelden`).

**Optionele parameters**:
- longlist_bron: Pad naar het originele longlist-document voor contextcompletiteit (type: Path, default: automatisch gelokaliseerd via verwijzingen in toetsing_bron).
- output_naam: Logische naam voor het outputbestand (type: string, default: afgeleid uit toetsing_bron).
- aanvullende_context: Extra context die in het rapport moet worden meegenomen (type: string, default: leeg).

**Afgeleide informatie** (gegenereerd door agent):
- samenvattend_overzicht: Geconsolideerd beeld van alle kandidaten met hun toetsingsuitkomst en spanningsveld-profiel.
- strategisch_profiel_per_kandidaat: Combinatie van toetsingsuitkomst en spanningsveld-indicaties per leverancier in één overzicht.

### Output (wat komt eruit)

De positionering-en-monetisatie-toetser levert:
- **Volledig toetsingsrapport** (.md) met:
  - Samenvatting van gebruikte kaders en gehanteerde aanpak
  - Per kandidaat: geconsolideerd strategisch profiel (toetsingsuitkomst + spanningsveld-samenvatting)
  - Samenvattend overzicht: strategisch meest compatibele kandidaten
  - Samenvattend overzicht: kandidaten met de meest significante spanningsvelden
  - Expliciete afbakening van wat het rapport wel en niet bevat
  - Herkomstverantwoording van alle gebruikte bronnen
- Het rapport bevat geen rangschikking, score of selectieoordeel; beslissing blijft bij de mens

**Deliverable bestand**: `artefacten/miv/miv.07.positionering-en-monetisatie-toetser/output/toetsingsrapport-{output_naam}.md`

**VERPLICHT**: Het bestand MOET worden weggeschreven naar de workspace (niet alleen voorgesteld).

**Outputformaat**:
```markdown
# Strategisch Toetsingsrapport: {titel}

## 1. Samenvatting
## 2. Gehanteerde kaders en aanpak
## 3. Gebruikte bronnen
## 4. Strategisch profiel per leverancier
### {Leverancier A}
- Toetsingsuitkomst: ondersteunend / neutraal / ondermijnend
- Spanningsveld-profiel: ...
- Toelichting: ...
## 5. Overzicht strategisch compatibele kandidaten
## 6. Overzicht kandidaten met significante spanningsvelden
## 7. Afbakening en beslissingskader
## 8. Herkomstverantwoording
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek
- Output consolideert en structureert bestaande toetsingen; voegt geen nieuwe beoordelingen toe die niet in de brondocumenten staan

**Contractuele templatebinding**:

```yaml
template: ~
```

### Foutafhandeling

De positionering-en-monetisatie-toetser:
- stopt wanneer toetsing_bron ontbreekt of niet leesbaar is;
- stopt wanneer spanningsvelden_bron ontbreekt of niet leesbaar is;
- stopt wanneer toetsing_bron en spanningsvelden_bron betrekking hebben op niet-overlappende sets leveranciers zonder expliciete toelichting;
- stopt wanneer de opdracht vraagt om in het toetsingsrapport een definitieve leveranciersselectie of rangschikking op te nemen;
- stopt wanneer de opdracht vraagt om nieuwe beoordelingen te genereren die niet in de brondocumenten aanwezig zijn;
- vraagt om verduidelijking wanneer bronnen inconsistente toetsingsuitkomsten bevatten die niet te consolideren zijn zonder nieuwe inhoudelijke beoordeling;
- escaleert naar `toets-strategische-compatibiliteit` intent wanneer de toetsing_bron ontbreekt en eerst toetsing moet plaatsvinden;
- escaleert naar `signaleer-spanningsvelden` intent wanneer de spanningsvelden_bron ontbreekt en eerst analyse moet plaatsvinden;
- STOP: bij brondocumenten die te fragmentarisch zijn om een samenhangend rapport te kunnen samenstellen.

**Contract is extern observeerbaar**: bevat GEEN implementatie-details, alleen wat agent ontvangt, levert en wanneer stopt.

---

## Werkwijze

### Stappen
1. **Valideer bronnen**: Controleer of toetsing_bron en spanningsvelden_bron aanwezig en leesbaar zijn en betrekking hebben op dezelfde of overlappende kandidatensets.
2. **Lees toetsingsresultaten**: Extraheer per leverancier de toetsingsuitkomst en onderbouwing uit toetsing_bron.
3. **Lees spanningsveld-analyse**: Extraheer per leverancier de gesignaleerde spanningsvelden en risicoprofiel-indicaties uit spanningsvelden_bron.
4. **Consolideer per kandidaat**: Combineer toetsingsuitkomst en spanningsveld-profiel tot één geconsolideerd strategisch profiel per leverancier.
5. **Stel samenvattende overzichten op**: Identificeer strategisch meest compatibele en meest risicovolle kandidaten op basis van de geconsolideerde profielen.
6. **Formuleer beslissingskader**: Beschrijf expliciet wat het rapport wel en niet bevat, welke beslissingen bij de mens liggen en welke vervolgstappen mogelijk zijn.
7. **Controleer boundary**: Valideer dat het rapport consolideert en structureert, niet rangschikt of nieuwe beoordelingen toevoegt.
8. **Schrijf output weg**: Leg het toetsingsrapport vast in de outputmap.

### Kwaliteitsborging
- Alle leveranciers uit de brondocumenten zijn opgenomen in het rapport
- Elk geconsolideerd strategisch profiel is herleidbaar naar de brondocumenten
- Het rapport voegt geen nieuwe inhoudelijke beoordelingen toe die niet in de bronnen staan
- De afbakening is expliciet: het rapport is geen selectieoordeel
- Bestand weggeschreven naar: `artefacten/miv/miv.07.positionering-en-monetisatie-toetser/output/toetsingsrapport-{output_naam}.md`

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar, geen implementatie
  - Principe 2 (Eenduidige Verantwoordelijkheid): Intent richt zich uitsluitend op het samenstellen van het toetsingsrapport
  - Principe 4 (Scheiding van Wat en Hoe): Contract beschrijft consolidatie van bestaande toetsingen, geen nieuwe beoordelingslogica
  - Principe 7 (Transparante Verantwoording): Herleidbaarheid naar toetsing_bron en spanningsvelden_bron is expliciet
  - Principe 9 (Output-formaat Normering): Markdown als default

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream `miv`
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: toetsing_bron, spanningsvelden_bron, longlist_bron indien aanwezig
- ✓ Aangemaakte bestanden: toetsingsrapport-{output_naam}.md
- ✓ Geen gewijzigde bestanden (output is nieuw artefact)
- ✓ Consolidatieaantekeningen: welke bronnen zijn samengevoegd en hoe

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → `toets-strategische-compatibiliteit`: wanneer toetsing_bron ontbreekt en eerst toetsing moet worden uitgevoerd
- → `signaleer-spanningsvelden`: wanneer spanningsvelden_bron ontbreekt en eerst analyse moet worden uitgevoerd
- → agent-curator: voor ecosysteem-validatie als het toetsingsrapport dreigt te overlappen met gunnings- of beslissingsadvies
- STOP: bij brondocumenten te fragmentarisch voor samenhangend rapport, bij opdracht tot rangordering of selectieoordeel

---

## Metadata

**Intent-ID**: miv.07.positionering-en-monetisatie-toetser.stel-toetsingsrapport-op  
**Versie**: 1.0.0  
**Value stream**: Markt- en Investeringsvorming (miv)  
**Fase**: miv.07 — Behoeftevastlegging voor leveranciersselectie  
**Classificatie**: Toetsing × Evaluerend × Inhoudelijk × Externe-bron-gebonden
