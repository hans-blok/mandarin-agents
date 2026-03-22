---
execution_id: 55e6
timestamp: 2026-03-21 09:41:27
agent: agent-curator
intent: valideer-runner-contract-consistentie
value_stream_fase: aeo.02
canon_ref: f1bc996
agent_naam: (alle agents)
---

# Runner-Contract Consistentierapport — aeo.02

**Execution ID**: 55e6  
**Timestamp**: 2026-03-21 09:41  
**Scope**: Alle agents in value_stream_fase `aeo.02`  
**Canon Reference**: f1bc996

---

## Samenvatting

| Agent | Eindoordeel |
|-------|-------------|
| agent-curator | CONSISTENT |
| agent-engineer | INCONSISTENT |
| agent-ontwerper | DEELS-CONSISTENT |
| capability-architect | CONSISTENT |
| ecosysteem-coordinator | INCONSISTENT |

**Totaal bevindingen**: 11 (2 KRITIEK · 5 WAARSCHUWING · 4 INFORMATIEF)

---

## Overzichtstabel per intent

| Agent | Intent | Contract | Prompt | Runner | Tasks | Status |
|-------|--------|:--------:|:------:|:------:|:-----:|--------|
| agent-curator | rapporteer-ecosysteem-overzicht | ✓ | ✓ | N/A | ✓ | CONSISTENT |
| agent-curator | rapporteer-prompts-overzicht | ✓ | ✓ | ✓ | ✓ | CONSISTENT |
| agent-curator | valideer-agent-consistentie | ✓ | ✓ | N/A | ✓ | CONSISTENT |
| agent-curator | valideer-boundary-overlap | ✓ | ✓ | N/A | ✓ | CONSISTENT |
| agent-curator | valideer-runner-contract-consistentie | ✓ | ✓ | N/A | ✓ | CONSISTENT |
| agent-curator | publiceer-json | — | — | ✓ | ✓ | INFORMATIEF |
| agent-curator | publiceer-overzicht | — | — | ✓ | ✓ | INFORMATIEF |
| agent-engineer | realiseer-agent-prompts | ✓ | ✓ | ✓ | ✓ | CONSISTENT |
| agent-engineer | realiseer-agent-runner | ✓ | ✓ | ✗ | ✗ | INCONSISTENT |
| agent-engineer | realiseer-agent-taskconfiguratie | ✓ | ✓ | ✓ | ✓ | DEELS-CONSISTENT |
| agent-engineer | pipeline | — | — | ✓ | ✓ | INFORMATIEF |
| agent-engineer | execute-from-execution-file | — | — | ✓ | — | INFORMATIEF |
| agent-engineer | save-output | — | — | ✓ | — | INFORMATIEF |
| agent-ontwerper | definieer-agent-charter | ✓ | ✓ | ✓ | ✓ | DEELS-CONSISTENT |
| agent-ontwerper | definieer-agent-contract | ✓ | ✓ | ✓ | ✓ | DEELS-CONSISTENT |
| agent-ontwerper | definieer-agent-template | ✓ | ✓ | ✓ | ✓ | DEELS-CONSISTENT |
| capability-architect | definieer-agent-boundary | ✓ | ✓ | ✓ | ✓ | CONSISTENT |
| ecosysteem-coordinator | consulteer-canon | ✓ | ✓ | ✓ | ✓ | DEELS-CONSISTENT |
| ecosysteem-coordinator | genereer-instructies | ✓ | ✓ | ✓ | ✓ | DEELS-CONSISTENT |
| ecosysteem-coordinator | activeer-workspace-configuratie | ✓ | ✓ | ✓ | ✓ | DEELS-CONSISTENT |
| ecosysteem-coordinator | valideer-agent-structuur | ✓ | ✓ | ✗ | ✗ | INCONSISTENT |

**Legenda**: ✓ aanwezig en consistent · ✗ afwijking · — niet aanwezig · N/A niet van toepassing (task roept ecosysteem-coordinator aan, geen eigen runner)

---

## Afwijkingtabel

| ID | Ernst | Agent | Intent | Parameter | Aangetroffen in | Ontbreekt in / Afwijking | Aanbeveling |
|----|-------|-------|--------|-----------|-----------------|--------------------------|-------------|
| AC-01 | KRITIEK | agent-engineer | realiseer-agent-runner | `overwrite_existing` | contract (opt), prompt, task | runner: `action="store_true"` (geen waarde), maar task passeert string-waarde | Wijzig runner naar `type=str` + intern evalueren als boolean, of verwijder uit task en maak vaste flag |
| AC-02 | KRITIEK | ecosysteem-coordinator | valideer-agent-structuur | `agent_naam` | task (als required input), runner (`required=True`) | contract: "geen verplichte parameters; valideert alle agents" | Wijzig runner naar `required=False` en implementeer fallback voor "alle agents" scope |
| AC-03 | WAARSCHUWING | agent-engineer | realiseer-agent-taskconfiguratie | `agent_contracts` | contract (als "verplichte parameter") | runner, prompt, task | Herclassificeer als "afgeleide informatie" in het contract; het wordt auto-detected, niet door gebruiker meegegeven |
| AC-04 | WAARSCHUWING | agent-ontwerper | definieer-agent-charter | `value_stream_fase` | runner, task, prompt | contract (geen expliciete param-vermelding) | Voeg `value_stream_fase` toe als optionele parameter in contract (nodig voor localisering boundary file) |
| AC-05 | WAARSCHUWING | agent-ontwerper | definieer-agent-contract | `value_stream_fase` | runner, task, prompt | contract | Zelfde als AC-04 |
| AC-06a | WAARSCHUWING | agent-ontwerper | definieer-agent-template | `value_stream_fase` | runner, task, prompt | contract | Zelfde als AC-04 |
| AC-06b | INFORMATIEF | agent-ontwerper | definieer-agent-template | `file_naam_inspiratie` | runner, task, prompt | contract (typo: `file_naam_inspiriratie`) | Corrigeer typo in contract: `file_naam_inspiriratie` → `file_naam_inspiratie` |
| AC-07 | WAARSCHUWING | ecosysteem-coordinator | consulteer-canon | `workspace_file` | contract (opt), prompt | runner argparse, task | Voeg `--workspace-file` toe aan runner argparse, of verwijder uit contract/prompt indien niet CLI-leverbaar |
| AC-08 | INFORMATIEF | agent-curator | publiceer-json, publiceer-overzicht | n.v.t. | runner, task | contract, prompt (beide ontbreken) | Bevestig in charter dat deze intents code-driven zijn (geen AI-aanroep, geen contract vereist) |
| AC-09 | INFORMATIEF | agent-engineer | pipeline, execute-from-execution-file, save-output | n.v.t. | runner | contract, prompt (allen ontbreken); `execute-from-execution-file` en `save-output` ook geen task | Bepaal of deze intents AI-driven zijn (contract vereist) of code-driven (geen contract nodig) |
| AC-10 | INFORMATIEF | ecosysteem-coordinator | genereer-instructies | meerdere | runner (`--input-file`, `--minimal`, `--minimal-template`, `--log-mode`, `--bootstrap-quiet`, `--no-save`) | contract, prompt | Documenteer interne runner-flags als aparte categorie "technische runner-params" in contract; zet `--agent` en `--intent` op `required=True` in argparse |
| AC-11 | INFORMATIEF | ecosysteem-coordinator | activeer-workspace-configuratie | `output_file`, `dry_run` | contract (opt), runner | prompt (`input_parameters` leeg) | Voeg `output_file` en `dry_run` toe aan prompt frontmatter `input_parameters` |

---

## Bevindingen per agent

### agent-curator — CONSISTENT

Alle AI-driven intents zijn consistent over de vier lagen. De intents `publiceer-json` en `publiceer-overzicht` zijn code-driven en hebben geen contract/prompt — dit is by design (zie AC-08).

**Escalaties**: Geen.

---

### agent-engineer — INCONSISTENT

**KRITIEK: AC-01 — `overwrite_existing` type mismatch**

De task `realiseer-agent-runner` passeert een gebruikersinput als waarde na `--overwrite-existing`:

```json
"--overwrite-existing",
"${input:in_agent_engineer_realiseer_agent_runner_overwrite_existing}"
```

Maar de runner definieert dit argument als `action="store_true"` (een boolean flag zonder waarde). Argparse zal de string-waarde interpreteren als een extra positional argument of een onbekend argument, wat leidt tot een fout bij uitvoering.

**Impact**: De task `realiseer-agent-runner` is momenteel niet uitvoerbaar wanneer `overwrite_existing` wordt geactiveerd.

**Aanbeveling**: Escaleer naar agent-engineer voor keuze uit:
- Optie A: Wijzig runner argparse: `--overwrite-existing` als `type=str, choices=["true","false","yes","no"]` + intern evalueren als boolean
- Optie B: Verwijder `overwrite_existing` uit de task en maak het een vaste interne keuze in de runner

**WAARSCHUWING: AC-03 — `agent_contracts` classificatiefout in contract**

In het contract van `realiseer-agent-taskconfiguratie` staat `agent_contracts` vermeld als verplichte parameter, maar de toelichting zegt "Automatisch gedetecteerd via workspace-structuur". Dit is een tegenstrijdigheid: auto-detected parameters zijn per definitie afgeleide informatie, geen verplichte input. De runner heeft geen `--agent-contracts` arg en de task vraagt er ook niet om.

**Aanbeveling**: Escaleer naar agent-ontwerper voor herclassificatie in het contract.

---

### agent-ontwerper — DEELS-CONSISTENT

**WAARSCHUWING: AC-04, AC-05, AC-06a — `value_stream_fase` ontbreekt in drie contracten**

Voor alle drie intents (`definieer-agent-charter`, `definieer-agent-contract`, `definieer-agent-template`) is `value_stream_fase` aanwezig in runner, task en prompt `input_parameters`, maar ontbreekt het als expliciete parameter in het contract. De parameter is functioneel noodzakelijk (gebruikt om de boundary file te lokaliseren via `derive_boundary_file()`).

**Aanbeveling**: Escaleer naar agent-ontwerper om `value_stream_fase` toe te voegen als optionele parameter in alle drie contracten.

**INFORMATIEF: AC-06b — Typo in `definieer-agent-template` contract**

Het contract vermeldt `file_naam_inspiriratie` (dubbele 'i'), terwijl alle andere lagen `file_naam_inspiratie` gebruiken.

**Aanbeveling**: Correctie door agent-ontwerper.

---

### capability-architect — CONSISTENT

Alle vier lagen zijn volledig consistent voor de enige intent `definieer-agent-boundary`. Geen bevindingen.

---

### ecosysteem-coordinator — INCONSISTENT

**KRITIEK: AC-02 — `agent_naam` required/optioneel conflict in `valideer-agent-structuur`**

Het contract beschrijft: *"Geen verplichte parameters; valideert alle agents in workspace"* en classificeert `agent_naam` als optioneel. Maar de runner heeft `p_val.add_argument("--agent-naam", required=True)`.

Dit maakt de beschreven "valideer alle agents" functionaliteit onbereikbaar via de runner — elke aanroep zonder `--agent-naam` faalt met een argparse-fout.

**Impact**: De task sluit aan op het runner-gedrag (vraagt altijd om `agent_naam`), maar de contractbeschrijving is misleidend voor gebruikers die verwachten dat ze alle agents in één keer kunnen valideren.

**Aanbeveling**: Escaleer naar agent-engineer voor keuze uit:
- Optie A: Wijzig runner naar `required=False` en implementeer fallback logic voor "alle agents"
- Optie B: Update contract om `agent_naam` als verplichte parameter te markeren en verwijder "alle agents in workspace" als default

**WAARSCHUWING: AC-07 — `workspace_file` in consulteer-canon**

`workspace_file` staat als optionele parameter in contract en prompt `input_parameters` maar er is geen corresponderende `--workspace-file` arg in het runner argparse en de task passeert hem niet.

**INFORMATIEF: AC-10, AC-11** — Zie afwijkingtabel.

---

## Gelezen bestanden

**Tasks.json bestanden:**
- `artefacten/aeo/aeo.02.agent-curator/tasks/aeo-02.agent-curator.tasks.json`
- `artefacten/aeo/aeo.02.agent-engineer/tasks/aeo-02.agent-engineer.tasks.json`
- `artefacten/aeo/aeo.02.agent-ontwerper/tasks/aeo-02.agent-ontwerper.tasks.json`
- `artefacten/aeo/aeo.02.capability-architect/tasks/aeo-02.capability-architect.tasks.json`
- `artefacten/aeo/aeo.02.ecosysteem-coordinator/tasks/aeo-02.ecosysteem-coordinator.tasks.json`

**Runner bestanden:**
- `artefacten/aeo/aeo.02.agent-curator/runner/agent-curator.runner.py`
- `artefacten/aeo/aeo.02.agent-engineer/runner/agent-engineer.runner.py`
- `artefacten/aeo/aeo.02.agent-ontwerper/runner/agent-ontwerper.runner.py`
- `artefacten/aeo/aeo.02.capability-architect/runner/capability-architect.runner.py`
- `artefacten/aeo/aeo.02.ecosysteem-coordinator/runner/ecosysteem-coordinator.runner.py`

**Prompt bestanden (YAML frontmatter):**
- `artefacten/aeo/aeo.02.agent-curator/prompts/` (5 bestanden)
- `artefacten/aeo/aeo.02.agent-engineer/prompts/` (3 bestanden)
- `artefacten/aeo/aeo.02.agent-ontwerper/prompts/` (3 bestanden)
- `artefacten/aeo/aeo.02.capability-architect/prompts/` (1 bestand)
- `artefacten/aeo/aeo.02.ecosysteem-coordinator/prompts/` (4 bestanden)

**Contract bestanden (`### Input` secties):**
- `artefacten/aeo/aeo.02.agent-curator/agent-contracten/` (5 bestanden)
- `artefacten/aeo/aeo.02.agent-engineer/agent-contracten/` (3 bestanden)
- `artefacten/aeo/aeo.02.agent-ontwerper/agent-contracten/` (3 bestanden)
- `artefacten/aeo/aeo.02.capability-architect/agent-contracten/` (1 bestand)
- `artefacten/aeo/aeo.02.ecosysteem-coordinator/agent-contracten/` (4 bestanden)

**Aangepaste bestanden**: Geen — de agent-curator corrigeert zelf geen artefacten.

**Aangemaakte bestanden:**
- `audit/runner-contract-consistentie-20260321-0941.rapport.md` (dit bestand)
