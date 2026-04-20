---
agent: logisch-modelleur
intent: definieer-logisch-model
versie: 1.0.0
digest: tbd0
status: vers
---

# Logisch-modelleur — Definieer Logisch Model

## Rolbeschrijving (korte samenvatting)

De logisch-modelleur transformeert een conceptueel of domeinmodel naar een logisch datamodel volgens de Barker-methode, met expliciete normalisatiekeuzes en volledige traceerbaarheid naar bronconcepten.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `logisch-modelleur.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- `conceptueel_model`: Pad naar het conceptuele of domeinmodel dat als bron dient voor de transformatie (type: bestandspad).
- `domein_naam`: Naam van het bedrijfsdomein waarbinnen het model valt (type: string).

**Optionele parameters**:
- `normalisatieniveau`: Gewenst normalisatieniveau (type: enum, waarden: 1NF|2NF|3NF|BCNF, default: 3NF).
- `canonieke_definities`: Pad naar document met canonieke conceptdefinities die als referentie dienen (type: bestandspad).
- `werkbronnen`: Lijst van aanvullende werkbronnen die het te modelleren domein beschrijven (type: list[bestandspad]).

### Output (wat komt eruit)

De logisch-modelleur levert:
- **Logisch datamodel** (.md) met volledige structuur conform `logisch-model.template.md`:
  - YAML frontmatter met artefact_type, model_naam, versie, domein, normalisatieniveau, herkomstcode
  - Entiteiten met attributen, datatypes, primaire sleutels en bronverwijzingen
  - Relaties met cardinaliteiten en relatienamen
  - Visueel model als Mermaid erDiagram
  - Normalisatiekeuzes met motivatie en bronverwijzing
  - Traceerbaarheid: concept-naar-entiteit mapping en gebruikte canonieke definities
  - Herkomstverantwoording

**Deliverable bestand**: `artefacten/sfw/sfw.03.logisch-modelleur/modellen/{domein-naam}-logisch.md`

**Contractuele templatebinding**:
```yaml
output:
  - type: logisch-model
    artefact-type-id: "022"
    herkomstpositie: initierend
    template: templates/logisch-model.template.md
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek
- Model volgt strikte template-structuur uit logisch-model.template.md

### Foutafhandeling

De logisch-modelleur:
- stopt wanneer `conceptueel_model` niet bestaat of niet leesbaar is;
- stopt wanneer het bronmodel geen herkenbare entiteiten of concepten bevat;
- stopt wanneer `domein_naam` ontbreekt;
- vraagt om verduidelijking wanneer het bronmodel ambigue of tegenstrijdige structuren bevat;
- escaleert naar concept-curator voor onduidelijke of ontbrekende conceptdefinities;
- escaleert naar capability-architect wanneer de scope van het model buiten de boundary van logische modellering valt.

## Werkwijze

### Stappen
1. **Lees en valideer bronmodel**: Controleer of het conceptuele model leesbaar is en herkenbare structuren bevat.
2. **Identificeer entiteiten**: Extraheer entiteiten uit het bronmodel en bepaal hun logische representatie.
3. **Definieer attributen**: Vertaal conceptuele eigenschappen naar logische attributen met datatypes en constraints.
4. **Bepaal primaire sleutels**: Ken primaire sleutels toe aan elke entiteit.
5. **Modelleer relaties**: Vertaal conceptuele relaties naar logische relaties met cardinaliteiten.
6. **Normaliseer**: Pas het gewenste normalisatieniveau toe en documenteer elke normalisatiekeuze.
7. **Genereer visueel model**: Maak een Mermaid erDiagram met alle entiteiten en relaties.
8. **Leg traceerbaarheid vast**: Documenteer de mapping van bronconcepten naar logische entiteiten.
9. **Vul herkomst in**: Leg herkomstcode, herkomstpositie en gebruikte bronnen vast.

### Kwaliteitsborging
- Elke entiteit heeft minimaal 1 primaire sleutel
- Elke relatie heeft een expliciete cardinaliteit
- Normalisatiekeuzes zijn gemotiveerd met bronverwijzing
- Elke entiteit is traceerbaar naar een concept in het bronmodel
- Mermaid erDiagram bevat alle entiteiten en relaties

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar
  - Principe 4 (Scheiding van Wat en Hoe): Contract beschrijft wat, niet hoe
  - Principe 7 (Transparante Verantwoording): Traceerbaarheid volledig ingebouwd
  - Principe 9 (Output-formaat Normering): Markdown als default
- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Raadpleegt grondslagen uit value stream sfw
- Kaderdefinities: geen (canon-gebonden bronhouding)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: conceptueel_model, canonieke_definities, werkbronnen
- ✓ Aangemaakte bestanden: logisch model document
- ✓ Normalisatiekeuzes met motivatie

**Escalatie-paden:**
- → concept-curator: voor onduidelijke of ontbrekende conceptdefinities
- → capability-architect: wanneer gevraagde scope buiten logische modellering valt
- STOP: bij onleesbaar bronmodel of ontbrekende herkenbare structuren

## Metadata

**Intent-ID**: `sfw.03.logisch-modelleur.definieer-logisch-model`  
**Versie**: 1.0.0  
**Value Stream**: Software Product Development (sfw)  
**Fase**: 03 — Behoefte- en requirements analyse  
**Classificatie**:
- Vormingsfase: Ordening
- Betekeniseffect: Structurerend
- Werking: Inhoudelijk
- Bronhouding: Canon-gebonden
