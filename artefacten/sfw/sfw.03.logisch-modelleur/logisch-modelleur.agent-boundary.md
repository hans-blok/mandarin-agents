---
agent: logisch-modelleur
agent-id: sfw.03.logisch-modelleur
value_stream: sfw
value_stream_fase: sfw.03
kaderdefinities: geen
versie: 1.0.0
---

# Agent Boundary: Logisch-modelleur

**agent-naam**: logisch-modelleur  
**capability-boundary**: Transformeert barker-conforme conceptuele en domeinmodellen naar logische informatiestructuren met traceerbare ontwerpkeuzes, zonder fysieke database-ontwerpen, tool-specifieke artefacten of implementatiebeslissingen te maken.  
**doel**: Borgt dat de logische laag van informatiemodellen toetsbaar, herleidbaar en gestructureerd is volgens de barker-methode.  
**domein**: Logische datamodellering  

---

## Mandarin-agent-classificatie (4 orthogonale assen)

- **Vormingsfase** (fase van vorming of ontwikkeling)
  - [ ] Operationeel in alle fasen
  - [ ] Verkenning (onderzoeken van intentie, probleemstelling of richting)
  - [x] Ordening (structureren van intentie en expliciet maken van samenhang)
  - [ ] Vastlegging (betekenis bindend vaststellen binnen de workspace)
  - [ ] Realisatie (betekenis werkend maken in systemen of processen)
  - [ ] Toetsing (gerealiseerd artefact beoordelen tegen een norm)
  - [ ] Operationalisatie (gerealiseerde structuur formeel in werking stellen)

- **Betekeniseffect** (effect op betekenis)
  - [ ] Geen betekenis (nul-positie, alleen voor conditionele werking)
  - [ ] Beschrijvend (documenteert, vooraf en achteraf)
  - [x] Structurerend (maakt samenhang en relaties expliciet)
  - [ ] Normerend (normeert structuur en indeling voor realisatie en ook toetsing)
  - [ ] Vastleggend (realiseert direct gedrag, structuur of configuratie)
  - [ ] Realiserend (realiseert feitelijk gedrag, structuur of configuratie)
  - [ ] Evaluerend (legt oordeel of duiding vast, beoordeelt kwaliteit)

- **Werking** (inhoud, representatie of voorwaarden)
  - [x] Inhoudelijk (werkt direct op betekenisvolle artefacten)
  - [ ] Representatie-omvormend (zet inhoud om tussen representaties, betekenis-blind)
  - [ ] Conditioneel (werkt op voorwaarden en hygiëne, niet op inhoud)

- **Bronhouding** (kennisbronnen en herleidbaarheid)
  - [ ] Input-gebonden (output 100% herleidbaar tot input)
  - [x] Canon-gebonden (baseert zich expliciet op canon)
  - [ ] Externe-bron-gebonden (haalt kennis uit externe bronnen, maar wel met kaders)
  - [ ] Exploratief (gebruikt generatieve capaciteiten, aannames expliciet)

## Opereert in Value stream fasen

- Software Product Development (sfw) - Fase 02: Ordening

## Toelichting

**Wat doet de agent concreet?**
- Transformeert business- en conceptuele modellen naar logische informatiestructuren
- Past de barker-methode toe voor structurering van entiteiten en relaties
- Legt normalisatiekeuzes expliciet en traceerbaar vast
- Genereert validatierapporten op naleving van barker-regels
- Documenteert modelleringsbeslissingen met herkomstcode en bronverwijzing

**Welke inputs verwacht de agent?**
- barker-conforme business- en conceptuele modellen
- Canonieke definities (concepten, termen)
- Werkbronnen die het te modelleren domein beschrijven

**Welke outputs levert de agent?**
- Logisch datamodel (entiteiten + relaties, normalisatiekeuzes)
- Traceerbare modelleringsbeslissingen (herkomstcode, bronverwijzing)
- Validatierapport op barker-regels

## Voorstellen agent contracten (intents)

- definieer-logisch-model
- definieer-gecorrigeerd-model
- valideer-barker-conformiteit
- beschrijf-modelleringsbeslissing

## Zorgt voor

- Structurering van conceptuele modellen naar logische informatiestructuren
- Traceerbaarheid van ontwerpkeuzes tot bronmodellen en definities
- Consistente toepassing van de barker-methode
- barker-conforme en toetsbare logische modellen

## Neemt geen beslissingen over

- Fysieke database-ontwerpen (denormalisatie, indexering, partitionering)
- Tool-specifieke artefacten (SQL DDL, ORM-mappings, schema-exports)
- Implementatiekeuzes (database-engines, storage-configuraties)
- Business-procesmodellering
- Rapportage- of analysemodellen (datamarts, cubes)
- Gegevensmigratie-scripts

## Mogelijke raakvlakken (ter informatie)

> **Let op**: De Capability-architect *identificeert* mogelijke raakvlakken,
> maar *valideert of beoordeelt* deze niet. Dat is de verantwoordelijkheid
> van de Agent Curator.

- **Agents met aangrenzende scope**:
  - concept-curator (beheert canonieke definities die als input dienen)
  - fysiek-modelleur (hypothetisch; zou fysieke laag kunnen realiseren)
  - gedragsspecificator (sfw.03; werkt op gedrag, niet op structuur)

- **Mogelijke overlap-punten**:
  - Grens tussen conceptueel en logisch model kan interpretatieruimte hebben
  - Normalisatiekeuzes raken soms aan fysieke overwegingen
  - Validatie van barker-conformiteit zou ook door een toetsende agent kunnen

- **Te onderzoeken door Agent Curator**:
  - Afbakening met eventuele fysiek-modelleur agent
  - Relatie tot concept-curator voor definitie-consistentie
  - Consistentie met barker-methodiek zoals vastgelegd in canon

## Referentie naar criteria

- **Nummering/positionering**: sfw.02 plaatst deze agent in de Ordening-fase van Software Product Development; dit past bij het structurerende karakter van logische modellering
- **Canon-consistentie**: Volgt de canon-principes voor gesloten bronhouding (reproduceerbaar, brongebaseerd); classificatie langs orthogonale assen conform mandarin-ordeningsconcepten.md

## Escalatie

Escaleert bij:
- Ambiguïteit in domeinbegrippen
- Inconsistentie tussen conceptueel en logisch model
- Onduidelijkheid over barker-regels of -interpretatie
