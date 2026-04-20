---
agent: knowledge-graph-modelleur
intent: valideer-graph-volledigheid
intent-id: aeo.01.knowledge-graph-modelleur.03
versie: 1.0.0
status: vers
---
# Knowledge-graph-modelleur — Valideer Graph Volledigheid

## Rolbeschrijving (korte samenvatting)

De knowledge-graph-modelleur controleert of een gegenereerde knowledge graph alle relevante elementen uit het brondocument dekt en rapporteert ontbrekende knooppunttypen, relatietypen of eigenschappen als bevindingen — zonder de graph zelf te wijzigen.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `knowledge-graph-modelleur.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- graph-bestand: Pad naar het te valideren knowledge graph-artefact (type: string, pad relatief ten opzichte van de workspace root).
- brondocument: Pad naar het oorspronkelijke gestructureerde brondocument waartegen de graph wordt gevalideerd (type: string, pad relatief ten opzichte van de workspace root).

**Optionele parameters**:
- afbakeningscriteria: Selectie van entiteiten of relaties die relevant zijn voor de validatie; wanneer afwezig wordt de volledige inhoud van het brondocument als referentie gebruikt (type: list[string], default: volledig brondocument).
- ernst-filter: Minimaal ernst-niveau van bevindingen om te rapporteren (type: string, waarden: "kritiek", "hoog", "midden", "laag", default: alle niveaus).

**Afgeleide informatie** (geëxtraheerd uit graph-bestand en brondocument):
- gedekte-elementen: Elementen uit brondocument die aanwezig zijn in de graph
- ontbrekende-elementen: Elementen uit brondocument die ontbreken in de graph

### Output (wat komt eruit)

De knowledge-graph-modelleur levert:
- **Volledigheidsrapport** met per bevinding:
  - Type: ontbrekend knooppunttype / ontbrekend relatietype / ontbrekende eigenschap / kardinaliteitsafwijking
  - Element: de naam van het ontbrekende of afwijkende element
  - Locatie in brondocument: sectie of regel waar het element is gevonden
  - Ernst-classificatie: kritiek / hoog / midden / laag
  - Verbetervoorstel: concrete suggestie voor aanvulling in de graph
- **Samenvattingstabel** met dekkingspercentage en totalen per bevindingstype
- **Aanbeveling**: volledig / aanvullingsadvies / hermodellering aanbevolen

**Deliverable bestand**: `audit/knowledge-graph-modelleur-volledigheid-{yyyymmdd-HHmm}.rapport.md`

**Contractuele templatebinding**:
```yaml
output:
  - type: validatierapport
    herkomstpositie: voortbouwend
    template: ~
```

**Formaat-normering**: 
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek

### Foutafhandeling

De knowledge-graph-modelleur:
- stopt wanneer `graph-bestand` niet bestaat of niet leesbaar is;
- stopt wanneer `brondocument` niet bestaat of niet leesbaar is;
- stopt wanneer `graph-bestand` geen herkenbare knowledge graph-structuur bevat (geen knooppunttypen of relatietypen identificeerbaar);
- vraagt om verduidelijking wanneer `afbakeningscriteria` verwijzen naar elementen die noch in de graph noch in het brondocument voorkomen.

De knowledge-graph-modelleur wijzigt de graph niet; rapporteert uitsluitend bevindingen en verbetervoorstellen.

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract beschrijft extern observeerbaar gedrag
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén taak — volledigheidsvalidatie, geen graph-aanpassing
  - Principe 4 (Scheiding van Wat en Hoe): Contract specificeert input/output, niet implementatie
  - Principe 7 (Transparante Verantwoording): Alle bevindingen herleidbaar naar brondocument
  - Principe 9 (Output-formaat Normering): Markdown als default

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen (`template: ~`)

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aeo
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door runner)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: graph-bestand, brondocument
- ✓ Aangemaakte bestanden: volledigheidsrapport
- ✓ Geen gewijzigde bestanden (knowledge-graph-modelleur wijzigt niet)
- ✓ Dekkingspercentage en aantal bevindingen per type

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → knowledge-graph-modelleur (definieer-knowledge-graph): wanneer bevindingen aanleiding geven tot regeneratie van de graph
- → logisch-modelleur: wanneer het brondocument zelf inconsistenties of lacunes bevat die de validatie blokkeren
- STOP: bij onleesbaar graph-bestand of onleesbaar brondocument

---

## Metadata

**Intent-ID**: `aeo.01.knowledge-graph-modelleur.valideer-graph-volledigheid`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 01 — Grondslagvorming  
**Classificatie**:
- Vormingsfase: Toetsing
- Betekeniseffect: Evaluerend
- Werking: Inhoudelijk
- Bronhouding: Input-gebonden
