---
agent: ecosysteem-beschrijver
intent: beschrijf-ecosysteem-value-streams-agents
intent-id: aeo.02.ecosysteem-beschrijver.04
versie: 1.0.0
digest: 9d40
status: vers
---
# Ecosysteem-beschrijver — Beschrijf Ecosysteem Value Streams & Agents

## Rolbeschrijving (korte samenvatting)

De ecosysteem-beschrijver legt een gestructureerd overzicht vast van alle value streams en hun agents — welke agents per value stream en fase actief zijn, inclusief hun boundary-classificatie, domein en intentaantal, volledig herleidbaar tot de boundary-documenten in de workspace.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `ecosysteem-beschrijver.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- `value_stream_fase`: Scope van het overzicht (type: string, bijv. "aeo.02" of "alle").

**Optionele parameters**:
- `value_stream`: Beperk het overzicht tot één value stream (type: string, bijv. "aeo", default: alle value streams in scope).

**Afgeleide informatie** (geëxtraheerd uit workspace):
- `agent_folders`: Alle mappen in `artefacten/{vs}/{vs}.{fase}.*`.
- `boundary_inhoud`: Capability boundary, domein, classificatie en intents per agent, uit het boundary-document.

### Output (wat komt eruit)

De ecosysteem-beschrijver levert:
- **Value streams & agents overzicht** (.md) met per value stream een gegroepeerd agent-overzicht en een agents-matrix.

**Deliverable bestand**: `artefacten/{vs}/{vs}.{fase}.ecosysteem-beschrijver/ecosysteem-beschrijver.beschrijf-ecosysteem-value-streams-agents.md`

**Outputformaat** (conform `beschrijf-ecosysteem-value-streams-agents.template.md`):
```markdown
---
agent: ecosysteem-beschrijver
intent: beschrijf-ecosysteem-value-streams-agents
value_stream_fase: {value_stream_fase}
scope: {scope}
timestamp: {yyyy-mm-dd HH:MM}
---

# Ecosysteem: Value Streams & Agents — {scope}

## {value-stream-code} — {value-stream-naam}

### Fase {fase-code}

| Agent | Korte boundary-zin | Domein | Intents |
|---|---|---|---|
| {agent-naam} | {eerste zin capability boundary} | {domein} | {n} |

## Agents-matrix

| Agent | Value stream | Fase | Output-type | Intents |
|---|---|---|---|---|
| {agent-naam} | {vs} | {fase} | {output-type} | {n} |

## Bronbestanden

- artefacten/{vs}/{vs}.{fase}.*/{agent}.agent-boundary.md
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Boundary-zin: eerste zin uit de `capability-boundary` van het boundary-document
- Intentaantal: geteld op basis van "Voorstellen agent contracten" sectie in boundary

**Contractuele templatebinding**:

```yaml
template: templates/beschrijf-ecosysteem-value-streams-agents.template.md
```

### Foutafhandeling

De ecosysteem-beschrijver:
- stopt wanneer geen boundary-documenten aanwezig zijn in de opgegeven scope;
- stopt wanneer de workspace-structuur niet bereikbaar of leesbaar is;
- produceert een gedeeltelijk overzicht (met expliciete melding) wanneer individuele boundary-documenten niet leesbaar zijn;
- vermeldt agents zonder boundary-document expliciet in de matrix als "(boundary ontbreekt)";
- escaleert naar agent-curator wanneer de mappenstructuur afwijkt van de verwachte `{vs}.{fase}.{agent}` conventie;
- STOP: bij volledig ontbreken van agent-folders in de opgegeven scope.

**Contract is extern observeerbaar**: bevat GEEN ontwerp, normering of beoordeling — alleen vastlegging van de actuele ecosysteemtoestand.

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar, geen implementatie
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén intent, één value stream & agents overzicht
  - Principe 7 (Transparante Verantwoording): Bronbestanden expliciet vermeld in output
  - Principe 9 (Output-formaat Normering): Markdown als default

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Niet van toepassing — ecosysteem-beschrijver is input-gebonden, geen canon-consultatie vereist

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: alle boundary-documenten in scope
- ✓ Aangemaakte bestanden: `ecosysteem-beschrijver.beschrijf-ecosysteem-value-streams-agents.md`
- ✓ Vermeld welke agents boundary-document missen (indien van toepassing)

**Escalatie-paden:**
- → agent-curator: als mappenstructuur of agent-naamgeving afwijkt van conventies
- → capability-architect: als agents ontbreken of boundary-documenten incompleet zijn (signalering, geen corrigerende actie)
- STOP: bij ontbrekende of volledig onleesbare workspace-structuur

---

## Metadata

**Intent-ID**: `aeo.02.ecosysteem-beschrijver.beschrijf-ecosysteem-value-streams-agents`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**:
- Vormingsfase: Vastlegging, Verantwoording
- Betekeniseffect: Beschrijvend
- Werking: Inhoudelijk
- Bronhouding: Input-gebonden
