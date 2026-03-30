---
agent: agent-ontwerper
intent: definieer-agent-charter
versie: 1.0.0
---

# Agent-ontwerper — Definieer Agent Charter

## Rolbeschrijving (korte samenvatting)

De Agent-ontwerper creëert het agent-charter document dat identiteit, rol, grenzen, kerntaken en werkwijze van een agent integreert op basis van het agent-boundary document.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `agent-ontwerper.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- agent_naam: Naam van de agent waarvoor het charter wordt gedefinieerd (type: string, kebab-case).

**Optionele parameters**:
- boundary_file: Pad naar het agent-boundary document (type: string, default: automatisch afgeleid uit `agent_naam` en folder-structuur).

**Afgeleide informatie** (automatisch gedetecteerd):
- value_stream_fase: Gedetecteerd uit folder-patroon `artefacten/{vs}/{vs}.{fase}.{agent-naam}/`

**Afgeleide informatie** (geëxtraheerd uit boundary):
- capability_boundary: Externe verantwoordelijkheid in één zin
- classificatie: Vormingsfase, Betekeniseffect, Werking, Bronhouding
- intents: Vastgelegde contracten voor deze agent.
- domein: Primair kennisgebied van agent
- kaderdefinities: Lijst van kaderdefinitie-documenten waarop de agent zich baseert (canonieke paden uit boundary, bijv. `grondslagen/kaderdefinities/togaf.kaderdefinitie.md`). "geen" wanneer niet van toepassing.

### Output (wat komt eruit)

De Agent-ontwerper levert:
- **Agent-charter document** met volledige agent-identiteit:
  - YAML frontmatter: agent-ID, versie, domein, value stream, bronhouding, governance
  - Mandarin-agent-classificatie: 4 orthogonale assen met checkbox-selectie
  - Doel en bestaansreden: Waarom de agent bestaat
  - Capability boundary: Eén-zin definitie van verantwoordelijkheid
  - Rol en verantwoordelijkheid: Wat de agent doet binnen ecosysteem
  - Kerntaken: Lijst van primaire intents met beschrijving
  - Grenzen: Expliciete WEL/NIET secties
  - Werkwijze: Stappen en beslispunten per intent
  - Traceerbaarheid: Links naar contracten, templates, prompts
  - Output-locaties: Bestandspaden waar agent deliverables schrijft
  - Logging bij handmatige initialisatie: Audit-specificatie
  - Herkomstverantwoording: Bronnen, doctrine-versies, templates gebruikt
  - Change Log: Versiehistorie met datum, versie, wijziging, auteur
- Korte toelichting op ontwerpkeuzes en doctrine-naleving

**Deliverable bestand**: `artefacten/{vs}/{vs}.{fase}.{agent}/{agent}.charter.md`

**VERPLICHT**: Het bestand MOET worden weggeschreven naar de workspace (niet alleen voorgesteld).

**Outputformaat** (volgens agent-charter.template.md):
```markdown
---
agent: {agent-naam}
versie: 1.0.0
domein: {domein}
value_stream: {value-stream-naam}
governance: Volgt beleid-workspace.md en doctrine-agent-charter-normering.md
---

# Agent Charter - {agent-naam}

**Agent-ID**: `{vs}.{fase}.{agent-naam}`
**Versie**: 1.0.0
**Domein**: {domein}
**Value Stream**: {value-stream-naam} (fase {fase} - {fase-naam})
**Governance**: Volgt `beleid-workspace.md` en `doctrine-agent-charter-normering.md`

## Mandarin-agent-classificatie (4 orthogonale assen)
[checkboxes volgens boundary classificatie]

## 1. Doel en bestaansreden
[waarom agent bestaat]

## 2. Capability boundary
[één-zin definitie uit boundary]

## 3. Rol en verantwoordelijkheid
[wat agent doet, wat agent waarborgd]

## 4. Kerntaken
[lijst van intents met beschrijving]

## 5. Grenzen
### Wat de {agent} WEL doet
### Wat de {agent} NIET doet

## 6. Werkwijze
[stappen en canon-consultatie]

## 7. Traceerbaarheid (contract <-> charter)
[links naar contracten en templates]

## 8. Output-locaties
[bestandspaden voor deliverables]

## 9. Logging bij handmatige initialisatie
[audit-specificatie]

## 10. Herkomstverantwoording
[bronnen en doctrine-versies]

## 11. Change Log
[versiehistorie tabel]
```

**Formaat-normering**: 
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek
- Charter volgt strikte template-structuur uit agent-charter.template.md

### Foutafhandeling

De Agent-ontwerper:
- stopt wanneer boundary_file niet bestaat of niet te lezen is;
- stopt wanneer agent_naam of value_stream_fase ontbreekt of incorrect format heeft;
- stopt wanneer boundary geen classificatie-sectie of capability-boundary bevat;
- stopt wanneer boundary geen "Voorstellen agent contracten" (intents) sectie bevat;
- vraagt om verduidelijking wanneer classificatie-assen onduidelijk of inconsistent zijn;
- escaleert naar capability-architect voor boundary-verfijning bij ontbrekende essentiële informatie;
- escaleert naar constitutioneel-auteur voor doctrine-interpretatie bij classificatie-onduidelijkheden;
- STOP: bij onvoldoende informatie om volledig charter te genereren dat doctrine-compliant is.

**Charter is extern observeerbaar identiteitsdocument**: bevat GEEN implementatie-details, alleen wat agent doet, waar grenzen liggen en hoe governance werkt.

---

## Werkwijze

### Stappen
1. **Analyseer boundary**: Lees boundary_file en extraheer alle essentiële elementen (capability, classificatie, intents, domein).
2. **Raadpleeg template**: Lees agent-charter.template.md voor volledige structuur en verplichte secties.
3. **Raadpleeg doctrine**: Check doctrine-agent-charter-normering.md v2.1.0 voor principes en compliance-vereisten.
4. **Definieer doel**: Formuleer waarom agent bestaat op basis van capability boundary en domein.
5. **Expliciteer rol**: Beschrijf wat agent doet binnen ecosysteem, welke verantwoordelijkheden hij draagt.
6. **Detail kerntaken**: Lijst alle intents uit boundary met beschrijving per intent (1-2 zinnen).
7. **Stel grenzen**: Formuleer minimaal 5 WEL en 5 NIET bullets op basis van boundary en vergelijkbare agents.
8. **Beschrijf werkwijze**: Generieke stappen (canon-consultatie, input-validatie, verwerking, output-generatie, logging).
9. **Traceer artefacten**: Lijst alle intent-contracten, templates en prompt-bestanden (volgens conventie, ook als ze nog niet bestaan).
10. **Specificeer output-locaties**: Bepaal bestandspaden waar agent outputs wegschrijft (conform workspace-structuur).
11. **Documenteer logging**: Specificeer audit-logbestand format en locatie voor handmatige initialisatie.
12. **Leg herkomst vast**: Documenteer welke templates, doctrine-versies en bronnen gebruikt zijn.
13. **Initialiseer change log**: Start met versie 1.0.0 en "Initiële charter {agent-naam}" entry.
14. **Schrijf charter**: Genereer volledig charter-bestand en schrijf weg naar correct pad.
15. **Valideer compleetheid**: Check alle verplichte secties aanwezig, classificatie correct, doctrine-compliant.

### Kwaliteitsborging
- Charter heeft YAML frontmatter met agent, versie, domein, value_stream, governance
- Classificatie heeft exact 4 assen met correcte checkboxes (- [x] voor geselecteerd)
- Capability boundary past in één zin
- Kerntaken lijst bevat alle intents uit boundary
- Grenzen WEL/NIET hebben minimaal 5 bullets elk
- Traceerbaarheid verwijst naar alle intent-contracten (ook als deze nog gerealiseerd moeten worden)
- Output-locaties volgen workspace-structuur artefacten/{vs}/{vs}.{fase}.{agent}/
- Change log start bij versie 1.0.0
- Bestand weggeschreven naar correct pad: artefacten/{vs}/{vs}.{fase}.{agent}/{agent}.charter.md

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Charter definieert externe kenmerken, geen implementatie
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén capability boundary per agent
  - Principe 4 (Scheiding van Wat en Hoe): Charter = wat agent doet, contract = hoe wordt aangeroepen
  - Principe 5 (Evolutionaire Integriteit): Versioning ingebouwd (start 1.0.0), change log verplicht
  - Principe 7 (Transparante Verantwoording): Logging-sectie verplicht, herkomstverantwoording expliciet
  - Principe 9 (Output-formaat Normering): Markdown als default
- **mandarin-ordeningsconcepten.md**: Classificatie-assen en definities correct gebruiken

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aeo
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: boundary_file, template_file (agent-charter.template.md), doctrine-bestanden
- ✓ Aangemaakte bestanden: {agent}.charter.md
- ✓ Geen gewijzigde bestanden (charter is nieuw, of wordt geversioned bij update)
- ✓ Intent-analyse: aantal intents geïdentificeerd, classificatie-assen gebruikt

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → capability-architect: voor boundary-verfijning of onduidelijke capability-definitie
- → constitutioneel-auteur: voor doctrine-interpretatie bij classificatie-vragen
- → agent-curator: voor ecosysteem-validatie als agent overlap lijkt te hebben met bestaande agents
- STOP: bij ontbrekende boundary, bij te vage classificatie die niet te vertalen is naar charter

---

## Metadata

**Intent-ID**: `aeo.02.agent-ontwerper.definieer-agent-charter`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**: 
- Vormingsfase: Vastlegging
- Betekeniseffect: Normerend
- Werking: Inhoudelijk
- Bron-houding: Canon-gebonden
