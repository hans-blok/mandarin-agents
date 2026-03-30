---
execution_id: 78af
timestamp: 2026-03-29 22:33:00
agent: agent-curator
intent: valideer-runner-contract-consistentie
value_stream_fase: aeo.02
canon_ref: ed83120
agent_naam: (alle agents)
---

# Runner-Contract Consistentierapport — aeo.02

**Execution ID**: 78af  
**Timestamp**: 2026-03-29 22:33  
**Scope**: Alle agents in value_stream_fase `aeo.02`  
**Canon Reference**: ed83120

---

## Samenvatting

| Agent | Eindoordeel |
|-------|-------------|
| agent-curator | DEELS-CONSISTENT |
| agent-engineer | CONSISTENT |
| agent-ontwerper | DEELS-CONSISTENT |
| capability-architect | CONSISTENT |
| ecosysteem-beschrijver | DEELS-CONSISTENT |

**Totaal bevindingen**: 4 (0 KRITIEK · 4 WAARSCHUWING · 0 INFORMATIEF)

---

## Interpretatiekader

- `Runner = N/A` is geldig wanneer de task bewust naar `ecosysteem-coordinator.runner.py genereer-instructies` delegeert en de intent dus niet via de eigen agent-runner wordt uitgevoerd.
- Code-driven intents zonder contract of prompt zijn buiten scope van contract-consistentie en worden alleen informatief vermeld.
- Tasks hoeven niet elke optionele parameter uit contract of runner te exposen; een subset is acceptabel zolang de task geen onbekende parameters vraagt.

---

## Overzichtstabel per intent

| Agent | Intent | Contract | Prompt | Runner | Tasks | Status |
|-------|--------|:--------:|:------:|:------:|:-----:|--------|
| agent-curator | rapporteer-ecosysteem-overzicht | ✓ | ✓ | N/A | ✓ | CONSISTENT |
| agent-curator | rapporteer-prompts-overzicht | ✓ | ✓ | ✗ | ✓ | DEELS-CONSISTENT |
| agent-curator | valideer-agent-consistentie | ✓ | ✓ | N/A | ✓ | CONSISTENT |
| agent-curator | valideer-boundary-overlap | ✓ | ✓ | N/A | ✓ | CONSISTENT |
| agent-curator | valideer-runner-contract-consistentie | ✓ | ✓ | N/A | ✓ | CONSISTENT |
| agent-curator | publiceer-json | — | — | ✓ | ✓ | INFORMATIEF |
| agent-curator | publiceer-overzicht | — | — | ✓ | ✓ | INFORMATIEF |
| agent-engineer | realiseer-agent-prompts | ✓ | ✓ | ✓ | ✓ | CONSISTENT |
| agent-engineer | realiseer-agent-runner | ✓ | ✓ | ✓ | ✓ | CONSISTENT |
| agent-engineer | realiseer-agent-taskconfiguratie | ✓ | ✓ | ✓ | ✓ | CONSISTENT |
| agent-engineer | pipeline | — | — | ✓ | — | INFORMATIEF |
| agent-engineer | execute-from-execution-file | — | — | ✓ | — | INFORMATIEF |
| agent-engineer | save-output | — | — | ✓ | — | INFORMATIEF |
| agent-ontwerper | definieer-agent-charter | ✓ | ✗ | ✓ | ✓ | DEELS-CONSISTENT |
| agent-ontwerper | definieer-agent-contract | ✓ | ✗ | ✓ | ✓ | DEELS-CONSISTENT |
| agent-ontwerper | definieer-agent-template | ✓ | ✓ | ✓ | ✓ | CONSISTENT |
| capability-architect | definieer-agent-boundary | ✓ | ✓ | ✓ | ✓ | CONSISTENT |
| ecosysteem-beschrijver | beschrijf-agent-positionering | ✓ | ✗ | ✗ | ✓ | DEELS-CONSISTENT |
| ecosysteem-beschrijver | beschrijf-ecosysteem-artefacten | ✓ | ✓ | ✓ | ✓ | CONSISTENT |
| ecosysteem-beschrijver | beschrijf-ecosysteem-contracten | ✓ | ✓ | ✓ | ✓ | CONSISTENT |
| ecosysteem-beschrijver | beschrijf-ecosysteem-value-streams-agents | ✓ | ✓ | ✓ | ✓ | CONSISTENT |

**Legenda**: ✓ aanwezig en consistent · ✗ afwijking · — niet aanwezig · N/A niet van toepassing door coordinator-delegatie

---

## Afwijkingtabel

| ID | Ernst | Agent | Intent | Parameter / onderwerp | Aangetroffen in | Ontbreekt in / Afwijking | Aanbeveling |
|----|-------|-------|--------|------------------------|-----------------|--------------------------|-------------|
| RC-01 | WAARSCHUWING | agent-curator | rapporteer-prompts-overzicht | intent-routing | contract, prompt, task definiëren een coordinator-gedreven intent zonder invoerparameters | eigen runner implementeert dezelfde intentnaam lokaal met extra CLI-parameters `scope` en `detail_niveau` | Kies één uitvoeringsmodel per intentnaam: ofwel task via eigen runner laten lopen en contract/prompt daarop aanpassen, ofwel de lokale runner-intent hernoemen/verwijderen |
| RC-02 | WAARSCHUWING | agent-ontwerper | definieer-agent-charter | `boundary_file` | contract markeert `boundary_file` als optionele parameter; runner ondersteunt `--boundary-file` | prompt-frontmatter en task-configuratie exposen deze override niet | Maak expliciet keuze: voeg `boundary_file` toe aan prompt/task, of herclassificeer deze override in het contract als niet-geëxposeerde technische parameter |
| RC-03 | WAARSCHUWING | agent-ontwerper | definieer-agent-contract | `boundary_file` | contract markeert `boundary_file` als optionele parameter; runner ondersteunt `--boundary-file` | prompt-frontmatter en task-configuratie exposen deze override niet | Zelfde oplossingsrichting als RC-02, zodat prompt en contract weer hetzelfde gebruikersoppervlak beschrijven |
| RC-04 | WAARSCHUWING | ecosysteem-beschrijver | beschrijf-agent-positionering | `scope` en `boundary_file` | contract noemt `boundary_file` en `scope` als optionele parameters; runner ondersteunt alleen `--boundary-file`; prompt en task exposen alleen `agent_naam` | `scope` ontbreekt volledig in runner, prompt en task; `boundary_file` ontbreekt in prompt en task | Verwijder `scope` uit het contract of implementeer deze parameter end-to-end; beslis daarnaast of `boundary_file` een echte gebruikersparameter is of een interne override |

---

## Bevindingen per agent

### agent-curator — DEELS-CONSISTENT

De curator-intents voor validatie en ecosysteemrapportage lopen grotendeels consistent via coordinator-delegatie. Voor die intents is `Runner = N/A` dus een geldige uitkomst. De resterende afwijking zit in `rapporteer-prompts-overzicht`: die intent bestaat tegelijk als coordinator-gedreven contract/prompt/task en als lokale runner-implementatie met een afwijkend CLI-oppervlak.

De code-driven intents `publiceer-json` en `publiceer-overzicht` zijn niet problematisch; zij hebben bewust geen contract of prompt en vallen buiten de AI-gedreven consistentietoets.

### agent-engineer — CONSISTENT

De drie contract-gedreven intents zijn nu synchroon over contract, prompt, runner en task-configuratie. De eerdere mismatch rond `overwrite_existing` is niet meer aanwezig: runner en tasks gebruiken nu compatibele parametersemantiek.

De aanvullende intents `pipeline`, `execute-from-execution-file` en `save-output` zijn interne/code-driven runnerpaden en vallen buiten de contractlaag.

### agent-ontwerper — DEELS-CONSISTENT

De recente opschoning rond `value_stream_fase` werkt zoals bedoeld: deze parameter is afgeleid en wordt niet langer onnodig aan de gebruiker gevraagd. De overgebleven afwijkingen zijn beperkter en zitten alleen in de optionele `boundary_file` override.

Voor `definieer-agent-charter` en `definieer-agent-contract` beschrijven contract en runner die override nog wel, maar prompt en task niet. Daardoor beschrijft de prompt niet het volledige gebruikersoppervlak van het contract.

### capability-architect — CONSISTENT

De intent `definieer-agent-boundary` is consistent over alle vier lagen. Geen bevindingen.

### ecosysteem-beschrijver — DEELS-CONSISTENT

Drie intents zijn consistent wanneer tasks als minimale uitvoerbare subset worden gelezen: `beschrijf-ecosysteem-artefacten`, `beschrijf-ecosysteem-contracten` en `beschrijf-ecosysteem-value-streams-agents`.

Alleen `beschrijf-agent-positionering` bevat contractdrift. Het contract noemt nog een `scope`-parameter die in runner, prompt en tasks niet meer bestaat. Daarnaast is `boundary_file` wel runner-ondersteund, maar niet zichtbaar in prompt of task.

---

## Conclusie

De AEO.02-scope is aantoonbaar gezonder dan in het eerdere rapport van 2026-03-21. De zware afwijkingen in `agent-engineer` zijn weggevallen en er resteert nu uitsluitend contract- en promptdrift in drie agents. Er zijn in deze run geen kritieke runner/task-breuken vastgesteld.

De eerstvolgende correctieronde kan beperkt blijven tot:

1. het opheffen van de dubbele intent-routing in `agent-curator`;
2. het expliciet maken van de status van `boundary_file` in `agent-ontwerper`;
3. het opschonen van de verouderde `scope`-parameter in `ecosysteem-beschrijver`.

---

## Gelezen bestanden

**Contracten**
- `artefacten/aeo/aeo.02.agent-curator/agent-contracten/*.agent.md`
- `artefacten/aeo/aeo.02.agent-engineer/agent-contracten/*.agent.md`
- `artefacten/aeo/aeo.02.agent-ontwerper/agent-contracten/*.agent.md`
- `artefacten/aeo/aeo.02.capability-architect/agent-contracten/*.agent.md`
- `artefacten/aeo/aeo.02.ecosysteem-beschrijver/agent-contracten/*.agent.md`

**Prompts**
- `artefacten/aeo/aeo.02.agent-curator/prompts/*.prompt.md`
- `artefacten/aeo/aeo.02.agent-engineer/prompts/*.prompt.md`
- `artefacten/aeo/aeo.02.agent-ontwerper/prompts/*.prompt.md`
- `artefacten/aeo/aeo.02.capability-architect/prompts/*.prompt.md`
- `artefacten/aeo/aeo.02.ecosysteem-beschrijver/prompts/*.prompt.md`

**Runners**
- `artefacten/aeo/aeo.02.agent-curator/runner/agent-curator.runner.py`
- `artefacten/aeo/aeo.02.agent-engineer/runner/agent-engineer.runner.py`
- `artefacten/aeo/aeo.02.agent-ontwerper/runner/agent-ontwerper.runner.py`
- `artefacten/aeo/aeo.02.capability-architect/runner/capability-architect.runner.py`
- `artefacten/aeo/aeo.02.ecosysteem-beschrijver/runner/ecosysteem-beschrijver.runner.py`

**Tasks**
- `artefacten/aeo/aeo.02.agent-curator/tasks/aeo-02.agent-curator.tasks.json`
- `artefacten/aeo/aeo.02.agent-engineer/tasks/aeo-02.agent-engineer.tasks.json`
- `artefacten/aeo/aeo.02.agent-ontwerper/tasks/aeo-02.agent-ontwerper.tasks.json`
- `artefacten/aeo/aeo.02.capability-architect/tasks/aeo-02.capability-architect.tasks.json`
- `artefacten/aeo/aeo.02.ecosysteem-beschrijver/tasks/aeo-02.ecosysteem-beschrijver.tasks.json`

**Aangemaakte bestanden**
- `audit/runner-contract-consistentie-20260329-2233.rapport.md`

**Aangepaste bestanden**: Geen