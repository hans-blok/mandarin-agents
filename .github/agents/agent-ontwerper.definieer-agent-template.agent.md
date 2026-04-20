---
agent: agent-ontwerper
intent: definieer-agent-template
intent-id: aeo.02.agent-ontwerper.03
versie: 1.0.0
digest: 286a
status: vers
---
# Agent-ontwerper — Definieer Agent Template

## Rolbeschrijving (korte samenvatting)

De Agent-ontwerper creëert context-specifieke output templates voor een agent, waarbij de structuur van elk template de verwachte output-structuur beschrijft en is afgeleid uit de capability boundary (bijv. ArchiMate-structuren voor architecten, document-structuren voor schrijvende agents).

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `agent-ontwerper.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- agent_naam: Naam van de agent waarvoor templates worden gedefinieerd (type: string, kebab-case).


**Optionele parameters**:
- file_naam_inspiratie: de gebruiker kan een file plaatsen in de folder temp. Deze dient als inspiratie voor de agent-ontwerper bij het vastleggen van het template (type: string, kebab-case).
- intent: standaard wordt voor alle intents in oorstellen agent contracten" sectie in boundary een template aangemaakt. Wanneer deze parameter is opgegeven, wordt alleen voor deze intent een template gegenereerd. (type: string, exact match met intent-naam in boundary)

**Afgeleide informatie** (automatisch gedetecteerd):
- value_stream_fase: Gedetecteerd uit folder-patroon `artefacten/{vs}/{vs}.{fase}.{agent-naam}/`
- boundary_file: Automatisch afgeleid uit `agent_naam` en gedetecteerde folder-structuur

**Afgeleide informatie** (geëxtraheerd uit boundary):
- intent_beschrijving: Uit "Voorstellen agent contracten" sectie in boundary

### Output (wat komt eruit)

De Agent-ontwerper levert:
- **Template document** met gestructureerde outputspecificatie:
  - YAML frontmatter: agent, template_naam, versie, output_type
  - Template-beschrijving: Doel en gebruik van template
  - Structuur-specificatie: Verplichte en optionele secties
  - Placeholder-definitie: Welke variabelen ingevuld moeten worden
  - Voorbeeld-output: Concrete voorbeeldinvulling van template
  - Validatie-criteria: Hoe te checken of output voldoet aan template
  - Gebruiksinstructies: Hoe agent dit template gebruikt
- Korte toelichting op template-keuzes en structuur-beslissingen

**Deliverable bestand**: `artefacten/{vs}/{vs}.{fase}.{agent}/templates/{template-naam}.template.md`

**Contractuele templatebinding**:
```yaml
output:
  - type: agent-template-document
    herkomstpositie: initiërend
    template: ~
```

**VERPLICHT**: Het bestand MOET worden weggeschreven naar de workspace (niet alleen voorgesteld).

**Outputformaat** (template-specifieke structuur):
```markdown
---
agent: {agent-naam}
template_naam: {template-naam}
versie: 1.0.0
output_type: {document/data-structure/diagram/configuration}
doel: {beschrijving waarvoor template dient}
---

# Template: {Template Titel}

## Doel en gebruik

{Beschrijf waarvoor dit template gebruikt wordt, door welke intents, en wat het resultaat is.}

## Structuur

Dit template beschrijft de OUTPUT structuur. Het gegenereerde artefact krijgt de volgende structuur:

```markdown
---
{verplichte frontmatter velden}
---

# {Hoofdtitel}

## {Sectie 1}
{Beschrijving wat in deze sectie staat}
{Placeholders: <placeholder-naam>, <andere-placeholder>}

## {Sectie 2}
{Beschrijving wat in deze sectie staat}

[...rest van structuur...]
```

## Placeholders

| Placeholder | Type | Beschrijving | Verplicht |
|-------------|------|--------------|-----------|
| `<placeholder-1>` | string | {wat hier ingevuld wordt} | Ja |
| `<placeholder-2>` | list | {wat hier ingevuld wordt} | Nee |
| `<placeholder-3>` | string | {wat hier ingevuld wordt} | Ja |

## Validatie-criteria

Een valide output volgens dit template:
- ✓ {criterium 1}
- ✓ {criterium 2}
- ✓ {criterium 3}

## Voorbeeld-output

{Concrete voorbeeld-invulling van het template}

## Gebruiksinstructies

Voor agents die dit template gebruiken:
1. {stap 1}
2. {stap 2}
3. {stap 3}

## Versiebeheer

| Versie | Datum | Wijziging |
|--------|-------|-----------|
| 1.0.0 | {datum} | Initiële template voor {agent-naam} |

---

**Template-categorie**: {Agent-specifiek/Generiek/Domein-specifiek}
**Gebruikt door intents**: {lijst van intents die dit template gebruiken}
```

**Formaat-normering**: 
- Default formaat: **Markdown** (.md) voor template-documenten
- Templates beschrijven output-structuur, niet implementatie
- Templates zijn agent-specifiek (in agent folder) of generiek (in shared folder)
- `template: ~` is expliciet omdat deze intent zelf template-documenten definieert en de outputvorm in dit contract al volledig is gespecificeerd

### Foutafhandeling

De Agent-ontwerper:
- stopt wanneer boundary_file niet bestaat of niet te lezen is;
- stopt wanneer agent_naam ontbreekt, of wanneer value_stream_fase niet afleidbaar is uit folder-structuur of boundary;
- stopt wanneer output_type niet herkend wordt (moet zijn: document, data-structure, diagram, configuration);
- vraagt om verduidelijking wanneer output-beschrijving in boundary te vaag is om template-structuur te bepalen;
- vraagt om voorbeeldstructuur wanneer output_type onduidelijk of complex is;
- escaleert naar capability-architect voor boundary-verfijning bij ontbrekende output-specificatie;
- escaleert naar domein-expert (indien beschikbaar) voor domein-specifieke template-structuren;
- STOP: bij onvoldoende informatie om gestructureerd template te definiëren met minimaal 3 verplichte secties.

**Template is structuur-beschrijving**: bevat GEEN implementatie-logica, alleen structuur en placeholders.

---

## Werkwijze

### Stappen
1. **Analyseer boundary**: Lees boundary_file, focus op "Welke outputs levert de agent?" sectie.
2. **Bepaal output-type**: Classificeer output als document, data-structure, diagram of configuration.
3. **Raadpleeg domein**: Begrijp domein-specifieke structureisen (bijv. ArchiMate voor architecten, wetenschappelijk artikel voor onderzoekers).
4. **Raadpleeg referenties**: Als referentie_templates opgegeven, lees deze voor structuur-patronen.
5. **Ontwerp structuur**: Bepaal verplichte en optionele secties op basis van domein en output-type.
6. **Definieer placeholders**: Lijst alle variabelen die ingevuld moeten worden (met type en verplicht/optioneel).
7. **Formuleer validatie-criteria**: Minimaal 3 criteria om te checken of output voldoet aan template.
8. **Creëer voorbeeld**: Schrijf concrete voorbeeld-invulling om template te illustreren.
9. **Schrijf gebruiksinstructies**: Leg uit hoe agent dit template gebruikt (in 3-5 stappen).
10. **Link aan intents**: Bepaal welke intents dit template gebruiken (uit boundary of charter).
11. **Schrijf template**: Genereer volledig template-bestand en schrijf weg naar correct pad.
12. **Valideer compleetheid**: Check minimale vereisten (structuur met ≥3 secties, placeholders gedocumenteerd, voorbeeld aanwezig).

### Kwaliteitsborging
- Template heeft YAML frontmatter met agent, template_naam, versie, output_type, doel
- Structuur-sectie toont volledige verwachte output met placeholders
- Placeholders-tabel documenteert alle variabelen met type en verplicht/optioneel
- Validatie-criteria lijst heeft minimaal 3 criteria
- Voorbeeld-output is concrete, realistische invulling van template
- Gebruiksinstructies bevatten 3-5 stappen voor agent die template gebruikt
- Versiebeheer-tabel start bij 1.0.0
- Bestand weggeschreven naar: artefacten/{vs}/{vs}.{fase}.{agent}/templates/{template-naam}.template.md

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Template definieert structuur, geen implementatie
  - Principe 4 (Scheiding van Wat en Hoe): Template = wat (structuur), niet hoe (generatie-logica)
  - Principe 5 (Evolutionaire Integriteit): Versioning ingebouwd (start 1.0.0), versiebeheer-tabel verplicht
  - Principe 7 (Transparante Verantwoording): Doel en gebruiksinstructies expliciet
  - Principe 9 (Output-formaat Normering): Template-documenten zijn Markdown
- **doctrine-templategebruik.md** (v1.0.0):
  - ook afwezigheid van een apart template wordt expliciet vastgelegd als `template: ~`
  - templatekeuze mag niet impliciet of alleen in vrije tekst verborgen blijven

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aeo
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: boundary_file, voorbeeldstructuur (indien opgegeven), referentie_templates (indien opgegeven)
- ✓ Aangemaakte bestanden: {template-naam}.template.md
- ✓ Geen gewijzigde bestanden (template is nieuw, of wordt geversioned bij update)
- ✓ Template-analyse: output-type bepaald, aantal secties, aantal placeholders, validatie-criteria gedefinieerd

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → capability-architect: voor boundary-verfijning of onduidelijke output-specificatie
- → domein-expert (indien beschikbaar): voor domein-specifieke structureisen (bijv. ArchiMate, wetenschappelijke publicatie)
- → agent-curator: voor validatie dat template consistent is met ecosysteem-patronen
- STOP: bij ontbrekende output-beschrijving in boundary, bij te complex of onduidelijk output_type

---

## Metadata

**Intent-ID**: `aeo.02.agent-ontwerper.definieer-agent-template`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**: 
- Vormingsfase: Vastlegging
- Betekeniseffect: Normerend
- Werking: Inhoudelijk
- Bron-houding: Canon-gebonden
