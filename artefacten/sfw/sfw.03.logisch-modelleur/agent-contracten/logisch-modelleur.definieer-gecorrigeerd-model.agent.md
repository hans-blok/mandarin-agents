---
agent: logisch-modelleur
intent: definieer-gecorrigeerd-model
versie: 1.0.0
digest: tbd0
status: vers
---

# Logisch-modelleur — Definieer Gecorrigeerd Model

## Rolbeschrijving (korte samenvatting)

De logisch-modelleur corrigeert een bestaand logisch datamodel op basis van een validatierapport of expliciete correctie-instructies, waarbij alle wijzigingen traceerbaar worden vastgelegd en het gecorrigeerde model opnieuw voldoet aan de Barker-methode.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `logisch-modelleur.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- `bronmodel`: Pad naar het bestaande logische datamodel dat gecorrigeerd moet worden (type: bestandspad).
- `correctie_instructies`: Pad naar het validatierapport of document met expliciete correctie-instructies (type: bestandspad).

**Optionele parameters**:
- `canonieke_definities`: Pad naar document met canonieke conceptdefinities die als referentie dienen (type: bestandspad).
- `modelleringsbeslissingen`: Paden naar relevante modelleringsbeslissingen die bij de correctie gerespecteerd moeten worden (type: list[bestandspad]).

### Output (wat komt eruit)

De logisch-modelleur levert:
- **Gecorrigeerd logisch datamodel** (.md) met dezelfde structuur als het bronmodel, conform `logisch-model.template.md`:
  - Alle correcties doorgevoerd op entiteiten, attributen en relaties
  - Bijgewerkt Mermaid erDiagram
  - Bijgewerkte normalisatiekeuzes indien van toepassing
  - Wijzigingsoverzicht: expliciete lijst van doorgevoerde correcties met verwijzing naar correctie-instructies
  - Herkomstverantwoording met herkomstpositie "voortbouwend"

**Deliverable bestand**: `artefacten/sfw/sfw.03.logisch-modelleur/modellen/{domein-naam}-logisch.md` (overschrijft het bronmodel)

**Contractuele templatebinding**:
```yaml
output:
  - type: logisch-model
    artefact-type-id: "022"
    herkomstpositie: voortbouwend
    template: templates/logisch-model.template.md
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Gecorrigeerd model volgt dezelfde template-structuur als het origineel

### Foutafhandeling

De logisch-modelleur:
- stopt wanneer `bronmodel` niet bestaat of niet leesbaar is;
- stopt wanneer `correctie_instructies` niet bestaat of geen herkenbare correcties bevat;
- stopt wanneer correctie-instructies conflicteren met elkaar;
- vraagt om verduidelijking wanneer correctie-instructies ambigu zijn of meerdere interpretaties toelaten;
- escaleert naar concept-curator wanneer correcties conceptuele definities raken die buiten scope vallen;
- escaleert naar capability-architect wanneer correcties de scope van logische modellering overschrijden (bijv. fysieke implementatiekeuzes).

## Werkwijze

### Stappen
1. **Lees bronmodel**: Laad het bestaande logische datamodel.
2. **Analyseer correctie-instructies**: Identificeer alle gevraagde correcties uit het validatierapport of instructiedocument.
3. **Valideer haalbaarheid**: Controleer of correcties binnen de scope van logische modellering vallen en niet conflicteren.
4. **Voer correcties door**: Pas entiteiten, attributen, relaties en normalisatiekeuzes aan.
5. **Werk visueel model bij**: Genereer bijgewerkt Mermaid erDiagram.
6. **Documenteer wijzigingen**: Leg alle doorgevoerde correcties vast met verwijzing naar bron.
7. **Vul herkomst bij**: Herkomstpositie = voortbouwend, verwijzing naar bronmodel en correctie-instructies.

### Kwaliteitsborging
- Elke correctie is traceerbaar naar een bevinding in het correctie-document
- Gecorrigeerd model voldoet nog steeds aan het opgegeven normalisatieniveau
- Geen correcties doorgevoerd die buiten de correctie-instructies vallen
- Wijzigingsoverzicht is volledig en correspondeert met het verschil tussen bron en resultaat

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar
  - Principe 4 (Scheiding van Wat en Hoe): Contract beschrijft wat, niet hoe
  - Principe 7 (Transparante Verantwoording): Wijzigingsoverzicht verplicht
  - Principe 9 (Output-formaat Normering): Markdown als default
- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Raadpleegt grondslagen uit value stream sfw
- Kaderdefinities: geen (canon-gebonden bronhouding)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: bronmodel, correctie_instructies, canonieke_definities, modelleringsbeslissingen
- ✓ Gewijzigde bestanden: gecorrigeerd logisch model
- ✓ Doorgevoerde correcties met verwijzing naar bron

**Escalatie-paden:**
- → concept-curator: wanneer correcties conceptuele definities raken
- → capability-architect: wanneer correcties buiten logische modellering vallen
- STOP: bij conflicterende correctie-instructies of onleesbaar bronmodel

## Metadata

**Intent-ID**: `sfw.03.logisch-modelleur.definieer-gecorrigeerd-model`  
**Versie**: 1.0.0  
**Value Stream**: Software Product Development (sfw)  
**Fase**: 03 — Behoefte- en requirements analyse  
**Classificatie**:
- Vormingsfase: Ordening
- Betekeniseffect: Structurerend
- Werking: Inhoudelijk
- Bronhouding: Canon-gebonden
