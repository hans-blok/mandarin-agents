---
agent: solution-architect
intent: definieer-integrale-architectuur
versie: 1.0.0
---

# Solution-architect — Definieer Integrale Architectuur

## Rolbeschrijving (korte samenvatting)

De Solution-architect synthetiseert alle beschikbare domeinarchitecturen (business, applicatie, data, technologie) tot één integrale architectuurbeschrijving met expliciete samenhang, gaps en afhankelijkheden, binnen het TOGAF-integratiekader.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `solution-architect.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- scope: Afbakening van het synthesegebied (type: string, bijv. "volledig landschap", "domein X + domein Y", "value stream aod").
- domeinarchitecturen: Lijst van paden naar domeinarchitectuur-artefacten die als input dienen (type: list[string], minimaal 2 domeinen).

**Optionele parameters**:
- strategische_kaders: Pad naar strategisch kaderdocument van strategy-framework-architect (type: string, default: geen).
- kaderdefinities: Kaderdefinitie-documenten waarop de synthese zich baseert (type: string, canonieke paden, default: "grondslagen/kaderdefinities/togaf.kaderdefinitie.md").
- template_file: Override voor output template locatie (type: string, default: "artefacten/aod/aod.05.solution-architect/templates/integrale-architectuur.template.md").
- focus_lagen: Specifieke architectuurlagen om op te focussen (type: list[string], bijv. ["business", "applicatie"], default: alle lagen).

**Afgeleide informatie** (geëxtraheerd uit boundary en kaderdefinitie):
- capability_boundary: Synthese-scope en -grenzen
- classificatie: Realiserend / Inhoudelijk / Canon-gebonden
- togaf_integratiekader: TOGAF Phase E principes en structuur uit kaderdefinitie

### Output (wat komt eruit)

De Solution-architect levert:
- **Integrale architectuurbeschrijving** met:
  - Cross-domein samenhanganalyse: hoe domeinen op elkaar aansluiten
  - Gap-analyse: waar samenhang ontbreekt of inconsistent is
  - Afhankelijkheidsmatrix: welke domeinen waarvan afhankelijk zijn
  - Geïntegreerd overzicht per laag (business → applicatie → data → technologie)
  - Traceability: hoe elementen uit verschillende domeinen zich tot elkaar verhouden
- Korte toelichting op synthese-keuzes en aannames

**Deliverable bestand**: `artefacten/aod/aod.05.solution-architect/output/integrale-architectuur-{scope-kort}.md`

**Outputformaat**:
```markdown
---
agent: solution-architect
intent: definieer-integrale-architectuur
scope: {scope}
kaderdefinities: {kaderdefinities}
versie: 1.0.0
---

# Integrale Architectuur: {Scope}

## Samenvatting
{1-3 zinnen over de synthese}

## Geanalyseerde domeinen
{Lijst van input-domeinarchitecturen met korte status}

## Cross-domein samenhanganalyse
### Business ↔ Applicatie
### Applicatie ↔ Data
### Data ↔ Technologie
### Business ↔ Technologie (end-to-end)

## Gap-analyse
{Waar ontbreekt samenhang, waar zijn inconsistenties}

## Afhankelijkheidsmatrix
{Welke domeinen afhankelijk zijn van welke}

## Traceability
{Hoe elementen zich tot elkaar verhouden}

## Aannames en beperkingen
{Expliciet gemaakte aannames bij de synthese}
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek
- Structuur volgt TOGAF integratieprincipes uit kaderdefinitie

### Foutafhandeling

De Solution-architect:
- stopt wanneer minder dan 2 domeinarchitecturen beschikbaar zijn (synthese vereist minimaal 2 domeinen);
- stopt wanneer scope ontbreekt of te vaag is om af te bakenen;
- stopt wanneer domeinarchitectuur-bestanden niet bestaan of niet te lezen zijn;
- vraagt om verduidelijking wanneer domeinarchitecturen onderling tegenstrijdige structuren bevatten die niet oplosbaar zijn;
- escaleert naar core-framework-architect voor ontbrekende of onvolledige domeinarchitecturen;
- escaleert naar strategy-framework-architect wanneer strategische kaders nodig zijn maar ontbreken;
- STOP: bij onvoldoende domeinmateriaal om zinvolle synthese te produceren.

---

## Werkwijze

### Stappen
1. **Valideer input**: Check of minimaal 2 domeinarchitecturen beschikbaar en leesbaar zijn
2. **Raadpleeg kaderdefinitie**: Lees TOGAF kaderdefinitie voor integratieprincipes en -structuur
3. **Analyseer per domein**: Extraheer kernstructuren, elementen en relaties per domeinarchitectuur
4. **Identificeer cross-domein relaties**: Map relaties tussen domeinen (serving, realization, access, flow)
5. **Voer gap-analyse uit**: Identificeer waar samenhang ontbreekt of inconsistent is
6. **Bouw afhankelijkheidsmatrix**: Documenteer welke domeinen waarvan afhankelijk zijn
7. **Synthethiseer integraal overzicht**: Combineer alle analyses tot één samenhangend document
8. **Documenteer aannames**: Maak alle aannames en beperkingen bij de synthese expliciet
9. **Schrijf document**: Genereer integrale architectuurbeschrijving en schrijf weg
10. **Valideer compleetheid**: Check of alle lagen, gaps en afhankelijkheden zijn gedocumenteerd

### Kwaliteitsborging
- Minimaal 2 domeinen geanalyseerd
- Cross-domein relaties expliciet gedocumenteerd per domeinpaar
- Gap-analyse bevat concrete gaps (niet alleen "geen gaps gevonden")
- Afhankelijkheidsmatrix is volledig (alle domeinparen)
- Alle aannames expliciet gemaakt
- TOGAF-kaderdefinitie aantoonbaar gevolgd
- Bestand weggeschreven naar correct pad

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.4.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract beschrijft extern observeerbaar gedrag
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén integrale synthese per uitvoering
  - Principe 7 (Transparante Verantwoording): Aannames en bronnen expliciet
  - Principe 9 (Output-formaat Normering): Markdown als default
- **doctrine-bronhouding-en-exploratie.md**: Kaderdefinitie als normatieve controlelaag, TOGAF wordt alleen gebruikt via de kaderdefinitie

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aod
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: alle domeinarchitectuur-bestanden, kaderdefinitie, strategische kaders (indien opgegeven)
- ✓ Aangemaakte bestanden: integrale-architectuur-{scope}.md
- ✓ Geen gewijzigde bestanden (synthese is nieuw document)
- ✓ Aannames: lijst van gemaakte aannames bij de synthese

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → core-framework-architect: voor ontbrekende of onvolledige domeinarchitecturen
- → strategy-framework-architect: voor ontbrekende strategische kaders
- → capability-architect: voor boundary-verfijning bij onduidelijke synthese-scope
- STOP: bij onvoldoende domeinmateriaal, bij onoplosbare tegenstrijdigheden tussen domeinen

---

## Metadata

**Intent-ID**: `aod.05.solution-architect.definieer-integrale-architectuur`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ontwerp & Doorontwikkeling (aod)  
**Fase**: 05 — Architectuursynthese  
**Classificatie**:
- Betekeniseffect: Realiserend
- Vormingsfase: Ordening
- Werking: Inhoudelijk
- Bron-houding: Canon-gebonden
