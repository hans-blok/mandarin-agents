---
agent: agent-curator
intent: valideer-agent-consistentie
versie: 1.0.0
digest: bc40
status: vers
---
# Agent-curator — Valideer Agent Consistentie

## Rolbeschrijving (korte samenvatting)

De agent-curator toetst per agent of de artefacten (charter, contracten, prompts, tasks) canoniek consistent zijn met de actuele constitutie, doctrines en ordeningsconcepten, en legt het resultaat vast als validatierapport.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `agent-curator.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- agent_naam: Naam van de agent die getoetst wordt (type: string, kebab-case, bijv. "agent-engineer").
- value_stream_fase: Value stream en fase code (type: string, format: "{vs}.{fase}", bijv. "aeo.02").

**Optionele parameters**:
- scope: Of alleen charter, alleen contracten, of alle artefacten getoetst worden (type: string, opties: "charter", "contracten", "prompts", "tasks", "alles", default: "alles").

**Afgeleide informatie** (geëxtraheerd uit artefacten-structuur):
- artefacten-paden: Automatisch bepaald op basis van `artefacten/{vs}/{vs}.{fase}.{agent_naam}/`
- doctrine-versies: Uit de canon-referentie

### Output (wat komt eruit)

De agent-curator levert:
- **Validatierapport** met per artefact:
  - Checklijst compleetheid (verplichte secties, frontmatter, classificatie)
  - Bevindingen-tabel (ID, zwaarte, artefact-pad, bevinding, aanbeveling)
  - Eindoordeel: COMPLIANT | DEELS-COMPLIANT | NON-COMPLIANT
- Escalatielijst voor bevindingen die niet door agent-curator opgelost kunnen worden

**Deliverable bestand**: `artefacten/{vs}/{vs}.{fase}.{agent_naam}/agent-curator.valideer-agent-consistentie.rapport.md`

**VERPLICHT**: Het bestand MOET worden weggeschreven naar de workspace.

**Outputformaat**: Volgt `artefacten/aeo/aeo.02.agent-curator/templates/validatierapport.template.md`.

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Zwaartecategorieën: KRITIEK / WAARSCHUWING / INFORMATIEF
- Eindoordeel per agent: COMPLIANT / DEELS-COMPLIANT / NON-COMPLIANT

### Foutafhandeling

De agent-curator:
- stopt wanneer agent_naam niet overeenkomt met een bekende agent-map in `artefacten/`;
- stopt wanneer value_stream_fase niet het format `{vs}.{fase}` heeft;
- stopt wanneer de artefacten-map van de agent_naam leeg is of niet bestaat — escaleert naar agent-ontwerper;
- corrigeert geen artefacten zelf — signaleert en escaleert uitsluitend;
- escaleert naar constitutioneel-auteur bij onduidelijkheid over doctrine-interpretatie;
- STOP: wanneer canon-ref niet te resolven is (geen geldige commit-hash en geen recente pull beschikbaar).

**Let op**: De agent-curator corrigeert geen artefacten. Correctie is verantwoordelijkheid van agent-smeder of agent-ontwerper.

---

## Werkwijze

### Stappen
1. **Bepaal artefacten-pad**: Stel pad vast op basis van `artefacten/{vs}/{vs}.{fase}.{agent_naam}/`.
2. **Inventariseer aanwezige artefacten**: Controleer welke mappen en bestanden aanwezig zijn (charter, agent-contracten/, prompts/, tasks/, templates/).
3. **Toets per artefact-type**: Doorloop de verplichte checkboxes per type (charter: 11 secties, contracten: frontmatter + rolbeschrijving + contract + governance + metadata).
4. **Raadpleeg canon**: Toets clasificatie-assen, doctrine-naleving en traceerbaarheid aan de actuele canon-versie.
5. **Registreer bevindingen**: Maak bevindingen-tabel met unieke ID (`{agent-naam}-{volgnummer}`), zwaarte, artefact-pad en aanbeveling.
6. **Bepaal eindoordeel**: KRITIEK aanwezig → NON-COMPLIANT; alleen WAARSCHUWING → DEELS-COMPLIANT; alles voldaan → COMPLIANT.
7. **Schrijf validatierapport**: Genereer rapport conform template en schrijf weg naar correct pad.

### Kwaliteitsborging
- Rapport bevat YAML frontmatter met agent, intent, scope, value_stream_fase, datum, canon_ref
- Elke bevinding heeft uniek ID, zwaarte, artefact-pad en concrete aanbeveling
- Eindoordeel is expliciet voor de getoetste agent
- Escalaties zijn traceerbaar naar ontvanger
- Geen zelf-correcties in rapport opgenomen

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 2 (Eenduidige Verantwoordelijkheid): Toetst boundaries op eenduidigheid, signaleert overlap
  - Principe 7 (Transparante Verantwoording): Rapporteert bevindingen transparant per artefact
  - Principe 9 (Output-formaat Normering): Markdown als default

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen
- Bootstrap via `scripts/bootstrap_canon_consult.py`

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: alle artefacten in scope van agent_naam
- ✓ Aangemaakte bestanden: validatierapport
- ✓ Geen gewijzigde bestanden (curator corrigeert niet)
- ✓ Canon-referentie gebruikt voor toetsing

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → agent-ontwerper: wanneer verplichte artefacten ontbreken (charter, contracten)
- → agent-smeder: wanneer bestaande artefacten inhoudelijk gecorrigeerd moeten worden
- → constitutioneel-auteur: bij onduidelijke doctrine-interpretatie
- STOP: wanneer agent-map niet bestaat of artefacten niet leesbaar zijn

---

## Metadata

**Intent-ID**: `aeo.02.agent-curator.valideer-agent-consistentie`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**:
- Betekeniseffect: Evaluerend
- Interventieniveau: Ecosysteem
- Werking: Inhoudelijk
- Bron-houding: Canon-gebonden
