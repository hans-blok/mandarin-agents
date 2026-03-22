---
agent: ecosysteem-beschrijver
template_naam: beschrijf-ecosysteem-artefacten
versie: 1.0.0
output_type: document
doel: Inventariseert alle aanwezige artefacten in het agent-ecosysteem per agent — welke bestanden aanwezig zijn, van welk type, op welk pad — volledig feitelijk.
---

# Template: Ecosysteem Artefacten-inventaris

## Doel en gebruik

Dit template structureert de output van de intent `beschrijf-ecosysteem-artefacten`. Het producert een gestructureerde inventaris van alle artefacten (charter, boundary, agent-contracten, prompts, runner, tasks, templates) per agent in de opgegeven scope. Het document is een feitelijke weergave van de aangetroffen bestanden — geen evaluatie van volledigheid of kwaliteit.

Gebruikt door: `beschrijf-ecosysteem-artefacten`

## Structuur

```markdown
---
agent: ecosysteem-beschrijver
intent: beschrijf-ecosysteem-artefacten
value_stream_fase: <value_stream_fase>
scope: <agent-naam of "alle agents in <fase>">
timestamp: <yyyy-mm-dd HH:MM>
---

# Ecosysteem Artefacten-inventaris — <scope>

## Inleiding

<Korte beschrijving van de scope en de basis voor deze inventaris (welke folders gescand).>

## Artefacten per agent

### <agent-naam-1>

**Artefacten-map**: `artefacten/<vs>/<vs>.<fase>.<agent-naam>/`

| Artefact-type | Bestandsnaam | Pad | Aanwezig |
|---------------|--------------|-----|----------|
| Charter | `<agent-naam>.charter.md` | `artefacten/<vs>/<vs>.<fase>.<agent>/` | <Ja/Nee> |
| Agent boundary | `<agent-naam>.agent-boundary.md` | `artefacten/<vs>/<vs>.<fase>.<agent>/` | <Ja/Nee> |
| Agent-contract | `<agent-naam>.<intent>.agent.md` | `agent-contracten/` | <Ja/Nee> |
| Prompt | `mandarin.<agent-naam>.<intent>.prompt.md` | `prompts/` | <Ja/Nee> |
| Runner | `<agent-naam>.runner.py` | `runner/` | <Ja/Nee> |
| Task-configuratie | `<fase>-<agent-naam>.tasks.json` | `tasks/` | <Ja/Nee> |
| Template | `<template-naam>.template.md` | `templates/` | <Ja/Nee> |

**Intents met contract**: <lijst van intents waarvoor een contract aanwezig is>  
**Intents met prompt**: <lijst van intents waarvoor een prompt aanwezig is>

---

### <agent-naam-2>

[herhaal structuur]

---

## Samenvatting

| Agent | Charter | Boundary | Contracten | Prompts | Runner | Tasks | Templates |
|-------|---------|----------|------------|---------|--------|-------|-----------|
| <agent-naam-1> | <Ja/Nee> | <Ja/Nee> | <aantal> | <aantal> | <Ja/Nee> | <Ja/Nee> | <aantal> |
| <agent-naam-2> | <Ja/Nee> | <Ja/Nee> | <aantal> | <aantal> | <Ja/Nee> | <Ja/Nee> | <aantal> |

## Gescande mappen

- `artefacten/<vs>/<vs>.<fase>.*/`
```

## Placeholders

| Placeholder | Type | Beschrijving | Verplicht |
|-------------|------|--------------|-----------|
| `<value_stream_fase>` | string | bijv. "aeo.02" | Ja |
| `<scope>` | string | agent-naam of "alle agents in aeo.02" | Ja |
| `<timestamp>` | string | ISO 8601 datetime | Ja |
| `<agent-naam>` | string | kebab-case agent naam | Ja |
| `<vs>` | string | value stream code, bijv. "aeo" | Ja |
| `<fase>` | string | fase-nummer, bijv. "02" | Ja |
| `<intent>` | string | intent-naam in kebab-case | Ja |
| `<template-naam>` | string | naam van het template-bestand zonder extensie | Nee |

## Validatie-criteria

- ✓ Elke agent in scope heeft een eigen tabel met alle 7 artefact-typen vermeld
- ✓ Aanwezigheid is sec feitelijk ("Ja"/"Nee") — geen kwaliteitsoordelen
- ✓ Samenvatting-tabel dekt alle agents in scope
- ✓ Gescande mappen zijn expliciet vermeld
- ✓ Intents met contract en intents met prompt zijn per agent apart vermeld

## Voorbeeld-output

```markdown
---
agent: ecosysteem-beschrijver
intent: beschrijf-ecosysteem-artefacten
value_stream_fase: aeo.02
scope: agent-curator
timestamp: 2026-03-21 10:00
---

# Ecosysteem Artefacten-inventaris — agent-curator

## Inleiding

Inventaris van artefacten voor agent-curator in aeo.02,
gescand in artefacten/aeo/aeo.02.agent-curator/.

## Artefacten per agent

### agent-curator

**Artefacten-map**: `artefacten/aeo/aeo.02.agent-curator/`

| Artefact-type | Bestandsnaam | Pad | Aanwezig |
|---------------|--------------|-----|----------|
| Charter | `agent-curator.charter.md` | `artefacten/aeo/aeo.02.agent-curator/` | Ja |
| Agent boundary | `agent-curator.agent-boundary.md` | `artefacten/aeo/aeo.02.agent-curator/` | Ja |
| Agent-contract | `agent-curator.valideer-agent-consistentie.agent.md` | `agent-contracten/` | Ja |
| Prompt | `mandarin.agent-curator.valideer-agent-consistentie.prompt.md` | `prompts/` | Ja |
| Runner | `agent-curator.runner.py` | `runner/` | Ja |
| Task-configuratie | `aeo-02.agent-curator.tasks.json` | `tasks/` | Ja |
| Template | `validatierapport.template.md` | `templates/` | Ja |

**Intents met contract**: valideer-agent-consistentie, rapporteer-ecosysteem-overzicht,
rapporteer-prompts-overzicht, valideer-boundary-overlap, valideer-runner-contract-consistentie  
**Intents met prompt**: valideer-agent-consistentie, rapporteer-ecosysteem-overzicht,
rapporteer-prompts-overzicht, valideer-boundary-overlap, valideer-runner-contract-consistentie

## Gescande mappen

- `artefacten/aeo/aeo.02.agent-curator/`
```

## Gebruiksinstructies

1. Bepaal de scope: één agent-folder of alle agent-folders in een fase.
2. Scan per agent de mapstructuur op de 7 artefact-typen (charter, boundary, contracten, prompts, runner, tasks, templates).
3. Noteer voor elk artefact-type het exacte bestandspad en of het bestand aanwezig is.
4. Vermeld per agent de intents waarvoor een contract en een prompt aanwezig zijn.
5. Vul de samenvatting-tabel met aantallen.
6. Schrijf het document weg conform de output-locatie-afspraak.

## Versiebeheer

| Versie | Datum | Wijziging |
|--------|-------|-----------|
| 1.0.0 | 2026-03-21 | Initiële template voor ecosysteem-beschrijver |

---

**Template-categorie**: Agent-specifiek  
**Gebruikt door intents**: beschrijf-ecosysteem-artefacten
