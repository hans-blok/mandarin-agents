---
agent: agent-curator
intent: valideer-boundary-overlap
versie: 1.0.0
---

# Agent-curator — Valideer Boundary Overlap

## Rolbeschrijving (korte samenvatting)

De agent-curator analyseert de capability boundaries van alle agents in een value stream fase op mogelijke overlap of lacunes, en legt de bevindingen vast als validatierapport ter informatie voor de human-in-the-loop en ter escalatie naar de capability-architect.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `agent-curator.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- value_stream_fase: Value stream en fase waarbinnen overlap geanalyseerd wordt (type: string, format: "{vs}.{fase}", bijv. "aeo.02").

**Optionele parameters**:
- agent_namen: Specifieke subset van agents die onderling vergeleken worden (type: list[string], default: alle agents in value_stream_fase).
- canon_ref: Commit-hash van de canon-versie als toetssteen (type: string, default: meest recente pull).

**Afgeleide informatie** (geëxtraheerd uit boundary-documenten):
- capability_boundaries: Uit `{agent}.agent-boundary.md` van elke agent in scope
- intents: Uit "Voorstellen agent contracten" sectie per boundary

### Output (wat komt eruit)

De agent-curator levert:
- **Validatierapport boundary-overlap** met:
  - Overlap-tabel: welke agentparen hebben aangrenzende of overlappende boundaries (met zwaarte en aanbeveling)
  - Lacune-tabel: capabilities die door geen enkele agent gedekt worden
  - Eindoordeel per agentpaar: GEEN OVERLAP / AANGRENZEND (informatief) / OVERLAP (waarschuwing) / CONFLICT (kritiek)
  - Escalatie-lijst naar capability-architect voor herbepaling van boundaries

**Deliverable bestand**: `artefacten/{vs}/{vs}.{fase}/agent-curator.valideer-boundary-overlap.rapport.md`

**VERPLICHT**: Het bestand MOET worden weggeschreven naar de workspace.

**Outputformaat**: Volgt `artefacten/aeo/aeo.02.agent-curator/templates/validatierapport.template.md` (overlap-sectie ingevuld).

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Zwaartecategorieën voor overlappen: KRITIEK (conflict) / WAARSCHUWING (overlap) / INFORMATIEF (aangrenzend)

### Foutafhandeling

De agent-curator:
- stopt wanneer value_stream_fase niet het format `{vs}.{fase}` heeft;
- stopt wanneer minder dan 2 agent-boundary-documenten beschikbaar zijn (overlap vereist minimaal 2 agents);
- slaat agents zonder boundary-document over en vermeldt dit expliciet in het rapport;
- valideert of beoordeelt boundaries inhoudelijk niet — identificeert alleen overlapsignalen op basis van capability-boundary-tekst;
- neemt geen beslissingen over welke agent "gelijk heeft" bij conflict — escaleert uitsluitend naar capability-architect;
- STOP: wanneer boundary-documenten niet leesbaar zijn of de artefacten-map ontbreekt.

**Let op**: Overlap-identificatie is observerend, geen waardeoordeel. Herbepaling van boundaries is verantwoordelijkheid van de capability-architect.

---

## Werkwijze

### Stappen
1. **Inventariseer boundaries**: Lees alle `{agent}.agent-boundary.md` bestanden in scope.
2. **Extraheer capability-boundaries**: Haal de `capability-boundary` zin en de WEL/NIET secties op per agent.
3. **Compare paargewijs**: Vergelijk elke combinatie van twee agents op semantische overlap in capability-boundary en WEL-secties.
4. **Classificeer overlap**: GEEN OVERLAP / AANGRENZEND / OVERLAP / CONFLICT op basis van mate van semantische overeenkomst.
5. **Identificeer lacunes**: Bepaal of er verwachte capabilities zijn (gebaseerd op value stream doel) die in geen enkele boundary voorkomen.
6. **Stel escalaties samen**: Maak escalatielijst voor OVERLAP en CONFLICT gevallen naar capability-architect.
7. **Schrijf rapport**: Genereer validatierapport (overlap-sectie ingevuld) en schrijf weg naar correct pad.

### Kwaliteitsborging
- Rapport bevat overlap-tabel met elke OVERLAP of CONFLICT op agent-pair niveau
- Lacune-tabel aanwezig (mag leeg zijn)
- Escalaties traceerbaar naar capability-architect met specifiek aandachtspunt
- Geen oordeel over welke boundary "correct" is opgenomen in rapport

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 2 (Eenduidige Verantwoordelijkheid): Toetst of elke capability precies één eigenaar heeft
  - Principe 7 (Transparante Verantwoording): Bevindingen transparant gerapporteerd per agentpaar
  - Principe 9 (Output-formaat Normering): Markdown als default

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen
- Bootstrap via `scripts/bootstrap_canon_consult.py`

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: alle boundary-documenten in scope
- ✓ Aangemaakte bestanden: validatierapport boundary-overlap
- ✓ Geen gewijzigde bestanden (curator corrigeert niet)
- ✓ Aantal agentparen vergeleken en aantal overlapsignalen gevonden

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → capability-architect: voor herbepaling van boundaries bij OVERLAP of CONFLICT
- → agent-curator zelf (`valideer-agent-consistentie`): voor dieper inhoudelijk onderzoek per agent
- STOP: wanneer minder dan 2 boundary-documenten beschikbaar zijn in scope

---

## Metadata

**Intent-ID**: `aeo.02.agent-curator.valideer-boundary-overlap`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**:
- Betekeniseffect: Evaluerend
- Interventieniveau: Ecosysteem
- Werking: Inhoudelijk
- Bron-houding: Canon-gebonden
