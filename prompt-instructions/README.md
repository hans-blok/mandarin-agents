# Execution-bestanden

Deze folder bevat gegenereerde execution-bestanden (**bronpakketten**) voor lokale uitvoering.
Een execution-bestand is het resultaat van bronassemblage door de ecosysteem-coordinator:
het bevat de volledige samengestelde instructies die een LLM als context ontvangt.

## Bestandsformaat

`<timestamp>-<agent-naam>.<intent>.md`

**Timestamp**: `yyyyMMddHHmmss` voor chronologische ordening  
**Agent-naam**: De uitvoerende agent (bijv. `agent-ontwerper`, `capability-architect`)  
**Intent**: De specifieke taak (bijv. `definieer-agent-charter`)

## Generatie

Gebruik de VS Code task: **"Agent: Execute (Generate + Save)"**
- `Ctrl+Shift+P` → `Tasks: Run Task` → Selecteer de task
- Vul agent-naam en intent in
- Bestand wordt automatisch aangemaakt en geopend

## Gebruik

1. Task genereert instructies via `generate_instructions.py` (stap 0-8)
2. Bestand wordt opgeslagen in deze folder
3. Bestand wordt automatisch geopend in VS Code
4. Kopieer de inhoud (`Ctrl+A`, `Ctrl+C`)
5. Plak in GitHub Copilot Chat (`Ctrl+V`)
6. Agent voert instructies uit met volledige canon context

## Tracking

Alle bestanden zijn traceerbaar via:
- Timestamp in hash (voor chronologie)
- Agent-naam (wie voert uit)
- Intent (wat wordt gedaan)

**Opmerking**: Execution-bestanden zijn lokaal en worden niet gecommit naar git (zie `.gitignore`).
