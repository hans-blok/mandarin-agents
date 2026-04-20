---
agent: positionering-en-monetisatie-toetser
intent: signaleer-spanningsvelden
intent-id: miv.07.positionering-en-monetisatie-toetser.01
versie: 1.0.0
---

# Positionering-en-monetisatie-toetser — Signaleer Spanningsvelden

## Rolbeschrijving (korte samenvatting)

De positionering-en-monetisatie-toetser identificeert per kandidaat-leverancier de concrete spanningsvelden rond vendor lock-in, platformafhankelijkheid en productiseerbaarheid, en maakt zichtbaar welke risico's de strategische bewegingsruimte van het product beperken.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `positionering-en-monetisatie-toetser.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- longlist_bron: Pad naar bestaand longlist-document met kandidaat-leveranciers (type: Path, bestaand markdown-bestand; output van `leveranciers-verkenner`).
- spanningsveld_focus: Beschrijving van de spanningsveld-dimensies die moeten worden gesignaleerd (type: string, minimaal 30 tekens; bijv. vendor lock-in, platformafhankelijkheid, productiseerbaarheid, licentieerbaarheid, interoperabiliteit).

**Optionele parameters**:
- strategische_kaders: Beschrijving van de geldende positioneringskaders als context voor spanningsveld-interpretatie (type: string, default: leeg — spanningsvelden worden dan algemeen beschreven zonder strategische weging).
- te_analyseren_kandidaten: Subset van leveranciers uit de longlist die moeten worden geanalyseerd (type: list[string], default: alle kandidaten in longlist_bron).
- output_naam: Logische naam voor het outputbestand (type: string, default: afgeleid uit longlist_bron).
- aanvullende_context: Extra technische of contractuele context over de leveranciers (type: string, default: leeg).

**Afgeleide informatie** (gegenereerd door agent):
- spanningsveld_per_kandidaat: Per leverancier het gesignaleerde spanningsveld met toelichting op aard en impact.
- risicoprofiel_indicatie: Indicatie van relatieve impact van gesignaleerde spanningsvelden op strategische bewegingsruimte (hoog / middel / laag), zonder formele score of rangschikking.

### Output (wat komt eruit)

De positionering-en-monetisatie-toetser levert:
- **Spanningsvelden-overzicht** (.md) met per kandidaat-leverancier:
  - Gesignaleerde spanningsvelden per dimensie (lock-in, platformafhankelijkheid, productiseerbaarheid)
  - Toelichting op aard en impact van elk spanningsveld
  - Risicoprofiel-indicatie (hoog / middel / laag) per gesignaleerd spanningsveld
  - Onzekerheden en verificatiepunten
- Samenvattend overzicht van leveranciers met de meest en minst significante spanningsvelden

**Deliverable bestand**: `artefacten/miv/miv.07.positionering-en-monetisatie-toetser/output/spanningsvelden-{output_naam}.md`

**VERPLICHT**: Het bestand MOET worden weggeschreven naar de workspace (niet alleen voorgesteld).

**Outputformaat**:
```markdown
# Spanningsvelden-overzicht: {titel}

## 1. Scope en gehanteerde spanningsveld-dimensies
## 2. Gebruikte bronnen en externe kennis
## 3. Spanningsvelden per leverancier
### {Leverancier A}
#### Vendor lock-in
- Spanningsveld: ...
- Impact: hoog / middel / laag
- Toelichting: ...
#### Platformafhankelijkheid
- ...
#### Productiseerbaarheid
- ...
- Onzekerheden: ...
## 4. Samenvattend overzicht
## 5. Afbakening
## 6. Herkomstverantwoording
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek
- Output signaleert en beschrijft spanningsvelden; bevat geen selectieoordeel, rangschikking of aanbeveling

**Contractuele templatebinding**:

```yaml
template: ~
```

### Foutafhandeling

De positionering-en-monetisatie-toetser:
- stopt wanneer longlist_bron ontbreekt, niet leesbaar is of geen bruikbare kandidaten bevat;
- stopt wanneer spanningsveld_focus ontbreekt of te vaag is om concrete spanningsvelden per leverancier te identificeren;
- stopt wanneer de opdracht vraagt om leveranciers te rangschikken, te scoren of een selectiebeslissing te nemen op basis van de gesignaleerde spanningsvelden;
- stopt wanneer de opdracht vraagt om de strategische kaders of positioneringsstrategie aan te passen op grond van de gesignaleerde spanningsvelden;
- vraagt om verduidelijking wanneer de spanningsveld_focus zo breed is dat geen zinvolle focus per leverancier mogelijk is;
- escaleert naar leveranciers-verkenner wanneer de longlist onvoldoende platformdetails bevat om spanningsvelden te signaleren;
- escaleert naar agent-curator wanneer de gesignaleerde spanningsvelden input vragen voor een formele gunnings- of scoreaanpak die buiten de scope van deze agent valt;
- STOP: bij onvoldoende leverancierskennis om per kandidaat zinvolle spanningsvelden te identificeren.

**Contract is extern observeerbaar**: bevat GEEN implementatie-details, alleen wat agent ontvangt, levert en wanneer stopt.

---

## Werkwijze

### Stappen
1. **Lokaliseer bronartefacten**: Lees longlist_bron en interpreteer de opgegeven spanningsveld_focus en eventuele strategische_kaders.
2. **Bepaal spanningsveld-dimensies**: Leg vast welke dimensies (lock-in, platformafhankelijkheid, productiseerbaarheid, etc.) per leverancier worden geanalyseerd.
3. **Activeer externe leverancierskennis**: Raadpleeg beschikbare kennis over platformlogica, contractuele modellen en vendor-strategieën van de relevante leveranciers.
4. **Signaleer per kandidaat**: Identificeer per leverancier welke spanningsvelden aanwezig zijn, beschrijf hun aard en indiceer hun impact.
5. **Maak onzekerheden expliciet**: Benoem punten die verdere verificatie of aanvullende beoordeling vragen.
6. **Stel samenvattend overzicht op**: Geef een overzicht van de meest en minst significante spanningsveld-profielen over alle kandidaten.
7. **Controleer boundary**: Valideer dat output signaleert en beschrijft, niet rangschikt of adviseert.
8. **Schrijf output weg**: Leg het spanningsvelden-overzicht vast in de outputmap.

### Kwaliteitsborging
- Elk gesignaleerd spanningsveld is herleidbaar naar externe leverancierskennis of longlist-informatie
- Per leverancier zijn alle opgegeven spanningsveld-dimensies adresseerd
- Risicoprofiel-indicaties zijn beschrijvend, niet scorend of rangschikkend
- Output bevat geen selectieadvies of voorkeursoordeel
- Bestand weggeschreven naar: `artefacten/miv/miv.07.positionering-en-monetisatie-toetser/output/spanningsvelden-{output_naam}.md`

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar, geen implementatie
  - Principe 2 (Eenduidige Verantwoordelijkheid): Intent richt zich uitsluitend op het signaleren van spanningsvelden
  - Principe 4 (Scheiding van Wat en Hoe): Contract beschrijft spanningsveld-analyse, geen scorings- of selectielogica
  - Principe 7 (Transparante Verantwoording): Herleidbaarheid naar longlist en externe leverancierskennis is expliciet
  - Principe 9 (Output-formaat Normering): Markdown als default

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream `miv`
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: longlist_bron, strategische_kaders_bron indien opgegeven
- ✓ Aangemaakte bestanden: spanningsvelden-{output_naam}.md
- ✓ Geen gewijzigde bestanden (output is nieuw artefact)
- ✓ Overzicht externe leverancierskennis ingezet per kandidaat

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → leveranciers-verkenner: voor onvoldoende platformdetails in longlist als basis voor spanningsveld-analyse
- → agent-curator: voor ecosysteem-validatie als spanningsveld-analyse dreigt te overlappen met formele gunnings- of scoreaanpak
- STOP: bij ontbrekende spanningsveld_focus, bij onvoldoende leverancierskennis voor zinvolle identificatie

---

## Metadata

**Intent-ID**: miv.07.positionering-en-monetisatie-toetser.signaleer-spanningsvelden  
**Versie**: 1.0.0  
**Value stream**: Markt- en Investeringsvorming (miv)  
**Fase**: miv.07 — Behoeftevastlegging voor leveranciersselectie  
**Classificatie**: Toetsing × Evaluerend × Inhoudelijk × Externe-bron-gebonden
