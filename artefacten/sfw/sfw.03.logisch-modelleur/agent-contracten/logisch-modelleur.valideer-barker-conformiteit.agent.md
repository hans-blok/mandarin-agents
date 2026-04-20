---
agent: logisch-modelleur
intent: valideer-barker-conformiteit
versie: 1.0.0
digest: tbd0
status: vers
---

# Logisch-modelleur — Valideer Barker-conformiteit

## Rolbeschrijving (korte samenvatting)

De logisch-modelleur valideert een bestaand logisch datamodel tegen de regels en principes van de Barker-methode en levert een validatierapport met bevindingen, conclusie en aanbevelingen.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `logisch-modelleur.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- `logisch_model`: Pad naar het logische datamodel dat gevalideerd moet worden (type: bestandspad).

**Optionele parameters**:
- `barker_regels`: Pad naar document met specifieke Barker-regels die getoetst moeten worden (type: bestandspad, default: standaard regelset uit canon).
- `scope_entiteiten`: Lijst van specifieke entiteiten die gevalideerd moeten worden; als leeg, worden alle entiteiten gevalideerd (type: list[string]).

### Output (wat komt eruit)

De logisch-modelleur levert:
- **Barker validatierapport** (.md) conform `barker-validatierapport.template.md`:
  - YAML frontmatter met artefact_type, gevalideerd_model, validatie_resultaat, herkomstcode
  - Toegepaste Barker-regels: lijst van getoetste regels met status per regel
  - Bevindingen: gecategoriseerd (kritiek/niet-kritiek/positief) met regel-referentie en aanbeveling
  - Detail per entiteit: aspect-niveau validatie (naamgeving, primaire sleutel, attributen, relaties)
  - Relatie-analyse: cardinaliteit en naamgeving per relatie
  - Normalisatie-check: toetsing op 1NF, 2NF, 3NF
  - Conclusie: conform/niet-conform/conditioneel-conform met actiepunten

**Deliverable bestand**: `artefacten/sfw/sfw.03.logisch-modelleur/validaties/{model-naam}-barker-validatie.md`

**Contractuele templatebinding**:
```yaml
output:
  - type: barker-validatierapport
    artefact-type-id: "021"
    herkomstpositie: voortbouwend
    template: templates/barker-validatierapport.template.md
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Rapport volgt strikte template-structuur uit barker-validatierapport.template.md

### Foutafhandeling

De logisch-modelleur:
- stopt wanneer `logisch_model` niet bestaat of niet leesbaar is;
- stopt wanneer het model geen herkenbare entiteiten of relaties bevat;
- stopt wanneer gevraagde `scope_entiteiten` niet voorkomen in het model;
- vraagt om verduidelijking wanneer Barker-regels onderling conflicteren of interpretatieruimte laten;
- escaleert naar capability-architect wanneer het model structuren bevat die buiten logische modellering vallen.

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar
  - Principe 4 (Scheiding van Wat en Hoe): Contract beschrijft wat, niet hoe
  - Principe 7 (Transparante Verantwoording): Bevindingen zijn traceerbaar naar regels
  - Principe 9 (Output-formaat Normering): Markdown als default
- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Raadpleegt grondslagen uit value stream sfw
- Kaderdefinities: geen (canon-gebonden bronhouding)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: logisch_model, barker_regels
- ✓ Aangemaakte bestanden: validatierapport
- ✓ Aantal getoetste regels, bevindingen en conclusie

**Escalatie-paden:**
- → capability-architect: wanneer modelstructuren buiten logische modellering vallen
- STOP: bij onleesbaar model of ontbrekende herkenbare structuren

## Metadata

**Intent-ID**: `sfw.03.logisch-modelleur.valideer-barker-conformiteit`  
**Versie**: 1.0.0  
**Value Stream**: Software Product Development (sfw)  
**Fase**: 03 — Behoefte- en requirements analyse  
**Classificatie**:
- Vormingsfase: Ordening
- Betekeniseffect: Structurerend
- Werking: Inhoudelijk
- Bronhouding: Canon-gebonden
