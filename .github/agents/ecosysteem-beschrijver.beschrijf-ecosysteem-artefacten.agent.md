---
agent: ecosysteem-beschrijver
intent: beschrijf-ecosysteem-artefacten
versie: 1.0.0
digest: f8ae
status: vers
---
# Ecosysteem-beschrijver — Beschrijf Ecosysteem Artefacten

## Rolbeschrijving (korte samenvatting)

De ecosysteem-beschrijver inventariseert alle artefacten in de workspace per agent — boundaries, charters, contracten, prompts, templates, runners en taken — en legt deze feitelijk vast als een gestructureerd overzicht, volledig herleidbaar tot de bestaande mappenstructuur.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `ecosysteem-beschrijver.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- `value_stream_fase`: Value stream fase als scope van de inventarisatie (type: string, bijv. "aeo.02").

**Optionele parameters**:
- `agent_naam`: Beperk de inventarisatie tot één specifieke agent (type: string, kebab-case, default: alle agents in de fase).
- `artefact_types`: Komma-gescheiden lijst van artefacttypen om te scannen (type: string, default: alle typen: "boundary,charter,contract,prompt,template,runner,task").

**Afgeleide informatie** (geëxtraheerd uit mappenstructuur):
- `agent_folders`: Alle mappen in `artefacten/{vs}/{vs}.{fase}.*` die als agent-folder kwalificeren.
- `artefact_paden`: Bestandspaden per artefacttype per agent.

### Output (wat komt eruit)

De ecosysteem-beschrijver levert:
- **Artefactenoverzicht** (.md) met per agent een tabel van aanwezige artefacten, inclusief pad en type.

**Deliverable bestand**: `artefacten/{vs}/{vs}.{fase}.ecosysteem-beschrijver/ecosysteem-beschrijver.beschrijf-ecosysteem-artefacten.md`

**Outputformaat** (conform `beschrijf-ecosysteem-artefacten.template.md`):
```markdown
---
agent: ecosysteem-beschrijver
intent: beschrijf-ecosysteem-artefacten
value_stream_fase: {value_stream_fase}
scope: {scope}
timestamp: {yyyy-mm-dd HH:MM}
---

# Ecosysteem Artefactenoverzicht — {scope}

## {agent-naam}

| Artefacttype | Bestandsnaam | Aanwezig |
|---|---|---|
| boundary | {agent}.agent-boundary.md | ✓ / — |
| charter | {agent}.charter.md | ✓ / — |
| contract | agent-contracten/{agent}.{intent}.agent.md | ✓ / — |
| ...

## Bronbestanden

- artefacten/{vs}/{vs}.{fase}.*/
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Tabellen per agent, één rij per artefact
- Aanwezigheid: ✓ (aanwezig) of — (ontbreekt)

### Foutafhandeling

De ecosysteem-beschrijver:
- stopt wanneer de `value_stream_fase` geen overeenkomende mappen heeft in `artefacten/`;
- stopt wanneer de workspace-structuur niet bereikbaar of leesbaar is;
- stopt wanneer `agent_naam` is opgegeven maar geen overeenkomende map bestaat;
- produceert een gedeeltelijk overzicht (met expliciete melding) wanneer individuele bestanden niet leesbaar zijn;
- escaleert naar agent-curator wanneer de mappenstructuur afwijkt van de verwachte fs-conventie;
- STOP: bij volledig ontbreken van agent-folders in de opgegeven fase.

**Contract is extern observeerbaar**: bevat GEEN oordeel over volledigheid of kwaliteit — alleen feitelijke inventarisatie.

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar, geen implementatie
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén intent, één artefactenoverzicht
  - Principe 7 (Transparante Verantwoording): Bronbestanden expliciet vermeld in output
  - Principe 9 (Output-formaat Normering): Markdown als default

**Canon-consultatie:**
- Niet van toepassing — ecosysteem-beschrijver is input-gebonden, geen canon-consultatie vereist

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gescande mappen: alle agent-folders in scope
- ✓ Aangemaakte bestanden: `ecosysteem-beschrijver.beschrijf-ecosysteem-artefacten.md`
- ✓ Vermeld per agent welke artefacttypen aanwezig of ontbrekend zijn

**Escalatie-paden:**
- → agent-curator: als mappenstructuur afwijkt van afgesproken conventies
- → agent-engineer: als verwachte artefacten structureel ontbreken (geen inventarisatie-taak, maar signalering)
- STOP: bij ontbrekende of onleesbare fase-map

---

## Metadata

**Intent-ID**: `aeo.02.ecosysteem-beschrijver.beschrijf-ecosysteem-artefacten`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**:
- Vormingsfase: Vastlegging, Verantwoording
- Betekeniseffect: Beschrijvend
- Werking: Inhoudelijk
- Bronhouding: Input-gebonden
