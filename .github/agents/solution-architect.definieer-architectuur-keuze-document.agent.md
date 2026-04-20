---
agent: solution-architect
intent: definieer-architectuur-keuze-document
intent-id: aod.05.solution-architect.03
versie: 1.0.0
digest: 4933
status: vers
---
# Solution-architect — Definieer Architectuur-keuze-document

## Rolbeschrijving (korte samenvatting)

De Solution-architect legt een architectuurkeuze gestructureerd vast met context, opties, afwegingen, advies en consequenties per architectuurlaag. Het document heeft raakvlakken met een ADR, maar het besluit zelf wordt door een andere agent of stakeholder genomen.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `solution-architect.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- onderwerp: Titel van de architectuurkeuze (type: string, bijv. "Keuze UBL voor e-factureren").
- probleemstelling: Beschrijving van de huidige situatie en het probleem of de kans (type: string).
- opties: Lijst van opties die vergeleken worden (type: list[string], minimaal 2).

**Optionele parameters**:
- integrale_architectuur: Pad naar integrale architectuurbeschrijving als achtergrond (type: string, default: geen).
- strategische_kaders: Pad naar strategisch kaderdocument voor beleidscontext (type: string, default: geen).
- kaderdefinities: Kaderdefinitie-documenten waarop de afweging zich baseert (type: string, canonieke paden, default: "grondslagen/kaderdefinities/togaf.kaderdefinitie.md").
- template_file: Override voor output template locatie (type: string, default: "artefacten/aod/aod.05.solution-architect/templates/solution-architect.definieer-architectuur-keuze-document.template.md").

**Afgeleide informatie** (geëxtraheerd uit boundary en kaderdefinitie):
- capability_boundary: Synthese-scope en -grenzen
- classificatie: Realiserend / Inhoudelijk / Canon-gebonden
- togaf_integratiekader: TOGAF Phase E afwegingscriteria uit kaderdefinitie

### Output (wat komt eruit)

De Solution-architect levert:
- **Architectuur-keuze-document** met:
  - Samenvatting van de kernkeuze
  - Context: probleemstelling met opties en achtergrond (beleid, kaders, eerdere besluiten)
  - Afweging: voordelen en nadelen per optiepaar
  - Advies: voorkeur met motivatie en alternatief met condities
  - Consequenties per architectuurlaag (dienstverlening, organisatie, informatie, techniek, financieel)
  - Implementatievoorstel: actietabel met verantwoordelijke en tijdspad
  - Betrokkenen: RACI-achtige tabel
- Expliciete aannames en beperkingen

**Let op**: Het document legt het advies vast, niet het besluit. Het besluit wordt genomen door de verantwoordelijke stakeholder(s) of besluitvormingsagent.

**Deliverable bestand**: `artefacten/aod/aod.05.solution-architect/output/architectuur-keuze-{onderwerp-kort}.md`

**Outputformaat**: Volgens template `solution-architect.definieer-architectuur-keuze-document.template.md`

```markdown
---
agent: solution-architect
intent: definieer-architectuur-keuze-document
scope: {scope-omschrijving}
kaderdefinities: {kaderdefinities}
versie: 1.0.0
datum: {yyyy-mm-dd}
---

# Architectuurkeuze-document: {Onderwerp}

**Status**: {Concept | In review | Geadviseerd | Besloten}
**Datum**: {yyyy-mm-dd}
**Auteur(s)**: {agent of persoon}

## Samenvatting Keuze
## Context
### Probleemstelling
### Achtergrond
## Afweging
### Voordelen {Optie A} t.o.v. {Optie B}
### Nadelen {Optie A} t.o.v. {Optie B}
## Advies
## Consequenties
### Dienstverlening & Samenleving
### Organisatie & (Keten)processen
### Informatie & Applicatie
### Techniek & Infrastructuur
### Financieel
## Implementatie (voorstel)
## Verwijzingen
## Openstaande vragen
## Betrokkenen
## Aannames en beperkingen
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek
- Structuur volgt template `solution-architect.definieer-architectuur-keuze-document.template.md`

**Contractuele templatebinding**:

```yaml
template: templates/solution-architect.definieer-architectuur-keuze-document.template.md
```

### Foutafhandeling

De Solution-architect:
- stopt wanneer onderwerp of probleemstelling ontbreekt;
- stopt wanneer minder dan 2 opties zijn opgegeven (afweging vereist minimaal 2 opties);
- vraagt om verduidelijking wanneer opties onvoldoende onderscheidend zijn om zinvolle voor-/nadelenanalyse te maken;
- escaleert naar strategy-framework-architect wanneer strategische kaders nodig zijn maar ontbreken;
- escaleert naar core-framework-architect voor aanvullende domeinkennis bij technische afwegingen;
- escaleert naar definieer-integrale-architectuur (eigen agent) wanneer een integrale architectuuranalyse nodig is als basis;
- STOP: bij onvoldoende informatie om een evenwichtige afweging te produceren.

---

## Werkwijze

### Stappen
1. **Valideer input**: Check of onderwerp, probleemstelling en minimaal 2 opties aanwezig zijn
2. **Raadpleeg kaderdefinitie**: Lees TOGAF kaderdefinitie voor afwegingscriteria
3. **Laad template**: Lees `solution-architect.definieer-architectuur-keuze-document.template.md`
4. **Analyseer context**: Verwerk probleemstelling, achtergrond en eventuele integrale architectuur
5. **Voer afweging uit**: Vergelijk opties op voordelen en nadelen per relevant aspect
6. **Formuleer advies**: Bepaal voorkeur met motivatie en identificeer alternatief met condities
7. **Analyseer consequenties**: Werk consequenties uit per architectuurlaag
8. **Stel implementatie voor**: Formuleer actietabel met verantwoordelijken en tijdspad
9. **Documenteer aannames**: Maak alle aannames en beperkingen expliciet
10. **Schrijf document**: Genereer architectuur-keuze-document volgens template en schrijf weg
11. **Valideer compleetheid**: Check of alle secties uit het template zijn ingevuld

### Kwaliteitsborging
- Minimaal 2 opties vergeleken met concrete voor- en nadelen
- Afweging bevat meerdere aspecten (niet alleen technisch)
- Advies is onderbouwd met verwijzing naar kaders en afwegingscriteria
- Consequenties zijn uitgewerkt per architectuurlaag
- Alle aannames expliciet gemaakt
- Template-structuur volledig gevolgd
- Bestand weggeschreven naar correct pad

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.4.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract beschrijft extern observeerbaar gedrag
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén architectuurkeuze per uitvoering
  - Principe 7 (Transparante Verantwoording): Aannames, afwegingen en bronnen expliciet
  - Principe 9 (Output-formaat Normering): Markdown als default, template-gebonden
- **doctrine-bronhouding-en-exploratie.md**: Kaderdefinitie als normatieve controlelaag, TOGAF wordt alleen gebruikt via de kaderdefinitie

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aod
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: template, integrale architectuur (indien opgegeven), kaderdefinitie, strategische kaders (indien opgegeven)
- ✓ Aangemaakte bestanden: architectuur-keuze-{onderwerp-kort}.md
- ✓ Geen gewijzigde bestanden (keuze-document is nieuw document)
- ✓ Aannames: lijst van gemaakte aannames bij de afweging

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → strategy-framework-architect: voor ontbrekende strategische kaders
- → core-framework-architect: voor aanvullende domeinkennis bij technische afwegingen
- → definieer-integrale-architectuur (eigen agent): wanneer integrale architectuuranalyse nodig is als basis
- → capability-architect: voor boundary-verfijning bij onduidelijke scope
- STOP: bij onvoldoende informatie voor evenwichtige afweging

---

## Metadata

**Intent-ID**: `aod.05.solution-architect.definieer-architectuur-keuze-document`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ontwerp & Doorontwikkeling (aod)  
**Fase**: 05 — Architectuursynthese  
**Template**: `artefacten/aod/aod.05.solution-architect/templates/solution-architect.definieer-architectuur-keuze-document.template.md`  
**Classificatie**:
- Betekeniseffect: Realiserend
- Vormingsfase: Ordening
- Werking: Inhoudelijk
- Bron-houding: Canon-gebonden
