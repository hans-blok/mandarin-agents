# Engineer-Steward Script Herschrijving Rapport

**Versie:** 1.0  
**Datum:** 2024-12-19  
**Agent:** engineer-steward  
**Intent:** schrijf-script  
**Opdracht:** Herschrijf copy_aeo_02_agents voor vereenvoudigde JSON-publicatie

---

## 1. Opdrachtbeschrijving

De gebruiker verzocht om herschrijving van `copy_aeo_02_agents` omdat `agents-publicatie.json` te veel data bevat. De nieuwe oplossing moet:

1. **JSON-schema maken** met vereenvoudigde structuur:
   - `value_streams` (array) met `code` property
   - `value_stream_fase` (array) met `volgnummer` property
   - `agents` (array) met alleen counts: `naam`, `aantal_agent_files`, `aantal_prompts`, `aantal_templates`, `aantal_charters`

2. **Alle value streams scannen** (niet alleen AEO 02)

3. **Clean Code principes** toepassen per engineer-steward charter

---

## 2. Gerealiseerde Artefacten

### 2.1 JSON Schema v2.0

**Bestand:** `schemas/agents-publicatie-schema.json`

**Status:** ✓ Gemaakt/Overschreven

**Wijzigingen:**
- Volledig nieuwe structuur met `metadata` en `value_streams` top-level properties
- `metadata` bevat: `gegenereerd_op` (ISO 8601), `versie`, `aantal_value_streams`, `aantal_agents`
- `value_streams` array met:
  - `code` (3-letter lowercase, bijv. "aeo", "miv")
  - `fasen` array met `volgnummer` (2-cijferig, bijv. "01", "02")
  - `agents` array met `naam` en 4 count fields
- Voldoet aan JSON Schema Draft 07 specificatie
- Inclusief regex patterns voor validatie (code: `^[a-z]{3}$`, volgnummer: `^\\d{2}$`)

### 2.2 Python Script

**Bestand:** `scripts/generate_agents_publicatie.py`

**Status:** ✓ Nieuw gemaakt

**Kenmerken:**
- **Versie:** 2.0.0
- **Regels:** 286 LOC
- **Type hints:** Volledig gedocumenteerd met moderne Python typing (`Dict`, `List`, `Tuple`, `Path`)
- **Docstrings:** Alle functies voorzien van Google-style docstrings met Args, Returns, Raises, Examples
- **PEP 8:** Conform (max line length 88, proper imports, snake_case)
- **Error handling:** Specifieke exceptions (FileNotFoundError, IOError) met duidelijke exit codes

**Functie-overzicht:**

1. `parse_agent_folder_name(folder_name: str) -> Tuple[str, str, str] | None`
   - Parse `aeo.01.canon-curator` naar `('aeo', '01', 'canon-curator')`
   - Regex validatie: `^([a-z]{3})\.(\d{2})\.([a-z][a-z0-9-]+)$`

2. `count_agent_artifacts(agent_path: Path) -> Dict[str, int]`
   - Tel `*.agent.md`, `*.prompt.md`, `*template*.md`, `*.charter.md`
   - Returns dictionary met 4 counts

3. `scan_value_stream_folders(artefacten_path: Path) -> Dict[str, Dict[str, List[Dict]]]`
   - Scan alle value_stream folders in `artefacten/`
   - Skip `__pycache__` en non-value_stream folders
   - Bouw nested dict: `{vs: {fase: [agents]}}`

4. `build_json_structure(data: Dict[..]) -> Dict`
   - Transform naar schema v2.0 structuur
   - Voeg metadata toe (timestamp, totals)
   - Sorteer value_streams, fasen, agents alfabetisch

5. `generate_agents_publicatie(workspace_root: Path, output_file: str) -> None`
   - Orchestratie functie met progress output
   - Schrijf JSON met UTF-8 encoding en indent=2

6. `main() -> None`
   - Entry point met exception handling
   - Bepaal workspace_root automatisch (2 levels omhoog)

**Verbeteringen t.o.v. oude script:**
- ✓ Scant **alle** value_streams (niet alleen AEO 02)
- ✓ Geen copy functionaliteit meer (focus op JSON generatie)
- ✓ Vereenvoudigde output (counts i.p.v. volledige metadata)
- ✓ Betere error handling en logging
- ✓ Type-safe met modern Python 3.9+ typing

### 2.3 Batch Wrapper

**Bestand:** `generate-agents-publicatie.bat`

**Status:** ✓ Nieuw gemaakt

**Functie:**
- Windows batch wrapper voor Python script
- Zet working directory naar workspace root
- Error checking met exit codes
- User-friendly output met banners

---

## 3. Voorbeeld Output Structuur

```json
{
  "metadata": {
    "gegenereerd_op": "2024-12-19T14:30:00.123456",
    "versie": "2.0",
    "aantal_value_streams": 6,
    "aantal_agents": 42
  },
  "value_streams": [
    {
      "code": "aeo",
      "fasen": [
        {
          "volgnummer": "01",
          "agents": [
            {
              "naam": "canon-curator",
              "aantal_agent_files": 4,
              "aantal_prompts": 4,
              "aantal_templates": 0,
              "aantal_charters": 1
            },
            {
              "naam": "workspace-steward",
              "aantal_agent_files": 3,
              "aantal_prompts": 3,
              "aantal_templates": 2,
              "aantal_charters": 1
            }
          ]
        },
        {
          "volgnummer": "02",
          "agents": [...]
        }
      ]
    },
    {
      "code": "miv",
      "fasen": [...]
    }
  ]
}
```

---

## 4. Uitvoering

### Via Batch File (Aanbevolen)
```batch
generate-agents-publicatie.bat
```

### Direct via Python
```powershell
cd C:\git\mandarin-agents
python scripts\generate_agents_publicatie.py
```

**Output:**
- Genereert `agents-publicatie.json` in workspace root
- Console output toont progress en statistics
- Exit codes:
  - 0 = Success
  - 1 = FileNotFoundError
  - 2 = IOError
  - 99 = Unexpected error

---

## 5. Validatie

Het gegenereerde JSON bestand kan gevalideerd worden tegen het schema:

```python
import json
import jsonschema

with open('agents-publicatie.json') as f:
    data = json.load(f)
    
with open('schemas/agents-publicatie-schema.json') as f:
    schema = json.load(f)
    
jsonschema.validate(data, schema)  # Raises exception bij invalide data
```

---

## 6. Migratie van Oude naar Nieuwe Versie

### Oude versie (`copy_aeo_02_agents.py`)
- Scant alleen `artefacten/aeo/aeo.02.*`
- Kopieert bestanden naar workspace locaties
- Genereert verbose JSON met volledige metadata:
  ```json
  {
    "naam": "agent-curator",
    "value_stream": "aeo",
    "fase": "01",
    "folder": "artefacten/aeo/aeo.01.agent-curator",
    "charter": true,
    "intents": ["analyseer", "bepaal-agent-boundary", ...],
    "runner": true,
    "contracten": 4
  }
  ```

### Nieuwe versie (`generate_agents_publicatie.py`)
- Scant **alle** value_streams
- Genereert alleen JSON (geen file copy)
- Vereenvoudigde output met counts only:
  ```json
  {
    "naam": "agent-curator",
    "aantal_agent_files": 4,
    "aantal_prompts": 4,
    "aantal_templates": 0,
    "aantal_charters": 1
  }
  ```

### Aanbeveling
- Behoud oude `copy_aeo_02_agents.py` voor backwards compatibility
- Gebruik nieuwe `generate_agents_publicatie.py` voor publicatie-doeleinden
- Oude JSON bevat meer detail (geschikt voor intern gebruik)
- Nieuwe JSON is schoner (geschikt voor externe publicatie)

---

## 7. Traceerbaarheid

**Bronnen:**
- Opdracht: Gebruiker message 15
- Charter: `agent-charters/engineer-steward.charter.md`
- Contract: `artefacten/fnd/fnd.01.engineer-steward/engineer-steward.schrijf-script.agent.md`
- Prompt metadata: `.github/prompts/mandarin.engineer-steward-schrijf.script.prompt.md`

**Herkomstverantwoording:**
- **Basis:** Herschrijving van `scripts/copy_aeo_02_agents.py` (v1.0, 86 LOC)
- **Inspiratie:** Engineer-steward charter sectie 8 (Code Complete principes)
- **Schema:** Nieuw ontwerp op basis van gebruikerswens voor vereenvoudiging
- **Naming:** Volgt mandarin conventie: `{value_stream}.{fase}.{agent_naam}`

**Versioning:**
- JSON Schema: v2.0 (breaking change door volledig nieuwe structuur)
- Python Script: v2.0.0 (major rewrite)
- Batch File: v2.0.0 (nieuw, gekoppeld aan script versie)

---

## 8. Toekomstige Uitbreidingen

Mogelijke verbeteringen:

1. **JSON Schema validatie in script**
   - Automatische validatie van output tegen schema
   - Requires: `pip install jsonschema`

2. **CI/CD integratie**
   - Automatisch regenereren bij commit
   - GitHub Action voor validatie

3. **Diff rapportage**
   - Vergelijk oude vs nieuwe JSON
   - Highlight toegevoegde/verwijderde agents

4. **Web visualisatie**
   - HTML dashboard met agent statistics
   - Grafische weergave van value_stream distributie

5. **API endpoint**
   - Serve JSON via REST API
   - Auto-update bij workspace changes

---

## 9. Conclusie

✓ **Opdracht voltooid**

- JSON-schema v2.0 gemaakt met vereenvoudigde structuur
- Python script met Code Complete principes (type hints, docstrings, PEP 8)
- Batch wrapper voor eenvoudige uitvoering
- Volledige documentatie in rapport

**Deliverables:**
1. `schemas/agents-publicatie-schema.json` (v2.0)
2. `scripts/generate_agents_publicatie.py` (286 LOC, v2.0.0)
3. `generate-agents-publicatie.bat` (v2.0.0)
4. Dit rapport (documentatie)

**Status:** Klaar voor gebruik
