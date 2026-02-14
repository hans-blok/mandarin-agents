# Agent Smeder — Maak Prompt Voor Agent

## Rolbeschrijving (korte samenvatting)

De Agent Smeder creëert minimale prompt-bestanden (.prompt.md) met YAML frontmatter voor elke intent, volgens het "Prompt First" principe en Convention over Configuration architectuur.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `{agent-naam}.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- boundary_file: Pad naar het boundary-bestand (type: string, relatief pad).
- agent_contract_file: Pad naar het agent-contract bestand (type: string, relatief pad, bijv. "artefacten/sfw/sfw.01.hypothese-vormer/agent-contracten/hypothese-vormer.formuleer-hypothese.agent.md").
- template_file: Template bestandsnaam voor prompt (type: string, bijv. "agent-prompt.template.md"). Locatie wordt afgeleid via conventie.

**Afgeleide informatie** (geëxtraheerd uit boundary en contract):
- agent_naam: Afgeleid uit boundary-bestandsnaam of contract metadata
- intent: Afgeleid uit agent_contract_file bestandsnaam
- value_stream_fase: Afgeleid uit boundary header (format: "{vs}.{fase}")

### Output (wat komt eruit)

De Agent Smeder levert:
- **Prompt-bestand** (`.prompt.md`) met minimale YAML frontmatter:
  ```yaml
  ---
  agent: mandarin.{agent-naam}
  intent: {intent-kortschrift}
  value_stream_fase: {vs}.{fase}
  
  bootstrap:
    script: scripts/bootstrap_canon_consult.py
  
  # Canon URL en grondslagen worden gelezen uit beleid-workspace.md
  # Agent-instructies staan in {agent-naam}.{intent}.agent.md
  # Charter wordt automatisch geladen: {agent-naam}.charter.md (zelfde folder)
  ---
  ```
- **Geen markdown body**: Prompt bevat ALLEEN metadata (SOLID Interface Segregation)
- Korte toelichting op architectuurkeuzes (Single Source of Truth, Convention over Configuration)

**Deliverable bestand**: `artefacten/{vs}/{vs}.{fase}.{agent}/prompts/mandarin.{agent}.{intent}.prompt.md`

**Naamgevingsconventie**: `mandarin.{agent-naam}.{intent-kortschrift}.prompt.md`

**Formaat-normering**: 
- Default formaat: **Markdown** (.md) met YAML frontmatter
- Body is leeg (agent-instructies in aparte .agent.md)
- YAML bevat minimale metadata (Principe Interface Segregation)
- Conform docs/README-PROMPT-ARCHITECTURE.md

### Foutafhandeling

De Agent Smeder:
- stopt wanneer boundary_file niet bestaat of niet te lezen is;
- stopt wanneer agent_contract_file niet bestaat (contract moet eerst bestaan);
- stopt wanneer agent_naam, intent of value_stream_fase niet af te leiden zijn;
- vraagt om verduidelijking wanneer een bestaand prompt-bestand al bestaat zonder versioning-instructie;
- escaleert naar agent-curator voor value_stream validatie;
- stopt wanneer de doelfolder `artefacten/{vs}/{vs}.{fase}.{agent}/prompts/` niet bestaat (moet eerst worden aangemaakt).

Prompt bevat GEEN charter_path, canon_url, of grondslagen (Convention over Configuration).

## Werkwijze

### Stappen
1. **Lees boundary**: Extraheer agent_naam, value_stream_fase uit header
2. **Lees agent-contract**: Extraheer intent uit metadata of bestandsnaam
3. **Lees template**: Gebruik agent-prompt.template.md als basis
4. **Vul metadata**: 
   - agent: mandarin.{agent_naam}
   - intent: {intent}
   - value_stream_fase: {vs}.{fase}
   - bootstrap: altijd scripts/bootstrap_canon_consult.py
5. **Minimaliseer content**: Body is leeg, alleen comments over architectuur
6. **Schrijf bestand**: Naar artefacten/{vs}/{vs}.{fase}.{agent}/prompts/mandarin.{agent}.{intent}.prompt.md
7. **Valideer naming**: Check bestandsnaam volgt conventie

### Kwaliteitsborging
- YAML frontmatter is valide (parseable door python-frontmatter)
- Alle verplichte velden aanwezig (agent, intent, value_stream_fase, bootstrap)
- Geen redundante velden (charter_path, canon_url, grondslagen)
- Bestandsnaam volgt conventie: mandarin.{agent}.{intent}.prompt.md
- Folder bestaat: artefacten/{vs}/{vs}.{fase}.{agent}/

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Prompt definieert extern contract
  - Principe 3 (Charter als Ecosysteem-Integrator): Prompt + agent.md + charter vormen geheel
  - Principe 5 (Evolutionaire Integriteit): Prompt-versioning via MAJOR.MINOR.PATCH systeem

**Architectuur-principes** (docs/README-PROMPT-ARCHITECTURE.md):
- **SOLID Interface Segregation**: Prompt bevat ALLEEN metadata voor run_prompt.py
- **Single Source of Truth**: Canon URL en grondslagen in beleid-workspace.md
- **Convention over Configuration**: Charter-pad en agent.md-pad worden afgeleid
- **Separation of Concerns**: Metadata (prompt) vs instructies (agent.md) vs context (charter)

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aeo
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: boundary_file, agent_contract_file, template_file
- ✓ Aangemaakte bestanden: mandarin.{agent}.{intent}.prompt.md
- ✓ Geen gewijzigde bestanden (prompt is nieuw, of wordt geversioned)

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → agent-curator: voor value_stream validatie of folder-aanmaak
- → engineer-steward: NIET (geen scripting nodig, pure metadata)
- STOP: bij bestaand prompt zonder versioning-instructie, bij ontbrekende folder, bij ongeldige naming

---

## Metadata

**Intent-ID**: `aeo.02.agent-smeder.leg-vast-agent-prompt`  
**Versie**: 1.0.0  
**Value Stream**: Agent Enablement Orchestration (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**: 
- Inhoudelijk: ecosysteem-normerend, structuurrealiserend
- Inzet: value-stream-specifiek
- Vorm: vormvast
- Werking: inhoudelijk
