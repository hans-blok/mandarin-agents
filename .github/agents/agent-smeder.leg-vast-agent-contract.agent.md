# Agent Smeder — Beschrijf Agent Contract

## Rolbeschrijving (korte samenvatting)

De Agent Smeder schrijft voor elke intent uit de boundary een gedetailleerd agent-contract (.agent.md) dat het externe contract van de agent functioneel beschrijft met input, output, foutafhandeling en governance.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `{agent-naam}.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- boundary_file: Pad naar het boundary-bestand (type: string, relatief pad).
- template_file: Template bestandsnaam voor agent-contract (type: string, bijv. "agent-contract-intent.template.md"). Locatie wordt afgeleid via conventie.

**Afgeleide informatie** (geëxtraheerd uit boundary):
- agent_naam: Afgeleid uit boundary-bestandsnaam of header
- value_stream_fase: Afgeleid uit boundary header (format: "{vs}.{fase}")
- intents: Alle intents uit sectie "Voorstellen agent contracten" in boundary

**Optionele parameters**:
- referenties: Lijst van referentie-documenten voor intent-definitie (type: string, komma-gescheiden paden).

### Output (wat komt eruit)

De Agent Smeder levert:
- **Agent-contract bestand** (`.agent.md`) met volledige contract-beschrijving:
  - Rolbeschrijving: Wat doet de agent bij deze specifieke intent
  - Input contract: Verplichte en optionele parameters met types en constraints
  - Output contract: Deliverables, bestandsformaten, outputlocaties
  - Foutafhandeling: Stop-condities en escalatiepaden
  - Governance: Doctrine-naleving, transparantie, canon-consultatie
  - Metadata: Intent-ID, versie, classificatie
- Korte toelichting op gemaakte ontwerpkeuzes

**Deliverable bestand**: `artefacten/{vs}/{vs}.{fase}.{agent}/agent-contracten/{agent}.{intent}.agent.md`

**Outputformaat** (standaard structuur per template):
```markdown
# {Agent} — {Intent Naam}

## Rolbeschrijving (korte samenvatting)
{1-2 zinnen specifiek voor deze intent}

## Contract
### Input (wat gaat erin)
**Verplichte parameters**: ...
**Optionele parameters**: ...

### Output (wat komt eruit)
**Deliverables**: ...
**Outputlocaties**: ...
**Formaat**: ...

### Foutafhandeling
{Stop-condities en escalaties}

## Governance
{Doctrine-naleving, transparantie, canon}

## Metadata
{Intent-ID, versie, classificatie}
```

**Formaat-normering**: 
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek
- Markdown bevat code blocks voor voorbeelden

### Foutafhandeling

De Agent Smeder:
- stopt wanneer boundary_file niet bestaat of niet te lezen is;
- stopt wanneer boundary geen "Voorstellen agent contracten" sectie bevat;
- stopt wanneer agent_naam of value_stream_fase niet uit boundary af te leiden zijn;
- vraagt om verduidelijking wanneer input/output specificaties onduidelijk zijn in boundary;
- escaleert naar agent-curator voor boundary-verfijning bij ontbrekende informatie;
- escaleert naar constitutioneel-auteur voor doctrine-interpretatie bij onduidelijkheden.

Contract-beschrijving bevat GEEN implementatie-details, alleen extern observeerbaar gedrag.

**Conventie**: Voor elk intent in de boundary wordt een apart agent-contract gegenereerd.

## Werkwijze

### Stappen
1. **Lees boundary**: Extraheer agent_naam, value_stream_fase uit header en alle intents uit "Voorstellen agent contracten" sectie
2. **Per intent**: Verwerk elk intent uit de boundary afzonderlijk
3. **Lees template**: Gebruik template als structuur-basis
4. **Analyseer input/output**: Bepaal welke parameters nodig zijn op basis van intent-doel uit boundary
5. **Definieer contract**: Specificeer verplichte vs optionele parameters met types
6. **Formuleer foutafhandeling**: Bepaal stop-condities en escalatiepaden
7. **Voeg governance toe**: Doctrine-referenties, transparantie-verplichtingen
8. **Vul metadata**: Intent-ID ({vs}.{fase}.{agent}.{intent}), classificatie uit boundary, start versie bij 1.0.0
9. **Schrijf bestand**: Naar agent-contracten/{agent}.{intent}.agent.md
10. **Valideer compleetheid**: Check template-checklist uit agent-contract-intent.template.md

### Kwaliteitsborging
- Input contract heeft minimaal 2 verplichte parameters
- Output contract specificeert concrete bestandspaden
- Foutafhandeling bevat minimaal 3 stop-condities
- Governance-sectie verwijst naar relevante doctrine-principes
- Metadata bevat correcte classificatie uit boundary

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar, geen implementatie
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén contract per intent
  - Principe 5 (Evolutionaire Integriteit): Versioning ingebouwd (start bij 1.0.0)
  - Principe 7 (Transparante Verantwoording): Transparantie-verplichtingen expliciet
  - Principe 9 (Output-formaat Normering): Markdown als default

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aeo
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: boundary_file, template_file, eventuele referenties
- ✓ Aangemaakte bestanden: {agent}.{intent}.agent.md
- ✓ Geen gewijzigde bestanden (contract is nieuw, of wordt geversioned)

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → agent-curator: voor boundary-verfijning of onduidelijke intent-beschrijving
- → constitutioneel-auteur: voor doctrine-interpretatie vragen
- → engineer-steward: NIET (dit is geen code-schrijven maar contract-ontwerp)
- STOP: bij ontbrekende intent in boundary, bij te vage intent-omschrijving die niet te vertalen is naar contract

---

## Metadata

**Intent-ID**: `aeo.02.agent-smeder.leg-vast-agent-contract`  
**Versie**: 1.0.0  
**Value Stream**: Agent Enablement Orchestration (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**: 
- Inhoudelijk: ecosysteem-normerend, structuurrealiserend
- Inzet: value-stream-specifiek
- Vorm: vormvast
- Werking: inhoudelijk
