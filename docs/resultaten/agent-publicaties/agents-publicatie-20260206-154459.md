# Agents Publicatie Overzicht

**Publicatiedatum**: 2026-02-06
**Tijdstip**: 15:44:59
**Digest**: fa897
**Totaal agents**: 22

## Value Stream: Agent Ecosysteem Ontwikkeling (AEO)

### Fase 01: Grondslagvorming

**Aantal agents**: 2

| Agent | Domein | Contracts | Templates | Runners |
|-------|--------|-----------|-----------|----------|
| canon-curator | Agent boundary-setting, value stream administratie, agent-ecosysteem oversight | 4 | 1 | 0 |
| constitutioneel-auteur | Normatieve doctrine en governance | 1 | 0 | 0 |

### Fase 02: Ecosysteeminrichting

**Aantal agents**: 2

| Agent | Domein | Contracts | Templates | Runners |
|-------|--------|-----------|-----------|----------|
| agent-curator | Agent-ecosysteem analyse en administratieve overzichten | 4 | 0 | 1 |
| agent-smeder | Agent-ontwerp, capability boundaries en contract-first uitvoering | 0 | 2 | 0 |

### Fase 03: Fase 03

**Aantal agents**: 2

| Agent | Domein | Contracts | Templates | Runners |
|-------|--------|-----------|-----------|----------|
| pipeline-executor | Pipeline-uitvoering, workflow-orkestratie | 1 | 0 | 0 |
| workflow-architect | Workflow-ontwerp, multi-agent orkestratie | 3 | 0 | 0 |

## Value Stream: Architectuur- en Oplossingsontwerp (AOD)

### Fase 01: Vraagverkenning

**Aantal agents**: 1

| Agent | Domein | Contracts | Templates | Runners |
|-------|--------|-----------|-----------|----------|
| mandarin-architect | architectuur | 2 | 0 | 0 |

### Fase 02: Architectuurkadering

**Aantal agents**: 1

| Agent | Domein | Contracts | Templates | Runners |
|-------|--------|-----------|-----------|----------|
| archimate-modelleur | Enterprise architecture modellering | 2 | 0 | 0 |

## Value Stream: Foundational (value-stream-overstijgend) (FND)

### Fase 01: Technische ondersteuning

**Aantal agents**: 2

| Agent | Domein | Contracts | Templates | Runners |
|-------|--------|-----------|-----------|----------|
| engineer-steward | Python-ontwikkeling, code-kwaliteit, technische stewardship | 3 | 0 | 0 |
| workspace-steward | Workspace-ordening, governance, agent-lifecycle | 5 | 0 | 0 |

### Fase 02: Fase 02

**Aantal agents**: 2

| Agent | Domein | Contracts | Templates | Runners |
|-------|--------|-----------|-----------|----------|
| concept-curator | Foundation (FND) - Conceptbeheer en taalconsistentie | 2 | 1 | 0 |
| formaat-vertaler | Formaat-conversie voor documenten | 3 | 0 | 0 |

## Value Stream: Kennisvastlegging (KVL)

### Fase 03: Vastlegging

**Aantal agents**: 3

| Agent | Domein | Contracts | Templates | Runners |
|-------|--------|-----------|-----------|----------|
| artikel-schrijver | Artikelproductie, kennisoverdracht | 6 | 0 | 0 |
| de-schrijver | Narratieve tekstproductie, kennisoverdracht | 0 | 0 | 0 |
| essayist | Essayproductie, reflectieve kennisoverdracht | 1 | 0 | 0 |

### Fase 04: Publicatie en Onderhoud

**Aantal agents**: 2

| Agent | Domein | Contracts | Templates | Runners |
|-------|--------|-----------|-----------|----------|
| heraut | Canonieke aankondiging, governance communicatie | 2 | 0 | 0 |
| vertaler | Tekstvertaling, meertalige kennisoverdracht | 1 | 0 | 0 |

## Value Stream: Markt- en Investeringsvorming (MIV)

### Fase 01: Strategische intentie expliciteren

**Aantal agents**: 1

| Agent | Domein | Contracts | Templates | Runners |
|-------|--------|-----------|-----------|----------|
| strategisch-analist | Markt- en investeringsvorming, strategische intentie-explicitering | 3 | 0 | 0 |

### Fase 02: Waarde-hypotheses formuleren

**Aantal agents**: 1

| Agent | Domein | Contracts | Templates | Runners |
|-------|--------|-----------|-----------|----------|
| hypothese-vormer | Productontwikkeling – Verandering & Verkenning | 3 | 1 | 0 |

## Value Stream: Softwareontwikkeling (SFW)

### Fase 01: Veranderkenning

**Aantal agents**: 1

| Agent | Domein | Contracts | Templates | Runners |
|-------|--------|-----------|-----------|----------|
| niam-analist | Informatieanalyse en conceptuele modellering | 5 | 0 | 0 |

### Fase 02: Werkvoorbereiding

**Aantal agents**: 2

| Agent | Domein | Contracts | Templates | Runners |
|-------|--------|-----------|-----------|----------|
| thema-verwoorder | themavorming naar epic-statement | 2 | 0 | 0 |
| verbeteringen-beschrijver | expliciete werkvoorbereiding volgens SAFe (THEMA, VERBETERING, WERKTAAK) | 2 | 0 | 0 |

## Metadata

- **Gescande folders**:
  - `artefacten/<vs-code>.<fase-nr>.<agent-naam>/` (alle agent folders)
- **Folder naamgevingsconventie**: `<vs-code>.<fase-nr>.<agent-naam>`
  - `vs-code`: 3-letter value stream code (aeo, sfw, aod, kvl, miv, fnd)
  - `fase-nr`: 2-cijferig fasenummer (01, 02, ...)
  - `agent-naam`: agent identifier (lowercase met hyphens)
- **Contracts**: `<agent-naam>.*.agent.md` bestanden in agent folder
- **Templates**: Template veld in charter (niet '-' of '—')
- **Runners**: `scripts/runners/<agent-naam>.py` of `scripts/runners/<agent-naam>/__init__.py`
- **Digest**: 5-karakter SHA-256 hash van agents-lijst (gesorteerd) voor change-tracking
- **Schema**: `schemas/agents-publicatie-schema.json`
- **Traceability**: Agent Curator charter, publiceer-agents-overzicht contract & prompt
