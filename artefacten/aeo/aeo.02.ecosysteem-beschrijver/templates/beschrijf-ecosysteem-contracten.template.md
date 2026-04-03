---
agent: ecosysteem-beschrijver
template_naam: beschrijf-ecosysteem-contracten
versie: 1.0.0
output_type: document
doel: Geeft een gestructureerd overzicht van alle agent-contracten in het ecosysteem — per agent, per intent — met de kerngegevens uit elke contract-frontmatter en input/output-synopsis.
digest: 52bc
status: vers
---
# Template: Ecosysteem Contractenoverzicht

## Doel en gebruik

Dit template structureert de output van de intent `beschrijf-ecosysteem-contracten`. Het produceert een leesbaar overzicht van alle agent-contracten in scope, inclusief de kerngegevens uit elk contract (agent, intent, versie, input-parameters, output-deliverable). Het document is beschrijvend — het evalueert niet of contracten volledig of correct zijn.

Gebruikt door: `beschrijf-ecosysteem-contracten`

## Structuur

```markdown
---
agent: ecosysteem-beschrijver
intent: beschrijf-ecosysteem-contracten
value_stream_fase: <value_stream_fase>
scope: <agent-naam of "alle agents in <fase>">
timestamp: <yyyy-mm-dd HH:MM>
---

# Ecosysteem Contractenoverzicht — <scope>

## Inleiding

<Korte beschrijving van de scope: welke agents, welke fase, op basis van welke bronbestanden.>

## Contracten per agent

### <agent-naam-1>

**Aantal contracten**: <n>

#### <intent-naam-1>

**Contract**: `agent-contracten/<agent-naam>.<intent-naam>.agent.md`  
**Versie**: <versie uit frontmatter, of "—" indien ontbreekt>

**Input-parameters**:
- Verplicht: <lijst of "geen">
- Optioneel: <lijst of "geen">
- Afgeleid: <lijst of "geen">

**Output-deliverable**: `<pad uit contract>`

**Foutafhandeling (samenvatting)**: <één zin over de voornaamste stop-conditie>

---

#### <intent-naam-2>

[herhaal structuur]

---

### <agent-naam-2>

[herhaal structuur]

---

## Samenvatting

| Agent | Intents | Contracten aanwezig | Gemiste contracten |
|-------|---------|--------------------|--------------------|
| <agent-naam-1> | <intents uit boundary> | <aanwezige intents> | <intents zonder contract> |
| <agent-naam-2> | ... | ... | ... |

## Bronbestanden

- `artefacten/<vs>/<vs>.<fase>.<agent>/agent-contracten/*.agent.md`
```

## Placeholders

| Placeholder | Type | Beschrijving | Verplicht |
|-------------|------|--------------|-----------|
| `<value_stream_fase>` | string | bijv. "aeo.02" | Ja |
| `<scope>` | string | agent-naam of "alle agents in aeo.02" | Ja |
| `<timestamp>` | string | ISO 8601 datetime | Ja |
| `<agent-naam>` | string | kebab-case agent naam | Ja |
| `<intent-naam>` | string | intent-naam in kebab-case | Ja |
| `<versie>` | string | versie-string uit contract-frontmatter, bijv. "1.0.0" | Ja |
| `<pad>` | string | output-pad uit contract | Ja |

## Validatie-criteria

- ✓ Elk contract heeft een sectie met input-parameters (verplicht/optioneel/afgeleid) en output-deliverable
- ✓ Versie is overgenomen uit contract-frontmatter (of "—" als ontbreekt)
- ✓ Samenvatting-tabel geeft per agent het delta tussen boundary-intents en aanwezige contracten
- ✓ Document bevat geen oordelen over contractkwaliteit
- ✓ Bronbestanden zijn expliciet vermeld

## Voorbeeld-output

```markdown
---
agent: ecosysteem-beschrijver
intent: beschrijf-ecosysteem-contracten
value_stream_fase: aeo.02
scope: agent-curator
timestamp: 2026-03-21 10:00
---

# Ecosysteem Contractenoverzicht — agent-curator

## Inleiding

Overzicht van alle contracten van agent-curator in aeo.02,
op basis van artefacten/aeo/aeo.02.agent-curator/agent-contracten/.

## Contracten per agent

### agent-curator

**Aantal contracten**: 5

#### valideer-agent-consistentie

**Contract**: `agent-contracten/agent-curator.valideer-agent-consistentie.agent.md`  
**Versie**: 1.0.0

**Input-parameters**:
- Verplicht: agent_naam, value_stream_fase
- Optioneel: scope
- Afgeleid: artefacten-paden, doctrine-versies

**Output-deliverable**: `artefacten/{vs}/{vs}.{fase}.{agent}/agent-curator.valideer-agent-consistentie.rapport.md`

**Foutafhandeling (samenvatting)**: Stopt wanneer vereiste bestanden ontleesbaar zijn.

## Samenvatting

| Agent | Intents in boundary | Contracten aanwezig | Gemiste contracten |
|-------|---------------------|--------------------|--------------------|
| agent-curator | 5 | 5 | geen |

## Bronbestanden

- artefacten/aeo/aeo.02.agent-curator/agent-contracten/
```

## Gebruiksinstructies

1. Bepaal de scope.
2. Lees per agent alle bestanden in `agent-contracten/`.
3. Extraheer per contract: frontmatter (agent, intent, versie), `### Input` sectie en output-pad.
4. Vergelijk de gevonden intents met de intents in het boundary-document.
5. Schrijf de samenvatting-tabel met het delta.
6. Schrijf het document weg conform de output-locatie-afspraak.

## Versiebeheer

| Versie | Datum | Wijziging |
|--------|-------|-----------|
| 1.0.0 | 2026-03-21 | Initiële template voor ecosysteem-beschrijver |

---

**Template-categorie**: Agent-specifiek  
**Gebruikt door intents**: beschrijf-ecosysteem-contracten
