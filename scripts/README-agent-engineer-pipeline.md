# Agent-Engineer Pipeline

Deze pipeline voert automatisch de twee cruciale agent-engineer intents uit voor een specifieke agent:

1. **realiseer-agent-prompts** - Genereert `.prompt.md` bestanden voor elke intent
2. **realiseer-agent-taskconfiguratie** - Genereert `tasks.json` bestanden voor VSCode tasks

Alle uitvoer wordt gelogd naar `logs/` folder met timestamp in de bestandsnaam.

## Gebruik

### Basis gebruik (verplicht: agent-naam)

```bash
# Windows batch
run-agent-engineer-pipeline.bat capability-architect

# Of direct Python
python scripts/agent_engineer_pipeline.py capability-architect
```

### Alle agents verwerken

```bash
# Windows batch
run-agent-engineer-pipeline.bat --all

# Of direct Python
python scripts/agent_engineer_pipeline.py --all
```

### Opties

```bash
# Dry run (toon wat uitgevoerd zou worden)
python scripts/agent_engineer_pipeline.py capability-architect --dry-run

# Skip bootstrap (sneller, alleen voor development)
python scripts/agent_engineer_pipeline.py agent-curator --skip-bootstrap

# Sla execution files op
python scripts/agent_engineer_pipeline.py agent-ontwerper --save-execution

# Combineer opties
python scripts/agent_engineer_pipeline.py agent-curator --skip-bootstrap --dry-run
```

## Wat doet de pipeline?

De pipeline:
1. **Ontdekt automatisch** alle agents met agent-contracten in `artefacten/`
2. **Voert sequentieel uit** voor elke agent:
   - `agent-engineer realiseer-agent-prompts` met parameter `agent_naam={agent}`
   - `agent-engineer realiseer-agent-taskconfiguratie` met parameter `agent_naam={agent}`
3. **Genereert**:
   - Prompt files in: `artefacten/{vs}/{vs}.{fase}.{agent}/prompts/mandarin.{agent}.{intent}.prompt.md`
   - Task files in: `artefacten/{vs}/{vs}.{fase}.{agent}/tasks/{vs}-{fase}.{agent}.tasks.json`
4. **Rapporteert** resultaten met duidelijke success/failure indicaties

## Input

De pipeline gebruikt **agent-contracten** als input. Deze worden automatisch ontdekt in:
```
artefacten/{vs}/{vs}.{fase}.{agent}/agent-contracten/*.agent.md
```

Voor elke agent met agent-contracten worden beide intents uitgevoerd.

## Output

### Per agent worden gegenereerd:

1. **Prompt bestanden** (1 per intent):
   - Locatie: `artefacten/{vs}/{vs}.{fase}.{agent}/prompts/`
   - Formaat: `mandarin.{agent}.{intent}.prompt.md`
   - Inhoud: YAML frontmatter + verwijzingen naar contract en charter

2. **Task configuratie** (1 bestand met alle intents):
   - Locatie: `artefacten/{vs}/{vs}.{fase}.{agent}/tasks/`
   - Formaat: `{vs}-{fase}.{agent}.tasks.json`
   - Inhoud: VSCode task definities voor alle intents

3. **Log bestand** (per pipeline run):
   - Locatie: `logs/`
   - Formaat: `YYYYMMDD-HHMMSS.agent-engineer-pipeline.log`
   - Inhoud: Volledige console output van de pipeline executie

### Voorbeeld output structuur:

```
artefacten/
  aeo/

logs/
  20260304-193523.agent-engineer-pipeline.log  ✓
    aeo.02.capability-architect/
      prompts/
        mandarin.capability-architect.definieer-agent-boundary.prompt.md  ✓
      tasks/
        aeo-02.capability-architect.tasks.json  ✓
```

## Vereisten

- Python 3.8+
- `python-frontmatter` package (`pip install python-frontmatter`)
- Toegang tot mandarin-canon repository (voor bootstrap)
- Workspace structuur met `artefacten/` folder

## Voorbeelden

### Voorbeeld 1: Specifieke agent verwerken

```bash
python scripts/agent_engineer_pipeline.py capability-architect
```

Output:
```
================================================================================
Agent-Engineer Pipeline: Realiseer Prompts & Tasks
================================================================================

📋 Discovering agents...
Found 1 agent(s):
  - capability-architect (1 contract(en))

[1/1] Processing: capability-architect
          Location: artefacten\aeo\aeo.02.capability-architect
  Executing: agent-engineer realiseer-agent-prompts for capability-architect
  Executing: agent-engineer realiseer-agent-taskconfiguratie for capability-architect
          Status: ✓ SUCCESS

================================================================================
Pipeline Summary
================================================================================
Total operations: 2
Completed: 2026-03-04 19:35:23
Log file: logs\20260304-193523.agent-engineer-pipeline.log

🎉 All operations completed successfully!

Log saved to: logs\20260304-193523.agent-engineer-pipeline.log
Failed:           0 ✗

🎉 All operations completed successfully!
```

### Voorbeeld 2: Alle agents verwerken

```bash
python scripts/agent_engineer_pipeline.py --all
```

Output:
```
================================================================================
Agent-Engineer Pipeline: Realiseer Prompts & Tasks
================================================================================

📋 Discovering agents...
Found 9 agent(s):
  - agent-curator (3 contract(en))
  - agent-engineer (3 contract(en))
  - agent-ontwerper (3 contract(en))
  - capability-architect (1 contract(en))
  ...

[1/9] Processing: agent-curator
          Location: artefacten\aeo\aeo.02.agent-curator
  Executing: agent-engineer realiseer-agent-prompts for agent-curator
  Executing: agent-engineer realiseer-agent-taskconfiguratie for agent-curator
          Status: ✓ SUCCESS
...

================================================================================
Pipeline Summary
================================================================================
Total operations: 18
Successful:       18 ✓
Failed:           0 ✗

🎉 All operations completed successfully!
```

### Voorbeeld 3: Dry-run voor een agent

```bash
python scripts/agent_engineer_pipeline.py capability-architect --dry-run
```

Output toont wat uitgevoerd zou worden zonder daadwerkelijke executie.

### Voorbeeld 4: Development iteratie (snel)

```bash
python scripts/agent_engineer_pipeline.py agent-curator --skip-bootstrap
```

Skipped de canon consultatie voor snellere iteraties (alleen gebruiken voor development).

## Error handling

De pipeline:
- **Stopt niet** bij individuele agent-fouten
- **Rapporteert** alle fouten aan het einde
- **Toont** gedetailleerde error output per gefaalde operatie
- **Exit code**: 0 = succes, 1 = één of meer fouten

## Integratie met workspace

Deze pipeline is onderdeel van de mandarin-agents workspace en gebruikt:
- `scripts/generate_instructions.py` - Voor het genereren van instructies
- `scripts/bootstrap_canon_consult.py` - Voor canon consultatie
- `beleid-workspace.md` - Voor workspace configuratie
- `audit/agent-instructions.log.md` - Voor logging

## Traceerbaarheid

Alle executies worden gelogd in:
- `audit/agent-instructions.log.md` - Volledige agent instructies
- `audit/canon-consult.log.md` - Canon consultaties

## Wanneer gebruiken?

Gebruik deze pipeline wanneer:
- ✅ Je nieuwe agent-contracten hebt toegevoegd
- ✅ Je bestaande agent-contracten hebt gewijzigd
- ✅ Je prompts en tasks wilt synchroniseren met contracten
- ✅ Je een bulk update wilt doen voor alle agents
- ✅ Je wilt valideren dat alle agents correct geconfigureerd zijn

## Zie ook

- [Agent-Engineer Charter](../artefacten/aeo/aeo.02.agent-engineer/agent-engineer.charter.md)
- [Agent-Engineer Contracten](../artefacten/aeo/aeo.02.agent-engineer/agent-contracten/)
- [Generate Instructions Script](./generate_instructions.py)
