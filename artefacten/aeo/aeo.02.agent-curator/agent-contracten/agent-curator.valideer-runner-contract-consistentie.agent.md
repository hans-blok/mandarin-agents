---
agent: agent-curator
intent: valideer-runner-contract-consistentie
versie: 1.0.0
digest: a51f
status: vers
---
# Agent-curator — Valideer Runner-Contract Consistentie

## Rolbeschrijving (korte samenvatting)

De agent-curator toetst of de vier parameter-lagen van een agent intern consistent zijn met elkaar: contract, prompt-frontmatter, runner (argparse) en tasks.json. De agent doet uitsluitend aanbevelingen voor correcties en past zelf niets aan.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `agent-curator.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Optionele parameters**:
- agent_naam: Naam van de agent die getoetst wordt (type: string, kebab-case, bijv. "agent-ontwerper"). Leeg = alle agents in value_stream_fase.
- value_stream_fase: Value stream en fase code (type: string, format: "{vs}.{fase}", bijv. "aeo.02", default: "aeo.02").

**Afgeleide informatie** (geëxtraheerd uit artefacten-structuur):
- runner-args: Uit argparse-definities in `{agent}.runner.py`
- contract-params: Uit `### Input` secties in `{agent}.{intent}.agent.md`
- task-args: Uit `args` arrays in `{fase}.{agent}.tasks.json`
- prompt-params: Uit `input_parameters` in YAML-frontmatter van `mandarin.{agent}.{intent}.prompt.md`

### Wat wordt getoetst

Per agent, per intent worden vier lagen vergeleken:

| Laag | Bron | Wat wordt gelezen |
|------|------|------------------|
| Contract | `agent-contracten/{agent}.{intent}.agent.md` | Verplichte + optionele parameters in `### Input` |
| Prompt | `prompts/mandarin.{agent}.{intent}.prompt.md` | `input_parameters` in YAML-frontmatter |
| Runner | `runner/{agent}.runner.py` | argparse `add_argument` definities per intent |
| Tasks | `tasks/{fase}.{agent}.tasks.json` | `args` array per task-definitie |

**Consistentieregels**:
1. Verplichte contract-parameters → moeten als runner-arg aanwezig zijn
2. Runner-args die als `-p key=value` doorgaan → moeten in het contract staan (verplicht of optioneel)
3. Prompt `input_parameters` → moet overeenkomen met contract-parameters
4. Task-args → moeten de runner-args weerspiegelen (geen params vragen die de runner niet kent)
5. Parameters die als "afgeleid" zijn gemarkeerd in het contract → mogen ontbreken in runner/tasks

### Output (wat komt eruit)

De agent-curator levert **uitsluitend aanbevelingen** — past zelf niets aan:
- **Consistentierapport**: `audit/runner-contract-consistentie-{yyyymmdd-HHmm}.rapport.md`
- Overzichtstabel: agent | intent | contract | prompt | runner | tasks | status
- Afwijkingtabel per bevinding: intent | parameter | aangetroffen in | ontbreekt in | ernst | aanbeveling
- Eindoordeel per agent: CONSISTENT / DEELS-CONSISTENT / INCONSISTENT

**VERPLICHT**: Rapport MOET worden weggeschreven naar de workspace.

**Formaat-normering**:
- Ernst-categorieën: KRITIEK (runner vraagt param die contract niet kent) / WAARSCHUWING (prompt niet synchroon met contract) / INFORMATIEF
- Eindoordeel: CONSISTENT / DEELS-CONSISTENT / INCONSISTENT

### Foutafhandeling

De agent-curator:
- meldt wanneer een runner geen duidelijke intent-scheiding heeft (monolithische runner zonder subcommands);
- meldt wanneer een contract geen `### Input` sectie heeft;
- **corrigeert zelf geen artefacten** — doet uitsluitend aanbevelingen;
- escaleert naar agent-engineer bij structurele runner-afwijkingen;
- escaleert naar agent-ontwerper bij ontbrekende of verouderde contracten.

### Governance

**Uitvoerend agent**: agent-curator  
**Intent-ID**: `aeo.02.agent-curator.valideer-runner-contract-consistentie`  
**Bronhouding**: Canon-gebonden  
**Traceerbaarheid**: Afgeleid van `agent-curator.agent-boundary.md`, volgt `agent-contract.template.md`
