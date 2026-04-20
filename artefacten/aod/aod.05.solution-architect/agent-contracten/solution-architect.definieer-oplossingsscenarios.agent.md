---
agent: solution-architect
intent: definieer-oplossingsscenarios
intent-id: aod.05.solution-architect.01
versie: 1.0.0
digest: 6a1a
status: vers
---
# Solution-architect — Definieer Oplossingsscenarios

## Rolbeschrijving (korte samenvatting)

De Solution-architect formuleert concrete oplossingsscenarios op basis van geïdentificeerde gaps en afhankelijkheden uit de integrale architectuuranalyse, met aandacht voor haalbaarheid, impact en veranderspanning per scenario.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `solution-architect.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- integrale_architectuur: Pad naar de integrale architectuurbeschrijving die als basis dient (type: string, output van definieer-integrale-architectuur).
- focus_gaps: Lijst van gaps of afhankelijkheden waarvoor oplossingsscenarios gewenst zijn (type: list[string], minimaal 1).

**Optionele parameters**:
- strategische_kaders: Pad naar strategisch kaderdocument van strategy-framework-architect voor prioritering (type: string, default: geen).
- kaderdefinities: Kaderdefinitie-documenten waarop de scenario-evaluatie zich baseert (type: string, canonieke paden, default: "grondslagen/kaderdefinities/togaf.kaderdefinitie.md").
- template_file: Override voor output template locatie (type: string, default: "artefacten/aod/aod.05.solution-architect/templates/oplossingsscenarios.template.md").
- max_scenarios_per_gap: Maximum aantal scenarios per gap (type: integer, default: 3).

**Afgeleide informatie** (geëxtraheerd uit boundary en kaderdefinitie):
- capability_boundary: Synthese-scope en -grenzen
- classificatie: Realiserend / Inhoudelijk / Canon-gebonden
- togaf_integratiekader: TOGAF Phase E evaluatiecriteria uit kaderdefinitie

### Output (wat komt eruit)

De Solution-architect levert:
- **Oplossingsscenarios** per gap met:
  - Scenario-beschrijving: wat verandert er concreet
  - Impact-analyse: welke domeinen en elementen worden geraakt
  - Haalbaarheidsanalyse: technische en organisatorische haalbaarheid
  - Veranderspanning: hoe groot is de inspanning en het risico
  - Trade-offs: wat win je, wat verlies je per scenario
- Vergelijkend overzicht van scenario's per gap
- Aanbeveling met onderbouwing

**Deliverable bestand**: `artefacten/aod/aod.05.solution-architect/output/oplossingsscenarios-{scope-kort}.md`

**Outputformaat**:
```markdown
---
agent: solution-architect
intent: definieer-oplossingsscenarios
integrale_architectuur: {integrale_architectuur}
kaderdefinities: {kaderdefinities}
versie: 1.0.0
---

# Oplossingsscenarios: {Scope}

## Samenvatting
{1-3 zinnen over de scenario-analyse}

## Bron: Integrale Architectuur
{Referentie naar en samenvatting van de gebruikte integrale architectuur}

## Scenario's per Gap

### Gap 1: {gap-beschrijving}

#### Scenario A: {scenario-naam}
- **Beschrijving**: {wat verandert er}
- **Impact**: {welke domeinen/elementen geraakt}
- **Haalbaarheid**: {technisch en organisatorisch}
- **Veranderspanning**: {laag|middel|hoog}
- **Trade-offs**: {winst vs. verlies}

#### Scenario B: {scenario-naam}
{idem}

#### Vergelijking en aanbeveling
{Vergelijkend overzicht en onderbouwde aanbeveling}

### Gap 2: {gap-beschrijving}
{idem structuur}

## Overkoepelende analyse
{Cross-gap afhankelijkheden, volgorde-implicaties}

## Aannames en beperkingen
{Expliciet gemaakte aannames bij de scenario-evaluatie}
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek
- Structuur volgt TOGAF scenarioprincipes uit kaderdefinitie

**Contractuele templatebinding**:

```yaml
template: ~
```

### Foutafhandeling

De Solution-architect:
- stopt wanneer integrale architectuurbeschrijving ontbreekt of niet leesbaar is;
- stopt wanneer focus_gaps leeg is (minimaal 1 gap vereist);
- stopt wanneer de integrale architectuur geen geïdentificeerde gaps bevat;
- vraagt om verduidelijking wanneer gaps te vaag zijn gedefinieerd om concrete scenarios te formuleren;
- escaleert naar core-framework-architect voor aanvullende domeinkennis bij complexe scenario's;
- escaleert naar strategy-framework-architect wanneer strategische prioritering nodig is maar kaders ontbreken;
- STOP: bij onvoldoende informatie om realistische scenario's te formuleren.

---

## Werkwijze

### Stappen
1. **Valideer input**: Check of integrale architectuurbeschrijving bestaat en minimaal 1 focus-gap is opgegeven
2. **Raadpleeg kaderdefinitie**: Lees TOGAF kaderdefinitie voor scenario-evaluatiecriteria
3. **Analyseer gaps**: Extraheer detail en context per focus-gap uit de integrale architectuur
4. **Formuleer scenario's**: Ontwikkel tot max_scenarios_per_gap scenario's per gap
5. **Voer impact-analyse uit**: Bepaal per scenario welke domeinen en elementen geraakt worden
6. **Beoordeel haalbaarheid**: Evalueer technische en organisatorische haalbaarheid per scenario
7. **Schat veranderspanning**: Classificeer inspanning en risico per scenario (laag/middel/hoog)
8. **Identificeer trade-offs**: Documenteer winst en verlies per scenario
9. **Vergelijk en adviseer**: Maak vergelijkend overzicht per gap met onderbouwde aanbeveling
10. **Analyseer cross-gap afhankelijkheden**: Check of scenario-keuzes in de ene gap andere gaps beïnvloeden
11. **Schrijf document**: Genereer oplossingsscenario-beschrijving en schrijf weg
12. **Valideer compleetheid**: Check of alle gaps, scenario's en criteria zijn gedocumenteerd

### Kwaliteitsborging
- Minimaal 1 gap geanalyseerd met minimaal 2 scenario's per gap
- Impact-analyse per scenario bevat concrete domeinreferenties
- Haalbaarheid bevat zowel technische als organisatorische aspecten
- Veranderspanning is geclassificeerd (laag/middel/hoog)
- Trade-offs zijn expliciet en evenwichtig (niet alleen voordelen)
- Aanbeveling per gap is onderbouwd met criteria uit kaderdefinitie
- Cross-gap afhankelijkheden zijn geïdentificeerd
- Alle aannames expliciet gemaakt
- Bestand weggeschreven naar correct pad

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.4.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract beschrijft extern observeerbaar gedrag
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén scenario-set per uitvoering
  - Principe 7 (Transparante Verantwoording): Aannames, trade-offs en bronnen expliciet
  - Principe 9 (Output-formaat Normering): Markdown als default
- **doctrine-bronhouding-en-exploratie.md**: Kaderdefinitie als normatieve controlelaag, TOGAF wordt alleen gebruikt via de kaderdefinitie

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aod
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: integrale architectuurbeschrijving, kaderdefinitie, strategische kaders (indien opgegeven)
- ✓ Aangemaakte bestanden: oplossingsscenarios-{scope}.md
- ✓ Geen gewijzigde bestanden (scenario-analyse is nieuw document)
- ✓ Aannames: lijst van gemaakte aannames bij de scenario-evaluatie

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → core-framework-architect: voor aanvullende domeinkennis bij complexe scenario's
- → strategy-framework-architect: voor ontbrekende strategische prioriteringskaders
- → capability-architect: voor boundary-verfijning bij onduidelijke scenario-scope
- → definieer-integrale-architectuur (eigen agent): wanneer integrale architectuur ontbreekt of verouderd is
- STOP: bij onvoldoende informatie voor realistische scenario's, bij onoplosbare tegenstrijdigheden in gaps

---

## Metadata

**Intent-ID**: `aod.05.solution-architect.definieer-oplossingsscenarios`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ontwerp & Doorontwikkeling (aod)  
**Fase**: 05 — Architectuursynthese  
**Classificatie**:
- Betekeniseffect: Realiserend
- Vormingsfase: Ordening
- Werking: Inhoudelijk
- Bron-houding: Canon-gebonden
