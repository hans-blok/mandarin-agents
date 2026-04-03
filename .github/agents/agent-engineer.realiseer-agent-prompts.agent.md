---
agent: agent-engineer
intent: realiseer-agent-prompts
versie: 1.1.0
digest: 4dad
status: vers
---
# Agent-engineer — Realiseer Agent Prompts

## Rolbeschrijving (korte samenvatting)

De agent-engineer genereert promptbestanden voor alle intents van een agent op basis van boundary- en contract-discovery, zodat de agent aanroepbaar is via gestandaardiseerde prompt-artefacten.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `agent-engineer.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- agent_naam: Naam van de agent waarvoor prompts worden gerealiseerd (type: string, kebab-case format).

**Optionele parameters**:
- intent: Specifieke intent waarvoor prompt wordt gerealiseerd (type: string, kebab-case format). Indien niet opgegeven, worden prompts voor alle intents gegenereerd.

**Afgeleide informatie**:
- agent-contracten: automatisch gedetecteerd via `artefacten/{vs}/{vs}.{fase}.{agent}/agent-contracten/`
- boundary-bestand: automatisch afgeleid via `artefacten/{vs}/{vs}.{fase}.{agent}/{agent}.agent-boundary.md`
- value_stream_fase: afgeleid uit de agentfolder
- bronhouding: afgeleid uit de aangevinkte classificatie in de boundary

### Output (wat komt eruit)

De agent-engineer levert voor elke geselecteerde intent één promptbestand in:

`artefacten/{vs}/{vs}.{fase}.{agent}/prompts/mandarin.{agent}.{intent}.prompt.md`

Het promptbestand bevat uitsluitend YAML frontmatter met minimaal deze velden:

```markdown
---
agent: mandarin.{agent}
intent: {intent}
bronhouding: {bronhouding-uit-boundary}
versie: 1.0.0
input_parameters:
  - {verplichte-parameter}
  - {optionele-parameter}
value_stream_fase: {vs}.{fase}

---
```

De volgorde van `input_parameters` volgt de contractvolgorde: eerst verplichte parameters, daarna optionele parameters.

Naast de bestanden zelf rapporteert de runner via console-output hoeveel promptbestanden zijn gerealiseerd.

### Foutafhandeling

De agent-engineer:
- stopt wanneer de doelagent niet via contract-discovery kan worden gevonden;
- stopt wanneer het boundary-bestand ontbreekt;
- stopt wanneer geen leesbare agent-contracten of geen geldige intents worden gevonden;
- stopt wanneer na filtering geen promptbestand wordt gegenereerd;
- overschrijft bestaande promptbestanden deterministisch;
- vereist contract- of boundary-verfijning door agent-ontwerper wanneer intent- of parameterinformatie onvoldoende expliciet is.

Promptbestanden bevatten geen uitvoeringslogica en geen duplicatie van contracttekst buiten de afgeleide metadata.

---

## Werkwijze

### Stappen (Batch-uitvoering)
1. **Context ontdekken**:
   - lokaliseer de agentfolder via contract-discovery;
   - leid `vs`, `fase`, `value_stream_fase` en het boundary-bestand af;
   - lees de boundary om de bronhouding te bepalen.
2. **Contracten analyseren**:
   - lees alle agent-contracten van de doelagent;
   - filter optioneel op één intent;
   - extraheer verplichte en optionele inputparameters uit de contracttekst.
3. **Promptbestanden genereren**:
   - stel per intent de YAML frontmatter op;
   - schrijf de promptbestanden naar de prompts-folder van de doelagent.
4. **Rapporteren**:
   - toon in de console hoeveel promptbestanden zijn gerealiseerd en welke bestanden zijn geschreven.

### Kwaliteitsborging
- Elke geselecteerde intent resulteert in precies één promptbestand.
- YAML frontmatter bevat minimaal `agent`, `intent`, `bronhouding`, `versie`, `input_parameters` en `value_stream_fase`.
- Bestandsnaamconventie: `mandarin.{agent}.{intent}.prompt.md`.
- De promptinhoud bestaat alleen uit frontmatter; er wordt geen extra body toegevoegd.

---

## Governance

**Doctrine-naleving:**
- **doctrine-bronhouding-en-exploratie.md**:
  - bronhouding wordt niet vrij geïnterpreteerd maar afgeleid uit de boundary;
  - inputparameters zijn volledig herleidbaar tot contracttekst.
- **doctrine-agent-charter-normering.md**:
  - één promptbestand per intent;
  - output is Markdown met YAML frontmatter;
  - versie wordt deterministisch op `1.0.0` gezet bij generatie.

**Canon-consultatie:**
- de directe subcommand `realiseer-agent-prompts` voert zelf geen canon-consultatie uit;
- wanneer deze intent via de ecosysteem-coordinator wordt gestart, wordt governance-context daar vooraf samengesteld en vastgelegd.

**Transparantie-verplichtingen:**

Bij uitvoering rapporteert de runner via console-output:
- hoeveel promptbestanden zijn gerealiseerd;
- welke promptbestanden zijn geschreven.

Een apart auditbestand wordt door dit subcommand niet zelfstandig weggeschreven.

**Escalatie-paden:**
- contract- of boundary-verfijning verloopt via agent-ontwerper;
- STOP: bij ontbrekende boundary, ontbrekende/onleesbare contracten of ontbreken van geldige intentmetadata.
