---
agent: logisch-modelleur
intent: beschrijf-modelleringsbeslissing
versie: 1.0.0
digest: tbd0
status: vers
---

# Logisch-modelleur — Beschrijf Modelleringsbeslissing

## Rolbeschrijving (korte samenvatting)

De logisch-modelleur documenteert een specifieke modelleringskeuze met volledige traceerbaarheid naar bronnen, motivatie, overwogen alternatieven en impact op het logisch model.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `logisch-modelleur.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- `model_naam`: Naam van het logische model waarop de beslissing betrekking heeft (type: string).
- `onderwerp`: Kort onderwerp van de modelleringsbeslissing, maximaal 50 tekens (type: string).

**Optionele parameters**:
- `logisch_model`: Pad naar het logische datamodel waarbinnen de beslissing speelt (type: bestandspad).
- `context_beschrijving`: Aanvullende contextbeschrijving voor de beslissing (type: string).
- `canonieke_definities`: Pad naar document met canonieke conceptdefinities die relevant zijn (type: bestandspad).

### Output (wat komt eruit)

De logisch-modelleur levert:
- **Modelleringsbeslissing** (.md) conform `modelleringsbeslissing.template.md`:
  - YAML frontmatter met artefact_type, beslissing_id, model, onderwerp, status, herkomstcode
  - Context: situatie en aanleiding met relevante bronnen
  - Probleemstelling: kernvraag met constraints en kwaliteitseisen
  - Beslissing: gekozen oplossing met rationale en impactanalyse
  - Alternatieven: overwogen alternatieven met voor-/nadelen en reden voor afwijzing
  - Bronverwijzingen: canonieke en domeinbronnen
  - Gevolgen: directe gevolgen, afhankelijkheden en risico's
  - Herkomstverantwoording

**Deliverable bestand**: `artefacten/sfw/sfw.03.logisch-modelleur/beslissingen/{model-naam}-{beslissing-id}.md`

**Contractuele templatebinding**:
```yaml
output:
  - type: modelleringsbeslissing
    artefact-type-id: "023"
    herkomstpositie: initierend
    template: templates/modelleringsbeslissing.template.md
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Beslissing volgt strikte template-structuur uit modelleringsbeslissing.template.md

### Foutafhandeling

De logisch-modelleur:
- stopt wanneer `model_naam` of `onderwerp` ontbreekt;
- stopt wanneer het onderwerp niet relateert aan logische modellering (bijv. fysieke implementatiekeuzes);
- vraagt om verduidelijking wanneer het onderwerp te breed of te vaag is om een concrete beslissing over te documenteren;
- escaleert naar concept-curator wanneer de beslissing conceptuele definities raakt die buiten logische modellering vallen;
- escaleert naar capability-architect wanneer de beslissing grensgevallen raakt met fysiek modelleren of andere domeinen.

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar
  - Principe 4 (Scheiding van Wat en Hoe): Contract beschrijft wat, niet hoe
  - Principe 7 (Transparante Verantwoording): Beslissing is volledig traceerbaar
  - Principe 9 (Output-formaat Normering): Markdown als default
- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Raadpleegt grondslagen uit value stream sfw
- Kaderdefinities: geen (canon-gebonden bronhouding)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: logisch_model, canonieke_definities
- ✓ Aangemaakte bestanden: modelleringsbeslissing document
- ✓ Beslissing-ID, gekozen oplossing en alternatieven

**Escalatie-paden:**
- → concept-curator: wanneer de beslissing conceptuele definities raakt
- → capability-architect: bij grensgevallen met fysiek modelleren of andere domeinen
- STOP: bij onderwerp buiten scope van logische modellering

## Metadata

**Intent-ID**: `sfw.03.logisch-modelleur.beschrijf-modelleringsbeslissing`  
**Versie**: 1.0.0  
**Value Stream**: Software Product Development (sfw)  
**Fase**: 03 — Behoefte- en requirements analyse  
**Classificatie**:
- Vormingsfase: Ordening
- Betekeniseffect: Structurerend
- Werking: Inhoudelijk
- Bronhouding: Canon-gebonden
