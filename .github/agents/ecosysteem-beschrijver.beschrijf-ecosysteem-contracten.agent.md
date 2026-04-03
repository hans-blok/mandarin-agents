---
agent: ecosysteem-beschrijver
intent: beschrijf-ecosysteem-contracten
versie: 1.0.0
digest: 1a38
status: vers
---
# Ecosysteem-beschrijver — Beschrijf Ecosysteem Contracten

## Rolbeschrijving (korte samenvatting)

De ecosysteem-beschrijver inventariseert alle agent-contracten in het ecosysteem per agent en intent, en legt de kerngegevens uit elk contract vast als feitelijk overzicht — inclusief delta tussen boundary-intents en aanwezige contracten.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `ecosysteem-beschrijver.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- `value_stream_fase`: Value stream fase als scope van de inventarisatie (type: string, bijv. "aeo.02").

**Optionele parameters**:
- `agent_naam`: Beperk de inventarisatie tot één specifieke agent (type: string, kebab-case, default: alle agents in de fase).

**Afgeleide informatie** (geëxtraheerd uit workspace):
- `contract_bestanden`: Alle `.agent.md` bestanden in `agent-contracten/` mappen per agent.
- `boundary_intents`: Intents uit de "Voorstellen agent contracten" sectie van elk boundary-document.
- `versie`: Uit de YAML frontmatter van elk contract (indien aanwezig).

### Output (wat komt eruit)

De ecosysteem-beschrijver levert:
- **Contractenoverzicht** (.md) met per agent een contractentabel en een samenvatting van het delta.

**Deliverable bestand**: `artefacten/{vs}/{vs}.{fase}.ecosysteem-beschrijver/ecosysteem-beschrijver.beschrijf-ecosysteem-contracten.md`

**Outputformaat** (conform `beschrijf-ecosysteem-contracten.template.md`):
```markdown
---
agent: ecosysteem-beschrijver
intent: beschrijf-ecosysteem-contracten
value_stream_fase: {value_stream_fase}
scope: {scope}
timestamp: {yyyy-mm-dd HH:MM}
---

# Ecosysteem Contractenoverzicht — {scope}

## {agent-naam}

#### {intent-naam}

**Contract**: `agent-contracten/{agent}.{intent}.agent.md`
**Versie**: {versie of "—"}

**Input-parameters**:
- Verplicht: {lijst}
- Optioneel: {lijst}

**Output-deliverable**: `{pad}`

---

## Samenvatting

| Agent | Intents in boundary | Contracten aanwezig | Gemiste contracten |
|---|---|---|---|
| {agent} | {n} | {n} | {lijst of "geen"} |

## Bronbestanden

- artefacten/{vs}/{vs}.{fase}.*/agent-contracten/
- artefacten/{vs}/{vs}.{fase}.*/{agent}.agent-boundary.md
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Versie: overgenomen uit contract-frontmatter of "—" als ontbreekt
- Geen evaluatie of oordeel — alleen feitelijke inventarisatie

### Foutafhandeling

De ecosysteem-beschrijver:
- stopt wanneer de `value_stream_fase` geen overeenkomende mappen heeft in `artefacten/`;
- stopt wanneer geen enkel boundary-document leesbaar is in de opgegeven scope;
- produceert een gedeeltelijk overzicht (met expliciete melding) wanneer individuele contractbestanden niet leesbaar zijn;
- vermeldt ontbrekende contracten in de samenvatting-tabel zonder dit te evalueren;
- escaleert naar agent-curator wanneer contractstructuur afwijkt van de verwachte `.agent.md` conventie;
- STOP: bij volledig ontbreken van `agent-contracten/` mappen in de opgegeven fase.

**Contract is extern observeerbaar**: bevat GEEN beoordeling van contractkwaliteit — alleen vastlegging van wat aanwezig is.

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar, geen implementatie
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén intent, één contractenoverzicht
  - Principe 7 (Transparante Verantwoording): Bronbestanden en delta expliciet vermeld in output
  - Principe 9 (Output-formaat Normering): Markdown als default

**Canon-consultatie:**
- Niet van toepassing — ecosysteem-beschrijver is input-gebonden, geen canon-consultatie vereist

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: alle boundary-documenten en contractbestanden in scope
- ✓ Aangemaakte bestanden: `ecosysteem-beschrijver.beschrijf-ecosysteem-contracten.md`
- ✓ Vermeld delta: welke boundary-intents geen contract hebben

**Escalatie-paden:**
- → agent-curator: als contractstructuur of naamgeving afwijkt van conventies
- → agent-ontwerper: als boundary-intents structureel geen contract hebben (signalering, geen corrigerende actie)
- STOP: bij ontbrekende of onleesbare fase-map

---

## Metadata

**Intent-ID**: `aeo.02.ecosysteem-beschrijver.beschrijf-ecosysteem-contracten`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**:
- Vormingsfase: Vastlegging, Verantwoording
- Betekeniseffect: Beschrijvend
- Werking: Inhoudelijk
- Bronhouding: Input-gebonden
